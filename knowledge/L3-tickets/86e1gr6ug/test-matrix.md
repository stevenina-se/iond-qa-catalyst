# Test Matrix — 86e1gr6ug (Mejoras de la interface en ionflow dualtrack)

> Generada por `test-docs/document` (modo matrix)
> Fecha: 2026-06-08
> Módulos: boards, pdf-templates, connections, integrations, keys, accounts, developer-apps, services
> Basada en: ac-consolidated.md v2 (32 ACs) + risk-triage.md v2 (27 edge cases)

## Resumen

| Métrica | Valor |
|---------|-------|
| Total de casos | 73 (68 Discovery + 5 Code Review) |
| Happy path | 28 |
| Edge cases | 22 |
| Negativos | 8 |
| Regresión | 10 |
| Code Review | 5 (inyectados 2026-06-25) |
| Automatizables | 38 |
| Cobertura de AC | 32/32 |
| Última actualización | 2026-06-25 — Deployment iniciado |

---

## Test Matrix

### EPIC 1 — Boards Telemetry + Payload Diet + Clone (AC-1 a AC-10)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-001 | boards | AC-1 | Happy Path | Badge de ejecución exitosa en lista de boards | Flow ejecutado exitosamente al menos una vez | Company Login > Sidebar: Boards > Navigate: /workflows > Verify: Flow con badge "completed" (color verde/éxito) visible | El flow muestra badge `completed` con la severidad correcta | 🔴 | ✅ | ⬜ Pendiente |
| TC-002 | boards | AC-1 | Edge Case | Badge de ejecución con warning (falla parcial) | Flow ejecutado con al menos un nodo en error pero flow completado | Company Login > Sidebar: Boards > Navigate: /workflows > Verify: Flow con badge "warning" (color amarillo/advertencia) | Badge muestra `warning` diferenciado visualmente de `error` y `completed` | 🟠 | ✅ | ⬜ Pendiente |
| TC-003 | boards | AC-1 | Edge Case | Badge de ejecución con error | Flow ejecutado con propagación de StatusError | Company Login > Sidebar: Boards > Navigate: /workflows > Verify: Flow con badge "error" (color rojo) | Badge muestra `error` con severidad correcta | 🟠 | ✅ | ⬜ Pendiente |
| TC-004 | boards | AC-1,P1 | Edge Case | Flow sin ejecuciones (NULL) | Flow recién creado, nunca ejecutado | Company Login > Sidebar: Boards > Navigate: /workflows > Verify: Flow sin badge de ejecución o con estado neutro "Sin ejecuciones" | No crashea. Muestra estado neutro o sin badge | 🟠 | ✅ | ⬜ Pendiente |
| TC-005 | boards | AC-2 | Happy Path | Switch activo/pausado independiente del badge | Flow activo con ejecución error | Company Login > Sidebar: Boards > Navigate: /workflows > Verify: Switch muestra "Activo" Y badge muestra "error" simultáneamente sin confusión | Ambos indicadores son visualmente independientes | 🔴 | ✅ | ⬜ Pendiente |
| TC-006 | boards | AC-2 | Happy Path | Cambiar estado sin corromper grafo | Flow activo con datos | Company Login > Sidebar: Boards > Navigate: /workflows > Click [FlowStatusBadge switch] > Verify: Estado cambia a Pausado > Verify: Flow completo sigue intacto (abrir canvas y verificar nodos) | El switch envía solo el campo de estado. El grafo no se sobrescribe con payload reducido | 🔴 | ❌ | ⬜ Pendiente |
| TC-007 | boards | AC-3 | Happy Path | Puntero last_execution_id actualizado post-ejecución | Flow existente | Company Login > Sidebar: Boards > Click [Flow] > Canvas: Ejecutar flow en modo Development > Wait: Ejecución completa > Verify BD: `SELECT last_execution_id FROM flows WHERE id = '<flow_id>'` muestra ID de última ejecución | `last_execution_id` apunta a la ejecución recién completada | 🔴 | ❌ | ⬜ Pendiente |
| TC-008 | boards | AC-4 | Happy Path | Estado terminal completed | Flow con todos nodos exitosos | Company Login > Sidebar: Boards > Click [Flow] > Canvas: Ejecutar flow > Wait: Ejecución completa > Verify BD: Ejecución con estado `completed` | Estado terminal = `completed` | 🔴 | ❌ | ⬜ Pendiente |
| TC-009 | boards | AC-4 | Edge Case | Estado terminal warning (StatusWarning) | Flow con un nodo que falla parcialmente | Company Login > Sidebar: Boards > Click [Flow con nodo falible] > Canvas: Ejecutar > Wait: Ejecución completa > Verify BD: Ejecución con estado `warning` | Estado terminal = `warning` (nuevo StatusWarning) | 🟠 | ❌ | ⬜ Pendiente |
| TC-010 | boards | AC-5 | Happy Path | execution_time poblado correctamente (bugfix) | Flow existente | Company Login > Sidebar: Boards > Click [Flow] > Canvas: Ejecutar flow > Wait: Ejecución completa > Verify BD: `execution_time > 0` en la ejecución | `execution_time` refleja duración real (no ~0s como antes del bugfix) | 🔴 | ❌ | ⬜ Pendiente |
| TC-011 | boards | AC-6 | Happy Path | Payload Diet — lista de boards con grafo reducido | Company con flows existentes | Company Login > Sidebar: Boards > Navigate: /workflows > DevTools: Network > Verify: Response de lista contiene `{nodes:[id,type], edges:[source,target]}` sin JSONB pesado | Payload reducido. No contiene datos completos de nodos | 🟠 | ✅ | ⬜ Pendiente |
| TC-012 | boards | AC-6 | Edge Case | Payload Diet — performance con 500+ flows | Company con muchos flows | Company Login > Navigate: /workflows > DevTools: Network > Verify: Tiempo de respuesta < 3s > Verify: No hay N+1 queries (check Laravel debug bar si disponible) | La lista carga en tiempo razonable con eager-load | 🟡 | ❌ | ⬜ Pendiente |
| TC-013 | boards | AC-7 | Edge Case | Poda de ejecución — ON DELETE SET NULL | Flow con last_execution_id apuntando a ejecución existente | Verify BD: Eliminar la ejecución referenciada > Verify BD: `last_execution_id = NULL` en el flow > Company Login > Sidebar: Boards > Verify: Flow muestra estado neutro (sin badge) | FK queda NULL. Frontend maneja graciosamente | 🟠 | ❌ | ⬜ Pendiente |
| TC-014 | boards | AC-8 | Happy Path | Expansión de fila — carga flow completo con Used Apps | Flow con nodos de connectors | Company Login > Sidebar: Boards > Navigate: /workflows > Click [Chevron expandir fila] > Verify: Drawer/expansión muestra secciones "GLOBAL" y "TENANT" apps correctamente separadas | Flow completo cargado del HUB. Apps categorizadas correctamente | 🟠 | ✅ | ⬜ Pendiente |
| TC-015 | boards | AC-8 | Edge Case | Expansión de fila — flow sin apps | Flow sin nodos de connectors | Company Login > Sidebar: Boards > Click [Chevron de flow sin apps] > Verify: Sección de apps muestra estado vacío correcto | No crashea. Secciones vacías manejadas | 🟡 | ✅ | ⬜ Pendiente |
| TC-016 | boards | AC-9 | Happy Path | Clonar flow (endpoint nativo) | Flow existente con nodos | Company Login > Sidebar: Boards > Navigate: /workflows > Click [FlowActionsMenu] > Click [Clonar] > Verify: Nuevo flow aparece en lista sin historial de ejecuciones > Verify BD: `last_execution_id = NULL` en clon | Clon limpio sin ejecuciones ni commits. Grafo completo copiado | 🟠 | ✅ | ⬜ Pendiente |
| TC-017 | boards | AC-9 | Negativo | Clonar flow sin permisos | Usuario sin permiso `create-board` | Company Login (usuario limitado) > Sidebar: Boards > Click [FlowActionsMenu] > Verify: Opción "Clonar" no disponible o retorna error 403 | Acción bloqueada por permisos | 🟡 | ✅ | ⬜ Pendiente |
| TC-018 | boards | AC-10 | Happy Path | Graph Utils — triggers y sinks identificados | Flow con trigger y nodos finales | Company Login > Sidebar: Boards > Click [Chevron expandir] > Verify: Preview identifica nodos trigger y sink del flow | Triggers y sinks correctamente detectados | 🟡 | ✅ | ⬜ Pendiente |

