# Skill: bug-reporter/create

> Convierte una descripción informal de QA en un **reporte de bug T-02** completo, con evidencia técnica verificable y la clasificación propuesta (tablero, TYPE, prioridad = severidad, tags `det-*` y de área, Project, Iond Subcategory, REQ violado, relación con el ticket origen o la tarea de Release). Tablero **Improvements** (`backlog`, o carril de hotfix). Reglas: §3, §7.5–7.6, §10, §12, §13 T-02; doc 05 §8.4 y Anexo B; `Q-15`, `Q-22`, `Q-25`, `Q-28`, `Q-38`, `Q-46`.

## Cuándo usar
- QA encuentra un defecto que debe ir a un ticket nuevo: hallazgo **fuera de matriz** en `mock testing` (C-17), `urgent` **preexistente** detectado en `mock testing`, hallazgo de `smoke`/`sanity`/`regression`, incidente o bug de producción, sesión de bug bash.
- No aplica a observaciones que incumplen un REQ del ticket en prueba: esas son `OBS-xx` del C-14 (`mock-testing/execute.md`).
- Frase disparadora: `Crea un nuevo ticket:` + ruta de navegación + descripción informal. Ej.: `Crea un nuevo ticket: Company > Boards — al duplicar un board con nombre existente no se muestra error`.

## Pre-requisitos (gates)
| Check | Si falla |
|---|---|
| La ruta de navegación identifica el módulo (SIDE + módulo de `knowledge/test-suites/_config/modules.csv`) | Preguntar a QA el módulo antes de seguir |
| Se conoce la fase de detección (para el tag `det-*`) y, si aplica, el ticket origen o la tarea de Release | Preguntar a QA |
| Repos de desarrollo accesibles en `../` | Seguir sin evidencia de código y marcarla `[AUSENTE]` con el motivo |

## Contexto a cargar
- **L1:** `sdlc-consolidation.md` (§3, §7.5–7.6, §10, §12, §13 T-02, §14 C-17, C-28, C-32) · doc 05 (§7, §8.4, Anexo B) · `business-rules.md`, `api-architecture.md`, `stack-overview.md`.
- **L2:** módulo según `modules.csv` (`SIDE`, `MODULE` → `L2_MODULE`; p. ej. `Company > Boards` = `TENANT, Boards → boards`; `Admin > Billing` = `ADMIN, Billing → billing`; `KC` → `auth`). Iond Subcategory candidata: filas de `subcategory-map.csv` con ese `L2_MODULE`. Leer reglas de negocio, Database, edge cases conocidos e Impacto Cruzado.
- **L3:** del ticket origen (matriz vigente, `test-matrix.md`, `code-review-qa.md`) si el bug nace de un `mock testing`; de la release (`knowledge/releases/<producto>/<versión>/`) si nace en una suite.
- **ClickUp:** `searchTasks` para duplicados en Improvements y Discovery; `getTaskById` del ticket origen.

## Stage 1 — Planning
```
🐛 SIGUIENTE SKILL: bug-reporter/create
   Ruta: <SIDE > Módulo > ...> → L2: <módulo> · Iond Subcategory candidata: <..>
   Fase de detección: <det-*> · Origen: <#ticket | tarea de Release vX.Y.Z | producción | bug bash>
   Descripción original: "<texto de QA, tal cual>"
   Plan: actualizar repos (Regla #7) → cargar L1/L2 → buscar duplicados → analizar con evidencia → borrador T-02
   Output esperado: borrador T-02 en el chat; al recibir el ID de ClickUp, L3/<id>/bug-report.md
¿Procedo?
```

## Stage 2 — Execution
1. **Actualizar los repos** según la Regla #7 del `SKILL.md` raíz (solo lectura). Para un bug de producción, contrastar también con la rama o el tag de la versión desplegada si existe.
2. **Duplicados:** `searchTasks` por palabras clave (resumen, módulo, mensaje de error) y *Edge Cases Conocidos* del L2. Si hay un candidato, mostrarlo a QA antes de seguir.
3. **Análisis técnico con evidencia verificable.** Buscar con `grep -rn` los términos clave en `../gateway-ion/src`, `../flow_binaries`, `../gateway/app` y `../webcomponents-flow`. Cada pieza de evidencia lleva su nivel:
   - `[CONFIRMADA]` — código, log o query encontrado: ruta real y número de línea real.
   - `[INFERIDA]` — lo documenta el L2 pero no hay hit en el código: citar el L2, con lenguaje de hipótesis.
   - `[AUSENTE]` — se buscó y no existe (p. ej. la validación): declarar la búsqueda y su resultado de 0 hits.
   Un fragmento de código sin hit real es una alucinación aunque parezca plausible. Las hipótesis de causa raíz se marcan `[Hipótesis técnica]:` y nunca se presentan como hechos. Queries de BD solo desde las migraciones (`skills/_shared/evidence.md`).
