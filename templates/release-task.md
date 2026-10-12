# Release [producto] - v[X.Y.Z]

> **Plantilla del QA Catalyst = T-04** (fuente canónica §13 · §7.1–§7.7 · `Q-32` a `Q-37`, `Q-47` a `Q-51` · Estándar de QA §6.3).
> **Se guarda en:** `knowledge/releases/[producto]/v[X.Y.Z]/release-task.md` · **Skill:** `skills/release/weekly-plan.md`. La tarea la crea el **SM** (con verificación del Dev) en la lista `Sprint [N] ([fecha inicio] - [fecha fin])` del folder Releases; el catalyst solo prepara el contenido.
> **Datos mínimos de la tarea:** fecha de vencimiento = viernes del Go/No-Go · Project · versión (Iond.Version / Ionmind.Version / Stagemind.Version / G.Version) · relación con cada ticket incluido. Los tickets no se mueven al tablero de Releases: cierran en `merged` en su kanban.

<!-- ===== INICIO: copiar en la descripción de la tarea de Release ===== -->

## Información general
| Campo | Valor |
|---|---|
| Producto / versión | [iond / IonMind / StageMind] v[X.Y.Z] |
| Repos y ramas RC | [repo] → [rama RC] · [repo] → [rama RC] |
| Ambiente de validación | preprod-[...] |
| Tickets incluidos | [N] — relación + versión objetivo |
| Riesgo | Alto / Medio / Bajo — [motivo] |
| Sprint · corte · Go/No-Go | Sprint [N] · lunes [AAAA-MM-DD] 09:00 · viernes [AAAA-MM-DD] 10:00 |
| Releases relacionados | [Release IonMind - vX.Y.Z / Release StageMind - vX.Y.Z] — orden de despliegue StageMind → IonMind → iond · Ninguno |
| Grupo de rotación capa 2 | G[n] (release anterior: G[n-1]) |

## Prerrequisitos (bloqueantes)
- [ ] Repos desplegados en preprod desde el mismo commit RC
- [ ] Migraciones ejecutadas · variables nuevas configuradas
- [ ] Dependencias de otros productos desplegadas (IonMind / StageMind)
- [ ] Datos de prueba cargados · acceso de QA confirmado

## Suites
| Suite | Matriz / ejecución | Resultado |
|---|---|---|
| Smoke maestro (preprod) | smoke-preprod | |
| Sanity (REQ críticos por ticket) | sanity-matrix | |
| Regression capa 1 (riesgo + cross-system) | regression-matrix | |
| E2E maestro capa 2 (automatizado + grupo G[n]) | e2e-run | |
| Smoke maestro (producción, company de prueba) | smoke-prod | |

## Hallazgos
| ID | Severidad | Fase | Decisión (fix-forward / Improvements / diferido) |
|---|---|---|---|

## Go / No-Go
[criterios — ver C-29]

## Despliegue y post-despliegue
[C-30 / C-31]

<!-- ===== FIN: copiar en la descripción de la tarea de Release ===== -->

## Tickets incluidos

| Ticket | Tablero | TYPE | Prioridad | Iond Subcategory | Versión objetivo | REQ críticos | QA Points | Veredicto | Subtareas |
|---|---|---|---|---|---|---|---|---|---|
| #[id] — [título] | Discovery / Improvements | [...] | [...] | [...] | v[X.Y.Z] | [n] | [n] | C-13 [fecha] (+ C-18) | `done w/d` ✅ / [n] pendientes |

**No incluidos:**

| Ticket | Motivo |
|---|---|
| #[id] | Versión objetivo vacía o `DEVELOPMENT`/`develop` (A-11) · sin C-13 · `uat-requerido` sin C-18 · diferido por capacidad (decide el PO) |

> Sin tickets en `ready to merge` para el producto no hay release esa semana (`Q-32`). Límite de lote: ≤ 15 QA Points de sanity por QA y semana.

