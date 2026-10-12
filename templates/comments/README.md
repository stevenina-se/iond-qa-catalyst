# Plantillas de comentario C-01 … C-33

> Generado desde knowledge/L1-project/sdlc-consolidation.md §14. No editar a mano: regenerar con build_templates.py.

> Se copian tal cual en ClickUp. `[...]` = completar. Los comentarios **se publican en el ticket** antes o al momento de mover el estado.

Las skills del catalyst **preparan** el borrador (en `knowledge/L3-tickets/<id>/comments/` o en la carpeta del release) y QA/SM lo **publican** en ClickUp. El MCP de ClickUp es de solo lectura.

| ID | Título | Tablero / fase | Archivo |
|---|---|---|---|
| C-01 | `idea/request` → `assignment` (PO) | Discovery — definición | [`C-01.md`](C-01.md) |
| C-02 | `assignment` → `r, d & architect review` (LD, con el QA que asigna el LQA) | Discovery — definición | [`C-02.md`](C-02.md) |
| C-03 | `r, d & architect review` → `prototype review` (Dev + aprobación LD) | Discovery — definición | [`C-03.md`](C-03.md) |
| C-04 | Acta de `prototype review` (SM/PO) | Discovery — definición | [`C-04.md`](C-04.md) |
| C-05 | Solicitud de VoBo (QA → PO) | Discovery — definición | [`C-05.md`](C-05.md) |
| C-06 | VoBo del PO | Discovery — definición | [`C-06.md`](C-06.md) |
| C-07 | Dudas del Dev sobre la matriz (opcional) | Discovery — definición | [`C-07.md`](C-07.md) |
| C-08 | Cambio de alcance (matriz v+1) | Discovery — definición | [`C-08.md`](C-08.md) |
| C-09 | Handoff del Dev (*Changes and Specifications Form for QA*) | Discovery / Improvements — construcción y validación | [`C-09.md`](C-09.md) |
| C-10 | Acta de `pilot presentation` (SM) | Discovery / Improvements — construcción y validación | [`C-10.md`](C-10.md) |
| C-11 | Resultado de Code Review (LD) | Discovery / Improvements — construcción y validación | [`C-11.md`](C-11.md) |
| C-12 | `ready for qa` — confirmación del QA (LQA) | Discovery / Improvements — construcción y validación | [`C-12.md`](C-12.md) |
| C-13 | Aprobación de QA (`mock testing` → `uat` / `ready to merge`) | Discovery / Improvements — construcción y validación | [`C-13.md`](C-13.md) |
| C-14 | Rechazo de QA (`mock testing` → `to do`) | Discovery / Improvements — construcción y validación | [`C-14.md`](C-14.md) |
| C-15 | Escalamiento de desacuerdo (QA o Dev) | Discovery / Improvements — construcción y validación | [`C-15.md`](C-15.md) |
| C-16 | Decisión del PO | Discovery / Improvements — construcción y validación | [`C-16.md`](C-16.md) |
| C-17 | Hallazgo fuera de matriz | Discovery / Improvements — construcción y validación | [`C-17.md`](C-17.md) |
| C-18 | Resultado de UAT | Discovery / Improvements — construcción y validación | [`C-18.md`](C-18.md) |
| C-19 | `merged` (RM) | Discovery / Improvements — construcción y validación | [`C-19.md`](C-19.md) |
| C-20 | `blocked` — inicio y actualización diaria | Discovery / Improvements — construcción y validación | [`C-20.md`](C-20.md) |
| C-21 | Desbloqueo | Discovery / Improvements — construcción y validación | [`C-21.md`](C-21.md) |
| C-22 | `invalid` (PO) | Discovery / Improvements — construcción y validación | [`C-22.md`](C-22.md) |
| C-23 | `dev preparation` concluido (RM) | Releases | [`C-23.md`](C-23.md) |
| C-24 | `unit test & ci` | Releases | [`C-24.md`](C-24.md) |
| C-25 | `smoke` (QA) | Releases | [`C-25.md`](C-25.md) |
| C-26 | `sanity` (QA) | Releases | [`C-26.md`](C-26.md) |
| C-27 | `regression` (QA) | Releases | [`C-27.md`](C-27.md) |
| C-28 | Bug en RC / fix-forward | Releases | [`C-28.md`](C-28.md) |
| C-29 | Acta Go / No-Go (`ready for release`) | Releases | [`C-29.md`](C-29.md) |
| C-30 | Despliegue ejecutado (RM) | Releases | [`C-30.md`](C-30.md) |
| C-31 | Validación post-despliegue | Releases | [`C-31.md`](C-31.md) |
| C-32 | Apertura de hotfix (PO / LQA) | Releases | [`C-32.md`](C-32.md) |
| C-33 | `backlog` → `to do` / `requirements` (PO/SM) | Improvements — triage | [`C-33.md`](C-33.md) |

Regenerar: `python -I docs/sdlc-iond/_build/build_templates.py` (desde la raíz del repo).
