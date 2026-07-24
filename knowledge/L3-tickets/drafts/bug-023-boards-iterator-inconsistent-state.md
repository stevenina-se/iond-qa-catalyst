# QA FOUND ISSUE ESCALATION REPORT — IOND

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | Boards / Nodes |
| Path | Company > Boards > [Board] > Canvas > Iterator Node |
| Versión | gateway-ion v0.1.0 · flow_binaries v0.1.0 · gateway v2.0.0 |

## Título

**Boards — Nodo Iterator queda inconsistente al quitar contexto previo, imposibilita items manuales**

## Description of the validated/replicated problem

Al configurar un nodo Iterator con una función `map`, ejecutarlo, y luego quitarle el contexto previo (desconectar el nodo fuente), el Iterator queda en un estado inconsistente. No es posible añadir items de forma manual después de quitar el contexto. El nodo no se resetea correctamente y queda inutilizable hasta que se reconfigure desde cero.

## Steps to Reproduce

1. Company Login > Sidebar: Boards > [Board]
2. En el canvas, agregar un nodo Iterator
3. Conectar un nodo previo que proporcione un array como input
4. Configurar la función `map` del Iterator
5. Ejecutar el flow
6. Desconectar el nodo fuente (quitar el edge de entrada al Iterator)
7. Intentar añadir items de forma manual al Iterator
8. Observar que no es posible → el nodo queda en un estado inconsistente

## Datos utilizados

- Rol: Company User con permiso `UPDATE_BOARD`
- Entorno: Staging
- Versión: v0.1.0
- Iterator previamente ejecutado con contexto, luego desconectado

## Current Behavior

El nodo Iterator mantiene un estado residual de la ejecución previa después de quitar la conexión de entrada. No permite añadir items manualmente y queda inutilizable.

## Expected Behavior

Al desconectar el nodo fuente, el Iterator debería resetearse a un estado limpio que permita:
1. Añadir items manualmente
2. O reconectarse a un nuevo nodo fuente sin problemas
3. El estado residual de ejecuciones previas no debería bloquear la reconfiguración

## Impacto

- Afecta a usuarios que reconfiguran flows con nodos Iterator
- Workaround: eliminar el nodo y crear uno nuevo desde cero

## Categorización

- 📊 Prioridad: **normal** — workaround disponible (recrear el nodo), no bloquea completamente
- 🏷️ Tipo: **bug** — el nodo debería resetearse correctamente al quitar su contexto
