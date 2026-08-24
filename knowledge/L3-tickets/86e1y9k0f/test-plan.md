# Test Plan — 86e1y9k0f (Expiring token requirements for public apps)

## Información del Ticket

| Campo | Valor |
|-------|-------|
| **ID** | 86e1y9k0f |
| **Título** | Expiring token requirements for public apps |
| **Módulo principal** | Integrations (Marketplace > Configured Channels > Shopify) |
| **Módulo secundario** | Connections (Channel package — OAuth/token refresh) |
| **Tipo** | Refactor |
| **Prioridad** | High |
| **Asignado a** | Alex Chura |
| **QA Engineer** | Steve Nina |
| **Fecha del plan** | 2026-08-06 |
| **URL** | [ClickUp](https://app.clickup.com/t/86e1y9k0f) |

---

## Resumen

- **Total de casos**: 28
- **Tiempo estimado**: ~180 min (3 horas)
- **Artefactos de Discovery usados**:
  - ✅ `risk-triage.md` — 10 riesgos, 12 edge cases, 10 preguntas para Developer
  - ✅ `ac-consolidated.md` — 9 AC confirmados + 3 AC propuestos
  - ✅ `test-matrix.md` — 28 casos (10 happy, 8 edge, 4 negativos, 6 regresión)
  - ✅ `test-matrix.csv` — Versión CSV para registro

---

## Orden de Ejecución

### BLOQUE 1 — SMOKE TESTS (ejecutar primero, si alguno falla → escalar)

> Si cualquier smoke test falla, PARAR y escalar al Developer antes de continuar.

```
□ TC-001: Alerta de re-autorización visible para Shopify existente — 🔴
□ REG-001: Integración Shopify existente sigue funcionando (no regresión) — 🔴
□ REG-002: Vista Configured Channels carga correctamente — 🟠
```

### BLOQUE 2 — CORE FLOW (flujo principal de re-autorización)

> El flujo completo de re-autorización es el corazón del ticket.

```
□ TC-002: Re-autorización OAuth exitosa completa — 🔴
□ TC-010: Campos de BD correctos después de re-autorización — 🔴
□ TC-003: Nueva instalación de Shopify obtiene expiring tokens — 🔴
□ TC-017: Campos de BD correctos después de nueva instalación — 🟠
□ TC-004: Nueva instalación NO muestra alerta — 🟠
```

### BLOQUE 3 — SYNCS POST-RE-AUTORIZACIÓN (verificar que todo funciona con nuevos tokens)

> Todos los syncs deben funcionar con los nuevos expiring tokens.

```
□ TC-005: Sync órdenes post-reauth — 🔴
□ TC-006: Sync productos post-reauth — 🔴
□ TC-007: Sync inventario post-reauth — 🟠
□ TC-008: Update tracking post-reauth — 🟠
□ TC-009: Token refresh automático transparente durante sync — 🔴
```

### BLOQUE 4 — EDGE CASES (bordes y escenarios atípicos)

> Estos casos verifican robustez. Pueden requerir manipulación de BD para simular condiciones.

```
□ TC-011: Re-autorización interrumpida (cerrar popup) — 🟠
□ TC-012: Refresh token expirado (>90 días) — 🔴
□ TC-013: UI se actualiza después de re-auth exitosa — 🟠
□ TC-014: Múltiples refreshes sucesivos — BD se actualiza — 🟠
□ TC-015: Múltiples integraciones Shopify — estado independiente — 🟡
□ TC-016: Re-auth en una no afecta las demás — 🟡
□ TC-018: Texto y diseño de alerta claros y accionables — 🟡
```

### BLOQUE 5 — NEGATIVOS (verificar que NO se pueda romper)

> Estos casos verifican que el sistema maneja errores correctamente.

```
□ TC-019: API call con token legacy post-deadline — error manejado — 🟠
□ TC-020: Refresh falla (Shopify API down) — error handling — 🟡
□ TC-021: Re-auth con scope inválido — 🟡
□ TC-022: Sync falla por datos inválidos (no confundir con error de token) — 🟡
```

### BLOQUE 6 — REGRESIÓN RESTANTE

```
□ REG-003: Configuración Shopify — campos editables no rotos — 🟠
□ REG-004: OAuth de otros connectors no afectado — 🟠
□ REG-005: Flow con nodo Shopify ejecuta correctamente — 🔴
□ REG-006: Eliminación de integración Shopify funciona — 🟡
```

### BLOQUE 7 — DB EVIDENCE (queries de verificación)

> Ejecutar queries en DBeaver via SSH tunnel. Las queries están en test-matrix.md.

```
□ DB-Q1: Campos de token post-re-autorización (TC-010) — expires_at, refresh_token, refresh_token_expires_at
□ DB-Q2: Campos de token post-nueva-instalación (TC-017)
□ DB-Q3: Token actualizado después de refresh (TC-014) — comparar antes/después
□ DB-Q4: Aislamiento multi-tenant (TC-015, TC-016) — re-auth no afecta otros
□ DB-Q5: Identificar tokens legacy vs migrados (AC-7)
```

---

## Datos Necesarios

| Dato | Cómo obtenerlo | Notas |
|------|---------------|-------|
| **Usuario Company** | `.env` del repo — `IONFLOW_COMPANY_USERNAME` | Rol: tenant |
| **Usuario Admin** | `.env` del repo — `IONFLOW_ADMIN_USERNAME` | Para verificar permisos si aplica |
| **Tienda Shopify de test** | `ionqa.myshopify.com` (del ticket) | Tienda configurada con Sfipedge |
| **Integración Shopify existente (legacy)** | Verificar en Configured Channels que existe una con token no-expirable | Prerequisito para TC-001, TC-002 |
| **Credenciales OAuth Shopify** | Panel de administración de Sfipedge en Shopify Partners | Para completar flujos OAuth |
| **Acceso DBeaver** | SSH tunnel ya configurado | Para queries de verificación BD |
| **Flow con nodo Shopify** | Verificar en Boards que existe un flow activo con nodo Shopify | Para REG-005 |

---

## Criterios de Aprobación/Rechazo

### ✅ CRITERIOS DE APROBACIÓN

```
✅ TODOS los smoke tests pasan (TC-001, REG-001, REG-002)
✅ TODOS los happy path pasan (TC-002 a TC-010)
✅ Al menos 80% de los edge cases pasan (6 de 8 mínimo)
✅ TODOS los negativos pasan — el sistema NO crashea ni genera errores silenciosos
✅ TODOS los casos de regresión pasan — funcionalidad existente no rota
✅ DB evidence confirma integridad de datos (todos los campos correctos)
```

### ❌ CRITERIOS DE RECHAZO

```
❌ Smoke test falla → rechazo inmediato
   Específicamente: si la alerta no aparece (TC-001) o si la funcionalidad existente
   se rompió (REG-001), no hay nada más que testear.

❌ Re-autorización OAuth falla (TC-002) → rechazo
   Este es el flujo principal del ticket. Sin esto, no hay migración posible.

❌ Token refresh automático no funciona (TC-009) → rechazo
   Los tokens expiran cada hora. Sin refresh automático, los syncs fallan cada hora.

❌ Syncs post-re-autorización fallan (TC-005 a TC-008) → rechazo
   Si los syncs no funcionan con nuevos tokens, la migración es inútil.

❌ Caso negativo falla (sistema crashea o error silencioso) → rechazo
   Los errores deben manejarse gracefully, especialmente para background jobs.

❌ Caso de regresión falla → rechazo con análisis de impacto
   Particularmente REG-005 (flows con nodos Shopify).

❌ DB evidence muestra datos corruptos → rechazo
   Campos de token null, timestamps incorrectos, o tokens stale.
```

### ⚠️ CRITERIOS DE APROBACIÓN CON OBSERVACIONES

```
⚠️ Edge case menor falla pero no es bloqueante → aprobar con bug registrado
   Ejemplo: TC-018 (texto de alerta no perfecto) → bug visual, no bloqueante.

⚠️ TC-015/TC-016 (múltiples tiendas Shopify) no reproducible por falta de datos
   → aprobar con observación "no testeado por falta de ambiente multi-shop".

⚠️ TC-019 (post-deadline) no reproducible hasta 1/1/2027
   → aprobar con observación "verificado por BD, no en runtime".
```

---

## Estimación de Tiempo

| Bloque | Casos | Tiempo estimado |
|--------|-------|-----------------|
| Smoke tests | 3 | ~15 min |
| Core flow (re-auth + nueva instalación) | 5 | ~40 min |
| Syncs post-re-autorización | 5 | ~30 min |
| Edge cases | 7 | ~45 min |
| Negativos | 4 | ~20 min |
| Regresión | 4 | ~20 min |
| DB evidence | 5 | ~10 min |
| **Total** | **28 + 5 queries** | **~180 min (3 horas)** |

> **Nota**: El tiempo real depende de la velocidad del ambiente de staging y la disponibilidad de la tienda Shopify de test. Los casos que requieren simular token expirado pueden necesitar manipulación directa de BD.

---

## Riesgos para la Sesión de Testing

| Riesgo | Mitigación |
|--------|------------|
| Tienda Shopify de test no disponible | Verificar acceso a `ionqa.myshopify.com` ANTES de iniciar |
| No se puede simular token expirado | Modificar `expires_at` directamente en BD para forzar expiración |
| No se puede simular refresh token expirado | Modificar `refresh_token_expires_at` en BD |
| OAuth popup bloqueado por browser | Usar browser sin bloqueador de popups |
| No existe flow con nodo Shopify para REG-005 | Crear un flow simple con nodo Shopify antes de iniciar |

---

## Estado

⏳ **Plan creado — esperando inicio de ejecución (Deployment)**

El ticket pasará a Deployment cuando el Developer lo mueva a la siguiente fase. Este plan estará listo para ejecutarse en ese momento.
