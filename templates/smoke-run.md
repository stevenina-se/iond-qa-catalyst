# Smoke maestro — [producto] v[X.Y.Z] — [preprod | producción]

> **Plantilla del QA Catalyst** — ejecución del smoke maestro (REL-03 en preprod · ACT-02 en producción · `Q-47`, `Q-52` · fuente canónica §7.7).
> **Se guarda en:** `knowledge/releases/[producto]/v[X.Y.Z]/smoke-preprod.md` o `smoke-prod.md` · **Skill:** `skills/release/smoke.md` · Comentario **C-25** (preprod) o **C-31** (producción).
> La lista es **única y fija** (SMK-01…SMK-17) y se copia de `knowledge/test-suites/smoke-master.md`; si difieren, prevalece el maestro. No incluye verificaciones de la versión: esas van en `sanity`.

## Encabezado

| Campo | Valor |
|---|---|
| Producto / versión | [iond / IonMind / StageMind] v[X.Y.Z] |
| Ambiente | preprod / producción (company de prueba) |
| Build / commit | [commit RC del C-23 (preprod) o del C-30 (producción)] |
| Fecha · inicio – fin | [AAAA-MM-DD] · [hh:mm] – [hh:mm] (producción: ≤ 2 h tras el C-30) |
| QA | @[qa] |
| Perfil de ambiente | `.env.preprod` / `.env.prod-testco` (solo el nombre; nunca valores) |
| Tarea de Release | [Release producto - vX.Y.Z] — [url] |

## Ejecución automática

| Campo | Valor |
|---|---|
| Comando (desde `../bot-test/apps/bot-test`) | `npx playwright test [specs] --config=tests/IONFLOW/playwright.ionflow.config.ts --project=ionflow-chromium -g "[IDs]"` |
| Resultado | [n] ✅ · [n] ❌ · [n] omitidos — duración [mm:ss] |
| Reporte HTML | `apps/bot-test/test-results/[JOB_ID / local]/` |

## Resultados

Resultado: ✅ · ❌ · ⏭️ (no aplica al producto del release, con motivo). Ejecución: Automática / Manual.

| ID | Producto | Verificación | Resultado esperado | Core | Ejecución | Resultado | Evidencia | Observación |
|---|---|---|---|---|---|---|---|---|
| SMK-01 | iond | **Login SSO** del usuario de la company: la app redirige a Keycloak, se ingresa y vuelve a la app | Dashboard visible, sin error de callback | ✅ | | | | |
| SMK-02 | iond | **Dashboard y navegación**: tarjetas, historial reciente y accesos del menú lateral | Carga sin errores ni paneles de acceso restringido; cada acceso del menú abre su vista | ✅ | | | | |
| SMK-03 | iond | **Crear un board** `autobot-smoke-<fecha>` con un trigger Webhook y un nodo (HTTP Request o Code) y guardarlo (commit) | El board aparece en la lista; el commit queda en el historial | ✅ | | | | |
| SMK-04 | iond | **Ejecutar en test** el board (preview / ejecución de prueba) | La ejecución termina con resultado por nodo | ✅ | | | | |
| SMK-05 | iond | **Ejecutar en producción**: activar el board, disparar el webhook y revisar el historial; luego pausar y **eliminar** el board | La ejecución aparece en Execution History con detalle por nodo y consumo registrado; el board queda eliminado | ✅ | | | | |
| SMK-06 | iond | **Webhooks**: el listado carga | Tabla con columnas y sin errores | | | | | |
| SMK-07 | iond | **Connections y App Connectors**: los listados cargan | Tablas sin errores | | | | | |
| SMK-08 | iond | **Persistent Data**: pestañas Data Store y Data Structure | Listados sin errores | | | | | |
| SMK-09 | iond | **PDF Templates**: listado y preview de la plantilla fija de la company de prueba | Se muestra el Blueprint Preview | | | | | |
| SMK-10 | iond | **Credentials**: el listado carga | Tabla sin errores | | | | | |
| SMK-11 | iond | **Notificaciones**: la campana abre el panel | Panel con notificaciones o estado vacío | | | | | |
| SMK-12 | iond | **Suscripción y consumo**: plan vigente y consumo visibles | Datos del plan y consumo coherentes con SMK-05 | | | | | |
| SMK-13 | iond (admin) | **Admin**: login, listado de companies e información de una company | Secciones visibles y company ACTIVE | | | | | |
| SMK-14 | Gateway | **Admin Gateway**: login y listado de Apps | Listado sin errores | | | | | |
| SMK-15 | iond · IonMind · StageMind | **Health de servicios**: endpoints de salud de la API de iond, IonMind y StageMind | Respuesta OK de cada servicio | ✅ | | | | |
| SMK-16 | IonMind | **Flujo de IA desde iond**: Flow Pilot con una consulta sobre el board de SMK-03 | Respuesta no vacía, sin errores de sesión ni de créditos; se valida la estructura, no el texto | | | | | |
| SMK-17 | StageMind | **Flujo representativo de StageMind** | Por definir | | | | | |

**Totales:** ✅ [n] · ❌ [n] · ⏭️ [n] · automáticos [n] · core [n/6]

## Regla de core

- **Core:** SMK-01 a SMK-05 y SMK-15.
- **Preprod:** si un SMK del core falla, no se inicia `sanity` en el área afectada y se decide **fix-forward** (C-28, subtarea con `fix-forward`) o **NO-GO**. Una falla fuera del core es un hallazgo con su severidad; el release continúa.
- **Producción:** una falla del core abre **hotfix** (C-32) o rollback (ver `deployment-protocol.md`); se avisa de inmediato al LD/RM y al PO.

## Limpieza de datos (obligatoria)

- [ ] Board `autobot-smoke-[AAAAMMDD]` pausado y eliminado (SMK-05), junto con su webhook.
- [ ] Ningún dato con prefijo `autobot-smoke-` remanente.
- [ ] Plantilla `autobot-smoke-template` intacta (es precargada; no se borra).
- [ ] Verificaciones sin borrado en la app ejecutadas en modo lectura.
- [ ] Producción: solo la company de prueba; la cuenta de administración solo en SMK-13 y SMK-14 (lectura).

## Fallas y hallazgos

| ID | SMK | Clasificación | Severidad | Decisión | Ticket / subtarea |
|---|---|---|---|---|---|
| [...] | SMK-[nn] | Real / inestable / ambiente / dato de prueba | `urgent` / `high` / `normal` / `low` | Fix-forward (C-28) / Improvements con `det-smoke` (o `det-prod`) / hotfix (C-32) | #[id] |

## Borrador del comentario

**Preprod — C-25** (texto de `templates/comments/C-25.md`):

```markdown
## 🧪 SMOKE — [producto vX.Y.Z] — [✅ / ❌]
**Ejecutados:** [N] · ✅ [n] · ❌ [n] · ⏭️ [n] · **Automatizados:** [n]
**Hallazgos:** [ID — severidad — decisión: fix-forward / Improvements #id / diferido]
**Evidencia / matriz:** [link]
```

**Producción — C-31** (texto de `templates/comments/C-31.md`):

```markdown
## 🔎 POST-DEPLOY — [✅ estable / ❌ incidente]
**Smoke en producción (company de prueba):** [n/n] · **Limpieza de datos:** ✅ · **Monitoreo 48 h:** [en curso / OK]
**Incidentes:** [#id hotfix]
```
