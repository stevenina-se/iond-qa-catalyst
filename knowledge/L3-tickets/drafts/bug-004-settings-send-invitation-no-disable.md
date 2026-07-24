# QA FOUND ISSUE ESCALATION REPORT — IOND

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | Accounts / Settings |
| Path | Company > Settings > Teams > + Invite Member |
| Versión | gateway-ion v0.1.0 · flow_binaries v0.1.0 · gateway v2.0.0 |

## Título

**Settings — Botón "Send Invitation" no se deshabilita durante la petición, permitiendo clicks múltiples**

## Description of the validated/replicated problem

Al utilizar la funcionalidad de invitación de miembros a un team, después de completar los campos (correo electrónico, fecha de caducidad, permisos) y presionar el botón "Send Invitation", este botón no se deshabilita ni muestra animación de carga mientras la petición está en proceso. Esto permite al usuario hacer click múltiples veces sobre el botón, emitiendo peticiones duplicadas que generan errores en las invocaciones subsecuentes.

## Steps to Reproduce

1. Company Login > Sidebar: Settings > Teams
2. Presionar Button: "+ Invite Member"
3. Completar el campo de correo electrónico con un email válido
4. Seleccionar una fecha de caducidad
5. Configurar permisos (añadir o quitar)
6. Presionar Button: "Send Invitation"
7. Inmediatamente hacer click nuevamente en el botón (antes de que la primera petición responda)
8. Observar en DevTools que se emiten múltiples peticiones y las subsecuentes retornan error

## Datos utilizados

- Rol: Company User con permisos de gestión de Teams
- Entorno: Staging
- Versión: v0.1.0
- Email de prueba válido
- Cualquier configuración de permisos

## Current Behavior

El botón "Send Invitation" permanece habilitado y sin indicador de carga durante toda la duración de la petición. Es posible clickearlo múltiples veces, generando peticiones duplicadas. Las peticiones adicionales fallan con error ya que la primera invitación se procesa correctamente.

## Expected Behavior

El botón "Send Invitation" debería:
1. Deshabilitarse inmediatamente al hacer el primer click
2. Mostrar un indicador de carga (spinner o animación) mientras la petición está en proceso
3. Rehabilitarse solo después de recibir la respuesta (éxito o error)
4. Alternativamente, implementar debounce para prevenir clicks múltiples

## Impacto

- Afecta a Company Users con permisos de gestión de teams
- No bloqueante (la primera invitación se envía correctamente)
- Genera confusión en el usuario al ver errores después de clicks adicionales

## Categorización

- 📊 Prioridad: **normal** — no bloquea el flujo pero genera confusión y errores innecesarios
- 🏷️ Tipo: **bug** — el botón debería deshabilitarse durante el procesamiento de la petición
