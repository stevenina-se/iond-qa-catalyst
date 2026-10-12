## Contexto

### Descripción
Automatización de la gestión de Apps desde Admin. Cubre los 4 tipos: Legacy, Applications, Grapps y Custom. Grapps es la prioridad más alta ya que incluye creación, edición, configuración de flow y el wizard con/sin IA.

### Módulo afectado
- Módulo principal: `Admin / Apps`
- Módulos relacionados: `Developers`, `Connectors`, `Gateway`, `IonMind`

### Pre-requisitos
- SE REQUIERE TENER UN FLOW MIGRADO COMO PRE-REQUISITO (para Grapps)

---

## Test Cases

### List > Legacy

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-ADMIN-APP-01 | Happy Path | Listar apps Legacy | 🟡 | ⬜ |
| TC-ADMIN-APP-02 | Happy Path | Editar app Legacy | 🟡 | ⬜ |

### List > Applications

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-ADMIN-APP-03 | Happy Path | Listar Applications | 🟡 | ⬜ |
| TC-ADMIN-APP-04 | Happy Path | Editar Application | 🟡 | ⬜ |

### List > Grapps

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-ADMIN-APP-05 | Happy Path | Crear Grapp (pre-req: flow migrado) | 🔴 | ⬜ |
| TC-ADMIN-APP-06 | Happy Path | Editar Grapp y verificar cambios en Gateway | 🔴 | ⬜ |
| TC-ADMIN-APP-07 | Happy Path | Configurar Flow de un Grapp | 🔴 | ⬜ |
| TC-ADMIN-APP-08 | Happy Path | Grapp Wizard SIN IA | 🔴 | ⬜ |
| TC-ADMIN-APP-09 | Happy Path | Grapp Wizard CON IA | 🔴 | ⬜ |
| TC-ADMIN-APP-10 | Negativo | Crear Grapp sin flow migrado — error controlado | 🟠 | ⬜ |
| TC-ADMIN-APP-11 | Edge Case | Editar Grapp con flow activo en producción | 🟠 | ⬜ |

### List > Custom

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-ADMIN-APP-12 | Happy Path | Editar app Custom | 🟡 | ⬜ |

### Add App

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-ADMIN-APP-13 | Happy Path | Agregar app Legacy | 🟡 | ⬜ |
| TC-ADMIN-APP-14 | Happy Path | Agregar app Application | 🟡 | ⬜ |
| TC-ADMIN-APP-15 | Happy Path | Agregar Simple Grapp | 🔴 | ⬜ |
| TC-ADMIN-APP-16 | Happy Path | Agregar app Custom | 🟡 | ⬜ |

---

## Notas de Automatización
- Grapps requiere un flow migrado como fixture — preparar seed data
- El wizard con IA requiere acceso a IonMind
- Verificar la reflexión de cambios en Gateway (E2E cross-system)
