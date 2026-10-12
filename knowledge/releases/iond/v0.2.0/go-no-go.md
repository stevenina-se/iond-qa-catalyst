# Go / No-Go — iond v0.2.0 (beta) + IonMind v1.10.2

> **Acta de la mesa Go/No-Go** (REL-06 · `Q-35` · fuente canónica §7.1, §7.5 y C-29 · Estándar de QA §7.1) · Skill `skills/release/go-no-go.md` · Comentario **C-29** (lo publica el LQA: con GO o CONDITIONAL GO la tarea pasa a `ready for release`; con NO-GO permanece en `regression`).
> Pre-armada el 2026-10-10 y se completa el viernes con los resultados. Reunión obligatoria **PO + LQA + RM**; sin quórum no hay decisión. El LQA **no firma un GO ni un CONDITIONAL GO con un `urgent` abierto**.
> Una sola mesa decide las dos versiones: IonMind v1.10.2 se despliega primero y las suites corrieron sobre el sistema integrado. Si IonMind es NO-GO, iond también lo es, salvo que el PO retire de iond los tickets que dependen de IonMind.

## Datos

| Campo | Valor |
|---|---|
| Producto / versión | iond v0.2.0 + IonMind v1.10.2 |
| Tareas de Release | Release iond - v0.2.0 — https://app.clickup.com/t/86e39jadr · Release IonMind - v1.10.2 — [url al crearla] |
| Fecha y hora de la mesa | 2026-10-16 10:00 |
| Quórum | [ ] PO · [ ] LQA · [ ] RM |

## Resultados por suite

| Suite | Resultado | Criterio GO | Cumple | Artefacto |
|---|---|---|---|---|
| Smoke maestro (preprod) | [n]/16 (SMK-17 no aplica) · core [n/6] | 100 % | ✅ / ❌ | `smoke-preprod.md` |
| Sanity | `urgent` [n]/61 · `high` [n]/84 · `normal` [n]/38 | 100 % de los casos `urgent`; `high` sin bugs `urgent` | ✅ / ❌ | `sanity-matrix.md` |
| Regression capa 1 | `urgent` [n]/94 · RGR [n]/12 · `high` [n]/74 | 100 % de `urgent` + RGR | ✅ / ❌ | `regression-matrix.md` |
| E2E maestro capa 2 | Automatizado [n]/71 · rotación G1 [n]/11 · cuarentena [n] | Fallas analizadas y clasificadas; NO-GO solo por un `urgent` provocado por el release | ✅ / ❌ | `e2e-run.md` |

## Lo no ejecutado por la priorización

Riesgo residual que la mesa acepta de forma explícita. Lo trasladan los C-26 y C-27.

| Suite | No ejecutado | Motivo | Lo cubre |
|---|---|---|---|
| Sanity | Casos `normal` no ejecutados: [IDs] · `high` no ejecutado: [IDs] · 14 tickets cubiertos solo vía regresión | Priorización / timebox | Regresión `urgent`–`high` y capa 2 |
| Regression capa 1 | `normal` por diseño (71 filas) · `high` no ejecutado: [IDs] | Priorización / timebox | Capa 2 (71 automáticas) y rotación G2–G4 |
| E2E capa 2 | Rotación G1 pendiente: [IDs] | Timebox | Siguiente release del grupo G1 |

## Decisiones del PO sobre las observaciones de preparación

Tomadas el miércoles 14/10 (`observaciones-preparacion.md`). Las que bloquean el GO si no se resuelven:

| ID | Tema | Decisión | Efecto en el Go/No-Go |
|---|---|---|---|
| OBS-01 | NOVASPHERE (86e1y463z) con último veredicto RECHAZADO | | Si los bloqueantes siguen abiertos: revertir de la RC (`diferido`) o NO-GO |
| OBS-02 | Aprobación de la monetización (86e1pzyug) no confirmada en ClickUp | | Se cierra con el sanity `urgent` completo |
| OBS-05 | 86e2p459r: PRs en la RC | | Si no entran, el ticket sale del release |
| OBS-18 | Proxy de Logo.dev cross-tenant | | Si se confirma: `urgent` → fix-forward o retirar la familia Logo.dev |
| OBS-19 | Guard de duplicados de IonMind retirado | | Si se confirma: `high` → aceptación del PO + backfill |
| OBS-06…17 | Desvíos aprobados | | Aceptados → release notes internas; rechazados → Improvements |

