# Reconstrucción formal del mecanismo, 2026-08-19

Síntesis de todo lo investigado hasta ahora (identificación de las 34 películas,
criterio de intrusos, barrido de 792 candidatos, búsqueda dirigida sobre Goonies/
Sharknado/Raiders). No se ejecuta ninguna búsqueda nueva ni prueba contra el
oráculo en este documento; es solo organización de lo ya encontrado, separado por
nivel de certeza.

## 1. Hechos confirmados

Verificados directamente (fuente primaria del propio puzzle, blockchain pública, o
fuente externa independiente que no dependía de esta investigación).

1. El puzzle consiste en 34 paneles numerados, cada uno un fotograma de una
   película distinta, publicados en orden fijo (`bitcoinmovieenigma.com/rules`,
   `clues/author-posts.md`).
2. Regla textual exacta del autor: "Transform 'somehow' each movie title into an
   English BIP-0039 seed word." El input declarado es el **título**, no la trama,
   el reparto ni ningún otro elemento de la película.
3. Regla textual exacta: de las 34 palabras resultantes, 10 son "intrusas" y deben
   descartarse usando información de la página de IMDb de cada película, dejando
   una mnemonic BIP39 de 24 palabras en el orden de los paneles.
4. Escrow `bc1q94ecsn0qk8lap2gefrycnms3ruepy889z969a6`: financiado el 2022-04-08
   (100,000 sats), sin gastar hasta el 2026-08-19 (verificado on-chain, lectura
   directa a mempool.space).
5. Las 34 películas están identificadas con confianza razonable (`data/films.csv`);
   los 2 paneles antes indeterminados (11 = Godzilla 1998, 34 = The Human
   Centipede (First Sequence)) se confirmaron con fuentes independientes que
   describían la escena/decorado sin haber sido inducidas por este panel
   específico.
6. `tools/oracle.py --selftest` pasa: la derivación (BIP84 principal, con BIP49/
   BIP44 y 3 rutas crudas como respaldo, ya que el autor nunca declara la ruta)
   está certificada contra los vectores de prueba públicos de BIP39/BIP84.
7. De las 34 palabras candidatas literales (substring dentro de una sola palabra
   del título, sin cruzar espacios), 31 tienen al menos una coincidencia; 3
   títulos no tienen ninguna: **The Goonies, Sharknado, Raiders of the Lost Ark**
   (comprobación exhaustiva contra las 2048 palabras de la wordlist, no una lista
   parcial).
8. Ninguno de esos 3 títulos tiene una coincidencia BIP39 en: títulos
   internacionales/alternativos, título de trabajo original, ni taglines
   oficiales de IMDb (comprobado explícitamente para los 3).
9. El sitio del puzzle no contiene texto oculto adicional por panel más allá de la
   imagen (verificado en el HTML fuente de varios paneles).
10. No existe una versión archivada anterior de la página de reglas en Wayback
    Machine; no hay evidencia de que el texto de la regla haya cambiado.
11. El barrido completo de 792 candidatos generados bajo la hipótesis de intrusos
    de abajo (16 palabras literales fijas + 5 paneles ambiguos + 3 palabras
    adivinadas para los paneles sin evidencia) dio **0 coincidencias** contra el
    oráculo (`analysis/tested.md`).

## 2. Hipótesis fuertes (bien sustentadas, no probadas)

Cosas que tienen evidencia real y consistente a favor, pero que solo un `MATCH`
del oráculo puede confirmar del todo.

### H1: criterio de intrusas: "comparte director o actor principal con otro panel de esta misma lista"

- Marca exactamente 10 de 34 paneles: {1, 2, 10, 14, 16, 17, 20, 22, 25, 33}, vía
  Stanley Kubrick (5 películas), John McTiernan (2), Tom Cruise (2) y Ryan Gosling
  (2) (`analysis/intruder_repeat_check.py`).
- Es el primer criterio, de unos 30 probados en total, que da un split exacto
  24/10.
- Validación cruzada independiente: de los paneles con palabra ambigua, 4 de 5
  quedan fuera de este conjunto de intrusas (Paths of Glory, el título de Cruise/
  De Palma en el panel 10, Eyes Wide Shut, A Clockwork Orange). Si el criterio
  fuera espurio, no habría razón para que coincidiera tanto con el problema de
  ambigüedad de palabras.
