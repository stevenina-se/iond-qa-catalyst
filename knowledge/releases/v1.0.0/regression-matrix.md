# Regression Matrix — v1.0.0

> Generado por `skills/release/regression-matrix`
> Fecha: 2026-06-24
> Versión: v1.0.0
> Fuente de tickets: `matched_tickets1.csv` (182 tickets reales de ClickUp)
> CSV guía: `Test Plan - IONFLOW - Smoke Test.csv`

---

## Resumen

| Métrica | Valor |
|---------|-------|
| Total de casos | 82 |
| Regresión directa | 38 |
| Regresión indirecta | 22 |
| Baseline | 22 |
| Módulos cubiertos | 12 |
| Módulos afectados por release | 9 |

---

## Cobertura por Módulo

| Módulo | Criticidad (L1) | Directos | Indirectos | Baseline | Total |
|--------|-----------------|---------|-----------|---------|-------|
| core-engine / Nodes | 🔴 Crítico | 12 | 3 | 0 | 15 |
| boards | 🔴 Crítico | 7 | 4 | 0 | 11 |
| auth | 🟠 Alto | 5 | 2 | 2 | 9 |
| connections | 🟠 Alto | 6 | 3 | 0 | 9 |
| data-store | 🟠 Alto | 4 | 2 | 0 | 6 |
| webhooks | 🟠 Alto | 3 | 2 | 2 | 7 |
| executions | 🟠 Alto | 1 | 3 | 2 | 6 |
| canvas / ux-ui | 🟡 Medio | 5 | 0 | 0 | 5 |
| admin / company | 🟡 Medio | 2 | 3 | 0 | 5 |
| pdf-templates | 🟠 Alto | 0 | 0 | 4 | 4 |
| billing | 🟠 Alto | 0 | 0 | 3 | 3 |
| keys / credentials | 🟠 Alto | 0 | 0 | 2 | 2 |

---

## Tickets del Release vs. Módulos Impactados

| Ticket | Descripción | Módulo directo | Módulos cross-impact |
|--------|-------------|---------------|---------------------|
| IONF-103 | Unificar endpoints para la creación de los grapp | connections | boards, services |
| IONF-110 | Exponer vistas públicas con apps de terceros | core-engine | boards, auth |
| IONF-114 | Crear/validar cuenta en Ion Flow con Keycloak | auth | todos |
| IONF-116 | Crear un app de forma manual | connections | services, boards |
| IONF-141 | Revisar errores de Basic Auth en GET | auth, connections | boards (nodos app) |
| IONF-142 | Refactorización de connections con integraciones | connections | boards, integrations |
| IONF-146 | Edición de nombres en Connections | connections | ux-ui |
| IONF-147 | Confirmación de cambios no guardados | ux-ui | boards, connections |
| IONF-159 | Data Store — modal conserva info anterior | data-store | canvas |
| IONF-162 | Data Store — solapamiento en WebComponent | data-store | canvas, boards |
| IONF-163 | Data Store — visualización de datos | data-store | boards, executions |
| IONF-165 | Completar Refresh token en motor de autorización | auth | connections, boards |
| IONF-168 | Corregir campos app | connections | boards |
| IONF-226 | Migrar componentes a TailwindCSS | canvas | all frontend |
| IONF-227 | Nodo Switch dinámico | core-engine (nodos) | boards, executions |
| IONF-266 | Nodo Timer | core-engine (nodos) | boards, executions |
| IONF-281 | Modales de confirmación para eliminación | ux-ui | boards, connections, data-store |
| IONF-309 | Revision Alpha webcomponents | canvas | boards |
| IONF-313 | Nested elements y Advance fields en Form | canvas, core-engine | boards |
| IONF-320 | Expression language en mappers (casteadores) | core-engine (transformer) | boards, executions |
| IONF-327 | Fix creación de módulos con mismo nombre | connections | boards |
| IONF-328 | Llamar un flow dentro de otro flow | core-engine (Call Flow) | boards, executions |
| IONF-362 | Login SSO con Keycloak | auth | todos |
| IONF-368 | UX/UI Error en pantalla de integrations | ux-ui | connections |
| IONF-376 | Fix casteo en expression language | core-engine (transformer) | boards, executions |
| IONF-379 | Refactorizar motor de ejecución de flows | core-engine, boards | executions, nodes |
| IONF-380 | Motor de nodos en Go (dev apps y companies) | core-engine | boards, connections |
| IONF-404 | Fix acumulador en transformer + collection | core-engine (transformer) | boards |
| IONF-406 | Fix recursividad en nodos entrelazados | core-engine, boards | executions |
| IONF-414 | Estructura Array no añade items | core-engine (canvas) | boards |
| IONF-416 | Default para booleans en transformer | core-engine (transformer) | boards |
| IONF-419 | Motor de versionamiento de flows (Git) | boards | core-engine |
| IONF-449 | Modificaciones en nodo webhook | webhooks, core-engine | boards, executions |
| IONF-463 | Iterar enteros en transformer | core-engine (transformer) | boards |
| IONF-482 | Restaurar flow mediante git | boards | core-engine |
| IONF-485 | Actualizar tema de la plataforma | ux-ui | all frontend |
| IONF-498 | Actualizar versión 1.2.x de gateway | auth | all modules |
| IONF-506 | Vista configuración de company | admin | auth |
| IONF-507 | Seeders de apps desplegadas | connections | admin |
| IONF-509 | Doble scroll en nodos del lienzo | canvas | boards |
| IONF-512 | Fix reinicio secuencia de IDs de nodos | core-engine | boards |
| IONF-516 | Fix Transformer sin salida | core-engine (transformer) | boards, executions |
| IONF-517 | Errores al configurar Custom App | connections | boards |
| IONF-552 | Nodos faltantes para Data Storage | data-store, core-engine | boards |
| IONF-680 | Fix ejecución de Schedule | core-engine (triggers) | boards, executions |
| IONF-695 | Soportar webhooks en los grapp | webhooks, connections | boards |
| IONF-763 | Usuario inicial sin todos los permisos | auth | todos |
| IONF-764 | Inconsistencias en UI de permisos de usuario | auth, ux-ui | todos |
| IONF-786 | Fix webhook con content-type | webhooks | boards, executions |
| IONF-820 | Nodo exportación PDF | core-engine, pdf-templates | boards |
| IONF-899 | URL no se actualiza al crear Board | boards | ux-ui |
| IONF-900 | Bug al actualizar label de nodo | core-engine, canvas | boards |
| IONF-901 | Bug mapeo de campos select y boolean | core-engine (Form/Mapper) | boards |
| IONF-935 | Nodo Aggregate en flows | core-engine (nodos) | boards, executions |
| IONF-939 | Nodo Code | core-engine (nodos) | boards, executions |
| IONF-1013 | Nodo Output genera array de arrays | core-engine | boards |
| IONF-1074 | Refactorizar Keycloak — fix login | auth | todos |

