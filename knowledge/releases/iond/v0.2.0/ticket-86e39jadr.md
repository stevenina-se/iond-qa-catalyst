## Información General

| Campo | Valor |
| --- | --- |
| Producto | iond (beta) — tarea relacionada: **Release IonMind - v1.10.2** |
| Versión bajo prueba | **v0.2.0** — alcance: tickets con el tag `iond-beta` |
| Repos involucrados | `ion_gateway` · `ion_gateway_ion` · `ion_flow_binaries` · `ion_webcomponents_flow` · `ionflow_template_maker` · documentación y landing del rebranding (`ionflow_docs`, `ion_dev_documentation`, `ionflow_ionflow_landing`) · IonMind: `ai_ionmind` (RC propia, se despliega antes) |
| Rama release-candidate | `v2.1.0` (`ion_gateway`) · `v0.2.0` (demás repos) — la confirma el RM en el C-23 |
| Ambiente de validación | `preprod-app.iond.ai` |
| Nivel de riesgo | 🔴 Alto — billing y consumo, pagos del marketplace, accesos de soporte, motor de ejecución, contrato de API externa y rebranding integral |
| Calendario | Corte **lun 12/10 09:00** · smoke lun PM – mar AM · sanity mar – mié · regresión jue · **Go/No-Go vie 16/10 10:00** |
| Equipo QA | Steve Nina (LQA) · Mijael Rojas |

* * *

## Descripción

Ticket de seguimiento del **ciclo de validación QA** de la versión **v0.2.0 de iond (beta)**, desde la conformación de la release candidate hasta la aprobación Go/No-Go y el smoke en producción.

Centraliza la planificación de pruebas, la ejecución de las cuatro suites (smoke, sanity, regresión y E2E maestro), la gestión de hallazgos, los criterios de aprobación y la evidencia de validación.

Esta release incluye cambios de alto impacto que requieren cobertura exhaustiva:

*   **Rebranding integral Ionflow → iond** (86e21f52d, 7 subtareas): dominios `iond.ai` con TLS, redirects 301 desde `alpha.ionflow.io`, emails con `hello@iond.ai`, landing y guía de usuario. Los identificadores técnicos (header, realm, bucket de logs) se conservan.
*   **Motor de exposición por API — FASE 1 / DevApp API 2.0** (86e1wfgam, 3 subtareas): OAuth2 `client_credentials` con scopes, accounts con `Account-Id`, actions de connectors, render de PDF templates y ejecución de flows, con aislamiento entre compañías.
*   **Monetización unificada** (86e1pzyug, 6 subtareas): billing **local, sin Stripe** (alcance IONF-1056-B). Incluye ledger de consumo, cuotas de `execution_time`, `pdf_impressions` y `ai_credits`, bloqueo al agotarse y emails al 80 % y al 100 %.
*   **Marketplace NOVASPHERE** (86e1y463z, 2 subtareas): es la **única parte con Stripe** (Stripe Connect): checkout embebido, Plans Studio, webhooks e instalación del GRAPP. ⚠️ Su último veredicto de QA es RECHAZADO (ver *Observaciones*).
*   **Accesos de soporte del admin vía VPN** (86e2fpp9y, 86e31pbz9).
*   **Motor de ejecución:**
    *   ciclo de vida de ejecuciones (86e2nazxp);
    *   SQLite persistente (86e2xnjyz);
    *   logs en R2 (86e1mdnbq);
    *   historial y replay (86e2ak75f).
*   **Navegación:** menú reorganizado (86e35882c) y websockets con token Bearer (86e35wv7f).

**Alcance:** 84 tickets con el tag `iond-beta`.

*   **79 en esta versión:** 49 principales y 30 subtareas.
    *   Los principales son 48 con pruebas y 1 informativa: 86e1m3jf8, pricing, que queda fuera de pruebas.
*   **5 en IonMind v1.10.2:** 86e2t9962 y la familia Logo.dev, 86e1fknjv con sus 3 subtareas.
*   **Distribución de los principales:** 22 bugs, 12 nuevas funcionalidades, 8 mejoras, 6 refactors y 3 tasks.

### Documento de la versión

