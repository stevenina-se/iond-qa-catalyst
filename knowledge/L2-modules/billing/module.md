# Módulo: Billing

> Gestión de suscripciones, planes y pagos vía Stripe. Cubre la relación entre entidades de IONFLOW (Company/Account) y los productos/planes de Stripe.
> Última actualización: 2026-06-02

## Información General

| Campo | Valor |
|-------|-------|
| Nombre interno | billing |
| Criticidad | 🟠 Alto |
| Repos involucrados | `flow_binaries` (API + webhook handler), `gateway-ion` (UI billing/checkout) |
| Estado | 🚧 En construcción — Fase 1 (ticket 86dzbhzdm) |
| Dependencias externas | Stripe API (`github.com/stripe/stripe-go/v81`) |
| Tickets origen | `86dzbhzdm` (Fase 1), `IONF-880` (Fase 2), `IONF-879` (Consumo) |

---

## Overview

El módulo de Billing gestiona las suscripciones de usuarios/compañías en IONFLOW conectándose con Stripe como procesador de pagos. Se implementa en dos fases:

- **Fase 1** (este módulo): Conexión administrativa con Stripe — persistencia de estado de suscripción, webhooks, consulta de planes. **Sin enforcement**.
- **Fase 2** (futuro): Conexión con consumo real medido (IONF-879) para aplicar límites, créditos y bloqueos.

### Concepto Clave: Dos Mundos de Identidad

La suscripción se vincula polimórficamente a dos tipos de entidad distintos:

| Entidad | Auth | DB | Quién la crea | Stripe Customer |
|---------|------|-----|---------------|-----------------|
| **Company** (IONFLOW) | Laravel JWT RS256 | Per-tenant Postgres (`TENANT_DB`) | Usuario se auto-registra | Company → 1 Stripe Customer |
| **Account** (Old Engine / Grapps) | WebComponent HMAC HS256 | Shared `MAIN_DB` con `account_id` FK | `DeveloperApp` la crea programáticamente | Account → 1 Stripe Customer |

---

## Frontend (gateway-ion)

> ⚠️ **Pendiente de implementación** — Las rutas se documentarán cuando el frontend de billing esté construido.

### Rutas esperadas (basadas en análisis técnico)

| Ruta | Vista | Descripción | Permiso esperado |
|------|-------|-------------|------------------|
| `/billing` | Billing Dashboard | Estado de suscripción actual, tier, fechas | Owner de company |
| `/billing/checkout` | Checkout redirect | Redirige a Stripe Checkout Session | Owner de company |
| `/billing/portal` | Portal redirect | Redirige a Stripe Billing Portal | Owner de company |

### Stores (Pinia) esperados

| Store | Estado que gestiona |
|-------|---------------------|
| `useBillingStore` | Tier actual, status, period dates, stripe_customer_id |

---

## API (flow_binaries)

### Endpoints — Fase 1A: Stripe Infrastructure

| Método | Path | Descripción | Auth requerida |
|--------|------|-------------|----------------|
| POST | `/stripe/webhook` | Endpoint público para recibir webhooks de Stripe | ❌ No (verificación por firma `STRIPE_WEBHOOK_SECRET`) |

### Endpoints — Fase 1B: Subscription Query

| Método | Path | Descripción | Auth requerida |
|--------|------|-------------|----------------|
| GET | `/api/1.0/tenants/{tenantId}/subscription` | Consulta suscripción de una Company | ✅ JWT (solo owner) |
| GET | `/api/2.0/webcomponent/subscription` | Consulta suscripción de un Account | ✅ WebComponent HMAC |

### Endpoints — Fase 1C: Checkout & Portal

