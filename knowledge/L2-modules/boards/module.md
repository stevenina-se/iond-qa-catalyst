# Módulo: Boards / Workflows

> Módulo de gestión de Boards (flows/workflows) en Ionflow. Es el módulo más crítico del producto.

## Información General

| Campo | Valor |
|-------|-------|
| Nombre interno | workflows / boards |
| Criticidad | 🔴 Crítico |
| Repos involucrados | `gateway-ion` (UI), `gateway` (API), `webcomponents-flow` (canvas) |
| Última actualización | Initial setup — Fase 5 |

---

## Rutas del Frontend (gateway-ion)

| Ruta | Vista | Componente | Permiso |
|------|-------|-----------|---------|
| `/workflows` | Lista de boards | `views/tenant/workflows/list.vue` | `READ_BOARD` |
| `/workflows/edit/:id` | Editor de flow (canvas) | `views/tenant/workflows/edit.vue` | `UPDATE_BOARD` |
| `/admin/workflows` | Admin: lista de boards globales | `views/admin/workflows/Index.vue` | Admin |

### Componentes clave
- `views/tenant/workflows/components/` — Componentes del módulo
- `views/tenant/workflows/services/` — Servicios API del módulo
  - `flow.service.ts` — CRUD de flows
  - `flow.key.service.ts` — Gestión de claves de flows
  - `flow.store.service.ts` — Store de datos de flows
  - `ws.service.ts` — WebSocket para ejecución en tiempo real

### Canvas (webcomponents-flow)
> ⚠️ El canvas NO está en gateway-ion. Está en `webcomponents-flow` y se importa via CDN.
- `webcomponents-flow/src/flow/` — Componentes del canvas (nodos, edges, drawer)
- Los tests E2E del canvas NO son automatizables con Playwright (aún)

---

## API Endpoints

### CRUD de Flows (gateway — `routes/tenants.php`)

| Método | Endpoint | Permiso | Descripción |
|--------|----------|---------|-------------|
| GET | `/1.0/tenants/{tenant}/flows` | `read-board` | Lista de flows de la company |
| GET | `/1.0/tenants/{tenant}/flows/{flow}` | `read-board` | Detalle de un flow |
| POST | `/1.0/tenants/{tenant}/flows` | `create-board` | Crear flow |
| PUT | `/1.0/tenants/{tenant}/flows/{flow}` | `update-board` | Actualizar flow |
| DELETE | `/1.0/tenants/{tenant}/flows/{flow}` | `delete-board` | Eliminar flow |

### Ejecución de Flows (gateway → proxy a flow_binaries)

| Método | Endpoint | Permiso | Descripción |
|--------|----------|---------|-------------|
| POST | `/1.0/tenants/{tenant}/flows/configure` | `update-board` | Cargar flow en motor (LoadFlow) |
| POST | `/1.0/tenants/{tenant}/flows/run` | `update-board` | Ejecutar nodo inicial (RunNode) |
| POST | `/1.0/tenants/{tenant}/flows/push` | `update-board` | Avanzar al siguiente nodo (PushNode) |
| POST | `/1.0/tenants/{tenant}/flows/continue` | `update-board` | Continuar la ejecución (ContinueNode) |
| POST | `/1.0/tenants/{tenant}/flows/run-mapper` | `update-board` | Ejecutar sub-flow mapper |

### Migración a Global (gateway — `routes/api.php`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| PUT | `/1.0/companies/{company}/flow/{appId}/migrate` | Migrar flow a global (GRAPP) |
| GET | `/1.0/companies/{company}/flows` | Listar flows de una company |

### Ciclo de ejecución en flow_binaries (Go)

```
1. LoadFlow(flowId, flow)     → Crea SQLite, guarda nodos/edges en workspace
2. RunNode(flowId, nodeId)    → Resuelve expresiones, inicia la queue
3. ContinueNode(flowId)      → Obtiene siguiente nodo de la queue
4. PushNode(flowId, outputs)  → Ejecuta nodo, fan-out por edges, persiste
5. Repeat 3-4 hasta queue vacía
```

