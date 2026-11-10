# Page_for_my_selft

## PixelLab (generación de assets de pixel art)

El servidor MCP de PixelLab está configurado en `.mcp.json` y lee la key de la
variable de entorno `PIXELLAB_API_KEY`. La key nunca se guarda en el repo.

- Claude Code web: Ajustes del entorno > Variables/Secretos > `PIXELLAB_API_KEY`.
- Local: `export PIXELLAB_API_KEY=pixl_...` y abre Claude Code en esta carpeta.

## Assets

### Joker Morado (`assets/joker-morado/`)
Sprite 64x64 generado con PixelLab a partir del concept art. Animaciones mirando a la derecha (`east`); las hojas `*_west_sheet.png` son el volteo horizontal.

| Animación | Fotogramas | Hoja de sprites |
|---|---|---|
| Idle | 4 | `idle_east_sheet.png` |
| Caminar | 8 | `walk_east_sheet.png` |
| Lanzar rayo | 6 | `cast_east_sheet.png` |

`frames/` tiene los PNG sueltos, `rotations/` las 8 direcciones estáticas y `*_preview.gif` una vista previa.

## Mapa de mundo: Isla Cascabel (`mapa-feria/`)

Mapa de mundo jugable con temática de feria y payasos, inspirado en cómo funciona el
mapa de Cuphead. Abre `mapa-feria/index.html` en el navegador; no necesita servidor ni dependencias.

![Vista general](mapa-feria/preview.png)

**Cómo está hecho (las mismas técnicas que el mapa de Cuphead):**
- **Cámara:** vista cenital oblicua 3/4 que sigue al jugador con suavizado y algo de
  anticipación según hacia dónde camina, con zoom fijo y límites en los bordes del mundo.
- **Profundidad:** cada objeto se ordena por su coordenada Y, así el jugador pasa por
  delante o por detrás de árboles y edificios.
- **Isla con volumen:** acantilado visible en las costas del sur, espuma animada y aguas someras.
- **Estilo cartoon de los años 30:** contorno de tinta grueso, trazo que tiembla a 12 fps
  (3 variantes por sprite), tinte sepia, viñeta, grano de película, polvo y rayas.
- **Niveles:** cada atracción tiene una bandera (gris pendiente, roja visitada), un botón
  "Z" flotante y una tarjeta de título. Al entrar se cierra un iris sobre el jugador.

**Forma de la isla:** gorro de bufón de tres puntas; en cada punta cuelga un "cascabel"
(islote) unido por un puente: Cañón humano, Noria y Caseta de tiro.

| Nivel | Atracción |
|---|---|
| 1 | Carrusel Desbocado |
| 2 | La Casa de la Risa |
| 3 | Montaña Rusa Infernal |
| 4 | El Gran Cañón Humano |
| 5 | La Noria Lunar |
| Jefe | ¡La Gran Función! (Gran Carpa) |

Extras: 4 monedas escondidas, martillo de fuerza, taquilla, poste indicador y caseta de tiro.
Controles: flechas/WASD para moverse; Z, Intro o Espacio para interactuar; X o Esc para volver;
joystick táctil en móvil.

El jugador es un **marcador provisional** (`drawPlayerToken`); se sustituirá por el sprite
definitivo del personaje.
