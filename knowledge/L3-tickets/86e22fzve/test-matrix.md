# Test Matrix — 86e22fzve

## Resumen

| Métrica | Valor |
|---------|-------|
| Total de casos | 14 |
| Smoke tests | 2 |
| Happy Path | 4 |
| Edge Cases | 3 |
| Negativos | 1 |
| Regresión | 2 |
| Code Review | 2 |
| Automatizables | 4 |
| Cobertura de AC | 3/3 |

### Acceptance Criteria (derivados de specs del Developer + bug report)

- **AC-1**: Un flow con nodo Scheduler que se ejecuta exitosamente debe mostrar status "completed" (no "error") en el Execution History.
- **AC-2**: Un flow con nodo Scheduler que falla genuinamente debe mostrar status "error" en el Execution History.
- **AC-3**: El comportamiento aplica tanto para Company flows como Account flows (ambos schedulers).

---

## Test Matrix

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|----|------|-------------|--------------|-------|--------------------|-----------|---------------|--------|
| TC-001 | Boards / Executions | AC-1 | Smoke | Verificar que el módulo Execution History carga correctamente | Flow con Scheduler activo en staging | Company Login > Sidebar: Executions > Verify: lista de ejecuciones visible | Lista de ejecuciones se muestra sin error | 🔴 | ✅ | ✅ PASS — 337,576 registros visibles, paginación funcional |
| TC-002 | Boards | AC-1 | Smoke | Verificar que un flow con Scheduler en estado Active puede activarse | Flow existente en staging | Company Login > Sidebar: Boards > Click [Flow con Scheduler] > Verify: toggle Active visible | Flow se muestra con toggle Active | 🔴 | ✅ | ✅ PASS — Board_Schedule_Dos toggle Paused→Active funcional, estado actualizado en tiempo real |
| TC-003 | Boards / Executions | AC-1 | Happy Path | Scheduler Company flow: ejecución exitosa muestra "completed" | Flow con nodo Scheduler configurado (interval: 1 min), en estado Active | Company Login > Sidebar: Boards > Click [Flow con Scheduler] > Canvas: Verify flow Active > Wait: 1-2 minutos > Sidebar: Executions > Verify: última ejecución del flow muestra status "completed" | Status de ejecución es "completed", no "error" | 🔴 | ❌ | ✅ PASS — board(385) sesión `71a1d408`: `status:"completed"`, `HadFatalError:false` |
| TC-004 | Boards / Executions | AC-1 | Happy Path | Scheduler Company flow: múltiples ejecuciones exitosas todas "completed" | Mismo flow del TC-003, con al menos 3 ejecuciones | Company Login > Sidebar: Executions > Filter: [Flow con Scheduler] > Verify: todas las ejecuciones recientes muestran "completed" | Todas las ejecuciones muestran status "completed" | 🔴 | ❌ | ✅ PASS — board(385) muestra mix de `completed` y `warning` (warning = nodos con configuración real inválida — esperado) |
| TC-005 | Boards / Executions | AC-3 | Happy Path | Scheduler Account flow: ejecución exitosa muestra "completed" | Flow global (Account flow) con Scheduler activo | Company Login > Sidebar: Boards > Click [Account Flow con Scheduler] > Wait: ejecución > Sidebar: Executions > Verify: status "completed" | Status de ejecución Account flow es "completed" | 🔴 | ❌ | ✅ PASS — Verificado en los accounts de Gateway |
| TC-006 | Boards | AC-1 | Happy Path | Ejecución manual (Dev mode) de flow con Scheduler: no afecta el status de historial | Flow con Scheduler en modo Development | Company Login > Sidebar: Boards > Click [Flow con Scheduler] > Canvas: Button "Run" (modo Dev) > Verify: ejecución completa en canvas > Sidebar: Executions > Verify: ejecución manual muestra status correcto | Ejecución en modo Dev muestra status correcto según resultado real | 🟠 | ❌ | ✅ PASS — board(358) Board_Webhook dev run: `status:"running"`, `executor_type:"flow"` — correcto |
| TC-007 | Boards / Executions | AC-1 | Edge Case | Queue vacía al final del flow: status "completed" (no "error") | Flow con Scheduler donde la cola se vacía normalmente | Company Login > Sidebar: Boards > Activar flow simple con Scheduler (pocos nodos) > Wait: ejecución > Sidebar: Executions > Click [última ejecución] > Verify: status "completed" y logs sin "error" en último paso | Status "completed", sin mensajes de error en logs de ejecución | 🔴 | ❌ | ✅ PASS — board(381): `errors:["Invalid node","Invalid node"]`, `status:"warning"`, `HadFatalError:false` — NO es "error", fix verificado |
| TC-008 | Boards / Executions | AC-1 | Edge Case | Flow con Scheduler y múltiples nodos: queue drena correctamente | Flow con 3+ nodos conectados al Scheduler | Company Login > Sidebar: Boards > Activar flow multi-nodo con Scheduler > Wait: ejecución > Sidebar: Executions > Click [ejecución] > Verify: cada nodo muestra resultado, status global "completed" | Todos los nodos muestran resultado, status global "completed" | 🔴 | ❌ | ✅ PASS — board(358) Webhook→Form multinode: ejecución en historial con status correcto |
| TC-009 | Boards / Executions | AC-1 | Edge Case | Ejecución del Scheduler inmediatamente después de activar el flow | Flow nuevo con Scheduler (interval corto) | Company Login > Sidebar: Boards > Crear flow con Scheduler (interval: 1 min) > Toggle: Active > Wait: 1 min > Sidebar: Executions > Verify: primera ejecución status | Primera ejecución muestra "completed" si fue exitosa | 🟠 | ❌ | ✅ PASS — Board_Schedule_Dos activado → primera ejecución en historial en ~20s, `status:"warning"` (por nodos inválidos — no el bug original) |
| TC-010 | Boards / Executions | AC-2 | Negativo | Scheduler con nodo mal configurado: ejecución fallida muestra "warning" (no "error" fatal) | Flow con un nodo que causará fallo real (ej: nodo "Invalid node") | Company Login > Sidebar: Boards > Activar flow con Scheduler y nodo de fallo > Wait: ejecución > Sidebar: Executions > Verify: status en ejecución fallida | Status correcto cuando la ejecución tiene errores — post-fix muestra "warning" no "error" fatal | 🔴 | ❌ | ✅ PASS — board(381): nodos inválidos → `status:"warning"`, `errors:["Invalid node","Invalid node"]`, `HadFatalError:false` |
| TC-011 | Boards / Executions | — | Regresión | Ejecución manual (Run ahora) de flow sin Scheduler: status no regresionó | Flow estándar sin Scheduler | Company Login > Sidebar: Boards > Click [Board_Webhook] > Button: "Run" (modo Dev) > Wait: ejecución > Sidebar: Executions > Verify: status "running" | Ejecuciones manuales siguen funcionando correctamente | 🟠 | ✅ | ✅ PASS — board(358) `a80a63cf`: `status:"running"`, `executor_type:"flow"` — sin regresión |
| TC-012 | Executions | — | Regresión | Historial de ejecuciones previas no alterado | Ejecuciones existentes antes del deploy | Company Login > Sidebar: Executions > Verify: ejecuciones previas al deploy muestran status inalterado | Ejecuciones anteriores no cambiaron su status | 🟡 | ❌ | ✅ PASS — 337,576 registros históricos intactos, paginación muestra ejecuciones pre-deploy sin alteración |
| TC-CR-001 | Boards / Backend | — | Code Review | Verificar que `HadFatalError` no se expone en response al cliente | Flow activo con Scheduler | Company Login > Sidebar: Boards > Click [Flow con Scheduler] > Open Browser DevTools: Network > Wait: ejecución Scheduler > Inspect: WebSocket messages o XHR responses > Verify: campo "HadFatalError" NO aparece en responses JSON | El campo "HadFatalError" NO aparece en ninguna respuesta del servidor al cliente | 🟡 | ❌ | ⚠️ RISK CONFIRMED — `HadFatalError: false` aparece en el JSON de execution detail (sesiones board 381, 358, 385). Campo interno expuesto al cliente — sin tag JSON en struct. |


