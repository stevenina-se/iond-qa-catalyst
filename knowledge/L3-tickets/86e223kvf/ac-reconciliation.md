# Reconciliación de AC — 86e223kvf

> Ticket: Mejoras estéticas globales en pantallas de iond / Ionflow
> Fecha de reconciliación: 2026-07-20
> Fuentes: Descripción del ticket + 2 comentarios del developer (10-Jul, 20-Jul)

---

## Tabla de Reconciliación

### 🔴 DIVERGENCIAS CRÍTICAS (Alcance expandido significativamente)

| # | AC Original (Descripción) | Decisión en Comentarios | AC Reconciliado | Fuente |
|---|--------------------------|------------------------|-----------------|--------|
| D-1 | **"No realizar cambios en backend, servicios, APIs, base de datos"** | Developer implementó: (1) Filtros `status` y `date_from/date_to` en `ExecutionController@index` (gateway/Laravel), (2) Search/filter/sort en Data Store & Data Structure (flow_binaries/Go), (3) Filtro `timezone` en accounts, (4) `applyProviderFilter()` en keys, (5) Fix de `description` en `FlowParams` | **AC EXPANDIDO**: Se realizaron cambios puntuales de backend para soportar búsqueda, filtrado y ordenamiento en las nuevas tablas. Estos cambios son funcionales (no solo estéticos) y requieren testing de API. | Comentario 20-Jul §2 (Backend API) y §3 (Microservices) |
| D-2 | **"Mejoras estéticas y de experiencia de usuario"** (scope cosmético) | Developer ejecutó una **migración arquitectónica completa**: PrimeVue → Tailwind 4 + shadcn-vue, ~90 primitivos nuevos, nuevo sistema de tokens, nuevo layout shell | **AC REDEFINIDO**: El ticket dejó de ser "mejoras estéticas" para convertirse en una **migración de framework UI** completa. El scope de testing cambia radicalmente. | Comentario 10-Jul (UX Research) + Comentario 20-Jul §1 (Frontend) |
| D-3 | **"Normalizar tablas y listados principales"** (ajustes visuales) | Developer reemplazó completamente PrimeVue `DataTable` por una tabla headless de shadcn (TanStack Table + reka-ui) con composables avanzados (`useColumnVisibility`, hide columns, resize, sort) | **AC EXPANDIDO**: No es normalización visual sino **reemplazo total del componente DataTable**. Requiere verificar que TODA la funcionalidad previa se preservó (paginación SSR, sort, filtros). | Comentario 20-Jul §1 - DataTable Avanzado |

### 🟠 DIVERGENCIAS ALTAS (Features nuevos no contemplados en AC)

| # | AC Original | Decisión en Comentarios | AC Reconciliado | Fuente |
|---|------------|------------------------|-----------------|--------|
| D-4 | (no existe) | Developer creó un **nuevo shell completo**: `TenantLayout.vue` reemplaza `CompanyLayout.vue`, incluye `TenantSidebar`, `TenantTopbar`, `GlobalSearch`, `NotificationsMenu`, `UserMenu`, `HelpMenu`, `ProductsMenu`, modales de Ayuda/Atajos/Novedades, composable `useCrumbs` | **AC NUEVO**: El nuevo layout TenantLayout debe preservar las 10 inyecciones de servicios existentes y el sync de `window.$useFlowCore.setUser`. La navegación, breadcrumbs y menús deben funcionar correctamente. | Comentario 20-Jul §1 - App Shell |
| D-5 | (no existe) | Developer implementó **toggle dark/light mode** con View Transitions API (expansión circular desde punto de click, fallback para `prefers-reduced-motion`) | **AC NUEVO**: El toggle de tema claro/oscuro debe funcionar correctamente, con transición visual suave y fallback accesible. | Comentario 20-Jul §1 - Toasts & tema |
| D-6 | (no existe) | Developer implementó **búsqueda global** (Cmd/Ctrl+K): command palette con debounce 600ms, fetch paralelo a flows/apps/appActions, AbortController, hasta 10 búsquedas recientes en localStorage | **AC NUEVO**: La búsqueda global debe funcionar con Cmd/Ctrl+K, mostrar resultados de flows/apps/appActions, y persistir búsquedas recientes. | Comentario 20-Jul §1 - Búsqueda global |
| D-7 | (no existe) | Developer reescribió `useToast()` como adapter sobre `vue-sonner` con deduplicación de notificaciones por `${tone}:${message}` | **AC NUEVO**: Las notificaciones toast deben funcionar sin apilar duplicados. Los ~168 call sites existentes no deben romperse. | Comentario 20-Jul §1 - Toasts |
| D-8 | **"Mantener funcionalidad existente"** | Developer migró `CreateConnectionV2Dialog.vue` (parte del editor de flujos, marcado en spec como "escalar, no tocar") y de paso arregló un bug: cuando solo la conexión secundaria resolvía, `activeTab` quedaba fijo en `'0'` sin tab/form | **AC EXPANDIDO**: Se migró un componente fuera del scope original. Se corrigió un bug real pero se introdujo riesgo de regresión en el editor de flujos. | Comentario 20-Jul §1 - Otros cambios |
| D-9 | (no existe) | Developer creó `SupportView.vue` — nueva vista que no estaba en el spec de migración | **AC NUEVO**: Vista de soporte creada fuera del alcance original. Verificar que existe y funciona. | Comentario 20-Jul §1 - Migración |

