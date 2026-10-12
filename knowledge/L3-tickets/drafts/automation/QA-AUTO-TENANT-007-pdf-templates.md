## Contexto

### Descripción
Automatización de la validación completa del módulo de PDF Templates: CRUD, import/export JSON, carga de PDF base, elementos del editor (text, image, SVG, table, signature, etc.) y acciones.

### Módulo afectado
- Módulo principal: `Tenant / PDF Templates`
- Módulos relacionados: `Boards / ION PDF nodes`, `IONPDF microservice`

---

## Test Cases

### CRUD

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-PDF-01 | Happy Path | Crear nuevo PDF Template | 🔴 | ⬜ |
| TC-PDF-02 | Happy Path | Importar template desde JSON | 🔴 | ⬜ |
| TC-PDF-03 | Happy Path | Exportar template como JSON | 🔴 | ⬜ |
| TC-PDF-04 | Happy Path | Cargar PDF base (Load Base PDF) | 🔴 | ⬜ |
| TC-PDF-05 | Negativo | Importar JSON inválido — error controlado | 🟠 | ⬜ |

### Configuración de Página

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-PDF-06 | Happy Path | Configurar Page Size | 🟠 | ⬜ |
| TC-PDF-07 | Happy Path | Configurar Margins | 🟠 | ⬜ |

### Elementos del Editor

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-PDF-08 | Happy Path | Agregar y configurar elemento Text | 🔴 | ⬜ |
| TC-PDF-09 | Happy Path | Agregar y configurar Multi Variable Text | 🔴 | ⬜ |
| TC-PDF-10 | Happy Path | Agregar y configurar Image | 🔴 | ⬜ |
| TC-PDF-11 | Happy Path | Agregar y configurar SVG | 🟠 | ⬜ |
| TC-PDF-12 | Happy Path | Agregar y configurar Signature | 🟠 | ⬜ |
| TC-PDF-13 | Happy Path | Agregar y configurar Table | 🔴 | ⬜ |
| TC-PDF-14 | Happy Path | Agregar y configurar Code 128 (barcode) | 🟠 | ⬜ |
| TC-PDF-15 | Happy Path | Agregar y configurar Shapes | 🟡 | ⬜ |
| TC-PDF-16 | Happy Path | Agregar y configurar Dates | 🟠 | ⬜ |
| TC-PDF-17 | Happy Path | Agregar y configurar Form Controls | 🟠 | ⬜ |
| TC-PDF-18 | Edge Case | Soporte de caracteres árabes en Text/Multi Variable Text | 🟠 | ⬜ |

### Actions

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-PDF-19 | Happy Path | Clonar template | 🟠 | ⬜ |
| TC-PDF-20 | Happy Path | Descargar template | 🟠 | ⬜ |
| TC-PDF-21 | Happy Path | Preview del template | 🔴 | ⬜ |

---

## Notas de Automatización
- 21 test cases — módulo complejo con editor visual
- Soporte de caracteres árabes es un bug fix de v0.2.0 (ticket 86e1xu7xp)
- Relacionar con los nodos ION PDF en el canvas (QA-AUTO-TENANT-001)
