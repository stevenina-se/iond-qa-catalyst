# Skill: prototype-review/review

> Prepara y registra el aporte de QA en `prototype review` (Discovery, **D-04**): testabilidad del prototipo y del contrato de interfaz, riesgos, requisitos no funcionales, datos de prueba, dependencias, preguntas al PO y al Dev/LD, y la captura inicial de requerimientos que alimenta `requirements`. Reglas: `Q-08`, `Q-09`, `Q-10`, `Q-12`, `Q-13`, `Q-20`, `Q-24`, `Q-27`.

## Cuándo usar
- Tablero **Discovery**, estado `prototype review` (reunión obligatoria PO + Dev + QA + LD). También en `r, d & architect review` cuando el C-03 ya está aprobado por el LD, para preparar la reunión.
- **Modo anticipado (opcional):** en `idea/request`, `assignment` o `r, d & architect review` sin C-03, para llevar riesgos y preguntas al refinamiento (*Discovery Review*). Solo ejecuta los pasos 1, 5, 6, 9 y 10; el resto se completa al llegar a `prototype review`.
- Frase disparadora: `Prototype review del ticket <id>` (modo anticipado: `Riesgos anticipados del ticket <id>`)

## Pre-requisitos (gates)
| Check | Si falla |
|---|---|
| El ticket está en Discovery, en `prototype review` o en `r, d & architect review` con C-03 aprobado (o en un estado previo, en modo anticipado) | PARAR. Indicar la skill que corresponde al estado (tabla de enrutamiento del `SKILL.md`) |
| Existe el C-03 (R&D concluido, aprobación del LD) | Modo anticipado. Si el ticket ya está en `prototype review` sin C-03: avisar a QA (no hay repos, contrato borrador ni NFR), seguir solo con su confirmación y registrar el vacío |
| El prototipo está disponible según el tipo de ticket (`Q-09`) | Registrar "prototipo no disponible" como pendiente para el acta C-04; el PO decide si la reunión sigue |
| La T-01 tiene TYPE, Project e Iond Subcategory (si Project = Iond) | Señalarlo como punto para el PO; no bloquea el análisis |
| Existe el L2 del módulo | Avisar que el L2 falta (crearlo desde `knowledge/L2-modules/_template.md`) y continuar con L1 |

## Contexto a cargar
- **L1:** `knowledge/L1-project/sdlc-consolidation.md` (§5 D-03 a D-05, §9.1, §10, §12, §14 C-03/C-04/C-05) · `docs/sdlc-iond/src/05-estandar-operativo-qa-iond.md` (§3.A checklist de testabilidad, §4.3 heurística de completitud, §4.5 a §4.9) · `business-rules.md`, `test-priorities.md`, `api-architecture.md`, `stack-overview.md`.
- **L2:** Iond Subcategory → `knowledge/test-suites/_config/subcategory-map.csv` → `L2_MODULE` (y `CROSS_SYSTEM`). Leer `module.md`: reglas de negocio, Database, Impacto Cruzado, archivos centinela, edge cases conocidos.
- **L3:** `knowledge/L3-tickets/<id>/ticket-memory.md` (crearlo desde `templates/ticket-memory.md` si no existe).
- **ClickUp** (`skills/_shared/clickup.md`): `getTaskById` → descripción T-01, campos, subtareas (spikes en `done w/d`) y comentarios C-01, C-02, C-03 y posteriores.

## Stage 1 — Planning
Anunciar con el protocolo Announce → Confirm → Act del `SKILL.md` raíz:
```
🔄 SIGUIENTE SKILL: prototype-review/review
   Ticket: <id> — <título> · Discovery · `<estado>` · TYPE <..> · Iond Subcategory <..>
   Prerequisitos: ✅/❌ C-03 · ✅/❌ prototipo (<tipo Q-09>) · ✅/❌ L2 <módulo>
   Code review del prototipo: ¿lo hago? (opcional — requiere rama o PR)
   Output esperado: L3/<id>/prototype-review-qa.md + comments/C-04-<fecha>.md (aporte de QA al acta)
¿Procedo?
```
Esperar confirmación explícita.

