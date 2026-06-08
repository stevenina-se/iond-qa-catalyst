# Test Matrix — IONF-1004

> Generada por `test-docs/document` (modo matrix)
> Fecha: 2026-06-02
> Módulo: Integrations (Gateway legacy — PHP)
> Ticket: Soporte de Listings para Etsy y WooCommerce en Gateway

## Resumen

| Métrica | Valor |
|---------|-------|
| Total de casos | 24 |
| Happy path | 8 |
| Edge cases | 7 |
| Negativos | 5 |
| Regresión | 4 |
| Automatizables | 10 |
| Cobertura de AC | 3/3 |

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

## Test Matrix

### Export Products — WooCommerce

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-001 | Integrations | AC-1 | Happy Path | Exportar producto simple a WooCommerce | Integración WC activa con tienda de prueba, queue workers corriendo (`artisan queue:restart`) | 1. Enviar POST a `/api/2.0/app/integrations/{gateway-key}/action` con resource `export_products` y 1 producto simple (1 variante) 2. Esperar procesamiento del job 3. Verificar webhook de respuesta 4. Verificar producto en tienda WC | Producto creado en WC con datos correctos (title, description, price, SKU, quantity). Webhook de éxito disparado a la app origen con campo `response` genérico | 🔴 | ✅ | ⬜ Pendiente |
| TC-002 | Integrations | AC-1 | Happy Path | Exportar producto con variantes a WooCommerce | Integración WC activa, tienda de prueba | 1. Enviar POST con 1 producto que tiene múltiples variantes (ej: Talla S, M, L) con diferentes precios y SKUs 2. Esperar procesamiento 3. Verificar en WC que el producto variable fue creado con todas sus variantes | Producto variable creado en WC. Cada variante tiene su SKU, precio y quantity correctos. Se hizo POST al producto general + POST de variantes en lote | 🔴 | ✅ | ⬜ Pendiente |
| TC-003 | Integrations | AC-1 | Happy Path | Procesamiento por lotes (batch) de múltiples productos a WooCommerce | Integración WC activa, chunk size configurado | 1. Enviar POST con 5+ productos en el array `products` 2. Esperar procesamiento en lotes 3. Verificar webhook por lote completado 4. Verificar todos los productos en tienda WC | Todos los productos creados correctamente. Procesamiento en chunks según configuración. Webhook de éxito reportando resultados | 🔴 | ✅ | ⬜ Pendiente |
| TC-004 | Integrations | AC-1 | Edge Case | Actualizar producto existente por SKU en WooCommerce | Producto ya existente en WC con SKU "CAM-028" | 1. Enviar POST con producto cuyo SKU ya existe en WC 2. Esperar procesamiento 3. Verificar que el producto fue ACTUALIZADO (no duplicado) en WC | Adapter busca por SKU, encuentra existente → hace update. No crea duplicado. Datos actualizados correctamente | 🟠 | ✅ | ⬜ Pendiente |
| TC-005 | Integrations | AC-1 | Edge Case | Producto con campos opcionales vacíos/omitidos en WooCommerce | Integración WC activa | 1. Enviar POST con `product_id_channel` vacío, `sku_id_channel` vacío, sin `aspects`, sin `dimensions` 2. Verificar procesamiento exitoso | Producto creado correctamente. Campos opcionales no causan error. Valores por defecto aplicados donde corresponda | 🟠 | ❌ | ⬜ Pendiente |

### Export Products — Etsy

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-006 | Integrations | AC-1 | Happy Path | Exportar producto simple a Etsy (flujo secuencial de 4 pasos) | Integración Etsy activa con tienda de prueba, category_id válido obtenido via `get_categories` | 1. Enviar POST con 1 producto con imagen y 1 variante 2. Verificar que el flujo secuencial se ejecutó: POST /listings (draft) → POST /images → PUT /inventory → PATCH /listings (active) 3. Verificar producto visible en tienda Etsy | Producto creado en Etsy, pasa por los 4 pasos secuenciales. Estado final: `active`. Imágenes subidas correctamente. SKU y precio configurados via inventory. Webhook de éxito disparado | 🔴 | ❌ | ⬜ Pendiente |
| TC-007 | Integrations | AC-1 | Happy Path | Exportar producto con múltiples imágenes a Etsy | Integración Etsy activa, producto con 3+ imágenes | 1. Enviar POST con producto que tiene múltiples URLs de imágenes en el array `images` 2. Verificar que todas las imágenes fueron subidas via endpoints separados de Etsy 3. Verificar producto en tienda | Todas las imágenes subidas al listing de Etsy. Proceso opaco al cliente (encapsulado dentro del adapter) | 🟠 | ❌ | ⬜ Pendiente |
| TC-008 | Integrations | AC-3 | Happy Path | Manejo de Rate Limit 429 en Etsy — abort + report | Integración Etsy activa, escenario que provoque 429 (lote grande o API throttled) | 1. Enviar POST con lote de productos a Etsy 2. Esperar a que Etsy responda con HTTP 429 (o simular condiciones) 3. Verificar comportamiento del Gateway | Gateway captura la excepción del lote. Abort inmediato (sin retry interno). Webhook de fallo disparado indicando error de Rate Limit y cuáles productos fallaron. App origen puede reintentarlos | 🔴 | ❌ | ⬜ Pendiente |
| TC-009 | Integrations | AC-1 | Edge Case | Actualizar producto existente por SKU en Etsy | Producto ya existente en Etsy con mismo SKU | 1. Enviar POST con producto cuyo SKU ya existe en Etsy 2. Verificar que el adapter busca por SKU y hace update | Producto actualizado sin crear duplicado. Flujo de actualización correcto | 🟠 | ❌ | ⬜ Pendiente |

