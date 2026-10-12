## Contexto

### Descripción
Automatización del nodo **Timer**. Este nodo pausa la ejecución del flow por un tiempo configurado (minutos y/o segundos), con un límite máximo de 15 minutos (900 segundos).

> **Fuente**: `Iond Testing Plan - Iond Automation Plan.csv` (línea 64)
> **Referencia técnica**: `knowledge/L2-modules/nodes/module.md` — Sección 8 (Timer)

### Módulo afectado
- Módulo principal: `Tenant / Boards / Canvas / Timer`
- Backend: `ion.action.timer` — Package `core/actions/timer`
- Config: `{ "minutes": N, "seconds": N }`
- Límite: Máximo 15 minutos (900 segundos)
- Outputs: `output` ({ duration, completed_at }), `error`
- Validaciones: minutes y seconds >= 0, total <= 900s
- Tests backend: `timer_test.go`

### Pre-requisitos
- Board de prueba con draft activo

---

## Test Cases

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-NODE-TIMER-01 | Happy Path | Configurar timer con 5 segundos — verificar delay y output con `duration` y `completed_at` | 🔴 | ⬜ |
| TC-NODE-TIMER-02 | Happy Path | Configurar timer con minutos y segundos combinados | 🟠 | ⬜ |
| TC-NODE-TIMER-03 | Edge Case | Timer con valor máximo (15 minutos / 900 segundos) — verificar que acepta | 🟠 | ⬜ |
| TC-NODE-TIMER-04 | Negativo | Timer con valor mayor a 15 minutos — verificar rechazo/validación | 🔴 | ⬜ |
| TC-NODE-TIMER-05 | Negativo | Timer con minutos o segundos negativos — verificar validación | 🟡 | ⬜ |
| TC-NODE-TIMER-06 | Negativo | Timer con 0 minutos y 0 segundos — verificar comportamiento | 🟡 | ⬜ |

---

## Notas de Automatización
- Para tests, usar valores bajos (5-10 segundos) para no alargar la suite
- TC-NODE-TIMER-03 (máximo 15 min) es un test largo — considerar ejecutar solo en regression completa
- Verificar que el output incluye `duration` y `completed_at` correctamente
- 6 test cases
