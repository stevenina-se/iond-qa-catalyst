# Test Plan — IONF-1121 (86e22fzrp)

> **Bug Fix**: Board sugiere cambios sin guardar tras commit exitoso al re-ingresar a la vista
> Módulo: **Boards** (🔴 Crítico)
> Tipo: Bug Fix | Prioridad: Normal | Subcategory: Boards
> Tags: `qa-regression-v0.1.0`, `iond-uxui-issue`
> Repo: `gateway-ion` | PR: https://github.com/altacrest/ion_gateway_ion/pull/9
> Branch: `IONF-1121`
> Assignee: Gustavo Mamani
> Desplegado: Sí (confirmado por Rodolfo Merlo Ali el 2026-07-09)

---

## Contexto del Bug

Al crear un nuevo Board, realizar un commit exitoso, salir de la vista de boards y volver a ingresar, el Board muestra una **alerta incorrecta** indicando que existen cambios sin guardar. El commit fue exitoso y no se realizaron cambios adicionales. La alerta es **temporal** — desaparece después de cierto tiempo.

**Impacto**: Genera confusión en el usuario. No bloqueante pero puede causar commits innecesarios.

## Cambios del Developer

- Se corrigió el problema de la alerta de cambios cuando se guardan los cambios (commit)
- 1 archivo de tests modificado, todos los tests pasan (`pnpm test:unit`)
- Code review approved por Alex Chura y Enrique Vicente

---

## Criterios de Aceptación

| # | AC | Tipo |
|---|-----|------|
| AC-1 | Después de un commit exitoso, al re-ingresar a la vista del Board NO debe mostrarse alerta de cambios sin guardar | Corrección del bug |
| AC-2 | La funcionalidad de detección de cambios sin guardar reales debe seguir funcionando (si hay cambios reales pendientes, la alerta SÍ debe aparecer) | Regresión |
| AC-3 | El commit de cambios en un Board debe seguir funcionando correctamente | Regresión |

---

## Estrategia de Testing

| Categoría | Enfoque |
|-----------|---------|
| Smoke | Verificar que el fix corrige el bug principal (AC-1) |
| Happy Path | Confirmar que cambios reales sí muestran la alerta (AC-2) |
| Regresión | Crear board, editar, commit, verificar flow normal (AC-3) |
| Edge cases | Múltiples commits, navegación rápida, refresh de página |

**Modo**: Asistido con Playwright MCP (Canal 1) — QA supervisa
**Entorno**: `dev-app.ionflow.io`
**Rol**: Company User (`UPDATE_BOARD`)
