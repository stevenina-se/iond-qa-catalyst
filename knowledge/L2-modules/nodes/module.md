# Módulo: Nodes (Tipos de Nodos del Canvas)

> Catálogo de todos los tipos de nodos disponibles en Ionflow para construir flows. Cada nodo es una acción ejecutable dentro del motor `flow_binaries` (Go).

## Información General

| Campo | Valor |
|-------|-------|
| Nombre interno | core/actions |
| Criticidad | 🔴 Crítico |
| Repo | `flow_binaries` — `core/actions/` |
| Motor | Go + SQLite (ejecución por nodo) |
| Última actualización | 2026-07-09 — v0.1.0 batch update |

---

## ⚠️ Mapeo Backend ↔ Canvas (CRÍTICO para QA)

> Los nombres de los nodos en el backend (`flow_binaries`) **NO coinciden** con los nombres que el usuario ve en el canvas (`webcomponents-flow`). Esta tabla es la referencia oficial.

| # | Nombre en el CANVAS (UI) | Módulo backend | Package (flow_binaries) | Grupo en UI | Icono |
|---|-------------------------|---------------|------------------------|-------------|-------|
| 1 | **Simple Decision** | `ion.action.condition` | `core/actions/condition` | Tools | `filter` |
| 2 | **Form** | `ion.action.mapper` | `core/actions/mapper` | Tools | `mapper` |
| 3 | **Mapper** | `ion.action.transformer` | `core/actions/transformer` | Tools | `transformer` |
| 4 | **Aggregate** | `ion.action.aggregate` | `core/actions/aggregate` | Tools | `aggregate` |
| 5 | **Iterator** | `ion.action.iterator` | `core/actions/iterator` | Tools | `iterator` |
| 6 | **Timer** | `ion.action.timer` | `core/actions/timer` | Tools | `delay` |
| 7 | **Multiple Decision** | `ion.action.switch` | `core/actions/switchnode` | Tools | `list-start` |
| 8 | **Code** | `ion.action.code` | `core/actions/code` | Tools | `code` |
| 9 | **Call Component-Flow** | `ion.action.executeWorkflow` | — (orquesta via API) | Tools | `log-in` |
| 10 | **On Call Component-Flow Trigger** | `ion.action.executeWorkflowTrigger` | — (trigger) | Tools | `log-out` |
| 11 | **Agent** | `ion.action.agent` | — (nuevo) | Tools | `bot` |
| 12 | **Persistent Data Save** | `ion.store.add` | `core/actions/store` | Persistent Data | `database` |
| 13 | **Persistent Data Update** | `ion.store.update` | `core/actions/store` | Persistent Data | `database` |
| 14 | **Persistent Data Get** | `ion.store.get` | `core/actions/store` | Persistent Data | `database` |
| 15 | **Persistent Data Delete** | `ion.store.delete` | `core/actions/store` | Persistent Data | `database` |
| 16 | **Persistent Data Check** | `ion.store.check` | `core/actions/store` | Persistent Data | `database` |
| 17 | **Persistent Data Count** | `ion.store.count` | `core/actions/store` | Persistent Data | `database` |
| 18 | **Persistent Data Delete All** | `ion.store.delete_all` | `core/actions/store` | Persistent Data | `database` |
| 19 | **Persistent Data Search** | `ion.store.search` | `core/actions/store` | Persistent Data | `database` |
| 20 | **Request** (Trigger HTTP) | `com.ion.request` | — (trigger) | Triggers | — |
| 21 | **Webhook Response** | `com.ion.webhook_response` | — (trigger) | Triggers | — |
| 22 | **Schedule** (Trigger programado) | `com.ion.schedule` | — (trigger) | Triggers | — |

> **Fuente**: `webcomponents-flow/src/flow/constants/apps.ts`

### Confusiones comunes a evitar

| ❌ No confundir | ✅ Es realmente |
|----------------|----------------|
| "Mapper" en el canvas | `transformer` en el backend — ejecuta un **sub-flow completo** |
| "Form" en el canvas | `mapper` en el backend — extrae `params` de un mapa |
| "Simple Decision" | `condition` — bifurca en `then`/`false` |
| "Multiple Decision" | `switch` — múltiples reglas/expresiones |

### Drawer de configuración en el Canvas

> Cuando el usuario hace click en un nodo → se abre un **FlowDrawer** con la configuración. Los nodos con drawer custom están en `webcomponents-flow/src/flow/components/FlowDrawer/`:

