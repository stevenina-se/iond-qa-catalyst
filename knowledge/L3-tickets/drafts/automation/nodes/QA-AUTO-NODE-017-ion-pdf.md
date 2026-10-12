## Contexto

### Descripción
Automatización de los nodos **ION PDF** en el canvas. Estos nodos permiten interactuar con PDF Templates directamente desde el flow: editar templates, agregar templates, mapear datos y generar PDFs.

> **Fuente**: `Iond Testing Plan - Iond Automation Plan.csv` (líneas 78-81)
> **Referencia técnica**: `knowledge/L2-modules/nodes/module.md`

### Módulo afectado
- Módulo principal: `Tenant / Boards / Canvas / ION PDF`
- Módulos relacionados: `PDF Templates`, `Boards`
- Dependencia: PDF Template existente en el módulo de PDF Templates

### Pre-requisitos
- Board de prueba con draft activo
- Al menos un PDF Template creado en el módulo PDF Templates
- Datos de prueba para mapear al template

---

## Test Cases

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-NODE-PDF-01 | Happy Path | **Edit Template on Canvas** — abrir editor de template PDF desde nodo en el board | 🔴 | ⬜ |
| TC-NODE-PDF-02 | Happy Path | **Add Template on Canvas** — agregar template PDF existente a un nodo | 🔴 | ⬜ |
| TC-NODE-PDF-03 | Happy Path | **Map Function** — mapear datos del flow a campos del template PDF | 🔴 | ⬜ |
| TC-NODE-PDF-04 | Happy Path | **Build a PDF** — generar PDF con datos reales y verificar output | 🔴 | ⬜ |
| TC-NODE-PDF-05 | Happy Path | Mapear múltiples campos con expresiones dinámicas `{{$N.field}}` | 🔴 | ⬜ |
| TC-NODE-PDF-06 | Negativo | Build PDF sin mapeo configurado — verificar error | 🟠 | ⬜ |
| TC-NODE-PDF-07 | Negativo | Build PDF con template inexistente — verificar error | 🟠 | ⬜ |
| TC-NODE-PDF-08 | Edge Case | Build PDF con datos que exceden el espacio del campo en el template | 🟡 | ⬜ |

---

## Notas de Automatización
- Depende del módulo PDF Templates (QA-AUTO-TENANT-007) para tener templates disponibles
- La generación de PDF se efectúa dentro del nodo en el canvas
- Los templates generados son consumidos por sistemas externos
- 8 test cases
