# Matriz del smoke maestro — iond v0.2.0 (beta) + IonMind v1.10.2

> **Matriz paso a paso** del smoke maestro (`Q-47`) para el release beta. Cada verificación del maestro se baja a casos concretos con su resultado esperado, y en OBSERVACION se indica **qué cambió en esa pantalla con v0.2.0**, para que el QA no confunda un cambio de la versión con una falla.
> **No agrega verificaciones de la versión** (esas van en `sanity-matrix.csv`): solo adapta la navegación a la nueva interfaz. Fuente: `knowledge/test-suites/smoke-master.md`; si difieren, prevalece el maestro.
> **Hojas de ejecución:** `smoke-matrix-preprod.csv` (gate, lunes 12/10 PM – martes 13/10 AM → `smoke-preprod.md`, C-25) y `smoke-matrix-prod.csv` (post-despliegue con la company de prueba, viernes 16/10 ≤ 2 h tras el C-30 → `smoke-prod.md`, C-31). Las dos tienen las mismas filas; la de producción agrega en OBSERVACION lo que es de solo lectura o consume créditos.

## Qué es SMK y cómo se lee el ID

- **SMK-xx** es el código de una **verificación del smoke maestro**: la lista fija de 17 verificaciones (SMK-01…SMK-17) que corre igual en todos los releases, en preprod y en producción. El número de cada SMK no cambia de un release a otro, así se pueden comparar resultados entre versiones. La definición de cada una está en `knowledge/test-suites/smoke-master.md`.
- El **ID** de cada fila es `SMK-xx.n`: la verificación SMK-xx y su caso número *n*. Por ejemplo, `SMK-05.3` es el tercer caso de SMK-05 (*Ejecutar en producción*): revisar la ejecución en Execution History.
- **FEATURE** repite el código y el nombre de la verificación (`SMK-05 · Ejecutar en producción y limpiar`) para poder filtrar la hoja por verificación.
- **Core:** SMK-01 a SMK-05 y SMK-15 llevan PRIORIDAD `urgent`. Si fallan, no se inicia el sanity en el área y se decide fix-forward (C-28) o NO-GO; en producción, hotfix (C-32) o rollback. El resto lleva `high`: una falla es un hallazgo y el release continúa.

## Columnas de la hoja

| Columna | Contenido |
|---|---|
| ID | `SMK-xx.n` (verificación y caso) |
| PRIORIDAD | `urgent` = core · `high` = resto · `normal` = no aplica en este release (SMK-17) |
| SIDE · MODULE · FEATURE | Dónde se prueba, el módulo y la verificación del smoke maestro |
| CASO | La acción a ejecutar, con los datos que necesita |
| RESULTADO ESPERADO | Lo que tiene que pasar para aprobar |
| QA ASIGNADO | Flujo principal (SMK-15, 01–05 y 16): Mijael Rojas · verificaciones de lectura (SMK-06 a SMK-14): Steve Nina. El LQA puede reasignar |
| RESOLUCION | ✅ Aprobado · ❌ Fallido · ⏭️ No aplica / no ejecutado (con motivo en OBSERVACION) |
| OBSERVACION | Precargada con el tipo de ejecución (automática o manual) y el cambio de v0.2.0 en esa pantalla; el QA agrega sus notas |
| TICKET · PRIORIDAD BUG | Si el caso falla: URL del bug creado y su prioridad (`urgent`, `high`, `normal` o `low`) |

## Resumen

| Dato | Valor |
|---|---|
| Verificaciones | 17 SMK · 29 casos |
| Automáticas hoy | SMK-02, SMK-09, SMK-11, SMK-16 (5 tests de la rama E2E de bot-test) |
| No aplica | SMK-17 (StageMind no está en el release; AV-12) |
| Timebox | Preprod ≤ 0,5 día · producción ≤ 2 h |
| Ambientes | Preprod: `preprod-app.iond.ai` (perfil `.env.preprod`) · Producción: `app.iond.ai`, solo la company de prueba (perfil `.env.prod-testco`, AV-09) |

## Orden de ejecución

- **SMK-15 va primero:** si un servicio no responde, el resto del smoke no tiene sentido y se avisa al RM de inmediato.
- **SMK-16 va antes de SMK-05:** Flow Pilot consulta el board `autobot-smoke-<AAAAMMDD>`, y SMK-05 lo elimina al final.

