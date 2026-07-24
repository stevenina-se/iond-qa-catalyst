# Test Plan — IONF-1056-B (Zero-Stripe)

> Generado por `sprint-testing/plan`
> Track: Discovery PASO 6 — Plan preparado para ejecución en Deployment

## Información del Ticket

| Campo | Valor |
|-------|-------|
| ID | 86e1pzyug (IONF-1056) |
| Título | Monetización unificada: Stripe, consumo por segundos, AI credits e IONPDF |
| Branch de Deployment | **IONF-1056-B** (variante zero-Stripe) |
| Módulo | billing (nuevo) |
| Módulos impactados | executions, boards, pdf-templates, nodes, dashboard |
| QA Engineer | Steve Nina |
| Developer | Enrique Vicente |
| Fecha del plan | 2026-07-23 |
| Branches | `IONF-1056-B` en flow_binaries, gateway, gateway-ion |

## Resumen

| Métrica | Valor |
|---------|-------|
| Total de casos | 61 (42 funcionales + 6 regresión + 6 nuevos IONF-1056-B + 5 code review + 2 bloqueados) |
| Tiempo estimado | ~8.5-10.5 horas (540 min) |
| Artefactos de Discovery | risk-triage.md, ac-reconciliation.md, ac-consolidated.md, test-matrix.md/.csv |
| Riesgo general | 🔴 Crítico (módulo nuevo que controla acceso a todo el producto) |
| Sesiones recomendadas | 3-4 sesiones de ~2.5 horas |

> **⚠️ NOTA SOBRE SCOPE**: Este plan es para el branch **IONF-1056-B** (zero-Stripe). Toda la funcionalidad de Stripe (checkout, webhooks, overage, meter events, cancel/resume) fue eliminada. Los planes se asignan exclusivamente por admin. La UI de tenant es read-only.

---

## Orden de Ejecución

### BLOQUE 1 — SMOKE TESTS (ejecutar PRIMERO — si alguno falla → ESCALAR)

> ⚠️ Si cualquier smoke test falla, el módulo de billing tiene un problema fundamental.
> NO continuar con los bloques siguientes hasta resolver.

```
□ TC-001: Plan free se aprovisiona al crear company — 🔴
□ TC-100: Admin asigna plan a company → consumptions se sincronizan — 🔴
□ TC-090: Flows con saldo disponible ejecutan correctamente — 🔴
□ TC-030: execution_time agotado bloquea en editor — 🔴
□ TC-022: available=-1 nunca bloquea — 🔴
□ TC-104: /billing/plans muestra pricing cards read-only — 🟠
```

**Gate de Smoke**: ¿Los 6 smoke tests pasaron?
- → SÍ: Continuar a Bloque 2
- → NO: **ESCALAR al Developer.** El problema es de fundación del billing.

---

### BLOQUE 2 — HAPPY PATH (Verificar flujos principales)

> Cubrir los flujos core del sistema de billing: provisioning, admin assignment, consumo, enforcement, notificaciones.

```
Admin Assignment:
□ TC-101: Admin asigna plan a company sin suscripción previa — 🔴
□ TC-113: Asignación admin genera fila admin_assigned en renewals — 🟠

Provisioning & Schema:
□ TC-003: Solo existe 1 suscripción por company — 🔴
□ TC-005: Billing owner puede ser company — 🟡

Consumo:
□ TC-020: Feature con ventanas mensual + diaria simultáneas — 🔴
□ TC-024: Lazy reset — consumed arranca en qty no en suma — 🔴
□ TC-026: GET /subscription/usage persiste lazy reset — 🟠
□ TC-027: Ventana absoluta (NULL) — reset_at=NULL nunca reinicia — 🟠
□ TC-028: Verificar que NO existe cron — resets son lazy — 🔴

Enforcement:
□ TC-031: execution_time agotado bloquea en live production — 🔴
□ TC-032: execution_time agotado — schedules/webhooks NO se eliminan — 🔴
□ TC-033: pdf_templates agotado bloquea creación — 🟠

Guard sin Overage (IONF-1056-B):
□ TC-106: Consumo supera cap → 403 + email "contact us" — 🔴
□ TC-108: Plan enterprise sin windows → guard bloquea todo — 🔴

AI Credits:
□ TC-110: Flow-pilot consume ai_credits — SSE limit message — 🔴
□ TC-111: IonMind endpoints retornan 403 al agotar — 🔴

Notificaciones:
□ TC-040: Email warning al 80% con "contact us" — 🟠
□ TC-043: Layout de email usa diseño IonFlow unificado — 🟡

Tenant UI:
□ TC-105: /billing/subscription muestra plan + usage bars sin acciones — 🟠
```