### EPIC 2 — PDF Templates + Clone nativo (AC-11 a AC-17)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-019 | pdf-templates | AC-11 | Happy Path | Formato y orientación derivados del schema | Template con schema A4 vertical | Company Login > Sidebar: PDF Templates > Navigate: /pdf-templates > Click [Expandir template A4] > Verify: Muestra "A4 - Portrait" con conversión mm/pulgadas | Formato y orientación correctos derivados del schema | 🟠 | ✅ | ⬜ Pendiente |
| TC-020 | pdf-templates | AC-11,P3 | Edge Case | Schema vacío o malformado | Template con schema JSONB vacío `{}` | Company Login > Sidebar: PDF Templates > Navigate: /pdf-templates > Click [Expandir template con schema vacío] > Verify: No crashea, muestra valor por defecto o "Formato desconocido" | Adaptador maneja graciosamente sin crash | 🟠 | ✅ | ⬜ Pendiente |
| TC-021 | pdf-templates | AC-11 | Edge Case | Dimensiones custom no mapeables | Template con dimensiones que no son A4/Carta/Legal | Company Login > Sidebar: PDF Templates > Click [Expandir template custom] > Verify: Muestra dimensiones en mm o indicador "Custom" | No crashea. Muestra información útil | 🟡 | ✅ | ⬜ Pendiente |
| TC-022 | pdf-templates | AC-12 | Happy Path | Badge "En uso" para template utilizado | Template con `generation_count > 0` | Company Login > Sidebar: PDF Templates > Navigate: /pdf-templates > Verify: Template muestra badge "En uso" | Badge de uso visible y correcto | 🟠 | ✅ | ⬜ Pendiente |
| TC-023 | pdf-templates | AC-12 | Edge Case | Badge "Nunca usado" para template nuevo | Template con `generation_count = 0` | Company Login > Sidebar: PDF Templates > Verify: Template muestra badge "Nunca usado" | Badge "Nunca usado" visible | 🟡 | ✅ | ⬜ Pendiente |
| TC-024 | pdf-templates | AC-12 | Edge Case | Etiqueta "Borrador" para template sin variables | Template sin variables dinámicas en schema | Company Login > Sidebar: PDF Templates > Verify: Template muestra etiqueta "Borrador" | `isDraft` derivado correctamente del schema | 🟡 | ✅ | ⬜ Pendiente |
| TC-025 | pdf-templates | AC-13 | Happy Path | Telemetría de generación incrementa | Template existente, flow con nodo PDF | Company Login > Sidebar: Boards > Click [Flow con nodo PDF] > Canvas: Ejecutar > Wait: Ejecución completa > Sidebar: PDF Templates > Verify: `generation_count` incrementó en 1 > Verify: `last_generated_at` actualizado | Contador incrementa. Timestamp actualizado | 🔴 | ❌ | ⬜ Pendiente |
| TC-026 | pdf-templates | AC-14 | Happy Path | Preview con proporción real y campos dinámicos | Template con campos dinámicos | Company Login > Sidebar: PDF Templates > Click [Expandir template] > Verify: Preview muestra mockup con proporción real > Verify: Pills de campos dinámicos visibles > Click [Copiar campo] > Verify: Copiado al clipboard | Preview, pills, y función de copiar funcionan | 🟠 | ✅ | ⬜ Pendiente |
| TC-027 | pdf-templates | AC-14 | Edge Case | Preview con dimensiones extremas | Template con dimensiones muy anchas o altas | Company Login > Sidebar: PDF Templates > Click [Expandir template extremo] > Verify: Preview se adapta sin desbordamiento | Preview no rompe el layout | 🟡 | ✅ | ⬜ Pendiente |
| TC-028 | pdf-templates | AC-15 | Happy Path | Clonar PDF Template (endpoint nativo Go) | Template existente con generaciones | Company Login > Sidebar: PDF Templates > Click [Menú Kebab] > Click [Clonar] > Verify: Nuevo template aparece con nombre + " (copy)" > Verify: `generation_count = 0` en clon | Copia profunda. Nombre con sufijo. Telemetría reseteada | 🟠 | ✅ | ⬜ Pendiente |
| TC-029 | pdf-templates | AC-16 | Happy Path | Payload Diet — lista sin JSONB pesado | Company con templates existentes | Company Login > Sidebar: PDF Templates > DevTools: Network > Verify: Response de lista NO contiene JSONB completo del schema | Payload reducido para performance | 🟠 | ✅ | ⬜ Pendiente |
| TC-030 | pdf-templates | AC-17 | Happy Path | Exportar JSON de template | Template existente | Company Login > Sidebar: PDF Templates > Click [Menú Kebab] > Click [Exportar JSON] > Verify: Archivo JSON descargado correctamente | JSON descarga con schema completo | 🟡 | ✅ | ⬜ Pendiente |
| TC-031 | pdf-templates | AC-17 | Happy Path | Columnas ordenables | Lista de templates visible | Company Login > Sidebar: PDF Templates > Click [Header "Generaciones"] > Verify: Lista se reordena ASC > Click [Header "Generaciones"] > Verify: Lista se reordena DESC | Ordenamiento funciona via `order_by`/`order_direction` | 🟡 | ✅ | ⬜ Pendiente |

