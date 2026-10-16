# RUTA — de 764 a jugador de torneo (1800+ y rating FIDE)

Este archivo define las FASES del proyecto. La fase actual lleva la marca
(⬅ FASE ACTUAL). Los detalles finos de cada fase se definen AL LLEGAR;
Claude mantiene este archivo y, al cambiar de fase, las metas de
`ajedrez.toml [metas]`.

**El objetivo real, en una línea:** dejar de jugar por jugar y convertirme,
con 30 minutos al día bien usados, en un jugador de torneo: 1800+ y rating
FIDE a largo plazo.

## Expectativas honestas (leer una vez)

- El rating se mueve con ruido: ±50 en una semana no significa nada. Por eso
  las fases se cierran con **rating sostenido 4 semanas + métricas de
  PROCESO + prácticas graduadas**, nunca con un pico.
- Lo que suele verse en adultos que entrenan con método: los primeros
  200-300 puntos llegan en meses, porque se corrigen errores de proceso (tu
  caso: jugar rápido, no mirar al rival, rendirte pronto). Después, 100-200
  puntos por año es un ritmo bueno.
- Con ~30 min/día, **1800 es un objetivo de varios años**. El plan no lo
  esconde: en la Fase 3 se revisa con datos si conviene subir a 45-60 min.
- Lo que acelera de verdad no es estudiar más cosas, es **no repetir los
  mismos errores**: por eso todo gira alrededor de TUS partidas.

## Lo que NUNCA cambia (en todas las fases)

- El ciclo: jugar lento → analizar (primero yo, después el motor) →
  entrenar lo que falló → jugar.
- El chequeo antes de mover (`ToDo/antes-de-mover.md`).
- Ninguna partida valorada sin analizar. Máximo 2 por día.
- El profe verifica con Stockfish, no de memoria.
- Las sesiones numeradas, Engram, GUIA.md, EJERCICIOS.md y los repasos
  espaciados. git lo maneja el profe.
- Todo en español; lo de chess.com en inglés, traducido al lado.

## FASE 0 — Diagnóstico y sistema (⬅ FASE ACTUAL) · 1-2 semanas

Objetivo: dejar el sistema andando y cambiar CÓMO juego antes de estudiar
nada nuevo.

- [x] Diagnóstico con datos (DIAGNOSTICO.md) — 2026-10-15
- [x] Herramientas instaladas y probadas: uv, python-chess, Stockfish 19,
      47 tests OK — 2026-10-15
- [x] Repo en GitHub: github.com/Ander0296/Ajedrez (público) — 2026-10-15
- [ ] chess.com configurado (docs/CHESSCOM.md, sección 2)
- [ ] Reglas de juego adoptadas (RUTINA.md): 10|5 o 15|10, máx. 2 por día,
      no rendirme antes de la 30
- [ ] Prácticas #01, #02 y #03 entregadas
- [ ] 5 partidas analizadas con `/partida`
- [ ] Primera `/semana` (línea de base en PROGRESO.md)

Termina cuando: todo lo de arriba + 2 semanas seguidas con la rutina.

## FASE 1 — Dejar de regalar · 764 → 1000

Objetivo: que mis partidas dejen de decidirse por piezas colgadas, amenazas
no vistas y regalos del rival que no cobro.

Qué se entrena (peso aproximado del tiempo):
- **Proceso (30%)**: el chequeo y el reloj, en cada partida. Partidas
  diarias para practicarlo sin presión.
- **Táctica dirigida (30%)**: tema de la semana en Problemas personalizados
  (horquillas, clavadas, descubiertas, piezas sueltas, mates en 1-2) + mis
  propias posiciones en repasos.
- **Partidas + análisis (25%)**: 2-3 por semana, todas con `/partida`.
- **Libro de Illescas (15%)**: los capítulos de defensa y táctica en
  TANDA; el resto en LECTURA (docs/ILLESCAS.md). Mates básicos y rey y peón.

Aperturas: solo los agujeros que muestran mis datos (f7 con negras, jugadas
raras). Nada de teoría nueva.

Termina cuando (todas):
- [ ] rápidas ≥ 1000 sostenido 4 semanas (PROGRESO.md)
- [ ] metas de proceso de `ajedrez.toml` cumplidas 3 semanas seguidas
      (s/jugada ≥ 15, jugadas < 3 s ≤ 10%, derrotas cortas ≤ 25%)
- [ ] ≤ 1,5 errores graves por partida y primer error grave en la jugada 18
      o después (`uv run ajedrez errores --ultimas 20`; hoy: 2,7 y ~10)
- [ ] prácticas #01-#03 graduadas (r3 bien) + oposición de rey y peón
- [ ] libro de Illescas terminado (lectura + tandas prioritarias)

## FASE 2 — Táctica y cálculo · 1000 → 1300

Objetivo: ver 2-3 jugadas adelante, cobrar todo lo que me regalan y no
regalar nada en la apertura.

- Táctica: combinaciones de 2-3 jugadas (desviación, atracción, eliminación
  del defensor, sobrecarga, jugada intermedia) y patrones de mate con
  nombre. Método: un set FIJO de problemas a mi nivel, repetido en ciclos
  cada vez más rápidos (la idea del método Woodpecker, a mi medida).
- Cálculo: visualizar sin mover; jugadas candidatas; buscar SIEMPRE la
  respuesta más fuerte del rival antes de decidir.
- Finales: rey y peón completo (oposición, triangulación, regla del
  cuadrado), Lucena y Philidor (drills de chess.com).
- Aperturas: mi repertorio escrito a ~8 jugadas con sus planes, en
  `repertorio/` (lo escribo yo; el profe lo verifica).
- Estrategia (introducción): actividad de las piezas, columnas abiertas,
  peones débiles, un plan simple cuando no hay táctica.
- Libro: "Ajedrez lógico, jugada a jugada" (Chernev) — 33 partidas con cada
  jugada explicada.

Termina cuando: rápidas ≥ 1300 sostenido 4 semanas · ≤ 1 error grave por
partida (20 partidas) · Lucena y Philidor graduados · repertorio escrito.

## FASE 3 — Planes, finales y primer torneo · 1300 → 1600

- Estrategia: las estructuras de peones de MI repertorio, puestos avanzados,
  alfil bueno/malo, espacio, profilaxis básica.
- Finales: de torre prácticos, piezas menores — "100 finales que hay que
  saber" (Jesús de la Villa).
- Partidas modelo: Capablanca y partidas comentadas.
- **Mundo real**: club en Bello/Medellín y PRIMER TORNEO presencial con
  ritmo lento (calendario de la Federación Colombiana / Liga de Antioquia
  vigente al llegar). Planilla, y análisis como siempre.
- Revisión del tiempo disponible con datos: ¿30 min alcanzan o conviene
  45-60?

Termina cuando: rápidas ≥ 1600 sostenido · primer torneo presencial jugado
y analizado.

## FASE 4 — Jugador de torneo · 1600 → 1800+ / rating FIDE

- Torneos válidos para FIDE en Colombia → rating FIDE.
- Repertorio más profundo, preparación según el rival, finales técnicos.
- Libros de entrenamiento de nivel y, si conviene, un entrenador humano.

Termina cuando: 1800+ en rápidas de chess.com sostenido, o rating FIDE
obtenido y en ascenso.

## Decisiones que se toman AL LLEGAR (a propósito no se fijan hoy)

- Libros y recursos de las fases 2-4 (se busca lo vigente; ver docs/RECURSOS.md).
- Si conviene un entrenador humano (F3-F4).
- El torneo concreto (calendario de ese momento).
- Si se sube el tiempo diario.
