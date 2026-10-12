# Skills — QA Catalyst de IOND

> Cada skill es una instrucción que un agente de IA sigue para una tarea concreta del SDLC. El agente lee primero el `SKILL.md` raíz (reglas, gates y enrutamiento) y después la skill del tablero y estado del ticket o del release.
> Las skills son agnósticas de herramienta (Markdown). Para Claude Code existen accesos en `.claude/skills/iond-*`.

## Contratos compartidos (`_shared/`)

| Archivo | Contenido |
|---|---|
| [`_shared/clickup.md`](_shared/clickup.md) | Tableros, estados, campos, frases fijas de C-xx, reglas del MCP de solo lectura |
| [`_shared/bot-test.md`](_shared/bot-test.md) | Estructura de bot-test, ejecución de suites por IDs, estados de automatización |
| [`_shared/evidence.md`](_shared/evidence.md) | Evidencia, bases de datos, Canal 1 (Playwright MCP), datos de prueba, secretos |
| [`_shared/artifacts.md`](_shared/artifacts.md) | Rutas de los artefactos por ticket, por release y transversales |

## Por estado del ticket

| Skill | Tablero · estado | Salida |
|---|---|---|
| [`prototype-review/review.md`](prototype-review/review.md) | Discovery · `prototype review` | `prototype-review-qa.md` |
| [`requirements/matrix.md`](requirements/matrix.md) | Discovery · `requirements` | Matriz de Requerimientos vN + C-05 |
| [`requirements/mini-matrix.md`](requirements/mini-matrix.md) | Improvements · `requirements` | Mini-matriz + C-05 |
| [`improvements-triage/triage.md`](improvements-triage/triage.md) | Improvements · `backlog` | `triage.md` + C-33 |
| [`code-review/review.md`](code-review/review.md) | `code review` / `ready for qa` | `code-review-qa.md` |
| [`mock-testing/plan.md`](mock-testing/plan.md) | `ready for qa` | Matriz de Pruebas con REQ-ID |
| [`mock-testing/execute.md`](mock-testing/execute.md) | `mock testing` | Resultados y evidencia; C-15/C-17/C-20 |
| [`mock-testing/report.md`](mock-testing/report.md) | Cierre de `mock testing` | `qa-report.md` + C-13 / C-14 |
| [`bug-reporter/create.md`](bug-reporter/create.md) | Bug nuevo | `bug-report.md` (T-02) |
| [`knowledge/update-module.md`](knowledge/update-module.md) | Después del despliegue | L2 actualizado |

## Release (Scrum Master, QA y LQA)

| Skill | Momento | Salida |
|---|---|---|
| [`release/weekly-plan.md`](release/weekly-plan.md) | Viernes previo · corte | T-04 + C-23 |
| [`release/ingest.md`](release/ingest.md) | `dev preparation` | `tickets.md` + mapa de impacto |
| [`release/smoke.md`](release/smoke.md) | `smoke` · post-despliegue | `smoke-preprod.md` / `smoke-prod.md` + C-25 / C-31 |
| [`release/sanity.md`](release/sanity.md) | `sanity` | `sanity-matrix.md` + C-26 |
| [`release/regression.md`](release/regression.md) | `regression` (capa 1) | `regression-matrix.md` + C-27 |
| [`release/e2e.md`](release/e2e.md) | `regression` (capa 2) | `e2e-run.md` + C-27 |
| [`release/go-no-go.md`](release/go-no-go.md) | `ready for release` | `go-no-go.md` + C-29 |
| [`release/notes.md`](release/notes.md) | `ready for release` | Notas interna y cliente |
| [`release/deployment-protocol.md`](release/deployment-protocol.md) | `ready for release` → ACT-01/02 | Protocolo + C-30 / C-31 |
| [`release/brief.md`](release/brief.md) | Cualquiera | Brief para stakeholders |
| [`release/bug-hunt.md`](release/bug-hunt.md) | ACT-03 bug bash quincenal | Reporte + bugs `det-exploratorio` |

## Suites, automatización y gobierno

| Skill | Para qué |
|---|---|
| [`test-suites/import-e2e.md`](test-suites/import-e2e.md) | Importar la hoja del E2E maestro con IDs estables y cobertura |
| [`test-suites/smoke-master.md`](test-suites/smoke-master.md) | Revisar el smoke maestro |
| [`test-suites/coverage.md`](test-suites/coverage.md) | Cobertura y hoja de ruta de automatización |
| [`automation/plan.md`](automation/plan.md) | Qué automatizar (smoke → baseline → sanity) |
| [`automation/code.md`](automation/code.md) | Paquete de automatización para el responsable de bot-test |
| [`automation/review.md`](automation/review.md) | Revisión y estabilidad 3/3 de los tests entregados |
| [`sdlc-audit/audit.md`](sdlc-audit/audit.md) | Auditoría de cumplimiento del flujo (SM) |
| [`metrics/weekly.md`](metrics/weekly.md) | Métricas semanales (doc 07) |

## Skills retiradas

Las skills del modelo anterior (Dual Track, sprints 2+1, smoke por ticket) están en [`docs/history/skills-legacy/`](../docs/history/skills-legacy/README.md), con la skill que reemplaza a cada una.
