# QA FOUND ISSUE ESCALATION REPORT — IOND

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | Boards / PDF Templates |
| Path | Company > Boards > [Board] > PDF Template Node |
| Versión | gateway-ion v0.1.0 · flow_binaries v0.1.0 · gateway v2.0.0 |

## Título

**Boards — Nodo PDF no habilita mapeo de datos hasta abrir y guardar modal de edición**

## Description of the validated/replicated problem

Al abrir la configuración del nodo PDF en el canvas de un Board y seleccionar un PDF template, la opción para realizar el mapeo de datos no se habilita automáticamente. Para poder acceder al mapeo, es necesario abrir manualmente el modal de edición del template y presionar guardar, sin necesidad de realizar cambios. Solo después de este paso adicional innecesario se habilita la funcionalidad de mapeo de datos.

## Steps to Reproduce

1. Company Login > Sidebar: Boards > [Board existente]
2. En el canvas, seleccionar o agregar un nodo de tipo PDF Template
3. Abrir la configuración del nodo PDF (click en el nodo > panel de configuración)
4. Seleccionar un PDF template existente del dropdown
5. Observar que la opción de mapeo de datos NO está habilitada
6. Abrir el modal de edición del template seleccionado
7. Sin realizar cambios, presionar Button: "Guardar"
8. Cerrar el modal → observar que ahora SÍ se habilita la opción de mapeo de datos

## Datos utilizados

- Rol: Company User con permiso `UPDATE_BOARD` + `READ_PDF_TEMPLATE`
- Entorno: Staging
- Versión: v0.1.0
- Board con nodo PDF Template + al menos un template existente

## Current Behavior

La opción de mapeo de datos no se habilita al seleccionar un PDF template. Requiere el paso adicional de abrir-guardar el modal de edición.

## Expected Behavior

Al seleccionar un PDF template en la configuración del nodo, la opción de mapeo de datos debería habilitarse automáticamente sin requerir pasos adicionales. La metadata del template debería cargarse al momento de la selección.

## Impacto

- Afecta a todos los usuarios que configuran nodos PDF en sus flows
- No bloqueante (tiene workaround: abrir y guardar el modal) pero degrada la UX significativamente
- Paso innecesario que confunde al usuario

## Categorización

- 📊 Prioridad: **high** — afecta flujo principal de configuración de nodos PDF, workaround no intuitivo
- 🏷️ Tipo: **bug** — la selección del template debería habilitar automáticamente el mapeo