| Artefacto | Link |
| --- | --- |
| Tickets de la versión (84, con QA asignado) | `tickets.csv` · `tickets-principales.csv` — [link a la hoja] |
| Matriz de smoke maestro (29 casos) | `smoke-matrix-preprod.csv` · `smoke-matrix-prod.csv` — [link a la hoja] |
| Matriz de sanity (183 casos priorizados) | `sanity-matrix.csv` — [link a la hoja] |
| Matriz de regresión capa 1 (251 filas) | `regression-matrix.csv` — [link a la hoja] |
| E2E maestro capa 2 (82 filas) | `e2e-run.csv` — [link a la hoja] |
| Observaciones de preparación (28) | `observaciones-preparacion.md` |
| Acta Go/No-Go y protocolo de despliegue | `go-no-go.md` · `deployment-protocol.md` |

Ruta en el QA Catalyst: `knowledge/releases/iond/v0.2.0/`. El alcance de tickets a validar es el de `tickets.csv`, con relación nativa a esta tarea. No se duplica la tabla completa en este ticket.

* * *

## Requisitos Previos (Bloqueantes)

> ⚠️ **No iniciar la validación QA hasta que TODOS los requisitos estén cumplidos.**

- [ ] Los repos desplegados en `preprod-app.iond.ai` desde el **mismo commit** de release-candidate (merge atómico: todos los PRs de un ticket entran juntos o ninguno)
- [ ] **IonMind v1.10.2** desplegado **antes** que iond y accesible (tarea relacionada). Los tickets de iond con PR en `ai_ionmind` dependen de él
- [ ] Migraciones ejecutadas correctamente (landlord + tenants):
  - monetización (ledger y enforcement);
  - DevApp API 2.0 (OAuth2, accounts);
  - historial y replay;
  - tokens de Flow Pilot;
  - registro de compañía.
- [ ] Backfill de endpoints duplicados de IonMind decidido por el RM (86e2g4ev0)
- [ ] Variables nuevas configuradas (solo se verifica su existencia, nunca se registran valores):
  - R2 (`STORAGE_SYNC_ENABLED` + bucket);
  - `CONSUMPTION_FLUSH_SECONDS`;
  - `VPN_ALLOWED_CIDRS`;
  - Reverb;
  - clientes OAuth2;
  - Stripe Connect y sus webhooks (solo marketplace);
  - `LOGO_DEV_ENABLED` / `LOGO_DEV_AS_PRIMARY`;
  - Geoapify;
  - Mattermost y SMTP.
- [ ] Dominios `iond.ai` con TLS, redirects 301 desde `alpha.ionflow.io` y remitente `hello@iond.ai`
- [ ] Ambiente de preprod aislado — sin tráfico externo ni datos de producción en uso
- [ ] Acceso de QA al ambiente confirmado (SSO, Admin, Admin Gateway y VPN para la sesión de soporte)
- [ ] Datos de prueba cargados:
  - company con plan y créditos de IA;
  - company con cuota baja (enforcement);
  - seller de Stripe Connect en modo test;
  - 2 apps de DevApp en 2 compañías distintas;
  - plantilla `autobot-smoke-template`;
  - conectores y boards de ejemplo.
- [ ] Company de prueba en producción para el smoke post-despliegue (AV-09). No bloquea preprod; sin ella, el smoke en producción se limita a lectura

### Verificación del ambiente

| Check | Cómo verificar | Estado |
| --- | --- | --- |
| Build de `ion_gateway` / `ion_gateway_ion` | `php artisan --version` + commit hash igual al de la RC | ⬜ |
| Build de `ion_flow_binaries` | `GET /api/ok` responde con versión | ⬜ |
| Build del frontend (`ion_webcomponents_flow`) | Verificar versión en footer o `meta` tag | ⬜ |
| Build del CDN | `ion@0.2.0.js` accesible | ⬜ |
| IonMind v1.10.2 accesible | Health check de IonMind responde OK (SMK-15) | ⬜ |
| DNS y TLS | `preprod-app.iond.ai` carga con TLS válido y la marca iond | ⬜ |
| Login SSO | Login con Keycloak funcional (SMK-01) | ⬜ |
| Websockets | La campana de notificaciones recibe eventos en tiempo real | ⬜ |
| Pipeline | Pruebas unitarias en verde (C-24) | ⬜ |

