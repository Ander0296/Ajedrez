---
description: Analizar una partida que jugué — primero yo, después el motor; lecciones, ejercicio y registro
argument-hint: [cuál: "la última", "la 2", un link de chess.com, o "analicé la partida en analisis/..."]
---

Partida para analizar. $ARGUMENTS

Aplicá **el ciclo de una partida** de CLAUDE.md (no lo leas con Read: ya
lo tenés cargado). La regla que no se negocia: **primero analizo yo,
después el motor.**

**Si todavía no hay archivo mío en `analisis/` para esta partida:**
1. Corré `uv run ajedrez partida <cuál>` SIN `--motor` (solo datos,
   jugadas y reloj).
2. Creá el arranque `analisis/AAAA-MM-DD-<rival>.md` con: la cabecera de
   la partida (fecha, colores, rival, resultado, control, apertura, link,
   mi reloj), las preguntas del autoanálisis (en caliente; 2-3 momentos
   críticos: qué jugué, qué pensaba, qué amenazaba el rival, qué jugaría
   ahora; mi categoría de error de la TAXONOMÍA; ¿usé el chequeo?) y al
   final el prompt de vuelta ya relleno:
   `/partida analicé la partida en analisis/AAAA-MM-DD-<rival>.md`
3. Decime dónde está, recordame `ToDo/despues-de-la-partida.md` (Game
   Review con "Reintentar" ANTES de volver) y **detenete**. Ni una línea del
   motor todavía.

**Si ya escribí mi análisis:**
1. Leelo. Corré `uv run ajedrez partida <cuál> --motor`.
2. En el chat: qué vi bien, qué no vi, y qué PASO DEL PROCESO falló en cada
   error grave (no solo la jugada: el porqué de no haberla visto). Máximo 3
   lecciones, de la más cara a la más barata. Todo lo concreto, verificado
   con el motor; las ideas, con palabras humanas.
3. Clasificá cada error grave con la TAXONOMÍA (contrastando la pista de la
   herramienta con lo que escribí yo).
4. Creá 1-2 prácticas POSICIÓN con las posiciones más instructivas (FEN y
   enlace Resolver de la herramienta, sin diagrama de texto: formato de
   CLAUDE.md) y registralas en
   EJERCICIOS.md.
5. Agregá la línea en PARTIDAS.md y actualizá "Última partida analizada"
   en el INICIO RÁPIDO de GUIA.md. Si la categoría ya apareció 3+ veces en
   las últimas 10 partidas, avisame: es un PATRÓN.
6. Revisá si hay que tocar un checklist de `ToDo/`. Si hubo lección nueva:
   1-2 frases a MECANOGRAFIA.md (+ ttyper) y 2-3 tarjetas a ANKI.txt, sin
   regalar la solución de las prácticas que acabás de crear.

Si la partida todavía se está jugando (diaria en curso), no la analices:
decímelo y por qué (fair play).

Cerrá con el bloque `▶ SIGUE`.
