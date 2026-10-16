# DIAGNÓSTICO — Buti-G

Foto fechada de cómo jugás, con datos. No se reescribe: cada diagnóstico
nuevo se agrega ARRIBA con su fecha, para poder comparar.
Se repite con: `uv run ajedrez resumen --todo` (estadísticas de proceso) y
`uv run ajedrez errores --ultimas 60 --dias 60` (Stockfish).

---

## 2026-10-15 — Diagnóstico inicial

Fuente: las 440 partidas de la API pública de chess.com (436 rápidas 10|0,
nov-2025 → oct-2026) + Stockfish 19 sobre las últimas 60 (29-sep → 15-oct).

### La foto

| | |
| --- | --- |
| Rápidas | **764** (máx. 819 el 2025-12-04) · 213 G / 213 P / 10 T |
| Problemas | **1477** (máx. 1550, mín. 749 en nov-2025) · Puzzle Rush récord 19 |
| Control | 10\|0 en 436 de 440 partidas |
| Rivales | ~730 de media |

Llegaste a ~750 en tus primeras 22 partidas (nov-2025). Desde ahí, **11
meses planos entre 650 y 820 con 418 partidas más**. Diciembre: 258
partidas (32 en un solo día) y terminaste el mes más abajo que lo empezaste
(764 → 731). Mientras tanto, los problemas subieron de 749 a 1550.

**Lectura:** sabés ver táctica cuando te avisan que hay una. En partida no
la usás. El cuello de botella no es lo que sabés: es CÓMO jugás. Y eso es una
buena noticia, porque se corrige más rápido que la falta de conocimiento.

### Hallazgo 1 — Tus derrotas se deciden temprano y por material

- **72% de tus derrotas** (154/213) tienen una pérdida de material (≥ 2
  puntos) que nunca recuperaste. Jugada mediana: la 13. 98 antes de la 15.
- **54% de tus derrotas duran 20 jugadas o menos** (116/213). Tus victorias
  duran una mediana de 28.
- Con Stockfish (últimas 60 partidas): **2,7 errores graves por partida**,
  52 de 60 partidas con al menos uno, y el **primero llega, de mediana, en
  la jugada 9-10**. Por fase: 57% medio juego, 31% apertura, 12% final.

### Hallazgo 2 — Jugás rápido y te sobra el reloj

- **6,9 segundos de mediana por jugada** (desde la 6ª). El 23% de tus
  jugadas las hacés en menos de 3 segundos.
- Perdés con el **67% del reloj sin usar** (mediana). En 155 de 213 derrotas
  te sobraba más de la mitad. Perdiste por tiempo 4 veces en 440 partidas.
- Con 10 minutos y ~35 jugadas tenés ~17 s por jugada. Usás menos de la mitad.
- PERO ojo con la conclusión fácil: de tus errores graves recientes, el 35%
  los pensaste 15 segundos o más. **Pensar más no alcanza: hay que pensar
  con un orden** (qué hizo el rival, qué dejo colgado). Eso es el chequeo.

### Hallazgo 3 — No ves lo que hace el rival… para mal y para bien

Tipos de error grave (Stockfish, 162 errores en 60 partidas, pista automática):

| Tipo | % | Qué significa |
| --- | --- | --- |
| amenaza del rival | 29% | su última jugada amenazaba algo y no lo viste |
| **no castigaste su error** | **29%** | el rival dejó algo y no lo cobraste |
| pieza regalada | 19% | dejaste una pieza capturable |
| táctica del rival con jaque | 12% | jaque doble, horquilla con jaque |
| material regalado | 7% | peón o cambio perdido |
| permitiste mate | 4% | |

El 71% son errores DEFENSIVOS (no mirar qué hace el rival) y el 29% son
OFENSIVOS (no mirar qué te regaló). Las dos cosas se arreglan con la misma
pregunta, antes de cada jugada: **"¿qué cambió con su última jugada?"**.
Ejemplos tuyos (verificados con el motor): el 1-oct el rival dejó su alfil
de g5 capturable — si su caballo de f3 recapturaba, tu alfil de g4 se comía
su dama — y jugaste 11...Df4 en vez de 11...Dxg5 (−5,7 para él). El 30-sep,
con ventaja ganadora (+3,6), jugaste 4.g3?? y la dama rival entró con jaque
en e4 atacando también tu torre de h1 (−5,3).

