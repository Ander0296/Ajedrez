"""
Estadísticas de un período: resultados, PROCESO y aperturas.

Lo usa /semana (últimos 7 días) y el diagnóstico (--todo). Las metas contra
las que se compara salen de ajedrez.toml [metas], que acompaña a la fase
actual de RUTA.md.
"""

from collections import Counter, defaultdict
from datetime import timedelta

import chess

from ajedrez import partidas as P
from ajedrez.notacion import linea_es


def _pct(n, total):
    return f"{100 * n / total:.0f}%" if total else "—"


def _seg(v):
    return "—" if v is None else f"{v:.1f}"


def calcular(lista):
    """Números del período. `lista` = Partidas ya filtradas, en orden cronológico."""
    vivas = [p for p in lista if p.base]                 # con reloj (no diarias)
    derrotas = [p for p in lista if p.resultado == "P"]
    victorias = [p for p in lista if p.resultado == "G"]
    derrotas_vivas = [p for p in derrotas if p.base]

    segundos = [s for p in vivas for s in P.segundos_por_jugada(p)]
    perdidas = {p.url: P.perdida_de_material(p) for p in derrotas}
    con_perdida = [p for p in derrotas if perdidas[p.url]]
    rendiciones = [p for p in derrotas if p.motivo == "resigned"]
    rendiciones_tempranas = [p for p in rendiciones if p.largo <= 20]
    mates = [p for p in derrotas if p.motivo == "checkmated"]

    por_dia = Counter(p.fin.astimezone().date() for p in lista if p.clase != "daily")
    racha = defaultdict(Counter)                          # resultado siguiente
    ordenadas = sorted(vivas, key=lambda p: p.fin)
    for a, b in zip(ordenadas, ordenadas[1:]):
        if b.fin - a.fin < timedelta(hours=1):
            racha[a.resultado][b.resultado] += 1

    return {
        "n": len(lista),
        "resultados": Counter(p.resultado for p in lista),
        "por_color": {c: Counter(p.resultado for p in lista if p.color == c)
                      for c in (chess.WHITE, chess.BLACK)},
        "por_clase": Counter(p.clase for p in lista),
        "por_control": Counter(p.control_legible for p in lista),
        "motivos_derrota": Counter(p.motivo for p in derrotas),
        "motivos_victoria": Counter(p.motivo for p in victorias),
        "largo_derrota": P.mediana([p.largo for p in derrotas]),
        "largo_victoria": P.mediana([p.largo for p in victorias]),
        "derrotas": len(derrotas),
        "derrotas_cortas": sum(p.largo <= 20 for p in derrotas),
        "segundos_mediana": P.mediana(segundos),
        "segundos_media": (sum(segundos) / len(segundos)) if segundos else None,
        "jugadas_rapidas": sum(s < 3 for s in segundos),
        "jugadas_medidas": len(segundos),
        "reloj_sin_usar_perdiendo": P.mediana([P.reloj_sin_usar(p) for p in derrotas_vivas]),
        "derrotas_con_media_hora": sum((P.reloj_sin_usar(p) or 0) > 0.5 for p in derrotas_vivas),
        "derrotas_vivas": len(derrotas_vivas),
        "con_perdida": len(con_perdida),
        "perdida_jugada": P.mediana([perdidas[p.url]["numero"] for p in con_perdida]),
        "perdida_hasta_15": sum(perdidas[p.url]["numero"] <= 15 for p in con_perdida),
        "perdida_pensado": P.mediana([perdidas[p.url]["pensado"] for p in con_perdida]),
        "rendiciones": len(rendiciones),
        "rendiciones_tempranas": len(rendiciones_tempranas),
        "material_al_rendirse": P.mediana([P.balance_final(p) for p in rendiciones_tempranas]),
        "rendido_sin_pieza_de_menos": sum(P.balance_final(p) > -3 for p in rendiciones),
        "mates": len(mates),
        "mates_cortos": sum(p.largo <= 20 for p in mates),
        "mates_con_material": sum(P.balance_final(p) >= 0 for p in mates),
        "abandonos": sum(p.motivo == "abandoned" for p in derrotas),
        "dias": len(por_dia),
        "dias_excedidos": por_dia,
        "max_dia": max(por_dia.items(), key=lambda kv: kv[1]) if por_dia else None,
        "racha": racha,
        "precision": {r: P.mediana([p.precision for p in lista if p.resultado == r])
                      for r in "GPT"},
        "revisadas": sum(p.precision is not None for p in lista),
        "rating": _rating(lista),
        "aperturas": _aperturas(lista),
    }


