# Risk Triage — IONF-1004 (Iteración 3)

> Generado por `test-docs/prioritize`
> Fecha: 2026-07-14
> Ticket: Soporte de Listings para Etsy y WooCommerce en Gateway
> Contexto: Iteración 3 después de 2 rechazos previos con 6 bugs históricos

---

## Resumen de Riesgo

| Métrica | Valor |
|---------|-------|
| Riesgo global | 🔴 ALTO |
| Razón principal | 2 rechazos previos, bug persistente (OBS-02), complejidad multi-cart |
| Iteración | 3 (bugs previos deben re-verificarse todos) |
| Repos afectados | Gateway (PHP legacy) — único repo |
| Superficie de impacto | Integrations (export_products, get_categories) |
| Tipo de cambio | New Feature + 3 rondas de bugfixes |

---

## Factores de Riesgo

### 🔴 Riesgo Alto

| # | Factor | Descripción | Impacto | Probabilidad |
|---|--------|-------------|---------|-------------|
| R-01 | **Bug persistente (OBS-02)** | El bug de imágenes inaccesibles en Etsy persistió de Iter.1 a Iter.2. Requiere verificación exhaustiva de que `uploadImages()` corregido realmente interrumpe el flujo | Listing fantasma en draft sin imágenes → cliente cree que exportó pero no | Alta |
| R-02 | **Duplicación de variantes WC (OBS-01 Iter.2)** | El fix crea `updateVariations()` separando create/update por `sku_id_channel`. Si el campo viene vacío en un update legítimo → crea variante nueva en vez de actualizar | Datos duplicados en tienda del cliente | Media |
| R-03 | **Validación de precio regex** | El precio usa regex `/^\d+(\.\d{2})$/` — rechaza precios como "10.0", "10", "10.123". Demasiado restrictivo vs payload real | Rechazo inesperado de payloads válidos | Alta |
| R-04 | **Activación silenciosa si falla** | En `createListing()`, si `activateListing()` falla → se loguea error pero retorna `success()`. El listing queda en draft pero se reporta éxito | Webhook falso positivo — cliente cree que el listing está activo | Alta |

### 🟠 Riesgo Medio

| # | Factor | Descripción | Impacto | Probabilidad |
|---|--------|-------------|---------|-------------|
| R-05 | **Variantes solo con > 1** | La condición `count($product['variants']) > 1` en WC ignora variantes cuando hay exactamente 1. El producto simple toma datos de `$variants[0]` en `buildPayload` pero no pasa por `createVariations()` | Para productos de 1 variante: funciona como simple. Si el cliente envía 1 variante esperando que se registre como variante en WC → no se registra | Media |
| R-06 | **property_id hardcodeado 513** | En Etsy `updateInventoryVariants`, si `property_id` no viene en el payload → usa `[513]` como fallback. Este ID puede no existir en la taxonomía del producto | Error 400 de Etsy si la property no es válida para ese taxonomy_id | Media |
| R-07 | **Dimensiones WC: `weight.unit` ignorado** | WC `buildVariationData()` toma `$weightObj['value']` pero ignora `$weightObj['unit']`. WC API acepta weight pero no especifica unidad en la API v3 (la unidad se configura globalmente en WC Settings) | Inconsistencia si la tienda WC usa kg pero el cliente envía lb | Baja |
| R-08 | **Images se re-suben en update Etsy** | `updateListing()` llama a `uploadImages()` — sube imágenes de nuevo en cada update. No elimina las anteriores. Puede acumular imágenes duplicadas | Imágenes duplicadas en listings existentes | Media |
| R-09 | **updateVariations WC: no retorna variaciones en respuesta** | En `updateProduct()`, después de `updateVariations()`, no se incluye `variations` en el retorno como sí hace `createProduct()` | Webhook de update no incluye IDs de variaciones para futuro update | Media |

### 🟡 Riesgo Bajo

| # | Factor | Descripción | Impacto | Probabilidad |
|---|--------|-------------|---------|-------------|
| R-10 | **`product_id` required en Etsy pero no en WC** | Etsy valida `products.*.product_id` como required, WC lo valida como `integer` (no required). Inconsistencia entre carts | Confusión del cliente al usar mismo payload para ambos | Baja |
| R-11 | **Etsy title truncado a 140 chars** | `substr($product['title'], 0, 140)` — truncamiento silencioso sin aviso al cliente | Título cortado sin warning | Baja |
| R-12 | **Aspects truncados a 20 chars en Etsy** | `substr($propValue, 0, 20)` en `updateInventoryVariants` — valores de property truncados | Variante con nombre cortado sin warning | Baja |
| R-13 | **`updateInvList` compartido en trait** | `InventoryServiceTrait` usa `$this->updateInvList` para `sync_inventory` Y `export_products`. Si ambas acciones corren cerca → posible contaminación cruzada | Datos mezclados en webhook | Muy baja |

---

## Mapa de Impacto

```
export_products (acción)
    ├── WooCommerce
    │   ├── createProduct() → buildPayload() + createVariations()
    │   │   └── Riesgos: R-03 (precio regex), R-05 (1 variante), R-07 (weight unit)
    │   ├── updateProduct() → buildPayload() + updateVariations()
    │   │   └── Riesgos: R-02 (duplicación), R-09 (no retorna variations)
    │   └── Webhook vía InventoryServiceTrait
    │       └── Riesgo: R-13 (array compartido)
    │
    ├── Etsy
    │   ├── createListing() → uploadImages() → updateInventoryVariants() → activateListing()
    │   │   └── Riesgos: R-01 (images fail), R-04 (activación silenciosa), R-06 (property_id 513)
    │   ├── updateListing() → uploadImages() → updateInventoryVariants()
    │   │   └── Riesgos: R-08 (images duplicadas)
    │   └── Webhook vía InventoryServiceTrait
    │       └── Riesgo: R-13 (array compartido)
    │
    └── Validación (rules)
        └── Riesgos: R-03 (regex precio), R-10 (product_id inconsistente)
```

---

## Recomendación de Priorización

1. **PRIMERO**: Re-verificar los 6 bugs históricos — son la causa de los 2 rechazos
2. **SEGUNDO**: Verificar R-04 (activación silenciosa) — potencial nuevo bug crítico
3. **TERCERO**: Verificar R-03 (regex precio) — potencial rechazo inesperado de payloads
4. **CUARTO**: Edge cases de variantes (R-02, R-05, R-09)
5. **ÚLTIMO**: Riesgos bajos (R-10, R-11, R-12)
