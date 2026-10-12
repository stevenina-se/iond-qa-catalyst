# Tickets — beta iond v0.2.0 + IonMind v1.10.2

> **Salida de `release/ingest`** para la beta (tag `iond-beta`, espacio NEW GATEWAY IOND). Datos leídos de ClickUp en **solo lectura** el 2026-10-10; fuente del inventario: `resources/iond-beta.csv` (80 filas) + los 4 tickets de Logo.dev que no estaban en el export.
> Archivos de datos: `tickets.csv` (los 84) y `tickets-principales.csv` (los 51 principales, con el QA asignado). Hallazgos para el PO: `observaciones-preparacion.md`. Cambios en ClickUp: `acciones-clickup.md`.

## Resumen

| Dato | Valor |
|---|---|
| Tickets con el tag | **84** = 51 principales + 33 subtareas |
| iond v0.2.0 | **79** = 49 principales (48 con pruebas + 1 informativa) + 30 subtareas |
| IonMind v1.10.2 | **5** = 86e2t9962 y 86e1fknjv + 3 subtareas de Logo.dev |
| Estados | `production deploy` 66 · `ready to merge` 16 · `mock testing` 1 · `release approval` 1 |
| Principales por TYPE | Bug 22 · New Feature 12 · Improvement 8 · Refactor 6 · Task 3 |
| Prioridad de sanity | `urgent` 19 · `high` 17 · `normal` 14 · `Informativa` 1 |
| QA asignado (autor del veredicto) | Mijael Jhonatan Rojas Arias 25 · Steve Nina 23 · Sin veredicto de QA 3 |
| Riesgo | **Alto** (billing y consumo, pagos, accesos, motor, contrato de API, integraciones con IonMind y Gateway) |

**Reparto entre releases.** Los principales con Project IONMIND (86e2t9962 y la familia de Logo.dev) van en IonMind v1.10.2; el resto, incluidos 86e3085ap (Project Gateway, `Q-44`) y 86e1r4bu7 (Project "iod"), en iond v0.2.0. Los tickets de iond con PR en `ai_ionmind` llevan además Ionmind.Version para que su PR entre a la RC de IonMind; las subtareas de Logo.dev con PR en repos de iond llevan además Iond.Version.

## Principales por área

### Marketplace y pagos

