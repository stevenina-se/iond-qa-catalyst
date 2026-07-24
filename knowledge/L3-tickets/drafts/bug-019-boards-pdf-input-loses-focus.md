# QA FOUND ISSUE ESCALATION REPORT — IOND

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | Boards / PDF Templates |
| Path | Company > Boards > [Board] > PDF Template Node |
| Versión | gateway-ion v0.1.0 · flow_binaries v0.1.0 · gateway v2.0.0 |

## Título

**Boards — Input de mapeo del nodo PDF se cierra inmediatamente al hacer click cuando tiene nodo previo conectado**

## Description of the validated/replicated problem

Al configurar un nodo PDF Template en el canvas, cuando este nodo está conectado previamente a cualquier otro nodo y se presiona "Add Item" para llenar datos del mapeo, al hacer click en el campo input este se cierra inmediatamente sin permitir la escritura. El usuario no puede persistir el foco del input para escribir. Este problema ocurre únicamente cuando el nodo PDF tiene una conexión previa con otro nodo; sin conexión previa, el input funciona correctamente.

## Steps to Reproduce

1. Company Login > Sidebar: Boards > [Board existente]
2. En el canvas, agregar cualquier nodo (por ejemplo, un Form)
3. Conectar ese nodo al nodo PDF Template (source → PDF)
4. Abrir la configuración del nodo PDF Template
5. Seleccionar un PDF template existente
6. Presionar Button: "Add Item" para agregar un campo de mapeo
7. Hacer click en el campo input del item agregado
8. Observar que el input se cierra/pierde foco inmediatamente
9. Verificar que sin la conexión previa, el input funciona normalmente

## Datos utilizados

- Rol: Company User con permiso `UPDATE_BOARD` + `READ_PDF_TEMPLATE`
- Entorno: Staging
- Versión: v0.1.0
- Board con nodo PDF conectado a cualquier otro nodo

## Current Behavior

Al hacer click en el input del mapeo de datos, el campo se cierra/pierde foco inmediatamente. No es posible escribir en el campo. Solo ocurre cuando el nodo PDF está conectado a otro nodo previo.

## Expected Behavior

El input debería mantener el foco al hacer click, permitiendo al usuario escribir y persistir la entrada de datos. El comportamiento no debería verse afectado por la existencia de conexiones previas al nodo.

## Impacto

- **Bloqueante** para la configuración de mapeo de datos del nodo PDF cuando tiene conexiones previas
- Afecta directamente el flujo de trabajo normal (los nodos PDF casi siempre tienen conexiones previas)
- Sin workaround viable en el flujo normal de uso

## Categorización

- 📊 Prioridad: **high** — bloquea configuración de nodo PDF en su caso de uso más común
- 🏷️ Tipo: **bug** — el input debería mantener foco independientemente de las conexiones del nodo
