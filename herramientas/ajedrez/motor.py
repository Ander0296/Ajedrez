"""
Stockfish a través de python-chess.

El profe NO calcula de memoria: todo lo concreto (la mejor jugada, si una
táctica funciona, cuánto costó un error) sale de acá. Un modelo de lenguaje
se inventa jugadas y tácticas que no existen; el motor no.

La clasificación de errores usa la misma escala que lichess: se convierte la
evaluación en "probabilidad de ganar" (de -1 a 1) y se mira cuánto cayó con
la jugada. Así perder un peón con la partida igualada pesa más que perderlo
con una torre de ventaja, que es lo que pasa en la práctica.
"""

import math
import os
import shutil
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

import chess
import chess.engine

from ajedrez.partidas import VALOR

MATE = 100_000
UMBRALES = ((0.3, "error grave"), (0.2, "error"), (0.1, "imprecisión"))


class SinMotor(RuntimeError):
    pass


def ruta_stockfish(preferida=""):
    candidatos = [preferida] if preferida else []
    candidatos += [shutil.which("stockfish") or "", "/usr/bin/stockfish",
                   "/usr/games/stockfish", str(Path.home() / ".local/bin/stockfish")]
    for c in candidatos:
        if c and os.path.isfile(c) and os.access(c, os.X_OK):
            return c
    raise SinMotor("No encuentro Stockfish.\n"
                   "  Instalalo con:   yay -S stockfish\n"
                   '  o poné la ruta en ajedrez.toml → [motor] ruta = "..."')


@contextmanager
def abrir(cfg):
    motor = chess.engine.SimpleEngine.popen_uci(ruta_stockfish(cfg.motor_ruta))
    try:
        opciones = {}
        if "Threads" in motor.options:
            opciones["Threads"] = cfg.hilos
        if "Hash" in motor.options:
            opciones["Hash"] = cfg.hash_mb
        motor.configure(opciones)
        yield motor
    finally:
        motor.quit()


# ======================================================================
#  EVALUACIONES
# ======================================================================

def chances(cp):
    """Probabilidad de ganar en [-1, 1] a partir de centipeones (fórmula de lichess)."""
    return 2 / (1 + math.exp(-0.00368208 * cp)) - 1


def clasificar(caida):
    for umbral, nombre in UMBRALES:
        if caida >= umbral:
            return nombre
    return None


@dataclass
class Eval:
    score: object          # chess.engine.PovScore; None si la posición ya es final
    pv: list               # mejor línea (chess.Move)
    final: str = ""        # "mate" / "tablas" si la partida ya terminó ahí

    def cp(self, color):
        """Centipeones desde `color` (mate = ±MATE)."""
        if self.score is None:
            return 0
        return self.score.pov(color).score(mate_score=MATE)

    def mate(self, color):
        """Jugadas para dar mate (>0), para recibirlo (<0) o None."""
        if self.score is None:
            return None
        return self.score.pov(color).mate()


def evaluar(motor, tablero, profundidad, multipv=1):
    """Lista de Eval (una por línea pedida), la mejor primero."""
    if tablero.is_game_over():
        if tablero.is_checkmate():
            # Le toca al que recibió mate: para él es -MATE.
            score = chess.engine.PovScore(chess.engine.Mate(0), tablero.turn)
            return [Eval(score, [], "mate")]
        return [Eval(None, [], "tablas")]
    infos = motor.analyse(tablero, chess.engine.Limit(depth=profundidad), multipv=multipv)
    return [Eval(i["score"], i.get("pv", [])) for i in infos]


def texto_eval(e, color=chess.WHITE):
    """'+1.2' / '#3' (das mate en 3) / '#-2' (recibís mate en 2), desde `color`."""
    if e.final == "tablas":
        return "0.0"
    m = e.mate(color)
    if m is not None:
        if m == 0:
            return "#0" if e.score.pov(color).score(mate_score=MATE) > 0 else "#-0"
        return f"#{m}"
    return f"{e.cp(color) / 100:+.1f}"


# ======================================================================
#  UNA PARTIDA COMPLETA
# ======================================================================

def evaluar_partida(motor, partida, profundidad, avisar=None):
    """Eval de cada posición: [antes de la jugada 1, después de la 1, ...]."""
    tablero = partida.juego().board()
    jugadas = list(partida.juego().mainline_moves())
    evals = [evaluar(motor, tablero, profundidad)[0]]
    for i, jugada in enumerate(jugadas, start=1):
        tablero.push(jugada)
        evals.append(evaluar(motor, tablero, profundidad)[0])
        if avisar:
            avisar(i, len(jugadas))
    return evals


def fase(tablero):
    piezas = {c: sum(VALOR[p.piece_type] for p in tablero.piece_map().values()
                     if p.color == c and p.piece_type not in (chess.PAWN, chess.KING))
              for c in (chess.WHITE, chess.BLACK)}
    if max(piezas.values()) <= 13:
        return "final"
    return "apertura" if tablero.fullmove_number <= 12 else "medio juego"


def _pista(antes, despues, tablero_despues, color):
    """Qué tipo de error fue, con una regla simple. Es una PISTA: la palabra
    final la tienen el análisis del usuario y el profe."""
    mate_antes, mate_despues = antes.mate(color), despues.mate(color)
    if mate_despues is not None and mate_despues < 0 and not (mate_antes is not None and mate_antes < 0):
        return "permitiste mate"
    if mate_antes is not None and mate_antes > 0 and not (mate_despues is not None and mate_despues > 0):
        return "mate no visto"
    if despues.pv:
        respuesta = despues.pv[0]
        if tablero_despues.is_capture(respuesta):
            victima = tablero_despues.piece_at(respuesta.to_square)
            if victima and VALOR[victima.piece_type] >= 3:
                return "pieza regalada"
        if tablero_despues.gives_check(respuesta):
            return "táctica del rival (jaque)"
        if tablero_despues.is_capture(respuesta):
            return "material regalado"
    return "amenaza del rival"


def momentos(partida, evals):
    """Errores míos y errores del rival que no castigué, en orden de partida."""
    yo = partida.color
    js = partida.jugadas()
    tablero = partida.juego().board()
    jugadas = list(partida.juego().mainline_moves())
    resultado = []
    caida_rival = 0.0
    for i, jugada in enumerate(jugadas):
        antes, despues = evals[i], evals[i + 1]
        mover = tablero.turn
        tablero_antes = tablero.copy(stack=False)
        tablero.push(jugada)
        caida = chances(antes.cp(mover)) - chances(despues.cp(mover))
        if mover != yo:
            caida_rival = caida
            continue
        tipo = clasificar(caida)
        no_castigo = caida_rival >= 0.3 and caida >= 0.2
        if tipo in ("error grave", "error") or no_castigo:
            resultado.append({
                "ply": i + 1,
                "numero": tablero_antes.fullmove_number,
                "jugada": jugada,
                "tablero": tablero_antes,
                "mejor": antes.pv[0] if antes.pv else None,
                "linea_mejor": antes.pv[:6],
                "antes": antes, "despues": despues,
                "caida": caida,
                "tipo": tipo or "error",
                "pista": "no castigaste su error" if no_castigo else _pista(antes, despues, tablero, yo),
                "fase": fase(tablero_antes),
                "pensado": js[i].pensado,
                "reloj": js[i].reloj,
            })
        caida_rival = 0.0
    return resultado
