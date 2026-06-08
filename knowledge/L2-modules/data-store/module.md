# Módulo: Data Store (Persistent Data)

> Mini base de datos en SQLite por backend que obedece a una estructura de datos. Almacena datos históricos.

## Información General

| Campo | Valor |
|-------|-------|
| Nombre interno | data-store / data-structure |
| Criticidad | 🟠 Alto |
| Repos involucrados | `gateway-ion` (UI), `gateway` (API), `flow_binaries` (SQLite) |
| Última actualización | Initial setup — Fase 5 |

---

## Rutas del Frontend (gateway-ion)

| Ruta | Vista | Componente | Permiso |
|------|-------|-----------|---------|
| `/data-store` | Data Store | `views/tenant/data-store/Index.vue` | `READ_DATA_STORE` / `READ_DATA_STRUCTURE` |

---

## Lógica de Negocio (flow_binaries — `core/actions/store/`)

> El Data Store es una mini BD SQLite por cliente (`clientPath`) que almacena datos persistentes. Se accede desde los flows a través de nodos de tipo Store.

### 8 Operaciones disponibles

| Operación | Tipo de nodo | Descripción |
|-----------|-------------|-------------|
| **Add** | `ion.store.add` | Insertar un registro en la tabla |
| **Update** | `ion.store.update` | Actualizar un registro por key |
| **Get** | `ion.store.get` | Obtener un registro por key |
| **Delete** | `ion.store.delete` | Eliminar un registro por key |
| **Check** | `ion.store.check` | Verificar si un registro existe |
| **Count** | `ion.store.count` | Contar registros en la tabla |
| **Delete All** | `ion.store.delete_all` | Eliminar todos los registros |
| **Search** | `ion.store.search` | Buscar registros con filtros |

### Configuración del nodo Store

```json
{
  "data_store": "<UUID de la tabla>",
  "params": {
    "key": "<clave del registro>",
    "...otros params según operación"
  },
  "metadata": { }
}
```

### Arquitectura

- Cada account tiene su propia BD SQLite en `clientPath`
- El `data_store` es un UUID que identifica la tabla dentro de esa BD
- El nodo Store valida que la BD exista antes de operar (`VerifyIfDBExists`)
- Los datos obedecen a una **estructura de datos (Data Structure)** definida previamente

### Reglas clave

1. Si el `clientPath` no existe → error "Persistent Data does not exist"
2. El `data_store` debe ser un UUID válido
3. Las operaciones son atómicas por nodo
4. La búsqueda (Search) soporta filtros complejos con `store_search.go`

---

## Lógica Backend (flow_binaries)

> Fuente: `../flow_binaries/core/actions/store/`, `docs/backend/services/`

### Servicios involucrados
| Service | Archivo | Función |
|---------|---------|---------|
| `DataStoreService` | `backend/ion/services/data_store_service.go` | CRUD de data stores (schemas) |
| `DataStructureService` | `backend/ion/services/data_structure_service.go` | CRUD de data structures |

### Store Node (8 operaciones — `core/actions/store/`)
| Archivo | Operación | Función |
|---------|-----------|---------|
| `store_add.go` | `ion.store.add` | Inserta un registro (key + params) |
| `store_update.go` | `ion.store.update` | Actualiza registro por key |
| `store_get.go` | `ion.store.get` | Obtiene registro por key |
| `store_delete.go` | `ion.store.delete` | Elimina registro por key |
| `store_check.go` | `ion.store.check` | Verifica existencia |
| `store_count.go` | `ion.store.count` | Cuenta registros |
| `store_delete_all.go` | `ion.store.delete_all` | Elimina todos los registros |
| `store_search.go` | `ion.store.search` | Búsqueda con filtros complejos |

### Modelo de ejecución
- **Patrón de BD**: SQLite del cliente (ruta `clientPath`) — independiente del SQLite de ejecución
- **Multi-tenant**: Sí — cada company tiene su propio directorio de data stores
- **`clientPath`**: Ruta al archivo SQLite del cliente (diferente al `<flowId>.db` de ejecución)
- **`data_store` UUID**: Identificador de la tabla dentro del SQLite del cliente

### Archivos centinela
| Repo | Archivo | Razón |
|------|---------|-------|
| flow_binaries | `core/actions/store/` | Todas las operaciones del store |
| flow_binaries | `core/actions/store/store_search.go` | Búsqueda con filtros (la más compleja) |
| flow_binaries | `core/actions/store/store_params.go` | Procesamiento de parámetros |
| flow_binaries | `backend/ion/services/data_store_service.go` | CRUD del data store |
| flow_binaries | `backend/ion/services/data_structure_service.go` | CRUD de estructura |
| flow_binaries | `server/` | REST endpoints: `/data-store-*`, `/data-structure-*` |

---

## Impacto Cruzado

### Módulos que Data Store afecta
| Módulo destino | Componente afectado | Tipo | Ejemplo |
|---------------|--------------------|-----------------|---------| 
| **Boards** | Flows que leen/escriben | Ejecución | Si el schema del data store cambia, nodos Store fallan |
| **Nodes** | Nodos `ion.store.*` | Ejecución | Los 8 tipos de nodo Store dependen del data store |

### Módulos que afectan a Data Store
| Módulo origen | Componente | Tipo | Ejemplo |
|--------------|------------|-----------------|---------| 
| **Boards** | Flows con nodos Store | Datos | Los flows escriben datos en el data store |
| **Auth** | Permisos | API | Solo users con permisos pueden gestionar data stores |

### Tablas compartidas
| Tabla | Módulos que la usan | Riesgo si cambia |
|-------|---------------------|------------------|
| SQLite del cliente (clientPath) | Data Store, Boards (runtime), Nodes (Store) | Schema de datos del cliente |

---

## Historial de Actualizaciones

| Fecha | Tickets | Cambios | Actualizado por |
|-------|---------|---------|----------------|
| Initial | — | Creación inicial | QA Catalyst |
| 2026-06-06 | — | Backend Logic (store operations, services) + Impacto Cruzado | QA Catalyst |
