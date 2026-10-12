# QA-AUTO-TENANT-001 — Tenant: Boards — All Tools (Nodos del Canvas)

> ⚠️ **Reemplazado** por los drafts individuales de [`nodes/`](nodes/README.md) (tickets `86e3ku71p`…`86e3ku985` de QA Kanban). Se conserva como referencia.

> Módulo: Tenant > Boards > Create Board > All Tools
> Side: TENANT
> Assignee: Steve Nina, Mijael
> Prioridad: 🔴 Urgent
> Status: Manual for now

## Contexto

### Descripción
Automatización de la validación de TODOS los tipos de nodo disponibles en el canvas de Boards. Este es el módulo más crítico del producto — cada nodo representa una funcionalidad core. Actualmente se ejecuta manualmente.

### Módulo afectado
- Módulo principal: `Tenant / Boards / Canvas / Nodes`
- Módulos relacionados: `Connections`, `App Connectors`, `PDF Templates`, `IonMind`

---

## Test Cases

### Nodos de Control de Flujo

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-BOARD-NODE-01 | Happy Path | Scheduler — configurar y ejecutar trigger programado | 🔴 | ⬜ |
| TC-BOARD-NODE-02 | Happy Path | Webhook — configurar y recibir request externa | 🔴 | ⬜ |
| TC-BOARD-NODE-03 | Happy Path | Webhook Response — configurar respuesta al webhook | 🔴 | ⬜ |
| TC-BOARD-NODE-04 | Happy Path | Timer — configurar delay y verificar ejecución | 🔴 | ⬜ |
| TC-BOARD-NODE-05 | Happy Path | Call Component-Flow — invocar sub-flow | 🔴 | ⬜ |
| TC-BOARD-NODE-06 | Happy Path | On Call Component-Flow — recibir invocación | 🔴 | ⬜ |

### Nodos de Lógica

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-BOARD-NODE-07 | Happy Path | Simple Decision — condición verdadera y falsa | 🔴 | ⬜ |
| TC-BOARD-NODE-08 | Edge Case | Simple Decision — comparar valores numéricos (no como strings) | 🔴 | ⬜ |
| TC-BOARD-NODE-09 | Happy Path | Multiple Decision — múltiples ramas con fallback | 🔴 | ⬜ |
| TC-BOARD-NODE-10 | Happy Path | Code — ejecutar JavaScript personalizado | 🔴 | ⬜ |
| TC-BOARD-NODE-11 | Happy Path | Agent — invocar agente IA | 🔴 | ⬜ |

### Nodos de Transformación

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-BOARD-NODE-12 | Happy Path | HTTP Request — GET, POST, PUT, DELETE | 🔴 | ⬜ |
| TC-BOARD-NODE-13 | Happy Path | Mapper — mapear campos entre input y output | 🔴 | ⬜ |
| TC-BOARD-NODE-14 | Happy Path | Form — presentar formulario y capturar datos | 🔴 | ⬜ |
| TC-BOARD-NODE-15 | Happy Path | Aggregate — agrupar datos de múltiples ejecuciones | 🔴 | ⬜ |
| TC-BOARD-NODE-16 | Happy Path | Iterator — iterar sobre arrays | 🔴 | ⬜ |
| TC-BOARD-NODE-17 | Edge Case | Iterator — array vacío, no ejecutar iteración | 🟠 | ⬜ |

### Nodos de Persistencia (Storage)

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-BOARD-STOR-01 | Happy Path | Storage > Save — guardar dato | 🔴 | ⬜ |
| TC-BOARD-STOR-02 | Happy Path | Storage > Update — actualizar dato existente | 🔴 | ⬜ |
| TC-BOARD-STOR-03 | Happy Path | Storage > Get — obtener dato por key | 🔴 | ⬜ |
| TC-BOARD-STOR-04 | Happy Path | Storage > Delete — eliminar dato | 🔴 | ⬜ |
| TC-BOARD-STOR-05 | Happy Path | Storage > Check — verificar existencia | 🔴 | ⬜ |
| TC-BOARD-STOR-06 | Happy Path | Storage > Count — contar registros | 🔴 | ⬜ |
| TC-BOARD-STOR-07 | Happy Path | Storage > Delete All — eliminar todos los registros | 🟠 | ⬜ |
| TC-BOARD-STOR-08 | Happy Path | Storage > Search — buscar registros con filtros | 🟠 | ⬜ |

### Nodos ION PDF

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-BOARD-PDF-01 | Happy Path | Edit Template on Canvas — editar template PDF desde el board | 🔴 | ⬜ |
| TC-BOARD-PDF-02 | Happy Path | Add Template on Canvas — agregar template al board | 🔴 | ⬜ |
| TC-BOARD-PDF-03 | Happy Path | Map Function — mapear datos al template | 🔴 | ⬜ |
| TC-BOARD-PDF-04 | Happy Path | Build a PDF — generar PDF con datos reales | 🔴 | ⬜ |

### Nodos Tenant App

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-BOARD-TAPP-01 | Happy Path | Use a Tenant Node — usar nodo de app del tenant | 🔴 | ⬜ |
| TC-BOARD-TAPP-02 | Happy Path | Add a node with IonMind — agregar nodo vía IA | 🔴 | ⬜ |

---

## Notas de Automatización
- Este ticket es el MÁS GRANDE del plan — 32 test cases solo para nodos
- Actualmente es "Manual for now" — priorizar automatización por bloques
- Cada nodo requiere un board de prueba con conexiones pre-configuradas
- Los nodos de IonMind requieren que IonMind esté desplegado
- Simple Decision: incluir caso específico de comparación numérica vs strings (bug v0.1.0)
