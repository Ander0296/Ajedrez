"""
`uv run ajedrez <comando>` — las herramientas del entrenador.

    resumen    estadísticas de un período: resultados, proceso, aperturas
    partidas   lista de las últimas partidas
    partida    una partida en detalle (reloj, material; con --motor, errores)
    posicion   un FEN: diagrama, enlaces y lo que dice Stockfish
    errores    Stockfish sobre tus últimas N partidas: dónde y cómo perdés
    descargar  refresca la caché de partidas de chess.com

La salida es Markdown: la lee Claude en /partida y /semana, y se puede leer
tal cual en la terminal. Las jugadas salen en notación ESPAÑOLA (la del
libro); los FEN y los PGN, en el formato estándar.
"""

import argparse
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone

import chess
import chess.pgn

from ajedrez import config as C
from ajedrez import motor as M
from ajedrez import partidas as P
from ajedrez import resumen as R
from ajedrez import tablero as T
from ajedrez.chesscom import ClienteChessCom, ErrorChessCom
from ajedrez.notacion import es_a_san, jugada_es, linea_desde, linea_es, san_a_es, tokens


def _cliente(cfg):
    return ClienteChessCom(cfg.usuario, cfg.agente, cfg.cache)


def _avisar(texto):
    print(texto, file=sys.stderr, flush=True)


def _hora(p):
    return p.fin.astimezone().strftime("%Y-%m-%d %H:%M")


def _mmss(segundos):
    if segundos is None:
        return "—"
    s = int(round(segundos))
    return f"{s // 60}:{s % 60:02d}"


# ======================================================================
#  resumen
# ======================================================================

def cmd_resumen(args):
    cfg = C.cargar()
    cli = _cliente(cfg)
    ahora = datetime.now(timezone.utc)
    if args.todo:
        desde, titulo = None, "todas las partidas"
    elif args.desde:
        desde = datetime.fromisoformat(args.desde).astimezone()
        titulo = f"desde el {args.desde}"
    else:
        desde = ahora - timedelta(days=args.dias)
        titulo = f"últimos {args.dias} días"
    lista = P.estandar(cli.partidas(desde, refrescar=args.refrescar), cfg.usuario)
    if args.clase:
        lista = [p for p in lista if p.clase == args.clase]
    d = R.calcular(lista)
    print(R.informe(d, f"Resumen — {cfg.usuario} — {titulo}", cfg.metas, cli.estadisticas()))
    return 0


# ======================================================================
#  partidas
# ======================================================================