`SMK-15 → SMK-01 → SMK-02 → SMK-03 → SMK-04 → SMK-16 → SMK-05 → SMK-06 … SMK-14 → SMK-17 (⏭️)`

## Prerrequisitos y datos

| Prerrequisito | Preprod | Producción |
|---|---|---|
| Despliegue | C-23 publicado y C-24 en verde | C-30 publicado |
| Company de prueba con usuario, plan y créditos de IA | Company de QA en preprod | Company de prueba dedicada (AV-09). Si no existe, el smoke de producción se limita a lectura, por decisión del Go/No-Go |
| Plantilla `autobot-smoke-template` precargada | Sí | Sí (AV-09) |
| Cuentas de administración (Admin y Admin Gateway) | Solo lectura (SMK-13 y SMK-14) | Solo lectura (SMK-13 y SMK-14) |
| Endpoints de salud de iond, IonMind y StageMind | Los define el LD (AV-11) | Los define el LD (AV-11) |
| Herramienta para disparar el webhook | curl o Postman | curl o Postman |
| Perfil de variables | `.env.preprod` (nunca se registran valores) | `.env.prod-testco` (nunca se registran valores) |

## Ejecución automática

Desde `../bot-test/apps/bot-test` (rama E2E), con el perfil del ambiente cargado:

```bash
npx playwright test tests/IONFLOW/Company-ION/dashboard/company-dashboard.spec.ts tests/IONFLOW/Company-ION/boards/company-boards.spec.ts tests/IONFLOW/Company-ION/pdf-templates/company-pdf-templates.spec.ts tests/IONFLOW/Company-ION/notifications/company-notifications.spec.ts --config=tests/IONFLOW/playwright.ionflow.config.ts --project=ionflow-chromium -g "TC-BOARD-FP-01|TC-BOARD-FP-02|TC-DASH-01|TC-NOTIF-01|TC-PDF-21"
```

Con el menú reorganizado y el rebranding, un test que falla por un selector es 🔵 *test desactualizado*: el caso se ejecuta a mano y se avisa al responsable de bot-test. No cuenta como falla del core.

## Matriz

PRIORIDAD, SIDE, MODULE, FEATURE y QA ASIGNADO van en el encabezado de cada verificación. RESOLUCION, TICKET y PRIORIDAD BUG se completan en la hoja de cada ambiente.

### 1. SMK-15 · Health de servicios

PRIORIDAD `urgent` · SIDE API · MODULE Health de servicios · QA ASIGNADO **Mijael Rojas** · Producto: iond · IonMind · StageMind · Filas E2E: — · Producción: Sí

| ID | CASO | RESULTADO ESPERADO | OBSERVACION |
|---|---|---|---|
| SMK-15.1 | Consultar el endpoint de salud de la API de iond. Datos: Endpoint de health definido por el LD (AV-11) | Respuesta OK (HTTP 200) | Manual (prueba de API) |
| SMK-15.2 | Consultar el endpoint de salud de IonMind. Datos: Endpoint de health de IonMind (AV-11) | Respuesta OK; si el endpoint informa la versión, es la v1.10.2 | Manual (prueba de API). Cambio en v0.2.0: IonMind v1.10.2 se despliega antes que iond |
| SMK-15.3 | Consultar el endpoint de salud de StageMind. Datos: Endpoint de health de StageMind (AV-11) | Respuesta OK (StageMind no cambia en este release, pero el servicio debe estar disponible) | Manual (prueba de API) |

### 2. SMK-01 · Login SSO

PRIORIDAD `urgent` · SIDE KC · MODULE Login SSO · QA ASIGNADO **Mijael Rojas** · Producto: iond · Filas E2E: E2E-KC-AUT-002 · Producción: Sí

| ID | CASO | RESULTADO ESPERADO | OBSERVACION |
|---|---|---|---|
| SMK-01.1 | Abrir la app en una ventana privada del navegador. Datos: Preprod: `https://preprod-app.iond.ai` · Producción: `https://app.iond.ai` | Redirige a Keycloak; la pantalla de login carga con TLS válido | Manual (spec existente rota, Ola 0). Cambio en v0.2.0: Rebranding: dominio, logo y textos de iond (86e21f52d) |
| SMK-01.2 | Ingresar con el usuario de la company de prueba. Datos: Usuario del perfil `.env.preprod` / `.env.prod-testco` (solo el nombre) | Vuelve a la app sin error de callback y muestra el Dashboard | Manual |

