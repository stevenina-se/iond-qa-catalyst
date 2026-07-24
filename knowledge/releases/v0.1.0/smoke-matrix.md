# Smoke Test Matrix — v0.1.0 | Validación de Ambiente de Producción

> Generado por `skills/release/smoke-matrix`
> Fecha: 2026-06-30
> Versión: v0.1.0
> Entorno: `app.ionflow.io` (producción)
> Origen: Derivado de la regression-matrix v0.1.0 + 9 flujos críticos de `test-priorities.md`

---

## Resumen

| Métrica | Valor |
|---------|-------|
| Total de casos | 38 |
| Flujos críticos cubiertos | 9/9 |
| TCs de riesgo alto (release) | 22 |
| TCs baseline | 16 |
| Tiempo estimado total | ~55 min |
| Modo sugerido | Playwright MCP / Manual |

### Mapeo de Riesgo por Flujo (v0.1.0)

| Flujo Crítico | ¿Impactado? | Tickets que lo afectan |
|---------------|-------------|------------------------|
| Login / Auth | ✅ Sí | IONF-362, IONF-1074, IONF-543 |
| Crear un flow (Board) | ✅ Sí | IONF-899, IONF-1144 |
| Agregar nodos al canvas | ✅ Sí | IONF-379, IONF-406, IONF-901, IONF-848 |
| Ejecutar un flow | ✅ Sí | IONF-379, IONF-680, IONF-516 |
| Ver historial de ejecuciones | ✅ Sí | IONF-518, IONF-798 |
| Crear conexiones | ✅ Sí | IONF-141, IONF-142, IONF-554 |
| Crear y editar un conector | ✅ Sí | IONF-116, IONF-327 |
| Crear y editar un service (GRAPP/Catalog) | ✅ Sí | IONF-997, IONF-103 |
| Template PDF | ✅ Sí | IONF-820, IONF-1123, IONF-1143 |

> 🔴 Los **9 flujos críticos** fueron impactados en esta versión. Todos los TCs son de Riesgo Alto.

---

## Bloque 1 — Login / Auth (SSO Keycloak)

> **Pregunta clave:** ¿Los usuarios pueden iniciar sesión con SSO?
> Riesgo: 🔴 Alto — IONF-362, IONF-1074, IONF-543 impactaron el módulo de auth

| ID | Caso de Test | Pasos (Breadcrumb) | Resultado Esperado | Riesgo | Prioridad | Estado |
|----|-------------|--------------------|--------------------|--------|-----------|--------|
| SM-001 | Login SSO — Company User | `Navigate: app.ionflow.io` → `Click "Login with SSO"` → `Keycloak: Fill #username: [user]` → `Fill #password: [pass]` → `Click #kc-login` → `Verify: Dashboard visible con nombre de la company` | Dashboard carga. Menú lateral visible. Nombre de la company en header. Sin errores 401/403. | 🔴 Alto | 🔴 | ⬜ |
| SM-002 | Login SSO — Admin Ionflow | `Navigate: app.ionflow.io` → `Login como usuario Admin` → `Verify: Admin sidebar visible (Companies, Templates, Connectors, Boards, Apps, Developers, Settings)` | Panel de Admin carga correctamente. Todas las secciones del sidebar visibles. | 🔴 Alto | 🔴 | ⬜ |
| SM-003 | Acceso sin sesión — Redirección a Login | `Navigate: app.ionflow.io/boards` (sin sesión activa) → `Verify: Redirige a pantalla de login / Keycloak` | No se puede acceder directamente a /boards sin sesión. Redirige a login. | 🔴 Alto | 🔴 | ⬜ |

---

## Bloque 2 — Crear un Flow (Board)

> **Pregunta clave:** ¿Se puede crear y guardar un Board nuevo?
> Riesgo: 🔴 Alto — IONF-899 (URL no se actualiza), IONF-1144 (no se puede crear Board tras nueva cuenta)

