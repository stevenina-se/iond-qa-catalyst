# Test Matrix — IONF-1056-B (Zero-Stripe)
> Módulo: billing (nuevo)
> Generado: 2026-06-14
> **Reconsiderado: 2026-07-23** — Pivot a IONF-1056-B (variante zero-Stripe)
> Basado en: ac-consolidated.md (reconsiderado) + risk-triage.md + QA Instructions IONF-1056-B
> Aprobado por QA Engineer: ✅ (Gate 5 — reconsideración)

---

## Convenciones

| Campo | Valores posibles |
|-------|-----------------|
| Tipo | `HP` Happy Path · `EC` Edge Case · `NEG` Negativo · `REG` Regresión |
| Prioridad | 🔴 Crítico · 🟠 Alto · 🟡 Medio |
| Estado | ⬜ Pendiente · 🔄 En ejecución · ✅ Pass · ❌ Fail · ⏸ Bloqueado |

> **NOTA**: Esta matriz refleja el branch **IONF-1056-B** (zero-Stripe). Las suites de Ciclo de Vida Stripe (Suite 2 original) y Overage/Stripe Billing Meters (Suite 6 original) fueron **eliminadas completamente**. Se agregaron suites nuevas para Admin Assignment, Guard sin Overage, AI Credits, Tenant UI Read-Only, Admin Catalog y Verificación Residual de Stripe.

---

## SUITE 1 — Suscripción y Provisioning

| TC-ID | Tipo | Caso de prueba | Pasos | AC | Prioridad | Estado |
|-------|------|----------------|-------|----|-----------|--------|
| TC-001 | HP | Plan free se aprovisiona automáticamente al crear company | 1. Crear nueva company vía API o UI<br>2. Verificar BD: `SELECT * FROM subscriptions WHERE subscriber_type='company' AND subscriber_id=<id>`<br>3. Verificar que `plan_id` corresponde al plan free<br>4. Verificar que `feature_consumptions` tiene filas para los features del plan free | AC-01 | 🔴 | ⬜ |
| TC-003 | EC | Solo existe 1 suscripción por company | 1. Verificar BD: `SELECT COUNT(*) FROM subscriptions WHERE subscriber_type='company' AND subscriber_id=<id>`<br>2. Resultado debe ser exactamente `1` | AC-02 | 🔴 | ⬜ |
| TC-004 | NEG | No existe columna `status` en tabla subscriptions | 1. Consultar BD: `SELECT column_name FROM information_schema.columns WHERE table_name='subscriptions'`<br>2. Verificar que `status` NO aparece en la lista | AC-03 | 🟠 | ⬜ |
| TC-005 | HP | Billing owner puede ser company | 1. Verificar BD: `SELECT subscriber_type FROM subscriptions WHERE subscriber_id=<company_id>`<br>2. Resultado: `'company'` | AC-05 | 🟡 | ⬜ |

---

## SUITE 2 — Admin Assignment y Plan Grant (NUEVA)

