# Regression Matrix — v0.1.1

> Generado por `skills/release/regression-matrix`
> Fecha: 2026-07-20
> Versión: **v0.1.1** (Regression fixes v0.1.0 + features Sprint 4)
> Formato: Template aprobado `templates/release-regression-matrix.md`
> Fuente de tickets: `get_tickets_deployment_4.csv` (16 tickets — ready to merge)
> Herencia: `knowledge/releases/v0.1.0/regression-matrix.md`

---

## Resumen

| Métrica | Valor |
|---------|-------|
| Versión | v0.1.1 |
| Total de casos | 49 |
| Regresión directa | 28 |
| Regresión indirecta | 9 |
| Baseline | 12 |
| Módulos cubiertos | 15 |
| Módulos afectados por release | 10 |
| Sides cubiertos | KC, ADMIN, TENANT, ADMIN GATEWAY |
| Tickets referenciados | 16 tickets del release |
| Items Skipped (pendientes 1.4.x) | 23 (heredados de v0.1.0) |

---

## Cobertura por Módulo

| Módulo | Criticidad (L1) | Directos | Indirectos | Baseline | Total |
|--------|-----------------|---------|-----------|---------|-------|
| Boards (Scheduler) | 🔴 Crítico | 4 | 1 | 0 | 5 |
| Boards (Nodes/Simple Decision) | 🔴 Crítico | 3 | 1 | 0 | 4 |
| Boards (Commit/Git) | 🔴 Crítico | 2 | 0 | 0 | 2 |
| Boards (Flow Pilot) | 🔴 Crítico | 2 | 1 | 0 | 3 |
| PDF Templates | 🟠 Alto | 4 | 1 | 0 | 5 |
| Connections (Integrations) | 🟠 Alto | 2 | 1 | 0 | 3 |
| Webhooks | 🟠 Alto | 2 | 1 | 0 | 3 |
| Executions | 🟠 Alto | 2 | 1 | 0 | 3 |
| Auth (Registration) | 🟠 Alto | 2 | 0 | 1 | 3 |
| Billing/Scraping | 🟠 Alto | 2 | 0 | 0 | 2 |
| Dashboard/UI | 🟡 Medio | 1 | 0 | 0 | 1 |
| Gateway Services | 🟠 Alto | 2 | 1 | 0 | 3 |
| Boards (core flow) | 🔴 Crítico | 0 | 0 | 4 | 4 |
| Connections (App Connectors) | 🟠 Alto | 0 | 0 | 2 | 2 |
| Data Store | 🟠 Alto | 0 | 0 | 1 | 1 |
| Accounts/Dev Apps | 🟠 Alto | 0 | 0 | 1 | 1 |
| Canvas (Vue Flow) | 🟡 Medio | 0 | 1 | 0 | 1 |
| Credentials | 🟠 Alto | 0 | 0 | 1 | 1 |
| PDF Templates (from canvas) | 🟠 Alto | 0 | 0 | 1 | 1 |
| Settings/Teams | 🟡 Medio | 0 | 0 | 1 | 1 |

---

## Regression Matrix

### Formato de Pasos (OBLIGATORIO)

> Los pasos usan formato **breadcrumb** explícito.
> Formato: `[Rol] Login > Sidebar: [Módulo] > [Acción] > [Sub-acción] > [Verificación]`

### Leyenda de Tipo de Regresión
- `[DIRECTA]` — Módulo cambiado directamente por un ticket del release
- `[INDIRECTA]` — Módulo posiblemente impactado por cross-impact
- `[BASELINE]` — Control de que el core del producto no se rompió

### Leyenda de Prioridad
- 🔴 Crítico — Testear siempre, bloqueante si falla
- 🟠 Alto — Testear siempre, puede ser bloqueante
- 🟡 Medio — Testear si hay tiempo
- 🟢 Bajo — Nice to have

### Leyenda de Estado
- ⬜ Pendiente
- ✅ Pasó
- ❌ Falló
- ⏭️ Saltado (con justificación)

---

### REGRESIÓN DIRECTA — Boards / Scheduler (IONF-1127, IONF-1007, IONF-1168)

