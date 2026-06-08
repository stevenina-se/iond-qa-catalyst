# Test Matrix — IONF-996

> Generada por `test-docs/document` (modo matrix)
> Fecha: 2026-06-02
> Módulos: Connections, Integrations, Accounts

## Resumen

| Métrica | Valor |
|---------|-------|
| Total de casos | 30 |
| Happy path | 8 |
| Edge cases | 7 |
| Negativos | 9 |
| Regresión | 6 |
| Automatizables | 28 |
| Cobertura de AC | 6/6 |

---

## Acceptance Criteria Derivados

> Los AC originales del ticket están incompletos (Gherkin con When/Then vacíos). Se derivaron AC funcionales del análisis técnico y del formulario de cambios del Developer.

| ID | AC |
|----|----|
| AC-1 | Las apps externas (M2M) pueden crear, leer, actualizar y eliminar connections de un account vía API app-scope |
| AC-2 | Las apps externas pueden instalar una integración (grapp) para un account vía API app-scope, obteniendo `integration_id` y `gateway_key` |
| AC-3 | El campo `connection` (secreto) NUNCA se expone en las respuestas JSON |
| AC-4 | Los 4 nuevos scopes (`app:connection-read/create/update/delete`) controlan el acceso a cada operación |
| AC-5 | La columna `connection` se encripta correctamente y se espeja en `data` |
| AC-6 | El account se resuelve del binding de ruta (`remote_id`), el app del token M2M (NO del body) |

---

## Test Matrix

### Connections CRUD — Happy Path

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-001 | Connections | AC-1 | Happy Path | Listar connections de un account | Account existente con ≥1 connection, token M2M con scope `app:connection-read` | 1. Obtener token M2M con scope `app:connection-read` 2. `GET /api/2.0/app/accounts/{remote_id}/connections` 3. Verificar response | 200 OK — Lista paginada de connections. Cada connection NO contiene campo `connection` (secreto) | 🔴 | ✅ | ⬜ Pendiente |
| TC-002 | Connections | AC-1 | Happy Path | Ver detalle de una connection | Connection existente, token con scope `app:connection-read` | 1. Obtener token M2M 2. `GET /api/2.0/app/accounts/{remote_id}/connections/{connectionId}` 3. Verificar campos del response | 200 OK — Detalle con `name`, `service_id`, `data`, `metadata`. Campo `connection` (secreto) NO presente | 🔴 | ✅ | ⬜ Pendiente |
| TC-003 | Connections | AC-1, AC-5 | Happy Path | Crear connection con todos los campos | Account existente, token con scope `app:connection-create`, service_id válido | 1. Obtener token M2M con scope `app:connection-create` 2. `POST /api/2.0/app/accounts/{remote_id}/connections` con body: `{name, service_id, data, connection, metadata}` 3. Verificar response 4. Verificar en BD que `connection` está encriptado y `data` espeja | 201 Created — Connection creada. En BD: columna `connection` encriptada, columna `data` con espejo. Response NO expone `connection` | 🔴 | ✅ | ⬜ Pendiente |
| TC-004 | Connections | AC-1, AC-5 | Happy Path | Actualizar connection CON campo `connection` | Connection existente, token con scope `app:connection-update` | 1. Obtener token M2M 2. `PUT /api/2.0/app/accounts/{remote_id}/connections/{id}` con body: `{name: "nuevo", connection: {new_secret}}` 3. Verificar response 4. Verificar en BD | 200 OK — Name actualizado, `connection` re-encriptado con nuevo valor, `data` espeja el nuevo valor | 🔴 | ✅ | ⬜ Pendiente |
| TC-005 | Connections | AC-1, AC-5 | Happy Path | Actualizar connection SIN campo `connection` | Connection existente con secreto, token con scope `app:connection-update` | 1. Obtener token M2M 2. `PUT /api/2.0/app/accounts/{remote_id}/connections/{id}` con body: `{name: "solo nombre"}` (sin campo `connection`) 3. Verificar en BD | 200 OK — Name actualizado. Secreto original PRESERVADO (no se borró ni se puso null) | 🔴 | ✅ | ⬜ Pendiente |
| TC-006 | Connections | AC-1 | Happy Path | Eliminar connection | Connection existente, token con scope `app:connection-delete` | 1. Obtener token M2M 2. `DELETE /api/2.0/app/accounts/{remote_id}/connections/{id}` 3. Verificar response 4. Verificar que GET retorna 404 | 200/204 — Connection eliminada. GET subsecuente retorna 404 | 🔴 | ✅ | ⬜ Pendiente |

