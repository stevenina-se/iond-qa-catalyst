# Ticket: 86e22fzve — Boards — Scheduler ejecuta flow correctamente pero status queda en "error"

> Sesión de deployment iniciada: 2026-07-13
> Módulo: Boards / Execution History
> QA Engineer: Steve Nina

## Contexto del Ticket

### Descripción
Bug: Al configurar un nodo Scheduler con ejecución periódica (ej: cada 1 minuto), guardar y activar el flow, tras la ejecución el status queda marcado como "error" en el Execution History. Sin embargo, la ejecución se realizó correctamente y los datos fluyeron por todos los nodos.

### Root Cause (identificado por Developer)
`GetQueue` en `queue_service.go` confundía "cola vacía" (`sql.ErrNoRows`) con un error real de SQL, propagando un error donde no había ninguno. Esto hacía que el scheduler marcara una ejecución exitosa como fatal error.

### Cambios del Developer (branch IONF-1127 → mergeado a DEVELOPMENT vía PR #11)

**Repo único afectado**: `flow_binaries`

| Archivo | Cambio Principal |
|---------|-----------------|
| `core/services/queue_service.go` | `GetQueue` ahora retorna `(nil, nil)` en `sql.ErrNoRows` en lugar de propagar error. `PopQueue` maneja `queue == nil` antes de dereferenciarlo. |
| `core/actions/flow/flow.go` | `ContinueNode` trata `queue == nil` como fin normal (early return sin error). |
| `backend/ion/board/company_dev_flow.go` | Eliminado `hadFatalError bool` local → usa `markFatalError()` centralizado. Fix de doble `SendError` en push-error path. |
| `backend/ion/board/account_dev_flow.go` | Mismo fix que company_dev_flow + `return nil` después de push-error fatal. |
| `backend/ion/board/company_live_flow.go` | `hadFatalError` local → `state.HadFatalError` en `ExecutionState`. |
| `backend/ion/board/account_live_flow.go` | Mismo fix que company_live_flow. |
| `backend/ion/board/flow_helpers.go` | Nueva función `markFatalError()` centralizada. `deriveTerminalStatus()` ahora recibe `*ExecutionState` completo. |
| `backend/ion/board/types.go` | `ExecutionState` agrega campo `HadFatalError bool`. |

### Módulo afectado
- Módulo principal: `Boards / Execution History`
- Módulos relacionados: `Executions`, `Dashboard` (métricas de ejecuciones)

### Datos del entorno de testing
- Rol: Company User con permiso `UPDATE_BOARD`
- Entorno: Staging
- Branch `IONF-1127` mergeada en DEVELOPMENT (PR #11, Jul 11 2026)
- Deployed: ✅ confirmado por Rodolfo (2026-07-11)

---

## Transcript de la Sesión

| Timestamp | Acción | Detalle |
|-----------|--------|---------|
| 2026-07-13 22:00 | Session Start | Contexto cargado: L1 completo + L2 boards + L2 executions + ticket de ClickUp |
| 2026-07-13 22:03 | Code Review | Repos actualizados. flow_binaries DEVELOPMENT actualizado (7 commits ahead). Diff IONF-1127 obtenido. |
| | Bug Hunting | En proceso... |
