# Módulo: Webhooks

> Gestión de URLs de webhooks genéricos y dedicados obtenidos desde el canvas.

## Información General

| Campo | Valor |
|-------|-------|
| Nombre interno | webhooks |
| Criticidad | 🟠 Alto |
| Repos involucrados | `gateway-ion` (UI), `gateway` (API) |
| Última actualización | Initial setup — Fase 5 |

---

## Rutas del Frontend (gateway-ion)

| Ruta | Vista | Componente | Permiso |
|------|-------|-----------|---------|
| `/webhooks` | Lista de webhooks | `views/tenant/webhooks/list.vue` | `READ_WEBHOOK` |

---

## API Endpoints (gateway — `routes/tenants.php`)

| Método | Endpoint | Permiso | Descripción |
|--------|----------|---------|-------------|
| GET | `/1.0/tenants/{tenant}/webhooks` | `read-webhook` | Lista de webhooks |
| PUT | `/1.0/tenants/{tenant}/webhooks/{webhook}/enable` | `update-webhook` | Activar webhook |
| PUT | `/1.0/tenants/{tenant}/webhooks/{webhook}/disable` | `update-webhook` | Desactivar webhook |
| DELETE | `/1.0/tenants/{tenant}/webhooks/{webhook}` | `delete-webhook` | Eliminar webhook |

> ⚠️ Los webhooks NO se crean desde esta vista. Se crean dentro de un **App Connector** (ver módulo connections → app-webhooks).

- `2022_02_14_235329_create_webhooks_table.php`
- `2023_10_11_234245_create_webhooks_module_table.php`
- `2025_07_28_185521_add_column_uuid_webhook.php`
- `2025_11_07_232407_make_event_nullable_in_webhooks_table.php`

---

## Reglas de Negocio

1. Los webhooks pueden ser eliminados y se pierde la referencia — deben almacenarse correctamente
2. Cada webhook pertenece a una company
3. Los webhooks son triggers para los flows

---

## Lógica Backend (flow_binaries)

> Fuente: `../flow_binaries/docs/backend/services/`

### Servicios involucrados
| Service | Archivo | Función |
|---------|---------|---------|
| `CompanyWebhookService` | `backend/ion/services/company_webhook_service.go` | CRUD de webhooks por company |
| `AccountWebhookService` | `backend/ion/services/account_webhook_service.go` | CRUD de webhooks por account |

### Modelo de ejecución
- **Patrón de BD**: Tenant (`CompanySchema("webhooks")`) para webhooks de company
- **Multi-tenant**: Sí — webhooks aislados por company
- **Trigger**: `HandleWebhook(tenantId, webhookUuid, payload)` → busca webhook → obtiene flow → ejecuta flow con el payload
- **Flujo**: HTTP POST al webhook URL → `HandleWebhook()` → `ExecuteFlow()` con el payload como input

### Archivos centinela
| Repo | Archivo | Razón |
|------|---------|-------|
| flow_binaries | `backend/ion/services/company_webhook_service.go` | CRUD webhooks |
| flow_binaries | `backend/ion/controllers/` | Controller que recibe el webhook |
| flow_binaries | `backend/routes/api.go` | Rutas webhook |

---

## Impacto Cruzado

### Módulos que Webhooks afecta
| Módulo destino | Componente afectado | Tipo | Ejemplo |
|---------------|--------------------|-----------------|---------| 
| **Boards** | Trigger de flows | Ejecución | Un webhook inicia un flow con `HandleWebhook()` |
| **Executions** | Historial | Datos | Cada webhook trigger crea una ejecución |

### Módulos que afectan a Webhooks
| Módulo origen | Componente | Tipo | Ejemplo |
|--------------|------------|-----------------|---------| 
| **Boards** | Flows con webhook trigger | Datos | Los flows definen los webhooks que escuchan |
| **Connections** | Webhooks de connectors | Datos | Los connectors definen webhooks dedicados |
| **Auth** | Permisos | API | Solo users autorizados gestionan webhooks |

---

## Historial de Actualizaciones

| Fecha | Tickets | Cambios | Actualizado por |
|-------|---------|---------|----------------|
| Initial | — | Creación inicial | QA Catalyst |
| 2026-06-07 | — | Backend Logic + Impacto Cruzado | QA Catalyst |
