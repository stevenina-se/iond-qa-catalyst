# AC Consolidados — IONF-1056-B (Zero-Stripe)
> Módulo: billing (nuevo)
> Generado: 2026-06-14
> **Reconsiderado: 2026-07-23** — Pivot a IONF-1056-B (variante zero-Stripe)
> Fuente: ac-reconciliation.md + risk-triage.md + Comentario Enrique 15-Jul (IONF-1056-B)
> Sin code review (Opción B — Paso 3.5 saltado)
> Aprobado por QA Engineer: ✅

---

## Criterio de escritura

Cada AC está redactado como una **sugerencia verificable**, con su fuente y prioridad de testing.  
Las preguntas abiertas (P-01) quedan marcadas como **⚠️ PENDIENTE** — deben resolverse con el Developer antes de la fase de testing.

> **NOTA SOBRE EL PIVOT A IONF-1056-B**: El branch IONF-1056-B elimina toda la integración Stripe (checkout, portal, webhooks, overage, meter events, cancel/resume). Los ACs relacionados a Stripe/Overage están marcados como **N/A — IONF-1056-B** y no forman parte de la matriz de testeo activa.
> La pregunta abierta **P-02** (cron vs lazy) se considera **resuelta**: el design doc de IONF-1056-B confirma explícitamente que los resets son lazy.

---

## BLOQUE 1 — Suscripción y Provisioning

| ID | Acceptance Criteria | Verificable por | Fuente | Prioridad |
|----|---------------------|-----------------|--------|-----------|
| AC-01 | Al crear una nueva company, el sistema le provisiona automáticamente una suscripción con plan `free` | BD: `SELECT * FROM subscriptions WHERE subscriber_type='company' AND subscriber_id=<id>` | Comentario Enrique 12-jun | 🔴 Crítico |
| AC-02 | Solo existe una suscripción activa por company | BD: `SELECT COUNT(*) FROM subscriptions WHERE subscriber_type='company' AND subscriber_id=<id>` = 1 | Prototipo | 🔴 Crítico |
| AC-03 | El estado de la suscripción se deriva de timestamps — no existe columna `status` | BD: verificar que la tabla `subscriptions` no tiene columna `status`; el estado se calcula | Prototipo + Enrique 12-jun | 🟠 Alto |
| ~~AC-04~~ | ~~`POST /checkout-session` solo funciona para la primera suscripción — devuelve 409 si ya existe~~ | ~~API: intentar segunda checkout session → esperar 409~~ | ~~Prototipo~~ | **N/A — IONF-1056-B**: endpoint eliminado |
| AC-05 | La entidad de cobro puede ser company o user (billing owner flexible) | BD: `subscriber_type` puede ser `company` o `user` | Descripción original | 🟡 Medio |

### ACs NUEVOS — Admin Assignment (IONF-1056-B)

| ID | Acceptance Criteria | Verificable por | Fuente | Prioridad |
|----|---------------------|-----------------|--------|-----------|
| AC-B01 | Admin puede asignar plan a una company vía Admin → Companies → Subscription tab. La asignación aplica **inmediatamente** sin checkout ni pago | UI Admin: asignar plan → verificar cambio inmediato en BD | QA Instructions IONF-1056-B | 🔴 Crítico |
| AC-B02 | Al asignar plan vía admin, `feature_consumptions` se re-sincroniza automáticamente con las windows del nuevo plan | BD: verificar que las filas de `feature_consumptions` reflejan el nuevo plan | QA Instructions IONF-1056-B #1 | 🔴 Crítico |
| AC-B03 | La asignación admin genera una fila en `subscription_renewals` con `event='admin_assigned'` | BD: `SELECT * FROM subscription_renewals WHERE subscription_id=<id> ORDER BY created_at DESC LIMIT 1` → `event='admin_assigned'` | QA Instructions IONF-1056-B #10 | 🟠 Alto |
| AC-B04 | Si la company no tenía suscripción previa, se crea una nueva y se asigna el plan en un solo paso | BD: verificar que tanto `subscriptions` como `feature_consumptions` existen después de la primera asignación | QA Instructions IONF-1056-B #10 | 🔴 Crítico |
| AC-B05 | El botón "Assign plan" está deshabilitado hasta que el admin seleccione un plan diferente al actual | UI: verificar estado disabled del botón con el plan actual seleccionado | QA Instructions IONF-1056-B #10 | 🟠 Alto |
| AC-B06 | La asignación admin limpia `stripe_subscription_id` localmente (nota: NO cancela en Stripe — comportamiento intencional) | BD: `SELECT stripe_subscription_id FROM subscriptions WHERE subscriber_id=<id>` → NULL después de admin assign | QA Instructions IONF-1056-B #10 | 🟠 Alto |

