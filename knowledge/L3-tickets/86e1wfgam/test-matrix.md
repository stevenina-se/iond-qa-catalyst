# Test Matrix — 86e1wfgam (Motor de exposición por API — FASE 1)

## Resumen

- **Total de casos**: 45
- **Happy path**: 14
- **Edge cases**: 15
- **Negativos**: 11
- **Regresión**: 5
- **Automatizables**: 38 (API tests vía colecciones `.http` o Playwright API)
- **Herramientas**: Colecciones `.http` (REST Client VS Code) en `gateway/`, DBeaver (BD)

---

## Prerequisitos de Setup

> Antes de ejecutar cualquier TC, completar estos pasos de deploy:

| # | Acción | Comando/Detalle |
|---|--------|-----------------|
| S-1 | Migración Gateway | `php artisan migrate` |
| S-2 | Variables de entorno Binaries | `PDF_GENERATE_URL`, `R2_*`, `DEVAPP_TOKEN_RATE`, `oauth-private.key` en `./storage` |
| S-3 | Servicio template-maker corriendo | `PORT=3005 bun run index.ts` (repo template-maker) |
| S-4 | Seeder de demo PDF | `php artisan db:seed --class=DevAppPdfTemplateSeeder` |
| S-5 | Identificar credenciales de apps | Query: `SELECT a.company_id, a.id AS app_id, a.name, c.id AS client_id, c.secret FROM apps a JOIN oauth_clients c ON c.id = a.oauth_client_id WHERE c.provider = 'apps' AND c.revoked = false ORDER BY a.company_id, a.id;` |
| S-6 | Elegir 2 apps de la MISMA compañía + 1 de otra | Para pruebas de aislamiento (Superficie 5) |

---

## SUPERFICIE 1: Motor de Tokens y Fronteras de Auth

> Colección: `gateway/devapp-token.http`

| ID | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-001 | AC-1 | Happy Path | Emitir token OAuth2 válido | App con client_id + secret válidos | `POST /api/2.0/app/token` > Body: `{grant_type: "client_credentials", client_id, client_secret, scope: "..."}` > Verify: 200 + JWT | 200 con JWT RS256, campo `access_token` presente, scopes en el payload | 🔴 | ✅ | ⬜ |
| TC-002 | AC-2 | Negativo | Grant type no soportado | App válida | `POST /api/2.0/app/token` > Body: `{grant_type: "authorization_code", ...}` > Verify: 400 | 400 sin datos internos expuestos | 🔴 | ✅ | ⬜ |
| TC-003 | AC-2 | Negativo | Sin scope en request de token | App válida | `POST /api/2.0/app/token` > Body: sin campo `scope` > Verify: 400 | 400 | 🔴 | ✅ | ⬜ |
| TC-004 | AC-2 | Negativo | Scope desconocido | App válida | `POST /api/2.0/app/token` > Body: `{scope: "scope_inexistente"}` > Verify: 422 | 422 | 🟠 | ✅ | ⬜ |
| TC-005 | AC-2 | Negativo | Secret incorrecto | Client_id válido, secret malo | `POST /api/2.0/app/token` > Body: `{client_secret: "wrong"}` > Verify: 401 | 401 sin leak de datos | 🔴 | ✅ | ⬜ |
| TC-006 | AC-2 | Negativo | Client ID de otro guard (no "apps") | OAuth client con provider != "apps" | `POST /api/2.0/app/token` > Body: `{client_id: <no-apps>}` > Verify: 401 | 401 | 🟠 | ✅ | ⬜ |
| TC-007 | AC-2 | Negativo | Body malformado | — | `POST /api/2.0/app/token` > Body: texto plano o JSON inválido > Verify: 400 | 400 | 🟡 | ✅ | ⬜ |
| TC-008 | AC-3 | Happy Path | Registrar customer (account) | Token válido con scope account | `POST /api/2.0/app/token` > Obtener token > `POST /accounts` > Body: `{remote_id: "QA-CUST-001", name: "Test"}` > Verify: 201 | 201 con datos del customer creado | 🔴 | ✅ | ⬜ |
| TC-009 | AC-3 | Edge Case | Repetir mismo remote_id | Customer ya creado con remote_id | `POST /accounts` > Body: `{remote_id: "QA-CUST-001"}` (repetido) > Verify: 409 | 409 (conflicto, unique por compañía) | 🔴 | ✅ | ⬜ |
| TC-010 | AC-3 | Happy Path | Listar y detallar accounts | Customer creado | `GET /accounts` > Verify: lista con customer > `GET /accounts/QA-CUST-001` > Verify: detalle | Lista incluye customer, detalle coincide con lo creado | 🟠 | ✅ | ⬜ |
| TC-011 | AC-4 | Negativo | Ruta account-scoped sin Account-Id | Token válido | Request a ruta account-scoped > Sin header `Account-Id` > Verify: 400 | 400 indicando que Account-Id es requerido | 🔴 | ✅ | ⬜ |
| TC-012 | AC-4 | Edge Case | Account-Id de cuenta ajena | Token de compañía A, Account-Id de compañía B | Request con `Account-Id` de otra compañía > Verify: 404 | 404 (mismo formato que inexistente, no leak) | 🔴 | ✅ | ⬜ |
| TC-013 | AC-5 | Edge Case | Token con scope parcial en endpoint que requiere otro | Token con solo scope `read` | Request a endpoint que requiere scope `execute` > Verify: 403 | 403 con nombre del scope faltante | 🟠 | ✅ | ⬜ |
| TC-014 | AC-6 | Edge Case | Token revocado | Token previamente emitido, luego revocado en BD | Request con token revocado > Verify: 401 "Invalid token" | 401 "Invalid token" (sin distinguir causa) | 🟠 | ✅ | ⬜ |
| TC-015 | AC-6 | Edge Case | Token expirado | Token con expires_at en el pasado | Request con token expirado > Verify: 401 "Invalid token" | 401 "Invalid token" (uniforme, deliberado) | 🟠 | ✅ | ⬜ |

