# Risk Triage — 86e1y463z (IONF-1088)

## Resumen
- Módulo principal: developer-apps (→ Marketplace/Stores)
- Módulos impactados: billing, services, integrations, auth (permisos Laratrust)
- Riesgo general: 🔴 Crítico
- Total superficies funcionales: 8
- Total edge cases identificados: 10
- Total preguntas para Developer: 12
- Contexto de ClickUp: 11 comentarios leídos, **6 divergencias encontradas** (AC nuevos no en descripción original)

---

## Análisis de Lógica de Negocio

| Pregunta | Análisis |
|----------|----------|
| ¿El feature respeta las reglas multi-tenant (company)? | ✅ Sí. El marketplace opera por company (seller). Cada company tiene sus stores, pricing groups y products. El aislamiento es por `company_id` en apps y por `app_id` en líneas de factura. **RIESGO**: La API DevApp M2M aísla por `app_id`, no por company — verificar que un marketplace de una company no puede acceder a datos de otro. |
| ¿Afecta la ejecución de flows/nodos? | ⚠️ Indirectamente. La automatización post-pago notifica al seller vía `apps.webhook_url` que puede disparar instalación de GRAPPs (que son flows). No toca el motor de ejecución directamente. |
| ¿Hay impacto en connectors globales vs company? | ⚠️ Indirectamente. Los services del marketplace pueden ser GRAPPs que usan connectors globales. La instalación post-pago crea integraciones que dependen de connectors. |
| ¿Se tocan datos de ejecución (SQLite) o datos persistentes (PostgreSQL)? | ✅ Solo PostgreSQL. Se crean 7+ tablas nuevas (marketplace_products, marketplace_prices, marketplace_pricing, marketplace_subscriptions, marketplace_invoices, + items, stripe_objects, stripe_connect_accounts). Se eliminan tablas legacy ION-137. |
| ¿Hay impacto en el sistema de permisos por usuario/company? | ✅ Sí. Nuevos permisos Laratrust: `pricing`, `marketplace-product`, `marketplace-billing`, `stripe-connect`. Rutas gateadas por `TENANT_PERMS`. |
| ¿El feature puede romper flujos de e-commerce existentes? | ⚠️ **Sí — demolición ION-137**. Se eliminan PriceController, PaymentController, PaymentWebhookController, ServicePaymentForm. Cualquier flujo que dependiera del stack de pagos legacy se rompe. Es intencional, pero hay que verificar que no hay dependencias ocultas. |

---

## Análisis de Impacto por Módulo

| Área | Impacto | Riesgo |
|------|---------|--------|
| **Frontend gateway-ion** (rutas, vistas, componentes) | MASIVO: +55K LOC. Nuevas rutas /stores, /pricing, /apps, Plans Studio. 119 archivos nuevos en marketplace-store/. Carrusel Embla, form builder, assign wizards, payouts gate. | 🔴 Crítico |
| **Frontend webcomponents-flow** (buyer CE) | ALTO: `<gt-pricing-table>` dual-mode, PaymentForm, PlanCard, GRAPP detail. Bundle CDN separado. Demolición ServicePaymentForm/payments.ts. | 🟠 Alto |
| **API flow_binaries** (endpoints, payloads) | MASIVO: +12K LOC, 51 commits. CRUD catálogo, Stripe Connect, checkout, webhooks, billing ledger, buyer projection, DevApp API. 4 superficies de auth distintas. | 🔴 Crítico |
| **BD PostgreSQL** (tablas, relaciones) | ALTO: 12+ migraciones nuevas. 7+ tablas creadas. Tablas legacy eliminadas. FKs, indexes, `public_key` con default UUID. | 🟠 Alto |
| **BD SQLite** (ejecuciones) | Sin impacto directo | 🟢 Bajo |
| **Stripe** (procesador externo) | ALTO: Connect Standard, direct charges, catalog push write-through, webhooks. Configuración manual requerida (3 eventos). | 🟠 Alto |
| **Auth/Permisos** | MEDIO: Nuevos permisos Laratrust, DevApp scopes, intent JWT, public_key. 4 stacks de auth no mezclables. | 🟡 Medio |
| **Billing SaaS plataforma** | RIESGO REGRESIÓN: `/plans`, `/subscription` no deben ser impactados. Dos stacks de billing en el mismo backend. | 🟠 Alto |

---

## Tabla de Riesgos

