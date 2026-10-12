# Aprobación de QA — C-13 (`mock testing` → `uat` / `ready to merge`)

> **Plantilla del QA Catalyst = C-13** de la fuente canónica (§14; copia generada en `templates/comments/C-13.md`; si difieren, prevalece la generada).
> **Borrador en:** `knowledge/L3-tickets/[id-clickup]/comments/C-13-[AAAA-MM-DD].md` · **Skill:** `skills/mock-testing/report.md` · Lo publica el Reviewer QA en el ticket antes de mover el estado.
> La frase **`El resultado de pruebas para este ticket es: APROBADO ✅`** es fija: la usan las skills y la auditoría para detectar el veredicto. No se modifica.

## Antes de publicar

- [ ] 100 % de los REQ críticos aprobados, ningún REQ incumplido y cero hallazgos `urgent` abiertos.
- [ ] No regresión de zonas cercanas en verde.
- [ ] Totales iguales a los de `test-matrix.md` (⏭️ solo con justificación).
- [ ] Cada hallazgo fuera de matriz tiene su ticket con `fuera-de-matriz` y su C-17 publicado.
- [ ] Destino: `uat` si el ticket tiene `uat-requerido` (solo Discovery); si no, `ready to merge`.
- [ ] Bug (Improvements): resultado esperado del reporte cumplido, prueba unitaria mencionada en el C-09 y checklist de no regresión en verde.

## Comentario (copiar en ClickUp)

```markdown
Estimado @[dev]
**El resultado de pruebas para este ticket es: APROBADO ✅**
**Matriz de Requerimientos:** v[N] (VoBo PO ✅)
| REQ | Resultado | Evidencia |
|---|---|---|
| REQ-01 | ✅ | [link] |
**TCs ejecutados:** [N] — ✅ [n] · ❌ 0 · ⏭️ [n] (justificación)
**Regresión de zonas cercanas:** ✅
**Hallazgos fuera de matriz (no bloquean):** [#id — `fuera-de-matriz`] / Ninguno
**Ambiente / rama / PRs:** [...]
→ [UAT | READY TO MERGE]
```

## Cómo completarlo

- **Tabla REQ:** una fila por REQ (los críticos primero). La evidencia enlaza la captura o la fila de `qa-report.md`.
- **Mini-matriz (Improvements):** `**Matriz de Requerimientos:** v[N] (mini-matriz, VoBo PO ✅)`.
- **Bug sin matriz:** `**Matriz de Requerimientos:** No aplica — bug (T-02)`; la tabla lleva una fila `Resultado esperado (T-02)` y otra `Prueba unitaria (C-09)`.
- **Re-test:** el veredicto cubre la iteración vigente; el detalle de las OBS corregidas va en `qa-report-iter[N].md`.
- El detalle (TC por REQ, evidencia, code review de QA) vive en `qa-report.md`; no se copia en el comentario.
