# Ticket Memory — IONF-996

## Datos del Ticket

| Campo | Valor |
|-------|-------|
| ID ClickUp | `86e17d4f4` |
| ID Interno | IONF-996 |
| URL | https://app.clickup.com/t/86e17d4f4 |
| Título | Endpoints de Instalación de Grapps (API-First) |
| Status | `qa in process` |
| Tipo | New Feature |
| Prioridad | High |
| Sprint | Sprint 1 (5/25 - 6/7) |
| Space | NEW GATEWAY IOND |
| Proyecto | IONFLOW |
| QA Points | 3 |
| Creador | Marcel Herrera Rendón |
| Asignado (Dev) | Gustavo Mamani |
| Watchers | Rodolfo Merlo Ali, Steve Nina, Gustavo Mamani, Marcel Herrera Rendón, Enrique Vicente |

---

## Merge Requests

| Repo | MR | Branch |
|------|----|--------|
| `gateway` (Laravel) | [MR #564](https://gitlab.com/altacrest/integrations/gateway/-/merge_requests/564) (original) | `IONF-996` |
| `gateway` (Laravel) | [MR #566](https://gitlab.com/altacrest/integrations/gateway/-/merge_requests/566) (correcciones) | `IONF-996` |
| `flow_binaries` | N/A | — |
| `gateway-ion` | N/A | — |
| `webcomponents-flow` | N/A | — |

---

## Resumen Funcional

Extender la API de Ionflow para permitir que aplicaciones externas (Omnio) realicen la instalación y activación de Grapps mediante endpoints API, sin depender de UI. Ion actúa como motor que recibe la orden de instalación y crea los registros necesarios. Scope: solo persistir registros, sin setup funcional de flows.

**Cambios implementados:**
1. **Connections CRUD (app-scope M2M)** — 5 endpoints bajo `/api/2.0/app/accounts/{account:remote_id}/connections`
2. **Install Integration endpoint** — `POST /api/2.0/app/accounts/{account:remote_id}/integrations`
3. **ConnectionM2MResource** — Resource que NUNCA expone el campo `connection` (secreto)
4. **4 nuevos OAuth scopes** — `app:connection-read`, `app:connection-create`, `app:connection-update`, `app:connection-delete`
5. **Scope existente** — `app:integration-create` (para install)
6. **16 archivos de documentación Markdown** — en `resources/js/Markdown/`

---

## Acceptance Criteria

> Los AC del ticket están incompletos (Gherkin con When/Then vacíos). Se derivan AC funcionales del análisis técnico y el formulario de cambios del Developer.

- [ ] **AC-1**: Las aplicaciones externas (M2M) pueden crear, leer, actualizar y eliminar connections de un account vía API app-scope
- [ ] **AC-2**: Las aplicaciones externas pueden instalar una integración (grapp) para un account vía API app-scope, obteniendo `integration_id` y `gateway_key`
- [ ] **AC-3**: El campo `connection` (secreto/credenciales) NUNCA se expone en las respuestas JSON (ConnectionM2MResource)
- [ ] **AC-4**: Los 4 nuevos scopes de autorización (`app:connection-read/create/update/delete`) controlan correctamente el acceso a cada operación
- [ ] **AC-5**: La columna `connection` se encripta correctamente y se espeja en `data` para que el runtime Go pueda leerla
- [ ] **AC-6**: El account se resuelve del binding de ruta (`remote_id`), el app se resuelve del token M2M (NO del body)

---

## Análisis Técnico (del ticket)

### Endpoints Nuevos

| # | Método | Endpoint | Scope | Descripción |
|---|--------|----------|-------|-------------|
| 1 | GET | `/api/2.0/app/accounts/{account:remote_id}/connections` | `app:connection-read` | Listado paginado (per_page, order_by, order_direction) |
| 2 | GET | `/api/2.0/app/accounts/{account:remote_id}/connections/{connectionId}` | `app:connection-read` | Detalle de connection |
| 3 | POST | `/api/2.0/app/accounts/{account:remote_id}/connections` | `app:connection-create` | Crear connection (name, service_id, data, connection, metadata) |
| 4 | PUT | `/api/2.0/app/accounts/{account:remote_id}/connections/{connectionId}` | `app:connection-update` | Actualización parcial; si se omite `connection`, secreto preservado |
| 5 | DELETE | `/api/2.0/app/accounts/{account:remote_id}/connections/{connectionId}` | `app:connection-delete` | Eliminar connection |
| 6 | POST | `/api/2.0/app/accounts/{account:remote_id}/integrations` | `app:integration-create` | Instalar grapp (service_id, name). Retorna integration_id + gateway_key |

### Decisiones Clave

| # | Decisión |
|---|----------|
| D1 | Scope = solo persistir registro. Setup funcional (flujo) fuera de scope |
| D2 | Auth = grupo app-scope (client_credentials / auth.app), M2M. No intent, no UI |
| D3 | Grapps simples, record-only |
| D4 | Integration → Account (customer vía remote_id). Devuelve integration_id |
| D5 | Endpoint install nuevo y limpio, account del binding de ruta (no body) |
| D6 | Reusar createIntegration como núcleo persist (evita rules().user_id, no duplica) |
| D7 | Descartado store(): arrastra lógica cart, no apto para install simple |
| D8 | Connection: poblar columna `connection` + espejo `data`, encriptado. Sin esto el grapp no autentica |

### Riesgos Identificados

| Riesgo | Impacto |
|--------|---------|
| `rules().user_id` required → bloquea install account-scoped | Relajar a nullable |
| Columna `connection` no `fillable` → setear explícito | Runtime Go la lee a ella, no a `data` |
| DB compartida (Postgres gateway): lo creado en Laravel lo ve Go sin sync | No duplicar lógica |
| `setOmnioConfiguration()` (Integration model, comentado, TODO) | Intento previo abandonado — confirmar descartado |

---

## Historial de Status

| Fecha | Status |
|-------|--------|
| 2026-05-04 | ideas |
| 2026-05-25 | for analysis |
| 2026-05-29 | sprint intake |
| 2026-05-29 | fortification |
| 2026-05-29 | code review |
| 2026-06-01 | qa testing |
| 2026-06-02 | deployed |
| 2026-06-02 | qa in process |
| 2026-06-03 | correcciones del dev (MR #566) |
| 2026-06-04 | re-deployed |

## Correcciones del Dev (MR #566 — 2026-06-03)

> **Cambios significativos al contrato del API.**

1. **`app_name` ahora es REQUERIDO** — Para crear y actualizar connections, se debe enviar `app_name` que se usa para resolver el `service` asociado (reemplaza envío directo de `service_id` en connections)
2. **Listado filtra por app** — `GET /connections` ahora solo retorna connections cuyo service está asociado a la app del token M2M
3. **CRUD valida asociación app↔service** — Create, update y delete verifican que el service esté asociado a la app del token (antes solo verificaban que `service_id` existiera)

**Impacto en testing**: 5 nuevos test cases (TC-025 a TC-029) para validar `app_name` requerido, app_name inválido, app_name de otra app, update sin app_name, y aislamiento en delete.

## Code Review

- **Enrique Vicente** (2026-05-29): ✅ Code review approved
- **Rodolfo Merlo Ali** (2026-05-29): Observaciones
- **Gustavo Mamani** (2026-05-29): Corrigió observaciones
- **Rodolfo Merlo Ali** (2026-06-01): ✅ Code review approved
- **Rodolfo Merlo Ali** (2026-06-02): `deployed`

---

## Módulos Afectados

| Módulo L2 | Impacto |
|-----------|---------|
| **Connections** | Nuevos endpoints app-scope para CRUD de connections |
| **Integrations** | Nuevo endpoint app-scope para install de grapps |
| **Accounts** | Account-bound routes (remote_id en URL) |
| **Developer Apps** | OAuth clients/scopes para M2M auth |

---

## Artefactos de la Sesión

| Artefacto | Estado | Archivo |
|-----------|--------|---------|
| Test Matrix | ✅ Completa (30 casos) | `test-matrix.md` |
| Test Matrix CSV | ✅ Completa | `test-matrix.csv` |
| Test Plan | ✅ Completo (~90 min) | `test-plan.md` |
| Postman Collection | ✅ Completa (30 requests) | `IONF-996.postman_collection.json` |
| QA Report | ✅ Completo (APPROVED) | `qa-report.md` |
| Test Results CSV | ✅ Completo | `IONF-996 - Review IONF-996.csv` |

---

## Bugs Encontrados

| Bug ID | Severidad | Descripción | TC relacionado | Evidencia |
|--------|-----------|-------------|---------------|-----------|
| | | | | |

---

## Veredicto

| Campo | Valor |
|-------|-------|
| Veredicto | ⏳ Pendiente |
| Aprobado por | |
| Fecha | |
| Observaciones | |

---

## Transcript

| Timestamp | Stage | Acción | Detalle |
|-----------|-------|--------|---------|
| 2026-06-02T12:48 | Session Start | Contexto cargado | L1 + L2 connections, integrations, accounts, developer-apps |
| 2026-06-02T12:50 | Planning | Ticket memory creado | IONF-996.md |
| 2026-06-02T12:50 | Execution | Generando test-matrix | test-docs/document (modo matrix) |
| 2026-06-02T12:52 | Reporting | Test matrix completada | 30 casos, 6 AC derivados |
| 2026-06-02T12:56 | Execution | Generando test plan | sprint-testing/plan |
| 2026-06-02T12:57 | Reporting | Test plan completado | 6 bloques, ~90 min estimado |
| 2026-06-02T12:59 | Execution | Generando Postman collection | sprint-testing/test (preparación) |
| 2026-06-02T13:02 | Reporting | Postman collection lista | 30 requests con auto-tests |
| 2026-06-04T12:19 | Update | Dev mandó correcciones | MR #566: app_name requerido, filtrado por app |
| 2026-06-04T12:22 | Execution | Postman collection v2 | Actualizada con 5 nuevos TCs (TC-025 a TC-029), variable app_name |
| 2026-06-04T12:46 | Reporting | QA Report generado | 30/30 PASS. Sugerencia: ✅ APPROVED |
