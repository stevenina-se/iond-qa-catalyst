# Risk Triage — 86e22fzvx

> Generado en: Discovery — 2026-07-14
> Ticket: Simple Decision compara valores numéricos como strings
> QA Engineer: Steve Nina

---

## Resumen de Riesgos

| # | Área | Riesgo | Severidad | Mitigación |
|---|------|--------|-----------|------------|
| R-01 | Backend / Condition | `ruleeval` nuevo package — posibles edge cases en conversión de tipo para `number` (float vs int) | 🔴 Alto | Testar con enteros y decimales |
| R-02 | Backend / Condition | Backward compatibility — condiciones sin campo `type` deben seguir usando legacy path | 🔴 Alto | Testar con condiciones antiguas guardadas |
| R-03 | Backend / Switch | `switchnode` ahora delega a `ruleeval` — riesgo de regresión en Multiple Decision | 🟠 Medio | Incluir TC de regresión de Switch |
| R-04 | Frontend / ConditionItem | Operadores dinámicos por tipo — un cambio de tipo puede mostrar operador inválido aún seleccionado | 🟠 Medio | Cambiar tipo con operador ya seleccionado y verificar |
| R-05 | Frontend / ConditionItem | Validación inline de número — puede rechazar entradas válidas o aceptar inválidas | 🟠 Medio | Testar con enteros, decimales, negativos, strings |
| R-06 | Frontend / ConditionItem | Valor oculto en operadores unarios (`is_true`, `is_empty`) — si no se limpia el valor al ocultarse, puede enviarse al backend | 🟡 Bajo | Verificar que el payload no incluye `value` para unarios |
| R-07 | Backend / ruleeval | Tipos `boolean`, `array`, `object` — menos testados en UI; pueden tener edge cases | 🟡 Bajo | Al menos un smoke test por tipo |
| R-08 | Cross-module | Flows guardados con Simple Decision en versión anterior — deben funcionar sin reconfiguración | 🔴 Alto | Testar flow con condición sin `type` existente en staging |
| R-09 | Frontend | Condición nueva por defecto `type: "string"`, `operator: "is_equal_to"` — verificar que se guarda correctamente | 🟡 Bajo | TC de creación de nueva condición |

---

## Área de Mayor Riesgo: Backward Compatibility (R-08)

> Este es el riesgo más crítico del ticket. El equipo tiene flows en staging con condiciones antiguas (sin campo `type`). Si el fix rompe esas condiciones, los flows existentes fallarán.

**Verificación requerida:**
- Identificar un flow existente en staging que use Simple Decision con operadores de comparación
- Ejecutarlo sin modificaciones y verificar que funciona correctamente
- Solo entonces proceder a crear nuevas condiciones con `type`

---

## Impacto Cruzado identificado

| Módulo | Componente | Riesgo | Acción |
|--------|-----------|--------|--------|
| **Multiple Decision (Switch)** | `switchrule.go` ahora delega a `ruleeval` | 🟠 Medio — posible regresión si `ruleeval` tiene bugs | TC de regresión Switch |
| **Boards** | Ejecución de flows con Simple Decision | 🔴 Alto — si condition falla, el flow falla | TC de ejecución completa |
| **Executions** | Historial por nodo | 🟡 Bajo — el status del nodo cambia si condition falla | Verificar status en historial |

---

## Preguntas para el Developer (formato abierto)

1. ¿Cuándo se cambia el `type` de una condición ya configurada (ej: de `string` a `number`), el `operator` se resetea automáticamente a uno válido para el nuevo tipo?
2. ¿El campo `value` se envía al backend como string siempre, o se convierte a number/boolean antes del envío?
3. ¿Los operadores unarios (`is_true`, `is_false`, `is_empty`, `is_not_empty`) ya están implementados en el `ruleeval` o solo en el frontend?
4. ¿Las condiciones existentes sin campo `type` se migran automáticamente al legacy path o hay algún caso donde podrían fallar?

---

## Aprobación

- [ ] QA Engineer aprueba este risk triage
