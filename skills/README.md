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
