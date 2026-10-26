# Perfil visual aprobado

El resultado de referencia es `output/exports/video_001/video_001.mp4`. Se usa como dirección artística, no como fuente de media.

## Formato base

- Duración objetivo: 20 segundos, ajustable si la persona lo solicita.
- Formato predeterminado: horizontal, 1920 × 1080, 30 FPS.
- Puede ser cuadrado si la persona lo pide o si la media funciona claramente mejor así.
- Sin título por defecto.

## Lente y encuadre

- Ventana de ojo de pez grande y ovalada que ocupa casi todo el cuadro.
- Exterior completamente negro, con borde oscuro grueso y un resplandor azul discreto.
- Sujeto o rostro principal centrado y visible. Ajustar por imagen `object-position` y, cuando no baste por la relación de aspecto, también el desplazamiento `xPercent`/`yPercent` del movimiento.
- Revisar un fotograma asentado de cada imagen: ojos, nariz o punto focal deben quedar próximos al centro del óvalo y no cortados por su borde.
- Movimiento lento dentro de cada imagen: acercamiento suave, desplazamiento corto o rotación mínima.

## Color y textura

- Colores brillantes pero agradables: subir vibrance y saturación con moderación, conservar detalle en luces y sombras.
- Contraste fuerte, negros profundos y viñeta ovalada.
- Aberración cromática visible pero controlada, curvatura CRT/ojo de pez y grano ligero.
- Destellos cromáticos breves solamente durante transiciones.

Valores de referencia del video aprobado: exposición `0.13`, contraste `0.18`, vibrance `0.50`, saturación `0.24`, viñeta `0.38`, grano `0.08`, aberración cromática `0.18` y curvatura `0.62`. Son puntos de partida; se ajustan si una imagen se quema, pierde detalle o cambia demasiado de color.

## Transiciones

Preferir una combinación elegida según el contenido:

- iris circular desde el centro;
- barrido dentado lateral;
- apertura rectangular desde un punto inquietante;
- expansión ovalada descentrada;
- ruptura poligonal o destello cromático corto.

Las transiciones deben leerse con claridad, durar aproximadamente `0.55–0.75 s` y conservar movimiento suave durante el resto de cada plano.

## Audio

- La música es opcional, pero debe añadirse cuando la persona la solicite. Puede proceder de `media/audio` o ser elegida con autorización.
- Mezcla de referencia: volumen cercano a `0.28`, entrada de `1.2 s` y salida de `1.8 s`, ajustable según la pista.
- No reutilizar `video_001-bgm.wav` automáticamente.

