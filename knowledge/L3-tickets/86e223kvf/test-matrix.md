# Test Matrix — 86e223kvf

> Generada por `test-docs/document` (modo matrix)
> Fecha: 2026-07-20
> Módulo: Multi-módulo — Migración UI Framework (PrimeVue → Tailwind 4 + shadcn-vue)
> Track: Discovery

## Resumen

| Métrica | Valor |
|---------|-------|
| Total de casos | 69 |
| Happy path | 24 |
| Edge cases | 16 |
| Negativos | 8 |
| Regresión | 14 |
| Code Review | 7 |
| Automatizables | 38 |
| Cobertura de AC | 20/20 |

---

## Test Matrix

### WAVE 1 — Fundación (BLOQUEANTE)

> Si algún TC de Wave 1 falla, las Waves 2 y 3 son inválidas.

#### AC-A1: TenantLayout (Shell de la app)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-001 | Layout | AC-A1 | Happy Path | TenantLayout carga con todos los servicios | Usuario tenant con credenciales válidas | Company Login > Verify: App carga sin errores > Verify: Sidebar visible > Verify: Topbar visible > Verify: Breadcrumbs visibles | App tenant carga completamente. Sidebar, Topbar y contenido principal visibles. Sin errores en consola. | 🔴 | ✅ | ⬜ |
| TC-002 | Layout | AC-A1 | Edge Case | TenantLayout preserva setUser sync con canvas | Usuario navega al editor de flows | Company Login > Sidebar: Boards > Click [cualquier Flow] > Verify: Canvas carga > Verify: Consola sin errores de `$useFlowCore` | El canvas carga correctamente. `window.$useFlowCore.setUser` sincronizado. Sin errores JS. | 🔴 | ❌ | ⬜ |
| TC-003 | Layout | AC-A1 | Edge Case | TenantLayout después de sesión expirada | Sesión expirada (cerrar y reabrir browser) | Navigate: URL de Ionflow > Verify: Redirect a login > Company Login > Verify: App carga correctamente | Después de re-login, la app carga con todos los servicios inyectados. | 🟠 | ✅ | ⬜ |

#### AC-A2: CSS Isolation (.modern-ui)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-004 | CSS | AC-A2 | Happy Path | Pantallas Tenant usan estilos Tailwind correctamente | Usuario tenant logueado | Company Login > Sidebar: Boards > Verify: Tabla con estilos shadcn > Sidebar: Executions > Verify: Tabla con estilos shadcn | Todas las pantallas tenant usan estilos modernos (Tailwind/shadcn). Sin mezcla con PrimeVue. | 🔴 | ✅ | ⬜ |
| TC-005 | CSS | AC-A2 | Happy Path | Pantallas Admin mantienen estilos PrimeVue sin regresión | Usuario admin logueado | Admin Login > Navigate: /admin/dashboard > Verify: Dashboard con estilos PrimeVue > Navigate: /admin/workflows > Verify: Tabla PrimeVue intacta | Pantallas Admin visualmente idénticas al estado anterior. Sin bleeding de Tailwind. | 🔴 | ✅ | ⬜ |
| TC-006 | CSS | AC-A2 | Edge Case | Navegación rápida entre Admin y Tenant | Usuario con ambos roles | Admin Login > Navigate: /admin/dashboard > Verify: Estilos Admin ok > Navigate: /workflows > Verify: Estilos Tenant ok > Navigate: /admin/workflows > Verify: Admin ok | No hay contaminación de estilos al alternar entre contextos Admin y Tenant. | 🔴 | ✅ | ⬜ |

