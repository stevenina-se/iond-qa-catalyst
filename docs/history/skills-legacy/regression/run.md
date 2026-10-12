# Skill: regression/run

> Ejecuta la suite de regresión E2E (Playwright) para un módulo o para la suite completa de Ionflow, y recopila los resultados.

## Cuándo usar este skill

- **Pre-release**: Antes de aprobar un deploy a producción
- **Post-merge**: Después de mergear un batch de tickets en DEVELOPMENT
- **On-demand**: Cuando el QA Engineer quiere verificar estabilidad de un módulo

## Pre-requisitos

- ✅ `knowledge/L1-project/test-priorities.md` — Para saber qué módulos son críticos
- ✅ Acceso a `../bot-test/apps/bot-test/tests/IONFLOW/` — Suite de tests
- ✅ Entorno de testing desplegado y accesible (dev-app.ionflow.io)

---

## Instrucciones de Ejecución

### Stage 1 — PLANNING

Reporta al QA Engineer:
1. El scope de la regresión (módulo específico o suite completa)
2. Los tests disponibles en la suite
3. El entorno donde se va a ejecutar
4. Tiempo estimado de ejecución

**Modos de ejecución:**

| Modo | Comando | Cuándo usar |
|------|---------|-------------|
| Suite completa | `npx nx run bot-test:test:ionflow` | Pre-release |
| Por módulo | `npx nx run bot-test:test:ionflow --args="--spec=tests/IONFLOW/<módulo>/"` | Verificar un área específica |
| Por ticket | `npx nx run bot-test:test:ionflow --args="--spec=tests/IONFLOW/tickets/<ticket-id>/"` | Verificar tests de un ticket |

**Espera aprobación antes de ejecutar.**

### Stage 2 — EXECUTION

#### Paso 1: Inventariar la suite

Antes de ejecutar, lista qué tests existen:

```
INVENTARIO DE SUITE — [scope]

Módulos con tests:
  - auth/: [N] tests
  - flows/: [N] tests
  - connectors/: [N] tests
  - ...

Tickets con tests:
  - TASK-12345/: [N] tests
  - TASK-12346/: [N] tests
  - ...

Total: [N] archivos .spec.ts, ~[N] test cases
```

#### Paso 2: Ejecutar la suite

```
⏸ El QA Engineer ejecuta el comando de Playwright.
  El Catalyst NO ejecuta los tests directamente.

Comando sugerido:
  npx nx run bot-test:test:ionflow [--args="--spec=..."]

El QA Engineer pegará la salida de Playwright cuando termine.
```

> **Nota**: El Catalyst puede preparar el comando exacto, pero el QA Engineer lo ejecuta y comparte los resultados.

#### Paso 3: Registrar resultados

Cuando el QA Engineer pegue la salida de Playwright, parsear y registrar:

| Test | Módulo | Resultado | Tiempo | Detalles |
|------|--------|-----------|--------|----------|
| `should login successfully` | auth | ✅ Pass | 2.3s | |
| `should create flow` | flows | ❌ Fail | 5.1s | Timeout en selector `.flow-card` |
| `should list connectors` | connectors | ✅ Pass | 1.8s | |

### Stage 3 — REPORTING

Guarda en `knowledge/L1-project/regression-results/` (crear directorio si no existe):

```markdown
# Regression Run — [fecha]

## Información
- Scope: [suite completa / módulo / ticket]
- Entorno: [dev-app.ionflow.io]
- Branch: DEVELOPMENT
- Ejecutado por: [QA Engineer]
- Duración total: [tiempo]

## Resumen

| Métrica | Valor |
|---------|-------|
| Total tests | [N] |
| Passed | [N] ([%]) |
| Failed | [N] ([%]) |
| Skipped | [N] |
| Flaky | [N] |

## Resultados por módulo

| Módulo | Total | ✅ Pass | ❌ Fail | Tasa |
|--------|-------|---------|---------|------|
| auth | | | | % |
| flows | | | | % |
| connectors | | | | % |

## Tests fallidos (detalle)
[tabla con detalles de cada fallo]

## Próximo paso
→ Pasar a `regression/analyze` para analizar los fallos
```

---

## Reglas de este Skill

1. **El QA Engineer ejecuta Playwright** — El Catalyst prepara el comando y analiza el output
2. **Siempre inventariar antes de ejecutar** — Saber qué hay en la suite
3. **Registrar CADA resultado** — Incluso los que pasan, para histórico
4. **Los resultados van en L1** (no L3) — La regresión es del proyecto, no de un ticket
5. **Guardar con fecha** — Para comparar entre runs
