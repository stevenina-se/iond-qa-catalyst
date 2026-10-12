## Contexto

### Descripción
Automatización de los nodos de **Persistent Data** (Storage). El módulo `ion.store` incluye 8 operaciones CRUD sobre la BD persistente (Data Store) del cliente: Save, Update, Get, Delete, Check, Count, Delete All y Search.

> **Fuente**: `Iond Testing Plan - Iond Automation Plan.csv` (líneas 70-77)
> **Referencia técnica**: `knowledge/L2-modules/nodes/module.md` — Sección 6 (Store)

### Módulo afectado
- Módulo principal: `Tenant / Boards / Canvas / Persistent Data`
- Backend: `ion.store.*` — Package `core/actions/store`
- BD: SQLite del cliente (ruta `clientPath`)
- Config: `{ "data_store": "<UUID>", "params": { "key": "...", ... }, "metadata": {...} }`
- Drawer en: `FlowDrawer/Store/`
- Tests backend: `store_test.go`, `store_add_test.go`, `store_update_test.go`, `store_search_test.go`, `store_params_test.go`
- Dependencia: `Data Store` y `Data Structure` del módulo Persistent Data

### Operaciones Disponibles

| Tipo | Constante Backend | Descripción |
|------|-------------------|-------------|
| Save | `ion.store.add` | Insertar registro |
| Update | `ion.store.update` | Actualizar registro |
| Get | `ion.store.get` | Obtener registro por key |
| Delete | `ion.store.delete` | Eliminar registro por key |
| Check | `ion.store.check` | Verificar si existe un registro |
| Count | `ion.store.count` | Contar registros |
| Delete All | `ion.store.delete_all` | Eliminar todos los registros |
| Search | `ion.store.search` | Buscar registros con filtros |

### Pre-requisitos
- Board de prueba con draft activo
- Data Store creado con al menos una Data Structure definida
- Datos de prueba para operaciones de búsqueda y actualización

---

## Test Cases

### Operaciones CRUD

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-NODE-STOR-01 | Happy Path | **Save** — insertar registro con key y params — verificar que se guarda en Data Store | 🔴 | ⬜ |
| TC-NODE-STOR-02 | Happy Path | **Update** — actualizar registro existente por key — verificar que los datos cambian | 🔴 | ⬜ |
| TC-NODE-STOR-03 | Happy Path | **Get** — obtener registro por key — verificar que retorna datos correctos | 🔴 | ⬜ |
| TC-NODE-STOR-04 | Happy Path | **Delete** — eliminar registro por key — verificar que desaparece | 🔴 | ⬜ |
| TC-NODE-STOR-05 | Happy Path | **Check** — verificar existencia de registro — retorna true/false | 🔴 | ⬜ |
| TC-NODE-STOR-06 | Happy Path | **Count** — contar registros en el Data Store | 🔴 | ⬜ |
| TC-NODE-STOR-07 | Happy Path | **Delete All** — eliminar todos los registros — verificar que Data Store queda vacío | 🟠 | ⬜ |
| TC-NODE-STOR-08 | Happy Path | **Search** — buscar registros con filtros — verificar resultados | 🟠 | ⬜ |

### Errores y Edge Cases

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-NODE-STOR-09 | Negativo | Save con Data Store UUID inválido o inexistente — verificar error | 🟠 | ⬜ |
| TC-NODE-STOR-10 | Negativo | Get con key inexistente — verificar que activa edge de error o retorna vacío | 🟠 | ⬜ |
| TC-NODE-STOR-11 | Negativo | Update con key inexistente — verificar comportamiento (error o upsert) | 🟡 | ⬜ |
| TC-NODE-STOR-12 | Edge Case | Save con datos complejos (nested objects, arrays) — verificar integridad | 🟠 | ⬜ |
| TC-NODE-STOR-13 | Edge Case | Search con filtros múltiples — verificar combinación de condiciones | 🟡 | ⬜ |
| TC-NODE-STOR-14 | Edge Case | Delete All en Data Store vacío — verificar que no genera error | 🟡 | ⬜ |
| TC-NODE-STOR-15 | Edge Case | Usar expresiones `{{$N.field}}` en key y params — verificar resolución | 🔴 | ⬜ |

---

## Notas de Automatización
- Requiere Data Store + Data Structure pre-creados — depende de QA-AUTO-TENANT-006
- Los 8 nodos de storage comparten el mismo package backend (`core/actions/store`)
- Verificar integridad de datos entre operaciones secuenciales (Save → Get → Update → Get → Delete)
- 15 test cases
