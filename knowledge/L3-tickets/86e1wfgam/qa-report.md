# QA Report — 86e1wfgam

> Reporte final de QA generado por `sprint-testing/report`
> Fecha: 2026-08-23
> QA Engineer: Steve Nina

## Información del Ticket

| Campo | Valor |
|-------|-------|
| Ticket ID | 86e1wfgam |
| Título | Motor de exposición por API (FASE 1) |
| Módulo | DevApp API — Connectors, Accounts, Flows, Mappers, PDF Templates |
| Branch | IONF-1082 (merged to DEVELOPMENT) |
| Entorno | dev-app.ionflow.io |
| Browser | Chrome |
| QA Engineer | Steve Nina |
| Fecha de testing | 2026-08-23 |

---

## Resumen Ejecutivo

| Métrica | Valor |
|---------|-------|
| Total de casos ejecutados | 45 |
| Casos aprobados | 45 |
| Casos fallidos | 0 |
| Casos parciales | 0 |
| Casos saltados | 0 |
| **Tasa de aprobación** | **100%** |
| Bugs encontrados (testing) | 0 |
| Bugs encontrados (code review) | 0 |
| Bugs bloqueantes (🔴) | 0 |
| Limitaciones conocidas | 2 (aceptadas) |

---

## Evaluación contra Criterios

| Criterio | Requerido | Resultado | Cumple |
|----------|-----------|-----------|--------|
| Happy Path | 100% | 14/14 (100%) | ✅ |
| Edge Cases | ≥80% | 15/15 (100%) | ✅ |
| Negativos | 100% | 11/11 (100%) | ✅ |
| Regresión | 100% | 5/5 (100%) | ✅ |
| Bugs 🔴 abiertos | 0 | 0 | ✅ |

---

## Veredicto

| Campo | Valor |
|-------|-------|
| Sugerencia del Catalyst | ✅ Approved |
| **Veredicto final (QA Engineer)** | **✅ Approved** |
| Firmado por | Steve Nina |
| Fecha | 2026-08-23 |
| Observaciones | 2 limitaciones conocidas documentadas (aceptadas, no son bugs) |

---

## Resultados por Bloque

### SUPERFICIE 1: Motor de Tokens y Fronteras de Auth (15 TCs)

| ID | Tipo | Caso | Resultado | Notas |
|----|------|------|-----------|-------|
| TC-001 | Happy Path | Emitir token OAuth2 válido | ✅ | JWT RS256, scopes en payload |
| TC-002 | Negativo | Grant type no soportado | ✅ | 400 sin datos internos |
| TC-003 | Negativo | Sin scope en request de token | ✅ | 400 |
| TC-004 | Negativo | Scope desconocido | ✅ | 422 |
| TC-005 | Negativo | Secret incorrecto | ✅ | 401 sin leak |
| TC-006 | Negativo | Client ID de otro guard | ✅ | 401 |
| TC-007 | Negativo | Body malformado | ✅ | 400 |
| TC-008 | Happy Path | Registrar customer (account) | ✅ | 201 con datos correctos |
| TC-009 | Edge Case | Repetir mismo remote_id | ✅ | 409 unique por compañía |
| TC-010 | Happy Path | Listar y detallar accounts | ✅ | Lista + detalle OK |
| TC-011 | Negativo | Ruta account-scoped sin Account-Id | ✅ | 400 |
| TC-012 | Edge Case | Account-Id de cuenta ajena | ✅ | 404 uniforme |
| TC-013 | Edge Case | Token con scope parcial | ✅ | 403 con scope faltante |
| TC-014 | Edge Case | Token revocado | ✅ | 401 "Invalid token" uniforme |
| TC-015 | Edge Case | Token expirado | ✅ | 401 "Invalid token" uniforme |

### SUPERFICIE 2: Connectors Autodescriptivos (11 TCs)

| ID | Tipo | Caso | Resultado | Notas |
|----|------|------|-----------|-------|
| TC-016 | Happy Path | Catálogo de connectors namespaced | ✅ | Names `app.<tipo>` |
| TC-017 | Edge Case | Alias resuelve igual que canónico | ✅ | `shipedge` = `app.shipedge` |
| TC-018 | Negativo | Namespace tenant reservado | ✅ | 404 |
| TC-019 | Happy Path | Detalle connector CON Account-Id | ✅ | Actions + conexiones |
| TC-020 | Edge Case | Detalle connector SIN Account-Id | ✅ | Solo specs |
| TC-021 | Happy Path | Ejecución con Connection-Id explícito | ✅ | Respuesta raw |
| TC-022 | Edge Case | Ejecución con 1 conexión implícita | ✅ | Implícita OK |
| TC-023 | Edge Case | Ejecución con >1 conexiones sin Connection-Id | ✅ | 409 + candidatas |
| TC-024 | Negativo | Connector no vinculado a la app | ✅ | 404 |
| TC-025 | Negativo | Action no habilitada | ✅ | 400 |
| TC-026 | Negativo | Token read-only intentando ejecutar | ✅ | 403 |

### SUPERFICIE 3: PDF Templates via API (6 TCs)