| Método | Path | Descripción | Auth requerida |
|--------|------|-------------|----------------|
| POST | `/api/1.0/tenants/{tenantId}/subscription/checkout` | Crear Stripe Checkout Session para Company | ✅ JWT (solo owner) |
| POST | `/api/1.0/tenants/{tenantId}/subscription/portal` | Generar URL de Stripe Billing Portal | ✅ JWT (solo owner) |
| POST | `/api/2.0/webcomponent/subscription/checkout` | Checkout para Account | ✅ WebComponent HMAC |
| POST | `/api/2.0/webcomponent/subscription/portal` | Portal para Account | ✅ WebComponent HMAC |

### Payloads (request/response) — Esperados

```json
// GET /api/1.0/tenants/{tenantId}/subscription
// Response:
{
  "subscribable_type": "company",
  "subscribable_id": 123,
  "stripe_customer_id": "cus_xxx",
  "stripe_subscription_id": "sub_xxx",
  "tier": "pro",
  "status": "active",
  "current_period_start": "2026-01-01T00:00:00Z",
  "current_period_end": "2026-02-01T00:00:00Z",
  "last_payment_date": "2026-01-01T00:00:00Z"
}
```

```json
// POST /api/1.0/tenants/{tenantId}/subscription/checkout
// Response:
{
  "checkout_url": "https://checkout.stripe.com/c/pay/cs_xxx"
}
```

```json
// POST /api/1.0/tenants/{tenantId}/subscription/portal
// Response:
{
  "portal_url": "https://billing.stripe.com/p/session/xxx"
}
```

---

## Canvas (webcomponents-flow)

> No aplica — El módulo de Billing no involucra el canvas de nodos.

---

## Database

> ⚠️ Schema propuesto — pendiente de implementación por DB expert.

### Tablas principales

| Tabla | Descripción | Ubicación |
|-------|-------------|-----------|
| `subscriptions` | Suscripciones polimórficas (Company o Account) | `MAIN_DB` |

### Modelo de datos propuesto

| Tabla | Columna | Tipo | Nullable | Descripción |
|-------|---------|------|----------|-------------|
| `subscriptions` | `id` | `uint64` / `uuid` | NO | PK |
| `subscriptions` | `subscribable_type` | `string` | NO | `"company"` o `"account"` |
| `subscriptions` | `subscribable_id` | `uint64` | NO | FK polimórfico |
| `subscriptions` | `stripe_customer_id` | `string` | NO | ID de customer en Stripe |
| `subscriptions` | `stripe_subscription_id` | `string` | YES | ID de suscripción en Stripe (null para Free/ION) |
| `subscriptions` | `tier` | `enum` | NO | `free`, `go`, `pro`, `teams`, `ion` |
| `subscriptions` | `status` | `enum` | NO | `active`, `past_due`, `canceled`, `unpaid`, `trialing` |
| `subscriptions` | `current_period_start` | `timestamp` | YES | Inicio del período actual |
| `subscriptions` | `current_period_end` | `timestamp` | YES | Fin del período (expiry_date) |
| `subscriptions` | `last_payment_date` | `timestamp` | YES | Último pago exitoso |

### Relaciones (Foreign Keys)

| Tabla origen | Columna | Tabla destino | Columna destino | Tipo |
|-------------|---------|--------------|-----------------|------|
| `subscriptions` | `subscribable_id` (when type=`company`) | `companies` | `id` | Polimórfico |
| `subscriptions` | `subscribable_id` (when type=`account`) | `accounts` | `id` | Polimórfico |

### Estados y transiciones

```
                    ┌─────────────┐
                    │  (no record)│ ── checkout ──→ ┌──────────┐
                    │  = "free"   │                 │ trialing │
                    └─────────────┘                 └────┬─────┘
                                                        │ payment success
                                                        ▼
┌──────────┐   invoice.payment_failed   ┌──────────┐
│ past_due │ ◄───────────────────────── │  active   │
└────┬─────┘                            └────┬─────┘
     │ payment success                       │ customer.subscription.deleted
     │ ──────────────► active                │
     │                                       ▼
     │ subscription.deleted             ┌──────────┐
     └─────────────────────────────────►│ canceled │
                                        └──────────┘

     Tier ION: No pasa por Stripe, se asigna manualmente.
     Status siempre "active", sin stripe_subscription_id.
```

