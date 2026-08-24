# Test Matrix — 86e1y9k0f (Expiring token requirements for public apps)

> Generado durante Discovery — 2026-08-06
> Módulo principal: Integrations (Marketplace > Configured Channels > Shopify)
> Módulo secundario: Connections (Channel package — OAuth/token refresh)
> Basado en: ac-consolidated.md + risk-triage.md

---

## Resumen

- **Total de casos**: 28
- **Happy path**: 10
- **Edge cases**: 8
- **Negativos**: 4
- **Regresión**: 6
- **Automatizables**: 12 (UI gateway-ion)
- **Queries de BD**: 5

---

## Test Matrix

### Happy Path

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-001 | Integrations | AC-4, AC-8, AC-9 | Happy Path | Alerta de re-autorización visible para integración Shopify existente con token no-expirable | Integración Shopify existente configurada con token no-expirable (legacy) | Company Login > Sidebar: Marketplace > Tab: Configured Channels > Click [Shopify channel] > Verify: Alerta "Shopify requires re-authorization" visible en Settings card > Verify: Botón "Re-Authorize" visible | La alerta de re-autorización y el botón "Re-Authorize" son visibles en la primera tarjeta de Settings de la integración Shopify existente | 🔴 | ✅ | ⬜ |
| TC-002 | Integrations | AC-4 | Happy Path | Re-autorización OAuth exitosa completa | Integración Shopify existente con alerta visible | Company Login > Sidebar: Marketplace > Tab: Configured Channels > Click [Shopify channel] > Button: "Re-Authorize" > Wait: Popup/redirect de Shopify OAuth > Completar autorización en Shopify > Wait: Redirect de vuelta a Ionflow > Verify: Alerta desaparece o mensaje de éxito | El flujo OAuth se completa exitosamente, se obtienen expiring tokens, y la integración queda actualizada | 🔴 | ❌ | ⬜ |
| TC-003 | Integrations | AC-1 | Happy Path | Nueva instalación de Shopify obtiene expiring tokens por defecto | Company sin integración Shopify configurada, credenciales OAuth de Shopify válidas | Company Login > Sidebar: Marketplace > Tab: Available Marketplace > Click [Shopify] > Completar flujo de instalación OAuth > Wait: Redirect de vuelta > Verify: Integración creada en Configured Channels > Verify: No alerta de re-autorización visible | La nueva integración se crea con expiring tokens por defecto. No se muestra alerta de re-autorización. | 🔴 | ❌ | ⬜ |
| TC-004 | Integrations | AC-8 | Happy Path | Nueva instalación NO muestra alerta de re-autorización | Integración Shopify nueva recién instalada (post-cambio, con expiring tokens) | Company Login > Sidebar: Marketplace > Tab: Configured Channels > Click [Shopify channel nuevo] > Verify: Settings card visible > Verify: NO alerta de re-autorización > Verify: NO botón "Re-Authorize" | La alerta y el botón "Re-Authorize" NO están visibles para integraciones nuevas que ya tienen expiring tokens | 🟠 | ✅ | ⬜ |
| TC-005 | Integrations | AC-6 | Happy Path | Sync de órdenes funciona post-re-autorización | Integración Shopify re-autorizada exitosamente | Company Login > Sidebar: Marketplace > Tab: Configured Channels > Click [Shopify channel] > Section: Orders > Select Order Status: Open > Fill Initial Date > Button: "Execute Get Orders" > Wait: Respuesta > Verify: Órdenes importadas correctamente | Las órdenes se importan correctamente usando los nuevos expiring tokens | 🔴 | ❌ | ⬜ |
| TC-006 | Integrations | AC-6 | Happy Path | Sync de productos funciona post-re-autorización | Integración Shopify re-autorizada exitosamente | Company Login > Sidebar: Marketplace > Tab: Configured Channels > Click [Shopify channel] > Section: Products > Button: "Execute Get Products" > Wait: Respuesta > Verify: Productos importados correctamente | Los productos se importan correctamente usando los nuevos expiring tokens | 🔴 | ❌ | ⬜ |
| TC-007 | Integrations | AC-6 | Happy Path | Sync de inventario funciona post-re-autorización | Integración Shopify re-autorizada exitosamente, Location Id configurado | Company Login > Sidebar: Marketplace > Tab: Configured Channels > Click [Shopify channel] > Section: Sync Inventory > Select Location Id > Button: "Execute Sync Inventory" > Wait: Respuesta > Verify: Inventario sincronizado | El inventario se sincroniza correctamente usando los nuevos expiring tokens | 🟠 | ❌ | ⬜ |
| TC-008 | Integrations | AC-6 | Happy Path | Update tracking funciona post-re-autorización | Integración Shopify re-autorizada exitosamente, órdenes con tracking disponible | Company Login > Sidebar: Marketplace > Tab: Configured Channels > Click [Shopify channel] > Section: Update Tracking > Button: "Execute Update Tracking" > Wait: Respuesta > Verify: Tracking actualizado correctamente | El tracking se actualiza correctamente usando los nuevos expiring tokens | 🟠 | ❌ | ⬜ |
| TC-009 | Integrations | AC-2, AC-P3 | Happy Path | Token refresh automático transparente durante sync | Integración Shopify con expiring tokens donde el access_token acaba de expirar (>1 hora desde último refresh), pero refresh_token aún válido | Company Login > Sidebar: Marketplace > Tab: Configured Channels > Click [Shopify channel] > Section: Orders > Button: "Execute Get Orders" > Wait: Respuesta > Verify: Órdenes importadas correctamente (refresh ocurrió de forma transparente) | El sistema detecta token expirado, ejecuta refresh automáticamente, y completa la operación sin error visible al usuario | 🔴 | ❌ | ⬜ |
| TC-010 | Integrations | AC-3 | Happy Path | Campos de BD correctos después de re-autorización | Re-autorización exitosa completada | Ejecutar TC-002 > Query BD: Verificar campos `expires_at`, `refresh_token`, `refresh_token_expires_at` en tabla de tokens/integrations | Los campos de BD contienen valores correctos: `expires_at` = timestamp futuro (~1 hora), `refresh_token` = valor no vacío, `refresh_token_expires_at` = timestamp futuro (~90 días) | 🔴 | ❌ | ⬜ |