### Get Categories (Acción sync)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-010 | Integrations | AC-4 | Happy Path | Obtener categorías de WooCommerce via `get_categories` | Integración WC activa con tienda que tiene categorías | 1. Enviar POST a `/api/2.0/app/integrations/{gateway-key}/action` con resource `get_categories` 2. Verificar respuesta | Respuesta sync (no job, no webhook). Retorna lista de categorías de la tienda WC con IDs válidos. El cliente puede usar estos IDs para enviar productos | 🟠 | ✅ | ⬜ Pendiente |
| TC-011 | Integrations | AC-5 | Happy Path | Obtener categorías de Etsy via `get_categories` (taxonomy global) | Integración Etsy activa | 1. Enviar POST con resource `get_categories` para Etsy 2. Verificar respuesta | Respuesta sync. Retorna taxonomy global de Etsy. IDs válidos para asignar a productos | 🟠 | ✅ | ⬜ Pendiente |

### Validación y Errores

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-012 | Integrations | AC-2 | Negativo | Payload inválido — estructura incorrecta | Integración activa (WC o Etsy) | 1. Enviar POST con payload que no coincide con la estructura genérica esperada (ej: sin campo `products`, array vacío, formato JSON inválido) 2. Verificar respuesta | HTTP 422 sync. Proceso de mapeo se detiene ANTES de procesar lotes. No se dispara webhook (override técnico). Mensaje de error detalla fallo de validación | 🔴 | ✅ | ⬜ Pendiente |
| TC-013 | Integrations | AC-2 | Negativo | Campos requeridos faltantes en producto | Integración activa | 1. Enviar POST con producto sin `title` (requerido) 2. Enviar POST con producto sin `description` (requerido) 3. Enviar POST con variante sin `sku` (requerido) 4. Enviar POST con variante sin `price` (requerido) | HTTP 422 para cada caso. Validación indica qué campo requerido falta. No se procesa ningún lote | 🔴 | ✅ | ⬜ Pendiente |
| TC-014 | Integrations | AC-2 | Negativo | Gateway-key inválido o integración inexistente | Ninguna integración con la key proporcionada | 1. Enviar POST a `/api/2.0/app/integrations/{invalid-key}/action` con resource `export_products` | Error de autenticación/autorización. Respuesta HTTP apropiada (401/403/404). No se procesa nada | 🟠 | ✅ | ⬜ Pendiente |
| TC-015 | Integrations | AC-1 | Negativo | Category_id inválido en producto enviado a WC | Integración WC activa, category_id que no existe en la tienda | 1. Enviar POST con producto que tiene un `category_id` inexistente 2. Verificar comportamiento | El lote falla para ese producto. Webhook reporta error indicando categoría inválida. Otros productos del lote no afectados (chunks atómicos per-product) | 🟠 | ❌ | ⬜ Pendiente |
| TC-016 | Integrations | AC-3 | Edge Case | Fallo parcial en un lote (algunos productos OK, otros fallan) | Integración activa (WC o Etsy), lote mixto | 1. Enviar lote con productos válidos e inválidos mezclados 2. Verificar procesamiento | Chunks atómicos per-product. Productos válidos se procesan correctamente. Productos fallidos se reportan. Sin rollback. Webhook reporta resultados parciales | 🟠 | ❌ | ⬜ Pendiente |
| TC-017 | Integrations | AC-1 | Edge Case | Producto con imágenes de URL inaccesible en Etsy | Integración Etsy activa | 1. Enviar POST con producto que tiene URL de imagen que retorna 404 o timeout 2. Verificar comportamiento en paso 2 (POST /images) del flujo Etsy | El flujo falla en el paso de images. Producto queda en draft o se aborta. Webhook reporta el fallo con detalle | 🟠 | ❌ | ⬜ Pendiente |
| TC-018 | Integrations | AC-2 | Negativo | Resource action no existente | Integración activa | 1. Enviar POST con resource diferente a `export_products` o `get_categories` (ej: `invalid_action`) | Error de validación. Acción no reconocida | 🟡 | ✅ | ⬜ Pendiente |