### Hallazgo 4 — Te rendís demasiado pronto

- **85 rendiciones antes de la jugada 20**, con una mediana de -3 de
  material (una pieza). 43 veces te rendiste con MENOS de una pieza de
  desventaja.
- Mientras tanto, el **46% de tus victorias (99 de 213) llegaron porque el
  rival se rindió**, y otras 29 porque abandonó. A tu nivel, las partidas
  se devuelven todo el tiempo: rendirse con una pieza de menos en la jugada
  15 es regalar la mitad de esas partidas.
- 43 mates recibidos: 21 antes de la jugada 20, y **24 con material igual
  o a favor** — el rey se cae por no mirar las amenazas, no por ir perdiendo.
- 13 partidas perdidas por irte (abandono): rating regalado.

### Hallazgo 5 — Un agujero de apertura concreto: f7

- Con blancas: 1.e4 siempre, y la Italiana te va bien (33-23 tras
  1.e4 e5 2.Cf3 Cc6 3.Ac4). Contra la escandinava, 14-15.
- **Con negras contra 1.e4 e5 2.Cf3 Cc6 3.Ac4: 7 G – 22 P**, tu peor línea.
  **Contra Ac4 + Cg5 (ataque a f7): 12 derrotas en 13 partidas**, varias en
  5-10 jugadas: 4...d6 5.Cxf7, 4...Ch5 5.Axf7+, 5...Cxd5 6.Cxf7…
  Y dos veces el rival jugó un Cg5 que se podía capturar gratis y te
  defendiste en vez de cobrarlo (Hallazgo 3 otra vez).
  → La solución no está acá a propósito: la encontrás vos en la
  **Práctica #01**.
- Con negras contra 1.e4 e5 2.Cf3 Cc6 3.Cc3: 5-10. Contra la jugada rara
  2...Df6 (con blancas): 1-6. Patrón: piloto automático contra lo que no
  conocés. La regla de apertura (ToDo/apertura.md) cubre eso.

### Hallazgo 6 — Volumen sin análisis

- **45 de tus 67 días de juego tuvieron más de 2 partidas.** Tu máximo (819)
  fue el día de 32 partidas.
- No hay "tilt" clásico: después de perder ganás la siguiente el 53%;
  después de ganar, el 45%. El problema no es emocional: es que **una
  partida sin análisis no enseña nada**, y jugaste 436.

### Qué significa para el plan (en 5 líneas)

1. **Proceso antes que conocimiento**: el chequeo antes de mover
   (ToDo/antes-de-mover.md) y usar el reloj. Es lo que más puntos da y lo
   más rápido. Práctica #03.
2. **Rápidas con incremento (10|5 o 15|10), máximo 2 partidas por día,
   cada una analizada** (primero vos, después el motor).
3. **Arreglar f7** (Práctica #01) y castigar los regalos del rival.
4. **No rendirse antes de la jugada 30** salvo dama de menos sin
   compensación o mate inevitable.
5. **Táctica dirigida a TUS errores**, no problemas al azar: el tema de la
   semana sale de `/partida` y `/semana`.

### Metas de proceso de la Fase 1 (vs. hoy)

| Indicador | Hoy | Meta F1 |
| --- | --- | --- |
| segundos por jugada (mediana) | 6,9 | ≥ 15 |
| jugadas en < 3 s | 23% | ≤ 10% |
| reloj sin usar al perder | 67% | ≤ 40% |
| derrotas en ≤ 20 jugadas | 54% | ≤ 25% |
| errores graves por partida (Stockfish) | 2,7 | ≤ 1,5 |
| jugada del primer error grave (mediana) | ~10 | ≥ 18 |
| rendiciones antes de la jugada 20 | 85 en total | 0 |
| días con más de 2 partidas | 45 de 67 | 0 |