---

## BLOQUE 2 — Estados de Suscripción y Ciclo de Vida Stripe

> **⚠️ BLOQUE COMPLETO N/A — IONF-1056-B**
> Toda la lógica de ciclo de vida Stripe (webhooks, cancel/resume, dunning, payment_succeeded/failed, subscription.deleted) fue eliminada del branch IONF-1056-B. Los siguientes ACs quedan archivados para referencia futura cuando se reintegre Stripe.

| ID | Acceptance Criteria | Estado | Motivo |
|----|---------------------|--------|--------|
| ~~AC-06~~ | Estado Active derivado de timestamps | **N/A — IONF-1056-B** | Sin webhooks Stripe |
| ~~AC-07~~ | Cancelación setea timestamps | **N/A — IONF-1056-B** | `POST /subscription/cancel` eliminado |
| ~~AC-08~~ | Dunning derivado de timestamps | **N/A — IONF-1056-B** | Sin webhook `payment_failed` |
| ~~AC-09~~ | Suscripción caducada | **N/A — IONF-1056-B** | Sin webhook `subscription.deleted` |
| ~~AC-10~~ | `payment_succeeded` no mueve `renews_at` por overage | **N/A — IONF-1056-B** | Sin webhooks |
| ~~AC-11~~ | `payment_succeeded` no deshace cancelación | **N/A — IONF-1056-B** | Sin webhooks |
| ~~AC-12~~ | `payment_failed` revoca overage | **N/A — IONF-1056-B** | Sin webhooks ni overage |
| ~~AC-13~~ | `subscription.deleted` → DowngradeToFree | **N/A — IONF-1056-B** | Sin webhooks |
| ~~AC-14~~ | `POST /subscription/cancel` | **N/A — IONF-1056-B** | Endpoint eliminado |
| ~~AC-15~~ | `POST /subscription/resume` | **N/A — IONF-1056-B** | Endpoint eliminado |

---

## BLOQUE 3 — Consumo y Ventanas (feature_consumptions)

| ID | Acceptance Criteria | Verificable por | Fuente | Prioridad |
|----|---------------------|-----------------|--------|-----------|
| AC-16 | Una feature puede tener múltiples ventanas simultáneas (ej. mensual + diaria) — cada una es una fila en `feature_consumptions` | BD: múltiples filas con mismo `feature_id` y `subscriber_id` distintas en `measure` | Prototipo + Enrique 12-jun | 🔴 Crítico |
| AC-17 | Una feature se bloquea (`blocked = true`) si **cualquier** ventana se agota, incluso si otras ventanas tienen saldo disponible | BD: `blocked = true` cuando diaria agotada aunque mensual tenga saldo | Prototipo | 🔴 Crítico |
| AC-18 | `available = -1` → ilimitado: nunca bloquea, nunca genera evento de overage en Stripe | Guard: verificar que el guard siempre retorna ALLOW | Prototipo | 🔴 Crítico |
| AC-19 | `available = 0` → siempre bloqueado, aunque `consumed = 0` | BD: `blocked = true` con `available=0 consumed=0`; guard retorna BLOCK | Prototipo | 🟠 Alto |
| AC-20 | Lazy reset: cuando `reset_at` ha pasado y se ejecuta `RecordConsumption`, el `consumed` resultante es igual a `qty` (no `consumed_anterior + qty`) | BD: después del reset, `consumed = qty` exactamente | Prototipo | 🔴 Crítico |
| AC-21 | El anchor del lazy reset avanza desde el anchor **anterior** (no desde `now`) — mantiene alineación con la fecha del ciclo | BD: `reset_at` = anchor_anterior + period, no = now + period | Prototipo | 🟠 Alto |
| AC-22 | `GET /subscription/usage` persiste los resets lazy — si una fila está vencida, la consulta la resetea y devuelve `consumed = 0` | API: llamar usage con fila vencida → verificar `consumed = 0` y nuevo `reset_at` en BD | Prototipo | 🟠 Alto |
| AC-23 | `period_unit = NULL` → ventana absoluta que nunca se reinicia (`reset_at = NULL`) | BD: `reset_at IS NULL` en ventanas absolutas (ej. `pdf_templates`) | Prototipo | 🟠 Alto |
| AC-24 | ✅ **RESUELTA (P-02)**: los resets son lazy (no hay cron de billing independiente). El branch IONF-1056-B confirma: "Consumption engine rewrite — lazy period resets (no crons)" | Código: verificar que NO existe cron job activo para resetear consumo | Design doc IONF-1056-B | 🔴 Crítico |

