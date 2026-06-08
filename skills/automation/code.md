# Skill: automation/code

> Orquesta la generación de tests E2E con Playwright a través de la skill `ionflow-playwright-creator` del repo bot-test.
> Este skill es el **Canal 2 (E2E Automation)** — genera tests permanentes y reutilizables.
>
> ⚠️ **NO confundir con Canal 1 (Playwright MCP)** que se usa en `sprint-testing/test.md`
> para testing asistido en tiempo real. Son canales diferentes con objetivos distintos.

## Cuándo usar este skill

- **Deployment Track**: Después de que `automation/plan` identifique los TCs a automatizar
- **Post-release**: Para consolidar tests de regresión

## Pre-requisitos

- ✅ `L3-tickets/<ticket-id>/automation-plan.md` (del skill `automation/plan`)
- ✅ `knowledge/L2-modules/<módulo>/module.md` — Rutas, componentes, selectores
- ✅ `L3-tickets/<ticket-id>/test-matrix.md` — Detalle de los TCs a automatizar
- ✅ Acceso de lectura a `../gateway-ion/src/` — Para verificar selectores reales
- ✅ Acceso de lectura a `../bot-test/` — Para reusar page objects y helpers

---

## Rol del Catalyst en este Skill

```
┌─────────────────────────────────┐     ┌──────────────────────────────┐
│        QA CATALYST              │     │ ionflow-playwright-creator   │
│      (este skill)               │     │   (skill en bot-test)        │
├─────────────────────────────────┤     ├──────────────────────────────┤
│ ✅ Decide QUÉ automatizar       │     │ ✅ Genera el código .spec.ts  │
│ ✅ Prepara el contexto del L2   │     │ ✅ Crea page objects si faltan│
│ ✅ Verifica selectores reales   │     │ ✅ Sigue las reglas E2E       │
│ ✅ Valida que el test hace      │     │                              │
│    lo que dice la test-matrix   │     │                              │
└─────────────────────────────────┘     └──────────────────────────────┘
              │                                       │
              │  Provee contexto + TCs                │
              ├──────────────────────────────────────►│
              │                                       │
              │  Recibe tests generados               │
              │◄──────────────────────────────────────┤
```

### Diferencia entre Canal 1 y Canal 2

| Aspecto | Canal 1 (Playwright MCP) | Canal 2 (E2E Automation) |
|---------|--------------------------|-------------------------|
| **Skill** | `sprint-testing/test.md` (Opción B) | `automation/code.md` (este skill) |
| **Propósito** | Testing asistido en tiempo real | Tests permanentes y reutilizables |
| **Quién ejecuta** | QA Catalyst navega el browser en vivo | `ionflow-playwright-creator` genera código |
| **Output** | Resultados de TCs + screenshots | Archivos `.spec.ts` + page objects |
| **Repo destino** | N/A (sesión en vivo) | `../bot-test/apps/bot-test/tests/IONFLOW/` |
| **Cuándo** | Durante testing de Deployment | Después de testing aprobado |

> **REGLA**: Este skill NO usa Playwright MCP directamente. DELEGA a `ionflow-playwright-creator`
> para que genere los tests E2E como código permanente.

## Instrucciones de Ejecución

### Stage 1 — PLANNING

Reporta al QA Engineer:
1. Los TCs aprobados para automatización (del automation-plan)
2. Los page objects y helpers que vas a reusar
3. Los nuevos page objects que necesitas crear
4. La estructura de archivos que vas a generar

```
ARCHIVOS A GENERAR — [TICKET-ID]

Destino: ../bot-test/apps/bot-test/tests/IONFLOW/tickets/[TICKET-ID]/

Archivos:
  - [TICKET-ID].spec.ts          ← Tests de los TCs aprobados
  - [TICKET-ID].page.ts          ← Page Object (si no existe uno para el módulo)

Page Objects existentes a reusar:
  - ../tests/IONFLOW/pages/[módulo].page.ts (si existe)

Helpers existentes a reusar:
  - ../tests/IONFLOW/utils/[helper].ts (si existe)
```

**Espera aprobación antes de generar código.**

### Stage 2 — EXECUTION

#### Paso 1: Preparar el contexto para `ionflow-playwright-creator`

