# Code Review QA — 86e31pbz9 (Modo Deployment / Bug Hunting)

## Resumen
- Repos revisados: gateway-ion, gateway, flow_binaries
- Commits analizados: 6 (2 por repo: feat + docs)
  - gateway-ion: `bab9a6b8`, `0c99e398`
  - gateway: `40466f5d`, `b6368583`
  - flow_binaries: `b2097db`, `0b7f232`
- Archivos modificados analizados: 72 (46 gateway-ion, 22 gateway, 4 flow_binaries)
- Hallazgos totales: 5
  - BUG confirmados: 0
  - RISK a verificar: 3 (🟠: 2, 🟡: 1)
  - SEC seguridad: 1 (🟠: 1)
  - EDGE cases: 1 (🟡: 1)
- Módulos con impacto cruzado: Auth → TODOS (middleware de tenant afecta todos los módulos)
- TCs inyectados en test-matrix: 5 (TC-CR-001 a TC-CR-005)

---

## Archivos Modificados

### REPO: gateway-ion (46 archivos, +497/-1800 líneas)

**Archivos nuevos:**
- `src/composables/useSupportSession.ts` — Nuevo composable para sesión de soporte
- `src/lib/supportSession.ts` — Helpers de localStorage para sesión de soporte
- `src/composables/useSupportSessionSync.ts` — Sync de sesión entre pestañas (storage event)
- `src/views/admin/companies/CompanySupportSession.vue` — Nueva pestaña "Support"
- `src/guards/role.guard.spec.ts` — Tests del role guard

**Archivos eliminados (11):**
- `useImpersonation.ts`, `useImpersonation.spec.ts`, `useImpersonationSync.spec.ts`
- `impersonation.ts`, `impersonation.spec.ts`
- `impersonation.service.ts`, `impersonation.service.spec.ts`
- `api-impersonation.spec.ts`
- `CompanyUsers.vue`, `CompanyUsers.spec.ts`
- `CompanyUserActionsMenu.vue`
- `StartSupportSessionDialog.vue`, `StartSupportSessionDialog.spec.ts`

**Archivos modificados clave:**
- `stores/auth.ts` — Nuevo state `supportCompany`, getter `company`, acción `leaveSupportSession()`
- `guards/role.guard.ts` — Admin en sesión de soporte redirigido de rutas admin a TenantDashboard
- `guards/auth.guard.ts` — Limpia sesión de soporte en logout
- `services/api.ts` — Eliminada lógica de Bearer token de impersonation, agregado `endSupportSession`
- `views/admin/companies/CompanyApps.vue` — Tab "Support" reemplaza "Users"
- `views/ForbiddenView.vue` — Detecta sesión de soporte para mostrar "Leave company" vs "Logout"

### REPO: gateway (22 archivos, +79/-1011 líneas)

**Archivos nuevos:**
- `app/Http/Middleware/EnsureAdminAccessVpn.php` — Middleware VPN para admin
- `config/vpn.php` — Nueva config de CIDRs de VPN
- `tests/Feature/Api/Tenant/AdminBypassTest.php` — Tests para bypass de admin

**Archivos eliminados:**
- `ImpersonationController.php`, `ImpersonationService.php`
- `EnforceImpersonationScope.php`, `config/impersonation.php`
- `ImpersonationTest.php`, `ImpersonationSessionTest.php`

**Archivos modificados clave:**
- `CompanyPermission.php` — Bypass para rol `administrator` (skip permission check)
- `TenantConnection.php` — Bypass para `administrator` + `owner` (no requiere membresía)
- `routes/tenants.php` — Middleware `impersonation.scope` → `admin.access.vpn`
- `channels.php` — Admin puede escuchar en canal de cualquier compañía

### REPO: flow_binaries (4 archivos, +21/-445 líneas)

**Archivos eliminados:**
- `impersonation_test.go`, `impersonation_service.go`

**Archivos modificados clave:**
- `laravel_auth.go` — Bypass de admin en `TenantAuthMiddleware` (VPN check) + skip permission en `TenantPermissionmiddleware`

---

## Sección 1 — BUGs Confirmados (BUG-CR-##)

> No se encontraron bugs confirmados reproducibles. La implementación es coherente y limpia.

---

## Sección 2 — Riesgos a Verificar (RISK-CR-##)

### RISK-CR-001: Error handler en CompanySupportSession muestra error.message crudo al usuario

