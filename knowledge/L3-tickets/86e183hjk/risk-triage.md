# Risk Triage — 86e183hjk
# [POC-GTW] Desacoplar envío de chunks de órdenes a ShipEdgeCore del ciclo HTTP síncrono

> Modo: **Discovery**
> Generado: 2026-07-06
> Estado del ticket: `test matrix`

---

## Contexto Rápido

El ticket implementa un **motor de delivery genérico y configurable por app** en el repo `gateway` (PHP/Laravel).
En lugar del `Http::post()` síncrono hardcodeado, cada app puede elegir entre **Webhook** (default, retrocompatible) y **RabbitMQ** como transporte de entrega de chunks de órdenes.
Hubo **2 iteraciones** del Developer documentadas en comentarios:

- **Iteración 1 (2026-06-25)**: Motor base Webhook + RabbitMQ, configuración por app, frontend del form.
- **Iteración 2 (2026-07-01)**: Test de conexión del broker, Static params por app, Compresión zlib del payload.

---

## Áreas de Riesgo

### 🔴 CRÍTICO

| # | Área | Riesgo | Justificación |
|---|------|--------|---------------|
| R-001 | **Retrocompatibilidad del transporte Webhook** | Apps sin configuración modificada podrían romperse si el motor de delivery tiene un bug en el path default | La mayoría de apps existentes usan webhook HTTP; cualquier regresión los deja sin integración |
| R-002 | **Entrega de órdenes vía RabbitMQ** | Si el `RabbitDriver::publish()` falla silenciosamente, Gateway marcará la entrega como exitosa pero Core no recibirá los chunks | Pérdida de datos de órdenes sin error visible |
| R-003 | **Enmascaramiento de credenciales AMQP** | Si `connection_uri` se expone en claro en respuestas de API, hay un leak de credenciales de producción | Riesgo de seguridad directo |

### 🟠 ALTO

| # | Área | Riesgo | Justificación |
|---|------|--------|---------------|
| R-004 | **Test de conexión del broker (throttle)** | Endpoint `POST /api/2.0/user/apps/test-connection` sin throttle o con throttle mal configurado puede ser abusado | Rate limit de 10/min declarado; verificar que el 429 se devuelve correctamente |
| R-005 | **Static params — colisión con campos reservados** | Keys como `account`, `type`, `data` son campos del envelope; si llegan como static params, el comportamiento es indefinido | Corrupción del payload entregado a Core |
| R-006 | **Compresión zlib — coordinación con Core** | Si un integrador activa la compresión antes de que Core soporte descomprimir, los mensajes llegarán corruptos | Blocker para Core hasta que implemente `gzuncompress()` |
| R-007 | **Resolución de ruta (resolveRoute)** | Si los overrides por acción no se aplican correctamente, `get_orders` podría ir por webhook en lugar de rabbit (o viceversa) | Entrega incorrecta sin error visible |
| R-008 | **Cierre de conexiones AMQP** | Si el canal AMQP no se cierra garantizadamente por job/request, se generan connection leaks en el broker | Degradación del broker en producción |

### 🟡 MEDIO

| # | Área | Riesgo | Justificación |
|---|------|--------|---------------|
| R-009 | **Validación inline de static params en frontend** | Keys duplicadas, keys inválidas o values vacíos deben bloquearse en el form antes del submit | UX degradada si la validación solo ocurre en backend |
| R-010 | **Logs de RabbitDriver** | Si el log incluye el payload completo o la credencial, hay un leak de datos sensibles en `storage/logs` | Seguridad de datos sensibles |
| R-011 | **Default transport RabbitMQ (todas las acciones)** | Con default=Rabbit y sin overrides, **todas** las acciones van a rabbit incluyendo eventos no-get_orders | Comportamiento inesperado para el developer si no entiende el alcance |
| R-012 | **Validación del connection_uri al guardar** | URI malformado debe ser rechazado con 422 claro, no un TypeError | Experiencia del integrador degradada |

### 🟢 BAJO

| # | Área | Riesgo | Justificación |
|---|------|--------|---------------|
| R-013 | **Logs de webhook legacy** | Logs anteriores marcaban como "no enviado" un publish exitoso a Rabbit | Solo confusión en observabilidad, no falla funcional |
| R-014 | **Form — botón Check con URI enmascarado** | Al editar una app existente, el URI se muestra `amqp://user:***@host`; tocar Check debe probar la credencial real guardada del lado servidor | UX edge case delicado |

---

## Módulos Impactados

