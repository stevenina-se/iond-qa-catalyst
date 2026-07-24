# Code Review QA — IONF-1004 (Iteración 3)

> Generado por `code-review/review` (modo Deployment / Bug Hunting)
> Fecha: 2026-07-14
> Repo: Gateway (PHP legacy) — Branch `IONF-1004`
> Developer: Sonia Vale
> Code Review Dev: Rodolfo Merlo Ali (aprobado 2026-07-14)
> Commit más reciente: `b8d8eb1a` — "Fix update variants and images inaccessible"

---

## Resumen

| Métrica | Valor |
|---------|-------|
| Archivos nuevos/modificados | ~20 archivos (core: 4 clases + 2 traits + 2 main classes) |
| Hallazgos totales | 8 |
| 🔴 Bugs confirmados | 2 |
| 🟠 Riesgos a verificar | 4 |
| 🟡 Observaciones | 2 |
| TCs inyectados en test-matrix | 8 (TC-CR-001 a TC-CR-008) |

---

## Archivos Revisados

| Archivo | Tipo | Cambios Clave |
|---------|------|---------------|
| `app/Classes/Woocommerce/ExportProducts.php` | **NUEVO** | Clase completa: execute(), createProduct(), updateProduct(), buildPayload(), createVariations(), updateVariations(), buildVariationData() |
| `app/Classes/Etsy/ExportProducts.php` | **NUEVO** | Clase completa: execute(), createListing(), updateListing(), uploadImages(), updateInventoryVariants(), activateListing() |
| `app/Classes/Woocommerce/Woocommerce.php` | MODIFICADO | +exportProducts(), +rules('export_products'), +use ProductsServiceTrait, InventoryServiceTrait |
| `app/Classes/Etsy/Etsy.php` | MODIFICADO | +exportProducts(), +rules('export_products'), +use ProductsServiceTrait, InventoryServiceTrait |
| `app/Traits/InventoryServiceTrait.php` | MODIFICADO | +mapExportproductsResponse(), +closeExportProducts() |
| `app/Traits/ProductsServiceTrait.php` | Existente | mapProductResponse() — no modificado |

---

## Hallazgos

### 🔴 BUG-CR-001 — Activación Etsy silenciosa: listing en draft reportado como éxito

**Severidad**: 🔴 Crítico
**Tipo**: BUG CONFIRMADO (estático, reproducible)
**Repo**: Gateway — `app/Classes/Etsy/ExportProducts.php`
**Línea**: ~196-199 (createListing)

**Descripción**:
En `createListing()`, después del flujo de 4 pasos (create → upload images → update inventory → activate), si `activateListing()` falla (HTTP 400/403/etc.), el código solo loguea el error pero **retorna `$this->success()`**. El listing queda en estado `draft` en Etsy (no visible en tienda), pero el webhook enviado a la app origen reporta `status: success`.

```php
$activationResponse = $this->activateListing($listingId);
if ($activationResponse->failed()) {
    Log::error("Error activating Etsy listing {$listingId}: " . $activationResponse->body());
}
// ↓ SIEMPRE retorna success, incluso si la activación falló
return $this->success($response, $product, $variant);
```

**Impacto**: El cliente recibe webhook de éxito pero el producto NO está visible en Etsy. Comportamiento idéntico al patrón del bug persistente OBS-02 de Iter.1/2 (webhook falso positivo).

**TC relacionado**: TC-CR-001

---

### 🔴 BUG-CR-002 — Validación de precio demasiado restrictiva (regex)

**Severidad**: 🔴 Crítico
**Tipo**: BUG CONFIRMADO
**Repo**: Gateway — `app/Classes/Woocommerce/Woocommerce.php` y `app/Classes/Etsy/ExportProducts.php`

**Descripción**:
La validación del campo `price` en variantes usa regex `regex:/^\d+(\.\d{2})$/`. Esto **solo acepta** precios con exactamente 2 decimales (ej: "10.00"). Rechaza:
- `"10"` → rechazado (sin decimales)
- `"10.0"` → rechazado (1 decimal)
- `"10.5"` → rechazado (1 decimal)
- `"10.123"` → rechazado (3 decimales)

Esto es inconsistente con las APIs de WooCommerce y Etsy que aceptan precios en múltiples formatos numéricos. Además, en el payload documentado por la developer se usan precios como `"60.00"` pero un usuario podría enviar `"60"` legítimamente.

**Presente en ambos carts**: Etsy (`validateProduct`) y WC (`rules`).

**Impacto**: Payloads legítimos son rechazados con HTTP 422 sin razón aparente para el usuario.

**TC relacionado**: TC-CR-002

---

### 🟠 BUG-CR-003 — updateVariations WC no retorna variations en webhook de update

**Severidad**: 🟠 High
**Tipo**: RIESGO A VERIFICAR
**Repo**: Gateway — `app/Classes/Woocommerce/ExportProducts.php`

**Descripción**:
En `createProduct()`, el retorno incluye `'variations' => $variationsData` con los IDs de variantes recién creadas. El método `exportProducts()` en `Woocommerce.php` luego incluye esas variations en el webhook:

```php
if (is_array($responseWoo) && !empty($result['variations'])) {
    $responseWoo['variations'] = $result['variations'];
}
```

Sin embargo, `updateProduct()` **NO retorna** el campo `'variations'` en su respuesta. El webhook de update no incluye los IDs de variantes actualizadas. El cliente que hizo update no recibe confirmación de qué variantes se actualizaron.