def _rating(lista):
    por_clase = defaultdict(list)
    for p in lista:
        por_clase[p.clase].append(p)
    resultado = {}
    for clase, ps in por_clase.items():
        ratings = [p.rating for p in ps]
        maximo = max(ps, key=lambda p: p.rating)
        resultado[clase] = {"inicio": ratings[0], "fin": ratings[-1], "min": min(ratings),
                            "max": maximo.rating, "max_fecha": maximo.fin.astimezone().date()}
    return resultado


def _aperturas(lista, plies=5, minimo=3):
    grupos = defaultdict(Counter)
    for p in lista:
        linea = tuple(P.linea_inicial(p, plies))
        if len(linea) == plies:
            grupos[(p.color, linea)][p.resultado] += 1
    filas = []
    for (color, linea), c in grupos.items():
        total = sum(c.values())
        if total >= minimo:
            filas.append((color, linea_es(list(linea)), total, c))
    return sorted(filas, key=lambda f: -f[2])


# ======================================================================
#  INFORME EN MARKDOWN
# ======================================================================

def _gpt(c):
    return f"{c['G']}-{c['P']}-{c['T']}"


def _motivos(c):
    return " · ".join(f"{P.MOTIVO.get(k, k)} {v}" for k, v in c.most_common()) or "—"


