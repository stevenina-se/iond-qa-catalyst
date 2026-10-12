## Contexto

### Descripción
Automatización de la gestión de compañías desde Admin. Incluye visualización de información, conectores (migrar/descargar configuración), boards (migrar), suscripciones (asignar plan) y usuarios (log as user).

### Módulo afectado
- Módulo principal: `Admin / Companies`
- Módulos relacionados: `Billing`, `Connectors`, `Boards`, `Subscriptions`

---

## Test Cases

### Company > Information

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-ADMIN-COMP-01 | Happy Path | Ver información completa de una compañía | 🟠 | ⬜ |
| TC-ADMIN-COMP-02 | Happy Path | Listar compañías — paginación y búsqueda | 🟡 | ⬜ |

### Company > Connectors

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-ADMIN-COMP-03 | Happy Path | Migrar conectores de una compañía a otra | 🟠 | ⬜ |
| TC-ADMIN-COMP-04 | Happy Path | Descargar configuración de conectores | 🟠 | ⬜ |
| TC-ADMIN-COMP-05 | Negativo | Migrar conectores a compañía inexistente | 🟡 | ⬜ |

### Company > Boards

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-ADMIN-COMP-06 | Happy Path | Migrar boards de una compañía a otra | 🟠 | ⬜ |
| TC-ADMIN-COMP-07 | Edge Case | Migrar board con dependencias de conexiones | 🟡 | ⬜ |

### Company > Subscription

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-ADMIN-COMP-08 | Happy Path | Asignar plan a compañía | 🟠 | ⬜ |
| TC-ADMIN-COMP-09 | Edge Case | Cambiar plan de compañía con plan activo | 🟡 | ⬜ |

### Company > User

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-ADMIN-COMP-10 | Happy Path | Log as a user — acceder al tenant como un usuario de la compañía | 🟠 | ⬜ |
| TC-ADMIN-COMP-11 | Edge Case | Log as a user — verificar que se mantiene la sesión del admin al salir | 🟡 | ⬜ |

---

## Notas de Automatización
- Pre-requisito: Al menos 2 compañías con datos, conectores y boards
- "Log as a user" requiere verificar el cambio de contexto de sesión
