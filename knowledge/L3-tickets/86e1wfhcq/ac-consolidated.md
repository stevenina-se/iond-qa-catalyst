# Acceptance Criteria Consolidados — 86e1wfhcq (IONF-1085)
## API REST de workspace/company de IOND (FASE 2)

> Generado: 2026-10-08
> Fuentes: Descripción del ticket + 8 cierres de subtareas (Rodolfo 2026-10-05) + Decisiones QA
> Modalidad: Discovery individual por subtarea, consolidado en el padre

---

## Subtarea 1 — IONF-1279: PAT y Autorización (P0)
**ClickUp ID:** `86e30115a` | **Módulo:** Auth/API | **Riesgo:** 🔴 Crítico

### AC Originales (del ticket)

| ID | Acceptance Criteria | Verificable | Fuente |
|----|-------------------|-------------|--------|
| AC-1.1 | Un usuario autenticado en Keycloak puede crear un PAT (`iondwk_`) con scopes y TTL permitidos, ligado a su company | ✅ | Descripción IONF-1279 |
| AC-1.2 | El sistema muestra el valor completo del token UNA sola vez al crear | ✅ | Descripción IONF-1279 |
| AC-1.3 | `/api/2.0/workspace/` acepta el PAT como bearer token | ✅ | Descripción IONF-1279 |
| AC-1.4 | Scopes efectivos = scopes del PAT ∩ permisos TPerm actuales del usuario en la company | ✅ | Descripción IONF-1279 |
| AC-1.5 | Si el usuario pierde un TPerm, la ruta correspondiente responde 403 nombrando el permiso; al devolverlo, funciona sin crear otro token | ✅ | Cierre Rodolfo 2026-10-05 |
| AC-1.6 | Membresía del usuario en la company se revalida en cada request | ✅ | Descripción IONF-1279 |
| AC-1.7 | PAT revocado o vencido → 401 | ✅ | Descripción IONF-1279 |
| AC-1.8 | Credenciales client_credentials de `/api/2.0/app` son rechazadas en workspace | ✅ | Descripción IONF-1279 |

### AC Propuestos (del cierre del Developer + risk-triage)

| ID | Acceptance Criteria | Justificación | Fuente |
|----|-------------------|---------------|--------|
| AC-1.9 | `GET /api/2.0/workspace/me` responde datos del usuario y la company del token | Endpoint de identidad para validar el PAT | Cierre Rodolfo 2026-10-05 |
| AC-1.10 | Límite de tokens activos por usuario+company = `WORKSPACE_TOKEN_LIMIT` (default 3). Al intentar crear el token #4 → error | Variable de entorno configurable | Cierre Rodolfo 2026-10-05 |
| AC-1.11 | UI Settings → API Tokens: crear, listar metadatos (sin valor), revocar | Funcionalidad de frontend | Cierre Rodolfo 2026-10-05 |
| AC-1.12 | El servidor solo guarda el SHA-256 del token, nunca el valor en claro | Seguridad por diseño | Cierre Rodolfo 2026-10-05 |
| AC-1.13 | Recurso de otra company, inexistente o ID malformado → siempre el mismo 404 uniforme | Aislamiento cross-company | Cierre Rodolfo 2026-10-05 |
| AC-1.14 | `Account-Id` y `workspaceId` no alteran la company resuelta desde el PAT | Decisión transversal | Descripción padre IONF-1085 |

### AC Diferidos

| ID | Acceptance Criteria | Razón |
|----|-------------------|-------|
| AC-1.D1 | Helper de auditoría registra escrituras y rechazos cross-tenant | NO IMPLEMENTADO (NFS). Follow-up en otro ticket — Decisión QA |
| AC-1.D2 | Rate limiting diferenciado para PAT | No mencionado en cierre — follow-up |

### Transformación AC → Casos de Test

| AC | Happy Path | Edge Case | Negativo |
|----|-----------|-----------|----------|
| AC-1.1 | Crear PAT con scopes válidos y TTL 30d | Crear con TTL=sin vencimiento | Crear sin sesión Keycloak |
| AC-1.2 | Ver token al crear, cerrar → no se ve más | Cerrar diálogo con Esc | Intentar copiar token después de cerrar |
| AC-1.4 | Request con scope+TPerm válidos → 200 | Quitar TPerm → 403 → devolver → 200 | PAT con scope que no mapea a TPerm |
| AC-1.7 | Token vigente → 200 | Token al borde de expirar | Token expirado → 401, token revocado → 401 |
| AC-1.8 | PAT workspace → 200 en workspace | App token → 401 en workspace | PAT workspace → rechazado en /app |
| AC-1.10 | Crear tokens 1,2,3 → OK | Crear token #4 → error | Revocar 1 → crear nuevo → OK |
| AC-1.13 | GET recurso propio → 200 | GET ID inexistente → 404 | GET ID de otra company → 404 (mismo formato) |

