# Test Plan — 86e1y463z (IONF-1088)

## Información del Ticket
- **ID**: 86e1y463z (IONF-1088)
- **Título**: Absorción y Unificación de NOVASPHERE en Gateway e Ionflow
- **Módulo principal**: developer-apps (→ Marketplace/Stores)
- **Módulos impactados**: billing, services, integrations
- **QA Engineer**: Steve Nina
- **Fecha del plan**: 2026-09-01
- **Track**: Discovery → Deployment

## Resumen
- **Total de casos**: 42 (12 happy path + 14 edge + 8 negativos + 8 regresión)
- **Tiempo estimado**: ~480 min (~8 horas)
- **Artefactos de Discovery usados**: risk-triage.md, ac-consolidated.md, test-matrix.md
- **Repos afectados**: 4 (gateway-ion, flow_binaries, gateway, webcomponents-flow)
- **Superficies funcionales**: 8

---

## Pre-requisitos de Deployment

> [!CAUTION]
> **Sin estos pre-requisitos el testing no puede iniciar**. Verificar antes de empezar.

| # | Pre-requisito | Verificación |
|---|--------------|-------------|
| 1 | Las 4 ramas `IONF-1088` mergeadas o desplegadas en staging | ⬜ |
| 2 | 3 eventos Stripe Connect habilitados: `checkout.session.expired`, `customer.subscription.created`, `invoice.finalized` | ⬜ |
| 3 | Al menos 1 company seller con Stripe Connect activo (`charges_enabled = true`) | ⬜ |
| 4 | Al menos 1 company buyer (diferente al seller) con un account | ⬜ |
| 5 | Tarjetas de prueba Stripe disponibles (4242424242424242, etc.) | ⬜ |
| 6 | Acceso a dashboard Stripe (test mode) para verificar espejo y reconciliación | ⬜ |
| 7 | Acceso a BD PostgreSQL (DBeaver o similar) para queries de verificación | ⬜ |
| 8 | Permisos Laratrust creados: `pricing`, `marketplace-product`, `marketplace-billing`, `stripe-connect` | ⬜ |

---

## Orden de Ejecución

### BLOQUE 1 — SMOKE TESTS (~30 min)
> Ejecutar primero. Si alguno falla → **escalar inmediatamente**.

| □ | TC | Descripción | Prioridad |
|---|-----|------------|-----------|
| ⬜ | TC-001 | Crear un Store completo | 🔴 |
| ⬜ | TC-008 | Abrir Plans Studio y editar un plan | 🔴 |
| ⬜ | TC-012 | Configurar Stripe Connect (onboarding) | 🔴 |
| ⬜ | TC-020 | Tabla de precios — fila única con buckets | 🔴 |
| ⬜ | TC-029 | Pago exitoso → ledger actualizado | 🔴 |

### BLOQUE 2 — HAPPY PATH (~90 min)
> Verificar flujo principal de cada superficie.

| □ | TC | Descripción | Prioridad |
|---|-----|------------|-----------|
| ⬜ | TC-002 | Crear Pricing Group y asignar a Store | 🔴 |
| ⬜ | TC-003 | Crear Plan dentro de Pricing Group | 🔴 |
| ⬜ | TC-004 | Crear Price para un Plan (espejo Stripe) | 🔴 |
| ⬜ | TC-009 | Guardar explícito — no autosave | 🔴 |
| ⬜ | TC-014 | Compra exitosa con tarjeta de prueba | 🔴 |
| ⬜ | TC-015 | Verificar trazabilidad en factura | 🔴 |
| ⬜ | TC-022 | Modo público (public-key) — catálogo sin sesión | 🔴 |
| ⬜ | TC-023 | Modo autenticado (intent secret) — checkout embebido | 🔴 |
| ⬜ | TC-024 | Flujo completo M2M catálogo → cargo → listado → cancel | 🔴 |
| ⬜ | TC-032 | Post-pago: notificación al seller vía webhook_url | 🟠 |

### BLOQUE 3 — EDGE CASES (~120 min)
> Verificar bordes y reconciliación.

| □ | TC | Descripción | Prioridad |
|---|-----|------------|-----------|
| ⬜ | TC-005 | Editar monto de precio — SUPERSEDED | 🟠 |
| ⬜ | TC-006 | prices-bulk atómico — fallo parcial revierte todo | 🟠 |
| ⬜ | TC-010 | Cerrar browser sin guardar — confirmación | 🟠 |
| ⬜ | TC-011 | Carrusel con 5+ planes — scroll horizontal | 🟡 |
| ⬜ | TC-013 | Activar plan sin Stripe Connect completado | 🟠 |
| ⬜ | TC-016 | Dos addons del mismo servicio = 2 subs separadas | 🔴 |
| ⬜ | TC-017 | Cambio de plan con prorrateo | 🟠 |
| ⬜ | TC-021 | Plan sin periodo seleccionado desaparece | 🟠 |
| ⬜ | TC-025 | Aislamiento: App A lee línea de App B cuenta compartida | 🔴 |
| ⬜ | TC-030 | Reconciliación: cambiar precio desde Stripe dashboard | 🟠 |
| ⬜ | TC-031 | Reconciliación: quitar item desde Stripe dashboard | 🟠 |

### BLOQUE 4 — NEGATIVOS (~60 min)
> Verificar que NO se pueda romper el sistema.

