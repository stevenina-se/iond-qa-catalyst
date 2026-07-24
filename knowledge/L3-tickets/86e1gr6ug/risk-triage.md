# Risk Triage — 86e1gr6ug (Mejoras de la interface en ionflow dualtrack)

> Última actualización: 2026-06-08 11:07 — Incorpora Epic Update del Developer (2026-06-08 10:47)

## Resumen
- Módulo principal: **boards** (EPIC 1 — Flow Execution Telemetry)
- Módulos impactados: **pdf-templates** (EPIC 2), **connections, integrations, keys, accounts, developer-apps, services** (EPIC 3 — Unified Search)
- Riesgo general: 🟠 Alto
- Total edge cases identificados: 27
- Total preguntas para Developer: 17 (14 originales + 3 pendientes post-matrix)
- Contexto de ClickUp: 3 comentarios leídos, divergencias significativas reconciliadas
- **Scope real**: ~73 archivos (35 frontend, 9 Laravel, 29 Go) en 8+ pantallas

---

## Análisis de Lógica de Negocio

| Pregunta | Análisis |
|----------|----------|
| ¿El feature respeta las reglas multi-tenant (company)? | ✅ Sí — Todos los cambios operan en `CompanySchema()`. **Reforzado**: ILIKE search en Go aplica filtro de tenant PRIMERO, luego ILIKE, luego Count/Paginación → previene cruces entre companies. |
| ¿Afecta la ejecución de flows/nodos? | ⚠️ **Sí** — EPIC 1 modifica post-ejecución (UPDATE `last_execution_id`). EPIC 2 incrementa `generation_count` (best-effort). Bugfix de `execution_time`. |
| ¿Hay impacto en connectors globales vs company? | ⚠️ **Indirecto** — La expansión de boards ahora separa "GLOBAL" vs "TENANT" apps used. Si la derivación falla, las apps podrían mostrarse en la categoría incorrecta. |
| ¿Se tocan datos de ejecución (SQLite) o datos persistentes (PostgreSQL)? | ⚠️ **Sí, ampliamente** — EPIC 1: FK en `flows` (PG). EPIC 2: columnas en `pdf_templates` (PG). EPIC 3: Índice funcional GIN + wrapper IMMUTABLE para FTS (PG). Migraciones en gateway y flow_binaries. |
| ¿Hay impacto en el sistema de permisos por usuario/company? | ✅ No directo — pero la búsqueda ILIKE refuerza el aislamiento por tenant. |
| ¿El feature puede romper flujos de e-commerce existentes? | ⚠️ **Riesgo bajo pero amplio** — El Payload Diet cambia la estructura de las respuestas API. Si el frontend antiguo depende del payload completo, podría romperse. El switch de estado debe no sobrescribir el grafo. |

---

## Análisis de Impacto por Módulo

### EPIC 1 — Boards Telemetry + Payload Diet + Clone

| Área | Impacto | Riesgo |
|------|---------|--------|
| **Frontend** — `/workflows` lista | Nuevos componentes: `BoardDetailsCell`, `FlowRunCell`, `FlowStatusBadge`, `FlowActionsMenu`, `FlowPreviewDrawer`, `helpers/flow.ts` | 🟠 Alto |
| **API** — `FlowListResource` (Laravel) | Payload Diet: reduce a `{nodes:[id,type], edges:[source,target]}` + `last_execution` ligero. Eager-load con columnas limitadas. Previene COUNT implícitos | 🟠 Alto |
| **API** — `POST flows/{flow}/clone` | Nuevo endpoint de clonación nativa con `replicate()` de Eloquent | 🟠 Alto |
| **BD PostgreSQL** — tabla `flows` | FK `last_execution_id` + backfill + índice GIN para FTS + wrapper IMMUTABLE | 🔴 Crítico |
| **Backend Go** — motor de ejecución | Estados terminales (`completed`/`StatusWarning`/`error`), UPDATE atómico, bugfix `execution_time` | 🔴 Crítico |
| **Módulos afectados** — Executions | FK flows → executions con `ON DELETE SET NULL` | 🟠 Alto |

### EPIC 2 — PDF Templates + Clone nativo

