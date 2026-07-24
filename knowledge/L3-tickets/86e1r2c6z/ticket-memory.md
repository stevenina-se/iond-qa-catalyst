# Ticket: 86e1r2c6z — Refactorizar flujo y formulario de registro de compañía

> Sesión de Discovery iniciada: 2026-06-23
> Sesión de Deployment iniciada: 2026-07-17
> Módulos: auth (formulario /create-company), gateway-ion (UI)
> QA Engineer: Steve Nina
> Track: Deployment
> Status en ClickUp: qa in process

## Contexto del Ticket

### Descripción
Refactorizar el formulario `/create-company` de Ionflow para que sea más completo, estético y comparable al formulario equivalente de Omnio. Incluye nuevos campos, autocompletado por servicio externo (Geoapify), timezone con autodetección de country, y mejoras visuales.

### Involucrados
- Creator: Marcel Herrera Rendón (PO)
- Assignee: Gustavo Mamani (Developer)
- Watchers: Rodolfo Merlo Ali, Alex Chura, Steve Nina, Gustavo Mamani, Marcel Herrera Rendón, Enrique Vicente
- Reviewers QA: Steve Nina
- Code Review: Rodolfo Merlo Ali ✅, Enrique Vicente ✅

### Tipo de ticket
- Type: Refactor
- Custom subcategory: Register Company
- Lista: Sprint 4 (7/6 - 7/19)
- Space: NEW GATEWAY IOND
- Tags: iond-dpl-4, iond-uxui

### Módulos afectados
- Módulo principal: `auth` (formulario de registro de compañía)
- Módulo secundario: `companies` (tabla `companies.timezone`) + `contacts` (morphOne para datos de contacto y dirección)