| □ | TC | Descripción | Prioridad |
|---|-----|------------|-----------|
| ⬜ | TC-007 | CRUD sin permisos TENANT_PERMS | 🟡 |
| ⬜ | TC-018 | Mezcla de monedas — 422 no 500 | 🔴 |
| ⬜ | TC-019 | Checkout sin seller con payouts | 🟠 |
| ⬜ | TC-026 | API sin scope → 403 | 🟠 |
| ⬜ | TC-027 | API sin Account-Id → 400 | 🟠 |
| ⬜ | TC-028 | API cuenta ajena → 404 | 🟠 |

### BLOQUE 5 — REGRESIÓN (~90 min)
> Verificar que no rompimos nada existente.

| □ | TC | Descripción | Prioridad |
|---|-----|------------|-----------|
| ⬜ | REG-001 | Diálogo GRAPP abre post-demolición ION-137 | 🟠 |
| ⬜ | REG-002 | Diálogo PDF/Producto abre normalmente | 🟠 |
| ⬜ | REG-003 | Producto sin metadata renderiza igual | 🟡 |
| ⬜ | REG-004 | ServiceInstallDialog legacy sigue funcionando | 🟠 |
| ⬜ | REG-005 | Admin PrimeVue sin regresión visual (claro) | 🟠 |
| ⬜ | REG-006 | Admin PrimeVue sin regresión visual (oscuro) | 🟠 |
| ⬜ | REG-007 | Billing SaaS plataforma intacto | 🟠 |
| ⬜ | REG-008 | Compra desde diálogo ambos caminos | 🔴 |

### BLOQUE 6 — DB EVIDENCE (~30 min)
> Queries de verificación en PostgreSQL.

| □ | Query | Verificar |
|---|-------|-----------|
| ⬜ | `SELECT * FROM marketplace_products WHERE company_id = ...` | Producto creado con pricing_id correcto |
| ⬜ | `SELECT * FROM marketplace_prices WHERE product_id = ...` | Precio con amount, currency, interval, status |
| ⬜ | `SELECT * FROM stripe_objects WHERE owner_type = 'marketplace_price'` | Espejo Stripe con stripe_id, status SUPERSEDED si editado |
| ⬜ | `SELECT * FROM marketplace_invoices JOIN marketplace_invoice_items ...` | Trazabilidad: app_id, price_id, account_id |
| ⬜ | `SELECT * FROM marketplace_subscriptions JOIN marketplace_subscription_items ...` | Suscripción activa con items correctos |
| ⬜ | `SELECT * FROM stripe_connect_accounts WHERE app_id = ...` | Cuenta Connect activa con fee_percent |
| ⬜ | `SELECT public_key FROM apps WHERE id = ...` | Empieza con 'ion_pk_' |
| ⬜ | `SELECT * FROM subscriptions WHERE subscriber_type = 'company'` | Billing SaaS plataforma intacto |

---

## Datos Necesarios

| Dato | Cómo obtenerlo | Notas |
|------|---------------|-------|
| Company seller | Existente en staging o crear nueva | Debe tener permisos marketplace |
| Company buyer | Existente diferente al seller | Debe tener un account |
| Token DevApp | POST /api/2.0/app/token con scopes | Necesita 2 apps para aislamiento |
| Tarjeta Stripe test | 4242 4242 4242 4242 | Exp: cualquier futuro, CVC: 123 |
| Tarjeta Stripe para rechazar | 4000 0000 0000 0002 | Para probar pagos fallidos |
| Stripe test key | Dashboard Stripe → Test mode → API keys | Connect endpoint configurado |
| DBeaver / pgAdmin | Conectar a PostgreSQL staging | Para queries de DB evidence |

---

## Criterios de Aprobación/Rechazo

```
CRITERIOS DE APROBACIÓN
  ✅ TODOS los smoke tests pasan (Bloque 1)
  ✅ TODOS los happy path pasan (Bloque 2)
  ✅ Al menos 80% de los edge cases pasan (Bloque 3)
  ✅ TODOS los negativos pasan — no se puede romper el sistema (Bloque 4)
  ✅ TODOS los casos de regresión pasan (Bloque 5)
  ✅ DB evidence confirma integridad de datos (Bloque 6)

CRITERIOS DE RECHAZO
  ❌ Algún smoke test falla → rechazo inmediato, escalar
  ❌ Happy path falla → rechazo
  ❌ Caso negativo falla (el sistema se puede romper) → rechazo
  ❌ Caso de regresión falla → rechazo con análisis de impacto
  ❌ DB evidence muestra datos corruptos → rechazo

CRITERIOS DE APROBACIÓN CON OBSERVACIONES
  ⚠️ Edge case falla pero no es bloqueante → aprobar con bug registrado
  ⚠️ Problema visual menor → aprobar con observación
  ⚠️ Carrusel scroll UX no ideal → aprobar con feedback
```

---

## Estimación de Tiempo

| Bloque | Casos | Tiempo estimado |
|--------|-------|-----------------| 
| Smoke tests | 5 | ~30 min |
| Happy path | 10 | ~90 min |
| Edge cases | 11 | ~120 min |
| Negativos | 6 | ~60 min |
| Regresión | 8 | ~90 min |
| DB evidence | 8 queries | ~30 min |
| Buffer/setup | — | ~60 min |
| **Total** | **42 + 8 queries** | **~480 min (~8 horas)** |

> [!TIP]
> **Recomendación**: Dividir en 2 sesiones de 4 horas. Sesión 1: Smoke + Happy + Edge. Sesión 2: Negativos + Regresión + DB.

---

## Estado

⏳ Plan creado — esperando inicio de ejecución (Deployment Track)