#### AC-A3: DataTable (shadcn/TanStack Table)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-007 | DataTable | AC-A3 | Happy Path | Paginación SSR funciona en DataTable | Módulo con >25 registros | Company Login > Sidebar: Executions > Verify: Tabla muestra página 1 > Click [Página 2] > Verify: Datos de página 2 cargan | La paginación SSR funciona: cada página hace request al servidor y muestra datos correctos. | 🔴 | ✅ | ⬜ |
| TC-008 | DataTable | AC-A3 | Happy Path | Ordenamiento por columna funciona | Módulo con múltiples registros | Company Login > Sidebar: Boards > Click [Header "Name"] > Verify: Ordenado A-Z > Click [Header "Name"] > Verify: Ordenado Z-A | Sort ascendente y descendente funciona en el DataTable. | 🔴 | ✅ | ⬜ |
| TC-009 | DataTable | AC-A3 | Edge Case | DataTable con 0 registros (empty state) | Módulo sin datos | Company Login > Sidebar: Webhooks > Verify: Empty state visible con mensaje apropiado | Se muestra un estado vacío claro y consistente, sin tabla rota ni error. | 🟠 | ✅ | ⬜ |
| TC-010 | DataTable | AC-A3 | Edge Case | Column visibility toggle | Tabla con columnas ocultables | Company Login > Sidebar: Executions > Click [Column Visibility] > Toggle: ocultar columna "Status" > Verify: Columna desaparece > Toggle: mostrar > Verify: Columna reaparece | Las columnas se pueden ocultar y mostrar dinámicamente. | 🟠 | ✅ | ⬜ |

#### AC-A4: Navigation (Sidebar + Topbar + Breadcrumbs)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-011 | Navigation | AC-A4 | Happy Path | Sidebar muestra todas las secciones según permisos | Usuario con todos los permisos | Company Login > Verify: Sidebar muestra todas las secciones (Boards, Executions, Connections, Data Store, PDF Templates, Webhooks, Keys, Accounts, Dashboard, Settings) | Todas las secciones del menú son visibles y clickeables. | 🟠 | ✅ | ⬜ |
| TC-012 | Navigation | AC-A4 | Happy Path | Breadcrumbs se actualizan al navegar | Usuario navegando | Company Login > Sidebar: Boards > Verify: Breadcrumb muestra "Boards" > Click [un Flow] > Verify: Breadcrumb muestra "Boards > [nombre]" | Breadcrumbs reflejan la ruta actual. Último crumb sin link. | 🟠 | ✅ | ⬜ |
| TC-013 | Navigation | AC-A4 | Edge Case | Usuario con permisos parciales | Usuario sin permiso de Boards | Company Login (usuario restringido) > Verify: Sidebar NO muestra "Boards" > Navigate: /workflows > Verify: Acceso denegado o redirect | Secciones sin permiso no aparecen en el menú. Acceso directo por URL es bloqueado. | 🟠 | ✅ | ⬜ |

#### AC-A5: Toast System (vue-sonner)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-014 | Toast | AC-A5 | Happy Path | Toast success aparece en operación CRUD | Usuario crea un recurso | Company Login > Sidebar: PDF Templates > Button: "Create" > Fill "Name": "Test Template" > Button: "Save" > Verify: Toast success visible | Toast de éxito aparece con mensaje descriptivo. | 🟠 | ✅ | ⬜ |
| TC-015 | Toast | AC-A5 | Happy Path | Toast error aparece en operación fallida | API retorna error | Company Login > Sidebar: Boards > Intentar acción que falla > Verify: Toast error visible con mensaje | Toast de error aparece sin stackar duplicados. | 🟠 | ✅ | ⬜ |
| TC-016 | Toast | AC-A5 | Edge Case | Deduplicación de toasts idénticos | Acción rápida repetida | Company Login > Ejecutar misma acción 3 veces rápidamente > Verify: Solo 1 toast visible (no 3 apilados) | Los toasts con mismo `tone:message` se deduplicán. Máximo 1 instancia visible. | 🟠 | ✅ | ⬜ |

---

### WAVE 2 — Features Nuevos + Backend

