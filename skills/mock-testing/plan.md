# Skill: mock-testing/plan

> Construye la **Matriz de Pruebas** del ticket (`test-matrix.md` + `test-matrix.csv`) con trazabilidad REQ-ID → TC, a partir de la matriz con VoBo (o la mini-matriz, o el reporte T-02 en bugs), el handoff del Dev (C-09) y la asignación (C-12). Estima o confirma QA Points y fija ambiente y datos. Estado `ready for qa` (**D-10** / **I-06**); reglas §9.3; doc 05 §5; `Q-05`, `Q-10`, `Q-17`, `Q-26`, `Q-45`.

## Cuándo usar
- Tablero Discovery o Improvements, estado `ready for qa` (o `mock testing` recién iniciado sin matriz de pruebas).
- **Modo borrador:** en `requirements` mientras se espera el VoBo (`Q-17`), para adelantar la matriz y los datos.
- **Modo re-test:** cuando el ticket vuelve a `ready for qa` después de un rechazo (Rejection_count > 0).
- Frase disparadora: `Planificar pruebas del ticket <id>`

## Pre-requisitos (gates)
| Check | Si falla |
|---|---|
| Criterio vigente: matriz o mini-matriz con `po-vobo` y C-06 de la versión más alta; en bugs, T-02 completo | PARAR. Sin VoBo no hay criterio de rechazo; solo modo borrador. **Excepción `Q-45`:** si el ticket ya estaba en `dev in progress` o más adelante al corte de transición, usar su documentación vigente y registrarlo |
| Existe el handoff C-09 (REQ cubiertos, repos/ramas/PRs, migraciones, variables, datos, pruebas unitarias) | Borrador de pedido al Dev; seguir con lo disponible y marcarlo |
| Existe el C-12 (Reviewer QA, QA Points, ambiente, build/rama) | Recordar al LQA (SLA 1 día hábil); el ambiente se confirma con QA |
| Merge Request con al menos un PR | Avisar: sin PR no se puede verificar la rama desplegada |
| `code-review-qa.md` con TC propuestos aún no inyectados | Inyectarlos en este plan (una sola vez, `ORIGEN = Code review`) |

## Contexto a cargar
- **L1:** `sdlc-consolidation.md` (§5 D-09 a D-11, §6 I-05 a I-07, §8.1–8.2, §9.3, §10, §14 C-09, C-12 a C-14) · doc 05 (§3, §5, §8.3, §9.3) · `test-priorities.md`.
- **L2:** módulo(s) vía `subcategory-map.csv` → `L2_MODULE`: rutas, endpoints, Database, queries frecuentes, selectores, Impacto Cruzado, archivos centinela, filas del E2E maestro del módulo.
- **L3:** `requirements-matrix-v<N>.md` (o T-02), `prototype-review-qa.md`, `code-review-qa.md`, `ticket-memory.md`; en re-test, el reporte de la iteración anterior (`qa-report.md` o `qa-report-iter<N>.md`).
- **ClickUp:** descripción (matriz vigente y *Datos de prueba*), C-06, C-09, C-11, C-12, campos Merge Request 1–4, Rejection_count, QA Points, tags.

## Stage 1 — Planning
```
🔄 SIGUIENTE SKILL: mock-testing/plan — <normal | borrador | re-test iteración N+1>
   Ticket: <id> · <tablero> · `<estado>` · criterio: <Matriz vN (VoBo ✅) | mini-matriz vN | T-02>
   REQ: <n> (críticos <n>, NF <n>) · TC del code review por inyectar: <n>
   Ambiente: <url del C-12> · rama: <rama> · PRs: <n>
   Output esperado: L3/<id>/test-matrix.md + test-matrix.csv · QA Points <estimado>
¿Procedo?
```

## Stage 2 — Execution
1. **Fijar el criterio.** Versión vigente de la matriz (la más alta de la descripción con C-06), filas *Pendiente de decisión PO* (no son criterio de rechazo), *Fuera de alcance* (no se prueban como requisito) y contrato referenciado (`Q-10`). En bugs: pasos, resultado esperado (y REQ-ID si lo cita) del T-02.
2. **Contrastar con el C-09.** ¿Los "REQ cubiertos" coinciden con la matriz? Un REQ no mencionado es un riesgo a verificar primero. Anotar migraciones, variables, comandos y datos que pide el Dev, y las zonas sensibles que declara. En bugs de Improvements, el C-09 debe mencionar la **prueba unitaria** que certifica la corrección (I-04).
3. **Diseñar los TC** con la cabecera exacta de `templates/test-matrix.md`: `ID,REQ_ID,ORIGEN,TIPO,PRECONDICION,PASOS,RESULTADO_ESPERADO,USO,AUTOMATIZABLE,ESTADO,EVIDENCIA` (IDs consecutivos `TC-01…`; un ID eliminado no se reutiliza):
   - Cada REQ tiene **al menos un TC**; cada REQ **crítico**, al menos un *Happy Path* y uno *Negativo* o *Borde*.
   - **TIPO:** `Happy Path`, `Negativo`, `Borde`, `Regresión`, `NF`. `REQ-NF` → TC `NF` con la métrica y la condición de medición. REQ de IA → TC sobre el corpus definido, con umbral y número de ejecuciones.
   - **ORIGEN:** `REQ` (derivado de la matriz) · `Regla L2` (regla del módulo que el REQ toca) · `Code review` · `Zona cercana` · `Exploratorio`. `REQ_ID = —` solo en `Zona cercana` y `Exploratorio`; en un bug sin matriz, `T-02` o el REQ-ID que cite el reporte.
   - **USO:** `Sanity` en los TC de REQ críticos (se re-ejecutan en `sanity`) · `Regresión candidata` en TC estables que conviene sumar al E2E maestro o automatizar · `Mock` en el resto.
   - **RESULTADO_ESPERADO** = el "¿Qué debe pasar?" del REQ, observable; nunca "funciona correctamente".
   - **PASOS en formato breadcrumb:** `[Rol] Login > Sidebar: [Módulo] > [Acción] > ... > Verify: [qué]` (p. ej. `Company Login > Sidebar: Boards > Button: "New board" > Fill "Name": "qa-board-01" > Button: "Save" > Verify: board en la lista`). Para API: `POST /ruta > Body: {...} > Verify: 201 + campo`.
