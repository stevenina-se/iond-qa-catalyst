# QA FOUND ISSUE ESCALATION REPORT — IOND

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | PDF Templates |
| Path | Company > PDF Templates |
| Versión | gateway-ion v0.1.0 · flow_binaries v0.1.0 · gateway v2.0.0 |

## Título

**PDF Templates — Paginación de la lista de templates no funciona correctamente**

## Description of the validated/replicated problem

La paginación de la vista de lista de PDF Templates no funciona correctamente. La navegación entre páginas de la lista de templates presenta problemas, impidiendo al usuario acceder a todos sus templates cuando la cantidad supera el límite de una sola página.

## Steps to Reproduce

1. Company Login > Sidebar: PDF Templates
2. Tener suficientes templates para que la lista requiera paginación
3. Intentar navegar entre páginas de la lista
4. Observar el comportamiento incorrecto de la paginación

## Datos utilizados

- Rol: Company User con permiso `READ_PDF_TEMPLATE`
- Entorno: Staging
- Versión: v0.1.0
- Suficientes templates PDF para activar paginación

## Current Behavior

La paginación no funciona correctamente. Los controles de navegación entre páginas presentan comportamiento defectuoso.

## Expected Behavior

La paginación debería:
1. Mostrar el número correcto de páginas basado en el total de templates
2. Navegar correctamente entre páginas
3. Mantener consistencia en el número de items por página
4. Reflejar correctamente la página actual

## Impacto

- Afecta a usuarios con múltiples templates PDF
- Puede impedir acceder a templates que están en páginas posteriores

## Categorización

- 📊 Prioridad: **normal** — afecta navegación pero no bloquea la funcionalidad principal
- 🏷️ Tipo: **bug** — la paginación es una funcionalidad estándar que debería operar correctamente
