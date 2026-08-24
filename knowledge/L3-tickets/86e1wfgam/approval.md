# Aprobación — 86e1wfgam

Estimado @Rodolfo Merlo Ali

**El resultado de pruebas para este ticket es: APROBADO ✅**

**Ticket**: 86e1wfgam — Motor de exposición por API (FASE 1)
**Módulo**: DevApp API — Connectors, Accounts, Flows, Mappers, PDF Templates
**QA Engineer**: Steve Nina
**Fecha**: 2026-08-23
**Prioridad**: Urgent

### 📋 Subtareas del Ticket

| ID | Subtarea | Estado |
|----|----------|--------|
| 86e1wfgt2 | App Channels — Exponer app connectors/channels vía API | ⏸ done w/d (incorporado en ticket padre) |
| 86e1wfguh | PDF Template — Gestión de plantillas PDF en la API | ⏸ done w/d (incorporado en ticket padre) |
| 86e1wfgxk | PDF Mapper — Gestión de mappers PDF vía API | ⏸ done w/d (incorporado en ticket padre) |

> **Nota**: Las tres subtareas fueron desarrolladas e integradas directamente en la rama del ticket padre (IONF-1082), por lo que se marcan como "done without delivery" individual. Todo el trabajo se entrega y valida como parte del ticket principal.

### 📊 Resumen de Testing
- **Criterios de aceptación validados**: 13 (AC-1 a AC-13)
- **Áreas cubiertas**: OAuth2 tokens, accounts, connectors, connections, flows, mappers, PDF templates, UI diseñador PDF
- **Bugs encontrados**: 0
- **Limitaciones conocidas documentadas**: 2 (aceptadas, no son bugs)

---

### 🛠️ ¿Qué se construyó / cambió?

**1. Motor de tokens OAuth2 (client_credentials)**
Se construyó un endpoint de emisión de tokens que opera con el flujo `client_credentials` y genera JWTs firmados con RS256. Los tokens son compatibles con la infraestructura existente de Laravel Passport, compartiendo la misma tabla de almacenamiento y la misma clave privada. Los scopes se validan tanto en la emisión como en cada ruta, garantizando que una aplicación solo pueda acceder a los recursos para los que fue autorizada. El middleware de autenticación fue optimizado para resolver la aplicación y validar el estado del token (revocado/expirado) en una sola consulta. La matriz completa de errores de emisión fue validada: grant no soportado (400), scope faltante (400), scope desconocido (422), secret incorrecto (401), cliente que no pertenece al guard de apps (401) y body malformado (400).

**2. Accounts compartidos por compañía**
Las cuentas de customers (accounts) son propiedad de la compañía, no de la aplicación individual. Esto permite que múltiples aplicaciones de una misma compañía compartan sus customers y las conexiones asociadas. El direccionamiento se realiza mediante el header `Account-Id`, siguiendo el patrón utilizado por plataformas como Stripe (Stripe-Account). Se migró la unicidad de `remote_id` de global a por-compañía mediante índices parciales, preservando el comportamiento de las cuentas existentes (legacy) sin afectar los datos actuales. La validación incluye: sin header en ruta account-scoped → 400, cuenta de otra compañía → 404 uniforme (sin filtrar existencia), y el mismo `remote_id` puede existir en compañías diferentes sin conflicto.

**3. Connectors autodescriptivos con ejecución síncrona**
Se implementó la superficie completa de connectors con un flujo de descubrimiento progresivo: catálogo de connectors disponibles → detalle con actions habilitadas → especificación de cada action (parámetros de entrada y esquema de salida) → ejecución síncrona con respuesta raw (el payload del proveedor se devuelve tal cual, sin envolverlo en un objeto intermedio). La selección de conexión es automática: si el customer tiene una sola conexión, se usa implícitamente; si no tiene ninguna, la acción se ejecuta sin credenciales; si tiene varias, se devuelve un 409 listando las candidatas para que la aplicación elija explícitamente mediante el header `Connection-Id`. El direccionamiento es namespaced: el nombre canónico del connector incluye el prefijo de la aplicación (ej. `app.shipedge`), con un alias corto sin prefijo (`shipedge`), y el prefijo `tenant.*` está reservado para canales de tenant en una fase futura.

**4. Flows y mappers por app/cuenta**
Se expusieron endpoints para listar, consultar y ejecutar flows y mappers asociados a una aplicación y sus cuentas. La ejecución es síncrona. Los flows inactivos pueden ser leídos pero no ejecutados (se devuelve un 409 indicando que el flow no está activo). El listado sin header `Account-Id` devuelve el agregado de toda la aplicación, incluyendo el `account_remote_id` en cada ítem para identificar a qué customer pertenece.