### Edge Cases

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-011 | Integrations | AC-P2 | Edge Case | Re-autorización interrumpida — usuario cierra popup de Shopify | Integración existente con alerta visible | Company Login > Sidebar: Marketplace > Tab: Configured Channels > Click [Shopify channel] > Button: "Re-Authorize" > Wait: Popup de Shopify aparece > Cerrar popup/cancelar > Verify: Regreso a vista de configuración > Verify: Alerta sigue visible > Verify: Token anterior sigue funcionando > Button: "Execute Get Orders" > Verify: Sync funciona | El token anterior no se invalidó, la alerta persiste, y se puede reintentar la re-autorización sin errores | 🟠 | ❌ | ⬜ |
| TC-012 | Integrations | AC-5 | Edge Case | Refresh token expirado (>90 días sin actividad) | Integración Shopify con expiring tokens donde el refresh_token ha expirado (simulado o verificado en BD) | Company Login > Sidebar: Marketplace > Tab: Configured Channels > Click [Shopify channel] > Verify: Alerta de re-autorización visible (refresh token expirado) > Verify: Syncs fallan con mensaje descriptivo (no crash silencioso) | El sistema detecta que el refresh token expiró, muestra alerta de re-autorización, y las operaciones de sync muestran error descriptivo en lugar de fallar silenciosamente | 🔴 | ❌ | ⬜ |
| TC-013 | Integrations | AC-P1 | Edge Case | UI se actualiza correctamente después de re-autorización exitosa | Integración existente con alerta visible, flujo OAuth listo | Company Login > Sidebar: Marketplace > Tab: Configured Channels > Click [Shopify channel] > Verify: Alerta visible > Button: "Re-Authorize" > Completar OAuth > Wait: Redirect > Verify: Alerta desaparece > Reload página > Verify: Alerta sigue sin aparecer | Después de re-autorizar, la alerta desaparece y no reaparece al recargar la página | 🟠 | ❌ | ⬜ |
| TC-014 | Connections | AC-2 | Edge Case | Múltiples refreshes sucesivos — valores de BD se actualizan correctamente | Integración Shopify con expiring tokens, forzar múltiples expirations | Ejecutar sync (TC-005) > Esperar expiración de token (~1h o simular) > Ejecutar sync nuevamente > Query BD: Verificar que `expires_at` se actualizó > Repetir una vez más > Query BD: Verificar `refresh_token` actualizado con nuevo valor | Cada refresh actualiza correctamente los campos de BD. No quedan tokens stale. El nuevo refresh_token reemplaza al anterior. | 🟠 | ❌ | ⬜ |
| TC-015 | Integrations | AC-4, AC-8 | Edge Case | Múltiples integraciones Shopify — cada una con estado independiente | Company con 2+ tiendas Shopify configuradas (una legacy, una nueva) | Company Login > Sidebar: Marketplace > Tab: Configured Channels > Verify: Múltiples canales Shopify listados > Click [Shopify legacy] > Verify: Alerta visible > Volver > Click [Shopify nueva] > Verify: NO alerta visible | Cada integración Shopify tiene su estado de token independiente. La alerta solo aparece en las que tienen tokens no-expirables. | 🟡 | ✅ | ⬜ |
| TC-016 | Integrations | AC-4 | Edge Case | Re-autorización en una de múltiples integraciones no afecta las demás | Company con 2+ tiendas Shopify, ambas legacy | Ejecutar re-autorización en Shopify #1 > Verify: Alerta desaparece en Shopify #1 > Navigate a Shopify #2 > Verify: Alerta sigue visible en Shopify #2 (no re-autorizada) | La re-autorización es por integración individual, no masiva | 🟡 | ❌ | ⬜ |
| TC-017 | Integrations | AC-3 | Edge Case | Campos de BD correctos después de nueva instalación con expiring tokens | Flujo de nueva instalación completado (TC-003) | Ejecutar TC-003 > Query BD: Verificar campos `expires_at`, `refresh_token`, `refresh_token_expires_at` en tabla de tokens/integrations para la nueva integración | Los campos de BD contienen valores correctos desde la primera instalación: `expires_at` ≈ now + 3600s, `refresh_token` no vacío, `refresh_token_expires_at` ≈ now + 7776000s | 🟠 | ❌ | ⬜ |
| TC-018 | Integrations | AC-9 | Edge Case | Texto y diseño de la alerta son claros y accionables | Integración existente con alerta visible | Company Login > Sidebar: Marketplace > Tab: Configured Channels > Click [Shopify channel] > Verify: Texto de alerta menciona "re-authorization" y deadline > Verify: Botón "Re-Authorize" tiene estilo prominente (no gris/deshabilitado) > Verify: Alerta está en la primera tarjeta (Settings) | La alerta es visualmente clara, el texto explica por qué re-autorizar, y el botón es fácilmente identificable | 🟡 | ✅ | ⬜ |

