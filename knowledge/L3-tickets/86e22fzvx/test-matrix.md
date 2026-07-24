# Test Matrix — 86e22fzvx

## Resumen

| Métrica | Valor |
|---------|-------|
| Total de casos | 20 |
| Ejecutados | 20 |
| PASS | 20 |
| FAIL | 0 |
| Smoke tests | 2 |
| Happy Path | 5 |
| Edge Cases | 5 |
| Negativos | 3 |
| Regresión | 3 |
| Code Review | 2 |
| Automatizables | 7 |
| Cobertura de AC | 6/6 |
| **Veredicto** | **✅ READY TO SHIP** |

### Acceptance Criteria (derivados de spec del Developer + bug report)

- **AC-1**: Cuando `type: "number"`, la comparación es numérica (`2 > 12` → `false`)
- **AC-2**: Condiciones sin campo `type` (legacy) siguen funcionando sin cambios (backward compatibility)
- **AC-3**: El drawer del Simple Decision incluye selector de tipo y operadores dinámicos por tipo
- **AC-4**: Operadores unarios ocultan el campo `value` en el drawer
- **AC-5**: Nuevas condiciones tienen `type: "string"` y `operator: "is_equal_to"` por defecto
- **AC-6**: El nodo Multiple Decision (Switch) no tiene regresiones (comparte `ruleeval`)

---