| ID | Side | Módulo | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Estado |
|----|------|--------|------|-------------|--------------|-------|-------------------|-----------|--------|
| REG-001 | TENANT | Boards > Scheduler | `[DIRECTA]` | Scheduler ejecuta flow → status "completed" | Flow con Scheduler activo en Production | [Tenant] Login > Sidebar: Boards > Abrir board con Scheduler > Activar Production > Esperar ejecución programada > Verificar Execution History | El flow ejecuta y el status final es "completed", NO "error" | 🔴 | ⬜ |
| REG-002 | TENANT | Boards > Scheduler | `[DIRECTA]` | Logs de Company Schedules sin desfase +4h | Flow con Scheduler activo ejecutado | [Tenant] Login > Sidebar: Boards > Board con Scheduler > Execution History > Verificar timestamp de logs | La hora mostrada en los logs coincide con la hora real de ejecución (sin offset de +4 horas) | 🔴 | ⬜ |
| REG-003 | TENANT | Boards > Scheduler | `[DIRECTA]` | Scheduler cron ejecuta en hora correcta UTC/Local | Flow con Scheduler configurado con hora específica | [Tenant] Login > Sidebar: Boards > Editar board > Configurar Scheduler cron a hora específica > Activar Production > Esperar trigger > Verificar hora de ejecución | La ejecución se dispara en la hora configurada respetando la zona horaria del usuario | 🔴 | ⬜ |
| REG-004 | TENANT | Boards > Scheduler | `[DIRECTA]` | Scheduler funciona en modo Test y Producción | Flow con Scheduler configurado | [Tenant] Login > Sidebar: Boards > Board con Scheduler > Ejecutar en modo Test > Verificar resultado > Activar Production > Verificar ejecución automática | Ambos modos ejecutan correctamente: Test (manual) y Production (automático) | 🔴 | ⬜ |

### REGRESIÓN DIRECTA — Boards / Simple Decision (IONF-1128)

| ID | Side | Módulo | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Estado |
|----|------|--------|------|-------------|--------------|-------|-------------------|-----------|--------|
| REG-005 | TENANT | Boards > Simple Decision | `[DIRECTA]` | Simple Decision compara valores numéricos correctamente | Flow con nodo Simple Decision | [Tenant] Login > Sidebar: Boards > Crear/editar board > Agregar Simple Decision > Configurar condición numérica (ej: valor > 100) > Ejecutar en Test con input numérico | La comparación se realiza como números (42 < 100 = true), NO como strings ("42" > "100") | 🔴 | ⬜ |
| REG-006 | TENANT | Boards > Simple Decision | `[DIRECTA]` | Simple Decision con valores string sigue funcionando | Flow con nodo Simple Decision | [Tenant] Login > Sidebar: Boards > Board con Simple Decision > Configurar condición con strings > Ejecutar en Test | Las comparaciones de strings funcionan correctamente (equals, contains, etc.) | 🔴 | ⬜ |
| REG-007 | TENANT | Boards > Simple Decision | `[DIRECTA]` | Simple Decision edge case: valor "0" vs 0 | Flow con Simple Decision comparando cero | [Tenant] Login > Sidebar: Boards > Board con Simple Decision > Configurar condición: valor == 0 > Enviar "0" como input > Ejecutar | La comparación de "0" con 0 es correcta y toma la rama esperada | 🟠 | ⬜ |

### REGRESIÓN DIRECTA — Boards / Commit (IONF-1121)

| ID | Side | Módulo | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Estado |
|----|------|--------|------|-------------|--------------|-------|-------------------|-----------|--------|
| REG-008 | TENANT | Boards > Commit | `[DIRECTA]` | Post-commit: re-ingresar sin false unsaved alert | Board con commit exitoso reciente | [Tenant] Login > Sidebar: Boards > Abrir board con commit exitoso > Salir > Re-ingresar al mismo board > Verificar UI | Al re-ingresar, NO se muestra alerta de "cambios sin guardar" si no hubo cambios | 🟠 | ⬜ |
| REG-009 | TENANT | Boards > Commit | `[DIRECTA]` | Save + Commit → no alerta falsa | Board con cambios pendientes | [Tenant] Login > Sidebar: Boards > Editar board > Hacer cambios > Save > Commit > Verificar que no aparece alerta falsa | Después de Save + Commit exitoso, la vista queda limpia sin alertas de unsaved changes | 🟠 | ⬜ |