### EPIC 3 — Unified Search & Lazy Catalog (AC-18 a AC-21)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-032 | connections | AC-18 | Happy Path | Búsqueda unificada en Connections | Connections existentes | Company Login > Sidebar: Connections > Fill "Search": "Shopify" > Press Enter > Verify: Lista filtrada muestra solo connections con "Shopify" | Búsqueda funciona solo con Enter. Resultados correctos | 🟠 | ✅ | ⬜ Pendiente |
| TC-033 | integrations | AC-18 | Happy Path | Búsqueda unificada en Integrations | Integrations existentes | Company Login > Sidebar: Integrations > Fill "Search": "test" > Press Enter > Verify: Lista filtrada | Búsqueda Enter-only funciona | 🟠 | ✅ | ⬜ Pendiente |
| TC-034 | keys | AC-18 | Happy Path | Búsqueda unificada en Keys | Keys existentes | Company Login > Sidebar: Keys > Fill "Search": "openai" > Press Enter > Verify: Lista filtrada | Búsqueda Enter-only funciona | 🟡 | ✅ | ⬜ Pendiente |
| TC-035 | accounts | AC-18 | Happy Path | Búsqueda unificada en Accounts | Accounts existentes | Company Login > Sidebar: Accounts > Fill "Search": "test" > Press Enter > Verify: Lista filtrada | Búsqueda Enter-only funciona | 🟡 | ✅ | ⬜ Pendiente |
| TC-036 | dev-apps | AC-18 | Happy Path | Búsqueda unificada en Developer Apps | Developer apps existentes | Company Login > Sidebar: Developer Apps > Fill "Search": "app" > Press Enter > Verify: Lista filtrada | Búsqueda Enter-only funciona | 🟡 | ✅ | ⬜ Pendiente |
| TC-037 | services | AC-18 | Happy Path | Búsqueda unificada en Services | Services existentes | Company Login > Sidebar: Services > Fill "Search": "api" > Press Enter > Verify: Lista filtrada | Búsqueda Enter-only funciona | 🟡 | ✅ | ⬜ Pendiente |
| TC-038 | multi | AC-18 | Edge Case | Búsqueda con Enter sin texto | Cualquier pantalla con búsqueda | Company Login > Sidebar: Connections > Click [Search input] > Press Enter (sin texto) > Verify: Lista muestra todos los registros o se resetea el filtro | No crashea. Comportamiento consistente | 🟡 | ✅ | ⬜ Pendiente |
| TC-039 | multi | AC-18 | Edge Case | URL con ?search= al cargar | URL con query param de búsqueda | Company Login > Navigate: /connections?search=Shopify > Verify: Lista carga con filtro aplicado > Verify: Input de búsqueda muestra "Shopify" | Sincronización URL ↔ input via `useListQuerySync` | 🟠 | ✅ | ⬜ Pendiente |
| TC-040 | multi | AC-18 | Negativo | Búsqueda sin resultados | Término que no coincide con ningún registro | Company Login > Sidebar: Connections > Fill "Search": "xxxxxxxxx" > Press Enter > Verify: Lista vacía con mensaje apropiado | Estado vacío manejado correctamente | 🟡 | ✅ | ⬜ Pendiente |
| TC-041 | multi | AC-19 | Happy Path | Lazy Catalog con cooldown | Pantalla con expansión de filas | Company Login > Sidebar: Connections > Click [Expandir fila 1] > Verify: Catálogo carga > Click [Colapsar fila 1] > Click [Expandir fila 2] (dentro de 30s) > Verify: Catálogo reutiliza datos sin nueva petición | Singleton con cooldown 30s funciona | 🟡 | ❌ | ⬜ Pendiente |
| TC-042 | boards | AC-20 | Happy Path | FTS PostgreSQL — búsqueda con acentos | Flows con nombres acentuados (ej. "Ejecución automática") | Company Login > Sidebar: Boards > Fill "Search": "ejecucion" (sin acento) > Press Enter > Verify: Flow "Ejecución automática" aparece en resultados | `unaccent` funciona en búsqueda FTS | 🟠 | ✅ | ⬜ Pendiente |
| TC-043 | boards | AC-20,P4 | Negativo | FTS — intento de inyección SQL | N/A | Company Login > Sidebar: Boards > Fill "Search": "'; DROP TABLE flows; --" > Press Enter > Verify: Sin error. Lista vacía o sin resultados | Input sanitizado. Sin inyección SQL | 🔴 | ✅ | ⬜ Pendiente |
| TC-044 | accounts | AC-21 | Happy Path | ILIKE search tenant-scoped | Accounts en company A y company B | Company Login (Company A) > Sidebar: Accounts > Fill "Search": "test" > Press Enter > Verify: Solo accounts de Company A en resultados | Aislamiento por tenant. No muestra datos de otra company | 🔴 | ❌ | ⬜ Pendiente |
| TC-045 | multi | AC-21 | Edge Case | ILIKE con caracteres especiales | N/A | Company Login > Sidebar: Keys > Fill "Search": "100%" > Press Enter > Verify: `%` escapado correctamente, sin resultados erróneos | Escape de `% _ \` funciona en `applyILIKE` | 🟠 | ✅ | ⬜ Pendiente |

### EPIC 4 — UI Polish, A11y & Safety (AC-22 a AC-25)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-046 | multi | AC-22 | Happy Path | Keyboard navigation en búsqueda | Cualquier pantalla con búsqueda | Company Login > Sidebar: Connections > Press Tab hasta icono de búsqueda > Verify: Focus visible en icono > Press Enter > Verify: Input de búsqueda activado | Keyboard navigation funciona. Focus visible | 🟡 | ✅ | ⬜ Pendiente |
| TC-047 | multi | AC-22 | Edge Case | Motion reduce — sin animaciones | Sistema con `prefers-reduced-motion: reduce` | Configurar OS con motion reduce > Company Login > Navigate: /workflows > Verify: Iconos de carga sin animación | `motion-reduce:animate-none` aplicado | 🟡 | ❌ | ⬜ Pendiente |
| TC-048 | multi | AC-23 | Happy Path | Safety — pointer-events-none durante recarga | Lista recargando datos | Company Login > Sidebar: Boards > Trigger recarga (cambiar filtro) > Intentar click en fila durante carga > Verify: Click bloqueado (pointer-events-none) > Wait: Recarga completa > Verify: Clicks funcionan de nuevo | Mutaciones bloqueadas durante recarga | 🟡 | ❌ | ⬜ Pendiente |
| TC-049 | multi | AC-24 | Happy Path | Dark Mode — contraste de enlaces y superficies | Dark mode activado | Company Login > Activar Dark Mode > Navigate: /workflows > Verify: Enlaces cyan legibles > Verify: Superficies slate con contraste correcto | Sin problemas de legibilidad en dark mode | 🟡 | ❌ | ⬜ Pendiente |
| TC-050 | multi | AC-25 | Happy Path | Reactivity fix — sin layout shifts al escribir | Cualquier pantalla con búsqueda | Company Login > Sidebar: Connections > Fill "Search": escribir rápidamente "test de búsqueda larga" > Verify: Sin saltos de layout ni re-renders visibles mientras se escribe | Variable local aislada. Sin fugas de reactividad | 🟠 | ❌ | ⬜ Pendiente |

### UX/UI General (AC-26 a AC-28)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-051 | multi | AC-26 | Happy Path | Estándar PrimeVue pt — sin hacks CSS | Código del prototipo disponible | Code Review: Buscar `:deep()` o `!important` en archivos CSS/Vue de los componentes nuevos > Verify: Cero ocurrencias | Solo estilos via `pt` de PrimeVue | 🟡 | ❌ | ⬜ Pendiente |
| TC-052 | multi | AC-27 | Happy Path | Tooltips en elementos interactivos | Pantalla con tooltips | Company Login > Sidebar: Boards > Hover [Botón/icono con tooltip] > Verify: Tooltip aparece con texto informativo > Verify: Tooltip desaparece al mover mouse | Tooltips visibles y útiles | 🟡 | ✅ | ⬜ Pendiente |
| TC-053 | multi | AC-28 | Happy Path | Responsividad 1920px | Desktop 1920x1080 | Company Login > Browser: Resize 1920x1080 > Navigate: /workflows > Verify: Layout correcto, sin truncamiento > Navigate: /pdf-templates > Verify: Layout correcto | Diseño adaptado a desktop | 🟡 | ✅ | ⬜ Pendiente |
| TC-054 | multi | AC-28 | Edge Case | Responsividad 768px tablet | Tablet 768px | Company Login > Browser: Resize 768x1024 > Navigate: /workflows > Verify: Layout adaptado sin desbordamiento > Navigate: /pdf-templates > Verify: Layout adaptado | Diseño adaptado a tablet | 🟡 | ✅ | ⬜ Pendiente |
| TC-055 | multi | AC-28 | Edge Case | Responsividad 375px mobile | Mobile 375px | Company Login > Browser: Resize 375x667 > Navigate: /workflows > Verify: Layout adaptado, columnas secundarias ocultas si necesario > Navigate: /pdf-templates > Verify: Adaptado | Diseño adaptado a mobile | 🟡 | ✅ | ⬜ Pendiente |

### Preguntas Pendientes para Developer (PD — documentadas en AC)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-PD1 | pdf-templates | AC-11,16 | Edge Case | Derivación de formato sin JSONB en lista | Template con schema | Company Login > Sidebar: PDF Templates > Verify: ¿Formato visible en lista o solo al expandir? > Click [Expandir] > Verify: Formato visible en expansión | **PD-1**: Confirmar con Developer dónde se ejecuta la derivación | 🟠 | ❌ | ⏳ Bloqueado |
| TC-PD2 | boards | AC-2 | Edge Case | Switch de estado — método HTTP | Flow existente | Company Login > Sidebar: Boards > DevTools: Network > Click [FlowStatusBadge switch] > Verify: Request es PATCH (no PUT) o envía solo campo status | **PD-2**: Confirmar método HTTP y payload del switch | 🔴 | ✅ | ⏳ Bloqueado |
| TC-PD3 | boards | AC-20 | Edge Case | Migración FTS reversible | Staging con migración aplicada | Verify BD: Índice GIN existe > Ejecutar rollback de migración > Verify: Índice removido sin error | **PD-3**: Confirmar reversibilidad | 🟡 | ❌ | ⏳ Bloqueado |

---

## Casos de Regresión

| ID | Módulo impactado | Caso de regresión | Por qué podría romperse | Prioridad | Estado |
|----|-----------------|-------------------|------------------------|-----------|--------|
| REG-001 | boards | Login y acceso a /workflows | Cambios en FlowController@index y FlowListResource podrían romper la carga de la lista | 🔴 | ⬜ Pendiente |
| REG-002 | boards | Crear flow nuevo | Migraciones en tabla `flows` (FK, índice GIN) podrían afectar INSERT | 🔴 | ⬜ Pendiente |
| REG-003 | boards | Editar flow existente (canvas) | Payload Diet cambia la estructura del response. Si el canvas depende del payload completo en la lista, podría romperse al navegar | 🟠 | ⬜ Pendiente |
| REG-004 | boards | Ejecutar flow (Production mode) | Cambios en motor Go (estados terminales, execution_time, UPDATE last_execution_id) afectan la ruta de ejecución | 🔴 | ⬜ Pendiente |
| REG-005 | executions | Ver historial de ejecuciones | FK `last_execution_id` y estados terminales modificados podrían afectar la visualización del historial | 🟠 | ⬜ Pendiente |
| REG-006 | pdf-templates | Crear/editar PDF template | Nuevas columnas en `pdf_templates` + Payload Diet no deberían romper CRUD existente | 🟠 | ⬜ Pendiente |
| REG-007 | pdf-templates | Generar PDF desde nodo en flow | Incremento atómico de telemetría post-render no debe afectar la generación en sí | 🟠 | ⬜ Pendiente |
| REG-008 | connections | CRUD de connections | Integración de `ListSearchInput` no debe romper la funcionalidad existente de la lista | 🟠 | ⬜ Pendiente |
| REG-009 | auth | Login SSO Keycloak | Cambios no deberían afectar auth, pero es regresión crítica | 🔴 | ⬜ Pendiente |
| REG-010 | multi | Navegación general entre módulos | Los cambios en 8+ pantallas no deben romper el routing ni la navegación del sidebar | 🟠 | ⬜ Pendiente |

---

## Queries de Verificación BD

> ⚠️ Queries basadas en schemas de migraciones documentados en L2-modules.
> Las nuevas columnas provienen del Epic Update del Developer (2026-06-08).

```sql
-- ============================================================
-- EPIC 1 — Boards Telemetry
-- ============================================================

