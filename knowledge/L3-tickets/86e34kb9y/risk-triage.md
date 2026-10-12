# Risk Triage — 86e34kb9y

> Ticket: [IOND] Mejorar búsqueda y jerarquía de resultados en Admin Companies
> Fecha: 2026-10-05
> Módulo principal: Auth (Admin Companies)
> Track: Discovery

---

## Resumen

- **Módulo principal**: Auth — Admin > Companies (`/admin/companies`)
- **Módulos impactados**: Auth (Admin + Tenant topbar), Dashboard (sidebar icons)
- **Riesgo general**: 🟠 Alto
- **Total edge cases identificados**: 18
- **Total preguntas para Developer**: 10
- **Contexto de ClickUp**: 2 comentarios leídos, 11 divergencias encontradas (3 altas, 4 medias, 4 técnicas)
- **Repos afectados**: `gateway` (PHP — motor de búsqueda), `gateway-ion` (Vue — UI completa)

---

## Análisis de Lógica de Negocio

| Pregunta | Análisis |
|----------|----------|
| ¿El feature respeta las reglas multi-tenant (company)? | ✅ **Sí** — La búsqueda opera exclusivamente en el contexto Admin. Los permisos excluyen companies sin autorización antes de ordenar. Sin embargo, la exposición de emails de company users es un área sensible que requiere verificación. |
| ¿Afecta la ejecución de flows/nodos? | ✅ **No** — Es una mejora de búsqueda en Admin Companies. No toca el motor de ejecución de flows. |
| ¿Hay impacto en connectors globales vs company? | ✅ **No** — No hay cambios en connectors. |
| ¿Se tocan datos de ejecución (SQLite) o datos persistentes (PostgreSQL)? | ⚠️ **PostgreSQL sí** — Se agregaron 3 migraciones: extensión `pg_trgm` + índices de expresión (global y por tenant). No se toca SQLite. |
| ¿Hay impacto en el sistema de permisos por usuario/company? | ⚠️ **Indirecto** — El buscador de tenant ahora depende de `useTenantsMenu()` que consulta el auth store para filtrar por permisos. El de admin usa `useAdminMenu()` que no filtra. Los resultados de búsqueda respetan permisos (companies sin permiso no aparecen). |
| ¿El feature puede romper flujos de e-commerce existentes? | ✅ **No** — No afecta flows, nodos, ni ejecuciones. Solo la vista administrativa de companies y el buscador global. |

---

## Análisis de Impacto por Módulo

| Área | Impacto | Riesgo |
|------|---------|--------|
| **Frontend — Admin Global Search** | Componente reescrito: `AdminGlobalSearch.vue` + shell reutilizable `GlobalSearchShell.vue`. Buscador anterior `SearchAdminDialog.vue` eliminado. Navegación por teclado implementada. | 🔴 Crítico |
| **Frontend — Tenant Global Search** | `GlobalSearch.vue` reescrito sobre el mismo shell (5 secciones). Dependencia nueva en Pinia (auth store). | 🟠 Alto |
| **Frontend — CompanyTable** | Migrada de PrimeVue a `@/components/ui/DataTable` (TanStack). `useListQuerySync` para persistencia de búsqueda en URL. `CompanyDetailsCell.vue` nuevo con avatar, badge, pista de match. | 🟠 Alto |
| **API — Motor de búsqueda** | 4 archivos nuevos/modificados en `gateway`: `SearchTerm.php`, `CompanySearch.php`, `RelevanceSearch.php`, `FullTextSearchTrait.php`. Escalera de relevancia con 5 tiers. Respuesta aditiva: `search_match_field` + `search_match_value`. | 🔴 Crítico |
| **BD PostgreSQL** | 3 migraciones: extensión `pg_trgm`, índices de expresión global y por tenant. El `to_tsvector` existente NO fue tocado (preserva `flows_fts_idx`). | 🟠 Alto |
| **BD SQLite** | Sin cambios. | 🟢 Sin impacto |
| **Canvas (Vue Flow)** | Sin cambios. | 🟢 Sin impacto |
| **CSS / Theming** | `.modern-ui` acotado a subárbol (tabla + disparadores del buscador). No se aplica a `AdminLayout`. Precedente: `DialogContent.vue:47`. | 🟡 Medio |
| **Iconografía** | `navIconsByHref(sections)` en `nav.config.ts`. Normalización de `pi-fw`. 3 iconos faltantes (`pi pi-building`, `pi pi-users`, `pi pi-cog`) añadidos. | 🟡 Medio |

