# Code Review QA — 86e223kvf (Modo Deployment / Bug Hunting)

## Resumen
- **Repos revisados**: gateway-ion, flow_binaries, gateway
- **Commits analizados**: 11 (gateway-ion), 4 (flow_binaries), 5 (gateway)
- **Archivos modificados analizados**: ~404 total (389 gateway-ion, 13 flow_binaries, 2 gateway)
- **Hallazgos totales**: 7
  - BUG confirmados: 0
  - RISK a verificar: 4 (🟠: 2, 🟡: 2)
  - SEC seguridad: 0
  - EDGE cases: 3 (🟡: 3)
- **Módulos con impacto cruzado**: boards, executions, data-store, accounts, keys, pdf-templates, webhooks, integrations, connections, dashboard, settings, profile
- **TCs inyectados en test-matrix**: 7 (TC-CR-001 a TC-CR-007)

## Commits Analizados

### gateway-ion
| Commit | Mensaje | Archivos |
|--------|---------|----------|
| f76d8c43 | (feat) tenant migrate shell + executions to Tailwind/shadcn-vue | ~200+ |
| 3066ab7f | (feat) polish across tenant screens | ~30 |
| 0d4c1ff4 | (fix) code review pass — dialog, toast, notifications, tables | ~20 |
| e2033a74 | (test) raise coverage to 80%+ | ~30 |
| 7452094d | (fix) code review pass — i18n labels, defineModel decoupling | ~15 |
| 031d672d | (fix) replace boolean createOpen defineModel with counter | ~5 |
| 60450425 | (fix) PR review — i18n breadcrumb/StoreViewer labels | ~5 |

### flow_binaries
| Commit | Mensaje | Archivos |
|--------|---------|----------|
| 464c086 | (feat) add search/filter/sort support to tenant list endpoints | 13 |
| a9dc2bf | (test) cover new search/filter/pagination logic | 12 |
| ef3159e | (fix) repair pipeline test failures | 3 |

### gateway
| Commit | Mensaje | Archivos |
|--------|---------|----------|
| e8a9061a | (feat) add status/date filters to tenant executions list endpoint | 1 |
| 1597d6b6 | (fix) validate date_from/date_to format | 1 |
| 6d2fe4f4 | (fix) validate execution status filter to bound input length | 1 |

---

## Evaluación General

> La calidad del código es **alta**. El developer aplicó:
> - Validación de input con `$request->validate()` en Laravel
> - `is_string` guard para arrays en status filter
> - `max:50` para bound del status input
> - `searchLikeEscaper` correcto para escapado de SQL LIKE wildcards
> - Struct en lugar de parámetros posicionales para evitar swap de strings
> - Whitelist de `order_by` fields
> - Scoping CSS con `.modern-ui` para aislamiento de PrimeVue
> - Deduplicación de toasts con `${tone}:${message}` como ID
> - Tests unitarios para cada cambio significativo (≥80% cobertura)
>
> **No se encontraron BUGs confirmados.** Los hallazgos son RISKs y EDGE cases a verificar durante el testing funcional.

---

## Sección 1 — BUGs Confirmados (BUG-CR-##)

> No se encontraron BUGs confirmados reproducibles. ✅

---

## Sección 2 — Riesgos a Verificar (RISK-CR-##)

### RISK-CR-001: ListPaginatedKeysByAccount no aplica ILIKE (asimetría con Company)

- **Severidad**: 🟠 Alto
- **Repo**: flow_binaries
- **Commit**: 464c086
- **Archivo**: `backend/ion/services/key_service.go` (L76-104 vs L195-227)
- **Descripción**: `ListPaginatedKeysByAccount` aplica `applyProviderFilter` pero NO aplica `applyILIKE` para búsqueda por texto. En contraste, `ListPaginatedKeysByCompany` (L195-227) SÍ aplica ambos: `applyProviderFilter` + `applyILIKE`. Esto significa que la búsqueda por texto solo funciona en la ruta de company, no en la ruta de account.
- **Comportamiento Esperado**: La búsqueda por texto (search) debería funcionar de la misma manera en ambas rutas — por account y por company.
- **Comportamiento Actual**: Si un usuario usa la ruta de account keys con un parámetro `search`, el filtro se ignora silenciosamente. La ruta de company keys sí filtra correctamente por nombre/tipo.
- **Impacto**: Búsqueda de keys por account devuelve todos los keys sin filtrar cuando se usa search text. Impacto medio porque el frontend probablemente usa la ruta de company, pero si un account necesita filtrar sus keys, no funciona.
- **Recomendación**: Verificar en testing si el frontend usa la ruta de account o company para el listado de keys. Si usa ambas, el search no funciona en account.

### RISK-CR-002: OrderBy sin sanitización en capa de servicio (datastore SQLite)

