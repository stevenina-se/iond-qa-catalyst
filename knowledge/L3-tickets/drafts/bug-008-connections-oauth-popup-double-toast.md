# QA FOUND ISSUE ESCALATION REPORT — IOND

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | Connections / Integrations |
| Path | Company > Connections > Reauthorize |
| Versión | gateway-ion v0.1.0 · flow_binaries v0.1.0 · gateway v2.0.0 |

## Título

**Connections — Ventana OAuth no se cierra automáticamente y emite doble toast de éxito en reautorización**

## Description of the validated/replicated problem

Al realizar el proceso de reautorización de una conexión con método de autenticación OAuth2, la ventana emergente (popup) de autorización no se cierra automáticamente después de completar el flujo de OAuth. Adicionalmente, se emiten dos toasts de éxito de reautorización en lugar de uno. Esto indica que el callback de OAuth se está procesando múltiples veces o que el evento de cierre del popup no se está manejando correctamente.

## Steps to Reproduce

1. Company Login > Sidebar: Connections
2. Seleccionar una conexión activa que utilice método de autenticación OAuth2
3. Presionar Button: "Reauthorize"
4. Completar el flujo de autorización OAuth2 en la ventana emergente
5. Observar que la ventana emergente NO se cierra automáticamente
6. Observar que se muestran DOS toasts de éxito de reautorización

## Datos utilizados

- Rol: Company User con permiso de gestión de connections
- Entorno: Staging
- Versión: v0.1.0
- Conexión con método de autenticación OAuth2 (Authorization Code)

## Current Behavior

1. La ventana emergente de OAuth permanece abierta después de completar la autorización
2. Se muestran 2 toasts de éxito en lugar de 1
3. El usuario debe cerrar manualmente la ventana emergente

## Expected Behavior

1. La ventana emergente debería cerrarse automáticamente al completar el callback de OAuth
2. Se debería mostrar un único toast de éxito confirmando la reautorización
3. El flujo debería ser transparente para el usuario sin requerir intervención manual

## Impacto

- Afecta a Company Users que reautorizan conexiones OAuth2
- No bloqueante (la reautorización funciona) pero genera confusión con el doble toast
- UX degradada por ventana que no se cierra automáticamente

## Categorización

- 📊 Prioridad: **normal** — la funcionalidad opera pero la UX es deficiente
- 🏷️ Tipo: **bug** — el popup debería cerrarse automáticamente y el toast debería emitirse una sola vez
