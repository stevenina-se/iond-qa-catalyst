# Test Plan — IONF-1004

## Información del Ticket

| Campo | Valor |
|-------|-------|
| ID | IONF-1004 (86e18mbg9) |
| Título | Soporte de Listings para Etsy y WooCommerce en Gateway |
| Módulo | Integrations (Gateway legacy — PHP) |
| Tipo | New Feature |
| QA Engineer | Steve Nina |
| Fecha del plan | 2026-06-02 |
| MR | [GitLab MR #560](https://gitlab.com/altacrest/integrations/gateway/-/merge_requests/560) |
| Branch | IONF-1004 |
| Repo | Gateway |

## Resumen

| Métrica | Valor |
|---------|-------|
| Total de casos | 24 |
| Tiempo estimado | ~180 min (~3 horas) |
| Artefactos de Discovery usados | test-matrix.md (generada), AC del ticket (Gherkin), Análisis Técnico, Dev Notes (Sonia Vale) |

## Contexto Compilado

| Artefacto | Estado | Nota |
|-----------|--------|------|
| `risk-triage.md` | ❌ No existe | Risk análisis implícito en el análisis técnico del ticket |
| `ac-consolidated.md` | ❌ No existe | AC extraídos directamente del ticket (Gherkin + Análisis Técnico → 5 ACs) |
| `test-matrix.md` | ✅ Generada | 24 TCs: 8 Happy Path, 7 Edge Cases, 5 Negativos, 4 Regresión |

---

## Orden de Ejecución

### BLOQUE 0 — PRE-REQUISITOS (antes de empezar)
- □ Ejecutar `artisan queue:restart` en el servidor staging (instrucción del developer)
- □ Verificar que la integración WooCommerce está activa en tienda de prueba
- □ Verificar que la integración Etsy está activa en tienda de prueba
- □ Obtener `gateway-key` válido para ambas integraciones
- □ Obtener `category_id` válido de cada cart via `get_categories` (TC-010, TC-011)

### BLOQUE 1 — SMOKE TESTS (si alguno falla → escalar inmediatamente)
- □ TC-001: Exportar producto simple a WooCommerce — 🔴
- □ TC-006: Exportar producto simple a Etsy (flujo 4 pasos) — 🔴
- □ TC-012: Payload inválido retorna 422 sync — 🔴

### BLOQUE 2 — HAPPY PATH (verificar flujo principal completo)
- □ TC-002: Exportar producto con variantes a WooCommerce — 🔴
- □ TC-003: Procesamiento por lotes (batch) múltiples productos a WC — 🔴
- □ TC-007: Exportar producto con múltiples imágenes a Etsy — 🟠
- □ TC-008: Manejo de Rate Limit 429 en Etsy — abort + webhook — 🔴
- □ TC-010: `get_categories` WooCommerce (sync) — 🟠
- □ TC-011: `get_categories` Etsy taxonomy (sync) — 🟠

### BLOQUE 3 — EDGE CASES (verificar bordes y comportamientos límite)
- □ TC-004: Actualizar producto existente por SKU en WC — 🟠
- □ TC-005: Campos opcionales vacíos/omitidos en WC — 🟠
- □ TC-009: Actualizar producto existente por SKU en Etsy — 🟠
- □ TC-016: Fallo parcial en un lote (mixto OK/fail) — 🟠
- □ TC-017: Imágenes con URL inaccesible en Etsy — 🟠
- □ TC-019: Campo `response` estandarizado en ambos adapters — 🟠
- □ TC-020: Currency desde config de conexión — 🟡

### BLOQUE 4 — NEGATIVOS (verificar que NO se puede romper)
- □ TC-013: Campos requeridos faltantes (title, sku, price, etc.) — 🔴
- □ TC-014: Gateway-key inválido → 401/403/404 — 🟠
- □ TC-015: Category_id inválido en producto — 🟠
- □ TC-018: Resource action no existente — 🟡

### BLOQUE 5 — REGRESIÓN (verificar que no rompimos nada)
- □ REG-001: Export products de eBay sigue funcionando — 🔴
- □ REG-002: Motor de webhooks funciona para otras acciones — 🟠
- □ REG-003: Endpoints App API existentes no afectados — 🟠
- □ REG-004: Feature hidden — no visible sin habilitación — 🟡

### BLOQUE 6 — DB EVIDENCE (queries de verificación)
- □ DB-001: Verificar jobs encolados correctamente para export_products
- □ DB-002: Verificar que no se crean jobs para payload inválido (422 sync)
- □ DB-003: Verificar que jobs de eBay no fueron afectados

---

## Datos Necesarios

| Dato | Cómo obtenerlo | Notas |
|------|---------------|-------|
| Gateway-key WooCommerce | Integración WC activa en staging | Tienda de prueba con categorías |
| Gateway-key Etsy | Integración Etsy activa en staging | ⚠️ Cuidado con listing fees ($0.20/listing) |
| Payload genérico de prueba | Construir basado en estructura del developer | Ver formato en notas de Sonia Vale |
| SKU existente para test update | Crear primero un producto y usar su SKU | Para TC-004 y TC-009 |
| Category IDs | Obtener via `get_categories` (TC-010, TC-011) | WC: custom per-store, Etsy: taxonomy global |
| Credenciales API | `.env` del proyecto o configuración de staging | Scope `app:integration-action` |
| Acceso DBeaver | SSH tunnel a PostgreSQL de staging | Para DB Evidence |

### Payload de Prueba Base (del developer)

```json
{
  "resource": "export_products",
  "params": {
    "products": [
      {
        "product_id": "45",
        "product_id_channel": "",
        "title": "Camisa a cuadros",
        "description": "Hermosa camisa a cuadros de dama",
        "images": [
          { "src": "https://example.com/image.jpg" }
        ],
        "variants": [
          {
            "name": "Camisa Talla M",
            "sku": "CAM-028",
            "sku_id_channel": "",
            "price": "10.00",
            "barcode": "677867",
            "quantity": 5,
            "aspects": {},
            "dimensions": {
              "length": 5,
              "width": 7,
              "Height": 8,
              "Weight": 9,
              "unit": "lb"
            }
          }
        ]
      }
    ]
  }
}
```

---

## Criterios de Aprobación/Rechazo

### ✅ Criterios de Aprobación
- ✅ TODOS los smoke tests pasan (TC-001, TC-006, TC-012)
- ✅ TODOS los happy path pasan
- ✅ Al menos 80% de los edge cases pasan (≥6 de 7)
- ✅ TODOS los negativos pasan (no se puede romper el sistema)
- ✅ TODOS los casos de regresión pasan (especialmente REG-001: eBay)
- ✅ DB evidence confirma integridad de datos (jobs correctos)

### ❌ Criterios de Rechazo
- ❌ Algún smoke test falla → **rechazo inmediato**
- ❌ Happy path falla → **rechazo**
- ❌ Caso negativo falla (el sistema se puede romper) → **rechazo**
- ❌ Caso de regresión falla (especialmente eBay) → **rechazo con análisis de impacto**
- ❌ DB evidence muestra datos corruptos o jobs mal encolados → **rechazo**

### ⚠️ Aprobación con Observaciones
- ⚠️ Edge case falla pero no es bloqueante → aprobar con bug registrado
- ⚠️ Problema con listing fees de Etsy impide testar TC-008 (Rate Limit) → aprobar con nota y verificación futura
- ⚠️ TC-020 (currency) falla → aprobar con bug bajo si la currency se toma del payload correctamente

---

## Estimación de Tiempo

| Bloque | Casos | Tiempo estimado |
|--------|-------|-----------------|
| Pre-requisitos | 5 | ~15 min |
| Smoke tests | 3 | ~20 min |
| Happy path | 6 | ~45 min |
| Edge cases | 7 | ~40 min |
| Negativos | 4 | ~25 min |
| Regresión | 4 | ~20 min |
| DB evidence | 3 | ~15 min |
| **Total** | **24 + 5 pre-req** | **~180 min (~3 horas)** |

---

## Consideraciones Especiales

1. **Etsy Listing Fees**: Cada producto creado en Etsy tiene un costo de $0.20. Usar tienda de prueba dedicada. Si el costo es bloqueante → testear solo WC y documentar
2. **Concurrencia**: No disparar batches concurrentes. Testear un batch a la vez
3. **Queue Workers**: Ejecutar `artisan queue:restart` antes de cada sesión de testing
4. **Sin Retry Interno**: Ante 429 de Etsy, el gateway aborta. El cliente debe reintentar manualmente
5. **Validación sync vs Webhook**: Errores de validación (422) son síncronos. Webhooks solo para flujo async (job)
6. **Feature Hidden**: Esta feature no aparece en seeders default. Debe estar habilitada manualmente para el tenant de prueba

---

## Estado

⏳ **Plan creado** — esperando aprobación del QA Engineer para iniciar ejecución
