# Acceptance Criteria Consolidados — 86e1y9k0f (Expiring token requirements for public apps)

> Generado durante Discovery — 2026-08-06
> Módulo principal: Integrations (Marketplace > Configured Channels > Shopify)
> Módulo secundario: Connections (Channel package — OAuth/token refresh)

---

## AC Originales (del ticket — "Expected Behavior")

Los AC originales fueron extraídos de la sección "Expected Behavior" del ticket. Se reconciliaron con los comentarios del Developer (Alex Chura) y la confirmación del QA Engineer.

---

## AC Consolidados Finales

### AC-1: Nuevas instalaciones con expiring tokens por defecto
**Dado que** un merchant instala Sfipedge en su tienda Shopify después de la implementación del cambio,
**cuando** completa el flujo OAuth de autorización,
**entonces** el sistema solicita **expiring offline access tokens** y el response incluye `access_token`, `expires_in` (3600s), `refresh_token`, y `refresh_token_expires_in` (7776000s = 90 días), todos almacenados correctamente en BD.

> **Fuente**: Descripción original del ticket (Expected Behavior #1) + Nota del Quick Prototype de Alex Chura [2026-08-04] — *"toda nueva integración soportará por defecto el nuevo Expiring token requerido por Shopify"*

### AC-2: Refresh automático de tokens antes de API calls
**Dado que** una integración Shopify tiene un `access_token` expirado (TTL: 1 hora),
**cuando** el sistema necesita hacer una API call a Shopify (REST o GraphQL),
**entonces** el sistema detecta la expiración, ejecuta el flujo de refresh usando el `refresh_token`, obtiene un nuevo `access_token` y `refresh_token`, los almacena en BD, y completa la API call sin interrupción.

> **Fuente**: Descripción original del ticket (Expected Behavior #2) — *"Antes de cualquier API call a Shopify, la app debe verificar si el access_token ha expirado y ejecutar el flujo de refresh"*

### AC-3: BD actualizada con campos de expiración
**Dado que** una integración Shopify obtiene tokens (nueva instalación o refresh),
**cuando** los tokens se almacenan en BD,
**entonces** los campos `expires_at`, `refresh_token`, y `refresh_token_expires_at` contienen valores correctos y actualizados.

> **Fuente**: Descripción original del ticket (Expected Behavior #3) — *"La tabla de tokens/sesiones debe contener los campos expires_at, refresh_token, y refresh_token_expires_at"*

### AC-4: Re-autorización manual para integraciones existentes
**Dado que** un merchant tiene una integración Shopify existente con token no-expirable,
**cuando** accede a la configuración de la integración (Marketplace > Configured Channels > Shopify),
**entonces** ve un mensaje de alerta indicando que Shopify requiere re-autorización, y un botón "Re-Authorize" que inicia un nuevo flujo OAuth para obtener expiring tokens.

> **Fuente**: Comentario Alex Chura [2026-08-04] UX Research — *"Es obligatorio realizar una nueva reautorización manual por parte del usuario"* + Quick Prototype — *"El mensaje ya implementado con el nuevo flujo de re-autorización estará ubicado en la primera tarjeta de configuraciones"*
> **Nota**: Shopify **no permite** migración automática de tokens (documentación oficial). La re-autorización manual es el **único mecanismo**. Confirmado por QA Engineer [2026-08-06].

### AC-5: Manejo de refresh token expirado
**Dado que** un merchant no ha usado su integración Shopify por más de 90 días (refresh token expirado),
**cuando** el sistema intenta refrescar el access token,
**entonces** el sistema detecta que el refresh token ha expirado, marca la integración como "requiere re-autorización", y presenta al merchant la alerta + botón "Re-Authorize" sin generar errors silenciosos ni crashes.

> **Fuente**: Descripción original del ticket (Expected Behavior #5) — *"Si el refresh_token expira (>90 días sin actividad), la app debe detectar este estado y solicitar al merchant que re-autorice la app"*

### AC-6: Sin interrupción de servicio post-re-autorización
**Dado que** un merchant completa la re-autorización exitosamente,
**cuando** se ejecutan las sincronizaciones automáticas (productos, órdenes, inventario, tracking),
**entonces** todas las sincronizaciones funcionan correctamente sin interrupción, usando los nuevos tokens expirables.

> **Fuente**: Descripción original del ticket (Expected Behavior #6)

### AC-7: Compatibilidad post-deadline (1 enero 2027)
**Dado que** la fecha es posterior al 1 de enero de 2027,
**cuando** Sfipedge realiza API calls a Shopify,
**entonces** ninguna API call usa tokens no-expirables. Todos los merchants que re-autorizaron funcionan correctamente; los que no re-autorizaron ven la alerta de re-autorización.

> **Fuente**: Descripción original del ticket (Expected Behavior #7)

### AC-8: Visibilidad condicional — solo integraciones existentes (NUEVO)
**Dado que** un merchant tiene una integración Shopify existente con tokens no-expirables,
**cuando** accede a la vista de configuración de la integración,
**entonces** el mensaje de alerta y el botón "Re-Authorize" son visibles.

**Dado que** un merchant instala una nueva integración Shopify (con expiring tokens por defecto),
**cuando** accede a la vista de configuración de la integración,
**entonces** el mensaje de alerta y el botón "Re-Authorize" NO son visibles.

> **Fuente**: Comentario Alex Chura [2026-08-04] Quick Prototype — *"El mensaje de alerta y el botón de reautorización serán únicamente visibles para integraciones ya existentes"*

### AC-9: Ubicación de la alerta en la UI (NUEVO)
**Dado que** una integración existente necesita re-autorización,
**cuando** el merchant ve la vista de configuración de Shopify,
**entonces** el mensaje de alerta y el botón "Re-Authorize" están ubicados en la **primera tarjeta de configuraciones** (Settings card).

> **Fuente**: Comentario Alex Chura [2026-08-04] Quick Prototype — *"El mensaje ya implementado con el nuevo flujo de re-autorización estará ubicado en la primera tarjeta de configuraciones de la integración"*

---

## AC Propuestos (sugerencias para acordar con el equipo)

> Estos AC emergieron del análisis de riesgo y edge cases. Se presentan como sugerencias para discusión.

### AC-P1 (Propuesto): Re-autorización exitosa actualiza la UI
**Dado que** un merchant completa la re-autorización exitosamente (OAuth flow completo),
**cuando** regresa a la vista de configuración de Shopify,
**entonces** el mensaje de alerta desaparece y/o se muestra confirmación de re-autorización exitosa.

> **Justificación**: Edge case EC-10 del risk-triage. Si la alerta persiste después de re-autorizar, el merchant queda confundido.

### AC-P2 (Propuesto): Re-autorización fallida/interrumpida
**Dado que** un merchant inicia la re-autorización pero cierra el popup de Shopify o la autorización falla,
**cuando** regresa a la vista de configuración,
**entonces** el token anterior sigue funcionando (no se invalidó), la alerta de re-autorización sigue visible, y se puede reintentar sin errores.

> **Justificación**: Edge case EC-6 del risk-triage. Proteger contra estados inconsistentes si el OAuth flow se interrumpe.

### AC-P3 (Propuesto): Background jobs con token expirado ejecutan refresh
**Dado que** un background job de sincronización (Import Orders, Get Products, Sync Inventory, Update Tracking) detecta que el access token expiró,
**cuando** intenta ejecutar la API call a Shopify,
**entonces** ejecuta el refresh automáticamente, obtiene un nuevo token, reintenta la API call, y completa la sincronización sin intervención humana.

> **Justificación**: R-003 del risk-triage. Los background jobs corren desatendidos — deben auto-recuperarse.

---

## AC Diferidos / Fuera de Scope

| AC | Razón | Para cuándo |
|----|-------|-------------|
| Notificación por email cuando se acerca el deadline sin re-autorización | Scope futuro — el ticket actual se enfoca en la mecánica de re-autorización y refresh | Futuro ticket si se decide |
| Revocación explícita del token viejo en Shopify después de re-autorizar | Depende de la API de Shopify — verificar si es necesario vs. dejar que expire naturalmente | Pregunta abierta para Developer |
| Soporte genérico para otros connectors OAuth (no solo Shopify) | El prototipo menciona "todas las integraciones antiguas" — requiere clarificación de scope | Pregunta abierta para Developer (pregunta #10 del risk-triage) |

---

## Transformación AC → Casos de Test

| AC | Caso de test (Happy Path) | Casos Edge | Caso Negativo |
|----|--------------------------|------------|---------------|
| AC-1 | Nueva instalación Shopify → OAuth → tokens expirables almacenados en BD | Instalación con scope limitado de Shopify | Instalación con credenciales inválidas |
| AC-2 | Token expirado → refresh automático → API call exitosa | Refresh durante ejecución de flow multi-nodo | Refresh token también expirado (>90 días) |
| AC-3 | Verificar campos `expires_at`, `refresh_token`, `refresh_token_expires_at` en BD post-instalación y post-refresh | Valores después de múltiples refreshes sucesivos | Campos con valores null/inválidos |
| AC-4 | Merchant con token viejo ve alerta + botón → click Re-Authorize → OAuth exitoso | Merchant con múltiples tiendas Shopify | Merchant sin permisos para editar integración |
| AC-5 | Refresh token expirado → sistema detecta → muestra alerta re-autorización | Token expirado justo durante un sync en ejecución | Sistema no detecta y falla silenciosamente |
| AC-6 | Post-re-autorización → Execute Get Orders → éxito, Execute Get Products → éxito | Sync mientras se está re-autorizando | Re-autorización con scope reducido |
| AC-7 | Post-deadline → API calls con expiring tokens → éxito | Merchant que nunca re-autorizó → error manejado | Token viejo post-deadline → error response |
| AC-8 | Integración nueva → NO alerta; integración existente → SÍ alerta | Integración existente que ya fue re-autorizada → NO alerta | — |
| AC-9 | Alerta visible en primera tarjeta Settings de la integración Shopify | Responsive / mobile view | — |
| AC-P1 | Post-re-autorización → alerta desaparece | Recargar página post-re-autorización → alerta no reaparece | — |
| AC-P2 | Iniciar OAuth → cancelar → token viejo funciona, alerta persiste | Múltiples intentos fallidos seguidos | — |
| AC-P3 | Background job → token expirado → refresh → retry → sync exitoso | Múltiples jobs concurrentes refrescan mismo token | Refresh falla (Shopify down) → log de error |
