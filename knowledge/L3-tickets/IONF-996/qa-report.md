# QA Report — IONF-996

> Reporte final de QA generado por `sprint-testing/report`
> Fecha: 2026-06-04
> QA Engineer: Steve Nina

## Información del Ticket

| Campo | Valor |
|-------|-------|
| Ticket ID | IONF-996 |
| Título | Endpoints de Instalación de Grapps (API-First) |
| Módulos | Connections, Integrations, Accounts |
| Branch | IONF-996 |
| Entorno | dev-app.ionflow.io |
| Browser | N/A (API Testing — Postman) |
| QA Engineer | Steve Nina |
| Fecha de testing | 2026-06-04 |

---

## Veredicto

| Campo | Valor |
|-------|-------|
| Sugerencia del Catalyst | ✅ APPROVED |
| **Veredicto final (QA Engineer)** | **⬜ Pendiente firma** |
| Firmado por | |
| Fecha | |

---

## Narrativa del Feature

### ¿Qué se construyó?

Se implementaron endpoints API de alcance **app-scope (M2M)** que permiten a aplicaciones externas (como Omnio) gestionar **connections** e **instalar grapps** en cuentas de clientes de forma programática, sin depender de la interfaz de usuario de Ion.

El cambio introduce:
1. **CRUD completo de Connections** — 5 endpoints bajo `/api/2.0/app/accounts/{account:remote_id}/connections` para crear, leer, listar, actualizar y eliminar conexiones con credenciales encriptadas.
2. **Instalación de Integrations (Grapps)** — 1 endpoint `POST` bajo `/api/2.0/app/accounts/{account:remote_id}/integrations` que crea el registro de integración y retorna `integration_id` + `gateway_key`.
3. **4 nuevos scopes OAuth** — `app:connection-read`, `app:connection-create`, `app:connection-update`, `app:connection-delete` registrados en `AuthServiceProvider`.
4. **ConnectionM2MResource** — Nuevo resource que serializa connections con fidelidad JSON y nunca expone el campo `connection` (secreto encriptado) en los responses.

### ¿Por qué es importante?

Las aplicaciones externas (apps de terceros) necesitan poder gestionar connections y grapps de sus clientes de forma programática mediante autenticación Client Credentials (OAuth2), sin requerir un usuario interactivo. Anteriormente, la creación y gestión de connections y la instalación de grapps solo estaba disponible a través del webcomponent (interfaz de usuario).

Este cambio habilita la **automatización completa del flujo de onboarding**: una app externa puede crear una cuenta, instalar un grapp, y configurar connections con credenciales encriptadas, todo vía API. Esto es clave para el modelo de negocio de Grapps como integraciones instalables por terceros.

### Arquitectura del cambio

