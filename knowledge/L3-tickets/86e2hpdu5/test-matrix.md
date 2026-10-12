# Test Matrix — 86e2hpdu5 (CLICKPOST Block Billing)

> **Ticket:** CLICKPOST - Implementar conteo de uso y plan mensual por bloques de tracking
> **Generado:** 2026-09-16 | **QA Engineer:** Steve Nina
> **Basado en:** ac-consolidated.md (13 AC) + risk-triage.md (10 riesgos, 18 edge cases)

---

## Resumen

- **Total de casos:** 42
- **Happy path:** 13
- **Edge cases:** 12
- **Negativos:** 8
- **Regresión:** 9
- **Automatizables:** 35 (83%)
- **Require acceso al ambiente:** Todos (los boards se ejecutan vía webhook en el dev environment)

---

## Nota sobre formato de Pasos

> ⚠️ Este ticket opera enteramente sobre **boards de ionflow** (no hay vistas UI dedicadas).
> Los pasos se ejecutan vía **webhook calls** al ambiente dev, no vía navegación de UI.
> Formato: `Webhook: POST <board-endpoint> > Payload: {...} > Verify: <resultado>`
> Para administración: `Navigate: dev-app.ionflow.io > Company Login > Sidebar: Boards > ...`

---

## Test Matrix

### BLOQUE 1 — Conteo de Uso y Deduplicación (AC-1 a AC-5, AC-10)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-001 | clickpost-usage | AC-2 | Happy Path | Registrar primer tracking único para un contrato activo | Contrato activo con 1 bloque, 0 trackings usados | Webhook: POST clickpost-usage/count > Payload: {"tracking_number": "1Z999AA1012345", "contract_id": "<id>"} > Verify: response.counted = true | Contador mensual incrementa a 1, registro de auditoría con `counted`, tracking normalizado almacenado | 🔴 | ✅ | ⬜ |
| TC-002 | clickpost-usage | AC-3 | Happy Path | Duplicado dentro de 120 días — mismo mes | TC-001 ejecutado, tracking ya registrado | Webhook: POST clickpost-usage/count > Payload: {"tracking_number": "1Z999AA1012345", "contract_id": "<id>"} > Verify: response.duplicate = true | NO incrementa contador, registro con `duplicate`, flow continúa operativo | 🔴 | ✅ | ⬜ |
| TC-003 | clickpost-usage | AC-3 | Edge Case | Duplicado dentro de 120 días — cruzando mes | Tracking registrado en mes anterior (hace < 120 días) | Webhook: POST clickpost-usage/count > Payload: {"tracking_number": "1Z999AA1012345"} > Verify: response.duplicate = true, periodo actual sin incremento | NO incrementa el contador del nuevo mes, evidencia de duplicado cross-month | 🔴 | ✅ | ⬜ |
| TC-004 | clickpost-usage | AC-4 | Happy Path | Tracking reutilizado después de 120 días | Tracking registrado hace > 120 días | Webhook: POST clickpost-usage/count > Payload: {"tracking_number": "1Z999AA1012345"} > Verify: response.counted = true, nuevo registro en periodo vigente | Se contabiliza como nueva alta, incrementa contador | 🔴 | ✅ | ⬜ |
| TC-005 | clickpost-usage | AC-5 | Edge Case | Concurrencia — 2 requests simultáneos del mismo tracking | Tracking no registrado previamente | 2x Webhook SIMULTÁNEOS: POST clickpost-usage/count > Payload: {"tracking_number": "NEW_TRACKING_001"} > Verify: solo 1 con counted=true | Solo uno incrementa el contador, el otro queda como `duplicate` | 🔴 | ✅ | ⬜ |
| TC-006 | clickpost-usage | AC-10 | Happy Path | Normalización — tracking con espacios, guiones y minúsculas | Contrato activo | Webhook: POST clickpost-usage/count > Payload: {"tracking_number": "1z 999-aa1 012"} > Verify: tracking almacenado como "1Z999AA1012" | Se normaliza a mayúsculas sin espacios ni guiones, dedupe aplica sobre valor normalizado | 🟠 | ✅ | ⬜ |
| TC-007 | clickpost-usage | AC-10 | Negativo | Tracking vacío o solo espacios | Contrato activo | Webhook: POST clickpost-usage/count > Payload: {"tracking_number": "   "} > Verify: error o rechazo | Rechazado con error claro, no incrementa contador | 🟠 | ✅ | ⬜ |
| TC-008 | clickpost-usage | AC-4 | Edge Case | Tracking exactamente al día 120 — ¿nuevo o duplicado? | Tracking registrado hace exactamente 120 días | Webhook: POST clickpost-usage/count > Payload: {"tracking_number": "<tracking_120_days>"} > Verify: comportamiento definido (counted o duplicate) | Verificar si el día 120 cuenta como dentro o fuera de la ventana. Documentar comportamiento | 🟠 | ✅ | ⬜ |

