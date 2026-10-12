# Skill: test-suites/smoke-master

> Mantiene el **smoke maestro** (`Q-47`): revisa su vigencia, propone cambios (verificaciones nuevas o retiradas) y actualiza su estado de automatización. El smoke es fijo; solo cambia con acuerdo del **LQA y el LD/RM**.

## Cuándo usar

- En la retro, cuando un incidente de producción revela un camino crítico no cubierto, cuando cambia la navegación principal o cuando se automatiza una verificación.
- Frase disparadora: `Revisar smoke maestro`.

## Pre-requisitos (gates)

| Check | Si falla |
|---|---|
| `knowledge/test-suites/smoke-master.md` existe | — |
| Motivo del cambio identificado (incidente `det-prod`, cambio de producto, automatización) | Sin motivo, no se cambia el smoke |

## Contexto a cargar

`smoke-master.md`, `knowledge/L1-project/test-priorities.md`, los `smoke-prod.md` y `smoke-preprod.md` de los últimos releases, bugs `det-prod` del período (MCP, solo lectura), `skills/_shared/bot-test.md`.

## Stage 1 — Planning

Anunciar el motivo y el tipo de revisión (cobertura, automatización o ambas). Esperar confirmación.

## Stage 2 — Execution

1. **Vigencia:** cada SMK sigue existiendo en la app, tiene resultado esperado verificable y cabe en el timebox (≤ 0,5 d manual, ≈ 15 min automatizado).
2. **Escapes:** cada bug `det-prod` del período que rompió un camino crítico → ¿lo habría detectado el smoke? Si no, proponer una verificación nueva o ajustar una existente.
3. **Producción:** cada verificación es segura con la company de prueba (crea y limpia, o es de solo lectura). Las que no, se marcan solo-preprod.
4. **Automatización:** actualizar la columna *Automatización hoy* con los tests reales de bot-test (IDs) y su estado; listar lo que falta para la Ola 1 de `automation-roadmap.md`.
5. **Tamaño:** el smoke no debería crecer más allá de ~20 verificaciones. Si una propuesta lo excede, proponer qué pasa al baseline de regresión.

## Stage 3 — Reporting

- Propuesta de cambios (diff de la tabla) para el acuerdo LQA + LD/RM.
- Una vez aprobada: `smoke-master.md` actualizado con una fila nueva en su **Historial**, y `templates/smoke-run.md` alineado si cambió la lista.
- Si cambia el alcance funcional del smoke, registrar la decisión en el Registro de Decisiones (doc 03) a través del SM.

## Reglas

- El smoke es **único para todo release**: nunca se agregan verificaciones de una versión específica (van a `sanity`).
- No se agregan verificaciones de producción que dejen datos sin limpiar.
