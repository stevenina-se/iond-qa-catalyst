# Acceptance Criteria Consolidados — 86e223kvf

> Ticket: Mejoras estéticas globales en pantallas de iond / Ionflow
> Fecha de consolidación: 2026-07-20
> Fuentes: Descripción original + Comentarios del Developer (10-Jul, 20-Jul) + Risk Triage
> Modo: Discovery — los AC propuestos son SUGERENCIAS para acuerdo con el equipo

---

## Evaluación de AC Originales (Gherkin del ticket)

| AC | Texto original | ¿Verificable? | ¿Completo? | ¿Ambiguo? | Observación |
|----|---------------|----------------|------------|-----------|-------------|
| AC-G1 | "La interfaz debe verse consistente, pulida y alineada con la referencia visual definida" | ❌ | ❌ | ✅ Ambiguo | "Consistente" y "pulida" no son medibles. No define qué es la "referencia visual". |
| AC-G2 | "No se deben haber modificado submenús internos, editores profundos o backend fuera de alcance" | ✅ | ❌ | ❌ | Violado: se tocó CreateConnectionV2Dialog (editor) y hay 3 cambios de backend. |
| AC-G3 | "La tabla debe seguir el patrón visual de PDF Templates" | ⚠️ | ❌ | ✅ Ambiguo | El "patrón de PDF Templates" no está documentado formalmente. El DataTable fue reemplazado completamente. |
| AC-G4 | "La columna principal debe aprovechar mejor el ancho disponible" | ✅ | ✅ | ❌ | Verificable visualmente. |
| AC-G5 | "Modal de eliminación debe seguir el patrón normalizado" | ✅ | ✅ | ❌ | Verificable comparando con otros modales. |
| AC-G6 | "Boards mejora experiencia de entrada sin tocar el editor" | ✅ | ⚠️ | ❌ | La vista sí fue mejorada. Pero CreateConnectionV2Dialog (parte del editor) fue migrada. |
| AC-G7 | "No deben existir cambios en backend, servicios, APIs, base de datos" | ✅ | ✅ | ❌ | **VIOLADO**: Hay cambios en gateway (Laravel) y flow_binaries (Go). |
| AC-G8 | "No debe existir texto cortado, overlap, overflow horizontal inesperado" | ✅ | ✅ | ❌ | Verificable visualmente en múltiples resoluciones. |

---

## AC Consolidados — Lista Final

> Estructura: AC originales preservados + AC expandidos por divergencia + AC nuevos por features no contemplados
> Cada AC incluye su fuente y justificación

### GRUPO A — Fundación del Sistema UI (Migración Arquitectónica)

> Estos AC cubren la nueva infraestructura UI que afecta TODO lo demás.

**AC-A1**: El nuevo `TenantLayout.vue` debe cargar correctamente, preservando las 10 inyecciones de servicios existentes y el sync de `window.$useFlowCore.setUser`.
- Fuente: Comentario Developer 20-Jul — "preservando las 10 inyecciones de servicios existentes y el sync de `window.$useFlowCore.setUser`"
- Riesgo: R-01 (🔴 Crítico)

**AC-A2**: El sistema de aislamiento CSS (wrapper `.modern-ui`) debe garantizar cero regresiones visuales en las pantallas de Admin/Legacy que usan PrimeVue. No debe haber bleeding de estilos Tailwind hacia componentes PrimeVue ni viceversa.
- Fuente: Comentario Developer 10-Jul — "garantizando cero regresiones visuales en las pantallas no migradas"
- Riesgo: R-02 (🔴 Crítico)

**AC-A3**: El nuevo componente DataTable (shadcn/TanStack Table) debe soportar paginación SSR, ordenamiento por columna, y visibilidad de columnas en todas las 14 pantallas migradas, con el mismo contrato de parámetros que el DataTable anterior de PrimeVue.
- Fuente: Comentario Developer 20-Jul — "integración total de composables avanzados (useColumnVisibility, hide columns, resize, sort) mapeados a la paginación real SSR pre-existente"
- Riesgo: R-03 (🔴 Crítico)

**AC-A4**: La navegación lateral (`TenantSidebar`), barra superior (`TenantTopbar`), y breadcrumbs (`useCrumbs`) deben funcionar correctamente, mostrando las secciones según los permisos del usuario y con la estructura reorganizada del menú.
- Fuente: Comentario Developer 20-Jul — App Shell
- Riesgo: R-05 (🟠 Alto)

**AC-A5**: El sistema de notificaciones toast (`useToast()` vía adapter vue-sonner) debe funcionar para los ~168 call sites existentes sin regresión. Las notificaciones duplicadas idénticas deben deduplicarse (no apilarse).
- Fuente: Comentario Developer 20-Jul — "reutiliza ${tone}:${message} como id de toast para deduplicar"
- Riesgo: R-04 (🟠 Alto)

---

### GRUPO B — Features Nuevos Transversales

