# Hoja de ruta de automatización — IOND

> **Responsable:** LQA. Se revisa en cada retro y cuando cambia el estado de un ticket de automatización (lista **QA Kanban** `901705382240`).
> **Principio (`Q-40`, `Q-50`):** primero lo que más se repite y más protege el release: **smoke → baseline crítico → TC estables de sanity → resto del E2E maestro**. La cobertura vigente está en [`coverage.md`](coverage.md); el detalle por fila, en [`e2e-master.csv`](e2e-master.csv).
> **Alcance del catalyst (`Q-54`):** el catalyst prioriza, mapea y genera comandos; **no modifica bot-test**. Los cambios en bot-test los hace su responsable con la skill `e2e-playwright-creator` del propio repositorio.

## Situación de partida (2026-10-10)

| Indicador | Valor |
|---|---|
| Filas del E2E maestro | 250 |
| Con spec en bot-test | 86 (34 %) |
| Ejecutables hoy (rama `test/ionflow-tenant-e2e`, PR abierto) | 71 (28 %) |
| Specs en `main` que no cargan | 15 filas (`Rota`) |
| Smoke maestro automatizable hoy | 5 de 17 verificaciones con test existente (`TC-DASH-01`, `TC-NOTIF-01`, `TC-PDF-21`, `TC-BOARD-FP-01/02`) |

## Ola 0 — Requisitos de bot-test (AV-11)

Condiciones para que las suites corran de forma confiable. Las entrega el LQA al responsable de bot-test; **no las ejecuta el catalyst**.

| # | Requisito | Por qué |
|---|---|---|
| 0.1 | Integrar el PR de la rama `test/ionflow-tenant-e2e` | Las 71 filas ejecutables viven solo en esa rama |
| 0.2 | Corregir los imports de las specs de `main` (Admin, login, app-connectors, execution-history, webhooks) y el `super()` de `CompanyDetailPage` | 15 filas del maestro están en estado `Rota` |
| 0.3 | Excluir las specs exploratorias (`scratch/`) de la corrida completa | Hoy rompen la carga de toda la suite |
| 0.4 | Perfiles de variables por ambiente (preprod y company de prueba) y variables `IONFLOW_ADMIN_*` | El smoke corre en preprod y en producción |
| 0.5 | Etiquetas de suite: `@smoke` en los tests de SMK y `@prod-safe` en los que pueden correr en producción | Hoy la suite se arma por IDs (`-g`) |
| 0.6 | Cuarentena visible de los `expect.soft` sobre bugs conocidos (`@bug` o `test.fail()`) | Evita rojos permanentes en la capa 2 |
| 0.7 | Reescribir las specs destructivas que operan sobre "el primer registro" (webhooks, execution-history, app-connectors) para que creen y limpien sus propios datos | No pueden correr en ambientes compartidos |

## Ola 1 — Smoke maestro al 100 %

| SMK | Estado | Acción |
|---|---|---|
| SMK-02, SMK-11, SMK-16 | Test existente en la rama E2E | Etiquetar `@smoke` (Ola 0.5) |
| SMK-09 | `TC-PDF-21` existe; necesita la plantilla fija de la company de prueba | Precargar `autobot-smoke-template` (AV-09) |
| SMK-01, SMK-13 | Spec existente rota | Ola 0.2 |
| SMK-03, SMK-04, SMK-05 | Nuevo: board de smoke de punta a punta (crear → ejecutar en test → ejecutar en producción → historial → limpiar) | Nuevo ticket propuesto **QA-AUTO-SMOKE-001** |
| SMK-06, 07, 08, 10, 12 | Nuevo: listados de solo lectura | Incluir en QA-AUTO-SMOKE-001 |
| SMK-15 | Nuevo: health de servicios (prueba de API) | Incluir en QA-AUTO-SMOKE-001 cuando el LD defina los endpoints |
| SMK-14 | Nuevo (Gateway) | Ola 3 |
| SMK-17 | Pendiente de definición (AV-12) | — |

