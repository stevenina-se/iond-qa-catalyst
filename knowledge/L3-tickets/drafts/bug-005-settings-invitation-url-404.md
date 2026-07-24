# QA FOUND ISSUE ESCALATION REPORT — IOND

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | Accounts / Settings / Auth |
| Path | Company > Settings > Teams > Invite Member > CTA de invitación |
| Versión | gateway-ion v0.1.0 · flow_binaries v0.1.0 · gateway v2.0.0 |

## Título

**Settings — URL de invitación de nuevo usuario retorna Error 404, bloqueando flujo de aceptación**

## Description of the validated/replicated problem

Al presionar el botón CTA de la invitación de nuevo usuario que fue enviada, el sistema redirige a una URL de invitación que retorna Error 404. Por ejemplo, la URL `https://staging-gateway.ionflow.io/invitation?intent_id=176d0005-1e75-4517-88be-6d0d0e58d1c5` no es encontrada. Esto bloquea completamente el flujo de aceptación de invitaciones, haciendo imposible que nuevos usuarios se unan al sistema a través del mecanismo de invitación.

## Steps to Reproduce

1. Company Login > Sidebar: Settings > Teams > + Invite Member
2. Enviar una invitación con datos válidos
3. Acceder a la invitación enviada (email o lista de invitaciones pendientes)
4. Presionar sobre el botón CTA de la invitación
5. Observar que la URL de destino (ejemplo: `https://staging-gateway.ionflow.io/invitation?intent_id={uuid}`) retorna Error 404

## Datos utilizados

- Rol: Nuevo usuario invitado / Company User que envía la invitación
- Entorno: Staging (`staging-gateway.ionflow.io`)
- Versión: v0.1.0 / gateway v2.0.0
- URL de ejemplo: `https://staging-gateway.ionflow.io/invitation?intent_id=176d0005-1e75-4517-88be-6d0d0e58d1c5`

## Current Behavior

La URL de invitación (`/invitation?intent_id={uuid}`) retorna HTTP 404. El flujo de aceptación de invitación está completamente roto.

## Expected Behavior

La URL de invitación debería resolver a una vista donde el nuevo usuario pueda aceptar la invitación, completar su registro y unirse a la Company. La ruta `/invitation` debería estar registrada en el gateway y manejar correctamente el parámetro `intent_id`.

## Impacto

- **Bloqueante crítico**: ningún nuevo usuario puede aceptar invitaciones
- Afecta el flujo completo de onboarding de nuevos miembros al sistema
- Impacto en todas las Companies que intentan invitar nuevos usuarios

## Categorización

- 📊 Prioridad: **urgent** — funcionalidad core completamente rota, bloquea onboarding de usuarios
- 🏷️ Tipo: **bug** — la ruta de invitación debería existir y funcionar correctamente