**Gate de Happy Path**: ¿Al menos 90% de los happy path pasaron?
- → SÍ: Continuar a Bloque 3
- → NO: Evaluar impacto. Si billing core falla → escalar.

---

### BLOQUE 3 — EDGE CASES (Verificar bordes)

```
Consumo:
□ TC-021: Ventana diaria agotada bloquea aunque mensual tenga saldo — 🔴
□ TC-023: available=0 bloquea aunque consumed=0 — 🟠
□ TC-025: Anchor lattice — reset_at avanza desde anchor anterior — 🟠

Enforcement:
□ TC-034: pdf_impressions agotado — nodo PDF falla mid-execution — 🟠
□ TC-035: Guard fail-open — error de infra permite ejecución — 🟠
□ TC-037: ⚠️ BLOQUEADO Grace execution — pendiente P-01 — 🔴 ⏸

Admin Assignment:
□ TC-102: Botón Assign plan deshabilitado hasta cambiar selección — 🟠
□ TC-103: Asignación admin limpia stripe_subscription_id local — 🟠

Notificaciones:
□ TC-041: Email warning al 100% sin mención de overage — 🟠
□ TC-042: Email de bloqueo al agotar saldo — 🟠
□ TC-045: Deduplicación de emails por threshold — 🟡

Stripe Residual:
□ TC-107: grep -ri stripe en flow_binaries — solo mappings dormidos — 🟠
```

---

### BLOQUE 4 — NEGATIVOS (Verificar que NO se puede romper)

```
□ TC-004: No existe columna status en subscriptions — 🟠
□ TC-036: Feature no provisionada → guard retorna 403 — 🟠
□ TC-044: No se generan notificaciones in-app — 🟡
□ TC-073: IONPDF no aparece clasificado como OCR — 🟡
```

---

### BLOQUE 5 — IONPDF Y RUNTIME HISTORY

> Funcionalidad específica de IONPDF y tracking de ejecuciones.

```
IONPDF:
□ TC-070: Asignación admin de plan IONPDF aprovisiona features — 🟠
□ TC-071: Cambio de plan — entitlements IONFLOW no se modifican — 🟠
□ TC-072: Consumo IONPDF queda en ledger unificado — 🟠

Runtime History:
□ TC-080: Ejecución registra active_seconds, idle_seconds, units_consumed — 🟠
□ TC-081: Nodo Timer incrementa idle_seconds — 🟠
□ TC-082: Subflow waitForResponse incrementa idle_seconds — 🟠
□ TC-083: ⚠️ BLOQUEADO Visualización Board — pendiente rediseño UI — 🟠 ⏸
□ TC-084: Estado neutro sin ejecuciones previas — 🟡
```

---

### BLOQUE 6 — REGRESIÓN

> Verificar que módulos existentes no se rompieron con la introducción de billing.

```
□ TC-091: Historial de ejecuciones sigue funcionando — 🔴
□ TC-092: Schedule no se elimina cuando execution_time se agota — 🟠
□ TC-093: Webhook no se elimina cuando execution_time se agota — 🟠
□ TC-094: Creación de PDF templates funciona con cuota disponible — 🟠
□ TC-095: Templates existentes no se ven afectados por quota — 🟠
```

---

### BLOQUE 7.5 — CODE REVIEW VERIFICATION

> TCs inyectados por el code review QA. Verifican riesgos encontrados en el código.

```
□ TC-CR-001: Company nueva: primer request post auto-provisioning — guard permite — 🟠
□ TC-CR-002: AI credits race condition: requests rápidos con créditos casi agotados — 🟠
□ TC-CR-003: PHP guard vs Go guard: reset_at vencido, primera consulta por PHP — 🟠
□ TC-CR-004: Admin cambia plan: ¿consumed persiste o se resetea? — 🟠
□ TC-CR-005: Feature con ventana diaria: ¿email de 80% se genera? — 🟡
```

---

### BLOQUE 8 — ADMIN CATALOG Y DB EVIDENCE

> Verificación de catálogo admin y queries de BD.

