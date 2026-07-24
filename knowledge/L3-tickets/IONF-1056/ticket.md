# Ticket: IONF-1056 → IONF-1056-B — Monetización unificada (Zero-Stripe)

> Sesión iniciada: 2026-06-14
> Modo: **Discovery** → **QA Testing** (IONF-1056-B)
> Módulo: billing (nuevo)
> QA Engineer: Steve Nina
> Assignee Dev: Enrique Vicente
> URL: https://app.clickup.com/t/86e1pzyug
> Branch de Deployment: **IONF-1056-B** (zero-Stripe variant)

---

## Estado del Discovery

| Paso | Descripción | Estado |
|------|-------------|--------|
| PASO 1 | Inicialización y carga de contexto | ✅ |
| PASO 2 | Reconciliación de AC con ClickUp | ✅ (ver ac-reconciliation.md) |
| PASO 3 | Análisis de riesgo (risk-triage) | ✅ (ver risk-triage.md) |
| PASO 3.5 | Code review de prototipo | ⏭️ Saltado (Opción B) |
| PASO 4 | Consolidación de AC | ✅ (ver ac-consolidated.md) |
| PASO 5 | Test Matrix | ✅ (ver test-matrix.md + test-matrix.csv) |
| PASO 5.1 | **Reconsideración de Test Matrix (pivot IONF-1056-B)** | ✅ (2026-07-23) |
| PASO 6 | Plan de testing | ✅ (ver test-plan.md) |

---

## Contexto del Ticket

### Pivot a IONF-1056-B (2026-07-15)

> **CAMBIO FUNDAMENTAL**: El branch que va a producción es **IONF-1056-B**, no el IONF-1056 original.

**Cronología del pivot:**
| Fecha | Evento |
|-------|--------|
| 2026-07-09 | Steve reportó bloqueo: planes de Stripe no creados |
| 2026-07-15 | Rodolfo: reunión con José — implementar motor marketplace (86e1y463z) |
| 2026-07-15 | Enrique publica IONF-1056-B: variante zero-Stripe |
| 2026-07-17 | Code review approved (Gustavo) |
| 2026-07-21 | Code review approved (Rodolfo) — status → `qa testing` |
| 2026-07-22 | Deployed por Rodolfo — status → `qa in process` |
| 2026-07-23 | Reconsideración de test matrix completada |

**Qué se eliminó en IONF-1056-B:**
- Stripe SDK (`stripe-go` dropped), webhook receiver, event router
- Checkout, portal, cancel, resume, change-plan, overage handlers
- Meter event reporting, overage service, overage helpers
- `STRIPE_*` env vars

**Qué se mantiene/agrega en IONF-1056-B:**
- `AdminAssignPlan` — única vía para cambiar plan (sin pago)
- Consumption engine con lazy resets (unchanged)
- Guard/quota enforcement (hard block, sin overage)
- Email templates dicen "contact us" en vez de sugerir overage
- Chat service registra `ai_credits` para flow-pilot (NUEVO)
- ProductSeeder con precios locales (`provider='local'`)
- Tenant UI read-only (pricing cards + usage bars, sin acciones)

### Subtareas (child tickets)