## Hallazgos abiertos

| ID | Severidad | Fase | Decisión | Riesgo aceptado por el PO | Workaround comunicado | Fix agendado |
|---|---|---|---|---|---|---|
| | | | | | | |

## Checklist de criterios (Estándar de QA §7.1)

**🟢 GO** — se cumplen todos:
- [ ] Smoke al 100 % (sin contar SMK-17, que no aplica)
- [ ] `sanity` con el 100 % de los casos `urgent` aprobados (incluidas sus revalidaciones)
- [ ] Flujos críticos de `regression` (`urgent` + RGR) al 100 %
- [ ] Cero `urgent` y cero `high` abiertos
- [ ] Rollback verificado y ventana acordada con DevOps

**🟡 CONDITIONAL GO** — se cumplen todos:
- [ ] Cero `urgent` abiertos
- [ ] Cada `high` abierto tiene la aceptación del riesgo por el PO en el C-29, el workaround comunicado al soporte general de la empresa y el fix agendado (ticket en Improvements con versión objetivo)
- [ ] `normal` y `low` registrados en Improvements
- [ ] Lo no ejecutado por la priorización está listado arriba y aceptado por el PO
- [ ] Ninguna condición de NO-GO

**🔴 NO-GO** — basta una:
- [ ] Algún `urgent` abierto sin fix-forward verificado ni revert del ticket
- [ ] `smoke` del core fallido
- [ ] Prerrequisitos o rollback sin verificar (incluido el orden IonMind → iond)
- [ ] El PO no acepta el riesgo de un `high` abierto

> Las fallas de la capa 2 que no son `urgent` provocadas por el release no cambian la decisión.

## Recomendación del catalyst (borrador para el LQA)

**Decisión sugerida:** [GO / CONDITIONAL GO / NO-GO] — [fundamento en 2–3 líneas]. Con la priorización, lo esperable es un **CONDITIONAL GO**: `urgent` y RGR completos, `high` aceptados por el PO y lo no ejecutado documentado.

## Votos

| Rol | Voto | Comentario |
|---|---|---|
| PO | ✅ / ❌ | |
| LQA | ✅ / ❌ | |
| RM | ✅ / ❌ | |

**Decisión de la mesa:** GO / CONDITIONAL GO / NO-GO

## Release notes, rollback y ventana

| Elemento | Estado |
|---|---|
| Release notes interna | `release-notes-internal.md` (skill `release/notes`, viernes AM) — incluye los desvíos aceptados |
| Release notes cliente | `release-notes-client.md` — la aprueba y comunica el PO (es la beta pública de iond) |
| Plan de rollback | Probado en preprod ✅ / ❌ — `deployment-protocol.md` §8 |
| Ventana de despliegue | 2026-10-16, antes de las 14:00, con DevOps · IonMind → iond |

## Si la decisión es NO-GO

- Las dos tareas de Release permanecen en `regression` con el C-29 NO-GO y se reprograma su fecha de vencimiento al siguiente Go/No-Go (`Q-35`).
- Si se desarma una versión, se cierra con un comentario y los tickets revertidos de la RC vuelven a `to do` con `diferido`.

## Borrador C-29

Se publica en las dos tareas de Release. Al publicar se deja **una sola** opción en la línea de decisión:

```markdown
## 🚦 GO / NO-GO — iond v0.2.0 + IonMind v1.10.2
**Decisión:** 🟢 GO / 🟡 CONDITIONAL GO / 🔴 NO-GO
**Votos:** PO @[..] [✅/❌] · LQA @[..] [✅/❌] · RM @[..] [✅/❌]
**Resultados:** Smoke [n/16] · Sanity `urgent` [n/61] · Regression capa 1 `urgent`+RGR [n/106] · E2E capa 2 [n/82]
**No ejecutado (priorización):** [resumen] — aceptado por el PO
**Hallazgos abiertos:** [ID — severidad — aceptado por PO / workaround]
**Release notes:** [interna] · [cliente]
**Rollback:** plan verificado ✅ · **Ventana de despliegue:** 2026-10-16 [hh:mm] con DevOps (IonMind → iond)
```
