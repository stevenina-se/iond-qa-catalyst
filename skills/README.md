# Skills — Motor de IA del Catalyst

> Cada skill es una instrucción que un agente de IA sigue para ejecutar una tarea de QA. El agente lee el SKILL.md maestro primero, luego el skill específico.

## Índice de Skills

### Orquestación — Runbooks de flujo completo

| Runbook | Archivo | Track | Descripción |
|---------|---------|-------|-------------|
| Discovery | `discovery-runbook.md` | Discovery | Flujo completo de revisión de prototipo con gates obligatorios |
| Deployment | `deployment-runbook.md` | Deployment | Flujo completo de testing de un ticket con gates obligatorios |

### Code Review QA — Revisión de código desde perspectiva QA

| Skill | Archivo | Track | Descripción |
|-------|---------|-------|-------------|
| Review | `code-review/review.md` | Discovery (opcional) + Deployment (obligatorio) | Bug Hunting + revisión de código + inyección de TCs |

### Sprint Testing — Testing de tickets en sprints

| Skill | Archivo | Track | Descripción |
|-------|---------|-------|-------------|
| Plan | `sprint-testing/plan.md` | Discovery + Deployment | Genera plan de testing desde AC del ticket |
| Test | `sprint-testing/test.md` | Deployment | Ejecuta sesión de testing con evidencia (Manual o Playwright MCP) |
| Report | `sprint-testing/report.md` | Deployment | Genera reporte de QA con veredicto (bugs de code review + testing) |

### Test Docs — Documentación de testing

| Skill | Archivo | Track | Descripción |
|-------|---------|-------|-------------|
| Prioritize | `test-docs/prioritize.md` | Discovery | Analiza riesgos, lee ClickUp, y prioriza qué testear |
| Document | `test-docs/document.md` | Discovery | Paso 0 (reconcilia AC con ClickUp) + Test Matrix con pasos breadcrumb |

### Automation — Automatización E2E (Canal 2)

| Skill | Archivo | Track | Descripción |
|-------|---------|-------|-------------|
| Plan | `automation/plan.md` | Deployment | Decide qué casos automatizar |
| Code | `automation/code.md` | Deployment | Delega a `ionflow-playwright-creator` en bot-test |
| Review | `automation/review.md` | Deployment | Revisa tests generados por IA |

### Regression — Suite de regresión

| Skill | Archivo | Track | Descripción |
|-------|---------|-------|-------------|
| Run | `regression/run.md` | Deployment | Ejecuta suite de regresión |
| Analyze | `regression/analyze.md` | Deployment | Analiza y clasifica fallas |
| Decide | `regression/decide.md` | Deployment | Emite veredicto Go/No-Go |

### Release Management — Gestión de versiones para producción

| Skill | Archivo | Track | Descripción |
|-------|---------|-------|-------------|
| Notes | `release/notes.md` | Release | Genera release notes en 2 versiones: interna y cliente |
| Regression Matrix | `release/regression-matrix.md` | Release | Genera matriz de regresión completa por versión |
| Smoke Matrix | `release/smoke-matrix.md` | Release | Genera matriz de smoke test desde los 9 flujos críticos |
| Bug Hunt | `release/bug-hunt.md` | Release | Bug hunting proactivo por módulo (UI + Backend) |

> **Nota**: Existen skills privadas del Scrum Master (`release/plan.md`, `release/plan-v1.md`)
> que no están en el repositorio (excluidas vía `.gitignore`).
> Los artefactos de release se almacenan en `knowledge/releases/<version>/`.

### Sprint Planning — Planificación de sprint y versión

| Skill | Archivo | Track | Descripción |
|-------|---------|-------|-------------|
| Sprint Board | `sprint-planning/SKILL.md` | Planning | Clasifica tickets, calcula cutoffs, genera sprint board y guiones de seguimiento |

> El entregable principal es `knowledge/releases/{version}/sprint-board.md`.
> Se genera/actualiza cada vez que se ejecuta el skill.

### Knowledge — Gestión de conocimiento

| Skill | Archivo | Track | Descripción |
|-------|---------|-------|-------------|
| Update Module | `knowledge/update-module.md` | Post-release | Retroalimenta L2 después de una release |

---

## Reglas de uso

1. **Siempre leer `SKILL.md` (maestro) antes de ejecutar cualquier skill**
2. **Para Discovery o Deployment → seguir el runbook correspondiente** (no improvisar la secuencia)
3. **Cargar el nivel de conocimiento correcto** antes de cada skill (ver knowledge/README.md)
4. **Respetar los 3 stages**: Planning → Execution → Reporting
5. **El QA Engineer aprueba** antes de pasar de Planning a Execution
6. **Registrar todo** en el L3 del ticket activo
7. **El reporte final es obligatorio** — Nunca terminar sin ejecutar `sprint-testing/report`

---

## Guía de Invocación — Cómo usar cada herramienta

> Referencia rápida con los comandos para invocar cada skill.
> El agente siempre pide confirmación antes de ejecutar.

---

### Orquestación — Runbooks

Los runbooks son flujos completos que orquestan múltiples skills en secuencia.

