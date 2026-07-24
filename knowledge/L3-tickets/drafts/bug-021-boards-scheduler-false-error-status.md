# QA FOUND ISSUE ESCALATION REPORT — IOND

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | Boards / Executions |
| Path | Company > Boards > [Board] > Canvas > Scheduler Node |
| Versión | gateway-ion v0.1.0 · flow_binaries v0.1.0 · gateway v2.0.0 |

## Título

**Boards — Scheduler ejecuta flow correctamente pero status queda en "error"**

## Description of the validated/replicated problem

Al configurar un nodo Scheduler con una ejecución periódica (por ejemplo, cada 1 minuto), guardar y activar el flow, se observa que tras la ejecución del flow el status de la ejecución queda marcado como "error". Sin embargo, la ejecución se realizó de forma correcta y los datos fluyeron normalmente por todos los nodos. El status es inconsistente con el resultado real de la ejecución.

## Steps to Reproduce

1. Company Login > Sidebar: Boards > [Board]
2. En el canvas, agregar un nodo Schedule (Trigger programado)
3. Configurar el schedule con ejecución periódica (ejemplo: cada 1 minuto)
4. Agregar nodos adicionales conectados al trigger
5. Guardar el flow (commit)
6. Activar el flow (toggle Active)
7. Esperar a que se ejecute al menos una vez según el schedule
8. Navegar a Execution History > verificar el status de la ejecución
9. Observar que el status es "error" a pesar de que la ejecución se completó correctamente

## Datos utilizados

- Rol: Company User con permiso `UPDATE_BOARD`
- Entorno: Staging
- Versión: v0.1.0
- Schedule: ejecución periódica cada 1 minuto
- Cualquier flow funcional con nodo Schedule

## Current Behavior

El flow se ejecuta correctamente vía el Scheduler pero el status de la ejecución se registra como "error" en el historial. La ejecución fue exitosa pero el status es incorrecto.

## Expected Behavior

Si la ejecución del flow se completó correctamente (todos los nodos ejecutaron sin error), el status de la ejecución debería ser "completed", no "error". El status debería reflejar fielmente el resultado real de la ejecución.

## Impacto

- Genera confusión sobre el estado real de los flows programados
- Puede activar alertas o métricas de error incorrectas
- Dificulta el monitoreo de flows en producción
- Relacionado con Bug #7 (inconsistencia de estados en ejecuciones)

## Categorización

- 📊 Prioridad: **high** — status incorrecto en funcionalidad core de ejecución programada, afecta monitoreo
- 🏷️ Tipo: **bug** — el status debería reflejar el resultado real de la ejecución
