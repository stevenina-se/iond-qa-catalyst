# Code Review QA — 86e1wfgam

> Reporte de revisión de código (Bug Hunting) generado por `code-review/review`
> Fecha: 2026-08-23
> QA Engineer: Steve Nina

## Información del Ticket

| Campo | Valor |
|-------|-------|
| Ticket ID | 86e1wfgam |
| Título | Motor de exposición por API (FASE 1) |
| Developer | Rodolfo Merlo Ali (principal), Alex Chura, Gustavo Mamani |
| Módulo | developer-apps, accounts, connections, pdf-templates |
| Branch | IONF-1082 (merged to DEVELOPMENT) |

---

## Pull Requests Revisados

| # | Repo | PR | Stack | Archivos cambiados | Líneas (+/-) |
|---|------|----|-------|-------------------|-------------|
| 1 | webcomponents-flow | [PR #28](https://github.com/altacrest/ion_webcomponents_flow/pull/28) | Vue 3 + TS | Webcomponentes `gt-pdf-list`, `gt-pdf-workspace` | N/A |
| 2 | gateway-ion | [PR #52](https://github.com/altacrest/ion_gateway_ion/pull/52) | Vue 3 + TS | Vistas PDF List, Marketplace tab | N/A |
| 3 | flow_binaries | [PR #16](https://github.com/altacrest/ion_flow_binaries/pull/16/changes) | Go | Motor OAuth2, endpoints DevApp API, PDF render | N/A |
| 4 | gateway | [PR #51](https://github.com/altacrest/ion_gateway/pull/51) | PHP 8.2 (Laravel) | Migraciones BD, seeder PDF demo, rutas Passport | N/A |

---

## Tests Automatizados del Developer

| Repo | Framework | Resultado | Notas |
|------|-----------|-----------|-------|
| flow_binaries (Go) | Go test | 1554 tests PASS, 0 FAIL ✅ | Suite completa |
| gateway-ion (Vue) | Vitest | 1625 passed, 3 skipped ✅ | Skips pre-existentes |
| webcomponents-flow (Vue) | Vitest | 797 passed, 1 skipped ✅ | Skip pre-existente |
| gateway (Laravel) | PHPUnit | Suite pre-existente ⚠️ | Fallas de entorno local, no relacionadas con este ticket |

**Total**: 3,976 tests automatizados pasando.

---

## Code Review Aprobado Por

| Reviewer | Resultado |
|----------|-----------|
| Gustavo Mamani | ✅ Aprobado |

---

## Hallazgos del Code Review

### Áreas revisadas

| Área | Verificación | Resultado |
|------|-------------|-----------|
| Multi-tenant isolation | Accounts filtrados por `company_id`, connectors por `app_id` | ✅ Correcto |
| SQL injection | Queries parametrizadas en Go (sqlx) y Laravel (Eloquent) | ✅ Correcto |
| Auth bypass | Middleware `AppAuthMiddleware` valida token + scopes en cada ruta | ✅ Correcto |
| Token security | RS256, tokens en `oauth_access_tokens`, revocación inmediata | ✅ Correcto |
| Error leakage | 401 uniforme para token revocado/expirado/desconocido | ✅ Correcto (deliberado) |
| Scope enforcement | Scopes validados en emisión y en cada endpoint | ✅ Correcto |
| Account-Id validation | Header obligatorio en rutas account-scoped, 404 para cross-company | ✅ Correcto |
| Connection-Id resolution | Automática (1 = implícita, 0 = sin credenciales, >1 = 409) | ✅ Correcto |
| PDF binary exposure | Binario nunca en respuesta, solo URL pública R2 | ✅ Correcto |
| Migration safety | Índices parciales preservan unicidad de cuentas legacy | ✅ Correcto |

### Bugs encontrados en Code Review

| Bug ID | Severidad | Descripción | TC inyectado | Estado |
|--------|-----------|-------------|-------------|--------|
| — | — | No se encontraron bugs durante el code review | — | — |

### Limitaciones conocidas identificadas (no son bugs)

| # | Descripción | Impacto | Decisión |
|---|-------------|---------|----------|
| LIM-01 | Laravel `POST /api/2.0/app/accounts` valida `remote_id` como único global (la superficie Go sí permite per-company) | Falla seguro (422), no corrompe datos | Aceptada — se resolverá cuando se scopeen los controllers Laravel por compañía |
| LIM-02 | Seq Scan en tabla `accounts` con pocos registros (PostgreSQL ignora índice cuando full scan es más barato) | Sin impacto funcional | Aceptada — beneficio aparece al crecer la tabla |

---

## TCs inyectados desde Code Review

No se inyectaron TCs adicionales. Los 45 TCs existentes de Discovery ya cubrían los escenarios de seguridad y multi-tenant identificados durante el code review.

---

## Conclusión

La revisión de código de 4 repositorios y 4 PRs no arrojó bugs. Las 10 áreas de verificación (multi-tenant, SQL injection, auth bypass, token security, error leakage, scope enforcement, Account-Id validation, Connection-Id resolution, PDF binary exposure, migration safety) fueron evaluadas satisfactoriamente. Se documentaron 2 limitaciones conocidas que no representan riesgo y fueron aceptadas por el equipo. Los 3,976 tests automatizados del developer pasan exitosamente.