| Directorio | Nodo | Descripción del drawer |
|-----------|------|----------------------|
| `Agent/` | Agent | Config de system_prompt, input_prompt, timeout |
| `AutoMapper/` | Mapper (transformer) | Editor visual del sub-flow mapper |
| `Code/` | Code | Editor de código con selector Python/JS + botón **Ask FlowPilot** ✨ (IONF-950) |
| `Condition/` | Simple Decision | Config de field/operator/value |
| `Mapper/` | Form (mapper) | Editor de formulario con params |
| `Store/` | Persistent Data | Config de data_store, key, params |
| `SubFlow/` | Call Component-Flow | Selector de Component-Flow |
| `Switch/` | Multiple Decision | Config de mode, rules/expressions |
| `Transformer/` | Mapper (transformer) | Configuración del sub-flow |

> **Fuente completa de specs**: `FlowDrawer/nodeSpecs.ts`

---

## Catálogo de Nodos

### 1. Aggregate (Canvas: "Aggregate")

| Campo | Valor |
|-------|-------|
| Package | `core/actions/aggregate` |
| Función | Agrupa N items que llegan en secuencia y los emite como un array cuando se alcanza el `length` configurado |
| Config | `{ "length": N }` — N debe ser > 0 |
| Inputs | `input` (datos), `input-error` (marca item como error) |
| Outputs | `output` (array de N items), `error` |
| BD | Usa SQLite para almacenar items parciales (tabla `aggregates`) |
| Tests | `aggregate_test.go` |

### 2. Code (Canvas: "Code")

| Campo | Valor |
|-------|-------|
| Package | `core/actions/code` |
| Función | Ejecuta código Python o JavaScript en un servicio externo (Code Runner) via gRPC |
| Lenguajes | `python`, `javascript` |
| Config | `{ "language": "python|javascript", "code_py": "...", "code_js": "...", "variables": [...], "timeout": 1-300, "dependencies": [...] }` |
| Outputs | `output` (resultado), `error` |
| Timeout | 1-300 segundos (default: 30s) |
| Servicio externo | `CODE_RUNNER_URL` (gRPC, puede ser TLS o insecure) |
| Response | `{ status, result, stdout, stderr, error: { type, message, line, traceback }, execution_time_ms }` |
| Tests | `code_test.go` |

**Reglas clave:**
- El código se lee desde `staticData` (no `processedData`) para evitar inyección de expresiones
- Las variables se pasan como pares name/value
- Soporta dependencias externas (pip/npm packages)

**Integración con FlowPilot (IONF-950):**
- Botón ✨ **"Ask Flow Pilot"** en el drawer de configuración del Code node
- Al pulsar, abre el chat de FlowPilot con contexto del nodo: lenguaje, variables, dependencias, nodos downstream
- FlowPilot genera código válido que respeta convenciones del Code Runner: sin `main()`, sin `processedData`, usando `input` para variables y `return` para resultados
- También corrige errores: lee logs de error de ejecución y genera código corregido
- Backend: regla CONFIDENTIALITY en `system.go` del agente para proteger contenido de skills
- Frontend: nuevo módulo `codeContext.ts` (función pura), handler `open_node_copilot` en `FlowEditor.vue`
- Tests: `codeContext.spec.ts` (148 líneas), `FlowEditor.spec.ts`

### 3. Condition (Canvas: "Simple Decision")

| Campo | Valor |
|-------|-------|
| Package | `core/actions/condition` |
| Función | Evalúa condiciones lógicas y rutea el flujo a `then` o `false` |
| Config | Array de condiciones: `[{ "field": "...", "operator": "...", "value": "..." }]` |
| Operadores | `is_equal`, `is_not_equal`, `is_greater`, `is_greater_equal`, `is_less`, `is_less_equal` |
| Outputs | `then` ("By True"), `false` ("By False"), `error` |
| Motor de expresiones | `expr-lang/expr` |
| Tests | `condition_test.go` |

### 4. Iterator (Canvas: "Iterator")

| Campo | Valor |
|-------|-------|
| Package | `core/actions/iterator` |
| Función | Itera sobre un array y emite cada item individualmente como output separado |
| Config | Recibe un array (JSON string o []interface{}) |
| Outputs | `output` (un output por cada item), `error` |
| Tests | No tiene test dedicado |

### 5. Mapper (Canvas: ⚠️ "Form")

| Campo | Valor |
|-------|-------|
| Package | `core/actions/mapper` |
| Función | Extrae el campo `params` de un mapa de datos y lo emite como output |
| Config | `{ "params": { ... } }` |
| Outputs | `output` (el valor de params), `error` |
| Error típico | "Mapper not configured" si no existe el campo `params` |

