# Skill: mock-testing/report

> Cierra `mock testing`: genera el **`qa-report.md` obligatorio** (trazabilidad REQ → TC → resultado → evidencia), sugiere el veredicto con el criterio de aprobación del estándar de QA y prepara el comentario que QA firma: **C-13** (→ `uat` si tiene `uat-requerido`, si no → `ready to merge`) o **C-14** (→ `to do`, Rejection_count + 1, iteración N+1). Deja los candidatos para automatización y para la regresión. Estado `mock testing` (**D-11** / **I-07**); reglas §8.1–8.2, §9.3; doc 05 §3, §5.2, §8.3.

## Cuándo usar
- Al terminar `mock-testing/execute.md` (todos los TC con estado final), **siempre**, sea cual sea el resultado.
- Frase disparadora: `Reporte de pruebas del ticket <id>`

## Pre-requisitos (gates)
| Check | Si falla |
|---|---|
| Ningún TC en `Pendiente` en `test-matrix.md` (los no ejecutados están `Omitido` o `Bloqueado` con motivo) | PARAR → completar con `mock-testing/execute.md` |
| `.md` y `.csv` de la matriz de pruebas coinciden | Sincronizar antes de reportar |
| Cada `OBS-xx` tiene REQ-ID, severidad, pasos, esperado vs. actual y evidencia | Completar la observación |
| No hay un `escalado-po` abierto sobre un REQ que decide el veredicto | Esperar el C-16 (SLA 4 h hábiles) o reportar con ese REQ pendiente |

## Contexto a cargar
- **L1:** `sdlc-consolidation.md` (§5 D-11 a D-13, §6 I-07, §8.1–8.2, §10, §14 C-13, C-14, C-17, C-18) · doc 05 (§3.A criterio de aprobación, §3.B, §5.2, §6.4, §8.3, §8.4).
- **L3:** `test-matrix.md` + `.csv`, `requirements-matrix-v<N>.md` (o T-02), `code-review-qa.md`, `screenshots/`, `ticket-memory.md`, reportes de iteraciones anteriores.
- **ClickUp:** tags (`uat-requerido`, `po-vobo`, `escalado-po`), Rejection_count, C-16 recientes, PRs (Merge Request 1–4).
- Plantillas: `templates/qa-report.md`, `templates/approval.md` (= C-13), `templates/rejection.md` (= C-14).

## Stage 1 — Planning
```
🔄 SIGUIENTE SKILL OBLIGATORIO: mock-testing/report — iteración <N>
   Ticket: <id> · <tablero> · matriz v<N> · TC: ✅ <n> ❌ <n> ⏭️ <n> ⛔ <n> · OBS: <n> · fuera de matriz: <n>
   Output esperado: L3/<id>/qa-report.md (o qa-report-iter<N>.md) + comments/C-13|C-14-<fecha>.md + test-matrix.md/.csv finales
¿Procedo?
```

## Stage 2 — Execution
1. **Consolidar resultados por REQ.** Para cada REQ: TC asociados, resultado (✅ todos aprobados · ❌ algún TC fallido · ⏳ pendiente de decisión del PO) y evidencia. Totales de la matriz: ejecutados, aprobados, fallidos, omitidos (con justificación), bloqueados.
2. **Consolidar hallazgos de todas las fuentes:** `OBS-xx` de la ejecución, hallazgos del code review verificados (confirmados o descartados en su TC con `ORIGEN = Code review`, según el mapeo `CR-xx → TC-nn` de `code-review-qa.md`), hallazgos fuera de matriz (con su ticket), urgentes preexistentes y escalamientos (C-15/C-16).
3. **Evaluar el criterio de aprobación.**
   - *Discovery y mejoras con matriz o mini-matriz* (doc 05 §3.A): **100 % de los REQ críticos aprobados** · **cero hallazgos `urgent` abiertos** · **ningún REQ incumplido** · **regresión de zonas cercanas en verde** (solo cuenta como falla la provocada por el cambio).
   - *Bug de Improvements* (I-07, doc 05 §3.B): se cumple el resultado esperado del T-02 · el C-09 menciona la prueba unitaria que certifica la corrección · pasa el checklist de no regresión de zonas cercanas.
   - Un REQ *Pendiente de decisión PO* no es criterio de rechazo: el ticket se aprueba cuando el REQ se resuelve o el PO divide el alcance (`Q-27`, C-16 + C-08).
4. **Sugerir el veredicto** con su justificación (cada criterio ✅/❌):
   - **APROBADO** → C-13. Destino: `uat` si el ticket es de Discovery y tiene `uat-requerido` (A-10 lo fuerza); si no, `ready to merge`.
   - **RECHAZADO** → C-14. Destino: `to do`; Rejection_count + 1 (uno por iteración, no por observación).
   - ⚠️ **La IA sugiere; QA firma.** Si QA cambia la sugerencia, registrar su motivo en el reporte.