| TC-ID | Tipo | Caso de prueba | Pasos | AC | Prioridad | Estado |
|-------|------|----------------|-------|----|-----------|--------|
| TC-100 | HP | Admin asigna plan a company — feature_consumptions se re-sincronizan y subscription_renewals tiene fila `admin_assigned` | 1. Admin → Companies → seleccionar company → Subscription tab<br>2. Seleccionar plan diferente al actual (ej. `go`)<br>3. Confirmar asignación<br>4. BD: `SELECT plan_id FROM subscriptions WHERE subscriber_id=<id>` → plan `go`<br>5. BD: `SELECT * FROM feature_consumptions WHERE subscriber_id=<id>` → windows del plan `go`<br>6. BD: `SELECT event FROM subscription_renewals WHERE subscription_id=<id> ORDER BY created_at DESC LIMIT 1` → `admin_assigned` | AC-B01, AC-B02, AC-B03 | 🔴 | ⬜ |
| TC-101 | HP | Admin asigna plan a company sin suscripción previa — crea suscripción y asigna en un paso | 1. Identificar company sin fila en `subscriptions` (o crear nueva company sin acceder a billing)<br>2. Admin → Companies → company → Subscription tab<br>3. Asignar plan `go`<br>4. BD: verificar que se creó la fila en `subscriptions` con `plan_id` = go<br>5. BD: verificar que `feature_consumptions` tiene las windows del plan | AC-B04 | 🔴 | ⬜ |
| TC-102 | EC | Botón "Assign plan" deshabilitado hasta cambiar selección | 1. Admin → Companies → company → Subscription tab<br>2. Verificar que el botón "Assign plan" está deshabilitado con el plan actual seleccionado<br>3. Cambiar selección a otro plan → verificar que el botón se habilita<br>4. Volver al plan actual → verificar que se deshabilita | AC-B05 | 🟠 | ⬜ |
| TC-103 | EC | Asignación admin limpia `stripe_subscription_id` local | 1. Company con `stripe_subscription_id` NOT NULL (si existe)<br>2. Admin asigna nuevo plan<br>3. BD: `SELECT stripe_subscription_id FROM subscriptions WHERE subscriber_id=<id>` → NULL<br>4. **Nota**: esto NO cancela la suscripción en Stripe — verificar que es comportamiento intencional | AC-B06 | 🟠 | ⬜ |
| TC-113 | HP | Asignación admin genera fila audit en subscription_renewals | 1. Admin asigna plan a company<br>2. BD: `SELECT * FROM subscription_renewals WHERE subscription_id=<id> ORDER BY created_at DESC LIMIT 1`<br>3. Verificar: `event = 'admin_assigned'` con datos de periodo correctos | AC-B03 | 🟠 | ⬜ |

---

## SUITE 3 — Consumo y Ventanas (feature_consumptions)

| TC-ID | Tipo | Caso de prueba | Pasos | AC | Prioridad | Estado |
|-------|------|----------------|-------|----|-----------|--------|
| TC-020 | HP | Feature con múltiples ventanas: mensual + diaria simultáneas | 1. BD: `SELECT measure, available, consumed, reset_at FROM feature_consumptions WHERE subscriber_id=<id> AND feature_id=<pdf_impressions_id>`<br>2. Verificar que existen al menos 2 filas: una con `measure='monthly'` y otra con `measure='daily'` | AC-16 | 🔴 | ⬜ |
| TC-021 | EC | Ventana diaria agotada bloquea aunque ventana mensual tenga saldo | 1. Consumir manualmente hasta agotar el diario de `pdf_impressions`<br>2. BD: verificar `blocked=true` en fila daily, `blocked=false` en fila monthly<br>3. Intentar usar nodo PDF → debe fallar (fila daily bloquea) | AC-17 | 🔴 | ⬜ |
| TC-022 | HP | `-1` en `available` nunca bloquea | 1. BD: `SELECT blocked FROM feature_consumptions WHERE available=-1`<br>2. Verificar: `blocked=false` en todas las filas con `available=-1`<br>3. Consumir feature ilimitada → ejecución no se bloquea | AC-18 | 🔴 | ⬜ |
| TC-023 | EC | `available=0` bloquea aunque `consumed=0` | 1. BD: forzar fila con `available=0, consumed=0` (ej. feature enterprise sin configurar)<br>2. BD: verificar que `blocked=true` (columna generada)<br>3. Intentar usar feature → debe retornar 403 | AC-19 | 🟠 | ⬜ |
| TC-024 | EC | Lazy reset: `consumed` arranca en `qty`, no en `consumed_anterior + qty` | 1. Tomar feature con `reset_at` en el pasado y `consumed > 0`<br>2. Ejecutar consumo de `qty = 5` unidades<br>3. BD: `SELECT consumed, reset_at FROM feature_consumptions WHERE id=<fc_id>`<br>4. Verificar: `consumed = 5` (no `consumed_anterior + 5`)<br>5. Verificar: `reset_at` avanzó desde anchor anterior | AC-20 | 🔴 | ⬜ |
| TC-025 | EC | Anchor lattice: `reset_at` avanza desde anchor anterior, no desde `now` | 1. Feature con `reset_at = 15-May` (anchor) y hoy = 03-Jul<br>2. Triggear consumo<br>3. BD: `SELECT reset_at FROM feature_consumptions WHERE id=<fc_id>`<br>4. Verificar: `reset_at = 15-Jul` (no `03-Jul + 1 mes`) | AC-21 | 🟠 | ⬜ |
| TC-026 | HP | `GET /subscription/usage` persiste lazy reset y devuelve `consumed=0` | 1. Feature con `reset_at` vencida y `consumed > 0`<br>2. `GET /api/1.0/tenants/{id}/subscription/usage`<br>3. Verificar en response: `consumed = 0` y nuevo `reset_at`<br>4. BD: confirmar que el reset quedó persistido | AC-22 | 🟠 | ⬜ |
| TC-027 | HP | Ventana absoluta (`period_unit=NULL`): `reset_at=NULL`, nunca se reinicia | 1. BD: `SELECT reset_at FROM feature_consumptions WHERE feature_id=<pdf_templates_id>`<br>2. Verificar: `reset_at IS NULL` | AC-23 | 🟠 | ⬜ |
| TC-028 | EC | Verificar que NO existe cron de billing — resets son lazy (P-02 resuelta) | 1. Verificar en código/configuración del servidor que no existe cron job para `reset_at` o consumos<br>2. Avanzar `reset_at` manualmente en BD a una fecha pasada<br>3. Verificar que el reset NO ocurre hasta que un consumo o lectura lo triggerea<br>4. Ejecutar consumo → verificar que el lazy reset se aplica en ese momento | AC-24 | 🔴 | ⬜ |

