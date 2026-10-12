## Contexto

### Descripción
Automatización del nodo **Iterator**. Este nodo itera sobre un array y emite cada item individualmente como un output separado. Cada item dispara la ejecución de los nodos downstream de forma independiente.

> **Fuente**: `Iond Testing Plan - Iond Automation Plan.csv` (línea 63)
> **Referencia técnica**: `knowledge/L2-modules/nodes/module.md` — Sección 4 (Iterator)

### Módulo afectado
- Módulo principal: `Tenant / Boards / Canvas / Iterator`
- Backend: `ion.action.iterator` — Package `core/actions/iterator`
- Config: Recibe un array (JSON string o []interface{})
- Outputs: `output` (un output por cada item), `error`
- Tests backend: No tiene test dedicado
- Drawer en: N/A (configuración estándar)

### Pre-requisitos
- Board de prueba con draft activo
- Nodo upstream que provea un array como output

---

## Test Cases

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-NODE-ITER-01 | Happy Path | Iterar sobre array de 5 elementos — verificar que emite 5 outputs individuales | 🔴 | ⬜ |
| TC-NODE-ITER-02 | Happy Path | Iterar sobre array de objetos — verificar que cada objeto llega completo al output | 🔴 | ⬜ |
| TC-NODE-ITER-03 | Edge Case | Iterar sobre array vacío — verificar que NO se ejecutan nodos downstream | 🟠 | ⬜ |
| TC-NODE-ITER-04 | Edge Case | Iterar sobre array de 1 elemento — verificar que emite un solo output | 🟡 | ⬜ |
| TC-NODE-ITER-05 | Edge Case | Input que no es array (string JSON) — verificar que parsea correctamente o activa error | 🟠 | ⬜ |
| TC-NODE-ITER-06 | Negativo | Input null o undefined — verificar activación del edge de error | 🟠 | ⬜ |

---

## Notas de Automatización
- No tiene tests dedicados en backend — mayor riesgo de regresión
- Comúnmente usado en combinación con Aggregate (Iterator → procesamiento → Aggregate)
- 6 test cases
