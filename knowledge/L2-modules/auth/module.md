# Módulo: Auth (Login, SSO, Companies, Users)

> Módulo de autenticación, gestión de usuarios, companies y permisos. Gestionado principalmente por el repo `gateway` (PHP/Laravel) con SSO Keycloak.

## Información General

| Campo | Valor |
|-------|-------|
| Nombre interno | auth / login / users / companies |
| Criticidad | 🟠 Alto |
| Repos involucrados | `gateway-ion` (UI), `gateway` (API + SSO Keycloak) |
| Última actualización | Initial setup — Fase 5 |

---

## Rutas del Frontend (gateway-ion)

| Ruta | Vista | Componente | Permiso |
|------|-------|-----------|---------|
| `/login` | Login (SSO Keycloak) | `views/LoginView.vue` | Público |
| `/sso/callback` | Callback SSO | `views/SSOCallbackView.vue` | Público |
| `/company-selection` | Selección de company | `views/CompanySelectionView.vue` | Autenticado |
| `/invitation/:token` | Aceptar invitación | `views/InvitationView.vue` | Público |
| `/forbidden` | Acceso prohibido | `views/ForbiddenView.vue` | Público |
| `/users` | Lista de usuarios | `views/tenant/user/Users.vue` | `READ_USER` |
| `/profile` | Perfil del usuario | `views/tenant/user/Profile.vue` | `READ_USER` |
| `/teams` | Equipos/invitaciones | `views/tenant/teams/Teams.vue` | `READ_INVITATION` |
| `/settings` | Configuración | `views/tenant/settings/Settings.vue` | `READ_SETTING` |
| `/admin/companies` | Admin: gestión de companies | `views/admin/companies/Index.vue` | Admin |
| `/admin/companies/:id` | Admin: apps de una company | `views/admin/companies/CompanyApp.vue` | Admin |

### Servicios clave
- `services/authentication.ts` — Servicio de autenticación
- `services/keycloak.service.ts` — Integración con SSO Keycloak
- `services/user.service.ts` — Gestión de usuarios
- `services/invitation.service.ts` — Sistema de invitaciones
- `stores/auth.ts` — Store de autenticación (Pinia)
- `guards/` — Guards de rutas (permisos)

### Tests unitarios existentes
- `views/CompanySelectionView.spec.ts`
- `views/InvitationView.spec.ts`
- `views/SSOCallbackView.spec.ts`
- `views/ForbiddenView.spec.ts`
- `stores/auth.spec.ts`

---

## API Endpoints

### Keycloak SSO (gateway — `routes/api.php`)

| Método | Endpoint | Auth | Descripción |
|--------|----------|------|-------------|
| GET | `/1.0/keycloak/redirect` | Público | Genera URL de redirect a Keycloak |
| GET | `/1.0/keycloak/callback` | Público | Callback SSO de Keycloak |
| POST | `/1.0/keycloak/oauth/token` | Público | Refresh token |
| POST | `/1.0/keycloak/logout` | Público | Logout de Keycloak |
| GET | `/1.0/keycloak/validate` | Público | Verificar usuario en Keycloak |
| GET | `/1.0/keycloak/logout-webhook` | Público | Webhook de logout |

### Users (gateway — `routes/tenants.php`)

| Método | Endpoint | Permiso | Descripción |
|--------|----------|---------|-------------|
| GET | `/1.0/tenants/{tenant}/users` | `read-user` + `company:read-user` | Lista de usuarios |
| PUT | `/1.0/tenants/{tenant}/users` | `update-user` + `company:update-user` | Actualizar usuario |
| POST | `/1.0/tenants/{tenant}/users/avatar` | `update-user` | Subir avatar |
| DELETE | `/1.0/tenants/{tenant}/users/avatar` | `update-user` | Eliminar avatar |
| GET | `/1.0/tenants/{tenant}/users/contact` | `read-user` | Datos de contacto |
| POST | `/1.0/tenants/{tenant}/users/contact` | `update-user` | Crear/actualizar contacto |
| PUT | `/1.0/tenants/{tenant}/users/{userId}/permissions` | `update-permission` | Actualizar permisos |
| GET | `/1.0/tenants/{tenant}/users/companies` | `read-user` | Companies del usuario |
| GET | `/2.0/user` | auth:api | Datos del usuario actual |
| POST | `/2.0/user/logout` | auth:api | Logout |
| POST | `/2.0/user/register` | Público (throttle) | Registro |

### Companies (gateway — `routes/tenants.php`)

| Método | Endpoint | Permiso | Descripción |
|--------|----------|---------|-------------|
| GET | `/1.0/tenants/{tenant}/companies` | `read-company` | Datos de la company |
| PUT | `/1.0/tenants/{tenant}/companies` | `update-company` | Actualizar company |
| POST | `/1.0/tenants/{tenant}/companies/logo` | `update-company` | Subir logo |
| DELETE | `/1.0/tenants/{tenant}/companies/logo` | `update-company` | Eliminar logo |

### Invitaciones (gateway — `routes/tenants.php`)