### Install Integration — Happy Path

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-007 | Integrations | AC-2, AC-6 | Happy Path | Instalar integración (grapp) para un account | Account existente, service válido, token con scope `app:integration-create` | 1. Obtener token M2M con scope `app:integration-create` 2. `POST /api/2.0/app/accounts/{remote_id}/integrations` con body: `{service_id, name}` 3. Verificar response contiene `integration_id` y `gateway_key` 4. Verificar en BD | 201 Created — Integración creada con `integration_id` y `gateway_key` en response. Config vacía `{}`. Account del binding de ruta, app del token | 🔴 | ✅ | ⬜ Pendiente |
| TC-008 | Connections | AC-1 | Happy Path | Listar connections con parámetros de paginación | Account con ≥3 connections | 1. `GET /connections?per_page=2&order_by=name&order_direction=asc` 2. Verificar paginación 3. Verificar ordenamiento | 200 OK — Máx 2 resultados por página, ordenados por name ASC. Metadata de paginación presente | 🟠 | ✅ | ⬜ Pendiente |

### Edge Cases

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-009 | Connections | AC-1 | Edge Case | Crear connection sin campo `data` (opcional) | Token válido, account existente | 1. `POST /connections` con body: `{name, service_id, connection: {...}}` (sin `data`) 2. Verificar creación | 201 Created — Connection creada con `data` null o vacío. Sin error | 🟠 | ✅ | ⬜ Pendiente |
| TC-010 | Connections | AC-1 | Edge Case | Crear connection sin campo `metadata` (opcional) | Token válido, account existente | 1. `POST /connections` con body: `{name, service_id, connection: {...}}` (sin `metadata`) 2. Verificar | 201 Created — Connection creada con `metadata` null. Sin error | 🟠 | ✅ | ⬜ Pendiente |
| TC-011 | Integrations | AC-2 | Edge Case | Instalar grapp con payload mínimo (solo service_id y name) | Token válido | 1. `POST /integrations` con body mínimo: `{service_id, name}` 2. Verificar response | 201 Created — Integración creada, configuración queda `{}` (vacía). Retorna integration_id + gateway_key | 🟠 | ✅ | ⬜ Pendiente |
| TC-012 | Connections | AC-1 | Edge Case | Listar connections de account sin connections | Account existente sin connections | 1. `GET /connections` para account vacío 2. Verificar response | 200 OK — Lista vacía `[]` o `{data: []}`, sin error. Paginación con total=0 | 🟠 | ✅ | ⬜ Pendiente |
| TC-013 | Connections | AC-1 | Edge Case | Actualizar connection con solo campo `name` | Connection existente | 1. `PUT /connections/{id}` con body: `{name: "only_name"}` 2. Verificar en BD | 200 OK — Solo name cambiado. `service_id`, `data`, `connection`, `metadata` preservados sin alteración | 🟠 | ✅ | ⬜ Pendiente |
| TC-014 | Connections | AC-5 | Edge Case | Crear connection con JSON grande en `data` y `metadata` | Token válido | 1. `POST /connections` con `data` de ~50KB y `metadata` complejo (anidado) 2. Verificar creación y lectura | 201 Created — Datos preservados con fidelidad JSON (tipos, anidamiento). ConnectionM2MResource mantiene fidelidad de tipos | 🟡 | ✅ | ⬜ Pendiente |
| TC-015 | Connections | AC-5 | Edge Case | Verificar que `data` y `connection` preservan tipos JSON (no castean a string) | Token válido | 1. Crear connection con `data: {count: 42, active: true, items: [1,2]}` 2. GET connection 3. Verificar que `count` es number, `active` es boolean, `items` es array | 200 OK — Tipos JSON preservados exactamente (numbers, booleans, arrays). No hay casteo a string | 🟠 | ✅ | ⬜ Pendiente |