### Negativos

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-019 | Integrations | AC-7 | Negativo | API call con token no-expirable post-deadline — error manejado | Simulación post-deadline: integración Shopify con token legacy (no-expirable) | Intentar ejecutar sync con token no-expirable > Verify: Error response de Shopify API > Verify: Error mostrado al usuario con mensaje descriptivo > Verify: Alerta de re-autorización visible | Si un token legacy se usa post-deadline, el error de Shopify se captura y se muestra un mensaje descriptivo al usuario indicando que debe re-autorizar | 🟠 | ❌ | ⬜ |
| TC-020 | Connections | AC-2 | Negativo | Refresh falla (Shopify API down) — error handling | Integración con expiring tokens, Shopify API no disponible durante refresh | Simular falla de Shopify API durante refresh > Ejecutar sync > Verify: Error descriptivo (no crash) > Verify: Log de error registrado > Verify: Se puede reintentar | Si el refresh falla porque Shopify no responde, el sistema muestra error descriptivo, no crashea, y registra log de error | 🟡 | ❌ | ⬜ |
| TC-021 | Integrations | AC-4 | Negativo | Re-autorización con scope inválido o restringido | Integración existente, credenciales OAuth con permisos limitados | Company Login > Sidebar: Marketplace > Tab: Configured Channels > Click [Shopify channel] > Button: "Re-Authorize" > En Shopify: intentar autorizar con scope limitado > Verify: Comportamiento definido (error o warning) | El sistema maneja correctamente el caso de scope OAuth insuficiente sin dejar la integración en estado inconsistente | 🟡 | ❌ | ⬜ |
| TC-022 | Integrations | AC-6 | Negativo | Sync falla por razón ajena al token (datos inválidos) post-re-autorización | Integración re-autorizada, pero datos de sync inválidos (ej: fecha futura) | Company Login > Sidebar: Marketplace > Tab: Configured Channels > Click [Shopify channel] > Section: Orders > Fill Initial Date: fecha futura > Button: "Execute Get Orders" > Verify: Error de datos, NO error de token | Post-re-autorización, los errores de datos se muestran correctamente (no se confunden con errores de token) | 🟡 | ❌ | ⬜ |

