# Contrato compartido: artefactos y rutas

> Dónde guarda cada skill lo que produce. Una salida que no está en su ruta no existe para los gates del `SKILL.md`.

## Por ticket — `knowledge/L3-tickets/<id-clickup>/`

| Artefacto | Lo produce | Estado del ticket |
|---|---|---|
| `ticket-memory.md` | Todas (se actualiza en cada sesión) | Cualquiera |
| `prototype-review-qa.md` | `prototype-review/review` | `prototype review` |
| `requirements-matrix-v<N>.md` | `requirements/matrix` o `requirements/mini-matrix` | `requirements` |
| `triage.md` | `improvements-triage/triage` | `backlog` |
| `code-review-qa.md` | `code-review/review` | `code review` / `ready for qa` |
| `test-matrix.md` + `test-matrix.csv` | `mock-testing/plan` (resultados por `execute`) | `ready for qa` / `mock testing` |
| `qa-report.md` (o `qa-report-iter<N>.md`) | `mock-testing/report` | Cierre de `mock testing` |
| `comments/C-xx-<AAAA-MM-DD>.md` | La skill que prepara el comentario | Según la transición |
| `bug-report.md` | `bug-reporter/create` | Bug nuevo |
| `automation-plan.md` · `automation-handoff.md` · `automation-review.md` | `automation/*` | Después de `merged` |
| `screenshots/` | Ejecución | — |

## Por release — `knowledge/releases/<producto>/<versión>/`

`<producto>` ∈ `iond`, `ionmind`, `stagemind` (los tickets con Project = Gateway van en el release de `iond`). `<versión>` = `vX.Y.Z`. Un hotfix usa su propia versión (`vX.Y.Z+1`).

| Artefacto | Lo produce | Estado de la tarea de Release |
|---|---|---|
| `release-task.md` | `release/weekly-plan` | Viernes previo / `dev preparation` |
| `tickets.md` + `tickets.csv` | `release/ingest` | `dev preparation` |
| `smoke-preprod.md` | `release/smoke` | `smoke` |
| `sanity-matrix.md` | `release/sanity` | `sanity` |
| `regression-matrix.md` + `.csv` | `release/regression` | `regression` (capa 1) |
| `e2e-run.md` + `.csv` | `release/e2e` | `regression` (capa 2) |
| `go-no-go.md` | `release/go-no-go` | `ready for release` |
| `release-notes-internal.md` · `release-notes-client.md` | `release/notes` | `ready for release` |
| `brief.md` | `release/brief` | Cualquiera (resumen para stakeholders) |
| `deployment-protocol.md` | `release/deployment-protocol` | `ready for release` → ACT-01 |
| `smoke-prod.md` | `release/smoke` (modo producción) | ACT-02 |
| `comments/C-xx-<AAAA-MM-DD>.md` | La skill que prepara el comentario | — |
| `evidence/` | Ejecución | — |

Las carpetas planas anteriores (`knowledge/releases/v0.1.0/`, `v0.1.1/`, `v1.0.0/`, `ionmind-v1.10.1/`, `stagemind-v1.5.1/`) son historial y no se mueven.

## Transversales

| Artefacto | Lo produce |
|---|---|
| `knowledge/test-suites/e2e-master.csv`, `coverage.md`, `exports/` | `test-suites/import-e2e`, `test-suites/coverage` |
| `knowledge/test-suites/smoke-master.md` | `test-suites/smoke-master` (con acuerdo LQA + LD/RM) |
| `knowledge/test-suites/automation-roadmap.md` | `test-suites/coverage` + LQA |
| `knowledge/dashboards/sdlc-audit-<AAAA-MM-DD>.md` | `sdlc-audit/audit` |
| `knowledge/dashboards/metrics-<AAAA>-W<NN>.md` | `metrics/weekly` |
| `knowledge/dashboards/bug-bash/bug-hunt-<módulo>-<AAAA-MM-DD>.md` | `release/bug-hunt` (ACT-03) |

## Nombres de borradores de comentario

`comments/C-13-2026-10-14.md`: el ID del comentario y la fecha. El encabezado del archivo indica dónde publicarlo (URL del ticket o de la tarea de Release) y quién lo publica.