---

## Regression Matrix

| ID | Side | Módulo | Tipo Regresión | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Estado |
|----|------|--------|---------------|-------------|--------------|-------|-------------------|-----------|--------|
| REG-001 | TENANT | core-engine / Nodes | `[DIRECTA]` | Nodo Transformer ejecuta sub-flow y retorna resultado | Flow con nodo Transformer (Mapper UI) configurado | Login > Sidebar: Boards > Abrir flow de prueba > Canvas: agregar nodo Transformer > Configurar sub-flow con 2 campos > Ejecutar flow > Verificar output | El nodo Transformer emite output con los campos mapeados correctamente, sin errores de acumulador ni salidas vacías (IONF-404, IONF-516) | 🔴 Crítico | ⬜ Pendiente |
| REG-002 | TENANT | core-engine / Nodes | `[DIRECTA]` | Nodo Transformer castea tipos con Expression Language | Flow con nodo Transformer y casteo de string a number | Login > Sidebar: Boards > Abrir flow > Canvas: configurar Transformer con expresión de casteo `{{$1.precio}}` como número > Ejecutar > Verificar resultado | El valor es casteado correctamente al tipo esperado (string, number, boolean, array). Fix de IONF-320, IONF-376 | 🔴 Crítico | ⬜ Pendiente |
| REG-003 | TENANT | core-engine / Nodes | `[DIRECTA]` | Nodo Transformer: default para boolean funciona | Flow con nodo Transformer con campo boolean sin valor | Login > Sidebar: Boards > Abrir flow > Canvas: Transformer con campo boolean sin valor en el input > Ejecutar > Verificar output | El nodo emite el valor default configurado (true/false) en vez de null o error (IONF-416) | 🔴 Crítico | ⬜ Pendiente |
| REG-004 | TENANT | core-engine / Nodes | `[DIRECTA]` | Nodo Transformer itera enteros correctamente | Flow con Transformer que itera sobre lista de números enteros | Login > Sidebar: Boards > Abrir flow > Canvas: Transformer con campo iterando lista `[1, 2, 3]` > Ejecutar > Verificar que itera todos los items | Cada entero de la lista es procesado individualmente. Sin errores de tipo (IONF-463) | 🔴 Crítico | ⬜ Pendiente |
| REG-005 | TENANT | core-engine / Nodes | `[DIRECTA]` | Nodo Switch dinámico rutea correctamente en modo rules | Flow con nodo Switch (Multiple Decision) configurado con 3 reglas | Login > Sidebar: Boards > Abrir flow > Canvas: agregar nodo Switch > Configurar mode=rules con condiciones string/number/boolean > Ejecutar con distintos inputs > Verificar ruteo | El flow se dirige al output correcto según la regla que aplica (IONF-227) | 🔴 Crítico | ⬜ Pendiente |
| REG-006 | TENANT | core-engine / Nodes | `[DIRECTA]` | Nodo Timer pausa el flow el tiempo configurado | Flow con nodo Timer configurado en 10 segundos | Login > Sidebar: Boards > Abrir flow > Canvas: agregar nodo Timer con 10s > Ejecutar flow > Verificar que el siguiente nodo se ejecuta después de 10s | El flow espera exactamente el tiempo configurado antes de continuar. El output incluye `duration` y `completed_at` (IONF-266) | 🔴 Crítico | ⬜ Pendiente |
| REG-007 | TENANT | core-engine / Nodes | `[DIRECTA]` | Nodo Call Component-Flow invoca sub-flow y retorna resultado | Flow principal con nodo Call Component-Flow apuntando a un Component-Flow existente | Login > Sidebar: Boards > Abrir flow principal > Canvas: agregar nodo Call Component-Flow > Seleccionar Component-Flow existente > Ejecutar flow > Verificar resultado | El Component-Flow se ejecuta correctamente y retorna el resultado al flow principal (IONF-328) | 🔴 Crítico | ⬜ Pendiente |
| REG-008 | TENANT | core-engine / Nodes | `[DIRECTA]` | Nodo Aggregate agrupa N items y emite array | Flow con nodo Aggregate configurado con length=3 | Login > Sidebar: Boards > Abrir flow > Canvas: agregar nodo Aggregate con length=3 > Enviar 3 items de input > Verificar que el output es un array de 3 elementos | El nodo Aggregate emite un array de 3 items al recibir el tercero, sin emitir antes (IONF-935) | 🔴 Crítico | ⬜ Pendiente |
| REG-009 | TENANT | core-engine / Nodes | `[DIRECTA]` | Nodo Code ejecuta Python correctamente | Flow con nodo Code en lenguaje Python | Login > Sidebar: Boards > Abrir flow > Canvas: agregar nodo Code > Seleccionar Python > Escribir `result = 2 + 2` > Ejecutar > Verificar output | El nodo Code retorna `4` como resultado. Timeout por defecto 30s respetado (IONF-939) | 🔴 Crítico | ⬜ Pendiente |
| REG-010 | TENANT | core-engine / Nodes | `[DIRECTA]` | Nodo Form (Mapper) extrae params correctamente | Flow con nodo Form configurado con params | Login > Sidebar: Boards > Abrir flow > Canvas: agregar nodo Form > Configurar params con 2 campos > Ejecutar > Verificar output | El nodo emite el valor del campo `params` correctamente. Sin error "Mapper not configured" (IONF-901) | 🔴 Crítico | ⬜ Pendiente |
| REG-011 | TENANT | core-engine / Nodes | `[DIRECTA]` | Nodo Schedule trigger inicia flow en el tiempo configurado | Flow con trigger Schedule configurado | Login > Sidebar: Boards > Abrir flow con trigger Schedule > Verificar que el flow se ejecuta según el cron configurado > Revisar historial de ejecuciones | El flow se dispara automáticamente en el horario configurado sin errores. Fix de IONF-680 | 🔴 Crítico | ⬜ Pendiente |
| REG-012 | TENANT | core-engine / Nodes | `[DIRECTA]` | Nodo con recursividad no provoca loop infinito | Flow con nodos entrelazados (potencial recursividad) | Login > Sidebar: Boards > Abrir flow con nodos que se referencian mutuamente > Ejecutar > Verificar que el flow termina correctamente | El motor detecta y maneja la recursividad sin colgarse ni provocar loop infinito (IONF-406) | 🔴 Crítico | ⬜ Pendiente |
| REG-013 | TENANT | boards | `[DIRECTA]` | Crear y guardar un flow nuevo | Usuario autenticado sin flows existentes | Login > Sidebar: Boards > Clic en "New Board" > Ingresar nombre > Guardar > Verificar que aparece en la lista | El flow se crea correctamente, aparece en la lista, y la URL se actualiza con su ID (IONF-899) | 🔴 Crítico | ⬜ Pendiente |
| REG-014 | TENANT | boards | `[DIRECTA]` | Motor de versionamiento Git — commit de cambios | Flow existente con cambios en el canvas | Login > Sidebar: Boards > Abrir flow > Canvas: modificar nodo existente > Guardar > Toolbar: clic en "Save Version" (o equivalente Git) > Verificar historial de versiones | El cambio se guarda como un commit en el historial de versiones del flow (IONF-419) | 🔴 Crítico | ⬜ Pendiente |
| REG-015 | TENANT | boards | `[DIRECTA]` | Restaurar flow mediante Git (discard changes) | Flow existente con al menos 2 versiones | Login > Sidebar: Boards > Abrir flow > Canvas: hacer un cambio > Toolbar: clic en "Restore" / "Discard Changes" > Seleccionar versión anterior > Confirmar | El flow vuelve al estado de la versión seleccionada sin pérdida de datos (IONF-482) | 🔴 Crítico | ⬜ Pendiente |
| REG-016 | TENANT | boards | `[DIRECTA]` | Ejecutar flow en modo Development step-by-step | Flow con al menos 2 nodos conectados | Login > Sidebar: Boards > Abrir flow > Canvas: clic en modo Development > Ejecutar trigger manualmente > Verificar que se puede avanzar nodo por nodo vía WebSocket | El flow se ejecuta nodo a nodo mostrando el output de cada uno en tiempo real (IONF-379) | 🔴 Crítico | ⬜ Pendiente |
| REG-017 | TENANT | boards | `[DIRECTA]` | Importar un flow desde archivo JSON/YAML | Archivo de flow válido para importar | Login > Sidebar: Boards > Clic en "Import Flow" > Seleccionar archivo > Confirmar > Verificar que el flow importado aparece en la lista | El flow se importa correctamente con todos sus nodos y conexiones intactos (IONF-530) | 🟠 Alto | ⬜ Pendiente |
| REG-018 | TENANT | boards | `[DIRECTA]` | Vista de gitdiff de flow no sobrecarga el browser | Flow con historial de versiones largo | Login > Sidebar: Boards > Abrir flow > Toolbar: abrir vista de Git Diff > Navegar entre versiones > Verificar rendimiento | La vista de Git Diff carga sin causar lag excesivo ni crash del browser (IONF-522) | 🟡 Medio | ⬜ Pendiente |
| REG-019 | TENANT | boards | `[DIRECTA]` | URL del board se actualiza al crearlo | Flow recién creado | Login > Sidebar: Boards > Clic en "New Board" > Nombrar y guardar > Verificar URL > Refrescar la página > Verificar que el board persiste | La URL se actualiza al ID del board. Al refrescar el board sigue visible (IONF-899) | 🟠 Alto | ⬜ Pendiente |
| REG-020 | KC | auth | `[DIRECTA]` | Login SSO con Keycloak — flujo completo | Entorno con Keycloak configurado, usuario válido | Navegar a `/login` > Clic en "Login with SSO" > Keycloak: ingresar credenciales > Callback > Seleccionar company > Verificar acceso al dashboard | El usuario puede loguearse correctamente vía Keycloak y accede con sus permisos (IONF-362, IONF-1074) | 🔴 Crítico | ⬜ Pendiente |
| REG-021 | TENANT | auth | `[DIRECTA]` | Refresh token funciona automáticamente | Usuario logueado con sesión a punto de expirar | Login > Dejar sesión hasta cerca de expiración > Realizar GET a la API > Verificar que el token se renueva sin re-login | El token es renovado automáticamente. La acción continúa exitosamente (IONF-165) | 🔴 Crítico | ⬜ Pendiente |
| REG-022 | ADMIN | auth | `[DIRECTA]` | Usuario inicial de company tiene todos los permisos | Company recién creada | Admin > Companies > Crear nueva company > Verificar permisos del usuario inicial | El usuario inicial tiene todos los permisos sin necesidad de intervención manual (IONF-763) | 🟠 Alto | ⬜ Pendiente |
| REG-023 | KC | auth | `[DIRECTA]` | Fix login con Keycloak en diferentes dominios | Entorno con múltiples subdominios | Login desde dominio A > Segunda pestaña en dominio B > Verificar SSO cross-domain | El login funciona correctamente en cualquier dominio configurado (IONF-543) | 🟠 Alto | ⬜ Pendiente |
| REG-024 | ADMIN | auth | `[DIRECTA]` | Permisos de usuario sin inconsistencias en UI | Usuario con múltiples roles en una company | Admin > Companies > Seleccionar company > Users > Seleccionar usuario > Ver permisos | Los permisos se muestran sin elementos duplicados ni estilos incorrectos (IONF-764) | 🟡 Medio | ⬜ Pendiente |
| REG-025 | TENANT | connections | `[DIRECTA]` | Crear App Connector manual — happy path | Usuario con permiso CREATE_APP | Login > Sidebar: Connections > Clic en "New App" > Tipo "Manual" > Completar nombre y categoría > Guardar | El connector se crea y aparece en la lista de connections (IONF-116) | 🟠 Alto | ⬜ Pendiente |
| REG-026 | TENANT | connections | `[DIRECTA]` | Editar nombre de App, Módulo y Connection | App Connector existente con módulos y conexiones | Login > Sidebar: Connections > Seleccionar connector > Editar nombre del App > Guardar > Editar nombre de módulo > Guardar | Los nombres se actualizan sin errores de duplicado (IONF-146, IONF-327) | 🟠 Alto | ⬜ Pendiente |
| REG-027 | TENANT | connections | `[DIRECTA]` | Basic Auth y API Key en GET request funcionan | App Connector con Basic Auth configurado | Login > Sidebar: Connections > Connector con Basic Auth > Crear conexión > Canvas: nodo de app GET > Ejecutar > Verificar respuesta | La request GET ejecuta correctamente con credenciales Basic Auth / API Key (IONF-141) | 🔴 Crítico | ⬜ Pendiente |
| REG-028 | TENANT | connections | `[DIRECTA]` | Configurar Custom App sin errores | Usuario con permiso CREATE_APP | Login > Sidebar: Connections > Clic en "New App" > Tipo "Custom" > Completar configuración OAuth > Guardar | La Custom App se configura sin errores de validación ni guardado (IONF-517) | 🟠 Alto | ⬜ Pendiente |
| REG-029 | ADMIN GATEWAY | connections | `[DIRECTA]` | Unificación de endpoints de Grapps funciona | GRAPP existente configurado | Admin > Apps > Seleccionar GRAPP > Instalar en company de prueba via endpoint unificado | El proceso usa el endpoint unificado correctamente sin errores de routing (IONF-103) | 🟠 Alto | ⬜ Pendiente |
| REG-030 | TENANT | connections | `[DIRECTA]` | Activar/desactivar channels en bulk | Lista de Apps con múltiples connections | Login > Sidebar: Connections > Seleccionar múltiples apps > Acción bulk "Enable"/"Disable" > Verificar estados | Todas las apps seleccionadas cambian su estado en una sola acción (IONF-642) | 🟡 Medio | ⬜ Pendiente |
| REG-031 | TENANT | data-store | `[DIRECTA]` | Crear Data Store y Data Structure | Usuario con permiso READ_DATA_STORE | Login > Sidebar: Data Store > Clic en "New Data Store" > Definir nombre y estructura > Guardar | El Data Store se crea con su estructura. El modal no conserva datos anteriores (IONF-159) | 🟠 Alto | ⬜ Pendiente |
| REG-032 | TENANT | data-store | `[DIRECTA]` | Nodo Persistent Data Save + Get en un flow | Flow con nodos Store Add y Store Get configurados | Login > Sidebar: Boards > Ejecutar flow: nodo Add guarda registro > nodo Get recupera el mismo registro | El registro es guardado y recuperado correctamente, sin solapamiento de datos (IONF-162) | 🔴 Crítico | ⬜ Pendiente |
| REG-033 | TENANT | data-store | `[DIRECTA]` | Visualización de datos del Data Store | Data Store con registros guardados | Login > Sidebar: Data Store > Seleccionar Data Store > Clic en "View Data" | Los datos se muestran sin solapamientos ni datos de otras sesiones (IONF-163) | 🟠 Alto | ⬜ Pendiente |
| REG-034 | TENANT | data-store | `[DIRECTA]` | 8 nodos de Data Storage disponibles en el canvas | Canvas abierto | Login > Sidebar: Boards > Abrir flow > Canvas: panel de nodos > Buscar "Persistent Data" > Verificar los 8 tipos | Los 8 nodos (Save, Update, Get, Delete, Check, Count, Delete All, Search) están en el canvas (IONF-552) | 🟠 Alto | ⬜ Pendiente |
| REG-035 | TENANT | webhooks | `[DIRECTA]` | Webhook trigger inicia flow correctamente | Flow con trigger Webhook activo | Login > Sidebar: Webhooks > Copiar URL > Enviar HTTP POST con payload JSON > Revisar historial | El flow se dispara con el payload recibido, sin errores de content-type (IONF-786) | 🔴 Crítico | ⬜ Pendiente |
| REG-036 | TENANT | webhooks | `[DIRECTA]` | Nodo Webhook Response retorna body configurado | Flow con nodo Webhook Response | Login > Sidebar: Boards > Abrir flow con nodo Webhook Response > Configurar body y status code > Ejecutar via webhook > Verificar respuesta HTTP | El response retorna el body y status code configurados correctamente (IONF-449) | 🟠 Alto | ⬜ Pendiente |
| REG-037 | TENANT | webhooks | `[DIRECTA]` | GRAPP soporta webhooks correctamente | GRAPP instalado con webhook configurado | Admin > Apps > GRAPP > Webhooks > Configurar > Activar > Enviar evento externo | El webhook del GRAPP se activa y el flow asociado ejecuta (IONF-695) | 🟠 Alto | ⬜ Pendiente |
| REG-038 | TENANT | canvas | `[DIRECTA]` | Canvas sin doble scroll ni desborde de componentes | Flow con múltiples nodos | Login > Sidebar: Boards > Abrir flow con 10+ nodos > Scrollear canvas horizontal y verticalmente | Un único scroll, sin desborde de componentes en los nodos (IONF-509) | 🟡 Medio | ⬜ Pendiente |
| REG-039 | TENANT | canvas | `[DIRECTA]` | Nodo Form muestra nested elements y advance fields | Flow con nodo Form con campos anidados | Login > Sidebar: Boards > Abrir flow > Canvas: clic en nodo Form > Drawer: verificar campos anidados y advanced fields | Los campos anidados y avanzados se renderizan correctamente (IONF-313) | 🟡 Medio | ⬜ Pendiente |
| REG-040 | TENANT | canvas | `[DIRECTA]` | Confirmación de cambios no guardados al salir | Flow con cambios sin guardar | Login > Sidebar: Boards > Abrir flow > Canvas: modificar nodo sin guardar > Intentar navegar a otra sección | Aparece modal de confirmación antes de salir (IONF-147) | 🟡 Medio | ⬜ Pendiente |
| REG-041 | TENANT | canvas | `[DIRECTA]` | Modales de confirmación para eliminación | Flow, connector o data store existente | Login > Sidebar: [Módulo] > Acción "Delete" | Aparece modal de confirmación. Los colores del modal son correctos, no invertidos (IONF-281) | 🟡 Medio | ⬜ Pendiente |
| REG-042 | TENANT | canvas | `[DIRECTA]` | IDs de nodos se reinician correctamente | Flow con nodos eliminados y nuevos | Login > Sidebar: Boards > Abrir flow > Canvas: 3 nodos > eliminar el 2do > agregar uno nuevo | Secuencia de IDs consistente, sin saltos incorrectos (IONF-512) | 🟡 Medio | ⬜ Pendiente |
| REG-043 | ADMIN | admin | `[DIRECTA]` | Vista de configuración de Company disponible | Company existente | Login Admin > Admin: Companies > Seleccionar company > Ver configuración | La vista carga y permite editar configuración de la company (IONF-506) | 🟡 Medio | ⬜ Pendiente |
| REG-044 | ADMIN | admin | `[DIRECTA]` | Seeders de apps están disponibles en catálogo | Entorno dev/preproducción | Admin Gateway > Apps > Verificar apps seedeadas | Las apps seedeadas aparecen sin necesidad de crearlas manualmente (IONF-507) | 🟡 Medio | ⬜ Pendiente |
| REG-045 | TENANT | executions | `[DIRECTA]` | Metadata `waiting_for_input` ausente en ejecuciones normales | Flow ejecutado sin input adicional | Login > Sidebar: Executions > Abrir detalle > Revisar JSON | El JSON no contiene `waiting_for_input` en ejecuciones normales (IONF-518) | 🟡 Medio | ⬜ Pendiente |
| REG-046 | TENANT | core-engine / Nodes | `[INDIRECTA]` | Preview de Transformer no conserva datos de otros nodos | Flow con 2+ nodos Transformer | Login > Sidebar: Boards > Abrir flow > Canvas: clic en Transformer A (ver preview) > clic en Transformer B (ver preview) | Cada preview muestra exclusivamente su propia configuración (IONF-511) | 🔴 Crítico | ⬜ Pendiente |
| REG-047 | TENANT | boards | `[INDIRECTA]` | Flow complejo end-to-end: Trigger > Transformer > Switch > Store | Flow con nodos encadenados | Login > Sidebar: Boards > Ejecutar flow complejo > Verificar que todos los nodos ejecutan en secuencia | El flow completo ejecuta de principio a fin registrando resultado de cada nodo (cross: IONF-379, IONF-406) | 🔴 Crítico | ⬜ Pendiente |
| REG-048 | TENANT | executions | `[INDIRECTA]` | Historial registra correctamente flujo complejo | Flow ejecutado con éxito | Login > Sidebar: Executions > Verificar ejecución reciente > Abrir detalle | Todos los nodos aparecen con su status y resultado (cross: IONF-379, IONF-935) | 🟠 Alto | ⬜ Pendiente |
| REG-049 | TENANT | executions | `[INDIRECTA]` | Ejecución falla correctamente cuando nodo falla | Flow con nodo Store con UUID inválido | Login > Sidebar: Boards > Ejecutar flow con Store UUID inválido > Revisar historial | Historial muestra `error`, nodo fallido identificado, edge de error activado | 🟠 Alto | ⬜ Pendiente |
| REG-050 | TENANT | connections | `[INDIRECTA]` | Nodo de App Connector en canvas ejecuta correctamente | Flow con nodo de connector activo (ej. Shopify) | Login > Sidebar: Boards > Abrir flow con nodo de app connector > Ejecutar > Verificar respuesta de API externa | El nodo ejecuta la llamada a la API externa exitosamente (cross: IONF-141, IONF-142) | 🔴 Crítico | ⬜ Pendiente |
| REG-051 | TENANT | connections | `[INDIRECTA]` | Token OAuth se refresca automáticamente en ejecución | Flow con nodo de app connector OAuth con token por expirar | Login > Boards > Token por expirar > Ejecutar flow con nodo OAuth > Verificar resultado | Token refrescado automáticamente sin interrumpir ejecución (cross: IONF-165, IONF-554) | 🟠 Alto | ⬜ Pendiente |
| REG-052 | TENANT | connections | `[INDIRECTA]` | Módulos de connector se listan sin errores de paginación | App Connector con múltiples módulos | Login > Sidebar: Connections > Seleccionar connector > Ver módulos/acciones | Los módulos se listan con filtros y paginación funcionales (cross: IONF-368) | 🟡 Medio | ⬜ Pendiente |
| REG-053 | TENANT | webhooks | `[INDIRECTA]` | Webhook de connector trigger inicia flow | Connector con webhook configurado y flow activo | Login > Sidebar: Connections > Connector > Webhooks > Copiar URL > Enviar evento externo | El evento activa el flow via webhook del connector (cross: IONF-449, IONF-695) | 🟠 Alto | ⬜ Pendiente |
| REG-054 | TENANT | webhooks | `[INDIRECTA]` | Lista de webhooks muestra URLs correctas | Tenant con múltiples webhooks activos | Login > Sidebar: Webhooks > Ver lista | Webhooks con URLs correctas, estados y sin duplicados (cross: IONF-449) | 🟡 Medio | ⬜ Pendiente |
| REG-055 | TENANT | data-store | `[INDIRECTA]` | Nodo Persistent Data Search retorna con filtros | Data Store con múltiples registros, nodo Store Search configurado | Login > Boards > Flow con nodo Persistent Data Search > Configurar filtro > Ejecutar | Solo retorna registros que coinciden con el filtro (cross: IONF-163, IONF-552) | 🟠 Alto | ⬜ Pendiente |
| REG-056 | TENANT | data-store | `[INDIRECTA]` | Data Store aislado entre companies (multi-tenant) | Dos companies con Data Stores separados | Login company A > Crear registro > Login company B > Verificar que Data Store B no tiene datos de A | Aislamiento multi-tenant funciona correctamente (cross: IONF-379) | 🔴 Crítico | ⬜ Pendiente |
| REG-057 | TENANT | boards | `[INDIRECTA]` | Flow con webhook trigger completa ejecución | Flow con Webhook trigger activo | Enviar POST al webhook URL > Login > Sidebar: Executions > Verificar ejecución | Flow en historial con status `completed` y resultado correcto (cross: IONF-786, IONF-449) | 🔴 Crítico | ⬜ Pendiente |
| REG-058 | TENANT | boards | `[INDIRECTA]` | Flow con nodos Data Store no corrompe datos | Flow con nodos Persistent Data Save + Update en secuencia | Login > Boards > Ejecutar flow > Sidebar: Data Store > Verificar registro | Registro tiene el valor final esperado, sin solapamiento (cross: IONF-162) | 🔴 Crítico | ⬜ Pendiente |
| REG-059 | ADMIN GATEWAY | admin | `[INDIRECTA]` | Marketplace de GRAPPs disponible | GRAPPs configurados en Admin Gateway | Admin Gateway > Apps > Ver lista de GRAPPs > Instalar en company de prueba | GRAPPs listados e instalables en companies (cross: IONF-103, IONF-533) | 🟠 Alto | ⬜ Pendiente |
| REG-060 | ADMIN | admin | `[INDIRECTA]` | Vista Admin sin scrolls múltiples | Admin con múltiples apps listadas | Login Admin > Admin: Apps > Scrollear > Admin: Developers > Scrollear | Un solo scroll por vista, sin múltiples scrollbars (IONF-711) | 🟡 Medio | ⬜ Pendiente |
| REG-061 | ADMIN | admin | `[INDIRECTA]` | Actualizar permisos de usuario en company | Usuario existente en company | Admin > Companies > Company > Users > Usuario > Modificar permisos > Guardar | Permisos actualizados y aplicados en el próximo login (cross: IONF-763, IONF-764) | 🟠 Alto | ⬜ Pendiente |
| REG-062 | TENANT | executions | `[INDIRECTA]` | Detalle de ejecución muestra logs completos | Ejecución de flow con logs generados | Login > Sidebar: Executions > Seleccionar ejecución > Ver logs de cada nodo | Logs con detalles (info, warning, error) completos (cross: IONF-798) | 🟡 Medio | ⬜ Pendiente |
| REG-063 | TENANT | executions | `[INDIRECTA]` | Historial filtra por flow específico | Múltiples flows ejecutados | Login > Sidebar: Executions > Filtrar por flow > Verificar resultados | Solo aparecen ejecuciones del flow seleccionado | 🟡 Medio | ⬜ Pendiente |
| REG-064 | TENANT | auth | `[INDIRECTA]` | Acceso sin permiso READ_BOARD retorna 403 | Usuario sin permiso READ_BOARD | Login sin READ_BOARD > Intentar acceder a /workflows | Sistema retorna 403 o redirige a `/forbidden` (cross: IONF-114) | 🔴 Crítico | ⬜ Pendiente |
| REG-065 | TENANT | auth | `[INDIRECTA]` | Logout destruye la sesión correctamente | Usuario logueado | Login > Navegar por la app > Perfil > Logout > Intentar acceder sin login | Usuario deslogueado, token invalidado, acceso denegado sin nuevo login (cross: IONF-362) | 🔴 Crítico | ⬜ Pendiente |
| REG-066 | TENANT | core-engine / Nodes | `[INDIRECTA]` | Nodo Simple Decision rutea por `then` y `false` | Flow con nodo Simple Decision configurado | Login > Boards > Flow con nodo Condition > Campo `status` is_equal "active" > Ejecutar "active" > Verificar then > Ejecutar "inactive" > Verificar false | Ruteo correcto para ambos valores (cross: IONF-379) | 🔴 Crítico | ⬜ Pendiente |
| REG-067 | TENANT | core-engine / Nodes | `[INDIRECTA]` | Iterator procesa cada elemento individualmente | Flow con nodo Iterator configurado | Login > Boards > Flow con Iterator > Input: array 5 elementos > Ejecutar > Verificar 5 ejecuciones del nodo downstream | Iterator emite cada item como output separado (cross: IONF-404) | 🔴 Crítico | ⬜ Pendiente |
| REG-068 | TENANT | boards | `[INDIRECTA]` | Flow de una company no visible para otra | Dos companies con flows propios | Login company A > Boards > Lista > Login company B > Boards > Lista | Cada company solo ve sus propios flows. Sin filtraciones cross-tenant | 🔴 Crítico | ⬜ Pendiente |
| REG-069 | KC | auth | `[BASELINE]` | Login con credenciales válidas | Usuario registrado en Keycloak | Navegar a `/login` > Clic en "Login with SSO" > Keycloak: email y password válidos > Callback > Seleccionar company | Usuario accede correctamente. Sesión iniciada y token JWT válido | 🔴 Crítico | ⬜ Pendiente |
| REG-070 | KC | auth | `[BASELINE]` | Login con credenciales inválidas retorna error | Credenciales incorrectas | Navegar a `/login` > "Login with SSO" > Keycloak: password incorrecto | Keycloak retorna error. La app no permite acceso | 🔴 Crítico | ⬜ Pendiente |
| REG-071 | TENANT | boards | `[BASELINE]` | Agregar y conectar nodos en el canvas | Flow vacío en el canvas | Login > Sidebar: Boards > Abrir flow vacío > Canvas: agregar nodo Transformer > agregar nodo Condition > Conectar por edge output→input | Nodos en canvas, conectados con edge, conexión persistida al guardar | 🔴 Crítico | ⬜ Pendiente |
| REG-072 | TENANT | boards | `[BASELINE]` | Eliminar un nodo del canvas | Flow con al menos 2 nodos | Login > Sidebar: Boards > Abrir flow > Canvas: clic derecho en nodo > Delete > Guardar | Nodo eliminado, edges conectados desaparecen, demás nodos persisten | 🔴 Crítico | ⬜ Pendiente |
| REG-073 | TENANT | executions | `[BASELINE]` | Historial de ejecuciones lista correctamente | Tenant con flows ejecutados | Login > Sidebar: Executions > Ver lista | Lista carga con flow name, status y fecha. Paginación funcional | 🟠 Alto | ⬜ Pendiente |
| REG-074 | TENANT | executions | `[BASELINE]` | Detalle de ejecución disponible | Ejecución completada | Login > Sidebar: Executions > Clic en ejecución > Ver detalle | Detalle con status de cada nodo, resultado y logs | 🟠 Alto | ⬜ Pendiente |
| REG-075 | TENANT | connections | `[BASELINE]` | Lista de connections carga correctamente | Tenant con connections configuradas | Login > Sidebar: Connections > Ver lista | Lista carga con connectors, filtros y paginación funcionales | 🟠 Alto | ⬜ Pendiente |
| REG-076 | TENANT | webhooks | `[BASELINE]` | Lista de webhooks muestra estado | Tenant con webhooks configurados | Login > Sidebar: Webhooks > Ver lista | Webhooks con URL, estado y acciones disponibles | 🟠 Alto | ⬜ Pendiente |
| REG-077 | TENANT | webhooks | `[BASELINE]` | Activar/desactivar webhook | Webhook existente | Login > Sidebar: Webhooks > Seleccionar webhook > Toggle Enable/Disable | Estado del webhook cambia, UI lo refleja sin recargar | 🟠 Alto | ⬜ Pendiente |
| REG-078 | TENANT | pdf-templates | `[BASELINE]` | Crear un template de PDF | Usuario con permisos de templates | Login > Sidebar: Templates (PDF) > "New Template" > Agregar elementos básicos > Guardar | Template creado y disponible en la lista (IONF-820 integró nodo PDF) | 🟠 Alto | ⬜ Pendiente |
| REG-079 | TENANT | pdf-templates | `[BASELINE]` | Editar un template de PDF | Template existente | Login > Sidebar: Templates > Seleccionar template > Editar > Guardar | Cambios guardados y template actualizado accesible | 🟠 Alto | ⬜ Pendiente |
| REG-080 | TENANT | pdf-templates | `[BASELINE]` | Nodo de PDF en canvas genera un archivo PDF | Flow con nodo PDF y template configurado | Login > Boards > Abrir flow con nodo PDF > Ejecutar > Verificar que se genera el PDF | El nodo genera el PDF con el contenido del template (IONF-820) | 🟠 Alto | ⬜ Pendiente |
| REG-081 | ADMIN | billing | `[BASELINE]` | Suscripción activa permite acceso completo | Company con suscripción activa | Login con company activa > Navegar a Boards, Connections, Executions | Todas las secciones accesibles sin restricciones de suscripción | 🟠 Alto | ⬜ Pendiente |
| REG-082 | ADMIN | billing | `[BASELINE]` | Company sin suscripción tiene acceso limitado | Company con suscripción inactiva | Login con company sin suscripción > Intentar funcionalidades premium | Acceso limitado con mensaje de renovación. Funcionalidades premium bloqueadas | 🟠 Alto | ⬜ Pendiente |

