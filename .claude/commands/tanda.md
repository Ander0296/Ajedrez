---
description: Explica los pantallazos del libro de Illescas que dejé en material/ (una tanda por sesión)
argument-hint: [opcional: qué hay en la tanda, ej "cap. 18 ataque doble, 4 pantallazos"]
---

Tanda nueva del libro. $ARGUMENTS

Los pantallazos están en `material/` (en orden de nombre). No entres a
`material/visto/`: eso ya está explicado. Antes de empezar, mirá en
`docs/ILLESCAS.md` qué prioridad tiene este capítulo (LECTURA, TANDA o
TANDA ★) para calibrar la profundidad.

Aplicá el **flujo por tanda** completo de CLAUDE.md (no lo leas con Read:
ya lo tenés cargado):

1. Explicámelo PIEZA POR PIEZA, anunciando cuál ("PANTALLAZO 2:"), en
   español, con palabras propias, COMPRIMIENDO. Conectalo con mis partidas
   cuando se pueda ("esto es lo que te pasó en...": mirá PARTIDAS.md con
   Grep si hace falta).
2. Cada diagrama importante: pasalo a FEN, validalo con
   `uv run ajedrez posicion "<FEN>" --orientacion blancas --sin-motor` y
   pedime que confirme con el enlace que coincide con el libro. Lo
   concreto, verificado con el motor antes de enseñarlo.
3. Si la tanda trae ejercicios del libro: que los intente yo ANTES de
   mirar las soluciones del libro; los que falle se vuelven prácticas
   POSICIÓN (máx. 2).
4. Verificá que entendí con 1-2 preguntas cortas antes de cerrar.

Cuando termines, en el mismo turno:
- mové los pantallazos a `material/visto/`;
- `GUIA.md`: la sesión en FORMATO CORTO y el INICIO RÁPIDO (con
  **PRÓXIMA SESIÓN** y el capítulo donde quedamos), y VOCABULARIO si
  apareció un término que en chess.com se dice en inglés;
- 1-2 frases a `MECANOGRAFIA.md` + su archivo de ttyper (append-only);
- 2-5 tarjetas 80/20 a `ANKI.txt`;
- revisá si hay que crear o tocar un checklist de `ToDo/`;
- guardá en Engram el capítulo y la página donde quedamos.

Cerrá con el bloque `▶ SIGUE`. Fue una tanda de IMÁGENES: lo que sigue es
`/cambio` (o `/cierre` si terminó el día), y decime por qué en una línea.
Si se cumple un disparador de `/examen`, sumalo en UNA línea.
