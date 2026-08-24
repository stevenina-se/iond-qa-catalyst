# Risk Triage — 86e1y9k0f (Expiring token requirements for public apps)

## Resumen
- **Módulo principal**: Integrations (Marketplace > Configured Channels > Shopify)
- **Módulos impactados**: Connections (Channel package — OAuth/token refresh), Boards (flows con nodos Shopify)
- **Riesgo general**: 🔴 Crítico
- **Total edge cases identificados**: 12
- **Total preguntas para Developer**: 10
- **Contexto de ClickUp**: 2 comentarios leídos (UX Research + Quick Prototype de Alex Chura), divergencia significativa detectada

---

## Reconciliación de AC (Descripción vs Comentarios)

> ⚠️ **DIVERGENCIA DETECTADA** entre la descripción original y las decisiones del Developer.

| # | AC Original (Descripción) | Decisión en Comentarios | AC Reconciliado | Fuente |
|---|--------------------------|------------------------|-----------------|--------|
| 1 | **Nuevas instalaciones**: OAuth solicita expiring tokens (`access_token`, `expires_in`, `refresh_token`, `refresh_token_expires_in`) | Sin cambio en comentarios | AC-1: Las nuevas instalaciones de Shopify soportan expiring tokens por defecto | Descripción + Nota del prototype |
| 2 | **Refresh automático**: Antes de cada API call, verificar si token expiró y ejecutar refresh | Sin discusión explícita en comentarios | AC-2: El sistema implementa refresh automático de tokens antes de API calls a Shopify | Descripción (pendiente confirmar) |
| 3 | **BD actualizada**: Campos `expires_at`, `refresh_token`, `refresh_token_expires_at` | Sin discusión explícita | AC-3: La BD almacena los campos de expiración y refresh token | Descripción (pendiente confirmar) |
| 4 | **Migración automática**: Token exchange automático para merchants existentes, token viejo revocado | ✅ **RESUELTO**: Shopify **no permite** migración automática de tokens (documentación oficial). Re-autorización manual es el ÚNICO mecanismo posible. La descripción original era imprecisa. | AC-4 CORREGIDO: Los merchants con integraciones existentes ven un mensaje de alerta y un botón "Re-Authorize" que inicia un nuevo flujo OAuth para obtener expiring tokens. No existe token exchange automático. | Comentario Alex Chura [2026-08-04] + Confirmación QA Engineer [2026-08-06] — Documentación Shopify |
| 5 | **Manejo de refresh token expirado**: Si `refresh_token` expira (>90 días), detectar y solicitar re-autorización sin crashes | Sin discusión explícita | AC-5: Si el refresh token expira, el sistema detecta el estado y solicita re-autorización | Descripción (pendiente confirmar) |
| 6 | **Sin interrupción de servicio**: Syncs (productos, órdenes, inventario) continúan post-migración | Sin discusión explícita | AC-6: Las sincronizaciones funcionan sin interrupción después de re-autorizar | Descripción |
| 7 | **Compatibilidad post-deadline**: Después del 1/1/2027, ningún API call usa tokens no-expirables | Sin discusión explícita | AC-7: No quedan tokens legacy en producción post-deadline | Descripción |
| — | (no existía) | Developer: Alerta + botón solo visibles para **integraciones existentes** | AC-8 NUEVO: El mensaje de alerta y botón "Re-Authorize" solo son visibles para integraciones ya existentes con tokens no-expirables | Comentario Alex Chura [2026-08-04] Quick Prototype |
| — | (no existía) | Developer: Ubicación en primera tarjeta de configuración | AC-9 NUEVO: El mensaje de alerta se ubica en la primera tarjeta de configuraciones (Settings) de la integración | Comentario Alex Chura [2026-08-04] Quick Prototype |

### ~~Divergencia Principal~~ — RESUELTA ✅

> **AC-4: Migración automática vs Re-autorización manual**
> - La descripción original sugería token exchange automático, pero la **documentación oficial de Shopify confirma que NO es posible**.
> - El Developer correctamente implementó **re-autorización manual** del usuario (botón "Re-Authorize") — es el **único mecanismo posible**.
> - **Implicación QA**: El merchant DEBE re-autorizar manualmente. Si no lo hace antes del deadline (1/1/2027), la integración dejará de funcionar.
> - **Confirmado por**: QA Engineer [2026-08-06]