| Ticket | Nombre | Estado |
|--------|--------|--------|
| [IONF-1057](https://app.clickup.com/t/86e1pzz9c) | Runtime history / última duración | `quick prototype` |
| [IONF-1058](https://app.clickup.com/t/86e1pzz9e) | Enforcement, warnings y estado combinado | `prototype review` |
| [IONF-1059](https://app.clickup.com/t/86e1pzz9f) | Catálogo comercial y planes unificados | `quick prototype` |
| [IONF-1060](https://app.clickup.com/t/86e1pzz9g) | IONPDF standalone, add-on y metering | `prototype review` |
| [IONF-1061](https://app.clickup.com/t/86e1pzz9h) | Ledger de consumo unificado | `prototype review` |
| [IONF-1062](https://app.clickup.com/t/86e1pzz9j) | Integración Stripe y facturación overage | `prototype review` |

### Módulo principal: `billing` (nuevo)
### Módulos secundarios impactados:
- `executions` — el guard bloquea ejecuciones según consumo
- `boards` — schedules y webhooks siguen activos pero no ejecutan
- `pdf-templates` — quota de templates y de impresiones gestionadas por billing
- `nodes` — nodo PDF falla mid-execution si pdf_impressions agotado
- `dashboard` — métricas de consumo provienen del ledger

---

## Branches y Repositorios (IONF-1056-B)

| Repository | Branch | PR |
|------------|--------|-----|
| flow_binaries | IONF-1056-B | [PR #21](https://github.com/altacrest/ion_flow_binaries/pull/21) |
| gateway | IONF-1056-B | [PR #18](https://github.com/altacrest/ion_gateway/pull/18) |
| gateway-ion | IONF-1056-B | [PR #20](https://github.com/altacrest/ion_gateway_ion/pull/20) |

---

## Acceptance Criteria — Descripción Original del Ticket

*(Extraídos de la descripción de IONF-1056 — ver ac-consolidated.md para la versión reconsiderada IONF-1056-B)*

### Modelo comercial
- [ ] **AC-MC-01**: La experiencia de pricing y compra muestra IONFLOW, IONPDF standalone y add-on en la misma superficie comercial
- [ ] **AC-MC-02**: Un cliente puede comprar IONPDF sin comprar IONFLOW
- [ ] **AC-MC-03**: Un cliente de IONFLOW puede comprar IONPDF como add-on mensual adicional
- [ ] **AC-MC-04**: Los precios finales no están hardcodeados en la especificación

### Entitlements y reset
- [ ] **AC-ENT-01**: IONFLOW se mide principalmente por segundos de ejecución
- [ ] **AC-ENT-02**: IONPDF standalone incluye bolsa de segundos para templates, menor que la de IONFLOW
- [ ] **AC-ENT-03**: Cada nivel incluye AI credits mensuales (cantidad crece por nivel)
- [ ] **AC-ENT-04**: El cobro adicional de AI credits sigue la fórmula: costo proveedor + margen × factor
- [ ] **AC-ENT-05**: Todos los saldos incluidos se resetean mensualmente (primera versión)

### Enforcement y notificaciones
- [ ] **AC-ENF-01**: Los topes de overage se manejan de forma independiente por recurso
- [ ] **AC-ENF-02**: Al agotar saldo sin overage, el sistema permite exactamente una ejecución de gracia y luego bloquea
- [ ] **AC-ENF-03**: Las alertas de consumo salen solo por email con thresholds fijos por porcentaje (80%, 100%, blocked)

### Ledger y billing
- [ ] **AC-LED-01**: El ledger registra segundos, AI credits, usos de IONPDF, templates y nodos PDF en el mismo modelo
- [ ] **AC-LED-02**: La entidad de cobro puede ser company o user según el caso
- [ ] **AC-LED-03**: Stripe refleja solo suscripciones, add-ons y overage a cobrar; el consumo/elegibilidad se calcula internamente
- [ ] **AC-LED-04**: Este ticket reemplaza IONF-659 e IONF-880 como fuente de verdad

### Criterios Gherkin (descripción original)
- [ ] **AC-GH-01**: Compra standalone de IONPDF → entitlement con capacidades IONPDF + bolsa menor de segundos
- [ ] **AC-GH-02**: Cliente IONFLOW compra add-on IONPDF → mantiene entitlement IONFLOW + suma capacidades IONPDF
- [ ] **AC-GH-03**: Límite superado sin overage → 1 ejecución de gracia → bloqueo hasta reset o cambio comercial
- [ ] **AC-GH-04**: Reset mensual → saldos reiniciados + estado combinado recalcula disponibilidad

---

## Decisiones Tomadas en Comentarios

*(Reconciliación del Paso 2 — basada en comentarios de Marcel y Enrique)*

| AC Original | Decisión en Comentarios | AC Reconciliado | Fuente |
|---|---|---|---|
| Reset mensual para todos | Sin crons de billing; resets son **lazy** (al leer/escribir cuando vence `reset_at`) | AC-ENT-05 ACTUALIZADO: "Reset lazy al leer/escribir, anclado al ciclo de suscripción" | Comentario Enrique 2026-06-08 |
| Stripe como capa de cobro | **IONF-1056-B: Stripe eliminado**. Planes son admin-assigned only con precios locales | AC-LED-03 → **N/A en IONF-1056-B** | Comentario Enrique 2026-07-15 |
| Bloqueo de ejecuciones | En `execution_time`: bloquea en editor y live; schedules/webhooks quedan activos | AC-ENF-02 DETALLADO: bloqueo no desactiva schedules/webhooks | Comentario Enrique 2026-06-09 |
| PDF enforcement | `pdf_templates`: controla creación hasta límite; `pdf_impressions`: falla el nodo mid-execution | AC nuevo: comportamiento diferenciado por tipo de feature | Comentario Enrique 2026-06-09 |
| Emails de notificación | **IONF-1056-B: emails dicen "contact us"** en vez de sugerir overage | AC-ENF-03 ADAPTADO: sin mención de overage | IONF-1056-B changes |
| Entitlement por company | Una suscripción por empresa; plan `free` auto-aprovisionado al crear company | AC-LED-02 ACLARADO: billing owner primary = company | Prototipo doc IONF-1056-prototype.md |
| Sin estimación avanzada en runtime | IONF-1057 simplificado a solo "última duración de ejecución completada" | AC-IONF1057: Muestra solo última duración, sin promedios ni predicciones | Descripción IONF-1057 |
| **Pivot a Zero-Stripe** | Reunión con José: implementar motor marketplace. Branch IONF-1056-B elimina toda integración Stripe | **26 TCs eliminados, 14 nuevos, 56 TCs totales** | Rodolfo 2026-07-15, Enrique 2026-07-15 |

---

## Transcript de Discovery

| Timestamp | Acción | Detalle |
|-----------|--------|---------|
| 2026-06-14 17:11 | Session Start | Carga inicial desde ClickUp ticket 86e1pzyug |
| 2026-06-14 17:18 | Runbook cargado | Revisión de discovery-runbook.md |
| 2026-06-14 17:19 | L1 cargado | business-rules, test-priorities, api-architecture, stack-overview |
| 2026-06-14 17:20 | L2 creado | `knowledge/L2-modules/billing/module.md` (módulo nuevo, no existía) |
| 2026-06-14 17:21 | L3 creado | Esta carpeta — modo Discovery |
| 2026-06-14 17:21 | PASO 2 | Reconciliación de AC completada — ver ac-reconciliation.md |
| 2026-06-14 18:03 | GATE 2 | Aprobado por QA Engineer — avanzar con preguntas abiertas como riesgo |
| 2026-06-14 18:03 | PASO 3 | risk-triage.md generado — 7 riesgos críticos, 2 preguntas abiertas |
| 2026-06-14 18:10 | PASO 3.5 | Saltado (Opción B) — sin code review |
| 2026-06-14 18:19 | PASO 5 | test-matrix.md + test-matrix.csv generados — 67 TCs en 9 suites, 4 bloqueados |
| 2026-07-23 13:25 | PASO 5.1 | **Reconsideración de test matrix** — pivot a IONF-1056-B. 26 TCs eliminados (Stripe/Overage), 14 nuevos (Admin Assignment, AI Credits, Guard sin Overage, Tenant UI, Admin Catalog, Stripe Residual). Resultado: 56 TCs en 13 suites, 2 bloqueados. P-02 resuelta (lazy resets confirmados). |
