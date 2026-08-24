# Test Plan — 86e1wfgam (Motor de exposición por API — FASE 1)

## Información del Ticket

| Campo | Valor |
|-------|-------|
| ID | 86e1wfgam |
| Título | Motor de exposición por API (FASE 1) |
| Módulo principal | Developer Apps |
| Módulos impactados | Accounts, Connections, PDF Templates, Boards |
| QA Engineer | Steve Nina |
| Developer | Rodolfo Merlo Ali |
| Fecha del plan | 2026-08-09 |
| Track | Discovery → Deployment |

---

## Resumen

| Métrica | Valor |
|---------|-------|
| Total de casos | 45 (40 funcionales + 5 regresión) |
| Tiempo estimado total | ~180 min (~3 horas) |
| Herramienta principal | Colecciones `.http` (REST Client VS Code) en `gateway/` |
| Herramienta BD | DBeaver (PostgreSQL vía SSH tunnel) |
| Herramienta UI | Browser directo (2 TCs UI) |

### Artefactos de Discovery usados

| Artefacto | Estado |
|-----------|--------|
| `risk-triage.md` | ✅ Aprobado |
| `ac-consolidated.md` | ✅ Aprobado (22 ACs en 8 superficies) |
| `test-matrix.md` + `.csv` | ✅ Aprobado (45 TCs) |
| `code-review-qa.md` | ⏭️ Omitido por decisión del QA |

---

## Setup Previo (antes de cualquier TC)

> ⏱️ Tiempo estimado: ~15 min

| # | Acción | Comando / Detalle | Verificación |
|---|--------|-------------------|--------------|
| S-1 | Migración Gateway | `php artisan migrate` | Sin errores |
| S-2 | Variables de entorno Binaries | Configurar en `.env`: `PDF_GENERATE_URL`, `R2_*`, `DEVAPP_TOKEN_RATE`, `oauth-private.key` en `./storage` | Binaries arranca sin error |
| S-3 | Template-maker corriendo | `PORT=3005 bun run index.ts` (repo template-maker) | Servicio responde en `:3005` |
| S-4 | Seeder demo PDF | `php artisan db:seed --class=DevAppPdfTemplateSeeder` | "Demo Order Receipt" existe |
| S-5 | Identificar credenciales | Query SQL (ver test-matrix.md) → seleccionar App A, App B (misma compañía) y App C (otra compañía) | 3 sets de credenciales listos |
| S-6 | Abrir colecciones `.http` | Abrir `devapp-token.http`, `devapp-connectors.http`, `devapp-pdf.http` en VS Code | Placeholders `<...>` completados |

---

## Orden de Ejecución

### BLOQUE 1 — SMOKE TESTS (ejecutar primero, si alguno falla → escalar)

> ⏱️ ~10 min | Si falla → **STOP, escalar al Developer**

```
□ TC-001: Emitir token OAuth2 válido — 🔴
□ TC-008: Registrar customer (account) — 🔴
□ TC-016: Catálogo de connectors namespaced — 🔴
□ TC-028: Render simple de PDF — 🔴
```

**Gate**: ¿Los 4 smoke tests pasan? → SÍ: continuar | NO: STOP y escalar.

---

### BLOQUE 2 — AUTH COMPLETO (Superficie 1)

> ⏱️ ~25 min | Colección: `devapp-token.http`

```
EMISIÓN DE TOKEN
  □ TC-001: Token válido → 200 + JWT RS256 — 🔴 (ya ejecutado en smoke)
  □ TC-002: Grant type no soportado → 400 — 🔴
  □ TC-003: Sin scope → 400 — 🔴
  □ TC-004: Scope desconocido → 422 — 🟠
  □ TC-005: Secret incorrecto → 401 — 🔴
  □ TC-006: Client no-apps → 401 — 🟠
  □ TC-007: Body malformado → 400 — 🟡

ACCOUNTS
  □ TC-008: Crear customer → 201 — 🔴 (ya ejecutado en smoke)
  □ TC-009: Repetir remote_id → 409 — 🔴
  □ TC-010: Listar + detallar → 200 — 🟠

FRONTERAS DE AUTH
  □ TC-011: Sin Account-Id → 400 — 🔴
  □ TC-012: Account-Id ajeno → 404 — 🔴
  □ TC-013: Scope parcial → 403 con nombre — 🟠
  □ TC-014: Token revocado → 401 uniforme — 🟠
  □ TC-015: Token expirado → 401 uniforme — 🟠
```

