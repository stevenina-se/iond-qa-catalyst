# QA FOUND ISSUE ESCALATION REPORT — IOND

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | Executions |
| Path | Company > Execution History > Data |
| Versión | gateway-ion v0.1.0 · flow_binaries v0.1.0 · gateway v2.0.0 |

## Título

**Executions — Status inconsistente entre lista ("completed") y detalle ("running") con end_time inválido**

## Description of the validated/replicated problem

Al verificar el historial de ejecuciones de flows, se observa una inconsistencia de datos entre la vista de lista y la vista de detalle. En la tabla de la lista, un flow muestra status "completed", pero al abrir los datos de ejecución del mismo flow, el status indica "running". Adicionalmente, el campo `end_time` muestra una fecha inválida: `0001-01-01T00:00:00Z` (zero value de Go), lo cual es una inconsistencia de datos que indica que la ejecución nunca fue marcada como finalizada correctamente en el backend.

## Steps to Reproduce

1. Company Login > Sidebar: Execution History
2. En la lista de ejecuciones, identificar un flow con status "completed"
3. Hacer click para ver los datos de ejecución del flow
4. Observar que en la vista de detalle el status es "running"
5. Verificar el campo `end_time` → muestra `0001-01-01T00:00:00Z`

## Datos utilizados

- Rol: Company User con permiso `READ_EXECUTION`
- Entorno: Staging
- Versión: v0.1.0
- Cualquier flow que haya sido ejecutado y cuya ejecución haya finalizado

## Current Behavior

- La lista de ejecuciones muestra status "completed"
- El detalle de la misma ejecución muestra status "running"
- El campo `end_time` tiene valor `0001-01-01T00:00:00Z` (zero value de Go/time.Time)
- Existe inconsistencia entre los datos de la lista y el detalle

## Expected Behavior

- El status debería ser consistente entre la lista y el detalle de la ejecución
- Si la ejecución finalizó correctamente, ambas vistas deben mostrar "completed"
- El campo `end_time` debería contener la fecha y hora real de finalización de la ejecución
- Un `end_time` con zero value debería interpretarse como ejecución aún en proceso, no como completada

## Impacto

- Afecta a todos los Company Users que monitorean ejecuciones de flows
- Genera confusión sobre el estado real de las ejecuciones
- Posible problema de integridad de datos en el backend (status/end_time no se actualizan correctamente al finalizar)

## Categorización

- 📊 Prioridad: **high** — datos inconsistentes en funcionalidad core de monitoreo, afecta la confiabilidad del historial
- 🏷️ Tipo: **bug** — el status y end_time deberían ser consistentes y correctos