-- Fuente: Epic Update (2026-06-08) — "Se agregó la columna last_execution_id (con backfill de FK/índices)"
-- Tabla: flows | Columnas verificadas: id, last_execution_id

-- TC-007: Verificar que last_execution_id se actualiza post-ejecución
-- BD: PostgreSQL (tenant schema)
SELECT id, name, last_execution_id
FROM flows
WHERE id = '<flow_id>';
-- Esperado: last_execution_id = ID de la última ejecución

-- TC-004: Verificar flow sin ejecuciones
SELECT id, name, last_execution_id
FROM flows
WHERE last_execution_id IS NULL;
-- Esperado: Flows nuevos o sin ejecuciones

-- TC-013: Verificar ON DELETE SET NULL después de eliminar ejecución
-- Paso 1: Identificar ejecución referenciada
SELECT f.id as flow_id, f.last_execution_id, e.id as exec_id
FROM flows f
LEFT JOIN executions e ON f.last_execution_id = e.id
WHERE f.id = '<flow_id>';
-- Paso 2: Después de eliminar la ejecución
SELECT id, last_execution_id FROM flows WHERE id = '<flow_id>';
-- Esperado: last_execution_id = NULL

-- TC-010: Verificar execution_time corregido (bugfix)
-- Fuente: Epic Update — "Se corrigió el cálculo del tiempo de ejecución (execTime)"
SELECT id, status, execution_time
FROM executions
WHERE executable_id = '<flow_id>'
ORDER BY created_at DESC
LIMIT 5;
-- Esperado: execution_time > 0 para ejecuciones post-fix

