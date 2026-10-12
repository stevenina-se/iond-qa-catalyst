# Skill: code-review/review

> Revisión del código del ticket **desde la perspectiva de QA** (bug hunting) para orientar las pruebas: lee los PR del ticket, compara contra la rama base, busca defectos con heurísticas de dominio y **convierte los hallazgos en TC** de la Matriz de Pruebas (una sola vez, `ORIGEN = Code review`). No reemplaza el `code review` del LD (D-09/I-05, C-11): QA no aprueba ni comenta PRs (doc 05 §2.3). Se ejecuta con el ticket en `code review` o `ready for qa`, antes de `mock-testing/execute.md`.

## Cuándo usar
- Tablero Discovery o Improvements, estado `code review` o `ready for qa` (antes de ejecutar pruebas). Es opcional y lo decide QA; se recomienda siempre en tickets con REQ críticos, migraciones o cambios en varios repos. Si se omite, se registra en `ticket-memory.md`.
- **Modo prototipo (opcional):** desde `prototype-review/review.md`, si hay rama o PR del prototipo y QA lo pide.
- Frase disparadora: `Code review QA del ticket <id>`

## Pre-requisitos (gates)
| Check | Si falla |
|---|---|
| Merge Request (y 2/3/4 si aplica) con URL `https://github.com/altacrest/<repo>/pull/<n>` | PARAR: sin PR no hay revisión (A-06 también lo exige antes de `code review`) |
| Repos de desarrollo accesibles en `../<repo>` (`gateway-ion`, `flow_binaries`, `webcomponents-flow`, `gateway`) | Pedir a QA que clone o actualice el repo; no seguir con código desactualizado |
| L2 del módulo cargado (Impacto Cruzado, archivos centinela, Database) | Avisar y seguir con el diff; registrar el vacío |
| Criterio disponible: matriz con VoBo (o T-02 en bugs) | Seguir, pero los hallazgos no se mapean a REQ hasta tenerlo |

## Contexto a cargar
- **L1:** `sdlc-consolidation.md` (§5 D-09/D-10, §6 I-04 a I-06, §8.2, §10, §14 C-09 y C-11) · `api-architecture.md`, `stack-overview.md`, `business-rules.md` · `SKILL.md` raíz, Regla #7 (navegación de repos).
- **L2:** módulo(s) vía `subcategory-map.csv` → `L2_MODULE`; módulos dependientes según Impacto Cruzado.
- **L3:** `requirements-matrix-v<N>.md` (o T-02), `test-matrix.md` (si existe), `ticket-memory.md`.
- **ClickUp:** C-09 (REQ cubiertos, repos/ramas/PRs, migraciones, variables, pruebas unitarias, zonas sensibles), C-11 si existe, campos Merge Request 1–4.

## Stage 1 — Planning
```
🔄 SIGUIENTE SKILL: code-review/review — <modo ticket | modo prototipo>
   Ticket: <id> · `<estado>` · PRs: <repo#n, ...> · base: DEVELOPMENT
   Módulo principal: <..> · impacto cruzado: <..> · REQ en la matriz: <n>
   Output esperado: L3/<id>/code-review-qa.md + TC con ORIGEN "Code review" en test-matrix (o propuestos si aún no existe)
¿Procedo?
```