4. **Regresión de zonas cercanas (3 a 5 TC, `REQ_ID = —`, `ORIGEN = Zona cercana`, `TIPO = Regresión`):** flujos del mismo módulo y los que comparten el código modificado. Fuentes: Impacto Cruzado y archivos centinela del L2, zonas sensibles del C-09, archivos del PR (`code-review-qa.md`), filas del E2E maestro del módulo. En mejoras, el checklist de la mini-matriz.
5. **TC del code review:** si `code-review-qa.md` tiene TC propuestos y la matriz no los tiene, agregarlos **una sola vez** con `ORIGEN = Code review` y el REQ-ID que verifican (si el hallazgo no toca un REQ: `Zona cercana` o `Exploratorio` con `—`); registrar en `code-review-qa.md` el mapeo `CR-xx → TC-nn`.
6. **Verificaciones en BD** (si el ticket persiste o modifica datos): queries de solo lectura construidas **solo** desde las migraciones (`skills/_shared/evidence.md`), con la migración fuente como comentario, en la sección *Verificación en BD* de la matriz, vinculadas a su TC.
7. **Orden de ejecución:** (0) verificación previa del ambiente: build de la rama del ticket, migraciones y variables del C-09 · (1) Happy Path de REQ críticos · (2) Negativo/Borde de REQ críticos · (3) resto de REQ · (4) NF · (5) TC del code review aún no cubiertos · (6) regresión de zonas cercanas.
8. **Ambiente y datos (`Q-05`):** ambiente asignado al QA con la rama del ticket (URL y build del C-12). Datos según la sección *Datos de prueba* de la matriz (mocks, colecciones simuladas o cuentas de prueba si la integración no tiene sandbox), con prefijo `qa-`. Indicar quién prepara cada dato.
9. **QA Points (`Q-26`, doc 05 §9.3):** Discovery → confirmar o ajustar el estimado de `requirements`; Improvements → estimarlo aquí. 1 ≤ 2 h · 2 ≈ ½ día · 3 ≈ 1 día · 5 ≈ 2 días · 8 ≥ 3 días (proponer dividir el alcance, `Q-27`).
10. **Modo re-test (iteración N+1, doc 05 §8.3):** partir de las filas de re-test que dejó el reporte de la iteración N (`qa-report.md` o `qa-report-iter<N>.md`, que conserva los resultados anteriores); en la misma `test-matrix.md`, volver a `Pendiente` los TC fallidos (con su `OBS-xx` de referencia), los TC de REQ críticos de las áreas tocadas por el fix y los de `Zona cercana`; los demás conservan su resultado aprobado. Actualizar *Iteración · Rejection_count* del control. No exigir repetir etapas ya aprobadas. Si hubo un nuevo VoBo (v+1), ajustar primero los TC de las filas cambiadas.

## Stage 3 — Reporting
- `knowledge/L3-tickets/<id>/test-matrix.md` con `templates/test-matrix.md` (control, resumen, cobertura por REQ, matriz, verificación en BD; se agrega el orden de ejecución y los datos de prueba preparados) y `test-matrix.csv` con su cabecera obligatoria. TC a ejecutar en `Pendiente`.
- `ticket-memory.md`: iteración, versión de la matriz usada, ambiente, rama, PRs y QA Points.
- **Acciones para QA:** registrar QA Points en ClickUp (si cambió) y mover a `mock testing` al iniciar.
- Siguiente skill: `mock-testing/execute.md` (si aún no se hizo, `code-review/review.md` antes de ejecutar).

```
🧪 MATRIZ DE PRUEBAS — <id> — iteración <N>
TC: <n> (HP <n> · Neg <n> · Borde <n> · NF <n> · Regresión <n>) · ORIGEN Code review <n> · Zona cercana <n> · USO Sanity <n>
Cobertura: <n>/<n> REQ · críticos <n>/<n> con HP + Neg/Borde · QA Points: <n>
```

## Reglas
- La Matriz de Pruebas es interna de QA y no requiere VoBo; su único criterio es la matriz vigente con VoBo.
- Ningún TC sin REQ-ID salvo `Zona cercana` o `Exploratorio` (doc 05 §5.1).
- No se crea un "smoke del ticket": el smoke es del release (smoke maestro).
- Las queries de BD salen de las migraciones; nunca se inventan tablas, campos ni relaciones.
- La matriz se ajusta después de cada nuevo VoBo y antes de re-ejecutar.
