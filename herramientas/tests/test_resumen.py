"""Estadísticas de un período e informe en Markdown."""

from ajedrez import partidas as P
from ajedrez import resumen as R
from conftest import YO


def test_calcular_y_mostrar(derrota, victoria, diaria):
    lista = P.estandar([derrota, victoria, diaria], YO)
    d = R.calcular(lista)
    assert d["n"] == 3
    assert (d["resultados"]["G"], d["resultados"]["P"], d["resultados"]["T"]) == (1, 1, 1)
    assert d["derrotas_cortas"] == 1
    assert d["rendiciones_tempranas"] == 1
    assert d["con_perdida"] == 1
    texto = R.informe(d, "prueba", {"segundos_por_jugada": 15})
    assert "### Proceso" in texto
    assert "≥ 15" in texto


def test_sin_partidas():
    assert "Sin partidas" in R.informe(R.calcular([]), "vacío", {})
