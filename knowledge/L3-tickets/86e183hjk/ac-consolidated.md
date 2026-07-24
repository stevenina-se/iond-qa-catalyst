# AC Consolidados — 86e183hjk
# [POC-GTW] Desacoplar envío de chunks de órdenes a ShipEdgeCore del ciclo HTTP síncrono

> Modo: **Discovery**
> Generado: 2026-07-06
> Tipo de ticket: Refactor / POC

---

## Nota Importante

> ⚠️ Este ticket es un **POC/Refactor** (tipo: Refactor) y NO tenía AC formales en la descripción original.
> Los Entregables originales + las instrucciones de QA detalladas por el Developer en los comentarios
> constituyen los AC funcionales reales. Se han reconciliado ambas fuentes.

---

## Tabla de Reconciliación (AC Originales vs Comentarios)

| AC Original (Entregables) | Decisión en Comentarios | AC Reconciliado | Fuente |
|---|---|---|---|
| Documento de evaluación con tabla comparativa | No mencionado en comentarios — ya entregado implícitamente | **AC-0** (informativo): Documento de evaluación existente | Descripción |
| POC modificando `WebhooksController::sendWebhook()` | Developer optó por **Alternativa A** (RabbitMQ directo). Comentario Paulo 2026-06-08: "Se optará por la opción A". Segunda iteración añade test-connection, static params y compresión | **AC consolidados abajo** | Comentario Paulo 2026-06-08 + Comentarios Rodolfo 2026-06-25 y 2026-07-01 |
| Video 5-10 min demostrando POC end-to-end | No mencionado en comentarios post-iteración 2 | **AC-10** (fuera de scope de QA): evidencia ya provista por Developer | Descripción original |

---

## AC Finales Consolidados

### Grupo 1 — Motor de Delivery y Transporte

**AC-01**: El form de configuración de una Developer App permite seleccionar un **Default Transport** (`Webhook` o `RabbitMQ`), agregar **overrides por acción** (nombre de acción + transporte + queue opcional) y configurar una **RabbitMQ Connection URI** por app.
> Fuente: Comentario Rodolfo 2026-06-25 (Iteración 1)

**AC-02**: Cuando el Default Transport es **Webhook** y no hay overrides, un `get_orders` se entrega por HTTP POST exactamente igual que antes del ticket (100% retrocompatible). No hay cambio de comportamiento observable.
> Fuente: Comentario Rodolfo 2026-06-25 + QA Instructions Step 1

**AC-03**: Cuando se configura un override `get_orders → RabbitMQ` con Connection URI válido, el chunk de órdenes aparece en la cola `get_orders` del broker RabbitMQ. El resto de acciones/eventos continúan por webhook.
> Fuente: Comentario Rodolfo 2026-06-25 + QA Instructions Step 2 y 3

**AC-04**: Cuando el Default Transport es **RabbitMQ** y no hay overrides, **todas** las acciones/eventos se entregan a rabbit (cola = nombre de la acción).
> Fuente: Comentario Rodolfo 2026-06-25 + QA Instructions Step 4

---

### Grupo 2 — Seguridad de Credenciales

**AC-05**: Al consultar el detalle de una app por API (`GET /api/2.0/user/apps/{appId}`), el campo `connection_uri` llega **enmascarado** (`amqp://user:***@host`). La password nunca aparece en claro en las respuestas API.
> Fuente: Comentario Rodolfo 2026-06-25 + QA Instructions Step 5

**AC-06**: Al editar una app con URI ya configurado y guardar sin modificar el URI, la credencial no se corrompe (se preserva la password original en BD).
> Fuente: Comentario Rodolfo 2026-06-25 + QA Instructions Step 5

---

### Grupo 3 — Validaciones (Iteración 1)