### Regresión

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| REG-001 | Integrations | N/A | Regresión | Integración Shopify existente con token válido sigue funcionando (pre-deadline) | Integración Shopify existente con token no-expirable, antes del deadline | Company Login > Sidebar: Marketplace > Tab: Configured Channels > Click [Shopify channel] > Section: Orders > Button: "Execute Get Orders" > Verify: Sync exitoso | Las integraciones existentes con tokens no-expirables siguen funcionando antes del deadline. El cambio NO rompe funcionalidad existente. | 🔴 | ❌ | ⬜ |
| REG-002 | Integrations | N/A | Regresión | Vista de Configured Channels carga correctamente | Company con integraciones configuradas | Company Login > Sidebar: Marketplace > Tab: Configured Channels > Verify: Lista de canales visible > Verify: Shopify channel clickeable > Verify: Otras integraciones (si existen) también visibles | La vista de Configured Channels carga sin errores y muestra todas las integraciones configuradas | 🟠 | ✅ | ⬜ |
| REG-003 | Integrations | N/A | Regresión | Configuración de integración Shopify (Settings) — campos editables | Integración Shopify configurada | Company Login > Sidebar: Marketplace > Tab: Configured Channels > Click [Shopify channel] > Verify: Integration Name visible > Verify: Shop Host visible > Verify: Campos de configuración de Orders, Products, Tracking, Inventory funcionan | Los campos de configuración existentes de la integración Shopify no se rompieron con el nuevo componente de alerta | 🟠 | ✅ | ⬜ |
| REG-004 | Connections | N/A | Regresión | OAuth flow de otros connectors no afectado | Company con connector OAuth diferente a Shopify (ej: WooCommerce, MercadoLibre) | Company Login > Sidebar: Marketplace > Instalar/conectar otro connector OAuth > Completar flujo OAuth > Verify: Conexión exitosa | El cambio en el flujo OAuth de Shopify no afecta el flujo OAuth de otros connectors | 🟠 | ❌ | ⬜ |
| REG-005 | Boards | N/A | Regresión | Flow con nodo Shopify existente ejecuta correctamente | Flow activo con nodo Shopify (Get Orders o similar), token válido | Company Login > Sidebar: Boards > Click [Flow con nodo Shopify] > Canvas: Ejecutar flow > Wait: Ejecución completa > Verify: Nodo Shopify ejecutó sin error | Los flows existentes con nodos Shopify siguen ejecutándose correctamente después del cambio | 🔴 | ❌ | ⬜ |
| REG-006 | Integrations | N/A | Regresión | Eliminación de integración Shopify sigue funcionando | Integración Shopify configurada (legacy o nueva) | Company Login > Sidebar: Marketplace > Tab: Configured Channels > Click [Shopify channel] > Eliminar integración > Verify: Integración eliminada > Verify: No queda en lista | La funcionalidad de eliminar integración no se rompió con los cambios de token | 🟡 | ✅ | ⬜ |

---

## Queries de Verificación BD

> ⚠️ **NOTA**: Las queries a continuación están basadas en los AC y la estructura conocida de la BD desde las migraciones del L2.
> Los campos `expires_at`, `refresh_token`, `refresh_token_expires_at` son **nuevos** (parte de este ticket).
> Las tablas y columnas exactas deben verificarse contra las migraciones del Developer durante Deployment.

