# Acceptance Criteria Consolidados — 86e1y463z (IONF-1088)

> Generado por: test-docs/document (modo AC)  
> Fuentes: Descripción original + 11 comentarios ClickUp + risk-triage.md  
> Fecha: 2026-09-01

---

## AC Originales (del ticket) — ACTUALIZADOS

### AC-1: Motor de recurrencia y trazabilidad financiera
```gherkin
Given una compañía seller tiene un servicio con pricing group, plan y precio configurado
  And la cuenta Stripe Connect del seller está activa con payouts habilitados
When un comprador adquiere el plan vía checkout embebido (Embedded Checkout Connect)
Then el sistema procesa el cobro como direct charge en la cuenta conectada del seller
  And cobra application fee según PLATFORM_FEE_PERCENT (override por seller en stripe_connect_accounts.fee_percent)
  And registra la trazabilidad: marketplace_invoice + marketplace_invoice_items con app_id, price_id, account_id
  And el entitlement se deriva de las líneas de suscripción vivas + one-time pagadas no reembolsadas
  And NO se crean suscripciones nativas de Stripe para controlar recurrencia
```
**Fuente**: AC original actualizado con decisiones de Jose Enrique (2026-08-30) y Enrique (2026-08-31)

---

### AC-2: Stripe como espejo del catálogo (write-through)
```gherkin
Given Stripe está configurado como procesador vía Connect (Standard dashboard)
When el seller crea o edita un producto/precio en el catálogo
Then el sistema hace push a Stripe dentro de la misma transacción (write-through)
  And si Stripe falla, la fila en BD se revierte
  And la BD es la única superficie de edición (no hay pull, ni webhooks de catálogo, ni job de reconciliación)
  And editar un monto (inmutable en Stripe) archiva el price y crea un reemplazo (SUPERSEDED)
  And todos los IDs de Stripe viven centralizados en stripe_objects (morph, stripe_id único)
```
**Fuente**: AC original actualizado con detalles de Enrique (2026-08-31) sobre catalog push

---

### AC-3: Automatización post-pago
```gherkin
Given una compañía adquiere un servicio asociado a una integración (GRAPP)
When el sistema recibe un evento de pago exitoso vía webhook Connect
Then notifica al seller vía apps.webhook_url con contexto completo (pricing, app, form_data)
  And para GRAPPs, el webcomponent <gt-pricing-table> dispara la instalación post-pago
  And la experiencia se mantiene consistente: pagar → instalar
```
**Fuente**: AC original actualizado con decisiones de Jose Enrique (2026-08-30) y Rodolfo (2026-08-31)

---

### AC-4: Gestión de marketplace desde gateway-ion (seller)
```gherkin
Given una compañía accede a gateway-ion como tenant
When navega a la sección de Apps
Then puede gestionar:
  | Sección | Ruta | Funcionalidad |
  | App Stores | /stores | CRUD de stores (apps), hero banner, chips de navegación |
  | Apps Catalog | /apps | Catálogo global de apps, EnableAppsDialog |
  | Pricing Plans | /pricing | Pricing groups CRUD, assign wizard, siblings |
  | Plans Studio | /pricing/:id/plans/:planId/studio | Editor visual: carrusel Embla, precios, features, card preview, form builder |
  | Master Plan | /stores/:id/master-plan/studio | Plan de tienda sin producto en URL |
  | Subscribers | /stores/:id/subscribers | Lista de suscriptores del store |
  | Invoices | /stores/:id/invoices | Facturas del store |
  | Subscriptions | /subscriptions | Ledger company-wide |
  And el guardado es explícito (botón Guardar), NO autosave
  And el servidor es la fuente de verdad (SoT)
  And cada acción está gateada por TENANT_PERMS con tooltip si falta permiso
  And las pantallas usan scope CSS .modern-ui con tokens brand-*/ui-surface-*
```
**Fuente**: AC original expandido masivamente con Jose Enrique (2026-07-27, 2026-08-30)

---

## AC Nuevos (acordados con el equipo)

