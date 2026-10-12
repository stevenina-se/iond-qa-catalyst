# Skill: knowledge/update-module

> Actualiza el conocimiento **L2** de los módulos afectados por un release **ya desplegado**, en lote, a partir de los tickets de la versión. Mantiene el L2 como reflejo de lo que está en producción: rutas, endpoints, schema, **reglas de negocio**, edge cases, impacto cruzado, **specs de bot-test** y **filas del E2E maestro**, y señala las filas nuevas que hay que agregar a la hoja "Iond Testing Plan". Se ejecuta después de ACT-01/ACT-02 (C-30 y C-31) de la tarea de Release (§7.3); `Q-49` a `Q-51`, `Q-54`.

## Principio
> "El L2 de un módulo refleja lo que está en producción, no lo que se planeó." Por eso se actualiza **después del despliegue del release**, no al aprobar un ticket en `mock testing`.

## Cuándo usar
- Tras el despliegue a producción de una versión (C-30 publicado y, de preferencia, C-31 con el smoke de producción en verde), incluido un release extraordinario de hotfix.
- Mantenimiento puntual: QA detecta que un L2 está desactualizado respecto de producción (modo módulo).
- Frases disparadoras: `Actualizar módulos post-release: <producto> v<X.Y.Z>` · `Actualizar L2 del módulo <módulo>`

## Pre-requisitos (gates)
| Check | Si falla |
|---|---|
| Existe `knowledge/releases/<producto>/<versión>/tickets.md` | PARAR → generarlo con `skills/release/ingest.md` o pedir a QA la lista de tickets |
| La versión está desplegada: C-29 con `Decisión: GO` o `CONDITIONAL GO` y C-30 publicado en la tarea de Release | PARAR: no se actualiza el L2 con lo que no está en producción |
| Se conocen las ramas RC por repo (C-23 / `release-task.md`) o el tag desplegado | Pedir a QA la referencia; sin ella, leer la rama principal que contenga el merge y anotarlo |
| Existe `knowledge/L2-modules/<módulo>/module.md` | Crearlo desde `knowledge/L2-modules/_template.md` (con aprobación de QA) |

## Contexto a cargar
- **L1:** `sdlc-consolidation.md` (§7.2–7.3, §7.7, §9.4) · `knowledge/test-suites/README.md`.
- **Release:** `tickets.md` (+ `tickets.csv`), `release-task.md`, `go-no-go.md`, C-23/C-30/C-31.
- **L3 de cada ticket incluido:** `requirements-matrix-v<N>.md` con VoBo vigente (o T-02), `qa-report.md` final, `code-review-qa.md`, `test-matrix.md` y las notas para L2 de `ticket-memory.md`.
- **Mapas:** `knowledge/test-suites/_config/subcategory-map.csv` (Iond Subcategory → `L2_MODULE`, `E2E_MODULES`, `CROSS_SYSTEM`), `_config/modules.csv` (SIDE/módulo → código de 3 letras → `L2_MODULE`), `_config/rules.csv` (spec y TC de bot-test por ruta), `knowledge/test-suites/e2e-master.csv`.
- **bot-test (solo lectura):** `../bot-test/apps/bot-test/tests/IONFLOW/{Admin-ION,Company-ION/<módulo>,shared,utils}` (`skills/_shared/bot-test.md`).

## Stage 1 — Planning
```
🔄 SIGUIENTE SKILL: knowledge/update-module — lote <producto> v<X.Y.Z>
   Tickets en la versión: <n> (excluidos diferidos/revertidos: <n>) · sin Iond Subcategory: <n>
   Módulos L2 afectados: <módulo (n tickets), ...>
   Referencia de código: <ramas RC por repo | tag>
   Output esperado: knowledge/L2-modules/<módulo>/module.md actualizados + propuesta de filas para la hoja E2E
¿Procedo? (se confirma módulo por módulo antes de escribir)
```

## Stage 2 — Execution
1. **Filtrar tickets.** De `tickets.md`, solo los que quedaron en la versión desplegada (`merged` con la versión objetivo; sin `diferido` ni revert por fix-forward). Listar aparte los excluidos.
2. **Mapear ticket → módulo L2** con la Iond Subcategory y `subcategory-map.csv` (`L2_MODULE`; una subcategoría `Nodo <nombre>` → `nodes`). Si falta la subcategoría o no está en el mapa, inferir el módulo por los archivos del PR (`code-review-qa.md`) y **marcarlo** para que QA agregue la fila al mapa.
3. **Extraer lo que cambió por ticket:**
   - *Reglas de negocio:* REQ de la matriz con VoBo vigente (la versión más alta con C-06), sin los que el PO trasladó a otro ticket; en bugs, el resultado esperado del T-02 corregido.
   - *Edge cases:* `OBS-xx` corregidas, hallazgos fuera de matriz, bugs `det-*` resueltos en la versión.
   - *Técnico:* endpoints, rutas, componentes, migraciones y archivos tocados (del diff y de `code-review-qa.md`).
   - *Pruebas:* TC con `USO = Regresión candidata` o `Sanity` y queries de BD útiles de `test-matrix.md`.
