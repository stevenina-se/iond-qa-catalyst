# Módulo: Developer Apps

> Apps de desarrollo donde se vinculan los accounts y gestionan los services.

## Información General

| Campo | Valor |
|-------|-------|
| Nombre interno | developer-apps |
| Criticidad | 🟠 Alto |
| Repos involucrados | `gateway-ion` (UI), `gateway` (API) |
| Última actualización | Initial setup — Fase 5 |

---

## Rutas del Frontend (gateway-ion)

| Ruta | Vista | Componente | Permiso |
|------|-------|-----------|---------|
| `/developer-apps` | Lista de developer apps | `views/tenant/developer-apps/list.vue` | `READ_DEVELOPER_APP` |
| `/developer-apps/:id/configure` | Configurar app | `views/tenant/developer-apps/configure.vue` | `UPDATE_DEVELOPER_APP` |

---

## API Endpoints

### Developer Apps (gateway — `routes/api.php` v2.0)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/2.0/user/apps` | Lista de apps del developer |
| GET | `/2.0/user/apps/{appId}` | Detalle de app |
| POST | `/2.0/user/apps` | Crear app |
| PUT | `/2.0/user/apps/{appId}` | Actualizar app |
| DELETE | `/2.0/user/apps/{appId}` | Eliminar app |
| POST | `/2.0/user/apps/{appId}/logo` | Subir logo |
| GET | `/2.0/user/apps/{appId}/webhook` | URL del webhook de la app |

### OAuth Clients (para API access)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/2.0/user/clients` | Lista de OAuth clients |
| GET | `/2.0/user/clients/{clientId}` | Detalle |
| GET | `/2.0/user/clients/{clientId}/secret` | Secret del client |
| POST | `/2.0/user/clients` | Crear client |
| PUT | `/2.0/user/clients/{clientId}` | Actualizar |
| DELETE | `/2.0/user/clients/{clientId}` | Eliminar |

### Services vinculados a la App

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/2.0/user/apps/{appId}/services` | Lista services vinculados |
| GET | `/2.0/user/apps/{appId}/services/{serviceId}` | Detalle |
| POST | `/2.0/user/apps/{appId}/services` | Vincular service |
| PUT | `/2.0/user/apps/{appId}/services/{serviceId}` | Actualizar |
| DELETE | `/2.0/user/apps/{appId}/services/{serviceId}` | Desvincular |
| PUT | `/2.0/user/apps/{appId}/services-sync` | Sincronizar services |

### Integrations de la App

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/2.0/user/apps/{appId}/integrations` | Lista integraciones |
| GET | `/2.0/user/apps/{appId}/integrations/{intId}` | Detalle |
| POST | `/2.0/user/apps/{appId}/integrations/{intId}/claim` | Reclamar integración |

### Tenant Endpoints

| Método | Endpoint | Permiso | Descripción |
|--------|----------|---------|-------------|
| POST | `/1.0/tenants/{tenant}/developer-apps/{appId}/logo` | `update-developer-app` | Subir logo |
| DELETE | `/1.0/tenants/{tenant}/developer-apps/{appId}/logo` | `update-developer-app` | Eliminar logo |

---

## Reglas de Negocio

1. En caso de fallar, las integraciones instaladas (GRAPPs) pueden quedar inutilizables
2. Las apps de desarrollo se vinculan con accounts
3. Gestionan los services asociados
4. Incluyen gestión de precios y pagos

---

## Lógica Backend (flow_binaries)

> Fuente: `../flow_binaries/packages/channel/models/`

### Modelo de ejecución
- **Patrón de BD**: Global (`database.GetConnection()`) — dev apps son globales
- **Multi-tenant**: No — las dev apps son a nivel account, no company
- **Channel models**: `App`, `AppAction`, `AppConnection`, `AppWebhook`, `Field` definen el schema de la dev app

### Archivos centinela
| Repo | Archivo | Razón |
|------|---------|-------|
| flow_binaries | `packages/channel/models/app.go` | Modelo de App |
| flow_binaries | `packages/channel/models/app_action.go` | Acciones disponibles |
| flow_binaries | `packages/channel/models/app_connection.go` | Config de conexión |
| flow_binaries | `packages/channel/models/app_webhook.go` | Config de webhooks |
| flow_binaries | `packages/channel/models/field.go` | Definiciones de campos |

---

## Impacto Cruzado

### Módulos que Developer Apps afecta
| Módulo destino | Componente afectado | Tipo | Ejemplo |
|---------------|--------------------|-----------------|---------| 
| **Services** | Catálogo | Datos | Dev apps crean services/apps en el catálogo |
| **Connections** | Config de connector | Datos | Dev apps definen los tipos de auth de los connectors |
| **Integrations** | Tipos disponibles | Datos | Las integraciones disponibles vienen de dev apps |

### Módulos que afectan a Developer Apps
| Módulo origen | Componente | Tipo | Ejemplo |
|--------------|------------|-----------------|---------| 
| **Accounts** | Accounts | Datos | Las dev apps se vinculan a accounts |
| **Auth** | Permisos admin | API | Solo admins pueden gestionar dev apps |

---

## Historial de Actualizaciones

| Fecha | Tickets | Cambios | Actualizado por |
|-------|---------|---------|----------------|
| Initial | — | Creación inicial | QA Catalyst |
| 2026-06-07 | — | Backend Logic + Impacto Cruzado | QA Catalyst |