---

## Tabla de Riesgos

| ID | Área | Riesgo | Descripción | Prioridad de testing | Justificación |
|----|------|--------|-------------|---------------------|---------------|
| R-001 | Escalera de relevancia (Backend) | 🔴 Crítico | El ranking de resultados es el corazón del ticket. 5 tiers para queries con formato email, 5 tiers para queries normales. Orden total con `ORDER BY search_tier, name, id`. | 1 — Testear primero | Si el ranking falla, la funcionalidad principal del ticket no funciona. Afecta directamente todos los AC Gherkin. |
| R-002 | Permisos y privacidad | 🔴 Crítico | Companies sin permiso no deben aparecer. Emails restringidos no deben exponerse. Solo admins autorizados ven emails. | 2 | Fuga de privacidad es un riesgo de seguridad. AC-4 Gherkin lo cubre explícitamente. |
| R-003 | Admin Global Search (UI) | 🔴 Crítico | Buscador completamente reescrito. Componente anterior eliminado. `⌘K`, debounce, recientes, estado vacío, navegación por teclado. | 3 | Cambio destructivo — no hay fallback al componente anterior. Si falla, admin pierde búsqueda. |
| R-004 | Paginación estable | 🟠 Alto | Búsqueda sobre colección completa antes de paginar. Deduplicación. Paginación estable (sin companies repetidas ni ausentes entre páginas). | 4 | AC-5 (Catálogo completo) + AC-3 (Deduplicación). El `id` final en el ORDER BY garantiza estabilidad — verificar. |
| R-005 | CompanyTable migrada | 🟠 Alto | PrimeVue → TanStack/shadcn. `useListQuerySync` para persistencia URL. Búsqueda sobrevive a F5 y navegación browser. | 5 | Cambio de framework de la tabla. Toda funcionalidad previa debe preservarse. 17 listas ya usan `useListQuerySync` — patrón probado pero nuevo para CompanyTable. |
| R-006 | Tenant Global Search (regresión) | 🟠 Alto | Reescrito sobre el mismo shell. 5 secciones. Depende de Pinia (auth store) para iconos de menú por permisos. | 6 | El ticket es de Admin Companies pero el Developer también reescribió el buscador de tenant. Regresión cruzada. |
| R-007 | Normalización de búsqueda | 🟠 Alto | Case-insensitive. Conservar caracteres significativos (+, puntos, guiones). Email completo, fragmento y dominio. | 7 | R-4 y R-5 de los requisitos. El motor viejo borraba `@ . + -` — el nuevo usa `pg_trgm` que debería preservarlos. |
| R-008 | Aislamiento CSS `.modern-ui` | 🟡 Medio | Acotado a subárbol, no a AdminLayout. Verificar que vistas admin PrimeVue existentes no se rompen. | 8 | Patrón ya probado en ticket 86e223kvf. Riesgo menor pero presente si el subárbol se aplica incorrectamente. |
| R-009 | Navegación por teclado | 🟡 Medio | Flechas mueven resaltado, Enter abre, Esc cierra. Home/End van a primer/último resultado (no mueven caret). | 9 | Trade-off aceptado por el Developer. Documentar como comportamiento conocido. |
| R-010 | Iconografía sidebar ↔ buscador | 🟡 Medio | `navIconsByHref(sections)` aplana menú a href→icono. Normalización de `pi-fw`. 3 iconos faltantes añadidos. | 10 | Riesgo visual — si la normalización falla, iconos caen a fallback `Circle`. No rompe funcionalidad. |
| R-011 | `contactable_type` morph map | 🟡 Medio | `CompanySearch` resuelve tipo con `(new Company())->getMorphClass()`. Morph map declara `'company' => Company::class`. | 11 | Si el morph map cambia, la búsqueda por email deja de funcionar. Verificar que los datos de staging usan `contactable_type = 'company'`. |

