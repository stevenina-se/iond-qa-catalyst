# Módulo: Integrations (Conexiones activas)

> Gestión de integraciones/conexiones activas entre connectors y apps externas con diferentes métodos de autenticación.

## Información General

| Campo | Valor |
|-------|-------|
| Nombre interno | integrations / connections activas |
| Criticidad | 🟠 Alto |
| Repos involucrados | `gateway-ion` (UI), `gateway` (API) |
| Última actualización | 2026-07-09 — v0.1.0 batch update |

---

## Rutas del Frontend (gateway-ion)

| Ruta | Vista | Componente | Permiso |
|------|-------|-----------|---------|
| `/integrations` | Lista de integraciones | `views/tenant/integrations/IntegrationListView.vue` | `READ_CONNECTION` |

---

## Schema de BD (PostgreSQL — gateway)

- `2022_04_06_222604_create_integrations_table.php`
- `2023_10_11_014626_add_soft_delete_columns_to_integrations.php`
- `2024_05_07_161320_add_app_to_integrations.php`
- `2025_05_14_300001_add_payment_statuses_to_integrations.php`
- `2025_07_09_154117_create_connections_table.php`
- `2025_07_09_161157_create_connection_integration_table.php`

---

## Reglas de Negocio

1. Las integraciones representan conexiones activas con apps externas
2. Cada integración usa un método de autenticación configurado en el connector
3. Las credenciales se almacenan de forma segura
4. Las integraciones tienen soft delete (se pueden restaurar)
5. Pueden tener estados de pago asociados

---

## Lógica Backend (flow_binaries)

> Fuente: `../flow_binaries/docs/backend/services/`, `packages/channel/`

### Servicios involucrados
| Service | Archivo | Función |
|---------|---------|---------|
| `IntegrationService` | `backend/ion/services/integration_service.go` | Manejo de integraciones |
| `AttemptService` | `backend/ion/services/attempt_service.go` | Intentos de conexión OAuth |

### Modelo de ejecución
- **Patrón de BD**: Tenant (`CompanySchema()`) para integraciones de company
- **Multi-tenant**: Sí — integraciones aisladas por company
- **Auth flow**: Channel package maneja OAuth → callback → token → refresh
- **Runtime**: Los app nodes en flows acceden a la integration para obtener credenciales

### Archivos centinela
| Repo | Archivo | Razón |
|------|---------|-------|
| flow_binaries | `backend/ion/services/integration_service.go` | Service principal |
| flow_binaries | `packages/channel/services/` | Motor de auth (authorize, token, refresh, callback) |
| flow_binaries | `packages/channel/models/connection.go` | Modelo de conexión con tokens |

---

## Impacto Cruzado

### Módulos que Integrations afecta
| Módulo destino | Componente afectado | Tipo | Ejemplo |
|---------------|--------------------|-----------------|---------| 
| **Boards** | App nodes en flows | Ejecución | Si la integration expira, nodos de app fallan |
| **Nodes** | App nodes | Ejecución | Los app nodes obtienen credenciales de la integration |
| **Connections** | Estado de conexión | Datos | Las integrations son instancias activas de connections |

### Módulos que afectan a Integrations
| Módulo origen | Componente | Tipo | Ejemplo |
|--------------|------------|-----------------|---------| 
| **Connections** | Config de connector | Datos | La integration se crea desde un connector |
| **Accounts** | Cuentas | Datos | Las accounts instalan integraciones |
| **Developer Apps** | Apps | Datos | Dev apps definen los tipos de integraciones |
| **Auth** | Permisos | API | Permisos para gestionar integraciones |

---

## Historial de Actualizaciones

| Fecha | Tickets | Cambios | Actualizado por |
|-------|---------|---------|----------------|
| Initial | — | Creación inicial | QA Catalyst |
| 2026-06-07 | — | Backend Logic + Impacto Cruzado | QA Catalyst |

---

## API Endpoints

### Integrations / Connections (gateway — `routes/tenants.php`)

| Método | Endpoint | Permiso | Descripción |
|--------|----------|---------|-------------|
| GET | `/1.0/tenants/{tenant}/connections` | `read-connection` | Lista de integraciones activas |
| DELETE | `/1.0/tenants/{tenant}/connections/{connection}` | `delete-connection` | Eliminar integración |

