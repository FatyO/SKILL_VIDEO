---
name: skill-faty-lendedistorcionado
description: Crea montajes automáticos en Video Motion Studio a partir de una colección nueva de imágenes, con ojo de pez ovalado, fondo negro, color intenso, aberración cromática y transiciones extrañas adaptadas al contenido. Úsala cuando la persona diga que ya agregó la media y pida crear, previsualizar o renderizar el siguiente video con el estilo Faty aprobado.
---

# Skill Faty: lente distorsionado

Trabaja dentro del proyecto `video-motion-studio`. Usa HyperFrames para la composición y FFprobe/FFmpeg para inspección y verificación.

## Flujo obligatorio

1. Espera a que la persona confirme que terminó de agregar la media. No crees el video antes de esa confirmación.
2. Detecta solamente archivos compatibles que estén sueltos en las carpetas de entrada de `media/`. Copia las imágenes nuevas a una colección `media/images/collections/video_NNN`; nunca muevas, sobrescribas ni alteres los originales.
3. Marca esa colección como activa en `output/catalog/active_image_collection.json`. No uses archivos de colecciones anteriores.
4. Ejecuta el catálogo del proyecto y revisa imágenes, videos y audios con FFprobe cuando corresponda. Registra duración, resolución, FPS, códec/formato y errores o incompatibilidades en JSON.
5. Inspecciona visualmente las imágenes de la colección activa. Ordénalas empezando por las más intensas/coloridas y avanzando hacia las más claras o menos coloridas, salvo que su contenido sugiera una secuencia narrativa mejor.
6. Construye el montaje siguiendo [el perfil visual](references/style-profile.md). Ajusta cada encuadre por separado para mantener el rostro o sujeto principal cerca del centro y evita cortes incómodos. Comprueba todos los planos con un fotograma asentado; no des por hecho que un `object-position` común centra todas las imágenes.
7. Elige transiciones visibles, extrañas y con carácter de terror/Halloween según la imagen; no repitas mecánicamente una sola transición.
8. Si hay música en `media/audio`, úsala cuando encaje con las imágenes o cuando la persona la solicite, con volumen agradable y fundidos de entrada/salida. Si no existe una pista o la persona pide silencio, produce el video sin música. Cada `video_NNN` debe tener música diferente: antes de renderizar compara el hash SHA-256 de la pista elegida con los audios de los proyectos anteriores y recházala si coincide. No reutilices automáticamente la música de otro video. Después de renderizar mide el audio del MP4 con FFmpeg; debe ser claramente audible (como referencia, volumen medio entre -24 y -14 dB y pico inferior a -1 dB). Si queda demasiado bajo, normalízalo y verifica de nuevo.
9. Crea `output/exports/video_NNN/` con el mismo nombre que la colección y prepara `export_config.json`.
10. Ejecuta `hyperframes check`, revisa fotogramas y muestra primero la previsualización. Renderiza únicamente cuando la persona lo pida o apruebe la previsualización.
11. Tras renderizar, verifica el MP4 con FFprobe y fotogramas decodificados. Informa duración, resolución, FPS, códecs y ubicación.

## Límites

- No mezcles material de `video_001` ni de otras colecciones con la colección activa.
- No añadas títulos por defecto.
- No cambies configuraciones globales de Windows, Conda ni FFmpeg.
- Mantén editables los elementos de HyperFrames y conserva los archivos originales.
- Explica brevemente qué se hizo al terminar cada paso.

