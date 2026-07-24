# Módulo: Connections (App Connectors)

> Módulo de gestión de App Connectors en Ionflow. Permite crear, editar y gestionar los conectores que abstraen APIs externas en nodos reutilizables.

## Información General

| Campo | Valor |
|-------|-------|
| Nombre interno | connections / app connectors |
| Criticidad | 🟠 Alto |
| Repos involucrados | `gateway-ion` (UI), `gateway` (API) |
| Última actualización | 2026-07-09 — v0.1.0 batch update |

---

## Rutas del Frontend (gateway-ion)

| Ruta | Vista | Componente | Permiso |
|------|-------|-----------|---------|
| `/connections` | Lista de app connectors | `views/tenant/connections/AppListView.vue` | `READ_APP` |
| `/connections/create` | Crear connector | `views/tenant/connections/AppCreateView.vue` | `CREATE_APP` |
| `/connections/:id` | Editar connector | `views/tenant/connections/AppEditView.vue` | `UPDATE_APP` |
| `/connections/:connectionId/auth/:authId` | Editar autenticación | `views/tenant/connections/AuthEditView.vue` | `UPDATE_APP_CONNECTION` |
| `/connections/:connectionId/webhook/:webhookId` | Editar webhook del connector | `views/tenant/connections/WebhookEditView.vue` | `UPDATE_APP_WEBHOOK` |
| `/connections/:connectionId/module/:moduleId` | Editar nodo/acción del connector | `views/tenant/connections/ActionEditView.vue` | `UPDATE_APP_NODE` |
| `/admin/connections` | Admin: lista de connectors globales | `views/admin/connections/Index.vue` | Admin |

### Estructura de vistas
```
views/tenant/connections/
├── Action/              ← Gestión de acciones/nodos del connector
├── App/                 ← Componentes del connector (app)
├── Auth/                ← Métodos de autenticación
├── Connections/         ← Gestión de conexiones
├── Webhook/             ← Webhooks del connector
├── components/          ← Componentes compartidos
├── AppListView.vue
├── AppCreateView.vue
├── AppEditView.vue
├── AuthEditView.vue
├── WebhookEditView.vue
├── ActionEditView.vue
└── useAppQueries.ts     ← Queries de TanStack/React Query
```

---

## API Endpoints

### Apps / Connectors CRUD (gateway — `routes/tenants.php`)

| Método | Endpoint | Permiso | Descripción |
|--------|----------|---------|-------------|
| GET | `/1.0/tenants/{tenant}/apps` | `read-app` | Lista de connectors de la company |
| GET | `/1.0/tenants/{tenant}/apps/{app}` | `read-app` | Detalle de un connector |
| POST | `/1.0/tenants/{tenant}/apps` | `create-app` | Crear connector |
| PUT | `/1.0/tenants/{tenant}/apps/{app}` | `update-app` | Actualizar connector |
| DELETE | `/1.0/tenants/{tenant}/apps/{app}` | `delete-app` | Eliminar connector |
| POST | `/1.0/tenants/{tenant}/apps/{app}/logo` | `update-app` | Subir logo |
| GET | `/1.0/tenants/{tenant}/apps-services` | `read-app` | Apps globales disponibles para flows |

### Actions / Nodos del Connector (gateway — `routes/tenants.php`)

| Método | Endpoint | Permiso | Descripción |
|--------|----------|---------|-------------|
| GET | `/1.0/tenants/{tenant}/app-actions` | `read-app-node` | Lista de acciones/nodos |
| GET | `/1.0/tenants/{tenant}/app-actions/{action}` | `read-app-node` | Detalle de acción |
| POST | `/1.0/tenants/{tenant}/app-actions` | `create-app-node` | Crear acción |
| PUT | `/1.0/tenants/{tenant}/app-actions/{action}` | `update-app-node` | Actualizar acción |
| DELETE | `/1.0/tenants/{tenant}/app-actions/{action}` | `delete-app-node` | Eliminar acción |

### Auth / Connections del Connector (gateway — `routes/tenants.php`)