### Integrations legacy (gateway — `routes/api.php`)

| Método | Endpoint | Permiso | Descripción |
|--------|----------|---------|-------------|
| GET | `/1.0/integrations` | `read-integration` | Lista de integraciones |
| GET | `/1.0/integrations/{integration}` | `read-integration` | Detalle |
| POST | `/1.0/integrations` | `create-integration` | Crear |
| PUT | `/1.0/integrations/{integration}` | `update-integration` | Actualizar |
| DELETE | `/1.0/integrations/{integration}` | `delete-integration` | Eliminar |
| POST | `/1.0/{resource}/install` | `read-integration` | Instalar integración (OAuth flow) |

### Webcomponent API (acceso externo desde GRAPPs)

| Método | Endpoint | Scope | Descripción |
|--------|----------|-------|-------------|
| GET | `/2.0/webcomponent/integrations` | `integration-read` | Lista integraciones del account |
| GET | `/2.0/webcomponent/integrations/{id}` | `integration-read` | Detalle |
| POST | `/2.0/webcomponent/integrations/{id}/install` | `integration-install` | Instalar |
| POST | `/2.0/webcomponent/integrations/{id}/uninstall` | `integration-install` | Desinstalar |
| PUT | `/2.0/webcomponent/integrations/{id}` | `integration-update` | Actualizar |
| DELETE | `/2.0/webcomponent/integrations/{id}` | `integration-delete` | Eliminar |
| POST | `/2.0/webcomponent/integrations/{id}/actions` | `integration-event` | Ejecutar acción |
| POST | `/2.0/webcomponent/integrations/{id}/event` | `integration-event` | Ejecutar evento |
| GET | `/2.0/webcomponent/integrations/{id}/executions` | `integration-read` | Historial de ejecuciones |
| GET | `/2.0/webcomponent/integrations/{id}/logs` | `integration-read` | Logs |
| POST | `/2.0/webcomponent/integrations/{id}/schedule` | `integration-schedule` | Crear schedule |
| PUT | `/2.0/webcomponent/integrations/{id}/schedule/{scheduleId}` | `integration-schedule` | Actualizar schedule |
| DELETE | `/2.0/webcomponent/integrations/{id}/schedule/{scheduleId}` | `integration-schedule` | Eliminar schedule |

### App API (acceso programático desde Developer Apps)

| Método | Endpoint | Scope | Descripción |
|--------|----------|-------|-------------|
| GET | `/2.0/app/integrations` | `app:integration-read` | Lista |
| GET | `/2.0/app/integrations/{id}` | `app:integration-read` | Detalle |
| POST | `/2.0/app/integrations/{id}/action` | `app:integration-action` | Ejecutar acción |
| PUT | `/2.0/app/integrations/{id}` | `app:integration-update` | Actualizar |
| DELETE | `/2.0/app/integrations/{id}` | `app:integration-delete` | Eliminar |
| POST | `/2.0/app/integrations/{id}/claim` | `app:integration-claim` | Reclamar |
| PATCH | `/2.0/app/integrations/{id}/status` | `app:integration-update` | Cambiar status |

### Instalación de Grapps via M2M (IONF-996)

> Endpoint para que apps externas instalen grapps en cuentas de clientes de forma programática.

| Método | Endpoint | Scope | Descripción |
|--------|----------|-------|-------------|
| POST | `/2.0/app/accounts/{account:remote_id}/integrations` | `app:integration-create` | Instalar grapp en cuenta → retorna `integration_id` + `gateway_key` |

> **IONF-996**: Este endpoint habilita la automatización completa del flujo de onboarding: una app externa puede crear una cuenta, instalar un grapp, y configurar connections con credenciales encriptadas, todo vía API M2M.

---

## Historial de Actualizaciones

| Fecha | Tickets | Cambios | Actualizado por |
|-------|---------|---------|----------------|
| Initial | — | Creación inicial | QA Catalyst |
| 2026-07-09 | IONF-996 | Endpoint M2M de instalación de grapps: POST integrations, retorna integration_id + gateway_key | QA Catalyst (batch v0.1.0) |
