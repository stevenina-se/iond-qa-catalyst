# Módulo: Services (Catalog)

> Catálogo de services disponibles donde es posible crear nuevos services (GRAPPs en su mayoría).

## Información General

| Campo | Valor |
|-------|-------|
| Nombre interno | services / catalog |
| Criticidad | 🟠 Alto |
| Repos involucrados | `gateway-ion` (UI), `gateway` (API) |
| Última actualización | Initial setup — Fase 5 |

---

## Rutas del Frontend (gateway-ion)

| Ruta | Vista | Componente | Permiso |
|------|-------|-----------|---------|
| `/services` | Lista de services | `views/tenant/services/list.vue` | `READ_TENANT_SERVICE` |
| `/admin/settings/categories` | Admin: categorías | `views/admin/settings/categories/List.vue` | Admin |

### Servicios clave
- `services/services.service.ts` — CRUD de services
- `services/categories.service.ts` — Gestión de categorías

---

## Schema de BD (PostgreSQL — gateway)

- `2022_03_31_215915_create_services_table.php`
- `2024_04_23_211719_add_configuration_json_to_services.php`
- `2024_07_09_140222_add_operations_services.php`
- `2024_07_17_031616_create_categories_table.php`
- `2024_07_17_191616_create_service_category_table.php`
- `2024_07_17_200222_add_tags_services.php`
- `2025_05_08_192616_update_services_columns_constraints.php`
- `2025_05_11_200850_add_category_services_table.php`
- `2025_07_29_140616_add_tenant_app_reference_in_services.php`
- `2026_01_15_151640_create_service_history_table.php`
- `2026_03_09_143000_create_fts_index_in_service_table.php`
- `2026_05_11_141610_add_company_columns.php`

---

## API Endpoints

### Services CRUD (gateway — `routes/api.php`)

| Método | Endpoint | Permiso | Descripción |
|--------|----------|---------|-------------|
| GET | `/1.0/services` | `read-integration` | Lista de services |
| GET | `/1.0/services/{service}` | `read-integration` | Detalle |
| POST | `/1.0/services` | `create-integration` | Crear service |
| PUT | `/1.0/services/{service}` | `update-service` | Actualizar |
| DELETE | `/1.0/services/{service}` | `delete-service` | Eliminar |
| POST | `/1.0/services/{service}/logo` | `create-integration` | Subir logo |
| GET | `/1.0/services/logos` | `read-integration` | Obtener logos |

### Prices (gateway — `routes/api.php`)

| Método | Endpoint | Permiso | Descripción |
|--------|----------|---------|-------------|
| GET | `/1.0/prices` | `read-integration` | Lista de precios |
| GET | `/1.0/prices/{price}` | `read-integration` | Detalle |
| POST | `/1.0/prices` | `create-integration` | Crear precio |
| PUT | `/1.0/prices/{price}` | `create-integration` | Actualizar |
| DELETE | `/1.0/prices/{price}` | `create-integration` | Eliminar |

### Categories (gateway — `routes/api.php`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/1.0/categories` | Lista de categorías |
| POST | `/1.0/categories` | Crear categoría |
| PUT | `/1.0/categories/{category}` | Actualizar |
| DELETE | `/1.0/categories/{category}` | Eliminar |

### Tenant Services (gateway — `routes/tenants.php`)

| Método | Endpoint | Permiso | Descripción |
|--------|----------|---------|-------------|
| POST | `/1.0/tenants/{tenant}/services/{serviceId}/logo` | `update-tenant-service` | Subir logo |
| DELETE | `/1.0/tenants/{tenant}/services/{serviceId}/logo` | `update-tenant-service` | Eliminar logo |

### Webcomponent Services (acceso externo)

| Método | Endpoint | Scope | Descripción |
|--------|----------|-------|-------------|
| GET | `/2.0/webcomponent/services` | `integration-read` | Lista para el account |
| GET | `/2.0/webcomponent/services-type/{serviceType}` | `integration-read` | Filtrar por tipo |

### Developer App Services

