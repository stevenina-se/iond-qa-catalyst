# Índice de Tickets — QA Automation: Nodos del Canvas

> Generado: 2026-10-06
> Total de tickets: 19
> Total de test cases: 138
> Referencia técnica: `knowledge/L2-modules/nodes/module.md`

---

## ⚠️ Mapeo Backend ↔ Canvas (CRÍTICO)

| Canvas (UI) | Backend | Package |
|-------------|---------|---------|
| Simple Decision | `ion.action.condition` | `core/actions/condition` |
| Form | `ion.action.mapper` | `core/actions/mapper` |
| Mapper | `ion.action.transformer` | `core/actions/transformer` |
| Multiple Decision | `ion.action.switch` | `core/actions/switchnode` |

---

## Tickets por Nodo

### Triggers

| # | Ticket | Nodo | TCs | Prioridad | Assignee | Status |
|---|--------|------|-----|-----------|----------|--------|
| 1 | [QA-AUTO-NODE-001](QA-AUTO-NODE-001-schedule.md) | Schedule (Trigger Programado) | 5 | 🔴 Urgent | Steve, Mijael | Pending |
| 2 | [QA-AUTO-NODE-002](QA-AUTO-NODE-002-http-request.md) | HTTP Request | 9 | 🔴 Urgent | Steve, Mijael | Pending |
| 3 | [QA-AUTO-NODE-003](QA-AUTO-NODE-003-webhook.md) | Webhook (Trigger) | 5 | 🔴 Urgent | Steve, Mijael | Pending |
| 4 | [QA-AUTO-NODE-004](QA-AUTO-NODE-004-webhook-response.md) | Webhook Response | 4 | 🔴 Urgent | Steve, Mijael | Pending |

### Lógica y Decisión

| # | Ticket | Nodo | TCs | Prioridad | Assignee | Status |
|---|--------|------|-----|-----------|----------|--------|
| 5 | [QA-AUTO-NODE-005](QA-AUTO-NODE-005-simple-decision.md) | Simple Decision (`condition`) | 10 | 🔴 Urgent | Steve, Mijael | Pending |
| 6 | [QA-AUTO-NODE-011](QA-AUTO-NODE-011-multiple-decision.md) | Multiple Decision (`switch`) | 10 | 🔴 Urgent | Steve, Mijael | Pending |

### Transformación y Datos

| # | Ticket | Nodo | TCs | Prioridad | Assignee | Status |
|---|--------|------|-----|-----------|----------|--------|
| 7 | [QA-AUTO-NODE-006](QA-AUTO-NODE-006-form.md) | Form (`mapper`) | 5 | 🔴 Urgent | Steve, Mijael | Pending |
| 8 | [QA-AUTO-NODE-007](QA-AUTO-NODE-007-mapper.md) | Mapper (`transformer`) | 6 | 🔴 Urgent | Steve, Mijael | Pending |
| 9 | [QA-AUTO-NODE-008](QA-AUTO-NODE-008-aggregate.md) | Aggregate | 5 | 🔴 Urgent | Steve, Mijael | Pending |
| 10 | [QA-AUTO-NODE-009](QA-AUTO-NODE-009-iterator.md) | Iterator | 6 | 🔴 Urgent | Steve, Mijael | Pending |
| 11 | [QA-AUTO-NODE-010](QA-AUTO-NODE-010-timer.md) | Timer | 6 | 🔴 Urgent | Steve, Mijael | Pending |
| 12 | [QA-AUTO-NODE-012](QA-AUTO-NODE-012-code.md) | Code (JS/Python + FlowPilot) | 14 | 🔴 Urgent | Steve, Mijael | Pending |

### Component-Flows

| # | Ticket | Nodo | TCs | Prioridad | Assignee | Status |
|---|--------|------|-----|-----------|----------|--------|
| 13 | [QA-AUTO-NODE-013](QA-AUTO-NODE-013-call-component-flow.md) | Call Component-Flow | 6 | 🔴 Urgent | Steve, Mijael | Pending |
| 14 | [QA-AUTO-NODE-014](QA-AUTO-NODE-014-on-call-component-flow.md) | On Call Component-Flow Trigger | 3 | 🔴 Urgent | Steve, Mijael | Pending |

### IA, Storage e Integraciones

| # | Ticket | Nodo | TCs | Prioridad | Assignee | Status |
|---|--------|------|-----|-----------|----------|--------|
| 15 | [QA-AUTO-NODE-015](QA-AUTO-NODE-015-agent.md) | Agent (IA) | 7 | 🔴 Urgent | Steve, Mijael | Pending |
| 16 | [QA-AUTO-NODE-016](QA-AUTO-NODE-016-persistent-data.md) | Persistent Data (8 operaciones) | 15 | 🔴 Urgent | Steve, Mijael | Pending |
| 17 | [QA-AUTO-NODE-017](QA-AUTO-NODE-017-ion-pdf.md) | ION PDF (Edit, Add, Map, Build) | 8 | 🔴 Urgent | Steve, Mijael | Pending |
| 18 | [QA-AUTO-NODE-018](QA-AUTO-NODE-018-tenant-app.md) | Tenant App (App Nodes + IonMind) | 6 | 🔴 Urgent | Steve, Mijael | Pending |

### General

| # | Ticket | Nodo | TCs | Prioridad | Assignee | Status |
|---|--------|------|-----|-----------|----------|--------|
| 19 | [QA-AUTO-NODE-019](QA-AUTO-NODE-019-general-behavior.md) | Comportamiento General de Nodos | 8 | 🔴 Urgent | Steve, Mijael | Pending |

---

## Resumen

| Grupo | Tickets | TCs |
|-------|---------|-----|
| Triggers | 4 | 23 |
| Lógica y Decisión | 2 | 20 |
| Transformación y Datos | 6 | 42 |
| Component-Flows | 2 | 9 |
| IA, Storage e Integraciones | 4 | 36 |
| General | 1 | 8 |
| **Total** | **19** | **138** |

---

## Orden de Ejecución Recomendado

```
Fase 1 — Core (sin dependencias externas)
├── NODE-019  General Behavior (valida reglas transversales)
├── NODE-005  Simple Decision (prioritario para sprint)
├── NODE-006  Form (prioritario para sprint)
├── NODE-009  Iterator
├── NODE-008  Aggregate
├── NODE-010  Timer
└── NODE-007  Mapper

Fase 2 — Triggers y HTTP
├── NODE-001  Schedule
├── NODE-002  HTTP Request
├── NODE-003  Webhook
└── NODE-004  Webhook Response

Fase 3 — Lógica avanzada
├── NODE-011  Multiple Decision
├── NODE-012  Code (requiere Code Runner)
├── NODE-013  Call Component-Flow
└── NODE-014  On Call Component-Flow

Fase 4 — Dependencias externas
├── NODE-015  Agent (requiere LLM credentials)
├── NODE-016  Persistent Data (requiere Data Store)
├── NODE-017  ION PDF (requiere PDF Templates)
└── NODE-018  Tenant App (requiere Connections + App Connectors)
```

---

## Dependencias Externas por Ticket

| Ticket | Requiere |
|--------|----------|
| NODE-001 a NODE-011 | Solo board de prueba |
| NODE-012 | Code Runner (`CODE_RUNNER_URL`) + IonMind (para FlowPilot) |
| NODE-013, NODE-014 | Component-Flow existente |
| NODE-015 | Credenciales LLM (módulo Credentials) |
| NODE-016 | Data Store + Data Structure |
| NODE-017 | PDF Template existente |
| NODE-018 | App Connector + Conexión activa + IonMind |
