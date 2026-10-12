# Test Matrix — 86e1wfhcq (IONF-1085)
## API REST de workspace/company de IOND (FASE 2)

> Generado: 2026-10-08
> Basado en: ac-consolidated.md + risk-triage.md
> Modalidad: Por subtarea, consolidado en padre

## Resumen

| Métrica | Valor |
|---------|-------|
| Total de casos | 87 |
| Happy Path | 28 |
| Edge Case | 22 |
| Negativo | 16 |
| Seguridad | 10 |
| Regresión | 11 |
| Automatizables (API) | 72 |
| Solo UI | 15 |

---

## IONF-1279 — PAT y Autorización (14 TCs)

| ID | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-001 | AC-1.1 | Happy Path | Crear PAT con scopes y TTL 30d | Usuario autenticado en Keycloak, company seleccionada | `Company Login > Settings > API Tokens > Button: "Create Token" > Select scopes > Select TTL: 30 days > Button: "Create" > Verify: Token value displayed` | Token creado, valor visible, prefix `iondwk_` | 🔴 | ✅ | ⬜ |
| TC-002 | AC-1.2 | Happy Path | Token se muestra una sola vez | Token recién creado | `TC-001 > Copy token value > Close dialog > Navigate: API Tokens list > Verify: Token value NOT visible, only metadata` | Solo metadatos visibles, sin valor | 🔴 | ✅ | ⬜ |
| TC-003 | AC-1.3 | Happy Path | PAT aceptado como bearer en workspace | PAT válido | `API: GET /api/2.0/workspace/me > Header: Authorization: Bearer iondwk_... > Verify: 200 with user+company data` | 200 con datos del usuario y company | 🔴 | ✅ | ⬜ |
| TC-004 | AC-1.4 | Happy Path | Doble llave: scope+TPerm válidos → 200 | PAT con scope X, usuario tiene TPerm X | `API: GET /api/2.0/workspace/{recurso} > Verify: 200` | Operación exitosa | 🔴 | ✅ | ⬜ |
| TC-005 | AC-1.5 | Edge Case | Quitar TPerm → 403 → devolver → 200 sin reemitir token | PAT con scope, usuario con TPerm | `API: Verify 200 > Remove TPerm from user > API: Same request > Verify: 403 naming the permission > Restore TPerm > API: Same request > Verify: 200` | 403 con nombre del permiso; luego 200 sin nuevo token | 🔴 | ✅ | ⬜ |
| TC-006 | AC-1.6 | Seguridad | Usuario removido de company → PAT rechazado | PAT activo, usuario miembro | `API: Verify 200 > Remove user from company > API: Same request > Verify: rejection without revealing resources` | Rechazado sin fuga de datos | 🔴 | ✅ | ⬜ |
| TC-007 | AC-1.7 | Negativo | PAT expirado → 401 | PAT con TTL corto ya vencido | `API: GET /api/2.0/workspace/me > Header: Bearer expired_token > Verify: 401` | 401 Unauthorized | 🔴 | ✅ | ⬜ |
| TC-008 | AC-1.7 | Negativo | PAT revocado → 401 | PAT revocado desde UI | `Revoke token via API/UI > API: GET /api/2.0/workspace/me > Verify: 401` | 401 Unauthorized | 🔴 | ✅ | ⬜ |
| TC-009 | AC-1.8 | Seguridad | App token de /api/2.0/app rechazado en workspace | App token válido de Developer Apps | `API: GET /api/2.0/workspace/me > Header: Bearer app_token > Verify: 401 rejection, not converted to user principal` | 401, sin elevación de privilegios | 🔴 | ✅ | ⬜ |
| TC-010 | AC-1.10 | Edge Case | Token limit: crear token #4 con limit=3 | 3 tokens activos, WORKSPACE_TOKEN_LIMIT=3 | `API: POST create token (4th) > Verify: Error indicating limit reached` | Error, token no creado | 🟠 | ✅ | ⬜ |
| TC-011 | AC-1.11 | Happy Path | UI: Listar y revocar tokens | Tokens existentes | `Company Login > Settings > API Tokens > Verify: Tokens listed with metadata > Click [Revoke] on a token > Verify: Token removed from list` | Token revocado, desaparece | 🟠 | ❌ | ⬜ |
| TC-012 | AC-1.13 | Seguridad | Cross-company: ID de recurso de otra company → 404 | 2 companies con recursos | `API: GET /api/2.0/workspace/{resource}/{id_of_other_company} > Verify: 404 uniform (no data leak)` | 404 uniforme, sin información de la otra company | 🔴 | ✅ | ⬜ |
| TC-013 | AC-1.13 | Seguridad | ID malformado → mismo 404 | PAT válido | `API: GET /api/2.0/workspace/boards/not-a-uuid > Verify: 404 uniform (same as cross-company)` | Mismo 404 que cross-company | 🔴 | ✅ | ⬜ |
| TC-014 | AC-1.14 | Seguridad | Account-Id header no altera company | PAT de company A, Account-Id de company B | `API: GET /api/2.0/workspace/me > Header: Account-Id: other_company > Verify: Response shows company A, not B` | Company del PAT, no del header | 🔴 | ✅ | ⬜ |

