# Test Matrix — IONF-1004 (Iteración 3)

> Generada por `test-docs/document` (modo matrix) — Iteración 3
> Fecha: 2026-07-14
> Módulo: Integrations (Gateway legacy — PHP)
> Ticket: Soporte de Listings para Etsy y WooCommerce en Gateway
> Historial: Iteración 1 (4 bugs, rechazado) → Iteración 2 (2 bugs, rechazado) → **Iteración 3**
> Archivos anteriores: `test-matrix-v2.md` (Iter. 2), `test-matrix-v2.csv`

## Resumen

| Métrica | Valor |
|---------|-------|
| Total de casos | 38 |
| Re-tests de bugs previos | 6 |
| TCs de Code Review (nuevos) | 8 |
| Happy path | 8 |
| Edge cases | 7 |
| Negativos | 5 |
| Regresión | 4 |
| Cobertura de AC | 5/5 |

---

## Acceptance Criteria (Referencia)

| ID | Descripción | Origen |
|----|-------------|--------|
| AC-1 | Recepción exitosa y mapeo a WooCommerce usando procesamiento por lotes → webhook de éxito | Ticket (Gherkin) |
| AC-2 | Recepción de payload inválido → proceso se detiene antes de lotes → **422 sync** (sin webhook — override técnico) | Ticket (Gherkin) + Override en Análisis Técnico |
| AC-3 | Manejo de Rate Limit 429 en Etsy → abort + webhook de fallo | Ticket (Gherkin) |
| AC-4 | Acción `get_categories` sync para WooCommerce (consultar categorías del cart) | Análisis Técnico (adicionada) |
| AC-5 | Acción `get_categories` sync para Etsy (taxonomy global) | Análisis Técnico (adicionada) |

> **Nota**: AC-2 fue overrideado por el análisis técnico: validation error = 422 sync sin webhook. Webhook solo para flujo async (job).

---

## 🔴 BLOQUE RE-TEST — Bugs de Iteraciones Anteriores (OBLIGATORIO — todos 🔴)

> ⚠️ Estos 6 casos son la razón de los 2 rechazos previos. Deben verificarse PRIMERO y TODOS deben pasar.

| ID | Bug Original | Cart | Caso de Re-test | Pasos | Resultado Esperado | Prioridad | Estado |
|----|-------------|------|----------------|-------|-------------------|-----------|--------|
| RT-001 | Iter.1 OBS-01 | Etsy | **category_id validado como required** | 1. Enviar POST export_products a Etsy SIN campo `category_id` 2. Verificar respuesta | HTTP 422 con mensaje claro indicando que category_id es requerido. NO se crea listing en Etsy. NO se envía webhook | 🔴 | ⬜ Pendiente |
| RT-002 | Iter.1+2 OBS-02 **PERSISTENTE** | Etsy | **uploadImages() con URL inaccesible interrumpe flujo** | 1. Enviar POST export_products a Etsy con `images: [{"src": "https://url-inexistente.com/img.jpg"}]` 2. Verificar estado del listing en Etsy 3. Verificar contenido del webhook | El flujo debe DETENERSE en el paso de images. No se ejecuta updateInventoryVariants ni activateListing. El webhook reporta ERROR (no éxito). El listing NO queda en draft como éxito fantasma | 🔴 | ⬜ Pendiente |
| RT-003 | Iter.1 OBS-03 | Etsy+WC | **Dimensiones y peso se mapean correctamente** | 1. Enviar POST a Etsy con `dimensions: {length: 21, width: 22, Height: 23, unit: "in"}` y `weight: {value: 24, unit: "lb"}` 2. GET listing en Etsy → verificar item_length, item_width, item_height, item_weight, item_dimensions_unit, item_weight_unit 3. Repetir para WC → verificar dimensions y weight | **Etsy**: item_length=21, item_width=22, item_height=23, item_dimensions_unit="in", item_weight=24, item_weight_unit="lb". **WC**: dimensions.length="21", width="22", height="23", weight="24" | 🔴 | ⬜ Pendiente |
| RT-004 | Iter.1 OBS-04 | Etsy | **Múltiples variantes registradas en inventory** | 1. Enviar POST a Etsy con producto de 3 variantes (con aspects y property_id) 2. GET /listings/{id}/inventory 3. Verificar que los 3 SKUs están registrados con sus precios y cantidades | Los 3 productos aparecen en el inventario con property_values correctos. SKU, precio y quantity coinciden con payload enviado | 🔴 | ⬜ Pendiente |
| RT-005 | Iter.2 OBS-01 | WC | **Actualización NO duplica variantes** | 1. Crear producto con 2 variantes → obtener product_id_channel y sku_id_channel de cada variante 2. Enviar POST de update con product_id_channel + sku_id_channel en cada variante, modificando solo el nombre 3. Verificar producto en WC | Variantes actualizadas IN-PLACE. NO se crean variantes nuevas. Total de variantes = 2 (no 4). Datos actualizados correctamente | 🔴 | ⬜ Pendiente |
| RT-006 | Iter.2 OBS-02 | Etsy | **Mismo caso que RT-002 — verificación doble del bug persistente** | 1. Enviar POST a Etsy con imagen válida + imagen inaccesible (2 imágenes) 2. Verificar que la imagen válida se sube 3. Verificar que la inaccesible no causa crash 4. Verificar webhook refleja realidad | Si al menos 1 imagen se sube → flujo continúa (uploadedCount > 0). Si 0 imágenes se suben → flujo se detiene. Webhook refleja el estado real | 🔴 | ⬜ Pendiente |

