## Contexto

### Descripción
Automatización del nodo **Simple Decision** (backend: `condition`). Este nodo evalúa condiciones lógicas y rutea el flujo a la rama `then` (verdadero) o `false` (falso).

> ⚠️ **Mapeo**: Canvas "Simple Decision" = Backend `ion.action.condition` (`core/actions/condition`)

> **Fuente**: `Iond Testing Plan - Iond Automation Plan.csv` (línea 59 — "Prioritario para el siguiente sprint")
> **Referencia técnica**: `knowledge/L2-modules/nodes/module.md` — Sección 3 (Condition)

### Módulo afectado
- Módulo principal: `Tenant / Boards / Canvas / Simple Decision`
- Backend: `ion.action.condition` — Package `core/actions/condition`
- Motor de expresiones: `expr-lang/expr`
- Operadores: `is_equal`, `is_not_equal`, `is_greater`, `is_greater_equal`, `is_less`, `is_less_equal`
- Outputs: `then` ("By True"), `false` ("By False"), `error`
- Tests backend: `condition_test.go`

### Pre-requisitos
- Board de prueba con draft activo
- Nodos upstream con datos para evaluar condiciones

---

## Test Cases

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-NODE-SD-01 | Happy Path | Configurar condición `is_equal` con string — verificar ruteo a `then` | 🔴 | ⬜ |
| TC-NODE-SD-02 | Happy Path | Verificar ruteo a `false` cuando la condición NO se cumple | 🔴 | ⬜ |
| TC-NODE-SD-03 | Happy Path | Usar operador `is_not_equal` — verificar evaluación correcta | 🔴 | ⬜ |
| TC-NODE-SD-04 | Happy Path | Usar operadores `is_greater`, `is_less` con valores numéricos | 🔴 | ⬜ |
| TC-NODE-SD-05 | Happy Path | Usar operadores `is_greater_equal`, `is_less_equal` — verificar límites | 🟠 | ⬜ |
| TC-NODE-SD-06 | Edge Case | Comparar valores numéricos que llegan como strings — verificar que NO compara como string (bug conocido v0.1.0) | 🔴 | ⬜ |
| TC-NODE-SD-07 | Edge Case | Configurar múltiples condiciones (AND lógico) — verificar que TODAS deben cumplirse | 🟠 | ⬜ |
| TC-NODE-SD-08 | Edge Case | Usar expresiones dinámicas `{{$N.field}}` en field y value | 🔴 | ⬜ |
| TC-NODE-SD-09 | Negativo | Campo referenciado no existe en el input — verificar activación del edge de error | 🟠 | ⬜ |
| TC-NODE-SD-10 | Negativo | Dejar condición sin configurar — verificar error o comportamiento default | 🟡 | ⬜ |

---

## Notas de Automatización
- **Bug conocido v0.1.0**: Comparación numérica como strings — TC-NODE-SD-06 es crítico
- Config del drawer: Array de condiciones `[{ "field": "...", "operator": "...", "value": "..." }]`
- Drawer en `webcomponents-flow/src/flow/components/FlowDrawer/Condition/`
- Prioritario para el siguiente sprint según el CSV
- 10 test cases
