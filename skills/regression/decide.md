# Skill: regression/decide

> Emite la sugerencia de veredicto Go/No-Go para release basado en el análisis de regresión. El QA Engineer toma la decisión final.

## Cuándo usar este skill

- **Pre-release**: Después de que `regression/analyze` clasifique los fallos
- **Gate de calidad**: Cuando el equipo necesita decidir si hacer deploy

## Pre-requisitos

- ✅ Análisis de regresión completado (`regression/analyze`)
- ✅ `knowledge/L1-project/test-priorities.md` — Criticidad de módulos
- ✅ Lista de tickets incluidos en el release

---

## Instrucciones de Ejecución

### Stage 1 — PLANNING

Reporta al QA Engineer:
1. Resumen del análisis de regresión
2. Los tickets incluidos en el release
3. Los módulos afectados y su criticidad

### Stage 2 — EXECUTION

#### Paso 1: Evaluar criterios de Go/No-Go

| Criterio | Umbral | Resultado actual | Cumple |
|----------|--------|-----------------|--------|
| Tasa de pass global | ≥95% | [N]% | ✅/❌ |
| Bugs reales en módulos 🔴 Críticos | 0 | [N] | ✅/❌ |
| Bugs reales en módulos 🟠 Altos | ≤1 | [N] | ✅/❌ |
| Tests flaky nuevos | ≤3 | [N] | ✅/❌ |
| Módulos sin cobertura E2E que cambiaron | 0 idealmente | [N] | ⚠️ |

#### Paso 2: Risk assessment por ticket

Para cada ticket incluido en el release:

| Ticket | Módulo | Tests E2E | Regresión OK | Riesgo |
|--------|--------|-----------|-------------|--------|
| TASK-001 | flows | ✅ 5 tests | ✅ Todos pasan | 🟢 Bajo |
| TASK-002 | auth | ✅ 3 tests | ⚠️ 1 flaky | 🟡 Medio |
| TASK-003 | connectors | ❌ Sin tests | N/A | 🟠 Alto (sin cobertura) |

#### Paso 3: Generar veredicto sugerido

**Caso GO:**
```
SUGERENCIA: 🟢 GO — Proceder con el release

Justificación:
- Tasa de pass: [N]% (≥95%)
- 0 bugs reales en módulos críticos
- Todos los tickets del release tienen cobertura
- [N] tests flaky conocidos (no bloqueantes)

Condiciones:
- Monitorear [módulo] post-deploy por [razón]
```

**Caso NO-GO:**
```
SUGERENCIA: 🔴 NO-GO — No proceder con el release

Justificación:
- [N] bugs reales en módulo [crítico]
- Tasa de pass: [N]% (< 95%)
- Ticket [ID] tiene fallos bloqueantes

Acción requerida:
- Corregir BUG-[ID] antes del release
- Re-ejecutar regresión después del fix
```

**Caso GO CON CONDICIONES:**
```
SUGERENCIA: 🟡 GO CON CONDICIONES

Justificación:
- Tasa de pass: [N]% (≥95%)
- [N] bugs no bloqueantes encontrados
- Ticket [ID] sin cobertura E2E pero testeado manualmente

Condiciones:
- Crear tests E2E para [TICKET-ID] post-release
- Monitorear [módulo] las primeras 24h
- Hotfix preparado para [riesgo identificado]
```

> ⚠️ **ESTA ES SOLO UNA SUGERENCIA. EL QA ENGINEER TOMA LA DECISIÓN FINAL.**

### Stage 3 — REPORTING

Guarda en `knowledge/L1-project/regression-results/`:

```markdown
# Release Decision — [fecha]

## Release Info
- Tickets incluidos: [lista]
- Branch: DEVELOPMENT
- Entorno: dev-app.ionflow.io → producción

## Criterios de Go/No-Go
[tabla del Paso 1]

## Risk Assessment por Ticket
[tabla del Paso 2]

## Veredicto
- Sugerencia del Catalyst: [GO/NO-GO/GO CON CONDICIONES]
- **Decisión final (QA Engineer)**: [GO/NO-GO]
- Firmado por: [nombre]
- Fecha: [fecha]
- Condiciones (si aplican): [lista]

## Historial de decisiones
| Fecha | Veredicto | Tasa de pass | Bugs bloqueantes | Notas |
|-------|-----------|-------------|-----------------|-------|
| [hoy] | [veredicto] | [%] | [N] | [nota] |
```

---

## Reglas de este Skill

1. **El Catalyst SUGIERE, el QA Engineer DECIDE** — La decisión de release es siempre humana
2. **0 bugs 🔴 en módulos críticos** — Es el mínimo no negociable
3. **Tests flaky no bloquean release** — Pero se registran para resolver
4. **Tickets sin cobertura E2E** se marcan como riesgo pero no bloquean si fueron testeados manualmente
5. **El historial de decisiones es importante** — Permite auditar patrones a lo largo del tiempo