* * *

## Alcance de la Validación

### Tipos de prueba incluidos

| Tipo | Objetivo | Alcance | Prioridad | Cuándo |
| --- | --- | --- | --- | --- |
| Smoke maestro | Gate de entrada: caminos críticos y salud de los servicios. Es la misma lista en todo release | 17 verificaciones fijas (29 casos), 6 de core | 🔴 Máxima (core) | Lun PM – mar AM |
| Sanity | Verificar que cada ticket de v0.2.0 cumple sus criterios críticos y que los tickets no se rompen entre sí | 183 casos priorizados uno por uno: **61 `urgent`** · 84 `high` · 38 `normal` | 🔴 Máxima (`urgent`) | Mar – mié |
| Regression capa 1 | Verificar que lo que funcionaba en v0.1.x no se rompió, seleccionado por riesgo desde el E2E maestro | 239 filas (**94 `urgent`** · 74 `high` · 71 `normal`) + **12 flujos cross-system (RGR)** | 🔴 `urgent` · 🟠 `high` | Jue |
| E2E maestro capa 2 | Todo lo automatizado + rotación manual del grupo G1, sin repetir la capa 1 | 71 automáticas + 11 manuales | 🟡 Hallazgo (NO-GO solo si es `urgent` y lo provocó el release) | Jue noche |
| Smoke en producción | Post-despliegue con la company de prueba | 29 casos (los mismos del smoke) | 🔴 Core | Vie, ≤ 2 h tras el despliegue |

### Áreas funcionales bajo prueba

Los casos de sanity incluyen los de los tickets de IonMind v1.10.2. Cada ticket lo prueba el QA que dio su veredicto; los que no tenían veredicto se asignaron para balancear.

| Área | Tickets v0.2.0 | Riesgo | Casos de sanity (`urgent` · `high` · `normal`) | Tester asignado |
| --- | --- | --- | --- | --- |
| Marketplace NOVASPHERE y pagos | 2 + 2 subtareas | 🔴 Alto — Stripe Connect; último veredicto RECHAZADO | 9 · 5 · 0 | Steve Nina |
| Billing y consumo | 2 + 6 subtareas | 🔴 Alto — enforcement y consumo local (sin Stripe) | 7 · 8 · 2 | Steve Nina |
| DevApp API 2.0 (Motor API FASE 1) | 1 + 3 subtareas | 🔴 Alto — contrato externo y aislamiento entre compañías | 3 · 4 · 2 | Mijael Rojas |
| Accesos de soporte del admin | 2 | 🔴 Alto — seguridad (VPN, aislamiento, rutas de admin) | 5 · 6 · 1 | Steve Nina · Mijael Rojas |
| Motor, ejecución e historial | 6 | 🔴 Alto — ciclo de vida, SQLite, R2, replay | 13 · 10 · 3 | Steve Nina · Mijael Rojas |
| App Connectors e IonMind | 10 + 6 subtareas | 🔴 Alto — cobro de extracción, tier, duplicados; cross-system con IonMind | 11 · 20 · 13 | Mijael Rojas · Steve Nina |
| Rebranding iond | 1 + 7 subtareas | 🟠 Medio — dominios, emails, OAuth/CORS e integraciones legacy | 4 · 6 · 5 | Mijael Rojas |
| Navegación y UI global | 3 | 🟠 Medio — menú nuevo y websockets | 5 · 7 · 2 | Steve Nina · Mijael Rojas |
| Flow Pilot | 2 | 🟠 Medio — tokens, costo y error 402 | 0 · 3 · 2 | Mijael Rojas |
| Nodos del canvas | 5 + 2 subtareas | 🟡 Bajo — bugs de v0.1.0 (Timer con revalidación) | 2 · 2 · 2 | Mijael Rojas |
| Grapps, Webhooks, Connections, Templates y registro | 7 | 🟡 Bajo — bugs y mejoras de v0.1.0; el registro de compañía es `urgent` | 2 · 5 · 2 | Steve Nina · Mijael Rojas |
| PDF Templates | 4 + 2 subtareas | 🟡 Bajo — bugs y mejoras | 0 · 2 · 1 | Steve Nina |
| Boards y canvas | 4 + 2 subtareas | 🟡 Bajo — bugs de v0.1.0 | 0 · 1 · 1 | Steve Nina |

