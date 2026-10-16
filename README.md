# AJEDREZ — de 764 a jugador de torneo, con Claude Code de entrenador

Sistema de entrenamiento con método, para dejar de jugar por jugar. **Yo
juego, analizo primero y resuelvo todo a mano.** Claude (el profe) analiza
mis partidas con Stockfish, encuentra el error de PROCESO detrás de cada
error de jugada, me arma ejercicios con MIS posiciones, mantiene el plan y
me dice siempre qué sigue.

Es el mismo sistema de mis otros proyectos (`/arranque` … `/cierre`), con
dos comandos propios del ajedrez: `/partida` y `/semana`. Y una diferencia de
fondo: acá **el libro no es el centro; el centro son mis partidas**.

Punto de partida (2026-10-15): rápidas **764**, problemas **1477**, 440
partidas. Objetivo: **1800+ y torneos con rating FIDE**, con ~30 min/día.

## Empezá acá (la primera semana)

1. **DIAGNOSTICO.md** (10 min): cómo juego, con datos de mis 440 partidas y
   Stockfish. Todo el plan sale de ahí.
2. **RUTINA.md** (5 min): qué hago cada día y las 6 reglas de juego.
3. **docs/CHESSCOM.md**, sección 3 (10 min): configurar chess.com.
4. **INSTALACION.md**, parte 3: subir este repo a GitHub (privado o público,
   lo decido yo).
5. **ejercicios/p01-defensa-de-f7-chesscom.md**: resolverla en chess.com, sin motor.
6. Primera partida 10|5 con el chequeo → `claude` → `/arranque` → `/partida`.
7. El domingo: `/semana`.

## Los tres lugares donde se hacen cosas

- `[TERMINAL]` = la consola de siempre
- `[CLAUDE]` = dentro del programa, después de escribir `claude`
- `[CHESS.COM]` = la web o la app (jugar, problemas, Game Review)

## El mapa en 30 segundos

```
Ajedrez/
├── DIAGNOSTICO.md   ★ cómo juego, con datos (una foto por fecha)
├── RUTINA.md        ★ qué hago cada día y las reglas de juego
├── RUTA.md            las fases hasta el objetivo, con criterios de salida
├── GUIA.md            INICIO RÁPIDO + lo que ENTENDÍ del libro, sesión a sesión
├── EJERCICIOS.md      SOLO lo vivo: prácticas, repasos, conceptos dominados
├── PARTIDAS.md        mis partidas analizadas y los patrones de error
├── PROGRESO.md        una fila por semana (la escribe /semana)
├── PENDIENTES.md      la deuda que no es una práctica (lo lee /pendientes)
├── ToDo/            ★ los checklists: antes de mover, después de la partida, apertura
├── docs/              la guía de referencia:
│   ├── CHESSCOM.md      cómo usar chess.com Diamante para mejorar
│   ├── METODO.md        cómo aprendemos y por qué así
│   ├── ILLESCAS.md      el plan del libro, capítulo por capítulo
│   ├── APERTURAS.md     qué estudiar (y qué no) de aperturas
│   ├── TEMARIO.md       el mapa de contenidos por fase
│   └── RECURSOS.md      libros, plataformas, canales, torneos en Antioquia
├── ejercicios/        mis prácticas (el profe deja el enunciado; yo resuelvo)
│   └── repasos/         los repasos, siempre desde cero
├── analisis/          mi autoanálisis de cada partida (lo escribo yo)
├── repertorio/        mi repertorio de aperturas (lo escribo yo, Fase 2)
├── material/          pantallazos del libro (NO va a git: copyright)
├── datos/             caché de chess.com y PGN generados (NO va a git)
├── herramientas/      el programa `ajedrez` (Python) y sus tests
├── ajedrez.toml       mi usuario, el motor y las metas de la fase
├── MECANOGRAFIA.md    frases de tipeo (ttyper)
├── ANKI.txt           tarjetas 80/20 para importar en Anki
├── CLAUDE.md          las reglas del profe
└── .claude/           los comandos y los dos automatismos
```

