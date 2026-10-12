# Skill: improvements-triage/triage

> Prepara el triage de QA de los tickets en `backlog` de Improvements: verifica la calidad del reporte (T-02 / T-03), reproduce, busca duplicados y propone la clasificación —tablero, TYPE, prioridad (= severidad en bugs), tags— y si el ticket pasa por `requirements`. Reconoce el carril de hotfix. Improvements `backlog` (**I-01**); §3, §10, §12; `Q-15`, `Q-25`, `Q-28`, `Q-29`, `Q-38`.

## Cuándo usar
- Tablero **Improvements**, estado `backlog` (triage semanal PO + QA, y el LD si hace falta — `Q-28`).
- Ticket con tag `hotfix` (va directo a `to do`): verificación rápida del reporte, sin esperar el triage semanal.
- Frases disparadoras: `Triage del ticket <id>` · `Preparar triage semanal` (todos los tickets en `backlog`).

## Pre-requisitos (gates)
| Check | Si falla |
|---|---|
| Ticket en la lista Improvements (`901717038640`), estado `backlog` (o `to do` con `hotfix`) | PARAR e indicar la skill del estado actual |
| El ticket usa la plantilla T-02 (bug) o T-03 (mejora) | Mapear el contenido a la plantilla y listar lo que falta |
| Se puede acceder a un ambiente para reproducir | Marcar "No reproducido — sin acceso" y seguir con el análisis documental |

## Contexto a cargar
- **L1:** `sdlc-consolidation.md` (§3 clasificación y TYPE, §6 I-01 a I-03, §7.5–7.6, §10, §11, §12, §13 T-02/T-03, §14 C-17 y C-33) · doc 05 (§3.B, §3.D, §7, Anexo B).
- **L2:** módulo vía Iond Subcategory → `subcategory-map.csv` → `L2_MODULE` (edge cases conocidos, reglas de negocio, Impacto Cruzado).
- **L3:** si existe `knowledge/L3-tickets/<id>/` (p. ej. `bug-report.md`); el L3 del ticket origen si el bug nació de un hallazgo `fuera-de-matriz` o `pilot-feedback`.
- **ClickUp:** `getTaskById` (descripción, campos, tags, prioridad, relaciones, comentarios); `searchTasks` en Improvements y Discovery para duplicados; en modo semanal, `searchTasks` con `list_ids = 901717038640` y `status = backlog`.

## Stage 1 — Planning
```
🔄 SIGUIENTE SKILL: improvements-triage/triage — <ticket | semanal>
   Tickets: <n> (<ids>) · con hotfix: <n>
   Ambiente para reproducir: <QA | preprod | producción con company de prueba>
   Output esperado: L3/<id>/triage.md + comments/C-33-<fecha>.md por ticket (+ agenda del triage en el chat)
¿Procedo?
```

## Stage 2 — Execution
Por cada ticket, de uno en uno:
1. **Leer** descripción, campos (TYPE, Project, Iond Subcategory, prioridad), tags (`det-*`, área `iond-*`, `fuera-de-matriz`, `pilot-feedback`, `hotfix`) y relaciones (ticket origen, tarea de Release).
2. **Carril de hotfix (`Q-38`).** Si es un incidente de producción con impacto bloqueante: recomendar TYPE `Bug`, prioridad `urgent`, tags `hotfix` + `det-prod`, paso directo a `to do` (A-17) y apertura con C-32 (la publican el PO o el LQA); se relaciona con la tarea de Release de la versión donde se detectó. Si ya tiene `hotfix`, solo verificar el reporte y avisar que su `mock testing` tiene prioridad.
3. **Calidad del reporte.**
   - *Bug (T-02):* checklist del Anexo B de doc 05 — resumen en una línea · ambiente con producto/versión, ambiente y rama o commit · `det-*` y tag de área · pasos reproducibles con datos y rol (frecuencia si es intermitente) · resultado esperado con REQ-ID o fuente · resultado actual factual · evidencia con datos sensibles enmascarados · impacto y workaround · prioridad según §10 · TYPE, Project e Iond Subcategory; un bug por ticket.
   - *Mejora (T-03):* ¿el criterio breve es verificable antes de que el Dev empiece? Si no, proponer `requirements`.
   - Lo que falte → borrador de comentario al reportante con los datos pedidos.