---

## Edge Cases Identificados

### Búsqueda por Email

| # | Edge Case | Riesgo | Relacionado con |
|---|-----------|--------|-----------------|
| EC-1 | Buscar email con caracteres especiales: `user+tag@domain.com` | 🟠 | R-5 (sin normalización destructiva) |
| EC-2 | Buscar solo el dominio: `@billing.com` | 🟠 | AC-2, R-4 |
| EC-3 | Buscar fragmento sin `@`: `billing` — ¿prioriza nombre o email? | 🟠 | Ranking tier 3-5 |
| EC-4 | Buscar email que coincide con company contact Y con company user → deduplicación + ¿qué match se muestra? | 🟠 | D-2, R-6, R-7 |
| EC-5 | Company con múltiples users que tienen el mismo dominio de email | 🟡 | R-6 (deduplicación) |
| EC-6 | Company sin Company User principal (solo usuarios secundarios) | 🟠 | R-2, R-9 (compatibilidad) |
| EC-7 | Company sin ningún Company User (company vacía) | 🟡 | R-9 (sigue siendo buscable por nombre/ID) |
| EC-8 | Email con mayúsculas mixtas: `Owner@BILLING.Com` | 🟡 | R-4 (normalización) |

### Paginación y Rendimiento

| # | Edge Case | Riesgo | Relacionado con |
|---|-----------|--------|-----------------|
| EC-9 | Buscar un email que coincide con companies en diferentes páginas | 🟠 | AC-5 (catálogo completo) |
| EC-10 | Cambiar `per_page` durante una búsqueda activa | 🟡 | R-004 (paginación estable) |
| EC-11 | Muchas companies (100+) coinciden con un dominio genérico (`gmail.com`) | 🟡 | R-10 (rendimiento) |

### Regresión del Buscador

| # | Edge Case | Riesgo | Relacionado con |
|---|-----------|--------|-----------------|
| EC-12 | Abrir buscador con `⌘K`, escribir query, presionar Esc → ¿se limpia la búsqueda? | 🟡 | R-003 |
| EC-13 | Búsquedas recientes (localStorage) — ¿persisten entre sesiones? | 🟡 | D-4 |
| EC-14 | "Ver las N companies" → navegar al listado → volver atrás → ¿buscador global se reabre? | 🟡 | D-6 |
| EC-15 | Buscar en admin → cambiar a tenant → buscar lo mismo → ¿resultados son diferentes? | 🟡 | D-4, R-006 |

### Aislamiento y CSS

| # | Edge Case | Riesgo | Relacionado con |
|---|-----------|--------|-----------------|
| EC-16 | Abrir una vista admin PrimeVue (ej. otra sección) después de usar la nueva CompanyTable | 🟡 | D-8 |
| EC-17 | Diálogo del buscador global (teleported a `<body>`) — ¿hereda `.modern-ui` correctamente? | 🟡 | D-8, precedente `DialogContent.vue:47` |

### Datos y BD

| # | Edge Case | Riesgo | Relacionado con |
|---|-----------|--------|-----------------|
| EC-18 | Company histórica con `contactable_type` diferente a `'company'` (datos legacy) | 🟡 | D-11, R-011 |

---

## Preguntas para el Developer

