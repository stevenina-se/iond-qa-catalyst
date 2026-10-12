# QA Report — 86e3fuwr8

> Reporte final de QA generado por `sprint-testing/report`
> Fecha: 2026-09-29
> QA Engineer: Steve Nina

## Información del Ticket

| Campo | Valor |
|-------|-------|
| Ticket ID | 86e3fuwr8 |
| Título | [SEC] Gateway — cerrar vía explotada y retirar endpoints antiguos |
| Módulo | Gateway (rutas v1/v2, middleware, apps, seeders, webhooks salientes) |
| Branch | IONF-1399 (gateway — [PR #87](https://github.com/altacrest/ion_gateway/pull/87)) |
| Entorno | dev-app.ionflow.io / producción (hotfix) |
| Browser | Postman / curl |
| QA Engineer | Steve Nina |
| Fecha de testing | 2026-09-29 |
| Prioridad | 🔴 Urgente (incidente de seguridad del 28/09/2026) |

---

## Contexto del Incidente

El 28/09/2026, 189 integraciones Shopify fueron desactivadas masivamente por una solicitud automatizada que entró por `POST /api/1.0/webhooks/shop/redact` — un endpoint v1 sin autenticación ni validación HMAC. La búsqueda `configuration LIKE '%1%'` coincidió con casi todas las integraciones activas. Las apps receptoras desactivaron las integraciones afectadas.

**Acciones tomadas:**
1. **Hotfix en producción** (ya desplegado): Se eliminaron los 3 endpoints mandatory v1
2. **Recuperación**: 189 integraciones restauradas a ACTIVE, schedules recreados (189 creados, 0 fallidos)
3. **Mejoras de seguridad** (rama IONF-1399): Propiedad de integraciones, rol admin v1, firma HMAC, soft delete, seeders idempotentes

---

## Resumen Ejecutivo

| Métrica | Valor |
|---------|-------|
| Total de casos ejecutados | 28 |
| Casos aprobados | 28 |
| Casos fallidos | 0 |
| **Tasa de aprobación** | **100%** |
| Bugs bloqueantes (🔴) | 0 |

---

## Evaluación contra Criterios de Aceptación

| AC | Criterio | Resultado | Cumple |
|----|----------|-----------|--------|
| AC-1 | Endpoints v1 mandatory ya no procesan solicitudes; v2 valida HMAC | ✅ | ✅ |
| AC-2 | Recuperación de integraciones afectadas y schedules verificada | ✅ | ✅ |
| AC-3 | Propiedad de integraciones v2 — apps/cuentas no acceden a ajenas | ✅ | ✅ |
| AC-4 | Endpoints gestión v1 exigen rol admin; rutas operativas sin cambio | ✅ | ✅ |
| AC-5 | Firma HMAC en webhooks salientes verificada end-to-end | ✅ | ✅ |
| AC-6 | Soft delete de apps y migración validados | ✅ | ✅ |
| AC-7 | PR #87 validado en ambiente correspondiente | ✅ | ✅ |
| AC-8 | Hallazgos pendientes documentados y enlazados | ✅ | ✅ |

---

## Resultados por Bloque

### Hotfix — Mandatory Webhooks v1 (ya en producción)

| ID | Caso | Resultado | Notas |
|----|------|-----------|-------|
| HF-001 | `POST /api/1.0/webhooks/shop/redact` → 405 | ✅ | Ruta eliminada |
| HF-002 | `POST /api/1.0/webhooks/customers/redact` → 405 | ✅ | Ruta eliminada |
| HF-003 | `POST /api/1.0/webhooks/customers/data_request` → 405 | ✅ | Ruta eliminada |

### Mandatory v2 — Sigue funcionando

| ID | Caso | Resultado | Notas |
|----|------|-----------|-------|
| V2-001 | `POST /api/2.0/webhooks/{slug}/shopifyv2/shop/redact` con HMAC válido → 200 | ✅ | App recibe evento para integración correcta |
| V2-002 | `POST /api/2.0/webhooks/{slug}/shopifyv2/shop/redact` con HMAC inválido → 401 | ✅ | Rechazado correctamente |

### Propiedad de Integraciones v2

| ID | Caso | Resultado | Notas |
|----|------|-----------|-------|
| OWN-001 | Integración propia (app A / cuenta X) — showApp, update, getLogs, destroy, updateStatus → funciona | ✅ | Sin cambio de comportamiento |
| OWN-002 | Integración de app B con credenciales de app A → 404 | ✅ | Aislamiento correcto |
| OWN-003 | Token webcomponent cuenta X → integración cuenta Y (misma app) → 404 | ✅ | Aislamiento por cuenta |
| OWN-004 | Key inexistente en `GET app/integrations/{key}` → 404 (antes 500) | ✅ | Error mejorado |
| OWN-005 | `DELETE app/integrations/{id}` con id de otra app → 404, integración intacta | ✅ | No afecta registros ajenos |
| OWN-006 | update/getLogs/showApp sobre integración INACTIVE → 404 | ✅ | Igual que antes |

### Rol Admin en v1

| ID | Caso | Resultado | Notas |
|----|------|-----------|-------|
| ADM-001 | Token de admin → rutas gestión v1 (users, integrations, schedules, services, apps, appsetups, accounts, requests) → funciona | ✅ | Acceso admin correcto |
| ADM-002 | Usuario sin rol admin → rutas gestión v1 → 403 | ✅ | Bloqueado correctamente |
| ADM-003 | Sin token → rutas gestión v1 → 401 | ✅ | Auth requerida |
| ADM-004 | Rutas operativas v1 (orders, inventory, shipments) → sin cambio | ✅ | No afectadas |

### Firma HMAC hacia las Apps

| ID | Caso | Resultado | Notas |
|----|------|-----------|-------|
| HMAC-001 | Disparar evento → header `X-Gateway-Hmac-Sha256` presente | ✅ | Header llega al request bin |
| HMAC-002 | Recalcular `base64(HMAC-SHA256(raw_body, client_secret))` → coincide | ✅ | Firma válida |
| HMAC-003 | Body idéntico al formato anterior (no breaking change) | ✅ | Retrocompatible |
| HMAC-004 | App sin OAuth client → evento sin header, log `App webhook sent unsigned` | ✅ | Documentado, sin firma |

### Soft Delete de Apps

| ID | Caso | Resultado | Notas |
|----|------|-----------|-------|
| SD-001 | Borrar app → desaparece de lista; fila con `deleted_at` en BD | ✅ | Borrado lógico correcto |
| SD-002 | Credenciales de app borrada en `app/*` → 401 | ✅ | Token revocado |
| SD-003 | Token webcomponent de app borrada → 401 (no 500) | ✅ | Error mejorado |
| SD-004 | Mandatory v2 con slug borrado → 404 | ✅ | Sin procesamiento |
| SD-005 | Crear app con slug de borrada → error validación (slug reservado) | ✅ | Previene conflicto |
| SD-006 | Crear/editar app con OAuth client de otra app → 409 | ✅ | App no se borra en update fallido |
| SD-007 | Bulk channel update con id de app borrada → 422 | ✅ | Rechazado |
| SD-008 | `migrate:rollback --step=1` y `migrate` → funciona | ✅ | Migración reversible |

### Seeders Idempotentes (entorno de pruebas)

| ID | Caso | Resultado | Notas |
|----|------|-----------|-------|
| SEED-001 | `db:seed --class=PassportSeeder` × 2 → no duplica clients | ✅ | `firstOrCreate` |
| SEED-002 | Cambiar password admin → `LaratrustSeeder` → password conservado | ✅ | No pisa datos existentes |

---

## Bugs Encontrados

**No se encontraron bugs durante el testing.**

---

## Veredicto

| Campo | Valor |
|-------|-------|
| Sugerencia del Catalyst | ✅ Approved |
| **Veredicto final (QA Engineer)** | **✅ Approved** |
| Firmado por | Steve Nina |
| Fecha | 2026-09-29 |
| Observaciones | Ninguna — ticket de seguridad urgente con todos los AC cumplidos |

---

## Información de Entorno

| Details | |
|---------|---|
| BROWSER | Postman / curl |
| BRANCH | IONF-1399 |
| ENV | dev-app.ionflow.io + producción (hotfix) |
| TEST MATRIX | L3-tickets/86e3fuwr8/qa-report.md |
| MERGE REQUEST | [PR #87](https://github.com/altacrest/ion_gateway/pull/87) |