| ID | Caso de Test | Pasos (Breadcrumb) | Resultado Esperado | Riesgo | Prioridad | Estado |
|----|-------------|--------------------|--------------------|--------|-----------|--------|
| SM-004 | Crear Board nuevo | `Company Login` → `Sidebar: Boards` → `Button: "+ New Board"` → `Fill nombre: "Smoke Test Board"` → `Click Crear/Save` → `Verify: Board aparece en lista y URL se actualiza` | Board creado exitosamente. URL cambia a la del board creado. Board visible en el listado. | 🔴 Alto | 🔴 | ⬜ |
| SM-005 | Abrir Board existente y verificar canvas | `Company Login` → `Sidebar: Boards` → `Click en cualquier Board existente` → `Verify: Canvas carga sin errores` | Canvas del board carga. Panel de nodos visible a la izquierda. Sin errores 500/502. | 🔴 Alto | 🔴 | ⬜ |
| SM-006 | Eliminar Board | `Company Login` → `Sidebar: Boards` → `Board existente: Click "···" / Delete` → `Confirm: Modal de confirmación` → `Verify: Board eliminado de la lista` | Modal de confirmación aparece. Board eliminado del listado correctamente. | 🟢 Baseline | 🟠 | ⬜ |

---

## Bloque 3 — Agregar Nodos al Canvas

> **Pregunta clave:** ¿El canvas funciona y los nodos se conectan correctamente?
> Riesgo: 🔴 Alto — IONF-379 (motor), IONF-406 (recursividad), IONF-901 (mapeo select/boolean)

| ID | Caso de Test | Pasos (Breadcrumb) | Resultado Esperado | Riesgo | Prioridad | Estado |
|----|-------------|--------------------|--------------------|--------|-----------|--------|
| SM-007 | Agregar nodo Scheduler (Trigger) | `Board abierto` → `Panel de nodos: Drag or Click "Scheduler"` → `Nodo aparece en canvas` → `Click nodo: Configurar frecuencia` → `Click Save` | Nodo Scheduler agregado y configurado. Sin errores al guardar. | 🔴 Alto | 🔴 | ⬜ |
| SM-008 | Agregar nodo HTTP Request y conectar | `Board abierto` → `Agregar nodo "HTTP Request"` → `Conectar salida de Scheduler con entrada de HTTP Request` → `Configurar URL de prueba` → `Click Save` | Conexión entre nodos visible. Configuración guardada. Sin errores. | 🔴 Alto | 🔴 | ⬜ |
| SM-009 | Agregar nodo Mapper y conectar | `Board abierto` → `Agregar nodo "Mapper"` → `Conectar con nodo anterior` → `Verificar que se puede mapear al menos un campo` | Mapper carga con el schema del nodo anterior. Campo mapeado sin errores. | 🔴 Alto | 🔴 | ⬜ |
| SM-010 | Agregar nodo Multiple Decision (Switch) | `Board abierto` → `Panel de nodos: Click "Multiple Decision"` → `Nodo aparece en canvas` → `Configurar al menos 2 salidas` | Nodo Switch visible con múltiples salidas configurables. Sin errores. | 🔴 Alto | 🔴 | ⬜ |
| SM-011 | Menú contextual de doble clic para agregar nodo | `Board abierto con canvas vacío` → `Double click en área vacía del canvas` → `Verify: Menú contextual de nodos aparece` | Menú contextual visible con categorías de nodos. | 🔴 Alto | 🟠 | ⬜ |

---

## Bloque 4 — Ejecutar un Flow

> **Pregunta clave:** ¿La ejecución del flow termina correctamente?
> Riesgo: 🔴 Alto — IONF-379 (motor refactorizado), IONF-516 (Transformer sin output), IONF-680 (schedules)

