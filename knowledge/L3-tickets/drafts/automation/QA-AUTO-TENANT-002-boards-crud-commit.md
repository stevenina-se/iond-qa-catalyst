## Contexto

### Descripción
Automatización de las operaciones de gestión de Boards: CRUD, sistema de commits (drafts, save, discard, history), preview, export/import, Flow Pilot y configuraciones de lista (columns, filters).

### Módulo afectado
- Módulo principal: `Tenant / Boards`
- Módulos relacionados: `Canvas`, `Flow Pilot`, `IonMind`

---

## Test Cases

### Board CRUD

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-BOARD-CRUD-01 | Happy Path | Crear nuevo board | 🔴 | ⬜ |
| TC-BOARD-CRUD-02 | Happy Path | Editar board (nombre, configuración) | 🔴 | ⬜ |
| TC-BOARD-CRUD-03 | Happy Path | Eliminar board | 🔴 | ⬜ |
| TC-BOARD-CRUD-04 | Happy Path | Clonar board existente | 🔴 | ⬜ |
| TC-BOARD-CRUD-05 | Happy Path | Descargar board (export JSON) | 🟠 | ⬜ |
| TC-BOARD-CRUD-06 | Happy Path | Activar / Pausar board (Active-Pause) | 🔴 | ⬜ |
| TC-BOARD-CRUD-07 | Happy Path | Agregar descripción al board | 🟡 | ⬜ |
| TC-BOARD-CRUD-08 | Happy Path | Preview del board | 🟠 | ⬜ |

### Commit System

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-BOARD-CMT-01 | Happy Path | Create Separate Draft — crear borrador nuevo | 🔴 | ⬜ |
| TC-BOARD-CMT-02 | Happy Path | Create From Existing — crear draft desde board existente | 🔴 | ⬜ |
| TC-BOARD-CMT-03 | Happy Path | Create From Saved State — crear draft desde un estado guardado | 🔴 | ⬜ |
| TC-BOARD-CMT-04 | Happy Path | Change Separate Draft — cambiar entre drafts | 🟠 | ⬜ |
| TC-BOARD-CMT-05 | Happy Path | Save — guardar draft como versión activa | 🔴 | ⬜ |
| TC-BOARD-CMT-06 | Happy Path | Discard Changes — descartar cambios del draft | 🔴 | ⬜ |
| TC-BOARD-CMT-07 | Happy Path | History — ver historial de commits | 🟠 | ⬜ |
| TC-BOARD-CMT-08 | Edge Case | Guardar sin cambios — no genera commit vacío | 🟡 | ⬜ |

### Export / Import

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-BOARD-EXP-01 | Happy Path | Exportar board completo como JSON | 🔴 | ⬜ |
| TC-BOARD-EXP-02 | Happy Path | Importar board desde JSON válido | 🔴 | ⬜ |
| TC-BOARD-EXP-03 | Negativo | Importar JSON inválido — error controlado | 🟠 | ⬜ |

### Flow Pilot

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-BOARD-FP-01 | Happy Path | Abrir chat session de Flow Pilot | 🔴 | ⬜ |
| TC-BOARD-FP-02 | Happy Path | Enviar mensaje — recibir respuesta de IA | 🔴 | ⬜ |
| TC-BOARD-FP-03 | Happy Path | Usar IA Tools — herramientas disponibles en el copilot | 🟠 | ⬜ |
| TC-BOARD-FP-04 | Edge Case | Flow Pilot con board vacío — sugerencias genéricas | 🟡 | ⬜ |

### Lista (Columns / Filters)

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-BOARD-LIST-01 | Happy Path | Configurar columnas visibles | 🟠 | ⬜ |
| TC-BOARD-LIST-02 | Happy Path | Aplicar filtros y verificar resultados | 🟠 | ⬜ |

---

## Notas de Automatización
- El commit system es complejo — requiere flujo secuencial (crear draft → modificar → save → verify history)
- Flow Pilot requiere IonMind activo
- Observación del CSV: "Mejorar el prompt" para IA Tools