#### AC-B1: Global Search (Cmd/Ctrl+K)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-017 | Search | AC-B1 | Happy Path | Búsqueda global encuentra flows | Flows existentes | Company Login > Keyboard: Ctrl+K > Verify: Command palette abre > Fill "Search": "test" > Wait: Resultados > Verify: Flows matching "test" visibles | Command palette muestra resultados de flows que contienen "test". | 🟠 | ✅ | ⬜ |
| TC-018 | Search | AC-B1 | Happy Path | Búsquedas recientes persisten | Búsqueda previa realizada | Company Login > Keyboard: Ctrl+K > Fill "Search": "mi flow" > Click [resultado] > Keyboard: Ctrl+K > Verify: "mi flow" aparece en recientes | Las últimas búsquedas se guardan y muestran al abrir el palette. | 🟠 | ✅ | ⬜ |
| TC-019 | Search | AC-B1 | Edge Case | Búsqueda rápida con cambio de query (race condition) | Flows existentes | Company Login > Keyboard: Ctrl+K > Fill "Search": "abc" > Rápidamente cambiar a "xyz" > Wait: Resultados > Verify: Solo resultados de "xyz" visibles | AbortController cancela la búsqueda anterior. Solo se muestran resultados de la última query. | 🟠 | ❌ | ⬜ |
| TC-020 | Search | AC-B1 | Negativo | Búsqueda sin resultados | Sin flows matching | Company Login > Keyboard: Ctrl+K > Fill "Search": "zzzznonexistent" > Wait: Resultados > Verify: Mensaje "No results" | Se muestra mensaje de "sin resultados" limpio, sin error. | 🟡 | ✅ | ⬜ |

#### AC-B2: Dark/Light Mode

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-021 | Theme | AC-B2 | Happy Path | Toggle dark mode funciona | App en light mode | Company Login > Click [Theme Toggle en Topbar] > Verify: UI cambia a dark mode > Verify: Transición visual suave | Dark mode se activa con transición. Todos los componentes adaptan colores. | 🟡 | ✅ | ⬜ |
| TC-022 | Theme | AC-B2 | Edge Case | Dark mode persiste entre recargas | Dark mode activo | Company Login > Click [Theme Toggle] > Verify: Dark mode > Reload page > Verify: Dark mode sigue activo | La preferencia de tema persiste tras recargar la página. | 🟡 | ✅ | ⬜ |

#### AC-C3: Boards — CreateConnectionV2Dialog

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-023 | Boards | AC-C3 | Happy Path | Vista lista de Boards carga correctamente | Boards existentes | Company Login > Sidebar: Boards > Verify: Lista de boards visible en DataTable > Verify: Acciones (crear, editar, eliminar) disponibles | Lista de boards con nuevo DataTable funcional. | 🟠 | ✅ | ⬜ |
| TC-024 | Connections | AC-C3 | Happy Path | CreateConnectionV2Dialog funciona (primary + secondary) | Connector con dual auth | Company Login > Sidebar: Boards > Click [Flow] > Canvas: Click [App Node sin conexión] > Drawer: Click "Create Connection" > Verify: Dialog abre > Verify: Tabs para primary y secondary visibles > Fill credentials > Button: "Save" | Conexión se crea correctamente. Tab correcto seleccionado según qué conexión resuelve. | 🟠 | ❌ | ⬜ |
| TC-025 | Connections | AC-C3 | Edge Case | CreateConnectionV2Dialog — solo secondary resuelve (bugfix) | Connector donde solo secondary connection resuelve | Company Login > Sidebar: Boards > Click [Flow] > Canvas: Click [App Node] > Drawer: Click "Create Connection" > Verify: activeTab apunta al tab con form disponible (no al tab '0' vacío) | El dialog NO queda en blanco. Se selecciona el tab que tiene contenido. | 🔴 | ❌ | ⬜ |