### REGRESIÓN DIRECTA — PDF Templates (IONF-1126, IONF-1116)

| ID | Side | Módulo | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Estado |
|----|------|--------|------|-------------|--------------|-------|-------------------|-----------|--------|
| REG-010 | TENANT | PDF Templates | `[DIRECTA]` | Escape con cambios sin guardar → confirmación | Template con cambios no guardados | [Tenant] Login > Sidebar: PDF Templates > Abrir template > Hacer cambios > Presionar Escape | Se muestra modal de confirmación: "¿Descartar cambios?" antes de cerrar. Los cambios NO se pierden silenciosamente | 🔴 | ⬜ |
| REG-011 | TENANT | PDF Templates | `[DIRECTA]` | Cerrar modal sin guardar → confirmación | Template abierto con ediciones | [Tenant] Login > Sidebar: PDF Templates > Abrir template > Hacer cambios > Click fuera del modal o botón cerrar | Se muestra confirmación antes de cerrar. Si el usuario cancela, permanece en la edición | 🔴 | ⬜ |
| REG-012 | TENANT | PDF Templates | `[DIRECTA]` | Load Base PDF grande → error controlado, sin crash | Archivo PDF > límite configurado | [Tenant] Login > Sidebar: PDF Templates > Nuevo template > Load Base PDF > Seleccionar archivo grande (>límite) | La vista NO crashea. Se muestra mensaje de error claro indicando el límite de tamaño | 🔴 | ⬜ |
| REG-013 | TENANT | PDF Templates | `[DIRECTA]` | Load Base PDF dentro de límite → funciona | Archivo PDF dentro del límite | [Tenant] Login > Sidebar: PDF Templates > Nuevo template > Load Base PDF > Seleccionar archivo válido | El PDF se carga correctamente y se puede editar el template | 🟠 | ⬜ |

### REGRESIÓN DIRECTA — Connections / Integrations (IONF-1114)

| ID | Side | Módulo | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Estado |
|----|------|--------|------|-------------|--------------|-------|-------------------|-----------|--------|
| REG-014 | TENANT | Connections (Integrations) | `[DIRECTA]` | Reauthorize API Key → sobrescribe, NO duplica | Conexión existente con API Key | [Tenant] Login > Sidebar: Connections (Integrations) > Seleccionar conexión API Key > Reauthorize > Ingresar nueva API Key > Guardar | La conexión se actualiza con la nueva key. NO se crea una segunda conexión duplicada | 🔴 | ⬜ |
| REG-015 | TENANT | Connections (Integrations) | `[DIRECTA]` | Verificar conexión única post-reauthorize | Conexión reauthorized con API Key | [Tenant] Login > Sidebar: Connections (Integrations) > Verificar lista de conexiones para el mismo connector | Solo existe UNA conexión activa para ese connector (la reauthorizada), no dos | 🔴 | ⬜ |

### REGRESIÓN DIRECTA — Webhooks (IONF-1169)

| ID | Side | Módulo | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Estado |
|----|------|--------|------|-------------|--------------|-------|-------------------|-----------|--------|
| REG-016 | TENANT | Webhooks | `[DIRECTA]` | Rutas públicas de webhooks accesibles sin CORS | Flow con webhook trigger en Production | Enviar POST request desde origen externo a la URL del webhook público | La request es aceptada sin error CORS. El flow se dispara correctamente | 🔴 | ⬜ |
| REG-017 | TENANT | Webhooks | `[DIRECTA]` | Webhook trigger externo ejecuta flow completo | Flow con webhook trigger activo | Enviar POST con payload válido a webhook URL > Verificar Execution History | El flow se ejecuta completamente. El resultado aparece en el historial de ejecuciones | 🔴 | ⬜ |