### 6. Store (Canvas: "Persistent Data [Save/Update/Get/Delete/Check/Count/Delete All/Search]")

| Campo | Valor |
|-------|-------|
| Package | `core/actions/store` |
| Función | CRUD completo sobre la BD persistente (Data Store) del cliente |
| Operaciones | 8 operaciones disponibles (ver tabla) |
| BD | SQLite del cliente (ruta `clientPath`) |
| Config | `{ "data_store": "<UUID>", "params": { "key": "...", ... }, "metadata": {...} }` |
| Tests | `store_test.go`, `store_add_test.go`, `store_update_test.go`, `store_search_test.go`, `store_params_test.go` |

**Operaciones del Store:**

| Tipo | Constante | Descripción |
|------|-----------|-------------|
| Add | `ion.store.add` | Insertar registro |
| Update | `ion.store.update` | Actualizar registro |
| Get | `ion.store.get` | Obtener registro por key |
| Delete | `ion.store.delete` | Eliminar registro por key |
| Check | `ion.store.check` | Verificar si existe un registro |
| Count | `ion.store.count` | Contar registros |
| Delete All | `ion.store.delete_all` | Eliminar todos los registros |
| Search | `ion.store.search` | Buscar registros con filtros |

### 7. Switch (Canvas: "Multiple Decision")

| Campo | Valor |
|-------|-------|
| Package | `core/actions/switchnode` |
| Función | Nodo de decisión múltiple con dos modos: reglas y expresiones |
| Modos | `rules` (reglas predefinidas), `expression` (expresiones evaluadas) |
| Config | `{ "mode": "rules|expression", "data": [...] }` |
| Operadores | `is_equal`, `is_not_equal`, `is_greater`, `is_greater_equal`, `is_less`, `is_less_equal` |
| Config Switch (rules) | Cada regla: `{ id, label, field, operator, value, type }` |
| Operadores Switch | `is_equal_to`, `is_not_equal_to`, `contains`, `does_not_contain`, `starts_with`, `does_not_starts_with`, `ends_with`, `does_not_ends_with`, `is_greater_than`, `is_less_than`, `is_greater_than_or_equal_to`, `is_less_than_or_equal_to` |
| Tipos Switch | `string`, `number`, `boolean`, `object`, `array` |
| Tests | `switch_test.go` |

### 8. Timer (Canvas: "Timer")

| Campo | Valor |
|-------|-------|
| Package | `core/actions/timer` |
| Función | Pausa la ejecución del flow por un tiempo configurado |
| Config | `{ "minutes": N, "seconds": N }` |
| Límite | Máximo 15 minutos (900 segundos) |
| Outputs | `output` ({ duration, completed_at }), `error` |
| Validaciones | minutes y seconds >= 0, total <= 900s |
| Tests | `timer_test.go` |

### 9. Transformer (Canvas: ⚠️ "Mapper")

| Campo | Valor |
|-------|-------|
| Package | `core/actions/transformer` |
| Nombre en Canvas | **"Mapper"** — ⚠️ NO confundir con `mapper` del backend que es "Form" |
| Función | Ejecuta un sub-flow completo (mapper) dentro de otro flow. Es un mini-motor de ejecución interno |
| Nodos internos | `source` (nodo inicio), `target` (nodo fin), + nodos intermedios |
| BD | Crea su propia instancia SQLite para el sub-flow |
| Ejecución | Queue-based: carga el sub-flow, ejecuta nodo por nodo, retorna el resultado del nodo `target` |

### 10. Flow (Motor de ejecución — NO es un nodo visible en el canvas)

| Campo | Valor |
|-------|-------|
| Package | `core/actions/flow` |
| Función | Motor principal de ejecución de flows. Maneja LoadFlow, RunNode, PushNode, ContinueNode |
| Ciclo de vida | `LoadFlow → RunNode → [ContinueNode → PushNode]* → Fin` |
| BD | SQLite por flow (`<flowId>.db`) |

### 11. Call Component-Flow (Canvas: "Call Component-Flow")

| Campo | Valor |
|-------|-------|
| Módulo | `ion.action.executeWorkflow` |
| Package backend | — (no hay package dedicado, orquesta via API) |
| Función | Invoca un flow reutilizable (Component-Flow) desde otro flow. Permite modularizar la lógica |
| Config | Select → elige qué Component-Flow ejecutar. Opción "New" para crear uno |
| Inputs | `input` |
| Outputs | `output`, `error` |

### 12. On Call Component-Flow Trigger (Canvas: "On Call Component-Flow Trigger")