Los tickets de riesgo bajo se cubren sobre todo con la regresión (filas del E2E maestro), no con casos de sanity propios.

* * *

## Smoke Test — Checklist Rápido

> Ejecutar **inmediatamente después** de confirmar que el ambiente está listo. Es el gate de entrada: si falla un ítem del **core**, no se inicia el sanity en el área afectada y se decide fix-forward o NO-GO.
> El smoke es el **smoke maestro**: la misma lista fija en todo release (SMK-01…SMK-17). Las features nuevas de v0.2.0 **no** se prueban aquí, sino en el sanity. Casos, datos y orden: `smoke-matrix.md`.

### Core (Bloqueante)

- [ ] **SMK-15 Health de servicios** — iond, IonMind v1.10.2 y StageMind responden OK (se ejecuta primero)
- [ ] **SMK-01 Login SSO** — Login con Keycloak en `preprod-app.iond.ai`, con la marca iond
- [ ] **SMK-02 Dashboard y navegación** — Dashboard y accesos del menú nuevo (OVERVIEW · AUTOMATE · RESOURCES · MARKETPLACE)
- [ ] **SMK-03 Crear board** — `autobot-smoke-<AAAAMMDD>` con trigger Webhook + nodo Code, guardado con commit
- [ ] **SMK-04 Ejecutar flow (Test)** — La ejecución en modo test muestra el resultado por nodo
- [ ] **SMK-05 Ejecutar flow (Production)** — Se dispara el webhook y la ejecución aparece en Execution History con consumo registrado; después se elimina el board

### Features Nuevas v0.2.0 → se validan en el sanity

Casos `urgent` del sanity que cubren lo que antes figuraba en este checklist:

| Feature | Casos `urgent` (sanity) |
| --- | --- |
| Motor API (DevApp API 2.0) | `SAN-86e1wfgam-AC-1/2` · `AC-5/6` · `AC-4/14/15` |
| Billing / consumo | `SAN-86e1pzyug-AC-B01` · `AC-B07` · `AC-STREAM` · `AC-B09/B10` · `SAN-86e1pzz9h-*` · `SAN-86e1pzz9j-AC-B15` |
| Marketplace (Stripe Connect) | `SAN-86e1y463z-AC-1` · `AC-2` · `AC-3` · `AC-6` · `REG-007` · `BUG-12-1` · `SAN-86e1y46c7-*` |
| Rebranding | `SAN-86e21f52d-AC-2` · `AC-5` · `SAN-86e2buw8v-AC-1` · `SAN-86e2buw9u-AC-1` |
| Admin Access (sesión de soporte) | `SAN-86e2fpp9y-AC-1` · `AC-4` · `AC-6` · `SAN-86e31pbz9-AC-5` · `AC-6` |
| Execution Replay | `SAN-86e2ak75f-AC-2` · `AC-NEG` |

### Integraciones (No bloqueante)

- [ ] **SMK-06 Webhooks** — El listado carga
- [ ] **SMK-07 Connections y App Connectors** — Los listados cargan (Connections ahora en Credentials)
- [ ] **SMK-08 Persistent Data** — Data Store y Data Structure
- [ ] **SMK-09 PDF Templates** — Preview de la plantilla fija
- [ ] **SMK-10 Credentials** — El listado carga
- [ ] **SMK-11 Notificaciones** — La campana abre el panel
- [ ] **SMK-12 Suscripción y consumo** — Billing en el menú de usuario, coherente con SMK-05
- [ ] **SMK-13 Admin** — Companies e información de la company (solo lectura)
- [ ] **SMK-14 Admin Gateway / Marketplace** — Listado de Apps (solo lectura)
- [ ] **SMK-16 Flow Pilot** — Consulta sobre el board del smoke, respuesta recibida (antes de eliminar el board)
- [ ] ~~SMK-17 StageMind~~ — No aplica en este release

* * *

## Regression Test — Plan de Ejecución