---

## IONF-1284 — Connections y Connectors (8 TCs)

| ID | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-015 | AC-2.1 | Happy Path | Listar connections filtro app_name | Connections existentes | `API: GET /api/2.0/workspace/connections?app_name=X > Verify: 200 with filtered results` | Solo connections del app_name indicado | 🟠 | ✅ | ⬜ |
| TC-016 | AC-2.1 | Edge Case | Filtro app_name + tenant_app_name juntos | N/A | `API: GET /api/2.0/workspace/connections?app_name=X&tenant_app_name=Y > Verify: Error or one filter ignored` | No se aceptan ambos filtros | 🟡 | ✅ | ⬜ |
| TC-017 | AC-2.2 | Happy Path | Listar y buscar App Connectors instalados | Connectors instalados | `API: GET /api/2.0/workspace/connectors > Verify: 200 with catalog` | Catálogo de connectors visibles | 🟠 | ✅ | ⬜ |
| TC-018 | AC-2.3 | Happy Path | Ver connector con actions | Connector existente | `API: GET /api/2.0/workspace/connectors/{id} > Verify: Connector details with actions index` | Connector con índice de actions | 🟠 | ✅ | ⬜ |
| TC-019 | AC-2.4 | Happy Path | Ver contrato de action | Action existente | `API: GET /api/2.0/workspace/connectors/{id}/actions/{actionId} > Verify: parameters_spec_json, output_spec_json, sample_json with data` | Contrato completo con datos | 🟠 | ✅ | ⬜ |
| TC-020 | AC-2.5 | Negativo | Connector en borrador no aparece | Connector draft | `API: GET /api/2.0/workspace/connectors > Verify: Draft connector NOT in list` | Borrador excluido | 🟠 | ✅ | ⬜ |
| TC-021 | AC-2.6 | Seguridad | Connection de otra company → 404 | Connection de company B | `API: GET /api/2.0/workspace/connections/{id_company_B} > Verify: 404 uniform` | 404 uniforme | 🔴 | ✅ | ⬜ |
| TC-022 | AC-2.6 | Happy Path | Ver connection propia → sin datos sensibles | Connection existente | `API: GET /api/2.0/workspace/connections/{id} > Verify: No tokens, passwords, secrets in response` | Campos no sensibles solamente | 🟠 | ✅ | ⬜ |

---

## IONF-1285 — Boards (10 TCs)

