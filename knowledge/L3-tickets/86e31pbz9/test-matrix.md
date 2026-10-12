# Test Matrix — 86e31pbz9 (Acceso directo a compañías sin inicio de sesión como usuario)

> Generada durante Deployment (modo mínimo) — 2026-09-03
> Módulo principal: Auth (Admin > Companies > [Company])
> Repos afectados: gateway-ion, gateway, flow_binaries
> Basado en: QA Instructions del Developer + Changes and Specifications Form

---

## Resumen

| Métrica | Valor |
|---------|-------|
| Total de casos | 29 |
| Happy path | 8 |
| Edge cases | 6 |
| Negativos | 4 |
| Regresión | 6 |
| Code Review | 5 (RISK: 3, SEC: 1, EDGE: 1) |
| Automatizables | 10 (UI gateway-ion) |
| Cobertura de AC | 10/10 QA Instructions |

---

## Test Matrix

### Happy Path

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-001 | Auth | QA-3 | Happy Path | Iniciar sesión de soporte desde panel Admin | Conectado a VPN con usuario `administrator`, compañía existente con usuarios | Admin Login > Sidebar: Companies > Click [Company] > Tab: Support > Button: "Start a support session" > Verify: Redirect al dashboard de tenant de la compañía | El navegador redirige al dashboard de tenant de la compañía seleccionada. Se inicia la sesión de soporte exitosamente. | 🔴 | ✅ | ⬜ Pendiente |
| TC-002 | Auth | QA-4 | Happy Path | Banner de sesión de soporte visible con info correcta | Sesión de soporte activa (TC-001 completado) | Verify: Barra superior muestra indicador "Support session" > Verify: Nombre de la compañía visible en el banner > Verify: Botón "Leave company" visible | El indicador "Support session" aparece en la barra superior con el nombre de la compañía y el botón "Leave company" | 🔴 | ✅ | ⬜ Pendiente |
| TC-003 | Auth | QA-6 | Happy Path | Operaciones de tenant completas durante sesión de soporte | Sesión de soporte activa en una compañía con datos | Admin Login > Iniciar sesión de soporte (TC-001) > Sidebar: Boards > Verify: Workflows visibles > Sidebar: Connections > Verify: Conexiones visibles > Sidebar: Data Store > Verify: Data stores visibles | Se pueden ver todos los recursos de la compañía (workflows, conexiones, data stores) con todos los permisos durante la sesión de soporte | 🔴 | ✅ | ⬜ Pendiente |
| TC-004 | Auth | QA-7 | Happy Path | Salir de sesión de soporte via banner | Sesión de soporte activa | Click: "Leave company" en el banner > Verify: Redirect al panel de admin > Verify: Banner de sesión de soporte desaparece > Verify: Rutas de admin accesibles nuevamente | Al hacer click en "Leave company", se sale de la sesión de soporte, se redirige al panel de admin y el banner desaparece | 🔴 | ✅ | ⬜ Pendiente |
| TC-005 | Auth | QA-5 | Happy Path | Restricción de rutas admin durante sesión de soporte | Sesión de soporte activa | Admin Login > Iniciar sesión de soporte (TC-001) > Navigate: /admin/companies > Verify: Redirigido al dashboard de tenant > Navigate: /admin > Verify: Redirigido al dashboard de tenant | Mientras la sesión de soporte está activa, navegar a rutas `/admin/*` redirige al dashboard de tenant. No se puede acceder a rutas de administrador. | 🔴 | ✅ | ⬜ Pendiente |
| TC-006 | Auth | QA-2 | Happy Path | Pestaña "Support" visible en detalle de compañía | Conectado a VPN como admin | Admin Login > Sidebar: Companies > Click [Company] > Verify: Tab "Support" visible > Click: Tab "Support" > Verify: Información sobre la sesión de soporte visible > Verify: Botón "Start a support session" visible | La pestaña "Support" aparece en el detalle de la compañía (reemplaza la pestaña anterior "Users"). Muestra información clara y botón para iniciar. | 🟠 | ✅ | ⬜ Pendiente |
| TC-007 | Auth | QA-7 | Happy Path | Salir de sesión de soporte via menú de usuario | Sesión de soporte activa | Click: Menú de usuario (esquina superior derecha) > Verify: Opción "Leave company" visible > Click: "Leave company" > Verify: Redirect al panel de admin | Se puede salir de la sesión de soporte también desde el menú de usuario, no solo desde el banner | 🟠 | ✅ | ⬜ Pendiente |
| TC-008 | Auth | QA-10 | Happy Path | Verificar config VPN — variable de entorno correcta | Acceso al entorno de staging/deployment | Verify: Variable `VPN_ALLOWED_CIDRS` configurada bajo `config/vpn.php` > Verify: NO existe `config/impersonation.php` > Verify: NO existe variable `IMPERSONATION_TTL_HOURS` | La configuración migró correctamente de `impersonation` a `vpn`. Las variables antiguas ya no existen. | 🟠 | ❌ | ⬜ Pendiente |

