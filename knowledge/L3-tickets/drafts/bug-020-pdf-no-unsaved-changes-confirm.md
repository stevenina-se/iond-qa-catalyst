# QA FOUND ISSUE ESCALATION REPORT — IOND

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | PDF Templates |
| Path | Company > PDF Templates > [Template] |
| Versión | gateway-ion v0.1.0 · flow_binaries v0.1.0 · gateway v2.0.0 |

## Título

**PDF Templates — Cambios sin guardar se pierden al presionar Escape o cerrar modal sin confirmación**

## Description of the validated/replicated problem

Al estar editando un template PDF, si el usuario presiona por error la tecla Escape o cierra el modal, todos los cambios no guardados se pierden sin ningún diálogo de confirmación. El mismo problema ocurre si por error se presiona "New Template" mientras se está editando un template existente. No existe alerta ni confirmación que prevenga la pérdida accidental de trabajo.

## Steps to Reproduce

1. Company Login > Sidebar: PDF Templates
2. Abrir un template existente para edición
3. Realizar modificaciones significativas en el template (agregar/modificar elementos)
4. Sin guardar, presionar la tecla Escape
5. Observar que el modal se cierra y los cambios se pierden sin confirmación
6. Alternativamente: presionar "New Template" mientras se edita → los cambios se pierden

## Datos utilizados

- Rol: Company User con permiso `READ_PDF_TEMPLATE`
- Entorno: Staging
- Versión: v0.1.0

## Current Behavior

Al presionar Escape, cerrar el modal, o presionar "New Template" durante la edición, los cambios sin guardar se pierden inmediatamente sin diálogo de confirmación.

## Expected Behavior

1. Al intentar cerrar el modal con cambios sin guardar, mostrar un diálogo de confirmación: "¿Estás seguro? Los cambios sin guardar se perderán"
2. Al presionar Escape con cambios pendientes, mostrar el mismo diálogo
3. Al presionar "New Template" durante la edición, mostrar confirmación antes de descartar el template actual
4. Opciones en el diálogo: "Guardar", "Descartar", "Cancelar"

## Impacto

- Afecta a todos los usuarios que editan templates PDF
- Potencial pérdida significativa de trabajo en templates complejos
- Particularmente problemático con acciones accidentales (Escape, click erróneo en New Template)

## Notas Adicionales

**Pregunta abierta del QA**: ¿La implementación planificada de Git para PDFs resolvería este problema al permitir recuperar versiones anteriores? Independientemente, el diálogo de confirmación es necesario como primera línea de defensa contra pérdida accidental.

## Categorización

- 📊 Prioridad: **normal** — pérdida potencial de trabajo pero hay workaround (guardar frecuentemente)
- 🏷️ Tipo: **bug** — toda aplicación de edición debería tener confirmación de descarte de cambios