| ID | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-023 | AC-3.1 | Happy Path | Listar boards de company | Boards existentes | `API: GET /api/2.0/workspace/boards > Verify: 200 with company boards` | Boards de la company del PAT | 🟠 | ✅ | ⬜ |
| TC-024 | AC-3.2 | Happy Path | Ver board por ID con nodos y schema | Board existente | `API: GET /api/2.0/workspace/boards/{id} > Verify: 200 with nodes and schema` | Board completo | 🟠 | ✅ | ⬜ |
| TC-025 | AC-3.3 | Happy Path | Ejecutar board → execution_id | Board válido, permisos OK | `API: POST /api/2.0/workspace/boards/{id}/executions > Verify: 200/202 with execution_id` | CompanyExecution creada, execution_id devuelto | 🔴 | ✅ | ⬜ |
| TC-026 | AC-3.4 | Edge Case | Board >5 min → 202 | Board con ejecución larga | `API: POST execute board (long running) > Verify: 202 with execution_id > API: GET execution > Verify: Status in progress` | 202 + consulta posterior | 🟠 | ✅ | ⬜ |
| TC-027 | AC-3.5 | Negativo | Sin execute-board → 403 | PAT sin permiso execute-board | `API: POST /api/2.0/workspace/boards/{id}/executions > Verify: 403` | 403 Forbidden | 🔴 | ✅ | ⬜ |
| TC-028 | AC-3.6 | Happy Path | Trigger type = api en execution | Board ejecutado vía API | `API: Execute board > API: GET /executions > Verify: trigger_type = "api"` | trigger_type = api | 🟠 | ✅ | ⬜ |
| TC-029 | AC-3.7 | Seguridad | Board de otra company → 404 | Board de company B | `API: GET /api/2.0/workspace/boards/{id_company_B} > Verify: 404` | 404 uniforme | 🔴 | ✅ | ⬜ |
| TC-030 | AC-3.9 | Edge Case | Board con connection de otro connector | Board con connection cruzada | `API: Execute board with wrong connection > Verify: Error "connection does not belong to this connector" before calling provider` | Error antes de llamar proveedor | 🔴 | ✅ | ⬜ |
| TC-031 | AC-3.10 | Happy Path | Nodo core Preview → 2 créditos | Board con nodo core | `API: Execute board in preview > Verify: 2 credits consumed` | 2 créditos cobrados | 🟠 | ✅ | ⬜ |
| TC-032 | AC-3.8 | Negativo | Flow de account no aparece como board | Flow de account existente | `API: GET /api/2.0/workspace/boards > Verify: Account flows NOT listed` | Solo boards de company | 🟠 | ✅ | ⬜ |

---

## IONF-1286 — CompanyExecution (8 TCs)

| ID | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-033 | AC-4.1 | Happy Path | Listar executions con filtros | Executions existentes | `API: GET /api/2.0/workspace/executions?status=completed&trigger_type=api > Verify: 200 filtered` | Filtrado correcto | 🟠 | ✅ | ⬜ |
| TC-034 | AC-4.2 | Happy Path | Ver execution por UUID | Execution existente | `API: GET /api/2.0/workspace/executions/{uuid} > Verify: 200 with details` | Detalle de execution | 🟠 | ✅ | ⬜ |
| TC-035 | AC-4.3 | Edge Case | Retention: execution vieja no aparece | Execution de hace 8 días, RETENTION=7 | `API: GET /api/2.0/workspace/executions > Verify: Old execution NOT in list` | Excluida por retención | 🟡 | ✅ | ⬜ |
| TC-036 | AC-4.4 | Happy Path | Ejecutar action → CompanyExecution + consumo 1 vez | Action de connector con connection | `API: POST /api/2.0/workspace/connectors/{id}/actions/{actionId}/execute > Header: Connection-Id > Verify: 200 + execution created + consumed once` | Execution + consumo exacto | 🔴 | ✅ | ⬜ |
| TC-037 | AC-4.5 | Happy Path | Ejecutar mapper → CompanyExecution + consumo | Mapper disponible | `API: POST mapper execute > Verify: Execution + consumption` | Mapper ejecutado, cobrado 1 vez | 🟠 | ✅ | ⬜ |
| TC-038 | AC-4.6 | Negativo | Action requiere connection, sin Connection-Id → 400 | Action que declara connection | `API: POST action execute (no Connection-Id) > Verify: 400, no execution, no charge` | 400, sin cobrar | 🔴 | ✅ | ⬜ |
| TC-039 | AC-4.7 | Negativo | Sin execute-app → 403 | PAT sin execute-app | `API: POST action execute > Verify: 403` | 403 | 🟠 | ✅ | ⬜ |
| TC-040 | AC-4.8 | Regresión | Devapp recurso único sin envoltorio | Account con recursos | `API: GET /api/2.0/app/accounts/{remote_id} > Verify: Response without wrapper (direct object, not {data: ...})` | Respuesta directa, sin `{data: ...}` | 🟠 | ✅ | ⬜ |

---

## IONF-1287 — Webhooks y Schedules (10 TCs)