| ID | Área | Riesgo | Descripción | Prioridad de testing | Justificación |
|----|------|--------|-------------|---------------------|---------------|
| R-001 | Checkout/CRUD | 🔴 Crítico | **PUT sobrescribe registro completo** — un patch parcial borra título, descripción o `configuration` en app_setup, marketplace_product y marketplace_price. Es deuda backend documentada. | 1 | Afecta TODO el CRUD. Cualquier formulario mal implementado corrompe datos silenciosamente. |
| R-002 | Catálogo | 🔴 Crítico | **JOIN `enabled` confunde "vinculado" con "activo"** — `LEFT JOIN` fija `AND app_setup.status = 'ACTIVE'` como literal. Desactivar un producto lo expulsa de la lista y del conteo. Para el usuario, desactivar es indistinguible de borrar. | 1 | UX engañosa que puede causar pérdida percibida de datos. |
| R-003 | Webhooks | 🔴 Crítico | **3 eventos Stripe Connect no habilitados = silenciosamente roto** — Sin `checkout.session.expired`: sesiones abandonadas no cierran factura. Sin `customer.subscription.created`: subs del dashboard no se adoptan. Sin `invoice.finalized`: factura solo existe cuando cobro triunfa. | 1 | Todo **parece** funcionar pero no persiste. Es la peor forma de estar roto. |
| R-004 | Checkout | 🟠 Alto | **Una moneda por buyer×seller** — Un buyer queda fijado a una moneda por seller. Intentar comprar en otra moneda debe retornar 422 legible, no 500. | 2 | Error de UX crítico si retorna 500 genérico. |
| R-005 | API DevApp | 🟠 Alto | **Aislamiento entre apps** — Token de App A no puede leer/cancelar líneas vendidas por App B sobre la misma cuenta compartida. Debe dar 404, no 403 ni éxito. | 2 | Fallo de aislamiento = leak de datos financieros entre marketplaces. |
| R-006 | Stripe Connect | 🟠 Alto | **Catalog push write-through** — Si Stripe falla, la fila en BD se revierte. Sin fallback, retry ni modo degradado. | 3 | Un error transitorio de Stripe puede hacer que el seller "pierda" un producto/precio que acababa de crear. |
| R-007 | UI Seller | 🟠 Alto | **CSS isolation** — Tokens `brand-*`/`ui-surface-*` bajo `.modern-ui`. Si escapan al scope global, repintan 14+ pantallas PrimeVue de Admin sin que nadie lo note. | 3 | Regresión visual silenciosa. El bug aparece y desaparece según el orden de carga de CSS en el build. |
| R-008 | Regresión | 🟠 Alto | **Billing SaaS de plataforma** — `/plans` y `/subscription` (billing de plataforma) comparten backend con marketplace Connect. No deben impactarse mutuamente. | 3 | Dos stacks de billing en `flow_binaries`. Un leak de lógica entre ellos rompe la monetización de la plataforma. |
| R-009 | UI Seller | 🟡 Medio | **`gateway-ion` type-check falla** — `PlansStudioStyleInspector.spec.ts:134` tiene un cast incorrecto de `siblingPlans`. Compilación con errores de TypeScript. | 4 | Puede haber errores de runtime no detectados si el type-check no pasa. |
| R-010 | UI Buyer | 🟡 Medio | **Build de `webcomponents-flow` no verificado** — `pnpm type-check` y `build-pricing` no se corrieron en el entorno de desarrollo reportado. | 4 | El bundle CDN podría no compilar en producción. |

---

## Edge Cases Identificados

| EC | Superficie | Descripción | Prioridad |
|----|-----------|-------------|-----------|
| EC-001 | Checkout | Comprar **dos addons** del mismo servicio → deben ser 2 suscripciones separadas (Stripe rechaza precios duplicados en una sola). Cancelar uno, el otro sigue vivo. | 🔴 |
| EC-002 | Checkout | Cambiar de plan y verificar **prorrateo** en factura siguiente. | 🟠 |
| EC-003 | API DevApp | Con token de App A, intentar **leer y cancelar** línea vendida por App B sobre la misma cuenta compartida → 404. | 🔴 |
| EC-004 | API DevApp | Casos de fallo: 403 sin scope, 404 cuenta ajena, 400 sin header `Account-Id`, 422 mezcla monedas. | 🟠 |
| EC-005 | Webhooks | **Reconciliación**: cambiar precio de un item desde dashboard Stripe → línea local sigue el precio nuevo con el mismo `si_`. | 🟠 |
| EC-006 | Webhooks | **Reconciliación**: quitar item desde dashboard Stripe → queda con `removed_at` sin desaparecer de facturas viejas. | 🟠 |
| EC-007 | Regresión WC | Diálogo abre igual para grapps, PDF y productos. `ServiceInstallDialog` (canales/legacy) no se toca. | 🟡 |
| EC-008 | Regresión WC | Producto sin `rating`, `system_requirements` ni apps declaradas renderiza igual que antes. | 🟡 |
| EC-009 | Catálogo | `prices-bulk` atómico `{ create, update, delete }` — si falla uno, todos se revierten. | 🟠 |
| EC-010 | Billing | Factura reembolsada sigue siendo `paid`. Refund y dispute son marcas de tiempo `set-once`, no estados. Nunca desaparecen de facturas viejas. | 🟠 |

---

## Preguntas para el Developer

### [LÓGICA DE NEGOCIO]

1. **Aislamiento multi-company**: ¿Un seller (company A) puede ver o acceder a los pricing groups, products o invoices de otro seller (company B)? ¿El aislamiento es puramente por `company_id` en la query o hay middleware adicional?

2. **Billing SaaS vs Marketplace**: ¿Hay algún punto donde la lógica de billing de plataforma (`/plans`, `/subscription`) y la de marketplace Connect comparten código, tablas o servicios? ¿Cómo se asegura que no se contaminen?