5. **Coherencia (doc 05 §5.2):** C-13 solo si todos los TC de todos los REQ están aprobados u omitidos con justificación; C-14 cita los REQ-ID de los TC fallidos; los totales del comentario son los de la matriz.
6. **Preparar el comentario** con la plantilla:
   - **C-13** (`templates/approval.md`): versión de la matriz con VoBo, tabla `REQ | Resultado | Evidencia`, TC ejecutados, regresión de zonas cercanas, hallazgos fuera de matriz (`#id — fuera-de-matriz` o Ninguno), ambiente/rama/PRs, destino.
   - **C-14** (`templates/rejection.md`): iteración y nuevo Rejection_count, versión de la matriz, una sección `OBS-xx — <prioridad> — REQ-xx — Estado: Nuevo/Persistente/Regresión` por observación (área/flujo, pasos, esperado según el REQ, actual, evidencia con la ruta de la captura), hallazgos fuera de matriz (no son causa de rechazo), ambiente/rama/PRs, `→ TO DO`.
   - **C-17** pendientes, si alguno no se preparó en la ejecución.
7. **Si el destino es `uat`:** preparar en el reporte el guion de UAT (REQ críticos, datos y pasos para el cliente o SH) y los datos en el ambiente de QA o preprod (`Q-16`). El resultado lo registra el PO en C-18; QA acompaña y clasifica observaciones (contradice la matriz → `to do`; nueva → ticket nuevo).
8. **Si el veredicto es rechazo — iteración N+1:** el reporte de esta iteración queda congelado (su trazabilidad conserva los resultados de cada TC); el de la siguiente será `qa-report-iter<N+1>.md`. Dejar listas en el reporte las filas de re-test (TC fallidos con su `OBS-xx`, TC de REQ críticos de las áreas del fix, TC de `Zona cercana`) para `mock-testing/plan.md` en modo re-test.
9. **Candidatos para después del cierre:**
   - *Sanity del release* (`Q-48`): TC con `USO = Sanity` (REQ críticos), que se re-ejecutarán como `SAN-<ticket>-<REQ>`. Confirmar que todos estén aprobados.
   - *Automatización:* TC aprobados con `AUTOMATIZABLE = Sí`, estables, de UI de `gateway-ion` o de API, priorizando REQ críticos → entrada de `skills/automation/plan.md` (se ejecuta después de `merged`).
   - *Regresión:* TC con `USO = Regresión candidata` → filas nuevas o cambios para el E2E maestro (hoja "Iond Testing Plan"; `knowledge/test-suites/e2e-master.csv` no se edita a mano), con SIDE, módulo, ruta y prioridad propuestos.
   - *Conocimiento L2:* edge cases, queries útiles y archivos centinela descubiertos, anotados en `ticket-memory.md` para `skills/knowledge/update-module.md` después del despliegue del release.

## Stage 3 — Reporting
- `knowledge/L3-tickets/<id>/qa-report.md` (iteración 1) o `qa-report-iter<N>.md` (iteración N ≥ 2) con `templates/qa-report.md`: *Información* · *1. Criterio de aprobación* · *2. Trazabilidad REQ → TC → resultado* · *3. No regresión de zonas cercanas* · *4. Hallazgos que causan rechazo* · *5. Fuera de matriz* · *6. Desacuerdos y decisiones del PO* · *7. Veredicto* (sugerido y firmado por QA) · *8. Candidatos* (sanity, automatización, E2E maestro) · *Evidencia*. Si aplican, agregar al final *Guion de UAT* y *Re-test (iteración N+1)*. Las notas para L2 van a `ticket-memory.md`.
- `test-matrix.md` y `test-matrix.csv` con los estados finales.
- `comments/C-13-<fecha>.md` o `comments/C-14-<fecha>.md` (+ `C-17-<fecha>.md` pendientes).
- `ticket-memory.md`: veredicto, fecha, iteración, Rejection_count, destino.
- **Acciones manuales para QA:** publicar el comentario; si rechaza, actualizar Rejection_count (+1; A-09 lo recuerda) y mover a `to do`; si aprueba, mover a `uat` o `ready to merge` (la versión objetivo la registran el SM y el RM — A-11).

```
✅/❌ CIERRE DE MOCK TESTING — <id> — iteración <N>
REQ críticos: <n>/<n> · REQ incumplidos: <n> · urgent abiertos: <n> · regresión cercana: ✅/❌
Veredicto sugerido: APROBADO → <uat | ready to merge> / RECHAZADO → to do (Rejection_count <n>)
Veredicto de QA: <pendiente de firma> · Comentario: comments/C-1x-<fecha>.md
```

## Reglas
- **El reporte es obligatorio:** ninguna sesión de `mock testing` termina sin `qa-report.md`, matriz actualizada y comentario preparado.
- El veredicto debe coincidir con la Matriz de Pruebas; QA rechaza solo contra la matriz con VoBo vigente.
- Los hallazgos fuera de matriz no bloquean ni suman Rejection_count; un requerimiento tardío exigido por el PO es C-08, no C-14.
- En el re-test no se exige repetir etapas aprobadas (Pilot, definiciones).
- El historial de iteraciones se conserva; nunca se sobrescribe un reporte anterior.
