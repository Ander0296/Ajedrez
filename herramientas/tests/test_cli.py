"""La CLI de punta a punta, sin red (posicion no usa chess.com)."""

from ajedrez.cli import main

FEN_CG5 = "r1bqkb1r/pppp1ppp/2n2n2/4p1N1/2B1P3/8/PPPP1PPP/RNBQK2R b KQkq - 5 4"


def test_posicion_sin_motor(repo, capsys):
    assert main(["posicion", FEN_CG5, "--sin-motor", "--orientacion", "blancas"]) == 0
    salida = capsys.readouterr().out
    assert "Juegan: negras" in salida
    assert " 5 │ · · · · p · C · │" in salida
    assert "chess.com/analysis?fen=" in salida


def test_linea_propuesta_legal_en_espanol(repo, capsys):
    assert main(["posicion", FEN_CG5, "--sin-motor", "--linea", "4...d5 5.exd5 Ca5"]) == 0
    assert "4...d5 5.exd5 Ca5" in capsys.readouterr().out


def test_jugada_ilegal_avisa_cual(repo, capsys):
    assert main(["posicion", FEN_CG5, "--sin-motor", "--linea", "4...Dxg5"]) == 1
    assert "«Dxg5» no es una jugada legal" in capsys.readouterr().err


def test_fen_invalido(repo, capsys):
    assert main(["posicion", "esto no es un fen", "--sin-motor"]) == 1
    assert "FEN inválido" in capsys.readouterr().err
