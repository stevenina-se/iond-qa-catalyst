# Test Plan — 86e22fzq7

> Ticket: Connections — Reautorización por API Key crea conexión duplicada en lugar de sobrescribir
> Módulo: Connections / Integrations
> QA Engineer: Steve Nina
> Fecha: 2026-07-14

---

## Objetivo

Verificar que el fix para el bug de reautorización de conexiones API Key:
1. Actualiza la conexión existente en lugar de crear un duplicado
2. Suprime toasts de éxito durante reauthorize
3. No introduce regresiones en flujos de creación nueva, OAuth, ni tenant apps
4. Preserva aislamiento multi-tenant

---

## Alcance

### In Scope
- Reautorización de conexiones API Key (bug fix principal)
- Reautorización de conexiones OAuth (cobertura de flujo `authorizing`)
- Creación de nuevas conexiones (regresión de toasts)
- Tenant apps (regresión)
- Aislamiento multi-tenant
- Flows que usan conexiones reautorizadas

### Out of Scope
- Creación/edición de App Connectors (no afectado por este fix)
- Webhooks de connectors (no afectado)
- Admin migration to global (no afectado)
- App-Scope M2M API (IONF-996, no afectado)

---

## Prerequisitos

| Prerequisito | Estado |
|-------------|--------|
| Branch IONF-1114 deployed en staging | ✅ Confirmado por Rodolfo (2026-07-14 16:51) |
| Conexión API Key activa en staging | ⬜ Verificar al iniciar |
| Conexión OAuth activa en staging | ⬜ Verificar al iniciar |
| Conexión de tenant app en staging | ⬜ Verificar al iniciar |
| Flow activo que use una conexión | ⬜ Verificar al iniciar |
| Credenciales de testing (.env) | ✅ Disponibles |
| 2 companies para test multi-tenant | ⬜ Verificar al iniciar |

---

## Estrategia de Ejecución

### Modo recomendado: Testing Asistido Playwright MCP (Canal 1)

**Justificación**: La mayoría de los TCs son verificación de UI (toasts, lista de connections, conteo de items). Playwright MCP puede navegar la app y capturar screenshots como evidencia. Los TCs de OAuth requieren interacción con popup externo → pueden requerir supervisión manual del QA Engineer.

### Orden de ejecución

```
BLOQUE 1 — Smoke Tests (2 TCs)
    TC-001: Vista de connections carga
    TC-002: Botón Reauthorize visible
    → Gate: Si falla → PARAR (el módulo no funciona)

BLOQUE 2 — Happy Path / Bug Fix Core (3 TCs)
    TC-003: Reauthorize API Key sin duplicado ← CASO CRÍTICO DEL BUG
    TC-004: Toasts suprimidos en reauthorize
    TC-005: Crear nueva — toasts intactos
    → Gate: Si TC-003 o TC-004 falla → REPORTAR BUG (fix no funciona)

BLOQUE 3 — Edge Cases (4 TCs)
    TC-006: OAuth reauthorize
    TC-007: Tenant app reauthorize
    TC-008: Connection_id inválido
    TC-009: Reauthorize + create new secuencial
    → Gate: Evaluar severidad de fallos

BLOQUE 4 — Negativos y Regresión (5 TCs)
    TC-010: Crear nueva sin supresión accidental
    TC-011: Multi-tenant isolation
    TC-012: Flow con conexión reautorizada
    TC-013: OAuth create new sin regresión
    TC-014: Lista post-reauthorize limpia

BLOQUE 5 — DB Evidence (1 TC)
    TC-015: Sin duplicados en BD
```

---

## Criterios de Aprobación

| Criterio | Requerido |
|----------|-----------|
| Smoke tests | 100% PASS |
| Happy path (TC-003, TC-004, TC-005) | 100% PASS |
| Edge cases | ≥75% PASS |
| Negativos | 100% PASS |
| Regresión | 100% PASS |
| Bugs 🔴 abiertos | 0 |

---

## Riesgos Identificados

| Riesgo | Impacto | Mitigación |
|--------|---------|------------|
| No hay tests automatizados del developer | Alto — solo nuestro testing manual cubre el fix | Testing exhaustivo + considerar automatización post-QA |
| OAuth popup en Playwright MCP | Medio — pueden no ser capturables por Playwright | Fallback a testing manual para TC-006 y TC-013 |
| Multi-tenant requiere 2 companies | Medio — puede no haber 2 configuradas | Verificar al inicio; si no hay → TC-011 SKIPPED con justificación |
| Flow activo con la conexión específica | Medio — puede no existir | Crear flow de prueba si es necesario |

---

## Estimación

| Métrica | Valor |
|---------|-------|
| TCs totales | 15 |
| Tiempo estimado | ~2-3 horas (asistido Playwright MCP) |
| Bloqueo por prerequisitos | Bajo (deploy confirmado) |
