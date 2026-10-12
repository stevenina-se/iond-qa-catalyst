# Rechazo de QA — C-14 (`mock testing` → `to do`)

> **Plantilla del QA Catalyst = C-14** de la fuente canónica (§14; copia generada en `templates/comments/C-14.md`; si difieren, prevalece la generada).
> **Borrador en:** `knowledge/L3-tickets/[id-clickup]/comments/C-14-[AAAA-MM-DD].md` · **Skill:** `skills/mock-testing/report.md` · Lo publica el Reviewer QA; luego mueve el ticket a `to do` (Discovery e Improvements) y suma **Rejection_count + 1** (uno por iteración, no por observación; recordatorio A-09).
> La frase **`El resultado de pruebas para este ticket es: RECHAZADO ❌`** es fija: la usan las skills y la auditoría para detectar el veredicto. No se modifica.

## Antes de publicar

- [ ] Cada OBS cita el REQ-ID incumplido de la matriz vigente con `po-vobo` (o el contrato de `prototype review` que la matriz referencia). Implementar algo distinto de lo acordado **sí** es rechazo.
- [ ] Lo no contemplado en la matriz **no** es rechazo: va como ticket nuevo con `fuera-de-matriz` y C-17.
- [ ] Excepción: un hallazgo `urgent` **provocado por el cambio** (regresión, pérdida de datos, seguridad, cobro incorrecto) sí es rechazo aunque no tenga REQ: en el título de la OBS, `Sin REQ (regresión provocada por el cambio)` en lugar de `REQ-[xx]`.
- [ ] QA y Dev coinciden en la interpretación; si no, se escala con C-15 + `escalado-po` en lugar de rechazar.
- [ ] Un requerimiento tardío que el PO exige incluir no es rechazo: vuelve a `to do` con C-08, sin sumar Rejection_count.
- [ ] Evidencia completa (Estándar de QA §8.4) y datos sensibles enmascarados.

## Comentario (copiar en ClickUp)

```markdown
Estimado @[dev]
**El resultado de pruebas para este ticket es: RECHAZADO ❌** — Iteración [N] (Rejection_count → [N])
**Matriz de Requerimientos:** v[N]
### OBS-01 — [urgent/high/normal/low] — REQ-[xx] — Estado: Nuevo / Persistente / Regresión
**Área / Flujo:** [...]
**Pasos:** 1. ...
**Resultado esperado (según REQ-[xx]):** [...]
**Resultado actual:** [...]
**Evidencia:** [...]
---
**Hallazgos fuera de matriz (no son causa de rechazo):** [#id]
**Ambiente / rama / PRs:** [...]
→ TO DO
```

## Cómo completarlo

- **Una sección `### OBS-xx` por observación** (hasta el `---`), ordenadas por severidad: `urgent` → `high` → `normal` → `low`.
- **Severidad = prioridad nativa de ClickUp:**

  | Prioridad | Severidad | Rechaza en `mock testing` |
  |---|---|---|
  | `urgent` | Bloqueante: core roto sin workaround, pérdida o corrupción de datos, seguridad, cobro incorrecto | Siempre |
  | `high` | Funcionalidad importante falla con workaround | Si incumple un REQ |
  | `normal` | Funcionalidad secundaria o UX con impacto moderado | Si incumple un REQ (fuera de matriz → ticket nuevo) |
  | `low` | Cosmético | Solo si incumple un REQ explícito |

- **Estado de la OBS:** *Nuevo* (primera vez) · *Persistente* (reportada en una iteración anterior y sin corregir) · *Regresión* (funcionaba en la iteración anterior y el fix la rompió).
- **Pasos:** numerados, en breadcrumb y desde un estado conocido, con los datos, el usuario y el rol usados (`Company Login > Sidebar: [Módulo] > ...`).
- **Evidencia:** `screenshots/[TC-ID]-[paso].png`, logs, `transaction_id`, request/response.
- **Ambiente / rama / PRs:** ambiente asignado al QA, rama del ticket, build o commit y Merge Request.
- **Pendiente de decisión PO:** si un REQ tiene una duda abierta, no se rechaza por él; se avanza con los demás.
