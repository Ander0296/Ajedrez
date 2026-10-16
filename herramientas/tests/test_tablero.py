"""Diagramas en texto: MAYÚSCULA = blancas, y la orientación correcta."""

import chess

from ajedrez import tablero as T


def test_inicial_desde_las_blancas():
    lineas = T.texto(chess.Board()).splitlines()
    assert lineas[1] == " 8 │ t c a d r a c t │"
    assert lineas[8] == " 1 │ T C A D R A C T │"
    assert lineas[-1].split() == list("abcdefgh")


def test_inicial_desde_las_negras():
    lineas = T.texto(chess.Board(), chess.BLACK).splitlines()
    assert lineas[1] == " 1 │ T C A R D A C T │"     # h1 a la izquierda
    assert lineas[-1].split() == list("hgfedcba")


def test_enlaces():
    fen = chess.Board().fen()
    assert T.enlace_chesscom(fen).startswith("https://www.chess.com/analysis?fen=rnbqkbnr/")
    assert " " not in T.enlace_chesscom(fen)
    assert T.enlace_lichess(fen, chess.BLACK).endswith("_w_KQkq_-_0_1?color=black")


def test_enlace_resolver_juega_el_bando_que_mueve():
    blancas = T.enlace_resolver(chess.Board().fen())
    assert blancas.startswith("https://www.chess.com/practice/custom?color=white&fen=rnbqkbnr/")
    assert blancas.endswith("&is960=false&moveList=")
    assert " " not in blancas
    negras = chess.Board()
    negras.push_san("e4")
    assert "?color=black&" in T.enlace_resolver(negras.fen())
