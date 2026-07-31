# Template de Rechazo — IONF-1056-B

Estimado @enrique

**El resultado de pruebas para este ticket es: RECHAZADO ❌**

**Ticket**: IONF-1056-B — Zero-Stripe (Billing & Consumption Guard)
**Módulo**: Billing, PDF Templates, Notifications, Webhooks, Admin Panel
**QA Engineer**: Steve Nina
**Fecha**: 2026-07-30

### Resumen de Testing
- Casos ejecutados: 110+ (incluyendo TCs del Code Review)
- Bugs encontrados en Code Review: 6
- Bugs encontrados en Testing: 14
- Bugs totales (bloqueantes): 5 🔴

### Code Review QA
> Resumen de la revisión de código realizada antes del testing funcional.

- Repos revisados: flow_binaries (backend Go), webcomponents-flow (frontend Vue), gateway (backend PHP)
- Hallazgos: 6 (🔴: 3, 🟠: 2, 🟡: 1)
- TCs inyectados en la test matrix desde el code review: 8
- Bugs del código que contribuyen al rechazo: BUG-CR-001, BUG-CR-003, BUG-CR-005, BUG-CR-006

---

### 📌 Observaciones

**🔴 OBS-01 - Urgent - Estado: Nuevo**
**Área / Flujo: Billing — PDF Templates (Consumption Guard)**

**Descripción:**
El enforcement de cupo de `pdf_templates` no bloquea la creación de nuevos templates. Se puede exceder la quota ilimitadamente sin que el guard intervenga.

**Pasos de reproducción:**

1. Admin Login > Plans > Editar plan free > Configurar `pdf_templates` con cupo de 2
2. Company Login > como Tenant User con ese plan free
3. PDF Templates > Crear template 1 → éxito ✅
4. Crear template 2 → éxito ✅
5. Crear template 3 → éxito ❌ (debería haberse bloqueado con 403)
6. Billing > Subscriptions > Verificar consumo → muestra **-150% (-3 de 2)** ❌

**Resultado esperado:**
La creación del 3er template debería bloquearse con 403 Forbidden. La vista debería mostrar 100% y estado "Bloqueado" al alcanzar el cupo. Referencia: AC-28.

**Comportamiento actual:**
Se crearon 3 templates con quota de 2 sin ningún bloqueo. La vista muestra porcentaje negativo (-150%), un valor imposible. El backend no ejecuta el guard al crear PDF templates.

**Evidencia:**
- BD: `feature_consumptions.consumed = 0` después de crear 3 templates (no registró +1)
- UI: porcentaje -150% (-3 de 2)

---

**🔴 OBS-02 - Urgent - Estado: Nuevo**
**Área / Flujo: Billing — Notifications (Consumption Notify)**

**Descripción:**
Los emails de notificación de consumo (80%, 100%, bloqueado) no se envían al usuario, pero el log de notificación sí se crea en `feature_consumption_logs` con campos vacíos.

**Pasos de reproducción:**

1. Company Login > como Tenant User con plan que incluye `execution_time`
2. Ejecutar flows hasta alcanzar el 80% del cupo
3. Verificar bandeja de correo del owner de la company → **no hay email** ❌
4. BD: `SELECT * FROM feature_consumption_logs WHERE log_type = 'notification_80'` → registro **existe** ✅
5. Inspeccionar registro: campos `source`, `reference_type`, `reference_id`, `metadata` → **vacíos** ❌
6. Continuar hasta 100% → verificar correo → **no hay email** ❌

**Resultado esperado:**
Se debe enviar email al owner de la company cuando el consumo alcanza 80%, 100% y bloqueado. Los campos del log deben estar poblados para trazabilidad. Referencia: AC-33, AC-34, AC-35.

**Comportamiento actual:**
El log `notification_100` / `notification_80` se crea en BD pero con campos vacíos. El email no se envía. El código en `consumption_notify.go` registra el log como placeholder pero el envío falla silenciosamente.

**Evidencia:**
- BD: `feature_consumption_logs` con `log_type = 'notification_100'`, campos `source`, `reference_type`, `reference_id`, `metadata` vacíos
- Bandeja de correo: sin emails de notificación

---

**🔴 OBS-03 - Urgent - Estado: Nuevo**
**Área / Flujo: Billing — Webhook Trigger (Flow Engine + Guard)**

