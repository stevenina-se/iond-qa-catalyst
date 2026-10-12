## Contexto

### Descripción
Automatización de la gestión de Billing desde Admin: sincronización de productos con Stripe, CRUD de planes, asignación/eliminación de features y gestión de ventanas de billing.

### Módulo afectado
- Módulo principal: `Admin / Billing`
- Módulos relacionados: `Stripe`, `Companies / Subscription`

### Blocker
> ⚠️ Este módulo está **BLOCKED** — la funcionalidad de Billing está en desarrollo activo (v0.2.0). Los tests no pueden ejecutarse hasta que el módulo esté estable.

---

## Test Cases

### Products

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-ADMIN-BILL-01 | Happy Path | Sincronizar productos desde Stripe | 🔴 | ⬜ |
| TC-ADMIN-BILL-02 | Edge Case | Re-sincronizar — productos existentes se actualizan sin duplicar | 🟠 | ⬜ |
| TC-ADMIN-BILL-03 | Negativo | Sincronizar con credenciales Stripe inválidas | 🟠 | ⬜ |

### Plans

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-ADMIN-BILL-04 | Happy Path | Crear plan nuevo | 🔴 | ⬜ |
| TC-ADMIN-BILL-05 | Happy Path | Editar plan existente | 🟠 | ⬜ |
| TC-ADMIN-BILL-06 | Happy Path | Eliminar plan | 🟠 | ⬜ |
| TC-ADMIN-BILL-07 | Negativo | Eliminar plan asignado a compañía activa | 🟠 | ⬜ |

### Plans > Features

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-ADMIN-BILL-08 | Happy Path | Asignar feature a un plan | 🔴 | ⬜ |
| TC-ADMIN-BILL-09 | Happy Path | Eliminar feature de un plan | 🟠 | ⬜ |
| TC-ADMIN-BILL-10 | Happy Path | Confirmar feature asignada — verificar persistencia | 🟠 | ⬜ |
| TC-ADMIN-BILL-11 | Happy Path | Agregar ventana (window) a un plan | 🟠 | ⬜ |

### Feature

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-ADMIN-BILL-12 | Happy Path | Editar feature existente | 🟠 | ⬜ |
| TC-ADMIN-BILL-13 | Negativo | Editar feature en uso — verificar propagación | 🟡 | ⬜ |

---

## Notas de Automatización
- Requiere Stripe en modo test con productos de prueba configurados
- Considerar cleanup de datos de Stripe después de cada test run
- BLOCKED hasta que billing v0.2.0 esté estable