**Impacto**: El cliente no puede saber qué variantes se actualizaron/crearon en un update. Los `sku_id_channel` de variantes nuevas (creadas durante update) se pierden.

**TC relacionado**: TC-CR-003

---

### 🟠 BUG-CR-004 — Re-upload de imágenes en updateListing Etsy (acumulación)

**Severidad**: 🟠 High
**Tipo**: RIESGO A VERIFICAR
**Repo**: Gateway — `app/Classes/Etsy/ExportProducts.php`

**Descripción**:
`updateListing()` llama a `uploadImages()` con el mismo array de imágenes. Etsy API añade nuevas imágenes al listing sin eliminar las existentes. Si el usuario envía 3 imágenes, después de 2 updates el listing tendrá 9 imágenes.

La función no verifica si las imágenes ya existen ni elimina las anteriores antes de subir.

**Impacto**: Acumulación de imágenes duplicadas en listings. Degradación visual del producto en Etsy.

**TC relacionado**: TC-CR-004

---

### 🟠 BUG-CR-005 — Producto simple con 1 variante: comportamiento ambiguo en WC

**Severidad**: 🟠 Medium
**Tipo**: RIESGO A VERIFICAR
**Repo**: Gateway — `app/Classes/Woocommerce/ExportProducts.php`

**Descripción**:
La condición `count($product['variants']) > 1` determina si un producto es `variable` o `simple` en WooCommerce. Un producto con **exactamente 1 variante** se crea como `simple`:
- `buildPayload()` toma precio, SKU, stock de `$variants[0]` → los aplica al producto principal
- `createVariations()` / `updateVariations()` **NO se ejecuta** para 1 variante

Esto es técnicamente correcto para WC (un producto simple tiene 1 SKU directo), pero:
- Si el cliente envía 1 variante con `sku_id_channel` esperando un update de variante → no se procesa
- Las dimensiones se aplican al producto principal en vez de a la variante

**Impacto**: Comportamiento confuso si el cliente espera que 1 variante se registre como variación.

**TC relacionado**: TC-CR-005

---

### 🟠 BUG-CR-006 — property_id fallback 513 puede causar error en Etsy

**Severidad**: 🟠 Medium
**Tipo**: RIESGO A VERIFICAR
**Repo**: Gateway — `app/Classes/Etsy/ExportProducts.php`

**Descripción**:
En `updateInventoryVariants()`, si el producto no incluye `property_id` en el payload, se usa `[513]` como fallback. El property_id `513` corresponde a una propiedad genérica de Etsy, pero puede no ser válida para todas las taxonomías.

Si el taxonomy_id del producto no acepta property 513, Etsy retorna 400. El flujo de variantes falla silenciosamente.

**Impacto**: Fallo de variantes en ciertas categorías de Etsy sin explicación clara para el usuario.

**TC relacionado**: TC-CR-006

---

### 🟡 BUG-CR-007 — Validación product_id inconsistente entre carts

**Severidad**: 🟡 Low
**Tipo**: OBSERVACIÓN
**Repo**: Gateway — `ExportProducts.php` (ambos carts)

**Descripción**:
- **Etsy**: `products.*.product_id` es `required|integer`
- **WC**: `products.*.product_id` es `integer` (NO required)

El payload documentado por la developer incluye `product_id` en ambos, pero la validación permite omitirlo en WC. Esto no es bloqueante pero es una inconsistencia que puede confundir.

**TC relacionado**: TC-CR-007

---

### 🟡 BUG-CR-008 — WC: `category_id` required en rules pero no siempre aplicable

**Severidad**: 🟡 Low
**Tipo**: OBSERVACIÓN
**Repo**: Gateway — `app/Classes/Woocommerce/Woocommerce.php`

**Descripción**:
Las validation rules de WC incluyen `'products.*.category_id' => 'required|integer'`. Sin embargo, WooCommerce permite crear productos sin categoría (se asigna "Uncategorized" por defecto). Forzar `category_id` como required puede ser innecesario y rechaza payloads válidos.

**TC relacionado**: TC-CR-008

---

## Resumen de TCs Inyectados

| TC ID | Bug/Riesgo | Qué verificar | Prioridad |
|-------|-----------|---------------|-----------|
| TC-CR-001 | BUG-CR-001 | Activación Etsy falla → ¿webhook reporta error o éxito? | 🔴 |
| TC-CR-002 | BUG-CR-002 | Enviar precio sin 2 decimales exactos (ej: "10", "10.5") → ¿422? | 🔴 |
| TC-CR-003 | BUG-CR-003 | Update producto WC con variantes → ¿webhook incluye variations? | 🟠 |
| TC-CR-004 | BUG-CR-004 | Update listing Etsy 2 veces → ¿imágenes se duplican? | 🟠 |
| TC-CR-005 | BUG-CR-005 | Exportar producto WC con exactamente 1 variante → tipo simple correcto | 🟠 |
| TC-CR-006 | BUG-CR-006 | Crear listing Etsy con variantes sin property_id en payload | 🟠 |
| TC-CR-007 | BUG-CR-007 | Enviar payload WC sin product_id → ¿acepta? | 🟡 |
| TC-CR-008 | BUG-CR-008 | Enviar payload WC sin category_id → ¿422? | 🟡 |
