# Release IonMind - v1.10.2

> **T-04** de la tarea de Release **a crear** en ClickUp: *Release IonMind - v1.10.2*. La crea el SM en la lista *Sprint 5 (10/12 - 10/18)* del folder Releases (ver `knowledge/releases/iond/v0.2.0/acciones-clickup.md`).
> Preparado por el catalyst el 2026-10-10. Datos leídos de ClickUp en **solo lectura**.
> Release relacionado: **Release iond - v0.2.0** (beta), en `knowledge/releases/iond/v0.2.0/`. IonMind se despliega **antes** que iond. Las suites corren una sola vez sobre el sistema integrado, y sus matrices y actas están en la carpeta de iond.

<!-- ===== INICIO: copiar en la descripción de la tarea de Release ===== -->

## Información general
| Campo | Valor |
|---|---|
| Producto / versión | IonMind v1.10.2 |
| Repos y ramas RC | `ai_ionmind` → rama RC a definir por el RM |
| Ambiente de validación | preprod, integrado con iond v0.2.0 (`preprod-app.iond.ai`) |
| Tickets propios | **5**: 86e2t9962 (minado en tiempo real, sin código) · 86e1fknjv Logo.dev, con 86e1fkxz7, 86e1fky0g y 86e1qzefc. Detalle en `tickets.md` |
| PRs de tickets de iond en `ai_ionmind` | #3 (86e20nmqx) · #11 (86e2e8gde) · #12 (86e2ft73m) · #16 (86e2p459r) · #17 (86e2j43eg) · #21 (86e2mt70g) · #25 (86e25j0rn). Se suma #8 (86e1fkxz7), que es propio |
| Riesgo | **Alto** por arrastre: cobro de la primera extracción, tiers, endpoints duplicados y notificaciones de error afectan a iond |
| Sprint · corte · Go/No-Go | Sprint 12/10–16/10 · lunes 2026-10-12 09:00 · viernes 2026-10-16 10:00 (mesa conjunta con iond) |
| Releases relacionados | Release iond - v0.2.0 — orden de despliegue IonMind → iond |

## Prerrequisitos (bloqueantes)
- [ ] RC de `ai_ionmind` desplegada en preprod antes que iond
- [ ] Variables configuradas (solo existencia): `LOGO_DEV_ENABLED`, `LOGO_DEV_AS_PRIMARY`, clave de Logo.dev, tiers y modelos de IA, notificación de errores (Gateway/Mattermost)
- [ ] Health de IonMind OK (SMK-15)

## Suites
Las suites cubren las dos versiones; los resultados se leen en la carpeta de iond:
| Suite | Matriz / ejecución |
|---|---|
| Smoke maestro (preprod) | `knowledge/releases/iond/v0.2.0/smoke-preprod.md` (SMK-15, SMK-16) |
| Sanity | `knowledge/releases/iond/v0.2.0/sanity-matrix.md`: 86e1fknjv y su familia (`urgent`), 86e2t9962 (`high`) y los tickets de iond con PR en `ai_ionmind` |
| Regression capa 1 | `knowledge/releases/iond/v0.2.0/regression-matrix.md`: RGR-04, RGR-05, RGR-06 y RGR-11 |
| E2E maestro capa 2 | `knowledge/releases/iond/v0.2.0/e2e-run.md` |

## Go / No-Go
Mesa conjunta (`knowledge/releases/iond/v0.2.0/go-no-go.md`). Si IonMind es NO-GO, iond también lo es, salvo que el PO retire de iond los tickets que dependen de IonMind.

## Despliegue y post-despliegue
C-30 / C-31 — `knowledge/releases/iond/v0.2.0/deployment-protocol.md` (paso 1).

<!-- ===== FIN: copiar en la descripción de la tarea de Release ===== -->

## Observaciones que tocan a IonMind

Detalle en `knowledge/releases/iond/v0.2.0/observaciones-preparacion.md`.

| ID | Tema |
|---|---|
| OBS-04 | 86e2t9962: resuelto reiniciando pods, sin código. Se verifica y se cierra sin merge |
| OBS-05 | 86e2p459r: rama marcada como cerrada; REQ 5 diferido a IONF-1154 |
| OBS-11 | 86e2mt70g: REQ-5 tachado pero exigido; vuelve a 3 tiers por defecto |
| OBS-16 | 86e25j0rn: dedup por caché de 10 min y notificación desde el 2.º intento |
| OBS-18 | 86e1qzefc: posible jobId cross-tenant en el proxy de force-update |
| OBS-19 | 86e2g4ev0: guard de duplicados retirado en el code review |
| OBS-20 | 86e2j43eg: conector de WhatsApp duplicado en la evidencia |
| OBS-23 | Familia Logo.dev sin veredicto de QA; source "ionmind" contra "crawler"; conflicto con `LOGO_DEV_AS_PRIMARY` |
