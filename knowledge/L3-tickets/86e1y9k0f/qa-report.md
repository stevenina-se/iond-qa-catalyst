# QA Report — 86e1y9k0f

> Reporte final de QA generado por `sprint-testing/report`
> Fecha: 2026-09-02
> QA Engineer: Steve Nina

## Información del Ticket

| Campo | Valor |
|-------|-------|
| Ticket ID | 86e1y9k0f |
| Título | Expiring token requirements for public apps |
| Módulo | Integrations (Marketplace > Configured Channels > Shopify) / Connections |
| Branch | `IONF-1091` (webcomponents-flow), `IONF-1091-A` (gateway) |
| Base | `v1.4.x` |
| Entorno | gateway.shipedge.com |
| Browser | Chrome |
| QA Engineer | Steve Nina |
| Developer | Alex Chura |
| Fecha de testing | 2026-09-02 |

---

## Resumen Ejecutivo

| Métrica | Valor |
|---------|-------|
| Total de casos ejecutados | 28 |
| Casos aprobados (✅) | 28 |
| Casos fallidos (❌) | 0 |
| Casos parciales (⚠️) | 0 |
| Casos saltados (⏭️) | 0 |
| **Tasa de aprobación** | **100%** |
| Bugs encontrados en testing | 0 |
| Bugs bloqueantes (🔴) | 0 |

---

## Evaluación contra Criterios

| Criterio | Requerido | Resultado | Cumple |
|----------|-----------|-----------|--------|
| Smoke tests pasan | 100% | 3/3 | ✅ |
| Happy path pasan | 100% | 10/10 | ✅ |
| Edge cases pasan | ≥80% | 8/8 (100%) | ✅ |
| Negativos pasan | 100% | 4/4 | ✅ |
| Regresión pasan | 100% | 6/6 | ✅ |
| DB evidence conforme | 100% | 5/5 | ✅ |
| Bugs 🔴 abiertos | 0 | 0 | ✅ |

---

## Veredicto

| Campo | Valor |
|-------|-------|
| Sugerencia del Catalyst | ✅ Approved |
| **Veredicto final (QA Engineer)** | **✅ Approved** |
| Firmado por | Steve Nina |
| Fecha | 2026-09-02 |
| Observaciones | Ninguna |

---

## Resultados por Bloque

### Bloque 1 — Smoke Tests

| ID | Caso | Resultado | Notas |
|----|------|-----------|-------|
| TC-001 | Alerta de re-autorización visible para Shopify existente | ✅ | Banner naranja visible en primera tarjeta Settings |
| REG-001 | Integración Shopify existente sigue funcionando | ✅ | Sync de órdenes exitoso con token legacy |
| REG-002 | Vista Configured Channels carga correctamente | ✅ | Lista de canales visible, Shopify clickeable |

### Bloque 2 — Core Flow (Re-autorización)

| ID | AC | Caso | Resultado | Notas |
|----|-----|------|-----------|-------|
| TC-002 | AC-4 | Re-autorización OAuth exitosa completa | ✅ | Flujo OAuth con Shopify completado, tokens expiring obtenidos |
| TC-010 | AC-3 | Campos de BD correctos post-re-autorización | ✅ | `expires_at`, `refresh_token`, `refresh_token_expires_at` correctos |
| TC-003 | AC-1 | Nueva instalación obtiene expiring tokens | ✅ | Nueva integración con tokens expirables por defecto |
| TC-017 | AC-3 | Campos de BD correctos post-nueva instalación | ✅ | Campos de expiración presentes desde instalación |
| TC-004 | AC-8 | Nueva instalación NO muestra alerta | ✅ | Sin banner de re-autorización para integraciones nuevas |

### Bloque 3 — Syncs Post-Re-autorización

| ID | AC | Caso | Resultado | Notas |
|----|-----|------|-----------|-------|
| TC-005 | AC-6 | Sync órdenes post-reauth | ✅ | Órdenes importadas correctamente |
| TC-006 | AC-6 | Sync productos post-reauth | ✅ | Productos importados correctamente |
| TC-007 | AC-6 | Sync inventario post-reauth | ✅ | Inventario sincronizado |
| TC-008 | AC-6 | Update tracking post-reauth | ✅ | Tracking actualizado |
| TC-009 | AC-2 | Token refresh automático transparente | ✅ | Refresh ejecutado automáticamente por `ShopifyTokenRefresher` |

### Bloque 4 — Edge Cases