**Descripción:**
Un flow live con webhook trigger devuelve **504 Gateway Timeout** (después de 30+ seg) en vez de **403 inmediato** cuando `execution_time` está bloqueado. Causa retry storms en callers externos y pérdida de eventos.

**Pasos de reproducción:**

1. Company Login > Ejecutar flows hasta agotar `execution_time` (consumed >= available)
2. Verificar feature **bloqueada** en Billing
3. Desde sistema externo: `POST /webhook/trigger/{flow_id}` al flow live
4. Observar que la respuesta **no llega inmediatamente** — se queda esperando
5. Después de ~30 seg → **504 Gateway Timeout** ❌
6. Sin body descriptivo — solo timeout genérico del proxy

**Resultado esperado:**
Respuesta **inmediata** (<1 seg) con **403 Forbidden** y body JSON descriptivo: `{"error": "quota_exceeded", "feature": "execution_time"}`. Referencia: AC-27 ("la ejecución del flow termina **inmediatamente**").

**Comportamiento actual:**
El webhook se queda colgado ~30 seg hasta que el gateway/proxy devuelve 504. El guard no propaga el bloqueo al response del webhook. Los callers externos (Shopify, MercadoLibre, etc.) reciben timeout genérico y activan retries automáticos.

**Evidencia:**
- Network: respuesta 504 después de ~30 seg
- Impacto: retry storms, pérdida de datos, acumulación de conexiones colgadas

---

**🔴 OBS-04 - Urgent - Estado: Nuevo**
**Área / Flujo: Billing — PDF Templates (Create/Delete Consumption)**

**Descripción:**
El commit `b1fb4a96` eliminó el guard y el `+1` del flujo de creación de PDF templates a nivel de **company**, pero dejó el `-1` en el delete. El `consumed` queda negativo y el cupo es inaplicable. La variante de **account** sí conserva ambas operaciones correctamente.

**Pasos de reproducción:**

1. Company Login > como Tenant User (plan con cupo de `pdf_templates`)
2. PDF Templates > Crear varios templates superando cualquier cupo teórico
3. Verificar que ninguna creación se bloquea ni registra consumo en `feature_consumptions`
4. Eliminar 3 templates
5. BD: `SELECT consumed FROM feature_consumptions WHERE feature_id = (SELECT id FROM features WHERE slug = 'pdf_templates')`
6. Observar que `consumed = -3` ❌

**Resultado esperado:**
Crear debería validar el cupo (`consumed >= available`) y registrar `+1`. Eliminar debería registrar `-1`. El contador debería reflejar los templates existentes (>= 0).

**Comportamiento actual:**
- Create (company): ❌ Sin guard, sin `+1` — eliminados en commit `b1fb4a96`
- Delete (company): ✅ Registra `-1` correctamente
- Resultado: `consumed` queda negativo (ej. -3 tras eliminar 3 templates)
- Create (account): ✅ Conserva guard + `+1` — referencia correcta

**Evidencia:**
- BD: `feature_consumptions.consumed = -3` después de eliminar 3 templates
- Repo: `flow_binaries` | Commit: `b1fb4a96` | Archivo: `backend/ion/services/pdf_template_service.go` (líneas 94–229)
- Auditoría: patrón de logs con solo `-1` sin `+1` previos

---

**🟡 OBS-05 - High - Estado: Nuevo**
**Área / Flujo: Billing — AI Credits (UI + Guard)**

**Descripción:**
La UI redondea `consumed = 199.8` a "200" y muestra "100%" pero el guard NO bloquea (porque en BD `consumed < available`). El usuario puede seguir consumiendo, excediendo el límite por fracción decimal. Impacto económico: consumo sin cobro.

**Pasos de reproducción:**

1. Company Login > Utilizar flow-pilot hasta acumular ~199.8 AI credits consumidos
2. Billing > AI Credits → UI muestra **"200 de 200 (100%)"** ❌
3. BD: `consumed = 199.8, available = 200` — no bloqueado
4. Hacer 1 request más al flow-pilot → **funciona** (no bloqueó)
5. Verificar consumed → puede ser ~201.5 (excedió el límite)