---

## BLOQUE 4 — Enforcement por Tipo de Feature

| ID | Acceptance Criteria | Verificable por | Fuente | Prioridad |
|----|---------------------|-----------------|--------|-----------|
| AC-25 | `execution_time` agotado: bloquea ejecuciones en el **editor** (dev mode) | UI: intentar ejecutar flow en canvas → debe mostrar error/bloqueo | Enrique 09-jun | 🔴 Crítico |
| AC-26 | `execution_time` agotado: bloquea ejecuciones en **live** (production flows) | API: ejecutar flow en producción → debe retornar error de bloqueo | Enrique 09-jun | 🔴 Crítico |
| AC-27 | `execution_time` agotado: los **schedules y webhooks permanecen activos** (no se eliminan) — solo la ejecución del flow termina inmediatamente | BD: registros de schedule/webhook siguen existiendo; log de ejecución muestra error de quota | Enrique 09-jun | 🔴 Crítico |
| AC-28 | `pdf_templates` agotado: bloquea la **creación** de nuevos templates (control en la acción de crear, no mid-execution) | UI/API: intentar crear template → debe bloquearse si quota = 0 | Enrique 09-jun | 🟠 Alto |
| AC-29 | `pdf_impressions` agotado: el **nodo PDF falla inmediatamente** durante la ejecución del flow | Execution log: nodo PDF muestra error de quota; flow queda en estado error | Enrique 09-jun | 🟠 Alto |
| AC-30 | Guard fail-open: si hay un error de infraestructura al consultar el feature, la ejecución **se permite** (no se bloquea por error técnico) | Simular error de BD → ejecución debe continuar | Prototipo | 🟠 Alto |
| AC-31 | Feature no provisionada para el plan (sin rows): guard retorna **BLOCK** con `ErrQuotaBlocked` (403) | API: acceder a feature fuera del plan → esperar 403 | Prototipo | 🟠 Alto |
| AC-32 | ⚠️ **PENDIENTE (P-01)**: Grace execution — verificar si existe o no. Según descripción: "1 ejecución de gracia antes del bloqueo definitivo". Según comentarios IONF-1058: bloqueo directo. IONF-1056-B no menciona grace execution. | Preguntar a Enrique; testear ambos comportamientos | Contradicción detectada | 🔴 Crítico |

### ACs NUEVOS — Enforcement sin Overage (IONF-1056-B)

| ID | Acceptance Criteria | Verificable por | Fuente | Prioridad |
|----|---------------------|-----------------|--------|-----------|
| AC-B07 | Al agotar saldo sin overage, el sistema bloquea (403) + envía email con mensaje **"contact us"** en vez de sugerir overage | API: consumir hasta agotar → 403; email con texto "contact us" | QA Instructions IONF-1056-B #3 | 🔴 Crítico |
| AC-B08 | Plan `enterprise` sin feature windows configuradas bloquea **todo** hasta que un admin configure windows | Guard: empresa con plan enterprise → BLOCK en todos los features hasta que admin configure `plan_features` | QA Instructions IONF-1056-B #3 | 🔴 Crítico |