| Método | Endpoint | Permiso | Descripción |
|--------|----------|---------|-------------|
| GET | `/1.0/tenants/{tenant}/invitations` | `read-invitation` | Lista de invitaciones |
| POST | `/1.0/tenants/{tenant}/invitations` | `create-invitation` | Enviar invitación |
| PUT | `/1.0/tenants/{tenant}/invitations/{inv}` | `update-invitation` | Actualizar |
| DELETE | `/1.0/tenants/{tenant}/invitations/{inv}` | `delete-invitation` | Eliminar |
| GET | `/api/invitations/validate` | Público | Validar token de invitación |
| GET | `/{tenant}/invitations-actions/{intent_id}/accept` | auth:api | Aceptar invitación |
| GET | `/{tenant}/invitations-actions/{intent_id}/attach-company` | auth:api | Vincular company |

### Permisos (gateway — `routes/tenants.php`)

| Método | Endpoint | Permiso | Descripción |
|--------|----------|---------|-------------|
| GET | `/1.0/tenants/{tenant}/permissions/user` | `read-permission` | Permisos del usuario |
| GET | `/1.0/tenants/{tenant}/permissions/tenant` | `read-permission` | Todos los permisos del tenant |

---

## Schema de BD

### PostgreSQL (gateway)
> Fuente: `gateway/database/migrations/`

**Tablas principales:**
- `users` — Usuarios del sistema
- `companies` — Companies (multi-tenant)
- `company_user` — Relación muchos a muchos
- `roles` / `permissions` / `role_user` — Sistema de permisos (Laratrust)
- `authentications` — Tokens de autenticación
- `invitations` — Invitaciones pendientes
- `sessions` — Sesiones activas

**Migraciones relevantes:**
- `2014_10_12_000000_create_users_table.php`
- `2022_03_30_145619_laratrust_setup_tables.php` (roles y permisos)
- `2024_11_26_091013_create_companies_table.php`
- `2024_11_26_092110_create_company_user_table.php`
- `2025_04_14_205717_add_authentication_id_to_users_table.php`
- `2025_04_17_173855_add_keycloak_refresh_token_to_users_table.php`
- `2025_05_09_144324_make_password_nullable_in_users_table.php`
- `2026_01_26_212709_create_invitation_table.php`
- `2026_02_09_151832_update_permission_user_primary_key_with_company.php`
- `2026_03_09_134948_create_sessions_table.php`

---

## Reglas de Negocio

1. Autenticación gestionada por **SSO Keycloak** a través de `gateway` (PHP)
2. Cada usuario pertenece a una o más **companies** (multi-tenant)
3. Los permisos determinan qué secciones puede ver/editar un usuario (no solo flows y connectors)
4. Un usuario selecciona la company activa al iniciar sesión
5. Las invitaciones se envían por email y tienen un token de aceptación
6. Los permisos se gestionan por company (un usuario puede tener diferentes permisos en diferentes companies)

---

## Lógica Backend (flow_binaries)

> Fuente: `../flow_binaries/docs/backend/database-connections.mdx`

### Modelo de autenticación en flow_binaries
- **JWT**: `golang-jwt/jwt/v5` — validación de tokens JWT con clave pública RSA
- **Middleware pipeline**: `JWTAuth` → `TenantAuth` → `PermissionAuth` → Controller
- **TenantAuth**: Extrae `tenantId` de la URL, carga `Company` del PG, inyecta en context
- **Clave pública**: `./storage/oauth-public.key` — cargada al inicio del backend

### Archivos centinela
| Repo | Archivo | Razón |
|------|---------|-------|
| flow_binaries | `backend/ion/middleware/` | Middlewares JWT, Tenant, Permission |
| flow_binaries | `backend/backend.go` | Carga de clave pública `LoadPublicKey()` |
| flow_binaries | `backend/routes/api.go` | Definición de rutas con middleware chain |
| gateway | `app/Http/Middleware/` | Middlewares Laravel (auth original) |
| gateway | `config/keycloak.php` | Config de Keycloak SSO |

---

## Impacto Cruzado

### Módulos que Auth afecta
| Módulo destino | Componente afectado | Tipo | Ejemplo |
|---------------|--------------------|-----------------|---------| 
| **TODOS** | Acceso a API | API | Sin auth válida, ningún endpoint es accesible |
| **Boards** | Permisos de flows | API | `READ_BOARD`, `CREATE_BOARD`, `UPDATE_BOARD`, `DELETE_BOARD` |
| **Connections** | Permisos de connectors | API | Gestión de connectors requiere permisos |
| **Billing** | Pipeline de suscripción | Middleware | Billing se consulta después de auth |

### Módulos que afectan a Auth
| Módulo origen | Componente | Tipo | Ejemplo |
|--------------|------------|-----------------|---------| 
| **Keycloak (externo)** | SSO Provider | Auth | Tokens JWT emitidos por Keycloak |
| **Billing** | Estado de suscripción | Middleware | Suscripción inactiva → acceso limitado |

### Tablas compartidas
| Tabla | Módulos que la usan | Riesgo si cambia |
|-------|---------------------|------------------|
| `companies` (PG) | Auth, TODOS (via CompanySchema) | Cambios afectan todo el multi-tenant |
| `users` (PG) | Auth, TODOS (permisos) | Cambios en permisos afectan acceso a todo |

---

## Selectores E2E conocidos
> ⚠️ Pendiente de poblar.

---

## Historial de Actualizaciones

| Fecha | Tickets | Cambios | Actualizado por |
|-------|---------|---------|----------------|
| Initial | — | Creación inicial | QA Catalyst |
| 2026-06-07 | — | Backend Logic (JWT, middleware) + Impacto Cruzado | QA Catalyst |
