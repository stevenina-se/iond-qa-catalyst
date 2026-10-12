# Skill: release/go-no-go

> Prepara el **acta Go/No-Go** (C-29) para la mesa del viernes 10:00 con quórum **PO + LQA + RM** (`Q-35`, REL-06). Consolida smoke, sanity, regresión capa 1, E2E capa 2 y hallazgos, y aplica los criterios del estándar de QA (doc 05 §7.1). Reemplaza a `regression/decide`.

## Cuándo usar

- Viernes, antes de las 10:00, con el C-27 consolidado. La mesa se hace al cerrar `regression`: con GO o CONDITIONAL GO la tarea pasa a `ready for release`; con NO-GO permanece en `regression` (`Q-35`).
- Frase disparadora: `Preparar Go/No-Go: <producto> vX.Y.Z`.

## Pre-requisitos (gates)

| Check | Si falla |
|---|---|
| `smoke-preprod.md`, `sanity-matrix.md`, `regression-matrix.md`, `e2e-run.md` completos | Completar la suite faltante o registrar por qué no se ejecutó |
| Hallazgos con decisión (fix-forward verificado / Improvements / diferido) | Resolver con PO + LD antes de la mesa |
| Plan de rollback y ventana de despliegue (AV-07) | Acción del LD/RM |

## Contexto a cargar

`docs/sdlc-iond/src/05-estandar-operativo-qa-iond.md` §7.1, fuente canónica §7.5 y C-29, los artefactos del release.

## Stage 1 — Planning

Anunciar los artefactos que se consolidan y los hallazgos abiertos. Esperar confirmación.

## Stage 2 — Execution

1. **Resultados por suite** (n/n y estado): smoke preprod, sanity (REQ críticos), capa 1 (flujos críticos), capa 2 (automático + rotación).
2. **Hallazgos abiertos** con severidad, fase (`det-smoke`, `det-sanity`, `det-regression`) y decisión.
3. **Aplicar criterios** (doc 05 §7.1):

   | Decisión | Condiciones |
   |---|---|
   | 🟢 **GO** | Smoke 100 % · sanity 100 % de REQ críticos · capa 1 con flujos críticos al 100 % · cero `urgent` y cero `high` abiertos · rollback verificado y ventana acordada |
   | 🟡 **CONDITIONAL GO** | Solo hallazgos `high` con workaround, riesgo aceptado por el PO y fix agendado (`Q-35`) |
   | 🔴 **NO-GO** | Algún `urgent` abierto sin fix-forward verificado ni revert · core del smoke fallido · prerrequisitos o rollback sin verificar · el PO no acepta el riesgo de un `high` |

   Las fallas de la capa 2 que no son `urgent` provocadas por el release **no** cambian la decisión.
4. **Recomendación del LQA** (borrador): decisión sugerida con su fundamento. La decisión final es de la mesa.
5. **Ante NO-GO** (`Q-35`): la tarea de Release permanece en `regression` con el C-29 NO-GO y se reprograma la fecha al siguiente Go/No-Go; si se desarma la versión, los tickets revertidos llevan `diferido`.

## Stage 3 — Reporting

- `go-no-go.md` con `templates/go-no-go.md` y borrador **C-29** en `comments/` (texto normalizado `Decisión: GO | CONDITIONAL GO | NO-GO`).
- Siguientes skills: `release/notes` (si GO/CONDITIONAL GO) y `release/deployment-protocol`.

## Reglas

- El catalyst **sugiere**; votan PO, LQA y RM. Sin quórum no hay decisión.
- Un `urgent` abierto es siempre NO-GO.
- Los votos y la decisión se publican en el C-29 de la tarea de Release (lo publica el LQA).