| ID | Escenario | Resultado | Notas |
|----|-----------|-----------|-------|
| TC-011 | Re-autorización interrumpida (cerrar popup) | ✅ | Token anterior sigue funcionando, alerta persiste |
| TC-012 | Refresh token expirado (>90 días) | ✅ | Sistema detecta, muestra alerta, error descriptivo |
| TC-013 | UI se actualiza después de re-auth exitosa | ✅ | Alerta desaparece, no reaparece al recargar |
| TC-014 | Múltiples refreshes sucesivos — BD correcta | ✅ | Campos actualizados correctamente en cada refresh |
| TC-015 | Múltiples integraciones Shopify — estado independiente | ✅ | Cada integración mantiene estado independiente |
| TC-016 | Re-auth en una no afecta las demás | ✅ | Aislamiento correcto entre integraciones |
| TC-018 | Texto y diseño de alerta claros | ✅ | Banner naranja con icono warning, texto claro con deadline |

### Bloque 5 — Negativos

| ID | Intento inválido | Resultado | Notas |
|----|-----------------|-----------|-------|
| TC-019 | API call con token legacy post-deadline | ✅ | Error manejado con mensaje descriptivo |
| TC-020 | Refresh falla (Shopify API down) | ✅ | Error handling correcto, retry implementado |
| TC-021 | Re-auth con scope inválido | ✅ | No deja integración en estado inconsistente |
| TC-022 | Sync falla por datos inválidos (no confundir con token) | ✅ | Errores de datos diferenciados de errores de token |

### Bloque 6 — Regresión

| ID | Módulo | Caso | Resultado | Notas |
|----|--------|------|-----------|-------|
| REG-003 | Integrations | Configuración Shopify — campos editables | ✅ | Campos de Settings no afectados |
| REG-004 | Connections | OAuth de otros connectors no afectado | ✅ | Sin regresión en otros flujos OAuth |
| REG-005 | Boards | Flow con nodo Shopify ejecuta correctamente | ✅ | Flows existentes no afectados |
| REG-006 | Integrations | Eliminación de integración funciona | ✅ | Funcionalidad de delete intacta |

### Bloque 7 — DB Evidence

| ID | Query | Esperado | Real | Match |
|----|-------|----------|------|-------|
| DB-Q1 | Campos token post-re-autorización | `expires_at`, `refresh_token`, `refresh_token_expires_at` presentes | Valores correctos | ✅ |
| DB-Q2 | Campos token post-nueva instalación | Mismos campos presentes desde instalación | Valores correctos | ✅ |
| DB-Q3 | Token actualizado después de refresh | Timestamps actualizados | Valores frescos | ✅ |
| DB-Q4 | Aislamiento multi-tenant | Re-auth no afecta otros tenants | Aislamiento correcto | ✅ |
| DB-Q5 | Identificar tokens legacy vs migrados | Distinción clara en campos | Distinción correcta | ✅ |

---

## Bugs Encontrados

**No se encontraron bugs durante la sesión de testing.**

---

## Code Review QA

- **Repos revisados**: gateway (IONF-1091-A, PR #50), webcomponents-flow (IONF-1091, PR #26)
- **Commits analizados**: 6 commits del ticket
  - `84bdc850` — Implement Shopify access token auto-refresh logic
  - `10228bc7` — Implement atomic cache locking in ShopifyTokenRefresher
  - `350ab589` — Add seeder to migrate Shopify integrations
  - `b22eb488` — Centralize request parameter rehydration logic
  - `1c8fd53` — Add ShopifyV2 re-authorization support (webcomponents)
  - `e8ceebd` — Remove unused useExpiration hook (webcomponents)
- **Archivos clave modificados**:
  - `ShopifyTokenRefresher.php` — Nueva clase con cache locking atómico, refresh al 50% TTL
  - `MigrateShopifyExpiringTokensSeeder.php` — Seeder de migración masiva (uso único)
  - `AuthorizationServiceTrait.php` — Rehydration de parámetros centralizada
  - `ServiceInstallForm.vue` — Banner de re-autorización para SHOPIFYV2
  - `useExpiration.ts` — Hook eliminado (lógica movida al backend)

---

## Información de Entorno

| Details | |
|---------|---|
| BROWSER | Chrome |
| BRANCH | `IONF-1091` (wc-flow) / `IONF-1091-A` (gateway) |
| BASE | `v1.4.x` |
| ENV | gateway.shipedge.com |
| TEST MATRIX | `L3-tickets/86e1y9k0f/test-matrix.md` |
| MERGE REQUEST | [gateway PR #50](https://github.com/altacrest/ion_gateway/pull/50) / [wc-flow PR #26](https://github.com/altacrest/ion_webcomponents_flow/pull/26) |
