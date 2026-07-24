# Test Plan — 86e22fzvx

> Generado en: Discovery — 2026-07-14
> Ticket: Simple Decision compara valores numéricos como strings, resultado incorrecto
> QA Engineer: Steve Nina
> Módulo: Nodes / Simple Decision (`ion.action.condition`)

---

## Información General

| Campo | Valor |
|-------|-------|
| Ticket | 86e22fzvx |
| Módulo principal | Nodes / Simple Decision |
| Backend | `flow_binaries` — `core/actions/condition` + `core/actions/ruleeval` |
| Frontend | `webcomponents-flow` — `FlowDrawer/Condition/` |
| Repos afectados | `flow_binaries` (PR #13), `webcomponents-flow` (PR #7) |
| Entorno | dev-app.ionflow.io (Staging) |
| Branch | DEVELOPMENT (IONF-1128 mergeado) |
| Rol de testing | Company User con permiso `UPDATE_BOARD` |
| Browser | Chrome |

---

## Estrategia de Testing

### Prioridad
**🔴 Crítico** — El nodo Simple Decision es parte del motor core de Ionflow. Un error en la lógica de condiciones puede causar flows incorrectos en producción con impacto real en el e-commerce de los clientes.

### Enfoque
1. **Verificar el fix del bug principal primero** (AC-1): comparación numérica correcta
2. **Verificar backward compatibility** (AC-2): flows antiguos sin `type` siguen funcionando
3. **Verificar cambios de UI** (AC-3, AC-4, AC-5): selector de tipo, operadores dinámicos
4. **Regresión de Switch** (AC-6): Multiple Decision no regresionó

### Modo de Ejecución
- **Playwright MCP** (Canal 1) — Testing asistido con el browser
- El QA Engineer supervisa en tiempo real

---

## Bloques de Testing

### Bloque 0 — Pre-requisitos
- Verificar que `code-review-qa.md` existe (será generado en Deployment)
- Verificar que staging está accesible y la branch DEVELOPMENT está deployed

### Bloque 1 — Smoke Tests
- Canvas carga correctamente con el nodo Simple Decision disponible
- El drawer del nodo Simple Decision se abre al hacer click

### Bloque 2 — Happy Path (AC-1, AC-3, AC-5)
- Condición numérica: `2 > 12` → resultado `false` (rama "By False")
- Condición numérica: `15 > 12` → resultado `true` (rama "By True")
- Condición numérica con decimal: `2.5 < 10.0` → resultado `true`
- UI: selector de tipo visible, operadores cambian por tipo
- UI: nueva condición tiene defaults `string` + `is_equal_to`

### Bloque 3 — Edge Cases (AC-1, AC-4)
- Igualdad numérica exacta: `12 == 12` → `true`
- Negativo: `-5 < 0` → `true`
- Decimal borderline: `10.0 >= 10` → `true`
- UI: operador unario oculta el campo value
- UI: cambio de tipo resetea/filtra operadores

### Bloque 4 — Negativos (AC-1)
- Condición numérica: `2 > 12` → verificar que sale por "By False" (no "By True")
- Tipo incorrecto: `type: "string"`, valor `"2"` vs `"12"` → verificar comportamiento string (lexicográfico)
- Validación frontend: campo `value` con texto en tipo `number` → debe mostrar error de validación

### Bloque 5 — Regresión (AC-2, AC-6)
- Flow existente con Simple Decision SIN `type` → debe ejecutarse igual que antes
- Flow existente con Multiple Decision (Switch) → sin regresión

### Bloque 6 — DB Evidence
- No aplica schema nuevo — verificación vía UI de Execution History
- Verificar en historial: status `completed` cuando condición se evalúa correctamente

---

## Criterios de Aceptación del Testing

| Criterio | Requerido | Aprobación |
|----------|-----------|-----------|
| Smoke tests | 100% PASS | Obligatorio |
| Happy Path (AC-1 fix numérico) | 100% PASS | Bloqueante |
| Backward compatibility (AC-2) | 100% PASS | Bloqueante |
| UI cambios (AC-3, AC-4, AC-5) | ≥80% PASS | Requerido |
| Regresión Switch (AC-6) | 100% PASS | Requerido |
| Bugs bloqueantes 🔴 | 0 | Obligatorio |

---

## Riesgos a Monitorear Durante Testing

| Riesgo | Área | Cómo detectarlo |
|--------|------|----------------|
| R-01: Float vs int en ruleeval | Backend | TC con decimales |
| R-02: Backward compat roto | Backend | TC con condición sin `type` |
| R-03: Regresión Switch | Backend | TC de Switch existente |
| R-04: Operador inválido al cambiar tipo | Frontend | TC de cambio de tipo con operador ya seleccionado |
| R-05: Validación number incorrecta | Frontend | TC con inputs de edge case |

---

## Dependencias

- Acceso al canvas de Boards en staging
- Un flow existente con Simple Decision (para backward compat)
- Posibilidad de crear un nuevo flow con nodo Simple Decision
- Un flow existente con Multiple Decision (para regresión de Switch)

---

## Aprobación del Plan

- [ ] QA Engineer aprueba este plan de testing