| Método | Endpoint | Permiso | Descripción |
|--------|----------|---------|-------------|
| GET | `/1.0/tenants/{tenant}/app-connections` | `read-app-connection` | Lista de conexiones auth |
| GET | `/1.0/tenants/{tenant}/app-connections/{conn}` | `read-app-connection` | Detalle |
| POST | `/1.0/tenants/{tenant}/app-connections` | `create-app-connection` | Crear conexión |
| PUT | `/1.0/tenants/{tenant}/app-connections/{conn}` | `update-app-connection` | Actualizar |
| DELETE | `/1.0/tenants/{tenant}/app-connections/{conn}` | `delete-app-connection` | Eliminar |

### App-Scope API — M2M (IONF-996)

> Endpoints para acceso programático desde apps externas vía Client Credentials (OAuth2 M2M).
> Rutas bajo `/api/2.0/app/accounts/{account:remote_id}/connections` con middleware `auth.app`.

| Método | Endpoint | Scope OAuth | Descripción |
|--------|----------|-------------|-------------|
| GET | `/2.0/app/accounts/{account:remote_id}/connections` | `app:connection-read` | Listar connections de la cuenta (filtradas por app) |
| GET | `/2.0/app/accounts/{account:remote_id}/connections/{id}` | `app:connection-read` | Detalle de una connection |
| POST | `/2.0/app/accounts/{account:remote_id}/connections` | `app:connection-create` | Crear connection con credenciales encriptadas |
| PUT | `/2.0/app/accounts/{account:remote_id}/connections/{id}` | `app:connection-update` | Actualizar connection |
| DELETE | `/2.0/app/accounts/{account:remote_id}/connections/{id}` | `app:connection-delete` | Eliminar connection |

**Detalles técnicos (IONF-996):**
- `app_id` se deriva del token M2M (no del body) — seguridad
- `app_name` es campo requerido para crear connections
- El listado filtra por `app_id` del token
- Columna `connection` encriptada vía trait `Encryptable`, con espejo en columna `data`
- `ConnectionM2MResource` serializa sin exponer el campo `connection` (secreto)
- Campos protegidos: `id`, `account_id`, `created_at` no son mass-assignable
- Account viene del binding de ruta (`remote_id`), no del payload

### Webhooks del Connector (gateway — `routes/tenants.php`)

| Método | Endpoint | Permiso | Descripción |
|--------|----------|---------|-------------|
| GET | `/1.0/tenants/{tenant}/app-webhooks` | `read-app-webhook` | Lista de webhooks |
| GET | `/1.0/tenants/{tenant}/app-webhooks/{wh}` | `read-app-webhook` | Detalle |
| POST | `/1.0/tenants/{tenant}/app-webhooks` | `create-app-webhook` | Crear webhook |
| PUT | `/1.0/tenants/{tenant}/app-webhooks/{wh}` | `update-app-webhook` | Actualizar |
| DELETE | `/1.0/tenants/{tenant}/app-webhooks/{wh}` | `delete-app-webhook` | Eliminar |

### Migración a Global (gateway — `routes/api.php`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| PUT | `/1.0/companies/{company}/app/{appId}/migrate` | Migrar connector a global |
| POST | `/1.0/companies/{company}/app/{appId}/export` | Exportar connector |

---

## Schema de BD

### PostgreSQL (gateway)
> Fuente: `gateway/database/migrations/`
- `2022_03_17_143123_create_app_services_table.php` — Tabla de app services
- `2024_04_23_211403_delete_auth_type_from_app_services.php`
- `2024_09_20_175742_add_configuration_to_app_services_table.php`

**Tablas principales:**
- `app_services` — Connectors/Apps
- `services` — Services asociados a los connectors

---

## Reglas de Negocio

1. **Dos tipos de connectors**: Company (solo para la company que lo creó) y Global (disponible para todas las companies)
2. Los connectors **globales** son migrados/aprobados por el usuario admin
3. Los nodos de un connector abstracten endpoints de APIs externas
4. Cada connector define sus **métodos de autenticación** (OAuth, API Key, Basic, etc.)
5. Para que un flow pueda ser migrado a global (GRAPP), todos sus nodos deben ser de connectors **globales**
6. Si un connector es eliminado, los flows que lo usan pueden quedar rotos

---

## Dependencias con otros módulos

