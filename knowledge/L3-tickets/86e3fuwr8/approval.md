# Template de Aprobación — 86e3fuwr8

Estimado @Rodolfo

**El resultado de pruebas para este ticket es: APROBADO ✅**

**Ticket**: 86e3fuwr8 — [SEC] Gateway — cerrar vía explotada y retirar endpoints antiguos
**Módulo**: Gateway (rutas v1/v2, middleware AccountCredentials, apps, seeders, webhooks salientes)
**QA Engineer**: Steve Nina
**Fecha**: 2026-09-29

### 📊 Resumen de Testing
- **Casos ejecutados**: 28
- **Casos aprobados**: 28
- **Tasa de aprobación**: 100%
- **Bugs encontrados**: 0

---

### 🛠️ ¿Qué se construyó / cambió?

- **Hotfix (ya en producción)**: Eliminación de los 3 endpoints mandatory v1 (`POST /api/1.0/webhooks/shop/redact`, `/customers/redact`, `/customers/data_request`) — vía explotada en el incidente del 28/09. Los flujos GDPR continúan por v2 con validación HMAC de Shopify.
- **Propiedad de integraciones v2**: Los endpoints `showApp`, `update`, `getLogs`, `destroy` y `updateStatus` ahora validan que la integración pertenece a la app y, en webcomponents, a la cuenta solicitante. Antes, cualquier app podía acceder a integraciones de otra app (incluidas credenciales del cart).
- **Rol admin en gestión v1**: El grupo de rutas `api/1.0` para `apps`, `appsetups`, `accounts`, `requests` y `factory` ahora requiere rol `superadministrator|administrator`. Las rutas operativas (`orders`, `inventory`, `shipments`) no cambian.
- **Firma HMAC-SHA256 en webhooks salientes**: Gateway firma con `base64(HMAC-SHA256(raw_body, client_secret))` usando el header `X-Gateway-Hmac-Sha256`. Apps sin OAuth client reciben el evento sin firma (documentado como `App webhook sent unsigned`).
- **Soft delete de apps**: Borrado lógico con `deleted_at`. Tokens de apps borradas retornan 401, slug reservado (no reutilizable), client protegido (409 si ligado a otra app). `migrate:rollback` funciona.
- **Seeders idempotentes**: `PassportSeeder` usa `firstOrCreate` (no duplica clients), `LaratrustSeeder` no sobrescribe contraseñas existentes del admin.

### 💡 ¿Por qué es importante?

- **Cierra la vulnerabilidad de seguridad**: La vía explotada que causó la desactivación masiva de 189 integraciones Shopify queda permanentemente eliminada. La validación de mandatorios se ejecuta únicamente por v2 con HMAC de Shopify.
- **Aislamiento entre apps y cuentas**: La validación de propiedad de integraciones evita que apps maliciosas o mal configuradas lean, modifiquen o eliminen integraciones de otros. Este control era código muerto antes del fix.
- **Trazabilidad de webhooks**: La firma HMAC permite a las apps verificar criptográficamente que un evento proviene de Gateway, cerrando la posibilidad de suplantación.
- **Resilencia operativa**: El soft delete previene integraciones huérfanas al borrar apps. Los seeders idempotentes evitan duplicación de clients Passport y reseteo de credenciales admin en cada deploy.

---

### 🎯 Criterios de Aceptación (AC) Clave Validados

#### **AC-1. Endpoints v1 mandatory retirados; v2 funciona con HMAC**
* **Validación realizada**: POST a los 3 endpoints v1 → 405. POST a v2 con HMAC válido → 200, con HMAC inválido → 401
* **Comportamiento observado**: Los endpoints legacy devuelven Method Not Allowed. La v2 procesa correctamente con validación de firma.

