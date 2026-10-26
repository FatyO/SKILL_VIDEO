# Importar archivos multimedia

Las imágenes del proyecto se guardan en `media/images`, los videos en
`media/videos` y el audio en `media/audio`.

Para importar archivos externos sin modificar los originales:

```powershell
.\import-media.ps1 "C:\ruta\imagen.jpg" "C:\ruta\cancion.mp3"
```

Para iniciar un grupo nuevo de imágenes destinado a un solo video:

```powershell
.\import-media.ps1 -NewCollection "C:\ruta\foto-1.jpg" "C:\ruta\foto-2.jpg"
```

Las colecciones se crean como `media/images/collections/video_001`,
`video_002`, etc. El archivo `output/catalog/active_image_collection.json`
indica cuál debe utilizar el próximo montaje. No deben mezclarse imágenes de
otras colecciones.

El importador copia los archivos, detecta duplicados por contenido y cambia el
nombre de una copia cuando existe otro archivo distinto con el mismo nombre.
Después puede ejecutarse `scan-media.ps1` para actualizar el catálogo JSON.