-- ============================================================
-- EPIC 2 — PDF Templates Telemetry
-- ============================================================

-- Fuente: Epic Update — "seguimiento de generation_count y last_generated_at"
-- Tabla: pdf_templates | Columnas: generation_count, last_generated_at

-- TC-025: Verificar incremento de generation_count post-generación
SELECT id, name, generation_count, last_generated_at
FROM pdf_templates
WHERE id = '<template_id>';
-- Esperado: generation_count > 0, last_generated_at NOT NULL después de generar

-- TC-028: Verificar clone resetea telemetría
SELECT id, name, generation_count, last_generated_at
FROM pdf_templates
WHERE name LIKE '%copy%'
ORDER BY created_at DESC
LIMIT 1;
-- Esperado: generation_count = 0, last_generated_at = NULL

-- ============================================================
-- EPIC 3 — Full-Text Search
-- ============================================================

-- Fuente: Epic Update — "índice funcional GIN en el tsvector de los flujos"

-- TC-042: Verificar que el índice GIN existe
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'flows'
AND indexdef LIKE '%gin%';
-- Esperado: Al menos un índice GIN con tsvector

-- Verificar wrapper IMMUTABLE de unaccent
SELECT proname, provolatile
FROM pg_proc
WHERE proname LIKE '%unaccent%';
-- Esperado: Función IMMUTABLE-safe existente

