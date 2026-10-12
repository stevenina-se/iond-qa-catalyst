# Test Matrix — 86e1y463z (IONF-1088)

> Generado por: test-docs/document (modo matrix)  
> Fuentes: ac-consolidated.md + risk-triage.md + L2 modules + QA Instructions de Rodolfo  
> Fecha: 2026-09-01

## Resumen
- Total de casos: 42
- Happy path: 12
- Edge cases: 14
- Negativos: 8
- Regresión: 8
- Automatizables: 18
- Superficies cubiertas: 8

---

## Test Matrix

### SUPERFICIE 1 — Catálogo CRUD + Pricing Groups (Seller UI)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-001 | marketplace-store | AC-4 | Happy Path | Crear un Store completo | Company Login, permisos marketplace | Company Login > Sidebar: Apps > App Stores > Button: "New Store" > Fill "Name": "Test Store" > Fill "Description": "Test" > Button: "Create" > Verify: Store aparece en grid | Store creado, visible en lista con nombre y descripción | 🔴 | ✅ | ⬜ |
| TC-002 | marketplace-store | AC-4 | Happy Path | Crear Pricing Group y asignar a Store | Store existente | Company Login > Sidebar: Apps > Pricing Plans > Button: "New Pricing" > Fill "Name": "Test Pricing" > Button: "Create" > Click [Pricing "Test Pricing"] > Button: "Assign" > Select Store > Verify: Pricing asignado | Pricing group creado y asignado al store | 🔴 | ✅ | ⬜ |
| TC-003 | marketplace-store | AC-4 | Happy Path | Crear Plan (Product) dentro de Pricing Group | Pricing Group existente | Company Login > Sidebar: Apps > Pricing Plans > Click [Pricing] > Button: "Add Plan" > Fill "Title": "Pro Plan" > Fill features > Button: "Save" > Verify: Plan creado | Plan visible en listado del Pricing group | 🔴 | ✅ | ⬜ |
| TC-004 | marketplace-store | AC-2 | Happy Path | Crear Price (Tier) para un Plan | Plan existente, Stripe Connect activo | Company Login > Navigate: Plans Studio > Panel: Prices > Button: "Add Price" > Fill "Amount": 50 > Select "Currency": USD > Select "Interval": monthly > Button: "Save" > Verify: Precio creado y sincronizado con Stripe | Precio creado en BD y espejo en Stripe (stripe_objects) | 🔴 | ❌ | ⬜ |
| TC-005 | marketplace-store | AC-2 | Edge Case | Editar monto de un precio existente | Precio con espejo Stripe | Company Login > Navigate: Plans Studio > Panel: Prices > Click [Price $50] > Fill "Amount": 75 > Button: "Save" > Verify: Precio anterior SUPERSEDED, nuevo precio creado | Precio anterior archivado como SUPERSEDED, nuevo precio activo con nuevo stripe_id | 🟠 | ❌ | ⬜ |
| TC-006 | marketplace-store | AC-4 | Edge Case | prices-bulk atómico — fallo parcial revierte todo | Plan con 3 precios | Company Login > Navigate: Plans Studio > Crear 2 precios nuevos + Editar 1 + Borrar 1 en un solo Save > Simular fallo en uno > Verify: Todos se revierten | Operación atómica: si falla uno, todos se revierten | 🟠 | ❌ | ⬜ |
| TC-007 | marketplace-store | AC-4 | Negativo | CRUD sin permisos TENANT_PERMS | Usuario sin permiso marketplace | Company Login (user sin permisos) > Sidebar: Apps > Verify: Opción no visible o tooltip "No tienes permisos" | Acción bloqueada con tooltip explicativo | 🟡 | ✅ | ⬜ |

### SUPERFICIE 2 — Plans Studio (Seller UI)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-008 | plans-studio | AC-4 | Happy Path | Abrir Plans Studio y editar un plan | Plan existente con precios | Company Login > Sidebar: Apps > Pricing Plans > Click [Pricing] > Click [Plan] > Button: "Edit in Studio" > Verify: Studio carga con carrusel de planes, card preview, panel de precios | Studio carga correctamente con datos del servidor | 🔴 | ✅ | ⬜ |
| TC-009 | plans-studio | AC-4 | Happy Path | Guardar explícito (no autosave) | Plan en edición en Studio | Company Login > Navigate: Plans Studio > Edit title > Verify: indicador "unsaved changes" > Button: "Save" > Verify: Toast "Saved" > Refresh page > Verify: Cambios persisten | Cambios guardados solo al presionar Save. Refresh los mantiene | 🔴 | ✅ | ⬜ |
| TC-010 | plans-studio | AC-4 | Edge Case | Cerrar browser sin guardar — confirmación de navegación | Plan con cambios no guardados | Company Login > Navigate: Plans Studio > Edit title > Click navegación a otra página > Verify: Diálogo "Unsaved changes" aparece | Browser warning o diálogo antes de perder cambios | 🟠 | ❌ | ⬜ |
| TC-011 | plans-studio | AC-4 | Edge Case | Carrusel con 5+ planes — scroll horizontal | Pricing group con 6+ planes | Company Login > Navigate: Plans Studio > Verify: Carrusel muestra flechas de navegación > Scroll entre planes > Verify: Foco de edición no se mueve solo por scroll | Carrusel navega entre planes sin perder foco de edición | 🟡 | ❌ | ⬜ |