### AC-5: Webcomponent buyer `<gt-pricing-table>` dual-mode
```gherkin
Given un producto del marketplace tiene planes ACTIVE asignados

Scenario: Modo público (public-key)
  When un visitante accede a una página con <gt-pricing-table public-key="ion_pk_...">
  Then ve el catálogo sin sesión
    And el CTA navega a return_url del backend con ?marketplace_price_id=
    And el destino NUNCA viene de un atributo HTML del embed

Scenario: Modo autenticado (intent secret)
  When un buyer autenticado accede al catálogo vía intent JWT
  Then ve el catálogo con Embedded Checkout Connect
    And el checkout usa stripeAccount = connected account del seller
    And la confirmación es server-side
    And emite purchase-completed sin navegar

Scenario: Visualización de planes
  When el buyer ve la tabla de precios
  Then muestra una sola fila de planes (centrada si caben, scroll horizontal si no)
    And nunca envuelve a una segunda fila
    And cambiar de bucket (Month/Year/Life Time) cambia todas las tarjetas a la vez
    And un plan sin el periodo elegido desaparece de la fila (no se queda con precio vacío)
```
**Fuente**: Jose Enrique (2026-08-30), Rodolfo QA Instructions (2026-08-31)

---

### AC-6: API DevApp M2M con aislamiento
```gherkin
Given una app de terceros tiene token con scopes app:marketplace-*

Scenario: Operaciones permitidas
  When usa el token para acceder a /api/2.0/app/marketplace/*
  Then puede: catálogo, cargo directo, listados de líneas, documentos del comprador, switch, cancelación, portal

Scenario: Aislamiento entre apps
  When App A intenta leer o cancelar una línea vendida por App B
    And ambas operan sobre la misma cuenta compartida del buyer
  Then recibe 404 (no 403 ni éxito)
    And el aislamiento es por app_id en marketplace_invoice_items y marketplace_subscription_items

Scenario: Casos de fallo
  When el token no tiene el scope requerido Then 403
  When usa una cuenta ajena Then 404
  When falta el header Account-Id Then 400
  When intenta mezclar monedas Then 422 con mensaje legible
```
**Fuente**: Rodolfo QA Instructions (2026-08-31)

---

### AC-7: Demolición ION-137 (pagos legacy)
```gherkin
Given el stack ION-137 existía en DEVELOPMENT

When se mergea la rama IONF-1088
Then se eliminan de gateway:
  | Eliminado | Tipo |
  | PriceController | Controller PHP |
  | PaymentController | Controller PHP |
  | PaymentWebhookController | Controller PHP |
  | Price model | Eloquent Model |
  | PaymentIntent model | Eloquent Model |
  | StripeProvider / ProviderInterface | Service PHP |
  | Tablas legacy de pricing | Migración DROP |
  And se eliminan de webcomponents-flow:
  | ServicePaymentForm.vue | Componente Vue |
  | payments.ts | Service TS |
  | models price/marketplace legacy | Modelos TS |
  And NO se restauran estas rutas/componentes bajo ninguna circunstancia
  And ServiceInstallDialog (canales/legacy) NO se toca
```
**Fuente**: Jose Enrique (2026-08-30), commit `b2edfc99` gateway, commit `ccef489` webcomponents

---

### AC-8: Moneda única por buyer×seller
```gherkin
Given Stripe permite una sola moneda por customer
  And el customer es por cuenta conectada (un buyer tiene un Customer por seller)

When un buyer intenta comprar en una moneda diferente a la ya fijada con ese seller
Then recibe un error 422 con mensaje legible
  And NO recibe "internal server error" ni error 500
  And la restricción aplica por empresa vendedora, en todos sus marketplaces
```
**Fuente**: Rodolfo QA Instructions (2026-08-31)

---

### AC-9: Eventos Stripe Connect obligatorios
```gherkin
Given los handlers de webhooks ya están implementados y registrados en flow_binaries

When se despliega el sistema
Then los siguientes eventos DEBEN estar habilitados en el endpoint Connect del dashboard de Stripe:
  | Evento | Consecuencia si falta |
  | checkout.session.expired | Sesión abandonada nunca cierra su factura |
  | customer.subscription.created | Subs creadas desde dashboard no se adoptan |
  | invoice.finalized | Factura solo existe cuando el cobro triunfa |
  And sin el evento habilitado no fallan: simplemente no ocurren (la peor forma de estar roto)
```
**Fuente**: Rodolfo QA Instructions — Pre-requisites (2026-08-31)