---

## SUPERFICIE 2: Connectors Autodescriptivos

> Colección: `gateway/devapp-connectors.http`

| ID | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-016 | AC-7 | Happy Path | Catálogo de connectors namespaced | Token válido | `GET /connectors` > Verify: lista con nombres namespaced `app.<tipo>` | Connectors listados con names namespaced | 🔴 | ✅ | ⬜ |
| TC-017 | AC-7 | Edge Case | Alias resuelve igual que canónico | Token válido, connector shipedge | `GET /connectors/shipedge` > Verify: mismo resultado que `GET /connectors/app.shipedge` | Ambas rutas resuelven al mismo connector | 🟠 | ✅ | ⬜ |
| TC-018 | AC-7 | Negativo | Namespace tenant reservado | Token válido | `GET /connectors/tenant.shipedge` > Verify: 404 | 404 (reservado para fase futura) | 🟡 | ✅ | ⬜ |
| TC-019 | AC-8 | Happy Path | Detalle de connector CON Account-Id | Token válido, Account-Id válido | `GET /connectors/{id}` con header `Account-Id` > Verify: actions + conexiones del customer | Detalle con actions habilitadas + conexiones | 🔴 | ✅ | ⬜ |
| TC-020 | AC-8 | Edge Case | Detalle de connector SIN Account-Id | Token válido, sin header Account-Id | `GET /connectors/{id}` sin Account-Id > Verify: solo specs | Detalle con solo specs, sin conexiones | 🟠 | ✅ | ⬜ |
| TC-021 | AC-9 | Happy Path | Ejecución con Connection-Id explícito | Token + Account-Id + Connection-Id | `POST /connectors/{id}/actions/{name}/execute` > Header: Connection-Id > Verify: 200 + respuesta raw | Respuesta raw del proveedor (sin envelope {data}) | 🔴 | ✅ | ⬜ |
| TC-022 | AC-9 | Edge Case | Ejecución con 1 conexión (implícita) | Customer con 1 sola conexión | `POST execute` sin Connection-Id > Verify: ejecución implícita OK | Ejecución usa conexión implícita | 🟠 | ✅ | ⬜ |
| TC-023 | AC-9 | Edge Case | Ejecución con >1 conexiones sin Connection-Id | Customer con múltiples conexiones | `POST execute` sin Connection-Id > Verify: 409 | 409 con lista de conexiones candidatas | 🟠 | ✅ | ⬜ |
| TC-024 | AC-10 | Negativo | Connector no vinculado a la app | Token válido, connector no setup | `GET /connectors/{id-no-vinculado}` > Verify: 404 | 404 | 🟠 | ✅ | ⬜ |
| TC-025 | AC-10 | Negativo | Action no habilitada | Connector vinculado, action deshabilitada | `POST execute` action no habilitada > Verify: 400 | 400 | 🟠 | ✅ | ⬜ |
| TC-026 | AC-10 | Negativo | Token read-only intentando ejecutar | Token con solo scope read | `POST execute` > Verify: 403 | 403 | 🟠 | ✅ | ⬜ |