### ACs NUEVOS — AI Credits Enforcement (IONF-1056-B)

| ID | Acceptance Criteria | Verificable por | Fuente | Prioridad |
|----|---------------------|-----------------|--------|-----------|
| AC-B09 | Flow-pilot chat consume `ai_credits`. Al agotar, streams SSE con mensaje "reached your AI credits limit" (no error genérico) | UI: usar flow-pilot hasta agotar → verificar mensaje SSE amigable | IONF-1056-B changes + QA Instructions gateway | 🔴 Crítico |
| AC-B10 | Gateway `IonMind` endpoints retornan **403** ("Feature quota exceeded") cuando `ai_credits` está agotado | API: llamar endpoints IonMind con `ai_credits` agotado → 403 | QA Instructions gateway IONF-1056-B #2 | 🔴 Crítico |

---

## BLOQUE 5 — Notificaciones por Email

| ID | Acceptance Criteria | Verificable por | Fuente | Prioridad |
|----|---------------------|-----------------|--------|-----------|
| AC-33 | Al llegar al **80%** de consumo del saldo incluido de un feature, se envía email de warning. **IONF-1056-B: el email dice "contact us" en vez de sugerir overage** | Email recibido con mensaje de 80% + texto "contact us" | Enrique 09-jun + IONF-1056-B changes | 🟠 Alto |
| AC-34 | Al llegar al **100%** de consumo, se envía email informando bloqueo. **IONF-1056-B: sin mención de overage** | Email recibido con mensaje de 100% | Enrique 09-jun + IONF-1056-B | 🟠 Alto |
| AC-35 | Al agotar el saldo: se detienen inmediatamente los recursos y se envía email de bloqueo con "contact us" | Email recibido; ejecuciones bloqueadas | Enrique 09-jun + IONF-1056-B | 🟠 Alto |
| AC-36 | Las notificaciones usan el **layout IonFlow unificado** | Visual: verificar que el email tiene el diseño IonFlow correcto | Enrique 11-jun | 🟡 Medio |
| AC-37 | Las notificaciones se envían **solo por email** — no hay notificaciones in-app | Verificar que no aparecen alertas en UI | Descripción original | 🟡 Medio |
| AC-38 | Los emails se **deduplican desde el último sync** — no se reenvían en cada consumo | Log: solo 1 email por threshold por ciclo | Prototipo | 🟡 Medio |
| AC-39 | ⚠️ Body y template final de emails **por definirse** — testear solo layout/estructura, no copy final | Verificar estructura; ignorar texto provisional | Enrique 11-jun | ℹ️ Pendiente |

---

## BLOQUE 6 — Overage y Stripe Billing Meters

> **⚠️ BLOQUE COMPLETO N/A — IONF-1056-B**
> Todo el concepto de overage (compra, Stripe Billing Meters, meter events, billableDelta, idempotencia) fue eliminado del branch IONF-1056-B. Los siguientes ACs quedan archivados para referencia futura.

| ID | Acceptance Criteria | Estado |
|----|---------------------|--------|
| ~~AC-40~~ | Overage en plan free → 422 | **N/A — IONF-1056-B** |
| ~~AC-41~~ | Overage en dunning → 422 | **N/A — IONF-1056-B** |
| ~~AC-42~~ | Overage en feature ilimitada → 422 | **N/A — IONF-1056-B** |
| ~~AC-43~~ | Overage sin producto Stripe → 422 | **N/A — IONF-1056-B** |
| ~~AC-44~~ | Activación overage: `available = included + units` | **N/A — IONF-1056-B** |
| ~~AC-45~~ | `billableDelta` cálculo | **N/A — IONF-1056-B** |
| ~~AC-46~~ | 6 escenarios de clipping | **N/A — IONF-1056-B** |
| ~~AC-47~~ | Idempotencia meter events | **N/A — IONF-1056-B** |
| ~~AC-48~~ | Invoice overage no modifica `renews_at` | **N/A — IONF-1056-B** |
| ~~AC-49~~ | Pago fallido bloquea overage | **N/A — IONF-1056-B** |
| ~~AC-50~~ | `units=0` detiene meter events | **N/A — IONF-1056-B** |

