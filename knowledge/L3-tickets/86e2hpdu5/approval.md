# Template de Aprobación — 86e2hpdu5

Estimado @Enrique

**El resultado de pruebas para este ticket es: APROBADO ✅**

**Ticket**: 86e2hpdu5 — CLICKPOST - Implementar conteo de uso y plan mensual por bloques de tracking
**Módulo**: Webhooks, Keys (webhook + SMTP), Nodes (Send Email), Gateway (OpenApiMapper)
**QA Engineer**: Steve Nina
**Fecha**: 2026-09-29

### 📊 Resumen de Testing
- **Casos ejecutados**: 42 (33 funcionales + 9 regresión)
- **Casos aprobados**: 42
- **Tasa de aprobación**: 100%
- **Bugs encontrados**: 0 bloqueantes

---

### 🛠️ ¿Qué se construyó / cambió?

- **Send Email Node (`com.ion.send_email`)**: Nodo de acción nuevo para envío de emails SMTP desde flows/boards. Incluye: lookup de SMTP credentials encriptados, validación RFC 5322, clasificación de errores por etapa (dial/auth/TLS/send), quoted-printable encoding, y error handles tipificados (503/401/408/400/502).
- **Webhook API Key Protection**: Mecanismo de protección de webhooks por API key (`X-Ion-Apikey` header). Hash SHA-256 con comparación constant-time. Webhooks sin keys permanecen abiertos (backwards compatible). Header stripping post-auth para evitar que el plaintext aparezca en logs de ejecución.
- **SMTP Key Type**: Nuevo tipo de credential `smtp` con host/port/security en metadata y password encriptado en parameters. UI dedicada (`SmtpKeyFormDialog`) con formulario de creación/edición.
- **Webhook Key Management UI**: Diálogo para crear/listar/eliminar API keys por webhook. Plaintext mostrado una sola vez al crear. Columna `api_keys_count` en la tabla de webhooks con COUNT subquery.
- **OpenApiMapper**: Resolución recursiva de `$ref` (JSON Pointer), mapping de `requestBody` OAS 3 como body parameter, y guard anti-recursión para schemas circulares.
- **Connections Refactor**: Migración de 30+ archivos de la arquitectura legacy (AppCreate/AppEdit/ActionList/WebhookList) a la nueva arquitectura modular (ConnectorCreateView/ConnectorNodeEditView/ConnectorAuthEditView/ConnectorWebhookEditView) con composables dedicados.

### 💡 ¿Por qué es importante?

- **Habilita el sistema de billing por bloques de ClickPost**: Los boards de conteo, alertas, cierre mensual, facturación y downgrade dependen de la plataforma Send Email (para notificaciones), webhook API keys (para seguridad de los endpoints), y SMTP credentials (para envío de alertas/facturas). Sin estos componentes, el sistema de billing no puede operar.
- **Seguridad de webhooks**: Los endpoints de webhook de ClickPost (y cualquier webhook custom) ahora pueden protegerse con API keys, evitando que terceros envíen datos arbitrarios a los flows del tenant.
- **Autonomía de envío de email**: Los tenants ahora pueden enviar emails desde sus flows usando sus propias credenciales SMTP, sin depender de un servicio de email compartido.

---

### 🎯 Criterios de Aceptación (AC) Clave Validados

#### **AC-1. Cada bloque = 5000 trackings únicos mensuales, $50/bloque**
* **Validación realizada**: Cierre mensual con distintos niveles de uso (0, 5000, 7200, 10001 trackings)
* **Comportamiento observado**: `ceil(usage/5000)` calcula correctamente los bloques requeridos. Auto-upgrade funciona, mínimo 1 bloque. Facturas con montos correctos.

#### **AC-3. Deduplicación con ventana de 120 días**
* **Validación realizada**: Tracking duplicado mismo mes, cross-month, y post-120 días
* **Comportamiento observado**: Duplicados dentro de ventana retornan `duplicate` sin incrementar. Tracking normalizado (mayúsculas, sin espacios/guiones). Post-120 días se cuenta como nueva alta.

#### **AC-5. Concurrencia — solo un registro por tracking**
* **Validación realizada**: 10+ requests simultáneos con mismo tracking; 10+ requests con trackings distintos
* **Comportamiento observado**: Solo 1 se cuenta para el mismo tracking. Trackings distintos se cuentan correctamente (unique_count final converge aunque las respuestas individuales muestren valores stale bajo carga).