---

## Análisis de Lógica de Negocio

| Pregunta | Análisis |
|----------|----------|
| ¿El feature respeta las reglas multi-tenant (company)? | ⚠️ **VERIFICAR**: Los tokens de Shopify están asociados a cada company/integration. La re-autorización debe actualizar tokens solo de la company que re-autoriza, sin afectar otras companies. |
| ¿Afecta la ejecución de flows/nodos? | 🔴 **SÍ — CRÍTICO**: Los nodos de Shopify en flows activos (Get Orders, Get Products, Sync Inventory, Update Tracking) usan tokens para API calls. Si el token expira sin refresh, los flows fallan silenciosamente o con error. |
| ¿Hay impacto en connectors globales vs company? | ⚠️ **VERIFICAR**: Shopify como connector es probablemente global, pero las integrations (tokens) son per-company. El mecanismo de refresh debe funcionar a nivel de integration, no de connector. |
| ¿Se tocan datos de ejecución (SQLite) o datos persistentes (PostgreSQL)? | 🟠 **PostgreSQL**: Se necesitan nuevos campos en la tabla de tokens/sesiones. SQLite (ejecuciones) no debería verse afectado directamente, pero los logs de ejecución de nodos Shopify reflejarán errores si los tokens fallan. |
| ¿Hay impacto en el sistema de permisos por usuario/company? | 🟡 **MÍNIMO**: El botón "Re-Authorize" probablemente requiere permiso de edición de integración. Verificar que solo usuarios con `update-integration` o equivalente puedan re-autorizar. |
| ¿El feature puede romper flujos de e-commerce existentes? | 🔴 **SÍ — CRÍTICO**: Si la migración de tokens tiene un bug, o si el refresh automático no funciona correctamente, TODOS los flows con nodos Shopify dejan de funcionar. Esto afecta órdenes, productos e inventario en producción. |

---

## Análisis de Impacto por Módulo

| Área | Impacto | Riesgo |
|------|---------|--------|
| **Frontend (gateway-ion)** | Nuevo componente de alerta + botón "Re-Authorize" en la vista de configuración de Shopify (Marketplace > Configured Channels). Lógica condicional: solo mostrar para integraciones existentes con tokens no-expirables. | 🟠 Alto |
| **API — OAuth flow (gateway / flow_binaries)** | Modificación del flujo OAuth de Shopify para solicitar expiring tokens. Nuevo endpoint o modificación del callback para manejar `expires_in`, `refresh_token`, `refresh_token_expires_in`. | 🔴 Crítico |
| **API — Token refresh (flow_binaries channel package)** | Nueva lógica de refresh automático en `packages/channel/services/refresh.go`. Antes de cada API call a Shopify, verificar expiración y refrescar si necesario. | 🔴 Crítico |
| **BD PostgreSQL** | Nuevos campos: `expires_at`, `refresh_token`, `refresh_token_expires_at` en la tabla de tokens/sesiones/connections. Migración de datos existentes. | 🟠 Alto |
| **Background jobs / Syncs** | Los jobs de sincronización (órdenes, productos, inventario) deben validar token antes de ejecutar. Si token expirado → refresh → retry. | 🔴 Crítico |
| **Canvas (nodos Shopify)** | Sin cambio directo, pero los nodos Shopify en flows dependen de tokens válidos. | 🟡 Medio (impacto indirecto) |
| **Otros módulos — Boards** | Flows activos con nodos Shopify pueden fallar si el refresh no funciona. | 🟠 Alto (impacto indirecto) |

---

## Edge Cases Identificados