#### AC-C4: Executions (filtros backend)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-026 | Executions | AC-C4 | Happy Path | Filtrar ejecuciones por status | Ejecuciones con distintos status | Company Login > Sidebar: Executions > Select "Status": "completed" > Verify: Solo ejecuciones completed visibles | Filtro por status funciona. Solo se muestran ejecuciones del status seleccionado. | 🟠 | ✅ | ⬜ |
| TC-027 | Executions | AC-C4 | Happy Path | Filtrar ejecuciones por rango de fechas | Ejecuciones en distintas fechas | Company Login > Sidebar: Executions > Fill "Date From": "2026-07-01" > Fill "Date To": "2026-07-15" > Verify: Solo ejecuciones del rango visibles | Filtro por fechas funciona. Inclusivo en ambos extremos. | 🟠 | ✅ | ⬜ |
| TC-028 | Executions | AC-C4 | Edge Case | Filtro status case-insensitive | Frontend envía "COMPLETED" en mayúsculas | Company Login > Sidebar: Executions > Filter status "COMPLETED" > Verify: Resultados iguales que "completed" | El filtro es case-insensitive — funciona independientemente de mayúsculas/minúsculas. | 🟡 | ✅ | ⬜ |
| TC-029 | Executions | AC-C4 | Negativo | Filtro con date_from > date_to | Rango de fechas invertido | Company Login > Sidebar: Executions > Fill "Date From": "2026-07-15" > Fill "Date To": "2026-07-01" > Verify: Resultado vacío o validación | No se muestran datos inconsistentes. Idealmente validación o lista vacía. | 🟡 | ✅ | ⬜ |

