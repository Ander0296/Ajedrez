"""
Cliente mínimo de la API pública de chess.com (solo lectura, sin dependencias).

Documentación oficial: https://www.chess.com/news/view/published-data-api

chess.com pide tres cosas a quien usa la API: pedidos en serie (nunca en
paralelo), un User-Agent que identifique la herramienta, y no volver a pedir
lo que ya se tiene. Por eso cada mes se guarda en datos/cache/: un mes
cerrado se baja una sola vez, y el mes en curso se refresca como mucho cada
10 minutos.
"""

import json
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

API = "https://api.chess.com/pub"
FRESCURA_MES_EN_CURSO = timedelta(minutes=10)
# Una partida que termina el último día del mes puede tardar en aparecer en
# el archivo: el mes se da por cerrado unas horas después de terminar.
MARGEN_CIERRE = timedelta(hours=6)


class ErrorChessCom(RuntimeError):
    pass


def mes_de_url(url):
    """'.../games/2025/11' -> (2025, 11)."""
    anio, mes = url.rstrip("/").split("/")[-2:]
    return int(anio), int(mes)


def fin_de_mes(anio, mes):
    siguiente = datetime(anio + (mes == 12), mes % 12 + 1, 1, tzinfo=timezone.utc)
    return siguiente + MARGEN_CIERRE


class ClienteChessCom:

    def __init__(self, usuario, agente, cache):
        if not usuario:
            raise ErrorChessCom(
                'Falta el usuario de chess.com en ajedrez.toml ([chesscom] usuario = "...").')
        self.usuario = usuario.lower()
        self.agente = agente
        self.cache = cache

    # ------------------------------------------------------------------
    #  RED
    # ------------------------------------------------------------------

    def _get(self, url, intentos=3):
        pedido = urllib.request.Request(
            url, headers={"User-Agent": self.agente, "Accept": "application/json"})
        for intento in range(intentos):
            try:
                with urllib.request.urlopen(pedido, timeout=30) as respuesta:
                    return json.load(respuesta)
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    raise ErrorChessCom(
                        f"chess.com no encuentra a «{self.usuario}» ({url}).") from e
                if e.code == 429 and intento < intentos - 1:
                    time.sleep(2 * (intento + 1))   # demasiados pedidos: esperar
                    continue
                raise ErrorChessCom(f"chess.com respondió {e.code} a {url}") from e
            except urllib.error.URLError as e:
                if intento < intentos - 1:
                    time.sleep(1 + intento)
                    continue
                raise ErrorChessCom(f"Sin conexión con chess.com: {e.reason}") from e
        raise ErrorChessCom(f"No pude leer {url}")

    def perfil(self):
        return self._get(f"{API}/player/{self.usuario}")

    def estadisticas(self):
        return self._get(f"{API}/player/{self.usuario}/stats")

    def meses(self):
        archivos = self._get(f"{API}/player/{self.usuario}/games/archives")["archives"]
        return [mes_de_url(u) for u in archivos]

    # ------------------------------------------------------------------
    #  PARTIDAS (con caché)
    # ------------------------------------------------------------------

    def _ruta(self, anio, mes):
        return self.cache / f"{self.usuario}-{anio:04d}-{mes:02d}.json"

    def _cache_valida(self, anio, mes, ahora):
        ruta = self._ruta(anio, mes)
        if not ruta.exists():
            return False
        escrito = datetime.fromtimestamp(ruta.stat().st_mtime, timezone.utc)
        return escrito >= fin_de_mes(anio, mes) or ahora - escrito < FRESCURA_MES_EN_CURSO

    def partidas_del_mes(self, anio, mes, refrescar=False, ahora=None):
        ahora = ahora or datetime.now(timezone.utc)
        ruta = self._ruta(anio, mes)
        if not refrescar and self._cache_valida(anio, mes, ahora):
            return json.loads(ruta.read_text(encoding="utf-8"))
        datos = self._get(f"{API}/player/{self.usuario}/games/{anio:04d}/{mes:02d}")["games"]
        self.cache.mkdir(parents=True, exist_ok=True)
        ruta.write_text(json.dumps(datos), encoding="utf-8")
        return datos

    def partidas(self, desde=None, refrescar=False):
        """Todas las partidas desde `desde` (datetime con zona), de la más vieja a la más nueva."""
        juegos = []
        for anio, mes in self.meses():
            if desde and (anio, mes) < (desde.year, desde.month):
                continue
            juegos += self.partidas_del_mes(anio, mes, refrescar)
        if desde:
            limite = desde.timestamp()
            juegos = [j for j in juegos if j.get("end_time", 0) >= limite]
        return sorted(juegos, key=lambda j: j.get("end_time", 0))
