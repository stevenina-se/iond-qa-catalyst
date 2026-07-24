# Módulo: Billing / Subscriptions

> Módulo que gestiona las suscripciones, entitlements, consumo de recursos y facturación vía Stripe.
> Introducido en: IONF-1056 (Monetización unificada)
> Última actualización: 2026-06-14

## Información General

| Campo | Valor |
|-------|-------|
| Nombre interno | billing |
| Criticidad | 🟠 Alto |
| Repos involucrados | `gateway` (schema BD + provisioning), `flow_binaries` (motor consumo + webhooks Stripe + API), `gateway-ion` (UI billing) |
| Última actualización | 2026-06-14 — Discovery IONF-1056 |

---

## Frontend (gateway-ion)

### Rutas
| Ruta | Vista | Descripción |
|------|-------|-------------|
| `/billing` (tentativo) | Billing UI Tenant | Vista de planes, uso, suscripción activa |
| `/admin/billing` (tentativo) | Admin plan editor | Editor de planes, features y ventanas |

### Componentes clave
| Componente | Ubicación | Descripción |
|-----------|-----------|-------------|
| Tenant billing UI | `src/views/billing/` (tentativo) | Muestra plan, barras de consumo por feature, reset date |
| Admin plan editor | `src/views/admin/billing/` (tentativo) | CRUD de products, plans, plan_features (ventanas) |

> ⚠️ Las rutas y componentes exactos están pendientes de confirmar en el repositorio (módulo en construcción).

---

## API (flow_binaries)

### Endpoints Tenant (`/api/1.0/tenants/{id}/`, JWT + TenantAuth, permiso `ManageBilling` o `ReadBilling`)

| Método | Path | Permiso | Descripción |
|--------|------|---------|-------------|
| GET | `/plans` | ReadBilling | Planes públicos disponibles |
| GET | `/subscription` | ReadBilling | Suscripción completa (plan, pending_plan, data, timestamps) |
| GET | `/subscription/usage` | ReadBilling | Consumo real por feature (persiste lazy resets) |
| POST | `/subscription/cancel` | ManageBilling | Cancela la suscripción (`canceled_at` + `expires_at`) |
| POST | `/subscription/resume` | ManageBilling | Reanuda suscripción cancelada |
| POST | `/checkout-session` | ManageBilling | Crea sesión de pago Stripe (solo primera suscripción → 409 si ya existe) |
| POST | `/subscription/change-plan` | ManageBilling | Cambia de plan (`{plan_slug, interval?, when?}`) |
| POST | `/subscription/overage` | ManageBilling | Activa/modifica overage para un feature (`{feature_slug, units}`) |
| POST | `/billing-portal` | ManageBilling | Crea sesión del portal de Stripe |

### Endpoints Admin (`/billing/...`)

| Método | Path | Descripción |
|--------|------|-------------|
| GET/POST/DELETE | `/billing/products` | CRUD de productos |
| GET/POST/PUT/DELETE | `/billing/plans` | CRUD de planes |
| GET/PUT | `/billing/features` | Listar y actualizar features |
| POST | `/billing/plans/{planId}/features` | Agregar UNA ventana de feature al plan |
| PUT/DELETE | `/billing/plan-features/{planFeatureId}` | Modificar/eliminar ventana específica |

### Códigos de respuesta clave
| Código | Situación |
|--------|-----------|
| 200/201 | Operación exitosa |
| 403 (`ErrQuotaBlocked`) | Feature bloqueada por consumo agotado |
| 409 | Intento de crear segunda suscripción (checkout-session) |
| 422 | Gates de overage fallaron (plan free, dunning, feature no en plan, etc.) |

---

## Database (PostgreSQL — gateway schema)

### Tablas principales

| Tabla | Descripción |
|-------|-------------|
| `products` | Productos Stripe (IONFLOW, IONPDF, etc.) |
| `plans` | Planes comerciales (free, go, pro, ion, enterprise) |
| `features` | Features medibles (execution_time, ai_credits, pdf_templates, pdf_impressions) |
| `plan_features` | Allowances por plan+feature+ventana (1 fila por ventana) |
| `subscriptions` | Suscripción activa por company (1 per company) |
| `feature_consumptions` | Consumo real por company+feature+ventana (fuente de verdad) |
| `feature_consumption_logs` | Log audit append-only de cada consumo |
| `subscription_renewals` | Log audit de ciclo de vida Stripe |

