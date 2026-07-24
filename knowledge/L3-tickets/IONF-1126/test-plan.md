# Test Plan — IONF-1126 (86e22fzut)

> **Bug Fix**: PDF Templates — Cambios sin guardar se pierden al presionar Escape o cerrar modal sin confirmación
> Módulo: PDF Templates (Iond Subcategory)
> Tipo: Bug | Prioridad: High | Tags: qa-regression-v0.1.0, iond-uxui-issue

---

## Contexto

Al editar un template PDF, si el usuario presiona Escape, cierra el modal o presiona "New Template" sin guardar, todos los cambios se pierden sin confirmación. El fix agrega un diálogo de confirmación con opciones "Continuar editando" y "Descartar cambios", y previene que la tecla Escape cierre el Drawer cuando hay un diálogo activo.

## Acceptance Criteria (del ticket)

1. Al intentar cerrar el modal con cambios sin guardar (×, Cancel, Escape) → mostrar diálogo de confirmación
2. Al presionar "New Template" con cambios pendientes → mostrar diálogo de confirmación
3. Sin cambios, cerrar → cierre inmediato sin confirmación
4. Drawer con diálogo PrimeVue activo + Escape → Drawer NO se cierra
5. Drawer sin diálogo activo + Escape → Drawer se cierra normalmente

## Criterios de Aprobación

| Criterio | Umbral |
|----------|--------|
| Smoke tests | 100% |
| Happy path | 100% |
| Edge cases | ≥80% |
| Regresión | 100% |

## Criterios de Rechazo

- Cualquier TC de tipo Smoke o Happy Path falla → ❌ REJECTED
- Cambios se pierden sin confirmación → ❌ REJECTED
- Escape cierra el Drawer con diálogo activo → ❌ REJECTED