| Campo | Valor |
|-------|-------|
| Módulo | `ion.action.executeWorkflowTrigger` |
| Package backend | — (trigger, no tiene ejecución propia) |
| Función | Nodo trigger que inicia un Component-Flow cuando es invocado por un nodo "Call Component-Flow" |
| Config | Select → elige qué Component-Flow se dispara |
| Inputs | Ninguno (es un trigger, inicia el flow) |
| Outputs | `output`, `error` |

### 13. Agent (Canvas: "Agent")

| Campo | Valor |
|-------|-------|
| Módulo | `ion.action.agent` |
| Package backend | — (nuevo, en desarrollo) |
| Función | Nodo de agente de IA. Permite ejecutar lógica basada en LLMs dentro del flow |
| Config | `{ system_prompt: string, input_prompt: string (required), timeout: 1-120s }` |
| Inputs | `input` |
| Outputs | `output`, `error` |

### 14. Triggers (Nodos de inicio de flow)

> Estos nodos NO están en `flow_binaries/core/actions/` pero sí existen en el canvas. Son nodos de **inicio** que disparan la ejecución de un flow.

| # | Nombre en Canvas | Módulo | Función |
|---|-----------------|--------|--------|
| a | **Request** (Trigger HTTP) | `com.ion.request` | Inicia el flow cuando recibe un HTTP request |
| b | **Webhook Response** | `com.ion.webhook_response` | Responde al webhook que disparó el flow |
| c | **Schedule** (Trigger programado) | `com.ion.schedule` | Inicia el flow según un schedule configurado |

---

## Schema SQLite de Ejecución

> Cada flow crea su propia BD SQLite. Schema definido en `core/db/database.go`:

### Tabla: `nodes`

| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | TEXT PK | ID del nodo |
| type | TEXT NOT NULL | Tipo de nodo (aggregate, code, condition, etc.) |
| data | TEXT | Datos de configuración del nodo (JSON) |
| data_type | TEXT | Tipo de dato de data |
| status | TEXT | `pending`, `processing`, `success`, `error` |
| updated_at | TIMESTAMP | Última actualización |
| cache | TEXT | Cache intermedio del nodo |
| cache_type | TEXT | Tipo de dato del cache |
| result | TEXT | Resultado final del nodo |
| result_type | TEXT | Tipo de dato del resultado |

### Tabla: `edges`

| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | TEXT PK | ID del edge |
| source | TEXT FK→nodes | Nodo origen |
| target | TEXT FK→nodes | Nodo destino |
| source_handler_id | TEXT | Handle del output origen |
| target_handler_id | TEXT | Handle del input destino |
| data | TEXT | Datos del edge |

### Tabla: `outputs`

| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | INTEGER PK AUTO | ID auto |
| node_id | TEXT FK→nodes | Nodo que generó el output |
| target_handle | TEXT | Handle del output |
| data | TEXT | Datos del output |

### Tabla: `queues`

| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | INTEGER PK AUTO | ID auto |
| data | TEXT | Datos en la cola |
| source/target | TEXT FK→nodes | Nodos origen/destino |
| source_handle/target_handle | TEXT | Handles |
| edge_id | TEXT FK→edges | Edge que conecta |
| status | TEXT | `pending`, `success`, `error` |

### Tabla: `stacks`
> Historial de la ejecución (traversal) del flow. Misma estructura que `queues`.

### Tabla: `logs`

| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | INTEGER PK AUTO | ID auto |
| content | TEXT | Contenido del log |
| type | TEXT | `info`, `warning`, `error` |
| created_at | TIMESTAMP | Fecha |

### Tabla: `variables`
> Variables globales del flow (key-value).

### Tabla: `aggregates`
> Datos parciales para nodos Aggregate (acumulación antes de emitir).

---

## Ciclo de Vida de un Nodo

```
LoadFlow(flowId, flow)
    ↓
RunNode(flowId, nodeId, targetId)
    ↓ (loop)
ContinueNode(flowId) → obtiene siguiente nodo de la queue
    ↓
PushNode(flowId, outputs, message, status) → ejecuta el nodo, fan-out por edges
    ↓ (repeat until queue empty)
FIN
```

**Status posibles de un nodo:**
- `pending` — No ejecutado aún
- `processing` — En ejecución
- `success` — Ejecutado correctamente
- `error` — Error en la ejecución

---

## Reglas de Negocio de Nodos