| Módulo | Tipo de impacto | Nivel |
|--------|----------------|-------|
| **Developer Apps** (form de config) | Directo — frontend y configuración | 🔴 |
| **Integrations / WebhooksController** | Directo — lógica de entrega | 🔴 |
| **Gateway API** (nuevo endpoint test-connection) | Directo — nuevo endpoint | 🟠 |
| **ShipEdgeCore** (coordinado) | Indirecto — consumidor de mensajes rabbit y payloads comprimidos | 🟠 |

---

## Preguntas para el Developer (Rodolfo) — Formato Abierto

> ⚠️ Estas son preguntas de QA para enriquecer el análisis, NO objeciones.

1. **R-002**: Cuando `RabbitDriver::publish()` falla (broker caído, credenciales expiradas), ¿qué sucede con el job `IntegrationActionJob`? ¿Lanza excepción, reintenta, o el chunk se pierde silenciosamente?

2. **R-006**: Para la compresión, ¿existe ya coordinación confirmada con el equipo de Core (ticket NCORE-3240) para que soporten `gzuncompress()`? ¿Hay un timeline? ¿Debería estar bloqueado el checkbox en UI hasta que Core esté listo?

3. **R-007**: En el `resolveRoute()`, ¿los overrides son por **nombre de proceso** exacto? ¿Hay case sensitivity? ¿Qué pasa si hay un proceso con nombre similar?

4. **R-008**: El cierre garantizado de canal AMQP, ¿es un destructor/finally del driver, o un hook de Laravel (terminated, etc.)? ¿Hay tests automáticos que validen esto?

5. **R-010**: ¿El log del `RabbitDriver` filtra el payload completo? El comentario dice "sin filtrar el payload ni la credencial" — ¿las 50 órdenes quedan en el log?

---

## Edge Cases Potenciales

| # | Caso | Módulo |
|---|------|--------|
| EC-001 | App con override `get_orders → Rabbit` pero Connection URI vacío → disparar get_orders | Developer Apps + Delivery |
| EC-002 | Cambiar transport de Rabbit → Webhook en una app activa con mensajes en cola | Delivery + Core |
| EC-003 | Static param con key `account` (reservada) — frontend bloquea, ¿la API también? | Gateway API |
| EC-004 | Más de 20 static params enviados directamente vía API (bypass del frontend) | Gateway API |
| EC-005 | Compresión ON + transport Webhook: header `Content-Encoding: deflate` en Core sin soporte | Delivery + Core |
| EC-006 | Múltiples apps con Rabbit activo simultáneamente → colas por-app no se mezclan | RabbitMQ |
| EC-007 | Check connection con URI enmascarado → check usa credencial guardada, no el string enmascarado | test-connection endpoint |

---

## Estado

> ⏳ **Pendiente aprobación del QA Engineer**

---

## Riesgos Adicionales — Identificados en Code Review (SEÑAL-09)

### 🔴 CRÍTICO

| # | Área | Riesgo | Evidencia en código |
|---|------|--------|---------------------|
| R-015 | **Doble entrega: deliver() + webhook legacy simultáneos** | En `WebhooksController::sendWebhook()`, si `$integration->app` existe, `deliver()` ya envía el payload. El código no hace early return y continúa hacia el webhook legacy. Si la integración tiene ambas configuraciones activas, el mismo payload (ej. 50 órdenes) se entrega **dos veces** a Core | `WebhooksController.php`: `deliver()` se llama sin `return`, el switch-case legacy sigue ejecutándose |

### 🟠 ALTO (actualización de riesgos existentes)

| # | Actualización |
|---|---------------|
| R-008 | **Confirmado en código**: `RabbitDriver::send()` no tiene try/finally — el canal AMQP puede quedar abierto si `queue_declare()` o `basic_publish()` fallan antes del `$channel->close()` |
| R-002 | **Matizado**: el fallo del RabbitDriver **no es silencioso** — la excepción sube al job. Pero con `tries=1`, el job va directo a `failed_jobs` sin reintento. La recuperación depende 100% del re-poll de Core |

### 🟡 MEDIO (señales pendientes de respuesta)

| # | Señal | Estado |
|---|-------|--------|
| SEÑAL-03 | Validación de `static_params` y `connection_uri` no encontrada en el `AppController::update()` | ⚠️ Pendiente respuesta del Developer — puede estar en un FormRequest no revisado |
| SEÑAL-04 | Features de Iteración 2 (Check button, static params, compresión) no encontrados en `AppEdit.vue` | ⚠️ Pendiente respuesta del Developer — puede estar en otro componente/PR |