> **Nota**: `flow_binaries` expone estos métodos via su propio servidor HTTP en `backend/routes/api.go`. Gateway actúa como proxy.

---

## Schema de BD

### PostgreSQL (gateway)
> Fuente: `gateway/database/migrations/`
- `2024_10_30_095742_create_flows_table.php`
- `2024_10_30_095942_create_mappers_table.php`
- `2025_07_24_231934_add_tenant_flow_reference_column.php`
- `2025_10_10_152939_update_flows_table_for_git.php`
- `2026_04_02_200000_add_missing_columns_to_flows_table.php`

**Tablas principales:** `flows`, `mappers`

### SQLite (flow_binaries — por cada ejecución)
> Schema completo en `core/db/database.go`. Cada flow crea su propia BD `<flowId>.db`

| Tabla | Función |
|-------|---------|
| `nodes` | Estado de cada nodo (data, status, cache, result) |
| `edges` | Conexiones entre nodos (source → target) |
| `outputs` | Salidas de cada nodo (múltiples por nodo) |
| `queues` | Cola de ejecución (nodos pendientes) |
| `stacks` | Historial de traversal del flow |
| `logs` | Logs de ejecución (info, warning, error) |
| `variables` | Variables globales del flow (key-value) |
| `aggregates` | Datos parciales para nodos Aggregate |

---

## Reglas de Negocio

1. Un flow solo puede ejecutarse si está en estado **Active** (Production)
2. Si se ejecuta desde el canvas → modo **Development** (ejecución manual)
3. Un flow en Development debe ejecutarse manualmente para escuchar el trigger
4. Para ser migrado a global (GRAPP), el flow NO debe contener nodos de connectors de tipo company
5. Cada flow pertenece a una **company** (multi-tenant)
6. El historial de ejecuciones registra el consumo en unidades de procesamiento

---

## Dependencias con otros módulos

| Módulo | Relación |
|--------|----------|
| **Connections** (App Connectors) | Los flows usan nodos de connectors |
| **Executions** | Historial de ejecuciones de flows |
| **Webhooks** | Los flows pueden tener triggers de webhooks |
| **Data Store** | Los flows pueden acceder a datos persistentes |
| **PDF Templates** | Los flows pueden generar PDFs |
| **Canvas** (webcomponents-flow) | La edición visual del flow |

---

## Lógica Backend (flow_binaries)

> Fuente: `../flow_binaries/docs/architecture.mdx`, `docs/core/`, `docs/backend/`

### Servicios involucrados
| Service | Archivo | Función |
|---------|---------|---------|
| `CompanyFlowService` | `backend/ion/services/company_flow_service.go` | CRUD de flows por company (List, Get, Create, Update, Delete) |
| `AccountFlowService` | `backend/ion/services/account_flow_service.go` | CRUD de flows a nivel account (global) |
| `FlowExecutionService` | `backend/ion/services/flow_execution_service.go` | Orquesta la ejecución de flows |
| `ScheduleService` | `backend/ion/services/schedule_service.go` | Cron scheduling para flows programados |

### Controladores
| Controller | Archivo | Endpoints |
|-----------|---------|-----------|
| `CompanyFlowController` | `backend/ion/controllers/company_flow_controller.go` | Tenant CRUD + ejecución |
| `AccountFlowController` | `backend/ion/controllers/account_flow_controller.go` | Account CRUD global |

### Modelo de ejecución
- **Patrón de BD**: Tenant (`CompanySchema()`) para datos de flows, SQLite por ejecución
- **Multi-tenant**: Sí — `company.CompanySchema(models.FlowTableName())` aísla flows por company
- **Nodos relacionados**: TODOS (el flow es el contenedor de nodos)
- **Board Engine**: WebSocket en `backend/ion/board/` — modos Dev (con feedback WS) y Live (background)
- **Estados de ejecución**: `pending` → `running` → `completed` / `error` / `paused` / `waiting_input` / `stopped`