### BLOQUE 2 — Alertas 80% y 100% (AC-9)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-009 | clickpost-alerts | AC-9 | Happy Path | Alerta de 80% al alcanzar 4000 trackings | Contrato con 1 bloque (5000 cap), 3999 trackings usados | Webhook: POST clickpost-usage/count > Payload: tracking #4000 > Verify: alerta 80% enviada por email + webhook a Shipedge y ClickPost | Alerta de 80% enviada una sola vez a ambas partes | 🔴 | ✅ | ⬜ |
| TC-010 | clickpost-alerts | AC-2 | Happy Path | Alerta de 100% al alcanzar 5000 trackings — servicio continúa | Contrato con 1 bloque, 4999 trackings usados | Webhook: POST clickpost-usage/count > Payload: tracking #5000 > Verify: alerta 100% + tracking #5001 procesado normalmente | Alerta 100% enviada, servicio NO se interrumpe, tracking #5001 se procesa | 🔴 | ✅ | ⬜ |
| TC-011 | clickpost-alerts | AC-9 | Edge Case | Alerta idempotente — reintento no duplica envío | Alerta de 80% ya enviada en el periodo | Webhook: POST clickpost-alerts/retry > Verify: no se envía segunda alerta, intento trazable | NO se envía segunda alerta exitosa, intento queda registrado | 🟠 | ✅ | ⬜ |
| TC-012 | clickpost-alerts | AC-9 | Negativo | Fallo en envío de email de alerta | SMTP credentials inválidas o servicio caído | Webhook: POST clickpost-usage/count > Payload: tracking que dispara alerta > Verify: fallo registrado, reintento posible | Intento fallido registrado, no duplica entregas exitosas previas | 🟠 | ✅ | ⬜ |
| TC-013 | clickpost-alerts | AC-9 | Edge Case | Nuevo periodo — alerta permitida nuevamente | Periodo anterior con alerta 80% enviada, nuevo periodo iniciado | Webhook: POST clickpost-usage/count > Payload: tracking #4000 del NUEVO periodo > Verify: nueva alerta 80% | Nueva alerta se envía en el nuevo periodo (reset de flag) | 🟠 | ✅ | ⬜ |