### PRs y Branches
| Repo | PR | Branch | Estado |
|------|----|--------|--------|
| gateway-ion | [PR #13](https://github.com/altacrest/ion_gateway_ion/pull/13) | IONF-1075 | Mergeado |
| flow_binaries | [PR #18](https://github.com/altacrest/ion_flow_binaries/pull/18) | IONF-1075 | Mergeado |

### Dependencias identificadas
- Servicio externo: **Geoapify Geocoding API** (requiere `GEOAPIFY_URL` + `GEOAPIFY_API_KEY` en `.env` de flow_binaries)
- Keycloak SSO: Email, `users.name` (nombre completo concatenado) vienen de Keycloak (read-only)
- Caché in-process con TTL: positiva 24h / negativa 1h (en flow_binaries Go)

---

## Respuestas del Developer a Preguntas Abiertas

> Fuente: TDD Build (Gustavo 29-jun) + Correcciones Code Review (Gustavo 13-jul)

| ID | Pregunta | Respuesta | Fuente |
|----|----------|-----------|--------|
| Q-001 | ¿Entidad de timezone? | `companies.timezone` (solo companies) | TDD Build 29-jun |
| Q-002 | ¿Servicio externo? | Geoapify Geocoding API | Quick Prototype 19-jun + Correcciones 13-jul |
| Q-003 | ¿Modo degradado? | Sí — endpoint 404 sin key; toast fallback en frontend | Correcciones 13-jul (H1) |
| Q-004 | ¿Postal Code obligatorio? | No — autofill con botón explícito, opcional | TDD Build 29-jun |
| Q-005 | ¿UTC → Country? | Guard manual-override protege; a verificar en testing | TDD Build 29-jun |
| Q-006 | ¿State dinámico? | Dropdown con subdivisions; texto libre sin subdivisions | TDD Build 29-jun (TC-020) |
| Q-007 | ¿Campos obligatorios? | Company Name, Timezone, Country — State y Postal opcionales | Correcciones 13-jul (M4) |
| Q-008 | ¿Contact Name? | Editable, prellenado desde `users.name` (Keycloak) | TDD Build 29-jun |
| Q-009 | ¿Servicio en staging? | Sí — requiere GEOAPIFY_API_KEY en .env de flow_binaries | Correcciones 13-jul (H3) |

---

## Hallazgos Clave del Code Review (Rodolfo + Enrique)

### Cambios arquitectónicos
- **Endpoint postal codes se movió de gateway (PHP) a flow_binaries (Go)** — H3
- Endpoint ahora bajo `/api/1.0` con `JWTAuthMiddleware` (Keycloak) — ya no es público — H1
- Caché negativa (misses) se cachean 1h (positiva 24h) — H1
- `states.json` es import dinámico (no en bundle inicial) — H2

### Correcciones del code review
- M1: `handleSubmit` con try/catch/finally — `isLoading` se resetea siempre
- M2: Si Keycloak no trae email → input editable con id `register-email`
- M3: `.env.gitlab` corregido — vars GEOAPIFY salieron de gateway
- M4: Timezone y Country ahora requeridos con `*` y validación
- L1-L6: Toast i18n, serverErrors limpiado, flag `isAutofilling`, logo comprimido, tests controller Go

---

## Transcript de la Sesión

| Timestamp | Acción | Detalle |
|-----------|--------|---------|
| 2026-06-23 15:22 | Session Start (Discovery) | Ticket leído desde ClickUp MCP — ticket 86e1r2c6z |
| 2026-06-23 15:22 | Discovery Paso 1 | L1 + L2/auth cargados |
| 2026-06-23 15:24 | Discovery Paso 2 | AC reconciliados — 6 divergencias identificadas, aprobadas por QA Engineer |
| 2026-06-23 15:24 | Discovery Paso 3 | Análisis de riesgo iniciado |
| 2026-07-17 14:14 | Session Start (Deployment) | Deployment iniciado — ticket en status "qa in process" |
| 2026-07-17 14:14 | Deployment Paso 1 | L1 + L2/auth + L3 cargados. Artefactos Discovery verificados (6/6 existen) |
| 2026-07-17 14:14 | Paso 1 — Reconciliación | 6 divergencias identificadas vs TDD Build. Todas las preguntas Q-001 a Q-009 resueltas |
| 2026-07-17 14:48 | Paso 1 — Actualización | Artefactos actualizados: ac-consolidated.md, test-matrix.md, test-matrix.csv, ticket-memory.md |
| 2026-07-17 14:55 | Deployment Paso 2 — Code Review QA | Repos actualizados: gateway-ion (43 archivos), flow_binaries (8 archivos) |
| 2026-07-17 14:56 | Paso 2 — Bug Hunting | Archivos clave revisados: CompanyForm.vue (657 líneas), company.ts (schema Zod), postal.service.ts, geoapify_controller.go, service.go, api.go, CreateCompany.vue, Section.tsx |
| 2026-07-17 14:58 | Paso 2 — Hallazgos | 0 bugs bloqueantes, 5 riesgos a verificar: BUG-CR-001 (Zod schema discrepancy), BUG-CR-002 (email input type), BUG-CR-003 (company suggestion), BUG-CR-004 (no confirm on cancel), BUG-CR-005 (Settings regression) |
| 2026-07-17 14:59 | Paso 2 — TCs inyectados | TC-CR-001 a TC-CR-005 inyectados en test-matrix.md y test-matrix.csv. Total TCs: 42 |
| 2026-07-17 15:04 | Deployment Paso 3 — Testing Sesión 1 | Modo Asistido Playwright MCP. Usuarios: skuanquis@gmail.com + testqacatalyst2026@gmail.com (nuevo) |
| 2026-07-17 15:08 | Paso 3 — Smoke + Regresión | TC-029/033/034/035 PASS (con usuario existente) |
| 2026-07-17 15:17 | Paso 3 — Nuevo usuario | Registrado testqacatalyst2026@gmail.com en Keycloak. Redirigido a /create-company |
| 2026-07-17 15:19 | Paso 3 — Happy Path | TC-001/002/003/004/005/006/008/009/010/017 PASS. TC-001 E2E: Company "QA Catalyst Test Company" creada exitosamente |
| 2026-07-17 15:38 | Paso 3 — Veredicto INCORRECTO | Sugerí APPROVED sin verificar post-registro. **ERROR del Catalyst** |
| 2026-07-17 18:36 | QA Engineer reportó bugs | /profile sin datos + Settings 403. QA Engineer cuestionó correctamente el veredicto |
| 2026-07-17 18:38 | Paso 3 — Investigación bugs | Playwright MCP confirmó: BUG-001 (403 BLOCKER), BUG-002 (profile MAJOR), BUG-003 (header MINOR) |
| 2026-07-17 18:42 | Paso 3 — Veredicto corregido | ❌ REJECTED. Artefactos actualizados: bug-report.md, test-results-s1.md, test-matrix.md |
| 2026-07-17 18:48 | QA Engineer — Regla añadida | Regla "Sincronización de Test Matrix en tiempo real" + "Verificación Post-Acción" añadida a sprint-testing/test.md |
| 2026-07-17 19:36 | Dev envió fix | Dev corrigió BUG-001 (permisos). BUG-002 (/profile) fuera de scope (feature distinta). Datos deben mostrarse en /settings |
| 2026-07-17 19:37 | Re-test Sesión 2 | Nuevo usuario: retestqacatalyst2026@gmail.com. Registro + submit + verificación post-acción completa |
| 2026-07-17 19:41 | Re-test — Resultados | BUG-001 ✅ CORREGIDO (Settings, Accounts sin 403). Datos persisten en /settings. TC-030/032/035 → PASS |
| 2026-07-17 19:44 | **Deployment Paso 4 — Reporte** | qa-report.md generado. **Veredicto: ✅ APROBADO**. Ticket listo para merge |