**AC-B1**: La búsqueda global (Cmd/Ctrl+K) debe abrir un command palette que busque en flows, apps y appActions con debounce, mostrando resultados relevantes y persistiendo hasta 10 búsquedas recientes en localStorage.
- Fuente: Comentario Developer 20-Jul — GlobalSearch
- Riesgo: R-09 (🟠 Alto)

**AC-B2**: El toggle de tema claro/oscuro debe funcionar correctamente con transición visual suave (View Transitions API donde esté soportada) y fallback instantáneo en navegadores sin soporte o con `prefers-reduced-motion: reduce`.
- Fuente: Comentario Developer 20-Jul — useThemeTransition
- Riesgo: R-12 (🟡 Medio)

**AC-B3**: La vista de soporte (`SupportView.vue`) debe ser accesible desde la navegación y funcionar correctamente.
- Fuente: Comentario Developer 20-Jul — "un nuevo SupportView.vue (técnicamente fuera de alcance)"
- Riesgo: R-15 (🟢 Bajo)

---

### GRUPO C — Pantallas Migradas (14 Áreas)

> Cada pantalla migrada hereda los AC-A (fundación). Estos AC cubren aspectos específicos por pantalla.

**AC-C1**: Cada una de las 14 pantallas migradas (webhooks, accounts, keys, activity, pdf-templates, dashboard, settings, profile, data-store/data-structure, integrations/connections, app connectors, workflows/boards, executions, support) debe:
- (a) Cargar sin errores de consola (JS errors)
- (b) Mostrar datos existentes correctamente en el nuevo DataTable
- (c) Soportar las acciones CRUD que tenía anteriormente (crear, editar, eliminar si aplica)
- (d) Mostrar modales de confirmación normalizados
- (e) No presentar texto cortado, overlap, ni overflow horizontal
- Fuente: AC originales G1, G4, G5, G8 + Comentario Developer 20-Jul
- Riesgo: R-03 (🔴 por multiplicación en 14 pantallas)

**AC-C2**: La vista de PDF Templates debe servir como **referencia visual** del patrón de diseño aplicado a las demás tablas. Las tablas en las demás pantallas deben seguir el mismo patrón de headers, filas, acciones y estados.
- Fuente: Descripción original — "referencia más importante es el diseño de tablas de PDF Templates"
- Riesgo: Medio

**AC-C3**: La primera vista de Boards/Workflows debe estar mejorada visualmente. El editor interno de Boards (canvas) NO debe haber sido modificado.
- Fuente: AC original G6
- ⚠️ Nota: `CreateConnectionV2Dialog` fue migrada pese a estar en el spec como "escalar, no tocar". Verificar que el flujo de creación de conexiones funciona correctamente.
- Riesgo: R-06 (🟠 Alto)

**AC-C4**: La pantalla de Executions (pantalla piloto de la migración) debe:
- (a) Mostrar el listado de ejecuciones con el nuevo DataTable
- (b) Soportar filtro por `status` (case-insensitive)
- (c) Soportar filtro por rango de fechas (`date_from`/`date_to`)
- (d) Mantener la paginación SSR funcional
- Fuente: Comentario Developer 20-Jul §2 — "ExecutionController@index gana filtros de status y rango de fechas"
- Riesgo: R-07 (🟠 Alto)

