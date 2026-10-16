# GUÍA: Ajedrez — de 764 a jugador de torneo

No asume conocimiento previo — la mantiene Claude Code sesión a sesión.
Cada SESIÓN #NN es una tanda del libro de Illescas (pantallazos del Kindle),
explicada en español y conectada con mis partidas. Lo que aprendo de mis
partidas vive en PARTIDAS.md; las prácticas, en EJERCICIOS.md.

## INICIO RÁPIDO

- Fase: F0 — Diagnóstico y sistema (RUTA.md; datos en DIAGNOSTICO.md)
- Tema de la semana: el chequeo antes de mover + f7 (hasta la 1ª /semana)
- Libro: sin empezar. Caps. 1-11 LECTURA; 1ª TANDA = caps. 12-15 (docs/ILLESCAS.md)
- Última tanda: ninguna todavía (las tandas se numeran "Sesión #NN")
- Última partida analizada: ninguna; las partidas hasta el 2026-10-15 20:12
  (vs Mandauw) las cubre el diagnóstico
- PRÓXIMA SESIÓN: `/rename ajedrez-s03`   ← sale SIEMPRE de acá, no se calcula
- Prácticas pendientes: #01 f7, #03 reloj · #02 mates ✅ (r1: 2026-10-19)
- Última /semana: nunca (la primera: domingo 2026-10-18)
- Último triage (`/pendientes`): nunca
- Último examen (`/examen`): nunca
- Entorno: Python 3.14 + uv · python-chess 1.11.2 · Stockfish 19 · 47 tests OK

## VOCABULARIO (lo que en chess.com y YouTube se dice en inglés; una fila por término nuevo)

| Inglés | Español | En una frase |
| --- | --- | --- |
| blunder (??) | error grave | Jugada que regala material o la partida. |
| mistake (?) | error | Empeora bastante la posición, sin regalarla. |
| inaccuracy (?!) | imprecisión | No es la mejor, pero casi no cambia nada. |
| miss | oportunidad perdida | No aprovechaste un error del rival. |
| hanging piece | pieza colgada / suelta | Atacada y sin defensa suficiente: se cae. |
| fork | horquilla (ataque doble) | Una pieza ataca dos cosas a la vez. |
| pin | clavada | Una pieza no puede moverse sin dejar expuesta otra más valiosa detrás. |
| skewer | enfilada (rayos X) | Como la clavada, pero la pieza valiosa está ADELANTE y tiene que salir. |
| discovered attack | ataque a la descubierta | Al mover una pieza, se destapa el ataque de otra que estaba atrás. |
| back-rank mate | mate del pasillo | Mate en la última fila con el rey encerrado por sus propios peones. |
| Game Review / Key moments / Retry | revisión de partida / momentos clave / reintentar | El análisis del coach de chess.com y su modo de volver a intentar. |
| Custom Puzzles | problemas personalizados | Problemas elegidos por tema (sin rating). |
| stalemate | ahogado | Sin jugadas legales y SIN jaque: son tablas. |
| opposition | oposición | Reyes frente a frente con una sola casilla entre ellos: el que mueve cede terreno. |

============================================================
(ACÁ VAN LAS SESIONES — Claude agrega la SESIÓN #01 con la primera tanda del
libro y sigue numerando hacia abajo, una sección por sesión, en el formato
CORTO del final. Cuando el archivo supere ~500 líneas, las sesiones viejas
van a GUIA-ARCHIVO.md.)
============================================================

# ============================================================
# FORMATO DE CADA SESIÓN (referencia para Claude — copiar y llenar)
# 5-8 bullets, SIN diagramas ni contenido repetido del chat. Máx. ~15 líneas.
# ============================================================

SESIÓN #NN — [fecha] — [tema] (cap. N, pantallazos X-Y, % del libro)
- [idea clave 1, una línea]
- [idea clave 2...]
- Conexión con mis partidas: [una línea, o "ninguna"]
- Ejercicios del libro: [serie N: resueltos/fallados → prácticas, o "ninguno"]
- Nota del profe: [solo si la hubo]
- Dudas: [tema + veredicto en una línea, o "ninguna"]
- PRÁCTICAS CREADAS: [#NN o "ninguna"]
- PRÓXIMO PASO: [una línea]
