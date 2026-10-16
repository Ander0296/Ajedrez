"""
Notación algebraica: la inglesa (SAN, la que usan chess.com, los PGN y
python-chess) y la española (la del libro de Illescas).

    inglés   K  Q  R  B  N        Kxf7 = el REY captura en f7
    español  R  D  T  A  C        Rxf7 = el REY captura en f7

La trampa: la R existe en las dos y significa cosas distintas (rook = torre
en inglés, rey en español). Por eso la traducción se hace de una sola vez
con una tabla, nunca letra por letra con reemplazos encadenados.
"""

import re

_A_ESPANOL = str.maketrans("KQRBN", "RDTAC")
_A_INGLES = str.maketrans("RDTAC", "KQRBN")
_NUMERO = re.compile(r"^\d+\.+")


def san_a_es(san):
    return san.translate(_A_ESPANOL)


def es_a_san(jugada):
    """'Cxf7+' -> 'Nxf7+'. Acepta 0-0 con ceros y quita !? de anotación."""
    j = jugada.strip().rstrip("!?")
    j = j.replace("0-0-0", "O-O-O").replace("0-0", "O-O")
    return j.translate(_A_INGLES)


def tokens(linea):
    """'4...d5 5.exd5 Ca5' -> ['d5', 'exd5', 'Ca5'] (sin números de jugada)."""
    resultado = []
    for t in linea.replace(",", " ").split():
        t = _NUMERO.sub("", t)
        if t and t not in ("...", "1-0", "0-1", "1/2-1/2", "*"):
            resultado.append(t)
    return resultado


def linea_es(sans, numero=1, blancas=True):
    """Lista de SAN -> '4...d5 5.exd5 Ca5', empezando en la jugada `numero`."""
    partes = []
    for i, san in enumerate(sans):
        es = san_a_es(san)
        if blancas:
            partes.append(f"{numero}.{es}")
        elif i == 0:
            partes.append(f"{numero}...{es}")
        else:
            partes.append(es)
        if not blancas:
            numero += 1
        blancas = not blancas
    return " ".join(partes)


def linea_desde(tablero, jugadas):
    """Línea en español a partir de una posición y una lista de chess.Move."""
    copia = tablero.copy(stack=False)
    sans = []
    for j in jugadas:
        sans.append(copia.san(j))
        copia.push(j)
    return linea_es(sans, tablero.fullmove_number, tablero.turn)


def jugada_es(tablero, jugada):
    """Una sola jugada con su número: '4...d5' o '5.exd5'."""
    return linea_es([tablero.san(jugada)], tablero.fullmove_number, tablero.turn)
