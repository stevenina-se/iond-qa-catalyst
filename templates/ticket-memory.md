# Memoria del ticket — [id-clickup] · [título del ticket]

> **Plantilla del QA Catalyst** — contexto persistente del ticket entre sesiones. Todas las skills la leen al empezar y la actualizan al terminar.
> **Se guarda en:** `knowledge/L3-tickets/[id-clickup]/ticket-memory.md`. La fuente de verdad del estado y de los campos es ClickUp (leído con el MCP, solo lectura); aquí se registra lo leído y su fecha.

## Ficha

| Campo | Valor |
|---|---|
| Ticket | [id-clickup] — [título] — [url] |
| Tablero | Discovery / Improvements |
| Estado actual | `[estado]` — leído el [AAAA-MM-DD hh:mm] |
| TYPE · prioridad | [New Feature / Improvement / Bug / Refactor / Task] · [`urgent` / `high` / `normal` / `low`] |
| Project · Iond Subcategory · área | [Iond / IONMIND / STAGEMIND / Gateway] · [subcategoría] · [`iond-core` / `iond-uxui` / `iond-infra` / `iond-ia`] |
| Versión objetivo | [Iond.Version / Ionmind.Version / Stagemind.Version / G.Version] = [vX.Y.Z / DEVELOPMENT / develop] |
| Dev (assignee) · Dev Reviewer | @[dev] · @[reviewer] |
| Reviewer QA · QA Points | @[qa] · [n] |
| Merge Request 1–4 | [altacrest/[repo] — PR] |
| Módulo L2 | `knowledge/L2-modules/[módulo]` (vía `knowledge/test-suites/_config/subcategory-map.csv`) |
| Tags SDLC | [`po-vobo` · `uat-requerido` · `cambio-alcance` · `escalado-po` · `bloq-*` · `det-*` · `fuera-de-matriz` · `pilot-feedback` · `hotfix` · `diferido`] |
| Ticket padre / subtareas | #[id] / #[id] — `[estado]` |

## Matriz y VoBo

| Campo | Valor |
|---|---|
| Matriz vigente | v[N] — `requirements-matrix-v[N].md` · No aplica (bug) |
| VoBo del PO | C-06 [AAAA-MM-DD] · tag `po-vobo`: [sí / no] |
| Acuse del Dev | Checklist marcado: [sí / no] |
| UAT | `uat-requerido`: [sí / no] |
| Contrato de `prototype review` | [versión / enlace] · No aplica |
| Pendientes de decisión del PO | REQ-[xx] — [...] · Ninguno |

## Iteraciones de `mock testing`

| Iteración | Fechas | Veredicto | Rejection_count | REQ incumplidos | Reporte | Comentario |
|---|---|---|---|---|---|---|
| 1 | [AAAA-MM-DD] | ✅ / ❌ | [n] | REQ-[xx] · — | `qa-report.md` | C-13 / C-14 [AAAA-MM-DD] |

## Hallazgos y tickets derivados

| ID | Origen | Severidad | Ticket | Tags | Estado |
|---|---|---|---|---|---|
| OBS-01 | `mock testing` / fuera de matriz / Pilot / UAT | [prioridad] | #[id] | `fuera-de-matriz` · `det-*` | [...] |

## Decisiones registradas en el ticket

| Fecha | Tema | Decisión | Rol que decide | Comentario |
|---|---|---|---|---|
| [AAAA-MM-DD] | [...] | [...] | PO / LD / QA | C-04 / C-06 / C-10 / C-16 / C-22 |

## Bloqueos

| Desde | Causa | Plan de acción | Hasta | Comentarios |
|---|---|---|---|---|
| [AAAA-MM-DD] | `bloq-externo` / `bloq-ambiente` / `bloq-definicion` / `bloq-dependencia` | [...] | [AAAA-MM-DD] | C-20 · C-21 |

## Artefactos

| Artefacto | Estado | Archivo |
|---|---|---|
| Revisión de QA en `prototype review` | ⬜ / ✅ / N/A | `prototype-review-qa.md` |
| Matriz de Requerimientos / mini-matriz | ⬜ / ✅ / N/A | `requirements-matrix-v[N].md` |
| Triage | ⬜ / ✅ / N/A | `triage.md` |
| Notas del Pilot | ⬜ / ✅ / N/A | `pilot-notes.md` |
| Code review de QA | ⬜ / ✅ / N/A | `code-review-qa.md` |
| Matriz de Pruebas | ⬜ / ✅ | `test-matrix.md` + `test-matrix.csv` |
| Reporte de QA | ⬜ / ✅ | `qa-report.md` / `qa-report-iter[N].md` |
| Reporte de bug | ⬜ / ✅ / N/A | `bug-report.md` |
| Borradores de comentario | — | `comments/C-xx-[AAAA-MM-DD].md` |
| Capturas | — | `screenshots/` |

## Comentarios publicados

| C-xx | Fecha | Publicado por (rol) | Borrador |
|---|---|---|---|
| C-[xx] | [AAAA-MM-DD] | QA / SM / PO / LD / RM | `comments/C-[xx]-[AAAA-MM-DD].md` |

## Bitácora de sesiones

| Fecha y hora | Skill | Acción | Resultado / siguiente paso |
|---|---|---|---|
| [AAAA-MM-DD hh:mm] | [área/acción] | Contexto cargado: L1 + L2 de [módulo] + L3 | [...] |