- El barrido de 792 candidatos NO lo refuta: de esos 24 paneles "keeper", 3 tenían
  palabra puramente adivinada (Goonies, Sharknado, Raiders). El resultado 0/792 es
  consistente con que esas 3 adivinanzas estén mal, no con que el criterio de
  intrusas esté mal.

### H2: para la mayoría de los títulos, la transformación es "substring BIP39 literal dentro de una palabra del título"

- Confirmado empíricamente en 31 de 34 casos.
- Cuando hay una coincidencia exacta de palabra completa del título (no solo un
  substring parcial) disponible, parece preferirse sobre un substring parcial. Por
  ejemplo: "A Clockwork Orange" da "orange" (coincide con la palabra completa
  "Orange") en vez de "clock"/"range"/"work" (todos substrings parciales); "Eyes
  Wide Shut" da "wide" en vez de "eye"; "Paths of Glory" da "glory" en vez de
  "path". Esto es un patrón observado en los datos disponibles, no una regla
  confirmada por el autor.

## 3. Hipótesis débiles (no descartadas, pero sin evidencia real que las respalde)

- **"chunk"** para The Goonies: nombre real de un personaje (Lawrence "Chunk"
  Cohen), pero nada en el texto del puzzle indica que los nombres de personajes
  cuenten como "el título transformado."
- **"tornado"** para Sharknado: tema central de la película, mismo problema:
  ninguna base textual que conecte "tema" con "título."
- Cualquiera de las 11 palabras temáticas probadas para Raiders of the Lost Ark
  (whip, snake, gold, hat, desert, skull, cave, stone, sand, jungle, crystal): sin
  ninguna base para preferir una sobre otra. **Se recomienda no usarlas más como
  candidatas**: ya fueron probadas contra el oráculo (dentro del barrido de 792) y
  fallaron.
- Que las 5 palabras ambiguas restantes (Star Trek: motion/picture; Valerian:
  city/planet/sand; Ordinary People: ordinary/people; Toy Story: story/toy; Human
  Centipede: human/first/man) se resuelvan por "preferir palabra completa" no
  ayuda en varios casos porque **ambas** opciones son coincidencias de palabra
  completa (Ordinary People, Toy Story, Human Centipede, Star Trek). No hay
  todavía una regla que las desempate.

## 4. Datos desconocidos

Cosas sobre las que no hay ninguna evidencia, ni fuerte ni débil, solo ausencia de
información.

- La palabra real (si existe) para The Goonies, Sharknado y Raiders of the Lost
  Ark: cero evidencia verificable encontrada tras revisar título, títulos
  alternativos, título de trabajo, taglines, y fuentes externas.
- La regla exacta que decide, entre 2-4 palabras BIP39 igualmente válidas dentro
  de un mismo título, cuál es la "correcta" (afecta a 5 paneles).
- El campo exacto de IMDb al que se refiere la regla de intrusas: la coincidencia
  con "director o actor principal repetido" es una hipótesis propia, no una cita
  textual del autor; el autor nunca dice "director" ni "actor" explícitamente.
- Si existe passphrase BIP39 (el oráculo asume que no).
- Si el orden de los paneles corresponde 1:1 al orden de las palabras en la
  mnemonic sin ninguna excepción (el texto del autor lo afirma, pero no hay forma
  de verificarlo hasta tener un candidato completo correcto).
- Cualquier instrucción adicional del autor sobre el mecanismo: no se encontró
  ninguna, en ningún canal público revisado (sitio, Nostr, commits del repo,
  discusión externa indexada).

## 5. Qué tendría que descubrirse para resolverlo

En orden de lo que más bloquea el progreso:

1. **Una palabra real, con evidencia (no adivinada), para The Goonies, Sharknado y
   Raiders of the Lost Ark.** Esto es lo único que bloquea totalmente el intento:
   sin esto, ni siquiera se puede construir un candidato completo de 24 palabras
   para probar. La vía más prometedora, dado que no hay más pistas públicas, es
   preguntar directamente al autor o encontrar a alguien que haya avanzado más en
   privado, no más búsqueda de patrones desde este lado.
2. **Una regla que desempate las 5 palabras ambiguas restantes** (o, en su
   defecto, aceptar seguir probando las combinaciones; ya cubierto una vez en el
   barrido de 792, se puede repetir combinado con las 3 palabras nuevas).
