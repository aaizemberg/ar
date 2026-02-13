# Directorio Public

Este directorio contiene assets estáticos que se sirven directamente.

## Archivos que van aquí:

- `favicon.ico` - Icono del sitio (16x16 o 32x32 píxeles)
- Imágenes que uses en tu app
- Archivos de datos estáticos (CSV, JSON, etc.)
- Fuentes personalizadas
- Otros assets públicos

## Cómo usar:

Los archivos en `public/` se sirven desde la raíz del sitio.

Por ejemplo:
- `public/favicon.ico` → accesible en `/favicon.ico`
- `public/logo.png` → accesible en `/logo.png`
- `public/data/ventas.csv` → accesible en `/data/ventas.csv`

## En tu código:

```html
<!-- En HTML -->
<img src="/logo.png" alt="Logo" />

<!-- En CSS -->
background-image: url('/imagen.jpg');
```

```javascript
// En JavaScript/Svelte
fetch('/data/ventas.csv')
  .then(response => response.text())
  .then(data => console.log(data));
```

**Nota:** Vite copia automáticamente todo lo que está en `public/` al directorio de salida cuando haces `npm run build`.