# Skill: release/ingest

> Consolida los datos de los tickets de una versión (MCP de ClickUp, solo lectura) para el resto del pipeline del release: síntesis por ticket, mapa de impacto por módulo y parámetros de las suites.
> Reglas: fuente canónica §7.1 (versión objetivo por Project) y §11. Se ejecuta después del corte (`dev preparation`).

## Cuándo usar

- Lunes, tras el corte y el C-23 del RM (o en cualquier momento para refrescar los datos).
- Frase disparadora: `Preparar datos de release: <producto> vX.Y.Z`.

## Pre-requisitos (gates)

| Check | Si falla |
|---|---|
| Existe `knowledge/releases/<producto>/<versión>/release-task.md` | Ejecutar `release/weekly-plan` |
| MCP de ClickUp responde | PARAR |

## Contexto a cargar

`skills/_shared/clickup.md` (campos y frases fijas), `knowledge/test-suites/_config/subcategory-map.csv`, L2 de los módulos impactados.

## Stage 1 — Planning

Anunciar la versión, la cantidad de tickets de la T-04 y los artefactos a generar (`tickets.md`, `tickets.csv`). Esperar confirmación.

## Stage 2 — Execution

1. **Lista de tickets.** Tomar los tickets de la `release-task.md`. Verificar con `searchTasks` (`status = ["ready to merge", "merged"]`) que la versión objetivo siga coincidiendo; reportar diferencias (tickets agregados o quitados después del plan).
2. **Por ticket** (`getTaskById`, de uno en uno, con avance `[i/N]`):

   | Dato | Fuente |
   |---|---|
   | Tablero, estado, Project, versión objetivo | `list`, `status`, `custom_project`, campo de versión |
   | TYPE, prioridad, Iond Subcategory, tags | `custom_type`, `priority`, `custom_iond_subcategory`, `tags` |
   | Repos y PRs | `custom_merge_request…_4` → `altacrest/<repo>` |
   | QA Points, Rejection_count, Reviewer QA | custom fields |
   | Matriz vigente | Sección `## Matriz de Requerimientos vN` de la descripción (o `knowledge/L3-tickets/<id>/requirements-matrix-v<N>.md`) |
   | REQ críticos | Columna *Crítico* = Sí |
   | Veredicto | C-13 (frase fija) y C-18 si hubo UAT; C-14 previos → iteraciones |
   | Infra | Comentarios C-09: variables, migraciones, endpoints nuevos |
   | Subtareas | Estado de cada subtarea (`done w/d` esperado) |

   - Si el campo de subcategoría está vacío, inferir el módulo por el título (Board/Flow/Nodo → Boards; PDF → PDF Templates; Connector → App Connectors; Webhook → Webhooks; Keycloak/SSO/Login → Auth; Grapp/Catalog/Marketplace → App Stores; Data Store/Storage → Persistent Data; Execution/History → Execution History; Setting/Theme → Settings) y marcarlo como **inferido** para confirmar con QA.
3. **Mapa de impacto.** Por subcategoría → `L2_MODULE`, `E2E_MODULES` y `CROSS_SYSTEM` de `subcategory-map.csv`. Una subcategoría nueva se agrega al mapa (acción para QA) antes de seguir.
4. **Riesgo.** Confirmar o ajustar el riesgo de la T-04 con los datos reales (billing, auth, motor, API, migraciones → Alto).
5. **Alertas para el LQA/SM:** ticket sin C-13, sin matriz o sin REQ críticos; subtareas fuera de `done w/d`; versión inconsistente; infra no documentada.

## Stage 3 — Reporting

Salidas en `knowledge/releases/<producto>/<versión>/`:
- `tickets.md`: resumen (totales por TYPE, subcategoría, repos), una ficha por ticket (datos de la tabla, REQ críticos, veredicto, infra) y el **mapa de impacto** (módulo L2 → tickets → módulos E2E → sistemas cruzados).
- `tickets.csv`: `id,url,tablero,project,version,type,priority,subcategory,l2_module,e2e_modules,cross_system,repos,qa_points,rejection_count,req_criticos,veredicto,alertas`.

Mostrar las alertas y los parámetros listos para las suites:
```
Sanity: [n] tickets · [n] REQ críticos
Regression capa 1: --subcategories "[lista]" --risk [Alto|Medio|Bajo]
Capa 2: --group G[n]
```
Siguiente skill: `release/smoke` (lunes PM).

## Reglas

- Fuente de la lista: la tarea de Release y la **versión objetivo**; no se usa ningún CSV externo de tickets.
- Los custom fields mandan; las inferencias por título se marcan y se confirman.
- Errores del MCP no bloquean: se reportan al final.
- No modificar artefactos de otros releases.