```
Categoría: RISK
Severidad: 🟠 Alto
Repo: gateway-ion
Commit: bab9a6b8
Archivo: src/views/admin/companies/CompanySupportSession.vue
Línea: 25-32

Descripción: El catch de getCompanyData() muestra `error.message` directamente en el toast.
  Si el backend devuelve un error 500 con body técnico, se mostraría al usuario.

Evidencia:
  .catch((error: { message: string }) => {
    toast.add({
      severity: 'error',
      summary: error.message ?? 'Error',   // ← Mensaje crudo del backend
      detail: error,                        // ← Objeto error completo en detail
      life: 5000,
    });
  });

Comportamiento Esperado:
  Un mensaje de error amigable (i18n) en lugar del mensaje técnico del backend.

Comportamiento Actual:
  Si getResource falla (ej: 500, network error), el toast muestra el
  error.message técnico del axios error que puede contener detalles internos.
  Además, `detail: error` pasa el objeto completo, que PrimeVue podría
  intentar renderizar como string.

Precondiciones:
  User Role: Administrator
  User State: Logged in, en pestaña Support de una compañía
  Company: ID inválido o backend caído

Pasos de Reproducción:
  1) Admin Login > Sidebar: Companies > Click [Company con ID inválido o backend down]
  2) Tab: Support
  3) Verificar: toast de error muestra mensaje técnico vs amigable

Impacto: Exposición de información interna del servidor en mensajes de error.

Recomendación: Inyectar como TC en la test-matrix para verificar en testing
```

### RISK-CR-002: `EnsureAdminAccessVpn` permite pasar requests de usuarios no-admin sin verificar VPN

```
Categoría: RISK
Severidad: 🟠 Alto
Repo: gateway
Commit: 40466f5d
Archivo: app/Http/Middleware/EnsureAdminAccessVpn.php
Línea: 20-24

Descripción: El middleware solo verifica VPN si el usuario es admin. Usuarios
  no-admin pasan directamente con `$next($request)` — esto es BY DESIGN ya
  que la VPN solo es requisito para el bypass de admin, pero debe verificarse
  que en combinación con TenantConnection, un usuario no-admin NO puede
  acceder a compañías de las que no es miembro.

Evidencia:
  if (!$user || !$user->hasRole(EnsureAdminRole::ROLE)) {
      return $next($request);   // ← non-admin skip VPN check (by design)
  }

Comportamiento Esperado:
  El middleware solo aplica la restricción VPN al admin. Los users normales
  siguen siendo filtrados por TenantConnection (requiere membresía en company).

Comportamiento Actual:
  Correcto por diseño. Pero la combinación EnsureAdminAccessVpn + TenantConnection
  debe verificarse end-to-end: que un user tenant sin membresía en company X
  NO puede acceder a datos de company X (TenantConnection lo bloquea).

Precondiciones:
  User Role: Tenant (no admin)
  Company: Company de la que el usuario NO es miembro

Pasos de Reproducción:
  1) Company Login con usuario que pertenece a Company A
  2) Intentar request API a Company B (ej: GET /1.0/tenants/{B_id}/flows)
  3) Verify: HTTP 401 "Unauthorized" de TenantConnection

Impacto: Si TenantConnection tuviera un bug, el admin.access.vpn no lo detectaría.

Recomendación: Inyectar como TC para verificar aislamiento multi-tenant
```

### RISK-CR-003: Duplicación de key `COMPANY_KEY` entre archivos

```
Categoría: RISK
Severidad: 🟡 Medio
Repo: gateway-ion
Commit: bab9a6b8
Archivo: src/lib/supportSession.ts (L3) y src/composables/useSupportSessionSync.ts (L3)

Descripción: La constante COMPANY_KEY = 'support_session_company' está definida
  en DOS archivos separados. Si alguien cambia la key en un archivo pero no en
  el otro, el sync entre pestañas dejaría de funcionar.

Evidencia:
  // supportSession.ts
  const COMPANY_KEY = 'support_session_company';

  // useSupportSessionSync.ts
  const COMPANY_KEY = 'support_session_company';

Comportamiento Esperado:
  La key debería estar definida en un solo lugar y exportada/importada.

Comportamiento Actual:
  Funciona correctamente AHORA, pero es frágil ante cambios futuros.
  No es un bug, pero es un riesgo de mantenimiento.

Impacto: Bajo — funciona hoy, riesgo si se modifica una key sin la otra.

Recomendación: Verificar que el sync funciona (TC-009 ya lo cubre)
```

