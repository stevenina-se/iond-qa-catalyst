# Templates del QA Catalyst — SDLC IOND

> Plantillas que usan las skills (`skills/`) para preparar artefactos y comentarios. Fuente de verdad: `knowledge/L1-project/sdlc-consolidation.md` (estados, tags, campos, T-01…T-04 y C-01…C-33) y el Estándar de QA (`docs/sdlc-iond/src/05-estandar-operativo-qa-iond.md`).
> Convenciones: `[...]` = completar · estados en `backticks` tal como en ClickUp · severidad = prioridad nativa (`urgent` / `high` / `normal` / `low`). El MCP de ClickUp es de solo lectura: las skills **preparan** y QA/SM **publican**. Rutas de salida: `skills/_shared/artifacts.md`.

## Por ticket — Discovery e Improvements

| Template | Para qué | Skill que lo usa | Comentario asociado |
|---|---|---|---|
| [`prototype-review-qa.md`](prototype-review-qa.md) | Salida de QA en `prototype review`: testabilidad, captura inicial de REQ, pendientes y propuesta de UAT | `prototype-review/review` | C-04 (insumo del acta) |
| [`architecture-brief-qa.md`](architecture-brief-qa.md) | Checklist técnico de `prototype review`: contrato, testabilidad, NFR, datos de prueba, dependencias, ¿`uat-requerido`? | `prototype-review/review` | C-04 (insumo) |
| [`requirements-matrix.md`](requirements-matrix.md) | Matriz de Requerimientos vN (Discovery, o Improvements con `requirements`) | `requirements/matrix` | C-05 · C-06 · C-07 · C-08 |
| [`mini-matrix.md`](mini-matrix.md) | Mini-matriz de Improvements (≤ 5 REQ + no regresión de zonas cercanas) | `requirements/mini-matrix` | C-05 · C-06 · C-07 · C-08 |
| [`triage.md`](triage.md) | Triage de `backlog`: calidad del reporte (T-02/T-03), clasificación y destino | `improvements-triage/triage` | C-33 |
| [`pilot-notes.md`](pilot-notes.md) | Clasificación de los ajustes de `pilot presentation` (`Q-11`) | Uso directo de QA (cambio de alcance → `requirements/matrix`) | C-10 (lo publica el SM) · C-08 |
| [`test-matrix.md`](test-matrix.md) | Matriz de Pruebas con REQ-ID + cabecera del `test-matrix.csv` | `mock-testing/plan` · `mock-testing/execute` | Coherencia con C-13 / C-14 |
| [`qa-report.md`](qa-report.md) | Reporte de `mock testing`: trazabilidad REQ → TC → resultado, hallazgos, veredicto y estado destino | `mock-testing/report` | C-13 · C-14 · C-17 |
| [`approval.md`](approval.md) | Aprobación de QA (= C-13 con frase fija) | `mock-testing/report` | C-13 |
| [`rejection.md`](rejection.md) | Rechazo de QA (= C-14 con frase fija) | `mock-testing/report` | C-14 |
| [`bug-ticket.md`](bug-ticket.md) | Bug (= T-02 + Project, Iond Subcategory, `det-*`, REQ violado, ticket padre) | `bug-reporter/create` | C-17 · C-28 · C-32 (según la fase) |
| [`ticket-memory.md`](ticket-memory.md) | Memoria del ticket entre sesiones (estado, matriz, VoBo, Rejection_count, iteraciones) | Todas | — |

## Por release — tarea de Release semanal

| Template | Para qué | Skill que lo usa | Comentario asociado |
|---|---|---|---|
| [`release-task.md`](release-task.md) | Tarea de Release (= T-04): información, prerrequisitos, suites, riesgo, calendario, quórum | `release/weekly-plan` | C-23 (RM) |
| [`smoke-run.md`](smoke-run.md) | Ejecución del smoke maestro SMK-01…SMK-17 (preprod o producción) con limpieza | `release/smoke` | C-25 · C-31 |
| [`sanity-matrix.md`](sanity-matrix.md) | Sanity de la versión: REQ críticos por ticket (`SAN-<ticket>-<REQ>`) e interacciones | `release/sanity` | C-26 |
| [`regression-matrix.md`](regression-matrix.md) | Regression capa 1: selección por riesgo del E2E maestro + filas `RGR-xx` | `release/regression` | C-27 (capa 1) |
| [`e2e-run.md`](e2e-run.md) | E2E maestro capa 2: automatizado completo + rotación G1–G4 | `release/e2e` | C-27 (capa 2) |
| [`go-no-go.md`](go-no-go.md) | Acta Go/No-Go con checklist de criterios y votos del quórum | `release/go-no-go` | C-29 |
| [`release-notes.md`](release-notes.md) | Release notes por producto y semana (interna y cliente) | `release/notes` | C-29 (enlaces) |
| [`release-brief.md`](release-brief.md) | Resumen para stakeholders: smoke → sanity → capa 1 → capa 2 → Go/No-Go | `release/brief` | — |
| [`deployment-protocol.md`](deployment-protocol.md) | Despliegue y post-despliegue: ramas RC, rollback, smoke en producción, monitoreo 48 h, hotfix | `release/deployment-protocol` | C-30 · C-31 · C-32 |
| [`bug-hunt-report.md`](bug-hunt-report.md) | Bug bash quincenal (ACT-03); hallazgos a `backlog` con `det-exploratorio` | `release/bug-hunt` | — (T-02) |

## Comentarios — `comments/`

[`comments/C-01.md` … `comments/C-33.md`](comments/README.md): una plantilla por comentario de transición, **generadas** desde la fuente canónica §14. No se editan a mano:

```bash
python -I docs/sdlc-iond/_build/build_templates.py
```

Los borradores se copian a `knowledge/L3-tickets/<id>/comments/C-xx-<AAAA-MM-DD>.md` (o a la carpeta del release). `approval.md` y `rejection.md` mantienen C-13 y C-14 con su guía de uso; si difieren del generado, prevalece el generado.

## Retirados

Las plantillas del proceso anterior (`release-plan.md`, `release-smoke-matrix.md`, `release-regression-matrix.md`, `comment.md`) están en `docs/history/templates-legacy/`.