> **Orden real:** sanity (fase 1, martes y miércoles) → regresión capa 1 (fase 2, jueves) → cross-system y capa 2 (fase 3, jueves y noche).
> Una sola escala de prioridad, la misma de los bugs: `urgent` = obligatoria para el GO · `high` = importante · `normal` = si queda tiempo; si no, la cubre la capa 2 o el release siguiente.
> Las hojas tienen las columnas ID · PRIORIDAD · SIDE · MODULE · FEATURE · CASO · RESULTADO ESPERADO · QA ASIGNADO · RESOLUCION · OBSERVACION · TICKET · PRIORIDAD BUG. Si un caso falla, la URL del bug va en TICKET y su prioridad en PRIORIDAD BUG.

### Fase 1: Sanity — validación de los tickets v0.2.0

> **Objetivo:** Verificar que CADA ticket incluido en v0.2.0 cumple sus criterios críticos y que no se rompe al integrarse con los demás. Hoja: `sanity-matrix.csv`, ordenada por prioridad.

| Grupo | Casos | Prioridad | Estimación | Tester | Estado |
| --- | --- | --- | --- | --- | --- |
| Seguridad y aislamiento, dinero, integridad de datos, contratos críticos, caminos principales y bugs bloqueantes | 61 | 🔴 `urgent` — martes | ~12 h | Steve Nina 36 · Mijael Rojas 25 | ⬜ |
| Funcional importante, manejo de errores, flujos secundarios e interacciones entre tickets (`SAN-INT`) | 84 | 🟠 `high` — miércoles | ~14 h | Steve Nina 41 · Mijael Rojas 43 | ⬜ |
| Visual, textos y marca, mediciones, casos borde | 38 | 🟡 `normal` — si queda tiempo | ~4 h | Steve Nina 12 · Mijael Rojas 26 | ⬜ |
| Subtotal | 183 (74 son revalidaciones) | | ~30 h | | |

Si un QA termina su parte, toma casos del otro en el mismo orden de prioridad.

### Fase 2: Regression de funcionalidades heredadas (capa 1)

> **Objetivo:** Verificar que NADA que funcionaba en v0.1.x se rompió. Hoja: `regression-matrix.csv` (filas del E2E maestro; las columnas de automatización van al final). Estimación ≈ 8 min por fila manual; las automáticas se lanzan a primera hora con bot-test.

| Módulo | Filas (`urgent` · `high` · `normal`) | Prioridad | Estimación (manual) | Tester | Estado |
| --- | --- | --- | --- | --- | --- |
| Boards (canvas, nodos, commits, ejecución) | 25 · 14 · 13 (23 automáticas) | 🔴 `urgent` | 2 h | Steve Nina | ⬜ |
| App Connectors | 11 · 9 · 0 | 🔴 `urgent` | 2,5 h | Mijael Rojas | ⬜ |
| Developers (DevApp, Grapps) | 12 · 0 · 0 | 🔴 `urgent` | 1,5 h | Mijael Rojas | ⬜ |
| Billing | 8 · 0 · 0 | 🔴 `urgent` | 1 h | Steve Nina | ⬜ |
| Customer (Admin Gateway / marketplace) | 7 · 7 · 0 | 🔴 `urgent` | 2 h | Steve Nina | ⬜ |
| Execution History | 6 · 0 · 0 | 🔴 `urgent` | 1 h | Mijael Rojas | ⬜ |
| Apps (Admin) | 5 · 0 · 37 | 🔴 `urgent` | 0,5 h | Mijael Rojas | ⬜ |
| Login, Register y Forgot Password (Keycloak) | 3 · 0 · 0 | 🔴 `urgent` | 0,5 h | Mijael Rojas | ⬜ |
| Connections · Companies | 4 · 2 · 4 | 🔴 `urgent` | 1 h | Steve Nina | ⬜ |
| Templates | 1 · 9 · 3 | 🟠 `high` | 1,5 h | Steve Nina | ⬜ |
| Webhooks | 0 · 6 · 0 | 🟠 `high` | 1 h | Mijael Rojas | ⬜ |
| PDF Templates · Credentials · Persistent Data · Notifications · Settings · Dashboard · Account · Language | 12 · 27 · 9 (todas automáticas) | 🔴 `urgent` / 🟠 `high` | — (bot-test) | Mijael Rojas | ⬜ |
| Teams · Connectors | 0 · 0 · 5 | 🟡 `normal` | — (capa 2) | — | ⬜ |
| Subtotal | 239 filas: 94 `urgent` · 74 `high` · 71 `normal` | | ~14,5 h | | |