---

## Sección 3 — Seguridad (SEC-CR-##)

### SEC-CR-001: Admin en sesión de soporte tiene bypass completo de permisos — sin auditoría

```
Categoría: SEC
Severidad: 🟠 Alto
Repo: gateway + flow_binaries
Commit: 40466f5d (gateway), b2097db (flow_binaries)
Archivo: CompanyPermission.php (L23-25), TenantPermissionmiddleware en laravel_auth.go (L318-321)

Descripción: El bypass de admin salta TODA verificación de permisos.
  CompanyPermission.php devuelve $next directamente si hasRole('administrator').
  TenantPermissionmiddleware en Go salta la verificación si isAdmin=true.
  Esto significa que un admin en sesión de soporte puede ejecutar ANY
  operación en ANY company sin restricción alguna — incluyendo DELETE,
  y NO hay log de auditoría que registre las acciones del admin en la
  sesión de soporte (solo se loguea cuando se BLOQUEA por VPN, no cuando se PERMITE).

Evidencia:
  // CompanyPermission.php
  if ($user->hasRole(EnsureAdminRole::ROLE)) {
      return $next($request);  // ← Full bypass, no audit log
  }

  // laravel_auth.go
  if isAdmin, _ := r.Context().Value(CtxIsAdmin).(bool); isAdmin {
      next.ServeHTTP(w, r)  // ← Full bypass, no audit log
      return
  }

Comportamiento Esperado:
  Si bien el bypass de permisos es by design (admin needs full access for support),
  debería existir algún nivel de registro de las acciones realizadas en sesión de soporte.

Comportamiento Actual:
  Las acciones del admin en sesión de soporte (crear, editar, eliminar recursos
  de una compañía) no se registran en ningún log específico. Solo se loguea
  el bloqueo por VPN (admin_access.blocked_off_vpn), no las acciones permitidas.

Precondiciones:
  User Role: Administrator
  User State: En sesión de soporte activa
  VPN: Conectada

Pasos de Reproducción:
  1) Admin Login > Sidebar: Companies > Click [Company] > Tab: Support > Start session
  2) Sidebar: Boards > Crear un flow > Eliminarlo
  3) Verify: ¿Existe algún log que registre las acciones del admin en esta compañía?

Impacto: Riesgo de auditoría — acciones destructivas de admin no rastreables.

Recomendación: Documentar como observación. No es bloqueante para QA pero
  sí es un hallazgo de seguridad que el PO/Developer debería conocer.
```

---

## Sección 4 — Edge Cases (EDGE-CR-##)

### EDGE-CR-001: `supportCompany` en auth store se inicializa desde localStorage una vez — no es reactivo a cambios externos

```
Categoría: EDGE
Severidad: 🟡 Medio
Repo: gateway-ion
Commit: bab9a6b8
Archivo: src/stores/auth.ts
Línea: 28

Descripción: El state `supportCompany` se inicializa leyendo localStorage
  con getSupportCompany() UNA vez al crear el store. Si otro proceso modifica
  localStorage, el store no se actualiza automáticamente — depende del
  useSupportSessionSync que hace un location.assign('/') (hard reload).

Evidencia:
  state: () => ({
    ...
    supportCompany: getSupportCompany(),  // ← Read once, not reactive to localStorage changes
  }),

Comportamiento Esperado:
  Si localStorage cambia (otra pestaña inicia/cierra sesión), el store
  refleje el cambio.

Comportamiento Actual:
  El sync se maneja via `useSupportSessionSync` que escucha el storage event
  y hace `globalThis.location.assign('/')` — un hard reload que re-inicializa
  el store. Funciona, pero no es reactivo en tiempo real (hay un momento de
  inconsistencia entre el storage event y el reload).

Precondiciones:
  Dos pestañas abiertas, iniciar sesión de soporte en una

Pasos de Reproducción:
  1) Abrir Ionflow en dos pestañas (ambas como admin)
  2) Pestaña 1: Iniciar sesión de soporte en Company A
  3) Pestaña 2: Verificar que se recarga automáticamente

Impacto: Bajo — el hard reload resuelve la inconsistencia, pero hay un
  breve momento donde la pestaña 2 puede estar en estado inconsistente.

Recomendación: TC-009 ya cubre este escenario. Verificar timing del reload.
```