### REGRESIÓN DIRECTA — Execution History (IONF-1168, IONF-1049)

| ID | Side | Módulo | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Estado |
|----|------|--------|------|-------------|--------------|-------|-------------------|-----------|--------|
| REG-018 | TENANT | Execution History | `[DIRECTA]` | Logs de ejecución con hora correcta | Al menos una ejecución completada | [Tenant] Login > Sidebar: Execution History > Abrir detalle de ejecución reciente > Verificar timestamps | Los timestamps de los logs son correctos (sin desfase de +4 horas respecto a la hora real) | 🔴 | ⬜ |
| REG-019 | TENANT | Execution History | `[DIRECTA]` | Logs sincronizados con R2 | Ejecuciones completadas | [Tenant] Login > Sidebar: Execution History > Verificar que los logs persisten después de tiempo | Los logs de ejecución están disponibles y sincronizados con R2 storage | 🟠 | ⬜ |

### REGRESIÓN DIRECTA — Auth / Registration (IONF-1075)

| ID | Side | Módulo | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Estado |
|----|------|--------|------|-------------|--------------|-------|-------------------|-----------|--------|
| REG-020 | KC | Auth (Registration) | `[DIRECTA]` | Registro de compañía con formulario refactorizado | Usuario no registrado | Navegar a Sign Up > Completar formulario de registro de compañía con datos válidos > Submit | El registro se completa exitosamente. Se crea la compañía y el usuario | 🟠 | ⬜ |
| REG-021 | KC | Auth (Registration) | `[DIRECTA]` | Flujo post-registro redirección correcta | Registro recién completado | Completar registro > Verificar redirección post-registro | El usuario es redirigido correctamente a la selección de company o dashboard | 🟠 | ⬜ |

### REGRESIÓN DIRECTA — Dashboard/UI (IONF-1030)

| ID | Side | Módulo | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Estado |
|----|------|--------|------|-------------|--------------|-------|-------------------|-----------|--------|
| REG-022 | TENANT | Dashboard | `[DIRECTA]` | Interface dualtrack mejoras visuales | Usuario autenticado | [Tenant] Login > Dashboard > Verificar mejoras de interface en la vista dualtrack | Las mejoras visuales se aplican correctamente. La interface es funcional y sin errores visuales | 🟡 | ⬜ |

### REGRESIÓN DIRECTA — Boards / Flow Pilot (IONF-1020)

| ID | Side | Módulo | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Estado |
|----|------|--------|------|-------------|--------------|-------|-------------------|-----------|--------|
| REG-023 | TENANT | Boards > Flow Pilot | `[DIRECTA]` | Monitoreo de tokens por usuario | Flow con nodo Code y FlowPilot activo, credenciales LLM configuradas | [Tenant] Login > Sidebar: Boards > Abrir board > Nodo Code > Ask FlowPilot > Enviar prompt > Verificar uso de tokens | El uso de tokens se registra por usuario. El monitoreo refleja el consumo real | 🟠 | ⬜ |
| REG-024 | TENANT | Boards > Flow Pilot | `[DIRECTA]` | Flow Pilot chat funcional con tracking | Credenciales LLM configuradas | [Tenant] Login > Sidebar: Boards > Board > Flow Pilot > Abrir chat > Enviar mensajes > Verificar respuestas y tracking | El chat funciona correctamente. Las sesiones se mantienen. El tracking de tokens es visible | 🟠 | ⬜ |

### REGRESIÓN DIRECTA — Billing / Scraping (IONF-1098)

| ID | Side | Módulo | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Estado |
|----|------|--------|------|-------------|--------------|-------|-------------------|-----------|--------|
| REG-025 | TENANT | Billing | `[DIRECTA]` | Primer scraping → confirmación de cobro visible | Plataforma de scraping configurada, primer uso | [Tenant] Iniciar primer scraping de plataforma > Verificar que aparece modal de confirmación de cobro | Se muestra confirmación clara del cobro antes de proceder con el scraping | 🔴 | ⬜ |
| REG-026 | TENANT | Billing | `[DIRECTA]` | Cobro confirmado → scraping ejecutado | Confirmación de cobro aceptada | [Tenant] Aceptar confirmación de cobro > Verificar que el scraping se ejecuta > Verificar resultado | El cobro se procesa y el scraping se ejecuta correctamente tras la confirmación | 🔴 | ⬜ |