## Stage 2 — Execution
1. **Leer y reconciliar la especificación.** De la T-01: problema, historia de usuario, criterios de alto nivel (numerarlos `CA-1…`), fuera de alcance preliminar. Del C-03: opciones, recomendación, repos afectados, contrato borrador, dependencias, riesgos y NFR. De los comentarios posteriores: decisiones que cambian el alcance. Registrar cada decisión en una tabla `Decisión | Fuente (comentario, fecha, autor) | Efecto en la especificación`. QA no resuelve contradicciones: las convierte en preguntas al PO.
2. **Contrastar el prototipo con lo esperado para su tipo (`Q-09`):** UI/UX → wireframe o mock navegable · API/backend → contrato OpenAPI con endpoints, request/response, códigos de error y límites · Integración → diseño del board/flow, mapeo de datos y manejo de errores · IA → dataset de ejemplo, salida esperada y criterio de calidad medible · Refactor/técnico → arquitectura actual vs. propuesta y NFR que se preservan. Anotar qué falta.
3. **Checklist de testabilidad** (doc 05 §3.A), cada punto `Sí / No / Parcial` + observación: resultado observable (UI, respuesta de API, historial, log con `transaction_id`) · ambiente y datos preparables (sandbox, mocks, companies de prueba — `Q-05`) · contrato versionado para referenciarlo desde la matriz (`Q-10`) · dependencias a simular · en IA, corpus y criterio medible (`Q-24`) · NFR con métrica.
4. **Checklist técnico** de `templates/architecture-brief-qa.md` sobre el C-03 y el prototipo (contrato, permisos por company, validación de entradas, multi-company, migraciones reversibles y datos existentes, rollback, observabilidad, rendimiento, impacto en la ejecución de boards/nodos), cada punto ✅ / ⚠️ / ❌ / N/A. Va como anexo de `prototype-review-qa.md`; en tickets L o con cambios de contrato o de BD, como archivo aparte `architecture-brief-qa.md`.
5. **Análisis de riesgo** (con L1 + L2 + C-03, sin inventar):
   - *Lógica de negocio:* aislamiento entre companies · ejecución de boards y nodos · App Connectors globales vs. de company · datos persistentes (PostgreSQL) vs. de ejecución (SQLite) · permisos · billing y consumo · flujos cross-system iond ↔ IonMind ↔ StageMind ↔ Gateway.
   - *Impacto por capa:* Frontend (`gateway-ion`) · API (`flow_binaries` / `gateway`) · Canvas (`webcomponents-flow`) · BD PostgreSQL · BD SQLite · otros módulos (Impacto Cruzado del L2). Riesgo **Alto / Medio / Bajo** con justificación.
   - *Tabla de riesgos* `R-01…` con área, descripción, prioridad de validación y por qué.