---

## Subtarea 2 — IONF-1284: Connections y Connectors (P1)
**ClickUp ID:** `86e3011aq` | **Módulo:** Connections | **Riesgo:** 🟠 Alto

### AC Consolidados

| ID | Acceptance Criteria | Fuente |
|----|-------------------|--------|
| AC-2.1 | Listar connections filtrando por `app_name` O por `tenant_app_name`, nunca ambos | Cierre Rodolfo |
| AC-2.2 | Listar, buscar y ver App Connectors del catálogo instalado | Cierre Rodolfo |
| AC-2.3 | Ver connector con índice de sus actions | Cierre Rodolfo |
| AC-2.4 | Ver contrato de action: `parameters_spec_json`, `output_spec_json`, `sample_json` con datos | Cierre Rodolfo |
| AC-2.5 | Connectors en borrador NO aparecen ni se pueden usar | Cierre Rodolfo |
| AC-2.6 | Verificar connection propia → campos no sensibles; connection ajena → 404 uniforme | Descripción IONF-1284 |
| AC-2.7 | `Account-Id` ignorado/rechazado en superficie workspace | Descripción IONF-1284 |

---

## Subtarea 3 — IONF-1285: Boards list/get/execute (P1)
**ClickUp ID:** `86e3011cy` | **Módulo:** Boards | **Riesgo:** 🔴 Crítico

### AC Consolidados

| ID | Acceptance Criteria | Fuente |
|----|-------------------|--------|
| AC-3.1 | Listar boards visibles de la company del PAT | Descripción IONF-1285 |
| AC-3.2 | Ver board por ID (con nodos y schema) solo si pertenece a la company | Cierre Rodolfo |
| AC-3.3 | Ejecutar board autorizado → crea CompanyExecution, devuelve execution_id | Descripción IONF-1285 |
| AC-3.4 | Ejecución <5 min → 200 con resultado; >5 min → 202 y sigue corriendo | Cierre Rodolfo |
| AC-3.5 | Requiere permiso `execute-board` (backfill desde `update-board`) | Cierre Rodolfo |
| AC-3.6 | Trigger registrado como `api` | Cierre Rodolfo |
| AC-3.7 | Board de otra company → 404 uniforme | Descripción IONF-1285 |
| AC-3.8 | Flow de account `/api/2.0/app` no aparece como board de company | Descripción IONF-1285 |
| AC-3.9 | NUEVO: Board con connection de otro connector falla ANTES de llamar al proveedor con "connection does not belong to this connector" | Cierre Rodolfo (padre) |
| AC-3.10 | NUEVO: Nodo core en Preview cuesta 2 créditos, igual que producción | Cierre Rodolfo (padre) |

---

## Subtarea 4 — IONF-1286: CompanyExecution (P1)
**ClickUp ID:** `86e3011f2` | **Módulo:** Executions | **Riesgo:** 🟠 Alto

### AC Consolidados

| ID | Acceptance Criteria | Fuente |
|----|-------------------|--------|
| AC-4.1 | Listar executions de company con filtros: `status`, `board_id`, `trigger_type`, `date_from`, `date_to` | Cierre Rodolfo |
| AC-4.2 | Ver execution por UUID | Cierre Rodolfo |
| AC-4.3 | Solo executions de los últimos `EXECUTION_RETENTION_DAYS` (default 7) aparecen | Cierre Rodolfo |
| AC-4.4 | Ejecutar action de connector → crea CompanyExecution + consume 1 vez via `Executable` | Cierre Rodolfo |
| AC-4.5 | Ejecutar mapper → crea CompanyExecution + consume 1 vez | Cierre Rodolfo |
| AC-4.6 | `Connection-Id` opcional; action que requiere connection sin ella → 400 sin crear execution ni cobrar | Cierre Rodolfo |
| AC-4.7 | Permiso `execute-app` (backfill desde `update-board`). Sin él → 403 | Cierre Rodolfo |
| AC-4.8 | REGRESIÓN: Devapp recursos únicos de accounts sin envoltorio (FR-028) | Cierre Rodolfo — Decisión QA: caso de regresión |

### AC Diferidos

| ID | Razón |
|----|-------|
| Logs de execution por execution_id | Diferido a otro ticket (cierre Rodolfo) |
| Control por execution_id (cancelar, reintentar) | Diferido a otro ticket (cierre Rodolfo) |

---

## Subtarea 5 — IONF-1287: Webhooks y Schedules (P1)
**ClickUp ID:** `86e3011gr` | **Módulo:** Webhooks | **Riesgo:** 🟠 Alto

