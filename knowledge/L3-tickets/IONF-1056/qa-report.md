# QA Report — IONF-1056-B (3er Ciclo — Aprobación)

> Reporte final de QA generado por `sprint-testing/report`
> Fecha: 2026-08-23
> QA Engineer: Steve Nina

## Información del Ticket

| Campo | Valor |
|-------|-------|
| Ticket ID | 86e1pzyug |
| Título | IONFLOW - Monetización unificada: Stripe, consumo por segundos, AI credits e IONPDF |
| Módulo | Billing (nuevo) — Subscriptions, Consumption Guard, Notifications, Admin Panel, Tenant UI |
| Branch | IONF-1056-B (merged to DEVELOPMENT) |
| Entorno | dev-app.ionflow.io |
| Browser | Chrome |
| QA Engineer | Steve Nina |
| Fecha de testing | 2026-08-23 (3er ciclo) |
| Ciclos totales | 3 (1er rechazo: 2026-07-30, 2do rechazo: 2026-08-14, aprobación: 2026-08-23) |

---

## Resumen Ejecutivo

| Métrica | 1er Ciclo | 2do Ciclo | 3er Ciclo |
|---------|-----------|-----------|-----------|
| Observaciones encontradas | 18 (OBS-01 a OBS-18) | 14 (OBS-R01 a OBS-R14) | 0 |
| Severidad 🔴 Urgent | 5 | 6 | 0 |
| Severidad 🟡 High | 9 | 4 | 0 |
| Preguntas abiertas | 5 | 2 | 0 |
| Observaciones reincidentes | — | 1 (OBS-R10 → OBS-02) | 0 |
| **Veredicto** | **❌ Rejected** | **❌ Rejected** | **✅ Approved** |

---

## Veredicto

| Campo | Valor |
|-------|-------|
| Sugerencia del Catalyst | ✅ Approved |
| **Veredicto final (QA Engineer)** | **✅ Approved** |
| Firmado por | Steve Nina |
| Fecha | 2026-08-23 |
| Observaciones | OBS-R02 y OBS-R08 trasladadas a tickets nuevos (no son bloqueantes para este ticket) |

---

## Historial de Correcciones por Ciclo

### 1er Ciclo → 2do Ciclo (Correcciones del Developer — 2026-08-04)

| OBS | Resolución |
|-----|-----------|
| OBS-01 🔴 | **Decisión**: `pdf_templates` deja de ser feature medible. AC-28 obsoleto. |
| OBS-02 🔴 | **Corregido**: Envío primero/marca después, log con contexto completo, destinatario resuelto explícitamente. |
| OBS-03 🔴 | **Corregido**: Guard evaluado antes de despachar flow → 403 inmediato. |
| OBS-04 🔴 | **Corregido**: Retirado `-1` de borrado company y `+1/-1` de account. |
| OBS-05 🟡 | **UI corregida**: Trunca hacia abajo, muestra decimal, nunca 100% si no bloqueada. |
| OBS-06 🟡 | **Corregido**: Select deshabilitado + guard de reentrada + no-op backend. |
| OBS-07 🟡 | **Corregido**: `createFreeSubscription` transaccional (suscripción + ventanas). |
| OBS-08 🔴 | **Decisión**: FeatureGuard PHP eliminado. IonMind sin medición hasta migrar a Go. |
| OBS-09 🟡 | **Corregido**: Fecha + hora del reinicio en zona horaria del navegador. |
| OBS-10 🔴 | **Corregido**: Detalle de plan carga desde `GET /billing/plans/{id}`. |
| OBS-11 🔴 | **Corregido**: Fila resaltada durante edición. |
| OBS-12 🟡 | **Corregido**: `useApiError().showApiError()` con mensajes contextuales. |
| OBS-13 🟡 | **Corregido**: Validaciones UI + API (enteros, rangos, patrones). |
| OBS-14 🟡 | **Reinterpretado**: Plan `internal` no puede llevar producto. |
| OBS-15 🟡 | **Corregido**: Estados en vuelo, diálogos no cerrables, inputs deshabilitados. |
| OBS-16 🟡 | **Corregido**: Formato monetario real + features sin snapshot no desaparecen. |
| OBS-17 🔴 | **Corregido**: Medidor en memoria + flush cada 15s + re-check guard. Estado `quota_exhausted`. |
| OBS-18 🟡 | **Definido**: "Detener al agotar" — flow arranca con cualquier saldo, se detiene al agotarlo. |