### 3. SMK-02 · Dashboard y navegación

PRIORIDAD `urgent` · SIDE TENANT · MODULE Dashboard · QA ASIGNADO **Mijael Rojas** · Producto: iond · Filas E2E: E2E-TEN-DSH-001 · Producción: Sí

| ID | CASO | RESULTADO ESPERADO | OBSERVACION |
|---|---|---|---|
| SMK-02.1 | Revisar el Dashboard | Las tarjetas y el historial reciente cargan sin errores ni paneles de acceso restringido | Automática: TC-DASH-01. Cambio en v0.2.0: Execution History quedó dentro de Dashboard (86e35882c) |
| SMK-02.2 | Abrir uno por uno los accesos del menú lateral (secciones OVERVIEW, AUTOMATE, RESOURCES y MARKETPLACE) | Cada acceso abre su vista sin errores | Manual. Cambio en v0.2.0: Menú reorganizado en cuatro secciones (86e35882c) |
| SMK-02.3 | Abrir el menú de usuario | Muestra el perfil, Billing y el idioma, y se cierra sin errores | Manual. Cambio en v0.2.0: Billing pasó al menú de usuario (86e35882c) |

### 4. SMK-03 · Crear un board

PRIORIDAD `urgent` · SIDE TENANT · MODULE Boards · QA ASIGNADO **Mijael Rojas** · Producto: iond · Filas E2E: E2E-TEN-BRD (New Board, Commit › Save) · Producción: Sí

| ID | CASO | RESULTADO ESPERADO | OBSERVACION |
|---|---|---|---|
| SMK-03.1 | Boards → Create Board con el nombre `autobot-smoke-<AAAAMMDD>`. Datos: autobot-smoke-<AAAAMMDD> | Abre el editor con el board vacío | Manual (propuesta Ola 1). Cambio en v0.2.0: Primera vista de Boards rediseñada; botón Library junto a Create Board (86e223kvf, 86e35882c) |
| SMK-03.2 | Agregar un trigger Webhook y conectarle un nodo Code que devuelva `{ "smoke": true }` (alternativa: HTTP Request a un endpoint estable). Datos: Nodo Code sin dependencias externas | Los dos nodos quedan conectados y sin advertencias de configuración | Manual. Cambio en v0.2.0: Los IDs de nodo se muestran sin "$" (86e2jwrvc) |
| SMK-03.3 | Commit → Save con el mensaje `smoke <AAAAMMDD>` | El commit queda en Commit › History y el board aparece en la lista de Boards | Manual |

### 5. SMK-04 · Ejecutar en test

PRIORIDAD `urgent` · SIDE TENANT · MODULE Boards · QA ASIGNADO **Mijael Rojas** · Producto: iond · Filas E2E: E2E-TEN-BRD-030 (Preview) · Producción: Sí

| ID | CASO | RESULTADO ESPERADO | OBSERVACION |
|---|---|---|---|
| SMK-04.1 | Ejecutar el board en modo de prueba (Preview) con el payload `{ "smoke": true }`. Datos: Payload de ejemplo | La ejecución termina y cada nodo muestra su resultado y su salida | Manual (Ola 1). Cambio en v0.2.0: Play bloqueado mientras corre y estado final registrado (86e2nazxp); progreso en tiempo real por websockets (86e35wv7f) |

### 6. SMK-16 · Flujo de IA desde iond (Flow Pilot)

PRIORIDAD `high` · SIDE TENANT · MODULE Flow Pilot · QA ASIGNADO **Mijael Rojas** · Producto: IonMind · Filas E2E: E2E-TEN-BRD-040 · Producción: Sí (consume créditos de IA de la company de prueba)

| ID | CASO | RESULTADO ESPERADO | OBSERVACION |
|---|---|---|---|
| SMK-16.1 | Abrir Flow Pilot en el board `autobot-smoke-<AAAAMMDD>` y preguntar "¿Qué hace este board?". Datos: Company con créditos de IA | Respuesta no vacía, sin errores de sesión ni de créditos. Se valida la estructura, no el texto | Automática: TC-BOARD-FP-01, TC-BOARD-FP-02. Cambio en v0.2.0: Flow Pilot registra tokens y costo por turno (86e1fawg0) |