| # | Edge Case | Riesgo | Área |
|---|-----------|--------|------|
| EC-1 | **Token refresh durante ejecución de flow**: Un flow está ejecutándose cuando el token expira a mitad de la ejecución. ¿Se refresca mid-flow o falla? | 🔴 | Token refresh + Boards |
| EC-2 | **Requests concurrentes de refresh**: Múltiples background jobs intentan refrescar el mismo token simultáneamente. ¿Hay race condition? ¿Se usa locking? | 🔴 | Token refresh |
| EC-3 | **Refresh token expirado (>90 días sin actividad)**: Un merchant no usa su integración por más de 90 días. El refresh token expira. ¿El sistema detecta esto y muestra la alerta de re-autorización? ¿O falla silenciosamente? | 🔴 | Token lifecycle |
| EC-4 | **Re-autorización con OAuth scope cambiado**: Si Shopify cambia los scopes disponibles entre la autorización original y la re-autorización, ¿se manejan correctamente? | 🟠 | OAuth flow |
| EC-5 | **Múltiples integraciones Shopify por company**: Si una company tiene más de una tienda Shopify configurada, ¿cada una se re-autoriza independientemente? ¿La UI muestra la alerta para cada una? | 🟠 | UI + Multi-tenant |
| EC-6 | **Re-autorización parcial / fallida**: El merchant inicia la re-autorización pero cierra el popup de Shopify antes de completar. ¿El token viejo sigue funcionando? ¿El estado de la integración queda inconsistente? | 🟠 | OAuth flow + UI |
| EC-7 | **Token expirado pero refresh exitoso durante sync**: Un background job de sync detecta token expirado, ejecuta refresh, y reintenta. ¿El sync completo se ejecuta o solo el request actual? | 🟠 | Background jobs |
| EC-8 | **Visibilidad de la alerta por rol de usuario**: ¿Un usuario sin permisos de edición de integración ve la alerta? ¿Ve el botón "Re-Authorize" deshabilitado o no lo ve? | 🟡 | UI + Permisos |
| EC-9 | **Nuevas instalaciones post-cambio**: Una company instala Shopify después del cambio. ¿El flujo OAuth ya solicita expiring tokens? ¿Se almacenan correctamente los campos de expiración? | 🟠 | OAuth flow + BD |
| EC-10 | **Estado visual de la integración post-re-autorización**: Después de re-autorizar exitosamente, ¿la alerta desaparece? ¿Se muestra algún mensaje de éxito? ¿La UI se actualiza sin reload? | 🟡 | UI |
| EC-11 | **Rollback / token viejo post-re-autorización**: Después de obtener el nuevo expiring token, ¿el token viejo no-expirable queda revocado en Shopify? ¿Se puede volver atrás? | 🟠 | Token lifecycle |
| EC-12 | **Deadline proximity sin re-autorización**: Si el merchant no ha re-autorizado y se acerca el deadline (1/1/2027), ¿hay algún mecanismo de urgencia (email, notificación más prominente)? | 🟡 | UX / Scope futuro |

---

## Preguntas para el Developer

### [LÓGICA DE NEGOCIO / TOKEN LIFECYCLE]

1. ~~**¿La re-autorización manual es el ÚNICO mecanismo de migración?**~~ ✅ **RESPONDIDA**: Sí, la re-autorización manual es el único mecanismo. La documentación de Shopify confirma que el token exchange automático **no es posible**. La descripción original del ticket era imprecisa.

2. **¿Qué sucede con el token no-expirable después de una re-autorización exitosa?** ¿Se revoca explícitamente en Shopify o simplemente se deja de usar? Si no se revoca, ¿podría causar confusión o problemas de seguridad?

3. **¿Cómo detecta el sistema que una integración tiene un token no-expirable vs uno expirable?** ¿Es por la presencia/ausencia del campo `expires_at` en BD? ¿O hay otro mecanismo?

### [TOKEN REFRESH / BACKGROUND JOBS]

4. **¿Cómo se maneja el refresh automático cuando múltiples background jobs necesitan el token simultáneamente?** ¿Hay un mecanismo de locking para evitar race conditions con refreshes concurrentes?

5. **¿Qué sucede si un flow está ejecutándose y el token expira a mitad de ejecución?** ¿El nodo actual refresca y reintenta, o falla todo el flow?

6. **¿El `isRefreshed` flag del channel package es suficiente para manejar el nuevo flujo, o se necesita lógica adicional?** ¿Se reutiliza `packages/channel/services/refresh.go` o se creó lógica nueva?

### [UI / FRONTEND]

7. **¿El botón "Re-Authorize" está disponible solo en la vista de Marketplace > Configured Channels > Shopify, o también desde otras vistas como el detalle de la integración?**

