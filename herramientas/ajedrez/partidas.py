"""
Lectura de las partidas que devuelve la API de chess.com.

Este módulo trabaja SIN red y SIN motor (es lo que cubren los tests). Mide
el PROCESO: cuánto pensaste cada jugada, cuándo perdiste material, cómo
terminó la partida. Hasta ~1500 el proceso explica más derrotas que el
conocimiento, y además se puede medir en cientos de partidas en segundos.
"""

import io
import statistics
from dataclasses import dataclass, field
from datetime import datetime, timezone

import chess
import chess.pgn

VALOR = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
         chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0}

# Códigos de "result" de chess.com (white.result / black.result).
TABLAS = {"agreed", "repetition", "stalemate", "insufficient", "50move",
          "timevsinsufficient"}
MOTIVO = {
    "checkmated": "mate",
    "resigned": "rendición",
    "timeout": "tiempo",
    "abandoned": "abandonó (se fue)",
    "agreed": "acuerdo",
    "repetition": "repetición",
    "stalemate": "ahogado",
    "insufficient": "material insuficiente",
    "50move": "regla de 50 jugadas",
    "timevsinsufficient": "tiempo vs. material insuficiente",
}


@dataclass
class Jugada:
    ply: int                 # 1 = primera jugada de las blancas
    numero: int              # número de jugada: 1, 1, 2, 2...
    color: bool              # quién la hizo
    san: str
    pensado: float | None    # segundos que se usaron en ESTA jugada
    reloj: float | None      # reloj que quedó después de hacerla
    material: int            # balance de material después, visto desde MI color
    fen_antes: str


@dataclass
class Partida:
    url: str
    fin: datetime
    color: bool              # con qué color jugué yo
    rating: int              # mi rating al terminar
    rival: str
    rating_rival: int
    resultado: str           # "G" gané · "P" perdí · "T" tablas
    motivo: str              # código de chess.com (resigned, checkmated...)
    clase: str               # rapid, blitz, bullet, daily
    control: str             # "600", "600+5", "1/259200"
    pgn: str
    apertura: str
    precision: float | None = None
    _juego: object = field(default=None, repr=False)
    _jugadas: list = field(default=None, repr=False)

    @property
    def id(self):
        return self.url.rstrip("/").rsplit("/", 1)[-1]

    @property
    def base(self):
        """Segundos iniciales del reloj; None en partidas diarias."""
        if not self.control or "/" in self.control or not self.control[0].isdigit():
            return None
        return int(self.control.split("+")[0])

    @property
    def incremento(self):
        return int(self.control.split("+")[1]) if "+" in self.control else 0

    @property
    def control_legible(self):
        if self.base is None:
            return "diaria"
        return f"{self.base // 60}|{self.incremento}"

    @property
    def color_texto(self):
        return "blancas" if self.color == chess.WHITE else "negras"

    def juego(self):
        if self._juego is None:
            self._juego = chess.pgn.read_game(io.StringIO(self.pgn))
        return self._juego

    def jugadas(self):
        if self._jugadas is None:
            self._jugadas = _leer_jugadas(self)
        return self._jugadas

    def mias(self):
        return [j for j in self.jugadas() if j.color == self.color]

    @property
    def largo(self):
        """Cantidad de jugadas (de cada bando) que duró la partida."""
        js = self.jugadas()
        return js[-1].numero if js else 0


# ======================================================================
#  CONSTRUCCIÓN
# ======================================================================

def nombre_apertura(eco_url):
    """'.../openings/Italian-Game-Two-Knights-Defense-4.Ng5-d5' -> 'Italian Game Two Knights Defense'."""
    if not eco_url:
        return "?"
    nombre = []
    for parte in eco_url.rstrip("/").rsplit("/", 1)[-1].split("-"):
        if parte[:1].isdigit():
            break
        nombre.append(parte)
    return " ".join(nombre) or "?"