```sql
-- ============================================================
-- QUERY 1: Verificar campos de token después de re-autorización (TC-010)
-- Fuente: L2-modules/integrations — tabla integrations (gateway)
-- Migraciones base: 2022_04_06_222604_create_integrations_table.php
-- Campos nuevos: expires_at, refresh_token, refresh_token_expires_at (migración pendiente de verificar)
-- ============================================================

SELECT 
    id,
    name,
    -- Campos existentes
    created_at,
    updated_at,
    -- Campos nuevos (verificar nombres exactos en migración del ticket)
    expires_at,
    refresh_token IS NOT NULL AS has_refresh_token,
    refresh_token_expires_at
FROM integrations -- O la tabla donde se almacenan tokens (verificar en migración)
WHERE name LIKE '%ionqa%' -- Ajustar al nombre de la integración de test
ORDER BY updated_at DESC
LIMIT 5;

-- Esperado post-re-autorización:
--   expires_at ≈ NOW() + 3600 seconds (1 hora)
--   has_refresh_token = true
--   refresh_token_expires_at ≈ NOW() + 7776000 seconds (90 días)


-- ============================================================
-- QUERY 2: Verificar campos de token para nueva instalación (TC-017)
-- Misma tabla y campos que Query 1
-- ============================================================

-- Ejecutar después de TC-003 (nueva instalación)
-- Misma query que QUERY 1 pero filtrando por la integración nueva
-- Esperado:
--   expires_at IS NOT NULL
--   has_refresh_token = true
--   refresh_token_expires_at IS NOT NULL


-- ============================================================
-- QUERY 3: Verificar que token se actualizó después de refresh (TC-014)
-- ============================================================

-- Ejecutar ANTES del sync: registrar valores actuales
SELECT id, expires_at, refresh_token_expires_at, updated_at
FROM integrations
WHERE name LIKE '%ionqa%';

-- Ejecutar DESPUÉS del sync (que forzó refresh):
-- Comparar: expires_at debe ser POSTERIOR al valor anterior
-- refresh_token_expires_at puede o no cambiar dependiendo de la implementación de Shopify


-- ============================================================
-- QUERY 4: Verificar aislamiento multi-tenant (TC-015, TC-016)
-- Fuente: L2-modules/integrations — multi-tenant por company
-- ============================================================

-- Verificar que la re-autorización de company A no afectó tokens de company B
SELECT 
    i.id,
    i.name,
    i.expires_at,
    i.refresh_token IS NOT NULL AS has_refresh_token,
    i.updated_at
FROM integrations i
-- JOIN con tabla de companies si necesario
ORDER BY i.updated_at DESC;

-- Esperado: Solo la integración re-autorizada tiene expires_at actualizado
-- Las demás integraciones mantienen sus valores originales


-- ============================================================
-- QUERY 5: Verificar que no quedan tokens legacy (AC-7, TC-019)
-- Para verificación post-deadline
-- ============================================================

SELECT 
    id,
    name,
    expires_at,
    refresh_token IS NOT NULL AS has_refresh_token,
    CASE 
        WHEN expires_at IS NULL THEN 'LEGACY (no-expirable)'
        ELSE 'MIGRADO (expirable)'
    END AS token_status
FROM integrations
WHERE name LIKE '%shopify%' -- Ajustar filtro
ORDER BY token_status, name;

-- Esperado post-deadline: Todas las integraciones activas deben ser 'MIGRADO'
-- Las que son 'LEGACY' deben tener la alerta de re-autorización visible
```

---

## Notas para Deployment

### Dependencias de testing
- **TC-002, TC-003** requieren acceso real a Shopify OAuth (tienda de test `ionqa.myshopify.com`)
- **TC-009** requiere simular expiración de token (esperar 1 hora o modificar BD directamente)
- **TC-012** requiere simular refresh token expirado (modificar BD)
- **TC-019** requiere simular comportamiento post-deadline (no reproducible hasta 1/1/2027 — verificar por BD)

### Orden de ejecución sugerido
1. **Smoke**: TC-001 (alerta visible), REG-001 (no regresión), REG-002 (vista carga)
2. **Core flow**: TC-002 (re-auth), TC-003 (nueva instalación), TC-010 (BD)
3. **Syncs post-reauth**: TC-005, TC-006, TC-007, TC-008
4. **Edge cases**: TC-011 a TC-018
5. **Negativos**: TC-019 a TC-022
6. **Regresión restante**: REG-003 a REG-006

### Preguntas pendientes para Developer (del risk-triage)
- Pregunta #10: ¿Aplica solo a Shopify o es genérico? Esto podría ampliar los casos de regresión (REG-004).
- Pregunta #4: ¿Cómo se manejan refreshes concurrentes? Impacta TC-014.
