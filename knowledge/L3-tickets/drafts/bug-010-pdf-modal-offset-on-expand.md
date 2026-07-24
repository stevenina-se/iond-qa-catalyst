# QA FOUND ISSUE ESCALATION REPORT — IOND

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | PDF Templates |
| Path | Company > PDF Templates > New Template |
| Versión | gateway-ion v0.1.0 · flow_binaries v0.1.0 · gateway v2.0.0 |

## Título

**PDF Templates — Modal de New Template se desfasa al expandirlo, imposibilitando cerrarlo**

## Description of the validated/replicated problem

Al crear un nuevo template PDF, el modal que se abre permite ser arrastrado (movido). Sin embargo, al expandir el modal (maximizarlo o cambiar su tamaño), este se desfasa de la vista visible, quedando parcial o completamente fuera de la pantalla. Una vez desfasado, resulta imposible cerrar el modal ya que los controles de cierre quedan fuera del viewport accesible.

## Steps to Reproduce

1. Company Login > Sidebar: PDF Templates
2. Presionar Button: "New Template"
3. Observar que se abre un modal para la creación del template
4. Arrastrar el modal a una posición diferente en la pantalla
5. Expandir/maximizar el modal
6. Observar que el modal se desfasa de la vista
7. Intentar cerrar el modal → no es posible, los controles de cierre están fuera del viewport

## Datos utilizados

- Rol: Company User con permiso `READ_PDF_TEMPLATE`
- Entorno: Staging
- Versión: v0.1.0

## Current Behavior

El modal es draggable y expandible. Al expandirlo después de haberlo movido, su posición se calcula incorrectamente, desfasándose fuera de los límites de la vista. Los controles de cierre quedan inaccesibles.

## Expected Behavior

1. Al expandir el modal, debería reposicionarse automáticamente centrado en el viewport
2. El modal nunca debería desfasarse fuera de los límites visibles de la pantalla
3. Los controles de cierre siempre deben ser accesibles
4. Alternativamente, soportar cierre con tecla Escape como fallback

## Impacto

- Afecta a Company Users que crean templates PDF
- Puede forzar al usuario a recargar la página para recuperar el control
- La pérdida del estado del modal puede significar pérdida de trabajo no guardado

## Categorización

- 📊 Prioridad: **normal** — workaround disponible (recargar la página), no bloquea funcionalidad principal
- 🏷️ Tipo: **bug** — el modal debería mantenerse dentro del viewport al expandirse
