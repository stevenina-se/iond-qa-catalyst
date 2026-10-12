# Release iond - v0.2.0 (beta)

> **T-04** de la tarea de Release existente en ClickUp: [86e39jadr](https://app.clickup.com/t/86e39jadr) (`Release iond - v0.2.0`). La descripción lista para pegar en ClickUp está en `ticket-86e39jadr.md`. Hoy está en `dev preparation` en la lista *Sprint 1 (9/14 - 9/20)* del folder Releases; se reutiliza y se mueve a *Sprint 5 (10/12 - 10/18)* (ver `acciones-clickup.md`).
> Preparado por el catalyst el 2026-10-10. Todos los datos se leyeron de ClickUp en **solo lectura**; los cambios en ClickUp los aplica el SM o el RM.
> Release relacionado: **Release IonMind - v1.10.2** (`knowledge/releases/ionmind/v1.10.2/`). IonMind se despliega antes que iond.

<!-- ===== INICIO: copiar en la descripción de la tarea de Release ===== -->

## Información general
| Campo | Valor |
|---|---|
| Producto / versión | iond v0.2.0 (beta) — tag de alcance `iond-beta` |
| Repos y ramas RC | `ion_gateway` · `ion_gateway_ion` · `ion_flow_binaries` · `ion_webcomponents_flow` → rama RC a definir por el RM (propuesta: `release/v0.2.0`) · repos de documentación y landing del rebranding: `ionflow_docs`, `ion_dev_documentation`, `ionflow_ionflow_landing` |
| Ambiente de validación | `preprod-app.iond.ai` |
| Tickets incluidos | **79 de iond**: 48 principales con pruebas + 1 informativa (pricing) + 30 subtareas. Los otros **5** (2 principales y 3 subtareas) van en IonMind v1.10.2. Total del tag: **84**. Detalle en `tickets-principales.csv` y `tickets.md`. |
| Riesgo | **Alto** — toca billing y consumo (enforcement local, sin Stripe), pagos del marketplace (Stripe Connect), autenticación y accesos (sesión de soporte, rebranding de login y emails), motor de ejecución (ciclo de vida, SQLite, R2, replay), contrato de API externa (DevApp API 2.0) e integraciones con IonMind y Gateway |
| Sprint · corte · Go/No-Go | Sprint 12/10–16/10 · lunes 2026-10-12 09:00 · viernes 2026-10-16 10:00 |
| Releases relacionados | Release IonMind - v1.10.2 — orden de despliegue IonMind → iond |
| Grupo de rotación capa 2 | G1 (primer release con el modelo de suites) |

## Prerrequisitos (bloqueantes)
- [ ] Repos desplegados en preprod desde el mismo commit RC; IonMind v1.10.2 desplegado antes
- [ ] Migraciones ejecutadas: monetización (ledger y enforcement locales), DevApp API 2.0 (OAuth2, accounts), replay e historial de ejecuciones, uso de tokens de Flow Pilot, backfill de endpoints duplicados de IonMind, registro de compañía
- [ ] Variables y servicios configurados (solo se verifica su existencia; los valores no se registran):
  - Stripe Connect del marketplace NOVASPHERE, con sus webhooks (el billing de la plataforma es local: sin Stripe)
  - bucket R2 de logs de ejecución
  - Reverb (websockets con token Bearer)
  - clientes OAuth2 de la DevApp API
  - VPN de la sesión de soporte
  - Logo.dev (flags de IonMind)
  - Geoapify (registro)
  - Mattermost y SMTP (notificaciones de IonMind)
  - dominios `iond.ai`, TLS, redirects 301 y remitente `hello@iond.ai`
- [ ] Datos de prueba cargados (company con plan y créditos, conectores, boards de ejemplo, plantilla PDF fija) · acceso de QA confirmado en preprod
- [ ] Company de prueba en producción (AV-09) para el smoke post-despliegue

## Suites
| Suite | Matriz / ejecución | Resultado |
|---|---|---|
| Smoke maestro (preprod) | Hoja `smoke-matrix-preprod.csv` (guía: `smoke-matrix.md`) → `smoke-preprod.md` | |
| Sanity priorizado por caso (`urgent` martes · `high` miércoles · `normal` si queda tiempo) | Hoja `sanity-matrix.csv` (guía: `sanity-matrix.md`) | |
| Regression capa 1 priorizada (`urgent` · `high` · `normal` → capa 2) + `RGR-xx` | Hoja `regression-matrix.csv` (guía: `regression-matrix.md`) | |
| E2E maestro capa 2 (automatizado + grupo G1) | `e2e-run.md` + `.csv` | |
| Smoke maestro (producción, company de prueba) | Hoja `smoke-matrix-prod.csv` → `smoke-prod.md` (después del despliegue) | |

## Hallazgos
| ID | Severidad | Fase | Decisión (fix-forward / Improvements / diferido) |
|---|---|---|---|

## Go / No-Go
Criterios del Estándar de QA §7.1 y acta C-29 (`go-no-go.md`). Se presenta la lista de lo **no ejecutado** por la priorización y las decisiones del PO de `observaciones-preparacion.md`.

## Despliegue y post-despliegue
C-30 / C-31 — `deployment-protocol.md`.

<!-- ===== FIN: copiar en la descripción de la tarea de Release ===== -->

## Alcance por área

| Área | Principales (prioridad de sanity) |
|---|---|
| Marketplace NOVASPHERE y pagos (Stripe Connect) | 86e1y463z (`urgent`, con 2 subtareas) · 86e2mc23t (`urgent`) |
| Billing y consumo (local, sin Stripe) | 86e1pzyug (`urgent`, con 6 subtareas) · 86e1m3jf8 (informativa) |
| DevApp API 2.0 | 86e1wfgam (`urgent`, con 3 subtareas) |
| Rebranding iond | 86e21f52d (`urgent`, con 7 subtareas) |
| Accesos de soporte del admin | 86e2fpp9y (`urgent`) · 86e31pbz9 (`urgent`) |
| Motor, ejecución e historial | 86e1mdnbq (`urgent`) · 86e2nazxp (`urgent`) · 86e2xnjyz (`urgent`) · 86e2ak75f (`urgent`) · 86e22fzve (`high`) · 86e2dpfek (`normal`) |
| Navegación y UI global | 86e35wv7f websockets (`urgent`) · 86e35882c (`urgent`) · 86e223kvf (`high`) |
| Flow Pilot | 86e1fawg0 (`urgent`) · 86e3085ap (`normal`) |
| App Connectors e IonMind | 86e20nmqx (`urgent`) · 86e2fazfh (`urgent`, con 2 subtareas) · 86e2mt70g (`urgent`) · 86e25dyyz (`high`) · 86e2e8gde (`high`) · 86e2g4ev0 (`high`) · 86e2p459r (`high`) · 86e2j43eg (`high`, con 4 subtareas) · 86e25j0rn (`high`) · 86e22q9h8 (`normal`) — y en IonMind v1.10.2: 86e1fknjv (`urgent`, con 3 subtareas) · 86e2t9962 (`high`) |
| Nodos del canvas | 86e22fzw2 Timer (`urgent`, con 1 subtarea) · 86e1kp55k Auto-mapper PDF (`high`) · 86e22fzvx Simple Decision (`normal`) · 86dy0bwmf Form (`normal`) · 86e22fzw6 Iterator (`normal`, con 1 subtarea) |
| PDF Templates | 86e22fzqu (`high`, con 2 subtareas) · 86e22fzut (`normal`) · 86e22fzq9 (`normal`) · 86e22q3pc (`normal`) |
| Boards y canvas | 86e2jwrvc (`high`) · 86e1gr6ug (`normal`) · 86e22fzrp (`normal`) · 86e22fzt2 (`normal`, con 2 subtareas) |
| Grapps, Webhooks, Connections, Templates y registro | 86e19dtkw (`high`) · 86e29hc1r (`high`) · 86e22fzq7 (`high`) · 86e1r2c6z (`high`) · 86e1r4bu7 (`high`) · 86e29e6jt (`normal`) · 86e04qn0d (`normal`) |

**No incluidos en las pruebas:** 86e1m3jf8 (pricing: definición sin entregable de código; el PO confirma su cierre).

## Riesgo del release (Estándar de QA §6.3)

| Nivel | Criterio | ¿Aplica? | Efecto en la regresión capa 1 |
|---|---|---|---|
| **Alto** | Toca billing o consumo, autenticación o permisos, el motor de ejecución, contratos de API o migraciones de datos | [x] | Suite extendida, **priorizada en `urgent`/`high`/`normal`** para entrar en el timebox (regla de recorte del §6.3) |
| **Medio** | Varios módulos sin reglas troncales | [ ] | — |
| **Bajo** | UI y textos | [ ] | — |

## Parámetros de las suites

| Suite | Parámetros |
|---|---|
| Smoke maestro | SMK-01…SMK-17, sin verificaciones de la versión |
| Sanity | 183 casos priorizados uno por uno: **61 `urgent`** (seguridad, dinero, integridad de datos, contratos y caminos principales; obligatorios para el GO) · **84 `high`** · **38 `normal`**. Alcance: 19 tickets completos, 17 con muestra de 1–2 criterios, 14 vía regresión, 7 interacciones `SAN-INT-01…07` |
| Regression capa 1 | 94 `urgent` + 12 RGR + 74 `high` + 71 `normal` (pasan a la capa 2) · `python -I scripts/e2e_master.py select --layer 1 --risk Alto --subcategories "App Stores,Billing,API,Boards,Execution History,Flowpilot,PDF Templates,Connections,App Connectors,Ionmind,Grapps,Webhooks,Admin,Register Company,Templates,Menu,Infra,Nodo Simple Decision,Nodo Iterator,Nodo Timer,Nodo Form" --focus knowledge/releases/iond/v0.2.0/_impact/focus.csv --out knowledge/releases/iond/v0.2.0/regression-matrix.csv` |
| E2E maestro capa 2 | 71 automáticas + 11 manuales de G1 · `python -I scripts/e2e_master.py select --layer 2 --group G1 --exclude knowledge/releases/iond/v0.2.0/regression-matrix.csv --out knowledge/releases/iond/v0.2.0/e2e-run.csv` |

## Calendario

| Día | Fecha | Actividad | Estado de la tarea | Responsable |
|---|---|---|---|---|
| Sábado y domingo | 2026-10-10 / 11 | Artefactos del catalyst · cierre del `mock testing` de websockets (86e35wv7f) · el SM aplica `acciones-clickup.md` | — | QA · SM |
| Lunes 09:00 | 2026-10-12 | Corte · merge a las ramas RC (iond e IonMind) · preprod (C-23) · pipeline (C-24) · smoke por la tarde | `dev preparation` → `unit test & ci` → `smoke` | RM · LD · QA |
| Martes | 2026-10-13 | Smoke (cierre AM, C-25) · sanity: los 61 casos `urgent` | `smoke` → `sanity` | 2 QAs |
| Miércoles | 2026-10-14 | Sanity: 84 casos `high` e interacciones; los 38 `normal` si queda tiempo · decisiones del PO sobre `observaciones-preparacion.md` (C-26) | `sanity` | 2 QAs · PO |
| Jueves | 2026-10-15 | Regresión capa 1: `urgent` (obligatoria) → `high` · capa 2 automatizada de noche · rotación G1 | `regression` | 2 QAs |
| Viernes 09:00 | 2026-10-16 | C-27 consolidado (capa 1 y capa 2, con lo no ejecutado) | `regression` | QA |
| Viernes 10:00 | 2026-10-16 | Go/No-Go (C-29) · despliegue IonMind → iond (C-30) · smoke en producción ≤ 2 h (C-31) | `ready for release` | PO + LQA + RM · DevOps · QA |

## Capacidad (2 QAs)

| Bloque | Estimación |
|---|---|
| Smoke preprod | ≈ 0,5 día-QA (5 verificaciones automatizables, el resto manual) |
| Sanity `urgent` (61 casos) | ≈ 1,5 días-QA |
| Sanity `high` (84 casos, con las interacciones) + `normal` (38, si queda tiempo) | ≈ 1,5–2 días-QA |
| Regresión `urgent` (71 filas manuales + 12 RGR + 23 automáticas) | ≈ 1,5 días-QA |
| Regresión `high` (35 filas manuales) | ≈ 0,5–0,8 días-QA, si hay tiempo |
| Rotación G1 (11 filas manuales) | ≈ 0,3 día-QA |
| **Total** | ≈ 6,5–7 días-QA, con 2 QAs entre el lunes PM y el jueves |

Lo que no entre queda como *No ejecutado — fuera de timebox* y se registra en el Go/No-Go. `normal` de la regresión pasa a la capa 2 y al release siguiente.

## Go/No-Go — quórum

Reunión obligatoria **PO + LQA + RM** (`Q-35`). El LQA no firma un GO ni un CONDITIONAL GO con un `urgent` abierto. Con la priorización, un **CONDITIONAL GO** es posible si solo quedan `high` con workaround aceptado por el PO y lo no ejecutado está documentado.

## Bugs del release (fuente canónica §7.5)

1. `urgent` → **fix-forward** en la rama RC (subtarea con `fix-forward`, C-28; decisión ≤ 4 h, fix ≤ 1 día).
2. Resto → ticket en Improvements `backlog` con `det-smoke` / `det-sanity` / `det-regression`, previa discusión con PO y LD.
3. Fix-forward fuera de plazo → revertir el ticket de la RC (`diferido`) o NO-GO.