**Resultado esperado:**
La UI debe mostrar el valor real (199.8 o "~200"). El porcentaje debe ser 99.9%, no 100%. Se debe definir un umbral mínimo de bloqueo para AI credits con consumo fraccionario.

**Comportamiento actual:**
UI redondea al entero. Dice 100% pero la feature no está bloqueada. El guard permite el siguiente request porque `199.8 < 200`. El consumed puede superar `available` por fracciones.

**Evidencia:**
- BD: `consumed = 199.8, available = 200`
- UI: "200 consumidos (100%)" — no bloqueado

---

**🟡 OBS-06 - High - Estado: Nuevo**
**Área / Flujo: Admin Panel — CompanySubscription UI**

**Descripción:**
El botón "Assign plan" no se deshabilita durante el request al backend. El dropdown de selección de plan tampoco se bloquea. Se puede presionar múltiples veces o cambiar de plan durante la operación, causando potenciales race conditions.

**Pasos de reproducción:**

1. Admin Login > Companies > seleccionar company > Subscription tab
2. Seleccionar plan en dropdown (ej. "Go")
3. DevTools > Network tab
4. Click en **"Assign plan"**
5. **Inmediatamente** click de nuevo (doble-click rápido)
6. Network: se enviaron **2 requests** al endpoint ❌
7. Alternativa: click en "Assign plan" → durante loading, cambiar dropdown a otro plan → permite selección ❌

**Resultado esperado:**
Al presionar "Assign plan", el botón y el dropdown deben quedar `disabled` con indicador de loading hasta que el backend responda. Solo un request debe enviarse.

**Comportamiento actual:**
Botón no se deshabilita. Dropdown sigue activo. Múltiples clicks generan múltiples requests simultáneos a `AdminAssignPlan`.

**Evidencia:**
- DevTools: 2+ requests al presionar rápidamente
- Componente: `CompanySubscription.vue` (+174 líneas)

---

**🟡 OBS-07 - High - Estado: Nuevo**
**Área / Flujo: Billing — Feature Consumptions (Data Integrity)**

**Descripción:**
El campo `consumed` en `feature_consumptions` tiene valores **negativos** (ej. -1). Valor lógicamente imposible. Al cambiar de plan, las `feature_consumptions` quedan como datos huérfanos con valores negativos. La UI muestra porcentajes negativos (-150%).

**Pasos de reproducción:**

1. Company Login > como Tenant User con plan free que incluye `pdf_templates`
2. Crear templates PDF (no se registra +1 — bug del guard)
3. Eliminar 1 template → sistema registra `-1`
4. BD: `consumed = -1` ❌
5. Admin Login > cambiar company de plan free a plan Go (que no incluye `pdf_templates`)
6. BD: fila de `feature_consumptions` con `consumed = -1` **persiste** como dato huérfano

**Resultado esperado:**
`consumed` nunca debe ser negativo (incluir `MAX(0, consumed - 1)` o validación). Al cambiar de plan, features huérfanas deben limpiarse o marcarse como inactivas.

**Comportamiento actual:**
`consumed = -1` persiste. Al cambiar de plan, datos huérfanos quedan en BD. UI muestra -150%. El guard puede interpretar incorrectamente datos de un plan que ya no aplica.

**Evidencia:**
- BD: `feature_consumptions.consumed = -1`
- UI: porcentaje -150% (-3 de 2)
- Causa raíz: BUG-03 (commit `b1fb4a96`)

---

**🟡 OBS-08 - High - Estado: Nuevo**
**Área / Flujo: Billing — Provisioning (Auto-provisioning / GetByEntity)**

**Descripción:**
Al crear una nueva company, no se crea inmediatamente un `subscriber_id` ni las `feature_consumptions`. La vista de Subscriptions no carga features en el primer acceso, pero funciona después de un refresh. El provisioning es lazy, no síncrono.

**Pasos de reproducción:**

1. Admin Login > Companies > Create Company
2. Llenar datos mínimos y crear
3. Inmediatamente navegar a tab **Subscriptions**
4. Observar: vista **no carga features** ❌ (loading infinito o vacía)
5. BD: `SELECT * FROM subscribers WHERE entity_type = 'company' AND entity_id = {id}` → **no hay registro** ❌
6. Hacer **refresh** (F5)
7. Ahora sí aparecen los features ✅
8. BD: ahora sí existe subscriber con `feature_consumptions`

