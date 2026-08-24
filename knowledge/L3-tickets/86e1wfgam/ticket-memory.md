# Ticket Memory — 86e1wfgam

> Motor de exposición por API (FASE 1) — DevApp API

## Información del Ticket

| Campo | Valor |
|-------|-------|
| Ticket ID | 86e1wfgam |
| Título | Motor de exposición por API (FASE 1) |
| ClickUp URL | https://app.clickup.com/t/86e1wfgam |
| Módulo principal | `developer-apps` |
| Módulos impactados | `accounts`, `connections`, `pdf-templates`, `boards` |
| Developer | Rodolfo Merlo Ali (principal), Alex Chura, Gustavo Mamani |
| QA Engineer | Steve Nina |
| Track | Discovery |
| Fecha de inicio | 2026-08-09 |
| Prioridad | 🔴 Urgent |
| Tags | iond-mvp |

### Child Tasks

| Child Task ID | Nombre | Status | Assignee |
|--------------|--------|--------|----------|
| 86e1wfgt2 | App Channels | quick prototype | Alex Chura, Gustavo Mamani |
| 86e1wfguh | PDF Template | quick prototype | Alex Chura |
| 86e1wfgxk | PDF Mapper | assignment | Rodolfo Merlo Ali |

---

## Acceptance Criteria

> Fuente: ClickUp ticket description + comentarios reconciliados.

### AC del ticket padre (descripción)

- [ ] AC-1: App externa con credenciales válidas puede POST a connectors/channels → 200/201 + ID de referencia
- [ ] AC-2: App autorizada puede crear/consultar/actualizar mappers, boards o PDFs → respuesta según esquema documentado
- [ ] AC-3: Petición sin credenciales o sin scope → 401/403 sin exposición de datos internos

### AC ampliados desde comentarios del Developer (Rodolfo, 2026-08-05)

- [ ] AC-4: Motor de tokens OAuth2 `client_credentials` → emite JWT RS256 compatible con Passport
- [ ] AC-5: Accounts compartidos por compañía (`accounts.company_id`) → apps de la misma compañía ven los mismos customers
- [ ] AC-6: Connectors autodescriptivos → catálogo → detalle con actions → spec → ejecución síncrona con respuesta raw
- [ ] AC-7: Selección de conexión automática (`Connection-Id` opcional) → 1 conexión = implícita, 0 = sin credenciales, >1 = 409
- [ ] AC-8: Direccionamiento namespaced (`app.shipedge` canónico, `shipedge` alias, `tenant.*` reservado)
- [ ] AC-9: Flows y mappers por app/cuenta con ejecución síncrona
- [ ] AC-10: PDF Templates → spec + render → URL pública en R2 (binario nunca en respuesta)
- [ ] AC-11: UI diseñador PDF (webcomponents `gt-pdf-list`/`gt-pdf-workspace`)
- [ ] AC-12: Migración BD: `accounts.remote_id` de unique global a unique por-compañía (índices parciales)
- [ ] AC-13: Token desconocido/revocado/expirado → mismo `401 "Invalid token"` (uniformidad deliberada)

---

## Decisiones del Equipo

> Acuerdos tomados con Developer/PO durante Discovery.

| Fecha | Decisión | Tomada por |
|-------|----------|-----------|
| 2026-08-05 | Respuestas raw (payload del proveedor sin envelope `{data}`) | Rodolfo (Dev) |
| 2026-08-05 | Tokens compatibles con Passport (misma tabla `oauth_access_tokens`) | Rodolfo (Dev) |
| 2026-08-05 | Accounts compartidos por compañía (no por app) | Rodolfo (Dev) |
| 2026-08-05 | `Connection-Id` como header (no body) | Rodolfo (Dev) |
| 2026-08-05 | Endpoint Laravel POST `/api/2.0/app/accounts` valida remote_id como global (limitación conocida, no bug) | Rodolfo (Dev) |
| 2026-08-05 | Flow INACTIVE no ejecuta (409) pero sí se puede leer | Rodolfo (Dev) |
| 2026-08-05 | Token revocado/expirado devuelve mismo 401 (antes distinguía mensajes) — deliberado | Rodolfo (Dev) |

---

## Artefactos de la Sesión

| Artefacto | Estado | Archivo |
|-----------|--------|---------|
| Risk Triage | ✅ Completado | `risk-triage.md` |
| AC Consolidados | ✅ Completado | `ac-consolidated.md` |
| Test Matrix | ✅ Completado | `test-matrix.md` + `test-matrix.csv` |
| Test Plan | ✅ Completado | `test-plan.md` |
| Code Review QA | ⬜ Pendiente | `code-review-qa.md` |
| QA Report | ⬜ Pendiente | `qa-report.md` |

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

> Log cronológico de la sesión.

| Timestamp | Stage | Acción | Detalle |
|-----------|-------|--------|---------|
| 2026-08-09 23:06 | Session Start | Contexto cargado | L1 (4 archivos) + L2 developer-apps + L2 accounts + L2 connections + L2 pdf-templates |
| 2026-08-09 23:07 | Session Start | ClickUp leído | Ticket padre + 3 child tasks + 4 comentarios |
| 2026-08-09 23:09 | Planning | Risk Triage | Aprobado por QA Engineer, ejecutando test-docs/prioritize |
