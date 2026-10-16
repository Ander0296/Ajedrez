"""Clasificación de errores y, si Stockfish está instalado, el análisis real."""

import shutil

import chess
import pytest

from ajedrez import config as C
from ajedrez import motor as M
from ajedrez import partidas as P
from conftest import YO

hay_stockfish = pytest.mark.skipif(shutil.which("stockfish") is None,
                                   reason="Stockfish no instalado (yay -S stockfish)")


def test_chances_es_simetrica_y_acotada():
    assert M.chances(0) == 0
    assert M.chances(300) == pytest.approx(-M.chances(-300))
    assert 0.49 < M.chances(300) < 0.51
    assert M.chances(M.MATE) == pytest.approx(1)


@pytest.mark.parametrize("caida, esperado", [
    (0.35, "error grave"), (0.25, "error"), (0.15, "imprecisión"), (0.05, None)])
def test_umbrales_de_lichess(caida, esperado):
    assert M.clasificar(caida) == esperado


def test_fase():
    assert M.fase(chess.Board()) == "apertura"
    assert M.fase(chess.Board("8/5k2/8/8/8/8/3R1K2/8 w - - 0 40")) == "final"


@hay_stockfish
def test_cg5_se_contesta_con_d5(repo):
    cfg = C.cargar()
    t = chess.Board("r1bqkb1r/pppp1ppp/2n2n2/4p1N1/2B1P3/8/PPPP1PPP/RNBQK2R b KQkq - 5 4")
    with M.abrir(cfg) as motor:
        mejor = M.evaluar(motor, t, 16)[0]
    assert t.san(mejor.pv[0]) == "d5"


@hay_stockfish
def test_momentos_encuentra_el_error_de_f7(repo, derrota):
    cfg = C.cargar()
    p = P.desde_api(derrota, YO)
    with M.abrir(cfg) as motor:
        momentos = M.momentos(p, M.evaluar_partida(motor, p, 12))
    primero = momentos[0]
    assert (primero["numero"], primero["tipo"]) == (4, "error grave")
    assert primero["tablero"].san(primero["jugada"]) == "d6"
