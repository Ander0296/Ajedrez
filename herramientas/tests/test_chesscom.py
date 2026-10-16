"""Caché de la API: un mes cerrado se baja una vez; el mes en curso, cada 10 minutos."""

import os
from datetime import datetime, timezone

import pytest

from ajedrez.chesscom import ClienteChessCom, ErrorChessCom, mes_de_url


def test_mes_de_url():
    assert mes_de_url("https://api.chess.com/pub/player/x/games/2025/11") == (2025, 11)


def test_sin_usuario_avisa_claro(tmp_path):
    with pytest.raises(ErrorChessCom, match="ajedrez.toml"):
        ClienteChessCom("", "agente", tmp_path)


@pytest.fixture
def cliente(tmp_path, monkeypatch):
    c = ClienteChessCom("yo_test", "agente-de-prueba", tmp_path)
    c.pedidos = 0

    def falso_get(url, intentos=3):
        c.pedidos += 1
        return {"games": [{"url": url, "end_time": 1}]}

    monkeypatch.setattr(c, "_get", falso_get)
    return c


def test_mes_cerrado_no_se_vuelve_a_pedir(cliente):
    ahora = datetime(2026, 10, 15, tzinfo=timezone.utc)
    cliente.partidas_del_mes(2026, 9, ahora=ahora)
    cliente.partidas_del_mes(2026, 9, ahora=ahora)
    assert cliente.pedidos == 1


def test_mes_cerrado_bajado_antes_de_terminar_se_pide_una_vez_mas(cliente):
    cliente.partidas_del_mes(2026, 9, ahora=datetime(2026, 9, 20, tzinfo=timezone.utc))
    ruta = cliente._ruta(2026, 9)
    viejo = datetime(2026, 9, 20, tzinfo=timezone.utc).timestamp()
    os.utime(ruta, (viejo, viejo))          # quedó escrito a mitad de mes
    cliente.partidas_del_mes(2026, 9, ahora=datetime(2026, 10, 15, tzinfo=timezone.utc))
    assert cliente.pedidos == 2


def test_refrescar_ignora_la_cache(cliente):
    ahora = datetime(2026, 10, 15, tzinfo=timezone.utc)
    cliente.partidas_del_mes(2026, 9, ahora=ahora)
    cliente.partidas_del_mes(2026, 9, refrescar=True, ahora=ahora)
    assert cliente.pedidos == 2