**AC-C5**: La pantalla de Data Store / Data Structure debe:
- (a) Mostrar el listado con búsqueda por nombre funcional
- (b) Soportar filtrado y ordenamiento por id, name, created_at
- (c) El StoreViewer (modal de visualización de datos) debe funcionar con datos anidados
- (d) Caracteres especiales en búsqueda (`%`, `_`, `\`) deben escaparse correctamente
- Fuente: Comentario Developer 20-Jul §3 — "Search/Filter/Sort en Data Store & Data Structure"
- Riesgo: R-08 (🟠 Alto)

**AC-C6**: La pantalla de Accounts debe soportar filtro por `timezone` y ordenamiento por `remote_id`.
- Fuente: Comentario Developer 20-Jul §3 — "filtro por timezone en accounts, remote_id como campo ordenable"
- Riesgo: R-10 (🟡 Medio)

**AC-C7**: La pantalla de Keys/Credentials debe soportar filtro por `provider` (metadata) con el nuevo helper `applyProviderFilter()` nil-safe.
- Fuente: Comentario Developer 20-Jul §3 — "applyProviderFilter() para filtrar keys por metadata->>'provider'"
- Riesgo: R-11 (🟡 Medio)

---

### GRUPO D — Backend (Cambios de API — Divergencia del AC original)

> ⚠️ El AC original G7 decía "No deben existir cambios en backend". 
> Estos AC documentan los cambios de backend que SÍ se realizaron.

**AC-D1**: Los nuevos filtros del endpoint `GET /1.0/tenants/{tenant}/executions` (status, date_from, date_to) deben funcionar correctamente:
- `status`: case-insensitive, tipo string (no array)
- `date_from`/`date_to`: filtro por `created_at` con `whereDate`, inclusivo en ambos extremos
- Fuente: Comentario Developer 20-Jul §2
- Riesgo: R-07

**AC-D2**: La búsqueda en Data Store/Data Structure (SQLite por tenant) debe:
- Escapar correctamente `\`, `%`, `_` con `searchLikeEscaper`
- Usar `ESCAPE '\'` explícito para SQLite
- La paginación via `BuildStorePaginationConfig` debe aplicar whitelist `{id, name, created_at}`
- Fuente: Comentario Developer 20-Jul §3
- Riesgo: R-08

**AC-D3**: El campo `description` de flows debe persistirse correctamente cuando se actualiza vía `UpdateCompanyFlow`.
- Fuente: Comentario Developer 20-Jul §3 — "FlowParams gana Description *string, Select() ampliado"
- Riesgo: R-14 (🟡 Medio)

---

### GRUPO E — Regresión y Calidad

**AC-E1**: Las pantallas Admin (que usan PrimeVue) deben funcionar sin ninguna regresión visual ni funcional después de los cambios.
- Fuente: Comentario Developer 10-Jul — estrategia de aislamiento CSS
- Riesgo: R-02 (🔴 Crítico)

**AC-E2**: Las traducciones (i18n) deben tener paridad entre `en` y `es` para todas las keys nuevas (+237 en / +228 es).
- Fuente: Comentario Developer 20-Jul — "i18n: +237 keys en/+228 keys es"
- Riesgo: R-13 (🟡 Medio)

**AC-E3**: El responsive básico debe validarse en las primeras vistas migradas — sin textos cortados, overlap, ni overflow horizontal en desktop (1920px, 1366px) y tablet (1024px).
- Fuente: AC original G8
- Riesgo: Medio

---

## AC Rechazados o Diferidos

| AC Propuesto | Razón de exclusión |
|---|---|
| AC original G7 "No cambios de backend" | **SUPERADO POR LA REALIDAD**: El developer implementó cambios de backend. Se reemplaza por AC-D1, AC-D2, AC-D3 que documentan los cambios reales. |
| Testing del canvas/editor de Boards | Fuera de alcance explícito del ticket. Solo la primera vista. |
| Testing de pantallas Admin (funcionalidad) | Solo se verifica regresión visual (AC-E1), no funcionalidad del Admin. |

---

## Transformación AC → Casos de Test (Preview)

> Tabla resumen — los test cases detallados se generarán en la Test Matrix (Paso 5)

| AC | Happy Path | Edge Case | Negativo |
|----|-----------|-----------|----------|
| AC-A1 (TenantLayout) | App tenant carga correctamente con todos los servicios | App carga después de sesión expirada | Un servicio no está disponible al mount |
| AC-A2 (CSS Isolation) | Admin y Tenant coexisten sin conflictos visuales | Navegar rápido entre Admin y Tenant | Clase `.modern-ui` aplicada fuera de Tenant |
| AC-A3 (DataTable) | Tabla muestra datos, pagina, ordena | >1000 registros, columnas ocultas | Sort por columna inválida |
| AC-A4 (Navigation) | Menú visible según permisos del rol | Usuario con permisos parciales | Ruta no existente en el menú |
| AC-A5 (Toast) | Toast success/error/warning aparece | 3 toasts idénticos rápidos (dedup) | Call site legacy con formato inesperado |
| AC-B1 (GlobalSearch) | Cmd+K busca y muestra resultados | Búsqueda rápida cambiando query | Sin resultados / query vacío |
| AC-B2 (Dark Mode) | Toggle cambia tema correctamente | Browser sin View Transitions | Dark mode + componente PrimeVue residual |
| AC-C1 (14 pantallas) | Cada pantalla carga y muestra datos | Pantalla sin datos (empty state) | Error de API al cargar |
| AC-C4 (Executions) | Filtrar por status y fecha | date_from > date_to / status array | Status inexistente |
| AC-C5 (Data Store) | Buscar por nombre, ordenar, paginar | Buscar con `%`, `_`, `\` | Data Store vacío / BD no existe |
| AC-D1 (API Executions) | GET con status=completed retorna ok | status="RUNNING" (case) | status como array [] |
| AC-E1 (Admin regresión) | Pantallas Admin visualmente intactas | Admin + Tenant abiertos en tabs | — |

---

## Resumen

| Métrica | Valor |
|---------|-------|
| AC Originales Gherkin | 8 |
| AC Consolidados finales | 20 |
| AC de Fundación (Grupo A) | 5 |
| AC de Features Nuevos (Grupo B) | 3 |
| AC de Pantallas (Grupo C) | 7 |
| AC de Backend (Grupo D) | 3 |
| AC de Regresión (Grupo E) | 3 |
| AC Rechazados/Diferidos | 3 |
