# QA FOUND ISSUE ESCALATION REPORT — IOND

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | Boards |
| Path | Company > Boards > New Board |
| Versión | gateway-ion v0.1.0 · flow_binaries v0.1.0 · gateway v2.0.0 |

## Título

**Boards — Board sugiere cambios sin guardar tras commit exitoso al re-ingresar a la vista**

## Description of the validated/replicated problem

Al crear un nuevo Board, realizar un commit exitoso, salir de la vista de boards y volver a ingresar, el Board muestra una alerta indicando que existen cambios sin guardar. Esta alerta es incorrecta ya que el commit fue exitoso y no se realizaron cambios adicionales. La alerta permanece visible durante una ventana de tiempo y luego desaparece automáticamente.

## Steps to Reproduce

1. Company Login > Sidebar: Boards
2. Crear un nuevo Board o editar uno existente
3. Realizar cambios en el canvas (agregar/editar nodos)
4. Realizar un commit exitoso
5. Salir de la vista de boards (navegar a otra sección)
6. Volver a ingresar a la vista de Boards
7. Observar la alerta de "cambios sin guardar"
8. Esperar → la alerta desaparece después de un tiempo

## Datos utilizados

- Rol: Company User con permiso `UPDATE_BOARD`
- Entorno: Staging
- Versión: v0.1.0
- Board con commit exitoso previo

## Current Behavior

El Board muestra incorrectamente una alerta de cambios sin guardar después de un commit exitoso, al re-ingresar a la vista. La alerta es temporal y desaparece después de cierto tiempo.

## Expected Behavior

Después de un commit exitoso, al re-ingresar a la vista del Board no debería mostrarse ninguna alerta de cambios sin guardar. El estado del Board debería reflejar que está sincronizado con el último commit.

## Impacto

- Genera confusión en los usuarios sobre el estado de sus cambios
- No bloqueante (la alerta desaparece sola)
- Puede llevar a commits innecesarios si el usuario confía en la alerta falsa

## Categorización

- 📊 Prioridad: **normal** — no bloquea funcionalidad pero genera confusión sobre el estado del board
- 🏷️ Tipo: **bug** — la alerta de cambios sin guardar es incorrecta tras un commit exitoso