| Ticket | IONF | Título | TYPE | Prioridad | Estado | Release | Sanity | QA asignado | Subtareas |
|---|---|---|---|---|---|---|---|---|---|
| [86e1y463z](https://app.clickup.com/t/86e1y463z) | IONF-1088 | Absorción y Unificación de NOVASPHERE en Gateway e Ionflow | New Feature | `urgent` | `ready to merge` | iond v0.2.0 | `urgent` | Steve Nina | 2 |
| [86e2mc23t](https://app.clickup.com/t/86e2mc23t) | IONF-1235 | Ocultar menu de categorias y barra de busqueda del webcomponente del marketplace mediante una prop | Improvement | `high` | `production deploy` | iond v0.2.0 | `urgent` | Steve Nina | — |

### Billing y consumo

| Ticket | IONF | Título | TYPE | Prioridad | Estado | Release | Sanity | QA asignado | Subtareas |
|---|---|---|---|---|---|---|---|---|---|
| [86e1pzyug](https://app.clickup.com/t/86e1pzyug) | IONF-1056 | IONFLOW - Monetización unificada: Stripe, consumo por segundos, AI credits e IONPDF | New Feature | `high` | `production deploy` | iond v0.2.0 | `urgent` | Steve Nina | 6 |
| [86e1m3jf8](https://app.clickup.com/t/86e1m3jf8) | IONF-1045 | Coste operativo por nodo y board para definir pricing y unidades de cobro | Task | `high` | `release approval` | iond v0.2.0 | `Informativa` | Sin veredicto | — |

### DevApp API 2.0

| Ticket | IONF | Título | TYPE | Prioridad | Estado | Release | Sanity | QA asignado | Subtareas |
|---|---|---|---|---|---|---|---|---|---|
| [86e1wfgam](https://app.clickup.com/t/86e1wfgam) | IONF-1080 | Motor de exposicion por API (FASE 1) | New Feature | `urgent` | `production deploy` | iond v0.2.0 | `urgent` | Mijael Rojas | 3 |

### Rebranding

| Ticket | IONF | Título | TYPE | Prioridad | Estado | Release | Sanity | QA asignado | Subtareas |
|---|---|---|---|---|---|---|---|---|---|
| [86e21f52d](https://app.clickup.com/t/86e21f52d) | IONF-1103 | Rebranding integral de Ionflow a iond | Refactor | `normal` | `production deploy` | iond v0.2.0 | `urgent` | Mijael Rojas | 7 |

### Accesos de soporte

| Ticket | IONF | Título | TYPE | Prioridad | Estado | Release | Sanity | QA asignado | Subtareas |
|---|---|---|---|---|---|---|---|---|---|
| [86e2fpp9y](https://app.clickup.com/t/86e2fpp9y) | IONF-1205 | [Ionflow] Permitir acceso administrativo temporal a una compañía sin credenciales del usuario | New Feature | `urgent` | `production deploy` | iond v0.2.0 | `urgent` | Mijael Rojas | — |
| [86e31pbz9](https://app.clickup.com/t/86e31pbz9) | IONF-1316 | Acceso directo a compañías sin inicio de sesión como usuario | New Feature | `high` | `production deploy` | iond v0.2.0 | `urgent` | Steve Nina | — |

### Motor y ejecución

| Ticket | IONF | Título | TYPE | Prioridad | Estado | Release | Sanity | QA asignado | Subtareas |
|---|---|---|---|---|---|---|---|---|---|
| [86e1mdnbq](https://app.clickup.com/t/86e1mdnbq) | IONF-1049 | Syncronizacion de logs con R2 | New Feature | `normal` | `production deploy` | iond v0.2.0 | `urgent` | Steve Nina | — |
| [86e2nazxp](https://app.clickup.com/t/86e2nazxp) | IONF-1248 | Fix Execution Lifecycle Bugs | Bug | `high` | `production deploy` | iond v0.2.0 | `urgent` | Steve Nina | — |
| [86e2xnjyz](https://app.clickup.com/t/86e2xnjyz) | IONF-1267 | Optimizar latencia de IONFLOW con conexión SQLite persistente | Refactor | `high` | `production deploy` | iond v0.2.0 | `urgent` | Mijael Rojas | — |
| [86e2ak75f](https://app.clickup.com/t/86e2ak75f) | IONF-1170 | Standardize Execution UI & Build Execution Replay Engine | New Feature | `high` | `production deploy` | iond v0.2.0 | `urgent` | Steve Nina | — |
| [86e22fzve](https://app.clickup.com/t/86e22fzve) | IONF-1127 | Boards — Scheduler ejecuta flow correctamente pero status queda en "error" | Bug | `high` | `production deploy` | iond v0.2.0 | `high` | Steve Nina | — |
| [86e2dpfek](https://app.clickup.com/t/86e2dpfek) | IONF-1191 | Bug en la compilacion de gateway-ion en DEVELOPMENT | Bug | `high` | `production deploy` | iond v0.2.0 | `normal` | Steve Nina | — |

### UI global

| Ticket | IONF | Título | TYPE | Prioridad | Estado | Release | Sanity | QA asignado | Subtareas |
|---|---|---|---|---|---|---|---|---|---|
| [86e35wv7f](https://app.clickup.com/t/86e35wv7f) | IONF-1347 | Soporte de websockets en el frontend | Bug | `high` | `mock testing` | iond v0.2.0 | `urgent` | Sin veredicto | — |
| [86e35882c](https://app.clickup.com/t/86e35882c) | IONF-1344 | IOND — Reorganizar el menú principal y unificar los accesos de Billing según la nueva estructura | Improvement | `high` | `ready to merge` | iond v0.2.0 | `urgent` | Mijael Rojas | — |
| [86e223kvf](https://app.clickup.com/t/86e223kvf) | IONF-1104 | Mejoras estéticas globales en pantallas de iond / Ionflow | Refactor | `high` | `production deploy` | iond v0.2.0 | `high` | Steve Nina | — |

### Flow Pilot

| Ticket | IONF | Título | TYPE | Prioridad | Estado | Release | Sanity | QA asignado | Subtareas |
|---|---|---|---|---|---|---|---|---|---|
| [86e1fawg0](https://app.clickup.com/t/86e1fawg0) | IONF-1020 | Implementar Monitoreo de Uso de Tokens por Usuario en Ion Flow (Flow Pilot) | Improvement | `high` | `production deploy` | iond v0.2.0 | `urgent` | Mijael Rojas | — |
| [86e3085ap](https://app.clickup.com/t/86e3085ap) | IONF-1305 | Flow Pilot no responde al enviar un mensaje en Gateway > Board | Bug | `normal` | `production deploy` | iond v0.2.0 | `normal` | Mijael Rojas | — |

### App Connectors e IonMind

| Ticket | IONF | Título | TYPE | Prioridad | Estado | Release | Sanity | QA asignado | Subtareas |
|---|---|---|---|---|---|---|---|---|---|
| [86e20nmqx](https://app.clickup.com/t/86e20nmqx) | IONF-1098 | Implementar confirmación y cobro para primer escrapeo de plataformas | New Feature | `high` | `production deploy` | iond v0.2.0 | `urgent` | Mijael Rojas | — |
| [86e2fazfh](https://app.clickup.com/t/86e2fazfh) | IONF-1201 | IonFlow: Rediseñar la vista y mejorar búsqueda, filtros y acciones de endpoints en App Connectors | Improvement | `normal` | `production deploy` | iond v0.2.0 | `urgent` | Mijael Rojas | 2 |
| [86e2mt70g](https://app.clickup.com/t/86e2mt70g) | IONF-1239 | IOND - Selección del service tier de IonMind | New Feature | `normal` | `production deploy` | iond v0.2.0 | `urgent` | Mijael Rojas | — |
| [86e1fknjv](https://app.clickup.com/t/86e1fknjv) | IONF-1022 | Integrar Logo.dev como fallback en el pipeline de logos de IonMind | New Feature | `normal` | `ready to merge` | IonMind v1.10.2 | `urgent` | Sin veredicto | 3 |
| [86e25dyyz](https://app.clickup.com/t/86e25dyyz) | IONF-1151 | Mejorar UX de navegación y edición en App Connectors creados | Improvement | `normal` | `ready to merge` | iond v0.2.0 | `high` | Mijael Rojas | — |
| [86e2e8gde](https://app.clickup.com/t/86e2e8gde) | IONF-1193 | Extraer conectores UPS Track Alert y FedEx Supply Chain con IonMind | Task | `high` | `ready to merge` | iond v0.2.0 | `high` | Mijael Rojas | — |
| [86e2g4ev0](https://app.clickup.com/t/86e2g4ev0) | IONF-1211 | [FIX] Investigar y corregir endpoints duplicados en App Connectors generados por IonMind | Bug | `high` | `production deploy` | iond v0.2.0 | `high` | Mijael Rojas | — |
| [86e2p459r](https://app.clickup.com/t/86e2p459r) | IONF-1249 | [BUG] IOND - Recuperar análisis de IonMind tras expiración de sesión y mostrar fallos terminales | Bug | `high` | `production deploy` | iond v0.2.0 | `high` | Mijael Rojas | — |
| [86e2j43eg](https://app.clickup.com/t/86e2j43eg) | IONF-1218 | IonMind - Extraer APIs de mensajería y generar App Connectors | Task | `normal` | `ready to merge` | iond v0.2.0 | `high` | Mijael Rojas | 4 |
| [86e2t9962](https://app.clickup.com/t/86e2t9962) | IONF-1253 | El estado de minado de un endpoint no se actualiza en tiempo real en App Connector | Bug | `high` | `ready to merge` | IonMind v1.10.2 | `high` | Mijael Rojas | — |
| [86e25j0rn](https://app.clickup.com/t/86e25j0rn) | IONF-1153 | Enviar errores de IonMind a Ionflow para notificaciones por correo y Mattermost | New Feature | `normal` | `production deploy` | iond v0.2.0 | `high` | Mijael Rojas | — |
| [86e22q9h8](https://app.clickup.com/t/86e22q9h8) | IONF-1141 | App Connectors/Boards - No se encuentra la lista de nodos minados previamente | Bug | `normal` | `production deploy` | iond v0.2.0 | `normal` | Mijael Rojas | — |

### Nodos del canvas

| Ticket | IONF | Título | TYPE | Prioridad | Estado | Release | Sanity | QA asignado | Subtareas |
|---|---|---|---|---|---|---|---|---|---|
| [86e22fzw2](https://app.clickup.com/t/86e22fzw2) | IONF-1130 | Boards — Animación del nodo Timer persiste al re-ingresar al canvas, inconsistencia visual | Bug | `normal` | `production deploy` | iond v0.2.0 | `urgent` | Mijael Rojas | 1 |
| [86e1kp55k](https://app.clickup.com/t/86e1kp55k) | IONF-1043 | El botón "Auto-mapper" en el nodo PDF Template no funciona al hacer clic | Improvement | `normal` | `production deploy` | iond v0.2.0 | `high` | Mijael Rojas | — |
| [86e22fzvx](https://app.clickup.com/t/86e22fzvx) | IONF-1128 | Boards — Simple Decision compara valores numéricos como strings, resultado incorrecto | Bug | `high` | `production deploy` | iond v0.2.0 | `normal` | Steve Nina | — |
| [86dy0bwmf](https://app.clickup.com/t/86dy0bwmf) | IONF-442 | Form Data Builder observations | Bug | `normal` | `production deploy` | iond v0.2.0 | `normal` | Steve Nina | — |
| [86e22fzw6](https://app.clickup.com/t/86e22fzw6) | IONF-1131 | Boards — Menú de contexto del Iterator muestra la data como collection vacío | Bug | `normal` | `production deploy` | iond v0.2.0 | `normal` | Mijael Rojas | 1 |

### PDF Templates

| Ticket | IONF | Título | TYPE | Prioridad | Estado | Release | Sanity | QA asignado | Subtareas |
|---|---|---|---|---|---|---|---|---|---|
| [86e22fzqu](https://app.clickup.com/t/86e22fzqu) | IONF-1119 | PDF Templates — Nodo PDF retorna error 500 genérico cuando la imagen no está en base64 | Bug | `high` | `production deploy` | iond v0.2.0 | `high` | Steve Nina | 2 |
| [86e22fzut](https://app.clickup.com/t/86e22fzut) | IONF-1126 | PDF Templates — Cambios sin guardar se pierden al presionar Escape o cerrar modal sin confirmación | Bug | `high` | `production deploy` | iond v0.2.0 | `normal` | Steve Nina | — |
| [86e22fzq9](https://app.clickup.com/t/86e22fzq9) | IONF-1116 | PDF Templates — Sin límite de tamaño para Load Base PDF, la vista crashea con archivos grandes | Bug | `high` | `production deploy` | iond v0.2.0 | `normal` | Steve Nina | — |
| [86e22q3pc](https://app.clickup.com/t/86e22q3pc) | IONF-1139 | Accounts - El buscador global no encuentra PDF Templates | Improvement | `normal` | `production deploy` | iond v0.2.0 | `normal` | Steve Nina | — |

### Boards y canvas

| Ticket | IONF | Título | TYPE | Prioridad | Estado | Release | Sanity | QA asignado | Subtareas |
|---|---|---|---|---|---|---|---|---|---|
| [86e2jwrvc](https://app.clickup.com/t/86e2jwrvc) | IONF-1223 | Ocultar prefijo "$" del nombre de los nodos | Refactor | `high` | `production deploy` | iond v0.2.0 | `high` | Steve Nina | — |
| [86e1gr6ug](https://app.clickup.com/t/86e1gr6ug) | IONF-1030 | Mejoras de la interface en ionflow dualtrack | Refactor | `normal` | `production deploy` | iond v0.2.0 | `normal` | Mijael Rojas | — |
| [86e22fzrp](https://app.clickup.com/t/86e22fzrp) | IONF-1121 | Boards — Board sugiere cambios sin guardar tras commit exitoso al re-ingresar a la vista | Bug | `normal` | `production deploy` | iond v0.2.0 | `normal` | Steve Nina | — |
| [86e22fzt2](https://app.clickup.com/t/86e22fzt2) | IONF-1122 | Boards — Historial de cambios activa evento de cambios sin guardar al revisar commits con comentarios | Bug | `normal` | `production deploy` | iond v0.2.0 | `normal` | Steve Nina | 2 |

### Grapps, Webhooks, Connections, Templates y registro

| Ticket | IONF | Título | TYPE | Prioridad | Estado | Release | Sanity | QA asignado | Subtareas |
|---|---|---|---|---|---|---|---|---|---|
| [86e19dtkw](https://app.clickup.com/t/86e19dtkw) | IONF-1007 | Error de sincronización UTC/Local en los disparadores de Company Schedules | Bug | `high` | `production deploy` | iond v0.2.0 | `high` | Mijael Rojas | — |
| [86e29hc1r](https://app.clickup.com/t/86e29hc1r) | IONF-1169 | Quitar CORS para rutas publicas de webhooks | Bug | `normal` | `production deploy` | iond v0.2.0 | `high` | Mijael Rojas | — |
| [86e22fzq7](https://app.clickup.com/t/86e22fzq7) | IONF-1114 | Connections — Reautorización por API Key crea conexión duplicada en lugar de sobrescribir | Bug | `high` | `production deploy` | iond v0.2.0 | `high` | Steve Nina | — |
| [86e1r2c6z](https://app.clickup.com/t/86e1r2c6z) | IONF-1075 | [Ionflow] Refactorizar flujo y formulario de registro de compañía | Refactor | `normal` | `production deploy` | iond v0.2.0 | `high` | Steve Nina | — |
| [86e1r4bu7](https://app.clickup.com/t/86e1r4bu7) | IONF-1076 | [Ionflow] Crear boards de ejemplo documentados y publicarlos como templates editables | New Feature | `normal` | `production deploy` | iond v0.2.0 | `high` | Steve Nina | — |
| [86e29e6jt](https://app.clickup.com/t/86e29e6jt) | IONF-1168 | Error de visualización (+4 horas) en los logs de ejecución de Company Schedules en UI Gateway | Bug | `normal` | `production deploy` | iond v0.2.0 | `normal` | Mijael Rojas | — |
| [86e04qn0d](https://app.clickup.com/t/86e04qn0d) | IONF-802 | Problemas con la validación al configurar en Admin - Orden de los nodos en Account - Pantalla sin App se visualiza al instalar una App en Account | Improvement | `normal` | `production deploy` | iond v0.2.0 | `normal` | Steve Nina | — |

## Subtareas

Siguen al padre (`A-20`): mismas suites, mismo QA y mismo destino en la RC.

| Subtarea | IONF | Título | Padre | Estado | Release | PRs | Nota |
|---|---|---|---|---|---|---|---|
| [86e1y46c7](https://app.clickup.com/t/86e1y46c7) | IONF-1089 | Implementación y Acople del Motor de Pagos Multicanal | 86e1y463z | `ready to merge` | iond v0.2.0 | — | Sin QA ni CR propio: revalidar. |
| [86e1y46d0](https://app.clickup.com/t/86e1y46d0) | IONF-1090 | Actualización de Frontend y Web Components en Gateway | 86e1y463z | `ready to merge` | iond v0.2.0 | — | Sin QA ni CR propio: revalidar. |
| [86e2epqqc](https://app.clickup.com/t/86e2epqqc) | IONF-1199 | Al pausar un flow con el nodo timer y luego hacer stop el flow continuasu ejecucion | 86e22fzw2 | `production deploy` | iond v0.2.0 | — | Sin QA ni CR propio: revalidar. |
| [86e2buw79](https://app.clickup.com/t/86e2buw79) | IONF-1172 | Migrar landing de alpha.ionflow.io a dominio iond.ai | 86e21f52d | `production deploy` | iond v0.2.0 | — | Redirects 301 sin evidencia de QA. |
| [86e2buw7v](https://app.clickup.com/t/86e2buw7v) | IONF-1173 | Actualizar documentación y guías de usuario de Ionflow a iond en inglés y español | 86e21f52d | `production deploy` | iond v0.2.0 | ionflow_docs#2 | QA en el padre. |
| [86e2buw8e](https://app.clickup.com/t/86e2buw8e) | IONF-1174 | Actualizar marca Ionflow a iond en producto y assets | 86e21f52d | `production deploy` | iond v0.2.0 | ion_gateway_ion#30, ion_flow_binaries#26, ion_webcomponents_flow#15, ion_gateway#34 | Cambió nombres de BD/servicios en docker-compose. |
| [86e2buw8v](https://app.clickup.com/t/86e2buw8v) | IONF-1175 | Actualizar documentación técnica e integraciones de Ionflow a iond | 86e21f52d | `production deploy` | iond v0.2.0 | ion_flow_binaries#25, ion_gateway#31, ion_gateway_ion#28, ion_webcomponents_flow#14, ion_dev_documentation (comentario) | QA en el padre. |
| [86e2buw9e](https://app.clickup.com/t/86e2buw9e) | IONF-1176 | Actualizar comunicaciones, emails y soporte de Ionflow a iond | 86e21f52d | `production deploy` | iond v0.2.0 | ion_gateway#35, ion_flow_binaries#27 | Sin QA ni CR propio; reporta IonMindControllerTest con 502. |
| [86e2buw9u](https://app.clickup.com/t/86e2buw9u) | IONF-1177 | Auditar identificadores técnicos y compatibilidad del rebranding a iond | 86e21f52d | `production deploy` | iond v0.2.0 | — | Auditoría: ~84 referencias pendientes. |
| [86e2czvzh](https://app.clickup.com/t/86e2czvzh) | IONF-1178 | Rediseñar landing principal de iond e implementar blog y gestión continua de contenido | 86e21f52d | `production deploy` | iond v0.2.0 | ionflow_ionflow_landing#2 | Sin QA ni CR propio; sin blog. |
| [86e2ft73m](https://app.clickup.com/t/86e2ft73m) | IONF-1206 | IonMind: Extraer y persistir descripciones para cada endpoint durante Discovery | 86e2fazfh | `production deploy` | iond v0.2.0 | ai_ionmind#12 | Solo code review (2026-07-27). PR en ai_ionmind: también Ionmind.Version. |
| [86e2ft7a8](https://app.clickup.com/t/86e2ft7a8) | IONF-1207 | IonFlow: Propagar y persistir descripciones de endpoints para App Connectors | 86e2fazfh | `production deploy` | iond v0.2.0 | — | Sin PR ni evidencia: revalidar. |
| [86e1pzz9g](https://app.clickup.com/t/86e1pzz9g) | IONF-1060 | Definir oferta standalone de IONPDF, add-on para IONFLOW y metering específico | 86e1pzyug | `production deploy` | iond v0.2.0 | — | QA en el padre (L3). |
| [86e1pzz9f](https://app.clickup.com/t/86e1pzz9f) | IONF-1059 | Definir catálogo comercial y planes unificados | 86e1pzyug | `production deploy` | iond v0.2.0 | — | QA en el padre (L3). |
| [86e1pzz9e](https://app.clickup.com/t/86e1pzz9e) | IONF-1058 | Definir enforcement, warnings y estado combinado | 86e1pzyug | `production deploy` | iond v0.2.0 | — | Sin QA propio; los emails mencionan gracia/overage (fuera del alcance B). |
| [86e1pzz9c](https://app.clickup.com/t/86e1pzz9c) | IONF-1057 | Incorporar historial de runtime y estimación de duración | 86e1pzyug | `production deploy` | iond v0.2.0 | — | Sin QA propio. |
| [86e1pzz9h](https://app.clickup.com/t/86e1pzz9h) | IONF-1061 | Implementar ledger de consumo y segundos por ejecución | 86e1pzyug | `production deploy` | iond v0.2.0 | — | Sin QA propio. |
| [86e1pzz9j](https://app.clickup.com/t/86e1pzz9j) | IONF-1062 | Diseñar integración Stripe y facturación de overage | 86e1pzyug | `production deploy` | iond v0.2.0 | — | Overage con Stripe Meters: fuera del alcance B (sin desarrollo) pero figura en production deploy. |
| [86e1wfgt2](https://app.clickup.com/t/86e1wfgt2) | IONF-1082 | app channels | 86e1wfgam | `production deploy` | iond v0.2.0 | — | Sin QA propio. |
| [86e1wfguh](https://app.clickup.com/t/86e1wfguh) | IONF-1081 | pdf template | 86e1wfgam | `production deploy` | iond v0.2.0 | — | Sin QA propio. |
| [86e1wfgxk](https://app.clickup.com/t/86e1wfgxk) | IONF-1083 | pdf mapper | 86e1wfgam | `production deploy` | iond v0.2.0 | — | Sin QA propio; mappers sin TC en la matriz L3. |
| [86e1fkxz7](https://app.clickup.com/t/86e1fkxz7) | IONF-1023 | Backend - Integrar Logo.dev y API de actualización en IonMind | 86e1fknjv | `ready to merge` | IonMind v1.10.2 | ai_ionmind#8 | Sin Iond Subcategory (propuesta: App Connectors). |
| [86e1fky0g](https://app.clickup.com/t/86e1fky0g) | IONF-1024 | Frontend - Atribución condicional y acción manual de Logo.dev en IonFlow | 86e1fknjv | `ready to merge` | IonMind v1.10.2 | ion_gateway_ion#17 | PR en un repo de iond: también Iond.Version v0.2.0. |
| [86e1qzefc](https://app.clickup.com/t/86e1qzefc) | — | Actualización del Backend de IonFlow | 86e1fknjv | `ready to merge` | IonMind v1.10.2 | ion_gateway#16 | PR en un repo de iond: también Iond.Version v0.2.0. Posible jobId cross-tenant en el proxy (AC-SEC). |
| [86e1xu7xp](https://app.clickup.com/t/86e1xu7xp) | IONF-1096 | ION PDF - ION PDF does not support Arabic characters | 86e22fzqu | `production deploy` | iond v0.2.0 | — | Caso de cliente; cubierto por los PRs y el QA del padre. |
| [86e22fzqh](https://app.clickup.com/t/86e22fzqh) | IONF-1118 | PDF Templates — Import Template no valida contenido JSON que rompe dimensiones del documento | 86e22fzqu | `production deploy` | iond v0.2.0 | — | QA en el padre. |
| [86e2j43xg](https://app.clickup.com/t/86e2j43xg) | IONF-1219 | IonMind - Extraer Telegram Bot API y crear App Connector | 86e2j43eg | `ready to merge` | iond v0.2.0 | — | QA en el padre. |
| [86e2j44hg](https://app.clickup.com/t/86e2j44hg) | IONF-1220 | IonMind - Extraer WhatsApp Cloud API y crear App Connector | 86e2j43eg | `ready to merge` | iond v0.2.0 | — | Evidencia parcial. |
| [86e2j4509](https://app.clickup.com/t/86e2j4509) | IONF-1221 | IonMind - Extraer Instagram API con Instagram Login y crear App Connector | 86e2j43eg | `ready to merge` | iond v0.2.0 | — | QA en el padre. |
| [86e2j45du](https://app.clickup.com/t/86e2j45du) | IONF-1222 | IonMind - Extraer Messenger Platform API y crear App Connector | 86e2j43eg | `ready to merge` | iond v0.2.0 | — | Evidencia parcial. |
| [86e22fzw1](https://app.clickup.com/t/86e22fzw1) | IONF-1129 | Boards — Nodo Iterator queda inconsistente al quitar contexto previo, imposibilita items manuales | 86e22fzw6 | `production deploy` | iond v0.2.0 | — | QA en el padre. |
| [86e22fzq2](https://app.clickup.com/t/86e22fzq2) | IONF-1111 | Boards — Toggle de Active Flow queda inconsistente al fallar la petición, sin toast de error | 86e22fzt2 | `production deploy` | iond v0.2.0 | — | QA en el padre. |
| [86e22fzw7](https://app.clickup.com/t/86e22fzw7) | IONF-1132 | Boards — Input de nueva conexión en nodo de app abre menú de contexto innecesariamente | 86e22fzt2 | `production deploy` | iond v0.2.0 | — | Va en la rama del padre. |

## PRs por repositorio (para armar las ramas RC)

Merge atómico (`Q-33`): todos los PRs de un ticket entran juntos o ninguno. *(comentario)* = el PR figura solo en los comentarios del ticket, no en su campo de MR; el RM lo confirma antes del corte.

| Repositorio | Release | PRs (ticket) |
|---|---|---|
| `ion_dev_documentation` | iond v0.2.0 | ion_dev_documentation (comentario) (86e2buw8v) |
| `ion_flow_binaries` | iond v0.2.0 | #5 (comentario) (86e1gr6ug) · #8 (86e1mdnbq) · #9 (comentario) (86e1gr6ug) · #10 (86e19dtkw) · #11 (86e22fzve) · #12 (86e1fawg0) · #13 (86e22fzvx) · #14 (86e22fzq7) · #15 (86e1r4bu7) · #16 (86e1wfgam) · #17 (comentario) (86e29hc1r) · #18 (86e1r2c6z) · #19 (86e29e6jt) · #20 (86e1kp55k) · #21 (86e1pzyug) · #22 (86e223kvf) · #23 (86e22fzw2) · #25 (86e2buw8v) · #26 (86e2buw8e) · #27 (86e2buw9e) · #28 (86e21f52d) · #30 (86e2nazxp) · #31 (86e22fzqu) · #32 (86e2fpp9y) · #33 (comentario) (86e1kp55k) · #38 (comentario) (86e1kp55k) · #39 (86e2xnjyz) · #45 (86e3085ap) · #46 (86e31pbz9) · #47 (86e2xnjyz) · #48 (86e2ak75f) · #49 (86e1y463z) · #56 (86e25dyyz) |
| `ion_gateway` | iond v0.2.0 | #11 (86e1fawg0) · #12 (86e20nmqx) · #15 (86e1r4bu7) · #16 (86e1qzefc) · #18 (86e1pzyug) · #22 (86e22q9h8) · #25 (comentario) (86e1r4bu7) · #27 (86e223kvf) · #31 (86e2buw8v) · #34 (86e2buw8e) · #35 (86e2buw9e) · #37 (86e21f52d) · #39 (86e2g4ev0) · #40 (86e2fpp9y) · #46 (86e2mt70g) · #51 (86e1wfgam) · #60 (86e31pbz9) · #62 (86e2ak75f) · #64 (86e25j0rn) · #65 (86e1y463z) · #70 (86e25j0rn) · #74 (comentario) (86e25dyyz) · #80 (86e35wv7f) |
| `ion_gateway_ion` | iond v0.2.0 | #4 (comentario) (86e1gr6ug) · #6 (86e20nmqx) · #9 (86e22fzrp) · #10 (86e22fzq9) · #11 (86e22fzut) · #12 (86e22fzq7) · #13 (86e1r2c6z) · #14 (86e1r4bu7) · #16 (comentario) (86e22fzrp) · #17 (86e1fky0g) · #18 (86e29e6jt) · #19 (86e1kp55k) · #20 (86e1pzyug) · #21 (comentario) (86e1r2c6z) · #22 (86e2dpfek) · #23 (86e223kvf) · #24 (86e22q9h8) · #25 (comentario) (86e1r4bu7) · #26 (86e22fzw2) · #28 (86e2buw8v) · #30 (86e2buw8e) · #31 (86e2jwrvc) · #32 (86e21f52d) · #34 (comentario) (86e1r4bu7) · #35 (comentario) (86e1kp55k) · #36 (86e2g4ev0) · #37 (86e2nazxp) · #38 (86e2fazfh) · #39 (86e2p459r) · #40 (86e22fzqu) · #41 (comentario) (86e1r4bu7) · #42 (86e2fpp9y) · #44 (86e04qn0d) · #45 (86e22q3pc) · #46 (comentario) (86e1kp55k) · #47 (86e2mt70g) · #52 (86e1wfgam) · #59 (86e3085ap) · #60 (86e25dyyz) · #61 (86e2mt70g) · #62 (86e31pbz9) · #63 (86e2ak75f) · #64 (86e1y463z) · #68 (comentario) (86e25dyyz) · #72 (86e35wv7f) · #73 (86e35882c) |
| `ion_webcomponents_flow` | iond v0.2.0 | #6 (86e22fzut) · #7 (86e22fzvx) · #8 (86e29e6jt) · #9 (86e1kp55k) · #10 (86dy0bwmf) · #11 (86e22fzw6) · #14 (86e2buw8v) · #15 (86e2buw8e) · #18 (86e2jwrvc) · #19 (86e21f52d) · #20 (86e2mc23t) · #21 (comentario) (86e1kp55k) · #22 (86e2nazxp) · #23 (86e04qn0d) · #25 (comentario) (86e1kp55k) · #27 (86e22fzt2) · #28 (86e1wfgam) · #29 (comentario) (86e1kp55k) · #32 (86e2ak75f) · #33 (86e1y463z) |
| `ionflow_docs` | iond v0.2.0 | #2 (86e2buw7v) |
| `ionflow_ionflow_landing` | iond v0.2.0 | #2 (86e2czvzh) |
| `ionflow_template_maker` | iond v0.2.0 | #1 (86e22fzqu) |
| `ai_ionmind` | IonMind v1.10.2 | #3 (86e20nmqx) · #8 (86e1fkxz7) · #11 (86e2e8gde) · #12 (86e2ft73m) · #16 (86e2p459r) · #17 (86e2j43eg) · #21 (86e2mt70g) · #25 (86e25j0rn) |

Sin PR: 86e2t9962 (se resolvió reiniciando pods), 86e1m3jf8 (informativa), 86e1fknjv (el código está en sus subtareas) y las subtareas cubiertas por la rama del padre.

## Mapa de impacto a nivel de feature

De cada ticket a las filas del E2E maestro que tocan sus features. Las filas del **foco** (`_impact/focus.csv`) entran como `urgent` en la regresión capa 1; las rutas por ticket `urgent` están en `_impact/impact-map.csv`.

### `urgent` — foco del release

| Ticket | Área | Rutas del E2E maestro | Filas en el foco | Sistemas cruzados | RGR |
|---|---|---|---|---|---|
| 86e35wv7f | UI global | tenant > notifications > open; tenant > execution history > details; tenant > boards > list > create board > preview; tenant > app connectors > create > connector via ionmind > analize | 4 | — | RGR-10 |
| 86e35882c | UI global | tenant > dashboard; tenant > settings > *; tenant > laanguaje > *; tenant > account > update personal information; tenant > templates > public templates > preview; tenant > credentials > edit key | 8 | — | — |
| 86e1y463z | Marketplace y pagos | admin gateway > customer > login > available market place > *; admin gateway > customer > login > configured channels > grapp instalation; admin > apps > add app > grapps > *; admin > apps > list > grapps > * | 12 | Gateway, Stripe | RGR-02 |
| 86e1mdnbq | Motor y ejecución | tenant > execution history > details | 1 | — | RGR-09 |
| 86e1fawg0 | Flow Pilot | tenant > boards > list > create board > flow pilot > * | 2 | IonMind | RGR-12 |
| 86e20nmqx | App Connectors e IonMind | tenant > app connectors > create > connector via ionmind > *; tenant > app connectors > create > endpoints via ionmind > * | 3 | IonMind | RGR-04 |
| 86e22fzw2 | Nodos del canvas | tenant > boards > list > create board > all tools > timer | 1 | — | — |
| 86e21f52d | Rebranding | kc > login with sso; kc > register with sso; kc > forgot password; tenant > dashboard; tenant > boards > list > download; tenant > boards > list > create board > export | 6 | — | RGR-07 |
| 86e2mc23t | Marketplace y pagos | admin gateway > customer > login > available market place > * | 6 | Gateway, Stripe | RGR-02 |
| 86e2fazfh | App Connectors e IonMind | tenant > app connectors > list > nodes > *; tenant > app connectors > list > base > edit; tenant > app connectors > filters > search | 7 | IonMind | RGR-04 |
| 86e2fpp9y | Accesos de soporte | admin > companies > list > company > user > log as a user | 1 | — | RGR-08 |
| 86e2nazxp | Motor y ejecución | tenant > boards > list > create board > preview; tenant > boards > list > active-pause; tenant > execution history > details | 3 | — | — |
| 86e1pzyug | Billing y consumo | admin > billing > *; admin > companies > list > company > subscription > assign plan; tenant > execution history > details | 10 | Stripe | RGR-03 |
| 86e1wfgam | DevApp API 2.0 | admin > developers > list > *; tenant > pdf templates > new template | 13 | — | RGR-01 |
| 86e2mt70g | App Connectors e IonMind | tenant > app connectors > create > connector via ionmind > analize | 1 | IonMind | RGR-04 |
| 86e31pbz9 | Accesos de soporte | admin > companies > list > company > user > log as a user | 1 | — | RGR-08 |
| 86e2xnjyz | Motor y ejecución | tenant > boards > list > create board > preview; tenant > boards > list > create board > storage > *; tenant > execution history > details | 10 | — | RGR-09 |
| 86e2ak75f | Motor y ejecución | tenant > execution history > * | 6 | — | — |
| 86e1fknjv | App Connectors e IonMind | tenant > app connectors > create > connector via ionmind > upload a logo via logo.dev; tenant > app connectors > create > manual connector | 2 | IonMind | RGR-04, RGR-11 |

### `high` — módulos del E2E maestro

| Ticket | Iond Subcategory | Módulos E2E | Cobertura en la regresión |
|---|---|---|---|
| 86e25dyyz | App Connectors | TEN-APC ADM-APC TEN-CNX | Filas `Urgent`/`High` de la hoja en esos módulos (`high`) |
| 86e19dtkw | Grapps | ADM-APP GTW-APP GTW-CUS TEN-CAT | Filas `Urgent`/`High` de la hoja en esos módulos (`high`) |
| 86e29hc1r | Webhooks | TEN-WHK | Filas `Urgent`/`High` de la hoja en esos módulos (`high`) |
| 86e22fzve | Execution History | TEN-EXH | Filas `Urgent`/`High` de la hoja en esos módulos (`high`) |
| 86e22fzq7 | Connections | TEN-CNX TEN-APC | Filas `Urgent`/`High` de la hoja en esos módulos (`high`) |
| 86e1r2c6z | Register Company | KC-AUT ADM-CMP | Filas `Urgent`/`High` de la hoja en esos módulos (`high`) |
| 86e1r4bu7 | Templates | TEN-TPL ADM-TPL | Filas `Urgent`/`High` de la hoja en esos módulos (`high`) |
| 86e2jwrvc | Boards | TEN-BRD ADM-BRD TEN-TPL ADM-TPL TEN-EXH | Filas `Urgent`/`High` de la hoja en esos módulos (`high`) |
| 86e2e8gde | Ionmind | TEN-APC TEN-CNX | Filas `Urgent`/`High` de la hoja en esos módulos (`high`) + RGR-05 |
| 86e22fzqu | Nodo PDF Templates | — | Filas `Urgent`/`High` de la hoja en esos módulos (`high`) |
| 86e1kp55k | Nodo PDF Templates | — | Filas `Urgent`/`High` de la hoja en esos módulos (`high`) |
| 86e223kvf | Boards | TEN-BRD ADM-BRD TEN-TPL ADM-TPL TEN-EXH | Filas `Urgent`/`High` de la hoja en esos módulos (`high`) |
| 86e2g4ev0 | Boards | TEN-BRD ADM-BRD TEN-TPL ADM-TPL TEN-EXH | Filas `Urgent`/`High` de la hoja en esos módulos (`high`) + RGR-04 |
| 86e2p459r | Ionmind | TEN-APC TEN-CNX | Filas `Urgent`/`High` de la hoja en esos módulos (`high`) + RGR-04 |
| 86e2j43eg | App Connectors | TEN-APC ADM-APC TEN-CNX | Filas `Urgent`/`High` de la hoja en esos módulos (`high`) + RGR-05 |
| 86e2t9962 | App Connectors | TEN-APC ADM-APC TEN-CNX | Filas `Urgent`/`High` de la hoja en esos módulos (`high`) + RGR-10 |
| 86e25j0rn | Ionmind | TEN-APC TEN-CNX | Filas `Urgent`/`High` de la hoja en esos módulos (`high`) + RGR-06 |

### `normal` — filas que los cubren

| Ticket | Filas E2E | Dónde corre |
|---|---|---|
| 86e22fzut | E2E-TEN-PDF-001, E2E-TEN-PDF-007 | capa 1 high, capa 1 urgent |
| 86e22fzq9 | E2E-TEN-PDF-004 | capa 1 urgent |
| 86e1gr6ug | E2E-TEN-BRD-030, E2E-TEN-BRD-046 | capa 1 urgent |
| 86e22fzrp | E2E-TEN-BRD-035, E2E-TEN-BRD-036 | capa 1 high, capa 1 urgent |
| 86e22fzvx | E2E-TEN-BRD-005 | capa 1 urgent |
| 86e29e6jt | E2E-GTW-CUS-002, E2E-GTW-CUS-006 | capa 1 high |
| 86e2dpfek | — | Fix de compilación: lo cubren el pipeline del C-24 y el smoke (la app compila y carga) |
| 86dy0bwmf | E2E-TEN-BRD-006 | capa 1 urgent |
| 86e22fzw6 | E2E-TEN-BRD-009 | capa 1 urgent |
| 86e22q9h8 | E2E-TEN-APC-005, E2E-TEN-APC-006 | capa 1 urgent |
| 86e04qn0d | E2E-GTW-CUS-001, E2E-GTW-CUS-004 | capa 1 high, capa 1 urgent |
| 86e22q3pc | — | Sin fila en el maestro: verificación puntual SAN-86e22q3pc-T-02 |
| 86e22fzt2 | E2E-TEN-BRD-037, E2E-TEN-BRD-046 | capa 1 high, capa 1 urgent |
| 86e3085ap | E2E-TEN-BRD-040 | capa 1 urgent |

## Infraestructura y prerrequisitos

Checklist en `release-task.md` (sección *Prerrequisitos*): migraciones (monetización, DevApp API 2.0, replay e historial, tokens de Flow Pilot, endpoints de IonMind, registro de compañía), servicios (R2, Reverb, OAuth2, VPN de soporte, Logo.dev, Geoapify, Mattermost, SMTP, Stripe Connect del marketplace) y dominios `iond.ai`.