**AC-07**: Si se intenta elegir RabbitMQ sin proporcionar `Connection URI`, el form **bloquea el submit**. Si el payload llega al backend sin URI, responde con un error claro (no un TypeError).
> Fuente: Comentario Rodolfo 2026-06-25 + QA Instructions Step 6

**AC-08**: Los webhooks legacy (`config['webhooks']`) y logs de eventos siguen funcionando correctamente. Un publish exitoso a rabbit NO aparece como "no enviado" en los logs.
> Fuente: Comentario Rodolfo 2026-06-25 + QA Instructions Step 7

---

### Grupo 4 — Test de Conexión al Broker (Iteración 2)

**AC-09**: El form muestra un botón **"Check"** al lado del campo Connection URI. Al hacer click con URI válido y broker activo → el botón queda **verde** con tooltip "Connection successful". Con URI inválido o broker caído → **rojo** con detalle del error en tooltip.
> Fuente: Comentario Rodolfo 2026-07-01 + QA Instructions Step 1

**AC-10**: Con el campo Connection URI vacío, el botón Check queda **deshabilitado**. Al modificar el URI o reabrir el form, el estado del botón vuelve a neutro.
> Fuente: Comentario Rodolfo 2026-07-01 + QA Instructions Step 1

**AC-11**: Al editar una app con URI enmascarado (`amqp://user:***@host`) y presionar Check **sin modificar el URI**, el sistema prueba la conectividad usando la credencial real guardada en BD (no el string enmascarado). La password nunca aparece en la respuesta ni en mensajes de error.
> Fuente: Comentario Rodolfo 2026-07-01 + QA Instructions Step 2

**AC-12**: El endpoint `POST /api/2.0/user/apps/test-connection` está throttleado a **10 requests/minuto**. Al superar el límite, responde con HTTP **429**. Después de esperar 1 minuto, el endpoint vuelve a funcionar.
> Fuente: Comentario Rodolfo 2026-07-01 + QA Instructions Step 7

---

### Grupo 5 — Static Parameters (Iteración 2)

**AC-13**: El form permite agregar **static parameters** (pares key/value). Al disparar cualquier acción, estos parámetros aparecen como campos **top-level** en el payload entregado (junto a `account`, `type`, `data`), tanto por webhook como por rabbit.
> Fuente: Comentario Rodolfo 2026-07-01 + QA Instructions Step 3

**AC-14 (tipado)**: Los valores de static params se tipan automáticamente: values numéricos llegan como `number`, values de texto como `string`.
> Fuente: QA Instructions Step 3

**AC-15 (validaciones del form)**: El form bloquea y muestra mensajes de error para: key duplicada, key reservada (`account`, `type`, `data`), key inválida (ej. `123` — debe ser tipo identificador), y value vacío (al hacer submit). Las tres primeras se validan al instante; el value vacío tras submit con mensaje del backend.
> Fuente: Comentario Rodolfo 2026-07-01 + QA Instructions Step 4

---

### Grupo 6 — Compresión de Payload (Iteración 2)

**AC-16**: El form incluye un checkbox **"Send payload compressed (zlib)"**. Al activarlo y disparar una acción:
- Por **RabbitMQ**: el mensaje trae `content_encoding: deflate` y el body se puede descomprimir con `gzuncompress()` al JSON original.
- Por **Webhook**: el POST incluye header `Content-Encoding: deflate`.
> Fuente: Comentario Rodolfo 2026-07-01 + QA Instructions Step 5

**AC-17**: Con el checkbox de compresión **desactivado**, el mensaje/request es **idéntico** al comportamiento actual (sin header/propiedad adicional, JSON plano). No hay diferencia observable.
> Fuente: Comentario Rodolfo 2026-07-01 + QA Instructions Step 6

---

## Resumen de AC por Prioridad