- **Backend (PHP/Laravel)**: 5 métodos nuevos en `ConnectionController` + 1 en `IntegrationController`. Rutas en grupo `app-scope` con middleware `auth.app` (client_credentials).
- **Persistencia**: Columna `connection` encriptada vía trait `Encryptable`, con espejo en columna `data`. El runtime Go lee `connection` para autenticar.
- **Seguridad**: `app_id` se deriva del token M2M (no del body). Campos protegidos (`id`, `account_id`, `created_at`) no son mass-assignable. Account viene del binding de ruta (`remote_id`), no del payload.
- **Correcciones (MR #566)**: Se agregó `app_name` como campo requerido para connections, filtrado por app en listado, y validación de asociación app↔service en todo el CRUD.

---

## Resultados de Testing

### Resumen Ejecutivo

| Métrica | Valor |
|---------|-------|
| Total de casos ejecutados | 30 |
| Casos aprobados | 30 |
| Casos fallidos | 0 |
| Casos parciales | 0 |
| Casos saltados | 0 |
| **Tasa de aprobación** | **100%** |
| Bugs encontrados | 0 |
| Bugs bloqueantes (🔴) | 0 |

### Evaluación contra Criterios

| Criterio | Requerido | Resultado | Cumple |
|----------|-----------|-----------|--------|
| Smoke tests | 100% | 3/3 (100%) | ✅ |
| Happy path | 100% | 7/7 (100%) | ✅ |
| Edge cases | ≥80% | 7/7 (100%) | ✅ |
| Negativos | 100% | 9/9 (100%) | ✅ |
| Regresión | 100% | 6/6 (100%) | ✅ |
| Bugs 🔴 abiertos | 0 | 0 | ✅ |

---

## Verificación por Funcionalidad

### AC-1 — CRUD de Connections (app-scope M2M)
**API > `GET/POST/PUT/DELETE` > `/api/2.0/app/accounts/{remote_id}/connections`**

Ahora es posible gestionar connections de forma programática vía API con autenticación M2M (client_credentials). Las aplicaciones externas pueden crear connections con credenciales encriptadas, consultarlas (sin exponer secretos), actualizarlas parcialmente (preservando el secreto si no se envía), y eliminarlas.

Ahora se cuenta con:
- Listado paginado con soporte de `per_page`, `order_by` y `order_direction`. Verificado que la paginación funciona correctamente con metadata de total y por página
- Detalle de connection individual que retorna `name`, `service_id`, `data` y `metadata`. El campo `connection` (secreto encriptado) **nunca se expone** en los responses
- Creación de connections con campos `name`, `app_name`, `data`, `connection` y `metadata`. En BD: columna `connection` encriptada, columna `data` como espejo
- Actualización parcial que preserva el secreto original cuando no se envía campo `connection`. Verificado que el update sin secreto no lo borra ni pone null
- Eliminación con verificación posterior: GET tras DELETE retorna 404 correctamente
- Preservación de tipos JSON (numbers, booleans, arrays, objetos anidados) sin casteo a string
- Aceptación de payloads JSON grandes con anidamiento profundo

| ID | Escenario | Resultado | Detalle |
|----|-----------|-----------|---------|
| TC-001 | Listar connections de un account | ✅ PASS | 200 OK — lista paginada, campo `connection` no expuesto |
| TC-002 | Ver detalle de connection | ✅ PASS | 200 OK — campos name, service_id, data, metadata presentes |
| TC-003 | Crear connection con todos los campos | ✅ PASS | 201 Created — secreto encriptado en BD, data espejo |
| TC-004 | Actualizar CON nuevo secreto | ✅ PASS | 200 OK — secreto re-encriptado con nuevo valor |
| TC-005 | Actualizar SIN secreto → preserva original | ✅ PASS | 200 OK — secreto original preservado |
| TC-006 | Eliminar connection | ✅ PASS | 200/204 — GET posterior retorna 404 |
| TC-008 | Listar con paginación | ✅ PASS | per_page=2, order_by=name, order_direction=asc |
| TC-009 | Crear sin campo data (opcional) | ✅ PASS | 201 Created sin error |
| TC-010 | Crear sin campo metadata (opcional) | ✅ PASS | 201 Created sin error |
| TC-013 | Actualizar solo name | ✅ PASS | Campos restantes preservados |
| TC-014 | JSON grande en data y metadata | ✅ PASS | Payload grande aceptado y preservado |
| TC-015 | Preservación de tipos JSON | ✅ PASS | Tipos preservados exactamente |

### AC-2 — Instalación de Integrations (Grapps)
**API > `POST` > `/api/2.0/app/accounts/{remote_id}/integrations`**

Ahora es posible instalar grapps (integrations) en cuentas de clientes de forma programática. El endpoint recibe `service_id` y `name`, crea el registro de integración con configuración vacía (`{}`), y retorna el `integration_id` junto con el `gateway_key` necesario para operaciones posteriores.

Ahora se cuenta con:
- Instalación de integración con payload mínimo (solo `service_id` + `name`), retornando `integration_id` y `gateway_key`
- Configuración inicial vacía (`{}`) que se completa vía wizard posterior
- Account derivado del binding de ruta (`remote_id`), app derivada del token M2M

| ID | Escenario | Resultado | Detalle |
|----|-----------|-----------|---------|
| TC-007 | Instalar integración (grapp) para un account | ✅ PASS | 201 Created — integration_id + gateway_key retornados |
| TC-011 | Instalar grapp con payload mínimo | ✅ PASS | Solo service_id + name → config vacía `{}` |
| TC-012 | Listar connections de account vacío | ✅ PASS | 200 OK — lista vacía sin error |

### AC-3/AC-4 — Seguridad y Autorización
**API > Autenticación M2M > Scopes > Mass Assignment**

Ahora se cuenta con protección completa contra accesos no autorizados y manipulación de datos protegidos:
- Token M2M requerido para todas las operaciones. Sin token retorna 401 Unauthorized
- Scopes granulares enforced: un token con solo `app:connection-read` no puede crear connections (403 Forbidden)
- Campos protegidos (`id`, `account_id`, `created_at`) son ignorados en el payload — el sistema genera ID automáticamente y toma `account_id` del binding de ruta
- El `app_id` de una integración se resuelve del token M2M, **no** del body del request. Intentos de inyectar un `app_id` falso son ignorados

| ID | Escenario | Resultado | Detalle |
|----|-----------|-----------|---------|
| TC-023 | Acceso sin token | ✅ PASS | 401 Unauthorized — sin stack trace |
| TC-018 | Scope incorrecto (solo read → intenta create) | ✅ PASS | 403 Forbidden |
| TC-022 | Mass assignment (id, account_id, created_at inyectados) | ✅ PASS | Campos ignorados, ID auto-generado |
| TC-024 | App viene del token, NO del body | ✅ PASS | app_id del body ignorado |

### AC-5/AC-6 — Validaciones y Manejo de Errores
**API > Validación de campos > Recursos inexistentes**

Ahora se cuenta con validaciones robustas en los endpoints:
- Campos requeridos validados: `service_id` para integrations, `name` para connections, retornando 422 con mensaje descriptivo
- Recursos inexistentes retornan 404 sin exponer stack traces ni información interna del servidor
- Operaciones (GET, PUT, DELETE) sobre connections inexistentes retornan 404 de forma consistente

| ID | Escenario | Resultado | Detalle |
|----|-----------|-----------|---------|
| TC-016 | Crear connection sin service_id | ✅ PASS | 422 — error de validación |
| TC-017 | Crear connection sin name | ✅ PASS | 422 — error de validación |
| TC-019 | Account inexistente | ✅ PASS | 404 — sin stack trace |
| TC-020 | Connection inexistente (GET/PUT/DELETE) | ✅ PASS | 404 para cada operación |
| TC-021 | Integración sin service_id | ✅ PASS | 422 — validación falla |

### Regresión — Funcionalidad existente no afectada

Se verificó que los nuevos endpoints y scopes no impactan negativamente las rutas y funcionalidades existentes del sistema.

**Tenant Routes > Connections**
Ahora se cuenta con la verificación de que el CRUD de connections vía rutas tenant (`/1.0/tenants/{tenant}/app-connections`) sigue funcionando correctamente, sin interferencia de las nuevas rutas app-scope.

**Webcomponent > Integrations**
Ahora se cuenta con la verificación de que los endpoints webcomponent de integrations (`/2.0/webcomponent/integrations`) siguen retornando datos correctos sin error.

**App API > Integrations existentes**
Ahora se cuenta con la verificación de que los endpoints existentes de integrations bajo app-scope (GET, action, update, delete) no se vieron afectados por el nuevo endpoint de instalación.

**OAuth > Scopes existentes**
Ahora se cuenta con la verificación de que la generación de tokens con scopes pre-existentes sigue funcionando. Los 4 nuevos scopes (`app:connection-*`) no interfieren con los scopes existentes del sistema.

**Go Runtime > Columna connection**
Ahora se cuenta con la verificación de que el runtime Go puede leer y desencriptar connections creadas mediante los nuevos endpoints. La columna `connection` se encripta correctamente vía trait `Encryptable`, manteniendo compatibilidad con el motor de ejecución.

**Legacy > Integrations v1.0**
Ahora se cuenta con la verificación de que los endpoints legacy de integrations (v1.0) siguen creándose correctamente con `user_id`. La relajación de la validación de `user_id` (de required a nullable) no rompió el flujo existente.

| ID | Caso | Resultado | Detalle |
|----|------|-----------|---------|
| REG-001 | CRUD tenant connections | ✅ PASS | Rutas tenant sin regresión |
| REG-002 | Webcomponent integrations | ✅ PASS | Endpoints webcomponent OK |
| REG-003 | App API integrations existentes | ✅ PASS | GET, action, update, delete sin afectación |
| REG-004 | OAuth tokens con scopes existentes | ✅ PASS | Nuevos scopes no interfieren |
| REG-005 | Go runtime lee connections nuevas | ✅ PASS | Columna `connection` encriptada correctamente |
| REG-006 | Legacy integrations v1.0 | ✅ PASS | user_id nullable no rompe legacy |

---

## Bugs Encontrados

**No se encontraron bugs durante la sesión de testing.** 🎉

---

## Conclusión

Los endpoints de instalación de grapps y gestión de connections operan correctamente en todos los escenarios verificados. El CRUD completo de connections — desde la creación con credenciales encriptadas hasta la eliminación — cumple con los requisitos de seguridad y funcionalidad. La instalación de integraciones vía API retorna correctamente el `integration_id` y `gateway_key` necesarios para el flujo posterior del wizard.

Las protecciones de seguridad más críticas fueron verificadas: la columna `connection` nunca se expone en responses, los campos protegidos no son mass-assignable, el `app_id` se resuelve del token M2M y los scopes OAuth se enforzan correctamente. La funcionalidad existente del sistema (rutas tenant, webcomponent, app API, legacy y Go runtime) no se vio afectada por los cambios.

**Ahora las aplicaciones externas (como Omnio) pueden instalar grapps y configurar connections con credenciales encriptadas de forma completamente programática vía API M2M, habilitando la automatización del flujo de onboarding sin depender de la UI de Ion.**

---

## Comentario Preparado para ClickUp

> El siguiente comentario está listo para que el QA Engineer lo revise y publique en ClickUp.

```
Estimado @Gustavo Mamani

El resultado de pruebas para este ticket es: **APROBADO ✅**

**Ticket**: IONF-996 — Endpoints de Instalación de Grapps (API-First)
**Módulos**: Connections, Integrations, Accounts
**QA Engineer**: Steve Nina
**Fecha**: 2026-06-04

### Resumen de Testing
- Casos ejecutados: 30 (24 funcionales + 6 regresión)
- Casos aprobados: 30
- Tasa de aprobación: 100%
- Bugs encontrados: 0

---

### AC-1. CRUD de Connections (app-scope M2M). API > `/api/2.0/app/accounts/{remote_id}/connections`
Ahora es posible gestionar connections de forma programática vía API con autenticación M2M
(client_credentials). Las aplicaciones externas pueden crear connections con credenciales
encriptadas, consultarlas (sin exponer secretos), actualizarlas parcialmente (preservando el
secreto si no se envía), y eliminarlas.

Ahora se cuenta con:
- Listado paginado con soporte de `per_page`, `order_by` y `order_direction` funcional
- Detalle de connection individual que retorna name, service_id, data y metadata. El campo
  `connection` (secreto encriptado) nunca se expone en los responses
- Creación con campos name, app_name, data, connection y metadata. En BD: columna connection
  encriptada, columna data como espejo del valor para consulta
- Actualización parcial que preserva el secreto original cuando no se envía campo connection
- Eliminación con verificación posterior: GET tras DELETE retorna 404 correctamente
- Preservación de fidelidad JSON (numbers, booleans, arrays, objetos anidados) sin casteo

### AC-2. Instalación de Integrations (Grapps). API > `POST /api/2.0/app/accounts/{remote_id}/integrations`
Ahora es posible instalar grapps en cuentas de clientes de forma programática. El endpoint recibe
service_id y name, crea el registro de integración con configuración vacía ({}), y retorna el
integration_id junto con el gateway_key necesario para operaciones posteriores del wizard.

Ahora se cuenta con:
- Instalación con payload mínimo (service_id + name), retornando integration_id y gateway_key
- Account del binding de ruta (remote_id), app derivada del token M2M (no del body)
- Configuración inicial vacía que se completa vía el wizard posterior

### AC-3/AC-4. Seguridad y Autorización
Ahora se cuenta con protección completa contra accesos no autorizados y manipulación de datos:
- Token M2M requerido (401 sin token). Scopes granulares enforced (403 con scope insuficiente)
- Campos protegidos (id, account_id, created_at) ignorados en el payload — mass assignment protegido
- app_id de integración se resuelve del token M2M, no del body del request

### AC-5/AC-6. Validaciones y Manejo de Errores
Ahora se cuenta con validaciones robustas:
- Campos requeridos (service_id, name) validados con 422 y mensaje descriptivo
- Recursos inexistentes retornan 404 sin exponer stack traces
- 4 nuevos scopes OAuth (app:connection-read/create/update/delete) registrados y funcionales

### Regresión
Se verificó que los cambios no impactan funcionalidad existente:
- **Tenant routes**: CRUD de connections vía rutas tenant sigue funcionando
- **Webcomponent**: Endpoints de integrations siguen retornando datos correctos
- **App API existente**: Endpoints existentes (GET, action, update, delete) sin afectación
- **OAuth**: Tokens con scopes pre-existentes siguen funcionando, nuevos scopes no interfieren
- **Go runtime**: Lee y desencripta correctamente connections creadas por nuevos endpoints
- **Legacy v1.0**: Integrations con user_id siguen creándose (validación relajada no rompe legacy)

Las aplicaciones externas ahora pueden instalar grapps y configurar connections con credenciales
encriptadas de forma programática vía API M2M, habilitando la automatización del onboarding.

| Details | |
|---------|---|
| BROWSER | N/A (API Testing — Postman) |
| BRANCH | IONF-996 |
| ENV | dev-app.ionflow.io |
| TEST MATRIX | 30 test cases |
| MERGE REQUEST | YES |
```

---

## Información de Entorno

| Details | |
|---------|---|
| BROWSER | N/A (API Testing — Postman) |
| BRANCH | IONF-996 |
| ENV | dev-app.ionflow.io |
| TEST MATRIX | knowledge/L3-tickets/IONF-996/test-matrix.md |
| MERGE REQUEST | [MR #564](https://gitlab.com/altacrest/integrations/gateway/-/merge_requests/564), [MR #566](https://gitlab.com/altacrest/integrations/gateway/-/merge_requests/566) |
