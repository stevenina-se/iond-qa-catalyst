# Matriz de Requerimientos v[N] — [id-clickup] · [título del ticket]

> **Plantilla del QA Catalyst** — Matriz de Requerimientos (fuente canónica §9.1 · D-05 / I-02 · Estándar de QA §4).
> **Se guarda en:** `knowledge/L3-tickets/[id-clickup]/requirements-matrix-v[N].md` · **Skill:** `skills/requirements/matrix.md` · **Comentarios:** C-05 (solicitud de VoBo) · C-06 (VoBo del PO) · C-07 (dudas del Dev) · C-08 (cambio de alcance).
> QA redacta con el apoyo técnico del Dev; el PO valida la matriz completa con **un único comentario de VoBo** (sin aprobación fila por fila). La sección entre los marcadores `INICIO` y `FIN` se copia en la descripción del ticket, debajo de la especificación del PO.

## Control (interno de QA — no se copia al ticket)

| Campo | Valor |
|---|---|
| Ticket | [id-clickup] — [título] — [url] |
| Tablero / estado | Discovery · `requirements` / Improvements · `requirements` |
| Project · Iond Subcategory · TYPE | [Iond / IONMIND / STAGEMIND / Gateway] · [subcategoría] · [New Feature / Improvement / Refactor / Task] |
| Versión de la matriz | v[N] |
| Estado del VoBo | Borrador · Enviada a VoBo (C-05 [AAAA-MM-DD]) · VoBo ✅ (C-06 [AAAA-MM-DD] + tag `po-vobo`) · v+1 pendiente de VoBo (`cambio-alcance`, C-08) |
| Contrato de `prototype review` | [versión / enlace aprobado en C-04] · No aplica |
| Reviewer QA · QA Points | @[qa] · [1 / 2 / 3 / 5 / 8] (se registra al salir de `requirements`) |
| UAT | Propuesta de QA: [Sí / No] — decide el PO (tag `uat-requerido`; solo Discovery) |
| Acuse del Dev | [ ] Checklist del ticket "Matriz de Requerimientos vN leída por el Dev" marcado |
| SLA | Matriz: 1 día hábil (S/M) · 2–3 días (L) · VoBo: 24 h hábiles (a las 24 h se vuelve a mencionar al PO; a las 48 h → `blocked` con `bloq-definicion`) |

<!-- ===== INICIO: copiar en la descripción del ticket ===== -->

## Matriz de Requerimientos v[N]

> Parte de la especificación del PO (historia, criterios de aceptación y fuera de alcance) y del contrato aprobado en `prototype review`: [versión / enlace]. El contrato referenciado forma parte del criterio de aceptación.

| ID | Módulo / Servicio | Requerimiento / Regla | ¿Cuándo aplica? (condición) | ¿Qué debe pasar? (resultado) | Excepciones / Fuera de alcance | Crítico |
|---|---|---|---|---|---|---|
| REQ-01 | [Iond Subcategory o servicio] | [Una regla funcional o de negocio, en una frase] | [Rol, estado previo, datos o disparador] | [Valor, estado, mensaje, código de respuesta o registro verificable] | [Casos NO considerados en esta entrega] | Sí / No |
| REQ-02 | [...] | [...] | [...] | [...] | [...] | Sí / No |
| REQ-NF-01 | [módulo / servicio] | [Rendimiento / seguridad / compatibilidad / resiliencia / observabilidad] | [Ambiente, volumen y datos de la medición] | [Métrica y umbral, p. ej. p95 ≤ [n] s en [n] solicitudes] | [...] | Sí / No |

**Fuera de alcance de la entrega:** [caso 1] · [caso 2] · [...]

**Trazabilidad con la especificación del PO:** `CA-1 → REQ-01, REQ-02` · `CA-2 → REQ-03` · completados por QA: `REQ-0[x]`, `REQ-NF-01`.

**Pendientes de decisión del PO:** REQ-[xx] — *Pendiente de decisión PO* (no es criterio de rechazo mientras el PO no decida en C-06 o C-16).

### Datos de prueba

- **Companies, usuarios y roles:** [...]
- **Estados iniciales:** [...]
- **Mocks y sandboxes:** [p. ej. proveedor de pagos en modo sandbox; integración sin sandbox → mock, colección simulada o cuenta de prueba]
- **Archivos o corpus:** [...]
- **Mecanismos especiales:** [p. ej. simular la fecha de renovación]
- **Ambiente:** [ambiente asignado al QA, con la rama del ticket] (`Q-05`)
- **Quién prepara cada dato:** [QA / Dev — seeds o migraciones, informado en C-09]