## Stage 2 — Execution
1. **Obtener los cambios (solo lectura).** Por cada PR: repo y número desde la URL; rama y base con `gh pr view <url> --json number,title,headRefName,baseRefName,commits,files` (si `gh` está autenticado) o con `git -C ../<repo> fetch origin` + `git -C ../<repo> branch -r`. Diff contra la base: `git -C ../<repo> diff --stat origin/DEVELOPMENT...origin/<rama>` y el diff completo; commits: `git -C ../<repo> log --oneline origin/DEVELOPMENT..origin/<rama>`. Si el PR declara otra base, usarla y anotarlo. Prohibido: `gh pr review`, `gh pr comment`, `gh pr merge`, `git push`, `commit` o `merge`.
2. **Cruce con la matriz y el C-09.** Tabla `Archivo → REQ-ID`. Un REQ sin cambio visible → `RISK`. Un cambio sin REQ → verificar que no implemente algo distinto de lo acordado (eso sí es rechazo, §8.2). Verificar lo que declara el C-09: migraciones y variables presentes en el PR; en bugs, la **prueba unitaria** que certifica la corrección (I-04).
3. **Bug hunting** (severidad sugerida si se confirma, con la prioridad de §10):

   | Área | Qué buscar | Sev. |
   |---|---|---|
   | Backend N1 | Query sin filtro por company/tenant · endpoint sin validación de entrada · SQL por concatenación · ruta sin autenticación · logs con secretos o datos personales | urgent |
   | Backend N1 | Error sin manejar · condición de carrera sin transacción · valores hardcodeados · migración sin reversa | high / normal |
   | Backend N2 | **Asimetría** de guards o registro entre operaciones inversas (create/delete, upgrade/downgrade, enable/disable) · **divergencia cross-repo** (Go vs PHP) para el mismo flujo · cambio de estado que **no revoca** permisos o recursos del estado anterior · columna generada sin fallback (fail-open) · campo enum aceptado como texto libre | urgent |
   | Backend N2 | Consumo registrado sin enforcement · enforcement sobre un contador que nadie incrementa · deduplicación anclada al timestamp equivocado · tiempo de reloj en vez de tiempo activo · aprovisionamiento perezoso que falla en la primera llamada · seeder que pisa configuración del admin · registro huérfano insertado antes del guard · early return que descarta el acumulador · test unitario que depende de un estado que el código productivo nunca produce | high |
   | Backend N2 | Seeder que busca por campo no único · endpoint de solo lectura bloqueado por un guard de consumo · cambio de configuración del padre sin re-sync a los dependientes | normal |
   | Frontend N1 | `v-html` con datos del usuario · ruta sin guard de permisos | urgent |
   | Frontend N1 | Sin estado de carga, vacío o error · formulario sin validación · llamada a API sin manejo de error · watchers o listeners sin limpieza · accesibilidad | high / normal |
   | Frontend N2 | Permisos creados pero no asignados a ningún rol (403 para todos) | urgent |
   | Frontend N2 | `catch` vacío que muestra "sin datos" ante un error · mensaje técnico o cuerpo 5xx mostrado al usuario · computed que muestra un estado falso con `null` · snapshot guardado en vez de datos vigentes | high |
   | Frontend N2 | Formato numérico o de moneda hardcodeado · placeholder i18n sin parámetro · `if (valor)` con 0 válido · botón "deshabilitado" solo por CSS · diálogo que no revierte cambios al cancelar · `:key` repetible en `v-for` · fechas UTC parseadas como hora local · UI que contradice un REQ | normal |
   | Canvas | Listener sin `removeEventListener` · prop que no re-renderiza · superposición de drawers o diálogos | high / normal |