8. **¿Qué pasa si un usuario sin permisos de edición ve la alerta?** ¿Ve el botón deshabilitado, ve solo el mensaje, o no ve nada?

### [BD / MIGRACIÓN]

9. **¿Se agrega una migración de BD para los nuevos campos (`expires_at`, `refresh_token`, `refresh_token_expires_at`)?** ¿Estos campos son nullable (para compatibilidad con tokens existentes)?

### [INTEGRACIÓN / SCOPE]

10. **¿Este cambio aplica SOLO a Shopify o se diseñó para ser genérico para cualquier connector que requiera token expirable en el futuro?** El prototipo muestra "para todas las integraciones antiguas" — ¿eso significa que otros connectors también mostrarán la alerta?

---

## Tabla de Riesgos (Priorización)

| ID | Área | Riesgo | Descripción | Prioridad de testing | Justificación |
|----|------|--------|-------------|---------------------|---------------|
| R-001 | Token refresh automático | 🔴 Crítico | La lógica de refresh automático es el corazón del cambio. Si falla, todos los flows con nodos Shopify dejan de funcionar después de 1 hora (TTL del token). | 1 (testear primero) | Impacto directo en producción: syncs de órdenes, productos, inventario |
| R-002 | OAuth re-autorización | 🔴 Crítico | El nuevo flujo OAuth debe obtener correctamente expiring tokens y almacenarlos en BD. Si falla, los merchants no pueden migrar. | 2 | Sin esto, la migración es imposible |
| R-003 | Background jobs con token expirado | 🔴 Crítico | Los jobs de sync deben validar token, refrescar si expirado, y reintentar. Race conditions posibles con refreshes concurrentes. | 3 | Los syncs corren desatendidos — errores silenciosos = datos incorrectos |
| R-004 | Migración de BD | 🟠 Alto | Nuevos campos en la tabla de tokens. Migración debe ser backward-compatible (nullable). | 4 | Si la migración falla, se rompe la BD |
| R-005 | UI alerta + botón Re-Authorize | 🟠 Alto | Visibilidad condicional (solo integraciones existentes con tokens no-expirables). Botón debe funcionar correctamente. | 5 | UX path principal del merchant para migrar |
| R-006 | Refresh token expirado (>90 días) | 🟠 Alto | Si el refresh token expira, el sistema debe detectarlo y solicitar re-autorización, no fallar silenciosamente. | 6 | Merchants con baja actividad pueden caer en este caso |
| R-007 | Nuevas instalaciones | 🟠 Alto | Post-cambio, las nuevas instalaciones deben solicitar expiring tokens por defecto. | 7 | Flujo feliz para nuevos merchants |
| R-008 | Multi-tenant isolation | 🟡 Medio | La re-autorización de una company no debe afectar tokens de otras companies. | 8 | Regla fundamental de Ionflow |
| R-009 | Estado visual post-re-autorización | 🟡 Medio | La alerta debe desaparecer después de re-autorizar exitosamente. | 9 | UX — no confundir al merchant |
| R-010 | Permisos para re-autorizar | 🟡 Medio | Solo usuarios con permisos adecuados deberían poder ejecutar la re-autorización. | 10 | Seguridad de acceso |

---

## Recomendación

### Áreas que requieren más atención

1. **Token refresh automático (R-001, R-003)**: Esta es la funcionalidad más crítica y la menos visible en el prototipo. Los background jobs deben manejar token refresh de forma transparente, incluyendo concurrencia y retry. Recomiendo que esta sea el **área principal de testing en Deployment**.

2. ~~**Divergencia AC-4**~~: ✅ RESUELTA — Es solo re-autorización manual. Focus en UI flow + token refresh automático post-re-autorización.

3. **Genericidad del cambio**: El Developer mencionó "todas las integraciones antiguas". Si el cambio es genérico (no solo Shopify), el scope de testing se expande significativamente a todos los connectors OAuth.

### Siguiente paso sugerido
Resolver la divergencia AC-4 y la pregunta de genericidad (pregunta 10) antes de construir la Test Matrix, ya que estas decisiones impactan directamente el número y tipo de test cases.