---

## Test Matrix — Export Products WooCommerce

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-001 | Integrations | AC-1 | Happy Path | Exportar producto simple a WooCommerce | Integración WC activa, queue workers corriendo | 1. POST export_products con 1 producto simple (1 variante) 2. Esperar procesamiento 3. Verificar webhook 4. Verificar producto en WC | Producto creado tipo `simple`. Datos correctos. Webhook éxito con campo `response` | 🔴 | ✅ | ⬜ Pendiente |
| TC-002 | Integrations | AC-1 | Happy Path | Exportar producto con variantes a WC | Integración WC activa | 1. POST con producto de 3+ variantes con SKUs, precios, quantities diferentes 2. Verificar en WC tipo `variable` con variaciones | Producto variable creado. Cada variante con SKU, precio, quantity. Webhook incluye `variations` con IDs | 🔴 | ✅ | ⬜ Pendiente |
| TC-003 | Integrations | AC-1 | Happy Path | Batch de múltiples productos a WC | Chunk size configurado | 1. POST con 5+ productos en array `products` 2. Verificar procesamiento batch 3. Verificar todos en WC | Todos creados correctamente. Webhook con resultados por producto | 🔴 | ✅ | ⬜ Pendiente |
| TC-004 | Integrations | AC-1 | Edge Case | Actualizar producto existente por SKU en WC | Producto existente en WC con product_id_channel | 1. POST con product_id_channel del producto existente + datos modificados 2. Verificar update en WC | Producto ACTUALIZADO, no duplicado. Datos modificados reflejados | 🟠 | ✅ | ⬜ Pendiente |
| TC-005 | Integrations | AC-1 | Edge Case | Campos opcionales vacíos/omitidos en WC | Integración WC activa | 1. POST con product_id_channel vacío, sin aspects, sin dimensions, sin weight 2. Verificar procesamiento | Producto creado sin error. Campos opcionales no causan 422 | 🟠 | ❌ | ⬜ Pendiente |

## Test Matrix — Export Products Etsy

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-006 | Integrations | AC-1 | Happy Path | Exportar producto simple a Etsy (4 pasos) | Integración Etsy, category_id válido, shipping profile, return policy | 1. POST con 1 producto + 1 variante + image válida + category_id leaf 2. Verificar 4 pasos: POST /listings → POST /images → PUT /inventory → PATCH /listings (active) 3. Verificar estado=active en Etsy | Producto active en Etsy. Imagen subida. Inventory configurado. Webhook éxito | 🔴 | ❌ | ⬜ Pendiente |
| TC-007 | Integrations | AC-1 | Happy Path | Exportar producto con múltiples imágenes a Etsy | Producto con 3+ URLs válidas | 1. POST con producto de 3 imágenes válidas 2. Verificar listing en Etsy | Las 3 imágenes subidas. Rank asignado (1,2,3) | 🟠 | ❌ | ⬜ Pendiente |
| TC-008 | Integrations | AC-3 | Happy Path | Rate Limit 429 en Etsy | Condiciones de throttle | 1. POST batch grande a Etsy 2. Esperar 429 de Etsy | Gateway aborta. Webhook de fallo con detalle de Rate Limit | 🔴 | ❌ | ⬜ Pendiente |
| TC-009 | Integrations | AC-1 | Edge Case | Update producto existente por product_id_channel en Etsy | Listing existente con product_id_channel | 1. POST con product_id_channel del listing existente + datos modificados | PATCH al listing. Datos actualizados. No se crea listing nuevo | 🟠 | ❌ | ⬜ Pendiente |

## Test Matrix — Get Categories (Sync)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-010 | Integrations | AC-4 | Happy Path | get_categories WooCommerce | Integración WC activa con categorías | 1. POST con resource `get_categories` | Respuesta sync con lista de categorías e IDs | 🟠 | ✅ | ⬜ Pendiente |
| TC-011 | Integrations | AC-5 | Happy Path | get_categories Etsy (taxonomy) | Integración Etsy activa | 1. POST con resource `get_categories` | Respuesta sync con taxonomy global de Etsy | 🟠 | ✅ | ⬜ Pendiente |

