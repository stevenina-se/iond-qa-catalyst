# Test Plan — 86e183hjk
# [POC-GTW] Desacoplar envío de chunks de órdenes a ShipEdgeCore del ciclo HTTP síncrono

> Fase: **Discovery → listo para Deployment**
> Generado: 2026-07-06
> Status actual del ticket: `test matrix`
> Repos: `gateway` (PHP/Laravel) · `ion_webcomponents_flow`
> Branches: Gateway PR#4 · Webcomponents PR#4

---

## Resumen del Cambio

Se implementó un **motor de delivery genérico y configurable por app** para el repo `gateway`.
El webhook HTTP síncrono sigue siendo el transporte por defecto (100% retrocompatible).
Se añade **RabbitMQ** como transporte alternativo configurable por acción.
Segunda iteración suma: test de conexión al broker, static params inyectados en cada payload y compresión zlib opcional.

**Archivos clave afectados:**
- `app/Services/Delivery/` — factory, drivers Webhook/Rabbit, registry de conexiones AMQP
- `app/Http/Controllers/WebhooksController.php` — migrado de `sendToWebhook()` (deprecated) a `deliver()`
- Frontend: form de Developer Apps — transporte, overrides, Connection URI, Check button, static params, compresión
- Nuevo endpoint: `POST /api/2.0/user/apps/test-connection` (throttled 10/min)
- **Sin migraciones** — configuración en JSON `apps.configuration`

---

## Ambiente Requerido

| Requisito | Detalle |
|-----------|---------|
| RabbitMQ local | `docker run -d --name rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3-management` |
| RabbitMQ UI | `http://localhost:15672` (guest/guest) |
| Workers de cola | `php artisan queue:work` activo en gateway |
| Frontend built | `pnpm install && pnpm build-gateway` |
| Migraciones | **No requeridas** |
| Variables de entorno | **No requeridas** (config es per-app) |
| Coordinación Core | Para TC-027/028 (compresión), Core debe soportar `gzuncompress()` — verificar con equipo |

---

## Secuencia de Ejecución Recomendada

### FASE 1 — Smoke Tests (Ejecutar primero, son bloqueantes)

> Si alguno falla, parar y reportar antes de continuar.

| Orden | TC-ID | Descripción | Criterio de Paso |
|-------|-------|-------------|-----------------|
| 1 | TC-001 | App legacy entrega por webhook sin cambio | Payload llega igual que antes del ticket |
| 2 | TC-004 | Override get_orders → RabbitMQ funciona | Mensaje aparece en cola `get_orders` en RabbitMQ UI |
| 3 | TC-008 | connection_uri enmascarado en API | Response nunca muestra la password en claro |

---

### FASE 2 — Happy Path Funcional

| Orden | TC-ID | Descripción | Prioridad |
|-------|-------|-------------|-----------|
| 4 | TC-002 | Default=Webhook explícito | 🔴 |
| 5 | TC-005 | Otras acciones siguen por webhook con override activo | 🟠 |
| 6 | TC-006 | Default transport = RabbitMQ (todas las acciones) | 🟠 |
| 7 | TC-009 | Editar app sin corromper credencial | 🟠 |
| 8 | TC-011 | Check connection verde con broker activo | 🟠 |
| 9 | TC-016 | Check con URI enmascarado usa credencial real | 🟠 |
| 10 | TC-019 | Static params en payload webhook (tipado correcto) | 🟠 |
| 11 | TC-020 | Static params en payload RabbitMQ | 🟠 |

---

### FASE 3 — Tests Negativos y Edge Cases

| Orden | TC-ID | Descripción | Prioridad |
|-------|-------|-------------|-----------|
| 12 | TC-010 | Password no expuesta en tooltips de error | 🔴 |
| 13 | TC-012 | Check connection rojo con URI inválido | 🟠 |
| 14 | TC-013 | Check connection rojo con broker caído | 🟠 |
| 15 | TC-017 | Throttle 429 al superar 10 checks/min | 🟠 |
| 16 | TC-031 | Rabbit sin URI bloquea el form | 🟠 |
| 17 | TC-032 | URI malformado → 422 claro (no TypeError) | 🟠 |
| 18 | TC-021 | Key duplicada en static params → error inline | 🟠 |
| 19 | TC-022 | Key reservada → error inline | 🟠 |
| 20 | TC-023 | Key inválida → error inline | 🟠 |
| 21 | TC-024 | Value vacío → 422 del backend visible | 🟠 |
| 22 | TC-025 | Key reservada por API directa → 422 | 🟠 |
| 23 | TC-014 | Check deshabilitado sin URI | 🟡 |
| 24 | TC-015 | Check vuelve a neutro al editar URI | 🟡 |
| 25 | TC-026 | >20 static params por API → 422 | 🟡 |
| 26 | TC-007 | Case sensitivity en resolveRoute | 🟡 |

---

### FASE 4 — Regresión y Observabilidad

| Orden | TC-ID | Descripción | Prioridad |
|-------|-------|-------------|-----------|
| 27 | TC-003 | Webhooks legacy sin regresión | 🟡 |
| 28 | TC-018 | Throttle se restablece en 1 min | 🟡 |
| 29 | TC-034 | Log RabbitDriver sin credenciales ni payload | 🟡 |
| 30 | TC-035 | Log NO incluye 50 órdenes | 🟡 |
| 31 | TC-033 | Error 422 visible en form | 🟡 |

---

### FASE 5 — Compresión (Requiere coordinación con Core)

> ⚠️ Confirmar con el equipo de Core (ticket NCORE-3240) que soportan `gzuncompress()` antes de ejecutar.