---

## SUPERFICIE 3: PDF Templates via API

> Colección: `gateway/devapp-pdf.http`

| ID | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-027 | AC-11 | Happy Path | Spec de template PDF | Template de demo (seeder), token + scope PDF | `GET /pdf-templates/{id}/spec` > Verify: shape autodescriptivo, params es array | 200 con spec (mismo shape que action) | 🟠 | ✅ | ⬜ |
| TC-028 | AC-11 | Happy Path | Render simple de PDF | Template de demo, Account-Id válido | `POST /pdf-templates/execute` > Body con campos demo (customer_name, order_number, total) > Verify: 200 con {filename, public_url} | 200, descargar public_url = PDF válido | 🔴 | ✅ | ⬜ |
| TC-029 | AC-11 | Edge Case | Render batch (2 páginas) | Template de demo | `POST /pdf-templates/execute` > Body con 2 elementos en params array > Verify: PDF con 2 páginas | 200 con PDF multi-página válido | 🟠 | ✅ | ⬜ |
| TC-030 | AC-12 | Negativo | PDF sin scope | Token sin scope PDF | `GET /pdf-templates/{id}/spec` > Verify: 403 | 403 | 🟠 | ✅ | ⬜ |
| TC-031 | AC-12 | Negativo | PDF sin Account-Id | Token válido, sin header Account-Id | `POST /pdf-templates/execute` > Sin Account-Id > Verify: 400 | 400 | 🟠 | ✅ | ⬜ |
| TC-032 | AC-12 | Negativo | Plantilla de otra compañía | Token de compañía A, template de compañía B | `GET /pdf-templates/{id-otra-company}/spec` > Verify: 404 | 404 | 🟠 | ✅ | ⬜ |

---

## SUPERFICIE 4: UI del Diseñador PDF

| ID | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-033 | AC-13 | Happy Path | Crear y diseñar PDF template | Usuario con permisos, cuenta con Account | `Company Login > Sidebar: Marketplace > Tab: PDF List > Button: "+ New" > Dialog: Fill "Template name": "QA Test" > Button: "Create" > Workspace: diseñar template (agregar Text field) > Button: "Save" > Verify: listado refresca con "QA Test"` | Template creado, visible en lista, workspace funcional | 🟡 | ❌ | ⬜ |
| TC-034 | AC-13 | Edge Case | Estado de error con motor caído | Template-maker no corriendo | `Company Login > Sidebar: Marketplace > Tab: PDF List > Button: "+ New" > Verify: mensaje de error visible (no fallo silencioso)` | Mensaje de error claro al usuario | 🟡 | ❌ | ⬜ |

---

## SUPERFICIE 5: Accounts Compartidos por Compañía

> La prueba central del modelo. Requiere 2 apps de la misma compañía + 1 de otra.

