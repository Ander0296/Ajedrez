"""Lectura de partidas de chess.com y métricas de proceso (sin red, sin motor)."""

import chess
import pytest

from ajedrez import partidas as P
from conftest import YO


@pytest.mark.parametrize("url, esperado", [
    ("https://www.chess.com/openings/Italian-Game-Two-Knights-Defense-4.Ng5-d6",
     "Italian Game Two Knights Defense"),
    ("https://www.chess.com/openings/Scandinavian-Defense-Mieses-Kotrc-Variation",
     "Scandinavian Defense Mieses Kotrc Variation"),
    ("", "?"),
])
def test_nombre_de_apertura_sin_las_jugadas(url, esperado):
    assert P.nombre_apertura(url) == esperado


def test_derrota_desde_mi_lado(derrota):
    p = P.desde_api(derrota, YO)
    assert (p.color, p.resultado, p.motivo) == (chess.BLACK, "P", "resigned")
    assert (p.rival, p.rating, p.rating_rival) == ("rival1", 750, 760)
    assert (p.base, p.incremento, p.control_legible) == (600, 0, "10|0")
    assert p.largo == 8
    assert p.apertura == "Italian Game Two Knights Defense"


def test_el_usuario_no_distingue_mayusculas(derrota):
    assert P.desde_api(derrota, "YO_TEST").color == chess.BLACK


def test_segundos_por_jugada_solo_las_mias_desde_la_sexta(derrota):
    # 6...Ae6 se jugó de 9:40 a 9:20 y 7...Dxe6 de 9:20 a 9:00
    assert P.segundos_por_jugada(P.desde_api(derrota, YO)) == [20.0, 20.0]


def test_el_incremento_se_suma_al_tiempo_pensado(victoria):
    p = P.desde_api(victoria, YO)
    # 3.Dh5: el reloj pasó de 10:02 a 9:57 con +5 de incremento -> pensó 10 s
    tercera = p.jugadas()[4]
    assert (tercera.san, tercera.pensado) == ("Qh5", 10.0)
    assert (p.resultado, p.motivo, p.control_legible) == ("G", "checkmated", "10|5")


def test_reloj_sin_usar(derrota):
    assert P.reloj_sin_usar(P.desde_api(derrota, YO)) == pytest.approx(0.9)


def test_perdida_de_material_atribuida_a_la_jugada_anterior_a_la_captura(derrota):
    # 4...d6?? permite 5.Cxf7 (horquilla a dama y torre). Sin motor, la pérdida
    # se ve recién con 6.Cxh8, y se atribuye a 5...De7: es una aproximación.
    perdida = P.perdida_de_material(P.desde_api(derrota, YO))
    assert perdida == {"numero": 5, "jugada": "Qe7", "pensado": 13.0, "puntos": 5}


def test_un_cambio_normal_no_es_perdida(victoria):
    assert P.perdida_de_material(P.desde_api(victoria, YO)) is None


def test_balance_final_desde_mi_color(derrota):
    assert P.balance_final(P.desde_api(derrota, YO)) == -6


def test_diaria_sin_reloj(diaria):
    p = P.desde_api(diaria, YO)
    assert (p.base, p.control_legible, p.resultado) == (None, "diaria", "T")
    assert P.segundos_por_jugada(p) == []
    assert P.reloj_sin_usar(p) is None


def test_estandar_descarta_variantes(derrota, victoria):
    victoria["rules"] = "chess960"
    assert [p.url for p in P.estandar([derrota, victoria], YO)] == [derrota["url"]]
