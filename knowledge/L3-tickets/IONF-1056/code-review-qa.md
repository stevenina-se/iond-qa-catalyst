# Code Review QA — IONF-1056-B (Modo Deployment / Bug Hunting)

> Generado por: `code-review/review` (modo Deployment)
> Fecha: 2026-07-23
> Branch: IONF-1056-B (zero-Stripe)
> QA Engineer: Steve Nina
> Developer: Enrique Vicente

## Resumen

| Métrica | Valor |
|---------|-------|
| Repos revisados | flow_binaries (Go), gateway (PHP), gateway-ion (Vue 3) |
| Archivos modificados analizados | ~254 (102 Go + 36 PHP + 116 Vue) |
| Bugs confirmados (reproducibles) | 0 |
| Riesgos a verificar en testing | 6 |
| Módulos con impacto cruzado | executions, boards, pdf-templates, nodes (AI/IonMind) |
| TCs inyectados en test-matrix | 5 (TC-CR-001 a TC-CR-005) |

---

## Archivos Modificados (billing core)

### [REPO: flow_binaries — Backend Go]

| Archivo | Tipo | Relevancia |
|---------|------|------------|
| `services/consumption_guard.go` (+89) | NUEVO | Guard principal — bloquea features agotados |
| `services/consumption_service.go` (+297) | MODIFICADO | Lazy reset, record consumption, log |
| `services/consumption_notify.go` (+184) | NUEVO | Emails de usage 80%/100%/blocked |
| `services/subscription/admin_service.go` (+227) | NUEVO | AdminAssignPlan, CRUD plans/features |
| `services/subscription/consumption_sync.go` (+266) | NUEVO | SyncConsumptions, upsert windows |
| `controllers/admin_billing_controller.go` (+410) | NUEVO | Admin HTTP handlers |
| `controllers/subscription_controller.go` (+59) | NUEVO | Tenant subscription endpoints |
| `controllers/chat_controller.go` (MODIFICADO) | MODIFICADO | Guard AI credits + SSE friendly message |
| `services/chatservice/chat_service.go` (MODIFICADO) | MODIFICADO | RecordConsumption de ai_credits al final del loop |
| `models/subscription.go`, `product.go`, `plan.go`, `feature*.go` | NUEVOS | Modelos de billing |

### [REPO: gateway — Backend PHP]

| Archivo | Tipo | Relevancia |
|---------|------|------------|
| `Services/Billing/FeatureGuard.php` (+57) | NUEVO | Guard en PHP para IonMind endpoints |
| `Controllers/Api/V2/App/IonMindController.php` (MODIFICADO) | MODIFICADO | Guard ai_credits en analyzeUrl, extractEndpoint, getEndpointVersions, forceUpdateLogo |
| `database/seeders/ProductSeeder.php` (+52) | NUEVO | Seeder de productos locales |
| `database/seeders/PlanSeeder.php` (+72) | NUEVO | Seeder de planes |
| `database/seeders/PlanFeatureSeeder.php` (+97) | NUEVO | Seeder de plan_features (windows) |
| `database/migrations/2026_05_28*` a `2026_06_11*` | NUEVOS | Schema billing completo |

### [REPO: gateway-ion — Frontend Vue 3]

| Archivo | Tipo | Relevancia |
|---------|------|------------|
| `views/tenant/billing/subscription.vue` (+393) | NUEVO | Vista de suscripción del tenant |
| `views/tenant/billing/plans.vue` (+231) | NUEVO | Vista de pricing cards |
| `views/admin/billing/Plans.vue` (+658) | NUEVO | Admin plan management |
| `views/admin/billing/Products.vue` (+103) | NUEVO | Admin product catalog |
| `views/admin/billing/Features.vue` (+173) | NUEVO | Admin features list |
| `views/admin/companies/CompanySubscription.vue` (+174) | NUEVO | Admin assign plan a company |
| `services/tenant/billing.service.ts` | NUEVO | API service tenant billing |
| `services/admin/billing.service.ts` | NUEVO | API service admin billing |
| `models/billing.ts` | NUEVO | TypeScript types para billing |