### Columnas clave — `subscriptions`

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `subscriber_type/id` | morph | Entidad suscrita (company o user) |
| `plan_id` | FK | Plan actual |
| `pending_plan_id` | FK nullable | Cambio de plan diferido |
| `data` | jsonb | Snapshot de entitlement (price + overage + ventanas por feature) |
| `stripe_subscription_id` | UK nullable | ID de suscripción en Stripe |
| `canceled_at` | timestamp | Cancelación solicitada por usuario |
| `expires_at` | timestamp | Cuándo termina el acceso |
| `renews_at` | timestamp | Próxima renovación (base lines only) |

### Columnas clave — `feature_consumptions`

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `feature_id` | FK bigint | Feature asociado |
| `subscriber_type/id` | morph | Company o user |
| `measure` | string | `absolute` \| `daily` \| `monthly` \| `weekly` \| `yearly` |
| `consumed` | decimal | Uso actual en la ventana |
| `available` | decimal | Límite; `-1` = ilimitado |
| `reset_at` | timestamp | Próximo reset lazy; `NULL` = nunca (absolute) |
| `blocked` | boolean GENERATED | `available <> -1 AND consumed >= available` — solo lectura |
| `metadata` | jsonb | `{ period_unit, period_count }` |

### Estados de suscripción (derivados de timestamps)

```
[Active]     canceled_at IS NULL AND (expires_at IS NULL OR expires_at > now)
[Canceled]   canceled_at IS NOT NULL  (acceso hasta expires_at)
[Dunning]    canceled_at IS NULL AND expires_at IS NOT NULL  (pago fallido)
[Lapsed]     expires_at <= now  (sin acceso, hasta webhook deleted)
[Free]       Post deleted webhook → DowngradeToFree
```

### Seed defaults de entitlements

| Feature \ Plan | free | go | pro | ion |
|---|---|---|---|---|
| `execution_time` (s/mes) | 600 | 3,600 | 86,400 | -1 (ilimitado) |
| `ai_credits` | 100 | 100,000 | 500,000 | -1 |
| `pdf_templates` (absoluto) | 1 | 3 | -1 | -1 |
| `pdf_impressions` | 50/mes + 10/día | 2,000/mes + 100/día | -1 | -1 |

### Queries de verificación frecuentes

```sql
-- Verificar suscripción activa de una company
SELECT id, plan_id, canceled_at, expires_at, renews_at, stripe_subscription_id, data
FROM subscriptions
WHERE subscriber_type = 'company' AND subscriber_id = <company_id>;

-- Estado derivado de la suscripción
SELECT
  id,
  CASE
    WHEN canceled_at IS NULL AND (expires_at IS NULL OR expires_at > NOW()) THEN 'Active'
    WHEN canceled_at IS NOT NULL THEN 'Canceled-serving'
    WHEN canceled_at IS NULL AND expires_at IS NOT NULL THEN 'Dunning'
    WHEN expires_at <= NOW() THEN 'Lapsed'
  END AS derived_state
FROM subscriptions WHERE subscriber_id = <company_id>;

-- Ver consumo actual por feature
SELECT fc.measure, fc.consumed, fc.available, fc.blocked, fc.reset_at, f.slug
FROM feature_consumptions fc
JOIN features f ON fc.feature_id = f.id
WHERE fc.subscriber_type = 'company' AND fc.subscriber_id = <company_id>
ORDER BY f.slug, fc.measure;

-- Verificar renewal log (ciclo de vida Stripe)
SELECT kind, event, period_start, period_end, amount, currency, created_at
FROM subscription_renewals
WHERE subscription_id = <sub_id>
ORDER BY created_at DESC;

-- Verificar logs de consumo de un feature
SELECT consumed_before, consumed_after, qty, created_at, notification_type
FROM feature_consumption_logs
WHERE feature_consumption_id = <fc_id>
ORDER BY created_at DESC
LIMIT 20;
```

---

## Lógica Backend (flow_binaries)

### Servicios involucrados

| Service | Archivo (tentativo) | Función |
|---------|---------------------|---------|
| `GuardFeature` / `IsBlocked` | `backend/ion/services/billing*.go` | Evalúa si feature está bloqueada antes de ejecución |
| `RecordConsumption` | `backend/ion/services/billing*.go` | Registra consumo, aplica lazy reset, dispara meter Stripe |
| `SyncConsumptions` | `backend/ion/services/billing*.go` | Sincroniza feature_consumptions desde plan_features |
| `EnsureSubscription` | `backend/ion/services/billing*.go` | Garantiza sub free + sync en primer touch |
| Stripe webhook handlers | `backend/ion/webhooks/stripe*.go` | `payment_succeeded`, `payment_failed`, `subscription.deleted` |

### Reglas de negocio críticas