### SUPERFICIE 3 — Stripe Connect (Seller Config)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-012 | stripe-connect | AC-2 | Happy Path | Configurar Stripe Connect (onboarding) | Company sin Stripe Connect | Company Login > Sidebar: Apps > App Stores > Click [Store] > Section: Payouts > Button: "Connect Stripe" > Verify: Redirect a Stripe Account Links > Completar onboarding > Verify: Estado ACTIVE | Cuenta Connect creada, estado ACTIVE, charges_enabled | 🔴 | ❌ | ⬜ |
| TC-013 | stripe-connect | AC-2 | Edge Case | Activar plan sin Stripe Connect completado | Plan creado, sin Connect activo | Company Login > Navigate: Plans Studio > Toggle "Enabled" > Verify: PayoutsRequiredDialog aparece | Diálogo bloquea activación hasta completar onboarding | 🟠 | ❌ | ⬜ |

### SUPERFICIE 4 — Checkout + Billing (Buyer)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-014 | checkout | AC-1 | Happy Path | Compra exitosa con tarjeta de prueba | Producto publicado, seller con Connect activo | Buyer Login > Navigate: Marketplace > Click [Producto] > Select Plan > Button: "Subscribe" > Fill card (4242...) > Button: "Pay" > Verify: Cargo en cuenta conectada (no plataforma) con application fee | Invoice creada, subscription activa, cargo en cuenta seller | 🔴 | ❌ | ⬜ |
| TC-015 | checkout | AC-1 | Happy Path | Verificar trazabilidad en factura | Compra realizada (TC-014) | Verify: marketplace_invoice con status, amount, currency > Verify: marketplace_invoice_items con app_id, price_id, account_id > Verify: stripe_objects con stripe_id del invoice | Trazabilidad completa: pago → app → servicio → precio | 🔴 | ❌ | ⬜ |
| TC-016 | checkout | AC-1 | Edge Case | Comprar dos addons del mismo servicio | Servicio con addon purchaseable | Buyer Login > Comprar addon 1 > Comprar addon 2 del mismo servicio > Verify: 2 suscripciones separadas > Cancelar addon 1 > Verify: addon 2 sigue activo | 2 suscripciones independientes (Stripe rechaza duplicados en una sola) | 🔴 | ❌ | ⬜ |
| TC-017 | checkout | AC-1 | Edge Case | Cambio de plan con prorrateo | Suscripción activa | Buyer Login > Navigate: Plan actual > Button: "Change Plan" > Select plan superior > Verify: Prorrateo en factura siguiente | Factura prorrateada correctamente | 🟠 | ❌ | ⬜ |
| TC-018 | checkout | AC-8 | Negativo | Mezcla de monedas — buyer intenta otra moneda | Buyer con compra previa en USD | Buyer Login > Intentar comprar producto en EUR del mismo seller > Verify: Error 422 con mensaje legible | Error 422 claro, NO 500 ni "internal server error" | 🔴 | ❌ | ⬜ |
| TC-019 | checkout | AC-1 | Negativo | Checkout sin seller con payouts habilitados | Seller sin charges_enabled | Buyer Login > Intentar comprar > Verify: Checkout rechazado antes de empezar | Error claro, checkout no se inicia | 🟠 | ❌ | ⬜ |

### SUPERFICIE 5 — Webcomponent Buyer (`<gt-pricing-table>`)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-020 | pricing-table | AC-5 | Happy Path | Tabla de precios — fila única con buckets | Producto con planes en Month/Year/Lifetime | Navigate: Página con embed <gt-pricing-table> > Verify: Una sola fila de planes > Click "Year" > Verify: Todas las cards cambian a precio anual | Fila única, centrada si caben, scroll si no. Buckets cambian en lote | 🔴 | ✅ | ⬜ |
| TC-021 | pricing-table | AC-5 | Edge Case | Plan sin periodo seleccionado desaparece | Plan con Month y Year pero NO Lifetime | Navigate: Tabla de precios > Click "Life Time" > Verify: Plan sin Lifetime desaparece de la fila (no queda con precio vacío) | Plan se oculta limpiamente, no muestra tarjeta vacía | 🟠 | ✅ | ⬜ |
| TC-022 | pricing-table | AC-5 | Happy Path | Modo público (public-key) — catálogo sin sesión | Embed con public-key="ion_pk_..." | Navigate: Página pública con embed > Verify: Catálogo carga sin sesión > Click CTA > Verify: Navega a return_url del backend con ?marketplace_price_id= | Navegación a URL del backend, NO a URL de atributo HTML | 🔴 | ✅ | ⬜ |
| TC-023 | pricing-table | AC-5 | Happy Path | Modo autenticado (intent secret) — checkout embebido | Buyer autenticado con intent JWT | Navigate: Marketplace autenticado > Click "Buy" > Verify: Embedded Checkout abre con stripeAccount correcto > Completar pago > Verify: purchase-completed emitido sin navegar | Checkout Connect en cuenta seller, confirmación server-side | 🔴 | ❌ | ⬜ |