| Módulo | Relación |
|--------|----------|
| **Boards** (Flows) | Los flows usan nodos de connectors |
| **Integrations** | Conexiones activas que usan los connectors |
| **Services** (Catalog) | Services vinculados a los connectors |
| **Webhooks** | Webhooks definidos dentro de un connector |

---

## Lógica Backend (flow_binaries)

> Fuente: `../flow_binaries/docs/architecture.mdx`, `packages/channel/`

### Servicios involucrados
| Service | Archivo | Función |
|---------|---------|---------|
| `ConnectionService` | `backend/ion/services/connection_service.go` | CRUD de conexiones |
| `IntegrationService` | `backend/ion/services/integration_service.go` | Manejo de integraciones |
| `AttemptService` | `backend/ion/services/attempt_service.go` | Intentos de conexión |

### Channel Package (`packages/channel/`)
> Motor de autenticación genérico usado por los nodos de app en los flows.

| Tipo Auth | Constante | Descripción |
|-----------|-----------|-------------|
| `oauth2_code` | OAuth 2.0 Authorization Code | Redirect → Callback → Token |
| `oauth2_code_refresh_token` | OAuth 2.0 + Refresh | Token auto-refresh |
| `api_key` | API Key | Header/Query parameter |
| `basic` | HTTP Basic Auth | Username:Password |
| `client_credentials` | OAuth 2.0 Client Credentials | Machine-to-machine |
| `owner_credentials` | OAuth 2.0 ROPC | Resource Owner Password |

### Modelo de ejecución
- **Patrón de BD**: Global (Account level) para apps globales, Tenant (Company) para connections de company
- **Multi-tenant**: Sí — connections aisladas por company via `CompanySchema()`
- **Refresh automático**: `services.Execute()` maneja token refresh transparentemente → `isRefreshed` flag

### Archivos centinela
| Repo | Archivo | Razón |
|------|---------|-------|
| flow_binaries | `packages/channel/services/authorize.go` | Flujo de autorización OAuth |
| flow_binaries | `packages/channel/services/token.go` | Obtención de tokens |
| flow_binaries | `packages/channel/services/refresh.go` | Token refresh logic |
| flow_binaries | `packages/channel/services/callback.go` | OAuth callback handling |
| flow_binaries | `packages/channel/models/` | Modelos: App, AppAction, Connection, Field |
| flow_binaries | `backend/ion/services/connection_service.go` | CRUD connections |

---

## Impacto Cruzado

### Módulos que Connections afecta
| Módulo destino | Componente afectado | Tipo | Ejemplo |
|---------------|--------------------|-----------------|---------| 
| **Boards** | Nodos de connector | Ejecución | Si la connection expira, nodos de app fallan en runtime |
| **Nodes** | App nodes | Ejecución | App nodes usan `channel.NewService()` con la connection |
| **Integrations** | Conexiones activas | Datos | Cada integration referencia una connection |
| **Webhooks** | Webhook callbacks | Ejecución | Webhooks de apps necesitan connection activa |

### Módulos que afectan a Connections
| Módulo origen | Componente | Tipo | Ejemplo |
|--------------|------------|-----------------|---------| 
| **Services** | Catálogo de apps | Datos | Las connections dependen de la config del app/service |
| **Auth** | Permisos | API | Solo users con permisos pueden gestionar connections |
| **Developer Apps** | Apps de desarrollo | Datos | Dev apps definen los tipos de auth disponibles |

### Tablas compartidas
| Tabla | Módulos que la usan | Riesgo si cambia |
|-------|---------------------|------------------|
| `connections` (PG) | Connections, Integrations, Boards (runtime) | Cambios rompen auth de todos los flows |
| `apps` (PG) | Connections, Services, Developer Apps | Config de auth afecta flujo de OAuth |

---

## Historial de Actualizaciones

| Fecha | Tickets | Cambios | Actualizado por |
|-------|---------|---------|----------------|
| Initial | — | Creación inicial desde exploración de repos | QA Catalyst |
| 2026-06-06 | — | Backend Logic (channel package) + Impacto Cruzado | QA Catalyst |
| 2026-07-09 | IONF-996 | App-Scope M2M API: 5 endpoints CRUD connections, 4 scopes OAuth, ConnectionM2MResource, seguridad de app_id desde token | QA Catalyst (batch v0.1.0) |
