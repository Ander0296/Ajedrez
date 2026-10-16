# Aperturas — qué estudiar y qué NO (Fase 1)

## La regla

A tu nivel, **las aperturas no deciden las partidas: las deciden las piezas
que se cuelgan en las jugadas 8-15.** El 31% de tus errores graves fue en la
apertura, pero casi nunca por no saber teoría: fue por no mirar qué
atacaba el rival. Por eso en la Fase 1:

1. **Principios** (ToDo/apertura.md) antes que jugadas de memoria.
2. **Tu repertorio actual se QUEDA**: 1.e4 con blancas, 1...e5 y 1...d5 con
   negras. Es sano y ya lo conocés. Cambiar de apertura ahora es empezar de
   cero sin ningún beneficio.
3. **Solo se estudian los agujeros que muestran TUS datos** (abajo). Nada de
   teoría por teoría.
4. Después de cada partida: Explorador de chess.com → ¿en qué jugada salí de
   la teoría y qué se juega ahí? Eso es toda la teoría que hace falta.

Todas las líneas de este archivo están verificadas con Stockfish 19.

## Tus datos (436 partidas)

| Yo con | Línea | G-P-T | Veredicto |
| --- | --- | --- | --- |
| blancas | 1.e4 e5 2.Cf3 Cc6 3.Ac4 (Italiana) | 33-23-0 | ✓ seguí así |
| blancas | 1.e4 d5 2.exd5 Dxd5 3.Cc3 (Escandinava) | 14-15-0 | se pierde en el medio juego, no en la apertura |
| blancas | 1.e4 e5 2.Cf3 d6 3.Ac4 (Philidor) | 5-8-0 | idem |
| blancas | 1.e4 e5 2.Cf3 Df6?! | 1-6-0 | la jugada rival es mala: ver abajo |
| negras | 1.e4 e5 2.Cf3 Cc6 3.Ac4 (Italiana) | **7-22-0** | ⚠ **el agujero: Práctica #01** |
| negras | 1.e4 e5 2.Cf3 Cc6 3.Cc3 | 5-10-0 | ⚠ medio juego |
| negras | 1.e4 e5 2.Dh5 Cc6 3.Ac4 (Pastor) | 5-7-1 | aceptable; ver abajo |
| negras | 1.e4 e5 2.d4 exd4 3.Dxd4 (Centro) | 9-3-1 | ✓ |
| negras | 1.d4 d5 2.Af4 (Londres) | 6-8-0 | medio juego |

## Con blancas: la Italiana (1.e4 e5 2.Cf3 Cc6 3.Ac4)

- **Contra 3...Ac5** (Giuoco Piano): plan simple c3 + d3 (o c3 + d4 si ya
  sabés los cambios), enroque, Te1, Cbd2-f1-g3. Sin apuro.
- **Contra 3...Cf6** (Dos caballos): **4.d3** es lo sólido (el motor la pone
  primera, +0,2). 4.Cg5 también es buena (+0,2) y a tu nivel gana muchas
  partidas por errores del rival — pero no la uses hasta entender la defensa
  correcta (Práctica #01): primero aprendés a defenderte, después a atacar.
- **Contra jugadas raras** (2...Df6, 2...f6, 2...d6): no hay que saber nada
  especial. Ejemplo verificado: tras 2...Df6 el motor da +1,1 a +1,2 para
  las blancas con desarrollo normal (3.Cc3, 3.Ac4 o 3.d4). Perdiste 6 de 7
  igual: no por la apertura, sino por lo que pasó después. **Las jugadas
  raras se castigan desarrollando, no atacando con una sola pieza.**

## Con negras contra 1.e4: 1...e5

- **Contra 3.Ac4**: tu agujero. Las respuestas a 4.Cg5 están en la
  **Práctica #01** (resolvela primero; cuando el profe la corrija, las
  jugadas se suman acá y a ToDo/apertura.md). Lo que ya sabés: tras
  3...Ac5 4.Cg5?! se juega **4...Dxg5**, y gana un caballo.
- **Contra 3...Ac5 4.c3**: 4...Cf6 (la mejor según el motor, +0,2 para las
  blancas = igualdad).
- **Contra la dama temprana** (1.e4 e5 2.Dh5 Cc6 3.Ac4): **3...g6**, que el
  motor pone primera, y tras 4.Df3, 4...Cf6. Regla: la dama que sale temprano
  se ataca con desarrollo, ganando tiempos.
- **Contra 2.d4 exd4 3.Dxd4**: 3...Cc6 con tiempo sobre la dama (ya te va bien).

## Con negras contra 1.d4: 1...d5

- Contra 2.c4: aceptar con 2...dxc4 (6-0 en tus partidas) o 2...e6.
- Contra la Londres (2.Af4): esquema simple ...Cf6, ...e6, ...c5, ...Cc6,
  ...Ad6. Evitá ...f6 temprano (debilita el rey: te pasó).

## Lo que NO se hace en la Fase 1

- Aprender aperturas nuevas "porque las juega un streamer".
- Memorizar líneas de 15 jugadas.
- Gambitos y "trampas" de videos como repertorio principal.
- Cambiar de apertura después de perder dos partidas.

## Fase 2: el repertorio escrito

En la Fase 2 escribís TU repertorio en `repertorio/` (una línea y la IDEA de
cada jugada, ~8 jugadas, con los planes del medio juego), y el profe lo
verifica con el motor y el Explorador. Ese archivo lo escribís vos: es
práctica, no apunte (el candado lo protege).