### BLOQUE 3 — Cierre Mensual y Auto-upgrade (AC-1, AC-6, AC-12)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-014 | clickpost-billing-cycle | AC-1 | Happy Path | Cierre con exceso — auto-upgrade a 2 bloques | 1 bloque activo, 7200 trackings únicos registrados | Webhook: POST clickpost-billing-cycle/close > Payload: {"force": true} > Verify: periodo cerrado, 2 bloques activos, factura $100 | Mes cerrado a $50. Siguiente ciclo: 2 bloques, 10000 cap, factura $100, notificación de upgrade | 🔴 | ✅ | ⬜ |
| TC-015 | clickpost-billing-cycle | AC-1 | Edge Case | Cierre con exactamente 5000 trackings | 1 bloque activo, 5000 trackings exactos | Webhook: POST clickpost-billing-cycle/close > Payload: {"force": true} > Verify: 1 bloque conservado, factura $50 | Plan conserva 1 bloque (ceil(5000/5000) = 1), no hay upgrade | 🟠 | ✅ | ⬜ |
| TC-016 | clickpost-billing-cycle | AC-1 | Edge Case | Cierre con 10001 trackings — requiere 3 bloques | 1 bloque activo, 10001 trackings | Webhook: POST clickpost-billing-cycle/close > Payload: {"force": true} > Verify: 3 bloques activos | ceil(10001/5000) = 3 bloques, factura $150 | 🟠 | ✅ | ⬜ |
| TC-017 | clickpost-billing-cycle | AC-6 | Happy Path | Consumo menor — bloques persisten sin downgrade automático | 2 bloques activos, 3000 trackings usados, sin solicitud de reducción | Webhook: POST clickpost-billing-cycle/close > Payload: {"force": true} > Verify: 2 bloques conservados | Plan conserva 2 bloques, factura $100. Sin downgrade automático | 🔴 | ✅ | ⬜ |
| TC-018 | clickpost-billing-cycle | AC-12 | Edge Case | Job reintentado — idempotencia del cierre | Cierre mensual ya ejecutado para el periodo | Webhook: POST clickpost-billing-cycle/close > Payload: {"force": true} > Verify: sin doble upgrade, sin doble factura | Sin doble upgrade, sin doble factura, sin doble notificación | 🔴 | ✅ | ⬜ |
| TC-019 | clickpost-billing-cycle | AC-12 | Edge Case | Día 1 perdido + retry webhook | El daily schedule no ejecutó el cierre el día 1 | Webhook: POST clickpost-billing-cycle/retry > Verify: cierre se ejecuta correctamente sin periodo duplicado | Cierre se ejecuta, periodo correcto cerrado, sin duplicados | 🟠 | ✅ | ⬜ |
| TC-020 | clickpost-billing-cycle | AC-1 | Negativo | Cierre con 0 trackings — mínimo 1 bloque | 1 bloque activo, 0 trackings usados | Webhook: POST clickpost-billing-cycle/close > Payload: {"force": true} > Verify: 1 bloque conservado | max(1, ceil(0/5000)) = 1. Plan conserva 1 bloque | 🟡 | ✅ | ⬜ |

### BLOQUE 4 — Facturación Invoice Ninja (AC-11)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-021 | clickpost-invoicing | AC-11 | Happy Path | Factura creada y enviada al cierre | Cierre mensual completado exitosamente | Verify tras TC-014: factura CP-<período> creada en Invoice Ninja > Email enviado | Factura con ID correcto, monto correcto, enviada por email | 🟠 | ✅ | ⬜ |
| TC-022 | clickpost-invoicing | AC-11 | Edge Case | Reintento de facturación — no duplicar | Factura ya creada para el periodo | Webhook: POST clickpost-invoicing/retry > Verify: no factura duplicada | Número de factura único previene duplicación | 🟠 | ✅ | ⬜ |
| TC-023 | clickpost-invoicing | AC-11 | Negativo | API de Invoice Ninja caída | Invoice Ninja no disponible | Webhook: POST clickpost-billing-cycle/close > Simular fallo API > Verify: fallo auditado | Fallo auditado, re-emisión posible vía retry, mes NO se re-cierra | 🟠 | ✅ | ⬜ |