### Negative Cases

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-016 | Connections | AC-1 | Negativo | Crear connection sin `service_id` (required) | Token válido | 1. `POST /connections` con body sin `service_id` | 422 Unprocessable Entity — Error de validación indicando `service_id` requerido | 🔴 | ✅ | ⬜ Pendiente |
| TC-017 | Connections | AC-1 | Negativo | Crear connection sin `name` (required) | Token válido | 1. `POST /connections` con body sin `name` | 422 Unprocessable Entity — Error de validación indicando `name` requerido | 🔴 | ✅ | ⬜ Pendiente |
| TC-018 | Connections | AC-4 | Negativo | Acceder a connections con scope incorrecto/insuficiente | Token con solo `app:connection-read` | 1. Intentar `POST /connections` (requiere `app:connection-create`) con token de solo lectura | 403 Forbidden — Scope insuficiente. No se crea ningún registro | 🔴 | ✅ | ⬜ Pendiente |
| TC-019 | Connections | AC-6 | Negativo | Acceder a connections de account inexistente | Token válido, remote_id que no existe | 1. `GET /api/2.0/app/accounts/INVALID_REMOTE_ID/connections` | 404 Not Found — Account no encontrado. Sin stack trace | 🟠 | ✅ | ⬜ Pendiente |
| TC-020 | Connections | AC-1 | Negativo | Operar sobre connection inexistente | Token válido, connectionId que no existe | 1. `GET /connections/99999999` 2. `PUT /connections/99999999` 3. `DELETE /connections/99999999` | 404 Not Found para cada operación. Sin stack trace ni crash | 🟠 | ✅ | ⬜ Pendiente |
| TC-021 | Integrations | AC-2 | Negativo | Instalar integración sin `service_id` | Token válido | 1. `POST /integrations` con body: `{name: "test"}` (sin service_id) | 422 Unprocessable Entity — Validación falla | 🔴 | ✅ | ⬜ Pendiente |
| TC-022 | Connections | AC-3 | Negativo | Mass assignment — enviar campos protegidos | Token válido | 1. `POST /connections` con body incluyendo: `{id: 1, account_id: 999, created_at: "..."}` además de campos válidos 2. Verificar en BD | Campos protegidos IGNORADOS. Connection creada con ID auto-generado, account del binding de ruta. Campos inyectados no persistidos | 🔴 | ✅ | ⬜ Pendiente |
| TC-023 | Connections | AC-4 | Negativo | Acceso sin token de autenticación | Sin auth header | 1. `GET /connections` sin header Authorization | 401 Unauthorized — Sin acceso | 🔴 | ✅ | ⬜ Pendiente |
| TC-024 | Integrations | AC-6 | Negativo | Instalar integración — verificar que app viene del token, no del body | Token M2M de App A | 1. `POST /integrations` con body: `{service_id, name, app_id: "APP_B_ID"}` 2. Verificar en BD qué app quedó asociada | Integration creada con app del TOKEN (App A), NO con app_id del body. Campo `app_id` del body IGNORADO | 🔴 | ✅ | ⬜ Pendiente |

---

## Casos de Regresión