| ID | Caso de Test | Pasos (Breadcrumb) | Resultado Esperado | Riesgo | Prioridad | Estado |
|----|-------------|--------------------|--------------------|--------|-----------|--------|
| SM-012 | Ejecutar flow en modo Development (manual) | `Board abierto con al menos 1 nodo (ej: HTTP Request)` → `Button: "Run" / Ejecutar` → `Verify: Ejecución inicia, nodo cambia de estado, resultado visible en el panel de salida` | Ejecución completa. Estado del nodo cambia a ✅. Output del nodo visible. Sin errores críticos. | 🔴 Alto | 🔴 | ⬜ |
| SM-013 | Activar flow a modo Production | `Board abierto` → `Toggle: "Development → Production"` → `Verify: Flow pasa a estado Active` → `Verify en Telescope que el job aparece registrado` | Flow activado. Estado visible como "Active" en el listado. Sin errores en Telescope. | 🔴 Alto | 🔴 | ⬜ |
| SM-014 | Ejecutar flow con nodo Transformer y verificar output | `Board con nodo Transformer configurado` → `Run en modo Development` → `Verify: Output del Transformer no es null ni vacío` | Transformer emite output válido. No debe mostrar datos de ejecución anterior. | 🔴 Alto | 🔴 | ⬜ |

---

## Bloque 5 — Historial de Ejecuciones

> **Pregunta clave:** ¿Los logs de ejecución son correctos y visibles?
> Riesgo: 🔴 Alto — IONF-518 (metadata waiting_for_input), IONF-798 (más detalles en logs)

| ID | Caso de Test | Pasos (Breadcrumb) | Resultado Esperado | Riesgo | Prioridad | Estado |
|----|-------------|--------------------|--------------------|--------|-----------|--------|
| SM-015 | Ver historial de ejecuciones | `Company Login` → `Sidebar: Execution History` → `Verify: Lista de ejecuciones visible` → `Click en una ejecución` → `Verify: Detalle de ejecución con logs por nodo` | Historial carga. Al menos una ejecución listada. Logs de cada nodo visibles. Sin errores 500. | 🔴 Alto | 🔴 | ⬜ |
| SM-016 | Verificar que ejecución muestra resultado por nodo | `Execution History` → `Click en ejecución reciente` → `Verify: cada nodo muestra su status (✅/❌) y resultado/output` | Cada nodo del flow tiene su status registrado. Output visible. Sin metadatos `waiting_for_input` expuestos. | 🔴 Alto | 🟠 | ⬜ |

---

## Bloque 6 — Crear Conexiones

> **Pregunta clave:** ¿Es posible crear nuevas conexiones con los diferentes métodos de autenticación?
> Riesgo: 🔴 Alto — IONF-141 (Basic Auth GET), IONF-142 (refactor de connections), IONF-554 (Refresh Token)

| ID | Caso de Test | Pasos (Breadcrumb) | Resultado Esperado | Riesgo | Prioridad | Estado |
|----|-------------|--------------------|--------------------|--------|-----------|--------|
| SM-017 | Crear conexión desde módulo Connections | `Company Login` → `Sidebar: Connections` → `Click "+ Add Connection"` → `Seleccionar app connector disponible` → `Fill credenciales` → `Click Save` → `Verify: Conexión aparece en la lista` | Conexión creada y listada correctamente. Sin errores de autenticación. | 🔴 Alto | 🔴 | ⬜ |
| SM-018 | Verificar estado de conexión existente | `Company Login` → `Sidebar: Connections` → `Click en conexión existente` → `Button: "Check Connection"` → `Verify: Estado "Connected" / OK` | Conexión verificada exitosamente. Sin errores de Basic Auth ni de Refresh Token. | 🔴 Alto | 🔴 | ⬜ |
| SM-019 | Re-autorizar conexión existente | `Company Login` → `Sidebar: Connections` → `Click en conexión` → `Button: "Reauthorize"` → `Verify: Flujo de re-auth completa sin errores` | Flujo de re-autorización completa. Conexión activa. | 🔴 Alto | 🟠 | ⬜ |

---

## Bloque 7 — Crear y Editar Conector

> **Pregunta clave:** ¿Se puede crear y editar un conector nuevo?
> Riesgo: 🔴 Alto — IONF-116 (crear app manual), IONF-327 (módulos mismo nombre)