### AC Consolidados

| ID | Acceptance Criteria | Fuente |
|----|-------------------|--------|
| AC-5.1 | Webhooks: listar, ver, habilitar y deshabilitar por API y UI | Cierre Rodolfo |
| AC-5.2 | Habilitar/deshabilitar migrado a Go; rutas Laravel `@deprecated` hasta deploy frontend | Cierre Rodolfo |
| AC-5.3 | Deshabilitar webhook de app NO llama al proveedor | QA instructions padre |
| AC-5.4 | Schedules: listar, ver, pausar y reanudar | Cierre Rodolfo |
| AC-5.5 | La pausa de schedule sobrevive a guardar el board | Cierre Rodolfo |
| AC-5.6 | Schedule vencido → 409 | Cierre Rodolfo |
| AC-5.7 | Permisos `create/read/update/delete-cron` (backfill desde `read-board`/`update-board`) | Cierre Rodolfo |
| AC-5.8 | BUG FIX: Guardar/borrar board 1 NO toca schedules de board 12 (fix del LIKE → coincidencia exacta) | Cierre Rodolfo |

### AC Diferidos

| ID | Razón |
|----|-------|
| Crear, editar, borrar webhooks y schedules | Diferido a fase MCP (cierre Rodolfo) |
| Secreto de firma de webhooks | Diferido a ticket aparte (cierre Rodolfo) |

---

## Subtarea 6 — IONF-1288: Authoring de App Connectors (P1)
**ClickUp ID:** `86e3011j1` | **Módulo:** Connectors | **Riesgo:** 🔴 Crítico

### AC Consolidados

| ID | Acceptance Criteria | Fuente |
|----|-------------------|--------|
| AC-6.1 | CRUD connector + actions + auth-methods + webhooks | Cierre Rodolfo |
| AC-6.2 | Motor validación (`packages/validation`): errores 422 con ruta, estilo Laravel | Cierre Rodolfo |
| AC-6.3 | `name` obligatorio, único en company sin sufijo, fijo de por vida | Cierre Rodolfo |
| AC-6.4 | Name duplicado → 422 "The name has already been taken." | Cierre Rodolfo |
| AC-6.5 | Actualizar = PATCH: solo cambia lo que se manda | Cierre Rodolfo |
| AC-6.6 | `validate` no cambia nada. `publish` valida completo y pasa draft→active. Requiere `publish-app` | Cierre Rodolfo |
| AC-6.7 | Borrar o despublicar en uso por board/connection/suscripción → 409 con lista de quién lo usa | Cierre Rodolfo |
| AC-6.8 | `common` de auth-methods cifrado campo por campo; nunca en claro; se muestra `••••` | Cierre Rodolfo |
| AC-6.9 | Guardar sin tocar secreto lo conserva | QA instructions padre |
| AC-6.10 | UI edición migrada a Go; wizard creación sigue en Laravel | Cierre Rodolfo |
| AC-6.11 | Workspace acepta solo JSON; UI tenant acepta JSONC | Cierre Rodolfo |
| AC-6.12 | Motor lee common cifrado transparentemente; filas viejas en claro siguen leyéndose | QA instructions padre |
| AC-6.13 | Método HTTP de actions siempre en mayúsculas (post → POST) | QA instructions padre |

---

## Subtarea 7 — IONF-1291: Persistent Data (P2)
**ClickUp ID:** `86e3011n0` | **Módulo:** Data Store | **Riesgo:** 🔴 Crítico

### AC Consolidados

| ID | Acceptance Criteria | Fuente |
|----|-------------------|--------|
| AC-7.1 | Structures: listar, ver, crear, editar, borrar | Cierre Rodolfo |
| AC-7.2 | Stores: listar, ver, crear, editar, borrar | Cierre Rodolfo |
| AC-7.3 | Borrar store en uso por board → 409 con lista de boards; sin uso → borra con contenido en transacción | Cierre Rodolfo |
| AC-7.4 | Borrar structure en uso por store → 409 | Cierre Rodolfo |
| AC-7.5 | Registros: crear (con/sin key; key repetida → 409), PUT reemplaza, PATCH combina (arrays al final), borrar, buscar | Cierre Rodolfo |
| AC-7.6 | API y nodos `ion.store.*` usan el mismo servicio de registros (extraído sin cambiar comportamiento) | Cierre Rodolfo |
| AC-7.7 | API valida strict contra structure; boards NO (comportamiento preservado) | Cierre Rodolfo |
| AC-7.8 | Spec de structures acepta: text, number, date (con formato), boolean, select (con opciones), binary, collection (anidada), array | Cierre Rodolfo |
| AC-7.9 | Names de campo libres (`first-name` válido), escapados en SQL | Cierre Rodolfo |
| AC-7.10 | Validación API: required en todos niveles, select en opciones, collection anidada, date según formato (ISO/TIMESTAMP) | Cierre Rodolfo |
| AC-7.11 | Búsqueda: 100 resultados default, max 1000 | Cierre Rodolfo |
| AC-7.12 | SEGURIDAD: ID de store se valida como UUID antes de consulta (fix SQL injection) | Cierre Rodolfo |
| AC-7.13 | UI tenant para structures y stores usa misma validación que API | Cierre Rodolfo |

