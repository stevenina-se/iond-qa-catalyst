# Triage — [id-clickup] · [título del ticket]

> **Plantilla del QA Catalyst** — triage de Improvements `backlog` (I-01 · `Q-15`, `Q-28`, `Q-29` · Estándar de QA §3.B y Anexo B).
> **Se guarda en:** `knowledge/L3-tickets/[id-clickup]/triage.md` · **Skill:** `skills/improvements-triage/triage.md` · Comentario **C-33** (lo publica el PO o el SM en el triage semanal: PO + QA; LD si hace falta).
> QA clasifica (tablero, TYPE y prioridad = severidad); el **PO aprueba**. Un incidente de producción con `hotfix` no pasa por triage: va directo a `to do` (C-32).

## Ficha

| Campo | Valor |
|---|---|
| Ticket | [id-clickup] — [título] — [url] |
| Registrado por | QA / Dev / PO / soporte general de la empresa (Form) |
| Plantilla | T-02 (bug) / T-03 (mejora) |
| Fecha de triage | [AAAA-MM-DD] |

## 1. Calidad del reporte

**Bug (T-02 — Anexo B):**
1. [ ] Resumen en una línea: qué falla y dónde.
2. [ ] Ambiente: producto y versión, ambiente y rama o commit.
3. [ ] Tag de detección `det-*` y, en iond, tag de área (`iond-core` / `iond-uxui` / `iond-infra` / `iond-ia`).
4. [ ] Pasos numerados y reproducibles, con datos y rol; frecuencia si es intermitente.
5. [ ] Resultado esperado con el REQ-ID si existe, o la fuente del esperado.
6. [ ] Resultado actual factual.
7. [ ] Evidencia con datos sensibles enmascarados.
8. [ ] Impacto y workaround.
9. [ ] Prioridad (= severidad) según la tabla de severidad.
10. [ ] TYPE `Bug`, Project e Iond Subcategory (si Project = Iond); un bug por ticket.

**Mejora (T-03):**
- [ ] Situación actual y mejora propuesta claras.
- [ ] Criterio de aceptación breve verificable antes de que el Dev empiece (si no lo es, pasa por `requirements`).
- [ ] Fuera de alcance indicado.

**Faltantes a pedir al autor:** [...] / Ninguno

## 2. Clasificación propuesta por QA

| Aspecto | Propuesta | Motivo |
|---|---|---|
| Tablero | Improvements / reclasificar a Discovery | Discovery si crea o cambia una regla de negocio, impacta más de un módulo, servicio, repo o producto, requiere R&D o cambio de contrato de API, o es funcionalidad nueva o estructural |
| TYPE | `Bug` / `Improvement` / `New Feature` / `Refactor` / `Task` | [...] |
| Prioridad | `urgent` / `high` / `normal` / `low` | Bug = severidad: bloqueante / con workaround / impacto moderado / cosmético |
| Project · Iond Subcategory | [...] · [...] | |
| Tags | `det-*` · área `iond-*` · `fuera-de-matriz` / `pilot-feedback` (si aplica) | |
| Duplicado | No / Sí → #[id] (el PO decide `invalid` con C-22) | |
| REQ de una matriz vigente | REQ-[xx] del ticket #[id] / Ninguno | |
| ¿Requiere `requirements`? (`Q-29`) | Sí / No | Bug → nunca. Mejora → Sí si el criterio no cabe en ≤ 3 líneas verificables, toca validaciones (cálculos, permisos, datos persistidos) o mensajes visibles para el usuario, o el TYPE es `New Feature`. Dudas de la T-03 que no se resuelven en < 2 h → se señalan y decide el PO |
| Estado destino sugerido | `to do` / `requirements` / reclasificar a Discovery (`idea/request`) / `invalid` | Decide el PO |

## 3. Decisión del triage (PO)

| Campo | Valor |
|---|---|
| Clasificación | Aprobada / ajustada: [...] |
| Prioridad final | [...] |
| Destino | `to do` / `requirements` / Discovery / `invalid` |

## 4. Borrador C-33

Texto de `templates/comments/C-33.md` (generado desde la fuente canónica; si difieren, prevalece el generado):

```markdown
## 🗂️ TRIAGE
**Prioridad:** [..] (bug = severidad) · **¿Requiere requirements?:** Sí / No
**Clasificación confirmada:** Improvements ✅ / reclasificar a Discovery
```
