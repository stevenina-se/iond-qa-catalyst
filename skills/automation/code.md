# Skill: automation/code

> Prepara el **paquete de automatización** para el responsable de bot-test: casos aprobados, selectores verificados en el código del frontend, page objects a reutilizar, ubicación y convenciones. El código lo genera el responsable de bot-test con la skill de su repositorio (`../bot-test/.agents/skills/e2e-playwright-creator/SKILL.md`). **El catalyst no escribe en bot-test** (`Q-54`).

## Cuándo usar

- Después de `automation/plan` aprobado por el LQA.
- Frase disparadora: `Preparar paquete de automatización: <ticket-id | prefijo E2E>`.

## Pre-requisitos (gates)

| Check | Si falla |
|---|---|
| `automation-plan.md` aprobado | Ejecutar `automation/plan` |
| Acceso de lectura a `../gateway-ion/src/` y `../bot-test/` | PARAR |

## Contexto a cargar

`automation-plan.md`, la Matriz de Pruebas o las filas E2E del alcance, L2 del módulo, `skills/_shared/bot-test.md`, la skill `e2e-playwright-creator` (para respetar sus convenciones) y `Company-ION/nodes/README.md` de bot-test cuando hay canvas.

## Stage 1 — Planning

Anunciar los casos del paquete, la carpeta destino propuesta en bot-test y los recursos a reutilizar. Esperar confirmación.

## Stage 2 — Execution

1. **Selectores reales** desde `../gateway-ion/src/` (router, vistas y componentes del módulo): roles accesibles, labels y textos estáticos; `data-testid` si existe. Orden de preferencia: `getByRole` > `getByLabel` > `getByText` (estático) > `getByTestId`. Nunca inventar selectores.
2. **Ubicación** según la convención de bot-test: `tests/IONFLOW/Company-ION/<módulo>/` (o `Admin-ION/<dominio>/`), con spec, page object y `.md` del módulo; nodos en `Company-ION/nodes/<nodo>/`; el canvas solo a través de sus componentes aislados.
3. **Convenciones:** ID en el título `[TC-<MÓDULO>-<GRUPO>-NN]` sin repetir los existentes; tags `@ionflow @company|@admin @<módulo> @<prioridad>` y de tipo; `@smoke` y `@prod-safe` cuando el caso pertenezca al smoke maestro; datos `autobot-*` con limpieza en `afterAll`; sin `waitForTimeout` ni `networkidle`; mocks solo donde el caso lo acuerde.
4. **Trazabilidad:** tabla caso → TC-ID propuesto → fila `E2E-…` → REQ-ID (si viene de un ticket) → resultado esperado → datos.
5. **Comando de verificación** que usará el responsable: `npx playwright test <spec> --config=tests/IONFLOW/playwright.ionflow.config.ts -g "<IDs>"` (3 corridas verdes consecutivas antes de integrar).

## Stage 3 — Reporting

- `automation-handoff.md` (L3 del ticket o `knowledge/test-suites/plans/`), listo para entregar al responsable de bot-test o adjuntar al ticket de QA Kanban.
- Acción posterior (cuando el código esté integrado): actualizar `_config/rules.csv` con spec, TC-IDs y estado, y reimportar el maestro (`test-suites/import-e2e`).
- Siguiente skill: `automation/review` cuando el responsable entregue los tests.

## Reglas

- **Nunca** crear ni editar archivos en `../bot-test` desde el catalyst.
- Cada test propuesto mapea a un caso aprobado; no se proponen tests "extra".
- No confundir con el Canal 1 (Playwright MCP en `mock testing`): aquí se definen tests permanentes.