def desde_api(j, usuario):
    usuario = usuario.lower()
    soy_blancas = j["white"]["username"].lower() == usuario
    yo, otro = (j["white"], j["black"]) if soy_blancas else (j["black"], j["white"])
    if yo["result"] == "win":
        resultado, motivo = "G", otro["result"]
    elif yo["result"] in TABLAS:
        resultado, motivo = "T", yo["result"]
    else:
        resultado, motivo = "P", yo["result"]
    precision = (j.get("accuracies") or {}).get("white" if soy_blancas else "black")
    return Partida(
        url=j.get("url", ""),
        fin=datetime.fromtimestamp(j.get("end_time", 0), timezone.utc),
        color=chess.WHITE if soy_blancas else chess.BLACK,
        rating=yo.get("rating", 0),
        rival=otro.get("username", "?"),
        rating_rival=otro.get("rating", 0),
        resultado=resultado,
        motivo=motivo,
        clase=j.get("time_class", ""),
        control=j.get("time_control", ""),
        pgn=j.get("pgn", ""),
        apertura=nombre_apertura(j.get("eco", "")),
        precision=precision,
    )


def estandar(juegos, usuario):
    """Solo ajedrez normal (sin variantes) y con PGN."""
    return [desde_api(j, usuario) for j in juegos
            if j.get("rules", "chess") == "chess" and j.get("pgn")]


def material(tablero, color):
    total = 0
    for pieza in tablero.piece_map().values():
        total += VALOR[pieza.piece_type] * (1 if pieza.color == color else -1)
    return total


def _leer_jugadas(p):
    juego = p.juego()
    tablero = juego.board()
    reloj = {chess.WHITE: p.base, chess.BLACK: p.base}
    jugadas = []
    for ply, nodo in enumerate(juego.mainline(), start=1):
        color, numero, fen = tablero.turn, tablero.fullmove_number, tablero.fen()
        san = tablero.san(nodo.move)
        tablero.push(nodo.move)
        quedo, pensado = nodo.clock(), None
        if quedo is not None and reloj[color] is not None:
            # %clk es el reloj DESPUÉS de jugar, ya con el incremento sumado.
            pensado = max(0.0, reloj[color] - quedo + p.incremento)
            reloj[color] = quedo
        jugadas.append(Jugada(ply, numero, color, san, pensado, quedo,
                              material(tablero, p.color), fen))
    return jugadas


# ======================================================================
#  MÉTRICAS DE PROCESO (una partida)
# ======================================================================

def segundos_por_jugada(p, desde=6):
    """Segundos que pensé cada una de MIS jugadas a partir de la jugada `desde`.

    Las primeras jugadas salen de memoria y se juegan rápido a propósito: no
    dicen nada del proceso, por eso se excluyen.
    """
    return [j.pensado for j in p.mias() if j.numero >= desde and j.pensado is not None]


def reloj_sin_usar(p):
    """Fracción (0-1) de mi tiempo inicial que quedaba al terminar. None sin reloj."""
    mias = [j for j in p.mias() if j.reloj is not None]
    if not mias or not p.base:
        return None
    return min(1.0, mias[-1].reloj / p.base)


def balance_final(p):
    js = p.jugadas()
    return js[-1].material if js else 0


def perdida_de_material(p, umbral=2, ventana=4):
    """Primera pérdida de material que NO se recupera enseguida.

    Se mira el balance "después de la respuesta del rival" (el mínimo entre
    una jugada y la siguiente): así un cambio normal (yo capturo, él
    recaptura) no cuenta como pérdida. Hay pérdida cuando ese balance cae
    `umbral` puntos o más y se queda abajo durante `ventana` medias jugadas.

    Es una aproximación sin motor: atribuye la pérdida a mi última jugada
    antes de que cayera el material, que no siempre es la jugada culpable
    (a veces el error fue una o dos jugadas antes). Para el culpable exacto
    está `ajedrez partida --motor`.
    """
    js = p.jugadas()
    if not js:
        return None
    inicial = material(p.juego().board(), p.color)
    b = [inicial] + [j.material for j in js]
    s = [min(b[k], b[k + 1]) for k in range(len(b) - 1)] + [b[-1]]
    for k in range(1, len(s)):
        tramo = s[k:k + ventana]
        if max(tramo) <= s[k - 1] - umbral:
            mias = [j for j in js[:k + 1] if j.color == p.color]
            culpable = mias[-1] if mias else None
            return {
                "numero": culpable.numero if culpable else js[k - 1].numero,
                "jugada": culpable.san if culpable else None,
                "pensado": culpable.pensado if culpable else None,
                "puntos": s[k - 1] - max(tramo),
            }
    return None


def linea_inicial(p, plies):
    return [j.san for j in p.jugadas()[:plies]]


def mediana(valores):
    valores = [v for v in valores if v is not None]
    return statistics.median(valores) if valores else None