---

## Observaciones

### Items del CSV guía actualizados para v1.0.0

| Feature (CSV) | Observación anterior | Actualización v1.0.0 |
|---------------|---------------------|----------------------|
| KC > Login with SSO | "Skipped - No intervienen los webcomponents" | ✅ Ahora INCLUIDO — IONF-362 e IONF-1074 refactorizaron el flujo SSO |
| TENANT > Webhooks | "Skipped - No intervienen los webcomponents" | ✅ Ahora INCLUIDO — IONF-449 e IONF-786 modificaron el nodo webhook |
| TENANT > Executions | "Skipped - No intervienen los webcomponents" | ✅ Ahora INCLUIDO — Motor refactorizado en IONF-379 |
| TENANT > Connections > Create Manual App | "Skipped - No intervienen los webcomponents" | ✅ Ahora INCLUIDO — IONF-116 implementó creación manual |
| ADMIN GATEWAY > Apps > Delete modal (colores invertidos) | "Failed - colores invertidos, así en ion.js" | ⚠️ Verificar si fue corregido en IONF-281 o sigue siendo bug conocido |
| ADMIN GATEWAY > Apps > Settings > Set Image | "Failed - no se puede guardar imagen, así en ion.js" | ⚠️ Sin ticket específico — mantener como bug conocido |
| ADMIN GATEWAY > Apps > Services > Filter by Categories/Type | "Failed - no filtra, así en ion.js" | ⚠️ Sin ticket específico — mantener como bug conocido |
| ADMIN GATEWAY > Apps > Services > Edit > Set Description | "Failed - no se muestra en tabla, así en ion.js" | ⚠️ Sin ticket específico — mantener como bug conocido |