## Test Matrix

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|----|------|-------------|--------------|-------|--------------------|-----------|---------------|--------|
| TC-001 | Nodes / Canvas | AC-1 | Smoke | Simple Decision está disponible en el canvas | Board activo en staging | Company Login > Sidebar: Boards > Click [Board] > Canvas: Verify nodo "Simple Decision" disponible en panel de nodos | El nodo Simple Decision aparece en el panel de nodos del canvas y puede arrastrarse al canvas | 🔴 | ✅ | ✅ **PASS** — 2026-07-14 |
| TC-002 | Nodes / Canvas | AC-3 | Smoke | El drawer del Simple Decision abre correctamente | Board con nodo Simple Decision en canvas | Company Login > Sidebar: Boards > Click [Board con Simple Decision] > Canvas: Doble click sobre ícono del nodo > Verify: drawer abre con campos field/operator/value/type | Drawer abre y muestra configuración del nodo | 🔴 | ✅ | ✅ **PASS** — 2026-07-14 |
| TC-003 | Nodes / Condition | AC-1 | Happy Path | Condición numérica: 2 > 12 → resultado false (rama "By False") | Flow con Simple Decision activo en staging; nodo Condition configurado con `field: {{$1.value}}`, `operator: is_greater`, `value: 12`, `type: number`; output conectado a dos nodos (then y false) | Company Login > Sidebar: Boards > Click [Board con Simple Decision numérico] > Canvas: Button "Run" > Input: value=2 > Wait: ejecución > Canvas: Verify nodo Condition tomó rama "By False" > Sidebar: Executions > Verify: status "completed" | El nodo toma la rama "By False" (2 NO es mayor que 12). Status: completed | 🔴 | ❌ | ✅ **PASS** — 2026-07-14 |
| TC-004 | Nodes / Condition | AC-1 | Happy Path | Condición numérica: 15 > 12 → resultado true (rama "By True") | Mismo flow del TC-003 | Company Login > Sidebar: Boards > Click [Board con Simple Decision numérico] > Canvas: Button "Run" > Input: value=15 > Wait: ejecución > Canvas: Verify nodo Condition tomó rama "By True" | El nodo toma la rama "By True" (15 SÍ es mayor que 12). Status: completed | 🔴 | ❌ | ✅ **PASS** — 2026-07-14 |
| TC-005 | Nodes / Condition | AC-1 | Happy Path | Condición numérica: igualdad `12 == 12` → resultado true | Flow con Simple Decision; `field: 12`, `operator: is_equal`, `value: 12`, `type: number` | Company Login > Sidebar: Boards > Click [Board] > Canvas: Configurar Simple Decision: field=12, operator="is equal to", value=12, type=number > Canvas: Button "Run" > Wait: ejecución > Verify: rama "By True" activa | Rama "By True" activa (12 == 12 es true numérico) | 🔴 | ❌ | ✅ **PASS** — 2026-07-14 |
| TC-006 | Nodes / Canvas | AC-3 | Happy Path | UI: selector de tipo visible y operadores cambian dinámicamente | Board con nodo Simple Decision en canvas | Company Login > Sidebar: Boards > Click [Board] > Canvas: Click [Simple Decision] > Drawer: Verify selector "Type" visible > Drawer: Select type "number" > Verify: lista de operadores contiene operadores numéricos (is greater, is less, etc.) > Drawer: Select type "string" > Verify: lista de operadores cambia | Al seleccionar "number" aparecen operadores numéricos; al seleccionar "string" los operadores cambian acordemente | 🟠 | ✅ | ✅ **PASS** — 2026-07-14 |
| TC-007 | Nodes / Canvas | AC-5 | Happy Path | UI: nueva condición tiene defaults string + is_equal_to | Board con nodo Simple Decision vacío | Company Login > Sidebar: Boards > Click [Board] > Canvas: Click [Simple Decision] > Drawer: Click "Add condition" (o similar) > Verify: type="string" preseleccionado > Verify: operator="is equal to" preseleccionado | Nueva condición aparece con type "string" y operator "is equal to" por defecto | 🟡 | ✅ | ✅ **PASS** — 2026-07-14 |
| TC-008 | Nodes / Condition | AC-1 | Edge Case | Condición numérica con decimal: 2.5 < 10.0 → resultado true | Flow con Simple Decision; `field: 2.5`, `operator: is_less`, `value: 10.0`, `type: number` | Company Login > Sidebar: Boards > Click [Board] > Canvas: Configurar Simple Decision: field=2.5, operator="is less than", value=10.0, type=number > Canvas: Button "Run" > Wait: ejecución > Verify: rama "By True" activa | Rama "By True" activa (2.5 < 10.0 es true numérico) | 🟠 | ❌ | ✅ **PASS** — 2026-07-14 |
| TC-009 | Nodes / Condition | AC-1 | Edge Case | Condición numérica borderline: 10.0 >= 10 → resultado true | Flow con Simple Decision; `field: 10.0`, `operator: is_greater_equal`, `value: 10`, `type: number` | Company Login > Sidebar: Boards > Click [Board] > Canvas: Configurar Simple Decision: field=10.0, operator="is greater than or equal to", value=10, type=number > Canvas: Button "Run" > Verify: rama "By True" | Rama "By True" (10.0 >= 10 es true) | 🟠 | ❌ | ✅ **PASS** — 2026-07-14 |
| TC-010 | Nodes / Condition | AC-1 | Edge Case | Condición numérica negativa: -5 < 0 → resultado true | Flow con Simple Decision; `field: -5`, `operator: is_less`, `value: 0`, `type: number` | Company Login > Sidebar: Boards > Click [Board] > Canvas: Configurar Simple Decision: field=-5, operator="is less than", value=0, type=number > Canvas: Button "Run" > Verify: rama "By True" | Rama "By True" (-5 < 0 es true numérico) | 🟡 | ❌ | ✅ **PASS** — 2026-07-14 |
| TC-011 | Nodes / Canvas | AC-4 | Edge Case | UI: operador unario oculta campo value | Board con nodo Simple Decision en canvas | Company Login > Sidebar: Boards > Click [Board] > Canvas: Click [Simple Decision] > Drawer: Select type "boolean" > Drawer: Select operator "is true" (unario) > Verify: campo "value" NO está visible en el formulario | El campo "value" desaparece al seleccionar un operador unario | 🟠 | ✅ | ✅ **PASS** — 2026-07-14 |
| TC-012 | Nodes / Canvas | AC-3 | Edge Case | UI: cambio de tipo con operador previamente seleccionado — no queda operador inválido | Board con nodo Simple Decision | Company Login > Sidebar: Boards > Click [Board] > Canvas: Click [Simple Decision] > Drawer: Select type "number" > Drawer: Select operator "is greater than" > Drawer: Select type "string" > Verify: operador seleccionado es válido para "string" (o se resetea) | Al cambiar tipo, el operador se actualiza a uno válido para el nuevo tipo (no queda un operador de number seleccionado cuando el tipo es string) | 🟠 | ✅ | ✅ **PASS** — 2026-07-14 |
| TC-013 | Nodes / Condition | AC-1 | Negativo | El bug original NO ocurre: `2 > 12` con `type: number` → false (no true) | Flow con Simple Decision configurado con `type: number` | Company Login > Sidebar: Boards > Click [Board] > Canvas: Configurar Simple Decision: field=2, operator="is greater than", value=12, type=number > Canvas: Button "Run" > Wait: ejecución > Verify: rama "By False" activa (NO "By True") | La rama "By False" está activa. El bug está corregido. Si el resultado es "By True" → bug no corregido | 🔴 | ❌ | ✅ **PASS** — 2026-07-14 🐛 BUG FIX VERIFICADO |
| TC-014 | Nodes / Condition | AC-2 | Negativo | Backward compat: condición sin `type` con string comparison — comportamiento legacy preservado | Flow existente en staging con Simple Decision configurado SIN campo `type` | Company Login > Sidebar: Boards > Click [Board existente con Simple Decision sin type] > Canvas: Button "Run" > Wait: ejecución > Verify: resultado es el mismo que antes del deploy | El resultado de la condición es el mismo (legacy path activo). El flow existente funciona sin cambios | 🔴 | ❌ | ✅ **PASS** — 2026-07-14 |
| TC-015 | Nodes / Canvas | AC-3 | Negativo | Validación frontend: campo value con texto en tipo number → error de validación | Board con nodo Simple Decision | Company Login > Sidebar: Boards > Click [Board] > Canvas: Click [Simple Decision] > Drawer: Select type "number" > Drawer: Fill value="hola" (texto) > Verify: mensaje de validación de error | El campo muestra error de validación (no acepta texto en tipo number) | 🟠 | ✅ | ✅ **PASS** — 2026-07-14 |
| TC-016 | Nodes / Switch | AC-6 | Regresión | Flow con Multiple Decision (Switch) no regresionó | Flow existente en staging con nodo Multiple Decision configurado | Company Login > Sidebar: Boards > Click [Board con Multiple Decision] > Canvas: Button "Run" > Wait: ejecución > Verify: resultado igual al esperado (mismo que antes del deploy) > Sidebar: Executions > Verify: status "completed" | El Multiple Decision funciona igual que antes. El cambio en switchrule no introdujo regresiones | 🔴 | ✅ | ✅ **PASS** — 2026-07-14 |
| TC-017 | Nodes / Condition | AC-2 | Regresión | Flow con Simple Decision legado — historial de ejecuciones no alterado | Ejecuciones previas del flow con Simple Decision sin `type` | Company Login > Sidebar: Executions > Filter: [Flow con Simple Decision] > Verify: ejecuciones previas al deploy muestran status inalterado | Ejecuciones anteriores no cambiaron su status | 🟡 | ❌ | ✅ **PASS** — 2026-07-14 |
| TC-018 | Boards / Executions | AC-1 | Regresión | Ejecución de flow con Simple Decision numérico registrada en historial con status correcto | Flow con Simple Decision numérico ejecutado (TC-003 o TC-004) | Company Login > Sidebar: Executions > Click [última ejecución del flow con Simple Decision] > Verify: status "completed" > Verify: nodo Condition muestra status "success" | Status de ejecución "completed", nodo Condition: "success" | 🟡 | ❌ | ✅ **PASS** — 2026-07-14 |
| TC-CR-001 | Nodes / Canvas | — | Code Review | Condición legacy editada (solo operador cambia) → backend acepta sin error y resultado correcto | Flow existente con Simple Decision SIN campo `type`; abrir el drawer y cambiar el operador | Company Login > Sidebar: Boards > Click [Board con Simple Decision legacy] > Canvas: Click [nodo Simple Decision] > Drawer: Cambiar operador (ej: seleccionar is_equal_to) > Drawer: Button "Save" > Canvas: Button "Run" > Verify: resultado correcto, sin error en la ejecución | El flow ejecuta sin error. El resultado es el esperado. No hay mensaje de "Operator is not valid" en la ejecución | 🟠 | ❌ | ✅ **PASS** — 2026-07-14 |
| TC-CR-002 | Nodes / Condition | — | Code Review | Condición legacy con is_greater (string-lexicográfico) preserva comportamiento previo | Flow existente con Simple Decision SIN campo `type` y operador `is_greater` o `is_less` configurado | Company Login > Sidebar: Boards > Click [Board con Simple Decision legacy is_greater] > Canvas: Button "Run" > Wait: ejecución > Verify: resultado idéntico al de antes del deploy | El legacy path se mantiene intacto para condiciones sin `type`. Resultado igual al esperado pre-deploy | 🟡 | ❌ | ✅ **PASS** — 2026-07-14 |

