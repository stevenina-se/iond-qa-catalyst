## Contexto

### Descripción
Automatización del nodo **Multiple Decision** (backend: `switch`). Este nodo evalúa múltiples reglas o expresiones y rutea el flujo a la rama que coincida. Soporta dos modos: `rules` (reglas predefinidas) y `expression` (expresiones evaluadas).

> ⚠️ **Mapeo**: Canvas "Multiple Decision" = Backend `ion.action.switch` (`core/actions/switchnode`)

> **Fuente**: `Iond Testing Plan - Iond Automation Plan.csv` (línea 65)
> **Referencia técnica**: `knowledge/L2-modules/nodes/module.md` — Sección 7 (Switch)

### Módulo afectado
- Módulo principal: `Tenant / Boards / Canvas / Multiple Decision`
- Backend: `ion.action.switch` — Package `core/actions/switchnode`
- Modos: `rules` (reglas predefinidas), `expression` (expresiones evaluadas)
- Config: `{ "mode": "rules|expression", "data": [...] }`
- Operadores Rules: `is_equal_to`, `is_not_equal_to`, `contains`, `does_not_contain`, `starts_with`, `does_not_starts_with`, `ends_with`, `does_not_ends_with`, `is_greater_than`, `is_less_than`, `is_greater_than_or_equal_to`, `is_less_than_or_equal_to`
- Tipos: `string`, `number`, `boolean`, `object`, `array`
- Config Regla: `{ id, label, field, operator, value, type }`
- Tests backend: `switch_test.go`
- Drawer en: `FlowDrawer/Switch/`

### Pre-requisitos
- Board de prueba con draft activo
- Nodos upstream con datos variados para evaluar múltiples condiciones

---

## Test Cases

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-NODE-MD-01 | Happy Path | Modo `rules` — configurar 3 reglas, enviar dato que matchea regla 2 — verificar ruteo correcto | 🔴 | ⬜ |
| TC-NODE-MD-02 | Happy Path | Modo `rules` — dato que no matchea ninguna regla — verificar ruteo a fallback/default | 🔴 | ⬜ |
| TC-NODE-MD-03 | Happy Path | Modo `expression` — configurar expresión evaluable y verificar ruteo | 🔴 | ⬜ |
| TC-NODE-MD-04 | Happy Path | Operadores string: `contains`, `starts_with`, `ends_with` — verificar evaluación | 🟠 | ⬜ |
| TC-NODE-MD-05 | Happy Path | Operadores negados: `does_not_contain`, `does_not_starts_with`, `does_not_ends_with` | 🟠 | ⬜ |
| TC-NODE-MD-06 | Happy Path | Operadores numéricos: `is_greater_than`, `is_less_than`, `is_greater_than_or_equal_to`, `is_less_than_or_equal_to` | 🟠 | ⬜ |
| TC-NODE-MD-07 | Happy Path | Tipos de dato: `string`, `number`, `boolean`, `object`, `array` — verificar cada tipo | 🟠 | ⬜ |
| TC-NODE-MD-08 | Edge Case | Múltiples reglas matchean — verificar cuál tiene prioridad (primera en orden) | 🟠 | ⬜ |
| TC-NODE-MD-09 | Edge Case | Expresiones con `{{$N.field}}` — verificar resolución dinámica | 🔴 | ⬜ |
| TC-NODE-MD-10 | Negativo | Switch sin reglas configuradas — verificar error o comportamiento default | 🟡 | ⬜ |

---

## Notas de Automatización
- Tiene 12 operadores — cada uno debe ser probado al menos una vez
- Soporta 5 tipos de dato — verificar casting y comparación correcta
- Modo `expression` usa motor `expr-lang/expr`
- 10 test cases
