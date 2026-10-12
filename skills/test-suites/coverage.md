# Skill: test-suites/coverage

> Analiza la **cobertura de automatización** del E2E maestro y del smoke, y actualiza la **hoja de ruta de automatización** (olas y tickets de QA Kanban). Herramienta del LQA para priorizar la automatización (`Q-40`, `Q-50`).

## Cuándo usar

- En la retro, al planificar el trabajo de automatización o cuando cambia el estado de tickets de QA Kanban.
- Frase disparadora: `Analizar cobertura de automatización`.

## Pre-requisitos (gates)

| Check | Si falla |
|---|---|
| `e2e-master.csv` actualizado | Ejecutar `test-suites/import-e2e` |
| MCP de ClickUp responde (lista QA Kanban `901705382240`) | Continuar sin estados de ClickUp y avisar |

## Contexto a cargar

`knowledge/test-suites/coverage.md`, `automation-roadmap.md`, `smoke-master.md`, `knowledge/L3-tickets/drafts/automation/` (drafts de tickets), `skills/_shared/bot-test.md`.

## Stage 1 — Planning

Anunciar las fuentes y el período de comparación (cobertura anterior en git). Esperar confirmación.

## Stage 2 — Execution

1. `python -I scripts/e2e_master.py coverage` y comparar con la versión anterior (`git diff knowledge/test-suites/coverage.md`).
2. **Estado de los tickets de automatización:** `searchTasks` en la lista `901705382240` (estados `Open`, `in progress`, `blocked`, `need escalation`). Cruzar cada ticket con su prefijo E2E (tabla de `automation-roadmap.md`).
3. **Inconsistencias:** ticket `Open` cuyas suites ya existen (en PR o integradas); ticket `in progress` sin spec; filas automatizadas sin ticket; tickets que se solapan; drafts sin ticket.
4. **Priorización por olas:**
   - Ola 0: requisitos de bot-test pendientes (AV-11).
   - Ola 1: verificaciones del smoke sin automatizar.
   - Ola 2: filas `BASELINE = sí` sin automatizar.
   - Ola 3: TC estables de sanity que se repitieron en ≥ 2 releases y el resto por prioridad de la hoja.
   Dentro de cada ola, ordenar por frecuencia de uso en releases (filas que aparecen en la capa 1) y por criticidad del módulo (`test-priorities.md`).
5. **Drafts:** marcar los reemplazados o desactualizados y proponer drafts nuevos para las brechas (sin crear tickets en ClickUp).

## Stage 3 — Reporting

- `coverage.md` regenerado.
- `automation-roadmap.md` actualizado (situación, olas, tabla de tickets y acciones).
- Lista de acciones para el LQA: tickets a crear, mover o cerrar en QA Kanban; requisitos a entregar al responsable de bot-test.
- Indicadores para `metrics/weekly`: % automatizado, % ejecutable, % del smoke y del baseline automatizados, tests en cuarentena.

## Reglas

- El catalyst prioriza y propone; el LQA decide y mueve los tickets en ClickUp.
- No se proponen cambios de código en bot-test fuera de un paquete de automatización (`automation/code`).