| Área | Impacto | Riesgo |
|------|---------|--------|
| **Frontend** — `/pdf-templates` lista | Nuevos componentes: `PdfTemplateDetailsCell`, `PdfTemplateStatusBadge`, `PdfTemplatePreview`, formateadores | 🟠 Alto |
| **API Go HUB** — Payload Diet | `ListPdfTemplatesByCompany` selecciona solo columnas de lista, elimina JSONB del schema | 🟠 Alto |
| **API Go HUB** — `ClonePdfTemplateByCompany` | Copia profunda de esquemas, sufijo " (copy)", reset telemetría | 🟠 Alto |
| **BD PostgreSQL** — `pdf_templates` | `generation_count` (unsigned, default 0) + `last_generated_at` (nullable) | 🟡 Medio |
| **Backend Go** — PdfTemplateAction | Incremento atómico best-effort post-render | 🟡 Medio |

### EPIC 3 — Unified Search & Lazy Catalog

| Área | Impacto | Riesgo |
|------|---------|--------|
| **Frontend** — 6 pantallas | `ListSearchInput` + `useListQuerySync` integrado en Connections, Integrations, Keys, Accounts, Developer Apps, Services | 🟠 Alto |
| **Frontend** — `useAppCatalog` | Singleton lazy con cooldown 30s | 🟡 Medio |
| **BD PostgreSQL** — FTS | Wrapper IMMUTABLE-safe para `unaccent` + índice funcional GIN en tsvector de flows | 🟠 Alto |
| **Backend Go** — `search_helpers.go` | `applyILIKE` (anti-injection) + `applyPagination` en 5 servicios | 🟠 Alto |

### EPIC 4 — UI Polish, A11y & Safety

| Área | Impacto | Riesgo |
|------|---------|--------|
| **A11y** | Keyboard nav, ARIA, motion-reduce, focus-visible | 🟡 Medio |
| **Safety** | `pointer-events-none` durante recarga | 🟡 Medio |
| **Dark Mode** | Contraste de enlaces cyan y superficies slate | 🟡 Medio |
| **Reactivity** | Aislamiento de variable de búsqueda | 🟡 Medio |

---

## Edge Cases Identificados

### EPIC 1 — Boards

| # | Edge Case | Severidad | Área |
|---|-----------|-----------|------|
| EC-01 | Flow sin ejecución previa (`last_execution_id = NULL`) — ¿qué badge? | 🟠 | Frontend |
| EC-02 | Ejecución purgada (`ON DELETE SET NULL`) — ¿badge se resetea? | 🟠 | BD/Frontend |
| EC-03 | Flow con `StatusWarning` — ¿visualización vs `error`? | 🟠 | Frontend |
| EC-04 | Fallo del UPDATE atómico a `last_execution_id` | 🔴 | Backend Go |
| EC-05 | Company con 500+ flows — eager-load performance con payload diet | 🟠 | API |
| EC-06 | Backfill de `last_execution_id` — flows sin ejecuciones → NULL | 🟡 | Migración |
| EC-07 | `execution_time` históricas con valor ~0s (pre-bugfix) | 🟡 | Backend Go |
| EC-08 | Concurrencia: dos ejecuciones terminan simultáneamente | 🟠 | Backend Go |
| EC-09 | **FlowStatusBadge: switch envía PUT con payload reducido — ¿sobrescribe grafo?** | 🔴 | Frontend/API |
| EC-10 | **Clonar flow: `replicate()` excluye tenant refs — ¿qué pasa si el flow referencia connectors de otra company?** | 🟠 | API |
| EC-11 | **Expandir fila: solicita flow completo del HUB — ¿qué pasa si el HUB está caído?** | 🟡 | Frontend |

### EPIC 2 — PDF Templates

