# QA FOUND ISSUE ESCALATION REPORT — IOND

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | Boards / Connections |
| Path | Company > Boards > [Board] > Canvas > App Node |
| Versión | gateway-ion v0.1.0 · flow_binaries v0.1.0 · gateway v2.0.0 |

## Título

**Boards — Input de nueva conexión en nodo de app abre menú de contexto innecesariamente**

## Description of the validated/replicated problem

Al configurar un nodo de app en el canvas que está conectado a cualquier otro nodo previo, al intentar crear una nueva conexión (credentials) haciendo click sobre el campo input, se abre el menú de contexto de forma innecesaria. El menú de contexto debería abrirse solo al hacer click derecho o al interactuar con el handle de contexto, no al hacer click en el input de nueva conexión.

## Steps to Reproduce

1. Company Login > Sidebar: Boards > [Board]
2. En el canvas, agregar un nodo de app (connector)
3. Conectar cualquier otro nodo previo al nodo de app
4. Abrir la configuración del nodo de app
5. En la sección de conexión/credenciales, intentar crear una nueva conexión
6. Hacer click sobre el campo input para seleccionar o crear la conexión
7. Observar que se abre el menú de contexto de forma innecesaria

## Datos utilizados

- Rol: Company User con permiso `UPDATE_BOARD`
- Entorno: Staging
- Versión: v0.1.0
- Nodo de app con conexión previa a otro nodo

## Current Behavior

Al hacer click en el input de nueva conexión del nodo de app, se abre el menú de contexto del nodo en lugar de permitir interactuar con el campo de conexión.

## Expected Behavior

El click en el input de nueva conexión debería:
1. Abrir el selector/creador de conexiones, no el menú de contexto
2. El menú de contexto solo debería abrirse con click derecho o en el handle designado
3. Los eventos de click deberían estar correctamente aislados entre el panel de configuración y el menú de contexto

## Impacto

- Afecta la UX de configuración de nodos de app
- Interfiere con el flujo de creación de nuevas conexiones
- No bloqueante pero frustrante para el usuario

## Categorización

- 📊 Prioridad: **normal** — no bloquea la funcionalidad pero interfiere con la UX de configuración
- 🏷️ Tipo: **bug** — el menú de contexto no debería activarse al interactuar con inputs de configuración
