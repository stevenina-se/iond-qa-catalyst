# Skills retiradas del QA Catalyst

> Historial de las skills del modelo anterior (Dual Track: *Discovery Track* / *Deployment Track*, sprints 2+1). Se conservan **solo como referencia**: ninguna skill vigente ni el `SKILL.md` raíz las invoca.
> Retiradas el 2026-10-10 con la adecuación del catalyst al **SDLC de IOND** (fuente canónica `knowledge/L1-project/sdlc-consolidation.md` v2.2 y `docs/sdlc-iond/src/05-estandar-operativo-qa-iond.md`).
> Cada archivo se movió sin cambios, con su ruta relativa a `skills/` (p. ej. `skills/test-docs/prioritize.md` → `docs/history/skills-legacy/test-docs/prioritize.md`).

## Qué cambió de fondo

| Modelo anterior (retirado) | SDLC vigente |
|---|---|
| Dual Track: *Discovery Track* y *Deployment Track* con runbooks | Skills por **tablero y estado** de ClickUp (Discovery, Improvements, Releases) |
| Acceptance Criteria / Gherkin consolidados por QA como contrato | **Matriz de Requerimientos vN** redactada por QA y validada por el PO con un único VoBo (C-06 + `po-vobo`) |
| "QA no rechaza en Discovery" | QA evalúa testabilidad en `prototype review` y **rechaza solo contra la matriz con VoBo** en `mock testing` (C-14); lo demás es fuera de matriz (C-17) |
| Testing en lote sobre `DEVELOPMENT` | `mock testing` en el **ambiente asignado al QA con la rama del ticket** (`Q-05`) |
| Smoke por ticket + bloques por tipo | Matriz de Pruebas con trazabilidad REQ-ID → TC; el smoke es del release (smoke maestro SMK-01…17) |
| Sprints 2+1 y regresión por sprint | Release semanal por producto (corte lunes 09:00, Go/No-Go viernes 10:00) con smoke, sanity y regression por riesgo |
| L2 actualizado al aprobar un ticket | L2 actualizado en lote **después del despliegue** del release |

## Skills retiradas y su reemplazo

| Skill retirada | Ruta en este historial | Reemplazo vigente | Notas |
|---|---|---|---|
| `skills/discovery-runbook.md` | `discovery-runbook.md` | `skills/prototype-review/review.md` → `skills/requirements/matrix.md` | La reconciliación de AC con comentarios pasa a la Matriz de Requerimientos; el análisis de riesgo, a `prototype review` |
| `skills/deployment-runbook.md` | `deployment-runbook.md` | `skills/code-review/review.md` → `skills/mock-testing/plan.md` → `execute.md` → `report.md` | Se conservan: code review de QA antes de ejecutar, Canal 1, evidencia en BD, reporte obligatorio, iteración N+1 |
| `skills/test-docs/prioritize.md` | `test-docs/prioritize.md` | `skills/prototype-review/review.md` (análisis de riesgo, preguntas al PO y al Dev/LD) | El `risk-triage.md` se integra en `prototype-review-qa.md` |
| `skills/test-docs/document.md` (modo AC) | `test-docs/document.md` | `skills/requirements/matrix.md` · `skills/requirements/mini-matrix.md` | `ac-consolidated.md` → `requirements-matrix-v<N>.md` |
| `skills/test-docs/document.md` (modo matrix) | `test-docs/document.md` | `skills/mock-testing/plan.md` | `test-matrix.md` + `.csv` con REQ-ID, ORIGEN y USO |
| `skills/test-docs/document.md` (modo Architecture Brief) | `test-docs/document.md` | `skills/prototype-review/review.md` (checklist técnico de `templates/architecture-brief-qa.md`) | |
| `skills/sprint-testing/plan.md` | `sprint-testing/plan.md` | `skills/mock-testing/plan.md` | `test-plan.md` desaparece: el orden de ejecución, el ambiente y los datos viven en `test-matrix.md` |
| `skills/sprint-testing/test.md` | `sprint-testing/test.md` | `skills/mock-testing/execute.md` | `db-evidence.md` → sección *Verificación en BD* de `test-matrix.md` |
| `skills/sprint-testing/report.md` | `sprint-testing/report.md` | `skills/mock-testing/report.md` | Veredicto con C-13 / C-14; historial `qa-report-iter<N>.md` |
| `skills/release/plan.md` · `plan-v1.md` | `release/plan.md` · `release/plan-v1.md` (fuera de git, privadas del SM) | `skills/release/weekly-plan.md` | Modelo 2+1 reemplazado por el corte semanal y la tarea de Release T-04 |
| `skills/sprint-planning/SKILL.md` | `sprint-planning/SKILL.md` | `skills/release/weekly-plan.md` + `skills/sdlc-audit/audit.md` | Usaba estados del modelo anterior |
| `skills/release/regression-matrix.md` | `release/regression-matrix.md` | `skills/release/regression.md` (capa 1) + `skills/release/e2e.md` (capa 2) | El motor DIRECTA / INDIRECTA / BASELINE pasa a la selección por riesgo desde el E2E maestro; las filas DIRECTA van a `sanity` |
| `skills/release/smoke-matrix.md` | `release/smoke-matrix.md` | `skills/release/smoke.md` + `knowledge/test-suites/smoke-master.md` | El smoke deja de armarse por versión: es único y fijo (Q-47) |
| `skills/regression/run.md` · `analyze.md` | `regression/run.md` · `regression/analyze.md` | `skills/release/regression.md` (§ *Clasificar fallas*) | La clasificación real / inestable / ambiente / desactualizado / dato se conserva |
| `skills/regression/decide.md` | `regression/decide.md` | `skills/release/go-no-go.md` (C-29) | Un único criterio de Go/No-Go (doc 05 §7.1) |

## Skills adaptadas en su lugar (no se movieron)

| Skill | Cambio principal |
|---|---|
| `skills/code-review/review.md` | Lee los PR de los campos Merge Request, compara contra `DEVELOPMENT`, mapea hallazgos a REQ-ID e inyecta TC una sola vez con `ORIGEN = Code review`; sin modos Discovery/Deployment |
| `skills/bug-reporter/create.md` | Reporte T-02 con `det-*`, tag de área, Project, Iond Subcategory, REQ violado y relación con el ticket origen o la tarea de Release |
| `skills/knowledge/update-module.md` | Solo en lote después del despliegue de un release; agrega *Reglas de negocio*, *Specs bot-test* y *Filas E2E* |

La versión anterior de estas tres skills está en el historial de git.

## Artefactos L3 del modelo anterior

| Artefacto anterior | Equivalente vigente |
|---|---|
| `risk-triage.md` | `prototype-review-qa.md` |
| `ac-consolidated.md` | `requirements-matrix-v<N>.md` |
| `architecture-brief-qa.md` | Checklist técnico de `prototype review`: anexo de `prototype-review-qa.md` (archivo aparte en tickets L o con cambios de contrato o de BD) |
| `test-plan.md` | `test-matrix.md` (control, orden de ejecución, ambiente y datos) |
| `db-evidence.md` | `test-matrix.md` § *Verificación en BD* |
| `test-matrix-v<N>.md` / `qa-report-v<N>.md` | Una sola `test-matrix.md` (iteración en su control) / `qa-report.md` (iteración 1) y `qa-report-iter<N>.md` (iteración N ≥ 2) |
| `pre-existing-bugs.md` | Sección *Preexistentes* de `code-review-qa.md` (+ T-02 con `bug-reporter/create`) |

Los L3 creados antes del corte de transición (`Q-45`) conservan sus artefactos anteriores y no se migran.