---

## BLOQUE 7 — IONPDF (Oferta standalone y add-on)

| ID | Acceptance Criteria | Verificable por | Fuente | Prioridad |
|----|---------------------|-----------------|--------|-----------|
| AC-51 | Un cliente puede tener IONPDF **sin** tener IONFLOW. **IONF-1056-B: asignado por admin, no por compra** | Admin UI: asignar plan IONPDF standalone a company sin IONFLOW | Descripción + Marcel 03-jun + IONF-1056-B | 🟠 Alto |
| AC-52 | IONPDF standalone provisiona una bolsa de segundos (menor que la de IONFLOW) | BD: `feature_consumptions` con `execution_time` a una cantidad menor que el plan go de IONFLOW | Descripción + Marcel 03-jun | 🟠 Alto |
| AC-53 | Un cliente con IONFLOW puede tener IONPDF como add-on sin perder su entitlement de IONFLOW. **IONF-1056-B: cambio de plan vía admin** | BD: los `feature_consumptions` de IONFLOW permanecen iguales después de cambiar plan vía admin | Descripción original + IONF-1056-B | 🟠 Alto |
| AC-54 | El consumo de IONPDF (usos, templates, nodos PDF, segundos relacionados) queda registrado en el ledger unificado | BD: `feature_consumption_logs` con dimensiones de IONPDF | Descripción IONF-1060 | 🟠 Alto |
| AC-55 | IONPDF se comporta como motor de **generación documental** — no como OCR | Verificar clasificación en el catálogo de nodos/features | Notas PM | 🟡 Medio |

---

## BLOQUE 8 — Runtime History (IONF-1057)

| ID | Acceptance Criteria | Verificable por | Fuente | Prioridad |
|----|---------------------|-----------------|--------|-----------|
| AC-56 | Cada ejecución completada registra `active_seconds`, `idle_seconds` y `units_consumed` | BD/API: consultar datos de ejecución reciente | Enrique 08-jun | 🟠 Alto |
| AC-57 | El tiempo idle incluye: Nodo Timer completado correctamente + subflow con `waitForResponse` activado | Ejecutar flow con Timer y subflow → verificar idle_seconds > 0 | Enrique 08-jun | 🟠 Alto |
| AC-58 | ⚠️ Visualización en Board **pendiente** por rediseño de UI — verificar vía API hasta que esté disponible | API: endpoint que devuelva última duración de ejecución | Enrique 08-jun | ⏳ Bloqueado |
| AC-59 | ⚠️ Fallback "estado neutro" cuando no hay ejecuciones previas — **no confirmado** en comentarios | Testear flow sin ejecuciones; verificar que no inventa un valor | Descripción IONF-1057 | 🟡 Medio |

---

## BLOQUE 9 — Regresión en Módulos Existentes

| ID | Acceptance Criteria | Módulo | Prioridad |
|----|---------------------|--------|-----------|
| AC-60 | Los flows con saldo de `execution_time` disponible ejecutan correctamente tras activar billing | Executions | 🔴 Crítico |
| AC-61 | El historial de ejecuciones (`/executions`) sigue mostrando ejecuciones correctamente tras activar billing | Executions | 🔴 Crítico |
| AC-62 | Los boards con schedules y webhooks configurados **no pierden** su configuración cuando `execution_time` se agota | Boards | 🟠 Alto |
| AC-63 | La creación de PDF templates sigue funcionando correctamente para usuarios con `pdf_templates` disponible | PDF Templates | 🟠 Alto |
| AC-64 | Los templates existentes de PDF no se ven afectados por el límite de `pdf_templates` (solo afecta creación de nuevos) | PDF Templates | 🟠 Alto |

---

## BLOQUE 10 — Tenant UI Read-Only y Admin Catalog (IONF-1056-B)

