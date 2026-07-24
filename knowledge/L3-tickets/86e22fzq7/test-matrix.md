# Test Matrix — 86e22fzq7

## Resumen

| Métrica | Valor |
|---------|-------|
| Total de casos | 17 |
| Ejecutados | 17 |
| PASS | 17 |
| FAIL | 0 |
| Smoke tests | 2 |
| Happy Path | 3 |
| Edge Cases | 4 |
| Negativos | 2 |
| Regresión | 3 |
| DB Evidence | 1 |
| Code Review | 2 |
| Automatizables | 5 |
| Cobertura de AC | 6/6 |
| **Veredicto** | **✅ READY TO SHIP** |

### Acceptance Criteria (reconciliados)

- **AC-1**: Reauthorize actualiza la conexión existente, no crea duplicado
- **AC-2**: Toasts de éxito suprimidos durante reauthorize
- **AC-3**: Toasts de éxito intactos en creación de nueva conexión
- **AC-4**: Tenant app connections sin regresiones al reauthorize
- **AC-5**: Flows que referencian la conexión usan credenciales actualizadas post-reauthorize
- **AC-6**: Ambos flujos de auth (OAuth/authorizing y API Key/success inmediato) funcionan

---

## Test Matrix

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|----|------|-------------|--------------|-------|--------------------|-----------|---------------|--------|
| TC-001 | Connections | AC-1 | Smoke | Vista de Connections carga con conexiones existentes | Company con al menos 1 conexión API Key activa | Company Login > Sidebar: Connections > Verify: lista de connections carga correctamente > Verify: conexión API Key visible en la lista | Lista de connections carga, conexión API Key visible con status activo | 🔴 | ✅ | ✅ **PASS** — 2026-07-14 |
| TC-002 | Connections | AC-1 | Smoke | Botón Reauthorize visible en conexión existente | Company con conexión API Key activa | Company Login > Sidebar: Connections > Click [conexión API Key] > Verify: botón "Reauthorize" visible | Botón "Reauthorize" visible y habilitado en la vista de detalle/edición de la conexión | 🔴 | ✅ | ✅ **PASS** — 2026-07-14 |
| TC-003 | Connections | AC-1 | Happy Path | Reauthorize API Key — conexión actualizada, sin duplicado | Company con conexión API Key activa. Contar conexiones antes del test. | Company Login > Sidebar: Connections > Contar conexiones totales (N) > Click [conexión API Key] > Button: "Reauthorize" > Fill: nueva API Key > Completar proceso > Sidebar: Connections > Contar conexiones totales > Verify: cantidad = N (no N+1) > Verify: conexión existente actualizada | La cantidad de conexiones es la misma. No se creó duplicado. La conexión existente tiene las credenciales actualizadas. | 🔴 | ❌ | ✅ **PASS** — 2026-07-14 |
| TC-004 | Connections | AC-2 | Happy Path | Reauthorize API Key — sin toasts de éxito | Company con conexión API Key activa | Company Login > Sidebar: Connections > Click [conexión API Key] > Button: "Reauthorize" > Fill: nueva API Key > Completar proceso > Verify: NO aparece toast "Connection approved successfully" > Verify: NO aparece toast "Connection validated successfully" | No se muestra ningún toast de éxito durante la reautorización | 🔴 | ✅ | ✅ **PASS** — 2026-07-14 |
| TC-005 | Connections | AC-3 | Happy Path | Crear conexión nueva — toasts aparecen normalmente | Company con app connector disponible | Company Login > Sidebar: Connections > Button: "Create" (o workflow de nueva conexión) > Completar proceso de creación con API Key > Verify: toast "Connection approved/validated successfully" aparece | Toast de éxito visible al crear nueva conexión (no fue suprimido) | 🔴 | ✅ | ✅ **PASS** — 2026-07-14 |
| TC-006 | Connections | AC-6 | Edge Case | Reauthorize conexión OAuth (flujo authorizing con popup) | Company con conexión OAuth activa (ej: Google, Slack) | Company Login > Sidebar: Connections > Click [conexión OAuth] > Button: "Reauthorize" > Verify: popup OAuth abre normalmente > Completar OAuth flow > Verify: no se crea conexión duplicada > Verify: no aparece toast de éxito | Popup OAuth funciona. Conexión actualizada sin duplicado. Sin toasts. | 🟠 | ❌ | ✅ **PASS** — 2026-07-14 |
| TC-007 | Connections | AC-4 | Edge Case | Reauthorize conexión de tenant app — sin regresiones | Company con conexión de tenant app (no global) | Company Login > Sidebar: Connections > Click [conexión de tenant app] > Button: "Reauthorize" > Completar proceso > Verify: funciona igual que antes del fix | El flujo de tenant app no cambió. Reauthorize funciona sin errores. | 🟠 | ❌ | ✅ **PASS** — 2026-07-14 |
| TC-008 | Connections | AC-1 | Edge Case | Reauthorize con connection_id inválido — no crash | Intentar reauthorize con una conexión que ya fue eliminada o ID inválido | Company Login > Sidebar: Connections > Manipular URL con connectionId inexistente > Verify: el sistema maneja el error gracefully | Mensaje de error apropiado. No crash. No duplicado. | 🟡 | ❌ | ✅ **PASS** — 2026-07-14 |
| TC-009 | Connections | AC-2 | Edge Case | Reauthorize seguido de creación nueva — toasts correctos en cada flujo | Company con conexión existente + app disponible | Company Login > Sidebar: Connections > Click [conexión] > Button: "Reauthorize" > Completar > Verify: sin toast > Sidebar: Connections > Button: "Create new" > Completar creación > Verify: toast aparece | En reauthorize: 0 toasts. En creación nueva inmediatamente después: toast aparece. La lógica `isReauthorize` se resetea correctamente. | 🟠 | ❌ | ✅ **PASS** — 2026-07-14 |
| TC-010 | Connections | AC-3 | Negativo | Crear conexión nueva — sin suppressión accidental de toasts | Company con app disponible, sin haber hecho reauthorize antes | Company Login > Sidebar: Connections > Crear nueva conexión desde cero (no reauthorize) > Completar proceso > Verify: toast de éxito aparece normalmente | El toast de éxito se muestra. La supresión solo aplica cuando `connectionId` prop está presente (reauthorize). | 🟠 | ✅ | ✅ **PASS** — 2026-07-14 |
| TC-011 | Connections | AC-1 | Negativo | Multi-tenant: reauthorize no afecta conexiones de otra company | Dos companies con conexiones API Key. Company A reauthorize su conexión. | Company Login (Company A) > Sidebar: Connections > Click [conexión API Key] > Button: "Reauthorize" > Completar > Company Login (Company B) > Sidebar: Connections > Verify: conexiones de Company B intactas | Las conexiones de Company B no fueron afectadas por el reauthorize de Company A. Aislamiento multi-tenant preservado. | 🟠 | ❌ | ✅ **PASS** — 2026-07-14 |
| TC-012 | Connections / Boards | AC-5 | Regresión | Flow con conexión reautorizada ejecuta con credenciales nuevas | Flow activo que usa nodo con la conexión reautorizada | Company Login > Sidebar: Connections > Click [conexión API Key del flow] > Button: "Reauthorize" > Completar > Sidebar: Boards > Click [Board con flow que usa la conexión] > Canvas: Button "Run" > Wait: ejecución > Verify: nodo de app ejecuta correctamente con nuevas credenciales | El flow ejecuta exitosamente usando las credenciales actualizadas de la conexión reautorizada | 🟠 | ❌ | ✅ **PASS** — 2026-07-14 |
| TC-013 | Connections | AC-6 | Regresión | OAuth flow completo (create new) no tiene regresiones | Company con app OAuth disponible | Company Login > Sidebar: Connections > Crear nueva conexión OAuth > Completar popup OAuth > Verify: conexión creada exitosamente > Verify: toast de éxito aparece | La creación de conexiones OAuth sigue funcionando como antes. Sin regresiones del refactor de `testAttempt`. | 🟠 | ❌ | ✅ **PASS** — 2026-07-14 |
| TC-014 | Connections | AC-4 | Regresión | Lista de connections post-reauthorize no muestra duplicados ni corrupción | Company con varias conexiones de diferentes tipos | Company Login > Sidebar: Connections > Reauthorize una conexión API Key > Sidebar: Connections > Verify: lista intacta, sin duplicados, conteo correcto > Verificar cada conexión tiene status correcto | La lista de connections está limpia. Sin duplicados. Todas las conexiones muestran status correcto. | 🟡 | ✅ | ✅ **PASS** — 2026-07-14 |
| TC-015 | Connections | AC-1 | DB Evidence | BD: no hay registros duplicados post-reauthorize | Reauthorize completado (TC-003) | Verificar vía UI o API: listar connections de la company > Verify: la connection reautorizada tiene un solo registro > Verify: no hay connections con mismo `app_name` + `app_id` duplicados | Un solo registro para la connection reautorizada en BD. No hay duplicados. | 🟡 | ❌ | ✅ **PASS** — 2026-07-14 |
| TC-CR-001 | Connections | — | Code Review | Reauthorize con connection eliminada — frontend maneja error gracefully | Connection eliminada entre apertura del dialog y click de reauthorize | Company Login > Sidebar: Connections > Click [conexión API Key] > Button: "Reauthorize" > (simular eliminación de connection en otra pestaña) > Completar reauthorize > Verify: error manejado gracefully, sin loader infinito, sin dialog colgado | Mensaje de error claro. Dialog se cierra o muestra error. No queda en estado inconsistente. | 🟠 | ❌ | ✅ **PASS** — 2026-07-14 |
| TC-CR-002 | Connections | — | Code Review | Post-reauthorize: lista de connections se refresca con credenciales actualizadas | Reauthorize completado exitosamente (TC-003) | Company Login > Sidebar: Connections > Click [conexión API Key] > Button: "Reauthorize" > Completar > Verify: dialog se cierra > Verify: lista de connections se actualiza > Verify: la conexión muestra datos actualizados (ej: fecha de última modificación) | La lista se refresca. La conexión muestra timestamp actualizado. No se necesita refresh manual de la página. | 🟡 | ❌ | ✅ **PASS** — 2026-07-14 |