### Queries de verificación frecuentes

```sql
-- Verificar suscripción de una company
SELECT * FROM subscriptions
WHERE subscribable_type = 'company' AND subscribable_id = '<company_id>';

-- Verificar suscripción de un account
SELECT * FROM subscriptions
WHERE subscribable_type = 'account' AND subscribable_id = '<account_id>';

-- Buscar suscripción por stripe_customer_id
SELECT * FROM subscriptions
WHERE stripe_customer_id = '<cus_xxx>';

-- Verificar transición de estado post-webhook
SELECT id, tier, status, current_period_end, last_payment_date
FROM subscriptions
WHERE stripe_subscription_id = '<sub_xxx>';

-- Listar todas las suscripciones activas
SELECT subscribable_type, subscribable_id, tier, status, current_period_end
FROM subscriptions
WHERE status = 'active'
ORDER BY current_period_end ASC;

-- Verificar tier ION (empleados internos)
SELECT * FROM subscriptions
WHERE tier = 'ion';

-- Detectar suscripciones vencidas (past_due o expiradas)
SELECT * FROM subscriptions
WHERE status = 'past_due'
   OR (status = 'active' AND current_period_end < NOW());
```

---

## Stripe Integration

### Tiers y Productos

| Tier | Stripe Product | Price | Notas |
|------|---------------|-------|-------|
| `free` | Sin producto | $0 | Estado default sin suscripción de Stripe |
| `go` | `prod_XXX` | Config en env (`STRIPE_GO_PRICE_ID`) | Plan de entrada |
| `pro` | `prod_XXX` | Config en env (`STRIPE_PRO_PRICE_ID`) | Tier medio |
| `teams` | `prod_XXX` | Config en env (`STRIPE_TEAMS_PRICE_ID`) | Multi-usuario |
| `ion` | Sin producto | Gratis | Interno/empleados. Ilimitado. Manual. |

### Webhook Events Procesados

| Evento Stripe | Acción en IONFLOW | Campos actualizados |
|---------------|-------------------|---------------------|
| `checkout.session.completed` | Crear registro de suscripción, vincular Stripe Customer | `stripe_customer_id`, `stripe_subscription_id`, `tier`, `status` |
| `customer.subscription.created` | Insert/update suscripción | `tier`, `status`, `current_period_start`, `current_period_end` |
| `customer.subscription.updated` | Actualizar (maneja cambios de plan) | `tier`, `status`, `current_period_start`, `current_period_end` |
| `customer.subscription.deleted` | Marcar como `canceled` | `status` → `canceled` |
| `invoice.payment_succeeded` | Actualizar pago | `last_payment_date`, `status` → `active` |
| `invoice.payment_failed` | Marcar como moroso | `status` → `past_due` |

### Variables de Entorno Requeridas

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `STRIPE_SECRET_KEY` | API key de Stripe (server-side) | `sk_test_xxx` |
| `STRIPE_WEBHOOK_SECRET` | Secret para verificar firma de webhooks | `whsec_xxx` |
| `STRIPE_GO_PRICE_ID` | Price ID del plan Go | `price_xxx` |
| `STRIPE_PRO_PRICE_ID` | Price ID del plan Pro | `price_xxx` |
| `STRIPE_TEAMS_PRICE_ID` | Price ID del plan Teams | `price_xxx` |

### Flujo de Checkout (Secuencia)

```
Usuario (Owner) → IONFLOW API → Stripe Checkout Session → Stripe Hosted Page
                                                              │
                                                        (pago exitoso)
                                                              │
                                                              ▼
Stripe webhook → IONFLOW /stripe/webhook → Verify signature → Route event
                                                                   │
                                              ┌────────────────────┤
                                              ▼                    ▼
                                    checkout.session       customer.subscription
                                    .completed             .created
                                              │                    │
                                              ▼                    ▼
                                    Create/Update           Update subscription
                                    subscription record     tier, status, dates
```

