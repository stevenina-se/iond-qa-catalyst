## Contexto

### Descripción
Automatización del nodo **Mapper** (backend: `transformer`). Este nodo ejecuta un sub-flow completo (mapper) dentro de otro flow, con nodos internos source → target. Es un mini-motor de ejecución interno.

> ⚠️ **Mapeo**: Canvas "Mapper" = Backend `ion.action.transformer` (`core/actions/transformer`) — NO confundir con `mapper` del backend que es "Form"

> **Fuente**: `Iond Testing Plan - Iond Automation Plan.csv` (línea 61)
> **Referencia técnica**: `knowledge/L2-modules/nodes/module.md` — Sección 9 (Transformer)

### Módulo afectado
- Módulo principal: `Tenant / Boards / Canvas / Mapper`
- Backend: `ion.action.transformer` — Package `core/actions/transformer`
- Nodos internos: `source` (inicio), `target` (fin), + nodos intermedios
- BD: Crea su propia instancia SQLite para el sub-flow
- Ejecución: Queue-based — carga el sub-flow, ejecuta nodo por nodo, retorna el resultado del nodo `target`
- Drawer en: `FlowDrawer/AutoMapper/` y `FlowDrawer/Transformer/`

### Pre-requisitos
- Board de prueba con draft activo
- Nodos upstream con datos para transformar

---

## Test Cases

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-NODE-MAPPER-01 | Happy Path | Configurar sub-flow mapper con source → target y verificar transformación de datos | 🔴 | ⬜ |
| TC-NODE-MAPPER-02 | Happy Path | Agregar nodos intermedios en el sub-flow del mapper — verificar ejecución secuencial | 🔴 | ⬜ |
| TC-NODE-MAPPER-03 | Happy Path | Mapper con múltiples campos mapeados — verificar que todos llegan al target | 🔴 | ⬜ |
| TC-NODE-MAPPER-04 | Edge Case | Mapper con input vacío — verificar que el sub-flow se ejecuta sin error | 🟠 | ⬜ |
| TC-NODE-MAPPER-05 | Edge Case | Mapper con nodos que fallan internamente — verificar que el error se propaga al flow principal | 🟠 | ⬜ |
| TC-NODE-MAPPER-06 | Negativo | Mapper sin configurar source/target — verificar error | 🟡 | ⬜ |

---

## Notas de Automatización
- El Mapper crea su propia SQLite para el sub-flow — verificar aislamiento
- Confusión de nombres frecuente: "Mapper" en UI = `transformer` en backend
- 6 test cases
