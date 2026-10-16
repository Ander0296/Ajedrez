"""
Diagramas en texto y enlaces para abrir una posición en chess.com o lichess.

Se usan LETRAS y no las figuras Unicode (♔♚): en una terminal oscura las
figuras "blancas" se ven huecas y las "negras" rellenas, al revés de lo que
uno espera, y algunas fuentes dibujan el peón negro como emoji ancho y
rompen la alineación. Con letras no hay dudas: MAYÚSCULA = blancas.
"""

import urllib.parse

import chess

LETRA = {chess.KING: "R", chess.QUEEN: "D", chess.ROOK: "T",
         chess.BISHOP: "A", chess.KNIGHT: "C", chess.PAWN: "P"}

LEYENDA = ("MAYÚSCULAS = blancas · minúsculas = negras · "
           "R rey · D dama · T torre · A alfil · C caballo · P peón")


def texto(tablero, orientacion=chess.WHITE):
    """Diagrama con coordenadas, visto desde `orientacion`."""
    filas = range(7, -1, -1) if orientacion == chess.WHITE else range(8)
    columnas = range(8) if orientacion == chess.WHITE else range(7, -1, -1)
    lineas = ["   ┌─────────────────┐"]
    for fila in filas:
        celdas = []
        for columna in columnas:
            pieza = tablero.piece_at(chess.square(columna, fila))
            if pieza is None:
                celdas.append("·")
            else:
                letra = LETRA[pieza.piece_type]
                celdas.append(letra if pieza.color == chess.WHITE else letra.lower())
        lineas.append(f" {fila + 1} │ {' '.join(celdas)} │")
    lineas.append("   └─────────────────┘")
    lineas.append("     " + " ".join(chess.FILE_NAMES[c] for c in columnas))
    return "\n".join(lineas)


def turno(tablero):
    return "blancas" if tablero.turn == chess.WHITE else "negras"


def enlace_chesscom(fen):
    return "https://www.chess.com/analysis?fen=" + urllib.parse.quote(fen)


def enlace_lichess(fen, orientacion=chess.WHITE):
    url = "https://lichess.org/analysis/standard/" + fen.replace(" ", "_")
    return url + ("?color=black" if orientacion == chess.BLACK else "")