def informe(d, titulo, metas, estadisticas=None):
    L = [f"## {titulo}", ""]
    if estadisticas:
        L += [_ratings_hoy(estadisticas), ""]
    if not d["n"]:
        return "\n".join(L + ["Sin partidas en el período."])

    r = d["resultados"]
    L.append(f"Partidas: {d['n']} · {r['G']} G · {r['P']} P · {r['T']} T · "
             f"blancas {_gpt(d['por_color'][chess.WHITE])} · negras {_gpt(d['por_color'][chess.BLACK])} "
             f"(G-P-T) · controles: " + ", ".join(f"{k} ×{v}" for k, v in d["por_control"].most_common()))
    for clase, x in d["rating"].items():
        if d["por_clase"][clase] < 3:      # 1 blitz suelto o diarias sin valorar: ruido
            continue
        L.append(f"Rating {clase}: {x['inicio']} → {x['fin']} (mín. {x['min']}, "
                 f"máx. {x['max']} el {x['max_fecha']})")
    L.append("")

    m = metas or {}
    medidas = d["jugadas_medidas"]
    max_dia = d["max_dia"]
    excedidos = sum(v > m.get("partidas_por_dia", 2) for v in d["dias_excedidos"].values())
    sin_usar = d["reloj_sin_usar_perdiendo"]
    sin_usar = "—" if sin_usar is None else f"{100 * sin_usar:.0f}%"
    L += ["### Proceso (lo que más pesa a tu nivel)", "",
          "| Indicador | Valor | Meta de la fase |", "| --- | --- | --- |",
          f"| segundos por jugada (mediana, desde la 6ª) | {_seg(d['segundos_mediana'])} "
          f"(media {_seg(d['segundos_media'])}) | ≥ {m.get('segundos_por_jugada', '—')} |",
          f"| jugadas hechas en < 3 s (desde la 6ª) | {_pct(d['jugadas_rapidas'], medidas)} "
          f"({d['jugadas_rapidas']}/{medidas}) | ≤ {m.get('jugadas_en_menos_de_3s', '—')}% |",
          f"| reloj sin usar al perder (mediana) | {sin_usar} "
          f"| ≤ {m.get('reloj_sin_usar_al_perder', '—')}% |",
          f"| derrotas con más de la mitad del reloj sin usar | "
          f"{d['derrotas_con_media_hora']}/{d['derrotas_vivas']} | — |",
          f"| derrotas en ≤ 20 jugadas | {_pct(d['derrotas_cortas'], d['derrotas'])} "
          f"({d['derrotas_cortas']}/{d['derrotas']}) | ≤ {m.get('derrotas_cortas', '—')}% |",
          f"| rendiciones antes de la jugada 20 | {d['rendiciones_tempranas']} | "
          f"{m.get('rendiciones_tempranas', '—')} |",
          f"| días con más de {m.get('partidas_por_dia', 2)} partidas | {excedidos} de {d['dias']} "
          f"(máx. {max_dia[1]} el {max_dia[0]}) | 0 |" if max_dia else "| días | — | — |",
          ""]

    L += ["### Material y finales de partida", "",
          f"- Derrotas con pérdida de material (≥ 2 puntos) que no se recuperó: "
          f"{d['con_perdida']}/{d['derrotas']} ({_pct(d['con_perdida'], d['derrotas'])}). "
          f"Jugada mediana: {d['perdida_jugada'] or '—'} · hasta la jugada 15: {d['perdida_hasta_15']} · "
          f"segundos pensados en la jugada que lo permitió (aprox.): {_seg(d['perdida_pensado'])}",
          f"- Duración mediana: derrotas {d['largo_derrota'] or '—'} jugadas · "
          f"victorias {d['largo_victoria'] or '—'} jugadas",
          f"- Rendiciones: {d['rendiciones']} · antes de la jugada 20: {d['rendiciones_tempranas']} "
          f"(material mediano al rendirte: {d['material_al_rendirse'] if d['material_al_rendirse'] is not None else '—'}) · "
          f"con menos de una pieza de desventaja: {d['rendido_sin_pieza_de_menos']}",
          f"- Mates recibidos: {d['mates']} · en ≤ 20 jugadas: {d['mates_cortos']} · "
          f"con material igual o a favor: {d['mates_con_material']}",
          f"- Abandonos (te fuiste de la partida): {d['abandonos']}",
          f"- Cómo perdés: {_motivos(d['motivos_derrota'])}",
          f"- Cómo ganás (lo que hizo el rival): {_motivos(d['motivos_victoria'])}",
          ""]

    if d["revisadas"]:
        pr = d["precision"]
        L.append(f"Precisión de chess.com ({d['revisadas']} partidas revisadas, mediana): "
                 f"victorias {_seg(pr['G'])} · derrotas {_seg(pr['P'])}")
    if d["racha"]:
        tras = []
        for previo, nombre in (("G", "ganar"), ("P", "perder")):
            c = d["racha"].get(previo)
            if c:
                tras.append(f"después de {nombre}: {_pct(c['G'], sum(c.values()))} de victorias "
                            f"({sum(c.values())} partidas)")
        L.append("Partida siguiente (jugada en menos de 1 hora) — " + " · ".join(tras))
    L.append("")

    if d["aperturas"]:
        L += ["### Aperturas (primeras 5 medias jugadas, ≥ 3 partidas)", "",
              "| Yo con | Línea | Partidas | G-P-T | |", "| --- | --- | --- | --- | --- |"]
        for color, linea, total, c in d["aperturas"][:14]:
            alerta = "⚠" if total >= 5 and c["G"] / total <= 0.35 else ""
            L.append(f"| {'blancas' if color == chess.WHITE else 'negras'} | {linea} | {total} "
                     f"| {_gpt(c)} | {alerta} |")
        L.append("")
    return "\n".join(L)


def _ratings_hoy(e):
    partes = []
    for clave, nombre in (("chess_rapid", "rápidas"), ("chess_blitz", "blitz"),
                          ("chess_bullet", "bullet"), ("chess_daily", "diarias")):
        x = e.get(clave)
        if x and "last" in x:
            mejor = x.get("best", {}).get("rating")
            rec = x.get("record", {})
            partes.append(f"{nombre} {x['last']['rating']}"
                          + (f" (máx. {mejor})" if mejor else "")
                          + f" [{rec.get('win', 0)}-{rec.get('loss', 0)}-{rec.get('draw', 0)}]")
    t = e.get("tactics", {})
    if t:
        partes.append(f"problemas: máx. {t.get('highest', {}).get('rating', '—')} "
                      f"(el rating actual de problemas no sale en la API: miralo en tu perfil)")
    pr = e.get("puzzle_rush", {}).get("best", {})
    if pr:
        partes.append(f"Puzzle Rush récord {pr.get('score')}")
    return "Ratings hoy: " + " · ".join(partes)
