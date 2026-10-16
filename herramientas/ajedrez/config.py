"""
Lectura de ajedrez.toml, el único archivo de configuración del repo.

Se busca subiendo desde la carpeta actual, así los comandos funcionan
desde cualquier subcarpeta del repo (ejercicios/, analisis/...).
"""

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

ARCHIVO = "ajedrez.toml"


@dataclass(frozen=True)
class Config:
    raiz: Path
    usuario: str
    agente: str
    motor_ruta: str = ""
    profundidad_partida: int = 14
    profundidad_errores: int = 12
    profundidad_posicion: int = 20
    hilos: int = 2
    hash_mb: int = 256
    metas: dict = field(default_factory=dict)

    @property
    def cache(self):
        """Partidas bajadas de chess.com. No va a git: se vuelve a bajar."""
        return self.raiz / "datos" / "cache"

    @property
    def datos(self):
        return self.raiz / "datos"


def buscar_raiz(desde=None):
    actual = Path(desde or Path.cwd()).resolve()
    for carpeta in (actual, *actual.parents):
        if (carpeta / ARCHIVO).is_file():
            return carpeta
    raise FileNotFoundError(
        f"No encuentro {ARCHIVO}: corré el comando dentro del repo de Ajedrez.")


def cargar(desde=None):
    raiz = buscar_raiz(desde)
    with open(raiz / ARCHIVO, "rb") as f:
        t = tomllib.load(f)
    cc, m = t.get("chesscom", {}), t.get("motor", {})
    return Config(
        raiz=raiz,
        usuario=str(cc.get("usuario", "")).strip().lower(),
        agente=str(cc.get("agente", "ajedrez-entrenamiento-personal/0.1")),
        motor_ruta=os.environ.get("AJEDREZ_STOCKFISH") or str(m.get("ruta", "")),
        profundidad_partida=int(m.get("profundidad_partida", 14)),
        profundidad_errores=int(m.get("profundidad_errores", 12)),
        profundidad_posicion=int(m.get("profundidad_posicion", 20)),
        hilos=int(m.get("hilos", max(1, (os.cpu_count() or 2) // 2))),
        hash_mb=int(m.get("hash_mb", 256)),
        metas=dict(t.get("metas", {})),
    )