| Método | Endpoint | Scope | Descripción |
|--------|----------|-------|-------------|
| GET | `/2.0/user/apps/{appId}/services` | auth:api | Lista services de una app |
| POST | `/2.0/user/apps/{appId}/services` | auth:api | Vincular service |
| PUT | `/2.0/user/apps/{appId}/services/{serviceId}` | auth:api | Actualizar |
| DELETE | `/2.0/user/apps/{appId}/services/{serviceId}` | auth:api | Desvincular |

---

## Reglas de Negocio — GRAPPs

> **GRAPP** = Global Reusable APP. Es el concepto central del ecosistema Ionflow.

### ¿Qué es un GRAPP?
1. Un **GRAPP** es un service que combina un App Connector (global) + un Flow (global) + una interfaz Webcomponent
2. Permite a **accounts de terceros** instalar y usar integraciones sin necesidad de configurar flows manualmente
3. Es el producto que Ionflow ofrece a sus clientes finales

### Ciclo de vida de un GRAPP
```
Developer crea App Connector (company)
    ↓ Migración a Global (admin aprueba)
Developer crea Flow (company)
    ↓ Migración a Global (admin aprueba, NO debe tener nodos company)
Developer crea Service → vincula App + Flow
    ↓
Service se publica en el catálogo
    ↓
Account instala el Service → crea una Integración
    ↓
Integración se ejecuta via webcomponent o schedule
```

### Reglas clave
1. Un service es la **fachada** que los accounts ven e instalan
2. Los services tienen **precios** asociados (pueden ser gratuitos o pagos)
3. Los services tienen **categorías** y **tags** para facilitar la búsqueda (FTS)
4. Los services tienen **historial de versiones** (`service_history`)
5. Un service puede tener múltiples **integraciones activas** (una por account)
6. Los services se asocian a companies (multi-tenant) — filtrado por `company_id`

---

## Lógica Backend (flow_binaries)

> Fuente: `../flow_binaries/docs/backend/services/`, `docs/backend/database-connections.mdx`

### Servicios involucrados
| Service | Archivo | Función |
|---------|---------|---------|
| `CompanyAppService` | `backend/ion/services/company_app_service.go` | CRUD de apps por company |
| `AccountAppService` | `backend/ion/services/account_app_service.go` | CRUD de apps por account |

### Modelo de ejecución
- **Patrón de BD**: Global (`database.GetConnection()`) para catálogo de services/apps
- **Multi-tenant**: Parcial — el catálogo es global pero las instancias son por company/account
- **Relación con Channel**: Los services definen el tipo de auth que usa `packages/channel/`

### Archivos centinela
| Repo | Archivo | Razón |
|------|---------|-------|
| flow_binaries | `backend/ion/services/company_app_service.go` | CRUD apps company |
| flow_binaries | `backend/ion/services/account_app_service.go` | CRUD apps account |
| flow_binaries | `packages/channel/models/app.go` | Modelo de App |
| flow_binaries | `packages/channel/models/app_action.go` | Acciones de App |

---

## Impacto Cruzado

### Módulos que Services afecta
| Módulo destino | Componente afectado | Tipo | Ejemplo |
|---------------|--------------------|-----------------|---------| 
| **Connections** | Tipo de connector | Datos | Los services definen los connectors disponibles |
| **Integrations** | Tipo de integración | Datos | Las integrations se crean desde services |
| **Nodes** | App nodes | Ejecución | App nodes usan services para ejecutar acciones |

### Módulos que afectan a Services
| Módulo origen | Componente | Tipo | Ejemplo |
|--------------|------------|-----------------|---------| 
| **Developer Apps** | Creación de services | Datos | Dev apps crean y gestionan services |
| **Accounts** | Instancias | Datos | Accounts instalan services |

---

## Historial de Actualizaciones

| Fecha | Tickets | Cambios | Actualizado por |
|-------|---------|---------|----------------|
| Initial | — | Creación inicial | QA Catalyst |
| 2026-06-07 | — | Backend Logic + Impacto Cruzado | QA Catalyst |