---

### BLOQUE 3 — CONNECTORS (Superficie 2)

> ⏱️ ~30 min | Colección: `devapp-connectors.http`

```
CATÁLOGO Y DETALLE
  □ TC-016: Catálogo namespaced — 🔴 (ya en smoke)
  □ TC-017: Alias vs canónico — 🟠
  □ TC-018: tenant.* → 404 — 🟡
  □ TC-019: Detalle CON Account-Id → actions + conexiones — 🔴
  □ TC-020: Detalle SIN Account-Id → solo specs — 🟠

EJECUCIÓN
  □ TC-021: Execute con Connection-Id explícito → raw response — 🔴
  □ TC-022: Execute con 1 conexión implícita — 🟠
  □ TC-023: Execute con >1 conexiones sin CID → 409 — 🟠

FRONTERAS
  □ TC-024: Connector no vinculado → 404 — 🟠
  □ TC-025: Action no habilitada → 400 — 🟠
  □ TC-026: Token read-only → 403 — 🟠
```

---

### BLOQUE 4 — PDF TEMPLATES (Superficie 3 + 4)

> ⏱️ ~25 min | Colección: `devapp-pdf.http` + Browser

```
API
  □ TC-027: Spec de template → shape autodescriptivo — 🟠
  □ TC-028: Render simple → {filename, public_url} + PDF válido — 🔴 (ya en smoke)
  □ TC-029: Render batch 2 páginas — 🟠
  □ TC-030: Sin scope → 403 — 🟠
  □ TC-031: Sin Account-Id → 400 — 🟡
  □ TC-032: Plantilla ajena → 404 — 🟡

UI (Browser)
  □ TC-033: Crear + diseñar + guardar template — 🟡
  □ TC-034: Motor caído → mensaje de error — 🟡
```

---

### BLOQUE 5 — ACCOUNTS COMPARTIDOS (Superficie 5)

> ⏱️ ~30 min | **LA PRUEBA CENTRAL DEL MODELO**

```
MODELO COMPARTIDO
  □ TC-035: App B ve customer de App A (misma compañía) — 🔴
  □ TC-036: App B no puede crear mismo remote_id → 409 — 🔴
  □ TC-037: App C (otra compañía) crea mismo remote_id → 201 — 🔴
  □ TC-038: App C no ve customer de compañía A — 🔴

UI
  □ TC-039: Customer API visible en UI Accounts — 🟠

EJECUCIÓN CROSS-APP
  □ TC-040: App B ejecuta contra customer de A con connector — 🔴
```

---

### BLOQUE 6 — FLOWS (Superficie 6)

> ⏱️ ~15 min

```
  □ TC-041: Listar flows sin Account-Id → agregado — 🟠
  □ TC-042: Ejecutar flow activo → OK — 🟠
  □ TC-043: Ejecutar flow INACTIVE → 409 — 🟠
```

---

### BLOQUE 7 — REGRESIÓN

> ⏱️ ~20 min | **Obligatorio antes del veredicto**

```
  □ REG-001: Flows del board ejecutan normal (runner compartido) — 🔴
  □ REG-002: Conexiones del webcomponent siguen normales — 🟠
  □ REG-003: Rutas Laravel existentes responden igual — 🟠
  □ REG-004: Migración BD → índices parciales correctos — 🔴
  □ REG-005: Cuentas legacy preservadas — 🟠
```

---

### BLOQUE 8 — DB EVIDENCE

> ⏱️ ~10 min | DBeaver

```
  □ DB-001: Token registrado en oauth_access_tokens con scopes correctos
  □ DB-002: Customer creado con company_id correcto
  □ DB-003: 2 customers con mismo remote_id en compañías diferentes
  □ DB-004: Índices parciales en accounts verificados (pg_indexes)
  □ DB-005: Cuentas legacy sin company_id intactas
  □ DB-006: Template de demo "Demo Order Receipt" con status active
```

