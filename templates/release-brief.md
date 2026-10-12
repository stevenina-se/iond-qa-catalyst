# Brief del release — [producto] v[X.Y.Z]

> **Plantilla del QA Catalyst** — resumen de una página para stakeholders y líderes (fuente canónica §7).
> **Se guarda en:** `knowledge/releases/[producto]/v[X.Y.Z]/brief.md` · **Skill:** `skills/release/brief.md`. Se regenera al cerrar cada suite y no reemplaza a los comentarios C-23 a C-31 de la tarea de Release.
> Lenguaje no técnico: sin IDs de PR ni detalles de código, y sin nombres de personas (solo roles).

**Estado de la tarea:** `[dev preparation / unit test & ci / smoke / sanity / regression / ready for release]` · **Actualizado:** [AAAA-MM-DD hh:mm] · **Go/No-Go:** viernes [AAAA-MM-DD] 10:00

## Alcance

[2–3 líneas: qué cambia en esta versión y para quién]

| Dato | Valor |
|---|---|
| Tickets incluidos | [N] — New Feature [n] · Improvement [n] · Bug [n] · Refactor [n] · Task [n] |
| Módulos | [Boards (n) · Billing (n) · PDF Templates (n) · ...] |
| Diferidos | [n] — [motivo en lenguaje simple] · Ninguno |

## Riesgo

**[Alto / Medio / Bajo]** — [motivo]. Dependencias con otros productos: [orden de despliegue StageMind → IonMind → iond] · Ninguna.

## Avance por suite

| Paso | Suite | Estado | Resultado | Nota |
|---|---|---|---|---|
| 1 | Smoke maestro (preprod) | ⬜ Pendiente / 🔄 En curso / ✅ / ❌ | [n/n] | Gate del release |
| 2 | Sanity (REQ críticos de cada ticket) | | [n/n] | |
| 3 | Regression capa 1 (por riesgo) | | Flujos críticos [n/n] | |
| 4 | E2E maestro capa 2 | | Automatizado [n/n] · rotación G[n] [n/n] | |
| 5 | Go/No-Go | | GO / CONDITIONAL GO / NO-GO | Quórum PO + LQA + RM |
| 6 | Smoke en producción | | [n/n] | ≤ 2 h tras el despliegue |

## Hallazgos

| Severidad | Abiertos | Tratamiento |
|---|---|---|
| `urgent` | [n] | Corrección en la versión (fix-forward) o retiro del cambio |
| `high` | [n] | Requiere aceptación del riesgo por el PO |
| `normal` / `low` | [n] | Mejoras programadas en Improvements |

## Decisión y despliegue

**Decisión:** [pendiente / GO / CONDITIONAL GO / NO-GO] · **Ventana:** [AAAA-MM-DD hh:mm] con DevOps · **Release notes:** [interna] · [cliente]

## Pendientes y bloqueos

| Pendiente | Responsable (rol) | Fecha |
|---|---|---|
| [...] | RM / LD / LQA / QA / PO / SM | [AAAA-MM-DD] |

## Texto corto para el canal del equipo (≤ 10 líneas)

```text
📦 [producto] v[X.Y.Z] — [estado]
Alcance: [N] cambios ([n] nuevas funcionalidades, [n] correcciones, [n] mejoras)
Riesgo: [Alto/Medio/Bajo] — [motivo breve]
Smoke [✅/❌/⬜] · Sanity [✅/❌/⬜] · Regresión [✅/❌/⬜] · E2E [✅/❌/⬜]
Hallazgos abiertos: [n] ([n] high)
Go/No-Go: viernes [fecha] 10:00 · Ventana: [fecha hora]
```