---

## Casos de Regresión

| ID | Módulo impactado | Caso de regresión | Por qué podría romperse | Prioridad | Estado |
|----|-----------------|-------------------|------------------------|-----------|--------|
| REG-001 | Connections / OAuth | Creación de nueva conexión OAuth → toasts intactos | Refactor de `testAttempt` en helpers puede haber cambiado el flujo | 🟠 | ✅ **PASS** — 2026-07-14 |
| REG-002 | Connections / Tenant | Reauthorize de tenant app → funciona como antes | Developer dice "not changed", pero comparte código refactorizado | 🟠 | ✅ **PASS** — 2026-07-14 |
| REG-003 | Boards | Flow con conexión reautorizada → credenciales actualizadas | Si el update fue in-place pero el runtime de flow cachea credenciales | 🟠 | ✅ **PASS** — 2026-07-14 |

---

## Queries de Verificación BD

> Nota: Las connections se almacenan en PostgreSQL (gateway). Las credenciales están encriptadas (trait `Encryptable`).
> Verificación principal será vía UI (lista de connections) debido a la encriptación.

```sql
-- Verificar que no hay connections duplicadas para la misma app+company
-- Fuente: gateway/database/migrations/ (tabla connections)
-- NOTA: Verificar nombres exactos de tabla y columnas contra migraciones antes de ejecutar
SELECT app_id, COUNT(*) as total
FROM connections
WHERE company_id = [COMPANY_ID]
GROUP BY app_id
HAVING COUNT(*) > 1;
-- Resultado esperado: 0 filas (sin duplicados)
```

---

## Notas

- El fix toca **dos repos**: backend (`flow_binaries`) para el upsert logic y frontend (`gateway-ion`) para los toasts.
- **No hay tests automatizados** del developer para este fix — esto aumenta la importancia del testing manual.
- El Developer no mencionó conexiones de tipo Basic Auth o Client Credentials — asumir que el fix aplica a todos los tipos pero priorizar API Key y OAuth.
- Para TC-011 (multi-tenant): se necesitan credenciales de dos companies diferentes.
- Para TC-012 (flows con conexión): se necesita un flow activo que use la conexión a reauthorize.
