# Notas de QA en `pilot presentation` — [id-clickup] · [título del ticket]

> **Plantilla del QA Catalyst** — clasificación de los ajustes del Pilot (D-08 · `Q-11` · Estándar de QA §3.A). Solo la **primera vez**: tras un rechazo de QA el ticket no vuelve a `pilot presentation`.
> **Se guarda en:** `knowledge/L3-tickets/[id-clickup]/pilot-notes.md`. Uso directo de QA para apoyar al SM en el acta **C-10** (la publica el SM). Si un ajuste es cambio de alcance, sigue `skills/requirements/matrix.md` (v+1, C-08).
> QA contrasta cada ajuste con la Matriz de Requerimientos vigente; el PO decide qué es imprescindible.

## Datos

| Campo | Valor |
|---|---|
| Ticket | [id-clickup] — [título] — [url] |
| Fecha | [AAAA-MM-DD] |
| Asistentes (roles) | SH · PO · LD · QA · Dev |
| Matriz vigente | v[N] (VoBo C-06 [AAAA-MM-DD]) |
| Ambiente de la demo | [local / dev] — rama [...] |

## Ajustes

| # | Ajuste solicitado | Rol que lo pide | ¿Lo regula un REQ? | Tipo | Tratamiento | Referencia |
|---|---|---|---|---|---|---|
| 1 | [...] | SH / PO | REQ-[xx] / No | Contradice matriz | Corregir en el ticket (vuelve a `dev in progress`) | — |
| 2 | [...] | SH / PO | No | Nuevo imprescindible | Cambio de alcance: matriz v+1, `cambio-alcance`, C-08 y nuevo VoBo (C-06) antes de tocar el código | C-08 [fecha] |
| 3 | [...] | SH / PO | No | Nuevo no imprescindible | Ticket nuevo en Improvements con `pilot-feedback`, enlazado al padre (lo crea el SM) | #[id] |

**Reglas de clasificación (`Q-11`):**
- **Contradice la matriz** → se corrige dentro del ticket.
- **Nuevo e imprescindible** para el valor mínimo (lo decide el PO) → cambio de alcance.
- **Nuevo y no imprescindible** → ticket nuevo con `pilot-feedback`.
- Si no hay acuerdo sobre si un ajuste contradice la matriz → C-15 + `escalado-po`; el PO decide (C-16).

**Visto bueno preliminar del PO/SH:** ✅ / ⚠️ con ajustes

## Borrador para el acta C-10 (lo publica el SM)

Texto de `templates/comments/C-10.md` (generado desde la fuente canónica; si difieren, prevalece el generado):

```markdown
## 🎬 PILOT PRESENTATION — ACTA
**Asistentes:** SH · PO · LD · QA · Dev
**Visto bueno preliminar:** ✅ / ⚠️ con ajustes
**Ajustes:**
| # | Ajuste | Tipo | Tratamiento |
|---|---|---|---|
| 1 | [...] | Contradice matriz / Nuevo imprescindible / Nuevo no imprescindible | Corregir en ticket / Cambio de alcance (C-08) / Ticket nuevo #[id] (`pilot-feedback`) |
→ CODE REVIEW
```