| AC | Descripción Breve | Prioridad | Grupo |
|----|------------------|-----------|-------|
| AC-02 | Retrocompatibilidad webhook default | 🔴 Crítico | Motor |
| AC-03 | Entrega por RabbitMQ con override | 🔴 Crítico | Motor |
| AC-05 | Credenciales enmascaradas en API | 🔴 Crítico | Seguridad |
| AC-01 | Form con configuración de transporte | 🟠 Alto | Motor |
| AC-04 | Default RabbitMQ todas las acciones | 🟠 Alto | Motor |
| AC-06 | Edición sin corrupción de credencial | 🟠 Alto | Seguridad |
| AC-07 | Validación URI obligatorio | 🟠 Alto | Validaciones |
| AC-09 | Check connection verde/rojo | 🟠 Alto | Test Broker |
| AC-11 | Check con URI enmascarado | 🟠 Alto | Test Broker |
| AC-12 | Throttle 429 en test-connection | 🟠 Alto | Test Broker |
| AC-13 | Static params top-level en payload | 🟠 Alto | Static Params |
| AC-15 | Validaciones del form static params | 🟠 Alto | Static Params |
| AC-08 | Webhooks legacy sin regresión | 🟡 Medio | Regresión |
| AC-10 | Botón Check deshabilitado sin URI | 🟡 Medio | Test Broker |
| AC-14 | Tipado de values en static params | 🟡 Medio | Static Params |
| AC-16 | Compresión zlib activada | 🟡 Medio | Compresión |
| AC-17 | Sin compresión = comportamiento actual | 🟡 Medio | Compresión |

---

## Estado

> ⏳ **Pendiente aprobación del QA Engineer**


---

## AC Adicionales — Identificados en Code Review

> Los siguientes AC surgieron del análisis del código durante el Paso 3.5 (Code Review Discovery).
> Se presentan como sugerencias para acordar con el Developer antes de Deployment.

### AC-18 (PROPUESTO — pendiente acuerdo con Developer)
**Descripción**: Cuando una integración tiene `deliver()` (nuevo motor) configurado, el sistema NO vuelve a entregar el mismo payload a través del webhook legacy `configuration['webhooks']` del método `sendWebhook()`.
**Justificación**: La SEÑAL-09 del code review identificó que `WebhooksController::sendWebhook()` llama a `deliver()` pero no hace `return` — el código continúa y podría ejecutar el webhook legacy, causando doble entrega.
> Fuente: SEÑAL-09 — Code Review Discovery 2026-07-06 — `WebhooksController::sendWebhook()`

### AC-19 (PROPUESTO — pendiente confirmación de features Iteración 2 en código)
**Descripción**: Los features de Iteración 2 (botón Check, static params, checkbox de compresión) están implementados y desplegados junto con los cambios de Iteración 1 en el mismo PR o en un PR separado identificado.
**Justificación**: La SEÑAL-04 del code review no encontró estos features en el `AppEdit.vue` revisado. Podría tratarse de un componente Vue no revisado o un PR adicional.
> Fuente: SEÑAL-04 — Code Review Discovery 2026-07-06 — `AppEdit.vue`

### AC-20 (PROPUESTO — pendiente respuesta del Developer)
**Descripción**: El `RabbitDriver::send()` maneja el cierre del canal AMQP de forma garantizada (try/finally o equivalente) incluso cuando `queue_declare()` o `basic_publish()` fallan.
**Justificación**: La SEÑAL-01 identificó que el `$channel->close()` solo se llama si no hay excepción previa.
> Fuente: SEÑAL-01 — Code Review Discovery 2026-07-06 — `RabbitDriver.php`

---

## AC Rechazados o Diferidos

| AC propuesto | Estado | Razón |
|---|---|---|
| AC de validación de `static_params` en API | ⚠️ Pendiente | Validación no encontrada en `AppController::update()` — puede estar en un FormRequest no revisado (SEÑAL-03) |
| AC de `connection_uri` en schema yup | ⚠️ Diferido | Validación implementada imperativa en `onSubmit` — es funcional pero no integrada al schema (SEÑAL-08) |