def cmd_partidas(args):
    cfg = C.cargar()
    cli = _cliente(cfg)
    desde = datetime.now(timezone.utc) - timedelta(days=args.dias)
    lista = P.estandar(cli.partidas(desde), cfg.usuario)[-args.ultimas:]
    if not lista:
        print(f"Sin partidas en los últimos {args.dias} días.")
        return 0
    print(f"## Últimas {len(lista)} partidas de {cfg.usuario} (la 1 es la más reciente)\n")
    print("| # | Fecha | Yo | Rival | Res. | Cómo | Jug. | Control | s/jug | Apertura | Link |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for n, p in enumerate(reversed(lista), start=1):
        s = P.mediana(P.segundos_por_jugada(p))
        print(f"| {n} | {_hora(p)} | {p.color_texto} {p.rating} | {p.rival} ({p.rating_rival}) "
              f"| {p.resultado} | {P.MOTIVO.get(p.motivo, p.motivo)} | {p.largo} | {p.control_legible} "
              f"| {'—' if s is None else f'{s:.0f}'} | {p.apertura} | {p.url} |")
    return 0


# ======================================================================
#  partida
# ======================================================================

def _buscar_partida(cfg, cual):
    """'ultima', un número (1 = la última), una URL de chess.com o un id."""
    cli = _cliente(cfg)
    if cual in ("ultima", "última") or cual.isdigit() and len(cual) < 4:
        n = 1 if not cual.isdigit() else int(cual)
        meses = cli.meses()
        juntadas = []
        for anio, mes in reversed(meses):
            juntadas = P.estandar(cli.partidas_del_mes(anio, mes), cfg.usuario) + juntadas
            if len(juntadas) >= n:
                break
        if len(juntadas) < n:
            raise ValueError(f"No hay {n} partidas.")
        return juntadas[-n]
    id_buscado = cual.rstrip("/").rsplit("/", 1)[-1].split("?")[0]
    for anio, mes in reversed(cli.meses()):
        for j in cli.partidas_del_mes(anio, mes):
            if j.get("url", "").rstrip("/").endswith("/" + id_buscado):
                return P.desde_api(j, cfg.usuario)
    raise ValueError(f"No encuentro la partida «{cual}» entre las de {cfg.usuario}.")


def _jugadas_con_tiempo(p):
    """'1.e4 e5·2 2.Cf3 Cc6·3 ...': tras MIS jugadas, los segundos que pensé."""
    partes = []
    for j in p.jugadas():
        texto = san_a_es(j.san)
        if j.color == chess.WHITE:
            texto = f"{j.numero}.{texto}"
        elif j.ply == 1:
            texto = f"{j.numero}...{texto}"
        if j.color == p.color and j.pensado is not None:
            texto += f"·{j.pensado:.0f}"
        partes.append(texto)
    return " ".join(partes)


def cmd_partida(args):
    cfg = C.cargar()
    p = _buscar_partida(cfg, args.cual)
    res = {"G": "GANASTE", "P": "PERDISTE", "T": "TABLAS"}[p.resultado]
    print(f"## Partida — {_hora(p)} — {cfg.usuario} ({p.color_texto}, {p.rating}) vs "
          f"{p.rival} ({p.rating_rival}) — {res} ({P.MOTIVO.get(p.motivo, p.motivo)}, "
          f"jugada {p.largo})")
    extra = f" · precisión chess.com {p.precision:.1f}" if p.precision is not None else ""
    print(f"{p.control_legible} · {p.apertura}{extra} · {p.url}")
    seg = P.segundos_por_jugada(p)
    if seg:
        sin_usar = P.reloj_sin_usar(p)
        print(f"Reloj: mediana {P.mediana(seg):.1f} s por jugada (desde la 6ª) · "
              f"{100 * sum(s < 3 for s in seg) / len(seg):.0f}% en < 3 s · "
              f"te quedó el {100 * sin_usar:.0f}% del tiempo")
    perdida = P.perdida_de_material(p)
    if perdida:
        print(f"Material (sin motor, aprox.): perdiste {perdida['puntos']} puntos cerca de tu jugada "
              f"{perdida['numero']} ({san_a_es(perdida['jugada'] or '?')}, pensada "
              f"{_seg(perdida['pensado'])}) y no lo recuperaste")
    print(f"\n### Jugadas (·N = segundos que pensaste esa jugada)\n\n{_jugadas_con_tiempo(p)}")
    if args.motor:
        with M.abrir(cfg) as motor:
            _avisar(f"Stockfish, profundidad {args.profundidad or cfg.profundidad_partida}...")
            evals = M.evaluar_partida(motor, p, args.profundidad or cfg.profundidad_partida)
        _imprimir_momentos(p, M.momentos(p, evals), args.profundidad or cfg.profundidad_partida)
    return 0


def _seg(v):
    return "—" if v is None else f"{v:.0f} s"


def _imprimir_momentos(p, momentos, profundidad):
    print(f"\n### Momentos críticos (Stockfish, profundidad {profundidad})\n")
    if not momentos:
        print("Ningún error ni error grave tuyo. Las imprecisiones no se listan a este nivel.")
        return
    print("| Jugada | Jugaste | Mejor | Eval (tuya) antes → después | Tipo | Pista | Fase | Pensaste | Reloj |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for m in momentos:
        t = m["tablero"]
        mejor = jugada_es(t, m["mejor"]) if m["mejor"] else "—"
        print(f"| {m['numero']}{'.' if t.turn == chess.WHITE else '...'} | "
              f"{san_a_es(t.san(m['jugada']))} | {mejor} | "
              f"{M.texto_eval(m['antes'], p.color)} → {M.texto_eval(m['despues'], p.color)} | "
              f"{m['tipo']} | {m['pista']} | {m['fase']} | {_seg(m['pensado'])} | {_mmss(m['reloj'])} |")
    print("\nLínea del motor y FEN de cada momento (para crear ejercicios):")
    for m in momentos:
        t = m["tablero"]
        linea = linea_desde(t, m["linea_mejor"]) if m["linea_mejor"] else "—"
        print(f"- {m['numero']}: {linea}\n  FEN `{t.fen()}`")


# ======================================================================
#  posicion
# ======================================================================

def _orientacion(tablero, opcion):
    if opcion == "blancas":
        return chess.WHITE
    if opcion == "negras":
        return chess.BLACK
    return tablero.turn


def _parsear_linea(tablero, texto, ingles):
    jugadas, copia = [], tablero.copy(stack=False)
    for t in tokens(texto):
        san = t if ingles else es_a_san(t)
        try:
            jugada = copia.parse_san(san)
        except ValueError as e:
            raise ValueError(f"«{t}» no es una jugada legal en esa posición "
                             f"(juegan {T.turno(copia)}).") from e
        jugadas.append(jugada)
        copia.push(jugada)
    return jugadas


def cmd_posicion(args):
    cfg = C.cargar()
    try:
        tablero = chess.Board(args.fen)
    except ValueError as e:
        raise ValueError(f"FEN inválido: {e}") from e
    orientacion = _orientacion(tablero, args.orientacion)
    print(f"```\n{T.texto(tablero, orientacion)}\n```")
    print(T.LEYENDA)
    print(f"Juegan: {T.turno(tablero)} · FEN `{tablero.fen()}`")
    if not tablero.is_valid():
        print(f"⚠ Posición ilegal según las reglas: {tablero.status()!r}. Revisá el FEN.")
        return 1
    print(f"Ver: {T.enlace_chesscom(tablero.fen())}\n     {T.enlace_lichess(tablero.fen(), orientacion)}")
    propuesta = _parsear_linea(tablero, args.linea, args.en) if args.linea else []
    if args.sin_motor:
        if propuesta:
            print(f"\nLínea propuesta (legal): {linea_desde(tablero, propuesta)}")
        return 0
    profundidad = args.profundidad or cfg.profundidad_posicion
    with M.abrir(cfg) as motor:
        mejores = M.evaluar(motor, tablero, profundidad, multipv=args.multipv)
        print(f"\n### Stockfish (profundidad {profundidad}, evaluación desde las blancas)\n")
        for n, e in enumerate(mejores, start=1):
            linea = linea_desde(tablero, e.pv[:8]) if e.pv else "—"
            print(f"{n}. {M.texto_eval(e)}  {linea}")
        if propuesta:
            _evaluar_propuesta(motor, tablero, propuesta, mejores[0], profundidad)
    return 0


def _evaluar_propuesta(motor, tablero, propuesta, mejor, profundidad):
    quien = tablero.turn
    copia = tablero.copy(stack=False)
    copia.push(propuesta[0])
    tras_primera = M.evaluar(motor, copia, profundidad)[0]
    caida = M.chances(mejor.cp(quien)) - M.chances(tras_primera.cp(quien))
    veredicto = M.clasificar(caida)
    es_la_mejor = bool(mejor.pv) and propuesta[0] == mejor.pv[0]
    print(f"\n### La línea propuesta: {linea_desde(tablero, propuesta)}\n")
    if es_la_mejor:
        print(f"✓ {jugada_es(tablero, propuesta[0])} es la jugada del motor.")
    elif veredicto is None:
        print(f"≈ {jugada_es(tablero, propuesta[0])} es buena: casi no cambia la evaluación "
              f"({M.texto_eval(mejor)} → {M.texto_eval(tras_primera)}).")
    else:
        print(f"✗ {jugada_es(tablero, propuesta[0])} es {veredicto} "
              f"({M.texto_eval(mejor)} → {M.texto_eval(tras_primera)}). "
              f"Mejor: {jugada_es(tablero, mejor.pv[0])}.")
        if tras_primera.pv:
            print(f"  Refutación: {linea_desde(copia, tras_primera.pv[:6])}")
    if len(propuesta) > 1:
        final = tablero.copy(stack=False)
        for j in propuesta:
            final.push(j)
        e = M.evaluar(motor, final, profundidad)[0]
        continua = linea_desde(final, e.pv[:4]) if e.pv else "—"
        print(f"Al final de tu línea: {M.texto_eval(e)} · el motor sigue: {continua}")
        sigue_igual = M.clasificar(M.chances(mejor.cp(quien)) - M.chances(e.cp(quien)))
        if sigue_igual:
            print(f"  Ojo: comparada con la mejor, tu línea completa es {sigue_igual}: "
                  f"alguna jugada del medio (tuya o del rival) no es la correcta.")


# ======================================================================
#  errores (varias partidas)
# ======================================================================

def cmd_errores(args):
    cfg = C.cargar()
    cli = _cliente(cfg)
    desde = datetime.now(timezone.utc) - timedelta(days=args.dias)
    lista = [p for p in P.estandar(cli.partidas(desde), cfg.usuario) if p.clase != "daily"]
    lista = lista[-args.ultimas:]
    if not lista:
        print("Sin partidas para analizar.")
        return 0
    profundidad = args.profundidad or cfg.profundidad_errores
    todos = []
    with M.abrir(cfg) as motor:
        for n, p in enumerate(lista, start=1):
            _avisar(f"[{n}/{len(lista)}] {_hora(p)} vs {p.rival}...")
            for m in M.momentos(p, M.evaluar_partida(motor, p, profundidad)):
                m["partida"] = p
                todos.append(m)
    graves = [m for m in todos if m["tipo"] == "error grave"]
    print(f"## Errores en {len(lista)} partidas — Stockfish profundidad {profundidad}\n")
    print(f"- Errores graves: {len(graves)} ({len(graves) / len(lista):.1f} por partida) · "
          f"errores: {sum(m['tipo'] == 'error' for m in todos)} · "
          f"partidas con al menos un error grave: "
          f"{len({m['partida'].url for m in graves})}/{len(lista)}")
    primeros = {}
    for m in graves:
        primeros.setdefault(m["partida"].url, m["numero"])
    if primeros:
        print(f"- Jugada del PRIMER error grave (mediana): {P.mediana(list(primeros.values()))}")
    _tabla_conteo("Qué tipo de error grave (pista automática)", Counter(m["pista"] for m in graves))
    _tabla_conteo("En qué fase", Counter(m["fase"] for m in graves))
    tiempos = Counter()
    for m in graves:
        s = m["pensado"]
        if s is None:
            tiempos["sin reloj"] += 1
        elif s < 5:
            tiempos["< 5 s"] += 1
        elif s < 15:
            tiempos["5-15 s"] += 1
        else:
            tiempos["≥ 15 s"] += 1
    _tabla_conteo("Cuánto pensaste la jugada del error grave", tiempos)
    apuro = sum(1 for m in graves if m["reloj"] is not None and m["partida"].base
                and m["reloj"] < 0.1 * m["partida"].base)
    print(f"Errores graves con menos del 10% del reloj (apuro de tiempo): {apuro}/{len(graves)}\n")

    print("### Los más caros (para ejercicios)\n")
    for m in sorted(graves, key=lambda m: -m["caida"])[:args.mostrar]:
        p, t = m["partida"], m["tablero"]
        mejor = jugada_es(t, m["mejor"]) if m["mejor"] else "—"
        print(f"- {_hora(p)} vs {p.rival}: jugaste {jugada_es(t, m['jugada'])} ({m['pista']}, "
              f"{_seg(m['pensado'])}); mejor {mejor} · {p.url}\n  FEN `{t.fen()}`")
    ruta = cfg.datos / "mis-errores.pgn"
    _exportar_pgn(todos, ruta, cfg.usuario)
    print(f"\nPGN con {len(todos)} posiciones para practicar: {ruta.relative_to(cfg.raiz)} "
          f"(importable en un Estudio de lichess o en el tablero de análisis de chess.com)")
    return 0


def _tabla_conteo(titulo, contador):
    total = sum(contador.values())
    if not total:
        return
    print(f"\n{titulo}: " + " · ".join(f"{k} {v} ({100 * v / total:.0f}%)"
                                      for k, v in contador.most_common()))


def _exportar_pgn(momentos, ruta, usuario):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        for m in momentos:
            p, t = m["partida"], m["tablero"]
            juego = chess.pgn.Game()
            juego.setup(t)
            juego.headers["Event"] = f"Mis errores — {m['tipo']} — {m['pista']}"
            juego.headers["Site"] = p.url
            juego.headers["Date"] = p.fin.astimezone().strftime("%Y.%m.%d")
            juego.headers["White"] = usuario if p.color == chess.WHITE else p.rival
            juego.headers["Black"] = p.rival if p.color == chess.WHITE else usuario
            juego.comment = (f"En la partida jugaste {jugada_es(t, m['jugada'])}. "
                             f"Juegan {T.turno(t)}: encontrá algo mejor.")
            nodo = juego
            for jugada in m["linea_mejor"]:
                nodo = nodo.add_variation(jugada)
            print(juego, file=f, end="\n\n")


# ======================================================================
#  descargar
# ======================================================================

def cmd_descargar(args):
    cfg = C.cargar()
    cli = _cliente(cfg)
    total = 0
    for anio, mes in cli.meses():
        n = len(cli.partidas_del_mes(anio, mes, refrescar=args.todo))
        total += n
        _avisar(f"{anio}-{mes:02d}: {n} partidas")
    print(f"{total} partidas en la caché ({cfg.cache.relative_to(cfg.raiz)}).")
    return 0


# ======================================================================
#  ENTRADA
# ======================================================================

def main(argv=None):
    ap = argparse.ArgumentParser(prog="ajedrez", description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="comando", required=True)

    s = sub.add_parser("resumen", help="estadísticas de un período (por defecto, 7 días)")
    s.add_argument("--dias", type=int, default=7)
    s.add_argument("--desde", help="AAAA-MM-DD")
    s.add_argument("--todo", action="store_true", help="todas las partidas (diagnóstico)")
    s.add_argument("--clase", choices=["rapid", "blitz", "bullet", "daily"])
    s.add_argument("--refrescar", action="store_true", help="ignorar la caché")
    s.set_defaults(funcion=cmd_resumen)

    s = sub.add_parser("partidas", help="lista de las últimas partidas")
    s.add_argument("--ultimas", type=int, default=10)
    s.add_argument("--dias", type=int, default=60)
    s.set_defaults(funcion=cmd_partidas)

    s = sub.add_parser("partida", help="una partida en detalle")
    s.add_argument("cual", nargs="?", default="ultima",
                   help="'ultima', N (1 = la última), URL de chess.com o id")
    s.add_argument("--motor", action="store_true", help="analizar con Stockfish")
    s.add_argument("--profundidad", type=int)
    s.set_defaults(funcion=cmd_partida)

    s = sub.add_parser("posicion", help="diagrama, enlaces y Stockfish para un FEN")
    s.add_argument("fen")
    s.add_argument("--linea", help='jugadas a evaluar, en español: "4...d5 5.exd5 Ca5"')
    s.add_argument("--en", action="store_true", help="la línea viene en notación inglesa")
    s.add_argument("--multipv", type=int, default=3)
    s.add_argument("--profundidad", type=int)
    s.add_argument("--orientacion", choices=["turno", "blancas", "negras"], default="turno")
    s.add_argument("--sin-motor", action="store_true", help="solo diagrama, enlaces y legalidad")
    s.set_defaults(funcion=cmd_posicion)

    s = sub.add_parser("errores", help="Stockfish sobre tus últimas N partidas")
    s.add_argument("--ultimas", type=int, default=20)
    s.add_argument("--dias", type=int, default=365)
    s.add_argument("--profundidad", type=int)
    s.add_argument("--mostrar", type=int, default=8, help="cuántos momentos caros listar")
    s.set_defaults(funcion=cmd_errores)

    s = sub.add_parser("descargar", help="refrescar la caché de chess.com")
    s.add_argument("--todo", action="store_true", help="volver a bajar también los meses cerrados")
    s.set_defaults(funcion=cmd_descargar)

    args = ap.parse_args(argv)
    try:
        return args.funcion(args)
    except (ErrorChessCom, M.SinMotor, FileNotFoundError, ValueError) as e:
        print(f"✗ {e}", file=sys.stderr)
        return 1
