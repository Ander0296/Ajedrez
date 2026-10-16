"""
Partidas de prueba con el formato EXACTO de la API de chess.com.

Son inventadas (rivales ficticios) pero reproducen los casos reales que
importan: la derrota rápida por no defender f7, una victoria con incremento
y una diaria sin reloj.
"""

import pytest

YO = "yo_test"

PGN_DERROTA = """[Event "Live Chess"]
[Site "Chess.com"]
[White "rival1"]
[Black "yo_test"]
[Result "1-0"]
[TimeControl "600"]
[Termination "rival1 won by resignation"]

1. e4 {[%clk 0:10:00]} 1... e5 {[%clk 0:09:59]} 2. Nf3 {[%clk 0:09:58]} 2... Nc6 {[%clk 0:09:57]}
3. Bc4 {[%clk 0:09:56]} 3... Nf6 {[%clk 0:09:55]} 4. Ng5 {[%clk 0:09:50]} 4... d6 {[%clk 0:09:53]}
5. Nxf7 {[%clk 0:09:45]} 5... Qe7 {[%clk 0:09:40]} 6. Nxh8 {[%clk 0:09:40]} 6... Be6 {[%clk 0:09:20]}
7. Bxe6 {[%clk 0:09:35]} 7... Qxe6 {[%clk 0:09:00]} 8. d3 {[%clk 0:09:30]} 1-0
"""

PGN_VICTORIA = """[Event "Live Chess"]
[Site "Chess.com"]
[White "yo_test"]
[Black "rival2"]
[Result "1-0"]
[TimeControl "600+5"]

1. e4 {[%clk 0:10:00]} 1... e5 {[%clk 0:10:00]} 2. Bc4 {[%clk 0:10:02]} 2... Nc6 {[%clk 0:10:03]}
3. Qh5 {[%clk 0:09:57]} 3... Nf6 {[%clk 0:09:50]} 4. Qxf7# {[%clk 0:09:55]} 1-0
"""

PGN_DIARIA = """[Event "Let's Play"]
[Site "Chess.com"]
[White "yo_test"]
[Black "rival3"]
[Result "1/2-1/2"]
[TimeControl "1/259200"]

1. d4 d5 2. c4 e6 1/2-1/2
"""


def _juego(url, pgn, control, clase, blanco, negro, fin, eco=""):
    return {"url": url, "pgn": pgn, "time_control": control, "end_time": fin,
            "rated": True, "time_class": clase, "rules": "chess",
            "white": blanco, "black": negro, "eco": eco}


@pytest.fixture
def derrota():
    return _juego("https://www.chess.com/game/live/111", PGN_DERROTA, "600", "rapid",
                  {"rating": 760, "result": "win", "username": "rival1"},
                  {"rating": 750, "result": "resigned", "username": YO},
                  1790000000,
                  "https://www.chess.com/openings/Italian-Game-Two-Knights-Defense-4.Ng5-d6")


@pytest.fixture
def victoria():
    return _juego("https://www.chess.com/game/live/222", PGN_VICTORIA, "600+5", "rapid",
                  {"rating": 758, "result": "win", "username": YO},
                  {"rating": 740, "result": "checkmated", "username": "rival2"},
                  1790003600)


@pytest.fixture
def diaria():
    return _juego("https://www.chess.com/game/daily/333", PGN_DIARIA, "1/259200", "daily",
                  {"rating": 800, "result": "agreed", "username": YO},
                  {"rating": 810, "result": "agreed", "username": "rival3"},
                  1790090000)


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """Un repo mínimo con ajedrez.toml, para correr la CLI sin tocar el real."""
    (tmp_path / "ajedrez.toml").write_text(
        '[chesscom]\nusuario = "yo_test"\n[motor]\nprofundidad_posicion = 10\n', encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    return tmp_path