### 7. SMK-05 · Ejecutar en producción y limpiar

PRIORIDAD `urgent` · SIDE TENANT · MODULE Boards · Execution History · QA ASIGNADO **Mijael Rojas** · Producto: iond · Filas E2E: E2E-TEN-EXH-001 · E2E-TEN-BRD-046 · Producción: Sí

| ID | CASO | RESULTADO ESPERADO | OBSERVACION |
|---|---|---|---|
| SMK-05.1 | Activar el board (Active) y copiar la URL de su webhook | El board queda en estado Active | Manual (Ola 1) |
| SMK-05.2 | Disparar el webhook con un POST `{ "smoke": true }` (curl o Postman). Datos: URL del webhook del paso anterior | Respuesta HTTP 2xx | Manual |
| SMK-05.3 | Abrir Dashboard › Execution History y el detalle de esa ejecución | La ejecución aparece como Live · Webhook, con detalle por nodo y consumo registrado | Manual. Cambio en v0.2.0: Historial dentro de Dashboard y replay de la ejecución (86e35882c, 86e2ak75f); logs sincronizados a R2 (86e1mdnbq) |
| SMK-05.4 | Pausar el board y eliminarlo junto con su webhook | El board y su webhook ya no figuran en las listas | Manual |

### 8. SMK-06 · Webhooks

PRIORIDAD `high` · SIDE TENANT · MODULE Webhooks · QA ASIGNADO **Steve Nina** · Producto: iond · Filas E2E: E2E-TEN-WHK · Producción: Sí (solo lectura)

| ID | CASO | RESULTADO ESPERADO | OBSERVACION |
|---|---|---|---|
| SMK-06.1 | Abrir Webhooks | La tabla carga con sus columnas y sin errores | Manual (Ola 1) |

### 9. SMK-07 · Connections y App Connectors

PRIORIDAD `high` · SIDE TENANT · MODULE Connections · App Connectors · QA ASIGNADO **Steve Nina** · Producto: iond · Filas E2E: E2E-TEN-CNX · E2E-TEN-APC · Producción: Sí (solo lectura)

| ID | CASO | RESULTADO ESPERADO | OBSERVACION |
|---|---|---|---|
| SMK-07.1 | Abrir Credentials › Connections | El listado de conexiones carga sin errores | Manual (Ola 1). Cambio en v0.2.0: Connections quedó como pestaña de Credentials (86e35882c) |
| SMK-07.2 | Abrir App Connectors | El listado de conectores carga sin errores | Manual. Cambio en v0.2.0: Navegación por pestañas en los conectores creados (86e25dyyz) |

### 10. SMK-08 · Persistent Data

PRIORIDAD `high` · SIDE TENANT · MODULE Persistent Data · QA ASIGNADO **Steve Nina** · Producto: iond · Filas E2E: E2E-TEN-PDS · Producción: Sí (solo lectura)

| ID | CASO | RESULTADO ESPERADO | OBSERVACION |
|---|---|---|---|
| SMK-08.1 | Abrir Persistent Data › Data Store | El listado carga sin errores | Manual (Ola 1) |
| SMK-08.2 | Abrir la pestaña Data Structure | El listado carga sin errores | Manual |

### 11. SMK-09 · PDF Templates

PRIORIDAD `high` · SIDE TENANT · MODULE PDF Templates · QA ASIGNADO **Steve Nina** · Producto: iond · Filas E2E: E2E-TEN-PDF-019 · Producción: Sí (solo lectura)

| ID | CASO | RESULTADO ESPERADO | OBSERVACION |
|---|---|---|---|
| SMK-09.1 | Abrir PDF Templates y la vista previa de `autobot-smoke-template`. Datos: Plantilla precargada `autobot-smoke-template` | Se muestra el Blueprint Preview de la plantilla | Automática: TC-PDF-21 |

### 12. SMK-10 · Credentials

PRIORIDAD `high` · SIDE TENANT · MODULE Credentials · QA ASIGNADO **Steve Nina** · Producto: iond · Filas E2E: E2E-TEN-CRD · Producción: Sí (solo lectura)