| ID | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-035 | AC-14 | Happy Path | App B ve customer de App A (misma compañía) | App A y App B = misma compañía | `Token App A > POST /accounts {remote_id: "SHARED-001"} > 201` > `Token App B > GET /accounts > Verify: SHARED-001 en lista` > `GET /accounts/SHARED-001 > Verify: detalle OK` | App B ve el customer creado por App A | 🔴 | ✅ | ⬜ |
| TC-036 | AC-15 | Edge Case | App B no puede crear mismo remote_id | Customer SHARED-001 ya existe para esa compañía | `Token App B > POST /accounts {remote_id: "SHARED-001"} > Verify: 409` | 409 (unique por compañía, no por app) | 🔴 | ✅ | ⬜ |
| TC-037 | AC-15 | Happy Path | App C (otra compañía) crea mismo remote_id | App C = compañía diferente | `Token App C > POST /accounts {remote_id: "SHARED-001"} > Verify: 201` | 201 (sin conflicto entre compañías) | 🔴 | ✅ | ⬜ |
| TC-038 | AC-15 | Edge Case | App C no ve customer de compañía A | App C = compañía diferente | `Token App C > GET /accounts/SHARED-001 > Verify: retorna SU customer, no el de compañía A` | Cada compañía ve solo sus customers | 🔴 | ✅ | ⬜ |
| TC-039 | AC-16 | Happy Path | Customer API visible en UI | Customer creado vía API | `Company Login > Sidebar: Accounts > Verify: "SHARED-001" en lista` | Cuenta aparece en vista de tenant Accounts | 🟠 | ❌ | ⬜ |
| TC-040 | AC-17 | Edge Case | App B ejecuta contra customer de A con connector | App B tiene connector vinculado + action habilitada | `Token App B > POST execute con Account-Id de SHARED-001 > Verify: ejecución OK` | Ejecución funciona (customers y conexiones compartidos) | 🔴 | ✅ | ⬜ |

---

## SUPERFICIE 6: Flows por API

| ID | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-041 | AC-18 | Happy Path | Listar flows sin Account-Id | Token válido, flows existentes | `GET /flows` sin Account-Id > Verify: agregado de toda la app, cada ítem con account_remote_id | Lista con todos los flows, campo account_remote_id presente | 🟠 | ✅ | ⬜ |
| TC-042 | AC-18 | Happy Path | Ejecutar flow activo | Flow con status ACTIVE | `POST /flows/{id}/execute` > Verify: ejecución síncrona OK | Resultado de ejecución retornado | 🟠 | ✅ | ⬜ |
| TC-043 | AC-18 | Negativo | Ejecutar flow inactivo | Flow con status INACTIVE | `POST /flows/{id}/execute` > Verify: 409 | 409 "flow is not active" (pero GET sí funciona) | 🟠 | ✅ | ⬜ |

---

## REGRESIÓN

| ID | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| REG-001 | AC-19 | Regresión | Flows del board ejecutan normal | Flow existente en board/canvas | `Company Login > Sidebar: Boards > Click [Flow existente] > Canvas: ejecutar flow > Verify: ejecución exitosa` | Runner compartido no afecta flows existentes | 🔴 | ❌ | ⬜ |
| REG-002 | AC-20 | Regresión | Conexiones del webcomponent | Connector con conexión existente | `Company Login > Sidebar: Connections > Click [Connector] > Tab: Connections > Verify: instalar/testear conexión normal` | Conexiones siguen funcionando | 🟠 | ❌ | ⬜ |
| REG-003 | AC-21 | Regresión | Rutas Laravel existentes | Endpoints `/api/2.0/app` previos | Request a endpoints Laravel existentes > Verify: mismas respuestas | Convivencia permanente, sin cambios | 🟠 | ✅ | ⬜ |
| REG-004 | AC-22 | Regresión | Migración BD correcta | Migración ejecutada | `DBeaver > Verify: índices parciales en accounts` (ver queries BD) | Índices parciales creados correctamente | 🔴 | ❌ | ⬜ |
| REG-005 | AC-22 | Regresión | Cuentas legacy preservadas | Cuentas sin company_id en BD | `DBeaver > SELECT * FROM accounts WHERE company_id IS NULL > Verify: datos intactos` | Cuentas legacy conservan garantía de unique | 🟠 | ❌ | ⬜ |

---

## Queries de Verificación BD

