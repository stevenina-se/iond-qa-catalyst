## Contexto

### Descripción
Automatización del nodo **Aggregate**. Este nodo agrupa N items que llegan en secuencia y los emite como un array cuando se alcanza el `length` configurado. Almacena items parciales en SQLite (tabla `aggregates`).

> **Fuente**: `Iond Testing Plan - Iond Automation Plan.csv` (línea 62)
> **Referencia técnica**: `knowledge/L2-modules/nodes/module.md` — Sección 1 (Aggregate)

### Módulo afectado
- Módulo principal: `Tenant / Boards / Canvas / Aggregate`
- Backend: `ion.action.aggregate` — Package `core/actions/aggregate`
- Config: `{ "length": N }` — N debe ser > 0
- Inputs: `input` (datos), `input-error` (marca item como error)
- Outputs: `output` (array de N items), `error`
- BD: SQLite — tabla `aggregates` para items parciales
- Tests backend: `aggregate_test.go`

### Pre-requisitos
- Board de prueba con draft activo
- Nodo upstream que emita múltiples outputs (ej. Iterator)

---

## Test Cases

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-NODE-AGG-01 | Happy Path | Configurar aggregate con length=3 y enviar 3 items — verificar que emite array de 3 | 🔴 | ⬜ |
| TC-NODE-AGG-02 | Happy Path | Enviar items uno a uno — verificar que acumula y no emite hasta completar el length | 🔴 | ⬜ |
| TC-NODE-AGG-03 | Edge Case | Enviar un item al `input-error` — verificar que el item se marca como error en el array | 🟠 | ⬜ |
| TC-NODE-AGG-04 | Edge Case | Aggregate con length=1 — verificar que emite inmediatamente | 🟡 | ⬜ |
| TC-NODE-AGG-05 | Negativo | Configurar aggregate con length=0 o negativo — verificar validación | 🟡 | ⬜ |

---

## Notas de Automatización
- Usa tabla SQLite `aggregates` para acumulación — verificar limpieza entre ejecuciones
- Comúnmente usado junto con Iterator → Aggregate
- 5 test cases