| ID | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-041 | AC-5.1 | Happy Path | Listar webhooks por API | Webhooks existentes | `API: GET /api/2.0/workspace/webhooks > Verify: 200 list` | Lista de webhooks | 🟠 | ✅ | ⬜ |
| TC-042 | AC-5.1 | Happy Path | Habilitar/deshabilitar webhook API | Webhook existente | `API: POST disable > Verify: disabled > API: POST enable > Verify: enabled` | Toggle funciona | 🟠 | ✅ | ⬜ |
| TC-043 | AC-5.2 | Happy Path | Habilitar/deshabilitar desde UI tenant (Go) | Webhook existente | `Company Login > Sidebar: Connectors > Select connector > Webhooks tab > Toggle enable/disable > Verify: State changed` | UI funciona contra Go | 🟠 | ❌ | ⬜ |
| TC-044 | AC-5.3 | Edge Case | Deshabilitar webhook de app → no llama proveedor | Webhook de app | `API: POST disable app webhook > Verify: 200, no external call made` | Sin llamada externa | 🟠 | ✅ | ⬜ |
| TC-045 | AC-5.4 | Happy Path | Listar y pausar schedules | Schedules existentes | `API: GET schedules > POST pause > Verify: paused` | Schedule pausado | 🟠 | ✅ | ⬜ |
| TC-046 | AC-5.5 | Edge Case | Pausa sobrevive guardar board | Schedule pausado | `API: Pause schedule > Save board > Verify: Schedule still paused` | Pausa persiste | 🟠 | ✅ | ⬜ |
| TC-047 | AC-5.6 | Negativo | Schedule vencido → 409 | Schedule con fecha pasada | `API: POST resume expired schedule > Verify: 409` | 409 Conflict | 🟡 | ✅ | ⬜ |
| TC-048 | AC-5.8 | Regresión | Bug LIKE: board 1 y board 12 independientes | Board 1 con schedules, Board 12 con schedules | `Save Board 1 > Verify: Board 12 schedules untouched > Delete Board 1 > Verify: Board 12 schedules untouched` | Schedules de board 12 intactos | 🔴 | ✅ | ⬜ |
| TC-049 | AC-5.8 | Edge Case | Bug LIKE: board IDs 1, 10, 100, 11 | Boards con IDs similares | `Save Board 1 > Verify: Boards 10, 100, 11 schedules untouched` | Coincidencia exacta, no LIKE | 🔴 | ✅ | ⬜ |
| TC-050 | AC-5.7 | Negativo | Sin permiso read-cron → 403 | PAT sin read-cron | `API: GET schedules > Verify: 403` | 403 | 🟡 | ✅ | ⬜ |

---

## IONF-1288 — Authoring Connectors (12 TCs)

| ID | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-051 | AC-6.1 | Happy Path | Crear connector vía API | PAT con permisos | `API: POST /api/2.0/workspace/connectors > Body: {name, ...} > Verify: 201` | Connector creado | 🟠 | ✅ | ⬜ |
| TC-052 | AC-6.4 | Negativo | Name duplicado → 422 | Connector existente | `API: POST create connector (same name) > Verify: 422 "The name has already been taken."` | 422 con mensaje específico | 🟠 | ✅ | ⬜ |
| TC-053 | AC-6.2 | Negativo | Action inválida → 422 con errores y ruta | N/A | `API: POST create action (invalid) > Verify: 422 with all errors and their paths` | Errores validación estilo Laravel | 🟠 | ✅ | ⬜ |
| TC-054 | AC-6.5 | Happy Path | PATCH actualiza solo campos enviados | Connector existente | `API: PATCH connector (partial fields) > Verify: Only sent fields changed` | Update parcial | 🟠 | ✅ | ⬜ |
| TC-055 | AC-6.6 | Happy Path | Validate → no cambia; Publish → draft→active | Connector con actions draft | `API: POST validate > Verify: No changes > POST publish > Verify: draft→active, inactive unchanged` | Validate idempotente, publish correcto | 🔴 | ✅ | ⬜ |
| TC-056 | AC-6.6 | Negativo | Publish sin publish-app → 403 | PAT sin publish-app | `API: POST publish > Verify: 403` | 403 | 🟠 | ✅ | ⬜ |
| TC-057 | AC-6.7 | Negativo | Borrar connector en uso → 409 con lista | Connector usado por board/connection | `API: DELETE connector > Verify: 409 with list of who uses it` | 409 con detalle de uso | 🔴 | ✅ | ⬜ |
| TC-058 | AC-6.8 | Seguridad | Common cifrado, muestra ••••  | Auth-method con common | `API: GET auth-method > Verify: common shows "••••" > DB: Verify each value encrypted, keys visible` | Cifrado campo por campo, enmascarado | 🔴 | ✅ | ⬜ |
| TC-059 | AC-6.9 | Edge Case | Guardar sin tocar secreto → conserva valor | Auth-method con secreto | `API: PATCH auth-method (no common change) > Verify: Secret preserved in DB` | Secreto intacto | 🟠 | ✅ | ⬜ |
| TC-060 | AC-6.10 | Happy Path | UI edición connector funciona (Go) | Connector existente | `Company Login > Sidebar: Connectors > Edit connector > Modify fields > Save > Verify: Changes saved via Go API` | Edición vía Go exitosa | 🟠 | ❌ | ⬜ |
| TC-061 | AC-6.12 | Regresión | Motor lee common cifrado transparentemente | Connector con common cifrado | `Execute board using connector with encrypted common > Verify: Authentication works` | Flow ejecuta sin error auth | 🔴 | ✅ | ⬜ |
| TC-062 | AC-6.13 | Regresión | HTTP method uppercase: "post" → POST | Connector con method "post" en seeder | `Execute action with method "post" in DB > Verify: Request sent as POST to provider` | Método correcto al proveedor | 🟠 | ✅ | ⬜ |