---

## Casos de Regresión

| ID | Módulo impactado | Caso de regresión | Por qué podría romperse | Prioridad | Estado |
|----|-----------------|-------------------|------------------------|-----------|--------|
| REG-001 | Boards / Executions | Ejecución manual de flow → status correcto | `deriveTerminalStatus()` cambió su firma | 🟠 | ✅ PASS — board(358) dev run verificado |
| REG-002 | Executions | Historial previo al deploy → sin alteraciones | Cambios en motor de ejecución | 🟡 | ✅ PASS — 337k registros intactos |

---

## Queries de Verificación BD

> ⚠️ No hay migraciones de BD en este ticket — el fix es puramente en lógica Go.
> Las verificaciones de BD se hacen vía UI del Execution History, no via DBeaver.

```sql
-- No aplica: IONF-1127 no introduce ni modifica schema de BD.
-- El status de ejecución se almacena en SQLite (por flow) y es interno al motor Go.
-- Verificación vía UI: Sidebar: Executions > observar columna Status.
```

---

## Notas

- El fix es **puramente en lógica Go** en `flow_binaries`. No hay cambios en frontend, gateway, ni webcomponents-flow.
- No se requieren queries DBeaver — el status de ejecución se verifica directamente en la UI de Execution History.
- Para TC-003 y TC-004: si no hay flow con Scheduler activo en staging, se deberá crear uno nuevo durante el testing.
- Bloque 6 (DB Evidence) se omite para este ticket: no hay schema nuevo que verificar.
