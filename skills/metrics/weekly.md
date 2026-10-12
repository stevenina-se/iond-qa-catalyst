# Skill: metrics/weekly

> Reporte semanal de métricas del SDLC para el **Scrum Master**, el **LQA**, el **PO** y el **LD/RM**, según el diccionario del documento 07 (M-01 a M-47). **Solo lectura**. Complementa los dashboards nativos de ClickUp con lo que ClickUp no calcula (Go/No-Go, suites del release, cobertura de automatización).

## Cuándo usar

- Viernes, después del Go/No-Go (o el lunes antes de la planificación).
- Frase disparadora: `Generar métricas semanales` (opcional: `semana AAAA-WNN`).

## Pre-requisitos (gates)

| Check | Si falla |
|---|---|
| MCP de ClickUp responde | PARAR |
| Artefactos del release de la semana en `knowledge/releases/<producto>/<versión>/` | Reportar las métricas de release como "sin datos" |

## Contexto a cargar

`docs/sdlc-iond/src/07-dashboards-y-metricas.md` §2 (definiciones, fuentes y metas), `knowledge/test-suites/coverage.md`, el reporte de la semana anterior en `knowledge/dashboards/`.

## Stage 1 — Planning

Anunciar la semana, los productos y los bloques de métricas que se pueden calcular con los datos disponibles. Esperar confirmación.

## Stage 2 — Execution

| Bloque | Métricas | Fuente |
|---|---|---|
| Flujo | M-03 (Time in Status de `requirements`, `ready for qa`, `code review`, `blocked`), M-04 throughput, M-06 WIP, M-08 aging, M-09 bloqueados | MCP: estados, historial de estados, tags `bloq-*` |
| Calidad | M-11 FPY, M-12 rechazos, M-13 detección por fase (`det-*`), M-14 escapes (`det-prod`) | MCP: Rejection_count, tags `det-*`, TYPE, prioridad |
| Requerimientos | M-17/M-18 VoBo, M-19 `cambio-alcance`, M-20 `fuera-de-matriz`, M-22 `escalado-po` | MCP: tags y comentarios C-05/C-06 |
| Capacidad | M-26 carga QA, M-27 QA Points completados, M-28/M-29 code review | MCP: QA Points, Reviewer QA, Dev Reviewer |
| Release | M-30 tamaño, M-31 listos sin versión, M-32 Go/No-Go, M-34 fix-forward, M-35 diferidos | `go-no-go.md`, `tickets.md`, MCP |
| Suites y automatización | M-16 y M-44 cobertura del E2E maestro (automatizada y ejecutable), M-43 paso del smoke (preprod y producción), M-45 avance de la rotación, M-46 tests en cuarentena, M-47 escapes por suite | `coverage.md`, `smoke-*.md`, `e2e-run.md`, `regression-matrix.md` |

- Comparar con la semana anterior y con la meta de cada métrica (doc 07). Marcar 🟢 en meta · 🟠 cerca · 🔴 fuera.
- Calcular solo lo que tiene datos; lo demás se reporta como "sin datos" con el motivo (no se estima).

## Stage 3 — Reporting

- `knowledge/dashboards/metrics-<AAAA>-W<NN>.md`: tablero por audiencia (PO, LD/RM, LQA, SM, stakeholders) con valor, meta, tendencia y lectura de 1 línea; top 3 riesgos y acciones sugeridas.
- Resumen corto para la retro o el canal del equipo, si el SM lo pide.

## Reglas

- Las métricas son del **sistema**, no de las personas: nunca rankings individuales (doc 07 §1.2).
- Los QA Points se usan para capacidad, no para evaluar desempeño (`Q-26`).
- Una métrica sin fuente confiable se marca como tal; no se completa con supuestos.