| ID | Acceptance Criteria | Verificable por | Fuente | Prioridad |
|----|---------------------|-----------------|--------|-----------|
| AC-B11 | Tenant `/billing/plans` muestra pricing cards read-only con precios seeded localmente — **sin botones de compra/upgrade** | UI: verificar que no existen acciones de purchase/checkout | QA Instructions IONF-1056-B #2 | 🟠 Alto |
| AC-B12 | Tenant `/billing/subscription` muestra plan actual y usage bars — **sin cancel/resume/overage UI** | UI: verificar que no aparecen acciones de cancel, resume ni overage | QA Instructions IONF-1056-B #2 | 🟠 Alto |
| AC-B13 | Admin `Products.vue` es read-only — sin botón de Stripe sync, sin `stripe_id` visible | UI Admin: verificar catálogo local sin referencias a Stripe | IONF-1056-B changes | 🟡 Medio |
| AC-B14 | `ProductSeeder` crea un producto local por plan con `data.prices` seeded y `provider='local'` | BD: `SELECT provider FROM products` → todos 'local' | Design doc IONF-1056-B | 🟠 Alto |

---

## BLOQUE 11 — Verificación Residual Stripe (IONF-1056-B)

| ID | Acceptance Criteria | Verificable por | Fuente | Prioridad |
|----|---------------------|-----------------|--------|-----------|
| AC-B15 | `grep -ri stripe` en flow_binaries Go code solo encuentra mappings de columna dormidos — **no hay llamadas SDK activas** | CLI: `grep -ri stripe` sobre el directorio flow_binaries → sin imports ni llamadas SDK | QA Instructions IONF-1056-B #4 | 🟠 Alto |

---

## Preguntas abiertas que bloquean AC específicos

> Deben resolverse con el Developer antes de testear los AC marcados con ⚠️

| Pregunta | AC bloqueado | Urgencia | Estado |
|----------|-------------|----------|--------|
| P-01: ¿Grace execution implementada o descartada? | AC-32 | 🔴 Urgente | ⚠️ Pendiente |
| ~~P-02: ¿Cron job o lazy reset?~~ | ~~AC-24~~ | ~~🔴 Urgente~~ | ✅ Resuelta — lazy (IONF-1056-B confirma) |
| P-03: ¿Qué mensaje ve el usuario en UI al bloquear execution_time? | AC-25, AC-26 | 🟠 Alto | ⚠️ Pendiente |
| P-04: ¿Existe endpoint API para consultar última duración? | AC-58 | 🟠 Alto | ⚠️ Pendiente |

---

## Conteo de AC por bloque y prioridad — IONF-1056-B

| Bloque | Total AC activos | 🔴 Crítico | 🟠 Alto | 🟡 Medio | Bloqueados/Pendientes |
|--------|-----------------|-----------|--------|---------|----------------------|
| Suscripción, Provisioning y Admin Assignment | 10 | 4 | 4 | 1 | 0 |
| ~~Ciclo de Vida Stripe~~ | ~~0~~ (N/A) | — | — | — | — |
| Consumo y Ventanas | 9 | 4 | 4 | 0 | 0 (P-02 resuelta) |
| Enforcement + Sin Overage + AI Credits | 12 | 7 | 3 | 0 | 1 (P-01) |
| Notificaciones | 7 | 0 | 3 | 3 | 1 (AC-39 pendiente) |
| ~~Overage y Stripe~~ | ~~0~~ (N/A) | — | — | — | — |
| IONPDF | 5 | 0 | 4 | 1 | 0 |
| Runtime History | 4 | 0 | 2 | 1 | 1 (AC-58 bloqueado) |
| Regresión | 5 | 2 | 3 | 0 | 0 |
| Tenant UI Read-Only y Admin Catalog | 4 | 0 | 3 | 1 | 0 |
| Verificación Residual Stripe | 1 | 0 | 1 | 0 | 0 |
| **TOTAL** | **57** | **17** | **27** | **7** | **3** |

> **Comparativa**: Original 64 ACs activos → IONF-1056-B **57 ACs activos** (-7 netos: -21 eliminados por Stripe, +14 nuevos por IONF-1056-B)