<!-- ===== FIN: copiar en la descripción del ticket ===== -->

## Variantes (conservar solo la que aplique)

**Épica con subtareas (`Q-12`).** Una sola matriz en el ticket padre, con las mismas columnas. Los REQ se agrupan por subtarea con su código corto: `REQ-[SUB]-01` (p. ej. `REQ-API-01`, `REQ-UI-01`). Debajo de la tabla: `Subtareas: API = #[id] · UI = #[id]`. Las subtareas cierran en `done w/d` sin QA individual; QA valida en el padre.

**Salida de IA — IonMind, StageMind o nodos con IA (`Q-24`).** El "¿Qué debe pasar?" se escribe con umbral medible: *"[resultado] en ≥ [n] % de un corpus de [N] casos de referencia ([composición]), evaluado por [método]"*. Cada REQ de IA define:

- [ ] Corpus versionado (tamaño y composición), congelado antes del VoBo y reutilizado en `sanity` y `regression`.
- [ ] Métrica y umbral · método de evaluación (automático o revisión visual con checklist).
- [ ] Quién revisa los casos dudosos (PO o SH).
- [ ] Número de ejecuciones si la salida no es determinista (el umbral se cumple en cada una).
- [ ] Versión del modelo o del prompt registrada · excepciones.

**Refactor o POC (`Q-13`).** Refactor: la matriz declara *"Sin cambio funcional"*; los REQ listan los flujos que deben comportarse igual que antes y los REQ-NF fijan la métrica que no puede empeorar. POC: los REQ describen la pregunta que se debe responder y el criterio de éxito.

## Checklist antes de pedir VoBo (Estándar de QA, Anexo A)

1. [ ] Cada criterio del PO está mapeado a uno o más REQ-IDs, sin reescribir lo que ya era claro (`Q-19`).
2. [ ] Una sola regla por fila, ID único y versión en el título (`## Matriz de Requerimientos vN`).
3. [ ] Cada "¿Cuándo aplica?" indica rol, estado previo o datos que disparan la regla.
4. [ ] Cada "¿Qué debe pasar?" es observable y verificable; sin "correctamente", "rápido" ni "adecuado".
5. [ ] Columna *Excepciones / Fuera de alcance* completa y bloque de fuera de alcance de la entrega presente.
6. [ ] Heurística de completitud aplicada: permisos, estados previos, límites, datos vacíos o inválidos, errores externos, idempotencia, aislamiento entre companies, impacto cruzado (iond ↔ IonMind ↔ StageMind), compatibilidad con datos existentes.
7. [ ] REQ críticos marcados (cobro incorrecto, pérdida de datos, permisos, flujo core, contrato con otro sistema, esencial para el PO).
8. [ ] No funcionales con métrica (`REQ-NF`); IA con corpus, umbral y método; épicas agrupadas por subtarea.
9. [ ] Contrato de `prototype review` referenciado (si aplica) y `### Datos de prueba` completo.
10. [ ] Reglas indefinidas listadas para el C-05 con opción recomendada; propuesta de `uat`; QA no decidió ninguna regla de negocio por su cuenta.

## Historial de versiones

| Versión | Fecha | Cambio | Filas afectadas | Solicitado por | VoBo (C-06) |
|---|---|---|---|---|---|
| v1 | [AAAA-MM-DD] | Versión inicial | — | — | [Pendiente / AAAA-MM-DD] |
| v[N+1] | [AAAA-MM-DD] | [Motivo] | REQ-[xx] (modificada) · REQ-[yy] (*Eliminado en v[N+1]*) | PO (C-08) | [AAAA-MM-DD] |

**Reglas de versión:**
- Los ajustes que pide el PO antes del VoBo generan v+1.
- Después del VoBo, solo el PO solicita o aprueba cambios: QA publica la v+1 con las filas marcadas y el C-08 (tabla Antes / Ahora), agrega `cambio-alcance` (A-04 retira `po-vobo`), el PO da un nuevo VoBo (C-06), QA vuelve a agregar `po-vobo` y **solo entonces** se modifica el código.
- Una respuesta a una duda del Dev que no altera la condición, el resultado ni el alcance es una aclaración (comentario, sin nueva versión).
- Las filas eliminadas se marcan *Eliminado en vN*; su ID no se reutiliza.
