# Smoke maestro — IOND

> **Única y fija para todo release** de iond, IonMind o StageMind (`Q-47`). La misma lista corre como **gate en preprod** (REL-03, comentario C-25) y **después del despliegue en producción** con la company de prueba (ACT-02, comentario C-31, `Q-52`).
> No incluye verificaciones de la versión: esas van en `sanity` (`Q-48`).
> Cambiar esta lista requiere acuerdo del LQA con el LD/RM y se registra en el historial al final del archivo.

## Reglas

- **Core del smoke:** SMK-01 a SMK-05 y SMK-15. Si alguno falla, no se inicia `sanity` en el área afectada y se decide fix-forward o NO-GO (fuente canónica §7.5). Una falla fuera del core es un hallazgo con su severidad; el release continúa.
- **Datos:** todo lo que el smoke crea lleva el prefijo `autobot-smoke-` y se elimina al terminar. Las verificaciones sin borrado en la app se hacen en modo lectura.
- **Producción:** solo con la **company de prueba** (AV-09). Credenciales en el `.env.prod-testco` de la máquina del QA, nunca en un repositorio. El smoke de producción no usa la cuenta de administración salvo SMK-13 y SMK-14, que son de solo lectura.
- **Timebox:** ≤ 0,5 día manual; objetivo ≈ 15 min automatizado. En producción, ≤ 2 h tras el despliegue.
- **Resultado:** cada fila se marca ✅ / ❌ / ⏭️ (no aplica al producto del release, con motivo). El consolidado va al C-25 o C-31 y a `knowledge/releases/<producto>/<versión>/smoke-<ambiente>.md`.

## Lista

| ID | Producto | Verificación | Resultado esperado | Datos y limpieza | Core | Automatización hoy | Filas E2E |
|---|---|---|---|---|---|---|---|
| SMK-01 | iond | **Login SSO** del usuario de la company: la app redirige a Keycloak, se ingresa y vuelve a la app | Dashboard visible, sin error de callback | — | ✅ | Spec existente rota (`company-login.spec.ts`, Ola 0) | E2E-KC-AUT-002 |
| SMK-02 | iond | **Dashboard y navegación**: tarjetas, historial reciente y accesos del menú lateral | Carga sin errores ni paneles de acceso restringido; cada acceso del menú abre su vista | — | ✅ | `TC-DASH-01` (rama E2E) | E2E-TEN-DSH-001 |
| SMK-03 | iond | **Crear un board** `autobot-smoke-<fecha>` con un trigger Webhook y un nodo (HTTP Request o Code) y guardarlo (commit) | El board aparece en la lista; el commit queda en el historial | Crea 1 board (se borra en SMK-05) | ✅ | Nueva (propuesta Ola 1); base: `TC-BOARD-CRUD-01`, `TC-BOARD-CMT-05` | E2E-TEN-BRD (New Board, Commit › Save) |
| SMK-04 | iond | **Ejecutar en test** el board (preview / ejecución de prueba) | La ejecución termina con resultado por nodo | — | ✅ | Nueva (Ola 1) | E2E-TEN-BRD (Preview) |
| SMK-05 | iond | **Ejecutar en producción**: activar el board, disparar el webhook y revisar el historial; luego pausar y **eliminar** el board | La ejecución aparece en Execution History con detalle por nodo y consumo registrado; el board queda eliminado | Limpieza obligatoria del board y su webhook | ✅ | Nueva (Ola 1) | E2E-TEN-EXH (Details), E2E-TEN-BRD (Active-Pause, Delete) |
| SMK-06 | iond | **Webhooks**: el listado carga | Tabla con columnas y sin errores | Solo lectura | | Nueva (Ola 1) | E2E-TEN-WHK |
| SMK-07 | iond | **Connections y App Connectors**: los listados cargan | Tablas sin errores | Solo lectura | | Nueva (Ola 1) | E2E-TEN-CNX, E2E-TEN-APC |
| SMK-08 | iond | **Persistent Data**: pestañas Data Store y Data Structure | Listados sin errores | Solo lectura (la app no permite borrar) | | Nueva (Ola 1) | E2E-TEN-PDS |
| SMK-09 | iond | **PDF Templates**: listado y preview de la plantilla fija de la company de prueba | Se muestra el Blueprint Preview | Plantilla `autobot-smoke-template` precargada (AV-09) | | `TC-PDF-21` (rama E2E; requiere la plantilla precargada) | E2E-TEN-PDF (Actions › Preview) |
| SMK-10 | iond | **Credentials**: el listado carga | Tabla sin errores | Solo lectura | | Nueva (Ola 1) | E2E-TEN-CRD |
| SMK-11 | iond | **Notificaciones**: la campana abre el panel | Panel con notificaciones o estado vacío | Solo lectura | | `TC-NOTIF-01` (rama E2E) | E2E-TEN-NTF (Open) |
| SMK-12 | iond | **Suscripción y consumo**: plan vigente y consumo visibles | Datos del plan y consumo coherentes con SMK-05 | Solo lectura; el flujo de cobro se prueba en el baseline de regresión | | Nueva (Ola 1) | E2E-ADM-CMP (Subscription) |
| SMK-13 | iond (admin) | **Admin**: login, listado de companies e información de una company | Secciones visibles y company ACTIVE | Solo lectura | | Spec existente rota (`companies.spec.ts`, Ola 0) | E2E-ADM-CMP-001 |
| SMK-14 | Gateway | **Admin Gateway**: login y listado de Apps | Listado sin errores | Solo lectura | | Nueva (Ola 3) | E2E-GTW-APP |
| SMK-15 | iond · IonMind · StageMind | **Health de servicios**: endpoints de salud de la API de iond, IonMind y StageMind | Respuesta OK de cada servicio | Endpoints definidos por el LD (AV-11) | ✅ | Nueva (Ola 1, prueba de API) | — |
| SMK-16 | IonMind | **Flujo de IA desde iond**: Flow Pilot con una consulta sobre el board de SMK-03 | Respuesta no vacía, sin errores de sesión ni de créditos; se valida la estructura, no el texto | Consume créditos de IA de la company de prueba | | `TC-BOARD-FP-01`, `TC-BOARD-FP-02` (rama E2E) | E2E-TEN-BRD (Flow Pilot) |
| SMK-17 | StageMind | **Flujo representativo de StageMind** | Por definir | Por definir | | Pendiente de definición (AV-12) | — |

## Ejecución automatizada

Mientras bot-test no tenga la etiqueta `@smoke` (AV-11), el catalyst arma el comando con los IDs de los tests existentes del smoke (ver `knowledge/test-suites/README.md`, sección *Ejecutar en bot-test*). Hoy son ejecutables desde la rama E2E: `TC-DASH-01`, `TC-NOTIF-01`, `TC-PDF-21`, `TC-BOARD-FP-01` y `TC-BOARD-FP-02`. Las filas sin automatización se ejecutan a mano.

## Historial

| Fecha | Cambio |
|---|---|
| 2026-10-10 | Primera versión del smoke maestro (Q-47). |
