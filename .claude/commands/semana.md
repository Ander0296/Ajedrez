---
description: Revisión semanal con datos — proceso, errores, rutina y el tema de la semana (domingo, 10 minutos)
argument-hint: [opcional: rating de problemas actual, días que entrené, cómo me sentí]
---

Revisión semanal. $ARGUMENTS

Aplicá la regla **Revisión semanal** de CLAUDE.md (no lo leas con Read: ya
lo tenés cargado). En tablas y sin discurso.

1. Corré `uv run ajedrez resumen --dias 7` (y, si es la última semana del
   mes, también `--dias 30`).
2. Leé PROGRESO.md (últimas 4 filas), las partidas de la semana en
   PARTIDAS.md, EJERCICIOS.md y los criterios de la fase actual en RUTA.md.
3. Lo que la API no ve, preguntámelo en UNA sola pregunta (si no vino en
   el comando): rating de problemas de hoy, cuántos días entrené de 7, qué
   bloques de la rutina hice y una línea de cómo me sentí.
4. Mostrame:
   - números de la semana vs. la anterior (rating, partidas, analizadas);
   - proceso vs. metas de `ajedrez.toml [metas]` (✓ / ✗);
   - errores graves de la semana por categoría de la TAXONOMÍA;
   - rutina: lo planeado vs. lo hecho;
   - criterios de salida de la fase: cumplidos / pendientes.
   Si algo está en rojo, primero y sin suavizarlo.
5. Decidí UNA cosa: el **tema de la semana** (del patrón de errores; en
   chess.com → Problemas personalizados con ese tema) y, solo si hace
   falta, UN ajuste de la rutina.

Después: fila nueva en PROGRESO.md, tema de la semana y "Última /semana"
en el INICIO RÁPIDO de GUIA.md, y PATRONES de PARTIDAS.md recalculados
(máx. 8 líneas). Si se cumplieron los criterios de fase, proponeme el
cambio de fase: lo decido yo.

Cerrá con el bloque `▶ SIGUE`.