### REGRESIÓN DIRECTA — Gateway Services (IONF-1004)

| ID | Side | Módulo | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Estado |
|----|------|--------|------|-------------|--------------|-------|-------------------|-----------|--------|
| REG-027 | ADMIN GATEWAY | Services (Listings) | `[DIRECTA]` | Listings Etsy disponibles en Gateway | Etsy connector configurado | [Admin Gateway] Login > Apps > Verificar servicio de Listings para Etsy | Los Listings de Etsy están disponibles y funcionales en el Gateway | 🟠 | ⬜ |
| REG-028 | ADMIN GATEWAY | Services (Listings) | `[DIRECTA]` | Listings WooCommerce disponibles en Gateway | WooCommerce connector configurado | [Admin Gateway] Login > Apps > Verificar servicio de Listings para WooCommerce | Los Listings de WooCommerce están disponibles y funcionales en el Gateway | 🟠 | ⬜ |

---

### REGRESIÓN INDIRECTA — Cross-Impact

| ID | Side | Módulo | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Estado |
|----|------|--------|------|-------------|--------------|-------|-------------------|-----------|--------|
| REG-029 | TENANT | Boards > App Nodes | `[INDIRECTA]` | Flow con nodos app connector ejecuta post-fix connections | Flow con nodos que usan connector con API Key | [Tenant] Login > Sidebar: Boards > Abrir board con nodos de app connector > Ejecutar en Test > Verificar ejecución | Los nodos de app connector ejecutan correctamente. La reauth de API Key (IONF-1114) no rompe flows existentes | 🟠 | ⬜ |
| REG-030 | TENANT | Boards > Webhook Trigger | `[INDIRECTA]` | Flow con webhook trigger recibe request post-CORS fix | Flow con webhook trigger en Production | Enviar POST desde dominio externo a webhook URL > Verificar que el flow se dispara | El fix de CORS (IONF-1169) no introduce regresiones en webhooks dedicados de flows. Los webhooks internos siguen funcionando | 🟠 | ⬜ |
| REG-031 | TENANT | Boards > Scheduler + Decision | `[INDIRECTA]` | Flow con Scheduler + Simple Decision funciona e2e | Flow con Scheduler que ejecuta y pasa por Simple Decision numérica | [Tenant] Login > Board con Scheduler > Configurar hora > Activar Production > Esperar ejecución > Verificar que Simple Decision toma la rama correcta | El flujo completo Scheduler→Decision funciona sin falsos negativos en la comparación numérica | 🔴 | ⬜ |
| REG-032 | ADMIN GATEWAY | Customer > Grapp Schedule | `[INDIRECTA]` | Grapp Schedule muestra hora correcta | Grapp instalado con schedule activo | [Admin Gateway] Login > Customer > Configured Channels > Seleccionar Grapp > Grapp Schedule > Verificar hora | La hora del schedule se muestra correctamente sin desfase UTC/Local (cross: IONF-1007) | 🟠 | ⬜ |
| REG-033 | TENANT | Boards > ION PDF | `[INDIRECTA]` | Nodo ION PDF en canvas respeta confirmación de cierre | Board con nodo ION PDF abierto | [Tenant] Login > Sidebar: Boards > Board > Nodo ION PDF > Editar template > Intentar cerrar con cambios | Se muestra confirmación antes de cerrar (cross: IONF-1126). Los cambios no se pierden silenciosamente | 🟠 | ⬜ |
| REG-034 | TENANT | Execution History | `[INDIRECTA]` | Ejecución de flow → registro correcto en historial con R2 sync | Flow ejecutado recientemente | [Tenant] Login > Sidebar: Execution History > Verificar ejecución reciente > Verificar logs completos | Los logs aparecen completos y sincronizados (cross: IONF-1049). Los timestamps son correctos (cross: IONF-1168) | 🟠 | ⬜ |
| REG-035 | TENANT | Credentials > LLM | `[INDIRECTA]` | Credenciales LLM → Flow Pilot funciona con token tracking | Credenciales LLM configuradas | [Tenant] Login > Sidebar: Credentials > Verificar key activa > Ir a Board > Flow Pilot > Usar IA > Verificar tokens | Las credenciales LLM siguen funcionando con el nuevo tracking de tokens (cross: IONF-1020) | 🟡 | ⬜ |
| REG-036 | ADMIN GATEWAY | Customer > Connections | `[INDIRECTA]` | Grapp Connections sin duplicación post-reauth | Grapp con conexión API Key | [Admin Gateway] Login > Customer > Grapp > Connections > Reauthorize API Key > Verificar lista | La reauthorización no genera conexiones duplicadas en el contexto de Grapps (cross: IONF-1114) | 🟠 | ⬜ |
| REG-037 | ADMIN GATEWAY | Customer > Marketplace | `[INDIRECTA]` | Marketplace muestra listings Etsy/WooCommerce | Listings configurados en Gateway | [Admin Gateway] Login > Customer > Available Marketplace > Verificar que Etsy y WooCommerce listings aparecen | Los nuevos listings (cross: IONF-1004) están disponibles en el marketplace del customer | 🟡 | ⬜ |