---

## SUITE 4 — Enforcement por Tipo de Feature

| TC-ID | Tipo | Caso de prueba | Pasos | AC | Prioridad | Estado |
|-------|------|----------------|-------|----|-----------|--------|
| TC-030 | HP | `execution_time` agotado: bloquea ejecución en editor (dev mode) | 1. Configurar company con `execution_time` agotado (`consumed >= available`)<br>2. Boards > [Flow] > Canvas editor > Ejecutar manualmente [Run]<br>3. Verificar: ejecución no inicia o termina inmediatamente con mensaje de error<br>4. Execution History > verificar log de error de quota | AC-25 | 🔴 | ⬜ |
| TC-031 | HP | `execution_time` agotado: bloquea ejecución en live (production) | 1. Flow en modo Production con `execution_time` agotado<br>2. Triggear vía webhook o schedule<br>3. Execution History > verificar que ejecución termina con error de quota (no queda en running) | AC-26 | 🔴 | ⬜ |
| TC-032 | EC | `execution_time` agotado: schedules y webhooks NO se eliminan | 1. Flow con schedule/webhook configurado + `execution_time` agotado<br>2. Boards > [Flow] > Verificar que el schedule sigue configurado<br>3. BD: `SELECT * FROM schedules WHERE flow_id=<id>` → fila existe<br>4. Webhook endpoint sigue respondiendo (no 404) | AC-27 | 🔴 | ⬜ |
| TC-033 | HP | `pdf_templates` quota agotada: bloquea creación de nuevo template | 1. Company con `pdf_templates.consumed >= pdf_templates.available`<br>2. PDF Templates > [New Template] > Intentar crear<br>3. Verificar: acción bloqueada con mensaje de error de quota<br>4. BD: count de templates no aumentó | AC-28 | 🟠 | ⬜ |
| TC-034 | EC | `pdf_impressions` agotado: nodo PDF falla mid-execution | 1. Company con `pdf_impressions.consumed >= pdf_impressions.available`<br>2. Ejecutar flow que contiene nodo PDF<br>3. Execution History > Log del nodo PDF > verificar error de quota<br>4. Verificar estado del flow: `error` (no `completed`) | AC-29 | 🟠 | ⬜ |
| TC-035 | EC | Guard fail-open: error de infra permite ejecución | 1. Simular error de conexión a BD en el guard (o feature lookup fallido)<br>2. Intentar ejecución del flow<br>3. Verificar: ejecución procede (no bloquea por error técnico) | AC-30 | 🟠 | ⬜ |
| TC-036 | NEG | Feature no provisionada en el plan: guard retorna 403 | 1. Company con feature fuera de su plan (ej. plan free intentando usar feature enterprise)<br>2. Intentar ejecución que usa esa feature<br>3. Verificar: respuesta `403` con `ErrQuotaBlocked` | AC-31 | 🟠 | ⬜ |
| TC-037 | EC | ⚠️ BLOQUEADO P-01: Grace execution | Pendiente confirmación con Enrique. Cuando se resuelva: Si existe → testear que se permite 1 ejecución adicional al llegar a 100%. Si no existe → documentar como comportamiento intencional (bloqueo directo). | AC-32 | 🔴 | ⏸ |