## Test Matrix — Validación y Errores

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-012 | Integrations | AC-2 | Negativo | Payload inválido — estructura incorrecta | Integración activa | 1. POST sin campo `products`, array vacío, JSON malformado | HTTP 422 sync. Sin webhook. Mensaje de validación | 🔴 | ✅ | ⬜ Pendiente |
| TC-013 | Integrations | AC-2 | Negativo | Campos requeridos faltantes | Integración activa | 1. POST sin `title` 2. POST variante sin `sku` 3. POST variante sin `price` 4. POST variante sin `quantity` | HTTP 422 para cada caso. Indica campo faltante | 🔴 | ✅ | ⬜ Pendiente |
| TC-014 | Integrations | AC-2 | Negativo | Gateway-key inválido | Key inexistente | 1. POST a `/api/2.0/app/integrations/{invalid-key}/action` | HTTP 401/403/404. No se procesa nada | 🟠 | ✅ | ⬜ Pendiente |
| TC-015 | Integrations | AC-1 | Negativo | category_id inválido en WC | WC activa | 1. POST con category_id inexistente en tienda WC | Producto se crea (WC asigna a Uncategorized si no encuentra) o error claro | 🟠 | ❌ | ⬜ Pendiente |
| TC-018 | Integrations | AC-2 | Negativo | Resource action no existente | Integración activa | 1. POST con resource `invalid_action` | Error de acción no reconocida | 🟡 | ✅ | ⬜ Pendiente |

## Test Matrix — Edge Cases Adicionales

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-016 | Integrations | AC-3 | Edge Case | Fallo parcial en lote mixto | Batch con productos válidos + inválidos | 1. Enviar 3 productos: 1 válido, 1 con imagen rota, 1 con category_id inválido | Producto válido se crea. Los otros reportan error. Webhook con resultados parciales. Sin rollback | 🟠 | ❌ | ⬜ Pendiente |
| TC-017 | Integrations | AC-1 | Edge Case | Imágenes URL inaccesible en Etsy (parcial) | Etsy activa, 3 imágenes: 2 válidas + 1 inaccesible | 1. POST con 2 imgs válidas + 1 URL rota 2. Verificar listing y count de imágenes | Las 2 válidas se suben. La inaccesible se omite. uploadedCount=2 → flujo continúa. Listing se activa | 🟠 | ❌ | ⬜ Pendiente |
| TC-019 | Integrations | AC-1 | Edge Case | Campo `response` estandarizado | WC y Etsy activas | 1. Exportar a WC → capturar webhook 2. Exportar a Etsy → capturar webhook 3. Comparar estructura | Ambos usan campo `data_response` con estructura genérica | 🟠 | ❌ | ⬜ Pendiente |
| TC-020 | Integrations | AC-1 | Edge Case | Currency desde config de conexión | Currency configurada en cart | 1. Enviar producto con precio sin currency 2. Verificar en cart destino | Usa currency de la configuración del cart | 🟡 | ❌ | ⬜ Pendiente |

---

## 🔍 BLOQUE CODE REVIEW — TCs Inyectados desde Bug Hunting

> Estos TCs provienen del code-review-qa.md y verifican los hallazgos del análisis estático de código.