| ID | Caso de Test | Pasos (Breadcrumb) | Resultado Esperado | Riesgo | Prioridad | Estado |
|----|-------------|--------------------|--------------------|--------|-----------|--------|
| SM-020 | Crear conector manual (App Connector) | `Company Login` → `Sidebar: Connections` → `Click "Create"` → `Seleccionar "Manual Connector"` → `Fill nombre, descripción, tipo` → `Click Save` → `Verify: Conector creado y visible en lista` | Conector creado exitosamente. Visible en el módulo de Connections. | 🔴 Alto | 🔴 | ⬜ |
| SM-021 | Editar nombre de conector existente | `Company Login` → `Sidebar: Connections` → `Click en conector existente` → `Edit nombre` → `Save` → `Verify: nombre actualizado en la lista` | Nombre del conector actualizado. Sin errores al guardar. | 🟢 Baseline | 🟠 | ⬜ |
| SM-022 | Agregar un endpoint (nodo) al conector | `Company Login` → `Sidebar: Connections` → `Click en conector` → `Tab: Nodes` → `Button: "Add Node"` → `Fill nombre y configuración básica` → `Save` | Nodo/endpoint agregado al conector. Visible en la lista de nodos del conector. | 🔴 Alto | 🔴 | ⬜ |

---

## Bloque 8 — Crear y Editar Service / GRAPP (Catalog)

> **Pregunta clave:** ¿Se puede crear y editar un service nuevo?
> Riesgo: 🔴 Alto — IONF-997 (Marketplace/GRAPPs), IONF-103 (endpoints de GRAPP), IONF-917 (Marketplace UI)

| ID | Caso de Test | Pasos (Breadcrumb) | Resultado Esperado | Riesgo | Prioridad | Estado |
|----|-------------|--------------------|--------------------|--------|-----------|--------|
| SM-023 | Acceder al Marketplace de GRAPPs | `Company Login (Customer/Tenant)` → `Sidebar: Available Market Place` → `Verify: Lista de GRAPPs disponibles carga` | Marketplace visible. Al menos un GRAPP listado. Sin errores 500. | 🔴 Alto | 🔴 | ⬜ |
| SM-024 | Instalar un GRAPP desde Marketplace | `Customer Login` → `Sidebar: Available Market Place` → `Click en GRAPP disponible` → `Click "Install"` → `Verify: GRAPP aparece en Configured Channels` | GRAPP instalado. Visible en Configured Channels del cliente. Sin errores en instalación. | 🔴 Alto | 🔴 | ⬜ |
| SM-025 | Crear nuevo GRAPP desde Admin | `Admin Ionflow Login` → `Sidebar: Apps > Grapps` → `Click "+ Create"` → `Fill nombre y configuración básica` → `Save` → `Verify: GRAPP creado en la lista` | GRAPP creado exitosamente. Visible en la lista de Apps > Grapps. | 🔴 Alto | 🟠 | ⬜ |
| SM-026 | Verificar Catalog — Agregar item | `Company Login` → `Sidebar: Catalog` → `Click "+ Add Catalog Item"` → `Seleccionar tipo GRAPP` → `Fill datos básicos` → `Save` → `Verify: Item visible en Catalog` | Item de catálogo creado. Visible en el módulo Catalog. | 🟢 Baseline | 🟡 | ⬜ |

---

## Bloque 9 — Template PDF

> **Pregunta clave:** ¿Se puede crear, editar y utilizar un template de PDF?
> Riesgo: 🔴 Alto — IONF-820 (nodo PDF), IONF-1123 (mapeo no habilitaba), IONF-1143 (FlowPilot + PDF), IONF-958 (menú lateral editor)