---

## SUITE 5 — Guard sin Overage y Enterprise Block (NUEVA)

| TC-ID | Tipo | Caso de prueba | Pasos | AC | Prioridad | Estado |
|-------|------|----------------|-------|----|-----------|--------|
| TC-106 | HP | Consumo supera cap → guard 403 + email "contact us" — sin meter event | 1. Company con plan `go` y `execution_time` casi agotado<br>2. Ejecutar flow que supere el saldo restante<br>3. Verificar: guard retorna 403 (hard block)<br>4. Verificar email: recibido con mensaje "contact us" (no sugiere overage)<br>5. BD/Logs: verificar que NO se generó ningún meter event de Stripe<br>6. Siguiente ejecución → sigue bloqueada (sin grace) | AC-B07 | 🔴 | ⬜ |
| TC-108 | EC | Plan enterprise sin windows configuradas — guard bloquea todo | 1. Admin asigna plan `enterprise` a una company<br>2. Verificar BD: `SELECT * FROM feature_consumptions WHERE subscriber_id=<id>` → sin filas (o filas con `available=0`)<br>3. Intentar ejecutar cualquier flow → guard retorna 403<br>4. Admin configura `plan_features` para enterprise con windows<br>5. Ejecutar `SyncConsumptions` (o reasignar plan)<br>6. Verificar: ahora las ejecuciones proceden | AC-B08 | 🔴 | ⬜ |

---

## SUITE 6 — AI Credits Enforcement (NUEVA)

| TC-ID | Tipo | Caso de prueba | Pasos | AC | Prioridad | Estado |
|-------|------|----------------|-------|----|-----------|--------|
| TC-110 | HP | Flow-pilot chat consume `ai_credits` — al agotar, streams SSE "reached your AI credits limit" | 1. Company con `ai_credits` casi agotado (ej. available=100, consumed=95)<br>2. Usar flow-pilot chat en el editor<br>3. Verificar: cada uso decrementa `ai_credits` consumed en BD<br>4. Agotar créditos completamente<br>5. Intentar usar flow-pilot → verificar: stream SSE con mensaje amigable "reached your AI credits limit" (no error genérico) | AC-B09 | 🔴 | ⬜ |
| TC-111 | NEG | Gateway IonMind endpoints retornan 403 al agotar `ai_credits` | 1. Company con `ai_credits` agotado (`consumed >= available`)<br>2. Llamar a cualquier endpoint de `IonMindController` en gateway<br>3. Verificar: respuesta 403 con mensaje "Feature quota exceeded"<br>4. Verificar: el AI chat se comporta de acuerdo (no hace llamadas al proveedor AI) | AC-B10 | 🔴 | ⬜ |

---

## SUITE 7 — Notificaciones por Email

