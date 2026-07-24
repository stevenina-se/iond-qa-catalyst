# Risk Triage — 86e223kvf

> Ticket: Mejoras estéticas globales en pantallas de iond / Ionflow
> Módulo principal: Multi-módulo (UI/UX global — migración arquitectónica)
> Fecha: 2026-07-20
> Track: Discovery

---

## Resumen

- **Módulo principal**: Multi-módulo — Migración UI Framework (PrimeVue → Tailwind 4 + shadcn-vue)
- **Módulos impactados**: boards, executions, pdf-templates, data-store, accounts, keys, webhooks, integrations, connections, dashboard, settings, profile, support (nuevo)
- **Riesgo general**: 🔴 Crítico
- **Total edge cases identificados**: 28
- **Total preguntas para Developer**: 15
- **Contexto de ClickUp**: 2 comentarios leídos, 12 divergencias documentadas (3 críticas, 6 altas, 3 medias)

---

## Paso 1: Análisis de Lógica de Negocio

| Pregunta | Análisis |
|----------|----------|
| ¿El feature respeta las reglas multi-tenant (company)? | ⚠️ **Requiere verificación**. El nuevo `TenantLayout` reemplaza `CompanyLayout` y preserva las 10 inyecciones de servicios (incluido `window.$useFlowCore.setUser`). Si alguna inyección falla, el aislamiento multi-tenant podría romperse. El dev dice haberlo preservado, pero es un área de alto riesgo. |
| ¿Afecta la ejecución de flows/nodos? | ⚠️ **Sí, indirectamente**. (1) `CreateConnectionV2Dialog` fue migrada — un bug aquí rompe la creación de conexiones que los flows necesitan. (2) Flow `description` fix en flow_binaries (`FlowParams.Description`) — cambio en cómo se persiste la descripción del flow. |
| ¿Hay impacto en connectors globales vs company? | 🟢 **No directamente**. Los cambios son de UI — la lógica de connectors no cambia. Pero los listados de connectors fueron migrados al nuevo DataTable. |
| ¿Se tocan datos de ejecución (SQLite) o datos persistentes (PostgreSQL)? | 🔴 **Sí**. (1) Data Store/Data Structure: nuevo search/filter/sort con `searchLikeEscaper` y `BuildStorePaginationConfig` (SQLite). (2) Accounts: filtro `timezone` (Postgres). (3) Keys: `applyProviderFilter()` (Postgres). (4) Executions: filtros `status` + `date_from/date_to` (Postgres). (5) Flow description: fix en `Select(...)` de gorm. |
| ¿Hay impacto en el sistema de permisos por usuario/company? | 🟡 **Indirecto**. El nuevo layout preserva RBAC según el dev, pero la reorganización de navegación (`menu.ts`) cambió la estructura de secciones. Si un permiso no mapea correctamente, secciones podrían quedar inaccesibles o visibles incorrectamente. |
| ¿El feature puede romper flujos de e-commerce existentes? | ⚠️ **Posible**. Si `CreateConnectionV2Dialog` tiene regresión (el dev reportó un bugfix en `activeTab`), crear nuevas conexiones OAuth podría fallar → flows sin auth → ejecuciones fallidas → pedidos/inventario no procesados. |

---

## Paso 2: Análisis de Impacto por Módulo

### Capa 1: Fundación (afecta TODO lo demás)

| Área | Impacto | Riesgo |
|------|---------|--------|
| **TenantLayout (nuevo shell)** | Reemplaza `CompanyLayout`. 10 inyecciones de servicios. `setUser` sync. Si falla, toda la app tenant queda inutilizable. | 🔴 Crítico |
| **Sistema de tokens CSS (theme.css)** | Nuevo sistema completo bajo `.modern-ui`. Si el scoping falla, regresión visual en Admin/Legacy. | 🔴 Crítico |
| **DataTable primitivo (shadcn)** | Reemplaza PrimeVue DataTable en 14 áreas. Paginación SSR, sort, column visibility. | 🔴 Crítico |
| **Sidebar + Topbar + Navigation** | `TenantSidebar`, `TenantTopbar`, `useCrumbs`. Reorganización de `menu.ts`. | 🟠 Alto |

