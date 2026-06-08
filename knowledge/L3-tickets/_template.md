# Ticket: [TICKET-ID] — [Título del ticket]

> Sesión de testing iniciada: [fecha]
> Módulo: [nombre del módulo]
> QA Engineer: [nombre]

## Contexto del Ticket

### Acceptance Criteria
> Pegar aquí los AC del ticket (desde ClickUp o manualmente)

- [ ] AC 1: ...
- [ ] AC 2: ...
- [ ] AC 3: ...

### Descripción
> Resumen del ticket y su propósito.

### Decisiones del equipo
> Decisiones relevantes tomadas durante Discovery o refinamiento.

- ...

### Módulo afectado
- Módulo principal: `[nombre]`
- Módulos relacionados: `[otros módulos si aplica]`

---

## Plan de Testing

> Generado por `sprint-testing/plan` — aprobado por QA Engineer

### Risk Triage
| Área | Riesgo | Prioridad |
|------|--------|-----------|
| ... | ... | 🔴/🟠/🟡 |

### Casos de Testing
| ID | Tipo | Caso | AC vinculado | Prioridad | Estado |
|----|------|------|-------------|-----------|--------|
| TC-001 | Happy Path | ... | AC 1 | 🔴 | ⬜ Pendiente |
| TC-002 | Edge Case | ... | AC 1 | 🟠 | ⬜ Pendiente |
| TC-003 | Negativo | ... | AC 2 | 🟡 | ⬜ Pendiente |

---

## Ejecución

### Smoke Tests
| Test | Resultado | Evidencia |
|------|-----------|-----------|
| Feature existe y carga | ⬜ | |

### UI Testing
| TC-ID | Resultado | Notas | Evidencia |
|-------|-----------|-------|-----------|
| TC-001 | ⬜ | | |

### API Testing
| TC-ID | Endpoint | Resultado | Response |
|-------|----------|-----------|----------|
| | | ⬜ | |

### DB Evidence
| Query | Resultado esperado | Resultado real | Match |
|-------|-------------------|----------------|-------|
| `SELECT ...` | ... | *(pegar de DBeaver)* | ⬜ |

---

## Bugs Encontrados

| Bug ID | Severidad | Descripción | TC relacionado | Evidencia |
|--------|-----------|-------------|---------------|-----------|
| BUG-001 | 🔴 | ... | TC-XXX | link |

---

## Veredicto

> **⏳ Pendiente** — Esperando ejecución completa

| Campo | Valor |
|-------|-------|
| Veredicto | ⏳ Pendiente / ✅ Approved / ❌ Rejected |
| Aprobado por | [QA Engineer] |
| Fecha | [fecha] |
| Observaciones | ... |

---

## Transcript de la Sesión

> Log cronológico de acciones tomadas durante la sesión.

| Timestamp | Acción | Detalle |
|-----------|--------|---------|
| | Session Start | Cargado L1 + L2 de [módulo] |
| | Planning | Risk triage completado |
| | Execution | ... |
| | Reporting | ... |