### Módulos con tickets en desarrollo activo (no completados)

- **IONF-260** (Shopify-Shelfter BinLogic) — `ready to merge` — Solo smoke básico
- **IONF-262** (Square-Shelfter) — `ready to merge` — Solo smoke básico
- **IONF-386** (Rithum-Shipedge) — `ready to merge` — Solo smoke básico
- **IONF-575** (Omnio-Ebay flow) — `dev in progress` — Excluir de regresión formal

### Módulos con mayor concentración de tickets críticos
- **core-engine / Nodes** — 12 tickets directos, múltiples fixes de nodos: Transformer (IONF-320, IONF-376, IONF-404, IONF-416, IONF-463, IONF-516), nuevos nodos (IONF-227, IONF-266, IONF-328, IONF-935, IONF-939)
- **auth** — Múltiples cambios de Keycloak (IONF-114, IONF-362, IONF-1074) — alto riesgo de regresión en acceso
- **boards** — Motor de ejecución refactorizado (IONF-379) + versionamiento Git (IONF-419, IONF-482) — riesgo alto

---

## Notas

- CSV guía de referencia: `Test Plan - IONFLOW - Smoke Test.csv`
- Fuente de tickets: `matched_tickets1.csv` (182 tickets reales de ClickUp — Sprints + Deployment)
- Tracking list base: `knowledge/releases/v1.0.0/tracking-list.md`
- L1 de criticidad: `knowledge/L1-project/test-priorities.md`
- L2 consultados: nodes, boards, auth, connections, data-store, webhooks, executions
- Los repos deben actualizarse a DEVELOPMENT antes de ejecutar: `git pull origin DEVELOPMENT`
- La columna Estado se actualiza durante la ejecución (⬜ Pendiente / ✅ Pasó / ❌ Falló / ⏭️ Saltado)

*Generado por ionflow-qa-catalyst — skill: release/regression-matrix*
*Fecha: 2026-06-24*