| ID | Tipo | Caso | Resultado | Notas |
|----|------|------|-----------|-------|
| TC-027 | Happy Path | Spec de template PDF | ✅ | Shape autodescriptivo |
| TC-028 | Happy Path | Render simple de PDF | ✅ | URL pública funcional |
| TC-029 | Edge Case | Render batch (2 páginas) | ✅ | PDF multi-página válido |
| TC-030 | Negativo | PDF sin scope | ✅ | 403 |
| TC-031 | Negativo | PDF sin Account-Id | ✅ | 400 |
| TC-032 | Negativo | Plantilla de otra compañía | ✅ | 404 |

### SUPERFICIE 4: UI del Diseñador PDF (2 TCs)

| ID | Tipo | Caso | Resultado | Notas |
|----|------|------|-----------|-------|
| TC-033 | Happy Path | Crear y diseñar PDF template | ✅ | Flujo completo funcional |
| TC-034 | Edge Case | Error con motor caído | ✅ | Mensaje de error visible |

### SUPERFICIE 5: Accounts Compartidos por Compañía (6 TCs)

| ID | Tipo | Caso | Resultado | Notas |
|----|------|------|-----------|-------|
| TC-035 | Happy Path | App B ve customer de App A | ✅ | Compartido por compañía |
| TC-036 | Edge Case | App B no puede crear mismo remote_id | ✅ | 409 unique por compañía |
| TC-037 | Happy Path | App C (otra compañía) crea mismo remote_id | ✅ | 201 sin conflicto |
| TC-038 | Edge Case | App C no ve customer de compañía A | ✅ | Aislamiento correcto |
| TC-039 | Happy Path | Customer API visible en UI | ✅ | Visible en tenant Accounts |
| TC-040 | Edge Case | App B ejecuta contra customer de A | ✅ | Ejecución compartida OK |

### SUPERFICIE 6: Flows por API (3 TCs)

| ID | Tipo | Caso | Resultado | Notas |
|----|------|------|-----------|-------|
| TC-041 | Happy Path | Listar flows sin Account-Id | ✅ | Agregado con account_remote_id |
| TC-042 | Happy Path | Ejecutar flow activo | ✅ | Ejecución síncrona OK |
| TC-043 | Negativo | Ejecutar flow inactivo | ✅ | 409 "flow is not active" |

### REGRESIÓN (5 TCs)

| ID | Tipo | Caso | Resultado | Notas |
|----|------|------|-----------|-------|
| REG-001 | Regresión | Flows del board ejecutan normal | ✅ | Runner compartido sin impacto |
| REG-002 | Regresión | Conexiones del webcomponent | ✅ | Sin cambios |
| REG-003 | Regresión | Rutas Laravel existentes | ✅ | Convivencia permanente |
| REG-004 | Regresión | Migración BD correcta | ✅ | Índices parciales creados |
| REG-005 | Regresión | Cuentas legacy preservadas | ✅ | Datos intactos |

---

## Bugs Encontrados

| Bug ID | Severidad | Estado | Módulo | Descripción | TC | Evidencia |
|--------|-----------|--------|--------|-------------|-----|-----------|
| — | — | — | — | No se encontraron bugs | — | — |

---

## Limitaciones Conocidas (documentadas, no son bugs)

| # | Descripción | Impacto | Decisión |
|---|-------------|---------|----------|
| LIM-01 | Laravel `POST /api/2.0/app/accounts` valida `remote_id` como único global (Go sí permite per-company) | Falla seguro (422), no corrompe datos | Aceptada — se resolverá en ticket de scoping Laravel |
| LIM-02 | Seq Scan en `accounts` con pocos registros (PostgreSQL descarta índice) | Sin impacto funcional | Aceptada — beneficio al crecer la tabla |

---

## Decisiones de Diseño Aceptadas

| Decisión | Justificación |
|----------|---------------|
| Token revocado/expirado devuelve 401 "Invalid token" uniforme | Evita enumeración de clientes OAuth |
| Accounts son propiedad de la compañía (no de la app) | Simplifica integración multi-app |
| Respuestas raw (sin envelope `{data}`) | Transparencia para integradores |
| `Connection-Id` como header (no body) | Patrón Stripe-Account |
| Flow INACTIVE no ejecuta (409) pero sí se puede leer | Separación lectura/escritura |
| `pdf_templates` no devuelve binario en response | Seguridad + performance |

---

## Información de Entorno

| Details | |
|---------|---|
| BROWSER | Chrome |
| BRANCH | IONF-1082 (merged to DEVELOPMENT) |
| ENV | dev-app.ionflow.io |
| TEST MATRIX | knowledge/L3-tickets/86e1wfgam/test-matrix.md |
| MERGE REQUESTS | [webcomponents-flow PR #28](https://github.com/altacrest/ion_webcomponents_flow/pull/28), [gateway-ion PR #52](https://github.com/altacrest/ion_gateway_ion/pull/52), [flow_binaries PR #16](https://github.com/altacrest/ion_flow_binaries/pull/16/changes), [gateway PR #51](https://github.com/altacrest/ion_gateway/pull/51) |
