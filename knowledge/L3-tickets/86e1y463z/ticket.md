# Ticket: 86e1y463z — Absorción y Unificación de NOVASPHERE en Gateway e Ionflow

> Sesión de Discovery iniciada: 2026-09-01
> Módulo principal: developer-apps (Marketplace)
> Módulos impactados: billing, services, integrations
> QA Engineer: Steve Nina
> Track: Discovery

## Contexto del Ticket

### Acceptance Criteria (Reconciliados — Paso 2 del Runbook)

- [ ] AC-1: Motor propio gestiona recurrencia vía Stripe Connect (direct charge + application fee). Ledger con trazabilidad por `app_id`.
- [ ] AC-2: Stripe como procesador transaccional vía Connect. BD es fuente de verdad (Stripe es espejo write-through).
- [ ] AC-3: Webhook Connect notifica al seller vía `apps.webhook_url`. GRAPPs disparan instalación post-pago.
- [ ] AC-4: Compañías gestionan Stores, Products, Pricing groups, Plans Studio, Subscribers e Invoices.
- [ ] AC-5: `<gt-pricing-table>` dual-mode: public-key (catálogo sin sesión) e intent secret (checkout embebido Connect).
- [ ] AC-6: API DevApp M2M con aislamiento por `app_id` (404 no 403). Scopes `app:marketplace-read|charge|manage`.
- [ ] AC-7: Stack ION-137 (pagos legacy) demolido deliberadamente. No restaurar.
- [ ] AC-8: Una moneda por buyer×seller. Error 422 legible si mezcla monedas.
- [ ] AC-9: 3 eventos Stripe Connect habilitados: `checkout.session.expired`, `customer.subscription.created`, `invoice.finalized`.
- [ ] AC-10: CSS isolation `.modern-ui` con tokens `brand-*`/`ui-surface-*`. Sin regresión en Admin PrimeVue.

### Descripción

EPIC multi-repo que absorbe NOVASPHERE en Gateway/Ionflow. Crea un Marketplace completo con Stripe Connect (direct charges), Pricing groups, Plans Studio, billing/invoices, y demolición del stack ION-137 legacy. 4 repos, ~72K LOC, 114 commits.

### Decisiones del equipo

- Pricing = grupo de planes; Product = plan; Price = tier (vocabulario vinculante)
- PUT sobrescribe registro completo (merge = deuda backend)
- Autosave eliminado → Guardar explícito (SoT servidor)
- Mocks del prototipo (`*Data.ts`) prohibidos
- Un CE `<gt-pricing-table>`, dos modos (public-key vs intent secret)
- Entitlement derivado, nunca almacenado
- Factura reembolsada sigue siendo `paid` (refund = marca de tiempo)

### Módulo afectado
- Módulo principal: `developer-apps` (→ marketplace/stores)
- Módulos relacionados: `billing`, `services`, `integrations`

---

## Plan de Testing

> ✅ Generado — ver `test-plan.md` (6 bloques, ~8h estimadas)

### Risk Triage
> ✅ Generado — ver `risk-triage.md` (10 riesgos, 10 edge cases, 12 preguntas)

### Casos de Testing
> ✅ Generado — ver `test-matrix.md` + `test-matrix.csv` (42 casos: 12 HP + 14 EC + 8 NEG + 8 REG)

---

## Ejecución

> Pendiente — se ejecutará en Deployment Track

---

## Veredicto

> **✅ Discovery COMPLETO** — Listo para Deployment Track

---

## Transcript de la Sesión

| Timestamp | Acción | Detalle |
|-----------|--------|---------|
| 2026-09-01 10:25 | Session Start | Cargado L1 + L2 de developer-apps, billing, services, integrations |
| 2026-09-01 10:25 | ClickUp MCP | Leídos ticket padre + 2 subtareas + todos los comentarios |
| 2026-09-01 10:28 | Paso 1 | Inicialización completa — Gate 1 ✅ |
| 2026-09-01 10:28 | Paso 2 | AC reconciliados (10 ACs: 4 actualizados + 6 nuevos) — Gate 2 ✅ |
| 2026-09-01 10:32 | Paso 3 | risk-triage.md generado — Gate 3 ✅ |
| 2026-09-01 10:32 | Paso 3.5 | Sin code review — Gate 3.5 ✅ |
| 2026-09-01 10:38 | Paso 4 | ac-consolidated.md generado — Gate 4 ✅ |
| 2026-09-01 10:40 | Paso 5 | test-matrix.md + .csv generados — Gate 5 ✅ |
| 2026-09-01 10:42 | Paso 6 | test-plan.md generado — Gate 6 ✅ |
| 2026-09-01 10:42 | Discovery | ✅ COMPLETO — Todos los artefactos generados |