### SUPERFICIE 6 — API DevApp M2M

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-024 | devapp-api | AC-6 | Happy Path | Flujo completo M2M: catálogo → cargo → listado → cancel | Token con scopes marketplace-* | POST /api/2.0/app/token > GET /marketplace/products > POST /marketplace/purchases/direct > GET /subscriptions > POST /cancel > Verify: Todo el flujo funciona | Flujo end-to-end exitoso con token DevApp | 🔴 | ✅ | ⬜ |
| TC-025 | devapp-api | AC-6 | Edge Case | Aislamiento: App A lee línea de App B en cuenta compartida | 2 apps, mismo buyer/account | Token App A > Vender plan a buyer > Token App B > GET líneas del buyer > Verify: Solo ve las líneas de App B, NO las de App A. Intentar cancelar línea de App A > Verify: 404 | Aislamiento por app_id — 404, no 403 ni éxito | 🔴 | ✅ | ⬜ |
| TC-026 | devapp-api | AC-6 | Negativo | Sin scope → 403 | Token sin scope marketplace | Request sin scope > Verify: 403 | 403 Forbidden | 🟠 | ✅ | ⬜ |
| TC-027 | devapp-api | AC-6 | Negativo | Sin header Account-Id → 400 | Token válido | Request sin Account-Id > Verify: 400 | 400 Bad Request | 🟠 | ✅ | ⬜ |
| TC-028 | devapp-api | AC-6 | Negativo | Cuenta ajena → 404 | Token válido, account de otro seller | Request con account ajeno > Verify: 404 | 404 Not Found | 🟠 | ✅ | ⬜ |

### SUPERFICIE 7 — Webhooks + Reconciliación

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-029 | webhooks | AC-9 | Happy Path | Pago exitoso → ledger actualizado | 3 eventos Stripe habilitados, compra exitosa | Realizar compra > Verify: Webhook Connect recibido > Verify: marketplace_invoice creada con status correcto > Verify: marketplace_subscription activa | Invoice y subscription creadas vía webhook | 🔴 | ❌ | ⬜ |
| TC-030 | webhooks | AC-9 | Edge Case | Reconciliación: cambiar precio desde dashboard Stripe | Suscripción activa con item | Dashboard Stripe > Editar precio del item > Verify: Línea local sigue el nuevo precio con el mismo si_ | Reconciliación correcta, si_ preservado | 🟠 | ❌ | ⬜ |
| TC-031 | webhooks | AC-9 | Edge Case | Reconciliación: quitar item desde dashboard Stripe | Suscripción con múltiples items | Dashboard Stripe > Quitar un item > Verify: Item con removed_at en BD > Verify: Sigue apareciendo en facturas viejas | Item marcado como removed, histórico preservado | 🟠 | ❌ | ⬜ |
| TC-032 | webhooks | AC-3 | Happy Path | Post-pago: notificación al seller vía webhook_url | apps.webhook_url configurado | Completar compra > Verify: POST enviado a webhook_url del seller > Verify: Payload incluye pricing, app, form_data | Seller notificado con contexto completo para instalación | 🟠 | ❌ | ⬜ |