### Capa 2: Features nuevos transversales

| Área | Impacto | Riesgo |
|------|---------|--------|
| **Dark/Light mode toggle** | View Transitions API con fallback. `useThemeTransition.ts`. | 🟡 Medio |
| **Global Search (Cmd/Ctrl+K)** | Command palette con debounce 600ms, fetch paralelo, AbortController, localStorage. | 🟠 Alto |
| **Toast system (vue-sonner)** | `useToast()` adapter sobre `vue-sonner`. Deduplicación por `${tone}:${message}`. ~168 call sites existentes. | 🟠 Alto |
| **Breadcrumbs (useCrumbs)** | Derivados de config de navegación + route-meta. `href: undefined` en último crumb. | 🟡 Medio |

### Capa 3: Pantallas migradas (14 áreas)

| Pantalla | Cambio UI | Cambio Backend | Riesgo |
|----------|-----------|---------------|--------|
| **Executions** | Reescritura completa (pantalla piloto) | ✅ Filtros status + date_from/date_to | 🔴 Crítico |
| **Data Store / Data Structure** | `StoreViewer` reescrito (Paginator+DataTable+Tree → shadcn) | ✅ Search/filter/sort SQLite + bugfix nil pagination | 🔴 Crítico |
| **Boards/Workflows** | Vista lista migrada (NO editor) | ❌ No | 🟠 Alto |
| **Connections (App Connectors)** | Vista lista migrada | ❌ No | 🟠 Alto |
| **Integrations** | Vista + `CreateConnectionV2Dialog` migrada + bugfix activeTab | ❌ No | 🟠 Alto |
| **Accounts** | Vista migrada | ✅ Filtro timezone + remote_id ordenable | 🟠 Alto |
| **Keys/Credentials** | Vista migrada | ✅ `applyProviderFilter()` provider metadata | 🟠 Alto |
| **PDF Templates** | Vista migrada (referencia visual de diseño) | ❌ No | 🟠 Alto |
| **Webhooks** | Vista migrada | ❌ No | 🟡 Medio |
| **Dashboard** | Vista migrada | ❌ No | 🟡 Medio |
| **Activity** | Vista migrada | ❌ No | 🟡 Medio |
| **Settings** | Vista migrada | ❌ No | 🟡 Medio |
| **Profile** | Vista migrada | ❌ No | 🟡 Medio |
| **Support** (nuevo) | Vista nueva fuera de scope original | ❌ No | 🟢 Bajo |

### Capa 4: Backend (cambios de API)