### Fase 3: Cross-system (RGR) y E2E maestro capa 2

> **Objetivo:** Verificar los flujos que cruzan iond con IonMind, Stripe Connect, Reverb, R2 y los dominios nuevos, y los contratos que no están en el E2E maestro. Las filas RGR son `urgent` (obligatorias para el GO) y van al final de `regression-matrix.csv`.

| Flujo | Descripción | Tester | Estimación | Estado |
| --- | --- | --- | --- | --- |
| RGR-01 DevApp API 2.0 | Token → accounts → action de connector → render de PDF → flows; negativo desde otra compañía | Mijael Rojas | 0,5 h | ⬜ |
| RGR-02 Compra en el marketplace | Plans Studio → checkout embebido → webhook Connect → invoice → GRAPP instalado; renovación y cancelación | Steve Nina | 0,5 h | ⬜ |
| RGR-03 Billing local | Consumo hasta el 80 % y el 100 %, emails y bloqueo 403 desde editor, live, webhook y scheduler; ninguna llamada a Stripe | Steve Nina | 0,5 h | ⬜ |
| RGR-04 Generación de conectores con IonMind | Tier → modal de costo → Discovery con descripciones → import (máx. 5) → sin duplicados → logo con Logo.dev | Mijael Rojas | 0,5 h | ⬜ |
| RGR-05 Conectores generados | Mensajería (Telegram, WhatsApp, Instagram, Messenger) y logística (UPS, FedEx) usables en un board | Mijael Rojas | 0,5 h | ⬜ |
| RGR-06 Notificaciones de error de IonMind | Fallo terminal de Discovery → email y Mattermost, sin secretos ni duplicados | Mijael Rojas | 0,5 h | ⬜ |
| RGR-07 Dominios iond.ai | TLS, 301 desde la URL legacy, emails, OAuth callbacks, CORS y webhooks entrantes | Steve Nina | 0,5 h | ⬜ |
| RGR-08 Sesión de soporte (VPN) | Inicio, banner, bloqueo de `/admin`, Leave company, fail-closed sin VPN, aislamiento de API | Steve Nina | 0,5 h | ⬜ |
| RGR-09 Sincronización a R2 | Jobs pending → done → cleaned, rutas por compañía, reintentos sin pérdida | Steve Nina | 0,5 h | ⬜ |
| RGR-10 Websockets (Reverb) | Mint del token, scope, canal ajeno, expiración y logout | Steve Nina | 0,5 h | ⬜ |
| RGR-11 Proxy de Logo.dev | `force-update` con el jobId de otro tenant → 403/404 | Mijael Rojas | 0,5 h | ⬜ |
| RGR-12 Flow Pilot | Tokens y costo por turno y sesión; error 402 en Gateway › Board | Mijael Rojas | 0,5 h | ⬜ |
| Capa 2 automatizada | 71 tests de bot-test, sin supervisión | QA de turno | Noche del jueves | ⬜ |
| Capa 2 rotación G1 | 11 filas manuales del grupo G1 | Steve Nina · Mijael Rojas | ~1,5 h | ⬜ |
| Subtotal | | | ~7,5 h | |

* * *

## Gestión de Hallazgos

### Clasificación de hallazgos

| Severidad (prioridad nativa) | Definición | Acción | Bloquea release |
| --- | --- | --- | --- |
| 🔴 `urgent` | Funcionalidad core rota, pérdida de datos, fallo de seguridad o de cobro, sin workaround | **Fix-forward** en la rama RC (subtarea con tag `fix-forward`, C-28): decisión ≤ 4 h y fix ≤ 1 día; QA re-ejecuta el caso. Si no llega a tiempo: revertir el ticket de la RC (`diferido`) o NO-GO | ✅ Sí |
| 🟠 `high` | Funcionalidad importante falla, con workaround posible | Ticket en Improvements `backlog` con su tag `det-*`, previa discusión con PO y LD. El PO acepta o no el riesgo en el Go/No-Go y se agenda el fix | ⚠️ CONDITIONAL GO |
| 🔵 `normal` y `low` | Comportamiento cosmético, UX menor | Ticket en Improvements con su tag `det-*` para un sprint siguiente | ❌ No |

