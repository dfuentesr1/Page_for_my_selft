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
