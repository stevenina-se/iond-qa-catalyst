# Ticket Memory: 86e1wfhcq — API REST de workspace/company de IOND (FASE 2)

> Sesión de Discovery iniciada: 2026-10-08
> Módulo principal: Auth (companies, users, permisos) + API
> QA Engineer: Steve Nina

## Datos del Ticket

| Campo | Valor |
|-------|-------|
| ID ClickUp | `86e1wfhcq` |
| ID Legible | IONF-1085 |
| URL | https://app.clickup.com/t/86e1wfhcq |
| Nombre | API REST de workspace/company de IOND (FASE 2) |
| Status | `test matrix` |
| Prioridad | High |
| Creador | Marcel Herrera Rendón |
| Asignado | Rodolfo Merlo Ali |
| Lista | Discovery (901717038641) |
| Tags | iond-core |
| Tipo | New Feature |
| Subcategoría | API |
| Proyecto | Iond |
| Branch | IONF-1085 |
| Progreso | 8.33% |

## Subtareas (child tasks)

86e30115a, 86e3011aq, 86e3011cy, 86e3011f2, 86e3011gr, 86e3011j1, 86e3011kh, 86e3011n0, 86e3011nj, 86e3011p8, 86e3011q6, 86e3011r5

## Subtareas funcionales (Fase 2)

| ID | Descripción |
|----|-------------|
| IONF-1279 | PAT y autorización de usuario para la API workspace |
| IONF-1284 | Connections de company y catálogo de App Connectors instalados |
| IONF-1285 | Boards de company: list, get y execute |
| IONF-1286 | CompanyExecution: list, get, logs y controles |
| IONF-1287 | CRUD de webhooks y schedules de company |
| IONF-1288 | Authoring y publicación de App Connectors |
| IONF-1291 | Persistent Data: data stores, structures y content |
| IONF-1292 | PDF Templates de company |

## Tickets excluidos/diferidos

| ID | Descripción | Razón |
|----|-------------|-------|
| IONF-1289 | IonMind workspace | Diferido a sucesor |
| IONF-1293 | Templates de company | Excluido por decisión Tech Lead |
| IONF-1294 → IONF-1416 | OpenAPI, generación, publicación | Trasladado a entrega independiente |
| IONF-1295 | QA como tarea independiente | Invalidada — QA se ejecuta por ticket |

## Repos y PRs

| Repo | Rama | PR |
|------|------|----|
| gateway-ion | `IONF-1085` | ion_gateway_ion#77 |
| flow_binaries | `IONF-1085` | ion_flow_binaries#58 |
| gateway | `IONF-1085` | ion_gateway#92 |
| webcomponents | N/A | N/A |

## Fase del Proceso

- [x] Discovery — PASO 1: Inicialización
- [x] Discovery — PASO 2: Reconciliación de AC
- [x] Discovery — PASO 3: Análisis de Riesgo
- [x] Discovery — PASO 4: Consolidación de AC (95 ACs activos, 8 diferidos)
- [x] Discovery — PASO 5: Test Matrix (87 TCs + CSV)
- [x] Discovery — PASO 6: Plan de Testing (8 fases, ~12.5h estimadas)

## Módulos Afectados

| Módulo | Rol | L2 cargado |
|--------|-----|------------|
| Auth (companies, users, permisos) | Principal | ✅ |
| Accounts | Secundario | ✅ |
| Boards | Impactado | ⬜ |
| Connections | Impactado | ⬜ |
| Webhooks | Impactado | ⬜ |
| Executions | Impactado | ⬜ |
| Data Store | Impactado | ⬜ |
| PDF Templates | Impactado | ⬜ |
| Billing | Potencialmente impactado | ⬜ |

## Dependencias

| Ticket | Relación |
|--------|----------|
| IONF-1080 | API Fase 1 (regresión) |
| IONF-1170/IONF-1248 | Executions (replay y lifecycle) |
| IONF-1277 | Servidor MCP (consumidor futuro) |
| IONF-1306 | Backlog posterior |