#### AC-C5: Data Store / Data Structure (search + filter)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-030 | Data Store | AC-C5 | Happy Path | Buscar Data Store por nombre | Data Stores existentes | Company Login > Sidebar: Data Store > Fill "Search": "orders" > Verify: Solo Data Stores con "orders" en nombre visibles | Búsqueda por nombre filtra correctamente. | 🟠 | ✅ | ⬜ |
| TC-031 | Data Store | AC-C5 | Happy Path | Ordenar Data Stores por created_at | Múltiples Data Stores | Company Login > Sidebar: Data Store > Click [Header "Created"] > Verify: Ordenado por fecha | Ordenamiento por created_at funciona correctamente. | 🟠 | ✅ | ⬜ |
| TC-032 | Data Store | AC-C5 | Happy Path | StoreViewer muestra datos anidados | Data Store con datos nested | Company Login > Sidebar: Data Store > Click [Data Store] > Verify: StoreViewer abre > Verify: Datos anidados visibles con NestedValueTree | StoreViewer muestra datos con estructura expandible/colapsable. | 🟠 | ✅ | ⬜ |
| TC-033 | Data Store | AC-C5 | Edge Case | Buscar con caracteres especiales (%_\) | Data Store existente | Company Login > Sidebar: Data Store > Fill "Search": "test%data" > Verify: Búsqueda literal, no wildcard | Los caracteres `%`, `_`, `\` se escapan correctamente. Búsqueda literal. | 🟠 | ❌ | ⬜ |
| TC-034 | Data Store | AC-C5 | Negativo | Ordenar por columna no whitelisted | Intento de sort por campo no permitido | API: GET /data-stores?order_by=invalid_field > Verify: Respuesta con default sort o error 400 | El backend rechaza o ignora campos de ordenamiento no whitelisted `{id, name, created_at}`. | 🟡 | ❌ | ⬜ |

#### AC-C6 / AC-C7: Accounts + Keys (filtros backend)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-035 | Accounts | AC-C6 | Happy Path | Filtrar accounts por timezone | Accounts con distintos timezones | Company Login > Sidebar: Accounts > Filter: timezone "America/La_Paz" > Verify: Solo accounts con ese timezone | Filtro por timezone funciona correctamente. | 🟡 | ✅ | ⬜ |
| TC-036 | Accounts | AC-C6 | Edge Case | Accounts sin timezone configurado | Accounts con timezone null | Company Login > Sidebar: Accounts > Filter: timezone (clear) > Verify: Accounts sin timezone aparecen | Accounts sin timezone no desaparecen del listado base. | 🟡 | ✅ | ⬜ |
| TC-037 | Keys | AC-C7 | Happy Path | Filtrar keys por provider | Keys con distintos providers | Company Login > Sidebar: Keys > Filter: provider "openai" > Verify: Solo keys de OpenAI visibles | Filtro por provider funciona. | 🟡 | ✅ | ⬜ |

---

### WAVE 3 — Pantallas Individuales + Polish

#### AC-C1: 14 Pantallas Migradas (smoke test por pantalla)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-038 | Boards | AC-C1 | Happy Path | Vista Boards carga y muestra datos | Boards existentes | Company Login > Sidebar: Boards > Verify: DataTable con boards > Verify: Acciones visibles | Tabla de boards funcional con nuevo diseño. | 🟠 | ✅ | ⬜ |
| TC-039 | Executions | AC-C1 | Happy Path | Vista Executions carga y muestra datos | Ejecuciones existentes | Company Login > Sidebar: Executions > Verify: DataTable con ejecuciones | Tabla de ejecuciones funcional. | 🟠 | ✅ | ⬜ |
| TC-040 | PDF Templates | AC-C1 | Happy Path | Vista PDF Templates carga (referencia de diseño) | Templates existentes | Company Login > Sidebar: PDF Templates > Verify: DataTable con templates > Verify: Diseño es la referencia para las demás tablas | Tabla de PDF Templates como patrón visual de referencia. | 🟠 | ✅ | ⬜ |
| TC-041 | Connections | AC-C1 | Happy Path | Vista App Connectors carga | Connectors existentes | Company Login > Sidebar: Connections > Verify: DataTable con connectors | Tabla de connectors funcional. | 🟠 | ✅ | ⬜ |
| TC-042 | Integrations | AC-C1 | Happy Path | Vista Integrations carga | Integraciones existentes | Company Login > Sidebar: Integrations > Verify: DataTable con integraciones | Tabla de integraciones funcional. | 🟠 | ✅ | ⬜ |
| TC-043 | Webhooks | AC-C1 | Happy Path | Vista Webhooks carga | Webhooks existentes | Company Login > Sidebar: Webhooks > Verify: DataTable con webhooks | Tabla de webhooks funcional. | 🟡 | ✅ | ⬜ |
| TC-044 | Accounts | AC-C1 | Happy Path | Vista Accounts carga | Accounts existentes | Company Login > Sidebar: Accounts > Verify: DataTable con accounts | Tabla de accounts funcional. | 🟡 | ✅ | ⬜ |
| TC-045 | Keys | AC-C1 | Happy Path | Vista Keys carga | Keys existentes | Company Login > Sidebar: Keys > Verify: DataTable con keys | Tabla de keys funcional. | 🟡 | ✅ | ⬜ |
| TC-046 | Dashboard | AC-C1 | Happy Path | Vista Dashboard carga | — | Company Login > Sidebar: Dashboard > Verify: Dashboard visible con métricas | Dashboard migrado funcional. | 🟡 | ✅ | ⬜ |
| TC-047 | Data Store | AC-C1 | Happy Path | Vista Data Store carga | Data Stores existentes | Company Login > Sidebar: Data Store > Verify: DataTable con data stores | Tabla de data stores funcional. | 🟡 | ✅ | ⬜ |
| TC-048 | Settings | AC-C1 | Happy Path | Vista Settings carga | — | Company Login > Navigate: /settings > Verify: Settings visible | Vista de settings migrada funcional. | 🟡 | ✅ | ⬜ |
| TC-049 | Profile | AC-C1 | Happy Path | Vista Profile carga | — | Company Login > Navigate: /profile > Verify: Profile visible | Vista de profile migrada funcional. | 🟡 | ✅ | ⬜ |
| TC-050 | Activity | AC-C1 | Happy Path | Vista Activity carga | — | Company Login > Navigate: /activity > Verify: Activity visible | Vista de activity migrada funcional. | 🟡 | ✅ | ⬜ |
| TC-051 | Support | AC-B3 | Happy Path | Vista Support carga | — | Company Login > Navigate: /support (o via menú) > Verify: Support visible | Nueva vista de soporte accesible y funcional. | 🟢 | ✅ | ⬜ |

#### AC-C2: Consistencia visual entre pantallas

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-052 | Visual | AC-C2 | Happy Path | Tablas siguen patrón de PDF Templates | Varias pantallas migradas | Company Login > Sidebar: PDF Templates > Capturar diseño visual > Sidebar: Boards > Comparar > Sidebar: Executions > Comparar | Headers, filas, acciones y estados son visualmente consistentes entre pantallas. | 🟡 | ❌ | ⬜ |

#### AC-C1: Modales normalizados

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-053 | Modal | AC-C1d | Happy Path | Modal de eliminación normalizado | Recurso eliminable existente | Company Login > Sidebar: Boards > Click [Delete en un board] > Verify: Modal de confirmación con título, mensaje, botón destructivo diferenciado | Modal sigue patrón normalizado: título, mensaje, botón cancel + botón destructivo rojo. | 🟠 | ✅ | ⬜ |
| TC-054 | Modal | AC-C1d | Happy Path | Otros modales de confirmación normalizados | — | Company Login > Trigger cualquier modal de confirmación > Verify: Patrón visual consistente con modal de eliminación (misma estructura, distinto color de acción) | Todos los modales de confirmación comparten estructura visual. | 🟡 | ❌ | ⬜ |

#### AC-E2 / AC-E3: i18n + Responsive

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-055 | i18n | AC-E2 | Happy Path | Textos en español sin keys faltantes | App en locale 'es' | Company Login (locale es) > Navegar por todas las pantallas migradas > Verify: Ningún texto muestra key raw (ej. "nav.boards.title") | Todos los textos están traducidos al español. Sin keys raw visibles. | 🟡 | ✅ | ⬜ |
| TC-056 | Responsive | AC-E3 | Happy Path | Pantallas legibles en 1366px | Browser en 1366px | Company Login > Resize: 1366x768 > Navegar: Boards, Executions, Data Store > Verify: Sin overflow, overlap ni texto cortado | Pantallas migradas se ven correctamente en resolución 1366x768. | 🟡 | ✅ | ⬜ |
| TC-057 | Responsive | AC-E3 | Edge Case | Pantallas en 1024px (tablet) | Browser en 1024px | Company Login > Resize: 1024x768 > Navegar: Boards, Executions > Verify: Sidebar colapsable > Verify: DataTable responsive | Layout se adapta. Sidebar colapsa. Tablas no tienen overflow horizontal. | 🟡 | ✅ | ⬜ |

#### AC-D3: Flow Description (backend fix)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-058 | Boards | AC-D3 | Happy Path | Descripción de flow se guarda correctamente | Flow existente | Company Login > Sidebar: Boards > Click [Flow] > Edit description > Fill "Description": "Test description" > Button: "Save" > Verify: Descripción persistida | La descripción del flow se guarda y persiste tras recargar. | 🟡 | ✅ | ⬜ |

---

## Casos de Regresión

| ID | Módulo impactado | Caso de regresión | Por qué podría romperse | Prioridad | Estado |
|----|-----------------|-------------------|------------------------|-----------|--------|
| REG-001 | Auth | Login flow funciona correctamente | TenantLayout reemplaza CompanyLayout — el flujo de auth podría romperse | 🔴 | ⬜ |
| REG-002 | Boards | Crear flow nuevo desde lista de boards | DataTable nuevo podría no tener el botón de crear o el handler | 🔴 | ⬜ |
| REG-003 | Boards | Editar flow existente (abrir canvas) | La navegación al editor debe seguir funcionando desde el nuevo DataTable | 🔴 | ⬜ |
| REG-004 | Boards | Ejecutar flow desde canvas (modo Development) | TenantLayout + setUser sync podría romper la ejecución | 🔴 | ⬜ |
| REG-005 | Connections | Crear nueva conexión OAuth (authorize → callback → token) | CreateConnectionV2Dialog fue migrada a primitivos nuevos | 🟠 | ⬜ |
| REG-006 | PDF Templates | Crear template desde vista lista | CRUD de templates debe seguir funcionando con nuevo DataTable | 🟠 | ⬜ |
| REG-007 | Webhooks | Eliminar webhook | Modal de eliminación normalizado + CRUD webhook | 🟠 | ⬜ |
| REG-008 | Data Store | Visualizar datos en StoreViewer | StoreViewer fue reescrito completamente | 🟠 | ⬜ |
| REG-009 | Executions | Ver detalle de ejecución | Vista de executions migrada completamente | 🟠 | ⬜ |
| REG-010 | Accounts | CRUD de accounts | Vista migrada + filtros backend nuevos | 🟡 | ⬜ |
| REG-011 | Keys | CRUD de keys/credentials | Vista migrada + filtro provider nuevo | 🟡 | ⬜ |
| REG-012 | Dashboard | Métricas cargan correctamente | Dashboard migrado debe seguir mostrando stats | 🟡 | ⬜ |
| REG-013 | Integrations | Instalar/desinstalar integración | Vista migrada, flujo de instalación debe seguir funcionando | 🟡 | ⬜ |
| REG-014 | Data Structure | CRUD de data structures | Vista migrada + search/filter backend nuevo | 🟡 | ⬜ |

---

## Queries de Verificación BD

> ⚠️ Queries basadas EXCLUSIVAMENTE en schemas de migraciones.

```sql
-- ==================================================================
-- TC-026/TC-028: Verificar filtro de Executions por status
-- Fuente: ../gateway/database/migrations/ (ExecutionController)
-- BD: PostgreSQL
-- ==================================================================