### BLOQUE 5 — Solicitudes de Reducción / Downgrade (AC-7, AC-8)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-024 | clickpost-contract-admin | AC-7 | Happy Path | Registrar solicitud de reducción | Contrato con 2 bloques activos | Webhook: POST clickpost-contract-admin/reduction > Payload: {"target_blocks": 1, "requester": "ClickPost", "evidence": "..."} > Verify: solicitud registrada | Solicitud registrada con fecha, actor, bloques solicitados. Estado: pendiente. 30 días de espera | 🟠 | ✅ | ⬜ |
| TC-025 | clickpost-contract-admin | AC-7 | Happy Path | Downgrade elegible aplicado en renovación | Solicitud con 30+ días, uso del periodo permite reducción | Webhook: POST clickpost-billing-cycle/close > Verify: plan reducido a 1 bloque, factura $50, notificación | Plan se reduce, ambas partes notificadas con confirmación | 🟠 | ✅ | ⬜ |
| TC-026 | clickpost-contract-admin | AC-8 | Edge Case | Downgrade impedido por capacidad requerida | Solicitud elegible a 1 bloque, pero uso = 7200 trackings | Webhook: POST clickpost-billing-cycle/close > Verify: plan conserva 2 bloques | Capacidad tiene precedencia, se registra el motivo, ambas partes notificadas | 🟠 | ✅ | ⬜ |
| TC-027 | clickpost-contract-admin | AC-7 | Edge Case | Solicitud antes de 30 días — no se aplica | Solicitud registrada hace 15 días | Webhook: POST clickpost-billing-cycle/close > Verify: plan sin cambio | No se aplica aún, queda pendiente hasta elegibilidad | 🟡 | ✅ | ⬜ |
| TC-028 | clickpost-contract-admin | AC-7 | Negativo | Intentar reducir por debajo de 1 bloque | Contrato con 1 bloque | Webhook: POST clickpost-contract-admin/reduction > Payload: {"target_blocks": 0} > Verify: rechazado | No se permite. Mínimo comercial = 1 bloque | 🟡 | ✅ | ⬜ |
| TC-029 | clickpost-contract-admin | — | Happy Path | Cancelar solicitud de reducción | Solicitud pendiente activa | Webhook: POST clickpost-contract-admin/admin > Payload: {"action": "cancel_reduction", "reduction_id": "<id>"} > Verify: cancelada con trazabilidad | Solicitud cancelada, registro de quién y cuándo | 🟡 | ✅ | ⬜ |

### BLOQUE 6 — Contrato y Separación Contable

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-030 | clickpost-contract-admin | — | Happy Path | Crear contrato con metadata completa | Ambiente dev configurado | Webhook: POST clickpost-contract-admin/admin > Payload: contrato con active_blocks, unit_size, price, currency, timezone | Contrato activo con todos los campos correctos | 🟠 | ✅ | ⬜ |
| TC-031 | clickpost-usage | — | Happy Path | Verificar separación contable vs ledger IOND | Contrato ClickPost activo, billing IOND activo | Registrar trackings en contrato ClickPost > Verify: datos NO aparecen en feature_consumptions de billing IOND | Circuitos de consumo aislados | 🟠 | ✅ | ⬜ |

### BLOQUE 7 — Reporte Auditable

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-032 | clickpost-usage | — | Happy Path | Consultar reporte de uso | Trackings registrados en periodo activo | Webhook: POST clickpost-usage/report > Verify: reporte con conteo, periodos, audit trail | Reporte contiene: contrato, periodo, uso, bloques, trazabilidad completa | 🟠 | ✅ | ⬜ |
| TC-033 | clickpost-usage | — | Edge Case | Reporte tras cierre mensual con upgrade | Cierre completado con auto-upgrade | Webhook: POST clickpost-usage/report > Verify: evidencia del cálculo | Reporte incluye: uso anterior, bloques antes, bloques después, importe, motivo | 🟡 | ✅ | ⬜ |

---

## Casos de Regresión