3. **Entitlement derivado**: El derecho de uso se calcula de las líneas de suscripción vivas + one-time pagadas no reembolsadas. ¿Hay un endpoint que exponga el entitlement calculado, o cada consumidor lo deriva por su cuenta? ¿Puede haber inconsistencia entre cálculos?

### [EDGE CASES]

4. **Sesión abandonada**: Sin el evento `checkout.session.expired`, ¿la factura queda `draft` indefinidamente? ¿Hay un job de limpieza o depende exclusivamente del webhook?

5. **Onboarding incompleto**: Si un seller inicia el onboarding de Stripe Connect pero no lo completa, ¿qué pasa con los productos/precios que ya creó en BD? ¿Se puede vender sin `charges_enabled`?

6. **Refund parcial**: Si Stripe envía un refund parcial vía webhook, ¿el entitlement se revoca completamente o proporcionalmente? (El modelo dice refund = marca set-once, ¿aplica para parciales?)

7. **Customer por seller**: Un buyer tiene un Customer por seller, creado lazy. ¿Qué pasa si el mismo buyer compra en dos marketplaces del mismo seller? ¿Comparten Customer o se crean dos?

### [INTEGRACIÓN]

8. **`apps.webhook_url` post-pago**: ¿El payload del webhook al seller incluye suficiente contexto para que la app vendedora pueda disparar la instalación sin un round-trip adicional? ¿Hay retry si el webhook del seller falla?

9. **Build de bundles**: ¿`build-pricing` y `build-gateway` son independientes? ¿Puede desplegarse uno sin el otro? ¿Hay versionamiento del CDN?

10. **Migraciones sin rollback**: Las migraciones `drop_legacy_pricing_tables` son destructivas. ¿Existe un plan de rollback si se necesita revertir el deploy? ¿Las tablas se respaldan antes?

### [FRONTEND]

11. **Plans Studio guardado**: Con el modelo de "Guardar explícito", ¿qué pasa si el usuario cierra el browser sin guardar? ¿Hay confirmación de navegación? ¿El draft local persiste entre sesiones o solo durante la sesión actual?

12. **Carrusel de planes buyer**: La tabla de precios muestra una sola fila con scroll horizontal. ¿Qué pasa con 10+ planes? ¿Hay un límite práctico de planes por pricing group?

---

## Contexto del Ticket (ClickUp)

### Divergencias entre descripción y comentarios

| # | Divergencia | Impacto |
|---|------------|---------|
| 1 | AC originales hablan de "motor propio de recurrencia" sin mencionar Stripe Connect ni direct charges | El modelo de negocio real es Stripe Connect, no un motor de pagos genérico |
| 2 | AC originales mencionan "interfaz multicanal de pagos" pero el ticket solo implementa Stripe | Solo Stripe en este alcance; multicanal es futuro |
| 3 | No hay AC sobre API DevApp M2M ni aislamiento entre apps | Superficie completa no cubierta por AC originales |
| 4 | No hay AC sobre demolición ION-137 | Es un breaking change fundamental no documentado en AC |
| 5 | No hay AC sobre el webcomponent `<gt-pricing-table>` ni sus dos modos | Superficie buyer completamente ausente de AC |
| 6 | No hay AC sobre CSS isolation ni regresión en Admin | Riesgo de regresión visual silenciosa |

### Últimas decisiones relevantes

- **Jose Flores (2026-08-24)**: Naming final de menú (Apps: App Stores, Pricing Plans) y tipos de apps
- **Jose Enrique (2026-08-30)**: UX Research completo con hallazgos arquitectónicos y requerimientos de implementación
- **Rodolfo (2026-08-31)**: QA Instructions detalladas con pre-requisitos de deployment, testing steps por superficie, y 7 videos de demo
- **Enrique (2026-08-31)**: Resumen de cambios backend IONF-1089 con modelo Connect, espejo de catálogo, checkout, ledger y webhooks

---

## Recomendación

### Áreas que requieren más atención (orden de prioridad de testing)

1. **🔴 Webhooks + Eventos Stripe** (R-003): Es la forma más peligrosa de fallo — todo parece funcionar pero no persiste. Probar con y sin los 3 eventos habilitados.

2. **🔴 Aislamiento DevApp** (R-005, EC-003): Fallo de aislamiento es un leak de datos financieros. Probar exhaustivamente con 2 apps sobre la misma cuenta.

3. **🔴 CRUD con PUT completo** (R-001): Probar que formularios reenvían registro completo. Un campo omitido = dato borrado.

4. **🟠 Checkout buyer** (R-004, EC-001, EC-002): Flujo de compra end-to-end con tarjeta de prueba, prorrateo, addons duplicados, mezcla de monedas.

5. **🟠 Regresión ION-137** (AC-7, EC-007, EC-008): Verificar que diálogos de GRAPP/PDF/productos siguen funcionando tras la demolición.

6. **🟠 Billing SaaS intacto** (R-008): Verificar que `/plans` y `/subscription` de plataforma no fueron afectados.

7. **🟠 CSS isolation** (R-007): Verificar visualmente que Admin y pantallas PrimeVue sin migrar no tienen regresión.