| ID | Caso de Test | Pasos (Breadcrumb) | Resultado Esperado | Riesgo | Prioridad | Estado |
|----|-------------|--------------------|--------------------|--------|-----------|--------|
| SM-027 | Crear template PDF nuevo | `Company Login` → `Sidebar: PDF Templates` → `Click "+ New Template"` → `Fill nombre` → `Agregar al menos un campo de texto` → `Save` | Template PDF creado. Visible en la lista de PDF Templates. Sin errores al guardar. | 🔴 Alto | 🔴 | ⬜ |
| SM-028 | Agregar nodo ION PDF al canvas y mapear | `Board abierto` → `Panel de nodos: Click "ION PDF"` → `Nodo aparece en canvas` → `Click nodo: Abrir modal de edición` → `Seleccionar template creado` → `Mapear al menos un campo` → `Click Save (guardar modal)` → `Verify: Mapeo visible y nodo configurado` | Nodo ION PDF configurado. Mapeo de campos habilitado correctamente al abrir el modal. Sin necesidad de abrir/cerrar dos veces. | 🔴 Alto | 🔴 | ⬜ |
| SM-029 | Generar PDF ejecutando flow | `Board con nodo ION PDF configurado` → `Run en modo Development` → `Verify: Output del nodo contiene referencia al PDF generado` → `Verify: PDF descargable / accesible` | PDF generado exitosamente. Link/referencia de descarga disponible en el output. Sin errores de generación. | 🔴 Alto | 🔴 | ⬜ |

---

## TCs Específicos del Release — Bugs Críticos Activos

> Estos TCs validan los bugs urgentes reportados durante el QA de v0.1.0.
> Deben verificarse **antes de activar el tráfico de producción**.

| ID | Ticket Origen | Caso de Test | Pasos (Breadcrumb) | Resultado Esperado | Prioridad | Estado |
|----|--------------|-------------|--------------------|--------------------|-----------|--------|
| SM-R-001 | IONF-1144 | Crear Board después de crear cuenta nueva | `Crear cuenta nueva en Ionflow (SSO)` → `Login con la cuenta nueva` → `Sidebar: Boards` → `Click "+ New Board"` → `Fill nombre` → `Click Crear` → `Verify: Board creado sin errores` | Board creado exitosamente. Sin error "failed to create". | 🔴 | ⬜ |
| SM-R-002 | IONF-1145 | Desactivar webhook custom | `Company Login` → `Sidebar: Webhooks` → `Click en webhook custom activo` → `Toggle: Desactivar` → `Verify: Estado cambia a Inactivo` | Webhook desactivado correctamente. Sin errores. Estado "Inactive" reflejado en lista. | 🔴 | ⬜ |
| SM-R-003 | IONF-1147 | Cambio de email de cuenta — integridad de acceso | `Company Login` → `Sidebar: Account` → `Button: "Change Email"` → `Fill nuevo email válido` → `Confirm` → `Verify: Sesión sigue activa o redirige a re-login correctamente sin romper la cuenta` | Email actualizado. Cuenta accesible con el nuevo email. Sin errores que rompan el acceso. | 🔴 | ⬜ |
| SM-R-004 | IONF-1108 | Migración de flow a global | `Admin Login` → `Companies` → `Seleccionar company` → `Flows: Click "Migrate" en un flow` → `Verify: Flow migrado a global sin error 500` | Flow migrado exitosamente. Sin error 500 "failed to create global flow: invalid field". | 🔴 | ⬜ |
| SM-R-005 | IONF-1123 | Mapeo en nodo PDF sin doble apertura | `Board abierto con nodo ION PDF` → `Click nodo` → `Modal se abre` → `Verify inmediatamente: campos de mapeo son editables sin necesidad de guardar y reabrir` | Mapeo habilitado al primer abrir del modal. Sin necesidad de abrir/guardar/cerrar ciclo extra. | 🔴 | ⬜ |
| SM-R-006 | IONF-1143 | FlowPilot reconoce nodo PDF Template | `Board abierto con nodo ION PDF configurado` → `Abrir FlowPilot (agente IA)` → `Pedir al agente que agregue o modifique el nodo PDF Template` → `Verify: El agente reconoce el nodo PDF sin errores` | FlowPilot reconoce el nodo ION PDF correctamente. Sin errores al interactuar. | 🔴 | ⬜ |

---

## TCs Complementarios — Módulos de Alto Riesgo

> Validaciones rápidas adicionales para módulos críticos impactados en v0.1.0.

