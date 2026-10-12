Estimado @Gustavo Mamani

**El resultado de pruebas para este ticket es: APROBADO ✅**

**Ticket**: 86e31pbz9 — Acceso directo a compañías sin inicio de sesión como usuario
**Módulo**: Auth (Admin > Companies > [Company] > Support)
**QA Engineer**: Steve Nina
**Fecha**: 2026-09-03

### 📊 Resumen de Testing
- **Casos ejecutados**: 29 (8 happy path + 6 edge cases + 4 negativos + 6 regresión + 5 code review)
- **Casos aprobados**: 29
- **Tasa de aprobación**: 100%
- **Bugs encontrados**: 0

---

### 💡 ¿Por qué es importante?

- **Simplificación arquitectural**: El sistema anterior de impersonation era inherentemente complejo: generaba tokens temporales, requería un controller dedicado, un servicio de Go y PHP sincronizados, y middleware de scope enforcement. El nuevo sistema de sesión directa elimina toda esa infraestructura, reduciendo la superficie de código en ~2,245 líneas y la superficie de ataque (menos endpoints, menos tokens circulando).

- **Experiencia de soporte mejorada**: Los administradores ahora acceden directamente a las compañías con un solo clic ("Start a support session"), sin necesidad de "iniciar sesión como usuario". La sesión no expira por TTL (antes `IMPERSONATION_TTL_HOURS`), sino que persiste hasta que el admin la cierra explícitamente. El banner de sesión de soporte siempre visible previene confusión sobre en qué contexto se está operando.

- **Seguridad reforzada por VPN**: El acceso de admin a datos de compañías ahora está condicionado a la VPN corporativa en AMBOS backends (PHP + Go), creando una capa de seguridad de red que la impersonation no tenía. Sin VPN, un admin no puede acceder a datos de ninguna compañía, incluso con credenciales válidas.

---

### 🎯 Criterios de Aceptación (AC) Clave Validados

#### **AC-1. Pestaña "Support" reemplaza pestaña "Users" (QA-2)**
* **Validación realizada**: Navegación a Admin > Companies > [Company] y verificación de pestañas disponibles.
* **Comportamiento observado**: La pestaña "Support" aparece con ícono `pi-sign-in` en el lugar de la antigua pestaña "Users". Al hacer click muestra 4 puntos informativos (acceso, no-impersonation, cierre, multi-tab) y botón "Start a support session".

#### **AC-2. Iniciar sesión de soporte redirige al dashboard de tenant (QA-3)**
* **Validación realizada**: Click en "Start a support session" desde la pestaña Support de una compañía.
* **Comportamiento observado**: El navegador redirige a `/dashboard` con la sesión de soporte activa. El admin puede ver workflows, conexiones y data stores de la compañía seleccionada con permisos completos.

#### **AC-3. Banner de sesión de soporte visible con controles (QA-4)**
* **Validación realizada**: Verificación visual del banner superior durante sesión de soporte activa.
* **Comportamiento observado**: StatusBadge "warning" con ping muestra "Support session" + nombre de la compañía + botón "Leave company" con ícono LogOut. Visible en resoluciones ≥lg.

#### **AC-4. Rutas admin bloqueadas durante sesión de soporte (QA-5)**
* **Validación realizada**: Navegación manual a `/admin/companies` y `/admin` durante sesión de soporte activa.
* **Comportamiento observado**: `role.guard.ts` detecta `auth.supportCompany` y redirige a `TenantDashboard`. Las rutas admin son inaccesibles hasta que el admin cierre la sesión de soporte.

#### **AC-5. Sin VPN se bloquea el acceso a datos de tenant con 403 (QA-9)**
* **Validación realizada**: Requests de tenant sin conexión VPN activa.
* **Comportamiento observado**: `EnsureAdminAccessVpn` retorna HTTP 403 con `{ message: "...", reason: "vpn_required" }`. El frontend detecta el `reason` en el interceptor de axios y muestra el overlay de VPN.

---

### 🔄 Pruebas de Regresión
- **Login de Admin (REG-001)**: Login vía Keycloak funciona correctamente, redirect a panel admin sin regresión.
- **Login de Company (REG-002)**: Login de tenant funciona correctamente, redirect a dashboard de tenant.
- **Lista de compañías (REG-003)**: Carga correctamente, información de compañías visible, detalle accesible.
- **Pestañas de compañía (REG-004)**: Information, App Connectors, Boards, Subscription — todas funcionan. Pestaña "Users" eliminada correctamente.
- **API de tenants para Company users (REG-005)**: Flows, conexiones y recursos accesibles. Los cambios en middlewares no afectan a users regulares.
- **Permisos de Company users (REG-006)**: Users con permisos limitados siguen siendo restringidos correctamente. El bypass de admin no afecta la verificación de permisos de users regulares.

---

La implementación de **Acceso directo a compañías sin inicio de sesión como usuario** cumple satisfactoriamente con todos los criterios de aceptación definidos. La migración de impersonation a sesión de soporte directa es arquitecturalmente sólida: elimina ~2,245 líneas de código complejo, reduce la superficie de ataque al eliminar tokens temporales, y refuerza la seguridad al condicionar el acceso de admin a la VPN corporativa en ambos backends (PHP y Go). El flujo de sesión de soporte funciona correctamente: inicio con un clic, banner informativo, confinamiento de rutas admin, operaciones de tenant completas, y salida limpia vía banner o menú de usuario. La sincronización multi-pestaña opera via storage events con reload automático. Las pruebas de regresión confirman que los cambios en los middlewares de tenant no afectan la funcionalidad existente para users regulares. Los 5 hallazgos del code review fueron verificados exitosamente, con una única observación de seguridad no bloqueante (SEC-CR-001). El ticket queda **formalmente aprobado para merge y deploy**.

| Details | |
|---|---|
| BROWSER | Chrome |
| BRANCH | `IONF-1316` (gateway-ion, gateway, flow_binaries) |
| ENV | dev-app.ionflow.io |
| TEST MATRIX | https://docs.google.com/spreadsheets/d/1DZuGNMJc_8Yp8amuPbi0ZQbI63cVPfJWvXbpJ7rEjSU/edit?usp=sharing |
| MERGE REQUEST | YES |
