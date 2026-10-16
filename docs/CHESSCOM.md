# chess.com Diamante — cómo usarlo para MEJORAR, no solo para jugar

> Verificado contra el Centro de ayuda de chess.com (página de membresías,
> actualizada el 21-jul-2026) y contra tus datos de la API. Los menús
> cambian de nombre seguido: si no encontrás algo, buscalo por el nombre en
> inglés que va entre paréntesis.

## 1. La idea en una línea

chess.com sirve para tres cosas: **JUGAR, REVISAR y ENTRENAR**. Hasta hoy
usaste casi todo tu tiempo en jugar (436 partidas, 32 en un solo día). El
plan reparte tus 30 minutos así: **~35% entrenar, ~35% revisar, ~30% jugar**.
Pagás Diamante justamente por las herramientas de revisar y entrenar.

## 2. Qué te da Diamante

| Herramienta | Qué es | Para qué la usás vos | Cuándo |
| --- | --- | --- | --- |
| **Game Review ilimitado + coach en TODAS tus jugadas** (solo Diamante) | El análisis de la partida con explicaciones en palabras | Paso 2 del protocolo de análisis | Después de cada partida valorada |
| **Insights** (solo Diamante) | Estadísticas de todas tus partidas: por fase, por apertura, por hora | Ver tendencias que una partida sola no muestra | 1 vez al mes (`/semana` de fin de mes) |
| **Análisis configurable** (solo Diamante) | Motor más profundo y ajustable en el tablero de análisis | Revisar posiciones de tus partidas | Al analizar, nunca durante una partida |
| Problemas ilimitados · **Problemas personalizados** · Puzzle Rush · Batalla | Táctica | El **tema de la semana** | 4-5 días por semana |
| Lecciones y videoteca ilimitadas | Cursos cortos con video + desafíos | Temas nuevos de cada fase | 1 vez por semana |
| **Práctica** (*Practice / Drills*) y Finales | Posiciones para jugar contra la máquina con un objetivo | Mates básicos, finales (técnica) | Jueves |
| Explorador de aperturas completo (incluye tus partidas) | Base de datos de partidas | Ver dónde saliste de la teoría | Al analizar |
| 100+ bots y partidas ilimitadas contra el Coach | Rivales sin rating en juego | Probar una apertura nueva sin arriesgar | Cuando aprendas algo nuevo |
| Estadísticas avanzadas | Más números en tu perfil | — | Poco |

**Lo que NO necesitás**: la **Liga** (*Leagues*: premia jugar mucho, que es
lo contrario de este plan; estás 3º en la Liga Champion y eso no te sube el
rating) y las rachas de partidas. La racha (18 días hoy) mantenela con
problemas, no con partidas.

## 3. Configuración inicial (10 minutos, una vez)

- [ ] **Desactivar los premovimientos** (*premoves*) en la configuración de
      juego en vivo. Un premove es mover sin mirar la jugada del rival:
      exactamente lo que el chequeo viene a corregir.
- [ ] **Coordenadas en el tablero**: activadas (para leer jugadas y el libro).
- [ ] **Problemas**: dificultad estándar (*Standard*) por ahora; difícil
      (*Hard*) en la Fase 2. La dificultad se ajusta en la configuración de
      problemas y vale también en la app.
- [ ] **Tablero de análisis**: ubicá el interruptor del motor (*engine*):
      apagado para tu autoanálisis, prendido después.
- [ ] **Control de tiempo**: dejá **10|5** como control de rápidas por
      defecto al buscar partida (o 15|10 los días con más tiempo).
- [ ] **Diarias**: 1-2 partidas a 3 días por jugada.

## 4. JUGAR con propósito

- **Rápidas 10|5 o 15|10**, máximo 2 por día, dos derrotas seguidas = parar
  (reglas completas en RUTINA.md). Tu rating de rápidas es uno solo: cambiar
  de 10|0 a 10|5 no te hace empezar de cero.
- **Diarias** (*Daily*): una jugada por día con el chequeo completo. Es el
  mejor gimnasio para el proceso: sin reloj, sin excusas.
- **Bots y Coach** (Jugar → Computadora): para estrenar una apertura nueva
  o practicar un final sin arriesgar rating. Para una posición concreta,
  cargala con el FEN en el tablero de análisis y buscá la opción de jugarla
  contra la computadora.

## 5. REVISAR (lo que más te va a subir)

### Game Review — después de cada partida valorada

1. **Primero tu autoanálisis sin motor** (`ToDo/despues-de-la-partida.md`).
   Si abrís el Game Review antes, ya no hay nada que entrenar.
2. **Momentos clave** (*Key moments*): en cada error tuyo, **Reintentar**
   (*Retry*) ANTES de ver la mejor jugada. Es un problema hecho a tu medida.
3. **Explicaciones del coach**: con Diamante las tenés en TODAS tus jugadas.
   Leelas en tus errores graves y en las jugadas del rival que no castigaste.