| ID | CASO | RESULTADO ESPERADO | OBSERVACION |
|---|---|---|---|
| SMK-10.1 | Abrir Credentials (pestaña AI Keys) | La tabla carga sin errores | Manual (Ola 1). Cambio en v0.2.0: Credentials con pestañas AI Keys y Connections (86e35882c) |

### 13. SMK-11 · Notificaciones

PRIORIDAD `high` · SIDE TENANT · MODULE Notifications · QA ASIGNADO **Steve Nina** · Producto: iond · Filas E2E: E2E-TEN-NTF-001 · Producción: Sí (solo lectura)

| ID | CASO | RESULTADO ESPERADO | OBSERVACION |
|---|---|---|---|
| SMK-11.1 | Abrir la campana de notificaciones | El panel abre con notificaciones o con el estado vacío | Automática: TC-NOTIF-01. Cambio en v0.2.0: Notificaciones por websockets con token Bearer (86e35wv7f) |

### 14. SMK-12 · Suscripción y consumo

PRIORIDAD `high` · SIDE TENANT · MODULE Billing · QA ASIGNADO **Steve Nina** · Producto: iond · Filas E2E: E2E-ADM-CMP (Subscription) · Producción: Sí (solo lectura)

| ID | CASO | RESULTADO ESPERADO | OBSERVACION |
|---|---|---|---|
| SMK-12.1 | Menú de usuario › Billing | Se ven el plan vigente y el consumo; el consumo refleja la ejecución de SMK-05 | Manual (Ola 1). Cambio en v0.2.0: Billing local de solo lectura en el menú de usuario (86e1pzyug, 86e35882c) |

### 15. SMK-13 · Admin: companies

PRIORIDAD `high` · SIDE ADMIN · MODULE Companies · QA ASIGNADO **Steve Nina** · Producto: iond (admin) · Filas E2E: E2E-ADM-CMP-001 · Producción: Sí (solo lectura)

| ID | CASO | RESULTADO ESPERADO | OBSERVACION |
|---|---|---|---|
| SMK-13.1 | Entrar al Admin, abrir Companies y la información de la company de prueba. Datos: Cuenta de administración (solo lectura) | Las secciones se ven y la company figura ACTIVE | Manual (spec existente rota, Ola 0). Cambio en v0.2.0: Buscador de companies por nombre, subdominio o ID (86e2fpp9y). No se inicia sesión de soporte |

### 16. SMK-14 · Admin Gateway: Apps

PRIORIDAD `high` · SIDE ADMIN GATEWAY · MODULE Apps · QA ASIGNADO **Steve Nina** · Producto: Gateway · Filas E2E: E2E-GTW-APP · Producción: Sí (solo lectura)

| ID | CASO | RESULTADO ESPERADO | OBSERVACION |
|---|---|---|---|
| SMK-14.1 | Entrar al Admin Gateway y abrir el listado de Apps. Datos: Cuenta del Admin Gateway (solo lectura) | El listado carga sin errores | Manual (Ola 3) |

### 17. SMK-17 · Flujo representativo de StageMind

PRIORIDAD `normal` · SIDE STAGEMIND · MODULE StageMind · QA ASIGNADO **Steve Nina** · Producto: StageMind · Filas E2E: — · Producción: No aplica

| ID | CASO | RESULTADO ESPERADO | OBSERVACION |
|---|---|---|---|
| SMK-17.1 | — | No aplica: StageMind no está en este release y su flujo está pendiente de definición (AV-12) |  |

## Limpieza (obligatoria en los dos ambientes)

- [ ] Board `autobot-smoke-<AAAAMMDD>` pausado y eliminado, junto con su webhook (SMK-05.4).
- [ ] Ningún dato con prefijo `autobot-smoke-` remanente.
- [ ] Plantilla `autobot-smoke-template` intacta (es precargada: no se borra).
- [ ] En producción: solo se usó la company de prueba; la cuenta de administración, solo en SMK-13 y SMK-14 y en modo lectura; no se inició ninguna sesión de soporte.

## Totales

| Ambiente | ✅ | ❌ | ⏭️ | Automáticos | Core `urgent` (6 SMK) | Hoja → registro |
|---|---|---|---|---|---|---|
| Preprod | | | 1 | /4 | /6 | `smoke-matrix-preprod.csv` → `smoke-preprod.md` → C-25 |
| Producción | | | 1 | /4 | /6 | `smoke-matrix-prod.csv` → `smoke-prod.md` → C-31 |