**Los dos automatismos que corren solos:**
- al abrir cualquier sesión se hace `git pull` (cuando el repo ya esté en
  GitHub), aunque me olvide de `/arranque`;
- Claude tiene **prohibido por el harness** editar lo que yo escribí en
  `ejercicios/`, `analisis/` y `repertorio/`: solo puede CREAR el archivo de
  arranque. Si algún día necesito desactivarlo: `/hooks`.

# ============================================================
# EL ÚNICO FLUJO QUE TENGO QUE SABER
# ============================================================

```
[TERMINAL]  cd ~/Proyectos/Ajedrez
[TERMINAL]  claude
[CLAUDE]    /arranque
```

El profe hace `git pull`, mira si jugué partidas que no analizamos, qué
prácticas y repasos tengo, qué toca hoy según la rutina, y me lo dice en
menos de 10 líneas. Termina siempre con un bloque así:

```
▶ SIGUE: analizar la partida de hoy contra fulano (perdiste en la 14)
  1. /rename ajedrez-s05     ← el nombre de ESTA sesión
  2. /partida la última
```

Copio eso y sigo. **No tengo que acordarme de ningún número ni de ningún
mensaje.** Si el bloque no aparece, lo pido: "¿qué sigue?".

# ============================================================
# LOS COMANDOS
# ============================================================

| Comando | Para qué | Cuándo lo uso |
| --- | --- | --- |
| `/arranque` | dónde quedamos, cómo se llama la sesión y qué toca hoy | **siempre, primero** |
| `/partida` | analizar una partida: primero yo, después el motor | después de cada partida valorada |
| `/tanda` | me explica los pantallazos del libro que dejé en `material/` | los lunes, si el capítulo es de TANDA |
| `/entrega` | corrige una práctica que terminé | cuando termino una |
| `/repaso` | repaso vencido, desde cero | cuando el profe avisa |
| `/semana` | revisión con datos: proceso, errores, tema de la semana | **domingo, 10 minutos** |
| `/examen` | examen en frío: posiciones y conceptos | cuando el profe lo propone |
| `/pendientes` | triage: qué se pudre, qué se salda, qué doy de baja | cada 1-2 semanas |
| `/cambio` | cierra esta sesión y abre una limpia | cuando el profe lo dice |
| `/cierre` | guarda todo y sube a git | **antes de salir, siempre** |

Todos aceptan contexto: `/partida la del link https://www.chess.com/game/live/...`,
`/semana problemas 1490, entrené 6 días, me sentí bien`.

### `/partida`, el comando más importante

1. Juego la partida (con el chequeo). Al terminar: `/partida la última`.
2. El profe me crea `analisis/AAAA-MM-DD-rival.md` con las preguntas y se
   detiene. **No me muestra nada del motor todavía.**
3. Yo: 3 minutos "en caliente" + 10 minutos de autoanálisis sin motor +
   Game Review de chess.com con "Reintentar" (`ToDo/despues-de-la-partida.md`).
4. Pego el prompt del final del archivo. El profe compara lo que vi contra
   Stockfish, me dice qué paso del PROCESO falló, deja 1-2 ejercicios con mis
   posiciones y registra la partida en PARTIDAS.md.

# ============================================================
# UNA SEMANA NORMAL (30 minutos por día)
# ============================================================

Lunes táctica + libro · martes jugar · miércoles analizar · jueves técnica ·
viernes jugar · sábado analizar · domingo repaso + `/semana`. Detalle y
reglas en **RUTINA.md**. Claude se abre sobre todo miércoles, sábado y
domingo; el resto del entrenamiento es en chess.com.

# ============================================================
# LAS HERRAMIENTAS (las corre el profe; yo también puedo)
# ============================================================