4. Las etiquetas: Brillante (!!), Genial (!), Mejor, Excelente, Buena,
   Teoría (*Book*), Imprecisión (?!), Error (?), **Oportunidad perdida**
   (*Miss*: el rival se equivocó y no lo aprovechaste — el 29% de tus
   errores graves) y **Error grave** (??).
5. **Precisión** (*Accuracy*): no te obsesiones. Tu mediana es 76 al ganar y
   65 al perder: las partidas se deciden por 2-3 jugadas, no por el promedio.

### Insights — una vez al mes

- **Fases de la partida**: tu precisión en apertura, medio juego y final, y
  cómo terminan tus partidas en cada fase.
- **Aperturas**: tus 10 aperturas más jugadas, con blancas y con negras, y la
  "maestría" (cuántas jugadas de teoría hacés de media).
- **Resultados por hora del día**: si rendís peor de noche, se nota acá.
- En `/semana` de fin de mes se comparan con `uv run ajedrez resumen --dias 30`.
- Cuentan las partidas de 10+ jugadas, ajedrez normal y no contra la máquina.

### Tablero de análisis, Explorador y Biblioteca

- **Análisis**: cargar una partida o un FEN (los enlaces de los ejercicios
  del repo abren directamente acá).
- **Explorador** (*Explorer*): después de cada partida, mirá en qué jugada
  saliste de la teoría y qué se juega ahí. Esa es TODA la teoría de
  aperturas que necesitás en la Fase 1.
- **Biblioteca / Colecciones**: guardá tus mejores partidas y las posiciones
  de tus errores.

## 6. ENTRENAR

### Problemas (*Puzzles*)

- **Personalizados** (*Custom Puzzles*), en el menú Problemas: elegís el
  tema. Es el corazón del entrenamiento: el **tema de la semana** sale de tus
  errores (`/semana`). No dan rating, a propósito: el foco es el patrón.
  Ojo: en sep-2026 chess.com cambió su clasificación de temas y por un
  tiempo puede haber menos temas disponibles; si falta el que buscás, usá
  el más cercano.
- **Valorados** (*Rated*): 2 días por semana. Medís el progreso.
- **Puzzle Rush / Batalla**: 1 vez por semana, por diversión. Premian la
  velocidad, que es justo lo que estás corrigiendo.
- Cómo: calculá la línea entera ANTES de tocar la pieza; si fallás, no pases
  al siguiente sin entender por qué.

Temas de la Fase 1 (nombres aproximados; en inglés entre paréntesis):
piezas colgadas / material suelto (*hanging piece*), horquilla (*fork*),
clavada (*pin*), ataque a la descubierta (*discovered attack*), enfilada
(*skewer*), mate en 1 y en 2 (*mate in 1/2*), mate del pasillo (*back rank
mate*), y jugadas defensivas (*defensive move*).

### Lecciones (*Lessons*)

Cursos cortos: video + desafíos interactivos, por nivel. Cómo sacarles jugo:
el video una vez, los desafíos SIN pistas, y al día siguiente repetís los
que fallaste. Por fase: F1 → táctica básica, mates básicos, principios de
apertura, defensa · F2 → cálculo, finales de rey y peón, "Endgame Patterns"
(oposición, triangulación, Lucena y Philidor) · F3 → estrategia y planes.

### Práctica (*Practice / Drills*) — chess.com/practice

Posiciones para jugar contra la computadora con un objetivo (dar mate,
ganar, hacer tablas). Es donde la técnica se vuelve automática: mates
básicos (Práctica #02), rey y peón (F1), Lucena y Philidor (F2). Regla: un
drill está dominado cuando sale **3 veces seguidas**.

### Visión (*Vision*) — chess.com/vision

Entrenador de coordenadas. 5 minutos, alguna vez por semana al principio:
ayuda a leer el libro y a ver las casillas sin pensar.

## 7. Lo que NO hacer

- Jugar bullet o blitz "para mejorar".
- Maratones de partidas (tu récord: 32 en un día; tu pico de rating fue ese
  día, y lo devolviste).
- Mirar la evaluación o el Game Review antes de pensar vos.
- Usar Puzzle Rush como entrenamiento principal.
- Perseguir la Liga o la racha de partidas.
- Obsesionarte con la precisión.
- Seguir jugando después de dos derrotas seguidas.
- Aprender aperturas de videos de "trampas" en vez de por principios.

## 8. Fair play — lo que está permitido

- **En vivo**: ninguna ayuda externa, de ningún tipo.
- **Diarias**: SÍ libros y bases de aperturas (el Explorador incluido). NO
  motores, NO bases de finales (*tablebases*), NO ayuda de otras personas.
  Por eso Claude no analiza una Diaria que todavía se está jugando.

## 9. Atajos

| Qué | Dónde |
| --- | --- |
| Problemas | chess.com/puzzles |
| Práctica (drills) | chess.com/practice |
| Lecciones | chess.com/lessons |
| Tablero de análisis | chess.com/analysis |
| Explorador | chess.com/analysis/explorer |
| Colecciones | chess.com/analysis/collections |
| Tus Insights | chess.com/insights/buti-g |
| Visión | chess.com/vision |