---

## Casos de Regresión

| ID | Módulo impactado | Caso de regresión | Por qué podría romperse | Prioridad | Estado |
|----|-----------------|-------------------|------------------------|-----------|--------|
| REG-001 | Nodes / Switch | Multiple Decision (Switch) → sin regresión | `switchrule.go` ahora delega a `ruleeval` en lugar de lógica propia | 🔴 | ✅ **PASS** — 2026-07-14 |
| REG-002 | Nodes / Condition | Flow con Simple Decision legacy (sin `type`) → sigue funcionando | Legacy path puede haberse roto | 🔴 | ✅ **PASS** — 2026-07-14 |
| REG-003 | Executions | Historial de ejecuciones previas intacto | Cambios en motor de condition | 🟡 | ✅ **PASS** — 2026-07-14 |

---

## Queries de Verificación BD

> ⚠️ No hay migraciones de BD en este ticket — el fix es en lógica Go.
> Las verificaciones de BD se hacen vía UI del Execution History, no via DBeaver.

```sql
-- No aplica: IONF-1128 no introduce ni modifica schema de BD.
-- El status de ejecución del nodo condition se almacena en SQLite por flow (interno al motor Go).
-- Verificación vía UI: Sidebar: Executions > Click [ejecución] > Inspect nodo Condition.
```