### Core API (ciclo de ejecución Go)
| Función | Archivo | Qué hace |
|---------|---------|----------|
| `LoadFlow()` | `core/actions/flow/flow.go` | Crea workspace SQLite, inicializa nodos/edges |
| `RunNode()` | `core/actions/flow/flow.go` | Inicia ejecución de un nodo, resuelve expresiones |
| `PushNode()` | `core/actions/flow/flow.go` | Empuja resultados, fan-out por edges |
| `ContinueNode()` | `core/actions/flow/flow.go` | Obtiene siguiente nodo de la queue |

### Archivos centinela
| Repo | Archivo | Razón |
|------|---------|-------|
| flow_binaries | `backend/ion/services/company_flow_service.go` | CRUD principal |
| flow_binaries | `backend/ion/controllers/company_flow_controller.go` | Endpoints API |
| flow_binaries | `backend/ion/board/engine.go` | Motor de ejecución WS |
| flow_binaries | `backend/ion/board/company_dev_flow.go` | Ejecución modo Dev |
| flow_binaries | `backend/ion/board/company_live_flow.go` | Ejecución modo Live |
| flow_binaries | `core/actions/flow/flow.go` | Core API de ejecución |
| flow_binaries | `core/db/database.go` | Schema SQLite de ejecuciones |
| flow_binaries | `backend/routes/api.go` | Rutas REST del backend Go |
| gateway-ion | `src/views/tenant/workflows/` | Vistas UI |

---

## Impacto Cruzado

### Módulos que Boards afecta
| Módulo destino | Componente afectado | Tipo | Ejemplo |
|---------------|--------------------|-----------------|---------| 
| **Executions** | Historial de ejecuciones | Datos | Cada ejecución de flow genera registros en executions |
| **Connections** | Nodos de connectors | Ejecución | Si un flow usa un connector, la ejecución depende de la conexión activa |
| **Webhooks** | Triggers de flows | Ejecución | Un webhook trigger inicia un flow vía `HandleWebhook()` |
| **Data Store** | Nodos Store/DataStore | Datos | Los flows escriben/leen de Data Store SQLite |
| **Nodes** | Todos los nodos del canvas | Ejecución | El flow es el contenedor: si el flow falla, ningún nodo ejecuta |
| **PDF Templates** | Nodo generador de PDFs | Ejecución | Los flows generan PDFs via nodos especializados |

### Módulos que afectan a Boards
| Módulo origen | Componente | Tipo | Ejemplo |
|--------------|------------|-----------------|---------| 
| **Auth** | Permisos | API | Sin `READ_BOARD`/`UPDATE_BOARD` no se puede acceder a flows |
| **Connections** | Estado de conexión | Ejecución | Si una conexión expira (OAuth), nodos de connector fallan |
| **Integrations** | Conexiones activas | Ejecución | Los flows necesitan integrations activas para nodos de app |
| **Keys** | Credenciales LLM | Ejecución | Flows con nodos AI necesitan keys configuradas |

### Tablas compartidas
| Tabla | Módulos que la usan | Riesgo si cambia |
|-------|---------------------|------------------|
| `flows` (PG) | Boards, Executions, Webhooks | Columnas de flows afectan listados, ejecución e historial |
| `mappers` (PG) | Boards, Data Store | Sub-flows de mapeo afectan transformación de datos |
| `nodes` (SQLite) | Boards, Nodes, Executions | Schema de nodos afecta toda la ejecución |
| `queues` (SQLite) | Boards (core) | El queue es el motor: cambios rompen ejecución |
| `stacks` (SQLite) | Boards (core) | El stack es el historial: cambios rompen referencias `{{$N}}` |

---

## Selectores E2E conocidos
> ⚠️ Pendiente de poblar al explorar el código de las vistas.

---

## Historial de Actualizaciones

| Fecha | Tickets | Cambios | Actualizado por |
|-------|---------|---------|----------------|
| Initial | — | Creación inicial desde exploración de repos | QA Catalyst |
| 2026-06-06 | — | Enriquecido con docs de flow_binaries: servicios, core API, impacto cruzado | QA Catalyst |
