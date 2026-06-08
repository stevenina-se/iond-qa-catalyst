# Prioridades de Testing — Ionflow

> Este documento define el ranking de criticidad de cada área del producto para guiar la priorización de testing.

## Matriz de Prioridades por Módulo

| Módulo | Criticidad | Justificación | Impacto de falla |
|--------|-----------|---------------|-------------------|
| **Nodes (Core)** | 🔴 Crítico | Motor principal del producto. Si los nodos no funcionan, Ionflow no funciona | Producto inutilizable |
| **Boards** | 🔴 Crítico | Orquestación de nodos. La ejecución correcta de flows es el valor principal | Automatizaciones rotas, datos del cliente afectados |
| **Auth / Login** | 🟠 Alto | Sin auth no hay acceso. Afecta a todos los usuarios | Acceso bloqueado al producto |
| **Connectors** | 🟠 Alto | Integraciones con plataformas externas (Shopify, etc.). Afecta directamente al e-commerce del cliente | Datos de pedidos/inventario incorrectos, acorde a como nodo este configurado puede afectar en diferentes acciones, como cada endpoint de las apis de las apps son abstraidos en nodos es critico |
| **Execuiton History** | 🟠 Alto | Registra datos de ejecucion de cada flow |Se registra el consumo en cuanto a la ejecucion de cada flow, es importante ya que se registra el consumo en unidades de procesamiento |
| **Webhooks** | 🟠 Alto | URLs de los webhooks genericos y dedicados que fueron obtenidos en el canvas | Se puede eliminar en y perder referencia de los webhooks, debe almacenarse de forma correcta |
| **Persisten Data** | 🟠 Alto | Mini base de datos en sqlite por backend que obecede a una estructura de base de datos | Almacena datos historicos |
| **PDF Templates** | 🟠 Alto | Modulo de PDFs de ionflow donde es posible customizar un template | Estos templates son consumidos por sistemas externos por lo que se debe asegurar su correcta funcionamiento, la generacion se efectua dentro del nodo en en canva |
| **Credentials** | 🟠 Alto | Gestiona las credenciales de los usuarios para sus LLMS | Credenciales de acceso a sus LLMs |
| **Accounts** | 🟠 Alto | Gestiona los datos de las cuentas asociadas a las Companias | Cuentas que podran instalar las integraciones (GRAPPs en su mayoria) |
| **Developer Apps** | 🟠 Alto | Apps de desarrollo donde se podran vincular los accounts y gestionaran los servicies | Aplicaciones de dedarrollo en caso de fallar las integraciones instaladas (GRAPPs en su mayoria) pueden quedar inutilizables |
| **Catalog** | 🟠 Alto | Catalogo de services disponibles, aqui es posible crear nuevos services (GRAPPs en su mayoria) | Si falla no se podra crear nuevos services |
| **Billing / Subscriptions** | 🟠 Alto | Gestión de suscripciones y pagos vía Stripe. Administra tiers, estados de suscripción y webhooks | Suscripciones desincronizadas, pagos no registrados, acceso no controlado a planes |
| **Canvas (Vue Flow)** | 🟡 Medio | Interfaz visual de construcción de flows. Puede haber workarounds | UX degradada pero producto funcional |
| **User Management** | 🟡 Medio | Gestión de usuarios y permisos. Afecta operaciones administrativas | Problemas de acceso por rol |
| **Dashboard / Views** | 🟢 Bajo | Vistas informativas. Errores aquí no bloquean operaciones | Información incorrecta pero no pérdida de datos |

## Prioridades por Tipo de Test

| Tipo de Test | Prioridad | Cuándo ejecutar |
|---|---|---|
| Smoke tests (happy path) | 🔴 Siempre | En cada ticket, antes de cualquier otra cosa |
| Functional tests (AC) | 🔴 Siempre | Verificar cada Acceptance Criteria del ticket |
| Edge cases | 🟠 Alto | Después del happy path, enfocado en módulos críticos |
| API contract validation | 🟠 Alto | En cambios de endpoints, nuevos nodos, nuevos conectores |
| DB integrity | 🟠 Alto | En operaciones CRUD y ejecución de flows |
| Cross-module | 🟡 Medio | En features que tocan más de un módulo |
| Negative tests | 🟡 Medio | Validaciones, permisos, datos inválidos |
| Visual / UI | 🟢 Bajo | Solo cuando hay cambios de diseño explícitos |

## Áreas de Regresión Crítica

Estas áreas SIEMPRE deben incluirse en regresión antes de una release:

1. **Login / Auth flow** — ¿Los usuarios pueden entrar?
2. **Crear un flow** — ¿Se puede crear y guardar un flow nuevo?
3. **Agregar nodos a un flow** — ¿El canvas funciona y los nodos se conectan?
4. **Ejecutar un flow** — ¿La ejecución termina correctamente?
5. **Ver historial de ejecuciones** — ¿Los logs son correctos?
6. **Crear conexiones** — ¿Es posible crear nuevas conexiones con los diferentes metodos de autenticacion (Segun se configuro el app connector)?
7. **Crear y editar un conector** — ¿Se puede crear y editar un conector nuevo?
8. **Crear y editar un service** — ¿Se puede crear y editar un service nuevo?
9. **Crear, editar y utilizar un template** - Se puede crear, editar y utilizar un template de PDF?
---

*Este archivo se actualiza cuando cambian las prioridades del producto. Última actualización: Initial setup.*