### 2do Ciclo → 3er Ciclo (Correcciones del Developer — 2026-08-19 + 2026-08-21)

| OBS | Resolución |
|-----|-----------|
| OBS-R01 🔴 | **Corregido**: Operación atómica para reservar `pdf_impressions`. |
| OBS-R02 🟡 | **Trasladado a ticket nuevo**: Comportamiento del scheduler (ticket 86e1mdnbq). |
| OBS-R03 🔴 | **Corregido**: Estado terminal registrado incluso sin nodos ejecutados. |
| OBS-R04 🔴 | **Corregido**: Status `quota_exceeded` en response. |
| OBS-R05 🟡 | **Corregido**: Badge y contador simultáneos. |
| OBS-R06 🔴 | **Corregido**: Stop detiene completamente la ejecución. |
| OBS-R07 🟡 | **Corregido**: `reference_id` consistente. |
| OBS-R08 🔴 | **Trasladado a ticket nuevo**: Saturación de BD — no replicado. |
| OBS-R09 🟡 | **Corregido**: Filtro `quota_exhausted` agregado. |
| OBS-R10 🔴 | **Corregido**: Variables de entorno corregidas en Dev. |
| OBS-R11 🟡 | **Corregido**: Límite de caracteres reducido a 50. |
| OBS-R12 🟡 | **Corregido**: `overflow-hidden` agregado. |
| OBS-R13 🔴 | **Corregido**: Features no presentes en nuevo plan se eliminan. |
| OBS-R14 🔴 | **Decisión de diseño**: Features se aplican solo para nuevas suscripciones. |
| Fix adicional | Corregido bug de notificaciones duplicadas en concurrencia. |

---

## Decisiones de Diseño Aceptadas

| Decisión | Observación | Justificación |
|----------|-------------|---------------|
| `pdf_templates` no es feature medible | OBS-01 | Solo se factura `pdf_impressions`. Creación ilimitada. |
| FeatureGuard PHP eliminado | OBS-08 | IonMind sin medición hasta migrar a Go. |
| No hay grace execution | OBS-18 | Ejecución parcial ES la gracia. |
| Emails solo para ventanas mensuales/anuales | Contrato QA | Diseño intencional. |
| Features no se propagan retroactivamente | OBS-R14 | Atómico para siguientes suscripciones. |
| `pdf_impressions` con reserva atómica | OBS-R01 | Solo para recursos reservables. |

---

## Observaciones Trasladadas a Tickets Nuevos

| Observación | Ticket Nuevo | Razón |
|-------------|-------------|-------|
| OBS-R02 | Draft: scheduler-concurrency-behavior | Comportamiento del scheduler introducido por ticket 86e1mdnbq. |
| OBS-R08 | Pendiente | Saturación de BD no replicada. |

---

## Información de Entorno

| Details | |
|---------|---|
| BROWSER | Chrome |
| BRANCH | IONF-1056-B (merged to DEVELOPMENT) |
| ENV | dev-app.ionflow.io |
| TEST MATRIX | knowledge/L3-tickets/IONF-1056/test-matrix.md |
| MERGE REQUESTS | [flow_binaries PR #34](https://github.com/altacrest/ion_flow_binaries/pull/34), [gateway-ion PR #48](https://github.com/altacrest/ion_gateway_ion/pull/48), [flow_binaries PR #37](https://github.com/altacrest/ion_flow_binaries/pull/37) |
