# Smoke maestro — iond v0.2.0 (beta) + IonMind v1.10.2 — preprod

> **Ejecución del smoke maestro** (REL-03 · `Q-47`, `Q-52` · fuente canónica §7.7) · Skill `skills/release/smoke.md` · Comentario **C-25**.
> Lista **única y fija** (SMK-01…SMK-17) copiada de `knowledge/test-suites/smoke-master.md`; si difieren, prevalece el maestro. No incluye verificaciones de la versión (van en `sanity-matrix.md`).
> **Casos, datos y orden de ejecución:** `smoke-matrix.md`; la hoja de ejecución es `smoke-matrix-preprod.csv`. SMK-15 se ejecuta primero y SMK-16 antes de SMK-05, que elimina el board del smoke. Las notas de la columna *Observación* solo indican dónde el release cambió la pantalla que recorre el smoke.

## Encabezado

| Campo | Valor |
|---|---|
| Producto / versión | iond v0.2.0 + IonMind v1.10.2 (sistema integrado) |
| Ambiente | preprod — `preprod-app.iond.ai` |
| Build / commit | Commit RC del C-23 (por repo) |
| Fecha · inicio – fin | 2026-10-12 PM – 2026-10-13 AM (cierre y C-25 antes del sanity) |
| QA | Steve Nina · Mijael Rojas |
| Perfil de ambiente | `.env.preprod` (solo el nombre; nunca valores) |
| Tarea de Release | Release iond - v0.2.0 — https://app.clickup.com/t/86e39jadr |

## Ejecución automática

| Campo | Valor |
|---|---|
| Comando (desde `../bot-test/apps/bot-test`, rama E2E) | `npx playwright test tests/IONFLOW/Company-ION/dashboard/company-dashboard.spec.ts tests/IONFLOW/Company-ION/boards/company-boards.spec.ts tests/IONFLOW/Company-ION/pdf-templates/company-pdf-templates.spec.ts tests/IONFLOW/Company-ION/notifications/company-notifications.spec.ts --config=tests/IONFLOW/playwright.ionflow.config.ts --project=ionflow-chromium -g "TC-BOARD-FP-01\|TC-BOARD-FP-02\|TC-DASH-01\|TC-NOTIF-01\|TC-PDF-21"` |
| Cubre | SMK-02 (`TC-DASH-01`) · SMK-09 (`TC-PDF-21`, requiere la plantilla `autobot-smoke-template`) · SMK-11 (`TC-NOTIF-01`) · SMK-16 (`TC-BOARD-FP-01/02`) |
| Resultado | [n] ✅ · [n] ❌ · [n] omitidos — duración [mm:ss] |
| Reporte HTML | `apps/bot-test/test-results/[JOB_ID / local]/` |

> Selectores que pueden romperse con el release: el menú se reorganizó (86e35882c) y la marca cambió (86e21f52d). Un test en rojo por un selector es 🔵 *test desactualizado*: se ejecuta a mano y se avisa al responsable de bot-test. No es una falla del core.

## Resultados

Resultado: ✅ · ❌ · ⏭️ (no aplica al producto del release, con motivo).