---

## IONF-1291 — Persistent Data (11 TCs)

| ID | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-063 | AC-7.1 | Happy Path | CRUD structures | PAT con permisos | `API: POST create structure > GET > PATCH > DELETE > Verify each step` | CRUD completo | 🟠 | ✅ | ⬜ |
| TC-064 | AC-7.8 | Edge Case | Structure con todos los tipos del editor | N/A | `API: POST structure with text, number, date(ISO), boolean, select(options), binary, collection, array > Verify: 201` | Todos los tipos aceptados | 🟠 | ✅ | ⬜ |
| TC-065 | AC-7.8 | Negativo | Structure con tipo desconocido → 422 | N/A | `API: POST structure with type "unknown" > Verify: 422` | Tipo rechazado | 🟡 | ✅ | ⬜ |
| TC-066 | AC-7.5 | Happy Path | Registros: crear, PUT, PATCH, borrar, buscar | Store con structure | `API: POST record > PUT replace > PATCH merge > DELETE > POST search > Verify each` | CRUD registros completo | 🔴 | ✅ | ⬜ |
| TC-067 | AC-7.5 | Edge Case | Key repetida → 409 | Registro con key existente | `API: POST record with same key > Verify: 409` | 409 Conflict | 🟠 | ✅ | ⬜ |
| TC-068 | AC-7.10 | Negativo | Registro sin required en collection anidada → 422 | Structure con required en collection | `API: POST record missing required nested field > Verify: 422` | 422 validación | 🟠 | ✅ | ⬜ |
| TC-069 | AC-7.7 | Edge Case | Campo no en structure: API→422, board→guarda | Structure definida | `API: POST record with extra field > Verify: 422 > Board: Write same data via ion.store.add > Verify: Saved` | API strict, board permisivo | 🔴 | ✅ | ⬜ |
| TC-070 | AC-7.3 | Negativo | Borrar store en uso → 409 con boards | Store usado por board | `API: DELETE store > Verify: 409 with board list` | 409 con detalle | 🟠 | ✅ | ⬜ |
| TC-071 | AC-7.12 | Seguridad | Store ID no-UUID → validado antes de query | ID malformado | `API: GET /data-stores/not-a-uuid > Verify: 404 (no SQL injection)` | Validación UUID, sin inyección | 🔴 | ✅ | ⬜ |
| TC-072 | AC-7.6 | Regresión | Nodos ion.store.* funcionan igual post-refactor | Board con nodos store | `Execute board with ion.store.add, update, get, delete, search, count > Verify: Same behavior as before` | Comportamiento preservado | 🔴 | ✅ | ⬜ |
| TC-073 | AC-7.11 | Edge Case | Búsqueda: max 1000 resultados | Store con >1000 registros | `API: POST search with limit=2000 > Verify: Max 1000 returned` | Cap en 1000 | 🟡 | ✅ | ⬜ |

---

## IONF-1292 — PDF Templates (9 TCs)

