# Sprites del circo (extraídos de `hoja_original.png`)

PNG RGBA con transparencia real. Todos los fotogramas de una animación tienen el mismo tamaño
de lienzo y están alineados por un punto de anclaje fijo (la base del personaje), así que no saltan.
`animaciones.json` indica fotogramas, FPS, tamaño y pivot de cada animación (el pivot está en el
formato del Custom Pivot de Unity). Cada carpeta tiene un `_preview.gif` para revisar el bucle.

| Carpeta | Fotogramas | FPS | Uso |
|---|---|---|---|
| `jefe_escribe/` | 8 | 8 | Jefe sentado escribiendo (bucle) |
| `jefe_cara/` | 6 | 4 | Expresiones del jefe: solo cabeza, sin silla ni mesa |
| `elefante/` | 7 | 6 | Elefante en equilibrio sobre la pelota (bucle) |
| `mono/` | 7 | 10 | Mono tocando los tambores (bucle) |
| `tigre/` | 6 | 6 | Tigre dentro de su jaula (bucle) |

`props/`: telón, gradas, carpa pequeña, escalera, banderines, barriles, pista, cajas, farola,
saco de boxeo, diana y cuerda.

Problemas conocidos:
- La guirnalda de bombillas no se pudo recortar limpia (el resplandor se confunde con el fondo) y no
  está incluida.
- La pelota del elefante está dibujada junto al elefante en cada fotograma; no se puede separar.
- Los barrotes de la jaula están pintados encima del tigre en cada fotograma; no hay capa separada.
- Las expresiones del jefe (`jefe_cara/`) no encajan con los fotogramas sentados (otro encuadre y sin
  silla); sirven como retratos para diálogos, no como continuación de la animación de escritura.
