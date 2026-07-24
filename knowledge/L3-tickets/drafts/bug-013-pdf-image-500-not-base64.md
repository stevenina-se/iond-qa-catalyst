# QA FOUND ISSUE ESCALATION REPORT — IOND

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | PDF Templates / Boards |
| Path | Company > PDF Templates > New Template > Elemento de imagen > Ejecución en Board |
| Versión | gateway-ion v0.1.0 · flow_binaries v0.1.0 · gateway v2.0.0 |

## Título

**PDF Templates — Nodo PDF retorna error 500 genérico cuando la imagen no está en base64**

## Description of the validated/replicated problem

Al arrastrar un elemento de tipo imagen en un template PDF y luego, desde un Board, enviar al campo de imagen una URL o texto plano (en lugar de base64), el servicio retorna un error 500 genérico. El error ocurre porque el campo esperaba una imagen codificada en base64. El mensaje de error no es específico ni descriptivo, dificultando al usuario entender qué formato se espera para el campo de imagen.

## Steps to Reproduce

1. Company Login > Sidebar: PDF Templates > New Template
2. Arrastrar un elemento de tipo "Imagen" al canvas del template
3. Guardar el template
4. Navegar a Company > Boards > [Board existente]
5. Conectar un nodo que envíe datos al nodo PDF Template
6. En el campo de imagen, enviar una URL (ejemplo: `https://example.com/image.png`) o texto plano
7. Ejecutar el nodo
8. Observar el error 500 en la respuesta del servicio

## Datos utilizados

- Rol: Company User
- Entorno: Staging
- Versión: v0.1.0
- Input: URL de imagen o texto plano (no base64)
- Template con elemento de imagen configurado

## Current Behavior

El servicio retorna HTTP 500 con un mensaje genérico. No indica que el campo esperaba una imagen en formato base64.

## Expected Behavior

1. El servicio debería retornar un error 400 (Bad Request) con un mensaje descriptivo como: `"Image field expects base64 encoded data, received URL/plain text"`
2. La documentación del nodo PDF debería indicar claramente que las imágenes deben proporcionarse en formato base64
3. Idealmente, el sistema debería aceptar tanto base64 como URLs (descargando la imagen automáticamente)

## Impacto

- Afecta a usuarios que integran imágenes dinámicas en templates PDF
- El error 500 genérico dificulta el debugging
- No bloqueante si el usuario conoce el formato esperado (base64)

## Categorización

- 📊 Prioridad: **normal** — workaround disponible (usar base64), pero el error debería ser descriptivo
- 🏷️ Tipo: **bug** — el error 500 debería ser un 400 con mensaje descriptivo
