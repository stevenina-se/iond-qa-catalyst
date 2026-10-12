## Contexto

### Descripción
Automatización del **comportamiento general** de todos los nodos del canvas. Estos test cases verifican reglas que aplican a TODOS los tipos de nodo: manejo de errores, ciclo de vida de status, resolución de expresiones, fan-out y aislamiento de ejecución.

> **Fuente**: `knowledge/L2-modules/nodes/module.md` — Reglas de Negocio de Nodos
> **Referencia técnica**: `knowledge/L2-modules/nodes/module.md` — Secciones: Ciclo de Vida, Schema SQLite

### Módulo afectado
- Módulo principal: `Tenant / Boards / Canvas / All Nodes`
- Backend: `core/actions/flow` — Motor principal de ejecución
- Expression Language: `expr-lang/expr` v1.17.2 — resuelve `{{$N.field}}`
- Ciclo: `LoadFlow → RunNode → [ContinueNode → PushNode]* → Fin`
- Status: `pending` → `processing` → `success`/`error`

### Pre-requisitos
- Board de prueba con draft activo y múltiples tipos de nodo
- Al menos un flow con múltiples edges de output (fan-out)

---

## Reglas de Negocio

1. **Todos los nodos tienen handle `error`** — Siempre hay una salida de error
2. **Los datos fluyen por los edges** — Un nodo NO puede acceder a datos de otro nodo directamente
3. **Las expresiones se resuelven** con `libs.ReplaceReferences` antes de ejecutar
4. **Cada ejecución crea una SQLite nueva** — No se reutilizan BDs entre ejecuciones
5. **Si un nodo falla → el edge de error se activa** — El flow puede manejar errores
6. **La queue se restaura en caso de fallo** — Permite retry

---

## Test Cases

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-NODE-GEN-01 | Happy Path | Todos los nodos tienen handle `error` — verificar que está disponible en el canvas | 🔴 | ⬜ |
| TC-NODE-GEN-02 | Happy Path | Error en un nodo activa el edge de error — verificar que el flow continúa por la rama de error | 🔴 | ⬜ |
| TC-NODE-GEN-03 | Happy Path | Verificar status de nodo durante ejecución: `pending` → `processing` → `success`/`error` | 🟠 | ⬜ |
| TC-NODE-GEN-04 | Happy Path | Datos fluyen por edges — verificar que un nodo accede a datos del nodo anterior via `{{$N.field}}` | 🔴 | ⬜ |
| TC-NODE-GEN-05 | Edge Case | Nodo sin edges downstream — verificar que la ejecución termina limpiamente | 🟡 | ⬜ |
| TC-NODE-GEN-06 | Edge Case | Fan-out: un nodo con múltiples edges de output — verificar que todos los downstream reciben datos | 🟠 | ⬜ |
| TC-NODE-GEN-07 | Edge Case | Cada ejecución crea SQLite nueva — verificar que no hay contaminación entre ejecuciones | 🟠 | ⬜ |
| TC-NODE-GEN-08 | Happy Path | Drawer de configuración — verificar que se abre al hacer click en cada tipo de nodo | 🔴 | ⬜ |

---

## Notas de Automatización
- Estos tests aplican a TODOS los nodos — ejecutar con al menos 3-4 tipos de nodo diferentes
- TC-NODE-GEN-07 (aislamiento SQLite) es crítico para evitar data leaks entre ejecuciones
- TC-NODE-GEN-08 (drawers) puede automatizarse como smoke test visual
- 8 test cases
