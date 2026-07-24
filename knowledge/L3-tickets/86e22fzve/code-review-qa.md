# Code Review QA — 86e22fzve (Modo Deployment / Bug Hunting)

> Fecha: 2026-07-13
> Ticket: 86e22fzve — Boards — Scheduler ejecuta flow correctamente pero status queda en "error"
> Branch: IONF-1127 → Mergeada en DEVELOPMENT (PR #11, 2026-07-11)
> Revisado por: QA Catalyst

---

## Resumen

| Métrica | Valor |
|---------|-------|
| Repos revisados | `flow_binaries` (único afectado) |
| Archivos modificados analizados | 8 |
| Bugs confirmados (reproducibles) | 0 |
| Riesgos a verificar en testing | 2 |
| Módulos con impacto cruzado | Executions, Dashboard |
| TCs inyectados en test-matrix | 2 (TC-CR-001, TC-CR-002) |

---

## Archivos Modificados

| Repo | Archivo | Cambio Principal | Líneas |
|------|---------|-----------------|--------|
| flow_binaries | `core/services/queue_service.go` | `GetQueue` retorna `(nil, nil)` en `ErrNoRows`; `PopQueue` nil-guard | +16/-13 |
| flow_binaries | `core/actions/flow/flow.go` | `ContinueNode` trata `queue == nil` como fin normal | +1/-1 |
| flow_binaries | `backend/ion/board/company_dev_flow.go` | Usa `markFatalError()` centralizado; fix doble SendError; `SendProgress` reordenado | +13/-10 |
| flow_binaries | `backend/ion/board/account_dev_flow.go` | Mismo fix + `return nil` post-push-error; `hadFatalError` local eliminado | +12/-8 |
| flow_binaries | `backend/ion/board/company_live_flow.go` | `hadFatalError` local → `state.HadFatalError` | +2/-2 |
| flow_binaries | `backend/ion/board/account_live_flow.go` | `hadFatalError` local → `state.HadFatalError` | +2/-2 |
| flow_binaries | `backend/ion/board/flow_helpers.go` | Nueva `markFatalError()`; `deriveTerminalStatus()` recibe `*ExecutionState` | +13/-3 |
| flow_binaries | `backend/ion/board/types.go` | Campo `HadFatalError bool` en `ExecutionState` (sin json tag) | +2/0 |

---

## Bugs Confirmados (Reproducibles)

> Ninguno. Los cambios del Developer son correctos y el fix es consistente. Los tests Go pasaron: `go test ./...` ✅ y `go vet ./...` ✅.

---

## Riesgos a Verificar

### BUG-CR-001 — RIESGO A VERIFICAR
**Clasificación**: RIESGO A VERIFICAR  
**Severidad**: 🟡 Medio  
**Repo**: `flow_binaries`  
**Archivo**: `backend/ion/board/types.go`  
**Línea**: ~79 (campo `HadFatalError bool` en struct `ExecutionState`)

**Descripción**: El campo `HadFatalError bool` se agrega a `ExecutionState` sin tag `json:"-"`. Otros campos internos del struct como `WaitingForInput` sí tienen el tag `json:"-"` para evitar su serialización. Si `ExecutionState` se serializa directamente en alguna respuesta HTTP o WebSocket, este campo interno podría exponerse al cliente.

**Evidencia**:
```go
// types.go — línea ~79
WaitingForInput bool  `json:"-"`       // ← correcto, marcado como interno
WaitingPayload  any   `json:"waiting_payload,omitempty"`
// ...
HadFatalError bool                     // ← sin json tag → se serializa como "HadFatalError"
```

**Escenario para verificar**:
1. Ejecutar un flow con Scheduler que genere un error real (ej: nodo mal configurado)
2. Observar la respuesta WebSocket / payload de la ejecución en devtools
3. Verificar si el campo `HadFatalError` aparece en el JSON de respuesta

**Por qué es riesgo**: Es un campo de estado interno de la máquina de estados del motor. Exponerlo al cliente podría causar confusión o ser usado inadvertidamente. Patrón del equipo: usar `json:"-"` para campos internos de control.

**Impacto potencial**: Exposición de estado interno al cliente. Severidad baja pero inconsistente con el patrón del código.

---

### BUG-CR-002 — RIESGO A VERIFICAR
**Clasificación**: RIESGO A VERIFICAR  
**Severidad**: 🟠 Alto  
**Repo**: `flow_binaries`  
**Archivo**: `backend/ion/board/company_dev_flow.go`, `account_dev_flow.go`  
**Línea**: `advanceFlow()` — post-fix de SendProgress

**Descripción**: En el nuevo código, `cf.control.SendProgress(rp)` se llama ANTES de verificar si `err != nil` en el path de `PushNode`. Si `PushNode` retorna tanto un `rp` válido como un `err`, el progreso se envía y luego se marca fatal error. El cliente recibiría primero progreso positivo y luego el error fatal. Verificar que la secuencia de mensajes WS no genera un estado visual inconsistente en la UI.

**Evidencia**:
```go
// company_dev_flow.go — nuevo orden
rp, err := flowCore.PushNode(...)
cf.control.SendProgress(rp)    // ← progreso enviado primero
if err != nil {
    log.Printf(errPushingBoardFmt, err)
    markFatalError(cf.control)  // ← luego error fatal
    return nil
}
```

**Escenario para verificar**:
1. Company Login > Sidebar: Boards > [Board con nodo que puede fallar en PushNode]
2. Ejecutar flow en modo Dev (canvas) con nodo configurado para fallar
3. Observar secuencia de mensajes en la UI durante la ejecución
4. Verificar que el estado final en canvas sea "error" y no quede en estado de progreso inconsistente

**Por qué es riesgo**: El Developer indica que `SendProgress(rp)` antes del check es intencional ("send progress even if it is null"), pero el comportamiento visual en el canvas con la secuencia progreso→error debe verificarse.

**Impacto potencial**: Estado visual del canvas inconsistente en ejecuciones que fallan via PushNode. No afecta la lógica de negocio (el status en BD será correcto), pero puede confundir al usuario.

---

## Impacto Cruzado

| Módulo Impactado | Componente Afectado | Riesgo | Verificación Necesaria |
|-----------------|---------------------|--------|------------------------|
| **Executions** | Historial de ejecuciones | 🟠 Alto | El status en historial debe ser "completed", no "error", para flows que terminan exitosamente |
| **Dashboard** | Métricas de ejecuciones | 🟡 Medio | Si Executions reporta el status correcto, Dashboard debería ser correcto automáticamente |

---

## TCs Inyectados en Test Matrix

| TC ID | Origen | Caso de Test | Severidad |
|-------|--------|-------------|-----------|
| TC-CR-001 | BUG-CR-001 | Verificar que `HadFatalError` no aparece en response WS/HTTP al cliente | 🟡 Medio |
| TC-CR-002 | BUG-CR-002 | Verificar secuencia visual en canvas al fallar PushNode en modo Dev | 🟠 Alto |