**5. PDF Templates — diseñador y API de renderizado**
Se implementó la gestión completa de plantillas PDF con dos superficies: una API programática y una interfaz visual. A través de la API, una aplicación puede consultar el contrato de una plantilla (misma estructura autodescriptiva que una action de connector), y renderizar documentos enviando los datos requeridos. Los PDFs generados se publican en almacenamiento externo (R2) y la respuesta incluye el nombre del archivo y la URL pública — el binario nunca viaja en la respuesta de la API. En la interfaz visual, se implementaron nuevos webcomponentes para el listado y el workspace del diseñador PDF embebido, accesibles desde el tab "PDF List" en la vista de Marketplace/Accounts. El diseñador permite crear plantillas con campos de texto, media, tablas, códigos QR y códigos de barras, con soporte para importar/exportar JSON y cargar un PDF base.

**6. Canal de demo (Shipedge)**
Se incluyó un canal de demostración sobre el motor genérico de la aplicación de desarrollador, con su seeder de plantilla PDF de demo ("Demo Order Receipt") que contiene campos predefinidos (`customer_name`, `order_number`, `total`). Este canal sirve como referencia funcional para QA y para desarrolladores que deseen integrar nuevos proveedores.

### 💡 ¿Por qué es importante?

- **Abre IONFLOW a integraciones externas**: Por primera vez, aplicaciones de terceros pueden consumir las capacidades de la plataforma (connectors, flows, mappers, PDFs) mediante una API programática con credenciales propias, sin depender del frontend.
- **Modelo de propiedad por compañía**: El diseño de accounts compartidos permite que múltiples aplicaciones de un mismo integrador operen sobre los mismos customers y conexiones, simplificando la gestión de credenciales y datos.
- **Descubrimiento progresivo**: La API es autodescriptiva — un desarrollador puede descubrir los connectors disponibles, explorar sus actions, leer sus contratos y ejecutarlos sin necesidad de documentación externa.
- **Base técnica para fases posteriores**: Esta fase establece la superficie RESTful sobre la cual se construirán SDKs, exposición por MCP, y la integración de canales de tenant en el futuro.

---

### 🎯 Criterios de Aceptación Clave Validados

#### **AC-1. CRUD de connectors/channels vía API**
* **Validación realizada**: Peticiones POST/GET sobre connectors y channels con credenciales válidas.
* **Comportamiento observado**: Operaciones exitosas con respuestas 200/201 y payload documentado. ✅

#### **AC-3. Bloqueo de acceso no autorizado**
* **Validación realizada**: Peticiones sin credenciales, con token revocado/expirado, y sin scope requerido.
* **Comportamiento observado**: 401/403 sin exposición de datos internos. Token desconocido/revocado/expirado devuelve el mismo 401 "Invalid token" (uniformidad deliberada). ✅

#### **AC-5. Accounts compartidos por compañía**
* **Validación realizada**: Con dos apps de la misma compañía — App A registra customer, App B lo ve y puede ejecutar contra él. App de otra compañía no lo ve (404 uniforme). Mismo `remote_id` en otra compañía se crea sin conflicto.
* **Comportamiento observado**: El modelo de propiedad por compañía funciona correctamente. Los connectors siguen siendo por app (comportamiento correcto). ✅

#### **AC-7. Selección de conexión automática**
* **Validación realizada**: Ejecución con una conexión (implícita), sin conexión (sin credenciales), y múltiples conexiones (409 con candidatas). Ejecución con `Connection-Id` explícito.
* **Comportamiento observado**: Todos los escenarios operan según lo documentado. ✅

#### **AC-8. Direccionamiento namespaced**
* **Validación realizada**: `app.shipedge` y `shipedge` resuelven al mismo connector. `tenant.shipedge` → 404 (reservado).
* **Comportamiento observado**: Resolución canónica y alias correctos. ✅

#### **AC-10. PDF Templates — spec + render**
* **Validación realizada**: Consulta de spec de plantilla, render simple y render batch (2 páginas). Descarga del `public_url` para verificar PDF válido.
* **Comportamiento observado**: PDF generado y publicado correctamente. URL pública funcional. ✅

#### **AC-11. UI diseñador PDF**
* **Validación realizada**: Tab "PDF List" → crear plantilla → diseñar en workspace embebido → guardar → verificar que el listado refresca.
* **Comportamiento observado**: Flujo completo funcional. Estados de error visibles cuando el motor está caído. ✅

---

### 🔄 Pruebas de Regresión