#### **AC-3. Propiedad de integraciones v2 — aislamiento entre apps y cuentas**
* **Validación realizada**: 6 escenarios con app A/B, cuenta X/Y, key inexistente, delete cross-app
* **Comportamiento observado**: Toda operación sobre integración ajena → 404. Las integraciones quedan intactas. Error mejorado (key inexistente ya no retorna 500).

#### **AC-5. Firma HMAC en webhooks salientes**
* **Validación realizada**: Request bin capturó header `X-Gateway-Hmac-Sha256`, recálculo manual coincide, body idéntico al formato previo
* **Comportamiento observado**: Firma correcta, retrocompatible, app sin OAuth client documentada con log.

#### **AC-6. Soft delete de apps**
* **Validación realizada**: 8 escenarios incluyendo borrado, tokens, slug reservado, client conflict, bulk update, rollback
* **Comportamiento observado**: Borrado lógico correcto, tokens revocados sin 500, migración reversible.

---

### 🔄 Pruebas de Regresión
- **Mandatory v2 (GDPR Shopify)**: ✅ Sigue procesando shop/redact solo para la integración con hostname coincidente
- **Rutas operativas v1** (orders, inventory, shipments): ✅ Sin cambio, no requieren rol admin
- **Integración propia** (showApp, update, getLogs): ✅ Funciona como antes para apps legítimas
- **Migración rollback**: ✅ `migrate:rollback --step=1` + `migrate` funciona

---

### 🔍 Code Review QA

- **Repos revisados**: gateway ([PR #87](https://github.com/altacrest/ion_gateway/pull/87))
- **Code Review by**: Joselo — ✅ APROBADO
- **Hallazgos adicionales de QA**: Ninguno — el code review del developer ya fue aprobado por Joselo

### ⚠️ Observaciones

- **Apps sin OAuth client**: Los webhooks salientes se envían sin firma HMAC. Está documentado con `App webhook sent unsigned` en logs. Es un comportamiento consciente, no un bug.
- **Seguimientos pendientes** (fuera de scope de este ticket):
  - Rutas sin auth (`GET /api/orders?gateway_key=`, receptores v1 sin HMAC, endpoints experimental/testing)
  - Proteger `/api/docs`, `/docs`, `/documentation` y `/login` con Cloudflare
  - Rotar secret de Passport expuesto en `/login`
  - Portar a `DEVELOPMENT` y `v2.0.x`
  - Limpiar 14 clients Passport duplicados en producción

### 📂 Evidencia
- **QA Report**: `knowledge/L3-tickets/86e3fuwr8/qa-report.md`
- **PR**: [PR #87](https://github.com/altacrest/ion_gateway/pull/87)
- **Incidente relacionado**: [NCORE-4273](https://app.clickup.com/t/86e3fre5w) (RCA en Shipedge Core)
- **Soporte**: [SUPP-8563](https://app.clickup.com/t/86e3fdrfa), [SUPP-8564](https://app.clickup.com/t/86e3fk4ce)

---

### 📝 Conclusión de QA

La remediación del incidente de seguridad del 28/09/2026 ha sido validada exhaustivamente. Los 28 casos de test cubren la eliminación de la vía explotada (mandatory v1), la validación de propiedad de integraciones v2, el refuerzo de roles en la gestión v1, la firma HMAC en webhooks salientes, el borrado lógico de apps y los seeders idempotentes. Todos los criterios de aceptación se cumplen al 100%. El hotfix ya desplegado cierra la vulnerabilidad inmediata y las mejoras del PR #87 endurecen sistemáticamente las capas de autenticación, autorización y trazabilidad del Gateway. El entregable es estable, seguro y listo para producción.

| Details | |
|---|---|
| BROWSER | Postman / curl |
| BRANCH | IONF-1399 |
| ENV | dev-app.ionflow.io + producción (hotfix) |
| TEST MATRIX | L3-tickets/86e3fuwr8/qa-report.md |
| MERGE REQUEST | [PR #87](https://github.com/altacrest/ion_gateway/pull/87) |
