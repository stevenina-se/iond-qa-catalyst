# Skill: release/smoke

> Ejecuta el **smoke maestro** (SMK-01…SMK-17), igual para todo release (`Q-47`), en dos modos: **gate en preprod** (REL-03, C-25) y **post-despliegue en producción** con la company de prueba (ACT-02, C-31, `Q-52`).
> Fuente: `knowledge/test-suites/smoke-master.md`. No se agregan verificaciones de la versión: esas van en `release/sanity`.

## Cuándo usar

| Modo | Momento | Frase disparadora |
|---|---|---|
| Preprod | Tarea de Release en `smoke` (lunes PM – martes AM) | `Ejecutar smoke: <producto> vX.Y.Z preprod` |
| Producción | Tras el C-30 del despliegue (≤ 2 h) | `Ejecutar smoke: <producto> vX.Y.Z producción` |

## Pre-requisitos (gates)

| Check | Si falla |
|---|---|
| Preprod: C-23 (preprod desplegado) y C-24 en verde | No iniciar el smoke con el pipeline en rojo; informar al RM |
| Producción: C-30 publicado | Esperar el despliegue |
| Producción: existe la company de prueba y su perfil `.env.prod-testco` (AV-09) | PARAR: el smoke de producción no se ejecuta con cuentas de clientes |
| Perfil del ambiente disponible en la máquina del QA | Pedir al QA que lo cargue (no leer sus valores) |

## Contexto a cargar

`knowledge/test-suites/smoke-master.md`, `skills/_shared/bot-test.md`, `skills/_shared/evidence.md`, `knowledge/releases/<producto>/<versión>/release-task.md`.

## Stage 1 — Planning

Anunciar el modo, el ambiente, el build/commit (del C-23 o C-30), qué SMK son automáticos hoy y cuáles manuales, y el comando de bot-test. Esperar confirmación.

## Stage 2 — Execution

1. Copiar `templates/smoke-run.md` a `knowledge/releases/<producto>/<versión>/smoke-preprod.md` (o `smoke-prod.md`).
2. **Automático.** Ejecutar los tests existentes del smoke (columna *Automatización hoy* del maestro) con el perfil del ambiente:
   ```bash
   npx playwright test <specs del smoke> --config=tests/IONFLOW/playwright.ionflow.config.ts --project=ionflow-chromium -g "TC-DASH-01|TC-NOTIF-01|TC-PDF-21|TC-BOARD-FP-01|TC-BOARD-FP-02"
   ```
   Cuando bot-test tenga la etiqueta `@smoke`, usar `-g @smoke` (y `@prod-safe` en producción).
3. **Manual.** Ejecutar el resto en orden SMK-01 → SMK-17 (Canal 1 opcional, con el QA supervisando). Para SMK-03 a SMK-05 usar el nombre `autobot-smoke-<AAAAMMDD>`.
4. **Productos.** Marcar ⏭️ con motivo lo que no aplica (por ejemplo, SMK-17 mientras AV-12 esté abierta).
5. **Limpieza** (obligatoria): board y webhook de smoke eliminados; ningún dato `autobot-smoke-` remanente. Registrar el checklist.
6. **Fallas.** Clasificar cada falla automática (real / inestable / ambiente / dato de prueba; ver `release/regression.md` § *Clasificar fallas*). Una falla real se registra con severidad (prioridad nativa).
7. **Regla de core** (SMK-01 a SMK-05 y SMK-15): si falla, no se inicia `sanity` en el área afectada y se propone **fix-forward** (C-28, subtarea con `fix-forward` en la tarea de Release) o NO-GO. En producción, una falla del core abre **hotfix** (C-32) y se avisa de inmediato al LD/RM y al PO.

## Stage 3 — Reporting

- `smoke-preprod.md` o `smoke-prod.md` con resultados, evidencia, limpieza y hallazgos.
- Borrador **C-25** (preprod) o **C-31** (producción) en `comments/`.
- Hallazgos no bloqueantes → propuesta de ticket en Improvements `backlog` con `det-smoke` (o `det-prod`), previa discusión con PO y LD.
- Siguiente skill: `release/sanity` (preprod) o cierre del release + monitoreo 48 h (producción).

## Reglas

- La lista del smoke **no se edita** en esta skill; los cambios se hacen en `smoke-master.md` con acuerdo del LQA y el LD/RM.
- En producción: solo company de prueba, solo verificaciones del smoke, y limpieza verificada antes de cerrar el C-31.
- La IA sugiere ✅/❌; **el QA firma** cada resultado.