---

## Datos Necesarios

| Dato | Cómo obtenerlo | Notas |
|------|---------------|-------|
| App A (client_id + secret) | Query S-5 | Compañía X |
| App B (client_id + secret) | Query S-5 | **Misma compañía X** que App A |
| App C (client_id + secret) | Query S-5 | **Compañía Y ≠ X** |
| Connector vinculado a App A | Configurar en la app (si no existe) | Con al menos 1 action habilitada |
| Connector shipedge | Verificar que existe como canal demo | Para tests de alias/namespacing |
| Flow activo e inactivo | Crear o identificar en BD | Para TC-042 y TC-043 |
| Template PDF de demo | Seeder S-4 | "Demo Order Receipt" |
| Usuario Company con permisos | Credenciales en `.env` del catalyst | Para UI tests (TC-033, TC-034, TC-039) |
| Acceso DBeaver | SSH tunnel configurado | Para DB Evidence |

---

## Criterios de Aprobación / Rechazo

### ✅ CRITERIOS DE APROBACIÓN

```
✅ TODOS los smoke tests pasan (Bloque 1: TC-001, 008, 016, 028)
✅ TODOS los happy path pasan (14 TCs)
✅ Al menos 80% de los edge cases pasan (12/15 mínimo)
✅ TODOS los negativos pasan (11 TCs — no se puede romper el sistema)
✅ TODOS los casos de regresión pasan (5 TCs)
✅ DB evidence confirma integridad de datos (6 queries)
✅ Aislamiento entre compañías verificado (TC-012, 035-038)
```

### ❌ CRITERIOS DE RECHAZO

```
❌ Algún smoke test falla → rechazo inmediato, escalar al Dev
❌ Happy path falla → rechazo
❌ Caso negativo falla (API se puede romper/datos se filtran) → rechazo
❌ Aislamiento entre compañías falla (TC-012, 038) → rechazo CRÍTICO
❌ Regresión de flows del board falla (REG-001) → rechazo con análisis de impacto
❌ Migración BD incorrecta (REG-004) → rechazo, no deployar
❌ DB evidence muestra datos cruzados entre compañías → rechazo CRÍTICO
```

### ⚠️ APROBACIÓN CON OBSERVACIONES

```
⚠️ Edge case de UI falla pero API funciona → aprobar con bug registrado
⚠️ Limitación conocida de Laravel remote_id (422 global) → documentar, no bloquear
⚠️ Rate limit no verificable en staging → aprobar con nota
⚠️ Motor caído no muestra mensaje claro (TC-034) → aprobar con bug UX
```

---

## Estimación de Tiempo

| Bloque | Casos | Tiempo estimado |
|--------|-------|-----------------|
| Setup | 6 pasos | ~15 min |
| Bloque 1: Smoke Tests | 4 | ~10 min |
| Bloque 2: Auth completo | 15 | ~25 min |
| Bloque 3: Connectors | 11 | ~30 min |
| Bloque 4: PDF Templates | 8 | ~25 min |
| Bloque 5: Accounts compartidos | 6 | ~30 min |
| Bloque 6: Flows | 3 | ~15 min |
| Bloque 7: Regresión | 5 | ~20 min |
| Bloque 8: DB Evidence | 6 | ~10 min |
| **Total** | **45 TCs + 6 DB** | **~180 min (~3 horas)** |

> ⚠️ El tiempo puede variar significativamente dependiendo del estado del ambiente de staging y la disponibilidad de datos de prueba.

---

## Riesgos del Plan

| Riesgo | Mitigación |
|--------|-----------|
| Template-maker no disponible | Ejecutar Bloque 4 al final; no bloquea Bloques 1-3, 5-6 |
| Faltan apps con OAuth en staging | Crear manualmente antes de iniciar (Query S-5) |
| Connector shipedge no configurado | Usar cualquier connector disponible para alias test |
| Flows no existen en la app | Crear un flow de prueba antes de Bloque 6 |

---

## Estado

⏳ **Plan creado** — Esperando inicio de ejecución en Deployment.

> Cuando el QA Engineer indique "testear ticket 86e1wfgam", seguir:
> **→ `skills/deployment-runbook.md`**