1. **Todos los nodos tienen handle `error`** — Siempre hay una salida de error
2. **Los datos fluyen por los edges** — Un nodo NO puede acceder a datos de otro nodo directamente
3. **Las expresiones se resuelven** con `libs.ReplaceReferences` antes de ejecutar
4. **Cada ejecución crea una SQLite nueva** — No se reutilizan BDs entre ejecuciones
5. **Si un nodo falla → el edge de error se activa** — El flow puede manejar errores
6. **La queue se restaura en caso de fallo** — Permite retry
7. **El Timer tiene un máximo de 15 minutos** — No se puede hacer un sleep infinito
8. **El Code Runner tiene un timeout máximo de 300s** — Con dependencias externas

## Lógica Backend (flow_binaries)

> Fuente: `../flow_binaries/docs/core/`, `docs/backend/nodes/`

### Arquitectura de nodos
- **Core nodes** (`core/actions/`): Genéricos, sin dependencias externas → condition, switch, mapper, transformer, iterator, timer, store, code, aggregate
- **Backend nodes** (`backend/ion/nodes/`): Plataforma-específicos → request, app nodes (usan `packages/channel/`)
- **Interfaz**: `ActionInterface { Execute() []models.Ot }` — todos los nodos implementan esta interfaz

### Modelo de ejecución
- **Patrón de BD**: SQLite por ejecución (cada flow crea su propia BD)
- **Multi-tenant**: No aplica directamente (el flow ya está aislado por company)
- **Expression Language**: `expr-lang/expr` v1.17.2 — resuelve `{{$1.field}}` desde el stack
- **Output Handles**: `output` (éxito), `error` (fallo) — fan-out por edges

### Archivos centinela
| Repo | Archivo | Razón |
|------|---------|-------|
| flow_binaries | `core/actions/<nodo>/` | Implementación de cada tipo de nodo |
| flow_binaries | `core/models/` | Estructuras de datos: Node, Queue, Stack, Edge |
| flow_binaries | `core/services/` | Servicios de negocio: node, queue, stack, edge |
| flow_binaries | `core/libs/` | Expression language (resolución de `{{$N}}`) |
| flow_binaries | `core/db/database.go` | Schema SQLite de ejecuciones |
| flow_binaries | `backend/ion/nodes/` | Backend nodes (request, app) |
| webcomponents-flow | `src/flow/constants/apps.ts` | Mapeo nombre UI ↔ tipo backend |
| webcomponents-flow | `src/flow/components/FlowDrawer/` | Drawers de configuración |

---

## Impacto Cruzado

### Módulos que Nodes afecta
| Módulo destino | Componente afectado | Tipo | Ejemplo |
|---------------|--------------------|-----------------|---------| 
| **Boards** | Ejecución de flows | Ejecución | Si un nodo falla, el flow se detiene o rutea al edge de error |
| **Executions** | Historial por nodo | Datos | Cada nodo genera registros de resultado en SQLite |
| **Data Store** | Nodos `ion.store.*` | Datos | Los nodos Persistent Data leen/escriben en Data Store |
| **Connections** | Nodos de app | Ejecución | Los app nodes dependen de connections activas |
| **Integrations** | Nodos con auth | Ejecución | OAuth refresh durante ejecución de app nodes |

### Módulos que afectan a Nodes
| Módulo origen | Componente | Tipo | Ejemplo |
|--------------|------------|-----------------|---------| 
| **Boards** | Motor de ejecución | Ejecución | LoadFlow/RunNode/PushNode determinan cómo se ejecutan |
| **Connections** | `packages/channel/` | Ejecución | App nodes necesitan service de channel para auth |
| **Keys** | Credenciales LLM | Ejecución | Agent nodes necesitan API keys |
| **Data Store** | Schema de datos | Datos | Nodos Store dependen del schema del data store del cliente |

### Tablas compartidas
| Tabla | Módulos que la usan | Riesgo si cambia |
|-------|---------------------|------------------|
| `nodes` (SQLite) | Nodes, Boards, Executions | Schema afecta todo el motor de ejecución |
| `queues` (SQLite) | Nodes (core), Boards | Cambios en queue rompen el orden de ejecución |
| `outputs` (SQLite) | Nodes, Executions | Cambios en outputs rompen el historial |

---

## Historial de Actualizaciones

| Fecha | Tickets | Cambios | Actualizado por |
|-------|---------|---------|----------------|
| Initial | — | Catálogo completo desde `flow_binaries/core/actions/` + schema SQLite | QA Catalyst |
| 2026-06-06 | — | Backend Logic + Impacto Cruzado con docs de flow_binaries | QA Catalyst |
| 2026-07-09 | IONF-950 | Integración FlowPilot en Code node: botón Ask FlowPilot, codeContext.ts, CONFIDENTIALITY rule, handler open_node_copilot | QA Catalyst (batch v0.1.0) |
