# Video Motion Studio

Proyecto para crear montajes automáticos de imágenes, video y audio con HyperFrames, FFmpeg, FFprobe y Python.

## Skill incluida

`skills/skill-faty-lendedistorcionado` crea montajes de 20 segundos con:

- lente de ojo de pez ovalada y exterior negro;
- color intenso, aberración cromática y movimiento suave;
- transiciones extrañas elegidas según las imágenes;
- colecciones separadas por video, sin modificar los originales;
- música diferente en cada montaje;
- validación de encuadres, compatibilidad y volumen antes de entregar.

## Entorno

El entorno Conda del proyecto se llama `video-motion`.

```powershell
conda activate video-motion
```

Después se pueden usar `ffmpeg`, `ffprobe`, `python` y los scripts del proyecto.

Los MP4 exportados se guardan localmente en `output/exports/` y no se suben al repositorio para evitar archivos binarios pesados.