| TC-ID | Tipo | Caso de prueba | Pasos | AC | Prioridad | Estado |
|-------|------|----------------|-------|----|-----------|--------|
| TC-040 | HP | Email de warning al 80% de consumo — texto "contact us" | 1. Consumir hasta llegar al 80% del saldo de `execution_time`<br>2. Verificar inbox: email recibido con mensaje de 80%<br>3. **IONF-1056-B**: verificar que el texto dice "contact us" (NO sugiere activar overage) | AC-33 | 🟠 | ⬜ |
| TC-041 | HP | Email de warning al 100% de consumo — sin mención de overage | 1. Consumir hasta llegar al 100% del saldo<br>2. Verificar inbox: email recibido con mensaje de 100%<br>3. **IONF-1056-B**: verificar que NO menciona overage | AC-34 | 🟠 | ⬜ |
| TC-042 | HP | Email de bloqueo al agotar saldo — "contact us" | 1. Company con saldo agotado y ejecución bloqueada<br>2. Verificar inbox: email de bloqueo recibido con "contact us"<br>3. Verificar: ejecuciones bloqueadas | AC-35 | 🟠 | ⬜ |
| TC-043 | HP | Layout de email usa diseño IonFlow unificado | 1. Triggear cualquier email de notificación de billing<br>2. Verificar visualmente: logo IonFlow, tipografía, colores, footer | AC-36 | 🟡 | ⬜ |
| TC-044 | NEG | No se generan notificaciones in-app (solo email) | 1. Consumir hasta 80%, 100% y agotamiento<br>2. Verificar UI de gateway-ion: no aparecen toasts, banners ni alertas de billing<br>3. Solo el inbox recibe las notificaciones | AC-37 | 🟡 | ⬜ |
| TC-045 | EC | Deduplicación: no se reenvían múltiples emails por el mismo threshold en el mismo ciclo | 1. Consumir hasta 80% → email recibido<br>2. Consumir más (manteniéndose en el mismo ciclo por encima del 80%)<br>3. Verificar: no llega segundo email de 80%<br>4. BD: solo 1 fila de `notification_80` desde el último sync | AC-38 | 🟡 | ⬜ |

---

## SUITE 8 — IONPDF Standalone y Add-on

| TC-ID | Tipo | Caso de prueba | Pasos | AC | Prioridad | Estado |
|-------|------|----------------|-------|----|-----------|--------|
| TC-070 | HP | Asignación admin de plan IONPDF standalone aprovisiona segundos y capacidades IONPDF | 1. Admin asigna plan IONPDF standalone a company (sin IONFLOW)<br>2. BD: `SELECT available, measure FROM feature_consumptions WHERE subscriber_id=<id>` → debe incluir `execution_time` con valor menor que IONFLOW go<br>3. BD: verificar features de IONPDF (pdf_templates, pdf_impressions) provisionadas | AC-51, AC-52 | 🟠 | ⬜ |
| TC-071 | EC | Cambio de plan vía admin: entitlements de IONFLOW no se modifican | 1. Company con plan IONFLOW activo → anotar `available` de `execution_time`<br>2. Admin cambia plan para agregar IONPDF (o asigna plan que incluya IONPDF add-on)<br>3. BD: `SELECT available FROM feature_consumptions WHERE feature_id=<exec_time_id>`<br>4. Verificar: `available` de IONFLOW sin cambios | AC-53 | 🟠 | ⬜ |
| TC-072 | HP | Consumo de IONPDF queda registrado en ledger unificado | 1. Usar funcionalidad de IONPDF (generar documento desde template)<br>2. BD: `SELECT * FROM feature_consumption_logs WHERE feature_consumption_id IN (SELECT id FROM feature_consumptions WHERE feature_id IN (SELECT id FROM features WHERE slug IN ('pdf_templates','pdf_impressions')))`<br>3. Verificar: logs con dimensiones de IONPDF | AC-54 | 🟠 | ⬜ |
| TC-073 | NEG | IONPDF no aparece clasificado como OCR en el catálogo de features/nodos | 1. Admin > Billing > Features > buscar features relacionadas a IONPDF<br>2. Verificar: descripción y clasificación no menciona "OCR"<br>3. Canvas > Nodos > buscar nodo PDF > verificar categoría | AC-55 | 🟡 | ⬜ |

---

## SUITE 9 — Runtime History (IONF-1057)