| Orden | TC-ID | Descripción | Prioridad |
|-------|-------|-------------|-----------|
| 32 | TC-029 | Compresión OFF = comportamiento actual | 🟡 |
| 33 | TC-030 | Apps existentes default a compresión OFF | 🟡 |
| 34 | TC-027 | Compresión ON + RabbitMQ: content_encoding deflate | 🟡 |
| 35 | TC-028 | Compresión ON + Webhook: header Content-Encoding | 🟡 |

---

## Preguntas Abiertas al Developer (Antes de Deployment)

> Responder antes de cerrar el Discovery. Estas respuestas pueden agregar TCs adicionales.

| # | Pregunta | Riesgo relacionado | Urgencia |
|---|----------|--------------------|----------|
| P-01 | Cuando `RabbitDriver::publish()` falla (broker caído), ¿el job `IntegrationActionJob` lanza excepción, reintenta, o el chunk se pierde? | R-002 | 🔴 Alta |
| P-02 | ¿Hay coordinación confirmada con Core para `gzuncompress()`? ¿Timeline? ¿Debe bloquearse el checkbox en prod? | R-006 | 🟠 Media |
| P-03 | `resolveRoute()` es case sensitive al comparar nombre de proceso? | R-007 | 🟡 Baja |
| P-04 | El cierre del canal AMQP, ¿es un `finally` del driver o un hook de Laravel? | R-008 | 🟡 Baja |
| P-05 | Los logs dicen "sin filtrar el payload" — ¿las 50 órdenes quedan en `storage/logs`? | R-010 | 🟡 Baja |

---

## Criterio de Aprobación (Definition of Done para QA)

| Criterio | Estado |
|----------|--------|
| ✅ Todos los TCs de FASE 1 (Smoke) pasaron | ⏳ |
| ✅ Todos los TCs 🔴 CRÍTICO pasaron | ⏳ |
| ✅ ≥ 90% de los TCs 🟠 ALTO pasaron | ⏳ |
| ✅ Preguntas abiertas P-01 y P-02 respondidas | ⏳ |
| ✅ Sin bugs 🔴 CRÍTICO abiertos | ⏳ |
| ✅ Retrocompatibilidad webhook confirmada (TC-001, TC-002) | ⏳ |
| ✅ Credenciales AMQP nunca expuestas (TC-008, TC-010) | ⏳ |

---

## Impacto Cruzado a Monitorear en Regresión

| Módulo | Qué verificar |
|--------|--------------|
| **Developer Apps** | Form de configuración carga correctamente, CRUDs de apps no afectados |
| **Integrations** | El proceso `get_orders` completo funciona end-to-end (trigger → entrega → Core) |
| **Gateway API** | Endpoints existentes de `/2.0/user/apps` responden sin degradación |
| **ShipEdgeCore** | Coordinar con equipo de Core para validar recepción de mensajes RabbitMQ |

---

## Estado del Plan

> ⏳ **Pendiente aprobación del QA Engineer**
> Cuando sea aprobado → El ticket está listo para pasar a **Deployment**.


---

## Actualización Post-Code Review

### TCs de Code Review — Fase adicional (ejecutar en Fase 3)

| Orden | TC-ID | Descripción | Prioridad |
|-------|-------|-------------|-----------|
| 36 | TC-CR-001 | deliver() + webhook legacy no causan doble entrega | 🔴 |
| 37 | TC-CR-004 | static_params key reservada rechazada por API backend | 🟠 |
| 38 | TC-CR-006 | connection_uri requerido por API directa | 🟠 |
| 39 | TC-CR-005 | Features Iteración 2 presentes en UI | 🟠 |
| 40 | TC-CR-002 | Canal AMQP se cierra tras fallo en queue_declare | 🟠 |
| 41 | TC-CR-003 | tries=1 fallo de RabbitMQ aparece en failed_jobs | 🟠 |

### Preguntas abiertas adicionales (surgidas del code review)

| # | Pregunta | Señal | Urgencia |
|---|----------|----|----------|
| P-06 | ¿`WebhooksController::sendWebhook()` hace early return después de `deliver()` o puede ejecutar el webhook legacy simultáneamente? | SEÑAL-09 | 🔴 Alta — posible doble entrega |
| P-07 | ¿`RabbitDriver::send()` tiene un try/finally para garantizar `$channel->close()` en caso de excepción? | SEÑAL-01 | 🟠 Media |
| P-08 | ¿Los features de Iteración 2 (Check, static params, compresión) están en el PR#4 o en un PR separado? ¿En qué componente Vue? | SEÑAL-04 | 🟠 Media |
| P-09 | ¿La validación de `static_params` y `connection_uri` en backend está en un FormRequest separado, o es el `fill()->save()` sin validación? | SEÑAL-03 | 🟠 Media |

### Criterio de aprobación actualizado (incluyendo code review)

| Criterio | Estado |
|----------|--------|
| ✅ Todos los TCs de FASE 1 (Smoke) pasaron | ⏳ |
| ✅ Todos los TCs 🔴 CRÍTICO pasaron (incluido TC-CR-001) | ⏳ |
| ✅ ≥ 90% de los TCs 🟠 ALTO pasaron | ⏳ |
| ✅ P-01, P-02 y P-06 respondidas por el Developer | ⏳ |
| ✅ Sin bugs 🔴 CRÍTICO abiertos | ⏳ |
| ✅ Retrocompatibilidad webhook confirmada | ⏳ |
| ✅ Credenciales AMQP nunca expuestas | ⏳ |
| ✅ Sin doble entrega confirmada (TC-CR-001) | ⏳ |
