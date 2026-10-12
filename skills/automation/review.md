# Skill: automation/review

> Revisa los tests E2E entregados por el responsable de bot-test antes de contarlos como cobertura del E2E maestro: calidad del código, trazabilidad al caso y **estabilidad 3/3**. Solo lectura sobre bot-test.

## Cuándo usar

- Cuando una spec nueva o modificada está en un PR o rama de bot-test.
- Frase disparadora: `Revisar automatización: <spec | PR de bot-test>`.

## Pre-requisitos (gates)

| Check | Si falla |
|---|---|
| `automation-handoff.md` del alcance | Revisar contra la Matriz de Pruebas o las filas E2E |
| La rama del PR de bot-test está disponible localmente (solo lectura) | Pedir al QA que la traiga (`git fetch`) |

## Contexto a cargar

`automation-handoff.md`, las specs y page objects entregados, `skills/_shared/bot-test.md`.

## Stage 1 — Planning

Anunciar las specs a revisar y los casos que deben cubrir. Esperar confirmación.

## Stage 2 — Execution

1. **Revisión de código** por spec:

   | Criterio | ✅/❌ |
   |---|---|
   | Selectores reales y estables (rol, label, test id; sin CSS frágil ni índices) | |
   | Assertions verifican el resultado esperado del caso (no solo visibilidad) | |
   | Independencia y limpieza de datos (`autobot-*`, `afterAll` sin remanentes) | |
   | Login compartido por archivo; sin `waitForTimeout` ni `networkidle` | |
   | IDs `TC-…` únicos en el título y tags correctos (incluidos `@smoke`/`@prod-safe` si aplica) | |
   | Bugs conocidos en cuarentena visible (`@bug` / `test.fail()`), no `expect.soft` silencioso | |
   | Reutiliza page objects y componentes existentes | |

2. **Estabilidad:** el QA ejecuta la spec **3 veces seguidas** con el perfil de preprod. Consistente = 3/3 verdes.
3. **Decisión por test:** 🟢 cuenta como cobertura · 🟡 corregir y volver a revisar · 🔴 descartar o reescribir.

## Stage 3 — Reporting

- `automation-review.md` (junto al handoff) con la tabla de criterios, las 3 corridas y la decisión por test.
- Para los 🟢: actualizar `_config/rules.csv` (`BOT_TEST_SPEC`, `BOT_TEST_TC`, `AUTOMATIZACION = En PR` o `Ejecutable` cuando se integre) y reimportar el maestro.
- Observaciones para el responsable de bot-test (sin comentar el PR desde el catalyst).

## Reglas

- Un test inestable no suma cobertura.
- 3 corridas consecutivas verdes es el mínimo.
- El LQA aprueba que un test cuente para el smoke o el baseline.