| TC-ID | Tipo | Caso de prueba | Pasos | AC | Prioridad | Estado |
|-------|------|----------------|-------|----|-----------|--------|
| TC-080 | HP | Ejecución completada registra active_seconds, idle_seconds y units_consumed | 1. Ejecutar un flow que complete correctamente<br>2. BD/API: consultar datos de la ejecución → verificar campos `active_seconds`, `idle_seconds`, `units_consumed` con valores > 0 | AC-56 | 🟠 | ⬜ |
| TC-081 | EC | Nodo Timer incrementa idle_seconds | 1. Ejecutar flow con nodo Timer (ej. esperar 3 segundos)<br>2. Verificar: `idle_seconds >= 3`<br>3. Verificar: `active_seconds` < tiempo total de ejecución | AC-57 | 🟠 | ⬜ |
| TC-082 | EC | Subflow con `waitForResponse=true` incrementa idle_seconds | 1. Ejecutar flow con subflow usando `waitForResponse`<br>2. Verificar: `idle_seconds` refleja el tiempo de espera del subflow | AC-57 | 🟠 | ⬜ |
| TC-083 | EC | ⚠️ BLOQUEADO: Visualización en Board — pendiente rediseño UI | Pendiente hasta que la vista de Board esté disponible. Verificar vía API mientras tanto: `GET /executions/<id>` → campo de duración | AC-58 | 🟠 | ⏸ |
| TC-084 | EC | Estado neutro cuando no hay ejecuciones previas | 1. Flow recién creado, sin ejecuciones<br>2. Consultar vía API o UI la última duración<br>3. Verificar: no muestra `0s` artificialmente ni valor inventado — muestra estado neutro/vacío | AC-59 | 🟡 | ⬜ |

---

## SUITE 10 — Regresión en Módulos Existentes

| TC-ID | Tipo | Caso de prueba | Pasos | AC | Prioridad | Estado |
|-------|------|----------------|-------|----|-----------|--------|
| TC-090 | REG | Flows con saldo disponible ejecutan correctamente tras activar billing | 1. Company con plan go y saldo de `execution_time` disponible<br>2. Boards > [Flow] > Ejecutar manualmente<br>3. Execution History > verificar ejecución completada exitosamente | AC-60 | 🔴 | ⬜ |
| TC-091 | REG | Historial de ejecuciones (`/executions`) sigue funcionando correctamente | 1. Company > Sidebar: Executions > verificar lista carga<br>2. Clic en una ejecución > verificar detalle con logs por nodo<br>3. Verificar que los datos de duración no interfieren con la vista existente | AC-61 | 🔴 | ⬜ |
| TC-092 | REG | Schedule de un flow no se elimina cuando `execution_time` se agota | 1. Flow con schedule configurado<br>2. Agotar `execution_time`<br>3. Boards > [Flow] > Verificar que el schedule sigue configurado en la UI<br>4. BD: registro de schedule existe | AC-62 | 🟠 | ⬜ |
| TC-093 | REG | Webhook configurado en flow no se elimina cuando `execution_time` se agota | 1. Flow con webhook trigger<br>2. Agotar `execution_time`<br>3. Verificar que el endpoint del webhook sigue respondiendo (no 404)<br>4. Enviar request al webhook → debe recibir respuesta (aunque el flow no ejecute) | AC-62 | 🟠 | ⬜ |
| TC-094 | REG | Creación de PDF templates funciona para usuarios con cuota disponible | 1. Company con `pdf_templates.consumed < pdf_templates.available`<br>2. PDF Templates > [New Template] > Crear template completo<br>3. Verificar: template creado exitosamente<br>4. BD: `COUNT(templates)` aumentó en 1 | AC-63 | 🟠 | ⬜ |
| TC-095 | REG | Templates existentes no se ven afectados por la quota de `pdf_templates` | 1. Company con `pdf_templates` agotado pero templates ya creados<br>2. Abrir template existente > editar y guardar<br>3. Verificar: edición exitosa (quota solo bloquea creación de nuevos) | AC-64 | 🟠 | ⬜ |

---

## SUITE 11 — Tenant UI Read-Only (NUEVA)