| Comando | Skill | Descripción |
|---------|-------|-------------|
| `Iniciar Discovery: <TICKET-ID>` | `discovery-runbook.md` | Flujo completo de revisión de prototipo |
| `Iniciar Deployment: <TICKET-ID>` | `deployment-runbook.md` | Flujo completo de testing de un ticket |

**Ejemplos:**
```
Iniciar Discovery: IONF-500
Iniciar Deployment: IONF-362
```

---

### Code Review QA

| Comando | Skill | Descripción |
|---------|-------|-------------|
| _(Se invoca automáticamente dentro de los runbooks)_ | `code-review/review.md` | Bug Hunting + revisión de código |

**Activación:**
- **Discovery**: Solo si el QA Engineer acepta (Paso 3.5 del Discovery Runbook)
- **Deployment**: SIEMPRE antes del testing funcional (Paso 2 del Deployment Runbook)

> No se invoca manualmente — es parte del flujo del runbook.

---

### Sprint Testing

| Comando | Skill | Descripción |
|---------|-------|-------------|
| _(Se invoca dentro del runbook)_ | `sprint-testing/plan.md` | Genera plan de testing desde AC del ticket |
| `Iniciar testing: <TICKET-ID>` | `sprint-testing/test.md` | Ejecuta sesión de testing completa |
| `Generar reporte: <TICKET-ID>` | `sprint-testing/report.md` | Genera reporte final con veredicto |

**Modos de `sprint-testing/test`:**
```
Iniciar testing: IONF-362                     → Modo manual (por defecto)
Iniciar testing: IONF-362 — modo asistido     → Modo Playwright MCP (la IA navega el browser)
```

> `sprint-testing/plan` se ejecuta automáticamente en Discovery (Paso 9) y al inicio de Deployment.
> `sprint-testing/report` es **OBLIGATORIO** después de cada sesión de testing.

---

### Test Docs

| Comando | Skill | Descripción |
|---------|-------|-------------|
| `Priorizar testing: <TICKET-ID>` | `test-docs/prioritize.md` | Analiza riesgos y prioriza qué testear |
| `Documentar testing: <TICKET-ID>` | `test-docs/document.md` | Genera Test Matrix con pasos breadcrumb |

**Ejemplos:**
```
Priorizar testing: IONF-500
Documentar testing: IONF-500
```

> Generalmente se invocan dentro del flujo del Discovery Runbook, pero pueden usarse de forma independiente.

---

### Automation — E2E

| Comando | Skill | Descripción |
|---------|-------|-------------|
| `Planificar automatización: <TICKET-ID>` | `automation/plan.md` | Decide qué casos automatizar |
| `Codificar automatización: <TICKET-ID>` | `automation/code.md` | Delega a `ionflow-playwright-creator` |
| `Revisar automatización: <TICKET-ID>` | `automation/review.md` | Revisa tests generados por IA |

**Ejemplo:**
```
Planificar automatización: IONF-362
```

---

### Regression — Suite de regresión

| Comando | Skill | Descripción |
|---------|-------|-------------|
| `Ejecutar regresión` | `regression/run.md` | Ejecuta suite de regresión E2E |
| `Analizar regresión` | `regression/analyze.md` | Analiza y clasifica fallas de la suite |
| `Decidir regresión` | `regression/decide.md` | Emite veredicto Go/No-Go |

**Ejemplo:**
```
Ejecutar regresión
Analizar regresión
```

---

### Bug Reporter

| Comando | Skill | Descripción |
|---------|-------|-------------|
| `Crea un nuevo ticket:` | `bug-reporter/create.md` | Crea un draft de ticket de bug con evidencia técnica |

**Ejemplos:**
```
Crea un nuevo ticket:
Company > Boards > al duplicar un board, el nombre no cambia

Crea un nuevo ticket:
Admin > Companies > al eliminar una company, los flows quedan huérfanos
```

> Se puede invocar manualmente o desde `release/bug-hunt` cuando el QA aprueba escalar un bug.

---

### Release Management

#### Skills privadas del Scrum Master (no suben al repo)

| Comando | Skill | Descripción |
|---------|-------|-------------|
| `Planificar primer release: v1.0.0` | `release/plan-v1.md` | Consolida todos los tickets históricos del primer release |
| `Planificar release: v[X.Y.Z]` | `release/plan.md` | Planifica releases normales (v1.1.0+) |

**Variantes de `plan-v1`:**
```
Planificar primer release: v1.0.0
Planificar primer release: v1.0.0 — deploy el 3 de julio
Planificar primer release: v1.0.0 — agregar IONF-500, IONF-501
```

**Variantes de `plan`:**
```
Planificar release: v1.1.0
Planificar release: v1.1.0 — deploy el 15 de agosto — sprint del 1 al 15 de agosto
```

**Agregar tickets después de la invocación:**
```
Agregar tickets: IONF-500, IONF-501, IONF-502
```

#### Skills públicas