```
PREGUNTAS PARA EL DEVELOPER — Ticket 86e34kb9y

[LÓGICA DE NEGOCIO]
1. ¿Cómo se define canónicamente el "Company User principal"? ¿Es el owner, 
   administrador principal, campo primary, o la relación equivalente? 
   (Requisito R-2 del ticket lo pide explícitamente en Discovery)

2. Cuando una búsqueda por email coincide tanto con el email de contacto de la 
   company como con un Company User, ¿cuál se prioriza en el `search_match_field`? 
   ¿El usuario ve "email de contacto" o "Company User"?

3. El requerimiento 1 fue trasladado al ticket 86e1ryauq por Marcel. ¿Puedes 
   confirmar que no hay dependencia funcional entre ambos tickets que afecte 
   el testing de este?

[EDGE CASES]
4. ¿Qué sucede si una company no tiene ningún Company User asociado? ¿Sigue 
   apareciendo en búsquedas por nombre/ID pero no por email?

5. Con `per_page=3` y un dominio genérico que coincide con 50+ companies, 
   ¿la paginación es estable al avanzar/retroceder páginas? 
   (El R&D report menciona verificación con `per_page=3`)

6. ¿Hay un límite de Company Users por company que afecte el rendimiento 
   de la búsqueda? ¿Qué pasa con companies con 100+ users?

[INTEGRACIÓN / REGRESIÓN]
7. El buscador de tenant fue reescrito sobre el mismo shell. ¿Verificaste que 
   las 5 secciones del tenant (flows, apps, appActions, etc.) siguen funcionando 
   correctamente después del cambio?

8. La dependencia de Pinia (`useTenantsMenu()`) en el buscador de tenant: 
   ¿hay algún escenario donde el auth store no esté disponible (ej. durante 
   hidratación, SSR, o race condition en el login)?

9. Los 3 iconos faltantes en `ICON_MAP` (`pi pi-building`, `pi pi-users`, 
   `pi pi-cog`) — ¿se mapearon a los iconos lucide correctos?

[RENDIMIENTO]
10. Las 3 migraciones de `pg_trgm` + índices de expresión — ¿se verificó el 
    plan de ejecución (EXPLAIN) con un dataset representativo? ¿Cuál es el 
    tamaño esperado de la tabla `companies` en producción?
```

---

## Contexto del Ticket (ClickUp)

### Divergencias detectadas entre descripción y comentarios:
- **D-1**: Requerimiento 1 trasladado a `86e1ryauq` (Marcel, 23-Sep)
- **D-2**: Búsqueda expandida a email de contacto de company (no solo Company Users)
- **D-4 a D-7**: Features adicionales implementados (buscador tenant reescrito, CompanyTable migrada, "Ver N companies", CompanyDetailsCell)
- **D-8 a D-11**: Decisiones técnicas de implementación (CSS, Pinia, teclado, iconos)

### Últimas decisiones relevantes:
1. **Motor de búsqueda**: Escalera de relevancia con `pg_trgm` — camino separado del `to_tsvector` existente para no invalidar `flows_fts_idx`
2. **Navegación por teclado**: Opción A elegida (`ListboxFilter` con `clientFilter=false`). Trade-off: Home/End van a primer/último resultado
3. **Aislamiento CSS**: `.modern-ui` en subárbol, NO en AdminLayout
4. **Iconografía**: `navIconsByHref(sections)` — fuente única de verdad desde `nav.config.ts`

---

## Recomendación

### Áreas que requieren más atención:

1. **🔴 Escalera de relevancia (R-001)**: Es el corazón del ticket. Verificar los 5 tiers con queries de email y queries normales. Usar los ejemplos del ranking del ticket como casos base.

2. **🔴 Permisos y privacidad (R-002)**: Companies sin permiso no deben aparecer ni exponer emails. Testear con usuario admin vs usuario sin permisos.

3. **🔴 Admin Global Search (R-003)**: Componente anterior eliminado — no hay fallback. Verificar `⌘K`, debounce, recientes, estado vacío, navegación por teclado completa.

4. **🟠 Regresión del buscador de tenant (R-006)**: Fue reescrito como efecto colateral del ticket de Admin. Requiere verificación de las 5 secciones.

5. **🟠 CompanyTable migrada (R-005)**: Verificar que toda la funcionalidad de PrimeVue DataTable se preservó en el nuevo componente TanStack.

### Nivel de complejidad del testing:
> Este ticket tiene **complejidad media-alta**. La búsqueda por email es straightforward pero la reescritura del buscador global (admin + tenant) y la migración de CompanyTable amplían significativamente el surface area de testing.