**Resultado esperado:**
Al crear company, subscriber + plan free + `SyncConsumptions` deben ejecutarse síncronamente (AC-01). Features deben estar disponibles inmediatamente sin refresh.

**Comportamiento actual:**
`GetByEntity` auto-provisiona lazy — crea subscriber al primer acceso a billing, no al crear la company. El primer request llega antes de que el provisioning complete.

**Evidencia:**
- BD: subscriber no existe hasta segundo request
- UI: vista vacía en primer acceso, funciona con refresh
- Referencia: BUG-CR-001

---

**🟡 OBS-09 - High - Estado: Nuevo**
**Área / Flujo: Billing — IONPDF (Ledger / Consumption Logs)**

**Descripción:**
Al crear templates PDF, no se genera ningún registro en `feature_consumption_logs` para `pdf_templates`. El ledger unificado queda vacío para esta feature. Incumple AC-54: "El consumo de IONPDF queda registrado en el ledger unificado".

**Pasos de reproducción:**

1. Company Login > como Tenant User con plan que incluye `pdf_templates`
2. PDF Templates > Crear un nuevo template
3. BD:
   ```sql
   SELECT * FROM feature_consumption_logs
   WHERE feature_consumption_id IN (
     SELECT id FROM feature_consumptions
     WHERE feature_id IN (
       SELECT id FROM features WHERE slug IN ('pdf_templates', 'pdf_impressions')
     )
   )
   ```
4. Observar: **no hay registros** ❌

**Resultado esperado:**
Cada creación de template debe generar un log en `feature_consumption_logs` con `amount: +1`, `source`, `reference_type`, `reference_id` y `metadata`. Cada eliminación debe generar un log con `amount: -1`. Referencia: AC-54.

**Comportamiento actual:**
No se generan logs. El ledger unificado está vacío para IONPDF. Sin trazabilidad de cuándo/quién/qué template fue creado desde la perspectiva de billing.

**Evidencia:**
- BD: `feature_consumption_logs` vacío para features de IONPDF
- Causa raíz: commit `b1fb4a96` eliminó `RecordConsumption(+1)` que también genera logs

---

**🔵 OBS-10 - Normal - Estado: Nuevo**
**Área / Flujo: Billing — IONPDF Standalone (Plan Assignment)**

**Descripción:**
No fue posible asociar un plan IONPDF standalone a una company sin IONFLOW. Según AC-51, el admin debería poder realizar esta asignación. Posiblemente no implementado en IONF-1056-B.

**Pasos de reproducción:**

1. Admin Login > Companies > seleccionar company **sin IONFLOW**
2. Subscription tab > buscar plan IONPDF standalone en dropdown
3. Intentar asignar el plan
4. La operación no se completa / el plan no está disponible

**Resultado esperado:**
El plan IONPDF standalone debe existir en el catálogo y poder asignarse a companies sin IONFLOW. Referencia: AC-51.

**Comportamiento actual:**
No fue posible completar la asociación. Se necesita confirmar si el plan no existe, no aparece en dropdown, o la asignación falla.

**Evidencia:**
- Verificar: `SELECT * FROM plans WHERE slug LIKE '%ionpdf%'`
- Verificar: dropdown de Admin > Subscription
- Pregunta pendiente: ¿IONPDF standalone está implementado en IONF-1056-B o es post-merge?

---

**🔴 OBS-11 - Urgent - Estado: Nuevo**
**Área / Flujo: Billing — FeatureGuard PHP (Gateway)**

**Descripción:**
El `FeatureGuard` del gateway (PHP) devuelve 403 `Feature quota exceeded` a companies nuevas que no tienen filas en `feature_consumptions`. A diferencia del guard de Go (que auto-aprovisiona vía `GetByEntity`), el guard PHP aplica la regla "sin filas = bloqueado" sin intentar aprovisionar la suscripción free. La company queda permanentemente bloqueada hasta que algún flujo de Go aprovisione la suscripción.

**Pasos de reproducción:**

