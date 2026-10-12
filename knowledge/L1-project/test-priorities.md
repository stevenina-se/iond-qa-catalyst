# Prioridades de Testing — Ionflow

> Este documento define el ranking de criticidad de cada área del producto para guiar la priorización de testing.

## Matriz de Prioridades por Módulo

| Módulo | Criticidad | Justificación | Impacto de falla |
|--------|-----------|---------------|-------------------|
| **Nodes (Core)** | 🔴 Crítico | Motor principal del producto. Si los nodos no funcionan, Ionflow no funciona | Producto inutilizable |
| **Boards** | 🔴 Crítico | Orquestación de nodos. La ejecución correcta de flows es el valor principal | Automatizaciones rotas, datos del cliente afectados |
| **Auth / Login** | 🟠 Alto | Sin auth no hay acceso. Afecta a todos los usuarios | Acceso bloqueado al producto |
| **Connectors** | 🟠 Alto | Integraciones con plataformas externas (Shopify, etc.). Afecta directamente al e-commerce del cliente | Datos de pedidos/inventario incorrectos, acorde a como nodo este configurado puede afectar en diferentes acciones, como cada endpoint de las apis de las apps son abstraidos en nodos es critico |
| **Execution History** | 🟠 Alto | Registra datos de ejecución de cada flow |Se registra el consumo en cuanto a la ejecución de cada flow, es importante ya que se registra el consumo en unidades de procesamiento |
| **Webhooks** | 🟠 Alto | URLs de los webhooks genericos y dedicados que fueron obtenidos en el canvas | Se puede eliminar en y perder referencia de los webhooks, debe almacenarse de forma correcta |
| **Persistent Data** | 🟠 Alto | Mini base de datos en sqlite por backend que obedece a una estructura de base de datos | Almacena datos historicos |
| **PDF Templates** | 🟠 Alto | Modulo de PDFs de ionflow donde es posible customizar un template | Estos templates son consumidos por sistemas externos por lo que se debe asegurar su correcta funcionamiento, la generación se efectua dentro del nodo en en canva |
| **Credentials** | 🟠 Alto | Gestiona las credenciales de los usuarios para sus LLMS | Credenciales de acceso a sus LLMs |
| **Accounts** | 🟠 Alto | Gestiona los datos de las cuentas asociadas a las Companias | Cuentas que podran instalar las integraciones (GRAPPs en su mayoria) |
| **Developer Apps** | 🟠 Alto | Apps de desarrollo donde se podran vincular los accounts y gestionaran los servicies | Aplicaciones de desarrollo en caso de fallar las integraciones instaladas (GRAPPs en su mayoria) pueden quedar inutilizables |
| **Catalog** | 🟠 Alto | Catalogo de services disponibles, aqui es posible crear nuevos services (GRAPPs en su mayoria) | Si falla no se podra crear nuevos services |
| **Billing / Subscriptions** | 🟠 Alto | Gestión de suscripciones y pagos vía Stripe. Administra tiers, estados de suscripción y webhooks | Suscripciones desincronizadas, pagos no registrados, acceso no controlado a planes |
| **Canvas (Vue Flow)** | 🟡 Medio | Interfaz visual de construcción de flows. Puede haber workarounds | UX degradada pero producto funcional |
| **User Management** | 🟡 Medio | Gestión de usuarios y permisos. Afecta operaciones administrativas | Problemas de acceso por rol |
| **Dashboard / Views** | 🟢 Bajo | Vistas informativas. Errores aquí no bloquean operaciones | Información incorrecta pero no pérdida de datos |

## Prioridades por tipo de prueba (SDLC)

| Tipo de prueba | Prioridad | Cuándo |
|---|---|---|
| REQ críticos de la Matriz de Requerimientos | 🔴 Siempre | `mock testing` (100 %) y `sanity` del release |
| Resto de REQ de la matriz | 🔴 Siempre | `mock testing` |
| No regresión de zonas cercanas (3 a 5 verificaciones) | 🟠 Alto | `mock testing` de cada ticket y de cada bug |
| Validación de contrato de API | 🟠 Alto | Cambios de endpoints, nodos o conectores; filas `RGR-xx` de la regresión |
| Integridad de datos en BD | 🟠 Alto | CRUD y ejecución de flows (queries desde las migraciones) |
| Cross-system (iond ↔ IonMind ↔ StageMind ↔ Gateway) | 🟡 Medio | Regresión capa 1 cuando el release toca integración, API o autenticación; completa una vez al mes |
| Negativos y permisos | 🟡 Medio | Según la matriz |
| Visual / UI | 🟢 Bajo | Solo con cambios de diseño explícitos |

> El smoke **no** se ejecuta por ticket. Es una suite única del release.

## Suites del release

Las áreas que siempre se verifican en un release ya no se listan aquí:

- **Caminos críticos (smoke):** `knowledge/test-suites/smoke-master.md` (SMK-01…SMK-17).
- **Baseline crítico de regresión:** filas con `BASELINE = sí` de `knowledge/test-suites/e2e-master.csv` (login/SSO, crear y ejecutar boards, historial, conexiones y App Connectors, plantillas PDF, consumo y billing).
- **Estrategia completa:** `knowledge/test-suites/README.md`.

La criticidad de la tabla anterior se usa para ordenar la ejecución manual dentro del timebox y para clasificar el impacto de una falla.

---

*Actualizado el 2026-10-10 con la estrategia de suites del release (Q-47 a Q-51).*
