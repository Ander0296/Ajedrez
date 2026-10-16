"""Inglés (SAN) <-> español. La R significa torre en inglés y rey en español."""

import chess
import pytest

from ajedrez.notacion import es_a_san, linea_desde, linea_es, san_a_es, tokens


@pytest.mark.parametrize("san, es", [
    ("Nxf7", "Cxf7"),
    ("Kxf7", "Rxf7"),      # rey
    ("Rxf7", "Txf7"),      # torre
    ("Qh5+", "Dh5+"),
    ("Bb5", "Ab5"),
    ("e8=Q#", "e8=D#"),
    ("O-O-O", "O-O-O"),
    ("exd5", "exd5"),
])
def test_ida_y_vuelta(san, es):
    assert san_a_es(san) == es
    assert es_a_san(es) == san


def test_es_a_san_acepta_ceros_y_anotaciones():
    assert es_a_san("0-0") == "O-O"
    assert es_a_san("0-0-0") == "O-O-O"
    assert es_a_san("Ca5!?") == "Na5"


def test_tokens_sin_numeros_de_jugada():
    assert tokens("4...d5 5.exd5 Ca5") == ["d5", "exd5", "Ca5"]
    assert tokens("1. e4 e5 2. Cf3 1-0") == ["e4", "e5", "Cf3"]


def test_linea_que_empieza_con_negras():
    assert linea_es(["d5", "exd5", "Na5"], numero=4, blancas=False) == "4...d5 5.exd5 Ca5"


def test_linea_desde_una_posicion():
    t = chess.Board("r1bqkb1r/pppp1ppp/2n2n2/4p1N1/2B1P3/8/PPPP1PPP/RNBQK2R b KQkq - 5 4")
    jugadas = [t.parse_san("d5")]
    assert linea_desde(t, jugadas) == "4...d5"