| ID | Módulo Impactado | AC | Caso de Regresión | Por Qué Podría Romperse | Pasos | Prioridad | Automatizable | Estado |
|----|-----------------|-----|-------------------|------------------------|-------|-----------|---------------|--------|
| REG-001 | Webhooks | AC-13 | Webhook EXISTENTE sin API key sigue aceptando requests | Enforce de `X-Ion-Apikey` es nuevo — podría romper webhooks preexistentes | Navigate: dev-app.ionflow.io > Company Login > Sidebar: Boards > Click [Flow existente con webhook trigger] > Enviar POST al webhook sin header X-Ion-Apikey > Verify: request procesado normalmente | 🔴 | ✅ | ⬜ |
| REG-002 | Webhooks | AC-13 | Webhook CON API key rechaza request sin header | La nueva funcionalidad debe funcionar correctamente | Configurar webhook con API key > Enviar POST sin X-Ion-Apikey > Verify: request rechazado antes de parsear body | 🔴 | ✅ | ⬜ |
| REG-003 | Webhooks | AC-13 | Webhook CON API key acepta request con key válida | Flujo completo con API key | Configurar webhook con API key > Enviar POST con X-Ion-Apikey correcto > Verify: flow ejecutado normalmente | 🔴 | ✅ | ⬜ |
| REG-004 | Nodes (Send Email) | — | Send Email node — envío con SMTP válido | Nodo nuevo en plataforma — verificar que funciona | Navigate: dev-app.ionflow.io > Company Login > Sidebar: Boards > Crear flow con Send Email node > Configurar SMTP > Ejecutar > Verify: email recibido | 🟠 | ✅ | ⬜ |
| REG-005 | Nodes (Send Email) | — | Send Email node — error con SMTP inválido | Error handles tipificados deben funcionar | Navigate: dev-app.ionflow.io > Company Login > Sidebar: Boards > Flow con Send Email node > SMTP credentials inválidas > Ejecutar > Verify: error handle activado con clasificación (dial/auth/timeout) | 🟠 | ✅ | ⬜ |
| REG-006 | Keys | — | Crear credential tipo `smtp` desde el catalogue | Nuevo tipo de key — UI debe renderizarlo | Navigate: dev-app.ionflow.io > Company Login > Sidebar: Boards > Canvas: Click [Send Email node] > Drawer: Button "Add credential" > Verify: formulario SMTP visible | 🟠 | ✅ | ⬜ |
| REG-007 | gateway (OpenApiMapper) | — | Importar spec OAS 3 con `$ref` y `requestBody` | Refactor del parser — specs existentes no deben romperse | Navigate: dev-app.ionflow.io > Admin Login > Crear App Connector > Import OpenAPI spec con $ref > Verify: parámetros resueltos correctamente | 🟠 | ✅ | ⬜ |
| REG-008 | IONF-1152 | — | Flow de tracking ClickPost-USPS sigue funcionando | Integración del conteo podría romper el flow operativo | Ejecutar flow IONF-1152 end-to-end > Verify: tracking sincronizado correctamente | 🟠 | ❌ | ⬜ |
| REG-009 | Boards | — | Flow existente con schedule trigger sigue ejecutándose | Cambios en plataforma no deben afectar schedules existentes | Navigate: dev-app.ionflow.io > Verificar que un flow con schedule trigger existente se ejecuta normalmente | 🟡 | ❌ | ⬜ |

---

## Queries de Verificación BD

> ⚠️ **Nota:** Este ticket usa **Data Stores** (SQLite del cliente), NO tablas PostgreSQL directas.
> Las queries a continuación verifican los data stores vía la API de Data Store o directamente en el SQLite del tenant.
> No se basa en migraciones SQL porque los schemas son definidos como Data Structures en ionflow.

```
-- TC-001: Verificar registro de tracking en data store de usage
-- Fuente: Data Store "clickpost-usage" del tenant
Persistent Data Get > data_store: <usage_store_uuid> > key: <tracking_normalizado>
Esperado: registro con {counted: true, contract_id, period, first_billed_at, source, idempotency_key}

-- TC-002: Verificar que duplicado NO incrementó el tally
-- Fuente: Data Store "clickpost-tally" del tenant
Persistent Data Get > data_store: <tally_store_uuid> > key: <period_key>
Esperado: unique_count no incrementado respecto al valor pre-duplicado

-- TC-014: Verificar cierre mensual en data store de periodos
-- Fuente: Data Store "clickpost-periods" del tenant
Persistent Data Get > data_store: <periods_store_uuid> > key: <period_key>
Esperado: {status: "closed", unique_count: 7200, blocks_before: 1, blocks_required: 2, blocks_after: 2, amount: 100}

-- TC-024: Verificar solicitud de reducción registrada
-- Fuente: Data Store "clickpost-reductions" del tenant
Persistent Data Search > data_store: <reductions_store_uuid> > filter: {status: "pending"}
Esperado: registro con {target_blocks: 1, requester, evidence, created_at, eligible_at: created_at + 30d}

-- TC-031: Verificar separación contable
-- Fuente: PostgreSQL (billing module)
-- Migración ref: gateway/database/migrations/2026_*_create_feature_consumptions_table.php
SELECT COUNT(*) FROM feature_consumptions
WHERE subscriber_type = 'company' AND subscriber_id = <clickpost_company_id>;
-- Esperado: 0 (ClickPost no tiene entries en el billing interno de IOND)
```
