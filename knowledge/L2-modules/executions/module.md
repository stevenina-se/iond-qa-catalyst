# Módulo: Executions (Historial de Ejecuciones)

> Módulo que registra y muestra el historial de ejecuciones de cada flow, incluyendo consumo de unidades de procesamiento.

## Información General

| Campo | Valor |
|-------|-------|
| Nombre interno | executions |
| Criticidad | 🟠 Alto |
| Repos involucrados | `gateway-ion` (UI), `gateway` (API), `flow_binaries` (motor + SQLite) |
| Última actualización | Initial setup — Fase 5 |

---

## Rutas del Frontend (gateway-ion)

| Ruta | Vista | Componente | Permiso |
|------|-------|-----------|---------|
| `/executions` | Lista de ejecuciones | `views/tenant/executions/list.vue` | `READ_EXECUTION` |

---

## API Endpoints (gateway — `routes/tenants.php`)

| Método | Endpoint | Permiso | Descripción |
|--------|----------|---------|-------------|
| GET | `/1.0/tenants/{tenant}/executions` | `read-execution` | Lista de ejecuciones |
| GET | `/1.0/tenants/{tenant}/executions/{execution}` | `read-execution` | Detalle de ejecución |
| DELETE | `/1.0/tenants/{tenant}/executions/{execution}` | `delete-execution` | Eliminar ejecución |

---

## Lógica de Ejecución (flow_binaries)

> El motor Go ejecuta los flows nodo por nodo. Cada ejecución se almacena en una BD SQLite independiente.

### Ciclo de vida

```
configure → run → [continue → push]* → fin
```

### Datos almacenados por nodo en SQLite

| Campo | Descripción |
|-------|-------------|
| `data` | Configuración del nodo (JSON) |
| `cache` | Cache intermedio durante procesamiento |
| `result` | Resultado final de la ejecución del nodo |
| `status` | `pending` → `processing` → `success` / `error` |

### Services clave (flow_binaries)

- `flow_logger.go` — Registra logs de ejecución (info/warning/error)
- `node_service.go` — CRUD de nodos en SQLite
- `queue_service.go` — Gestión de la cola de ejecución
- `edge_service.go` — Resolución de edges (qué nodo sigue)
- `workspace_service.go` — Inicializa el workspace por flow
2. Se registra el resultado por cada nodo ejecutado
3. Los logs de ejecución aún son simples pero se cuenta con el resultado de cada ejecución
4. Las ejecuciones se filtran por company (multi-tenant)

---

## Lógica Backend (flow_binaries)

> Fuente: `../flow_binaries/docs/backend/`, `docs/core/execution-model.mdx`

### Servicios involucrados
| Service | Archivo | Función |
|---------|---------|---------|
| `FlowExecutionService` | `backend/ion/services/flow_execution_service.go` | Orquesta ejecución completa |
| `CompanyFlowService` | `backend/ion/services/company_flow_service.go` | Accede al flow para ejecutar |

### Board Engine (motor de ejecución)
| Componente | Archivo | Función |
|-----------|---------|---------|
| `ExecutionEngine` | `backend/ion/board/engine.go` | Lifecycle de ejecución (Start/Pause/Resume/Stop) |
| `CompanyDevFlow` | `backend/ion/board/company_dev_flow.go` | Modo Dev — WebSocket con feedback en tiempo real |
| `CompanyLiveFlow` | `backend/ion/board/company_live_flow.go` | Modo Live — Background sin WebSocket |
| `Hub` | `backend/ion/board/hub.go` | Gestión de conexiones WebSocket |

### Modelo de ejecución
- **Patrón de BD**: SQLite por ejecución (cada flow crea `<flowId>.db`)
- **Multi-tenant**: Sí — las ejecuciones están aisladas por company
- **Estados**: `pending` → `running` → `completed` / `error` / `paused` / `waiting_input` / `stopped`
- **Modo Dev**: Step-by-step con WebSocket feedback, Pause/Resume/Stop
- **Modo Live**: Background, persiste estado, sin feedback real-time

### Archivos centinela
| Repo | Archivo | Razón |
|------|---------|-------|
| flow_binaries | `backend/ion/board/engine.go` | Motor principal |
| flow_binaries | `backend/ion/board/company_dev_flow.go` | Ejecución Dev |
| flow_binaries | `backend/ion/board/company_live_flow.go` | Ejecución Live |
| flow_binaries | `core/actions/flow/flow.go` | Core API (LoadFlow/RunNode/PushNode/ContinueNode) |
| flow_binaries | `core/db/database.go` | Schema SQLite de ejecución |

---

## Impacto Cruzado

### Módulos que Executions afecta
| Módulo destino | Componente afectado | Tipo | Ejemplo |
|---------------|--------------------|-----------------|---------| 
| **Dashboard** | Métricas/Stats | Datos | Dashboard muestra conteos y stats de ejecuciones |
| **Billing** | Consumo de unidades | Datos | Cada ejecución consume unidades de procesamiento |

### Módulos que afectan a Executions
| Módulo origen | Componente | Tipo | Ejemplo |
|--------------|------------|-----------------|---------| 
| **Boards** | Trigger de ejecución | Ejecución | Un flow trigger (webhook, schedule) crea la ejecución |
| **Nodes** | Resultado por nodo | Datos | Cada nodo genera registros en SQLite |
| **Connections** | Estado de auth | Ejecución | Si una connection expira mid-execution, el nodo falla |
| **Webhooks** | Webhook triggers | Ejecución | `HandleWebhook()` inicia un flow y crea ejecución |

### Tablas compartidas
| Tabla | Módulos que la usan | Riesgo si cambia |
|-------|---------------------|------------------|
| `nodes` (SQLite) | Executions, Nodes, Boards | Status de nodos afecta historial |
| `logs` (SQLite) | Executions | Logs de ejecución para debugging |
| `queues`/`stacks` (SQLite) | Executions, Boards (core) | Motor de ejecución |

---

## Historial de Actualizaciones

| Fecha | Tickets | Cambios | Actualizado por |
|-------|---------|---------|----------------|
| Initial | — | Creación inicial | QA Catalyst |
| 2026-06-06 | — | Backend Logic (Board Engine, execution model) + Impacto Cruzado | QA Catalyst |