-- Verificar que filtro status es case-insensitive
SELECT id, status, created_at 
FROM executions 
WHERE LOWER(status) = LOWER('completed')
AND company_id = '<company_id>'
ORDER BY created_at DESC
LIMIT 10;
-- Esperado: Solo ejecuciones con status 'completed' (cualquier case)

-- ==================================================================
-- TC-027: Verificar filtro de Executions por rango de fechas
-- BD: PostgreSQL
-- ==================================================================

SELECT id, status, created_at
FROM executions
WHERE company_id = '<company_id>'
AND DATE(created_at) >= '2026-07-01'
AND DATE(created_at) <= '2026-07-15'
ORDER BY created_at DESC;
-- Esperado: Solo ejecuciones dentro del rango (inclusivo)

-- ==================================================================
-- TC-058: Verificar persistencia de flow description
-- Fuente: ../gateway/database/migrations/2026_04_02_200000_add_missing_columns_to_flows_table.php
-- Tabla: flows (company schema) | Columnas: id, name, description
-- BD: PostgreSQL
-- ==================================================================

SELECT id, name, description
FROM flows
WHERE company_id = '<company_id>'
AND name = '<flow_name>';
-- Esperado: description = 'Test description' (valor actualizado)

-- ==================================================================
-- TC-030/TC-033: Verificar búsqueda en Data Store (SQLite)
-- Fuente: ../flow_binaries/core/actions/store/storeservice/search.go
-- BD: SQLite (por tenant)
-- Nota: Estas queries se verifican vía la UI, no directamente en DBeaver
-- ==================================================================