1. **Guard fail-open**: si hay error de infra, se permite (no se bloquea por error técnico)
2. **Grace execution**: 1 ejecución de gracia cuando se agota saldo sin overage → luego bloqueo
3. **Lazy resets**: no hay cron; el reset ocurre al leer/escribir cuando vence `reset_at`
4. **Anchor lattice**: `reset_at` avanza desde el anchor anterior, nunca desde "now"
5. **billableDelta**: `max(0, min(after, included+overage) - max(before, included))` — nunca over-bill
6. **renews_at solo de base lines**: overage invoices no mueven la fecha de renovación del plan base
7. **payment_failed**: revoca TODO el overage + abre dunning; recovery requiere re-activar overage manualmente
8. **-1 = ilimitado**: nunca bloquea, nunca cobra overage

### Archivos centinela

| Repo | Área | Razón |
|------|------|-------|
| `flow_binaries` | `backend/ion/services/` | Motor de consumo y guard |
| `flow_binaries` | `backend/ion/controllers/` | Endpoints billing API |
| `flow_binaries` | `backend/ion/webhooks/` | Handlers de Stripe |
| `gateway` | `database/migrations/` | Schema de todas las tablas de billing |
| `gateway` | `database/seeders/` | Seed de planes, features y entitlements |
| `gateway-ion` | `src/views/billing/` | UI de billing del tenant |

---

## Impacto Cruzado

### Módulos que Billing afecta

| Módulo destino | Componente afectado | Tipo | Ejemplo |
|---------------|--------------------|----|---------|
| **Executions** | Ejecución de flows | Bloqueo | Guard bloquea ejecución si `execution_time` agotado |
| **Boards** | Ejecución live/dev | Bloqueo | Schedules y webhooks quedan activos pero la ejecución no corre |
| **PDF Templates** | Creación de templates | Quota | `pdf_templates` es absoluto; si se agota no se crean más |
| **Nodes (PDF)** | Nodo PDF en canvas | Bloqueo | `pdf_impressions` falla mid-execution si agotado |
| **Dashboard** | Métricas de consumo | Datos | Dashboard debe reflejar consumo real del ledger |

### Módulos que afectan a Billing

| Módulo origen | Componente | Tipo | Ejemplo |
|--------------|------------|------|---------|
| **Executions** | `active_seconds` + `idle_seconds` | Consumo | Cada ejecución alimenta `execution_time` en el ledger |
| **PDF Templates** | Creación/uso de template | Consumo | Usa `pdf_templates` (quota) y `pdf_impressions` (ventana) |
| **Stripe** | Webhooks | Lifecycle | `payment_failed/succeeded/deleted` cambian estado de sub y entitlements |

### Tablas compartidas

| Tabla | Módulos que la usan | Riesgo si cambia |
|-------|---------------------|------------------|
| `feature_consumptions` | Billing, Executions, PDF Templates | Consumo incorrecto → bloqueos falsos o facturación errónea |
| `subscriptions` | Billing, Boards, Dashboard | Estado de sub incorrecto → acceso no controlado |
| `plan_features` | Billing, Admin | Cambio de allowances afecta entitlements de TODOS los subscribers |

---

## Edge Cases Conocidos (Discovery)

| ID | Descripción | Severidad |
|----|-------------|-----------|
| EC-001 | `renews_at` no debe avanzar en facturas de overage (solo base lines) | 🔴 Crítico |
| EC-002 | `payment_succeeded` mientras `canceled_at IS NOT NULL` no debe deshacer la cancelación | 🔴 Crítico |
| EC-003 | Lazy reset al 100% de consumo: `consumed` debe empezar en `qty`, no en `consumed + qty` | 🔴 Crítico |
| EC-004 | Overage `billableDelta` al cruzar el límite de `included`: solo cobra la porción sobre el límite | 🟠 Alto |
| EC-005 | Overage en plan anual + invoice mensual: no debe tocar `renews_at` anual | 🟠 Alto |
| EC-006 | Enterprise tier: sin features configuradas → guard bloquea todo por default | 🟠 Alto |
| EC-007 | Stripe redelivery de meter event no debe duplicar cargo (idempotencia `fcl:<log_id>`) | 🟠 Alto |
| EC-008 | `webcomponents-flow` aún lee shape antiguo de suscripción (pendiente migración) | 🟡 Medio |

---

## Historial de Cambios

| Fecha | Tickets | Cambios | Actualizado por |
|-------|---------|---------|----------------|
| 2026-06-14 | IONF-1056 | Creación inicial del módulo — Discovery prototipo | QA Catalyst |
