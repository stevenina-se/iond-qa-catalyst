# Go / No-Go — [producto] v[X.Y.Z]

> **Plantilla del QA Catalyst** — acta de la mesa Go/No-Go (REL-06 · `Q-35` · fuente canónica §7.1, §7.5 y C-29 · Estándar de QA §7.1).
> **Se guarda en:** `knowledge/releases/[producto]/v[X.Y.Z]/go-no-go.md` · **Skill:** `skills/release/go-no-go.md` · Comentario **C-29** (lo publica el LQA en la tarea de Release: con GO o CONDITIONAL GO queda en `ready for release`; con NO-GO permanece en `regression`).
> Mesa del viernes 10:00, reunión obligatoria **PO + LQA + RM**; sin quórum no hay decisión. El catalyst sugiere; vota el quórum. El LQA **no firma un GO ni un CONDITIONAL GO con un `urgent` abierto**.

## Datos

| Campo | Valor |
|---|---|
| Producto / versión | [iond / IonMind / StageMind] v[X.Y.Z] |
| Tarea de Release | [Release producto - vX.Y.Z] — [url] |
| Fecha y hora de la mesa | [AAAA-MM-DD] 10:00 |
| Quórum | [ ] PO · [ ] LQA · [ ] RM |

## Resultados por suite

| Suite | Resultado | Criterio GO | Cumple | Artefacto |
|---|---|---|---|---|
| Smoke maestro (preprod) | [n/n] · core [n/6] | 100 % | ✅ / ❌ | `smoke-preprod.md` |
| Sanity | REQ críticos [n/n] | 100 % de los REQ críticos | ✅ / ❌ | `sanity-matrix.md` |
| Regression capa 1 | Flujos críticos [n/n] | 100 % de los flujos críticos | ✅ / ❌ | `regression-matrix.md` |
| E2E maestro capa 2 | Automatizado [n/n] · rotación G[n] [n/n] · cuarentena [n] | Fallas analizadas y clasificadas; NO-GO solo por un `urgent` provocado por el release | ✅ / ❌ | `e2e-run.md` |

## Hallazgos abiertos

| ID | Severidad | Fase | Decisión | Riesgo aceptado por el PO | Workaround comunicado | Fix agendado |
|---|---|---|---|---|---|---|
| [...] | `urgent` / `high` / `normal` / `low` | `det-smoke` / `det-sanity` / `det-regression` | Fix-forward verificado / revert (`diferido`) / Improvements | Sí / No | Sí (soporte general de la empresa) / No | #[id] — v[X.Y.Z+1] |

## Checklist de criterios (Estándar de QA §7.1)

**🟢 GO** — se cumplen todos:
- [ ] Smoke al 100 %
- [ ] `sanity` con el 100 % de los REQ críticos aprobados
- [ ] Flujos críticos de `regression` al 100 %
- [ ] Cero `urgent` y cero `high` abiertos
- [ ] Rollback verificado y ventana acordada con DevOps

**🟡 CONDITIONAL GO** — se cumplen todos:
- [ ] Cero `urgent` abiertos
- [ ] Cada `high` abierto tiene la aceptación del riesgo por el PO en el C-29, el workaround comunicado al soporte general de la empresa y el fix agendado (ticket en Improvements con versión objetivo)
- [ ] `normal` y `low` registrados en Improvements
- [ ] Ninguna condición de NO-GO

**🔴 NO-GO** — basta una:
- [ ] Algún `urgent` abierto sin fix-forward verificado ni revert del ticket
- [ ] `smoke` del core fallido
- [ ] Prerrequisitos o rollback sin verificar
- [ ] El PO no acepta el riesgo de un `high` abierto

> Las fallas de la capa 2 que no son `urgent` provocadas por el release no cambian la decisión.

## Recomendación del catalyst (borrador para el LQA)

**Decisión sugerida:** GO / CONDITIONAL GO / NO-GO — [fundamento en 2–3 líneas, citando el checklist].

## Votos

| Rol | Voto | Comentario |
|---|---|---|
| PO | ✅ / ❌ | [...] |
| LQA | ✅ / ❌ | [...] |
| RM | ✅ / ❌ | [...] |

**Decisión de la mesa:** GO / CONDITIONAL GO / NO-GO

## Release notes, rollback y ventana

| Elemento | Estado |
|---|---|
| Release notes interna | `release-notes-internal.md` — [enlace] |
| Release notes cliente | `release-notes-client.md` — la aprueba y comunica el PO |
| Plan de rollback | Probado en preprod ✅ / ❌ — `deployment-protocol.md` |
| Ventana de despliegue | [AAAA-MM-DD hh:mm] con DevOps (viernes antes de las 14:00 o lunes temprano) |

## Si la decisión es NO-GO

- La tarea de Release permanece en `regression` con el C-29 NO-GO y se reprograma su fecha de vencimiento al siguiente Go/No-Go (`Q-35`).
- Si se desarma la versión, se cierra con un comentario y los tickets revertidos de la RC vuelven a `to do` con `diferido`.

## Borrador C-29

Texto de `templates/comments/C-29.md` (generado desde la fuente canónica; si difieren, prevalece el generado). Al publicar se deja **una sola** opción en la línea de decisión (texto normalizado `Decisión: GO | CONDITIONAL GO | NO-GO`, fuente canónica §7.1):

```markdown
## 🚦 GO / NO-GO — [producto vX.Y.Z]
**Decisión:** 🟢 GO / 🟡 CONDITIONAL GO / 🔴 NO-GO
**Votos:** PO @[..] [✅/❌] · LQA @[..] [✅/❌] · RM @[..] [✅/❌]
**Resultados:** Smoke [..] · Sanity [..] · Regression capa 1 [..] · E2E capa 2 [..]
**Hallazgos abiertos:** [ID — severidad — aceptado por PO / workaround]
**Release notes:** [interna] · [cliente]
**Rollback:** plan verificado ✅ · **Ventana de despliegue:** [fecha hora] con DevOps
```