---

## Follow-the-Flow Maps

### FLOW MAP — Iniciar sesión de soporte

```
1. CALLERS:
   → CompanySupportSession.vue: enterSupportSession() (click del botón)
   → Solo un caller en el frontend

2. PERSISTENCIA:
   → setSupportCompany() escribe en localStorage (no BD)
   → location.assign('/dashboard') fuerza hard reload
   → NO hay registro server-side de la sesión de soporte

3. CONSUMIDORES:
   → auth.ts store: lee supportCompany al inicializarse (getSupportCompany)
   → role.guard.ts: verifica auth.supportCompany para decidir rutas
   → TenantLayout, SupportSessionBanner: leen supportCompany del store
   → api.ts: isInSupportSession() para decidir si limpiar en redirect

4. RENDER:
   → Banner "Support session" + nombre de company + "Leave company"
   → Dashboard de tenant con todos los recursos de la compañía

5. ERROR PATH:
   → CompanySupportSession.vue: toast con error.message (RISK-CR-001)
   → VPN bloqueada: overlay de VPN (403 con reason=vpn_required)
   → 401: redirect a SSO + clear support session

6. OPERACIÓN OPUESTA:
   → endSupportSession(): clearSupportSession() + redirect a /admin/companies
   → leaveSupportSession(): store.supportCompany = null + clear localStorage
   → logout(): llama a leaveSupportSession() — ✅ simétrico
```

### FLOW MAP — Admin bypass en middlewares (cross-repo)

```
1. CALLERS:
   → gateway: EnsureAdminAccessVpn → TenantConnection → CompanyPermission
   → flow_binaries: JWTAuthMiddleware → TenantAuthMiddleware → TenantPermissionmiddleware

2. CONSISTENCIA CROSS-REPO:
   ✅ Ambos repos verifican VPN para admin
   ✅ Ambos repos saltan verificación de membresía para admin
   ✅ Ambos repos saltan verificación de permisos para admin
   ❓ gateway retorna 403 con JSON {message, reason} — flow_binaries retorna 403 con JSON {message, reason}
   ✅ Consistente: ambos usan el mismo formato de respuesta VPN

3. PERSISTENCIA: N/A (middleware, no persiste)

4. ERROR PATHS:
   ✅ gateway: 403 + vpn_required reason → FE muestra overlay VPN
   ✅ flow_binaries: 403 + vpn_required reason → FE muestra overlay VPN
```

---

## Impacto Cruzado

| Módulo Impactado | Componente Afectado | Riesgo | Verificación Necesaria |
|---|---|---|---|
| **TODOS (Boards, Connections, etc.)** | Middleware de tenant (gateway + flow_binaries) | 🟠 Alto | Los cambios en TenantConnection y TenantAuthMiddleware afectan TODOS los endpoints de tenant. Verificar que users normales siguen funcionando (REG-005, REG-006). |
| **Auth** | Login, guards, stores | 🟠 Alto | El auth.guard y role.guard modificados deben seguir redirigiendo correctamente para todos los roles. |
| **Broadcasting** | channels.php | 🟡 Medio | Admin puede escuchar en canal de cualquier compañía. Verificar que un tenant user NO puede escuchar en canal de otra compañía. |

---

## TCs Inyectados en Test Matrix

| TC ID | Categoría | Origen | Caso de Test | Severidad |
|-------|-----------|--------|-------------|-----------|
| TC-CR-001 | RISK | RISK-CR-001 | Verificar mensaje de error en toast cuando la carga de datos de compañía falla (CompanySupportSession) | 🟠 |
| TC-CR-002 | RISK | RISK-CR-002 | Verificar aislamiento multi-tenant: user de Company A no puede acceder a Company B via API | 🟠 |
| TC-CR-003 | SEC | SEC-CR-001 | Verificar si existen logs de auditoría para acciones del admin en sesión de soporte | 🟠 |
| TC-CR-004 | EDGE | EDGE-CR-001 | Verificar timing de sync entre pestañas al iniciar sesión de soporte | 🟡 |
| TC-CR-005 | RISK | RISK-CR-003 | Verificar que la key de localStorage es consistente entre lib/supportSession y useSupportSessionSync | 🟡 |