| Comando | Skill | Descripción |
|---------|-------|-------------|
| `Generar release notes: v[X.Y.Z]` | `release/notes.md` | Genera 2 versiones: interna + cliente |
| `Generar regression matrix: v[X.Y.Z]` | `release/regression-matrix.md` | Matriz de regresión por versión (.md + .csv) |
| `Generar smoke matrix: v[X.Y.Z]` | `release/smoke-matrix.md` | Smoke test desde 9 flujos críticos (.md + .csv) |
| `Bug Hunt: <Módulo>` | `release/bug-hunt.md` | Bug hunting proactivo UI + Backend |

**Ejemplos de release notes:**
```
Generar release notes: v1.0.0
```

**Ejemplos de regression matrix:**
```
Generar regression matrix: v1.0.0
```

**Ejemplos de smoke matrix:**
```
Generar smoke matrix: v1.0.0
Generar smoke matrix: v1.0.0 — entorno: dev-app.ionflow.io
```

**Ejemplos de bug hunt:**
```
Bug Hunt: Boards
Bug Hunt: Connections — métodos de autenticación
Bug Hunt: Data Store — CRUD operations para v1.0.0
```

**Escalar un bug desde bug hunt a ticket:**
```
Crea ticket para BUG-BH-001
```

> **Flujo recomendado**: Plan → Notes → Regression Matrix → Smoke Matrix → Bug Hunt.
> El plan debe ir primero porque genera la `tracking-list.md` que las demás necesitan.

---

### Sprint Planning — Planificación de sprint y versión

| Comando | Skill | Descripción |
|---------|-------|-------------|
| `Planificar sprint` | `sprint-planning/SKILL.md` | Análisis completo del sprint actual con clasificación y cutoffs |
| `Planificar versión: v[X.Y.Z]` | `sprint-planning/SKILL.md` | Planificación enfocada en una versión target |
| `Actualizar sprint board` | `sprint-planning/SKILL.md` | Re-ejecuta el análisis con datos frescos de ClickUp |
| `Generar followups` | `sprint-planning/SKILL.md` | Genera guiones de seguimiento para cada dev |

**Variantes:**
```
Planificar sprint
Planificar sprint — CSV: get_tickets_deployment_4.csv
Planificar versión: v0.1.1
Actualizar sprint board
Generar followups
```

**Entregables generados:**
- `knowledge/releases/{version}/sprint-board.md` — Board completo (cutoffs, tickets, riesgos, priorización, followups)
- `knowledge/releases/{version}/followups/{fecha}-followup.md` — Guiones de seguimiento fechados

> El sprint board incluye:
> - Cutoff dates calculados (DEV, CR, QA, FREEZE, DEADLINE)
> - Tickets clasificados por categoría (regression fixes vs features vs backlog)
> - Riesgo por ticket (🟢 On Track, 🟡 At Risk, 🔴 Off Track)
> - Priorización QA ordenada
> - Carga por developer y bottlenecks
> - Guiones de seguimiento con preguntas específicas por status
> - Proyección de versión

---

### Knowledge — Gestión de conocimiento

| Comando | Skill | Descripción |
|---------|-------|-------------|
| `Actualizar módulo: <Módulo>` | `knowledge/update-module.md` | Retroalimenta L2 después de una release |

**Ejemplo:**
```
Actualizar módulo: Boards
```

---

### Referencia rápida — Todos los comandos

| Comando | Skill |
|---------|-------|
| `Iniciar Discovery: <TICKET-ID>` | `discovery-runbook.md` |
| `Iniciar Deployment: <TICKET-ID>` | `deployment-runbook.md` |
| `Iniciar testing: <TICKET-ID>` | `sprint-testing/test.md` |
| `Generar reporte: <TICKET-ID>` | `sprint-testing/report.md` |
| `Priorizar testing: <TICKET-ID>` | `test-docs/prioritize.md` |
| `Documentar testing: <TICKET-ID>` | `test-docs/document.md` |
| `Planificar automatización: <TICKET-ID>` | `automation/plan.md` |
| `Codificar automatización: <TICKET-ID>` | `automation/code.md` |
| `Revisar automatización: <TICKET-ID>` | `automation/review.md` |
| `Ejecutar regresión` | `regression/run.md` |
| `Analizar regresión` | `regression/analyze.md` |
| `Decidir regresión` | `regression/decide.md` |
| `Crea un nuevo ticket:` | `bug-reporter/create.md` |
| `Planificar primer release: v1.0.0` | `release/plan-v1.md` 🔒 |
| `Planificar release: v[X.Y.Z]` | `release/plan.md` 🔒 |
| `Generar release notes: v[X.Y.Z]` | `release/notes.md` |
| `Generar regression matrix: v[X.Y.Z]` | `release/regression-matrix.md` |
| `Generar smoke matrix: v[X.Y.Z]` | `release/smoke-matrix.md` |
| `Bug Hunt: <Módulo>` | `release/bug-hunt.md` |
| `Planificar sprint` | `sprint-planning/SKILL.md` |
| `Planificar versión: v[X.Y.Z]` | `sprint-planning/SKILL.md` |
| `Actualizar sprint board` | `sprint-planning/SKILL.md` |
| `Generar followups` | `sprint-planning/SKILL.md` |
| `Actualizar módulo: <Módulo>` | `knowledge/update-module.md` |
