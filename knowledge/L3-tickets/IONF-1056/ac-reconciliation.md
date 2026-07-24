# Reconciliación de AC — IONF-1056 (Padre + 6 Subtareas)
> Paso 2 del Discovery Runbook
> Fecha: 2026-06-14
> Fuente: Descripción + Comentarios/Actividad de todos los tickets

---

## TICKET PADRE — IONF-1056
**[https://app.clickup.com/t/86e1pzyug](https://app.clickup.com/t/86e1pzyug)**

### Comentarios de Actividad (cronológico)

| Fecha | Autor | Contenido clave |
|-------|-------|----------------|
| 2026-06-03T16:56 | Marcel Herrera Rendón | *"Detalles y dudas resueltas en esta reunión"* — sin contenido adicional registrado |
| 2026-06-03T18:41 | Marcel Herrera Rendón | Propuesta provisional de planes Go/Pro/Enterprise con valores numéricos tentativos |
| 2026-06-12T16:52 | Enrique Vicente | **Reporte Quick Prototype** — confirma arquitectura, principios y documento IONF-1056-prototype.md |

### Decisiones clave de comentarios vs descripción

| # | AC Descripción | Decisión Comentario | Divergencia |
|---|---|---|---|
| D-01 | "Reset mensual inicial" | Enrique 12-jun: **sin crons** — resets **perezosos** al leer/escribir | ⚠️ DIVERGE — no es cron mensual, es lazy |
| D-02 | "Stripe como capa de cobro" | Enrique 12-jun: Stripe Billing Meters específicamente | ⚠️ DETALLA — mecanismo concreto |
| D-03 | "El estado es timestamp, no columna status" | Enrique 12-jun: confirma `canceled_at` + `expires_at` | ✅ Alineado |
| D-04 | "Una suscripción por empresa" | Enrique 12-jun: confirmado, plan free auto-aprovisionado | ✅ Alineado |
| D-05 | "Medición por segundos" | Enrique 12-jun: "medición por ventanas" — puede haber múltiples ventanas simultáneas (ej. mensual + diaria) | ⚠️ AMPLÍA — no solo mensual, pueden coexistir ventanas |
| D-06 | Bloqueo simple | Enrique 12-jun: `blocked = available <> -1 AND consumed >= available` (cualquier ventana agotada bloquea) | ⚠️ DETALLA — bloquea si CUALQUIER ventana se agota |
| D-07 | Precios provisionales | Marcel 03-jun: Go=$7, Pro=$15, Enterprise=$300/año con valores de segundos y AI credits | ℹ️ PROVISIONAL — no son precios finales, solo referencia |

---

## IONF-1057 — Runtime History (Historial de Duración)
**[https://app.clickup.com/t/86e1pzz9c](https://app.clickup.com/t/86e1pzz9c)**
**Estado final:** `quick prototype`

### Comentarios de Actividad

| Fecha | Autor | Contenido clave |
|-------|-------|----------------|
| 2026-06-08T12:32 | Enrique Vicente | Implementación del sistema de tiempo de ejecución |

### Detalles del comentario de Enrique (2026-06-08)

> Se implementó el sistema que registra el tiempo de ejecución, considerando el tiempo **activo** y de espera **idle** que contempla los siguientes casos:
> - Nodo Timer ejecutado correctamente
> - Llamada a un subflow con la opción `waitForResponse` activada
>
> La visualización de esta data en la vista de Board está por definirse por el rediseño de la UI.

### Divergencias encontradas

| # | AC Descripción | Decisión Comentario | Divergencia |
|---|---|---|---|
| D-IONF1057-01 | "Mostrar duración de última ejecución completada" | Implementado: registra `active_seconds` + `idle_seconds` + `units_consumed` separados | ✅ Alineado con alcance |
| D-IONF1057-02 | "Fallback sin histórico: mostrar estado neutro" | No confirmado explícitamente en comentarios — implementación pendiente de confirmar | ❓ SIN CONFIRMAR |
| D-IONF1057-03 | "Visualización en Board" | Enrique: **"está por definirse"** por rediseño de UI | ⚠️ BLOQUEADO — UI pendiente de diseño |
| D-IONF1057-04 | "Actualización continua cada nueva ejecución" | El sistema registra por ejecución: datos de `session_id`, `start_time`, `end_time`, `active_seconds`, `idle_seconds`, `units_consumed` | ✅ Alineado |

**AC nuevo detectado en comentario:**
- La duración incluye tiempo **activo** y tiempo **idle** por separado
- Los casos especiales de idle: Timer nodes y subflow `waitForResponse`

---

## IONF-1058 — Enforcement, Warnings y Estado Combinado
**[https://app.clickup.com/t/86e1pzz9e](https://app.clickup.com/t/86e1pzz9e)**
**Estado final:** `prototype review`

### Comentarios de Actividad

| Fecha | Autor | Contenido clave |
|-------|-------|----------------|
| 2026-06-09T19:33 | Enrique Vicente | Implementación del sistema de enforcement y warnings |
| 2026-06-11T18:18 | Enrique Vicente | Actualización: layout de emails configurado |

### Detalles del comentario de Enrique (2026-06-09)

> **Por feature:**
> - `execution_time`: bloquea futuras ejecuciones tanto en el editor como en live (no elimina webhooks ni schedules, solo termina la ejecución inmediatamente con un mensaje de error)
> - `pdf_templates`: controla la creación de templates hasta el límite establecido
> - `pdf_impressions`: si el límite es excedido el nodo PDF falla inmediatamente en tiempo de ejecución
>
> **Emails implementados:**
> - Al 80% → alerta al usuario que puede activar overage para que no se detengan sus flows
> - Al 100% → puede seguir si tiene overage activado
> - Al agotar el límite de overage → se detienen inmediatamente los recursos asociados

### Detalles del comentario de Enrique (2026-06-11)

> Layout IonFlow unificado para todas las notificaciones. Template y body de email finales **por definirse**.

### Divergencias encontradas

| # | AC Descripción | Decisión Comentario | Divergencia |
|---|---|---|---|
| D-IONF1058-01 | "1 ejecución de gracia por ciclo" | Comentario Enrique: NO menciona la grace execution explícitamente — el sistema bloquea al llegar al 100% | ⚠️ CRÍTICO: Grace execution NO fue confirmada en implementación |
| D-IONF1058-02 | "Bloqueo hasta reset/upgrade/compra" | Implementado: bloqueo inmediato al agotar saldo sin overage | ✅ Parcialmente alineado |
| D-IONF1058-03 | "Email only, thresholds fijos" | Confirmado: 80%, 100%, y al agotar overage | ✅ Alineado |
| D-IONF1058-04 | "Reglas independientes por recurso" | Confirmado: `execution_time`, `pdf_templates`, `pdf_impressions` tienen comportamientos diferentes | ✅ Alineado — con detalles adicionales |
| D-IONF1058-05 | "Body/template email final" | Enrique 11-jun: **"Template y body de email finales por definirse"** | ⚠️ PENDIENTE — email no finalizado |
| D-IONF1058-06 | (no en descripción) | Nuevo: al 80% se invita a activar overage para no detener flows | ℹ️ AC NUEVO detectado en implementación |

**RIESGO CRÍTICO DETECTADO:**
> La descripción dice "1 ejecución de gracia" pero Enrique en los comentarios de IONF-1058 describe bloqueo directo al 100% sin mencionar grace execution. **Necesita aclaración con el equipo.**

---

## IONF-1059 — Catálogo Comercial y Planes Unificados
**[https://app.clickup.com/t/86e1pzz9f](https://app.clickup.com/t/86e1pzz9f)**
**Estado final:** `quick prototype`

### Comentarios de Actividad

| Fecha | Autor | Contenido |
|-------|-------|-----------|
| *(sin comentarios de contenido)* | — | Solo cambios de status registrados |

### Divergencias encontradas

| # | AC Descripción | Situación | Divergencia |
|---|---|---|---|
| D-IONF1059-01 | "Una sola pantalla comercial" | Sin comentarios adicionales — solo status changes | ❓ SIN VALIDACIÓN adicional en comentarios |
| D-IONF1059-02 | "Sin precios hardcodeados" | Sin comentarios — se asume vigente | ✅ Asumido vigente |
| D-IONF1059-03 | "Matriz de beneficios plan×feature" | Sin comentarios — no confirmada implementación | ❓ SIN CONFIRMAR |

**Nota:** IONF-1059 está en `quick prototype` — puede significar que la UI comercial aún no está implementada.

---

## IONF-1060 — IONPDF Standalone, Add-on y Metering
**[https://app.clickup.com/t/86e1pzz9g](https://app.clickup.com/t/86e1pzz9g)**
**Estado final:** `prototype review`

### Comentarios de Actividad

| Fecha | Autor | Contenido clave |
|-------|-------|----------------|
| 2026-06-03T13:47 | Marcel Herrera Rendón | *"Más que definir es solo poner unos provisionales de prueba, realmente tenemos dependencia del ticket de Rodolfo"* |
| 2026-06-03T18:51 | Marcel Herrera Rendón | Propuesta provisional de planes IONPDF y IONFLOW |

### Divergencias encontradas

| # | AC Descripción | Decisión Comentario | Divergencia |
|---|---|---|---|
| D-IONF1060-01 | "IONPDF standalone debe incluir bolsa menor de segundos" | Marcel 03-jun: "Incluir algunos segundos para que puedan usar sus boards con ionpdf" | ✅ Alineado — confirmado intención |
| D-IONF1060-02 | (oferta IONPDF) | Marcel: "tenemos dependencia del ticket de Rodolfo" | ⚠️ DEPENDENCIA EXTERNA: hay una dependencia con Rodolfo Merlo (mencionado en IONF-1061) no documentada en AC |
| D-IONF1060-03 | "Sin precios hardcodeados en especificación" | Marcel propone: Go=$7, Pro=$15, Enterprise=$300 — como "provisionales de prueba" | ℹ️ PROVISIONAL — son ejemplos, no precios finales |
| D-IONF1060-04 | "Metering por múltiples dimensiones (usos, templates, nodos PDF, segundos)" | Sin confirmación de implementación en comentarios | ❓ SIN CONFIRMAR en comentarios — se asume de descripción |

---

## IONF-1061 — Ledger de Consumo Unificado
**[https://app.clickup.com/t/86e1pzz9h](https://app.clickup.com/t/86e1pzz9h)**
**Estado final:** `prototype review`

### Comentarios de Actividad

| Fecha | Autor | Contenido clave |
|-------|-------|----------------|
| 2026-06-08T19:29 | Enrique Vicente | Implementación del ledger — extensión del trabajo de Rodolfo Merlo |

### Detalles del comentario de Enrique (2026-06-08)

> Se extendió el esquema base trabajado por @Rodolfo Merlo Ali con nuevas columnas:
>
> - **`measure`**: `absolute` (límite reiniciado externamente, ej. webhook o admin), `daily/weekly/etc` (se reinicia según periodo definido — ej: rate limit de 100 créditos/día independiente del measure absolute)
> - **`available`**: hard limit; una vez alcanzado se restringe el uso (flows dejan de funcionar, no se pueden crear más templates, etc.)
> - **`empty`**: campo calculado desde `available` y `consumed` — facilita las restricciones
> - **`reset_at`**: indica cuándo debe reiniciarse el consumo — controlado mediante **cron job**, independiente de reinicios por suscripción. Un `measure = absolute` siempre tiene `null`
>
> La función `services.RecordConsumption` orquesta toda la lógica internamente sin alterar el contrato de registros anteriores.

### DISCREPANCIA CRÍTICA DETECTADA

| # | AC Descripción | Decisión Comentario | Divergencia |
|---|---|---|---|
| D-IONF1061-01 | "Sin crons" (según prototipo) | Enrique 08-jun: `reset_at` **"será controlado mediante un cron job"** | 🔴 CONTRADICCIÓN: el prototipo dice "sin crons", el comentario dice "cron job" |
| D-IONF1061-02 | "Múltiples recursos en un mismo modelo" | Confirmado: `measure` permite múltiples ventanas por feature | ✅ Alineado |
| D-IONF1061-03 | "Auditable e idempotente" | `RecordConsumption` mantiene contrato para registros anteriores | ✅ Alineado |
| D-IONF1061-04 | "Reusar sistema existente de Rodolfo" | Confirmado: se extendió el esquema de Rodolfo Merlo Ali | ✅ Alineado |

**RIESGO CRÍTICO DETECTADO:**
> Comentario de Enrique (08-jun) menciona "cron job" para manejar `reset_at`. El prototipo final (12-jun) dice explícitamente "Sin crons: los webhooks de Stripe gobiernan el ciclo de vida y los reinicios son perezosos". **Posible evolución del diseño entre el 08-jun y el 12-jun** — la versión del prototipo del 12-jun es la más reciente y debe considerarse la fuente de verdad.

---

## IONF-1062 — Integración Stripe y Facturación Overage
**[https://app.clickup.com/t/86e1pzz9j](https://app.clickup.com/t/86e1pzz9j)**
**Estado final:** `prototype review`

### Comentarios de Actividad

| Fecha | Autor | Contenido clave |
|-------|-------|----------------|
| 2026-06-11T13:05 | Enrique Vicente | Estrategia Stripe Billing Meters + reglas de overage |

### Detalles del comentario de Enrique (2026-06-11)

> Se utilizará **Stripe Billing Meters** para medir el monto a cobrar al usuario:
> - El cobro de overage se hará **mensualmente**, independientemente del plan adquirido (mensual, trimestral, anual)
> - Solo se reportará a Stripe los consumos **por encima del uso incluido en plan** (simplificar modelo y evitar llamadas innecesarias)
> - Solo features que tienen asociado un **producto de Stripe** son elegibles para activar overage
> - Si un pago no se completa, **queda bloqueada la opción de activar overage** hasta que se complete el pago pendiente — sin alterar el estado de la suscripción
> - Toda actividad dentro del ciclo queda registrada en `subscription_renewals` (kind: base/overage, events: payment_succeeded/payment_failed/downgraded/upgraded, invoices, period_start, period_end)

### Divergencias encontradas

| # | AC Descripción | Decisión Comentario | Divergencia |
|---|---|---|---|
| D-IONF1062-01 | "Overage en siguiente factura" (AC original) | Enrique: Stripe Billing Meters (in arrears mensualmente, misma suscripción) | ✅ Alineado — mecanismo confirmado |
| D-IONF1062-02 | "Agrupación por recurso" | Stripe Billing Meters separa por `event_name = overage_<slug>` | ✅ Alineado |
| D-IONF1062-03 | "Billing owner flexible (company/user)" | Sin mención en comentario — asumido del AC original | ❓ SIN CONFIRMAR en comentarios |
| D-IONF1062-04 | (no en descripción) | NUEVO: pago fallido bloquea activar overage pero **no altera la suscripción** | ℹ️ AC NUEVO — comportamiento específico importante |
| D-IONF1062-05 | "Solo features con producto Stripe son elegibles para overage" | Enrique: confirmado — sin producto Stripe asociado → no puede activar overage | ℹ️ IMPORTANTE para testing |

---

## RESUMEN CONSOLIDADO DE DIVERGENCIAS

### 🔴 CRÍTICAS (requieren aclaración antes de avanzar)

| ID | Ticket | Divergencia | Pregunta para el equipo |
|----|--------|-------------|------------------------|
| C-01 | IONF-1056 + IONF-1058 | **Grace execution**: descripción dice "1 ejecución de gracia"; comentarios de IONF-1058 describen bloqueo directo sin mencionar grace. ¿Está implementada la grace execution? | ¿La grace execution está implementada en el prototipo actual o quedó fuera del scope del prototipo? |
| C-02 | IONF-1061 | **Crons vs Lazy**: comentario del 08-jun dice "cron job"; prototipo del 12-jun dice "sin crons, resets perezosos". ¿Cuál es el estado actual del código? | ¿El cron mencionado en el comentario del 08-jun fue eliminado en favor del lazy reset? |

### ⚠️ IMPORTANTES (documentar y monitorear)

| ID | Ticket | Divergencia |
|----|--------|-------------|
| I-01 | IONF-1057 | Visualización de runtime history en Board **pendiente** por rediseño de UI |
| I-02 | IONF-1057 | Fallback "estado neutro" cuando no hay histórico — no confirmado en comentarios |
| I-03 | IONF-1058 | Template/body de emails **por definirse** — diseño no finalizado |
| I-04 | IONF-1059 | Pantalla comercial unificada — sin comentarios de validación de implementación |
| I-05 | IONF-1060 | Dependencia con **Rodolfo Merlo** no documentada en AC formal |
| I-06 | IONF-1062 | Pago fallido bloquea activar overage (sin alterar suscripción) — comportamiento nuevo importante |

### ✅ ALINEADOS (AC vigentes confirmados por comentarios)

| AC | Confirmado en |
|----|--------------|
| Una suscripción por empresa, free auto-aprovisionado | Enrique 12-jun (parent) |
| Bloqueo si CUALQUIER ventana se agota | Enrique 12-jun (parent) + prototipo |
| Stripe Billing Meters para overage | Enrique 11-jun (IONF-1062) + 12-jun (parent) |
| Overage mensual in arrears independiente del plan | Enrique 11-jun (IONF-1062) |
| -1 = ilimitado (nunca bloquea, nunca cobra) | Prototipo + comentarios |
| execution_time: bloquea en editor y live, respeta schedules/webhooks | Enrique 09-jun (IONF-1058) |
| pdf_templates: quota en creación | Enrique 09-jun (IONF-1058) |
| pdf_impressions: fallo mid-execution del nodo | Enrique 09-jun (IONF-1058) |
| Emails: 80%, 100%, agotado overage | Enrique 09-jun (IONF-1058) |
| Layout de email unificado IonFlow | Enrique 11-jun (IONF-1058) |
| RecordConsumption orquesta sin alterar contrato anterior | Enrique 08-jun (IONF-1061) |
| subscription_renewals: audit log de ciclo de vida | Enrique 11-jun (IONF-1062) |

---

## AC FINALES RECONCILIADOS

> Las siguientes son las fuentes de verdad para el Paso 3 (Risk Triage).
> Precedencia: Prototipo doc (12-jun) > Comentarios recientes > Descripción original

### Suscripción y provisioning
- **AC-R-01**: Una suscripción por empresa; plan `free` auto-aprovisionado al crear company
- **AC-R-02**: Entidad de cobro puede ser company o user (billing owner flexible)
- **AC-R-03**: El estado de suscripción se deriva de `canceled_at` y `expires_at` — NO existe columna `status`

### Consumo y ventanas
- **AC-R-04**: Medición por ventanas múltiples (ej. mensual + diaria simultáneas); `period_unit = NULL` = absoluto, nunca reinicia
- **AC-R-05**: Resets son **lazy** (al leer/escribir cuando vence `reset_at`) — no cron de billing
- **AC-R-06**: Una feature se bloquea si CUALQUIER ventana se agota
- **AC-R-07**: `-1` = ilimitado; nunca bloquea, nunca genera overage

### Enforcement (por tipo de feature)
- **AC-R-08**: `execution_time`: bloquea en editor y live; no elimina schedules ni webhooks
- **AC-R-09**: `pdf_templates`: controla creación hasta el límite (quota absoluta)
- **AC-R-10**: `pdf_impressions`: el nodo PDF falla inmediatamente mid-execution al superar límite
- **AC-R-11**: ~~Grace execution~~ — **PENDIENTE DE CONFIRMAR** con el equipo
- **AC-R-12**: Guard fail-open: error de infra → se permite la ejecución

### Notificaciones
- **AC-R-13**: Emails al 80%, 100% y al agotar overage — solo email, sin in-app
- **AC-R-14**: Al 80% se invita a activar overage para no detener flows
- **AC-R-15**: Layout IonFlow unificado; body/template final **pendiente de definir**

### Overage y Stripe
- **AC-R-16**: Overage vía Stripe Billing Meters; evento `overage_<slug>` con idempotencia `fcl:<log_id>`
- **AC-R-17**: Solo features con producto Stripe asociado son elegibles para overage
- **AC-R-18**: Overage se cobra mensualmente in arrears, independiente del intervalo del plan base
- **AC-R-19**: Pago fallido bloquea activar overage (sin alterar estado de suscripción)
- **AC-R-20**: payment_failed revoca TODO el overage activo y abre dunning
- **AC-R-21**: subscription.deleted → DowngradeToFree (plan free, sin acceso pagado)

### IONPDF
- **AC-R-22**: IONPDF puede comprarse standalone sin IONFLOW
- **AC-R-23**: IONPDF standalone incluye bolsa de segundos (menor que IONFLOW) para ejecutar templates
- **AC-R-24**: Clientes IONFLOW pueden agregar IONPDF como add-on mensual
- **AC-R-25**: IONPDF = motor de generación documental, no OCR

### Runtime History (IONF-1057)
- **AC-R-26**: Se muestra solo la duración de la última ejecución completada (sin promedio ni predicción)
- **AC-R-27**: Duración registra `active_seconds` + `idle_seconds` separados (idle incluye Timer nodes y subflow `waitForResponse`)
- **AC-R-28**: Si no hay histórico → mostrar estado neutro (no confirmado en comentarios — ❓)
- **AC-R-29**: Visualización en Board **pendiente** por rediseño de UI
