# SDLC IOND — Documentación de consolidación

Documentación para adoptar el SDLC de IOND (Discovery · Improvements · Releases semanales) y el rol de QA como Analista de Calidad y Requerimientos. Estado: **versión consolidada con las decisiones Q-01 a Q-55** (fase F1 cerrada el 2026-10-09; plan de pruebas de release F2b cerrado el 2026-10-10). Propuesta por Steve Nina — Scrum Master IOND.

## Documentos

| # | Documento | Fuente (Markdown) | PDF |
|---|---|---|---|
| 00 | Hoja de Ruta | [src/00-hoja-de-ruta.md](src/00-hoja-de-ruta.md) | [pdf](pdf/00-hoja-de-ruta.pdf) |
| 01 | Diagnóstico y Plan de Adecuación del QA Catalyst | [src/01-diagnostico-y-plan-catalyst.md](src/01-diagnostico-y-plan-catalyst.md) | [pdf](pdf/01-diagnostico-y-plan-catalyst.pdf) |
| 02 | Análisis del Flujo SDLC IOND | [src/02-analisis-flujo-sdlc-iond.md](src/02-analisis-flujo-sdlc-iond.md) | [pdf](pdf/02-analisis-flujo-sdlc-iond.pdf) |
| 03 | Registro de Decisiones, Riesgos y Limitaciones | [src/03-preguntas-inconsistencias-riesgos.md](src/03-preguntas-inconsistencias-riesgos.md) | [pdf](pdf/03-preguntas-inconsistencias-riesgos.pdf) |
| 04 | Acuerdo de Flujo de Trabajo IOND | [src/04-acuerdo-flujo-trabajo-iond.md](src/04-acuerdo-flujo-trabajo-iond.md) | [pdf](pdf/04-acuerdo-flujo-trabajo-iond.pdf) |
| 05 | Estándar Operativo de QA — Aplicación IOND | [src/05-estandar-operativo-qa-iond.md](src/05-estandar-operativo-qa-iond.md) | [pdf](pdf/05-estandar-operativo-qa-iond.pdf) |
| 06a | Guía de Gobierno ClickUp — Scrum Master | [src/06a-guia-clickup-scrum-master.md](src/06a-guia-clickup-scrum-master.md) | [pdf](pdf/06a-guia-clickup-scrum-master.pdf) |
| 06b | Guía Operativa ClickUp — Development + QA | [src/06b-guia-clickup-dev-qa.md](src/06b-guia-clickup-dev-qa.md) | [pdf](pdf/06b-guia-clickup-dev-qa.pdf) |
| 07 | Dashboards y Métricas | [src/07-dashboards-y-metricas.md](src/07-dashboards-y-metricas.md) | [pdf](pdf/07-dashboards-y-metricas.pdf) |
| 08 | Guía de Uso del QA Catalyst | [src/08-guia-uso-qa-catalyst.md](src/08-guia-uso-qa-catalyst.md) | [pdf](pdf/08-guia-uso-qa-catalyst.pdf) |

**Fuente canónica** (estados, roles, campos, tags, plantillas de comentario y automatizaciones): [knowledge/L1-project/sdlc-consolidation.md](../../knowledge/L1-project/sdlc-consolidation.md). Los documentos incluyen secciones de ella con `<!-- @include … #seccion -->`, así que **se edita la fuente canónica y se regeneran los PDF**.

**Suites del release** (smoke maestro, E2E maestro, cobertura y automatización): [knowledge/test-suites/](../../knowledge/test-suites/README.md).

**Plantillas de comentario C-01…C-33** para el catalyst: se generan desde la fuente canónica con `python -I docs/sdlc-iond/_build/build_templates.py` (salida en `templates/comments/`).

**Guías tabulares por estado:** `resources/IOND SDLC - DISCOVERY.csv`, `- IMPROVEMENTS.csv`, `- RELEASES.csv`. Las versiones anteriores están en [_build/fuentes-originales/](_build/fuentes-originales/).

## Regenerar los PDF

Requisitos: Node ≥ 18, Google Chrome o Microsoft Edge y acceso a internet (marked y Mermaid se cargan desde `cdn.jsdelivr.net`).

```bash
node docs/sdlc-iond/_build/build.mjs        # todos los documentos
node docs/sdlc-iond/_build/build.mjs 03     # solo los que empiezan con "03"
```

- El HTML intermedio queda en `_build/html/` y los PDF en `pdf/`.
- Si el navegador no está en la ruta estándar, define `CHROME_PATH`.
- **Portada:** todo lo que está antes de la primera línea `---` del Markdown.
- **Diagramas:** bloques ` ```mermaid `.

## Convenciones

- Los estados se escriben con el nombre exacto de ClickUp, en minúsculas y entre backticks.
- Custom fields de IOND: los 13 originales (Merge Request 1–4, Rejection_count, Dev Reviewer, Iond Subcategory, Iond.Version, Ionmind.Version, Project, QA Points, Reviewer QA y TYPE) más **Stagemind.Version**; el heredado **G.Version** solo se llena para Project = Gateway. Lo demás se cubre con tags SDLC y la prioridad nativa.
- **(Q-xx)** remite a la decisión del *Registro de Decisiones* (documento 03); **AV-xx** a una acción de verificación con responsable.
- **IDs de referencia:** Q (decisiones), AV (acciones de verificación), O (observaciones), F (inconsistencias), R (riesgos), L (limitaciones), B (puntos de quiebre del catalyst), A (automatizaciones), C (plantillas de comentario), T (plantillas de tarea), M (métricas), SMK (smoke maestro) y E2E (filas del E2E maestro).