---

## Componentes de Código (flow_binaries)

### Archivos nuevos esperados

| Archivo / Paquete | Fase | Descripción |
|--------------------|------|-------------|
| `backend/ion/services/stripe/` | 1A | Stripe API client (Go wrapper) |
| `backend/ion/models/subscription.go` | 1A (interface) / 1B (impl) | Modelo de suscripción + binding polimórfico |
| `backend/ion/services/subscription_service.go` | 1A (interface) / 1B (impl) | Servicio CRUD de suscripciones |
| `backend/routes/api.go` | 1A-1C | Nuevas rutas de webhook, query, checkout |
| `backend/ion/middleware/` | 1C | Middleware de inyección de contexto de suscripción |
| `backend/ion/controllers/` | 1B-1C | Controllers de billing y suscripciones |

### Patrones a seguir

- **Polimorfismo**: Seguir el patrón existente de `Webhook` (`WebhookableType` + `WebhookableId`)
- **Webhook HTTP**: Seguir la convención existente `/webhook/{tenantId}/{webhookUuid}`
- **Middleware**: Insertar después de JWT/Tenant resolution como paso read-only (Fase 1)
- **Service interface**: Definir interface primero (1A), implementar con GORM después (1B)

---

## Impacto Cruzado

### Módulos que Billing afecta
| Módulo destino | Componente afectado | Tipo | Ejemplo |
|---------------|--------------------|-----------------|---------| 
| **Auth** | Middleware pipeline | Middleware | Billing inyecta contexto de suscripción post-auth (read-only F1) |
| **Boards** | Ejecución de flows (Fase 2) | Ejecución | Futuro: enforcement de límites por tier |
| **Executions** | Consumo (Fase 2) | Datos | Futuro: billing consultará `UnitsConsumed` de executions |

### Módulos que afectan a Billing
| Módulo origen | Componente | Tipo | Ejemplo |
|--------------|------------|-----------------|---------| 
| **Auth** | JWT + Tenant resolution | Middleware | Billing requiere auth válida para consultar suscripción |
| **Accounts** | Account path | Datos | Accounts pueden tener suscripciones (polimórfico) |
| **Developer Apps** | Creación de accounts | Datos | Dev apps crean accounts que pueden tener billing |
| **Stripe (externo)** | Webhooks | Datos | Eventos Stripe actualizan estado de suscripción |

### Tablas compartidas
| Tabla | Módulos que la usan | Riesgo si cambia |
|-------|---------------------|------------------|
| `subscriptions` (PG) | Billing (exclusivo) | Solo billing por ahora; Fase 2 lo expone a más módulos |
| `companies` (PG) | Billing (subscribable_id), Auth, TODOS | FK polimórfico: cambios en companies afectan billing |
| `accounts` (PG) | Billing (subscribable_id), Accounts, Integrations | FK polimórfico: cambios en accounts afectan billing |

---

## Preguntas Abiertas (sin respuesta del PM)

> ⚠️ Estas preguntas fueron identificadas en el análisis técnico y bloquean parcialmente Phase 1B.

| ID | Pregunta | Impacto |
|----|----------|---------|
| Q1 | ¿Modelo polimórfico (Company+Account) es correcto, o solo un tipo inicialmente? | Diseño de tabla |
| Q2 | ¿Quién maneja billing para Accounts creados por DeveloperApp? | Flujo de checkout/portal |
| Q3 | ¿Cómo distinguir company owner vs member? (no hay `role` en `company_user`) | Permisos de billing |
| Q4 | ¿Cómo se asigna el tier ION? ¿Manual? ¿Email domain? ¿Flag? | Implementación de override |
| Q5 | ¿Free es suscripción de Stripe con $0 o simplemente ausencia de suscripción? | Lógica de createOrUpdate |