| ID | Módulo | Caso de Test | Pasos (Breadcrumb) | Resultado Esperado | Prioridad | Estado |
|----|--------|-------------|--------------------|--------------------|-----------|--------|
| SM-C-001 | Data Store | Crear y leer un Data Store | `Company Login` → `Sidebar: Data Store` → `Create` → `Fill nombre y estructura` → `Save` → `Verify: Data Store en lista` → `Abrir: Ver view de datos` | Data Store creado. Vista de datos accesible. Sin solapamiento de datos de sesión anterior. | 🔴 | ⬜ |
| SM-C-002 | Webhooks | Activar/Desactivar webhook | `Company Login` → `Sidebar: Webhooks` → `Toggle Active en un webhook existente` → `Toggle nuevamente a Inactive` → `Verify: Estado refleja cambio en ambas direcciones` | Webhook cambia de Active a Inactive y viceversa sin errores. | 🔴 | ⬜ |
| SM-C-003 | Teams / Permisos | Invitar miembro a la company | `Company Login` → `Sidebar: Teams` → `Click "Invite Member"` → `Fill email del invitado` → `Asignar rol` → `Send` → `Verify: Invitación aparece en lista de invitaciones pendientes` | Invitación enviada. Visible en lista de Teams. Sin errores. | 🟠 | ⬜ |
| SM-C-004 | Gateway Admin — Customer Login | Instalar GRAPP desde Gateway | `Admin Gateway Login` → `Customer: Configured Channels` → `Verify: GRAPPs instalados visibles` → `Click en GRAPP instalado` → `Verify: Historial de ejecuciones del GRAPP disponible` | GRAPPs del Customer visibles. Ejecuciones registradas. Sin errores. | 🔴 | ⬜ |
| SM-C-005 | Credentials | Agregar credencial LLM | `Company Login` → `Sidebar: Credentials` → `Button: "Add"` → `Seleccionar Provider (ej: OpenAI)` → `Fill API Key` → `Seleccionar Model` → `Save` → `Verify: Credencial en lista` | Credencial guardada. Sin errores. Visible en el listado. | 🟠 | ⬜ |
| SM-C-006 | FlowPilot (IonMind) | Abrir FlowPilot y hacer consulta básica | `Board abierto` → `Abrir Flow Pilot (botón/chat)` → `Escribir: "Add a Scheduler node"` → `Verify: Agente responde y ejecuta acción en el canvas` | FlowPilot responde. Acción ejecutada en el canvas. Sin errores ni pantalla en blanco. | 🔴 | ⬜ |

---

## Modo de Ejecución Sugerido

| Modo | Recomendación | Razón |
|------|--------------|-------|
| **Playwright MCP** | ✅ Recomendado | Velocidad + screenshots automáticos como evidencia de go-live |
| Manual | ⬜ Alternativa | Para TCs que requieren interacción específica (FlowPilot, PDF download) |

---

## Leyendas

### Riesgo
- `🔴 Alto` — Módulo impactado directamente por v0.1.0
- `🟢 Baseline` — Módulo no tocado directamente, validación de no-regresión

### Prioridad
- 🔴 Crítico — Testear siempre antes del go-live
- 🟠 Alto — Testear siempre
- 🟡 Medio — Testear si hay tiempo

### Estado
- ⬜ Pendiente
- ✅ Pasó
- ❌ Falló
- ⏭️ Saltado (con justificación)

---

## Criterio de Aprobación del Smoke

> El smoke se considera **APROBADO** y se puede activar el tráfico de producción si:

- ✅ **100%** de los TCs `SM-001` a `SM-029` con estado PASS o Saltado justificado
- ✅ **100%** de los TCs `SM-R-001` a `SM-R-006` (bugs críticos activos) con estado PASS
- ✅ Cero TCs en estado FAIL con prioridad 🔴
- ⚠️ Si algún TC 🔴 falla → **NO activar tráfico**. Escalar inmediatamente y evaluar si se hace rollback.

---

*Generado por ionflow-qa-catalyst — skill: release/smoke-matrix*
*Fecha: 2026-06-30 | Versión: v0.1.0*
