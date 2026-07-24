# AC Consolidados — 86e22fzvx

> Generado en: Discovery — 2026-07-14
> Ticket: Simple Decision compara valores numéricos como strings, resultado incorrecto
> Fuentes: Descripción del ticket + Spec del Developer (comentario Gustavo, 2026-07-07)
> QA Engineer: Steve Nina

---

## Acceptance Criteria Finales

### AC-1 — Comparación numérica correcta
**Fuente**: Bug report (descripción) + Spec Developer  
**Texto**: Cuando una condición del nodo Simple Decision tiene `type: "number"`, la comparación se realiza de forma numérica.

**Ejemplos verificables:**
- `field: 2, operator: is_greater, value: 12, type: number` → resultado: `false` (rama "By False")
- `field: 15, operator: is_greater, value: 12, type: number` → resultado: `true` (rama "By True")
- `field: 2.5, operator: is_less, value: 10.0, type: number` → resultado: `true`
- `field: 12, operator: is_equal, value: 12, type: number` → resultado: `true`

**Criterio de aceptación**: La salida del nodo es por la rama correcta (`then` / `false`) según el valor numérico real.

---

### AC-2 — Backward Compatibility (Legacy Path)
**Fuente**: Spec Developer  
**Texto**: Las condiciones existentes sin campo `type` (guardadas antes del fix) continúan evaluándose por el path legacy (string/expr-lang), sin necesidad de reconfiguración.

**Criterio de aceptación**: Un flow con Simple Decision configurado en la versión anterior (sin `type`) se ejecuta correctamente sin ningún cambio del usuario.

---

### AC-3 — Selector de tipo en el drawer del frontend
**Fuente**: Spec Developer  
**Texto**: El drawer de configuración del nodo Simple Decision (ConditionItem) incluye un selector de tipo (`string`, `number`, `boolean`, `array`, `object`) y los operadores disponibles se filtran dinámicamente según el tipo seleccionado.

**Criterio de aceptación**:
- El selector de tipo está visible en la UI al configurar una condición
- Al cambiar el tipo, la lista de operadores cambia acorde
- Los operadores mostrados son válidos para el tipo seleccionado

---

### AC-4 — Ocultamiento del campo value en operadores unarios
**Fuente**: Spec Developer  
**Texto**: Para operadores unarios como `is_true`, `is_false`, `is_empty`, `is_not_empty`, el campo "value" se oculta en el drawer porque no es necesario.

**Criterio de aceptación**: Al seleccionar un operador unario, el campo de valor desaparece del formulario.

---

### AC-5 — Condición nueva: defaults correctos
**Fuente**: Spec Developer  
**Texto**: Al crear una nueva condición en el Simple Decision, los valores por defecto son `type: "string"` y `operator: "is_equal_to"`.

**Criterio de aceptación**: Una nueva condición aparece con tipo "string" y operador "is equal to" preseleccionados.

---

### AC-6 — Sin regresión en Multiple Decision (Switch)
**Fuente**: Riesgo identificado en risk-triage (R-03)  
**Texto**: El nodo Multiple Decision (Switch) continúa funcionando correctamente. El cambio en `switchrule.go` para delegar a `ruleeval` no introduce regresiones.

**Criterio de aceptación**: Un flow existente con Multiple Decision se ejecuta con el mismo resultado que antes del deploy.

---

## Notas de Reconciliación

| AC | Estado | Nota |
|----|--------|------|
| AC-1 | ✅ Nuevo (resuelve el bug) | Core del ticket |
| AC-2 | ✅ Nuevo (backward compat) | Crítico — protege flows existentes |
| AC-3 | ✅ Nuevo (frontend) | Feature de UX |
| AC-4 | ✅ Nuevo (frontend) | UX de operadores unarios |
| AC-5 | ✅ Nuevo (frontend) | Defaults de nuevas condiciones |
| AC-6 | ✅ Nuevo (regresión) | Protección del Switch |

> No hubo divergencias entre la descripción original del bug y la spec del Developer. La spec es una addenda que detalla cómo se resuelve el bug y qué funcionalidades adicionales se agregan.

---

## Aprobación

- [ ] QA Engineer aprueba estos AC consolidados