---

## Test Data

### Datos necesarios para testing

| Dato | Cómo obtenerlo | Notas |
|------|----------------|-------|
| Stripe test API key | Stripe Dashboard → Developers → API keys (Test mode) | `sk_test_xxx` |
| Stripe webhook secret | Stripe CLI o Dashboard | `whsec_xxx` |
| Stripe test Products/Prices | Crear en Stripe Dashboard (Test mode) | Uno por tier (Go, Pro, Teams) |
| Company de prueba | Crear via UI o DB seed | Para probar Company path |
| Account de prueba | Crear via DeveloperApp API | Para probar Account path |
| Tarjetas de prueba Stripe | `4242424242424242` (success), `4000000000000341` (fail) | [Stripe test cards](https://docs.stripe.com/testing) |

### Herramientas de testing

| Herramienta | Uso |
|-------------|-----|
| **Stripe CLI** | `stripe listen --forward-to localhost:PORT/stripe/webhook` — forward webhooks locales |
| **Stripe CLI trigger** | `stripe trigger checkout.session.completed` — simular eventos |
| **Postman** | Test de endpoints de query/checkout/portal |
| **DBeaver** | Validación de tabla `subscriptions` |

---

## Tests E2E Existentes (bot-test)

> ❌ No existen tests E2E para Billing — módulo completamente nuevo.

### Tests a crear

| Test | Cobertura | Prioridad |
|------|-----------|-----------|
| `billing-subscription-query.spec.ts` | Query de suscripción por Company y Account | 🔴 |
| `billing-webhook-processing.spec.ts` | Procesamiento de webhooks de Stripe (simulated) | 🔴 |
| `billing-checkout-flow.spec.ts` | Flujo de checkout end-to-end | 🟠 |
| `billing-tier-ion.spec.ts` | Override de tier ION para empleados | 🟡 |
| `billing-no-enforcement.spec.ts` | Regresión: flows siguen ejecutándose sin restricción | 🟡 |

---

## Edge Cases Conocidos

| ID | Descripción | Severidad | Mitigación |
|----|-------------|-----------|------------|
| EC-001 | Webhook duplicado — Stripe reintenta y el handler procesa el mismo evento dos veces | 🔴 Crítico | Handlers idempotentes, check de event ID procesado |
| EC-002 | Race condition — Dos webhook events para la misma suscripción llegan simultáneamente | 🟠 Alto | DB locking o `ON CONFLICT` upsert en `stripe_subscription_id` |
| EC-003 | Estado divergente — DB local desincronizado de Stripe (sin job de reconciliación en F1) | 🟠 Alto | Aceptado como limitación de Fase 1; sync job en futuro |
| EC-004 | Company sin owner — `company_user` no tiene `role`; no se puede determinar quién accede a billing | 🟠 Alto | Depende de Q3 del PM |
| EC-005 | Webhook sin firma válida — Si no se valida `STRIPE_WEBHOOK_SECRET`, cualquiera puede enviar eventos falsos | 🔴 Crítico | Verificación de firma obligatoria en handler |
| EC-006 | Tier ION sin Stripe — Empleados no tienen `stripe_subscription_id`; queries deben manejar null | 🟡 Medio | Check de `tier == 'ion'` antes de llamar Stripe |
| EC-007 | Free tier ambiguity — ¿Registro sin suscripción o suscripción con tier=free? Afecta queries | 🟡 Medio | Depende de Q5 del PM |

---

## Historial de Actualizaciones

| Fecha | Tickets | Cambios | Actualizado por |
|-------|---------|---------|-----------------|
| 2026-06-02 | `86dzbhzdm` | Creación inicial del módulo L2 Billing basado en análisis técnico de Fase 1 Stripe | QA Catalyst |
