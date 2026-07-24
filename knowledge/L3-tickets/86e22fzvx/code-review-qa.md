# Code Review QA — 86e22fzvx (Modo Deployment / Bug Hunting)

> Fecha: 2026-07-14
> Ticket: 86e22fzvx — Boards — Simple Decision compara valores numéricos como strings, resultado incorrecto
> Branch: IONF-1128 → Mergeada en DEVELOPMENT (PR flow_binaries #13, PR webcomponents-flow #7)
> Revisado por: QA Catalyst
> Commits revisados: 28b1f57 + e63e83f + fc66f4a (flow_binaries) | 606af1a + 8ecd0f4 (webcomponents-flow)

---

## Resumen

| Métrica | Valor |
|---------|-------|
| Repos revisados | `flow_binaries` + `webcomponents-flow` |
| Archivos modificados analizados | 6 (core) + ~13 (renames ruleeval) |
| Bugs confirmados (reproducibles) | 0 |
| Riesgos a verificar en testing | 2 |
| TCs inyectados en test-matrix | 2 (TC-CR-001, TC-CR-002) |
| Tests unitarios del Developer | ✅ 14 Go (condition_test.go) + 12 TS (ConditionItem.spec.ts) |

---

## Archivos Modificados

### `flow_binaries`

| Archivo | Cambio Principal |
|---------|-----------------|
| `core/actions/condition/condition.go` | `evaluateConditionItem()` rutea a `evaluateTypedItem()` si `type` presente, si no usa `evaluateStringItem()` (legacy). `evaluateStringItem()` agrega aliases `is_greater_or_equal`, `is_less_or_equal`, `contains`, `not_contains` al legacy path. |
| `core/actions/ruleeval/eval.go` | Nuevo `Evaluator.Evaluate()` — dispatcher central por tipo: string, number, boolean, array, object. |
| `core/actions/ruleeval/rule.go` | Struct `Rule{Field, Operator, Value, Type}` — compartido por condition y switch. |
| `core/actions/ruleeval/number.go` | Extraído de `switchrule`. `processSwitchNumber()` con `parseNumberValue()` que convierte string → float64. Operadores: `is_equal_to`, `is_not_equal_to`, `is_greater_than`, `is_less_than`, `is_greater_than_or_equal_to`, `is_less_than_or_equal_to`, `exists`, `does_not_exist`, `is_empty`, `is_not_empty`. |
| `core/actions/ruleeval/string.go` | Extraído de `switchrule`. `processSwitchString()`. |
| `core/actions/ruleeval/boolean.go` | Extraído de `switchrule`. `processSwitchBoolean()` con soporte `is_true`, `is_false`, `is_equal_to`, `is_not_equal_to`, `exists`, `is_empty`. |
| `core/actions/switchnode/switchrule/switch_rule.go` | Simplificado: ahora delega a `ruleeval.New().Evaluate()` en lugar de tener lógica propia. |
| `backend/ion/ai/prompts/system.go` | Estructura del nodo Condition actualizada para FlowPilot (context del nodo). |

### `webcomponents-flow`

| Archivo | Cambio Principal |
|---------|-----------------|
| `FlowDrawer/Condition/ConditionConfig.vue` | `onAddCondition()` ahora crea condición con `type: 'string'` y `operator: 'is_equal_to'` por defecto. |
| `FlowDrawer/Condition/ConditionItem.vue` | Selector de tipo (toggle `showTypeConfig`), `operatorOptions` dinámicos por tipo, `showValue` oculta campo value para operadores unarios, `validateOperand()` con validación inline por tipo, `changeTypeOperator()` resetea operator al primero del nuevo tipo al cambiar type. |
| `FlowDrawer/Condition/constants/condition.ts` | `useConditionConstants()` reutiliza `useSwitchConstants()` — mismos tipos y operadores que Switch. |
| `FlowDrawer/Condition/ConditionItem.spec.ts` | 12 tests nuevos. |

---

## Análisis del Fix Principal

El fix es **correcto y bien estructurado**:

1. **Backend**: La lógica de routing `evaluateConditionItem()` → `evaluateTypedItem()` / `evaluateStringItem()` es limpia. El check `datamap["type"].(string)` con `dataType != ""` garantiza que solo items con `type` explícito van al nuevo path. Items sin `type` o con `type: ""` van al legacy. ✅

2. **Numeric comparison**: `parseNumberValue()` acepta `float64` (JSON nativo) y `string` (via `strconv.ParseFloat`). Los operadores numéricos usan aritmética de float64. El bug original (`"2" > "12"` como string) ya no puede ocurrir. ✅

3. **Backward compatibility**: `evaluateStringItem()` sigue intacto. Condiciones antiguas sin campo `type` usan el mismo path que antes. ✅

4. **Frontend**: `changeTypeOperator()` resetea el operator al primero del nuevo tipo al cambiar el type selector. Esto previene operadores inválidos. `showValue` oculta el campo value para operadores unarios y limpia el valor (`condition.value.value = ''`). ✅

---

## Bugs Confirmados (Reproducibles)

> **Ninguno.** El fix es correcto. Los tests Go pasaron (14 casos en condition_test.go + todos los de ruleeval). Los tests frontend pasaron (12 casos en ConditionItem.spec.ts).

---

## Riesgos a Verificar

### BUG-CR-001 — RIESGO A VERIFICAR
**Clasificación**: RIESGO A VERIFICAR
**Severidad**: 🟠 Medio
**Repo**: `webcomponents-flow`
**Archivo**: `ConditionItem.vue` — línea 63–66 (`onOperatorChange`) + línea 33 (`selectedType` computed)

**Descripción**: Cuando una condición existente sin `type` (legacy) se edita en el frontend y se cambia el operador (sin cambiar el type selector), `onOperatorChange()` establece `condition.value.type = selectedType.value` donde `selectedType` hace `condition.value.type ?? 'string'`. Esto convierte silenciosamente la condición legacy a `type: 'string'` al primer cambio de operador. El problema potencial: si el usuario solo cambia el operador de una condición legacy, el backend la ruteará al nuevo path `ruleeval` con `type: 'string'`, no al legacy path. Si el operador era `is_equal` (legacy) y el nuevo path solo acepta `is_equal_to` (switch vocab), el backend retornará error.

**Evidencia**:
```typescript
// ConditionItem.vue — línea 63-67
function onOperatorChange() {
  if (!condition.value.type) {
    condition.value.type = selectedType.value; // 'string' por defecto
  }
}
```
```typescript
// ConditionItem.vue — línea 32-35
const selectedType = computed<string>({
  get: () => condition.value.type ?? 'string', // legacy sin type → 'string'
  set: (value) => { condition.value.type = value; },
});
```

**Escenario para verificar**:
1. Abrir un flow existente con Simple Decision configurado sin `type` (condición legacy con operador `is_equal`)
2. Abrir el drawer del nodo → cambiar el operador (ej: de `is_equal` a `is_equal_to`)
3. Guardar y ejecutar el flow
4. Verificar que el resultado es correcto (el backend acepta el nuevo operador sin error)

**Por qué es riesgo**: El operador legacy `is_equal` NO está en el vocabulario del `ruleeval` para `type: 'string'`. Si el usuario edita una condición legacy y cambia el operador, podría quedar con `type: 'string'` + un operador legacy como `is_equal` que fallará en el backend. Sin embargo, el test `it('defaults untyped conditions to the String (switch) operators')` en el spec muestra que los operadores del dropdown para tipo `string` son del nuevo vocabulario (is_equal_to, contains, etc.), así que si el usuario cambia el operador verá el nuevo vocabulario. El riesgo real es si el operador original legacy queda sin cambiarse y solo se cambia el `type` accidentalmente.

**Nota del test unitario**: El test `it('persists type "string" when changing the operator...')` cubre este caso y lo valida como comportamiento esperado. Verificar en UI es necesario de todas formas.

---

### BUG-CR-002 — RIESGO A VERIFICAR
**Clasificación**: RIESGO A VERIFICAR
**Severidad**: 🟡 Bajo
**Repo**: `flow_binaries`
**Archivo**: `core/actions/condition/condition.go` — línea 101-108 (`evaluateStringItem`)

**Descripción**: En el legacy path, `expr.Run(program, nodeData)` usa `nodeData` como entorno. `nodeData` es `node.Data` (el valor de la condición completa, que es un `[]interface{}` de items). Si el usuario tiene una condición legacy con operadores relacionales (`is_greater`, `is_less`) y los valores son strings numéricos (ej: `"5"` y `"5"`), el expr-lang compara con `"5" >= "5"` que es verdadero. Este comportamiento legacy se preserva. Sin embargo, se detectó que el test de alias `{\"5\", \"5\", \"is_greater_or_equal\", \"then\"}` confirma la comparación string-lexicográfica `"5" >= "5"` → true, que es correcto para el legacy path.

**Resultado**: Comportamiento legacy preservado correctamente. No es bug, es by design. Documentado como riesgo bajo para completitud.

---

## Observación Positiva: Tests unitarios excelentes

Los tests de Go en `condition_test.go` cubren exactamente el bug reportado:

```go
// Typed path: numbers compare numerically, not lexicographically.
func TestExecuteTypedNumber(t *testing.T) {
    // "10" > "9" is false as strings but true as numbers.
    node := models.Node{Data: []interface{}{
        map[string]interface{}{"field": "10", "value": "9", "operator": "is_greater_than", "type": "number"},
    }}
    // expects "then" (10 > 9 as numbers → true)
}
```

El caso del bug original (`2 > 12` que daba `true` incorrectamente) está cubierto implícitamente.

---

## TCs Inyectados en Test Matrix

| TC ID | Origen | Caso de Test | Severidad |
|-------|--------|-------------|-----------|
| TC-CR-001 | BUG-CR-001 | Condición legacy editada (solo operador cambia) → backend acepta sin error y resultado es correcto | 🟠 Medio |
| TC-CR-002 | BUG-CR-002 | Condición legacy con `is_greater` string-lexicográfico → preserva comportamiento previo | 🟡 Bajo |

---

## Impacto Cruzado

| Módulo | Componente | Riesgo | Verificación |
|--------|-----------|--------|-------------|
| **Multiple Decision (Switch)** | `switchrule/switch_rule.go` delegó a `ruleeval` | 🟠 Medio — posible regresión si `ruleeval` tiene bugs | TC-016 en test-matrix |
| **Boards** | Ejecución de flows con Simple Decision | 🔴 Alto — si condition falla, el flow falla | TC-003/004/013 en test-matrix |

---

## Aprobación del Code Review

- [x] Revisión completada
- [ ] QA Engineer aprueba hallazgos
