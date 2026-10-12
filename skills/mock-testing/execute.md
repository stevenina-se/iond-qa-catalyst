# Skill: mock-testing/execute

> Ejecuta la Matriz de Pruebas en `mock testing` —manualmente o asistido con Playwright MCP (Canal 1) bajo supervisión de QA—, registra la evidencia y clasifica cada hallazgo contra la matriz vigente: observación (`OBS-xx`, con REQ-ID y severidad), hallazgo fuera de matriz (C-17), desacuerdo (C-15) o bloqueo (C-20). Estado `mock testing` (**D-11** / **I-07**); reglas §8.1 a §8.4, §10; doc 05 §7, §8; `Q-05`, `Q-22`, `Q-25`, `Q-27`, `Q-31`.

## Cuándo usar
- Tablero Discovery o Improvements, estado `mock testing` (o `ready for qa` con QA iniciando: QA mueve a `mock testing`).
- Frase disparadora: `Ejecutar pruebas del ticket <id>`

## Pre-requisitos (gates)
| Check | Si falla |
|---|---|
| Existe `test-matrix.md` de la iteración vigente | PARAR → `mock-testing/plan.md` |
| La matriz de pruebas corresponde a la versión de la matriz con VoBo vigente | PARAR → ajustar con `mock-testing/plan.md` |
| Se ejecutó `code-review/review.md` o QA decidió omitirlo | Preguntar a QA; registrar la decisión en `ticket-memory.md` |
| Ambiente asignado al QA con la rama del ticket, migraciones y variables del C-09 (`Q-05`) | No ejecutar. Si no se resuelve en el día: `blocked` + `bloq-ambiente` (o `bloq-dependencia`) con borrador C-20 |
| Modo Canal 1: Playwright MCP disponible y QA presente frente al navegador visible | Usar modo manual |

## Contexto a cargar
- **L1:** `sdlc-consolidation.md` (§5 D-11, §6 I-07, §8, §10, §14 C-14 a C-17, C-20) · doc 05 (§5, §7, §8) · `skills/_shared/evidence.md` · `skills/_shared/bot-test.md` (solo si se usa Canal 2).
- **L2:** rutas, selectores, Database y queries frecuentes del módulo.
- **L3:** `test-matrix.md` + `.csv`, `requirements-matrix-v<N>.md` (o T-02), `code-review-qa.md`, `ticket-memory.md`; en re-test, el reporte de la iteración anterior (`qa-report.md` o `qa-report-iter<N>.md`).
- **ClickUp:** comentarios recientes (¿nuevo VoBo, C-16 o C-08 desde el plan?).

## Stage 1 — Planning
Preguntar el modo y anunciar:
```
❓ ¿Cómo ejecutamos?  A) Manual — QA navega; yo guío, genero queries y documento
                      B) Asistido (Canal 1) — navego con Playwright MCP; QA supervisa y confirma cada resultado
🔄 SIGUIENTE SKILL: mock-testing/execute — modo <A|B> — iteración <N>
   Ticket: <id> · matriz v<N> · TC: <n> (críticos <n>) · ambiente: <url> · rama: <rama> · rol: <Company | Admin>
   Output esperado: test-matrix.md/.csv con resultados, OBS-xx, screenshots/, borradores C-15/C-17/C-20 si aplican
¿Procedo?
```

## Stage 2 — Execution
1. **Verificación previa del ambiente:** build y rama del C-12, migraciones y variables del C-09, datos de *Datos de prueba* listos. Si falla, aplicar el gate de bloqueo; nunca probar sobre otra rama.
2. **Ejecutar en el orden del plan.** Por TC: presentar precondición, pasos y resultado esperado (REQ-ID) → ejecutar → comparar → registrar.
   - **Modo A (manual):** QA ejecuta y describe lo observado; la IA registra, genera queries y documenta. La IA no hace clics.
   - **Modo B (Canal 1):** credenciales desde `.env` del catalyst (registrar solo el usuario; no imprimir valores); navegador **visible**; URL del ambiente del C-12 (si difiere de `IONFLOW_ENVIRONMENT_URL`, confirmar con QA). Login en Keycloak (`#username`, `#password`, `#kc-login`) y confirmar a QA. Por cada TC: **anunciar → esperar → navegar → ejecutar (anunciando cada clic) → capturar → reportar**. Selectores: L2 del módulo; genéricos `role="menuitem"` (sidebar), `role="button"` con nombre, `label`/`placeholder` (inputs), `tr[data-pc-section='bodyrow']` (tablas PrimeVue), `role="dialog"`, `.p-toast-message`. QA puede decir "para" en cualquier momento.