-- Verificación conceptual del escape:
-- Buscar "test%data" debe usar: WHERE name LIKE '%test\%data%' ESCAPE '\'
-- El % literal debe ser escapado, no actuar como wildcard
```

---

## Code Review TCs (inyectados por Code Review QA)

> Origen: `code-review-qa.md` — generado 2026-08-02 por Code Review QA (modo Deployment / Bug Hunting)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Auto | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|------|--------|
| TC-CR-001 | Keys | AC-C4 | Code Review — RISK | Buscar keys por texto en ruta account | Cuenta con ≥3 keys de distinto nombre | Company Login > Sidebar: Configuración > Keys (ruta account) > Search: nombre parcial > Verify: resultados filtrados | Si la ruta es por account, search debería filtrar. Si no filtra, confirmar que el FE usa ruta company (RISK-CR-001) | 🟠 | ❌ | ⬜ |
| TC-CR-002 | DataStore | AC-D1 | Code Review — RISK | Ordenar Data Store por columna no whitelisted | ≥2 data stores existentes | Company Login > Sidebar: Data Store > Intentar ordenar por columna inválida (modificar request en DevTools: `order_by=DROP`) > Verify: Error 400 | La API rechaza columnas no whitelisted con error 400 (RISK-CR-002) | 🟡 | ❌ | ⬜ |
| TC-CR-003 | Keys | AC-C4 | Code Review — RISK | OrderDirection con valor no estándar en keys listing | ≥2 keys existentes | Company Login > DevTools > Modificar request: `order_direction=desc;DROP` > Verify: Error o ignorado | OrderDirection solo acepta asc/desc. Valores inválidos son rechazados o normalizados (RISK-CR-003) | 🟠 | ❌ | ⬜ |
| TC-CR-004 | Boards | AC-C1 | Code Review — RISK | Listado de flows con filtros de status y search | ≥3 flows con distintos status | Company Login > Sidebar: Boards > Filtrar por status "active" > Search: nombre parcial > Verify: Resultados correctos | Filtros de status y búsqueda funcionan correctamente juntos (RISK-CR-004) | 🟡 | ✅ | ⬜ |
| TC-CR-005 | Layout | AC-A1 | Code Review — EDGE | Toasts no se duplican (PrimeVue + vue-sonner) | Usuario tenant logueado | Company Login > Realizar una acción que genera toast (ej: crear board) > Verify: Solo UN toast aparece, no duplicado | Solo un toast visible. No hay duplicación entre PrimeVue Toast y vue-sonner Toaster (EDGE-CR-001) | 🟡 | ❌ | ⬜ |
| TC-CR-006 | Layout | AC-A3 | Code Review — EDGE | 3 clics rápidos en delete — dedup de toasts | ≥1 item eliminable | Company Login > Sidebar: Data Store > Create 3 test stores > Delete cada uno rápidamente (clic-clic-clic) > Verify: Toasts deduplicados | No se apilan 3 toasts idénticos. La deduplicación funciona (EDGE-CR-002) | 🟡 | ❌ | ⬜ |
| TC-CR-007 | DataStore | AC-D1 | Code Review — EDGE | Data Store filtra correctamente por tenant | ≥2 tenants con data stores | Company Login como tenant A > Sidebar: Data Store > Verify: Solo data stores de tenant A visibles | Data Store aislado por tenant. No se ven stores de otros tenants (EDGE-CR-003) | 🟡 | ❌ | ⬜ |

---

## Notas

- Queries de PostgreSQL ejecutadas en DBeaver (via SSH tunnel)
- Queries de SQLite (Data Store) verificadas via UI — no acceso directo
- Los TCs de Canvas (TC-002, TC-024, TC-025) NO son automatizables con Playwright por limitaciones de webcomponents-flow
- Los TCs visuales (TC-052, TC-054) requieren inspección manual — no son automatizables
- 7 TCs inyectados por Code Review QA (TC-CR-001 a TC-CR-007) — requieren verificación manual
- Total automatizables: 38/69 (55%)
