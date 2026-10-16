# PRÁCTICA #01 — f7 bajo ataque: Ac4 + Cg5 (POSICIÓN ×3 + EXPLICAR)

Por qué: con negras, contra 1.e4 e5 2.Cf3 Cc6 3.Ac4 ganaste 7 y perdiste 22
(tu peor línea). Contra Ac4 + Cg5 perdiste 12 de 13, varias antes de la
jugada 10. Son partidas que se pierden antes de empezar a jugar.

Cómo se resuelve: SIN motor y sin mover piezas en un tablero de análisis.
Mirá el diagrama (está desde TU lado: jugás con negras) o armá la posición en
un tablero físico. Escribí la jugada, la respuesta que esperás de las blancas
y POR QUÉ. Las posiciones salen de tus partidas.

Si te trabás: `ToDo/apertura.md` y `ToDo/antes-de-mover.md` (paso 1).

## Posición A — juegan negras

1.e4 e5 2.Cf3 Cc6 3.Ac4 Cf6 4.Cg5

```
   ┌─────────────────┐
 1 │ T · · R D A C T │
 2 │ P P P · P P P P │
 3 │ · · · · · · · · │
 4 │ · · · P · A · · │
 5 │ · C · p · · · · │
 6 │ · · c · · c · · │
 7 │ p p p · p p p p │
 8 │ t · a r d a · t │
   └─────────────────┘
     h g f e d c b a
```
MAYÚSCULAS = blancas · minúsculas = negras · R rey · D dama · T torre · A alfil · C caballo · P peón

FEN `r1bqkb1r/pppp1ppp/2n2n2/4p1N1/2B1P3/8/PPPP1PPP/RNBQK2R b KQkq - 5 4`
Ver: https://www.chess.com/analysis?fen=r1bqkb1r/pppp1ppp/2n2n2/4p1N1/2B1P3/8/PPPP1PPP/RNBQK2R%20b%20KQkq%20-%205%204

1. ¿Qué amenazan las blancas? Escribí la jugada concreta y qué ganarían.
2. ¿Qué jugás? Tu jugada y la respuesta más probable de las blancas.
3. En tus partidas jugaste acá 4...d6 y 4...Ch5. ¿Qué jugada blanca castiga
   cada una y qué ganan?

Tu respuesta:
-

## Posición B — juegan negras

1.e4 e5 2.Cf3 Cc6 3.Ac4 Cf6 4.Cg5 d5 5.exd5

```
   ┌─────────────────┐
 1 │ T · · R D A C T │
 2 │ P P P · P P P P │
 3 │ · · · · · · · · │
 4 │ · · · · · A · · │
 5 │ · C · p P · · · │
 6 │ · · c · · c · · │
 7 │ p p p · · p p p │
 8 │ t · a r d a · t │
   └─────────────────┘
     h g f e d c b a
```

FEN `r1bqkb1r/ppp2ppp/2n2n2/3Pp1N1/2B5/8/PPPP1PPP/RNBQK2R b KQkq - 0 5`
Ver: https://www.chess.com/analysis?fen=r1bqkb1r/ppp2ppp/2n2n2/3Pp1N1/2B5/8/PPPP1PPP/RNBQK2R%20b%20KQkq%20-%200%205

1. Dos veces jugaste acá 5...Cxd5. ¿Qué jugada de las blancas te espera y
   por qué es tan peligrosa? (la idea, no hace falta calcular hasta el final)
2. ¿Qué jugás en su lugar, y qué idea tiene tu jugada?

Tu respuesta:
-

## Posición C — juegan negras (jugada única)

Igual jugaste 5...Cxd5, y vino 6.Cxf7 Rxf7 7.Df3+. Tu rey está en jaque y tu
caballo de d5 está atacado dos veces. Hay UNA sola jugada que mantiene la
partida; las demás pierden. En una partida tuya jugaste 7...Df6 y perdiste.

```
   ┌─────────────────┐
 1 │ T · · R · A C T │
 2 │ P P P · P P P P │
 3 │ · · D · · · · · │
 4 │ · · · · · A · · │
 5 │ · · · p c · · · │
 6 │ · · · · · c · · │
 7 │ p p r · · p p p │
 8 │ t · a · d a · t │
   └─────────────────┘
     h g f e d c b a
```

FEN `r1bq1b1r/ppp2kpp/2n5/3np3/2B5/5Q2/PPPP1PPP/RNB1K2R b KQ - 1 7`
Ver: https://www.chess.com/analysis?fen=r1bq1b1r/ppp2kpp/2n5/3np3/2B5/5Q2/PPPP1PPP/RNB1K2R%20b%20KQ%20-%201%207

1. ¿Cuál es la jugada? ¿Por qué 7...Df6 falla? ¿Y el otro movimiento de rey
   que parece natural?

Tu respuesta:
-

## Posición D — EXPLICAR (esta ya la conocés)

1.e4 e5 2.Cf3 Cc6 3.Ac4 Ac5 4.Cg5 — en tus partidas jugaste acá 4...Ch6 y
4...Cf6. En la sesión de setup te conté que 4...Dxg5 gana un caballo.
Ahora explicalo vos:

```
   ┌─────────────────┐
 1 │ T · · R D A C T │
 2 │ P P P · P P P P │
 3 │ · · · · · · · · │
 4 │ · · · P · A · · │
 5 │ · C · p · a · · │
 6 │ · · · · · c · · │
 7 │ p p p · p p p p │
 8 │ t c · r d a · t │
   └─────────────────┘
     h g f e d c b a
```

FEN `r1bqk1nr/pppp1ppp/2n5/2b1p1N1/2B1P3/8/PPPP1PPP/RNBQK2R b KQkq - 5 4`

1. ¿Por qué el caballo de g5 está indefenso? (qué piezas blancas podrían
   defenderlo y por qué no lo hacen)
2. ¿Por qué en la Posición A NO podés jugar ...Dxg5? (mirá qué cambió)
3. La regla general que te llevás para tus partidas, en una frase.

Tu respuesta:
-

---
Cuando termines, copiá y pegá:
/entrega la práctica 01 está en ejercicios/p01-defensa-de-f7.md, resolví las 4 posiciones sin motor