**Meta:** smoke de iond 100 % automatizado y ejecutable en preprod y en producción.

## Ola 2 — Baseline crítico de regresión

Filas con `BASELINE = sí` del maestro (25). Prioridad dentro de la ola: ejecución de boards por trigger (Scheduler ya automatizado; Webhook y HTTP Request pendientes), historial de ejecuciones, App Connectors, conexiones y billing.

| Bloque | Ticket QA Kanban | Estado |
|---|---|---|
| Nodos de ejecución (Webhook, HTTP Request) | 86e3ku7cw, 86e3ku75b | Open |
| Execution History (Details, View Logs) | 86e39pgbr | Open — la spec de `main` está rota (Ola 0.2) |
| App Connectors (Manual Connector, Base Edit, Nodes Add) | 86e39pht7 | Open — spec de `main` rota y parcial |
| Connections (Check, Reauthorize) | 86e39pgy4 | Open |
| Billing (Assign Plan, Create Plan, Assign Feature) | 86e39kzyb, 86e39kx9v | Open — la hoja lo marca `Blocked`: confirmar con el LD si sigue bloqueado |

## Ola 3 — Resto del E2E maestro

Por prioridad de la hoja: nodos del canvas (tickets `86e3ku7xx`–`86e3ku985`), Templates del tenant, App Connectors completo, Admin (Apps, Developers, Templates, Settings), Admin Gateway. Los TC estables de `sanity` que se repiten en varios releases pasan a esta ola.

## Tickets de QA Kanban ↔ drafts ↔ E2E maestro

