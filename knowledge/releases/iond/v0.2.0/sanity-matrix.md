# Sanity — iond v0.2.0 (beta) + IonMind v1.10.2

> **Sanity de la versión** (REL-04 · `Q-48` · fuente canónica §7.7 y §9.4 · Estándar de QA §6.2) · Skill `skills/release/sanity.md` · Comentario **C-26**.
> **Priorizado caso por caso** para entrar en martes–miércoles con 2 QAs. Fuente de los criterios: `_impact/sanity-source.csv` (matrices L3, Gherkin y QA Instructions de cada ticket).
> **Hoja de ejecución:** `sanity-matrix.csv`, ordenada por PRIORIDAD (primero `urgent`, después `high` y al final `normal`), con las columnas ID · PRIORIDAD · SIDE · MODULE · FEATURE · CASO · RESULTADO ESPERADO · QA ASIGNADO · RESOLUCION · OBSERVACION · TICKET · PRIORIDAD BUG. Si un caso falla, se crea el bug y su URL va en **TICKET** y su prioridad en **PRIORIDAD BUG**.
> **Criterio de salida:** 100 % de los casos `urgent` aprobados; los `high` sin fallas `urgent`; los `normal` que no entren en el timebox se marcan ⏭️ y se informan en el Go/No-Go.

## Encabezado

| Campo | Valor |
|---|---|
| Producto / versión | iond v0.2.0 + IonMind v1.10.2 (sistema integrado; IonMind se despliega antes) |
| Ambiente · build | `preprod-app.iond.ai` · commit RC del C-23 |
| Fechas | 2026-10-13 – 2026-10-14 |
| QA | Steve Nina · Mijael Rojas |
| Smoke previo | `smoke-preprod.md` — se ejecuta el lunes 12/10 PM |
| Tarea de Release | Release iond - v0.2.0 — https://app.clickup.com/t/86e39jadr |

## Priorización por caso

Cada caso tiene su propia PRIORIDAD según el riesgo de lo que verifica, no según el ticket al que pertenece. Un ticket importante puede tener casos `normal` (por ejemplo, un texto o un estilo) y un ticket menor puede tener un caso `urgent` (por ejemplo, un registro de compañía o una credencial expuesta).

| PRIORIDAD | Qué entra | Cuándo | Casos | Si no se ejecuta |
|---|---|---|---|---|
| `urgent` | Seguridad y aislamiento entre tenants o compañías · dinero (cobros, cuotas, doble consumo) · integridad de datos (pérdida, duplicados, estados finales) · contratos críticos (API, integraciones legacy, OAuth) · el camino principal de cada feature grande · bugs bloqueantes conocidos | Martes 13/10 | **61** | NO-GO, salvo decisión explícita del PO |
| `high` | Comportamiento funcional importante, manejo de errores, permisos de UI y flujos secundarios de las features | Miércoles 14/10 | **84** | Se informa en el Go/No-Go con su riesgo |
| `normal` | Visual y textos, marca, mediciones documentadas, casos borde de bajo impacto | Miércoles PM, si queda tiempo | **38** | ⏭️ *No ejecutado — fuera de timebox*; lo cubre la regresión o el release siguiente |
| **Total** | | | **183** | 74 son revalidaciones (motivo en OBSERVACION) |

**Alcance por ticket.** Además de la prioridad del caso, cada ticket tiene un alcance: los críticos se prueban **completos**, los demás con una **muestra** de 1–2 criterios y los de menor riesgo **vía regresión** (filas del E2E maestro).

| Alcance | Tickets | Casos |
|---|---|---|
| Completo | 19 principales y sus subtareas | 142 |
| Muestra | 17 principales | 33 |
| Vía regresión | 14 principales | 1 (verificación puntual de 86e22q3pc, que no tiene fila en el maestro) |
| Interacciones entre tickets | — | 7 |

## Columnas de la hoja

| Columna | Contenido |
|---|---|
| ID | `SAN-<ticket>-<criterio>` (las subtareas usan su propio ID de ticket) · `SAN-INT-xx` para las interacciones |
| PRIORIDAD | `urgent` · `high` · `normal`, por caso (tabla anterior) |
| SIDE · MODULE · FEATURE | Dónde se prueba (TENANT, ADMIN, ADMIN GATEWAY, KC, API, IONMIND, WEB o CROSS), el módulo y el ticket (título) |
| CASO | La verificación a ejecutar, con su precondición |
| RESULTADO ESPERADO | Lo que tiene que pasar para aprobar |
| QA ASIGNADO | El QA que dio el veredicto del ticket (los que no tenían veredicto se asignaron para balancear la carga) |
| RESOLUCION | ✅ Aprobado · ❌ Fallido · ⏭️ No ejecutado |
| OBSERVACION | Viene precargada con el motivo cuando el caso es una **revalidación**; el QA agrega sus notas |
| TICKET · PRIORIDAD BUG | Si el caso falla: URL del bug creado y su prioridad (`urgent`, `high`, `normal` o `low`) |

## Orden de ejecución y reparto

| QA ASIGNADO | `urgent` (martes) | `high` (miércoles) | `normal` (si queda tiempo) | Total |
|---|---|---|---|---|
| Steve Nina | 36 | 41 | 12 | 89 |
| Mijael Rojas | 25 | 43 | 26 | 94 |

- **Martes** (después del cierre del smoke a media mañana): todos los casos `urgent`. Un ❌ en un `urgent` se escala ese mismo día (fix-forward o decisión del PO).
- **Miércoles:** los `high` y las interacciones; luego los `normal` hasta el cierre. Decisiones del PO sobre `observaciones-preparacion.md` antes del C-26.
- Si un QA termina su parte, toma casos del otro en el mismo orden de prioridad. Cada ticket lo prueba el QA que dio su veredicto; los `urgent` sin veredicto (websockets y Logo.dev) se asignaron para balancear y el LQA puede reasignar.

## Revalidaciones

Tickets o subtareas cuyo veredicto no cubre lo que entra a la RC. Sus casos llevan el motivo en OBSERVACION; la prioridad de cada caso decide cuándo se ejecuta.

| Ticket | Principal | Motivo | `urgent` | `high` | `normal` |
|---|---|---|---|---|---|
| 86e35wv7f | — | En mock testing al preparar | 3 | 3 | — |
| 86e1y463z | — | Último veredicto RECHAZADO y está en ready to merge | 6 | 1 | — |
| 86e1y46c7 | 86e1y463z | Subtarea sin QA ni CR propio | 2 | — | — |
| 86e22fzw2 | — | Evidencia de QA solo visual | 1 | 1 | 1 |
| 86e2epqqc | 86e22fzw2 | Subtarea sin QA ni CR propio | 1 | — | — |
| 86e21f52d | — | Req 14, redirects 301 y OAuth/CORS sin evidencia de QA | 2 | 3 | — |
| 86e2buw8v | 86e21f52d | Subtarea sin QA propio | 1 | — | — |
| 86e2buw9u | 86e21f52d | Subtarea sin QA propio | 1 | 1 | — |
| 86e2mc23t | — | Cambio del 2026-10-09 sin re-test | 1 | 2 | — |
| 86e1pzyug | — | Aprobación tomada del L3, no confirmada en ClickUp | 4 | 2 | — |
| 86e1pzz9h | 86e1pzyug | Subtarea sin QA propio | 2 | — | — |
| 86e1pzz9j | 86e1pzyug | Subtarea sin desarrollo: confirmar que no queda Stripe | 1 | — | — |
| 86e1fknjv | — | Sin veredicto de QA | 1 | 2 | 2 |
| 86e1qzefc | 86e1fknjv | Sin veredicto de QA | 1 | 1 | — |
| 86e2g4ev0 | — | Guard de duplicados retirado en el CR | 1 | 1 | — |
| 86e1y46d0 | 86e1y463z | Subtarea sin QA ni CR propio | — | 2 | — |
| 86e2buw79 | 86e21f52d | Subtarea sin evidencia de QA (redirects 301) | — | 1 | — |
| 86e2buw9e | 86e21f52d | Subtarea sin QA ni CR propio | — | 1 | 1 |
| 86e2ft73m | 86e2fazfh | Solo code review | — | 1 | — |
| 86e2ft7a8 | 86e2fazfh | Sin PR ni evidencia | — | 2 | — |
| 86e1pzz9e | 86e1pzyug | Subtarea sin QA propio | — | 2 | — |
| 86e1pzz9c | 86e1pzyug | Subtarea sin QA propio | — | 1 | 1 |
| 86e1wfgt2 | 86e1wfgam | Subtarea sin QA propio | — | 1 | — |
| 86e1fkxz7 | 86e1fknjv | Sin veredicto de QA | — | 1 | 1 |
| 86e2p459r | — | REQ 5 diferido; rama marcada como cerrada | — | 1 | 1 |
| 86e2j43eg | — | Conector duplicado en la evidencia | — | 1 | 1 |
| 86e2buw7v | 86e21f52d | Subtarea sin QA propio | — | — | 1 |
| 86e2buw8e | 86e21f52d | Subtarea sin QA propio | — | — | 2 |
| 86e2czvzh | 86e21f52d | Subtarea sin QA ni CR propio | — | — | 1 |
| 86e1wfguh | 86e1wfgam | Subtarea sin QA propio | — | — | 1 |
| 86e1wfgxk | 86e1wfgam | Subtarea sin QA propio | — | — | 1 |
| 86e1fky0g | 86e1fknjv | Sin veredicto de QA | — | — | 1 |

## Resumen por ticket