4. **Leer el estado final del código** en la referencia desplegada (no el diff): rutas del router de `gateway-ion`, handlers de `flow_binaries`/`gateway`, migraciones nuevas (`../gateway/database/migrations/`, `../flow_binaries/migrations/`). Solo lectura.
5. **Proponer los cambios por módulo y confirmar con QA** antes de escribir:
   ```
   🔄 L2 — <módulo> (<tickets>)
     Reglas de negocio: +<n> / ~<n> (deprecadas <n>) · Endpoints: +<n> · Rutas: +<n> · Database: +<tablas/columnas>
     Edge cases: +<n> · Impacto cruzado / centinela: ~<n> · Specs bot-test: <n> · Filas E2E: <n> (+<n> propuestas)
   ¿Aplico en este módulo?
   ```
6. **Actualizar `module.md`** (crear la sección si no existe, con el formato del `_template.md`):
   - Endpoints, rutas y componentes; **Database** desde las migraciones (nunca inventar columnas); queries de verificación frecuentes.
   - **Reglas de negocio:** una línea por regla vigente con su fuente (`<id-ticket> REQ-xx vN`); las reemplazadas se marcan *Deprecada en v<X.Y.Z>*, no se borran.
   - **Edge Cases Conocidos** con la versión donde se corrigieron o descubrieron; **Impacto Cruzado** y **archivos centinela**.
   - **Specs bot-test:** specs y page objects que cubren el módulo (`Company-ION/<módulo>`, `Admin-ION/<dominio>`), IDs de test `[TC-<MÓDULO>-<GRUPO>-NN]` y estado de automatización (`Ejecutable`, `En PR`, `Rota`, `Pendiente`) según `rules.csv` y `e2e-master.csv`.
   - **Filas E2E:** IDs del E2E maestro del módulo (prefijo `E2E-<SIDE>-<CÓDIGO>` de `modules.csv`, p. ej. `E2E-TEN-BRD-`), con conteo por prioridad, las de `BASELINE = sí`, su grupo de rotación y su automatización.
7. **Filas nuevas para el E2E maestro.** Por cada funcionalidad desplegada sin fila en `e2e-master.csv` (o con un cambio de comportamiento que invalida su fila), proponer la fila para la hoja "Iond Testing Plan" (pestaña "Iond Automation Plan"): SIDE, MODULE, FEATURE, CASO, PATH, TEST_CASES, PRIORITY y nota de origen (ticket y REQ). El CSV **no se edita a mano**: QA agrega la fila en la hoja y corre `python -I scripts/e2e_master.py import` (ver `knowledge/test-suites/README.md`).
8. **Historial:** agregar a la sección de historial del módulo (`## Historial de Cambios Post-Release` en el `_template.md`; algunos L2 la llaman *Historial de Actualizaciones* o *Historial de Cambios*) la fila `| <fecha> | <producto> v<X.Y.Z> | <tickets> | <resumen> | QA Catalyst (lote) |` y la fecha de *Última actualización*.

## Stage 3 — Reporting
- `knowledge/L2-modules/<módulo>/module.md` actualizados (solo los confirmados por QA).
- Resumen en el chat:
```
🔄 L2 POST-RELEASE — <producto> v<X.Y.Z> — COMPLETADO
Módulos actualizados: <módulo (n tickets)>, ... · L2 nuevos: <n>
Tickets excluidos (diferidos/revertidos): <ids> · Tickets sin módulo L2: <ids>
Discrepancias L2 anterior vs. código: <n> (detalle por módulo)
Filas propuestas para la hoja "Iond Testing Plan": <n> · Subcategorías a agregar en subcategory-map.csv: <lista>
```
- **Acciones para QA:** agregar las filas a la hoja e importar; agregar las subcategorías nuevas a `_config/subcategory-map.csv`; si cambió el estado de una spec de bot-test, actualizar `AUTOMATIZACION` en `_config/rules.csv` y reimportar.

## Reglas
- El L2 refleja producción: solo tickets de una versión desplegada; nada de lo planeado o diferido.
- No se elimina información: se marca como deprecada con la versión.
- Cada regla de negocio cita su fuente (ticket, REQ y versión de la matriz).
- QA aprueba cada módulo antes de escribir; el L2 es la fuente de verdad del equipo.
- Solo lectura en repos de desarrollo y en bot-test; `e2e-master.csv` se regenera desde la hoja, nunca a mano.
