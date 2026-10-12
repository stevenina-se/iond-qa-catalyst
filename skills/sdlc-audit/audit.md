# Skill: sdlc-audit/audit

> Auditoría de cumplimiento del SDLC para el **Scrum Master** (y el LQA): detecta en los tableros desvíos que ClickUp no impide de forma nativa (`L-01`) y arma la lista de ajustes. **Solo lectura**: el catalyst reporta; el SM corrige o pide la corrección.

## Cuándo usar

- **Diaria** (rápida, antes de la daily) y **semanal** (completa, viernes antes del plan del release).
- Frase disparadora: `Auditar SDLC` (diaria) o `Auditar SDLC semanal`.

## Pre-requisitos (gates)

| Check | Si falla |
|---|---|
| MCP de ClickUp responde | PARAR |

## Contexto a cargar

Fuente canónica §4–§8, §11, §12, §15 y §16; `skills/_shared/clickup.md`; el último reporte en `knowledge/dashboards/`.

## Stage 1 — Planning

Anunciar el modo (diaria o semanal), las listas a revisar (Discovery, Improvements y las tareas de Release del sprint) y los controles. Esperar confirmación.

## Stage 2 — Execution

`searchTasks` por lista y estado; `getTaskById` solo para los tickets que necesiten detalle (comentarios, subtareas).

| # | Control | Regla | Modo |
|---|---|---|---|
| 1 | Ticket fuera de `requirements` sin `po-vobo` | A-03, `Q-17` | Diaria |
| 2 | `requirements` con VoBo pendiente > 24 h hábiles (alerta) o > 48 h (debe pasar a `blocked`) | §16, `Q-17` | Diaria |
| 3 | `code review` sin Merge Request | A-06 | Diaria |
| 4 | Sin Reviewer QA en Discovery desde `r, d & architect review` (`Q-55`), o `ready for qa` sin Reviewer QA o sin Rejection_count | A-08 | Diaria |
| 5 | Salida de `mock testing` sin C-13/C-14 o con Rejection_count que no coincide con los C-14 | §8.1, A-09 | Diaria |
| 6 | `ready to merge` sin versión objetivo (según Project) | A-11, M-31 | Diaria |
| 7 | `blocked` sin tag `bloq-*`, sin C-20 del día o con más de 48 h sin escalamiento | §8.3, A-12, A-13 | Diaria |
| 8 | `uat-requerido` en `ready to merge` sin C-18 | A-10 | Diaria |
| 9 | Subtareas en un estado distinto al del padre en `ready to merge` / `merged` (`done w/d` que no siguió al padre) o padre en `done w/d` | D-15, A-20, `Q-53` | Diaria |
| 10 | Tags legacy en los tableros SDLC; tickets sin TYPE, Project o Iond Subcategory | §11, §12 | Semanal |
| 11 | `invalid` sin C-22 | A-16 | Semanal |
| 12 | Hallazgos `fuera-de-matriz` sin C-17 en el ticket origen | §8.2 | Semanal |
| 13 | Tarea de Release sin fecha de vencimiento, Project, versión o relaciones; C-23…C-29 faltantes según su estado | §7.1, A-18 | Semanal |
| 14 | WIP: `code review` > 3 por revisor, `mock testing` > 2 por QA, aging > 5/10 días | M-06 a M-08 | Semanal |
| 15 | Tickets de QA Kanban en un estado inconsistente con la cobertura (ver `test-suites/coverage`) | `Q-54` | Semanal |

Clasificar cada desvío: 🔴 bloquea el flujo o el release · 🟠 incumple un SLA · 🟡 dato faltante.

## Stage 3 — Reporting

- `knowledge/dashboards/sdlc-audit-<AAAA-MM-DD>.md`: resumen por severidad, tabla `control → ticket (URL) → desvío → acción → responsable (rol)` y comparación con el reporte anterior (desvíos recurrentes).
- Mensajes sugeridos (borradores) para los responsables, sin publicarlos.

## Reglas

- Solo lectura; no se mueve ni se comenta ningún ticket.
- Se reporta por **rol** (PO, LD/RM, QA, Dev), no se evalúa el desempeño de personas.
- Los desvíos recurrentes se llevan a la retro como mejora del proceso, no como culpa.
