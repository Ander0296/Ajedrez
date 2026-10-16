# Cómo vamos a aprender (y por qué así)

## La idea central

**El ajedrez no se aprende jugando mucho: se aprende jugando, analizando y
entrenando lo que falló.** Tu historial lo demuestra mejor que cualquier
libro: 418 partidas en 11 meses y el rating en el mismo lugar. Cada partida
sin analizar repite los mismos errores con la misma velocidad.

```
         ┌──────────────── JUGAR (lento, con el chequeo) ───────────────┐
         │                                                              │
 ENTRENAR LO QUE FALLÓ                                         ANALIZAR
 (tema de la semana, tus                              (primero vos, sin motor;
  posiciones en repasos)  ◄──────── /partida ────────  después Game Review y Claude)
```

## Lo que dice la investigación (en corto)

- **Práctica deliberada**: en el estudio de Charness y colaboradores (2005)
  con cientos de jugadores, lo que mejor predecía el nivel no era la cantidad
  de partidas sino las horas de **estudio serio a solas** (analizar,
  resolver, estudiar). Jugar cuenta, pero sin análisis rinde poco.
- **Patrones**: Chase y Simon (1973) mostraron que los jugadores fuertes no
  calculan más: **reconocen** configuraciones que ya vieron miles de veces.
  Por eso los problemas por tema y los repasos de TUS posiciones: construyen
  esa biblioteca de patrones.
- **Recordar es mejor que releer** (efecto de la evaluación, Roediger y
  Karpicke, 2006): intentar resolver antes de mirar la solución fija más que
  leerla. Por eso primero autoanálisis, "Reintentar" en el Game Review y
  exámenes en frío.
- **Espaciar** (efecto del espaciado): repasar a los 3 días, a las 2
  semanas y al mes fija más que repasar diez veces el mismo día. Por eso el
  sistema de repasos.

## Los frentes y su peso en la Fase 1

| Frente | Peso | Cómo | Por qué |
| --- | --- | --- | --- |
| Proceso (el chequeo, el reloj) | 30% | en cada partida, sobre todo en las Diarias | es tu cuello de botella (DIAGNOSTICO.md) |
| Táctica dirigida | 30% | problemas del tema de la semana + tus posiciones | patrones que sí aparecen en tus partidas |
| Partidas + análisis | 25% | 2-3 por semana, todas analizadas | la fuente de todo lo demás |
| Libro + técnica | 15% | Illescas por prioridad, drills de mates y finales | la base que faltaba |
| Aperturas | ~0% aparte | solo tus agujeros, dentro del análisis | no deciden partidas a tu nivel |

## Quién hace qué

| Vos | Claude (el profe) |
| --- | --- |
| Jugás, con el chequeo | Detecta qué partidas faltan analizar |
| Analizás PRIMERO, sin motor | Compara con Stockfish y encuentra el error de PROCESO detrás de cada error de jugada |
| Resolvés las prácticas a mano | Las crea con TUS posiciones, verificadas con el motor, y agenda los repasos |
| Hacés los problemas y drills | Elige el tema de la semana según tus errores |
| Leés el libro | Explica las tandas y las conecta con tus partidas |
| Decidís | Propone (cambio de fase, bajas, exámenes) y dice siempre qué sigue |

## Cómo se mide el progreso

- **El rating es un indicador lento y ruidoso** (±50 en una semana no dice
  nada). Se mira la tendencia de 4 semanas en PROGRESO.md.
- **Los indicadores que se mueven primero son los de PROCESO**: segundos por
  jugada, jugadas en < 3 s, derrotas cortas, errores graves por partida, en
  qué jugada llega el primero. Si esos mejoran, el rating viene detrás.
- Las prácticas graduadas y los exámenes dicen qué conceptos se sostienen.

## Los errores típicos del adulto que quiere mejorar (y cómo los evita el sistema)

| Error | El sistema |
| --- | --- |
| Jugar mucho y rápido | máx. 2 partidas por día, 10\|5, regla de las dos derrotas |
| No analizar | ninguna partida sin `/partida` |
| Mirar el motor antes de pensar | autoanálisis primero; Claude no muestra el motor antes |
| Estudiar aperturas de más | solo los agujeros de tus datos |
| Cambiar de plan cada semana | un solo ajuste por semana, en `/semana` |
| Obsesionarse con el rating | metas de proceso + tendencia de 4 semanas |
| Problemas al azar | tema de la semana, sacado de tus errores |
| Aprender sin repasar | repasos espaciados de tus propias posiciones |