6. **Heurística de completitud** (doc 05 §4.3) → casos borde candidatos: roles y permisos · estados previos · límites (0, exacto, máximo, ilimitado) · datos vacíos, inválidos o duplicados · errores y timeouts externos · concurrencia e idempotencia · aislamiento entre companies · impacto cruzado · datos existentes y compatibilidad.
7. **Captura inicial de requerimientos** (borrador, no es la matriz): `CA-n → REQ candidatos`; candidatos a **crítico** según doc 05 §4.5; filas `REQ-NF` con métrica tomada del C-03 (`Q-13`); en refactors, REQ de invariancia; en IA, propuesta de corpus y casos borde (el **umbral lo define el PO** — `Q-24`); en épicas, códigos de subtarea para `REQ-<SUB>-01` (`Q-12`); candidatos a **Fuera de alcance**. Si algo agrega un actor, una regla o un módulo nuevo, proponer **otro ticket** (`Q-27`, decide el PO).
8. **Datos de prueba y ambiente:** companies, usuarios y roles, estados iniciales, sandboxes o mocks, integraciones sin sandbox (cómo se probarán), mecanismos especiales (simular fechas) y quién prepara cada dato (QA, o el Dev si requiere seeds o migraciones).
9. **Dependencias:** otros productos, terceros, tickets (dependencia nativa *waiting on*), DevOps.
10. **Preguntas.** Al **PO**: reglas de negocio indefinidas, cada una con opciones y una **opción recomendada justificada** (`Q-20`, `Q-21`). Al **Dev/LD**: preguntas técnicas abiertas (no objeciones), p. ej. "¿El endpoint filtrará por company?", "¿Qué pasa con los registros existentes al aplicar la migración?".
11. **Propuesta de UAT:** recomendar `uat-requerido` si el resultado lo debe validar el cliente o un SH (cambio visible para clientes, integración contractual, calidad de IA juzgada por negocio). Es una recomendación; el PO decide en `requirements` (C-05/C-06).
12. **Code review del prototipo (opcional).** Solo si QA lo aprueba y hay rama o PR: ejecutar `skills/code-review/review.md` en **modo prototipo** (señales formuladas como preguntas) y llevar el resultado al bloque *Señales del código* de *4. Observaciones para el acta*.
13. **Recomendación para la decisión del PO:** `Listo para requirements` · `Listo con pendientes` (listarlos) · `Riesgo de concepto o arquitectura` (sugerir volver a `r, d & architect review`, con el motivo). QA no rechaza el prototipo: informa la testabilidad y los riesgos; decide el PO.

## Stage 3 — Reporting
- `knowledge/L3-tickets/<id>/prototype-review-qa.md` con `templates/prototype-review-qa.md`: *Contexto* (incluye prototipo vs. tipo y contrato) · *1. Checklist de testabilidad* · *2. Captura inicial de requerimientos* (REQ candidatos, heurística de completitud) · *3. Riesgos de calidad* (análisis por negocio y por capa, dependencias) · *4. Observaciones para el acta* (reconciliación, preguntas al Dev/LD, señales del código si aplica, recomendación) · *5. Pendientes para `requirements`* (preguntas al PO con opción recomendada, datos de prueba y accesos) · *6. Propuesta de UAT* · *7. Siguiente paso* (QA Points preliminares). Anexo o archivo `architecture-brief-qa.md` con el checklist técnico.
- `knowledge/L3-tickets/<id>/comments/C-04-<AAAA-MM-DD>.md`: **aporte de QA** al acta C-04 (testabilidad, decisiones sugeridas, *Pendientes para requirements*, versión o enlace del contrato aprobado). El acta la publican el SM o el PO; el encabezado del borrador lo indica.
- `ticket-memory.md`: tablero Discovery, estado, fecha de la reunión, riesgos principales, pendientes y contrato de referencia.
- **Estado destino sugerido** (lo decide el PO en C-04): `requirements` → siguiente skill `requirements/matrix.md` · o `r, d & architect review`.

```
✅ PROTOTYPE REVIEW QA — <id>
Testabilidad: <n>/6 Sí · Riesgo general: Alto/Medio/Bajo · Riesgos: <n> · Preguntas PO: <n> · Dev/LD: <n>
REQ candidatos: <n> (críticos <n>, NF <n>) · UAT recomendado: Sí/No
Recomendación: <...> · Borrador C-04 (aporte QA): comments/C-04-<fecha>.md
```

## Reglas
- QA evalúa la **testabilidad**; no diseña la solución, no aprueba la arquitectura (LD) ni decide avanzar (PO).
- No se reescribe la especificación del PO: se registran sus criterios y se pregunta lo que falta.
- El contrato aprobado en C-04 es línea base **solo cuando la matriz lo referencie** (`Q-10`): anotar su versión o enlace para `requirements`.
- Ningún riesgo sin fuente (L1, L2, C-03, prototipo o código). Las hipótesis se marcan como tales.
- Toda regla indefinida sale con opción recomendada; ninguna queda "a criterio del Dev".
- El MCP de ClickUp es de solo lectura: la skill prepara borradores; QA, el SM o el PO publican.