1. Admin Login > Companies > Crear una company nueva
2. **Sin abrir ninguna vista de billing ni ejecutar flows** (para que no se dispare el auto-provisioning lazy de Go)
3. Invocar `POST /1.0/tenants/{id}/ionmind/analyze` como primera acción
4. Observar la respuesta: **403 Feature quota exceeded** ❌
5. Verificar BD: `SELECT * FROM feature_consumptions WHERE subscriber_id = (SELECT id FROM subscribers WHERE entity_id = {company_id})` → **no hay filas**
6. La feature `ai_credits` está ACTIVE en el catálogo de features

**Resultado esperado:**
El guard PHP debería aprovisionar la suscripción free (como hace Go vía `GetByEntity`) y permitir la acción con el saldo free. Ambos guards (Go y PHP) deben tener el mismo comportamiento ante una company sin aprovisionar.

**Comportamiento actual:**
El guard PHP consulta `feature_consumptions`, no encuentra filas, aplica la regla "sin filas = bloqueado" y responde 403 permanentemente. La company queda bloqueada hasta que algún flujo del backend Go la aprovisione (ej. al acceder a la vista de Billing desde el frontend).

**Evidencia:**
- Response: `403 Feature quota exceeded` al invocar `/ionmind/analyze` en company sin aprovisionar
- BD: `feature_consumptions` vacío para esa company
- Divergencia Go vs PHP: Go auto-aprovisiona, PHP bloquea
- Repo: `gateway` | Commit: `03d2a2bb` | Archivos: `app/Services/Billing/FeatureGuard.php`, `app/Http/Controllers/IonMindController.php`

---

**🟡 OBS-12 - High - Estado: Nuevo**
**Área / Flujo: Billing — Usage View (reset_at date)**

**Descripción:**
Al crear una company nueva hoy (30 de julio), la vista de Billing > Usage muestra `pdf_impressions: 0 de 10` con reset diario y fecha de reset **30 de julio** (hoy). Si el reset es diario, la fecha debería ser **31 de julio** (mañana), no el mismo día de creación.

**Pasos de reproducción:**

1. Admin Login > Companies > Crear company nueva (hoy 30 de julio)
2. Asignar plan que incluya `pdf_impressions` con reset diario
3. Company Login > Billing > Usage
4. Observar la feature `pdf_impressions`: **0 de 10 impresiones**
5. Observar la fecha de reset: **30 de julio** ❌ (hoy, mismo día de creación)
6. Esperado: **31 de julio** (mañana)

**Resultado esperado:**
La fecha de `reset_at` para un reset diario debe ser el **día siguiente** a la creación/último reset. Si la company se creó el 30 de julio, el primer reset debería ser el 31 de julio. El `reset_at` indica **cuándo** se reseteará el consumo, no cuándo se creó.

**Comportamiento actual:**
La vista muestra `reset_at = 30 de julio` (hoy), lo que implica que el consumed debería resetearse **hoy mismo**. Esto puede significar:
- El `reset_at` se calcula como `NOW()` en vez de `NOW() + 1 day` al crear la suscripción
- O el lazy reset ya se ejecutó inmediatamente al crear, dejando el `reset_at` sin avanzar al siguiente ciclo

**Evidencia:**
- UI: Billing > Usage > `pdf_impressions` muestra reset date = 30 de julio (hoy)
- Company creada hoy 30 de julio
- Reset diario debería mostrar 31 de julio como próximo reset

---

**🔴 OBS-13 - Urgent - Estado: Nuevo**
**Área / Flujo: Billing — Consumption Guard (execution_time mid-execution + concurrencia)**

**Descripción:**
Un flow con carga pesada (200 elementos) fue matado en la iteración 50 por timeout de 30 min. La company ya tenía 170 seg consumidos de 600 disponibles. El flow se registró con status `stopped` + **1800 seg de consumo**. Total resultante: 170 + 1800 = **1970 seg consumidos de 600 disponibles** (328% del cap). Mientras el flow pesado estaba corriendo, **otros flows de la misma company también se ejecutaron** porque el guard solo veía 170/600 en BD (consumo del flow en curso no persistido).

**Pasos de reproducción:**

1. Company Login > Company con `execution_time: consumed=170, available=600`
2. Ejecutar un flow pesado con ~200 elementos (diseñado para tardar >30 min)
3. Mientras el flow pesado está en ejecución, lanzar otros flows desde la misma company
4. Observar que los flows adicionales **pasan el guard** (ven 170/600 en BD) ❌
5. Esperar a que el flow pesado sea matado por timeout (30 min)
6. Verificar BD: `consumed = 170 + 1800 + X = 1970+ seg` de 600 disponibles ❌
7. Verificar status del flow: `stopped` ✅ (correcto para timeout)