### 🟡 DIVERGENCIAS MEDIAS (Cambios técnicos relevantes)

| # | AC Original | Decisión en Comentarios | AC Reconciliado | Fuente |
|---|------------|------------------------|-----------------|--------|
| D-10 | **"No se deben haber modificado submenús internos, editores profundos"** | La estrategia CSS `.modern-ui` aísla los componentes nuevos de los legacy. PrimeVue **no se removió** — Admin sigue operando. Sin embargo, se migró `CreateConnectionV2Dialog` que es parte del editor. | **AC PARCIALMENTE RESPETADO**: La estrategia de aislamiento protege las pantallas Admin/legacy, pero se tocó un componente del editor (CreateConnectionV2Dialog). | Comentario 10-Jul (Aislamiento CSS) + 20-Jul |
| D-11 | **"14 áreas migradas"** pero AC dice "primeras vistas" | Las 14 áreas incluyen pantallas completas con DataTables, diálogos, specs. El `StoreViewer` fue reescrito completamente reemplazando `Paginator`/`DataTable`/`Tree` de PrimeVue. | **AC EXPANDIDO**: No son solo "primeras vistas" — son migraciones completas de cada área incluyendo componentes internos (diálogos, viewers, etc.) | Comentario 20-Jul §1 - Migración |
| D-12 | (no existe) | i18n: +237 keys en / +228 keys es. `AbstractNotificationService` cambió de export default a export nombrado. Polyfill de `scrollIntoView` agregado para tests. | **AC NUEVO TÉCNICO**: Cambios transversales que podrían afectar importaciones existentes y tests. | Comentario 20-Jul §1 - Otros |

### ✅ AC ORIGINALES PRESERVADOS (sin divergencia)

| # | AC Original | Estado |
|---|------------|--------|
| AC-P1 | Primeras vistas de módulos principales auditadas | ✅ Preservado (expandido a 14 áreas) |
| AC-P2 | Tablas alineadas a diseño de PDF Templates | ✅ Preservado (implementado via shadcn DataTable) |
| AC-P3 | Modales de confirmación normalizados | ✅ Preservado |
| AC-P4 | Primera vista de Boards mejorada sin tocar editor | ⚠️ Parcial — la vista fue migrada pero `CreateConnectionV2Dialog` (editor) fue tocado |
| AC-P5 | Responsive validado | ✅ Preservado como requisito |
| AC-P6 | Sin textos cortados, overlap, overflow | ✅ Preservado como requisito |

---

## Resumen Ejecutivo de Divergencias

```
📊 ANÁLISIS DE DIVERGENCIAS — 86e223kvf

  AC Originales: 6 escenarios Gherkin + 9 items QA Matrix + 12 DoD items
  
  Divergencias encontradas: 12
    🔴 Críticas: 3 (D-1, D-2, D-3) — Cambio fundamental de scope
    🟠 Altas: 6 (D-4 a D-9) — Features nuevos no contemplados
    🟡 Medias: 3 (D-10, D-11, D-12) — Cambios técnicos relevantes
    ✅ Preservados: 5/6 AC originales (1 parcial)

  ⚠️ CONCLUSIÓN: El ticket evolucionó de "mejoras estéticas" a 
     "migración arquitectónica de UI framework". Los AC originales 
     son INSUFICIENTES como base de testing. Se requiere construir 
     AC consolidados que reflejen el alcance real.
```

---

## Impacto en el Testing

### Lo que CAMBIA para QA:

1. **No es solo UI visual** — Hay cambios de backend que requieren testing de API (filtros, search, sort)
2. **Riesgo de regresión en Admin** — La estrategia `.modern-ui` DEBE verificarse exhaustivamente
3. **Nuevo DataTable** — Toda la funcionalidad previa (paginación SSR, sort) debe re-verificarse en cada pantalla
4. **Nuevo Layout** — El `TenantLayout` preserva 10 inyecciones de servicios — cualquier falla es catastrófica
5. **Features nuevos** — Dark mode, búsqueda global, toasts, breadcrumbs — cada uno requiere TCs propios
6. **3 repos afectados** — No solo gateway-ion: gateway (Laravel) y flow_binaries (Go) tienen cambios

### Recomendación del QA Catalyst:

> Los AC Gherkin originales del ticket son una **base mínima**, pero son **insuficientes** para cubrir el alcance real.
> Se necesita construir AC consolidados que incorporen las 12 divergencias identificadas.
> El testing de este ticket es equivalente en complejidad a una **mini-release**.