#### **AC-9. Alertas de 80% y 100% idempotentes**
* **Validación realizada**: Alerta al cruzar umbral, reintento, reset por nuevo periodo
* **Comportamiento observado**: Una sola alerta por umbral por periodo. Nuevo periodo permite nueva alerta.

#### **AC-7/AC-8. Solicitudes de reducción con período de gracia de 30 días**
* **Validación realizada**: Solicitud, elegibilidad, impedimento por capacidad, cancelación
* **Comportamiento observado**: Downgrade respeta los 30 días, la capacidad prevalece sobre la solicitud, mínimo 1 bloque.

---

### 🔄 Pruebas de Regresión
- **Webhooks existentes sin API key** (REG-001): ✅ Siguen aceptando requests sin header — backwards compatible
- **Webhook CON API key** (REG-002/003): ✅ Rechaza sin key (401), acepta con key válida
- **Send Email node** (REG-004/005): ✅ Envío exitoso con SMTP válido, error handle con SMTP inválido
- **SMTP credential creation** (REG-006): ✅ Formulario visible y funcional en la UI
- **OpenApiMapper** (REG-007): ✅ Importar spec OAS 3 con `$ref` y `requestBody` funciona
- **Flow ClickPost-USPS** (REG-008): ✅ Tracking flow operativo sin afectación
- **Schedule triggers existentes** (REG-009): ✅ Sin impacto

---

### 🔍 Code Review QA

- **Repos revisados**: flow_binaries (38 archivos), gateway-ion (220 archivos), gateway (6 archivos)
- **Hallazgos identificados**: 9 totales (🟠: 4, 🟡: 3, ✅ resolved: 3)
- **Riesgos inyectados a la Matrix**: 6 TCs creados a partir del código revisado
- **Estado**: 3 hallazgos resueltos durante la revisión (constant-time comparison confirmada, ApiKeysCount correctamente populado). Los 6 activos restantes son todos no-bloqueantes (1 BUG informativo de concurrencia en respuesta, 3 RISK menores, 1 SEC menor, 1 EDGE case UI).

### ⚠️ Observaciones

- **BUG-CR-001 (Informativo)**: Bajo alta concurrencia (5+ req/s), el `unique_count` en la respuesta del webhook puede mostrar valores stale. El dato persistido es correcto y las alertas/cierre se basan en el tally persistido. No afecta lógica de negocio.
- **RISK-CR-002**: Verificar post-merge que editar un SMTP credential dejando password vacío preserva el password existente (el FE maneja esto, pero el backend no tiene guard explícito).
- **RISK-CR-004**: Crear webhook con "Require API key" donde la creación de key falla deja el webhook sin key. Diseño consciente del developer para evitar webhooks duplicados.

### 📂 Evidencia
- **Test Matrix**: `knowledge/L3-tickets/86e2hpdu5/test-matrix.md`
- **QA Report**: `knowledge/L3-tickets/86e2hpdu5/qa-report.md`
- **Code Review QA**: `knowledge/L3-tickets/86e2hpdu5/code-review-qa.md`
- **Data Store Evidence**: Verificado vía Persistent Data Get/Search (SQLite del tenant)
- **Logs**: `responses_log.txt` (líneas 14764-14800 — evidencia de concurrencia)

---

### 📝 Conclusión de QA

La implementación del sistema de conteo de uso por bloques de tracking para ClickPost ha sido verificada exhaustivamente. Los 42 casos de test (13 happy path, 12 edge cases, 8 negativos, 9 regresión) pasaron al 100%. Los componentes de plataforma — Send Email node, webhook API key protection, SMTP credentials, y OpenApiMapper — están implementados con calidad de producción: error handling tipificado, deduplicación con normalización, idempotencia en alertas y cierre mensual, separación contable respecto al billing IOND, y backwards compatibility total con webhooks existentes. El code review identificó hallazgos menores que no afectan la aprobación. El entregable es estable y cumple con todos los criterios de aceptación documentados.

| Details | |
|---|---|
| BROWSER | Chrome / Postman |
| BRANCH | IONF-1217 |
| ENV | dev-app.ionflow.io |
| TEST MATRIX | L3-tickets/86e2hpdu5/test-matrix.md |
| MERGE REQUEST | YES |