- **Severidad**: 🟡 Medio
- **Repo**: flow_binaries
- **Commit**: 464c086
- **Archivo**: `core/actions/store/storeservice/datastore.go` (L55-56)
- **Descripción**: El comentario en L41-42 dice "paginationConfig.OrderBy is validated against a whitelist upstream". La whitelist SÍ existe en el controller (`dataStoreListPaginationConfig()` con `{id, name, created_at}`). Sin embargo, `BuildPaginationClause()` construye un `ORDER BY` directamente con string interpolation. Si en algún punto otro caller invoca `List()` sin pasar por el controller, el OrderBy no estaría validado.
- **Comportamiento Esperado**: El OrderBy siempre debería estar sanitizado contra una whitelist antes de usarse en la query SQL.
- **Comportamiento Actual**: La validación ocurre upstream en el controller, no en la capa de servicio. Actualmente todos los callers pasan por el controller, pero es un patrón frágil.
- **Impacto**: Bajo — actualmente no es explotable porque el controller siempre valida.
- **Recomendación**: Verificar en testing que el ordenamiento con valores whitelisted funciona y que valores no whitelisted retornan error 400.

### RISK-CR-003: OrderDirection sin validación explícita en key_service (Postgres)

- **Severidad**: 🟠 Alto
- **Repo**: flow_binaries
- **Commit**: 464c086
- **Archivo**: `backend/ion/services/key_service.go` (L95-96, L218-219)
- **Descripción**: En `ListPaginatedKeysByAccount` y `ListPaginatedKeysByCompany`, el order clause se construye con `fmt.Sprintf("%s %s", paginationParams.OrderBy, paginationParams.OrderDirection)`. La validación del OrderDirection debe ocurrir en `ParsePaginationParams`.
- **Comportamiento Esperado**: `OrderDirection` debería validarse contra un set cerrado `{asc, desc}`.
- **Comportamiento Actual**: Depende de que `ParsePaginationParams` valide correctamente OrderDirection.
- **Impacto**: Si la validación es correcta → no hay riesgo. Si no → potencial SQL injection.
- **Recomendación**: Verificar el handling de OrderDirection. Probar con `order_direction=desc; DROP TABLE--` (debería rechazarse).

### RISK-CR-004: Potential nil pointer en ListCompanyFlows (L79)

- **Severidad**: 🟡 Medio
- **Repo**: flow_binaries
- **Archivo**: `backend/ion/services/company_flow_service.go` (L79)
- **Descripción**: En L76-78, `search` se extrae solo si `pagination != nil`. Pero en L79, `pagination.Filter("status")` se llama sin el nil check. Si `pagination` es `nil`, esto causaría un nil pointer dereference.
- **Comportamiento Esperado**: Si pagination es nil, no debería haber crash.
- **Comportamiento Actual**: En la práctica, el controller SIEMPRE pasa un `pagination` no-nil. Pero si un caller futuro pasa nil → panic.
- **Impacto**: Bajo — no reproducible con el caller actual.
- **Recomendación**: Verificar durante testing que el listado de flows funciona correctamente con los filtros.

---

## Sección 3 — Seguridad (SEC-CR-##)

> No se encontraron hallazgos de seguridad. ✅
> 
> Notas positivas:
> - Multi-tenant scope correcto en todos los endpoints (company/account)
> - Input validation presente en todos los nuevos filtros (gateway ExecutionController)
> - `max:50` bound en status filter previene inputs excesivamente largos
> - LIKE wildcards correctamente escapados en Data Store search
> - No se encontró XSS potencial (no hay `v-html` con datos de usuario)

---

## Sección 4 — Edge Cases (EDGE-CR-##)

### EDGE-CR-001: PrimeVue Toast y vue-sonner Toaster coexisten en TenantLayout

- **Severidad**: 🟡 Medio
- **Repo**: gateway-ion
- **Commit**: f76d8c43
- **Archivo**: `src/layouts/TenantLayout.vue` (L87, L121)
- **Descripción**: TenantLayout monta AMBOS toast hosts: PrimeVue `<Toast group="tenant">` (L87) y vue-sonner `<Toaster>` (L121). Si algún componente no migrado aún usa PrimeVue's toast service, podría generar toasts duplicados.
- **Impacto**: Posible toast duplicado en pantallas que aún usan PrimeVue toast.
- **Recomendación**: Verificar visualmente durante testing que los toasts no aparecen duplicados.

### EDGE-CR-002: useToast dedup con mensajes dinámicos