```
Admin Catalog:
□ TC-109: Admin Products.vue read-only sin Stripe sync — 🟡
□ TC-112: ProductSeeder crea producto local con provider=local — 🟠

DB Evidence:
□ DB-001: SELECT * FROM subscriptions WHERE subscriber_type='company' → plan_id correcto, sin columna status
□ DB-002: SELECT * FROM feature_consumptions → windows del plan sincronizadas con available correcto
□ DB-003: SELECT * FROM subscription_renewals WHERE event='admin_assigned' → audit trail correcto
□ DB-004: SELECT blocked, available, consumed FROM feature_consumptions WHERE available=-1 → blocked=false
□ DB-005: SELECT provider FROM products → todos 'local' (sin Stripe references)
□ DB-006: Verificar que NO existe columna 'status' en subscriptions: information_schema.columns
```

---

## Datos Necesarios

| Dato | Cómo obtenerlo | Notas |
|------|---------------|-------|
| **Usuario Tenant (Company)** | `.env` → `IONFLOW_COMPANY_USERNAME` / `IONFLOW_COMPANY_PASSWORD` | Rol Company — para testing de tenant UI y consumo |
| **Usuario Admin** | `.env` → `IONFLOW_ADMIN_USERNAME` / `IONFLOW_ADMIN_PASSWORD` | Rol Administrator — para Admin Assignment y Catalog |
| **URL de staging** | `.env` → `IONFLOW_ENVIRONMENT_URL` | Canal 1 (Playwright MCP) |
| **Company de prueba** | Company existente en staging con plan free auto-provisionado | Para TC-001, TC-003, TC-100 |
| **Company nueva** | Crear durante testing o usar company sin billing access previo | Para TC-101 (admin assign sin suscripción) |
| **Flow de prueba** | Flow existente con nodos configurados (idealmente con nodo PDF y Timer) | Para TC-030/031/032, TC-034, TC-080/081 |
| **Flow con subflow** | Flow que llame a un subflow con `waitForResponse=true` | Para TC-082 |
| **Template PDF existente** | Template PDF ya creado en staging | Para TC-094, TC-095 |
| **DBeaver** | Conexión SSH tunnel activa al PostgreSQL de staging | Para DB-001 a DB-006 |
| **Setup BD** | Migraciones ejecutadas + seeders: FeatureSeeder → PlanSeeder → PlanFeatureSeeder + laratrust reseed | **Prerequisito del deploy** (confirmado por Rodolfo 22-Jul) |

### Setup especial para testing

> Basado en las QA Instructions del branch IONF-1056-B:

| Paso de setup | Repo | Detalle |
|--------------|------|---------|
| Migraciones | gateway | `products` → `plans` → `plan_features` → `subscriptions` → `features.product_id` → `feature_consumptions` alter → `subscription_renewals` |
| Seeders | gateway | `FeatureSeeder` → `PlanSeeder` → `PlanFeatureSeeder` (en orden) |
| Laratrust | gateway | Re-run con `truncate_tables => true` — re-seed roles después |
| Env vars | flow_binaries | `STRIPE_*` vars **NO necesarias** en IONF-1056-B |
| Hub URL | gateway-ion | Verificar `VITE_APP_HUB_URL` seteado — billing calls lo necesitan |

---

## Criterios de Aprobación/Rechazo

### ✅ CRITERIOS DE APROBACIÓN

```
✅ TODOS los smoke tests (Bloque 1) pasan — 6/6
✅ TODOS los happy path críticos (🔴) pasan
✅ Al menos 85% de los happy path totales (Bloque 2) pasan — 16/19
✅ Al menos 75% de los edge cases (Bloque 3) pasan — 9/12
✅ TODOS los negativos (Bloque 4) pasan — 4/4
✅ TODOS los casos de regresión (Bloque 6) pasan — 5/5
✅ DB evidence confirma integridad de datos — 6/6
```

### ❌ CRITERIOS DE RECHAZO

```
❌ Algún smoke test falla → RECHAZO INMEDIATO
❌ Plan free no se aprovisiona (TC-001) → RECHAZO — billing inutilizable
❌ Admin assign no funciona (TC-100) → RECHAZO — única vía de cambio de plan
❌ Guard no bloquea execution_time (TC-030/031) → RECHAZO — enforcement roto
❌ Guard bloquea feature ilimitada available=-1 (TC-022) → RECHAZO — funcionalidad core rota
❌ Flows con saldo no ejecutan (TC-090) → RECHAZO — regresión crítica
❌ Lazy reset suma en vez de reemplazar (TC-024) → RECHAZO — consumo corrupto
❌ Caso negativo falla (sistema se puede romper) → RECHAZO
❌ DB evidence muestra datos corruptos → RECHAZO
```