| ID | Módulo impactado | Caso de regresión | Por qué podría romperse | Prioridad | Estado |
|----|-----------------|-------------------|------------------------|-----------|--------|
| REG-001 | Connections (Tenant) | CRUD de connections vía tenant routes sigue funcionando | Se agregaron 5 nuevos métodos al ConnectionController — podrían afectar los existentes | 🔴 | ⬜ Pendiente |
| REG-002 | Integrations (Webcomponent) | Endpoints de webcomponent integrations siguen funcionando (install/uninstall) | Se agregó lógica de install nueva usando `createIntegration` — podría afectar el trait compartido | 🔴 | ⬜ Pendiente |
| REG-003 | Integrations (App API) | Endpoints existentes de app integrations (GET, action, update, delete) | Se agregó nuevo endpoint POST en el mismo grupo de rutas | 🟠 | ⬜ Pendiente |
| REG-004 | Auth (OAuth) | Generación de tokens con scopes existentes no se rompió | 4 nuevos scopes registrados en AuthServiceProvider — podría afectar el registry | 🟠 | ⬜ Pendiente |
| REG-005 | Connections (Runtime Go) | Go runtime puede leer connections creadas vía los nuevos endpoints | Columna `connection` se setea explícitamente (no fillable) — si falla, Go no autentica el grapp | 🔴 | ⬜ Pendiente |
| REG-006 | Integrations (Legacy) | Endpoints legacy de integraciones (routes/api.php v1.0) siguen funcionando | Se relajó `user_id` required en `Integration::rules()` — podría afectar validaciones existentes | 🟠 | ⬜ Pendiente |

---

## Queries de Verificación BD

```sql
-- ================================================================
-- BD: PostgreSQL (gateway) — Ejecutar en DBeaver via SSH tunnel
-- ================================================================

-- TC-003: Verificar connection creada con campos encriptados
-- Reemplazar {connectionId} con el ID devuelto por el POST
SELECT id, name, service_id, 
       connection IS NOT NULL AS has_connection_encrypted,
       data IS NOT NULL AS has_data_mirror,
       metadata,
       account_id,
       created_at
FROM connections 
WHERE id = {connectionId};
-- Esperado: has_connection_encrypted = true, has_data_mirror = true

-- TC-003/TC-004: Verificar que connection y data están encriptados (no plaintext)
SELECT id, 
       LEFT(connection::text, 50) AS connection_preview,
       LEFT(data::text, 50) AS data_preview
FROM connections 
WHERE id = {connectionId};
-- Esperado: Valores NO legibles (encriptados por trait Encryptable)

-- TC-005: Verificar que update sin `connection` preserva el secreto
SELECT id, name, connection, data 
FROM connections 
WHERE id = {connectionId};
-- Esperado: name = "solo nombre", connection = [valor original sin cambios]

-- TC-006: Verificar que connection fue eliminada
SELECT COUNT(*) FROM connections WHERE id = {connectionId};
-- Esperado: 0

-- TC-007: Verificar integración instalada
SELECT id, name, service_id, account_id, app_id, 
       gateway_key, configuration, user_id,
       created_at
FROM integrations 
WHERE id = {integrationId};
-- Esperado: account_id = account del remote_id, 
--           app_id = app del token M2M,
--           configuration = '{}' (vacío),
--           user_id = NULL (install account-scoped, sin user)

-- TC-022: Verificar que mass assignment no funcionó
SELECT id, account_id FROM connections 
WHERE id = {connectionId};
-- Esperado: id = auto-generado (NO el inyectado), 
--           account_id = del binding de ruta (NO el inyectado)

-- TC-024: Verificar que app viene del token, no del body
SELECT id, app_id FROM integrations 
WHERE id = {integrationId};
-- Esperado: app_id = ID de la app del token M2M (NO el enviado en body)

-- REG-006: Verificar que integraciones existentes con user_id siguen intactas
SELECT id, user_id, account_id FROM integrations 
WHERE user_id IS NOT NULL 
LIMIT 5;
-- Esperado: Registros existentes con user_id preservados
```

---

## Notas

- **Auth M2M**: Los endpoints usan `client_credentials` grant type. Se necesita un OAuth client con los scopes correctos para testear
- **Base URL staging**: `https://dev-app.ionflow.io`
- **Documentación**: Verificar disponibilidad en `{base_url}/documentation`
- **Runtime Go**: El riesgo más crítico es que la columna `connection` esté correctamente poblada. Si solo se escribe `data` (como hacían los endpoints antiguos), el motor Go no podrá autenticar el grapp
- **Scope del ticket**: Solo persistir registros — NO hay setup funcional de flows, NO hay OAuth redirect dance, NO hay link integration↔connection
- **Test unitarios del dev**: 176 tests passed (782 assertions) — cubren flujos funcionales, validación, seguridad y mass-assignment