Lee el código real de `../gateway-ion/src/` para el módulo afectado y extrae:

| Info | Fuente | Para qué |
|------|--------|---------|
| Rutas de la app | `src/router/` | Navegación en los tests |
| Selectores de componentes | `src/views/<módulo>/` y `src/components/<módulo>/` | `data-testid`, clases, IDs |
| Llamadas a API | `src/services/` o `src/api/` | Interceptar requests si es necesario |
| Estado inicial necesario | `src/stores/` | Setup del test (login, datos previos) |

#### Paso 2: Delegar a `ionflow-playwright-creator`

> ⚠️ La generación de código E2E **NO se hace en este repo**.
> Se delega completamente al skill del repo `bot-test`.

Leer la skill ubicada en:
```
../bot-test/.agents/skills/ionflow-playwright-creator/SKILL.md
```

**Protocolo de delegación:**
1. Leer `SKILL.md` de ionflow-playwright-creator ANTES de generar cualquier código
2. Seguir las convenciones y reglas definidas en esa skill
3. Proveer como contexto:
   - Los TCs a automatizar (de la test-matrix, solo los aprobados manualmente)
   - Los selectores verificados del frontend real (gateway-ion)
   - Los page objects existentes en bot-test para reusar
   - Las rutas de la app (del router de gateway-ion)
   - Las convenciones de nombres del proyecto
4. El código generado va en:
   ```
   ../bot-test/apps/bot-test/tests/IONFLOW/tickets/<TICKET-ID>/
   ```
5. **NUNCA generar código E2E fuera de `../bot-test/`**
6. **NUNCA generar código E2E en este repo (ionflow-qa-catalyst)**

#### Paso 3: Verificar los tests generados

Para cada test generado, verificar:

| Check | Estado |
|-------|--------|
| ¿El test cubre exactamente el TC de la matrix? | ✅/❌ |
| ¿Los selectores son reales (verificados en el código)? | ✅/❌ |
| ¿Se reusan page objects existentes donde es posible? | ✅/❌ |
| ¿El test es independiente (no depende del orden)? | ✅/❌ |
| ¿El test hace cleanup de datos si es necesario? | ✅/❌ |
| ¿Los assertions verifican lo correcto? | ✅/❌ |

#### Paso 4: Registrar el mapeo TC → Test

| TC-ID | Archivo de test | Test name | Estado |
|-------|----------------|-----------|--------|
| TC-001 | `TASK-12345.spec.ts` | `should create a new flow` | ✅ Generado |
| TC-004 | `TASK-12345.spec.ts` | `should show error for empty name` | ✅ Generado |

### Stage 3 — REPORTING

Guarda en `L3-tickets/<ticket-id>/automation-result.md`:

```markdown
# Automatización E2E — [TICKET-ID]

## Resumen
- TCs automatizados: [N] de [total candidatos]
- Archivos generados: [lista]
- Page Objects creados: [lista]
- Destino: ../bot-test/apps/bot-test/tests/IONFLOW/tickets/[TICKET-ID]/

## Mapeo TC → Test
[tabla del Paso 4]

## Ejecución
Comando para ejecutar los tests:
  npx nx run bot-test:test:ionflow --args="--spec=tests/IONFLOW/tickets/[TICKET-ID]/"

## Pendiente
- [ ] QA Engineer ejecuta los tests y verifica que pasan
- [ ] Si pasan → considerar migración a suite permanente del módulo
```

---

## Reglas de este Skill

1. **Solo UI de gateway-ion** — No generar tests para canvas/webcomponents
2. **Siempre verificar selectores contra el código real** — Nunca inventar selectores
3. **Reusar page objects y helpers existentes** — No duplicar código
4. **Cada test debe mapear a un TC de la matrix** — No generar tests "extras"
5. **Los tests van en `tickets/<TICKET-ID>/`** — No en la suite permanente directamente
6. **El QA Engineer valida antes de considerar el test como confiable**
7. **Solo automatizar TCs ya validados manualmente** — NUNCA automatizar sin testing previo
8. **Delegación estricta** — Leer `ionflow-playwright-creator/SKILL.md` antes de generar código
9. **No confundir con Canal 1** — Canal 1 (Playwright MCP) es testing asistido, Canal 2 es automation
