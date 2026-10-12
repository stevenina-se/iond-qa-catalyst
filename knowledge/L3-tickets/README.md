# L3 — Memoria por ticket

> Una carpeta por ticket con todo lo que QA produce en el SDLC: matrices, pruebas, evidencia, reportes y borradores de comentario. Se crea al primer contacto de QA con el ticket y queda como registro histórico.

## Convención

- **Carpeta:** `knowledge/L3-tickets/<id-clickup>/` (el ID corto de ClickUp, p. ej. `86e3xxxxx`). Los tickets anteriores con ID custom (`IONF-xxx`) conservan su carpeta.
- **Primer archivo:** `ticket-memory.md` desde `templates/ticket-memory.md`.
- **Nombres de artefactos:** los de `skills/_shared/artifacts.md` (sección *Por ticket*).

## Artefactos por estado

| Estado | Artefacto | Skill |
|---|---|---|
| `prototype review` | `prototype-review-qa.md` | `prototype-review/review` |
| `requirements` | `requirements-matrix-v<N>.md` (una por versión; la vigente es la de N más alto con VoBo) | `requirements/matrix` · `requirements/mini-matrix` |
| `backlog` (Improvements) | `triage.md` | `improvements-triage/triage` |
| `code review` / `ready for qa` | `code-review-qa.md` | `code-review/review` |
| `ready for qa` | `test-matrix.md` + `test-matrix.csv` (TC con REQ-ID) | `mock-testing/plan` |
| `mock testing` | resultados en la matriz, `screenshots/`, `qa-report.md` (o `qa-report-iter<N>.md`) | `mock-testing/execute` · `report` |
| Cualquiera | `comments/C-xx-<AAAA-MM-DD>.md` (borradores para publicar) | La skill del estado |
| Después de `merged` | `automation-plan.md` · `automation-handoff.md` · `automation-review.md` | `automation/*` |

## Ciclo

```
prototype review → requirements (matriz vN + VoBo) → ready for qa (matriz de pruebas)
→ mock testing (ejecución) → reporte + C-13 / C-14 → [iteración N+1 si hay rechazo] → merged
```

- Un rechazo (C-14) incrementa Rejection_count y abre la iteración N+1 en el mismo L3 (`qa-report-iter<N>.md`).
- Un cambio de alcance después del VoBo crea `requirements-matrix-v<N+1>.md` (C-08).

## Carpetas especiales

- `drafts/`: borradores de tickets (por ejemplo, de automatización en `drafts/automation/`) antes de crearse en ClickUp.
- Los artefactos de tickets del modelo anterior (`ac-consolidated.md`, `test-plan.md`, `risk-triage.md`) se conservan como historial.

## Referencias

- Fuente canónica: `knowledge/L1-project/sdlc-consolidation.md` (estados, matrices §9, comentarios §14, tags §12).
- Plantillas: `templates/README.md`.
