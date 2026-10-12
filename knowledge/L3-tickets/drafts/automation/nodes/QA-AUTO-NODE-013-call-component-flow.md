## Contexto

### Descripción
Automatización del nodo **Call Component-Flow**. Este nodo invoca un flow reutilizable (Component-Flow) desde otro flow, permitiendo modularizar la lógica en sub-flows reutilizables.

> **Fuente**: `Iond Testing Plan - Iond Automation Plan.csv` (línea 67)
> **Referencia técnica**: `knowledge/L2-modules/nodes/module.md` — Sección 11 (Call Component-Flow)

### Módulo afectado
- Módulo principal: `Tenant / Boards / Canvas / Call Component-Flow`
- Backend: `ion.action.executeWorkflow` — no tiene package dedicado, orquesta via API
- Config: Select → elige qué Component-Flow ejecutar. Opción "New" para crear uno
- Inputs: `input`
- Outputs: `output`, `error`
- Drawer en: `FlowDrawer/SubFlow/`

### Pre-requisitos
- Board de prueba con draft activo
- Al menos un Component-Flow existente (board tipo component)
- Component-Flow con nodo "On Call Component-Flow Trigger" configurado

---

## Test Cases

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-NODE-CCF-01 | Happy Path | Seleccionar Component-Flow existente y ejecutar — verificar que el sub-flow se invoca | 🔴 | ⬜ |
| TC-NODE-CCF-02 | Happy Path | Verificar que el output del Component-Flow llega al nodo siguiente en el flow principal | 🔴 | ⬜ |
| TC-NODE-CCF-03 | Happy Path | Pasar datos del flow principal como input al Component-Flow | 🔴 | ⬜ |
| TC-NODE-CCF-04 | Happy Path | Crear nuevo Component-Flow desde el dropdown del nodo ("New") | 🟠 | ⬜ |
| TC-NODE-CCF-05 | Negativo | Seleccionar Component-Flow que fue eliminado — verificar error | 🟠 | ⬜ |
| TC-NODE-CCF-06 | Edge Case | Component-Flow que falla internamente — verificar que el error se propaga al flow principal | 🟠 | ⬜ |

---

## Notas de Automatización
- Siempre se testea en conjunto con On Call Component-Flow Trigger (NODE-014)
- Probar escenario de Component-Flow eliminado es importante para robustez
- 6 test cases