3. **Verificación posterior a la acción.** Un toast de éxito o una redirección no aprueban un TC: verificar persistencia (recargar la vista o el listado), consistencia de los datos y permisos en las vistas afectadas. Un TC de flujo completo se aprueba cuando se verifica el último paso de la cadena.
4. **Registrar en tiempo real.** Actualizar `ESTADO` y `EVIDENCIA` en `test-matrix.md` **y** `.csv` después de cada TC: `Aprobado` · `Fallido` (con `OBS-xx` en EVIDENCIA) · `Omitido` (justificación en EVIDENCIA) · `Bloqueado` (motivo). **La IA sugiere; QA confirma** cada resultado antes de registrarlo. Capturas en `screenshots/<TC-ID>-<paso>.png`; ante un fallo, captura inmediata `screenshots/<TC-ID>-fallo.png` (evidencia permanente).
5. **Evidencia en BD.** Queries de solo lectura desde las migraciones (`../gateway/database/migrations/*.php` para PostgreSQL; `../flow_binaries/migrations/*.sql` para el esquema de ejecuciones, consultado vía UI o API del historial), con la migración fuente como comentario. QA ejecuta en DBeaver y pega el resultado; se guarda en la sección *Verificación en BD* de la matriz con `Coincide / No coincide`, y la EVIDENCIA del TC la referencia.
6. **Clasificar cada hallazgo** (doc 05 §8.1):
   - **¿Lo regula un REQ vigente o el contrato referenciado?** No, o está en *Fuera de alcance* → **hallazgo fuera de matriz**: no bloquea ni suma Rejection_count. Preparar el ticket nuevo con `skills/bug-reporter/create.md` (`fuera-de-matriz`, `det-mock`, relación con este ticket) y el borrador **C-17**.
   - **Sí, y se incumple el "¿Qué debe pasar?"** → **`OBS-xx`** con el formato de C-14: severidad (prioridad de §10), REQ-ID, área/flujo, pasos, resultado esperado según el REQ, resultado actual, evidencia, ambiente/rama/PR.
   - **QA y Dev no coinciden en la interpretación** → borrador **C-15** (punto exacto, postura de cada parte en 1–2 líneas, impacto) + tag `escalado-po`; el PO decide en 4 h hábiles (C-16). Se sigue con los demás REQ; nadie continúa con una interpretación propia.
   - **`urgent` provocado por el cambio** (regresión, pérdida de datos, seguridad, cobro incorrecto) → `OBS-xx` y motivo de rechazo aunque no esté en un REQ. **`urgent` preexistente**, no provocado por el cambio → ticket nuevo inmediato (`det-mock`) y aviso al PO; no bloquea este ticket.
   - **Falla de un TC `Zona cercana` o `Exploratorio`:** es rechazo solo si es una regresión provocada por el cambio; si no, C-17.
   - **Requerimiento tardío** (algo que "debería" hacer y no está en la matriz): no es rechazo. Opción preferida: aprobar con la matriz vigente + ticket nuevo. Si el PO exige incluirlo → cambio de alcance (`requirements/matrix.md`, Modo C): vuelve a `to do` con C-08, sin Rejection_count.
7. **Re-test (iteración > 1):** cada observación se marca **Nuevo**, **Persistente** o **Regresión** respecto de la iteración anterior. Lo nuevo fuera de matriz sigue la regla C-17.
8. **Bloqueos durante la ejecución (§8.3):** si un impedimento detiene la prueba (ambiente caído, dependencia o servicio externo, definición pendiente), borrador **C-20** con el tag de causa (`bloq-ambiente`, `bloq-dependencia`, `bloq-externo`, `bloq-definicion`), estado previo y plan de acción. Si solo afecta a un REQ, seguir con los demás (avance sin bloqueos).
9. **Canal 2 (opcional):** si una zona cercana ya tiene spec en bot-test y existe un perfil del ambiente de QA, ejecutarla según `skills/_shared/bot-test.md` (sin modificar bot-test) y registrar el resumen como evidencia del TC de regresión.

## Stage 3 — Reporting
- `test-matrix.md` y `test-matrix.csv` actualizados con estados y evidencia; `screenshots/`; queries con resultados.
- Lista de `OBS-xx` (en `ticket-memory.md` hasta el reporte) y borradores en `comments/`: `C-15-<fecha>.md`, `C-17-<fecha>.md`, `C-20-<fecha>.md`, según correspondan.
- Resumen para QA:
```
📊 EJECUCIÓN — <id> — iteración <N>
TC: <n> · ✅ <n> · ❌ <n> · ⏭️ <n> · ⛔ <n> | REQ críticos aprobados: <n>/<n>
OBS: <n> (urgent <n> · high <n> · normal <n> · low <n>) · Fuera de matriz: <n> · Escalados al PO: <n>
```
- **Siguiente paso obligatorio:** `mock-testing/report.md`. La sesión no termina sin el reporte.

## Reglas
- QA rechaza **solo** contra la matriz con VoBo vigente (y el contrato que referencia); implementar algo distinto de lo acordado sí es motivo de rechazo.
- La IA nunca marca un TC como aprobado o fallido sin la confirmación de QA, ni emite el veredicto.
- Canal 1 solo con el navegador visible y QA supervisando; nunca para automatización permanente (eso es bot-test).
- Toda observación lleva pasos, REQ-ID, esperado vs. actual, evidencia, ambiente/rama/PR y severidad; datos sensibles enmascarados.
- Nada se publica en ClickUp desde la skill: QA publica los borradores y gestiona tags y estados.