| Ticket | Nombre | Estado ClickUp | Draft | Prefijo E2E | Observación |
|---|---|---|---|---|---|
| 86e39m0ym | Keycloak: Login, Registro y Recuperación | in progress | QA-AUTO-KC-001 | `E2E-KC-AUT` | Login existe pero rota (Ola 0.2) |
| 86e2r4nqx | Fix Login and Register | in progress | QA-AUTO-KC-001 | `E2E-KC-AUT` | Se solapa con 86e39m0ym: unificar |
| 86e39pg62 | Tenant: Boards - CRUD | in progress | QA-AUTO-TENANT-002 | `E2E-TEN-BRD` | 22 filas en el PR; cerrar al integrar |
| 86e39phnx | Tenant: PDF Templates | in progress | QA-AUTO-TENANT-007 | `E2E-TEN-PDF` | 19/19 filas en el PR; cerrar al integrar |
| 86e39phay | Tenant: Persistent Data | in progress | QA-AUTO-TENANT-006 | `E2E-TEN-PDS` | 7/7 filas en el PR; cerrar al integrar |
| 86e39phvu | Tenant: Credentials, Notifications, Settings, Teams, Account, Language | Open | QA-AUTO-TENANT-009 | `E2E-TEN-CRD/NTF/SET/TEA/PRF/LNG` | Las suites ya están en el PR: actualizar el estado del ticket |
| 86e3ku71p | Tenant: Nodo Schedule | Open | nodes/QA-AUTO-NODE-001 | `E2E-TEN-BRD` (Scheduler) | Suite ya en el PR: actualizar el estado del ticket |
| 86e3ku75b … 86e3ku8qj | Tenant: Nodos (HTTP Request … Agent) | Open | nodes/QA-AUTO-NODE-002 a 015 | `E2E-TEN-BRD` (All Tools) | Ola 2 (Webhook, HTTP Request) y Ola 3 |
| 86e3ku8uw | Tenant: Persistent Data (nodo Storage) | Open | nodes/QA-AUTO-NODE-016 | `E2E-TEN-BRD` (Storage) | Ola 3 |
| 86e3ku8xw | Tenant: PDF Template (nodo ION PDF) | Open | nodes/QA-AUTO-NODE-017 | `E2E-TEN-BRD` (ION PDF) | Ola 3 |
| 86e3ku985 | Tenant: Custom App | Open | nodes/QA-AUTO-NODE-018 | `E2E-TEN-BRD` (Tenant App) | Ola 3 |
| 86e3ku95e | Tenant: General Behavior | Open | nodes/QA-AUTO-NODE-019 | — | Sin fila en la hoja: proponer la fila "Boards › Create Board › All Tools › General Behavior" |
| 86e39pgbr | Tenant: Execution History | Open | QA-AUTO-TENANT-003 | `E2E-TEN-EXH` | Ola 2 |
| 86e39pgn7 | Tenant: Templates (Public & Community) | Open | QA-AUTO-TENANT-004 | `E2E-TEN-TPL` | Ola 3 |
| 86e39pgy4 | Tenant: Webhooks & Connections | Open | QA-AUTO-TENANT-005 | `E2E-TEN-WHK`, `E2E-TEN-CNX` | Ola 2 (Connections) y Ola 3 |
| 86e39pht7 | Tenant: App Connectors | Open | QA-AUTO-TENANT-008 | `E2E-TEN-APC` | Ola 2 |
| 86e39kw8h | Admin: Templates | Open | QA-AUTO-ADMIN-002 | `E2E-ADM-TPL` | Ola 3 |
| 86e39kx9v | Admin: Companies | Open | QA-AUTO-ADMIN-003 | `E2E-ADM-CMP` | Ola 0.2 (specs rotas) y Ola 2 (Subscription) |
| 86e39ky6f | Admin: Apps | Open | QA-AUTO-ADMIN-004 | `E2E-ADM-APP` | Ola 3 |
| 86e39kym1 | Admin: Developer Apps | Open | QA-AUTO-ADMIN-005 | `E2E-ADM-DEV` | Ola 3 |
| 86e39kz87 | Admin: Settings | Open | QA-AUTO-ADMIN-006 | `E2E-ADM-SET` | Ola 0.2 (spec rota) |
| 86e39kzyb | Admin: Billing | Open | QA-AUTO-ADMIN-007 | `E2E-ADM-BIL` | Ola 2; confirmar si sigue bloqueado |
| — | Sin ticket | — | QA-AUTO-ADMIN-001, ADMIN-006 (Connectors/Boards list), GW-001, GW-002, TENANT-010 | `E2E-ADM-DSH`, `E2E-ADM-APC`, `E2E-ADM-BRD`, `E2E-GTW-*`, `E2E-TEN-ACC/DVA/CAT` | Crear tickets cuando entren en una ola |
| *(propuesto)* | QA-AUTO-SMOKE-001 — Smoke maestro automatizado | — | — | SMK-03…SMK-08, SMK-10, SMK-12, SMK-15 | Ola 1 |

## Depuración de los drafts (`knowledge/L3-tickets/drafts/automation/`)

- **QA-AUTO-TENANT-001** (All Tools, 32 TC) queda **reemplazado** por `nodes/` (19 tickets, 138 TC), que es la versión vigente y coincide con los tickets de QA Kanban.
- **QA-AUTO-TENANT-003** y **QA-AUTO-ADMIN-007** marcan *View Execution Logs* y *Billing* como bloqueados hasta la v0.2.0 (release beta en curso, `knowledge/releases/iond/v0.2.0/`). Al desplegarse la beta, confirmar con el LD y actualizar la hoja y las olas.
- Cada draft se vincula al maestro por su prefijo E2E (tabla anterior). Los TC del draft son el detalle de implementación; **el alcance y el estado se gobiernan desde la hoja y el maestro**.
- Los tickets nuevos (por ejemplo, QA-AUTO-SMOKE-001) se proponen como draft en esa carpeta. El LQA los crea en ClickUp; el catalyst no escribe en ClickUp.

## Seguimiento

- Indicadores en el reporte semanal (`skills/metrics/weekly.md`): % del maestro automatizado y ejecutable, % del smoke automatizado, % del baseline automatizado, tests en cuarentena.
- Cada cambio de estado de una suite se refleja en `_config/rules.csv` y se reimporta el maestro.