---

### BASELINE — Flujos Críticos (L1 test-priorities.md)

> Módulos 🔴/🟠 del L1 no tocados directamente por tickets de v0.1.1.
> Verificar que el core del producto no se rompió.

| ID | Side | Módulo | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Estado |
|----|------|--------|------|-------------|--------------|-------|-------------------|-----------|--------|
| REG-038 | KC | Auth / Login | `[BASELINE]` | Login SSO funciona correctamente | Usuario registrado con SSO | Navegar a Login > Click "Login with SSO" > Autenticar en Keycloak > Verificar redirección | El usuario puede iniciar sesión vía SSO y es redirigido al dashboard/company selection | 🟠 | ⬜ |
| REG-039 | TENANT | Boards | `[BASELINE]` | Crear un flow nuevo | Usuario con permiso CREATE_BOARD | [Tenant] Login > Sidebar: Boards > Crear Board > Asignar nombre > Guardar | El flow se crea y aparece en la lista de boards | 🔴 | ⬜ |
| REG-040 | TENANT | Boards > Canvas | `[BASELINE]` | Agregar nodos y conectar en canvas | Board existente | [Tenant] Login > Sidebar: Boards > Abrir board > Agregar nodos (HTTP Request, Mapper) > Conectar con edges | Los nodos se agregan al canvas y las conexiones (edges) se establecen correctamente | 🔴 | ⬜ |
| REG-041 | TENANT | Boards > Execution | `[BASELINE]` | Ejecutar un flow completo en modo Test | Board con nodos conectados y configurados | [Tenant] Login > Sidebar: Boards > Abrir board > Click Test > Ejecutar desde nodo inicial > Verificar resultado | La ejecución recorre todos los nodos y termina en status "completed" | 🔴 | ⬜ |
| REG-042 | TENANT | Execution History | `[BASELINE]` | Ver historial de ejecuciones completo | Al menos una ejecución completada | [Tenant] Login > Sidebar: Execution History > Verificar lista > Abrir detalle | Los logs muestran datos correctos: nodos ejecutados, resultados, timestamps | 🟠 | ⬜ |
| REG-043 | TENANT | Connections (Integrations) | `[BASELINE]` | Crear conexión con diferentes métodos auth | Connector con auth configurado | [Tenant] Login > Sidebar: Connections > Check Connection > Crear nueva conexión (OAuth/Basic/API Key) | La conexión se crea correctamente con el método de autenticación seleccionado | 🟠 | ⬜ |
| REG-044 | TENANT | Connections (App Connectors) | `[BASELINE]` | Crear y editar conector | Usuario con permiso CREATE_APP | [Tenant] Login > Sidebar: Connections > Create > Manual Connector > Completar datos > Guardar > Editar | El connector se crea, se guarda y se puede editar posteriormente | 🟠 | ⬜ |
| REG-045 | TENANT | Catalog | `[BASELINE]` | Crear y editar service | Usuario con acceso a Catalog | [Tenant] Login > Sidebar: Catalog > Add Catalog Item > Crear Grapp > Guardar > Editar | El service/grapp se crea y se puede editar | 🟠 | ⬜ |
| REG-046 | TENANT | PDF Templates | `[BASELINE]` | Crear, editar y utilizar template PDF | Usuario con permiso READ_PDF_TEMPLATE | [Tenant] Login > Sidebar: PDF Templates > New Template > Agregar elementos (Text, Image, Table) > Guardar > Verificar en flow | El template se crea, los elementos se guardan, y el nodo ION PDF puede utilizarlo | 🟠 | ⬜ |
| REG-047 | TENANT | Data Store | `[BASELINE]` | Data Store CRUD operations | Data Store/Structure existente | [Tenant] Login > Sidebar: Data Store > Create > Edit > View > Verificar datos | Las operaciones CRUD de Data Store funcionan correctamente | 🟡 | ⬜ |
| REG-048 | TENANT | Accounts / Dev Apps | `[BASELINE]` | Accounts y Developer Apps operativas | Company con cuentas configuradas | [Tenant] Login > Sidebar: Accounts > Add Account > Sidebar: Developer Apps > Configure App | Las cuentas se pueden gestionar y las dev apps se configuran correctamente | 🟡 | ⬜ |
| REG-049 | TENANT | Teams / Permissions | `[BASELINE]` | Permisos por usuario funcionan | Company con múltiples usuarios | [Tenant] Login > Sidebar: Teams > Edit Permissions > Verificar que los permisos se aplican | Los cambios de permisos se reflejan correctamente en el acceso a módulos | 🟡 | ⬜ |

