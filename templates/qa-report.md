# Reporte de QA — [id-clickup] · [título del ticket] — Iteración [N]

> **Plantilla del QA Catalyst** — cierre de `mock testing` (D-11 / I-07 · Estándar de QA §3, §5, §7 y §8).
> **Se guarda en:** `knowledge/L3-tickets/[id-clickup]/qa-report.md` (desde la segunda iteración, `qa-report-iter[N].md`) · **Skill:** `skills/mock-testing/report.md` · Prepara **C-13** o **C-14**, y un **C-17** por cada hallazgo fuera de matriz.
> La IA sugiere; el Reviewer QA decide y firma el veredicto. No incluye smoke por ticket: el smoke maestro corre una vez por release.

## Información

| Campo | Valor |
|---|---|
| Ticket | [id-clickup] — [título] — [url] |
| Tablero · TYPE · prioridad | Discovery / Improvements · [TYPE] · [prioridad] |
| Project · Iond Subcategory | [...] · [...] |
| Base de validación | Matriz de Requerimientos v[N] (C-06 [AAAA-MM-DD]) · Mini-matriz v[N] · Reporte del bug (T-02) |
| Contrato referenciado | [versión / enlace] · No aplica |
| Ambiente · rama · build/commit · PRs | [ambiente asignado al QA] · [rama] · [commit] · [Merge Request 1–4] |
| Handoff C-09 | [AAAA-MM-DD] — prueba unitaria: [sí / no] |
| Code review de QA | `code-review-qa.md` — [n] TC con ORIGEN `Code review` · No aplica |
| Reviewer QA · QA Points | @[qa] · [n] |
| Iteración · Rejection_count | [N] · [n] |
| Fechas de ejecución | [AAAA-MM-DD] – [AAAA-MM-DD] |

## 1. Criterio de aprobación

| Criterio (Estándar de QA §3) | Resultado | Cumple |
|---|---|---|
| REQ críticos aprobados | [n]/[N] — 100 % requerido | ✅ / ❌ |
| Ningún REQ incumplido | [n] incumplidos | ✅ / ❌ |
| Hallazgos `urgent` abiertos | [n] — 0 requerido | ✅ / ❌ |
| No regresión de zonas cercanas | [n]/[n] | ✅ / ❌ |
| Bug: resultado esperado del reporte (T-02) | [...] | ✅ / ❌ / No aplica |
| Bug: prueba unitaria que certifica la corrección (C-09) | [...] | ✅ / ❌ / No aplica |
| Totales del comentario = `test-matrix.md` | [...] | ✅ |

## 2. Trazabilidad REQ → TC → resultado

| REQ | Crítico | Requerimiento (resumen) | TC | Resultado | Evidencia | OBS |
|---|---|---|---|---|---|---|
| REQ-01 | Sí | [...] | TC-01, TC-02 | ✅ | [ruta / enlace] | — |
| REQ-02 | No | [...] | TC-03 | ❌ | [ruta / enlace] | OBS-01 |
| REQ-03 | Sí | [...] | TC-04 | ⏳ Pendiente de decisión PO | — | — |

**Totales (de `test-matrix.md`):** ejecutados [N] · ✅ [n] · ❌ [n] · ⏭️ [n] (justificación) · ⛔ [n]

## 3. No regresión de zonas cercanas

| TC / NR | Zona o flujo | Por qué podría romperse | Resultado | Evidencia |
|---|---|---|---|---|
| TC-06 | [...] | [archivo o servicio compartido con el cambio] | ✅ / ❌ | [...] |

## 4. Hallazgos que causan rechazo (C-14)

| OBS | Severidad (prioridad) | REQ-ID | Estado | Resumen | TC | Evidencia |
|---|---|---|---|---|---|---|
| OBS-01 | `urgent` / `high` / `normal` / `low` | REQ-[xx] | Nuevo / Persistente / Regresión | [...] | TC-[nn] | [...] |

Severidad = prioridad nativa: `urgent` siempre rechaza; `high` y `normal` rechazan si incumplen un REQ; `low` solo si incumple un REQ explícito.

## 5. Hallazgos fuera de matriz (C-17 — no bloquean)

| # | Observación | Por qué está fuera | Severidad propuesta | Ticket nuevo |
|---|---|---|---|---|
| 1 | [...] | No contemplado en ningún REQ / listado en Fuera de alcance | [prioridad] | T-02 o T-03 con `fuera-de-matriz` — #[id] o pendiente |

> Un `urgent` **preexistente** (no provocado por el cambio) se registra de inmediato como ticket nuevo con `det-mock` y se avisa al PO; no bloquea este ticket.

## 6. Desacuerdos y decisiones del PO

| Punto | Comentarios | Decisión | Efecto |
|---|---|---|---|
| REQ-[xx] / [comportamiento] | C-15 [fecha] · C-16 [fecha] | [...] | Bug del ticket / se acepta / cambio de alcance (C-08) / ticket nuevo |

## 7. Veredicto

| Campo | Valor |
|---|---|
| Sugerencia del catalyst | APROBADO ✅ / RECHAZADO ❌ — [fundamento en 1 línea] |
| **Veredicto del Reviewer QA** | **APROBADO ✅ / RECHAZADO ❌** |
| Estado destino sugerido | `uat` (con `uat-requerido`) · `ready to merge` · `to do` (rechazo; Rejection_count → [N]) · `to do` por cambio de alcance (C-08; sin Rejection_count) |
| Comentarios preparados | `comments/C-13-[fecha].md` / `comments/C-14-[fecha].md` · `comments/C-17-[fecha].md` |
| Acciones de QA en ClickUp | Publicar el comentario · mover el estado · Rejection_count + 1 si rechaza · crear los tickets `fuera-de-matriz` |

## 8. Candidatos para el release y la automatización

| TC | REQ | USO | Automatizable | Propuesta |
|---|---|---|---|---|
| TC-01 | REQ-01 (crítico) | Sanity | Sí | Re-ejecutar en el `sanity` de la versión objetivo |
| TC-04 | REQ-02 | Regresión candidata | Sí | Fila del E2E maestro [E2E-...] o fila nueva en la hoja "Iond Testing Plan" · plan en `skills/automation/plan.md` |

## Evidencia

- Matriz de Pruebas: `test-matrix.md` · `test-matrix.csv`
- Capturas: `screenshots/`
- Queries de BD (solo lectura): [query + resultado pegado por el QA] · No aplica
- Reporte de Playwright (si hubo ejecución automática): [ruta]