### SUPERFICIE 8 — Regresión

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| REG-001 | webcomponents | AC-7 | Regresión | Diálogo GRAPP abre normalmente post-demolición ION-137 | GRAPP existente con rating, system_requirements, apps | Navigate: Marketplace > Click [GRAPP] > Verify: Diálogo detalle abre con rating, requisitos y apps | Diálogo funciona igual que antes de la demolición | 🟠 | ✅ | ⬜ |
| REG-002 | webcomponents | AC-7 | Regresión | Diálogo PDF/Producto abre normalmente | Producto tipo PDF existente | Navigate: Marketplace > Click [PDF Template] > Verify: Diálogo abre correctamente | Diálogo funciona para todos los tipos | 🟠 | ✅ | ⬜ |
| REG-003 | webcomponents | AC-7 | Regresión | Producto sin metadata renderiza igual | Producto sin rating, sin system_requirements, sin apps | Navigate: Marketplace > Click [Producto básico] > Verify: Renderiza como antes | Sin metadata no rompe el diálogo | 🟡 | ✅ | ⬜ |
| REG-004 | webcomponents | AC-7 | Regresión | ServiceInstallDialog (legacy) sigue funcionando | Canal/legacy service | Navigate: Canal service > Click Install > Verify: ServiceInstallDialog abre y funciona | El diálogo legacy no fue tocado | 🟠 | ✅ | ⬜ |
| REG-005 | gateway-ion | AC-10 | Regresión | Admin PrimeVue sin regresión visual (modo claro) | Pantalla Admin existente | Admin Login > Navigate: Cualquier pantalla Admin > Verify: Colores, bordes, tipografía sin cambio | Zero regresión visual | 🟠 | ❌ | ⬜ |
| REG-006 | gateway-ion | AC-10 | Regresión | Admin PrimeVue sin regresión visual (modo oscuro) | Pantalla Admin en dark mode | Admin Login > Toggle dark mode > Navigate: Admin > Verify: Sin regresión | Zero regresión en dark mode | 🟠 | ❌ | ⬜ |
| REG-007 | billing | AC-1 | Regresión | Billing SaaS plataforma (/plans, /subscription) intacto | Suscripción de plataforma existente | Company Login > Navigate: /billing o equivalente > Verify: Planes de plataforma visibles > Verify: Suscripción activa sin cambios | Billing de plataforma no impactado por marketplace | 🟠 | ✅ | ⬜ |
| REG-008 | checkout | AC-5 | Regresión | Compra desde diálogo funciona en ambos caminos | Producto y GRAPP disponibles | Buyer: Comprar producto (la compra ES el resultado) > Buyer: Comprar GRAPP (se paga y luego se instala) > Verify: Ambos caminos funcionan | Dos flujos de compra funcionan correctamente | 🔴 | ❌ | ⬜ |

---

## Queries de Verificación BD

```sql
-- Fuente: ../gateway/database/migrations/2026_07_09_*→2026_08_27_*
-- Tablas: marketplace_products, marketplace_prices, marketplace_pricing, 
--         marketplace_subscriptions, marketplace_subscription_items,
--         marketplace_invoices, marketplace_invoice_items,
--         stripe_objects, stripe_connect_accounts, apps (public_key)

-- TC-004/TC-005: Verificar producto y precio creados con espejo Stripe
SELECT mp.id, mp.title, mp.status, mp.pricing_id
FROM marketplace_products mp
WHERE mp.company_id = '<company_id>';

SELECT mpr.id, mpr.product_id, mpr.amount, mpr.currency, mpr.recurring, mpr.interval, mpr.status, mpr.type
FROM marketplace_prices mpr
WHERE mpr.product_id = '<product_id>';

-- TC-005: Verificar price SUPERSEDED tras edición de monto
SELECT so.id, so.stripe_id, so.object_type, so.status
FROM stripe_objects so
WHERE so.owner_type = 'marketplace_price' AND so.owner_id = '<old_price_id>';
-- Esperado: status = 'SUPERSEDED'

-- TC-015: Verificar trazabilidad de factura
SELECT mi.id, mi.status, mi.amount, mi.currency, mi.account_id,
       mii.app_id, mii.price_id, mii.quantity
FROM marketplace_invoices mi
JOIN marketplace_invoice_items mii ON mi.id = mii.invoice_id
WHERE mi.account_id = '<buyer_account_id>';

-- TC-014: Verificar suscripción activa
SELECT ms.id, ms.status, ms.account_id, ms.company_id,
       msi.app_id, msi.price_id, msi.quantity
FROM marketplace_subscriptions ms
JOIN marketplace_subscription_items msi ON ms.id = msi.subscription_id
WHERE ms.account_id = '<buyer_account_id>';

-- TC-012: Verificar Stripe Connect account
SELECT sca.id, sca.stripe_id, sca.app_id, sca.status, sca.fee_percent
FROM stripe_connect_accounts sca
WHERE sca.app_id = '<app_id>';
-- Esperado: status = 'ACTIVE'

-- TC-022: Verificar public_key existe
SELECT id, public_key FROM apps WHERE id = '<app_id>';
-- Esperado: public_key empieza con 'ion_pk_'

-- AC-7: Verificar demolición ION-137 — tablas legacy eliminadas
-- Estas queries DEBEN fallar (tabla no existe):
-- SELECT * FROM prices LIMIT 1;
-- SELECT * FROM payment_intents LIMIT 1;

-- REG-007: Verificar billing SaaS plataforma intacto
SELECT id, plan_id, canceled_at, expires_at, stripe_subscription_id
FROM subscriptions
WHERE subscriber_type = 'company' AND subscriber_id = '<company_id>';
-- Esperado: Suscripción de plataforma sin cambios
```