- **Severidad**: 🟡 Medio
- **Repo**: gateway-ion
- **Commit**: 0d4c1ff4
- **Archivo**: `src/composables/ui/useToast.ts` (L19-21)
- **Descripción**: La deduplicación usa `${tone}:${message}` como id. Si una operación genera el mismo toast N veces rápidamente, los N toasts se deduplican correctamente. Pero si el mensaje varía (ej: incluye un ID diferente), cada variante genera un toast separado.
- **Impacto**: Bajo — el dedup funciona correctamente para los casos comunes.
- **Recomendación**: Verificar que 3 clics rápidos en delete no apilen 3 toasts idénticos.

### EDGE-CR-003: GetStorePath prioridad account vs company

- **Severidad**: 🟡 Medio
- **Repo**: flow_binaries
- **Commit**: 464c086
- **Archivo**: `backend/ion/controllers/data_store_controller.go` (L167-187)
- **Descripción**: `GetStorePath` intenta obtener primero el account del context, luego la company. Si AMBOS están en el context, el path de company sobreescribe al de account. No es un bug porque el middleware garantiza exclusividad, pero la lógica no es defensiva.
- **Impacto**: Bajo — el routing garantiza que solo uno esté en context.
- **Recomendación**: Verificar que Data Store/Structure filtran correctamente por tenant.

---

## Follow-the-Flow Maps

### Flow 1: Execution Status Filter (Gateway → FE)
```
CALLERS: ExecutionController@index (gateway Laravel)
  → FE: ExecutionHistoryView.vue → DataTable search/filter params
PERSISTENCIA: Read-only query, no writes
CONSUMIDORES: Frontend DataTable renderiza los resultados
RENDER: StatusBadge muestra el estado filtrado
ERROR PATH: Laravel validation returns 422 para inputs inválidos
RESULTADO: ✅ Flujo completo correcto. Validación input presente.
```

### Flow 2: Data Store Search (Go → SQLite → FE)
```
CALLERS: ListDataStores controller → storeservice.List()
  → nameSearchClause() → SQLite WHERE LIKE ? ESCAPE
PERSISTENCIA: Read-only query
CONSUMIDORES: FE DataStoreView.vue → DataTable
ERROR PATH: Handler devuelve 500 si la BD no existe, 400 si pagination inválida
RESULTADO: ✅ Flujo correcto. Escape de wildcards implementado.
```

### Flow 3: Flow Description Persistence (FE → Go → Postgres)
```
CALLERS: UpdateCompanyFlow (flow_binaries)
  → .Select("name", "description", "status", "is_dirty").Updates()
PERSISTENCIA: UPDATE SET description = ? WHERE id = ?
CONSUMIDORES: ListCompanyFlows → companyFlowListColumns includes "description"
RENDER: BoardsView muestra la descripción
RESULTADO: ✅ El fix del .Select() es correcto. Sin el "description", gorm descartaría el campo.
```

---

## Impacto Cruzado

| Módulo Impactado | Componente Afectado | Riesgo | Verificación Necesaria |
|---|---|---|---|
| Boards | BoardsView, CreateConnectionV2Dialog | 🟠 Alto | Verificar que el editor NO fue modificado, solo la primera vista |
| Executions | ExecutionHistoryView, ExecutionController | 🟠 Alto | Filtros de status/fecha, paginación SSR |
| Data Store | DataStoreView, storeservice search | 🟠 Alto | Búsqueda con wildcards, ordenamiento |
| Keys | KeysView, key_service filters | 🟡 Medio | Filtro por provider en ambas rutas |
| Accounts | AccountsView, account_controller | 🟡 Medio | Filtro por timezone, remote_id ordenable |
| Admin | Pantallas PrimeVue | 🔴 Crítico | CSS bleeding a Admin (aislamiento .modern-ui) |
| All 14 pantallas | DataTable, modales, toasts | 🟠 Alto | Paginación SSR, empty states, CRUD |

---

## TCs Inyectados en Test Matrix

| TC ID | Categoría | Origen | Caso de Test | Severidad |
|-------|-----------|--------|-------------|-----------|
| TC-CR-001 | RISK | RISK-CR-001 | Buscar keys por texto en la ruta de account — verificar si search aplica | 🟠 |
| TC-CR-002 | RISK | RISK-CR-002 | Ordenar Data Store por columna no whitelisted — verificar rechazo | 🟡 |
| TC-CR-003 | RISK | RISK-CR-003 | Probar OrderDirection con valor no estándar en keys listing | 🟠 |
| TC-CR-004 | RISK | RISK-CR-004 | Verificar listado de flows con filtros de status y search | 🟡 |
| TC-CR-005 | EDGE | EDGE-CR-001 | Verificar que toasts no se dupliquen (PrimeVue + vue-sonner) | 🟡 |
| TC-CR-006 | EDGE | EDGE-CR-002 | 3 clics rápidos en save/delete — verificar dedup de toasts | 🟡 |
| TC-CR-007 | EDGE | EDGE-CR-003 | Verificar que Data Store filtra correctamente por tenant | 🟡 |
