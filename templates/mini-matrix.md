# Mini-matriz v[N] — [id-clickup] · [título del ticket]

> **Plantilla del QA Catalyst** — mini-matriz de Improvements (fuente canónica §9.2 · I-02 · Estándar de QA §3.B).
> **Se guarda en:** `knowledge/L3-tickets/[id-clickup]/requirements-matrix-v[N].md` · **Skill:** `skills/requirements/mini-matrix.md` · **Comentarios:** C-05 · C-06 (+ tag `po-vobo`) · C-07 · C-08.
> Hasta **5 REQ** con el mismo formato de la Matriz de Requerimientos + checklist de no regresión de zonas cercanas. Si supera 5 REQ, toca una regla troncal o impacta varios módulos o productos, QA lo advierte y el **PO** reclasifica el ticket a Discovery (`idea/request`).

## Control (interno de QA — no se copia al ticket)

| Campo | Valor |
|---|---|
| Ticket | [id-clickup] — [título] — [url] |
| Tablero / estado | Improvements · `requirements` |
| Project · Iond Subcategory · TYPE | [Iond / IONMIND / STAGEMIND / Gateway] · [subcategoría] · [Improvement / New Feature pequeña / Refactor / Task] |
| Motivo para pasar por `requirements` (`Q-29`) | [ ] El criterio no cabe en ≤ 3 líneas verificables · [ ] Toca validaciones (cálculos, permisos, datos persistidos) o mensajes visibles para el usuario · [ ] TYPE `New Feature` (obligatorio) |
| Versión · VoBo | v[N] · Borrador / C-05 [AAAA-MM-DD] / C-06 [AAAA-MM-DD] + `po-vobo` |
| Reviewer QA | @[qa] |
| SLA | QA 1 día hábil · VoBo 24 h hábiles |

<!-- ===== INICIO: copiar en la descripción del ticket ===== -->

## Matriz de Requerimientos v[N]

> Mini-matriz (Improvements). Parte de la T-03: situación actual, mejora propuesta, criterio de aceptación breve y fuera de alcance.

| ID | Módulo / Servicio | Requerimiento / Regla | ¿Cuándo aplica? (condición) | ¿Qué debe pasar? (resultado) | Excepciones / Fuera de alcance | Crítico |
|---|---|---|---|---|---|---|
| REQ-01 | [Iond Subcategory o servicio] | [Una regla en una frase] | [Rol, estado previo, datos o disparador] | [Resultado observable y verificable] | [Casos NO considerados] | Sí / No |
| REQ-02 | [...] | [...] | [...] | [...] | [...] | Sí / No |

**Fuera de alcance de la entrega:** [...]

### Checklist de no regresión de zonas cercanas

3 a 5 verificaciones del módulo y de los flujos que comparten el código modificado:

- [ ] NR-01 — [flujo o pantalla vecina] — [resultado esperado]
- [ ] NR-02 — [...] — [...]
- [ ] NR-03 — [...] — [...]

### Datos de prueba

- **Companies, usuarios y roles:** [...]
- **Mocks, sandbox o datos especiales:** [...]
- **Ambiente:** [ambiente asignado al QA, con la rama del ticket] (`Q-05`)

<!-- ===== FIN: copiar en la descripción del ticket ===== -->

## Checklist de acuse (checklist del ticket en ClickUp)

- [ ] Mini-matriz vN leída por el Dev

## Historial de versiones

| Versión | Fecha | Cambio | Filas afectadas | VoBo (C-06) |
|---|---|---|---|---|
| v1 | [AAAA-MM-DD] | Versión inicial | — | [Pendiente / AAAA-MM-DD] |

> Las reglas de VoBo, cambio de alcance y versionado son las de la Matriz de Requerimientos (`templates/requirements-matrix.md`). En `mock testing` la mejora se aprueba con la mini-matriz aprobada y el checklist de no regresión en verde.
