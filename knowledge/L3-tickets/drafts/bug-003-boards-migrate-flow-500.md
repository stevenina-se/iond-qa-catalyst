# QA FOUND ISSUE ESCALATION REPORT — IOND

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | Boards |
| Path | Admin > Companies > List > Boards > [Board] > Copy |
| Versión | gateway-ion v0.1.0 · flow_binaries v0.1.0 · gateway v2.0.0 |

## Título

**Boards — Migración de flow a global retorna error 500 "failed to create global flow: invalid field"**

## Description of the validated/replicated problem

Al intentar migrar un flow desde el panel de Admin (Companies > List > Boards > [Board] > Copy), la operación falla con un error 500 visible en los DevTools. El mensaje de error es: `"failed to create global flow: invalid field"`. Este error bloquea completamente la funcionalidad de migración de flows a global (GRAPP), que es una funcionalidad core del sistema para la distribución de flows entre companies.

## Steps to Reproduce

1. Admin Login > Sidebar: Companies > List
2. Seleccionar una Company que tenga boards con flows
3. Navegar a la sección Boards de la Company seleccionada
4. Seleccionar un Board existente > opción "Copy" (migrar a global)
5. Abrir DevTools del navegador (F12) > Tab: Network
6. Confirmar la operación de migración
7. Observar el error 500 en la respuesta: `"failed to create global flow: invalid field"`

## Datos utilizados

- Rol: Admin
- Entorno: Staging
- Versión: v0.1.0
- Endpoint afectado: `PUT /1.0/companies/{company}/flow/{appId}/migrate`
- Cualquier flow válido dentro de un Board de una Company

## Current Behavior

La migración de flow retorna HTTP 500 con el mensaje `"failed to create global flow: invalid field"`. La operación falla completamente y el flow no se migra a global.

## Expected Behavior

La migración debería crear exitosamente una copia global del flow (GRAPP) accesible para todas las companies. El endpoint `/migrate` debería validar los campos requeridos antes de intentar la creación y retornar un error descriptivo si falta algún campo obligatorio (en lugar de un 500 genérico).

## Impacto

- Bloqueante para la funcionalidad de migración de flows a global (GRAPP)
- Afecta exclusivamente a usuarios Admin
- Impacto crítico: sin esta funcionalidad no se pueden distribuir flows a nivel plataforma

## Categorización

- 📊 Prioridad: **urgent** — funcionalidad core completamente rota, bloqueante para la creación de GRAPPs
- 🏷️ Tipo: **bug** — la migración es una funcionalidad existente que debería funcionar correctamente