---

## Notas

- El fix es en **lógica Go** en `flow_binaries/core/actions/condition/` + nuevo package `ruleeval/` (extraído de switchnode).
- Frontend: cambios en `webcomponents-flow/src/flow/components/FlowDrawer/Condition/`.
- No se requieren queries DBeaver — el resultado de la condición se verifica directamente en el canvas (rama activa) y en la UI de Execution History.
- **Prioridad de testing**: TC-003/TC-004/TC-013 son el corazón del fix (el bug original). TC-014 es crítico para backward compat.
- Para TC-003 y TC-004: se necesita un flow con Simple Decision configurado con tipo numérico en staging, o crear uno nuevo durante el testing.

---

## Hallazgos del Testing (2026-07-14)

| # | Tipo | Descripción |
|---|------|-------------|
| OBS-001 | Comportamiento | El drawer del nodo se abre con **doble click sobre el ícono** (embudo), no sobre el texto del nodo. Doble click sobre el texto activa el modo "inline rename". |
| OBS-002 | Confirmación | Tipos disponibles en selector: **String, Number, Boolean, Array, Object** |
| OBS-003 | Confirmación | El operador `exists` (String/unario) oculta el campo Value correctamente |
| OBS-004 | Confirmación | Al cambiar de Number → String, el operador `is_greater_than` desaparece y se reemplaza por `exists` |
| OBS-005 | Evidencia CR | Ejecución registrada: `HadFatalError: false`, `status: completed`, `units_consumed: 3` |