---

## Subtarea 8 — IONF-1292: PDF Templates (P2)
**ClickUp ID:** `86e3011nj` | **Módulo:** PDF Templates | **Riesgo:** 🟠 Alto

### AC Consolidados

| ID | Acceptance Criteria | Fuente |
|----|-------------------|--------|
| AC-8.1 | CRUD: listar, ver, crear, editar, borrar. PATCH escribe solo lo enviado | Cierre Rodolfo |
| AC-8.2 | JSON pdfme validado en servidor (páginas, tipos campo, fuentes, geometría) | Cierre Rodolfo |
| AC-8.3 | Importar/exportar: mismo JSON que la UI. Export UI → Import API y viceversa | Cierre Rodolfo |
| AC-8.4 | `GET /pdf-templates/{id}/spec` muestra campos para imprimir | Cierre Rodolfo |
| AC-8.5 | `POST /pdf-templates/execute` → 2 créditos + 1 impresión, 1 sola vez; falla → no cobra + devuelve impresión | Cierre Rodolfo |
| AC-8.6 | Template `inactive` → 409; sin `execute-pdf-template` → 403 | Cierre Rodolfo |
| AC-8.7 | Permiso `execute-pdf-template` (backfill a quien tiene `execute-board`) | Cierre Rodolfo |
| AC-8.8 | Contrato devapp no cambió; hay tests de regresión | Cierre Rodolfo |
| AC-8.9 | FIX: Total del listado ya no cuenta templates borrados | Cierre Rodolfo |

### AC Diferidos

| ID | Razón |
|----|-------|
| Clonar, preview, assets | Diferido (cierre Rodolfo) |
| Versionado | Diferido (cierre Rodolfo) |

---

## Familia 9 — Transversales, Regresión y UI (padre IONF-1085)

### AC Consolidados

| ID | Acceptance Criteria | Fuente |
|----|-------------------|--------|
| AC-9.1 | Suite devapp `/api/2.0/app` sigue pasando (spec + execute PDF) | QA instructions padre |
| AC-9.2 | REGRESIÓN: Recursos únicos accounts sin envoltorio | Cierre Rodolfo IONF-1286 |
| AC-9.3 | Precios centralizados en tabla `executable` | QA instructions padre |
| AC-9.4 | Graceful shutdown (SIGINT/SIGTERM): deja de aceptar, espera en curso, cierra | QA instructions padre |
| AC-9.5 | Cambiar company sin recargar: datos actualizados, sin datos anteriores | QA instructions padre |
| AC-9.6 | Diálogo token no se cierra con Esc ni clic afuera sin confirmar | QA instructions padre |
| AC-9.7 | Webhook con `/` en nombre se puede editar y borrar | QA instructions padre |
| AC-9.8 | Auth-method `api_key` funciona correctamente | QA instructions padre |
| AC-9.9 | Wizard crear connector sigue funcionando igual | QA instructions padre |
| AC-9.10 | Editar detalles, base, auth-method, action, webhook en UI connectors | QA instructions padre |
| AC-9.11 | Action status ya no ofrece `deprecated` | QA instructions padre |
| AC-9.12 | UI tenant: crear/editar structures, stores, PDF templates con validación nueva | QA instructions padre |
| AC-9.13 | Board con connector cuyo common tiene OAuth/client_secret → autentica correctamente después de cifrar datos existentes | QA instructions padre |

---

## Estadísticas Totales

| Subtarea | ACs activos | ACs diferidos |
|----------|-------------|---------------|
| IONF-1279 (PAT) | 14 | 2 |
| IONF-1284 (Connections) | 7 | 0 |
| IONF-1285 (Boards) | 10 | 0 |
| IONF-1286 (Executions) | 8 | 2 |
| IONF-1287 (Webhooks/Schedules) | 8 | 2 |
| IONF-1288 (Authoring) | 13 | 0 |
| IONF-1291 (Data Store) | 13 | 0 |
| IONF-1292 (PDF Templates) | 9 | 2 |
| Transversales (padre) | 13 | 0 |
| **TOTAL** | **95** | **8** |
