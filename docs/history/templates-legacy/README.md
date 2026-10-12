# Templates retirados del QA Catalyst

> Historial. Estas plantillas pertenecen al **proceso anterior** ("Dual Track": fases Discovery / Deployment y release armado por el SM) y **no se usan** en el SDLC de IOND vigente (`knowledge/L1-project/sdlc-consolidation.md`). Se conservan solo como referencia; no se actualizan.

| Template retirado | Lo reemplaza | Motivo |
|---|---|---|
| `release-plan.md` | `templates/release-task.md` (T-04) | El cronograma por versión pasó a la tarea de Release semanal con calendario fijo (corte lunes 09:00, Go/No-Go viernes 10:00). |
| `release-smoke-matrix.md` | `templates/smoke-run.md` + `knowledge/test-suites/smoke-master.md` | El smoke ya no se arma por versión: es el smoke maestro único y fijo (SMK-01…SMK-17), en preprod y en producción (`Q-47`, `Q-52`). Las verificaciones de la versión pasaron a `templates/sanity-matrix.md`. |
| `release-regression-matrix.md` | `templates/regression-matrix.md` (capa 1) + `templates/e2e-run.md` (capa 2) | La regresión se selecciona por riesgo desde el E2E maestro (`Q-49`) y se complementa con la corrida del E2E maestro y la rotación G1–G4 (`Q-50`). |
| `comment.md` | `templates/comments/C-01.md` … `C-33.md` (generados desde la fuente canónica §14) · `templates/approval.md` (C-13) · `templates/rejection.md` (C-14) | Los comentarios de cierre de fase se reemplazaron por las plantillas de comentario por transición del SDLC. |