- Cada caso fallido registra en su hoja la **URL del bug** (TICKET) y su **prioridad** (PRIORIDAD BUG). El bug lleva el tag de la fase (`det-smoke`, `det-sanity` o `det-regression`) y se relaciona con esta tarea.
- **Observaciones de preparación** (`observaciones-preparacion.md`, 28): el PO decide sobre ellas el **miércoles 14/10**. Cinco pueden bloquear el GO:
  - **OBS-01:** NOVASPHERE con último veredicto RECHAZADO.
  - **OBS-02:** la aprobación del billing no figura en ClickUp.
  - **OBS-05:** confirmar los PRs de 86e2p459r en la RC.
  - **OBS-18:** posible acceso a jobs de otro tenant en el proxy de Logo.dev.
  - **OBS-19:** se quitó el guard de duplicados de IonMind.

* * *

## Criterio de Aprobación (Go / No-Go)

Mesa del **viernes 16/10 a las 10:00**, conjunta con IonMind v1.10.2. Quórum obligatorio **PO + LQA + RM**; sin quórum no hay decisión. El LQA no firma un GO ni un CONDITIONAL GO con un `urgent` abierto. El acta se publica como **C-29**.

### 🟢 GO — Aprobado para producción

Se otorga GO **solo si TODOS** los siguientes criterios se cumplen:

- [ ] Smoke maestro en preprod al 100 % (SMK-17 no aplica)
- [ ] Sanity: 100 % de los **61 casos `urgent`** aprobados
- [ ] Regression capa 1: 100 % de las **94 filas `urgent`** y de los **12 flujos RGR**
- [ ] Cero hallazgos `urgent` y cero `high` abiertos
- [ ] Rollback probado en preprod y ventana acordada con DevOps (orden IonMind → iond)

### 🟡 CONDITIONAL GO — Aprobado con condiciones

Se otorga CONDITIONAL GO si:

- [ ] No hay ningún hallazgo `urgent` abierto
- [ ] Cada `high` abierto tiene el riesgo aceptado por el PO en el C-29, el workaround comunicado y el fix agendado (ticket en Improvements con versión objetivo)
- [ ] Lo no ejecutado por la priorización (casos `high`/`normal` del sanity, filas `normal` de la regresión, rotación pendiente) está documentado y aceptado por el PO
- [ ] No se cumple ninguna condición de NO-GO

### 🔴 NO-GO — Bloqueado

Se declara NO-GO si:

- [ ] Existe al menos 1 hallazgo `urgent` abierto sin fix-forward verificado ni revert del ticket (incluye los bloqueantes de NOVASPHERE si siguen abiertos y no se decide revertirlo)
- [ ] El smoke falla en ítems del core
- [ ] Los prerrequisitos o el rollback no están verificados
- [ ] El PO no acepta el riesgo de un `high` abierto
- [ ] IonMind v1.10.2 es NO-GO, salvo que el PO retire de iond los tickets que dependen de IonMind

Con NO-GO la tarea permanece en `regression` y se reprograma su fecha de vencimiento al siguiente Go/No-Go.

* * *

## Criterios de Aceptación del Ciclo de QA

- [ ] Ambiente `preprod-app.iond.ai` verificado (builds, migraciones, variables, IonMind v1.10.2) — C-23 (RM) y C-24 (LD)
- [ ] Smoke maestro en preprod ejecutado — C-25
- [ ] Sanity ejecutado por prioridad, con las decisiones del PO sobre las observaciones de preparación — C-26
- [ ] Regresión capa 1 (incluidas las 12 RGR) y E2E maestro capa 2 ejecutados — C-27 consolidado antes de las 09:00 del viernes
- [ ] Todos los hallazgos reportados, clasificados y gestionados (TICKET y PRIORIDAD BUG completos en las hojas)
- [ ] Decisión Go/No-Go tomada y documentada — C-29
- [ ] Despliegue ejecutado por DevOps (C-30) y smoke maestro en producción con la company de prueba en ≤ 2 h, con limpieza de datos — C-31
- [ ] Tickets del release en `merged` en su kanban, con sus subtareas siguiendo al padre
- [ ] Reporte final de QA publicado como comentario en esta tarea