### ⚠️ APROBACIÓN CON OBSERVACIONES

```
⚠️ Edge case no bloqueante falla → Aprobar + bug registrado
⚠️ Email con defecto visual menor (layout) → Aprobar con observación
⚠️ Botón "Assign plan" sin disable state (TC-102) → Aprobar con observación
⚠️ Runtime History con issue menor → Aprobar con bug de prioridad baja
⚠️ TC-037 (grace execution) bloqueado por P-01 → Aprobar con P-01 documentada como pendiente
⚠️ TC-083 (Board UI) bloqueado por rediseño → Aprobar si API funciona correctamente
```

---

## Estimación de Tiempo

| Bloque | Casos | Tiempo estimado | Notas |
|--------|-------|-----------------|-------|
| 1. Smoke Tests | 6 | ~30 min | Gate bloqueante |
| 2. Happy Path | 19 | ~120 min | Core del billing — incluye AI credits |
| 3. Edge Cases | 12 | ~90 min | Incluye boundary conditions y lazy reset |
| 4. Negativos | 4 | ~20 min | Rápidos — verificaciones de schema y guards |
| 5. IONPDF + Runtime | 8 | ~60 min | Setup de datos específico |
| 6. Regresión | 5 | ~40 min | Módulos existentes |
| 7.5 Code Review | 5 | ~30 min | Verificación de riesgos del code review |
| 8. Admin Catalog + DB | 8 | ~45 min | DBeaver queries + catalog UI |
| **Total** | **67** (incl. DB) | **~435 min (~7.25 hrs)** | **3-4 sesiones recomendadas** |

### Distribución recomendada de sesiones

| Sesión | Bloques | Duración | Foco |
|--------|---------|----------|------|
| **Sesión 1** | Bloques 1 + 2 (parcial: Admin + Provisioning + Consumo) | ~2 hrs | Fundación. Si falla aquí → escalar |
| **Sesión 2** | Bloque 2 (resto: Enforcement + AI + UI) + Bloque 3 | ~2.5 hrs | Guards, edge cases, lazy reset |
| **Sesión 3** | Bloques 4 + 5 + 6 | ~2 hrs | Negativos, IONPDF, regresión |
| **Sesión 4** | Bloque 7 | ~45 min | DB evidence y catalog |

---

## Herramientas de Testing

| Herramienta | Uso | Canal |
|------------|-----|-------|
| **Playwright MCP** | Navegación asistida para UI tenant/admin | Canal 1 — supervisado por QA |
| **DBeaver** | Queries BD (PostgreSQL SSH tunnel) — evidencia de provisioning, consumptions, renewals | Manual |
| **DevTools (F12)** | Consola (errores JS), Network (API 403s), verificar SSE messages (AI credits) | Manual |
| **cURL / API Client** | Testing directo de endpoints: `/subscription/usage`, guards 403 | Manual / script |

---

## Preguntas Pendientes (del Risk Triage / Discovery)

> ⚠️ Estas preguntas afectan TCs específicos. Resolver ANTES o DURANTE testing.

| # | Pregunta | TC afectado | Urgencia |
|---|----------|-------------|----------|
| P-01 | ¿Grace execution implementada o descartada? IONF-1056-B no la menciona | TC-037 | 🔴 Urgente |
| P-03 | ¿Qué mensaje ve el usuario en UI al bloquear execution_time? | TC-030, TC-031 | 🟠 Alto |
| P-04 | ¿Existe endpoint API para consultar última duración de ejecución? | TC-083 | 🟠 Alto |

> **P-02 RESUELTA**: Los resets son lazy. IONF-1056-B confirma explícitamente. TC-028 desbloqueado.

---

## Estado

```
✅ Plan creado en Discovery PASO 6 — listo para Deployment.

Artefactos de Discovery completos:
  ✅ ac-reconciliation.md (7 divergencias críticas documentadas)
  ✅ risk-triage.md (7 riesgos críticos, 15 altos, 7 medios)
  ✅ ac-consolidated.md (57 ACs activos — reconsiderado IONF-1056-B)
  ✅ test-matrix.md + .csv (56 TCs en 13 suites — reconsiderado IONF-1056-B)
  ✅ test-plan.md (este documento)
```