4. **Pasos para reproducir.** Si QA dio pasos, refinarlos sin reemplazarlos (precondiciones, pasos implícitos, formato). Si no, generarlos desde la ruta, el L2 y el frontend real. Formato breadcrumb desde un estado conocido, con datos, usuario y rol (`Company Login > Sidebar: Boards > ...`); frecuencia si es intermitente (p. ej. 3 de 5).
5. **Resultado esperado.** Si el comportamiento lo regula una matriz vigente (ticket ya `merged`), citar el **REQ-ID** y la versión; si no, la fuente del esperado (L2, regla de negocio, comportamiento previo). Si el REQ es de un ticket que aún no está en `merged`, no crear el bug: es una `OBS-xx` de su `mock testing`.
6. **Clasificación propuesta** (QA propone; el PO aprueba en el triage — `Q-15`):
   - *Título* (`Q-46`): `[PRODUCTO][Módulo] Verbo + objeto`, conciso y directo al problema.
   - *TYPE:* `Bug` por defecto ("no funciona como se espera"); otro TYPE solo con evidencia (nunca existió → `New Feature`; deuda interna sin impacto funcional → `Refactor`).
   - *Prioridad = severidad* con la tabla de §10 y su motivo (`urgent` core roto sin workaround, pérdida de datos, seguridad o cobro incorrecto · `high` con workaround · `normal` secundaria o UX moderada · `low` cosmético).
   - *Tags:* `det-*` según la fase · un tag de área `iond-core` / `iond-uxui` / `iond-infra` / `iond-ia` · `fuera-de-matriz` si nace de un hallazgo fuera de matriz · `hotfix` solo como propuesta (lo ponen el PO o el LQA).
   - *Campos:* Project, Iond Subcategory (si Project = Iond).
   - *Relación:* ticket origen (`fuera-de-matriz`, `pilot-feedback`) o tarea de Release de la versión (bugs `det-smoke`/`det-sanity`/`det-regression`, `det-prod` y `hotfix`).
7. **Tratamiento según la fase** (§7.5–7.6, Q-22): fuera de matriz → ticket nuevo + borrador **C-17** para el ticket origen (no bloquea) · `urgent` preexistente en `mock testing` → ticket nuevo `det-mock` y aviso inmediato al PO · `urgent` en el release → **fix-forward**: subtarea de la tarea de Release con `fix-forward` y borrador **C-28** · resto del release → `backlog` con `det-smoke/sanity/regression`, previa discusión con PO y LD · incidente de producción → carril de hotfix (`urgent` + `hotfix` + `det-prod`, `to do` directo, C-32 del PO/LQA).
8. **Autorrevisión** con el checklist del Anexo B (10 puntos) incluido en `templates/bug-ticket.md`.

## Stage 3 — Reporting
1. Presentar el borrador completo con `templates/bug-ticket.md`: tabla de campos y tags, descripción T-02 lista para pegar (*Resumen, Ambiente, Pasos para reproducir, Resultado esperado, Resultado actual, Evidencia, Impacto*), checklist del Anexo B y razonamiento de la prioridad y el TYPE. Preguntar: `¿Apruebas el borrador o ajusto algo?`
2. Aplicar ajustes hasta la aprobación. **QA crea el ticket en ClickUp** (Form de intake o manual); el catalyst no escribe en ClickUp.
3. Mientras no haya ID, el borrador puede guardarse en `knowledge/L3-tickets/drafts/bug-<NNN>-<slug>.md`.
4. **Cuando QA da el ID de ClickUp:** crear `knowledge/L3-tickets/<id>/` con `bug-report.md` (borrador aprobado) y `ticket-memory.md` (tablero Improvements, estado `backlog` o `to do` si es hotfix, relación con el origen). Mover ahí el borrador de `drafts/` si existía.
5. Borradores de comentario derivados en el L3 del **ticket origen** o de la release: `comments/C-17-<fecha>.md` (fuera de matriz) o `comments/C-28-<fecha>.md` (fix-forward). Actualizar la tabla *Hallazgos y tickets derivados* del `ticket-memory.md` del origen.

```
🐛 BORRADOR T-02 — [PRODUCTO][Módulo] <título>
Prioridad: <..> (motivo) · TYPE: Bug · det-*: <..> · área: <..> · Iond Subcategory: <..>
REQ violado: <REQ-xx vN de #id | Ninguno> · Relación: <#origen | Release vX.Y.Z> · Duplicados: descartados
Evidencia: <n> [CONFIRMADA] · <n> [INFERIDA] · <n> [AUSENTE]
```

## Reglas
- Nunca inventar evidencia: sin hit real no hay código citado; 0 resultados también es evidencia (`[AUSENTE]`).
- Formalizar sin distorsionar la descripción de QA; pasos dados por QA se refinan, no se reemplazan.
- Un bug por ticket; solo tags SDLC (nunca legacy, §12.1).
- La prioridad propuesta siempre lleva su motivo; el PO aprueba la clasificación en el triage.
- La carpeta L3 se crea solo cuando QA entrega el ID de ClickUp.
- Solo lectura en repos y ClickUp; credenciales y datos personales enmascarados en la evidencia.