```
uv run ajedrez partidas                  mis últimas 10 partidas
uv run ajedrez partida 1 --motor         la última, con Stockfish
uv run ajedrez posicion "<FEN>"          diagrama, enlaces y top 3 del motor
uv run ajedrez resumen --dias 7          mi semana: proceso vs. metas
uv run ajedrez errores --ultimas 20      dónde y cómo pierdo (tarda unos minutos)
```

Las jugadas salen en notación española (R D T A C), como en el libro.

# ============================================================
# EL LIBRO (Kindle → pantallazos)
# ============================================================

No se pasa entero: cada capítulo tiene una profundidad (LECTURA solo,
TANDA o TANDA ★) en **docs/ILLESCAS.md**. Para una tanda: 3-5 pantallazos
nítidos en `material/` con nombres en orden (`01.png`, `02.png`...) →
`/tanda`. Una tanda de imágenes por sesión: después, el profe me manda a
`/cambio` o `/cierre`. Los ejercicios del libro los intento SIEMPRE antes
de mirar las soluciones.

# ============================================================
# QUIÉN DECIDE QUÉ
# ============================================================

| Decisión | Quién |
| --- | --- |
| Cuándo juego y cuándo entreno | **yo**, con RUTINA.md |
| Qué partida se analiza primero | el profe (la más reciente / la más instructiva) |
| El tema de la semana | el profe, en `/semana`, con mis datos |
| **Cuándo cortar la sesión** | **el profe**, con el motivo |
| Cómo se llama cada sesión | el profe (sale de GUIA.md) |
| Cuándo tomar examen | el profe lo propone, yo digo sí o no |
| Cambiar de fase | el profe lo propone con los criterios; **decido yo** |
| Resolver, analizar, escribir el repertorio | **yo, siempre** |
| Todo lo de git | el profe (`pull` al abrir, `commit` + `push` al cerrar) |

Si no sé qué sigue, la pregunta es literal: **"¿qué sigue?"**.

# ============================================================
# SI SE CERRÓ LA TERMINAL SIN QUERER (mismo día)
# ============================================================

`[TERMINAL]` `claude --resume ajedrez-sNN` — solo el MISMO día. Día nuevo =
sesión nueva.

# ============================================================
# REGLAS DE ORO
# ============================================================

1. `/arranque` siempre primero; **nunca salir sin `/cierre`**.
2. **Ninguna partida valorada sin analizar.** Máximo 2 por día; dos derrotas
   seguidas = se terminó por hoy.
3. **Primero analizo yo, después el motor.** Nunca al revés.
4. **El chequeo en cada jugada desde la 5ª** (`ToDo/antes-de-mover.md`).
5. **No me rindo antes de la jugada 30** (salvo dama de menos sin
   compensación o mate inevitable). Nunca abandono una partida.
6. Las prácticas se resuelven en chess.com (enlace Resolver), sin motor y
   sin mover piezas hasta escribir la respuesta; los repasos, desde cero.
7. Problemas: precisión antes que velocidad. Puzzle Rush es un juego.
8. `material/` nunca va a git (copyright).
9. Fair play: en las Diarias, Explorador sí; motor y ayuda de otros, NUNCA.
   Claude no analiza partidas en curso.
10. Cuándo cortar lo dice el profe. Cuando lo dice: `/cambio`, nunca
    `Ctrl+D` pelado.

# ============================================================
# MECANOGRAFÍA Y TARJETAS ANKI
# ============================================================

Mecanografía (`MECANOGRAFIA.md`): CTRL+SUPER+ALT+T abre ttyper con una frase
al azar de mis proyectos de estudio; desde ahora también salen frases de
ajedrez (`~/.config/ttyper/texts/ajedrez-*.txt`). Las agrega el profe.

Anki (`ANKI.txt`): Archivo → Importar → elegir este archivo. Mazo, separador
y etiquetas vienen en las cabeceras. Re-importar no duplica: actualiza. En
ajedrez, Anki es para principios y reglas; los patrones se entrenan con
problemas y repasos de posiciones.
