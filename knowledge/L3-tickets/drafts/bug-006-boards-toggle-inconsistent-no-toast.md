# QA FOUND ISSUE ESCALATION REPORT — IOND

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | Boards |
| Path | Company > Boards > Active Flow |
| Versión | gateway-ion v0.1.0 · flow_binaries v0.1.0 · gateway v2.0.0 |

## Título

**Boards — Toggle de Active Flow queda inconsistente al fallar la petición, sin toast de error**

## Description of the validated/replicated problem

Al utilizar el toggle de activación/desactivación de un flow en la vista de Boards, si la petición HTTP falla (por ejemplo, por error de conexión de red), el toggle queda en un estado visual inconsistente respecto al estado real del flow en el backend. Adicionalmente, no se muestra ningún toast de error informando al usuario que la operación falló. Este mismo problema ocurre al intentar eliminar un flow cuando la petición falla.

## Steps to Reproduce

1. Company Login > Sidebar: Boards
2. Identificar un flow con toggle de estado (Active/Inactive)
3. Simular un error de conexión (desconectar red momentáneamente o throttle en DevTools)
4. Presionar el toggle de Active Flow
5. Observar que el toggle cambia visualmente pero la petición falla
6. Verificar que no se muestra toast de error
7. Reconectar la red → el toggle muestra un estado diferente al real del backend
8. Repetir con la acción de eliminar un flow bajo condiciones de error de red

## Datos utilizados

- Rol: Company User con permiso `UPDATE_BOARD`
- Entorno: Staging
- Versión: v0.1.0
- Cualquier flow existente en un Board

## Current Behavior

1. El toggle cambia visualmente de forma optimista sin confirmar el resultado de la petición
2. Si la petición falla, el toggle queda en el estado incorrecto
3. No se muestra toast de error para informar al usuario del fallo
4. El mismo comportamiento aplica a la eliminación de flows

## Expected Behavior

1. El toggle debería revertir a su estado anterior si la petición falla (rollback optimistic update)
2. Se debería mostrar un toast de error informando que la operación falló
3. En el caso de eliminación, si falla, se debería mostrar toast de error y el flow debería permanecer visible en la lista

## Impacto

- Afecta a todos los Company Users que gestionan el estado de sus flows
- Puede causar confusión sobre el estado real de un flow (activo vs inactivo)
- Afecta tanto el toggle de activación como la eliminación de flows

## Categorización

- 📊 Prioridad: **high** — afecta la integridad del estado visual vs real del flow, sin feedback de error al usuario
- 🏷️ Tipo: **bug** — el toggle debería revertir en caso de error y mostrar notificación