### Edge Cases

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-009 | Auth | QA-8 | Edge Case | Multi-pestaña — sesión de soporte sincroniza entre pestañas | Sesión no activa, dos pestañas abiertas en Ionflow (mismo browser) | Pestaña 1: Admin Login > Sidebar: Companies > Click [Company] > Tab: Support > Button: "Start a support session" > Pestaña 2: Verify: Recarga automática o refleja la sesión de soporte activa | Al iniciar sesión de soporte en una pestaña, la otra pestaña debe recargar automáticamente y reflejar el estado de la sesión | 🟠 | ❌ | ⬜ Pendiente |
| TC-010 | Auth | QA-3 | Edge Case | Iniciar sesión de soporte en compañía diferente (switch) | Sesión de soporte activa en Compañía A | Estando en sesión de soporte de Compañía A > Click: "Leave company" > Sidebar: Companies > Click [Compañía B] > Tab: Support > Button: "Start a support session" > Verify: Dashboard de Compañía B | Se puede cambiar de compañía en sesión de soporte: primero salir, luego entrar a otra | 🟠 | ✅ | ⬜ Pendiente |
| TC-011 | Auth | QA-11 | Edge Case | Broadcasting — canales de compañía en sesión de soporte | Sesión de soporte activa, eventos en tiempo real disponibles | Admin Login > Iniciar sesión de soporte (TC-001) > Verify: Suscripción a canales de broadcasting de la compañía (App.Models.Company.{id}) funciona > Trigger: Evento en la compañía > Verify: Notificación recibida en tiempo real | La suscripción a canales de broadcasting de la compañía funciona correctamente durante sesión de soporte | 🟡 | ❌ | ⬜ Pendiente |
| TC-012 | Auth | N/A | Edge Case | Persistencia de sesión de soporte — recargar página | Sesión de soporte activa | Recargar la página (F5) > Verify: Sesión de soporte sigue activa > Verify: Banner visible > Verify: Dashboard de tenant de la compañía correcta | La sesión de soporte persiste después de recargar la página (almacenada en localStorage) | 🟠 | ✅ | ⬜ Pendiente |
| TC-013 | Auth | N/A | Edge Case | Cerrar y reabrir browser — sesión de soporte | Sesión de soporte activa | Cerrar el browser > Reabrir browser > Navigate: URL de Ionflow > Verify: Estado de sesión de soporte (puede o no persistir dependiendo de la implementación) | Verificar el comportamiento al cerrar/reabrir browser. Documentar si la sesión persiste o se limpia. | 🟡 | ❌ | ⬜ Pendiente |
| TC-014 | Auth | N/A | Edge Case | Navegar directamente a URL de tenant sin sesión de soporte | Admin logueado, NO en sesión de soporte | Admin Login > Navigate: /dashboard (ruta de tenant) > Verify: Comportamiento definido (redirect a /admin o acceso denegado) | Sin sesión de soporte activa, un admin no debe poder acceder directamente a rutas de tenant (solo a /admin/*) | 🟠 | ❌ | ⬜ Pendiente |

### Negativos

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-015 | Auth | QA-9 | Negativo | Sin VPN — requests de tenant devuelven 403 | Admin logueado, VPN desconectada | Desconectar VPN > Iniciar sesión de soporte o intentar request de tenant > Verify: Respuesta HTTP 403 > Verify: Mensaje de "VPN requerida" > Verify: Overlay de VPN visible en la UI | Sin VPN, cualquier request de tenant como admin devuelve 403 con mensaje de VPN requerida y se muestra el overlay de VPN | 🔴 | ❌ | ⬜ Pendiente |
| TC-016 | Auth | N/A | Negativo | Usuario no-admin intenta acceder a sesión de soporte | Logueado como usuario Company (no admin) | Company Login > Navigate: /admin/companies > Verify: Acceso denegado/redirect > Verify: No existe opción de "Support" en rutas de tenant | Un usuario con rol Company (no administrator) no puede acceder a la funcionalidad de sesión de soporte ni a rutas de admin | 🟠 | ✅ | ⬜ Pendiente |
| TC-017 | Auth | N/A | Negativo | Admin sin VPN intenta requests de tenant via API | Admin logueado, VPN desconectada, herramienta de requests HTTP | Desconectar VPN > Ejecutar request GET/POST a un endpoint de tenant (ej: /1.0/tenants/{id}/...) con cookies de admin > Verify: HTTP 403 con mensaje de VPN | El middleware `EnsureAdminAccessVpn` bloquea requests de tenant si el admin no está en la VPN, incluso con credenciales válidas | 🟠 | ❌ | ⬜ Pendiente |
| TC-018 | Auth | N/A | Negativo | Verificar eliminación completa de impersonation | Entorno deployado | Verify: Endpoint /impersonation/end NO existe (404) > Verify: Endpoint /companies/{id}/impersonate NO existe (404) > Verify: No hay referencias a "impersonate" en la UI | Las rutas y funcionalidad de impersonation fueron completamente eliminadas. No se pueden acceder. | 🟠 | ❌ | ⬜ Pendiente |

### Regresión

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| REG-001 | Auth | N/A | Regresión | Login de Admin funciona correctamente | Credenciales de admin válidas | Admin Login via Keycloak (#username, #password, #kc-login) > Verify: Redirect a panel admin > Verify: Sidebar de admin visible (Dashboard, Companies, etc.) | El login de admin no se rompió con los cambios de eliminación de impersonation | 🔴 | ✅ | ⬜ Pendiente |
| REG-002 | Auth | N/A | Regresión | Login de Company funciona correctamente | Credenciales de company válidas | Company Login via Keycloak > Verify: Redirect a dashboard de tenant > Verify: Sidebar de tenant visible (Boards, Connections, etc.) | El login de Company user no se rompió con los cambios | 🔴 | ✅ | ⬜ Pendiente |
| REG-003 | Auth | N/A | Regresión | Lista de compañías en panel admin | Admin logueado | Admin Login > Sidebar: Companies > Verify: Lista de compañías carga > Verify: Información de compañías visible (nombre, status, location) > Click [Company] > Verify: Detalle de compañía carga | La lista y detalle de compañías siguen funcionando después de eliminar impersonation | 🟠 | ✅ | ⬜ Pendiente |
| REG-004 | Auth | N/A | Regresión | Pestañas de configuración de compañía (Information, App Connectors, Boards, Subscription) | Admin en detalle de compañía | Admin Login > Sidebar: Companies > Click [Company] > Tab: Information > Verify: Información visible > Tab: App Connectors > Verify: Carga correctamente > Tab: Boards > Verify: Carga correctamente > Tab: Subscription > Verify: Carga correctamente | Las pestañas de configuración de compañía (excepto la eliminada "Users") siguen funcionando correctamente | 🟠 | ✅ | ⬜ Pendiente |
| REG-005 | Auth | N/A | Regresión | API de tenants funciona para Company users | Company user logueado, con permisos estándar | Company Login > Sidebar: Boards > Verify: Lista de flows carga > Sidebar: Connections > Verify: Conexiones cargan > Crear un recurso (ej: flow) > Verify: Creación exitosa | Las APIs de tenant siguen funcionando correctamente para users normales (no admin). Los cambios en los middlewares no afectan a users regulares. | 🔴 | ❌ | ⬜ Pendiente |
| REG-006 | Auth | N/A | Regresión | Permisos de usuario Company respetados | Company user logueado con permisos limitados | Company Login (usuario con permisos limitados) > Navigate a sección sin permiso (ej: /users si no tiene READ_USER) > Verify: Acceso denegado/redirect a forbidden | El bypass de admin en los middlewares no afecta la verificación de permisos para users regulares | 🟠 | ❌ | ⬜ Pendiente |

---

## Queries de Verificación BD

> ⚠️ No se requieren queries de BD para este ticket.
> El cambio es principalmente de arquitectura (eliminación de impersonation, adición de sesión de soporte).
> No hay migraciones de base de datos en este cambio.
> Los tokens de impersonation existentes en `oauth_access_tokens` quedarán huérfanos (el sistema ya no los lee).

---

### Code Review (TC-CR-xxx)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-CR-001 | Auth | RISK-CR-001 | Code Review | Error handler en CompanySupportSession muestra error.message crudo | Admin logueado, backend caído o compañía inválida | Admin Login > Sidebar: Companies > Click [Company inválida] > Tab: Support > Verify: toast de error muestra mensaje amigable (no técnico) | El toast de error muestra un mensaje amigable al usuario, no el error.message técnico del backend ni el objeto error completo | 🟠 | ❌ | ⬜ Pendiente |
| TC-CR-002 | Auth | RISK-CR-002 | Code Review | Aislamiento multi-tenant: user de Company A no accede a Company B | Dos companies existentes, user miembro solo de Company A | Company Login (user de Company A) > Request API: GET /1.0/tenants/{CompanyB_id}/flows > Verify: HTTP 401 "Unauthorized" | El middleware TenantConnection bloquea al usuario de Company A de acceder a datos de Company B. El bypass de admin no se aplica a users regulares. | 🟠 | ❌ | ⬜ Pendiente |
| TC-CR-003 | Auth | SEC-CR-001 | Code Review | Auditoría de acciones de admin en sesión de soporte | Admin en sesión de soporte activa | Admin Login > Iniciar sesión de soporte > Sidebar: Boards > Crear flow > Eliminar flow > Verify: ¿Existe log/registro de estas acciones del admin? | Documentar si existen logs de auditoría para acciones del admin en sesión de soporte. Si no existen, documentar como observación de seguridad. | 🟠 | ❌ | ⬜ Pendiente |
| TC-CR-004 | Auth | EDGE-CR-001 | Code Review | Timing de sync entre pestañas al iniciar sesión de soporte | Dos pestañas abiertas como admin | Pestaña 1: Iniciar sesión de soporte > Pestaña 2: Observar timing del reload > Verify: Pestaña 2 se recarga y refleja la sesión | Al iniciar sesión de soporte, el storage event dispara un reload en la otra pestaña. Verificar que no hay momento de inconsistencia visible. | 🟡 | ❌ | ⬜ Pendiente |
| TC-CR-005 | Auth | RISK-CR-003 | Code Review | Key de localStorage consistente entre módulos | Sesión de soporte activa | Iniciar sesión de soporte > Abrir DevTools > Application > localStorage > Verify: key "support_session_company" existe > Verify: sync entre pestañas funciona con esta key | La key de localStorage usada para almacenar la sesión de soporte es la misma en ambos módulos (lib/supportSession.ts y useSupportSessionSync.ts) | 🟡 | ❌ | ⬜ Pendiente |

---

## Notas

- **Prerequisito crítico**: Estar conectado a la VPN corporativa para los tests de sesión de soporte
- **Cambio de config**: `impersonation.vpn_allowed_cidrs` → `vpn.allowed_cidrs` (nuevo `config/vpn.php`)
- **Eliminaciones**: `useImpersonation`, `ImpersonationController`, `impersonation_service.go`, ~2,245 líneas eliminadas
- **Nuevo composable**: `useSupportSession` reemplaza `useImpersonation`
- **Nuevo componente**: `CompanySupportSession.vue` reemplaza `CompanyUsers.vue`
- **Nuevo middleware**: `EnsureAdminAccessVpn` reemplaza `EnforceImpersonationScope`
- **3 PRs**: gateway-ion #62, gateway #60, flow_binaries #46
