# QA-AUTO-ADMIN-002 — Admin: Templates

> Módulo: Admin > Templates
> Side: ADMIN
> Assignee: Mijael
> Prioridad: 🟡 Normal
> Status: Pending

## Contexto

### Descripción
Automatización de la gestión de Templates desde el panel de Admin. Incluye creación vía JSON, importación desde compañía y edición.

### Módulo afectado
- Módulo principal: `Admin / Templates`
- Módulos relacionados: `Companies`, `Tenant / Templates`

---

## Test Cases

### New Template

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-ADMIN-TPL-01 | Happy Path | Crear nuevo template vía JSON válido | 🟠 | ⬜ |
| TC-ADMIN-TPL-02 | Negativo | Crear template con JSON inválido — error descriptivo | 🟠 | ⬜ |
| TC-ADMIN-TPL-03 | Happy Path | Importar template desde una compañía existente | 🟠 | ⬜ |
| TC-ADMIN-TPL-04 | Negativo | Importar template de compañía sin templates — estado vacío | 🟡 | ⬜ |

### Actions

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-ADMIN-TPL-05 | Happy Path | Editar template existente — guardar cambios | 🟠 | ⬜ |
| TC-ADMIN-TPL-06 | Edge Case | Editar template y cancelar — no se guardan cambios | 🟡 | ⬜ |

---

## Notas de Automatización
- Pre-requisito: Login como Admin, al menos 1 compañía con templates existentes
- Preparar fixtures de JSON válido e inválido
