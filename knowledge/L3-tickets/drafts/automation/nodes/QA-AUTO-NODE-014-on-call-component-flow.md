## Contexto

### Descripción
Automatización del nodo **On Call Component-Flow Trigger**. Este nodo trigger inicia un Component-Flow cuando es invocado por un nodo "Call Component-Flow" desde otro flow.

> **Fuente**: `Iond Testing Plan - Iond Automation Plan.csv` (línea 68)
> **Referencia técnica**: `knowledge/L2-modules/nodes/module.md` — Sección 12 (On Call Component-Flow Trigger)

### Módulo afectado
- Módulo principal: `Tenant / Boards / Canvas / On Call Component-Flow Trigger`
- Backend: `ion.action.executeWorkflowTrigger` — trigger, no tiene ejecución propia
- Config: Select → elige qué Component-Flow se dispara
- Inputs: Ninguno (es un trigger)
- Outputs: `output`, `error`

### Pre-requisitos
- Board tipo Component-Flow creado
- Al menos un board con nodo Call Component-Flow apuntando a este Component-Flow

---

## Test Cases

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-NODE-OCCF-01 | Happy Path | Configurar trigger y verificar que inicia cuando es invocado por Call Component-Flow | 🔴 | ⬜ |
| TC-NODE-OCCF-02 | Happy Path | Verificar que los datos del caller llegan al trigger como input | 🔴 | ⬜ |
| TC-NODE-OCCF-03 | Edge Case | Múltiples Call Component-Flow apuntando al mismo On Call — verificar ejecuciones independientes | 🟠 | ⬜ |

---

## Notas de Automatización
- Siempre se testea en conjunto con Call Component-Flow (NODE-013)
- Ticket pequeño (3 TCs) pero crítico para modularidad de flows
- 3 test cases