```sql
-- ═══════════════════════════════════════════════════════
-- SETUP: Identificar apps para testing
-- Fuente: gateway/database/migrations/2024_05_06_191644_create_apps_table.php
-- Tabla: apps | Columnas: id, name, company_id, oauth_client_id
-- Fuente: gateway/database/migrations/2016_06_01_000004_create_oauth_clients_table.php
-- Tabla: oauth_clients | Columnas: id, secret, provider, revoked
-- ═══════════════════════════════════════════════════════

-- S-5: Listar apps con sus credenciales OAuth (guard "apps")
SELECT a.company_id, a.id AS app_id, a.name, c.id AS client_id, c.secret
FROM apps a
JOIN oauth_clients c ON c.id = a.oauth_client_id
WHERE c.provider = 'apps' AND c.revoked = false
ORDER BY a.company_id, a.id;

-- ═══════════════════════════════════════════════════════
-- TC-001: Verificar token emitido en BD
-- Fuente: gateway/database/migrations/2016_06_01_000002_create_oauth_access_tokens_table.php
-- Tabla: oauth_access_tokens | Columnas: id, user_id, client_id, scopes, revoked, expires_at
-- ═══════════════════════════════════════════════════════

-- Verificar que el token se registró en oauth_access_tokens
SELECT id, client_id, scopes, revoked, expires_at, created_at
FROM oauth_access_tokens
WHERE client_id = '<client_id>'
ORDER BY created_at DESC
LIMIT 5;

-- ═══════════════════════════════════════════════════════
-- TC-008/TC-035: Verificar customer creado
-- Fuente: gateway/database/migrations/2024_05_06_191505_create_accounts_table.php
-- + gateway/database/migrations/2026_05_11_141610_add_company_columns.php
-- Tabla: accounts | Columnas: id, remote_id, name, email, company_id, created_at
-- ═══════════════════════════════════════════════════════

-- Verificar customer creado con company_id correcto
SELECT id, remote_id, name, email, company_id, created_at
FROM accounts
WHERE remote_id = 'QA-CUST-001';

-- TC-037: Verificar que 2 compañías pueden tener el mismo remote_id
SELECT id, remote_id, company_id
FROM accounts
WHERE remote_id = 'SHARED-001'
ORDER BY company_id;
-- Esperado: 2 filas, cada una con company_id diferente

-- ═══════════════════════════════════════════════════════
-- REG-004: Verificar migración de índices parciales
-- Fuente: comentario Dev — migración 2026_08_07_000001_scope_accounts_remote_id_to_company
-- ═══════════════════════════════════════════════════════

-- Verificar índices en tabla accounts
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'accounts'
AND (indexname LIKE '%remote_id%' OR indexname LIKE '%company%');
-- Esperado: 2 índices parciales:
--   1. UNIQUE (company_id, remote_id) WHERE company_id IS NOT NULL
--   2. UNIQUE (remote_id) WHERE company_id IS NULL

-- REG-005: Verificar que cuentas legacy sin company_id mantienen su constraint
SELECT COUNT(*) AS legacy_accounts
FROM accounts
WHERE company_id IS NULL;

-- ═══════════════════════════════════════════════════════
-- TC-028: Verificar PDF template de demo (seeder)
-- Fuente: gateway/database/migrations/2026_04_02_210000_create_pdf_templates_table.php
-- Tabla: pdf_templates | Columnas: id, account_id, user_id, name, description, schema, status
-- ═══════════════════════════════════════════════════════

SELECT id, account_id, name, status, created_at
FROM pdf_templates
WHERE name = 'Demo Order Receipt';
-- Esperado: 1 fila con status = 'active'
```

---

## Resumen de Prioridades

| Prioridad | Cantidad | TCs |
|-----------|----------|-----|
| 🔴 Crítico | 15 | TC-001,002,003,005,008,009,011,012,016,021,028,035,036,037,038,040, REG-001,004 |
| 🟠 Alto | 20 | TC-004,006,010,013,014,015,017,019,020,022,023,024,025,026,027,029,030,039,041,042,043, REG-002,003,005 |
| 🟡 Medio | 5 | TC-007,018,033,034,031,032 |
| 🟢 Bajo | 0 | — |