| Repo | Cambio | Riesgo |
|------|--------|--------|
| **gateway (Laravel)** | `ExecutionController@index`: filtros status (case-insensitive `whereRaw LOWER()`), date_from/date_to (`whereDate`). Guardia contra array en status. | 🟠 Alto |
| **flow_binaries (Go)** | Data Store: `searchLikeEscaper` (escape `\`, `%`, `_`), `nameSearchClause` con `ESCAPE '\'` para SQLite. `BuildStorePaginationConfig` migrado a struct. Bugfix nil pagination → whitelist `{id, name, created_at}`. | 🟠 Alto |
| **flow_binaries (Go)** | Accounts: `remote_id` sortable, filtro `timezone`. Keys: `applyProviderFilter()` nil-safe. | 🟡 Medio |
| **flow_binaries (Go)** | Flow: `FlowParams.Description *string`, `.Select(...)` ampliado con `"description"`. | 🟡 Medio |

---

## Paso 3: Edge Cases Identificados

### 🔴 Edge Cases Críticos (Fundación)

| EC | Área | Descripción | Condición |
|----|------|-------------|-----------|
| EC-01 | CSS Isolation | Las pantallas Admin (PrimeVue) se rompen visualmente porque el global reset de Shadcn escapa del scope `.modern-ui` | Admin navega pantallas legacy |
| EC-02 | CSS Isolation | Colisión de nombres: `bg-primary` de Tailwind sobreescribe `bg-primary` de PrimeVue en Admin | Admin con ambos CSS cargados |
| EC-03 | TenantLayout | Una de las 10 inyecciones de servicio falla → toda la app tenant no carga | Cualquier servicio no disponible al mount |
| EC-04 | TenantLayout | `window.$useFlowCore.setUser` no sincroniza → canvas/webcomponents-flow no reconoce al usuario | Usuario navega al editor de flows |
| EC-05 | DataTable | Paginación SSR no funciona con el nuevo componente → tabla muestra datos incorrectos o no pagina | Tabla con >25 registros |
| EC-06 | DataTable | Sort no funciona o invierte la dirección respecto al DataTable anterior | Usuario ordena columnas |

### 🟠 Edge Cases Altos (Features nuevos)

| EC | Área | Descripción | Condición |
|----|------|-------------|-----------|
| EC-07 | Toast | Los ~168 call sites existentes de `useToast()` no son compatibles con el nuevo adapter vue-sonner | Cualquier acción que dispara toast |
| EC-08 | Toast | La deduplicación por `${tone}:${message}` falla y los toasts se apilan | Acciones rápidas repetidas |
| EC-09 | GlobalSearch | Fetch paralelo genera race condition — resultados de una búsqueda anterior aparecen después de la nueva | Búsqueda rápida con cambio de query |
| EC-10 | GlobalSearch | AbortController no cancela correctamente → memory leak con requests pendientes | Múltiples búsquedas rápidas sin seleccionar |
| EC-11 | GlobalSearch | localStorage con 10 búsquedas recientes falla en modo privado/incógnito | Navegador en modo privado |
| EC-12 | Dark Mode | View Transitions API no soportada → fallback no activa correctamente el modo oscuro | Firefox u otro browser sin View Transitions |
| EC-13 | Dark Mode | Toggle rompe estilos de componentes legacy/PrimeVue | Dark mode activo en pantallas con componentes mixtos |
| EC-14 | CreateConnectionV2Dialog | El bugfix de `activeTab` introduce regresión: cuando ambas conexiones resuelven, el tab incorrecto queda seleccionado | Connector con primary + secondary connection |
| EC-15 | CreateConnectionV2Dialog | Migración a primitivos nuevos rompe el flujo OAuth (redirect → callback → formulario) | Crear nueva conexión OAuth |

### 🟡 Edge Cases Medios (Pantallas migradas)

| EC | Área | Descripción | Condición |
|----|------|-------------|-----------|
| EC-16 | Executions | Filtro `status` case-insensitive no funciona con valores mixtos del frontend | Frontend envía "Running" en vez de "running" |
| EC-17 | Executions | `date_from/date_to` con timezone diferente al servidor produce rango incorrecto | Usuario en timezone diferente |
| EC-18 | Data Store | `searchLikeEscaper` no escapa correctamente caracteres especiales → SQL injection en SQLite search | Búsqueda con `%`, `_` o `\` en el nombre |
| EC-19 | Data Store | `BuildStorePaginationConfig` struct con `OrderBy` inválido → whitelist rechaza campo legítimo | Frontend envía columna que no está en whitelist |
| EC-20 | Data Store | Bugfix nil pagination → regresión: paginación que antes funcionaba ahora aplica defaults diferentes | Data Store con ordenamiento custom pre-existente |
| EC-21 | StoreViewer | Reescritura de `NestedValueTree` pierde funcionalidad de expandir/colapsar nodos | Data Store con datos anidados profundos |
| EC-22 | StoreViewer | Bugfix `h-full` → el modal ahora tiene altura fija que corta datos en pantallas pequeñas | Modal de StoreViewer en resolución baja |
| EC-23 | Accounts | Filtro `timezone` no encuentra cuentas con timezone null o vacío | Accounts sin timezone configurado |
| EC-24 | Keys | `applyProviderFilter()` nil-safe pero no valida provider name → filtra con valor incorrecto | Frontend envía provider inexistente |
| EC-25 | Navigation | Reorganización de `menu.ts` rompe rutas o permisos → sección inaccesible | Usuario con permisos parciales |
| EC-26 | Breadcrumbs | `useCrumbs` con `breadcrumbLabel` undefined en una ruta → breadcrumb muestra "undefined" | Ruta sin route-meta configurada |
| EC-27 | i18n | +237 keys en / +228 keys es → hay keys sin traducción al español | Usuario con locale 'es' navega pantallas migradas |
| EC-28 | AbstractNotificationService | Cambio de export default → export nombrado rompe importaciones existentes | Cualquier archivo que importaba con `import default` |

---

## Paso 4: Preguntas para el Developer

```
PREGUNTAS PARA EL DEVELOPER — Ticket 86e223kvf

[FUNDACIÓN / ARQUITECTURA]

1. ¿Se validó que las 10 inyecciones de servicios de TenantLayout funcionan 
   idénticamente a CompanyLayout? ¿Hay algún servicio que se inicialice 
   diferente o en diferente orden?

2. ¿Se hizo testing de las pantallas Admin (PrimeVue legacy) después de 
   cargar el nuevo CSS? ¿Se verificó que no hay colisiones de clases 
   entre Tailwind y PrimeVue en esas pantallas?

3. ¿El DataTable nuevo de shadcn mantiene exactamente el mismo contrato de 
   paginación SSR que el DataTable de PrimeVue? ¿Los parámetros de query 
   (page, per_page, sort_by, sort_direction) son idénticos?

[FEATURES NUEVOS]

4. ¿La búsqueda global (Cmd/Ctrl+K) tiene límite de resultados por categoría?
   ¿Qué pasa si hay 100+ flows que matchean la búsqueda?

5. ¿El toggle dark/light mode persiste entre sesiones? ¿Dónde se almacena 
   la preferencia (localStorage, cookie, API)?

6. ¿El toast adapter vue-sonner fue probado con TODOS los tipos de toast que 
   el sistema usa actualmente? ¿Se preservaron success, error, warning, info?

7. ¿Los breadcrumbs se generan correctamente para TODAS las rutas del tenant?
   ¿Se verificó que `breadcrumbLabel` y `breadcrumbTrail` están configurados 
   en todas las rutas?

[BACKEND / DATA]

8. ¿El escape de caracteres especiales en Data Store search (`searchLikeEscaper`)
   fue probado con: backslash (\), porcentaje (%), underscore (_), 
   y combinaciones de estos?

9. ¿El cambio de `BuildStorePaginationConfig` de parámetros posicionales a struct 
   se aplicó en TODOS los call sites? ¿Hay algún call site que aún use el formato 
   anterior?

10. ¿Los filtros de Executions (status, date_from, date_to) fueron probados 
    con valores edge: status vacío, fechas invertidas (from > to), 
    status que no existe en el enum?

[REGRESIÓN / SCOPE]

11. ¿CreateConnectionV2Dialog fue marcada en el spec como "escalar, no tocar" — 
    ¿qué motivó la decisión de migrarla? ¿Se probó el flujo completo de 
    OAuth (authorize → callback → token → crear conexión)?

12. ¿SupportView.vue tiene funcionalidad real o es un placeholder? 
    ¿Se conecta a algún servicio de soporte externo?

13. ¿El polyfill de `scrollIntoView` para jsdom afecta el comportamiento 
    en navegadores reales? ¿Es solo para el ambiente de tests?

[i18n / EXPORTACIONES]

14. ¿Las +237 keys en y +228 keys es tienen paridad completa? ¿Hay keys 
    que existen en inglés pero no en español o viceversa?

15. ¿El cambio de AbstractNotificationService de export default a export 
    nombrado se aplicó en todos los archivos que lo importan?
```

---

## Paso 5: Tabla de Riesgos Priorizada

| ID | Área | Riesgo | Descripción | Prioridad | Justificación |
|----|------|--------|-------------|-----------|---------------|
| R-01 | TenantLayout (Shell) | 🔴 Crítico | Nuevo shell reemplaza CompanyLayout con 10 inyecciones de servicios. Fallo = app tenant inoperativa | 1 — Testear PRIMERO | Sin layout funcional, nada más funciona |
| R-02 | CSS Isolation (.modern-ui) | 🔴 Crítico | Scoping CSS entre Tailwind 4 y PrimeVue. Regresión en Admin = pantallas legacy rotas | 2 | Admin no fue objetivo del ticket pero puede tener regresión catastrófica |
| R-03 | DataTable (shadcn) | 🔴 Crítico | Reemplazo de componente DataTable en 14 pantallas. Paginación SSR, sort, filtros | 3 | Afecta la funcionalidad base de TODAS las pantallas migradas |
| R-04 | Toast System | 🟠 Alto | Adapter vue-sonner con ~168 call sites. Deduplicación. | 4 | Regresión silenciosa: los toasts podrían no aparecer o apilar |
| R-05 | Navigation/Menu | 🟠 Alto | Reorganización de menu.ts + useCrumbs + permisos | 5 | Secciones inaccesibles o visibles sin permiso |
| R-06 | CreateConnectionV2Dialog | 🟠 Alto | Migrada fuera de scope + bugfix activeTab. Flujo OAuth completo en riesgo. | 6 | Impacta la capacidad de crear conexiones → flows sin auth |
| R-07 | Executions (backend) | 🟠 Alto | Nuevos filtros status + date_from/date_to en ExecutionController | 7 | Cambio de API no contemplado en AC originales |
| R-08 | Data Store (backend) | 🟠 Alto | Search/filter/sort + bugfix nil pagination + escape chars SQLite | 8 | Cambio de API + riesgo de regresión en paginación existente |
| R-09 | Global Search | 🟠 Alto | Command palette Cmd/Ctrl+K con fetch paralelo y AbortController | 9 | Feature completamente nuevo, sin precedente en la app |
| R-10 | Accounts (backend) | 🟡 Medio | Filtro timezone + remote_id sortable | 10 | Cambio menor pero de API |
| R-11 | Keys (backend) | 🟡 Medio | applyProviderFilter() compartido entre listados | 11 | Riesgo de filtrado incorrecto |
| R-12 | Dark/Light Mode | 🟡 Medio | Toggle con View Transitions API + fallback | 12 | Feature nuevo, posible incompatibilidad de browser |
| R-13 | i18n Paridad | 🟡 Medio | +237 en / +228 es → posible paridad incompleta | 13 | Textos sin traducir en locale español |
| R-14 | Flow Description | 🟡 Medio | FlowParams.Description + Select() fix en gorm | 14 | Fix real pero de scope limitado |
| R-15 | SupportView (nuevo) | 🟢 Bajo | Vista nueva fuera de scope | 15 | No impacta funcionalidad existente |

---

## Recomendación

### Estrategia de Testing Propuesta

Este ticket tiene **complejidad equivalente a una mini-release**. Recomiendo dividir el testing en 3 waves:

**Wave 1 — Fundación (BLOQUEANTE)**
> Si algo falla aquí, las demás waves son inválidas.
- R-01: TenantLayout → ¿La app carga? ¿Servicios inyectados? ¿setUser sync?
- R-02: CSS Isolation → ¿Admin/Legacy intacto? ¿No hay bleeding de estilos?
- R-03: DataTable → ¿Paginación SSR? ¿Sort? ¿Column visibility?
- R-04: Toast → ¿Los toasts aparecen? ¿Deduplicación funciona?
- R-05: Navigation → ¿Menú visible? ¿Permisos? ¿Breadcrumbs?

**Wave 2 — Features nuevos + Backend**
- R-06: CreateConnectionV2Dialog → Flujo OAuth completo
- R-07: Executions filtros → status, dates
- R-08: Data Store search/filter → escape chars, pagination
- R-09: Global Search → Cmd/K, resultados, recientes
- R-10-R-11: Accounts/Keys filtros

**Wave 3 — Pantallas individuales + Polish**
- Cada una de las 14 pantallas migradas → verificar que DataTable + acciones + modales funcionan
- R-12: Dark mode
- R-13: i18n
- R-14: Flow description
- R-15: SupportView

### Áreas que requieren más atención

1. **TenantLayout**: Es single point of failure. Si falla, nada funciona.
2. **CSS Isolation**: Regresión invisible — puede pasar desapercibida hasta que alguien use Admin.
3. **DataTable en 14 pantallas**: Multiplicador de riesgo — un bug en el componente base afecta a todas.
4. **Backend changes**: Contradicen el AC "no backend". Requieren testing de API explícito.
5. **CreateConnectionV2Dialog**: Fuera de scope declarado pero impacta un flujo crítico (OAuth).