| TC-ID | Tipo | Caso de prueba | Pasos | AC | Prioridad | Estado |
|-------|------|----------------|-------|----|-----------|--------|
| TC-104 | HP | `/billing/plans` muestra pricing cards read-only — sin botones de compra | 1. Login como tenant user con permiso `read-billing`<br>2. Navegar a `/billing/plans`<br>3. Verificar: pricing cards se muestran con precios seeded localmente<br>4. Verificar: NO existen botones de "Upgrade", "Buy", "Checkout" ni acciones de compra<br>5. Verificar: toggle monthly/yearly funciona (si aplica) mostrando precios locales | AC-B11 | 🟠 | ⬜ |
| TC-105 | HP | `/billing/subscription` muestra plan actual y usage bars — sin cancel/resume/overage | 1. Login como tenant user con permiso `read-billing`<br>2. Navegar a `/billing/subscription`<br>3. Verificar: se muestra el plan actual con su nombre y precio<br>4. Verificar: usage bars/cards muestran consumo por feature con progress bars<br>5. Verificar: NO existen botones de "Cancel", "Resume", "Buy Overage", "Change Plan" ni acciones de modificación<br>6. Verificar: precio viene de `plan.product.prices` (seeded local) | AC-B12 | 🟠 | ⬜ |

---

## SUITE 12 — Admin Catalog y Product Seeding (NUEVA)

| TC-ID | Tipo | Caso de prueba | Pasos | AC | Prioridad | Estado |
|-------|------|----------------|-------|----|-----------|--------|
| TC-109 | HP | Admin Products.vue read-only — sin Stripe sync ni stripe_id visible | 1. Login como admin<br>2. Navegar a Admin > Billing > Products<br>3. Verificar: lista de productos muestra catálogo local<br>4. Verificar: NO existe botón "Add from Stripe" ni "Sync"<br>5. Verificar: NO se muestra `stripe_id` en la interfaz | AC-B13 | 🟡 | ⬜ |
| TC-112 | HP | ProductSeeder crea producto local por plan con `provider='local'` | 1. BD: `SELECT id, name, provider, data FROM products`<br>2. Verificar: cada producto tiene `provider = 'local'`<br>3. Verificar: `data->'prices'` contiene precios seeded (monthly amounts)<br>4. Verificar: cada plan tiene un `product_id` asociado | AC-B14 | 🟠 | ⬜ |

---

## SUITE 13 — Verificación Residual de Stripe (NUEVA)

| TC-ID | Tipo | Caso de prueba | Pasos | AC | Prioridad | Estado |
|-------|------|----------------|-------|----|-----------|--------|
| TC-107 | EC | `grep -ri stripe` en flow_binaries — solo mappings de columna, sin llamadas SDK | 1. Ejecutar en terminal: `grep -ri stripe` sobre el directorio de flow_binaries Go code<br>2. Verificar: los resultados son solo mappings de columnas de BD (ej. `stripe_subscription_id`, `stripe_customer_id`) y constantes de modelo<br>3. Verificar: NO hay imports de `stripe-go` ni llamadas a `stripe.Client`<br>4. Verificar: NO existe el directorio `ion/services/stripe/` | AC-B15 | 🟠 | ⬜ |

---

## SUITE 14 — Code Review / Bug Hunting (Inyectados en Deployment)

> TCs derivados del code review QA. Cada uno verifica un riesgo identificado en el código.