| ID | Producto | Verificación | Resultado esperado | Core | Ejecución | Resultado | Evidencia | Observación |
|---|---|---|---|---|---|---|---|---|
| SMK-01 | iond | **Login SSO** del usuario de la company: la app redirige a Keycloak, se ingresa y vuelve a la app | Dashboard visible, sin error de callback | ✅ | Manual | | | Login con la marca iond (rebranding) |
| SMK-02 | iond | **Dashboard y navegación**: tarjetas, historial reciente y accesos del menú lateral | Carga sin errores ni paneles de acceso restringido; cada acceso del menú abre su vista | ✅ | Automática + manual | | | Menú nuevo: OVERVIEW / AUTOMATE / RESOURCES / MARKETPLACE |
| SMK-03 | iond | **Crear un board** `autobot-smoke-20261012` con un trigger Webhook y un nodo (HTTP Request o Code) y guardarlo (commit) | El board aparece en la lista; el commit queda en el historial | ✅ | Manual | | | Primera vista de Boards rediseñada (86e223kvf) |
| SMK-04 | iond | **Ejecutar en test** el board (preview / ejecución de prueba) | La ejecución termina con resultado por nodo | ✅ | Manual | | | Play bloqueado durante la ejecución (86e2nazxp) |
| SMK-05 | iond | **Ejecutar en producción**: activar el board, disparar el webhook y revisar el historial; luego pausar y **eliminar** el board | La ejecución aparece en Execution History con detalle por nodo y consumo registrado; el board queda eliminado | ✅ | Manual | | | Historial dentro de Dashboard (86e35882c); consumo con el billing local (86e1pzyug) |
| SMK-06 | iond | **Webhooks**: el listado carga | Tabla con columnas y sin errores | | Manual | | | |
| SMK-07 | iond | **Connections y App Connectors**: los listados cargan | Tablas sin errores | | Manual | | | Connections dentro de Credentials (86e35882c) |
| SMK-08 | iond | **Persistent Data**: pestañas Data Store y Data Structure | Listados sin errores | | Manual | | | |
| SMK-09 | iond | **PDF Templates**: listado y preview de la plantilla fija de la company de prueba | Se muestra el Blueprint Preview | | Automática | | | |
| SMK-10 | iond | **Credentials**: el listado carga | Tabla sin errores | | Manual | | | |
| SMK-11 | iond | **Notificaciones**: la campana abre el panel | Panel con notificaciones o estado vacío | | Automática | | | Ahora por websockets con Bearer (86e35wv7f) |
| SMK-12 | iond | **Suscripción y consumo**: plan vigente y consumo visibles | Datos del plan y consumo coherentes con SMK-05 | | Manual | | | Billing en el menú de usuario, solo lectura (86e35882c, 86e1pzyug) |
| SMK-13 | iond (admin) | **Admin**: login, listado de companies e información de una company | Secciones visibles y company ACTIVE | | Manual | | | |
| SMK-14 | Gateway | **Admin Gateway**: login y listado de Apps | Listado sin errores | | Manual | | | |
| SMK-15 | iond · IonMind · StageMind | **Health de servicios**: endpoints de salud de la API de iond, IonMind y StageMind | Respuesta OK de cada servicio | ✅ | Manual | | | Endpoints definidos por el LD (AV-11); IonMind ya en v1.10.2 |
| SMK-16 | IonMind | **Flujo de IA desde iond**: Flow Pilot con una consulta sobre el board de SMK-03 | Respuesta no vacía, sin errores de sesión ni de créditos; se valida la estructura, no el texto | | Automática | | | Registra tokens y costo (86e1fawg0) |
| SMK-17 | StageMind | **Flujo representativo de StageMind** | Por definir | | — | ⏭️ | | No aplica: StageMind no está en el release y el flujo está pendiente de definición (AV-12) |

**Totales:** ✅ [n] · ❌ [n] · ⏭️ [n] · automáticos [n]/4 · core [n/6]

## Regla de core

- **Core:** SMK-01 a SMK-05 y SMK-15.
- Si un SMK del core falla, no se inicia `sanity` en el área afectada y se decide **fix-forward** (C-28, subtarea con `fix-forward`) o **NO-GO**. Una falla fuera del core es un hallazgo con su severidad; el release continúa.

## Limpieza de datos (obligatoria)

- [ ] Board `autobot-smoke-20261012` pausado y eliminado (SMK-05), junto con su webhook.
- [ ] Ningún dato con prefijo `autobot-smoke-` remanente.
- [ ] Plantilla `autobot-smoke-template` intacta (es precargada; no se borra).
- [ ] Verificaciones sin borrado en la app ejecutadas en modo lectura.

## Fallas y hallazgos

| ID | SMK | Clasificación | Severidad | Decisión | Ticket / subtarea |
|---|---|---|---|---|---|
| | | | | | |

## Borrador C-25

Se publica en la tarea de Release de iond el martes 13/10 por la mañana.

```markdown
## 🧪 SMOKE — iond v0.2.0 + IonMind v1.10.2 — [✅ / ❌]
**Ejecutados:** [N]/17 · ✅ [n] · ❌ [n] · ⏭️ 1 (SMK-17 no aplica) · **Automatizados:** [n]/4
**Hallazgos:** [ID — severidad — decisión: fix-forward / Improvements #id / diferido]
**Evidencia / matriz:** knowledge/releases/iond/v0.2.0/smoke-preprod.md
```