3. **Confirmación independiente del criterio de intrusas (H1).** La única forma de
   confirmarlo de verdad es un `MATCH` real; si tras resolver el punto 1 sigue sin
   haber coincidencia, eso sería la primera evidencia real en contra de H1, y
   habría que retomar la búsqueda de un criterio distinto entre los ~30 ya
   descartados o uno nuevo.

No hay ningún atajo computacional para el punto 1: es un vacío de información, no
un problema de búsqueda más grande. Los puntos 2 y 3 sí son de naturaleza
combinatoria y ya están acotados (unas pocas decenas a unos pocos cientos de
candidatos una vez resuelto el punto 1).

## 6. Actualización, 2026-08-19 (más tarde el mismo día): panel 8 corregido

El panel 8 ("The Goonies", confianza "probable") era una identificación incorrecta.
Se descargó el fotograma real servido en `bitcoinmovieenigma.com/blog/08` y se pasó
por Bing Visual Search; la descripción devuelta por el propio motor coincide
palabra por palabra con la escena (dos hombres con gabardina y sombrero bajo
paraguas negros junto al agua): es **Shutter Island (2010, dir. Martin Scorsese)**,
no The Goonies. Detalle completo y fuente en `analysis/tested.md`.

Dos consecuencias directas:

1. **Se resuelve una de las 3 palabras huecas.** "Shutter Island" contiene "island"
   como palabra BIP39 completa y literal (índice 948 de la wordlist), con el mismo
   patrón de "palabra completa preferida" que "orange", "wide", "glory" o "human"
   en otros paneles. Esto no es una adivinanza: es una coincidencia literal
   verificada. El hueco de palabras adivinadas baja de 3 a 2 (Sharknado, Raiders of
   the Lost Ark).
2. **El criterio H1 de intrusos queda en duda.** El director de Shutter Island,
   Martin Scorsese, también dirige el panel 13 (Goodfellas). Aplicando la misma
   lógica que ya contaba a McTiernan, Cruise y Gosling como disparadores válidos
   con solo 2 películas cada uno, el par Scorsese debería contarse igual --y al
   hacerlo, el criterio marca 12 paneles, no 10. No hay ninguna razón, dentro de la
   lógica original de H1, para excluir este par sin también excluir a los otros 3.
   Esto no se ha resuelto: sigue abierto como el nuevo lead #2.

Este hallazgo confirma el patrón de fondo que ya sugería el propio archivo: una
confianza "probable" (frente a "confirmed") no es garantía, y vale la pena
re-verificar visualmente cualquier identificación de menor confianza antes de
construir más hipótesis encima de ella.

## 7. Actualización, 2026-08-19 (más tarde el mismo día): panel 11 corregido

El panel 11, identificado como Godzilla (1998) con confianza "confirmed" y con una
fuente externa independiente que describía la escena exacta, fue corregido a **Ace
Ventura: When Nature Calls (1995, dir. Steve Oedekerk, protagonizada por Jim
Carrey)** a partir de una identificación visual directa del usuario sobre el
fotograma real, no de una búsqueda de este lado. Antes de aceptar el cambio,
contrasté ambas hipótesis: la escena de Godzilla (latas de atún Bumble Bee en un
naufragio en Panamá) tiene una fuente externa independiente que la describe sin
haber sido inducida por este panel; lo único encontrado para Ace Ventura es la
frase hablada "Bumblebee tuna!" del personaje, no una escena documentada con latas
físicas. Se lo señalé al usuario, quien confirmó que su identificación es visual
directa (no una asociación por la frase) y pidió mantener la corrección. Aplicando
el mismo estándar que este repositorio ya usa para este tipo de panel (una persona
que vio la película reconoce el fotograma, el método que cerró originalmente los
paneles 11 y 34), la corrección se acepta, documentada explícitamente como
identificación de primera mano sin corroboración escrita propia (a diferencia de
Shutter Island y Human Centipede, que sí la tienen).

Consecuencias, recalculadas desde cero (no reutilizando los 792 candidatos
anteriores, que usaban "ill" fijo en esta posición):

1. **Candidatas BIP39 literales para el título corregido:** "when" y "nature"
   (palabra completa), "call" (vía el mismo recorte de plural ya usado en el
   dataset, boy/boys, river/rivers). Las 3 son literales, ninguna es adivinanza.
   "ace" y "ventura" no dan ningún candidato. El panel pasa de tener una única
   palabra fija ("ill") a ser un panel ambiguo con 3 opciones reales.
