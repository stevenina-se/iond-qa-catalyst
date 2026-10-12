# Índice de Drafts — QA Automation Plan iond

> **Estado vigente y prioridades:** [`knowledge/test-suites/automation-roadmap.md`](../../../test-suites/automation-roadmap.md) (olas, tickets de QA Kanban y prefijos del E2E maestro) y [`coverage.md`](../../../test-suites/coverage.md). Este índice conserva el detalle de los TC de cada draft; el orden de ejecución de abajo queda reemplazado por las olas de la hoja de ruta.
> **QA-AUTO-TENANT-001** quedó reemplazado por los 19 drafts de [`nodes/`](nodes/README.md).
>
> Generado: 2026-09-15 | Actualizado: 2026-10-10
> Total de tickets: 17
> Total de test cases: ~392

---

## Resumen por Prioridad

| Prioridad | Tickets | Test Cases |
|-----------|---------|------------|
| 🔴 Urgent | 6 | ~258 |
| 🟠 High | 7 | ~84 |
| 🟡 Normal | 2 | ~22 |
| 🔵 Low | 1 | ~29 |
| ⛔ Blocked | 2 | ~23 |
| **Total** | **17** | **~392** |

---

## KC — Keycloak

| Ticket | Módulo | TCs | Prioridad | Assignee | Status |
|--------|--------|-----|-----------|----------|--------|
| [QA-AUTO-KC-001](QA-AUTO-KC-001-keycloak.md) | Login SSO, Registro, Forgot Password | 15 | 🔴 Urgent | Steve | Pending |

---

## ADMIN — Panel de Administración

| Ticket | Módulo | TCs | Prioridad | Assignee | Status |
|--------|--------|-----|-----------|----------|--------|
| [QA-AUTO-ADMIN-001](QA-AUTO-ADMIN-001-dashboard.md) | Dashboard | 4 | 🔵 Low | Mijael | Pending |
| [QA-AUTO-ADMIN-002](QA-AUTO-ADMIN-002-templates.md) | Templates | 6 | 🟡 Normal | Mijael | Pending |
| [QA-AUTO-ADMIN-003](QA-AUTO-ADMIN-003-companies.md) | Companies (Info, Connectors, Boards, Subscription, User) | 11 | 🟡 Normal | Steve | Pending |
| [QA-AUTO-ADMIN-004](QA-AUTO-ADMIN-004-apps.md) | Apps (Legacy, Applications, Grapps, Custom) | 16 | 🟠 High | Steve, Mijael | Pending |
| [QA-AUTO-ADMIN-005](QA-AUTO-ADMIN-005-developers.md) | Developers (Legacy, Applications, Custom, Grapp) | 13 | 🟠 High | Steve | Pending |
| [QA-AUTO-ADMIN-006](QA-AUTO-ADMIN-006-settings-connectors-boards.md) | Settings, Connectors, Boards | 9 | 🟡 Normal / 🔵 Low | Mijael | Pending |
| [QA-AUTO-ADMIN-007](QA-AUTO-ADMIN-007-billing.md) | Billing (Products, Plans, Features) | 13 | 🟠 High | Steve, Mijael | ⛔ Blocked |

---

## TENANT — Panel del Tenant

| Ticket | Módulo | TCs | Prioridad | Assignee | Status |
|--------|--------|-----|-----------|----------|--------|
| [QA-AUTO-TENANT-001](QA-AUTO-TENANT-001-boards-all-tools.md) | Boards — All Tools (Nodos del Canvas) | 32 | 🔴 Urgent | Steve, Mijael | Manual for now |
| [QA-AUTO-TENANT-002](QA-AUTO-TENANT-002-boards-crud-commit.md) | Boards — CRUD, Commit, Export/Import, Flow Pilot | 26 | 🔴 Urgent | Steve | Pending |
| [QA-AUTO-TENANT-003](QA-AUTO-TENANT-003-execution-history.md) | Execution History | 8 | 🟠 High | Mijael | Pending |
| [QA-AUTO-TENANT-004](QA-AUTO-TENANT-004-templates.md) | Templates (Public & Community) | 10 | 🟠 High | Mijael | Pending |
| [QA-AUTO-TENANT-005](QA-AUTO-TENANT-005-webhooks-connections.md) | Webhooks & Connections | 13 | 🟠 High | Mijael | Pending |
| [QA-AUTO-TENANT-006](QA-AUTO-TENANT-006-persistent-data.md) | Persistent Data (Data Store & Data Structure) | 9 | 🟠 High | Mijael | Pending |
| [QA-AUTO-TENANT-007](QA-AUTO-TENANT-007-pdf-templates.md) | PDF Templates (Editor completo) | 21 | 🔴 Urgent | Steve | Pending |
| [QA-AUTO-TENANT-008](QA-AUTO-TENANT-008-app-connectors.md) | App Connectors (List, Create, Draft) | 21 | 🔴 Urgent | Mijael | Pending |
| [QA-AUTO-TENANT-009](QA-AUTO-TENANT-009-config-modules.md) | Credentials, Notifications, Settings, Teams, Account, Language | 25 | 🟠 High | Steve, Mijael | Pending |
| [QA-AUTO-TENANT-010](QA-AUTO-TENANT-010-blocked-modules.md) | Accounts, Developer Apps, Catalog | 10 | 🟠 High | [PENDIENTE] | ⛔ Blocked |
| [QA-AUTO-TENANT-011](QA-AUTO-TENANT-011-nodes-deep.md) | Nodes — 19 tickets individuales en [`nodes/`](nodes/README.md) | 138 | 🔴 Urgent | Steve, Mijael | Pending |

