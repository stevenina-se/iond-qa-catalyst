# Sanity — [producto] v[X.Y.Z]

> **Plantilla del QA Catalyst** — sanity de la versión (REL-04 · `Q-48` · fuente canónica §7.7 y §9.4 · Estándar de QA §6.2).
> **Se guarda en:** `knowledge/releases/[producto]/v[X.Y.Z]/sanity-matrix.md` · **Skill:** `skills/release/sanity.md` · Comentario **C-26**.
> Re-ejecuta en preprod los TC de los **REQ críticos** de cada ticket del release (de su Matriz de Pruebas) y las interacciones entre tickets del mismo módulo o Iond Subcategory. **Criterio de salida:** 100 % de los REQ críticos aprobados por ticket, sin efectos colaterales. Timebox ≤ 1,5 días (martes – miércoles).

## Encabezado

| Campo | Valor |
|---|---|
| Producto / versión | [iond / IonMind / StageMind] v[X.Y.Z] |
| Ambiente · build | preprod · [commit RC] |
| Fechas | [AAAA-MM-DD] – [AAAA-MM-DD] |
| QA | @[qa] · @[qa] |
| Smoke previo | `smoke-preprod.md` — core ✅ (o áreas excluidas: [...]) |
| Tarea de Release | [Release producto - vX.Y.Z] — [url] |

## Resumen por ticket

| Ticket | Título | Iond Subcategory | Matriz | REQ críticos | ✅ | ❌ | ⏭️ | Estado |
|---|---|---|---|---|---|---|---|---|
| #[id] | [...] | [...] | v[N] | [n] | [n] | [n] | [n] | ✅ / ❌ |

## Matriz por ticket

ID = `SAN-[ticket]-[REQ]`. Un REQ crítico sin TC → se crea el TC mínimo (Happy Path) y se marca *Brecha de matriz*. En un bug, el ID usa `T-02` (resultado esperado del reporte) y se suma su no regresión de zonas cercanas.

| ID | Ticket | REQ crítico | TC (Matriz de Pruebas) | Verificación | Resultado esperado | Resultado | Evidencia | Observación |
|---|---|---|---|---|---|---|---|---|
| SAN-[ticket]-REQ-01 | #[id] | REQ-01 | TC-01, TC-02 | [...] | [según REQ-01, matriz v[N]] | ✅ / ❌ / ⏭️ | [ruta] | |
| SAN-[ticket]-REQ-03 | #[id] | REQ-03 | TC-04 | [...] | [...] | | | |
| SAN-[ticket]-T-02 | #[id] (bug) | Resultado esperado (T-02) | TC-01 | [...] | [...] | | | |

## Interacciones entre tickets

Pares de tickets con la misma Iond Subcategory o el mismo módulo L2: 1 a 3 verificaciones del flujo combinado.

| ID | Tickets | Módulo / Subcategory compartido | Flujo combinado | Resultado esperado | Resultado | Evidencia |
|---|---|---|---|---|---|---|
| SAN-INT-01 | #[id] + #[id] | [...] | [...] | [...] | ✅ / ❌ | |

## Hallazgos

| ID | Fila | Ticket origen | Severidad | Causa | Decisión | Ticket / subtarea |
|---|---|---|---|---|---|---|
| [...] | SAN-[...] | #[id] | `urgent` / `high` / `normal` / `low` | Ticket / integración entre tickets | Fix-forward (C-28) / Improvements con `det-sanity` / revertir con `diferido` | #[id] |

> `urgent` → fix-forward en la rama RC (decisión ≤ 4 h, fix ≤ 1 día) y QA re-ejecuta el REQ afectado. El resto, previa discusión con PO y LD, va a `backlog`. Un hallazgo fuera de matriz no bloquea el ticket salvo regresión `urgent` provocada por el release.

## Candidatos a regresión y automatización

| TC | Ticket / REQ | Motivo | Propuesta |
|---|---|---|---|
| TC-[nn] | #[id] / REQ-[xx] | Estable y se repite en varios releases | Fila del E2E maestro (hoja "Iond Testing Plan") / automatizar (`skills/automation/plan.md`) |

## Borrador C-26

Texto de `templates/comments/C-26.md`; la línea *Por ticket* agrega el detalle que pide el Estándar de QA §6.2:

```markdown
## 🧪 SANITY — [producto vX.Y.Z] — [✅ / ❌]
**Ejecutados:** [N] · ✅ [n] · ❌ [n] · ⏭️ [n] · **Automatizados:** [n]
**Hallazgos:** [ID — severidad — decisión: fix-forward / Improvements #id / diferido]
**Evidencia / matriz:** [link]
**Por ticket:** #[id] — REQ-01 ✅ · REQ-03 ✅ | #[id] — REQ-02 ❌ (fix-forward)
```