4. **Duplicados.** `searchTasks` por palabras clave del resumen, módulo y mensaje de error, en Improvements y Discovery; revisar *Edge Cases Conocidos* del L2. Si es duplicado, recomendar `invalid` con C-22 ("duplicado de #id"); decide el PO.
5. **Reproducir** en el ambiente de QA o en el reportado (en producción, solo con la company de prueba y nunca con datos de clientes), manualmente o con Canal 1 según `skills/_shared/evidence.md`. Resultado: `Reproducido` · `Intermitente (x de y)` · `No reproducido` (con los datos que faltan). Evidencia en `screenshots/`.
6. **¿Rompe un REQ vigente?** Buscar la matriz del ticket que introdujo el comportamiento (L3 o descripción en ClickUp). Si existe, citar el REQ-ID en *Resultado esperado*. Si ese ticket **aún no está en `merged`**, no es un bug de backlog: es una observación de su `mock testing` (avisar a QA).
7. **Clasificación (`Q-15`)** — QA propone, el PO aprueba en el triage:
   - *Tablero:* Discovery si cumple alguna condición de §3.1 (regla de negocio, varios módulos o productos, R&D, contrato de API, funcionalidad nueva o refactor estructural); si no, Improvements.
   - *TYPE* (§3.2): `Bug`, `Improvement`, `New Feature` (pequeña y sin regla de negocio → Improvements con `requirements` obligatorio), `Refactor`, `Task`.
   - *Prioridad:* en bugs = **severidad** con la tabla de §10 (`urgent` core roto sin workaround, pérdida de datos, seguridad o cobro incorrecto · `high` con workaround · `normal` secundaria o UX moderada · `low` cosmético), con el motivo. En mejoras la prioridad es de negocio y la define el PO.
   - *Tags:* confirmar `det-*` (fase de detección) y un tag de área `iond-*`; ningún tag legacy (§12.1).
   - *Campos:* Project e Iond Subcategory (si Project = Iond).
8. **¿Requiere `requirements`? (`Q-29`).** Bug → **No**, nunca. Mejora → **Sí** cuando el criterio no cabe en ≤ 3 líneas verificables; toca validaciones (cálculos, permisos, datos persistidos) o mensajes visibles para el usuario; o el TYPE es `New Feature`. Si la T-03 deja dudas que no se resuelven en < 2 h, se señala en el triage y decide el PO.
9. **Bugs de producción (`det-prod`):** proponer el TC de regresión que lo habría detectado, como fila candidata para la hoja "Iond Testing Plan" (E2E maestro), y relacionar el ticket con la tarea de Release de la versión donde se detectó.

## Stage 3 — Reporting
- `knowledge/L3-tickets/<id>/triage.md` con `templates/triage.md`: checklist T-02/T-03, duplicados, reproducción, REQ afectado, clasificación propuesta con su motivo, decisión sobre `requirements`, carril de hotfix y datos pedidos al reportante. Si la carpeta no existe, crearla con `ticket-memory.md` (tablero Improvements, estado `backlog`).
- `comments/C-33-<fecha>.md`: borrador del C-33 con la prioridad, "¿Requiere requirements?" y "Clasificación confirmada: Improvements ✅ / reclasificar a Discovery". Lo publican el PO o el SM tras aprobar la clasificación.
- Borradores adicionales si aplican: pedido de datos al reportante · C-22 sugerido (duplicado; lo publica el PO).
- **Modo semanal:** agenda en el chat para la reunión:

| Ticket | Resumen | TYPE | Prioridad propuesta | ¿`requirements`? | Tablero | Reproducido | Duplicado |
|---|---|---|---|---|---|---|---|

- **Estado destino sugerido** (decide el PO): `to do` · `requirements` (→ `requirements/mini-matrix.md`) · reclasificar a Discovery (`idea/request`) · `invalid` (C-22).

## Reglas
- QA clasifica los bugs según su criterio y **el PO aprueba** en el triage; el PO decide el orden de atención y lo que es `invalid`.
- La prioridad de un bug expresa su severidad con la escala única de §10 (`Q-25`), siempre con el motivo.
- Un bug no pasa por `requirements`: su reporte T-02 es la especificación.
- Nunca se usan datos ni cuentas de clientes para reproducir en producción.
- El MCP es de solo lectura: QA, el PO o el SM actualizan campos, tags y estado.