---

### AC-10: CSS isolation — sin regresión en Admin
```gherkin
Given las pantallas del marketplace tenant usan el scope .modern-ui

When se renderiza cualquier pantalla PrimeVue de Admin o pantalla sin migrar
Then NO hay desplazamiento visual, cambio de color, cambio de tipografía ni cambio de bordes
  And bg-primary sigue resolviendo a PrimeVue en Admin
  And los tokens brand-* y ui-surface-* solo aplican dentro de .modern-ui
  And el reset base de shadcn está re-escrito a .modern-ui * (no global)
  And esto aplica en modo claro y oscuro
```
**Fuente**: Jose Enrique UX Research (2026-07-27, 2026-08-30)

---

## AC Rechazados o Diferidos

| AC Propuesto | Razón | Estado |
|---|---|---|
| Motor de recurrencia multicanal (Mercado Pago, Binance, etc.) | Solo Stripe en este alcance. Multicanal es futuro | Diferido |
| Merge parcial en PUT (patch) | Es deuda de backend documentada. Este ticket no lo resuelve | Diferido — documentado en risk-triage R-001 |
| Corrección del JOIN `enabled` | Es deuda de backend documentada | Diferido — documentado en risk-triage R-002 |
| Tabla y endpoints de `plan_schedules` | Entidades relacionales deliberadamente no metidas en JSONB. Frontend entrega stub en localStorage | Diferido |
| Parámetro `search` en listados de services | Se ignora en servidor; el buscador no filtra | Diferido |

---

## Transformación AC → Casos de Test

| AC | Happy Path | Edge Cases | Caso Negativo |
|----|-----------|------------|---------------|
| AC-1 | Checkout completo → factura creada con trazabilidad | Dos addons del mismo servicio = 2 subs separadas. Cambio de plan con prorrateo | Checkout sin seller con payouts → rechazado. Amount libre → rechazado |
| AC-2 | Crear producto → espejo en Stripe | Editar monto → archiva price, crea reemplazo SUPERSEDED. Stripe caído → BD revierte | Crear sin Stripe Connect account → 422 |
| AC-3 | Pago exitoso → webhook → instalación GRAPP | GRAPP sin planes ACTIVE → no muestra tabla de precios, instala directo | Webhook del seller falla → ¿retry? |
| AC-4 | CRUD completo de Store → Pricing → Plans Studio → Guardar | Cerrar browser sin guardar → confirmación de navegación. 10+ planes en carrusel | Sin permisos TENANT_PERMS → tooltip, acción bloqueada |
| AC-5 | Tabla de precios: 1 fila, scroll horizontal, cambio de bucket | Plan sin periodo seleccionado → desaparece (no vacío). Bundle público vs gateway | public-key inválido → error legible |
| AC-6 | Token App A: CRUD completo de marketplace | App A lee línea de App B → 404. Misma cuenta, diferente app | Sin scope → 403. Sin Account-Id → 400. Moneda mezclada → 422 |
| AC-7 | Diálogo GRAPP/PDF/producto abre normalmente post-demolición | ServiceInstallDialog (legacy) sigue funcionando | Intentar acceder a rutas legacy eliminadas → 404 (no 500) |
| AC-8 | Buyer compra en USD → OK. Compra en USD de nuevo → OK | Buyer cambia de plan mismo seller misma moneda → OK | Buyer intenta EUR con mismo seller → 422 legible |
| AC-9 | Con 3 eventos habilitados: sesión expirada cierra factura, sub adoptada, factura creada | — | Sin eventos: sesión no cierra, sub no se adopta, factura no existe |
| AC-10 | Admin PrimeVue: mismo look en claro y oscuro post-deploy | Modo oscuro: .dark .modern-ui no leak | bg-primary en Admin resuelve a PrimeVue (no a brand) |