| ID | Bug Origen | Cart | Caso de Test | Pasos | Resultado Esperado | Prioridad | Estado |
|----|-----------|------|-------------|-------|-------------------|-----------|--------|
| TC-CR-001 | BUG-CR-001 | Etsy | **Activación falla → ¿webhook reporta error?** | 1. Crear condición donde activateListing falle (ej: listing sin return_policy en shop que lo requiere, o sin shipping_profile) 2. Verificar webhook enviado | Si la activación falla, el webhook debe incluir indicación de que el listing quedó en draft. NO debe reportar éxito completo | 🔴 | ⬜ Pendiente |
| TC-CR-002 | BUG-CR-002 | Ambos | **Precio sin 2 decimales exactos → ¿422?** | 1. POST a WC con price: "10" 2. POST a WC con price: "10.5" 3. POST a Etsy con price: "60" 4. Verificar respuesta | Verificar si la regex `/^\d+(\.\d{2})$/` rechaza precios válidos. Si rechaza → es bug. Documentar formatos aceptados reales | 🔴 | ⬜ Pendiente |
| TC-CR-003 | BUG-CR-003 | WC | **Update WC con variantes → webhook incluye variations?** | 1. Crear producto con variantes → obtener IDs 2. Actualizar producto con sku_id_channel 3. Verificar contenido del webhook de update | El webhook de update debería incluir `variations` con IDs actualizados. Si no los incluye → documentar como observación | 🟠 | ⬜ Pendiente |
| TC-CR-004 | BUG-CR-004 | Etsy | **Update listing Etsy 2x → ¿imágenes duplicadas?** | 1. Crear listing con 2 imágenes 2. Update mismo listing con las mismas 2 imágenes 3. Verificar total de imágenes en Etsy | Después del update NO deben haber 4 imágenes. Si hay 4 → documentar como bug de acumulación | 🟠 | ⬜ Pendiente |
| TC-CR-005 | BUG-CR-005 | WC | **Producto WC con exactamente 1 variante → tipo simple** | 1. POST con producto de 1 variante 2. Verificar en WC: ¿tipo simple o variable? 3. Verificar que price, SKU, stock se aplican al producto | Producto tipo `simple`. Price/SKU/stock del producto tomados de la variante. No se crean variation entries | 🟠 | ⬜ Pendiente |
| TC-CR-006 | BUG-CR-006 | Etsy | **Variantes Etsy sin property_id en payload** | 1. POST a Etsy con producto de 2+ variantes con aspects PERO sin campo `property_id` en el payload principal 2. Verificar si usa fallback 513 3. Verificar inventario | Si el category_id acepta property 513 → funciona. Si no → documenta error de Etsy (400). Verificar con una categoría que no acepte 513 | 🟠 | ⬜ Pendiente |
| TC-CR-007 | BUG-CR-007 | WC | **WC sin product_id en payload → ¿acepta?** | 1. POST a WC omitiendo campo `product_id` 2. Verificar si se crea producto | Debería aceptar (WC rules no lo marca required). Documentar comportamiento | 🟡 | ⬜ Pendiente |
| TC-CR-008 | BUG-CR-008 | WC | **WC sin category_id → ¿422 innecesario?** | 1. POST a WC omitiendo campo `category_id` 2. Verificar respuesta | HTTP 422 por rules (`required|integer`). Si WC API acepta sin categoría → documentar como observación sobre validación excesiva | 🟡 | ⬜ Pendiente |

---

## Casos de Regresión

| ID | Módulo | Caso de regresión | Por qué podría romperse | Prioridad | Estado |
|----|--------|-------------------|------------------------|-----------|--------|
| REG-001 | Integrations | Export products de eBay sigue funcionando | Los nuevos adapters comparten InventoryServiceTrait y patrón similar. Cambios en infra de batching podrían afectar | 🔴 | ⬜ Pendiente |
| REG-002 | Integrations | Motor de webhooks funciona para otras acciones | Los nuevos adapters usan sendWebhook. Verificar que sync_inventory y get_products siguen disparando webhooks | 🟠 | ⬜ Pendiente |
| REG-003 | Integrations | Endpoints App API existentes no afectados | Nuevas acciones registradas no deben romper acciones existentes | 🟠 | ⬜ Pendiente |
| REG-004 | Integrations | Feature hidden — no aparece sin habilitación | La feature no debe ser visible para tenants sin ella | 🟡 | ⬜ Pendiente |

---

## Queries de Verificación BD

> **Nota**: Este ticket NO tiene migraciones de BD. La verificación es sobre el comportamiento del job queue y logs.

```sql
-- RT-001/TC-012: Verificar que NO se creó job para payload inválido (422 sync)
SELECT * FROM jobs WHERE payload LIKE '%export_products%' ORDER BY created_at DESC LIMIT 1;
-- Esperado: No hay job nuevo (validación falló sync antes de encolar)

-- TC-001/TC-006: Verificar que el job fue encolado correctamente
SELECT * FROM jobs WHERE payload LIKE '%export_products%' ORDER BY created_at DESC LIMIT 5;
-- Esperado: Job creado con payload correspondiente

-- TC-003: Verificar procesamiento en lotes
SELECT * FROM jobs WHERE payload LIKE '%export_products%' AND attempts > 0 ORDER BY created_at DESC LIMIT 10;
-- Esperado: Jobs procesados (attempts > 0), sin failed_at

-- REG-001: Verificar que eBay export sigue funcionando
SELECT * FROM jobs WHERE payload LIKE '%export_products%' AND payload LIKE '%ebay%' ORDER BY created_at DESC LIMIT 5;
-- Esperado: Jobs de eBay no afectados
```

---

## Notas

- **QA Instruction del Developer**: Ejecutar `artisan queue:restart` antes de testear
- **Payload actualizado**: El payload de Iter.3 incluye `weight` como objeto separado de `dimensions` (cambio del developer en correcciones)
- **Tiendas de prueba**: WooCommerce staging + Etsy dedicada (⚠️ listing fees $0.20/listing)
- **Concurrencia**: NO disparar batches concurrentes. Uno a la vez
- **Sin retry interno**: Ante 429, Gateway aborta y reporta
- **Feature Hidden**: Debe estar habilitada manualmente para el tenant
- **Iteración 3**: Los retests (RT-001 a RT-006) son BLOQUEANTES. Si alguno falla → rechazo inmediato
