# Catálogo de medios

Ejecuta el análisis desde la raíz del proyecto:

```powershell
.\scan-media.ps1
```

El programa revisa recursivamente `media/videos`, `media/images` y
`media/audio`. FFprobe obtiene los datos técnicos y el resultado se guarda en
`output/catalog/media_catalog.json`.

Los videos compatibles se ordenan por ruta y se agrupan de tres en tres. Cada
grupo recibe un manifiesto en `output/catalog/batches/batch_NNN/manifest.json`.
Los manifiestos solo contienen referencias: los archivos originales nunca se
mueven ni se modifican.

Estados posibles:

- `compatible`: FFprobe pudo leer el archivo y encontró la pista esperada.
- `warning`: puede utilizarse, pero requiere atención; por ejemplo, está en la
  carpeta equivocada.
- `incompatible`: FFprobe no pudo leerlo, la extensión no está admitida o no
  contiene la pista esperada.