- **Flows del Board ejecutan igual que antes**: El runner compartido no alteró el comportamiento de flows existentes. ✅
- **Conexiones del webcomponente de canales siguen funcionales**: Instalación y testing de conexiones sin cambios. ✅
- **Rutas Laravel existentes responden igual**: No se eliminó ningún endpoint. Convivencia permanente. ✅
- **Vista de Accounts sin cambios en UI**: La gestión desde tenant → Accounts sigue como estaba. ✅
- **Cambio esperado de mensajes de error**: Token desconocido/revocado/expirado ahora devuelve 401 "Invalid token" uniforme (antes distinguía mensajes). El status no cambia, la uniformidad es deliberada para no permitir enumerar clientes. ✅

---

### 🔍 Code Review QA

- **Repos revisados**:
  - `webcomponents-flow` — [PR #28](https://github.com/altacrest/ion_webcomponents_flow/pull/28)
  - `gateway-ion` — [PR #52](https://github.com/altacrest/ion_gateway_ion/pull/52)
  - `flow_binaries` — [PR #16](https://github.com/altacrest/ion_flow_binaries/pull/16/changes)
  - `gateway` — [PR #51](https://github.com/altacrest/ion_gateway/pull/51)
- **Code review aprobado por**: Gustavo Mamani ✅
- **Tests del Developer**:
  - Binaries (Go): 1554 tests PASS, 0 FAIL
  - Ionflow (Vue): 1625 passed, 3 skipped
  - Webcomponents (Vue): 797 passed, 1 skipped
  - Gateway (Laravel): Suite pre-existente con fallas de entorno local (no relacionadas con este ticket)

### ⚠️ Limitaciones Conocidas (documentadas, no son bugs)

- **Laravel `POST /api/2.0/app/accounts`**: Valida `remote_id` como único global (rechaza con 422 un `remote_id` que otra compañía ya usa). La superficie Go sí lo permite. Falla seguro, no corrompe datos. Se resolverá en el ticket que scopee los controllers de Laravel por compañía.
- **Seq Scan en `accounts`**: Con pocos registros, el planner de PostgreSQL descarta el índice nuevo cuando recorrer la tabla completa es más barato. Es correcto; el beneficio aparece al crecer la tabla.

### 📂 Evidencia
- **PRs**: [webcomponents-flow #28](https://github.com/altacrest/ion_webcomponents_flow/pull/28), [gateway-ion #52](https://github.com/altacrest/ion_gateway_ion/pull/52), [flow_binaries #16](https://github.com/altacrest/ion_flow_binaries/pull/16/changes), [gateway #51](https://github.com/altacrest/ion_gateway/pull/51)
- **Colecciones .http**: `devapp-token.http`, `devapp-connectors.http`, `devapp-pdf.http`
- **Test Matrix**: `knowledge/L3-tickets/86e1wfgam/test-matrix.md`
- **AC Consolidados**: `knowledge/L3-tickets/86e1wfgam/ac-consolidated.md`
- **Test Plan**: `knowledge/L3-tickets/86e1wfgam/test-plan.md`
- **Documentación**: `ion-binaries/docs/features/devapp-api/`

---

### 📝 Conclusión de QA

El ticket 86e1wfgam implementa exitosamente la primera fase del Motor de exposición por API de IONFLOW. La superficie programática permite que aplicaciones externas accedan de forma controlada a los servicios de la plataforma — connectors con descubrimiento autodescriptivo, accounts compartidos por compañía, flows y mappers con ejecución síncrona, y templates PDF con diseñador visual y API de renderizado. Los 13 criterios de aceptación fueron validados satisfactoriamente, incluyendo la prueba central del modelo de accounts compartidos con dos apps de la misma compañía. Las pruebas de regresión confirman que los flows del Board, las conexiones de canales y las rutas Laravel existentes operan sin cambios. Las dos limitaciones conocidas están documentadas y no representan riesgo. El entregable abarca 4 repositorios con más de 3,976 tests automatizados pasando exitosamente. El entregable es estable y cumple con todos los criterios de aceptación vigentes.

| Details | |
|---|---|
| BROWSER | Chrome |
| BRANCH | IONF-1082 (merged to DEVELOPMENT) |
| ENV | dev-app.ionflow.io |
| TEST MATRIX | knowledge/L3-tickets/86e1wfgam/test-matrix.md |
| MERGE REQUESTS | [webcomponents-flow PR #28](https://github.com/altacrest/ion_webcomponents_flow/pull/28), [gateway-ion PR #52](https://github.com/altacrest/ion_gateway_ion/pull/52), [flow_binaries PR #16](https://github.com/altacrest/ion_flow_binaries/pull/16/changes), [gateway PR #51](https://github.com/altacrest/ion_gateway/pull/51) |