-- ============================================================
-- REGRESIÓN
-- ============================================================

-- REG-002: Verificar que INSERT en flows sigue funcionando con la nueva FK
-- (ejecutar después de crear un flow nuevo via UI)
SELECT id, name, last_execution_id, created_at
FROM flows
ORDER BY created_at DESC
LIMIT 1;
-- Esperado: Flow creado correctamente, last_execution_id = NULL
```

---

## Code Review QA — TCs Inyectados (2026-06-25)

> Basados en el análisis estático de commits IONF-1030 en los 3 repos. Ver `code-review-qa.md`.

| ID | Módulo | AC | Tipo | Caso de Test | Pasos | Resultado Esperado | Prioridad | Estado |
|----|--------|-----|------|-------------|-------|-------------------|-----------|--------|
| TC-CR-001 | boards | AC-3 | Code Review | Backfill `last_execution_id` — flows con historial sin puntero | DBeaver > Tenant schema > `SELECT f.id, f.name, f.last_execution_id, MAX(e.id) as latest FROM flows f LEFT JOIN executions e ON e.executable_id = f.id AND e.executable_type = 'flow' GROUP BY f.id, f.name, f.last_execution_id HAVING MAX(e.id) IS NOT NULL AND f.last_execution_id IS NULL` | Query retorna 0 rows (todos los flows con ejecuciones tienen puntero correcto) | 🔴 | ⬜ Pendiente |
| TC-CR-002 | boards | AC-4 | Code Review | `deriveTerminalStatus` en modo Dev — nodo fallido desde canvas | Company Login > Sidebar: Boards > Click [Flow con nodo HTTP falible] > Canvas: Configurar nodo para que falle > Button: Ejecutar (modo Development) > Wait: Ejecución completa > Verify: Badge muestra `warning` o `error` (no `completed`) | Estado terminal NO es `completed` cuando un nodo falla. Modo Dev y Live coinciden | 🟠 | ⬜ Pendiente |
| TC-CR-003 | boards | AC-21 | Code Review | `immutable_unaccent` existe en BD + índice GIN activo | DBeaver > `SELECT proname, provolatile FROM pg_proc WHERE proname = 'immutable_unaccent'` > `SELECT indexname FROM pg_indexes WHERE indexname = 'flows_fts_idx'` | Función existe con `provolatile = 'i'`. Índice `flows_fts_idx` existe | 🔴 | ⬜ Pendiente |
| TC-CR-004 | boards | AC-9 | Code Review | Flow clonado: verificar status inicial del clon | Company Login > Sidebar: Boards > Click [FlowActionsMenu] > Click [Clonar] > Verify: Nuevo flow aparece en lista > Verify: Status inicial del clon (¿ACTIVE o INACTIVE?) > Verify BD: `SELECT status, last_execution_id FROM flows ORDER BY created_at DESC LIMIT 1` | Clon con status esperado por el negocio. `last_execution_id = NULL` | 🟠 | ⬜ Pendiente |
| TC-CR-005 | boards | AC-3 | Code Review | Badge de ejecución no cruza tenants — aislamiento multi-tenant | Login Company A > Sidebar: Boards > Verificar badges de ejecución > Login Company B > Sidebar: Boards > Verificar que Company B NO muestra ejecuciones de Company A | Los badges de ejecución están estrictamente aislados por company | 🟠 | ⬜ Pendiente |

---

## Notas

- Queries ejecutadas en DBeaver (PostgreSQL via SSH tunnel al schema del tenant)
- Para datos de ejecución de nodos, verificar via UI de historial de ejecuciones (SQLite interno)
- Fuentes de schema: `../gateway/database/migrations/*.php` y `../flow_binaries/migrations/*.sql`
- 3 TCs están **bloqueados** (TC-PD1, TC-PD2, TC-PD3) pendientes de respuesta del Developer
- Branches: `IONF-1030` mergeada en `DEVELOPMENT` — deployed 2026-06-19
- Code Review QA ejecutado 2026-06-25 — 8 hallazgos, 5 TCs inyectados