**Resultado esperado:**
El enfoque acordado en la reunión del 07-30-2026 establece un **enforcement per-node con persistencia intermedia**: el consumo se registra nodo por nodo (no al final del flow), se persiste en Postgres y se cachea en Redis después de cada nodo. Antes de ejecutar el siguiente nodo, el guard verifica el saldo consultando Redis (fast-path) o Postgres (fallback). Si el saldo se agota mid-flow, el flow se detiene en ese nodo con status indicando quota agotada. Esto resuelve tanto el enforcement mid-execution como la visibilidad del consumo en tiempo real para flows concurrentes.

**Comportamiento actual:**

| Aspecto | Observado | Esperado |
|---------|-----------|----------|
| Guard al inicio del flow | ✅ Verificó 170 < 600 — permitió | ✅ Correcto |
| Enforcement mid-execution | ❌ No existe — flow consumió 1800 seg con solo 430 de saldo | Guard per-node debe detener cuando saldo se agota |
| Consumo visible en tiempo real | ❌ No — otros flows ven 170/600 durante los 30 min | Consumo debe persistirse nodo a nodo en Postgres + Redis |
| Flows concurrentes | ❌ Pasan el guard con datos obsoletos | Guard debe consultar Redis para ver consumo actualizado |
| Consumed registrado | 1800 seg (timeout completo) | Tiempo real procesado hasta el nodo donde se detuvo |
| Total final | 1970 de 600 (328%) | No debería superar 600 |

**Evidencia:**
- BD: `feature_consumptions.consumed = 1970, available = 600`
- Flow status: `stopped` (timeout 30 min)
- Otros flows ejecutados durante los 30 min con guard que veía 170/600
- Referencia: BUG-CR-006 (`consumptionLocks` in-process, no protege multi-replica)
- Enfoque acordado: ver diagrama de la reunión 07-30-2026 (enforcement per-node con Redis)

---

**🟡 OBS-14 - High - Estado: Pendiente de definición**
**Área / Flujo: Billing — Consumption Guard (grace execution al borde del límite)**

**Descripción:**
Con 590 de 600 seg consumidos, el siguiente flow consume 40 seg. ¿Debería completarse como "gracia" o bloquearse? ¿Qué pasa si al mismo instante se lanzan 10-15 flows más? La pregunta P-01 de los ACs sigue sin resolver — hay contradicción entre AC-32 (grace execution) y los comentarios de IONF-1056-B (hard block).

**Pasos de reproducción:**

1. Company con `execution_time: consumed=590, available=600` (saldo restante: 10 seg)
2. Ejecutar un flow que consume 40 seg
3. Observar si el flow se permite (grace) o se bloquea (hard block)
4. Variante concurrente: con 590/600, lanzar 15 flows simultáneamente (cada uno ~40 seg)
5. Observar cuántos se ejecutan vs cuántos se bloquean

**Resultado esperado:**
Pendiente de definición. Tres opciones en evaluación:

| Opción | Comportamiento | Pro | Contra |
|--------|---------------|-----|--------|
| **A: Hard block** | `consumed >= available` → bloquea | Simple, predecible, seguro | Flow de 1 seg se bloquea con 599/600 |
| **B: Grace execution** | Permite 1 flow adicional al 100%, luego bloquea | Mejor UX | Flow de 2000 seg como "gracia" |
| **C: Soft check** | Permite si `consumed < available`, sin garantía mid-execution | Balance | No controla cuánto consume el flow |

**Comportamiento actual:**
El guard en `consumption_guard.go` verifica `consumed >= available` → **hard block directo**. No hay evidencia de grace execution en el código. Pero AC-32 sugiere que debería existir.

**Evidencia:**
- Código: `consumption_guard.go` — condición `consumed >= available`
- AC-32: menciona grace execution
- IONF-1056-B comentarios: mencionan hard block
- Race condition: 15 flows simultáneos con 590/600 → todos ven 590/600 → todos pasan → consumo total 590 + (15 × 40) = 1190 seg de 600 disponibles
- Referencia: BUG-CR-006 (race condition del guard)

