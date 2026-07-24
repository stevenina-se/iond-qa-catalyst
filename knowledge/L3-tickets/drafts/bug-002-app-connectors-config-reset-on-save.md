# QA FOUND ISSUE ESCALATION REPORT — IOND

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | Connections (App Connectors) |
| Path | Company > App Connectors > [Connector] |
| Versión | gateway-ion v0.1.0 · flow_binaries v0.1.0 · gateway v2.0.0 |

## Título

**App Connectors — Configuración vaciada se restablece al guardar en lugar de persistir corchetes vacíos**

## Description of the validated/replicated problem

Al ingresar a la configuración de un App Connector y eliminar completamente el contenido de las secciones Parameters, Interface, Samples o Communication y presionar Save, la data se restablece a su estado anterior en lugar de persistir los valores vacíos (`{}`). Este comportamiento impide al usuario limpiar la configuración de webhooks, nodos y connections del connector. Se espera que al eliminar toda la configuración y guardar, se almacenen corchetes vacíos `{}` como indicador de configuración limpia.

## Steps to Reproduce

1. Company Login > Sidebar: App Connectors
2. Seleccionar un Connector existente con configuración previa
3. Navegar a cualquiera de las secciones: Parameters, Interface, Samples o Communication
4. Eliminar todo el contenido de la configuración (vaciar los campos por completo)
5. Presionar Button: "Save"
6. Recargar la vista o navegar fuera y volver a entrar al connector
7. Observar que la configuración eliminada se ha restablecido a su estado previo

## Datos utilizados

- Rol: Company User con permiso `UPDATE_APP`
- Entorno: Staging
- Versión: v0.1.0
- Connector con configuración previa en Parameters, Interface, Samples y/o Communication

## Current Behavior

Al eliminar la configuración completa de las secciones y presionar Save, la data se restablece a su estado anterior. Los cambios no se persisten y la configuración previa reaparece. Esto aplica a webhooks, nodos y connections.

## Expected Behavior

Al eliminar completamente la configuración de cualquier sección y guardar, el sistema debería almacenar corchetes vacíos `{}` como valor válido, permitiendo al usuario resetear la configuración del connector. La operación PUT debería aceptar objetos vacíos como payload válido.

## Impacto

- Afecta a Company Users que necesitan limpiar o resetear la configuración de sus connectors
- Bloquea el flujo de reconfiguración de connectors existentes
- Afecta webhooks, nodos y connections del connector

## Categorización

- 📊 Prioridad: **high** — impide reconfigurar connectors existentes, sin workaround simple
- 🏷️ Tipo: **bug** — comportamiento incorrecto; se espera que los valores vacíos se persistan