| ID | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-074 | AC-8.1 | Happy Path | CRUD PDF template | PAT con permisos | `API: POST create > GET > PATCH (partial) > DELETE > Verify each` | CRUD completo, PATCH parcial | 🟠 | ✅ | ⬜ |
| TC-075 | AC-8.2 | Negativo | Schema pdfme inválido → 422 | N/A | `API: POST template with invalid pdfme JSON > Verify: 422` | Validación server-side | 🟠 | ✅ | ⬜ |
| TC-076 | AC-8.3 | Happy Path | Export → Import consistente | Template existente | `API: GET export > API: POST import (same JSON) > Verify: Identical template` | Import/export idempotente | 🟠 | ✅ | ⬜ |
| TC-077 | AC-8.4 | Happy Path | Spec muestra campos para imprimir | Template con campos | `API: GET /pdf-templates/{id}/spec > Verify: Fields listed` | Spec completo | 🟡 | ✅ | ⬜ |
| TC-078 | AC-8.5 | Happy Path | Imprimir → 2 créditos + 1 impresión | Template activo | `API: POST /pdf-templates/execute > Verify: 200 with PDF URL + 2 credits + 1 impression charged once` | Cobro exacto una vez | 🔴 | ✅ | ⬜ |
| TC-079 | AC-8.5 | Edge Case | Render falla → no cobra, devuelve impresión | Template que causa error render | `API: POST execute (trigger render failure) > Verify: No credits charged, impression returned` | Sin cobro en fallo | 🔴 | ✅ | ⬜ |
| TC-080 | AC-8.6 | Negativo | Template inactive → 409 | Template inactivo | `API: POST execute inactive template > Verify: 409` | 409 | 🟡 | ✅ | ⬜ |
| TC-081 | AC-8.6 | Negativo | Sin execute-pdf-template → 403 | PAT sin permiso | `API: POST execute > Verify: 403` | 403 | 🟠 | ✅ | ⬜ |
| TC-082 | AC-8.9 | Regresión | Total listado no cuenta borrados | Templates con algunos borrados | `API: GET /pdf-templates > Verify: Total excludes deleted` | Conteo correcto | 🟡 | ✅ | ⬜ |

---

## Transversales y Regresión (5 TCs)

| ID | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-083 | AC-9.1 | Regresión | Suite devapp /api/2.0/app pasa | Suite existente | `Run devapp test suite including spec and execute PDF > Verify: All pass` | Suite aprobada | 🔴 | ✅ | ⬜ |
| TC-084 | AC-9.4 | Happy Path | Graceful shutdown | Backend Go corriendo | `Send SIGTERM to backend > Verify: Stops accepting requests, finishes in-flight, closes clean` | Apagado limpio | 🟡 | ✅ | ⬜ |
| TC-085 | AC-9.5 | Happy Path | Cambiar company sin recargar | 2 companies, datos diferentes | `Company Login > Switch company (no reload) > Verify: Tokens, connectors, screens show new company data, no previous data` | Datos actualizados correctamente | 🟠 | ❌ | ⬜ |
| TC-086 | AC-9.6 | Edge Case | Diálogo token: no cierra con Esc | Token recién creado | `Create token > Dialog visible > Press Esc > Verify: Dialog remains open` | Diálogo no se cierra | 🟡 | ❌ | ⬜ |
| TC-087 | AC-9.13 | Regresión | Motor con common cifrado: flow con OAuth sigue autenticando | Connector OAuth con common cifrado | `After encrypting existing data > Execute flow with OAuth connector > Verify: Authentication succeeds` | Flow funciona post-cifrado | 🔴 | ✅ | ⬜ |

---

## Queries de Verificación BD

```sql
-- Fuente: gateway/database/migrations/ (nueva tabla workspace_tokens)
-- TC-001/TC-008: Verificar token creado y revocado
SELECT id, user_id, company_id, name, scopes, expires_at, revoked
FROM workspace_tokens
WHERE user_id = '<user_id>' AND company_id = '<company_id>';

-- TC-010: Verificar límite de tokens activos
SELECT COUNT(*)
FROM workspace_tokens
WHERE user_id = '<user_id>' AND company_id = '<company_id>' AND revoked = false AND (expires_at IS NULL OR expires_at > NOW());
-- Esperado: <= WORKSPACE_TOKEN_LIMIT

-- TC-058: Verificar cifrado de common
SELECT id, common FROM app_connections WHERE company_id = '<company_id>' LIMIT 1;
-- Verificar: Las claves del JSON son visibles, los valores están cifrados

-- TC-048/TC-049: Verificar schedules no afectados por bug LIKE
SELECT id, board_id FROM schedules WHERE board_id IN (1, 12, 10, 100);
-- Verificar antes y después de guardar board 1
```
