# QA FOUND ISSUE ESCALATION REPORT — IOND

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | Templates / Library |
| Path | Sidebar > AUTOMATE > Templates |
| Versión | gateway-ion (actual) |

## Description of the validated/replicated problem

En el menú lateral (sidebar), bajo la sección AUTOMATE, la opción aparece como **"Templates"** cuando debería decir **"Library"**. El breadcrumb muestra `Dashboard > Templates` cuando debería mostrar `Automations > Library`. Dentro de la vista, el tab system muestra **"Templates"** y "Community" — el primer tab debería llamarse **"Official"**. Adicionalmente, los filtros (pills/chips debajo del buscador) actualmente filtran por **categorías de templates** (pro-categories), cuando deberían filtrar por **tipo de recurso**: All, PDF, y Flows.

## Steps to Reproduce

1. Login > Sidebar: observar bajo la sección **AUTOMATE**
2. Observar que la opción dice **"Templates"** → ❌ debería decir **"Library"**
3. Click en "Templates" para acceder a la vista
4. Observar el breadcrumb: muestra `Dashboard > Templates` → ❌ debería mostrar `Automations > Library`
5. Observar los tabs: el primer tab dice **"Templates"** → ❌ debería decir **"Official"**
6. Observar los filtros (pills) debajo del buscador: filtran por categorías de templates
7. → ❌ deberían filtrar por tipo de recurso: **All** | **PDF** | **Flows**

## Datos utilizados

- Rol: Cualquier usuario autenticado con acceso al sidebar
- Entorno: Staging
- Versión: actual
- No requiere datos específicos — reproducible con cualquier cuenta

## Current Behavior

- Sidebar muestra **"Templates"** bajo AUTOMATE.
- Breadcrumb muestra `Dashboard > Templates`.
- El primer tab del tab system muestra **"Templates"**.
- Los filtros (chips) debajo del buscador filtran por **categorías de templates** (pro-categories), sin opción de filtrar por tipo de recurso.

## Expected Behavior

- Sidebar debe mostrar **"Library"** bajo AUTOMATE.
- Breadcrumb debe mostrar `Automations > Library`.
- El primer tab debe mostrar **"Official"** (el tab "Community" permanece sin cambios).
- Los filtros deben ser reemplazados por tipo de recurso:
  - **All** — Muestra todos los recursos (seleccionado por defecto)
  - **PDF** — Filtra solo PDF Templates
  - **Flows** — Filtra solo Flows/Boards templates
- La búsqueda por texto debe funcionar en combinación con los filtros de tipo.

## Impacto

- Afecta a todos los usuarios que acceden a la sección de templates/library desde el sidebar
- No bloqueante — la funcionalidad existe pero con nomenclatura incorrecta y filtros limitados
- Los filtros por categoría no permiten distinguir entre PDFs y Flows, dificultando la búsqueda del recurso correcto

## Categorización

- 📊 Prioridad: **normal** — no bloquea funcionalidad pero impacta usabilidad y nomenclatura
- 🏷️ Tipo: **bug** — nomenclatura incorrecta y filtros no alineados con la estructura de recursos actual