---

## Hallazgos del Bug Hunting

### BUG-CR-001 — RIESGO A VERIFICAR

**Severidad**: 🟠 Alto
**Repo**: flow_binaries
**Archivo**: [consumption_guard.go](file:///c:/Users/STEVE/Desktop/Automation/flow_binaries/backend/ion/services/consumption_guard.go#L44-L46)

**Descripción**: `isBlocked` retorna `true` cuando no hay filas (`len(rows) == 0`). Esto es correcto por diseño (feature no provisionada = bloqueada), pero **`GuardFeature` puede crear una suscripción free implícitamente** en L65-73 sin sincronizar consumptions. Si `GetByEntity` crea la suscripción pero `SyncConsumptions` no se ejecuta inmediatamente, hay una ventana temporal donde el guard bloquea features que deberían estar disponibles en plan free.

**Evidencia**:
```go
// L62-73 de consumption_guard.go
sub, err := subscription.GetByEntity(subscriber)
if err != nil {
    log.Printf("[consumption] GuardFeature: get subscriber: %v", err)
    return nil  // fail-open
}
if sub == nil {
    return nil  // no subscription — pass through
}
```

**Escenario para verificar**:
1. Company nueva sin suscripción previa
2. `GetByEntity` auto-provisiona suscripción free
3. Primer request intenta ejecutar un flow → ¿`isBlocked` retorna true por falta de filas en `feature_consumptions`?
4. Verificar si `SyncConsumptions` se ejecuta como parte de `GetByEntity`

**Impacto potencial**: Company nueva podría quedar bloqueada la primera vez que intenta ejecutar un flow

---

### BUG-CR-002 — RIESGO A VERIFICAR

**Severidad**: 🟡 Medio
**Repo**: flow_binaries
**Archivo**: [consumption_notify.go](file:///c:/Users/STEVE/Desktop/Automation/flow_binaries/backend/ion/services/consumption_notify.go#L63-L67)

**Descripción**: `maybeNotifyUsage` solo envía emails para ventanas con `period_unit = "month"` o `"year"` (L65-67). Si un plan tiene una ventana `"day"` o `"week"` como headline, las notificaciones de 80%/100% NO se enviarán.

**Evidencia**:
```go
// L65-67 de consumption_notify.go
if *window.PeriodUnit != "month" && *window.PeriodUnit != "year" {
    return
}
```

**Escenario para verificar**:
1. Feature con ventana diaria como headline
2. Consumir hasta 80% del saldo diario
3. Verificar que NO llega email (comportamiento intencional o bug?)

**Impacto potencial**: Features con ventanas diarias/semanales no generan alertas de consumo — puede ser diseño intencional, pero necesita confirmación

---

### BUG-CR-003 — RIESGO A VERIFICAR

**Severidad**: 🟠 Alto
**Repo**: flow_binaries
**Archivo**: [chat_service.go](file:///c:/Users/STEVE/Desktop/Automation/flow_binaries/backend/ion/services/chatservice/chat_service.go#L553-L603)

**Descripción**: `recordGlobalConsumption` registra los AI credits **en background** (`go cs.recordGlobalConsumption(totalUsage)` en L231). Esto significa que el `RecordConsumption` de ai_credits se ejecuta DESPUÉS de que la respuesta del chat ya fue enviada al usuario. Si el guard se ejecuta al inicio del próximo request y el consumo anterior aún no fue persistido, el usuario podría usar más créditos de los asignados (race condition entre guard y consumption).

**Evidencia**:
```go
// L231 de chat_service.go
go cs.recordGlobalConsumption(totalUsage)
```

**Escenario para verificar**:
1. Company con ai_credits casi agotados (ej. available=100, consumed=95)
2. Hacer múltiples requests rápidos al chat
3. ¿El guard bloquea correctamente o se pasan requests de más por la persistencia asíncrona?

**Impacto potencial**: Consumo de AI credits puede superar el límite asignado por la persistencia asíncrona

---

### BUG-CR-004 — RIESGO A VERIFICAR

**Severidad**: 🟠 Alto
**Repo**: gateway (PHP)
**Archivo**: [FeatureGuard.php](file:///c:/Users/STEVE/Desktop/Automation/gateway/app/Services/Billing/FeatureGuard.php#L31-L55)

**Descripción**: El `FeatureGuard.php` implementa la misma lógica de bloqueo que el Guard Go, pero **no aplica lazy resets**. El Go guard en `isBlocked` llama `resetDue` y si una ventana está vencida la ignora (L49-52 de consumption_guard.go), pero el PHP guard tiene la misma lógica de skip (L46-48). Sin embargo, el PHP guard NO persiste el reset — solo lo ignora. Esto podría llevar a inconsistencias si el guard PHP es la primera consulta después de un ciclo vencido: la fila sigue con `consumed` viejo en BD aunque el guard la ignora.

**Evidencia**:
```php
// L46-48 de FeatureGuard.php
if ($row->reset_at !== null && $row->period_unit !== null && $row->reset_at->lte($now)) {
    continue;  // Skip — but does NOT persist the reset
}
```

**Escenario para verificar**:
1. Feature con reset_at vencido (pasó la fecha del ciclo)
2. Primer acceso es vía gateway PHP (IonMind endpoint)
3. PHP guard permite la acción (correcto) pero no persiste el reset
4. Siguiente acceso vía Go → ¿el lazy reset se aplica correctamente?

**Impacto potencial**: Inconsistencia temporal si PHP es el único gateway consultado — bajo riesgo porque el Go guard eventualmente aplica el reset, pero podría generar emails con porcentajes incorrectos

---

### BUG-CR-005 — RIESGO A VERIFICAR

**Severidad**: 🟠 Alto
**Repo**: flow_binaries
**Archivo**: [admin_service.go](file:///c:/Users/STEVE/Desktop/Automation/flow_binaries/backend/ion/services/subscription/admin_service.go#L164-L208)

**Descripción**: `AdminAssignPlan` limpia `stripe_subscription_id`, `pending_plan_id`, `renews_at`, `canceled_at` y `expires_at` (todo a nil). Luego ejecuta `SyncConsumptions`. Sin embargo, `SyncConsumptions` usa `upsertConsumptionWindow` que solo actualiza `available` en filas existentes (L161-164 de consumption_sync.go) — **no resetea `consumed` a 0**. Si una company tenía un plan `free` con 1000 seg y consumió 800, y el admin la cambia a plan `go` con 10000 seg, la fila de consumo se actualiza a `available=10000` pero `consumed=800` persiste.

**Evidencia**:
```go
// L161-164 de consumption_sync.go
return database.MAIN_DB.
    Model(&models.FeatureConsumption{}).
    Where("id = ?", existing.ID).
    Update("available", available).Error
```

**Escenario para verificar**:
1. Company con plan free: `execution_time consumed=800, available=1000`
2. Admin asigna plan go: `available` cambia a 10000
3. Verificar BD: ¿`consumed` sigue en 800 o se reseteó a 0?
4. Si consumed=800 persiste, ¿es comportamiento intencional? (el saldo usado se mantiene entre plan changes)

**Impacto potencial**: El consumo acumulado anterior podría persistir entre cambios de plan — verificar si es diseño intencional o si debería resetearse

---

### BUG-CR-006 — RIESGO A VERIFICAR

**Severidad**: 🟡 Medio
**Repo**: flow_binaries
**Archivo**: [consumption_guard.go](file:///c:/Users/STEVE/Desktop/Automation/flow_binaries/backend/ion/services/consumption_guard.go#L22)

**Descripción**: `consumptionLocks` usa `sync.Map` como lock pool in-process. Este mecanismo solo protege contra races dentro del mismo proceso Go. Si hay múltiples réplicas del backend, las races cross-replica se manejan con el `WHERE reset_at = ?` optimistic locking de `applyLazyReset`. El código documenta esto correctamente (L21), pero en un escenario de alta concurrencia con múltiples réplicas, podría haber writes perdidos si dos réplicas intentan `incrementConsumed` simultáneamente.

**Evidencia**:
```go
// L21-22 de consumption_guard.go
// In-process only; cross-replica races are settled by the guarded UPDATE in applyLazyReset.
var consumptionLocks sync.Map
```

**Escenario para verificar**: Documentar como riesgo conocido — no es un bug sino una limitación de arquitectura para entorno single-replica

---

## Impacto Cruzado

| Módulo Impactado | Componente Afectado | Riesgo | Verificación Necesaria |
|---|---|---|---|
| **Executions** | Guard bloquea ejecuciones en editor y live | 🔴 Crítico | TC-030, TC-031: verificar que el guard se ejecuta antes de Board.Execute y Engine.Run |
| **Boards** | Schedules/webhooks siguen activos cuando execution_time bloqueado | 🟠 Alto | TC-032, TC-092, TC-093: verificar que schedules no se eliminan |
| **PDF Templates** | Guard en `pdf_templates` y `pdf_impressions` | 🟠 Alto | TC-033, TC-034, TC-094 |
| **IonMind (AI)** | FeatureGuard.php bloquea endpoints IonMind + SSE message en flow-pilot | 🔴 Crítico | TC-110, TC-111: verificar guard + mensaje amigable |
| **Chat (flow-pilot)** | RecordConsumption asíncrono de ai_credits | 🟠 Alto | BUG-CR-003: race condition potencial |

---

## TCs Inyectados en Test Matrix

| TC ID | Origen | Caso de Test | Severidad |
|-------|--------|-------------|-----------|
| TC-CR-001 | BUG-CR-001 | Company nueva: primer request después de auto-provisioning de suscripción free — ¿guard bloquea o permite? | 🟠 Alto |
| TC-CR-002 | BUG-CR-003 | AI credits race condition: múltiples requests rápidos al chat con créditos casi agotados — ¿se pasan del límite? | 🟠 Alto |
| TC-CR-003 | BUG-CR-004 | PHP guard vs Go guard: reset_at vencido consultado primero por PHP (IonMind) y luego por Go — ¿lazy reset se aplica? | 🟠 Alto |
| TC-CR-004 | BUG-CR-005 | Admin cambia plan: ¿consumed persiste o se resetea? Verificar BD antes y después del plan change | 🟠 Alto |
| TC-CR-005 | BUG-CR-002 | Feature con ventana diaria: ¿se genera email al 80%? O solo aplica a month/year | 🟡 Medio |

---

## Observaciones Positivas

1. **Guard fail-open correcto**: Tanto en Go (`return nil` en error, L67-68, L77-78) como en PHP (`return` en feature not found, L18-19) — alineado con AC-30
2. **Optimistic locking en lazy reset**: `WHERE id = ? AND reset_at = ?` (L170) garantiza que solo un writer gana — bien diseñado para multi-replica
3. **Deduplicación de emails**: `alreadyNotified` (L122-133) busca desde `sub.UpdatedAt` — correcto para evitar spam
4. **AI credits SSE message**: `respondIfAICreditsBlocked` (L298-318) envía stream event con mensaje amigable antes de cerrar — alineado con AC-B09
5. **AdminAssignPlan transaccional**: Limpia todos los campos Stripe, ejecuta SyncConsumptions, y registra audit trail — bien orquestado
6. **Tests unitarios existentes**: consumption_guard_test.go, consumption_service_test.go, consumption_billing_test.go, subscription_test.go — cobertura de unit tests razonable