### Consistencia de Datos

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-019 | Integrations | AC-1 | Edge Case | Verificar campo `response` estandarizado en adapters nuevos | Integración WC y Etsy activas | 1. Exportar producto a WC → capturar webhook response 2. Exportar producto a Etsy → capturar webhook response 3. Comparar estructura del campo `response` | Ambos adapters retornan campo `response` con estructura genérica estandarizada (no cart-specific en la capa externa) | 🟠 | ❌ | ⬜ Pendiente |
| TC-020 | Integrations | AC-1 | Edge Case | Currency tomada de configuración de conexión (cart config) | Integración con currency configurado (ej: USD) | 1. Enviar producto con precio sin indicar currency 2. Verificar que el producto en el cart destino usa la currency de la configuración de la conexión | Precio del producto en el cart usa la currency de la config del cart, no del payload | 🟡 | ❌ | ⬜ Pendiente |

---

## Casos de Regresión

| ID | Módulo impactado | Caso de regresión | Por qué podría romperse | Prioridad | Estado |
|----|-----------------|-------------------|------------------------|-----------|--------|
| REG-001 | Integrations | Export products de eBay (existente) sigue funcionando | Los nuevos adapters de WC/Etsy se basan en el patrón de eBay. Cambios en la infra de batching o response podrían afectar eBay | 🔴 | ⬜ Pendiente |
| REG-002 | Integrations | Motor de webhooks (`sendWebhook`) funciona para otras acciones | Aunque el ticket dice "sin cambios en motor de webhook", los nuevos adapters lo usan. Verificar que otras acciones existentes (sync_inventory, etc.) siguen disparando webhooks correctamente | 🟠 | ⬜ Pendiente |
| REG-003 | Integrations | Endpoints existentes de App API no afectados | Nuevas acciones registradas no deben romper acciones existentes del endpoint `/action` | 🟠 | ⬜ Pendiente |
| REG-004 | Integrations | Feature es hidden — no aparece en seeders default | La feature no debe ser visible para tenants que no la tienen habilitada | 🟡 | ⬜ Pendiente |

---

## Queries de Verificación BD

> **Nota**: Este ticket NO tiene migraciones de BD. La verificación es sobre el comportamiento del job queue y logs.

```sql
-- TC-001/TC-006: Verificar que el job fue encolado correctamente
-- BD: PostgreSQL (gateway)
SELECT * FROM jobs WHERE payload LIKE '%export_products%' ORDER BY created_at DESC LIMIT 5;
-- Esperado: Job creado con payload correspondiente al request

-- TC-003: Verificar procesamiento en lotes
SELECT * FROM jobs WHERE payload LIKE '%export_products%' AND attempts > 0 ORDER BY created_at DESC LIMIT 10;
-- Esperado: Jobs procesados (attempts > 0), sin failed_at

-- TC-012/TC-013: Verificar que NO se creó job para payload inválido
SELECT * FROM jobs WHERE payload LIKE '%export_products%' ORDER BY created_at DESC LIMIT 1;
-- Esperado: No hay job nuevo (validación falló sync antes de encolar)

-- REG-001: Verificar que eBay export_products sigue funcionando
SELECT * FROM jobs WHERE payload LIKE '%export_products%' AND payload LIKE '%ebay%' ORDER BY created_at DESC LIMIT 5;
-- Esperado: Jobs de eBay no afectados por los cambios
```

---

## Notas

- **QA Instruction del Developer**: Ejecutar `artisan queue:restart` antes de testear (para que los workers tomen los cambios del código)
- **Tiendas de prueba necesarias**: WooCommerce (tienda staging) + Etsy (tienda de prueba dedicada — cuidado con listing fees de $0.20)
- **Concurrencia**: El cliente NO debe disparar batches concurrentes. Testear un batch a la vez
- **Sin retry interno**: Ante 429, el Gateway aborta y reporta. No hay retry automático
- Queries ejecutadas en DBeaver (PostgreSQL via SSH tunnel)
