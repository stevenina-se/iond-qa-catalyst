# Ticket: 86e22fzvx — Boards — Simple Decision compara valores numéricos como strings, resultado incorrecto

> Sesión de Discovery iniciada: 2026-07-14
> Módulo: Nodes / Simple Decision (Canvas) — `ion.action.condition` (Backend)
> QA Engineer: Steve Nina

## Contexto del Ticket

### Descripción
Bug: El nodo Simple Decision evalúa comparaciones numéricas como strings. Por ejemplo, `2 > 12` devuelve `true` porque lexicográficamente `"2" > "1"`. Los operadores `is_greater`, `is_less`, etc. no realizaban conversión de tipo para valores numéricos.

### Root Cause (identificado por Developer)
El nodo `condition` trataba todos los operandos como strings y usaba `expr-lang/expr` con comparación de strings. No había lógica de tipo.

### Solución del Developer (branch IONF-1128)

**Repos afectados**: `flow_binaries` (PR #13) + `webcomponents-flow` (PR #7)

| Repo | Cambio Principal |
|------|-----------------|
| `flow_binaries` | Nuevo package `core/actions/ruleeval/` extraído de switchnode. `condition.go` rutea ítems con campo `type` a `ruleeval.Evaluate()`. Legacy path mantiene backward compatibility. |
| `webcomponents-flow` | `ConditionItem` con selector de tipo, operadores dinámicos por tipo, validación inline, constantes compartidas con Switch. |

### Módulo afectado
- Módulo principal: `Nodes / Simple Decision` (`ion.action.condition`)
- Módulos relacionados: `Boards` (ejecución de flows), `Executions` (historial), `Multiple Decision` (Switch — comparte `ruleeval`)

### Datos del entorno de testing
- Rol: Company User con permiso `UPDATE_BOARD`
- Entorno: Staging (dev-app.ionflow.io)
- Branch `IONF-1128` → base `DEVELOPMENT`
- PRs: flow_binaries PR #13, webcomponents-flow PR #7
- Deployed: ✅ confirmado por Rodolfo (2026-07-14 09:59)

---

## Transcript de la Sesión

| Timestamp | Acción | Detalle |
|-----------|--------|---------|
| 2026-07-14 10:13 | Session Start | Contexto cargado: L1 completo + L2 nodes + ticket de ClickUp |
| 2026-07-14 10:13 | Discovery | AC reconciliados con spec del Developer (sin divergencias) |
| 2026-07-14 10:13 | Discovery | risk-triage.md generado |
| 2026-07-14 10:13 | Discovery | ac-consolidated.md generado |
| 2026-07-14 10:13 | Discovery | test-matrix.md + test-matrix.csv generados |
| 2026-07-14 10:13 | Discovery | test-plan.md generado |