---

## Tickets del Release vs. Módulos Impactados

| Ticket | Descripción | Prioridad | Módulo directo | Módulos cross-impact | TCs |
|--------|-------------|-----------|---------------|---------------------|-----|
| IONF-1169 | Quitar CORS para rutas públicas de webhooks | 🟠 Normal | Webhooks | Boards (triggers) | REG-016, 017, 030 |
| IONF-1168 | Error +4h en logs Company Schedules UI | 🟠 Normal | Executions, Boards | Dashboard | REG-002, 018, 034 |
| IONF-1149 | Protocolo de Despliegue v0.1.0 | 🔴 High | Infra/Ops | — | N/A (doc) |
| IONF-1128 | Simple Decision compara strings como números | 🔴 High | Boards (Nodes) | Executions | REG-005, 006, 007, 031 |
| IONF-1127 | Scheduler status queda en "error" | 🔴 High | Boards (Scheduler) | Executions | REG-001, 004, 031 |
| IONF-1126 | PDF Templates: cambios se pierden sin confirmación | 🔴 High | PDF Templates | Boards (canvas) | REG-010, 011, 033 |
| IONF-1121 | Boards: false unsaved alert post-commit | 🟠 Normal | Boards (Commit) | — | REG-008, 009 |
| IONF-1116 | PDF Templates: sin límite tamaño → crash | 🔴 High | PDF Templates | — | REG-012, 013 |
| IONF-1114 | Connections: API Key crea duplicado | 🔴 High | Connections (Integrations) | Boards (app nodes) | REG-014, 015, 029, 036 |
| IONF-1098 | Confirmación cobro primer scraping | 🔴 High | Billing/Integrations | Accounts | REG-025, 026 |
| IONF-1075 | Refactorizar registro de compañía | 🟠 Normal | Auth (Registration) | — | REG-020, 021 |
| IONF-1049 | Sincronización de logs con R2 | 🟠 Normal | Executions (Logs) | — | REG-019, 034 |
| IONF-1030 | Mejoras interface dualtrack | 🟠 Normal | Dashboard/UI | Boards | REG-022 |
| IONF-1020 | Monitoreo tokens Flow Pilot | 🔴 High | Boards (Flow Pilot) | Credentials | REG-023, 024, 035 |
| IONF-1007 | Error UTC/Local Company Schedules | 🔴 High | Boards (Scheduler) | Executions, ADMIN GW | REG-003, 032 |
| IONF-1004 | Listings Etsy/WooCommerce en Gateway | 🟠 Normal | Integrations (Gateway) | Connections | REG-027, 028, 037 |