---

## ADMIN GATEWAY — Panel de Gateway

| Ticket | Módulo | TCs | Prioridad | Assignee | Status |
|--------|--------|-----|-----------|----------|--------|
| [QA-AUTO-GW-001](QA-AUTO-GW-001-apps.md) | Apps (Settings, Services, Integrations) | 29 | 🔵 Low | [PENDIENTE] | Manual for now |
| [QA-AUTO-GW-002](QA-AUTO-GW-002-customer.md) | Customer (Marketplace, Grapps E2E) | 14 | 🔴 Urgent | Steve, Mijael | Manual for now |

---

## Orden de Ejecución Recomendado

```
Fase 1 — 🔴 Urgent (Prioridad inmediata)
├── QA-AUTO-KC-001    Keycloak (pre-req para todo)
├── QA-AUTO-TENANT-001  Boards All Tools (core del producto)
├── QA-AUTO-TENANT-002  Boards CRUD/Commit
├── QA-AUTO-TENANT-007  PDF Templates
├── QA-AUTO-TENANT-008  App Connectors
├── QA-AUTO-GW-002    Customer Marketplace E2E
└── QA-AUTO-TENANT-011  Nodes Deep (Config + Ejecución + Edge Cases)

Fase 2 — 🟠 High
├── QA-AUTO-ADMIN-004   Admin Apps (Grapps)
├── QA-AUTO-ADMIN-005   Admin Developers
├── QA-AUTO-TENANT-003  Execution History
├── QA-AUTO-TENANT-004  Templates
├── QA-AUTO-TENANT-005  Webhooks & Connections
├── QA-AUTO-TENANT-006  Persistent Data
└── QA-AUTO-TENANT-009  Config Modules

Fase 3 — 🟡 Normal / 🔵 Low
├── QA-AUTO-ADMIN-001   Admin Dashboard
├── QA-AUTO-ADMIN-002   Admin Templates
├── QA-AUTO-ADMIN-003   Admin Companies
├── QA-AUTO-ADMIN-006   Admin Settings/Connectors/Boards
└── QA-AUTO-GW-001    Gateway Apps

⛔ Backlog (Blocked)
├── QA-AUTO-ADMIN-007   Billing
└── QA-AUTO-TENANT-010  Accounts, DevApps, Catalog
```

---

## Asignación por Persona

### Steve Nina
- QA-AUTO-KC-001 — Keycloak
- QA-AUTO-ADMIN-003 — Companies
- QA-AUTO-ADMIN-005 — Developers
- QA-AUTO-TENANT-002 — Boards CRUD/Commit
- QA-AUTO-TENANT-007 — PDF Templates
- QA-AUTO-TENANT-009 — Config modules (parcial)

### Mijael
- QA-AUTO-ADMIN-001 — Dashboard
- QA-AUTO-ADMIN-002 — Templates
- QA-AUTO-ADMIN-006 — Settings/Connectors/Boards
- QA-AUTO-TENANT-003 — Execution History
- QA-AUTO-TENANT-004 — Templates
- QA-AUTO-TENANT-005 — Webhooks & Connections
- QA-AUTO-TENANT-006 — Persistent Data
- QA-AUTO-TENANT-008 — App Connectors

### Compartidos (Steve + Mijael)
- QA-AUTO-ADMIN-004 — Apps (Grapps)
- QA-AUTO-ADMIN-007 — Billing (Blocked)
- QA-AUTO-TENANT-001 — Boards All Tools
- QA-AUTO-TENANT-011 — Nodes Deep
- QA-AUTO-GW-002 — Customer E2E