| Ticket | IONF | FEATURE | MODULE | Alcance | QA ASIGNADO | `urgent` | `high` | `normal` | Revalida | ✅ | ❌ | ⏭️ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [86e35wv7f](https://app.clickup.com/t/86e35wv7f) | IONF-1347 | Soporte de websockets en el frontend | Notifications (websockets) | Completo | Steve Nina | 3 | 3 | — | 6 | | | |
| [86e35882c](https://app.clickup.com/t/86e35882c) | IONF-1344 | IOND — Reorganizar el menú principal y unificar los accesos de Billing según la nueva estructura | Menu | Completo | Mijael Rojas | 1 | 4 | 1 | — | | | |
| [86e1y463z](https://app.clickup.com/t/86e1y463z) | IONF-1088 | Absorción y Unificación de NOVASPHERE en Gateway e Ionflow | Marketplace (App Stores) | Completo | Steve Nina | 8 | 3 | — | 11 | | | |
| [86e1mdnbq](https://app.clickup.com/t/86e1mdnbq) | IONF-1049 | Syncronizacion de logs con R2 | Execution History | Completo | Steve Nina | 5 | 1 | — | — | | | |
| [86e1fawg0](https://app.clickup.com/t/86e1fawg0) | IONF-1020 | Implementar Monitoreo de Uso de Tokens por Usuario en Ion Flow (Flow Pilot) | Flow Pilot | Completo | Mijael Rojas | — | 3 | 2 | — | | | |
| [86e20nmqx](https://app.clickup.com/t/86e20nmqx) | IONF-1098 | Implementar confirmación y cobro para primer escrapeo de plataformas | App Connectors | Completo | Mijael Rojas | 4 | 2 | — | — | | | |
| [86e22fzw2](https://app.clickup.com/t/86e22fzw2) | IONF-1130 | Boards — Animación del nodo Timer persiste al re-ingresar al canvas, inconsistencia visual | Boards | Completo | Mijael Rojas | 2 | 1 | 1 | 4 | | | |
| [86e21f52d](https://app.clickup.com/t/86e21f52d) | IONF-1103 | Rebranding integral de Ionflow a iond | Rebranding | Completo | Mijael Rojas | 4 | 6 | 5 | 15 | | | |
| [86e2mc23t](https://app.clickup.com/t/86e2mc23t) | IONF-1235 | Ocultar menu de categorias y barra de busqueda del webcomponente del marketplace mediante una prop | Customer | Completo | Steve Nina | 1 | 2 | — | 3 | | | |
| [86e2fazfh](https://app.clickup.com/t/86e2fazfh) | IONF-1201 | IonFlow: Rediseñar la vista y mejorar búsqueda, filtros y acciones de endpoints en App Connectors | App Connectors | Completo | Mijael Rojas | 1 | 5 | 2 | 3 | | | |
| [86e2fpp9y](https://app.clickup.com/t/86e2fpp9y) | IONF-1205 | [Ionflow] Permitir acceso administrativo temporal a una compañía sin credenciales del usuario | Companies | Completo | Mijael Rojas | 3 | 2 | 1 | — | | | |
| [86e2nazxp](https://app.clickup.com/t/86e2nazxp) | IONF-1248 | Fix Execution Lifecycle Bugs | Boards | Completo | Steve Nina | 3 | 2 | 1 | — | | | |
| [86e1pzyug](https://app.clickup.com/t/86e1pzyug) | IONF-1056 | IONFLOW - Monetización unificada: Stripe, consumo por segundos, AI credits e IONPDF | Billing | Completo | Steve Nina | 7 | 8 | 2 | 13 | | | |
| [86e1wfgam](https://app.clickup.com/t/86e1wfgam) | IONF-1080 | Motor de exposicion por API (FASE 1) | DevApp API 2.0 | Completo | Mijael Rojas | 3 | 4 | 2 | 3 | | | |
| [86e2mt70g](https://app.clickup.com/t/86e2mt70g) | IONF-1239 | IOND - Selección del service tier de IonMind | App Connectors | Completo | Mijael Rojas | 3 | 3 | — | — | | | |
| [86e31pbz9](https://app.clickup.com/t/86e31pbz9) | IONF-1316 | Acceso directo a compañías sin inicio de sesión como usuario | Companies | Completo | Steve Nina | 2 | 4 | — | — | | | |
| [86e2xnjyz](https://app.clickup.com/t/86e2xnjyz) | IONF-1267 | Optimizar latencia de IONFLOW con conexión SQLite persistente | Boards | Completo | Mijael Rojas | 3 | 2 | 1 | — | | | |
| [86e2ak75f](https://app.clickup.com/t/86e2ak75f) | IONF-1170 | Standardize Execution UI & Build Execution Replay Engine | Execution History | Completo | Steve Nina | 2 | 4 | — | — | | | |
| [86e1fknjv](https://app.clickup.com/t/86e1fknjv) | IONF-1022 | Integrar Logo.dev como fallback en el pipeline de logos de IonMind | App Connectors | Completo | Steve Nina | 2 | 4 | 4 | 10 | | | |
| [86e25dyyz](https://app.clickup.com/t/86e25dyyz) | IONF-1151 | Mejorar UX de navegación y edición en App Connectors creados | App Connectors | Muestra | Mijael Rojas | — | 1 | 1 | — | | | |
| [86e19dtkw](https://app.clickup.com/t/86e19dtkw) | IONF-1007 | Error de sincronización UTC/Local en los disparadores de Company Schedules | Customer | Muestra | Mijael Rojas | — | 1 | 1 | — | | | |
| [86e29hc1r](https://app.clickup.com/t/86e29hc1r) | IONF-1169 | Quitar CORS para rutas publicas de webhooks | Webhooks | Muestra | Mijael Rojas | — | 1 | — | — | | | |
| [86e22fzve](https://app.clickup.com/t/86e22fzve) | IONF-1127 | Boards — Scheduler ejecuta flow correctamente pero status queda en "error" | Execution History | Muestra | Steve Nina | — | 1 | 1 | — | | | |
| [86e22fzq7](https://app.clickup.com/t/86e22fzq7) | IONF-1114 | Connections — Reautorización por API Key crea conexión duplicada en lugar de sobrescribir | Connections | Muestra | Steve Nina | — | 2 | — | — | | | |
| [86e1r2c6z](https://app.clickup.com/t/86e1r2c6z) | IONF-1075 | [Ionflow] Refactorizar flujo y formulario de registro de compañía | Register Company | Muestra | Steve Nina | 1 | — | 1 | — | | | |
| [86e1r4bu7](https://app.clickup.com/t/86e1r4bu7) | IONF-1076 | [Ionflow] Crear boards de ejemplo documentados y publicarlos como templates editables | Templates | Muestra | Steve Nina | 1 | 1 | — | — | | | |
| [86e2jwrvc](https://app.clickup.com/t/86e2jwrvc) | IONF-1223 | Ocultar prefijo "$" del nombre de los nodos | Boards | Muestra | Steve Nina | — | 1 | 1 | — | | | |
| [86e2e8gde](https://app.clickup.com/t/86e2e8gde) | IONF-1193 | Extraer conectores UPS Track Alert y FedEx Supply Chain con IonMind | App Connectors | Muestra | Mijael Rojas | — | — | 2 | — | | | |
| [86e22fzqu](https://app.clickup.com/t/86e22fzqu) | IONF-1119 | PDF Templates — Nodo PDF retorna error 500 genérico cuando la imagen no está en base64 | PDF Templates | Muestra | Steve Nina | — | 2 | — | — | | | |
| [86e1kp55k](https://app.clickup.com/t/86e1kp55k) | IONF-1043 | El botón "Auto-mapper" en el nodo PDF Template no funciona al hacer clic | PDF Templates | Muestra | Mijael Rojas | — | 1 | 1 | — | | | |
| [86e223kvf](https://app.clickup.com/t/86e223kvf) | IONF-1104 | Mejoras estéticas globales en pantallas de iond / Ionflow | Boards | Muestra | Steve Nina | 1 | — | 1 | — | | | |
| [86e2g4ev0](https://app.clickup.com/t/86e2g4ev0) | IONF-1211 | [FIX] Investigar y corregir endpoints duplicados en App Connectors generados por IonMind | App Connectors | Muestra | Mijael Rojas | 1 | 1 | — | 2 | | | |
| [86e2p459r](https://app.clickup.com/t/86e2p459r) | IONF-1249 | [BUG] IOND - Recuperar análisis de IonMind tras expiración de sesión y mostrar fallos terminales | App Connectors | Muestra | Mijael Rojas | — | 1 | 1 | 2 | | | |
| [86e2j43eg](https://app.clickup.com/t/86e2j43eg) | IONF-1218 | IonMind - Extraer APIs de mensajería y generar App Connectors | App Connectors | Muestra | Mijael Rojas | — | 1 | 1 | 2 | | | |
| [86e2t9962](https://app.clickup.com/t/86e2t9962) | IONF-1253 | El estado de minado de un endpoint no se actualiza en tiempo real en App Connector | App Connectors | Muestra | Mijael Rojas | — | 1 | 1 | — | | | |
| [86e25j0rn](https://app.clickup.com/t/86e25j0rn) | IONF-1153 | Enviar errores de IonMind a Ionflow para notificaciones por correo y Mattermost | Notificaciones de IonMind | Muestra | Mijael Rojas | — | 1 | 1 | — | | | |
| [86e22fzut](https://app.clickup.com/t/86e22fzut) | IONF-1126 | PDF Templates — Cambios sin guardar se pierden al presionar Escape o cerrar modal sin confirmación | PDF Templates | Vía regresión | Steve Nina | — | — | — | — | | | |
| [86e22fzq9](https://app.clickup.com/t/86e22fzq9) | IONF-1116 | PDF Templates — Sin límite de tamaño para Load Base PDF, la vista crashea con archivos grandes | PDF Templates | Vía regresión | Steve Nina | — | — | — | — | | | |
| [86e1gr6ug](https://app.clickup.com/t/86e1gr6ug) | IONF-1030 | Mejoras de la interface en ionflow dualtrack | Boards | Vía regresión | Mijael Rojas | — | — | — | — | | | |
| [86e22fzrp](https://app.clickup.com/t/86e22fzrp) | IONF-1121 | Boards — Board sugiere cambios sin guardar tras commit exitoso al re-ingresar a la vista | Boards | Vía regresión | Steve Nina | — | — | — | — | | | |
| [86e22fzvx](https://app.clickup.com/t/86e22fzvx) | IONF-1128 | Boards — Simple Decision compara valores numéricos como strings, resultado incorrecto | Boards | Vía regresión | Steve Nina | — | — | — | — | | | |
| [86e29e6jt](https://app.clickup.com/t/86e29e6jt) | IONF-1168 | Error de visualización (+4 horas) en los logs de ejecución de Company Schedules en UI Gateway | Customer | Vía regresión | Mijael Rojas | — | — | — | — | | | |
| [86e2dpfek](https://app.clickup.com/t/86e2dpfek) | IONF-1191 | Bug en la compilacion de gateway-ion en DEVELOPMENT | Infra | Vía regresión | Steve Nina | — | — | — | — | | | |
| [86dy0bwmf](https://app.clickup.com/t/86dy0bwmf) | IONF-442 | Form Data Builder observations | Boards | Vía regresión | Steve Nina | — | — | — | — | | | |
| [86e22fzw6](https://app.clickup.com/t/86e22fzw6) | IONF-1131 | Boards — Menú de contexto del Iterator muestra la data como collection vacío | Boards | Vía regresión | Mijael Rojas | — | — | — | — | | | |
| [86e22q9h8](https://app.clickup.com/t/86e22q9h8) | IONF-1141 | App Connectors/Boards - No se encuentra la lista de nodos minados previamente | App Connectors | Vía regresión | Mijael Rojas | — | — | — | — | | | |
| [86e04qn0d](https://app.clickup.com/t/86e04qn0d) | IONF-802 | Problemas con la validación al configurar en Admin - Orden de los nodos en Account - Pantalla sin App se visualiza al instalar una App en Account | Customer | Vía regresión | Steve Nina | — | — | — | — | | | |
| [86e22q3pc](https://app.clickup.com/t/86e22q3pc) | IONF-1139 | Accounts - El buscador global no encuentra PDF Templates | Accounts | Vía regresión | Steve Nina | — | — | 1 | — | | | |
| [86e22fzt2](https://app.clickup.com/t/86e22fzt2) | IONF-1122 | Boards — Historial de cambios activa evento de cambios sin guardar al revisar commits con comentarios | Boards | Vía regresión | Steve Nina | — | — | — | — | | | |
| [86e3085ap](https://app.clickup.com/t/86e3085ap) | IONF-1305 | Flow Pilot no responde al enviar un mensaje en Gateway > Board | Flow Pilot | Vía regresión | Mijael Rojas | — | — | — | — | | | |

## Casos `urgent` — martes (61)

Obligatorios para el GO. FEATURE solo se repite en las filas de subtareas. Un criterio sin TC en la matriz L3 se ejecuta como Happy Path y se anota en OBSERVACION como brecha.

### 86e35wv7f · IONF-1347 — Soporte de websockets en el frontend

SIDE TENANT · MODULE Notifications (websockets) · QA ASIGNADO **Steve Nina** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e35wv7f-AC-1 | — | Suscribirse a un canal privado de Reverb con el Bearer ws-token, sin cookies. Precondición: Usuario tenant con token válido | /broadcasting/auth responde 200; llegan los eventos en tiempo real (notificaciones, historial) | | Revalidación: En mock testing al preparar | | |
| SAN-86e35wv7f-AC-3 | — | Usar el ws-token contra una ruta de la API distinta de broadcasting/auth. Precondición: ws_token del storage, llamada directa | 403 reason ws_token_scope; los tokens normales y las cookies siguen funcionando | | Revalidación: En mock testing al preparar | | |
| SAN-86e35wv7f-AC-4 | — | Suscribirse al canal privado de otro usuario o compañía. Precondición: Dos usuarios/compañías | Autorización denegada; no llegan eventos ajenos | | Revalidación: En mock testing al preparar | | |

### 86e35882c · IONF-1344 — IOND — Reorganizar el menú principal y unificar los accesos de Billing según la nueva estructura

SIDE TENANT · MODULE Menu · QA ASIGNADO **Mijael Rojas** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e35882c-AC-4 | — | Credentials con un usuario que tiene AI Keys pero no Connections. Precondición: Rol con AI Keys y sin Connections | Solo ve AI Keys; Connections bloqueada también por URL directa | |  | | |

### 86e1y463z · IONF-1088 — Absorción y Unificación de NOVASPHERE en Gateway e Ionflow

SIDE ADMIN GATEWAY · MODULE Marketplace (App Stores) · QA ASIGNADO **Steve Nina** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e1y463z-AC-1 | — | Compra con checkout embebido Connect y tarjeta de prueba. Precondición: Seller Connect ACTIVE, plan publicado | Direct charge al seller con application fee correcto; marketplace_invoice con app_id, price_id, account_id | | Revalidación: Último veredicto RECHAZADO y está en ready to merge | | |
| SAN-86e1y463z-AC-2 | — | Crear o editar un precio en Plans Studio (write-through a Stripe). Precondición: Plan existente, Connect activo | Precio en BD y en Stripe; el anterior queda SUPERSEDED; si Stripe falla se revierte la BD | | Revalidación: Último veredicto RECHAZADO y está en ready to merge | | |
| SAN-86e1y463z-AC-3 | — | Pago exitoso por webhook Connect y automatización post-pago. Precondición: Eventos Connect, webhook_url configurado | Invoice y subscription creadas; seller notificado vía webhook_url; la GRAPP se instala tras pagar | | Revalidación: Último veredicto RECHAZADO y está en ready to merge | | |
| SAN-86e1y463z-AC-6 | — | API M2M: App A lee o cancela una línea vendida por App B. Precondición: Dos apps, mismo buyer | 404; sin scope 403; sin Account-Id 400; moneda mezclada 422 legible | | Revalidación: Último veredicto RECHAZADO y está en ready to merge | | |
| SAN-86e1y463z-REG-007 | — | Billing de la plataforma (plan IOND de la compañía) tras el marketplace. Precondición: Compañía con suscripción IOND | Plan y suscripción de plataforma sin cambios | | Revalidación: Último veredicto RECHAZADO y está en ready to merge | | |
| SAN-86e1y463z-BUG-12-1 | — | Borrar un tier con ventas (bug bloqueante de la iteración 2). Precondición: Tier con ventas registradas | No da 500; Stripe y BD quedan consistentes | | Revalidación: Bug bloqueante de la iteración 2 | | |
| SAN-86e1y46c7-AC-1 | (subtarea) Implementación y Acople del Motor de Pagos Multicanal | Renovación, fallo y cancelación de una suscripción marketplace por webhooks Connect. Precondición: Suscripción activa en la cuenta conectada | Ledger marketplace_invoices actualizado por evento; entitlement correcto; seller notificado | | Revalidación: Subtarea sin QA ni CR propio | | |
| SAN-86e1y46c7-AC-2 | (subtarea) Implementación y Acople del Motor de Pagos Multicanal | Compra con un seller sin charges_enabled, o compra directa M2M con monto libre. Precondición: Seller RESTRICTED; token DevApp | Rechazo antes de cobrar (422); M2M solo acepta precios de catálogo | | Revalidación: Subtarea sin QA ni CR propio | | |

### 86e1mdnbq · IONF-1049 — Syncronizacion de logs con R2

SIDE TENANT · MODULE Execution History · QA ASIGNADO **Steve Nina** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e1mdnbq-AC-2 | — | El cron de sincronización procesa los jobs pendientes. Precondición: Credenciales R2 válidas | pending → uploading → done; archivo en R2 con remote_key igual a la estructura storage/ | |  | | |
| SAN-86e1mdnbq-AC-3 | — | Limpieza local después de subir. Precondición: Jobs en done | El archivo local se borra solo después de done → cleaned | |  | | |
| SAN-86e1mdnbq-AC-4 | — | R2 no disponible temporalmente. Precondición: Credenciales R2 inválidas | Reintenta hasta 5 veces, luego failed; el archivo local se conserva | |  | | |
| SAN-86e1mdnbq-AC-5 | — | Flujos dev/live y Execution History con el sync activo. Precondición: Flows existentes | Ejecuciones completan sin errores; historial y detalle visibles | |  | | |
| SAN-86e1mdnbq-AC-6 | — | Ejecuciones de dos compañías que se sincronizan. Precondición: Dos companies con flows | Rutas R2 separadas por compañía, sin mezcla | |  | | |

### 86e20nmqx · IONF-1098 — Implementar confirmación y cobro para primer escrapeo de plataformas

SIDE TENANT · MODULE App Connectors · QA ASIGNADO **Mijael Rojas** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e20nmqx-AC-1 | — | Analyze de una URL no cacheada en Create Connector. Precondición: URL nunca analizada | exists=false; modal con costo; no arranca análisis hasta confirmar | |  | | |
| SAN-86e20nmqx-AC-2 | — | Confirmar con Execute en el modal. Precondición: URL no cacheada | Se dispara /analyze; la plataforma queda en caché; cobro solo en la ejecución inicial | |  | | |
| SAN-86e20nmqx-AC-3 | — | Cancelar o cerrar el modal. Precondición: Modal visible | No hay análisis profundo ni cobro | |  | | |
| SAN-86e20nmqx-AC-4 | — | Analyze de una URL ya cacheada. Precondición: URL previamente analizada | exists=true; autocompleta sin modal ni cobro | |  | | |

### 86e22fzw2 · IONF-1130 — Boards — Animación del nodo Timer persiste al re-ingresar al canvas, inconsistencia visual

SIDE TENANT · MODULE Boards · QA ASIGNADO **Mijael Rojas** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e22fzw2-AC-2 | — | Salir del canvas durante la ejecución. Precondición: Timer 60 s en Development | La ejecución sigue en background, completa y queda en Execution History | | Revalidación: Evidencia de QA solo visual | | |
| SAN-86e2epqqc-AC-1 | (subtarea) Al pausar un flow con el nodo timer y luego hacer stop el flow continuasu ejecucion | Pausar el flow durante el Timer y luego pulsar Stop. Precondición: Flow con Timer y nodos posteriores | Se detiene de inmediato, estado Stopped, sin ejecutar nodos posteriores | | Revalidación: Subtarea sin QA ni CR propio | | |

### 86e21f52d · IONF-1103 — Rebranding integral de Ionflow a iond

SIDE TENANT · MODULE Rebranding · QA ASIGNADO **Mijael Rojas** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e21f52d-AC-2 | — | Login Keycloak y flujos core (crear/ejecutar board) tras el rebranding. Precondición: Usuario existente | Sin errores; realm/client y header técnico operativos | | Revalidación: Req 14, redirects 301 y OAuth/CORS sin evidencia de QA | | |
| SAN-86e21f52d-AC-5 | — | OAuth callbacks, CORS y webhooks entrantes de integraciones existentes. Precondición: Conector OAuth y webhook configurados | Sin regresiones con los dominios nuevos; consumidores legacy funcionan | | Revalidación: Req 14, redirects 301 y OAuth/CORS sin evidencia de QA | | |
| SAN-86e2buw8v-AC-1 | (subtarea) Actualizar documentación técnica e integraciones de Ionflow a iond | Integración existente que usa una URL o identificador legacy. Precondición: Integración creada antes del rebranding | Sigue funcionando por alias, redirect o transición documentada | | Revalidación: Subtarea sin QA propio | | |
| SAN-86e2buw9u-AC-1 | (subtarea) Auditar identificadores técnicos y compatibilidad del rebranding a iond | Identificadores conservados (header técnico, clave de idioma en localStorage, bucket de logs, realm). Precondición: Usuario con preferencias previas | Requests con el header aceptadas; idioma guardado se conserva; sync R2 funciona | | Revalidación: Subtarea sin QA propio | | |

### 86e2mc23t · IONF-1235 — Ocultar menu de categorias y barra de busqueda del webcomponente del marketplace mediante una prop

SIDE ADMIN GATEWAY · MODULE Customer · QA ASIGNADO **Steve Nina** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2mc23t-AC-1 | — | Renderizar <gt-service-list> sin atributos en Available Marketplace. Precondición: Admin Gateway > Customer > Available Marketplace | Muestra filtros y búsqueda como antes (retrocompatible) | | Revalidación: Cambio del 2026-10-09 sin re-test | | |

### 86e2fazfh · IONF-1201 — IonFlow: Rediseñar la vista y mejorar búsqueda, filtros y acciones de endpoints en App Connectors

SIDE TENANT · MODULE App Connectors · QA ASIGNADO **Mijael Rojas** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2fazfh-AC-3 | — | Seleccionar en varias páginas, buscar/filtrar/limpiar e importar. Precondición: Conector con endpoints | La selección persiste; Import Selection importa exactamente lo seleccionado | |  | | |

### 86e2fpp9y · IONF-1205 — [Ionflow] Permitir acceso administrativo temporal a una compañía sin credenciales del usuario

SIDE ADMIN · MODULE Companies · QA ASIGNADO **Mijael Rojas** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2fpp9y-AC-1 | — | Usuario tenant intenta abrir Admin > Companies o llamar GET /1.0/companies. Precondición: Usuario con rol tenant autenticado | 403 o redirección; no lista compañías ni usuarios ajenos | |  | | |
| SAN-86e2fpp9y-AC-4 | — | Iniciar soporte sin VPN o en un entorno sin VPN_ALLOWED_CIDRS. Precondición: VPN desconectada o CIDRs vacíos | Se bloquea (fail-closed): overlay "VPN required", 403 vpn_required, no se abre sesión | |  | | |
| SAN-86e2fpp9y-AC-6 | — | Usuario tenant navega por URL directa a rutas exclusivas de admin. Precondición: Usuario tenant autenticado | El guard de rol lo redirige; no ve vistas de admin | |  | | |

### 86e2nazxp · IONF-1248 — Fix Execution Lifecycle Bugs

SIDE TENANT · MODULE Boards · QA ASIGNADO **Steve Nina** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2nazxp-AC-2 | — | Clics rápidos repetidos en Play, o el mismo flow en dos pestañas. Precondición: Board en Company > Boards | Una sola ejecución; sin registros colgados en running/pending; aviso de ejecución en curso | |  | | |
| SAN-86e2nazxp-AC-3 | — | Toda ejecución termina en un estado final. Precondición: Varias ejecuciones Dev y Live | completed, warning o error (stopped al detener o cerrar la pestaña); nunca running/pending indefinido | |  | | |
| SAN-86e2nazxp-AC-4 | — | Ejecutar en Dev y en Live un flow con nodo mal configurado. Precondición: Flow con nodo sin configurar (HTTP o Form) | El historial registra error/warning en ambos modos, nunca completed | |  | | |

### 86e1pzyug · IONF-1056 — IONFLOW - Monetización unificada: Stripe, consumo por segundos, AI credits e IONPDF

SIDE ADMIN · TENANT · MODULE Billing · QA ASIGNADO **Steve Nina** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e1pzyug-AC-B01 | — | Admin asigna otro plan en Companies > Subscription. Precondición: Admin; compañía con plan free | feature_consumptions se resincroniza; subscription_renewals event=admin_assigned; botón deshabilitado durante la operación | | Revalidación: Aprobación tomada del L3, no confirmada en ClickUp | | |
| SAN-86e1pzyug-AC-B07 | — | Ejecutar con execution_time agotado desde editor, live, webhook y scheduler. Precondición: consumed >= available en execution_time | 403 inmediato, estado quota_exhausted, email "contact us"; schedules y webhooks no se borran | | Revalidación: Aprobación tomada del L3, no confirmada en ClickUp | | |
| SAN-86e1pzyug-AC-STREAM | — | Flow largo consume execution_time durante la ejecución. Precondición: CONSUMPTION_FLUSH_SECONDS=5; saldo bajo | consumed crece en cada flush; al agotarse corta con quota_exhausted; sin doble conteo | | Revalidación: Aprobación tomada del L3, no confirmada en ClickUp | | |
| SAN-86e1pzyug-AC-B09/B10 | — | Usar Flow Pilot y endpoints de IonMind con ai_credits agotado. Precondición: ai_credits consumed >= available | SSE "reached your AI credits limit"; IonMind 403 "Feature quota exceeded"; no llama al proveedor | | Revalidación: Aprobación tomada del L3, no confirmada en ClickUp | | |
| SAN-86e1pzz9h-AC-16/18/19 | (subtarea) Implementar ledger de consumo y segundos por ejecución | Evaluar el guard con varias ventanas y límites especiales. Precondición: Filas feature_consumptions preparadas | daily+monthly simultáneas; available=-1 nunca bloquea; available=0 bloquea aunque consumed=0 | | Revalidación: Subtarea sin QA propio | | |
| SAN-86e1pzz9h-AC-IDEM | (subtarea) Implementar ledger de consumo y segundos por ejecución | Reintento o cierre final de una ejecución ya contabilizada. Precondición: Ejecución con flush intermedio | No se duplica el consumo (solo se suma el remanente no persistido) | | Revalidación: Subtarea sin QA propio | | |
| SAN-86e1pzz9j-AC-B15 | (subtarea) Diseñar integración Stripe y facturación de overage | Verificar que no queda integración Stripe en ningún flujo de billing. Precondición: Entorno desplegado | Sin checkout/portal/webhooks ni llamadas al SDK de Stripe; ningún cargo externo | | Revalidación: Subtarea sin desarrollo: confirmar que no queda Stripe | | |

### 86e1wfgam · IONF-1080 — Motor de exposicion por API (FASE 1)

SIDE API · MODULE DevApp API 2.0 · QA ASIGNADO **Mijael Rojas** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e1wfgam-AC-1/2 | — | Emitir token client_credentials en /api/2.0/app. Precondición: Client id/secret de app | 200 con JWT RS256; secret malo 401, scope desconocido 422, grant no soportado 400 | |  | | |
| SAN-86e1wfgam-AC-5/6 | — | Llamar endpoints sin token, con token revocado/expirado o sin scope. Precondición: Token revocado y token read-only | 401 "Invalid token" uniforme; 403 nombrando el scope; sin detalles internos | |  | | |
| SAN-86e1wfgam-AC-4/14/15 | — | Operar accounts con Account-Id desde apps de la misma y de otra compañía. Precondición: 2 apps compañía A, 1 app compañía B | Sin header 400; misma compañía comparte customers; remote_id repetido 409; otra compañía 404 uniforme | |  | | |

### 86e2mt70g · IONF-1239 — IOND - Selección del service tier de IonMind

SIDE TENANT · MODULE App Connectors · QA ASIGNADO **Mijael Rojas** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2mt70g-AC-2 | — | Seleccionar tier y confirmar la extracción. Precondición: URL de documentación nueva | Un solo job; tier enviado a /ionmind/analyze y /extract y persistido en el borrador | |  | | |
| SAN-86e2mt70g-AC-3 | — | Comparar el costo del modal de primera extracción entre los tres tiers. Precondición: URL no cacheada; cada tier configurado | El costo cambia según el tier; nunca un valor fijo | |  | | |
| SAN-86e2mt70g-AC-5 | — | Doble clic en Analyze/Confirm. Precondición: Modal con tier válido | Un solo job y un solo cargo | |  | | |

### 86e31pbz9 · IONF-1316 — Acceso directo a compañías sin inicio de sesión como usuario

SIDE ADMIN · MODULE Companies · QA ASIGNADO **Steve Nina** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e31pbz9-AC-5 | — | Requests tenant del admin con la VPN desconectada. Precondición: Admin; VPN desconectada | 403 vpn_required en PHP y Go; overlay VPN | |  | | |
| SAN-86e31pbz9-AC-6 | — | Usuario no-admin intenta Support/admin o la API de otra compañía. Precondición: Usuario miembro solo de compañía A | Acceso denegado; GET /tenants/{B}/flows da 401; el bypass es solo para admin | |  | | |

### 86e2xnjyz · IONF-1267 — Optimizar latencia de IONFLOW con conexión SQLite persistente

SIDE TENANT · MODULE Boards · QA ASIGNADO **Mijael Rojas** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2xnjyz-AC-2 | — | Terminar el flow por éxito, stop o error. Precondición: Flows con error forzado | Cierra exactamente una vez; FDs vuelven a la línea base; sin conexiones huérfanas | |  | | |
| SAN-86e2xnjyz-AC-3 | — | Disparar 3 o más flows simultáneos. Precondición: Webhook con payloads distintos | Cada uno con su conexión (opens=1); sin contaminación de nodes/outputs/queues; HTTP 200 | |  | | |
| SAN-86e2xnjyz-AC-4 | — | Disparar flows por webhook con payloads de 1 a 5000 órdenes. Precondición: Flow webhook existente | Mismo contrato (HTTP 200, mismo body); esquema SQLite sin cambios | |  | | |

### 86e2ak75f · IONF-1170 — Standardize Execution UI & Build Execution Replay Engine

SIDE TENANT · MODULE Execution History · QA ASIGNADO **Steve Nina** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2ak75f-AC-2 | — | Seleccionar una ejecución terminada en Execution History, la lista de boards o el toggle del editor. Precondición: Ejecución reciente (< 7 días); permiso read-execution | Canvas de solo lectura con nodos verde/rojo/gris; URL compartible | |  | | |
| SAN-86e2ak75f-AC-NEG | — | ?run= con una ejecución de otro board o compañía; usuario sin read-execution. Precondición: Dos boards; usuario sin permiso | 404 con mensaje comprensible; sin permiso no ve el toggle ni la ruta | |  | | |

### 86e1fknjv · IONF-1022 — Integrar Logo.dev como fallback en el pipeline de logos de IonMind

SIDE TENANT · MODULE App Connectors · QA ASIGNADO **Steve Nina** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e1fknjv-AC-5 | — | Consumir un payload con campo source y un payload legado sin source. Precondición: Jobs nuevos y legados | Campos previos (img, url_r2) intactos; Create Connector no falla | | Revalidación: Sin veredicto de QA | | |
| SAN-86e1qzefc-AC-SEC | (subtarea) Actualización del Backend de IonFlow | Llamar al proxy force-update con un jobId de otro tenant. Precondición: Dos tenants con jobs propios | 403/404: no se actualiza el logo de otro tenant (verificación de pertenencia del jobId) | | Revalidación: Sin veredicto de QA | | |

### 86e1r2c6z · IONF-1075 — [Ionflow] Refactorizar flujo y formulario de registro de compañía

SIDE KC · MODULE Register Company · QA ASIGNADO **Steve Nina** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e1r2c6z-AC-1 | — | Registrar una compañía desde /create-company. Precondición: Usuario nuevo de Keycloak sin compañía | Toast de éxito; Dashboard; el usuario es owner con Settings, Accounts y Teams | |  | | |

### 86e1r4bu7 · IONF-1076 — [Ionflow] Crear boards de ejemplo documentados y publicarlos como templates editables

SIDE TENANT · MODULE Templates · QA ASIGNADO **Steve Nina** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e1r4bu7-AC-10 | — | Instalar un template con 2 o más apps globales. Precondición: Template con Gmail y Shopify | El wizard pide conexión propia por app; sin credenciales del original | |  | | |

### 86e223kvf · IONF-1104 — Mejoras estéticas globales en pantallas de iond / Ionflow

SIDE TENANT · MODULE Boards · QA ASIGNADO **Steve Nina** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e223kvf-AC-5 | — | Renombrar, cambiar estado o clonar un board desde la primera vista. Precondición: Board con nodos y posiciones guardadas | No sobrescribe nodos ni posiciones; editor sin cambios | |  | | |

### 86e2g4ev0 · IONF-1211 — [FIX] Investigar y corregir endpoints duplicados en App Connectors generados por IonMind

SIDE TENANT · MODULE App Connectors · QA ASIGNADO **Mijael Rojas** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2g4ev0-AC-2 | — | Reprocesar o reimportar el mismo artefacto o endpoint de IonMind. Precondición: Conector con endpoints importados (USPS, Locus) | No crea un endpoint adicional; los importados quedan Complete y deshabilitados | | Revalidación: Guard de duplicados retirado en el CR | | |

## Casos `high` — miércoles (84)

Un ❌ en un caso `high` se trata igual que cualquier hallazgo: severidad y decisión de la fuente canónica §7.5.

### 86e35wv7f · IONF-1347 — Soporte de websockets en el frontend

SIDE TENANT · MODULE Notifications (websockets) · QA ASIGNADO **Steve Nina** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e35wv7f-AC-2 | — | Mint del token WS: POST /api/1.0/ws-token con cookie Keycloak. Precondición: Sesión Keycloak activa | Token con scope user:broadcast (TTL ≤ 1 día); sin sesión o con Bearer → rechazo | | Revalidación: En mock testing al preparar | | |
| SAN-86e35wv7f-AC-5 | — | Token inválido o expirado al autorizar un canal. Precondición: Forzar expiración o borrar ws_token | 401 → renueva y reintenta una vez; 403 sin reintento; la UI sigue operativa | | Revalidación: En mock testing al preparar | | |
| SAN-86e35wv7f-AC-6 | — | Logout directo y logout por Keycloak con socket activo. Precondición: Usuario con socket activo | Socket desconectado, canales liberados, ws_token borrado; al volver a loguear se reconecta | | Revalidación: En mock testing al preparar | | |

### 86e35882c · IONF-1344 — IOND — Reorganizar el menú principal y unificar los accesos de Billing según la nueva estructura

SIDE TENANT · MODULE Menu · QA ASIGNADO **Mijael Rojas** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e35882c-AC-1 | — | Sidebar con OVERVIEW, AUTOMATE, RESOURCES y MARKETPLACE en orden, sin Templates. Precondición: Usuario con todos los permisos | Elementos según la tabla del requerimiento en cada sección | |  | | |
| SAN-86e35882c-AC-2 | — | Execution History conserva listado, filtros y acceso a resultados/errores. Precondición: Board con ejecuciones previas | Historial y detalle cargan; filtros funcionan (dentro de Dashboard) | |  | | |
| SAN-86e35882c-AC-5 | — | Abrir Billing en el menú de usuario y Accounting en Marketplace. Precondición: Compañía con plan IOND y clientes | Billing: plan, suscripción y consumo IOND; Accounting: suscripciones/facturas de clientes | |  | | |
| SAN-86e35882c-AC-6 | — | Abrir por URL directa las rutas nuevas y las retiradas, con y sin permisos. Precondición: Usuarios con y sin permisos | Rutas nuevas cargan; retiradas dan 404 (desvío aceptado o no por el PO); sin permiso se bloquea | |  | | |

### 86e1y463z · IONF-1088 — Absorción y Unificación de NOVASPHERE en Gateway e Ionflow

SIDE ADMIN GATEWAY · MODULE Marketplace (App Stores) · QA ASIGNADO **Steve Nina** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e1y463z-AC-4 | — | Usuario sin permiso o de solo lectura en Stores/Pricing/Plans Studio. Precondición: Rol de solo lectura | Acciones bloqueadas con tooltip; sin modal de edición ni requests 403 | | Revalidación: Último veredicto RECHAZADO y está en ready to merge | | |
| SAN-86e1y46d0-AC-1 | (subtarea) Actualización de Frontend y Web Components en Gateway | El seller crea Store → Pricing → Plan → Precio en Plans Studio y guarda. Precondición: Company con permisos de marketplace | Los cambios persisten tras refrescar y quedan disponibles para compra | | Revalidación: Subtarea sin QA ni CR propio | | |
| SAN-86e1y46d0-AC-2 | (subtarea) Actualización de Frontend y Web Components en Gateway | <gt-pricing-table> en modo público y autenticado. Precondición: Embed con public-key / intent JWT | Público: CTA al return_url; autenticado: Embedded Checkout emite purchase-completed | | Revalidación: Subtarea sin QA ni CR propio | | |

### 86e1mdnbq · IONF-1049 — Syncronizacion de logs con R2

SIDE TENANT · MODULE Execution History · QA ASIGNADO **Steve Nina** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e1mdnbq-AC-1 | — | Ejecución dev o live finalizada, y nodo Request con binario. Precondición: STORAGE_SYNC_ENABLED=true | storage_sync_jobs en pending (dev/live/file), creado solo tras cerrar el SQLite | |  | | |

### 86e1fawg0 · IONF-1020 — Implementar Monitoreo de Uso de Tokens por Usuario en Ion Flow (Flow Pilot)

SIDE TENANT · MODULE Flow Pilot · QA ASIGNADO **Mijael Rojas** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e1fawg0-REQ-R2 | — | Flow Pilot captura tokens prompt/completion por turno. Precondición: Modelo configurado en Flow Pilot | usage_metadata del turno con prompt, completion, total_tokens y cost | |  | | |
| SAN-86e1fawg0-REQ-R3 | — | Acumulado por sesión en Postgres. Precondición: Varias preguntas en la misma sesión | Suma incremental exacta; total_cost ≤ 4 decimales; ligado a sesión/usuario/company | |  | | |
| SAN-86e1fawg0-AC-3 | — | Respuesta del chat de Flow Pilot con el registro de tokens activo. Precondición: Sesión de Flow Pilot | Sin demora perceptible; llega el evento Done | |  | | |

### 86e20nmqx · IONF-1098 — Implementar confirmación y cobro para primer escrapeo de plataformas

SIDE TENANT · MODULE App Connectors · QA ASIGNADO **Mijael Rojas** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e20nmqx-AC-5 | — | Dos usuarios piden la misma URL no cacheada a la vez. Precondición: Dos compañías, misma URL nueva | Un solo scraping y un solo cobro | |  | | |
| SAN-86e20nmqx-AC-6 | — | Llamar /analyze directo (sin el modal) con una URL ya cacheada. Precondición: URL cacheada; llamada directa a la API | No cobra ni vuelve a escrapear | |  | | |

### 86e22fzw2 · IONF-1130 — Boards — Animación del nodo Timer persiste al re-ingresar al canvas, inconsistencia visual

SIDE TENANT · MODULE Boards · QA ASIGNADO **Mijael Rojas** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e22fzw2-AC-3 | — | Pulsar Stop después de que el flow terminó. Precondición: Flow finalizado | El estado se mantiene completed | | Revalidación: Evidencia de QA solo visual | | |

### 86e21f52d · IONF-1103 — Rebranding integral de Ionflow a iond

SIDE TENANT · MODULE Rebranding · QA ASIGNADO **Mijael Rojas** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e21f52d-AC-1 | — | Recorrer la app (login, sidebar, títulos, favicon, i18n EN/ES). Precondición: Usuario tenant, ambos idiomas | Marca visible iond; Boards/Nodes/Grapps sin renombrar | | Revalidación: Req 14, redirects 301 y OAuth/CORS sin evidencia de QA | | |
| SAN-86e21f52d-AC-3 | — | Abrir landing.iond.ai y docs.iond.ai, y una URL legacy de alpha.ionflow.io | TLS válido y marca iond; la legacy redirige 301 preservando path y query | | Revalidación: Req 14, redirects 301 y OAuth/CORS sin evidencia de QA | | |
| SAN-86e21f52d-AC-4 | — | Emails transaccionales (invitación, conexiones inactivas, consumo). Precondición: SMTP configurado, buzón de prueba | Marca y logo iond; soporte hello@iond.ai; CTAs al host vigente | | Revalidación: Req 14, redirects 301 y OAuth/CORS sin evidencia de QA | | |
| SAN-86e2buw79-AC-1 | (subtarea) Migrar landing de alpha.ionflow.io a dominio iond.ai | Abrir alpha.ionflow.io/<ruta>?<query> | 301 a landing.iond.ai equivalente, sin loops ni pérdida de parámetros; TLS válido | | Revalidación: Subtarea sin evidencia de QA (redirects 301) | | |
| SAN-86e2buw9e-AC-1 | (subtarea) Actualizar comunicaciones, emails y soporte de Ionflow a iond | Invitar a un miembro y usar el CTA del email. Precondición: Rol admin, email de prueba | La URL resuelve en el host vigente, completa Keycloak y asocia a la compañía | | Revalidación: Subtarea sin QA ni CR propio | | |
| SAN-86e2buw9u-AC-2 | (subtarea) Auditar identificadores técnicos y compatibilidad del rebranding a iond | Middleware con el alias verify.ionflow. Precondición: Integración con el alias legacy | Las requests con el alias legacy siguen aceptadas | | Revalidación: Subtarea sin QA propio | | |

### 86e2mc23t · IONF-1235 — Ocultar menu de categorias y barra de busqueda del webcomponente del marketplace mediante una prop

SIDE ADMIN GATEWAY · MODULE Customer · QA ASIGNADO **Steve Nina** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2mc23t-AC-2 | — | Usar los atributos hide-filters y/o hide-search. Precondición: Página con el embed | Cada atributo oculta solo su elemento; espaciado correcto | | Revalidación: Cambio del 2026-10-09 sin re-test | | |
| SAN-86e2mc23t-AC-3 | — | Elegir una app del marketplace después del cambio. Precondición: Customer con apps disponibles | Abre el flujo de instalación/configuración sin errores | | Revalidación: Cambio del 2026-10-09 sin re-test | | |

### 86e2fazfh · IONF-1201 — IonFlow: Rediseñar la vista y mejorar búsqueda, filtros y acciones de endpoints en App Connectors

SIDE TENANT · MODULE App Connectors · QA ASIGNADO **Mijael Rojas** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2fazfh-AC-1 | — | Paso Import Nodes después de analizar la URL. Precondición: Conector con documentación analizada | Columnas Selección/Método/Ruta/Descripción/Estado/Acciones; acciones URL fuente y ver nodo | |  | | |
| SAN-86e2fazfh-AC-4 | — | Intentar seleccionar más de 5 endpoints para minar. Precondición: Conector con más de 5 endpoints | Selección bloqueada con aviso "maximum of 5 nodes" | |  | | |
| SAN-86e2ft73m-AC-1 | (subtarea) IonMind: Extraer y persistir descripciones para cada endpoint durante Discovery | Discovery sobre documentación con varios endpoints. Precondición: URL nueva | Cada endpoint trae method, path, description (inglés) y source_url, sin inventar | | Revalidación: Solo code review | | |
| SAN-86e2ft7a8-AC-1 | (subtarea) IonFlow: Propagar y persistir descripciones de endpoints para App Connectors | Guardar un App Connector con descriptions y volver a abrirlo. Precondición: Conector creado vía IonMind | Devuelve las mismas descripciones, identidad y selección | | Revalidación: Sin PR ni evidencia | | |
| SAN-86e2ft7a8-AC-2 | (subtarea) IonFlow: Propagar y persistir descripciones de endpoints para App Connectors | Procesar o editar un conector con payload legacy sin description. Precondición: Conector antiguo | Sin errores; description null o ausente | | Revalidación: Sin PR ni evidencia | | |

### 86e2fpp9y · IONF-1205 — [Ionflow] Permitir acceso administrativo temporal a una compañía sin credenciales del usuario

SIDE ADMIN · MODULE Companies · QA ASIGNADO **Mijael Rojas** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2fpp9y-AC-3 | — | Salir de la sesión de soporte con "Leave company" o "Cerrar sesión" dentro del soporte. Precondición: Sesión de soporte activa | Vuelve a Admin > Companies sin pasar por SSO; la sesión admin original sigue intacta | |  | | |
| SAN-86e2fpp9y-AC-5 | — | Cerrar la sesión de soporte en una pestaña teniendo otra abierta. Precondición: Dos pestañas con sesión de soporte | La otra pestaña deja de navegar vistas tenant y muestra aviso | |  | | |

### 86e2nazxp · IONF-1248 — Fix Execution Lifecycle Bugs

SIDE TENANT · MODULE Boards · QA ASIGNADO **Steve Nina** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2nazxp-AC-1 | — | Clic en Play de un nodo del canvas. Precondición: Board con 2 o más nodos | Play se deshabilita al instante con spinner; los Play de los demás nodos quedan bloqueados | |  | | |
| SAN-86e2nazxp-AC-6 | — | Detener el flow o refrescar la pestaña durante una ejecución Dev. Precondición: Flow Dev de larga duración | Queda en estado stopped con la causa registrada; no sigue corriendo en segundo plano | |  | | |

### 86e1pzyug · IONF-1056 — IONFLOW - Monetización unificada: Stripe, consumo por segundos, AI credits e IONPDF

SIDE ADMIN · TENANT · MODULE Billing · QA ASIGNADO **Steve Nina** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e1pzyug-AC-PDF | — | 8 flows con nodo PDF disparados en concurrencia por scheduler. Precondición: Cuota pdf_impressions baja (p. ej. 10) | Nunca se supera la cuota diaria de pdf_impressions (consumed ≤ available) | | Revalidación: Aprobación tomada del L3, no confirmada en ClickUp | | |
| SAN-86e1pzyug-AC-20/21 | — | Registrar consumo con reset_at vencido (reset perezoso). Precondición: Ventana con reset_at pasado y consumed > 0 | consumed arranca en la cantidad nueva; reset_at avanza desde el ancla anterior | | Revalidación: Aprobación tomada del L3, no confirmada en ClickUp | | |
| SAN-86e1pzz9g-AC-51/52 | (subtarea) Definir oferta standalone de IONPDF, add-on para IONFLOW y metering específico | Admin asigna plan IONPDF standalone a una compañía sin IONFLOW. Precondición: Compañía sin plan IONFLOW | Se provisionan pdf_templates/pdf_impressions y un execution_time menor que el de IONFLOW | |  | | |
| SAN-86e1pzz9g-AC-54 | (subtarea) Definir oferta standalone de IONPDF, add-on para IONFLOW y metering específico | Generar un documento desde un template IONPDF. Precondición: Plan con IONPDF y cuota disponible | Consumo registrado en feature_consumption_logs (ledger unificado) | |  | | |
| SAN-86e1pzz9f-AC-B11/B12 | (subtarea) Definir catálogo comercial y planes unificados | Tenant abre /billing/plans y /billing/subscription. Precondición: Usuario con permiso read-billing | Solo lectura: precios locales y barras de uso; sin Buy/Upgrade/Cancel/Overage | |  | | |
| SAN-86e1pzz9e-AC-33/35/38 | (subtarea) Definir enforcement, warnings y estado combinado | Consumir hasta 80 %, 100 % y bloqueo de execution_time. Precondición: Ventana mensual; inbox del contacto | Un email por umbral y ciclo con "contact us", sin mencionar overage; sin duplicados en concurrencia | | Revalidación: Subtarea sin QA propio | | |
| SAN-86e1pzz9e-AC-17 | (subtarea) Definir enforcement, warnings y estado combinado | Agotar la ventana diaria de pdf_impressions con saldo mensual disponible. Precondición: Ventanas daily y monthly configuradas | El nodo PDF se bloquea (blocked=true en la fila daily) | | Revalidación: Subtarea sin QA propio | | |
| SAN-86e1pzz9c-AC-56/57 | (subtarea) Incorporar historial de runtime y estimación de duración | Ejecutar un flow con nodo Timer o subflujo waitForResponse. Precondición: Flow con Timer de 3 s | Guarda active_seconds, idle_seconds ≥ espera y units_consumed; columna Execution Time visible | | Revalidación: Subtarea sin QA propio | | |

### 86e1wfgam · IONF-1080 — Motor de exposicion por API (FASE 1)

SIDE API · MODULE DevApp API 2.0 · QA ASIGNADO **Mijael Rojas** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e1wfgam-AC-9/10 | — | Ejecutar una action del connector con 0, 1 o varias conexiones. Precondición: Customer con conexiones Shipedge | 1 conexión implícita; varias sin Connection-Id 409 con candidatas; respuesta raw del proveedor | |  | | |
| SAN-86e1wfgam-AC-11/12 | — | Pedir el spec y ejecutar el render de un PDF template vía API. Precondición: Seeder DevAppPdfTemplateSeeder | 200 con {filename, public_url} y PDF válido en R2; plantilla ajena 404; sin schema_id 400 | |  | | |
| SAN-86e1wfgam-AC-18/19 | — | Listar y ejecutar flows de la app; regresión del board. Precondición: Flows ACTIVE e INACTIVE | Flow activo ejecuta; INACTIVE 409 "flow is not active"; los flows del board se comportan igual | |  | | |
| SAN-86e1wfgt2-AC-7/8 | (subtarea) app channels | Consultar el catálogo y el detalle del connector namespaced. Precondición: App con connector Shipedge vinculado | app.shipedge = shipedge; tenant.shipedge 404; no vinculado 404; token read-only ejecutando 403 | | Revalidación: Subtarea sin QA propio | | |

### 86e2mt70g · IONF-1239 — IOND - Selección del service tier de IonMind

SIDE TENANT · MODULE App Connectors · QA ASIGNADO **Mijael Rojas** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2mt70g-AC-1 | — | Abrir el modal "Select AI Model" en Create Connector. Precondición: Cache miss; GET /ionmind/tiers disponible | Básico/Estándar/Premium, Estándar por defecto; tiers sin modelo deshabilitados | |  | | |
| SAN-86e2mt70g-AC-4 | — | Usar un App Connector ya existente en caché. Precondición: Conector previamente extraído | Se reutiliza; sin nueva extracción ni cargo de primera extracción | |  | | |
| SAN-86e2mt70g-AC-6 | — | Cancelar, o backend responde 422 (tier sin modelo, inválido o ausente). Precondición: Tier premium sin modelo en BD | Sin job parcial ni cargo; error claro; la selección se conserva | |  | | |

### 86e31pbz9 · IONF-1316 — Acceso directo a compañías sin inicio de sesión como usuario

SIDE ADMIN · MODULE Companies · QA ASIGNADO **Steve Nina** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e31pbz9-AC-1 | — | Admin en VPN: Companies > [Company] > Support > "Start a support session". Precondición: Admin conectado a VPN | Redirige al dashboard tenant de esa compañía sin elegir usuario | |  | | |
| SAN-86e31pbz9-AC-2 | — | Operar durante la sesión de soporte. Precondición: Sesión de soporte activa | Banner "Support session" + compañía + "Leave company"; ve boards, conexiones y data stores | |  | | |
| SAN-86e31pbz9-AC-3 | — | Leave company desde el banner o el menú de usuario. Precondición: Sesión de soporte activa | Vuelve al panel admin; el banner desaparece; sin volver a iniciar sesión | |  | | |
| SAN-86e31pbz9-AC-4 | — | Navegar a /admin/* durante la sesión de soporte. Precondición: Sesión de soporte activa | Redirige al dashboard tenant; las rutas admin quedan inaccesibles | |  | | |

### 86e2xnjyz · IONF-1267 — Optimizar latencia de IONFLOW con conexión SQLite persistente

SIDE TENANT · MODULE Boards · QA ASIGNADO **Mijael Rojas** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2xnjyz-AC-1 | — | Ejecutar cualquier flow. Precondición: Acceso a los logs del pod | El log muestra "[FlowDB] close flow=<id> opens=1 hits=N": una sola conexión por ejecución | |  | | |
| SAN-86e2xnjyz-AC-6 | — | Descargar la execution DB de un flow Dev. Precondición: Ejecución Dev finalizada | Archivo completo y legible | |  | | |

### 86e2ak75f · IONF-1170 — Standardize Execution UI & Build Execution Replay Engine

SIDE TENANT · MODULE Execution History · QA ASIGNADO **Steve Nina** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2ak75f-AC-2-IO | — | Hacer clic en un nodo del replay. Precondición: Ejecución con nodos exitosos y fallidos | El panel muestra el Input y Output JSON exactos y los logs del nodo | |  | | |
| SAN-86e2ak75f-AC-9 | — | Ejecutar el board, modificarlo y abrir el replay anterior. Precondición: Board editado después de ejecutar | Muestra el board tal como se ejecutó, no la versión actual | |  | | |
| SAN-86e2ak75f-AC-3/4 | — | Abrir por URL una ejecución expirada (> 7 días), sin snapshot o en curso. Precondición: Ejecuciones antiguas, legacy y running | Cabecera con estado/duración/origen y aviso expired/missing/running; nunca un 500 | |  | | |
| SAN-86e2ak75f-AC-8 | — | Ejecutar desde el editor, por webhook, por schedule y por subflujo. Precondición: Migración mode/trigger_type aplicada | Dev·Manual, Live·Webhook, Live·Schedule; subflujo según la decisión vigente del PO (OBS-01) | |  | | |

### 86e1fknjv · IONF-1022 — Integrar Logo.dev como fallback en el pipeline de logos de IonMind

SIDE TENANT · MODULE App Connectors · QA ASIGNADO **Steve Nina** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e1fknjv-AC-1 | — | Crawler sin logo válido con LOGO_DEV_ENABLED=true. Precondición: Dominio sin logo crawleable | Obtiene el logo de Logo.dev, lo sube a R2 y source="logo.dev" | | Revalidación: Sin veredicto de QA | | |
| SAN-86e1fknjv-AC-4 | — | Usar el botón "Get logo from Logo.dev" y confirmar el modal. Precondición: Conector con logo de otro origen | Reemplaza el logo en R2; source=logo.dev; toast "Logo updated via Logo.dev" | | Revalidación: Sin veredicto de QA | | |
| SAN-86e1fkxz7-AC-1 | (subtarea) Backend - Integrar Logo.dev y API de actualización en IonMind | POST /api/v1/logo/force-update/{job_id} en IonMind. Precondición: job_id finalizado; dominio existe en Logo.dev | 200 con url_r2 nueva; logos actualizado con source logo.dev | | Revalidación: Sin veredicto de QA | | |
| SAN-86e1qzefc-AC-1 | (subtarea) Actualización del Backend de IonFlow | Proxy POST /api/1.0/tenants/{t}/ionmind/analyze/{jobId}/logo/force-update. Precondición: IonMind arriba y abajo | Éxito 200; dominio inexistente: 400 con el mensaje de IonMind; caída: 502 | | Revalidación: Sin veredicto de QA | | |

### 86e25dyyz · IONF-1151 — Mejorar UX de navegación y edición en App Connectors creados

SIDE TENANT · MODULE App Connectors · QA ASIGNADO **Mijael Rojas** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e25dyyz-AC-9 | — | Navegar entre secciones y guardar metadata (label, descripción, versión, logo). Precondición: Conector publicado; editar Details y guardar | Nodos, webhooks, conexiones y auth intactos; sigue Published, sin volver a draft | |  | | |

### 86e19dtkw · IONF-1007 — Error de sincronización UTC/Local en los disparadores de Company Schedules

SIDE ADMIN GATEWAY · MODULE Customer · QA ASIGNADO **Mijael Rojas** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e19dtkw-AC-1 | — | Schedule mensual de un Grapp con el timezone de la company/account. Precondición: Company con timezone America/La_Paz; schedule mensual | Ejecuta a la hora local configurada, sin desfase de +4 h | |  | | |

### 86e29hc1r · IONF-1169 — Quitar CORS para rutas publicas de webhooks

SIDE TENANT · MODULE Webhooks · QA ASIGNADO **Mijael Rojas** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e29hc1r-AC-1 | — | Request desde un origen externo a un Custom Webhook público. Precondición: Custom Webhook activo; dominio externo | Sin error CORS; el flow se dispara | |  | | |

### 86e22fzve · IONF-1127 — Boards — Scheduler ejecuta flow correctamente pero status queda en "error"

SIDE TENANT · MODULE Execution History · QA ASIGNADO **Steve Nina** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e22fzve-AC-1 | — | Ejecución exitosa disparada por el Scheduler (flows de company y de account). Precondición: Board con Scheduler cada 1 min | Execution History registra completed, no error; sin error al cliente | |  | | |

### 86e22fzq7 · IONF-1114 — Connections — Reautorización por API Key crea conexión duplicada en lugar de sobrescribir

SIDE TENANT · MODULE Connections · QA ASIGNADO **Steve Nina** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e22fzq7-AC-1 | — | Reautorizar una conexión (API Key u OAuth). Precondición: Conexión API Key activa de una app global | Actualiza la conexión existente; mismo número de conexiones; un solo toast | |  | | |
| SAN-86e22fzq7-AC-3 | — | Ejecutar los flows que usan la conexión reautorizada. Precondición: Flow activo que referencia la conexión | El nodo de app ejecuta sin error de autenticación | |  | | |

### 86e1r4bu7 · IONF-1076 — [Ionflow] Crear boards de ejemplo documentados y publicarlos como templates editables

SIDE TENANT · MODULE Templates · QA ASIGNADO **Steve Nina** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e1r4bu7-AC-4 | — | Instalar un template. Precondición: Template activo con PDFs y apps globales | Board editable en la company; PDFs clonados con IDs remapeados; template original intacto | |  | | |

### 86e2jwrvc · IONF-1223 — Ocultar prefijo "$" del nombre de los nodos

SIDE TENANT · MODULE Boards · QA ASIGNADO **Steve Nina** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2jwrvc-AC-2 | — | Mapper, IA, merge de import y ejecución. Precondición: Board con nodos conectados | Se conserva "$N" interno; mapper inserta "$1.output.campo"; ejecución correcta | |  | | |

### 86e22fzqu · IONF-1119 — PDF Templates — Nodo PDF retorna error 500 genérico cuando la imagen no está en base64

SIDE TENANT · MODULE PDF Templates · QA ASIGNADO **Steve Nina** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e22fzqu-AC-4 | — | Inputs de imagen del nodo PDF Template. Precondición: Template con elemento imagen | PNG URL, JPEG data URI y base64 OK; GIF/WebP/SVG o URL inaccesible fallan con mensaje, nunca HTTP 500 | |  | | |
| SAN-86e22fzqu-AC-1 | — | PDF con texto árabe (solo, mixto, dígitos, tablas, bold). Precondición: Template con campos árabes (caso de la subtarea 86e1xu7xp) | Árabe RTL legible y dígitos en orden; templates latinos sin cambios | |  | | |

### 86e1kp55k · IONF-1043 — El botón "Auto-mapper" en el nodo PDF Template no funciona al hacer clic

SIDE TENANT · MODULE PDF Templates · QA ASIGNADO **Mijael Rojas** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e1kp55k-AC-2 | — | Nodo PDF Template tras una rama Gateway. Precondición: Flow Gateway → PDF Template | El formulario carga de inmediato; la ejecución genera el PDF | |  | | |

### 86e2g4ev0 · IONF-1211 — [FIX] Investigar y corregir endpoints duplicados en App Connectors generados por IonMind

SIDE TENANT · MODULE App Connectors · QA ASIGNADO **Mijael Rojas** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2g4ev0-AC-4 | — | Operaciones con la misma ruta y distinto método, versión o tipo. Precondición: Conector con la misma ruta y distinto método | Siguen separadas; cada una aparece una sola vez en FlowToolBar | | Revalidación: Guard de duplicados retirado en el CR | | |

### 86e2p459r · IONF-1249 — [BUG] IOND - Recuperar análisis de IonMind tras expiración de sesión y mostrar fallos terminales

SIDE TENANT · MODULE App Connectors · QA ASIGNADO **Mijael Rojas** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2p459r-AC-3 | — | IonMind responde 200 con data.status=failed. Precondición: URL de documentación inválida | Spinner detenido, toast de error; sin loop ni importación | | Revalidación: REQ 5 diferido; rama marcada como cerrada | | |

### 86e2j43eg · IONF-1218 — IonMind - Extraer APIs de mensajería y generar App Connectors

SIDE IONMIND · MODULE App Connectors · QA ASIGNADO **Mijael Rojas** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2j43eg-AC-1 | — | Conectores de Telegram, WhatsApp, Instagram y Messenger. Precondición: Fuentes oficiales | Cuatro conectores independientes, sin duplicados, con source_url oficial | | Revalidación: Conector duplicado en la evidencia | | |

### 86e2t9962 · IONF-1253 — El estado de minado de un endpoint no se actualiza en tiempo real en App Connector

SIDE TENANT · MODULE App Connectors · QA ASIGNADO **Mijael Rojas** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2t9962-AC-1 | — | Minado de un endpoint en Create Connector > Import Nodes. Precondición: Webhooks/websocket activos | Pasa de Mining a Complete/Error sin recargar | |  | | |

### 86e25j0rn · IONF-1153 — Enviar errores de IonMind a Ionflow para notificaciones por correo y Mattermost

SIDE IONMIND · MODULE Notificaciones de IonMind · QA ASIGNADO **Mijael Rojas** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e25j0rn-AC-1 | — | Fallo terminal de Discovery. Precondición: URL inaccesible; 2 o más intentos fallidos | ionmind.discovery.failed al Gateway tras persistir; email y Mattermost sin secretos | |  | | |

### Interacciones entre tickets

| ID | MODULE | FEATURE | CASO | RESULTADO ESPERADO | QA ASIGNADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|---|---|
| SAN-INT-01 | App Stores · Billing · Menu | Interacción entre 86e1y463z + 86e1pzyug + 86e35882c | Comprar un plan del marketplace en una company y revisar Billing (menú de usuario) y Accounting (Marketplace) | Billing muestra solo el plan IOND y el consumo de la company, sin cargos de Stripe; Accounting muestra la venta del cliente; el consumo de execution_time no cambia por la compra | Steve Nina | | | | |
| SAN-INT-03 | Websockets · App Connectors · Execution History | Interacción entre 86e35wv7f + 86e2t9962 + 86e2ak75f + 86e2nazxp | Con el socket autenticado por Bearer: minar un endpoint y ejecutar un board; abrir el replay de esa ejecución | El minado y el historial se actualizan en tiempo real sin recargar; la ejecución termina en estado final; el replay muestra el board ejecutado | Steve Nina | | | | |
| SAN-INT-04 | Rebranding · Register Company · Auth | Interacción entre 86e21f52d + 86e1r2c6z + 86e2buw9e | Registrar una company nueva en el dominio iond.ai e invitar a un miembro por email | Registro y login Keycloak sin errores; el email llega con marca iond y CTA al host vigente; el invitado queda asociado a la company | Mijael Rojas | | | | |
| SAN-INT-05 | Admin · Menu · Billing | Interacción entre 86e31pbz9 + 86e2fpp9y + 86e35882c + 86e1pzyug | En sesión de soporte (con VPN): navegar el menú nuevo de la company, ejecutar un board y salir con Leave company | Menú según permisos; la ejecución se registra en la company soportada (historial y consumo); sin acceso a otra company; Leave company vuelve al admin | Steve Nina | | | | |
| SAN-INT-06 | App Connectors · Ionmind · Billing | Interacción entre 86e2mt70g + 86e20nmqx + 86e1pzyug | Primera extracción con cada tier y luego con ai_credits agotado | El costo del modal cambia según el tier y se cobra una vez; con créditos agotados IonMind responde 403 'Feature quota exceeded' sin cobro ni job | Mijael Rojas | | | | |

## Casos `normal` — si queda tiempo (38)

Se ejecutan al final del miércoles. Los que no entren se marcan ⏭️ con el motivo y se listan en el Go/No-Go.

### 86e35882c · IONF-1344 — IOND — Reorganizar el menú principal y unificar los accesos de Billing según la nueva estructura

SIDE TENANT · MODULE Menu · QA ASIGNADO **Mijael Rojas** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e35882c-AC-3 | — | Botón Library en la cabecera de Boards, a la izquierda de Create Board. Precondición: Permiso de Boards y biblioteca | Abre /boards/library; la instalación funciona; Boards conserva crear/editar/ejecutar | |  | | |

### 86e1fawg0 · IONF-1020 — Implementar Monitoreo de Uso de Tokens por Usuario en Ion Flow (Flow Pilot)

SIDE TENANT · MODULE Flow Pilot · QA ASIGNADO **Mijael Rojas** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e1fawg0-AC-1 | — | Pregunta compleja que usa herramientas (varias iteraciones). Precondición: Prompt que dispare herramientas | Tokens y costos de todas las iteraciones agregados en un solo turno | |  | | |
| SAN-86e1fawg0-AC-2 | — | Retomar un chat antiguo y borrar un chat desde la UI. Precondición: Sesión previa con consumo | El acumulado continúa; el borrado es soft delete y el consumo persiste | |  | | |

### 86e22fzw2 · IONF-1130 — Boards — Animación del nodo Timer persiste al re-ingresar al canvas, inconsistencia visual

SIDE TENANT · MODULE Boards · QA ASIGNADO **Mijael Rojas** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e22fzw2-AC-1 | — | Flow con Timer de 60 s: salir del canvas y volver. Precondición: Board con nodo Timer | Sin animación residual; el estado visual refleja la ejecución real | | Revalidación: Evidencia de QA solo visual | | |

### 86e21f52d · IONF-1103 — Rebranding integral de Ionflow a iond

SIDE TENANT · MODULE Rebranding · QA ASIGNADO **Mijael Rojas** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2buw7v-AC-1 | (subtarea) Actualizar documentación y guías de usuario de Ionflow a iond en inglés y español | Guía de usuario en EN y ES. Precondición: Guía publicada | Ambas usan iond; cero "ionflow" renderizado; enlaces e imágenes válidos | | Revalidación: Subtarea sin QA propio | | |
| SAN-86e2buw8e-AC-1 | (subtarea) Actualizar marca Ionflow a iond en producto y assets | Product switcher, favicon, logos light/dark y export JSON. Precondición: gateway-ion y webcomponents desplegados | El item "iond" enlaza a la app correcta; archivo *-iond.json | | Revalidación: Subtarea sin QA propio | | |
| SAN-86e2buw8e-AC-2 | (subtarea) Actualizar marca Ionflow a iond en producto y assets | Login y navegación tras el cambio de logos y del product switcher. Precondición: Usuario tenant | Sin regresión en login ni navegación | | Revalidación: Subtarea sin QA propio | | |
| SAN-86e2buw9e-AC-2 | (subtarea) Actualizar comunicaciones, emails y soporte de Ionflow a iond | Revisar los emails enviados (subject, logo, footer). Precondición: Disparar los emails | iond en subject y logo; soporte hello@iond.ai; razón social según decisión del PO | | Revalidación: Subtarea sin QA ni CR propio | | |
| SAN-86e2czvzh-AC-1 | (subtarea) Rediseñar landing principal de iond e implementar blog y gestión continua de contenido | Landing en desktop y mobile, CTAs y páginas legales EN/ES | Layout correcto; Sign Up → app.iond.ai; Contact → hello@iond.ai | | Revalidación: Subtarea sin QA ni CR propio | | |

### 86e2fazfh · IONF-1201 — IonFlow: Rediseñar la vista y mejorar búsqueda, filtros y acciones de endpoints en App Connectors

SIDE TENANT · MODULE App Connectors · QA ASIGNADO **Mijael Rojas** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2fazfh-AC-2 | — | Buscar por ruta/método/descripción y filtrar por método o tipo. Precondición: Endpoints en más de una página | Filtra la colección completa; paginación coherente; sin nueva extracción | |  | | |
| SAN-86e2fazfh-AC-5 | — | Endpoint con descripción larga y endpoint histórico sin descripción. Precondición: Endpoints con y sin description | Truncado con "+" y modal; sin descripción → "Descripción no disponible" | |  | | |

### 86e2fpp9y · IONF-1205 — [Ionflow] Permitir acceso administrativo temporal a una compañía sin credenciales del usuario

SIDE ADMIN · MODULE Companies · QA ASIGNADO **Mijael Rojas** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2fpp9y-AC-2 | — | Admin busca compañía por nombre, subdominio o ID. Precondición: Admin; varias compañías, una con varios usuarios | Resultados correctos y paginados; placeholder "Search by name, subdomain or ID" | |  | | |

### 86e2nazxp · IONF-1248 — Fix Execution Lifecycle Bugs

SIDE TENANT · MODULE Boards · QA ASIGNADO **Steve Nina** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2nazxp-AC-5 | — | Revisar el mensaje de error en el modal y en el log de esa ejecución. Precondición: Ejecución fallida de AC-4 | Muestra la causa raíz, igual en Dev y Live, nunca "Invalid Node" | |  | | |

### 86e1pzyug · IONF-1056 — IONFLOW - Monetización unificada: Stripe, consumo por segundos, AI credits e IONPDF

SIDE ADMIN · TENANT · MODULE Billing · QA ASIGNADO **Steve Nina** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e1pzz9f-AC-B14 | (subtarea) Definir catálogo comercial y planes unificados | Revisar el catálogo de productos sembrado. Precondición: Admin > Billing > Products | Cada plan con producto provider='local' y data.prices; sin stripe_id visible | |  | | |
| SAN-86e1pzz9c-AC-59 | (subtarea) Incorporar historial de runtime y estimación de duración | Consultar runtime de un flow recién creado. Precondición: Flow sin ejecuciones | Estado neutro; no muestra 0 s ni una estimación inventada | | Revalidación: Subtarea sin QA propio | | |

### 86e1wfgam · IONF-1080 — Motor de exposicion por API (FASE 1)

SIDE API · MODULE DevApp API 2.0 · QA ASIGNADO **Mijael Rojas** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e1wfguh-AC-13 | (subtarea) pdf template | Crear, diseñar y guardar una plantilla en Marketplace > PDF List. Precondición: Vista de customer/account | El listado refresca sin duplicados, filtrado por account; error visible si el motor cae | | Revalidación: Subtarea sin QA propio | | |
| SAN-86e1wfgxk-AC-1 | (subtarea) pdf mapper | Ejecutar o gestionar un mapper vía API; enviar un mapper inválido. Precondición: App autorizada; mapper existente | Respuesta según contrato; el inválido se rechaza con error claro 4xx | | Revalidación: Subtarea sin QA propio | | |

### 86e2xnjyz · IONF-1267 — Optimizar latencia de IONFLOW con conexión SQLite persistente

SIDE TENANT · MODULE Boards · QA ASIGNADO **Mijael Rojas** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2xnjyz-AC-5 | — | Medir el flow de ~5000 órdenes contra el baseline. Precondición: Flow de referencia, varias corridas | Mejora documentada (≈ 52,9 s → 36,9 s); la meta de 3-5 s no se cumple (decisión del PO) | |  | | |

### 86e1fknjv · IONF-1022 — Integrar Logo.dev como fallback en el pipeline de logos de IonMind

SIDE TENANT · MODULE App Connectors · QA ASIGNADO **Steve Nina** · alcance completo

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e1fknjv-AC-2 | — | Ejecutar el discovery con LOGO_DEV_ENABLED=false. Precondición: Variable de entorno en false (solo QA de IonMind) | No llama a Logo.dev; usa el pipeline IA Vision | | Revalidación: Sin veredicto de QA | | |
| SAN-86e1fknjv-AC-3 | — | Ver el logo en Create Connector según el source. Precondición: Logos con source logo.dev y crawler | Logos provided by Logo.dev solo si source=logo.dev | | Revalidación: Sin veredicto de QA | | |
| SAN-86e1fkxz7-AC-2 | (subtarea) Backend - Integrar Logo.dev y API de actualización en IonMind | Alternar LOGO_DEV_AS_PRIMARY entre true y false. Precondición: LOGO_DEV_ENABLED=true | true: Logo.dev primero; false: IA primero y Logo.dev como fallback | | Revalidación: Sin veredicto de QA | | |
| SAN-86e1fky0g-AC-1 | (subtarea) Frontend - Atribución condicional y acción manual de Logo.dev en IonFlow | Mostrar u ocultar el botón Logo.dev según el origen del logo. Precondición: Create Connector con logo IonMind | Oculto si source=logo.dev; reaparece al borrar el logo; modal antes de sobrescribir | | Revalidación: Sin veredicto de QA | | |

### 86e25dyyz · IONF-1151 — Mejorar UX de navegación y edición en App Connectors creados

SIDE TENANT · MODULE App Connectors · QA ASIGNADO **Mijael Rojas** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e25dyyz-AC-1 | — | Configurar un App Connector creado: el usuario elige Details, Base, Webhooks, Nodes o Connections. Precondición: Conector publicado con nodos, webhooks y conexiones | Aterriza en Details con tabs visibles; ?tab=nodes abre Nodes; Back to List regresa | |  | | |

### 86e19dtkw · IONF-1007 — Error de sincronización UTC/Local en los disparadores de Company Schedules

SIDE ADMIN GATEWAY · MODULE Customer · QA ASIGNADO **Mijael Rojas** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e19dtkw-AC-2 | — | Timezone inválido o vacío en la company/account. Precondición: Timezone nulo o inválido en BD (sin UI) | Fallback a UTC con warning en el log; los demás schedules corren | |  | | |

### 86e22fzve · IONF-1127 — Boards — Scheduler ejecuta flow correctamente pero status queda en "error"

SIDE TENANT · MODULE Execution History · QA ASIGNADO **Steve Nina** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e22fzve-AC-2 | — | Fallo real en ContinueNode o PushNode. Precondición: Forzar fallo de PushNode/ContinueNode | Ejecución fatal con un único error; no continúa tras el fallo | |  | | |

### 86e1r2c6z · IONF-1075 — [Ionflow] Refactorizar flujo y formulario de registro de compañía

SIDE KC · MODULE Register Company · QA ASIGNADO **Steve Nina** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e1r2c6z-AC-13 | — | Datos de compañía, contacto, dirección y timezone tras el registro. Precondición: Registro con America/New_York, postal 10001 | Settings muestra todo; timezone en companies.timezone | |  | | |

### 86e2jwrvc · IONF-1223 — Ocultar prefijo "$" del nombre de los nodos

SIDE TENANT · MODULE Boards · QA ASIGNADO **Steve Nina** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2jwrvc-AC-1 | — | ID de los nodos en canvas, preview, chat de IA e Import Flow. Precondición: Board con varios tipos de nodo | Labels "1", "2", "3" sin el prefijo "$" | |  | | |

### 86e2e8gde · IONF-1193 — Extraer conectores UPS Track Alert y FedEx Supply Chain con IonMind

SIDE IONMIND · MODULE App Connectors · QA ASIGNADO **Mijael Rojas** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2e8gde-AC-1 | — | Artefacto UPS Track Alert v2. Precondición: Fuentes oficiales UPS | OAuth, alta de suscripción, webhook Tracking Event y Track API; máx. 100 trackings y 14 días | |  | | |
| SAN-86e2e8gde-AC-3 | — | Artefacto FedEx Supply Chain. Precondición: Sandbox FedEx SC | Create/Get/Update Webhook, eventos de orden, firma HMAC-SHA256 e idempotencia | |  | | |

### 86e1kp55k · IONF-1043 — El botón "Auto-mapper" en el nodo PDF Template no funciona al hacer clic

SIDE TENANT · MODULE PDF Templates · QA ASIGNADO **Mijael Rojas** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e1kp55k-AC-1 | — | Automap with AI en el formulario del nodo PDF Template. Precondición: Flow con 3 o más nodos ejecutados antes | Campos poblados con {{$N.field}}; Accept/Discard funcionan | |  | | |

### 86e223kvf · IONF-1104 — Mejoras estéticas globales en pantallas de iond / Ionflow

SIDE TENANT · MODULE Boards · QA ASIGNADO **Steve Nina** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e223kvf-AC-2 | — | Tablas y listados de las primeras vistas. Precondición: Boards, Executions, Connectors | Patrón visual de PDF Templates; sin overflow | |  | | |

### 86e2p459r · IONF-1249 — [BUG] IOND - Recuperar análisis de IonMind tras expiración de sesión y mostrar fallos terminales

SIDE TENANT · MODULE App Connectors · QA ASIGNADO **Mijael Rojas** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2p459r-AC-2 | — | Recargar la página durante Discovery o Mining. Precondición: Draft con job pendiente | Restaura el draft y consulta el job existente, sin POST duplicados | | Revalidación: REQ 5 diferido; rama marcada como cerrada | | |

### 86e2j43eg · IONF-1218 — IonMind - Extraer APIs de mensajería y generar App Connectors

SIDE IONMIND · MODULE App Connectors · QA ASIGNADO **Mijael Rojas** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2j43eg-AC-2 | — | Inventario de endpoints de cada plataforma. Precondición: Índice oficial por plataforma | Todo endpoint documentado clasificado; auth sin secretos reales | | Revalidación: Conector duplicado en la evidencia | | |

### 86e2t9962 · IONF-1253 — El estado de minado de un endpoint no se actualiza en tiempo real en App Connector

SIDE TENANT · MODULE App Connectors · QA ASIGNADO **Mijael Rojas** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e2t9962-AC-2 | — | Discovery (análisis de URL) al terminar. Precondición: URL de documentación válida | El resultado aparece sin recarga manual | |  | | |

### 86e25j0rn · IONF-1153 — Enviar errores de IonMind a Ionflow para notificaciones por correo y Mattermost

SIDE IONMIND · MODULE Notificaciones de IonMind · QA ASIGNADO **Mijael Rojas** · alcance muestra

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e25j0rn-AC-5 | — | Polling, caché o reintentos del mismo job fallido. Precondición: Job fallido; GET repetido | Un correo y un mensaje por job en 10 min; un fallo de envío no altera el job | |  | | |

### 86e22q3pc · IONF-1139 — Accounts - El buscador global no encuentra PDF Templates

SIDE TENANT · MODULE Accounts · QA ASIGNADO **Steve Nina** · alcance vía regresión

| ID | FEATURE | CASO | RESULTADO ESPERADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|
| SAN-86e22q3pc-T-02 | — | Buscar un PDF Template por nombre en el buscador global de Accounts. Precondición: Company con PDF Templates | Aparece en los resultados y abre el template | |  | | |

### Interacciones entre tickets

| ID | MODULE | FEATURE | CASO | RESULTADO ESPERADO | QA ASIGNADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|---|---|
| SAN-INT-02 | API · App Connectors · PDF Templates | Interacción entre 86e1wfgam + 86e2fazfh + 86e22fzqu | Vía DevApp API 2.0: ejecutar una action de un conector creado con IonMind (con descripciones) y renderizar un PDF Template con imagen creado en la UI | Contratos 200; la action responde raw del proveedor; el PDF se genera en R2 sin HTTP 500 | Mijael Rojas | | | | |
| SAN-INT-07 | Nodo Timer · Boards · Infra · Execution History | Interacción entre 86e22fzw2 + 86e2nazxp + 86e2xnjyz + 86e1mdnbq | Flow con Timer detenido con Stop en Live y otro completado | El detenido queda stopped y el completado completed; el SQLite se cierra una vez (opens=1) y el job de R2 se crea tras el cierre | Mijael Rojas | | | | |

## Tickets cubiertos por la regresión

No se re-ejecutan en el sanity: sus features están en filas del E2E maestro. Si la fila es `urgent` en la capa 1 corre el jueves AM; si es `high`, el jueves PM; si queda en la capa 2, la cubre la corrida nocturna o la rotación. La única verificación puntual (86e22q3pc) está en los casos `normal`.

| Ticket | IONF | FEATURE | Filas E2E | Dónde corren | Nota |
|---|---|---|---|---|---|
| [86e22fzut](https://app.clickup.com/t/86e22fzut) | IONF-1126 | PDF Templates — Cambios sin guardar se pierden al presionar Escape o cerrar modal sin confirmación | E2E-TEN-PDF-001, E2E-TEN-PDF-007 | capa 1 high, capa 1 urgent |  |
| [86e22fzq9](https://app.clickup.com/t/86e22fzq9) | IONF-1116 | PDF Templates — Sin límite de tamaño para Load Base PDF, la vista crashea con archivos grandes | E2E-TEN-PDF-004 | capa 1 urgent |  |
| [86e1gr6ug](https://app.clickup.com/t/86e1gr6ug) | IONF-1030 | Mejoras de la interface en ionflow dualtrack | E2E-TEN-BRD-030, E2E-TEN-BRD-046 | capa 1 urgent | Refactor de interfaz: preview y activar/pausar |
| [86e22fzrp](https://app.clickup.com/t/86e22fzrp) | IONF-1121 | Boards — Board sugiere cambios sin guardar tras commit exitoso al re-ingresar a la vista | E2E-TEN-BRD-035, E2E-TEN-BRD-036 | capa 1 high, capa 1 urgent |  |
| [86e22fzvx](https://app.clickup.com/t/86e22fzvx) | IONF-1128 | Boards — Simple Decision compara valores numéricos como strings, resultado incorrecto | E2E-TEN-BRD-005 | capa 1 urgent | Fila urgent de la capa 1 (nodo Simple Decision): comparar valores numéricos |
| [86e29e6jt](https://app.clickup.com/t/86e29e6jt) | IONF-1168 | Error de visualización (+4 horas) en los logs de ejecución de Company Schedules en UI Gateway | E2E-GTW-CUS-002, E2E-GTW-CUS-006 | capa 1 high | Hora local (sin +4 h) en los logs del schedule |
| [86e2dpfek](https://app.clickup.com/t/86e2dpfek) | IONF-1191 | Bug en la compilacion de gateway-ion en DEVELOPMENT | — | — | Fix de compilación: lo cubren el pipeline del C-24 y el smoke (la app compila y carga) |
| [86dy0bwmf](https://app.clickup.com/t/86dy0bwmf) | IONF-442 | Form Data Builder observations | E2E-TEN-BRD-006 | capa 1 urgent |  |
| [86e22fzw6](https://app.clickup.com/t/86e22fzw6) | IONF-1131 | Boards — Menú de contexto del Iterator muestra la data como collection vacío | E2E-TEN-BRD-009 | capa 1 urgent |  |
| [86e22q9h8](https://app.clickup.com/t/86e22q9h8) | IONF-1141 | App Connectors/Boards - No se encuentra la lista de nodos minados previamente | E2E-TEN-APC-005, E2E-TEN-APC-006 | capa 1 urgent |  |
| [86e04qn0d](https://app.clickup.com/t/86e04qn0d) | IONF-802 | Problemas con la validación al configurar en Admin - Orden de los nodos en Account - Pantalla sin App se visualiza al instalar una App en Account | E2E-GTW-CUS-001, E2E-GTW-CUS-004 | capa 1 high, capa 1 urgent | Validación al configurar, orden de nodos y pantalla sin App al instalar |
| [86e22q3pc](https://app.clickup.com/t/86e22q3pc) | IONF-1139 | Accounts - El buscador global no encuentra PDF Templates | — | — | Sin fila en el maestro: verificación puntual SAN-86e22q3pc-T-02 |
| [86e22fzt2](https://app.clickup.com/t/86e22fzt2) | IONF-1122 | Boards — Historial de cambios activa evento de cambios sin guardar al revisar commits con comentarios | E2E-TEN-BRD-037, E2E-TEN-BRD-046 | capa 1 high, capa 1 urgent | Incluye las subtareas 86e22fzq2 (toggle Active Flow) y 86e22fzw7 |
| [86e3085ap](https://app.clickup.com/t/86e3085ap) | IONF-1305 | Flow Pilot no responde al enviar un mensaje en Gateway > Board | E2E-TEN-BRD-040 | capa 1 urgent | Flow Pilot en Gateway > Board: la fila cubre el chat; validar también el mensaje del error 402 |

## Hallazgos

Resumen de los casos con RESOLUCION ❌ (el detalle está en las columnas TICKET y PRIORIDAD BUG de la hoja).

| ID del caso | PRIORIDAD del caso | Ticket origen | PRIORIDAD BUG | Causa | Decisión | TICKET |
|---|---|---|---|---|---|---|
| | | | | Ticket / integración entre tickets | Fix-forward (C-28) / Improvements con `det-sanity` / revertir con `diferido` | |

> Bug `urgent` → fix-forward en la rama RC (decisión ≤ 4 h, fix ≤ 1 día) y QA re-ejecuta el caso. El resto, previa discusión con PO y LD, va a Improvements `backlog` con `det-sanity`. Si el fix-forward no llega en plazo: revertir el ticket de la RC (`diferido`) o NO-GO.

## Candidatos a regresión y automatización

| Caso | Motivo | Propuesta |
|---|---|---|
| SAN-86e2ak75f-AC-2 · AC-9 | Feature nueva (replay) sin fila en el maestro | Fila nueva `TENANT > Execution History > Replay` + automatizar (`skills/automation/plan.md`) |
| SAN-86e31pbz9-AC-1…AC-6 | Accesos de soporte: riesgo de seguridad | Fila nueva `ADMIN > Companies > Support session` (hoy solo existe *log as a user*) |
| SAN-86e1wfgam-* | Contrato de la API externa | Suite de API en bot-test (RGR-01 como base) |
| SAN-86e35882c-AC-5 | Menú nuevo de Billing y Accounting | Filas nuevas `TENANT > Billing` y `TENANT > Marketplace > Accounting` |
| SAN-86e1pzyug-AC-B07 · AC-STREAM | Enforcement de consumo | Automatizar con una company de cuota baja (RGR-03) |
| SAN-86e35wv7f-AC-1…AC-6 | Websockets con Bearer | Prueba de API del mint y del scope (RGR-10) |

## Borrador C-26

Texto de `templates/comments/C-26.md`; se publica el miércoles al cierre en la tarea de Release de iond (y se enlaza desde la de IonMind):

```markdown
## 🧪 SANITY — iond v0.2.0 + IonMind v1.10.2 — [✅ / ❌]
**Ejecutados:** [N]/183 · ✅ [n] · ❌ [n] · ⏭️ [n] · **Automatizados:** 0
**Por prioridad:** urgent [n]/61 · high [n]/84 · normal [n]/38
**Hallazgos:** [ID — prioridad — decisión: fix-forward / Improvements #id / diferido]
**Evidencia / matriz:** knowledge/releases/iond/v0.2.0/sanity-matrix.csv
**Por ticket:** #86e1pzyug — AC-B01 ✅ · AC-B07 ✅ | #86e1y463z — AC-1 ✅ · BUG-12-1 ❌ (fix-forward) | …
**Decisiones del PO (observaciones de preparación):** [OBS-xx — aceptado / rechazado]
```