---

## Items Skipped — Pendientes de 1.4.x (heredados de v0.1.0)

Los siguientes ítems del side **ADMIN GATEWAY > Apps > Services** permanecen como `Skipped` desde v0.1.0 porque dependen de la fusión de la rama `1.4.x` a `DEVELOPMENT`. Deben re-evaluarse en la próxima release:

- Set Image, Filter by Slug/Title/Description/Categories/Type
- Enable/Disable in bulk, Enable, Disable
- Edit > Set Image/Title/Details/Description/Features/Groups/Category/Enable Badge/Custom Credentials
- Copy Cart/Install/Callback
- Custom Integrations > Create
- Integrations > List, Claim
- Go Back

---

## Observaciones

1. **IONF-1149** (Protocolo de Despliegue v0.1.0) es un ticket de documentación/ops, no genera TCs de regresión funcional.
2. **v0.1.1 es una patch release**: Los tickets principales son regression fixes de v0.1.0. El riesgo de regresión está concentrado en **Boards** (Scheduler, Simple Decision, Commit) y **PDF Templates**.
3. **CORS fix (IONF-1169)**: Impacto potencial en todos los webhooks públicos. Verificar que los webhooks dedicados (no públicos) no se vean afectados.
4. **Sync R2 (IONF-1049)**: El cambio en la sincronización de logs puede afectar la disponibilidad de historial de ejecuciones. Testear tanto ejecuciones nuevas como históricas.
5. **Reauth API Key (IONF-1114)**: Este fix tiene alto cross-impact con flows que usan nodos de app connector. Una conexión duplicada podría causar que flows existentes usen credenciales obsoletas.
6. **Herencia v0.1.0**: Los items Skipped de ADMIN GATEWAY > Services se mantienen sin cambio. No hubo fusión de 1.4.x en este sprint.
7. **Edge case documentado (v0.1.0)**: IONF-1087 (nodo IonPDF sin edge → spinner permanente) sigue vigente — no fue resuelto en v0.1.1.

---

## Instrucciones de uso

1. **Abrir el CSV** en Google Sheets / Excel: [regression-matrix.csv](file:///c:/Users/STEVE/Desktop/Automation/ionflow-qa-catalyst/knowledge/releases/v0.1.1/regression-matrix.csv)
2. **La columna RESOLUTION** acepta: `Passed`, `Failed`, `Skipped`, `Blocked`
3. **La columna ASSIGNED** indica el tester responsable de cada fila
4. **La columna COMMENTS** es libre para notas durante la ejecución
5. **La columna OBSERVATION** contiene instrucciones pre-existentes (ej. "Verificar en modo Test y modo Produccion")
6. **La columna TICKET** referencia los tickets de v0.1.1 que motivaron ese caso de test
7. **La columna TIPO** indica DIRECTA / INDIRECTA / BASELINE
8. **Los ítems sin TICKET** son parte del baseline de regresión — deben ejecutarse aunque no tengan ticket directo

---

## Notas

- Formato basado en: `templates/release-regression-matrix.md`
- Fuente de tickets: `get_tickets_deployment_4.csv` (16 tickets ready to merge)
- Herencia de v0.1.0: `knowledge/releases/v0.1.0/regression-matrix.md`
- CSV de regresión guía: `Ionflow Testing Plan - Regression Test Template.csv`
- L1 test-priorities.md usado para baseline y criticidad
- L2 modules cargados: boards, pdf-templates, connections, executions, auth, billing, integrations
- Los items `Skipped` de ADMIN GATEWAY preservan la observación original del template aprobado
- Esta versión es **v0.1.1** — patch release con regression fixes de v0.1.0 + features Sprint 4

*Generado por ionflow-qa-catalyst — skill: release/regression-matrix*
*Fecha: 2026-07-20*