4. **Follow-the-flow** de cada cambio significativo: (1) quién lo invoca, también desde otro repo · (2) qué persiste y si el insert ocurre antes del guard · (3) quién consume el dato · (4) cómo lo ve el usuario con `null`, 0 o vacío · (5) qué pasa cuando falla · (6) si existe la operación opuesta y es simétrica. Patrones: asimetría, hueco sin registro, divergencia, dependencia frágil, estado zombie.
5. **Barrido de heurísticas QA:** entradas (trim, requeridos, longitud, caracteres especiales) · estados de UX (carga, vacío, error accionable, acción primaria deshabilitada durante la carga) · doble acción (doble clic, reintento, varias pestañas) · integridad (duplicados, guardados parciales, caché obsoleta) · permisos validados también en backend · contratos entre repos (nombres de campos, formas de respuesta, códigos, timeouts) · observabilidad · idempotencia.
6. **Impacto cruzado:** módulos y archivos centinela del L2 que toca el diff; tabla `Módulo | Componente | Riesgo | Verificación`. Alimenta la regresión de zonas cercanas.
7. **Clasificar el origen** antes de documentar: *introducido por el ticket* · *expuesto por el ticket* (código no tocado que el cambio activa) · *preexistente* (sección aparte; candidato a T-02 con `skills/bug-reporter/create.md`) · *incierto* (`RISK` con nota "verificar con git blame").
8. **Documentar cada hallazgo** `CR-xx` con categoría (`BUG` reproducible · `RISK` a verificar · `SEC` seguridad · `EDGE` borde, idempotencia o regresión), severidad sugerida, REQ-ID afectado (o "sin REQ"), repo, commit, archivo y líneas, evidencia (fragmento real), comportamiento esperado (según el REQ o el dominio), comportamiento actual (qué hace el código hoy), precondiciones (rol, company, datos) y pasos de reproducción. Sin reproducción paso a paso, es `RISK`, no `BUG`. Pasos según el tipo de UI: CRUD (crear → verificar en lista → editar → eliminar sin residuos) · formulario (válido e inválido → feedback → recargar y persistir) · listado (filtro, orden, paginación, limpiar) · diálogo (abrir, inválido, válido, cancelar sin cambios) · canvas (nodo, configurar, conectar, guardar, recargar, ejecutar) · resiliencia (forzar error → mensaje accionable, sin registros parciales).
9. **Inyectar en la Matriz de Pruebas (una sola vez).** Cada `CR-xx` que requiere verificación → una fila con el siguiente `TC-nn` consecutivo y la cabecera de `templates/test-matrix.md`: `ORIGEN = Code review` y el `REQ_ID` que verifica; si el hallazgo no toca ningún REQ, `ORIGEN = Zona cercana` (regresión) o `Exploratorio`, con `REQ_ID = —`. TIPO `Negativo`, `Borde` o `Regresión`; pasos breadcrumb; resultado esperado; `USO = Mock` (o `Regresión candidata` si conviene sumarlo al E2E maestro). La trazabilidad `CR-xx → TC-nn` (con `Repo | Commit | Archivo:líneas` y la prioridad sugerida) queda en `code-review-qa.md`. Si ese `CR-xx` ya tiene TC, actualizarlo; no duplicar. Si `test-matrix.md` aún no existe, dejar las filas en la sección *TC propuestos* para que `mock-testing/plan.md` las inyecte.

### Modo prototipo
Mismos pasos 1, 4 y 6, sin bug hunting formal: las señales se formulan como **preguntas** ("¿El endpoint filtrará por company?", "¿Qué pasa con los registros existentes al aplicar la migración?") y van al bloque *Señales del código* de la sección *4. Observaciones para el acta* de `prototype-review-qa.md`. No se crea `code-review-qa.md` ni se inyectan TC.

## Stage 3 — Reporting
- `knowledge/L3-tickets/<id>/code-review-qa.md`: resumen (PRs, base, commits, archivos, hallazgos por categoría y severidad) · cruce archivo → REQ y verificación del C-09 · `BUG` · `RISK` · `SEC` · `EDGE` · mapas follow-the-flow que revelaron hallazgos · impacto cruzado · preexistentes · TC inyectados o propuestos (`CR-xx | TC-nn | REQ_ID | ORIGEN | TIPO | Severidad sugerida`).
- `test-matrix.md` + `.csv` con las filas `ORIGEN = Code review` (si la matriz existe). `ticket-memory.md` con la fecha y el resumen.
- Siguiente skill: `mock-testing/plan.md` (si falta la matriz) o `mock-testing/execute.md`.

```
🔎 CODE REVIEW QA — <id>
PRs: <n> · commits: <n> · archivos: <n> · hallazgos: BUG <n> · RISK <n> · SEC <n> · EDGE <n> · preexistentes <n>
TC inyectados (ORIGEN Code review): <n> (propuestos: <n>) · REQ sin cambio visible: <lista>
```

## Reglas
- Solo lectura: nunca modificar, commitear, pushear ni mergear en los repos de desarrollo; nunca comentar, aprobar ni rechazar un PR.
- Un hallazgo de código no rechaza el ticket por sí solo: se verifica en `mock testing` y se juzga contra la matriz (§8.2). Sin REQ, si se confirma, es fuera de matriz (C-17), salvo un `urgent` provocado por el cambio.
- Si un hallazgo impide iniciar las pruebas (falta una migración o variable del C-09), QA lo informa al Dev en el ticket o aplica `blocked` (C-20) según §8.3.
- Toda evidencia es código real con ruta y línea; nunca código "plausible". Las queries salen de las migraciones.
- Los preexistentes se documentan aparte; nunca contaminan el veredicto del ticket.
