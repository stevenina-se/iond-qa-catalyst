## Contexto

### Descripción
Automatización de módulos menores del Admin: Settings (Categories CRUD), Connectors (listado) y Boards (listado).

### Módulo afectado
- Módulo principal: `Admin / Settings`, `Admin / Connectors`, `Admin / Boards`

---

## Test Cases

### Settings > Categories

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-ADMIN-SET-01 | Happy Path | Agregar categoría nueva | 🟡 | ⬜ |
| TC-ADMIN-SET-02 | Happy Path | Editar categoría existente | 🟡 | ⬜ |
| TC-ADMIN-SET-03 | Happy Path | Eliminar categoría | 🟡 | ⬜ |
| TC-ADMIN-SET-04 | Negativo | Crear categoría con nombre duplicado | 🟡 | ⬜ |
| TC-ADMIN-SET-05 | Edge Case | Eliminar categoría en uso — verificar impacto | 🟡 | ⬜ |

### Connectors

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-ADMIN-CONN-01 | Happy Path | Listar conectores en Admin | 🔵 | ⬜ |
| TC-ADMIN-CONN-02 | Happy Path | Filtrar y buscar conectores | 🔵 | ⬜ |

### Boards

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-ADMIN-BRD-01 | Happy Path | Listar boards en Admin | 🔵 | ⬜ |
| TC-ADMIN-BRD-02 | Happy Path | Filtrar y buscar boards | 🔵 | ⬜ |

---

## Notas de Automatización
- Settings > Categories es pre-requisito para clasificación de apps
