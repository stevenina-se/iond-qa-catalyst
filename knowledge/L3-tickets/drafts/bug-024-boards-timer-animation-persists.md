# QA FOUND ISSUE ESCALATION REPORT — IOND

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | Boards / Nodes |
| Path | Company > Boards > [Board] > Canvas > Timer Node |
| Versión | gateway-ion v0.1.0 · flow_binaries v0.1.0 · gateway v2.0.0 |

## Título

**Boards — Animación del nodo Timer persiste al re-ingresar al canvas, inconsistencia visual**

## Description of the validated/replicated problem

Al utilizar un nodo Timer en el canvas, si el usuario sale de la vista de edición del canvas y vuelve a entrar, la animación del nodo Timer continúa ejecutándose visualmente. Esto genera inconsistencias visuales ya que el Timer no está realmente en ejecución; la animación es un residuo del estado anterior que no se limpia al salir y re-ingresar al canvas.

## Steps to Reproduce

1. Company Login > Sidebar: Boards > [Board]
2. En el canvas, agregar un nodo Timer
3. Configurar el Timer con un delay (ejemplo: 60 segundos)
4. Ejecutar el flow en modo Development (la animación del Timer se activa)
5. Salir de la vista de edición del canvas (navegar a otra sección)
6. Volver a ingresar al canvas del mismo Board
7. Observar que la animación del nodo Timer sigue ejecutándose

## Datos utilizados

- Rol: Company User con permiso `UPDATE_BOARD`
- Entorno: Staging
- Versión: v0.1.0

## Current Behavior

La animación del nodo Timer persiste visualmente al re-ingresar al canvas, incluso cuando el Timer no está en ejecución activa.

## Expected Behavior

Al re-ingresar al canvas, el estado visual de todos los nodos debería reflejar su estado real actual. Si el Timer no está en ejecución, no debería mostrar animación. El componente debería limpiar su estado visual al destruirse y restaurar el estado correcto al montarse.

## Impacto

- Puramente cosmético / visual
- Puede generar confusión sobre si el flow está en ejecución o no
- No afecta la funcionalidad

## Categorización

- 📊 Prioridad: **low** — cosmético, no afecta funcionalidad ni datos
- 🏷️ Tipo: **bug** — la animación debería reflejar el estado real del nodo