| TC-ID | Tipo | Caso de prueba | Pasos | AC | Prioridad | Estado |
|-------|------|----------------|-------|----|-----------|--------|
| TC-CR-001 | EC | Company nueva: primer request después de auto-provisioning — ¿guard permite? | 1. Crear company nueva (sin acceso previo a billing)<br>2. Inmediatamente intentar ejecutar un flow<br>3. Verificar: ejecución procede (guard permite)<br>4. BD: verificar que `subscriptions` y `feature_consumptions` se crearon automáticamente | BUG-CR-001 | 🟠 | ⬜ |
| TC-CR-002 | EC | AI credits race condition: requests rápidos con créditos casi agotados | 1. Company con `ai_credits consumed=95, available=100`<br>2. Abrir flow-pilot chat y enviar 3 mensajes rápidos en sucesión<br>3. Verificar BD: `consumed` no supera `available` significativamente<br>4. Verificar que el guard bloquea al agotar | BUG-CR-003 | 🟠 | ⬜ |
| TC-CR-003 | EC | PHP guard vs Go guard: reset_at vencido, primera consulta por PHP | 1. Feature con `reset_at` vencido y `consumed > 0`<br>2. Llamar endpoint IonMind (pasa por PHP FeatureGuard)<br>3. Verificar: acción permitida (PHP skip la fila vencida)<br>4. Ejecutar flow (pasa por Go GuardFeature)<br>5. BD: verificar que lazy reset se aplicó (`consumed=0`, `reset_at` avanzó) | BUG-CR-004 | 🟠 | ⬜ |
| TC-CR-004 | EC | Admin cambia plan: ¿consumed persiste o se resetea? | 1. Company con plan free: `execution_time consumed=800, available=1000`<br>2. Admin asigna plan go<br>3. BD: `SELECT consumed, available FROM feature_consumptions WHERE feature_id=<exec_time>`<br>4. Verificar: `available` cambió a valor del plan go<br>5. Documentar si `consumed` persiste (800) o se reseteó (0) | BUG-CR-005 | 🟠 | ⬜ |
| TC-CR-005 | EC | Feature con ventana diaria: ¿email de 80% se genera? | 1. Feature con ventana `period_unit='day'`<br>2. Consumir hasta 80% del saldo diario<br>3. Verificar inbox: ¿llega email de 80%?<br>4. Si no llega → documentar como diseño intencional (solo month/year genera emails) | BUG-CR-002 | 🟡 | ⬜ |

---

## Resumen de cobertura — IONF-1056-B (Post Code Review)

| Suite | TCs | 🔴 | 🟠 | 🟡 | ⏸ Bloqueados |
|-------|-----|----|----|----|-------------|
| 1 — Provisioning | 4 | 2 | 1 | 1 | 0 |
| 2 — Admin Assignment (NUEVA) | 5 | 2 | 3 | 0 | 0 |
| 3 — Consumo y ventanas | 9 | 4 | 4 | 0 | 0 |
| 4 — Enforcement | 8 | 4 | 3 | 0 | 1 (TC-037) |
| 5 — Guard sin Overage (NUEVA) | 2 | 2 | 0 | 0 | 0 |
| 6 — AI Credits (NUEVA) | 2 | 2 | 0 | 0 | 0 |
| 7 — Notificaciones | 6 | 0 | 3 | 3 | 0 |
| 8 — IONPDF | 4 | 0 | 3 | 1 | 0 |
| 9 — Runtime History | 5 | 0 | 2 | 1 | 1 (TC-083) |
| 10 — Regresión | 6 | 2 | 4 | 0 | 0 |
| 11 — Tenant UI Read-Only (NUEVA) | 2 | 0 | 2 | 0 | 0 |
| 12 — Admin Catalog (NUEVA) | 2 | 0 | 1 | 1 | 0 |
| 13 — Stripe Residual (NUEVA) | 1 | 0 | 1 | 0 | 0 |
| **14 — Code Review (NUEVA)** | **5** | **0** | **4** | **1** | **0** |
| **TOTAL** | **61** | **18** | **31** | **8** | **2** |

### Comparativa con matriz anterior

| Métrica | IONF-1056 (original) | IONF-1056-B (reconsiderado) | Post Code Review | Delta vs original |
|---------|---------------------|---------------------------|-----------------|-------------------|
| Total TCs | 67 | 56 | 61 | -6 |
| 🔴 Crítico | 28 | 18 | 18 | -10 |
| 🟠 Alto | 28 | 27 | 31 | +3 |
| 🟡 Medio | 7 | 7 | 8 | +1 |
| ⏸ Bloqueados | 4 | 2 | 2 | -2 |
| Suites | 9 | 13 | 14 | +5 |

### TCs bloqueados (esperando resolución)

| TC-ID | Bloqueado por | Pregunta |
|-------|--------------|----------|
| TC-037 | P-01 | ¿Grace execution implementada o descartada? |
| TC-083 | Rediseño UI | Vista de Board de Runtime History pendiente |

### TCs desbloqueados (respecto a la matriz anterior)

| TC-ID | Era bloqueado por | Resolución |
|-------|--------------------|-----------|
| TC-028 | P-02 (cron vs lazy) | ✅ IONF-1056-B design doc confirma: resets son lazy, sin crons |

