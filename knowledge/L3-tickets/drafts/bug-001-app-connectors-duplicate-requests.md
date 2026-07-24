# QA FOUND ISSUE ESCALATION REPORT — IOND

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | Connections (App Connectors) |
| Path | Company > App Connectors > [Connector] |
| Versión | gateway-ion v0.1.0 · flow_binaries v0.1.0 · gateway v2.0.0 |

## Título

**App Connectors — Peticiones HTTP duplicadas al cargar configuración del connector**

## Description of the validated/replicated problem

Al ingresar a la vista de configuración de un App Connector, se observa en los DevTools del navegador que se disparan peticiones HTTP duplicadas: 2 peticiones para la obtención de `app-webhooks` y 3 peticiones para la obtención de `app-connections`. Este comportamiento se replica consistentemente al crear nodos, crear connections, o al recargar la vista. Las peticiones redundantes generan carga innecesaria al backend y potenciales condiciones de carrera en el estado del frontend.

## Steps to Reproduce

1. Company Login > Sidebar: App Connectors
2. Seleccionar cualquier Connector existente de la lista
3. Abrir DevTools del navegador (F12) > Tab: Network
4. Observar las peticiones realizadas al cargar la configuración
5. Verificar que se realizan **2 peticiones** a `GET /1.0/tenants/{tenant}/app-webhooks` y **3 peticiones** a `GET /1.0/tenants/{tenant}/app-connections`
6. Repetir navegando a crear un nodo o connection dentro del connector → mismo comportamiento
7. Recargar la vista (F5) → mismo comportamiento

## Datos utilizados

- Rol: Company User con permiso `READ_APP`
- Entorno: Staging
- Versión: v0.1.0
- Cualquier App Connector existente con webhooks y connections configurados

## Current Behavior

Se realizan múltiples peticiones redundantes al mismo endpoint al cargar la configuración del connector. `app-webhooks` se llama 2 veces y `app-connections` se llama 3 veces. El comportamiento se repite al crear nodos, connections o al recargar la vista.

## Expected Behavior

Cada endpoint debería ser llamado una única vez al cargar la vista de configuración del connector. Las peticiones deben consolidarse en una sola llamada por recurso, utilizando el sistema de cache de queries (TanStack Query) para evitar refetches innecesarios.

## Impacto

- Afecta a todos los Company Users que editan App Connectors
- No bloqueante pero genera carga innecesaria al backend y potencial degradación de performance
- Posibles condiciones de carrera si las respuestas duplicadas se procesan en orden inconsistente

## Categorización

- 📊 Prioridad: **normal** — no bloquea funcionalidad pero impacta performance y genera carga innecesaria al backend
- 🏷️ Tipo: **bug** — comportamiento incorrecto; las peticiones deberían realizarse una sola vez