2. **Criterio H1 (director/actor repetido):** el director (Oedekerk) y el actor
   principal (Carrey) no se repiten en ningún otro de los 34 paneles. El panel 11
   NO queda marcado como intrusa bajo H1 -- igual que tampoco lo estaba como
   Godzilla. El conjunto de 12 paneles marcados por H1 (con la complicación
   Scorsese ya documentada arriba) no cambia en absoluto con esta corrección; son
   hallazgos independientes.
3. **¿Aparece Godzilla en otra parte del puzzle?** No. Ni la película, ni su
   director, ni su actor principal aparecen en ningún otro archivo del dataset;
   eliminarla no rompe ninguna otra deducción por referencia cruzada.
4. **Conteos derivados:** el número de paneles sin ningún candidato literal (huecos
   reales, no solo ambiguos) sigue siendo 2 (Sharknado, Raiders of the Lost Ark) --
   el panel 11 nunca fue un hueco bajo ninguna de las dos identidades. El número de
   paneles ambiguos sube de 5 a 6. El espacio total de combinaciones abiertas sube
   de 792 a 2,376 (216 del producto de los 6 paneles ambiguos, por 11 opciones de
   Raiders, por 1 opción fija de Sharknado), verificado por enumeración directa sin
   ejecutar el oráculo.

**Qué queda invalidado:** los 792 candidatos ya probados contra el escrow (en ambos
barridos, el original y el corregido con "island"), porque todos fijaban "ill" en
esta posición. **Qué NO queda invalidado:** el conjunto de 12 paneles marcados por
H1, las correcciones de los paneles 8 y 34, ni la metodología general. No se ha
ejecutado ningún brute force nuevo tras esta corrección, según lo pedido.

## 8. Actualización, 2026-08-19 (más tarde el mismo día): verificación independiente del panel 11, y reversión del panel 8

Antes de aceptar sin más la corrección del panel 11, descargué el fotograma real y
lo pasé por búsqueda visual inversa (mismo método que resolvió el panel 8): el
resultado fue inconcluso, el motor solo reconoce el producto ("Bumble Bee"), sin
asociarlo a ninguna película. Busqué además una escena documentada con latas de
atún en arena en *Ace Ventura: When Nature Calls*: no existe -- la apertura real de
la película transcurre en un monasterio tibetano, y la única referencia a
"Bumblebee tuna" es una frase suelta del personaje en una escena sin relación
(saliendo de un rinoceronte de attrezzo). La identificación de Godzilla, en cambio,
sigue teniendo una fuente independiente que describe la escena exacta del
fotograma. Esto se le señaló al usuario como una tensión evidencial abierta, no
resuelta por esta verificación en ningún sentido.

También apliqué el mismo método al panel 34 (a raíz de una duda planteada por un
análisis externo de ChatGPT que no había comparado el fotograma real): resultado
débil pero consistente con la identificación ya existente (Human Centipede aparece
entre resultados relacionados, Dead Ringers no aparece en absoluto). Sin cambios.

El usuario, tras ver esta evidencia, decidió: mantener *Ace Ventura* como panel 11
pese a la tensión señalada, y **revertir el panel 8 a *The Goonies*** como hipótesis
principal, conservando *Shutter Island* como probabilidad secundaria (ninguna
descartada). Esto elimina por completo la complicación Scorsese en H1 (era
específica de la hipótesis Shutter Island): con Goonies como principal, H1 vuelve a
marcar exactamente los 10 paneles originales, sin ambigüedad.

Se construyó y ejecutó un cruce completo de 4.752 candidatos (7 paneles ambiguos,
incluyendo ambas palabras de ambas hipótesis del panel 8 -- "chunk" e "island" -- y
las 3 del panel 11 corregido, por las 11 opciones de Raiders) contra el oráculo:
**0 coincidencias**. El self-test del oráculo pasó antes y después de la corrida.
Esto no refuta ninguna hipótesis individual dentro del espacio: los 2 paneles
realmente huecos (Sharknado, Raiders of the Lost Ark) siguen siendo adivinanzas
ahí dentro, y continúan siendo la explicación más simple del resultado negativo.