## Riesgo del release (Estándar de QA §6.3)

| Nivel | Criterio | ¿Aplica? | Efecto en la regresión capa 1 |
|---|---|---|---|
| **Alto** | Toca billing o consumo, autenticación o permisos, el motor de ejecución, contratos de API o migraciones de datos | [ ] | Suite extendida: todas las filas no bloqueadas |
| **Medio** | Varios módulos sin reglas troncales | [ ] | Baseline + filas `Urgent` y `High` de los módulos impactados + cross-system |
| **Bajo** | UI y textos | [ ] | Baseline + filas `Urgent` de los módulos impactados + cross-system |

**Riesgo:** [Alto / Medio / Bajo] — [motivo].

## Parámetros de las suites

| Suite | Parámetros |
|---|---|
| Smoke maestro | SMK-01…SMK-17 (`knowledge/test-suites/smoke-master.md`), sin verificaciones de la versión |
| Sanity | [n] tickets · [n] REQ críticos · interacciones: [tickets con la misma Subcategory] |
| Regression capa 1 | `python -I scripts/e2e_master.py select --layer 1 --subcategories "[lista]" --risk [Alto/Medio/Bajo] --out knowledge/releases/[producto]/v[X.Y.Z]/regression-matrix.csv` (+ `--cross-system sí` si es el primer release del mes) |
| E2E maestro capa 2 | `--layer 2 --group G[n] --exclude .../regression-matrix.csv` |

## Calendario (fuente canónica §7.4)

| Día | Fecha | Actividad | Estado de la tarea | Responsable |
|---|---|---|---|---|
| Viernes previo | [AAAA-MM-DD] | Verificar candidatos y preparar la tarea de Release | — | SM |
| Lunes 09:00 | [AAAA-MM-DD] | Corte · merge a las ramas RC · preprod (C-23) · pipeline (C-24) · smoke por la tarde | `dev preparation` → `unit test & ci` → `smoke` | RM · LD · QA |
| Martes | [AAAA-MM-DD] | Smoke (cierre AM, C-25) · sanity | `smoke` → `sanity` | QA |
| Miércoles | [AAAA-MM-DD] | Sanity (C-26) | `sanity` | QA |
| Jueves | [AAAA-MM-DD] | Regression capa 1 (día) · E2E capa 2 automatizado (noche) · rotación manual G[n] | `regression` | QA |
| Viernes 09:00 | [AAAA-MM-DD] | Consolidado de la capa 2 en el C-27 | `regression` | QA |
| Viernes 10:00 | [AAAA-MM-DD] | Go/No-Go (C-29) · despliegue en la ventana con DevOps (C-30) · smoke en producción ≤ 2 h (C-31) | `ready for release` | PO + LQA + RM · DevOps · QA |

## Go/No-Go — quórum

Reunión obligatoria **PO + LQA + RM** (`Q-35`); sin quórum no hay decisión. Criterios y acta: `templates/go-no-go.md` (C-29). El LQA certifica la calidad y no firma un GO ni un CONDITIONAL GO con un `urgent` abierto.

## Bugs del release (fuente canónica §7.5)

1. `urgent` → **fix-forward** en la rama RC: subtarea de esta tarea con tag `fix-forward` (C-28); decisión ≤ 4 h, fix ≤ 1 día; QA re-ejecuta la verificación afectada.
2. Resto → ticket en Improvements `backlog` con `det-smoke` / `det-sanity` / `det-regression`, previa discusión con PO y LD.
3. Fix-forward fuera de plazo → PO + LD + RM deciden revertir el ticket de la RC (vuelve a `to do` con `diferido`) o NO-GO.

> **Hotfix** (`Q-38`): la tarea se llama `Hotfix [producto] - v[X.Y.Z+1]`, lleva el tag `hotfix` y ejecuta smoke + sanity focalizado. Autorizan PO y LD; ejecuta el RM.
