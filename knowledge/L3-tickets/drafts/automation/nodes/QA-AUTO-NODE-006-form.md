## Contexto

### Descripción
Automatización del nodo **Form** (backend: `mapper`). Este nodo extrae el campo `params` de un mapa de datos y lo emite como output. Funciona como un formulario de mapeo de campos.

> ⚠️ **Mapeo**: Canvas "Form" = Backend `ion.action.mapper` (`core/actions/mapper`) — NO confundir con "Mapper" del canvas que es `transformer`

> **Fuente**: `Iond Testing Plan - Iond Automation Plan.csv` (línea 60 — "Prioritario para el siguiente sprint")
> **Referencia técnica**: `knowledge/L2-modules/nodes/module.md` — Sección 5 (Mapper)

### Módulo afectado
- Módulo principal: `Tenant / Boards / Canvas / Form`
- Backend: `ion.action.mapper` — Package `core/actions/mapper`
- Config: `{ "params": { ... } }`
- Outputs: `output` (valor de params), `error`
- Error típico: "Mapper not configured"
- Drawer en: `FlowDrawer/Mapper/`

### Pre-requisitos
- Board de prueba con draft activo
- Nodos upstream con datos para mapear

---

## Test Cases

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-NODE-FORM-01 | Happy Path | Configurar params y verificar que se extraen correctamente del mapa de datos | 🔴 | ⬜ |
| TC-NODE-FORM-02 | Happy Path | Mapear múltiples campos con expresiones `{{$N.field}}` | 🔴 | ⬜ |
| TC-NODE-FORM-03 | Negativo | Configurar Form sin params — verificar error "Mapper not configured" | 🟠 | ⬜ |
| TC-NODE-FORM-04 | Edge Case | Params con valores nested (objetos/arrays) — verificar extracción correcta | 🟠 | ⬜ |
| TC-NODE-FORM-05 | Edge Case | Referenciar campo inexistente en expresión — verificar valor null o error | 🟡 | ⬜ |

---

## Notas de Automatización
- Prioritario para el siguiente sprint según el CSV
- Confusión de nombres frecuente: "Form" en UI = `mapper` en backend
- 5 test cases
