# Contrato compartido: lectura de ClickUp

> Lo usan todas las skills. ClickUp es la **fuente oficial** del flujo; el catalyst lo **lee** con el MCP en modo solo lectura (`L-09`) y **prepara** comentarios y artefactos que QA, el SM o el LQA publican a mano.

## Espacio y tableros

| Tablero | ID de lista | Estados (exactos) |
|---|---|---|
| Discovery | `901717038641` | `idea/request`, `assignment`, `r, d & architect review`, `prototype review`, `requirements`, `to do`, `dev in progress`, `pilot presentation`, `code review`, `ready for qa`, `mock testing`, `uat`, `ready to merge`, `merged`, `blocked`, `done w/d`, `invalid` |
| Improvements | `901717038640` | `backlog`, `requirements`, `to do`, `dev in progress`, `code review`, `ready for qa`, `mock testing`, `ready to merge`, `merged`, `blocked`, `done w/d`, `invalid` |
| Releases (folder) | `901711332702` | Listas semanales `Sprint N (fecha - fecha)` con tareas `Release <producto> - vX.Y.Z`: `dev preparation`, `unit test & ci`, `smoke`, `sanity`, `regression`, `ready for release` |
| QA Kanban | `901705382240` | Tickets de automatización (`Test Automation - …`): `Open`, `in progress`, `blocked`, `task completed`, `need escalation`, `Closed` |

Espacio: **NEW GATEWAY IOND** (`90171116803`). Los folders legacy del espacio **no** se usan para el SDLC.

## Herramientas (solo lectura)

| Tool | Uso |
|---|---|
| `getTaskById` | Detalle de un ticket: descripción (con la Matriz de Requerimientos), custom fields, comentarios, historial de estados, subtareas |
| `searchTasks` | Tickets por lista y estado (`list_ids` + `status`), o por texto/ID |
| `getListInfo` | Estados y tags disponibles de una lista |
| `getTimeEntries`, `readDocument` | Tiempo registrado y documentos de ClickUp |

**Prohibido:** crear, editar, mover o comentar tareas. Si una skill necesita un cambio en ClickUp, lo deja como **acción para QA/SM** en su reporte.

## Campos que se leen

| Campo (MCP) | Significado |
|---|---|
| `status`, `list` | Tablero y estado → define la skill (tabla de enrutamiento del `SKILL.md`) |
| `custom_project` | `Iond`, `IONMIND`, `STAGEMIND` o `Gateway` |
| `custom_iond.version`, `custom_ionmind.version`, `custom_stagemind.version`, `custom_g.version` | **Versión objetivo** según el Project (`develop`/`DEVELOPMENT` = sin versión asignada) |
| `custom_iond_subcategory` | Módulo → `knowledge/test-suites/_config/subcategory-map.csv` → L2 y módulos del E2E maestro |
| `custom_type` | `Bug`, `New Feature`, `Improvement`, `Refactor`, `Task` |
| `custom_merge_request` … `_4` | PRs del ticket (`https://github.com/altacrest/<repo>/pull/<n>` → repo `<repo>`) |
| `custom_reviewer_qa`, `custom_dev_reviewer` | QA asignado y revisores de código |
| `custom_qa_points`, `custom_rejection_count` | Esfuerzo de validación e iteraciones de rechazo |
| `priority` | Severidad (`urgent`, `high`, `normal`, `low`) |
| `tags` | Tags SDLC (`po-vobo`, `uat-requerido`, `cambio-alcance`, `escalado-po`, `fuera-de-matriz`, `pilot-feedback`, `bloq-*`, `det-*`, `hotfix`, `fix-forward`, `diferido`) |
| `parent_task_id` | Subtarea (`done w/d` sigue al padre, A-20) |

## Frases fijas que se interpretan (contrato de parsing)

| Comentario | Frase / encabezado |
|---|---|
| C-06 VoBo del PO | Encabezado `✅ VoBo PO — Matriz de Requerimientos v[N]` + tag `po-vobo` |
| C-13 Aprobación de QA | `El resultado de pruebas para este ticket es: APROBADO ✅` |
| C-14 Rechazo de QA | `El resultado de pruebas para este ticket es: RECHAZADO ❌` |
| C-11 Code review | `CODE REVIEW APROBADO ✅` / `CODE REVIEW RECHAZADO ❌` |
| C-29 Go/No-Go | `Decisión:` seguido de `GO`, `CONDITIONAL GO` o `NO-GO` (una sola opción; se ignoran `**` y emoji) |

La Matriz de Requerimientos vigente es la sección `## Matriz de Requerimientos vN` de la **descripción** del ticket con el número de versión más alto; el VoBo vale para esa versión.

## Buenas prácticas

- Procesar los tickets de uno en uno e informar el avance; si el MCP falla en un ticket, continuar y listarlo al final.
- Citar siempre el ticket por su URL `https://app.clickup.com/t/<id>`.
- Filtrar siempre por las listas SDLC (los tags se comparten con folders legacy).
- Plantillas de comentario: `templates/comments/C-xx.md` (generadas desde la fuente canónica §14).