---

### ❓ Preguntas abiertas para el Developer

| # | Pregunta | Urgencia | Observación relacionada |
|---|----------|----------|------------------------|
| 1 | ¿El guard se ejecuta antes de **cada flow individual** o solo al inicio? ¿Considera el consumo de flows en ejecución paralela (in-memory), o solo el valor persistido en BD? | 🔴 | OBS-01, OBS-04 |
| 2 | ¿**Grace execution** (P-01) está implementada o no? El testing sugiere que NO hay grace — el guard bloquea con `consumed >= available` sin margen. ¿Es intencional? | 🔴 | General |
| 3 | ¿Por qué el **webhook no retorna 403 inmediato** cuando `execution_time` está bloqueado? ¿El guard no se ejecuta en el path del webhook trigger, o el resultado del guard no se propaga al response? | 🔴 | OBS-03 |
| 4 | **Timeout de 30 min**: ¿el `consumed` registra los **1800 seg del timeout** o el **tiempo real procesado** (que fue menor, interrumpido en iteración 50 de 200)? | 🟠 | General |
| 5 | ¿`AdminAssignPlan` debería **resetear `consumed` a 0** al cambiar de plan? Actualmente no lo hace — el consumed persiste entre cambios de plan. ¿Es intencional? | 🟠 | OBS-07 |
| 6 | ¿A qué **usuario/email** se envían las notificaciones en una company multiusuario? ¿Solo al owner? ¿A todos los usuarios con rol admin? | 🟠 | OBS-02 |
| 7 | ¿**IONPDF standalone** está implementado en IONF-1056-B o es trabajo post-merge? | 🟠 | OBS-10 |
| 8 | ¿El **FeatureGuard de PHP** (gateway) debería auto-aprovisionar la suscripción free cuando no encuentra filas en `feature_consumptions`, o solo el backend Go es responsable del provisioning? ¿Cómo se garantiza que ambos guards tengan el mismo comportamiento? | 🔴 | OBS-11 |
| 9 | ¿El `reset_at` de features con reset diario debería calcularse como `NOW() + 1 day` al crear la suscripción? Actualmente parece calcularse como `NOW()`, causando que el reset se muestre para el mismo día de creación. | 🟠 | OBS-12 |
| 10 | ¿El enforcement **per-node con Redis** acordado en la reunión del 07-30 reemplaza completamente el guard actual (solo pre-check)? ¿Cuándo se espera la implementación? ¿El `consumed` del timeout debería registrar los 1800 seg o el **tiempo real procesado** hasta el nodo donde murió? | 🔴 | OBS-13 |
| 11 | ¿**Grace execution** (P-01) está definida como hard block, grace, o soft check? ¿Cuál de las 3 opciones aplica? Esto afecta directamente cómo se testea el borde del límite con flows concurrentes. | 🔴 | OBS-14 |

---

### Evidencia General
- Test Matrix: [test-matrix.md](file:///c:/Users/STEVE/Desktop/Automation/ionflow-qa-catalyst/knowledge/L3-tickets/IONF-1056/test-matrix.md)
- Code Review QA: [code-review-qa.md](file:///c:/Users/STEVE/Desktop/Automation/ionflow-qa-catalyst/knowledge/L3-tickets/IONF-1056/code-review-qa.md)
- AC Consolidado: [ac-consolidated.md](file:///c:/Users/STEVE/Desktop/Automation/ionflow-qa-catalyst/knowledge/L3-tickets/IONF-1056/ac-consolidated.md)
- Análisis detallado: [analysis_results.md](file:///c:/Users/STEVE/Desktop/Automation/ionflow-qa-catalyst/knowledge/L3-tickets/IONF-1056/analysis_results.md)

| Details | |
|---|---|
| BROWSER | Chrome |
| BRANCH | IONF-1056-B |
| ENV | dev-app.ionflow.io |
| TEST MATRIX | [test-matrix.md](file:///c:/Users/STEVE/Desktop/Automation/ionflow-qa-catalyst/knowledge/L3-tickets/IONF-1056/test-matrix.md) |
| CODE REVIEW | ✅ Realizado |
| MERGE REQUEST | PENDIENTE (bugs encontrados) |