| # | Edge Case | Severidad | Área |
|---|-----------|-----------|------|
| EC-12 | Template sin schema JSONB — ¿adaptador crashea? | 🟠 | Frontend |
| EC-13 | Template sin variables → "Borrador" correcto | 🟡 | Frontend |
| EC-14 | Template nunca usado → "Nunca usado" badge | 🟡 | Frontend |
| EC-15 | **Clonar PDF: nombre largo + " (copy)" excede límite de columna** | 🟡 | Backend Go |
| EC-16 | Exportar JSON — ¿reimportable? | 🟡 | Frontend |
| EC-17 | Formato no reconocido en schema pdfme | 🟡 | Frontend |
| EC-18 | Fallo incremento atómico `generation_count` | 🟡 | Backend Go |
| EC-19 | Preview con dimensiones extremas | 🟡 | Frontend |
| EC-20 | **Payload Diet: lista sin JSONB → ¿derivación de formato/campos imposible en vista de lista?** | 🔴 | Frontend/API |

### EPIC 3 — Unified Search

| # | Edge Case | Severidad | Área |
|---|-----------|-----------|------|
| EC-21 | **Búsqueda con caracteres especiales `% _ \` en ILIKE — ¿escapados correctamente?** | 🟠 | Backend Go |
| EC-22 | **FTS con inyección SQL via tsvector** | 🟠 | BD/Laravel |
| EC-23 | **Búsqueda con acentos — `unaccent` wrapper IMMUTABLE funciona** | 🟡 | BD |
| EC-24 | **Enter sin texto → ¿resetea filtro o no hace nada?** | 🟡 | Frontend |
| EC-25 | **URL con `?search=` al cargar — ¿se aplica el filtro automáticamente?** | 🟡 | Frontend |

### EPIC 4 — UI Polish

| # | Edge Case | Severidad | Área |
|---|-----------|-----------|------|
| EC-26 | Tooltips en responsive — posicionamiento | 🟡 | Frontend |
| EC-27 | `pointer-events-none` — ¿se remueve correctamente al terminar la recarga? | 🟡 | Frontend |

---

## Preguntas para el Developer

### [LÓGICA DE NEGOCIO] (originales)

1. **EPIC 1 — Atomicidad del UPDATE**: Si `UPDATE flows SET last_execution_id = ?` falla, ¿la ejecución queda en `executions` pero el puntero no se actualiza? ¿O hay rollback?

2. **EPIC 1 — Estado `warning`**: ¿Cómo se determina "falla parcial de un nodo" para `StatusWarning`? ¿Al menos un nodo con `StatusError` pero flow completó?

3. **EPIC 2 — Política best-effort**: Si `generation_count` falla silenciosamente, ¿hay reconciliación futura?

4. **EPIC 2 — Campo `status` original**: ¿Se elimina de la BD o solo se deja de usar en frontend?

### [EDGE CASES] (originales)

5. **EPIC 1 — Concurrencia**: ¿El UPDATE a `last_execution_id` es realmente atómico? ¿Usa CAS o simple WHERE?

6. **EPIC 1 — Poda**: Con `ON DELETE SET NULL`, ¿hay proceso que busque nueva última ejecución?

7. **EPIC 2 — Formato desconocido**: Si dimensiones no mapean a tamaño nombrado, ¿retorna "Custom"?

### [INTEGRACIÓN] (originales)

8. **EPIC 1 — API Laravel**: `?includes=lastExecution` — ¿controlador existente o nuevo?

9. **EPIC 1 — Expansión flow-canvas**: ¿Reutiliza `webcomponents-flow` o preview simplificado?

10. **EPIC 2 — Migración dual**: ¿Se ejecuta desde Laravel o desde ambos repos?

### [UX/UI] (originales)

11. **Tooltips**: ¿Componente nativo PrimeVue o custom? ¿Qué elementos los tienen?

12. **Responsividad**: ¿Breakpoints definidos? ¿Columnas de telemetría se ocultan en mobile?

13. **PrimeVue `pt`**: ¿Theme/preset existente o estilos desde cero por componente?

### [NUEVAS — del Epic Update]

14. **Flow Clone**: `replicate()` excluye tenant refs, commits, ejecuciones — ¿el nombre del clon tiene sufijo? ¿Qué pasa con webhooks asociados al flow original?

### [PENDIENTES POST-MATRIX] (no preguntar aún)

15. **PD-1**: ¿Payload Diet de PDF elimina JSONB → derivación de formato/campos solo al expandir?
16. **PD-2**: ¿FlowStatusBadge envía PATCH o PUT? ¿Cómo evita sobrescribir campos del payload reducido?
17. **PD-3**: ¿Migración FTS (wrapper IMMUTABLE + índice GIN) reversible? ¿Impacto en rendimiento de escritura?

---

## Tabla de Riesgos Priorizada

| ID | Área | Riesgo | Descripción | Prioridad | Justificación |
|----|------|--------|-------------|-----------|---------------|
| R-001 | Backend Go — Motor de ejecución | 🔴 Crítico | Modificación de la ruta de finalización: estados terminales + UPDATE atómico + bugfix execution_time. Error aquí afecta TODAS las ejecuciones. | 1 | Core del producto |
| R-002 | BD — Migraciones `flows` | 🔴 Crítico | FK `last_execution_id` + backfill + índice GIN FTS + wrapper IMMUTABLE. Tabla más crítica del sistema. | 2 | 4 cambios en la misma tabla crítica |
| R-003 | API — Payload Diet (Boards) | 🟠 Alto | `FlowListResource` reduce payload. Si el switch de estado envía el objeto reducido → corrupción de grafo. | 3 | Riesgo de corrupción de datos |
| R-004 | API — Payload Diet (PDF) | 🟠 Alto | Lista sin JSONB del schema. ¿Derivación de formato/campos imposible en vista de lista? | 4 | Rompe contrato del EPIC 2 original |
| R-005 | Backend Go — PdfTemplateAction | 🟠 Alto | Incremento atómico + Clone nativo con copia profunda de esquemas | 5 | Acción de renderizado no debe verse afectada |
| R-006 | Frontend — `mapFlowRunState()` | 🟠 Alto | Deriva runState/severity. Error → badges incorrectos en TODOS los flows | 6 | Impacto visual masivo |
| R-007 | Backend Go — ILIKE Search | 🟠 Alto | `applyILIKE` en 5 servicios. Si el escape falla → inyección SQL. Si el tenant filter falla → data leak | 7 | Seguridad |
| R-008 | BD — FTS Infrastructure | 🟠 Alto | Wrapper IMMUTABLE + índice GIN. Si la migración falla → búsqueda no funciona | 8 | Infraestructura nueva |
| R-009 | Frontend — Clone nativo (Flow + PDF) | 🟠 Alto | Nuevos endpoints. El clon debe ser limpio (sin historial, sin tenant refs) | 9 | Integridad de datos |
| R-010 | Frontend — Unified Search (6 pantallas) | 🟠 Alto | `ListSearchInput` + `useListQuerySync` en 6 pantallas. Error → búsqueda rota en múltiples vistas | 10 | Blast radius amplio |
| R-011 | Frontend — Adaptadores schema pdfme | 🟠 Alto | `getFormat`, `getDynamicFields`, `isDraft`, `blueprintSize`. Schema inesperado → crash | 11 | Derivación de datos |
| R-012 | Frontend — A11y + Safety | 🟡 Medio | Keyboard nav, ARIA, pointer-events-none, dark mode | 12 | UX/accesibilidad |
| R-013 | Frontend — Tooltips + Responsividad | 🟡 Medio | Tooltips sin especificación de elementos. Responsividad sin breakpoints | 13 | Underspecified |
| R-014 | Frontend — Lazy Catalog + Reactivity | 🟡 Medio | Singleton con cooldown. Aislamiento de variable de búsqueda | 14 | Performance |

---

## Recomendación

### Máxima atención en Deployment:
1. **Motor Go (R-001)**: Verificar con ejecuciones reales que estados terminales y execution_time son correctos
2. **Migraciones (R-002)**: 4 cambios en tabla `flows` — ejecutar en staging y verificar con queries
3. **Payload Diet + Switch de estado (R-003)**: Verificar que el switch NO sobrescribe el grafo reducido
4. **Payload Diet PDF (R-004)**: Aclarar con Developer cómo funciona la derivación sin JSONB en lista
5. **Búsqueda ILIKE (R-007)**: Probar inyección SQL y verificar aislamiento por tenant

### Scope expandido — impacto en testing:
El Epic Update expandió el scope de **2 pantallas → 8+ pantallas** y de **2 EPICs → 4 EPICs**. Esto incrementa significativamente el esfuerzo de testing necesario.
