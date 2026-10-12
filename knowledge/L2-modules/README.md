# L2 — Módulos de iond

> Cada subdirectorio contiene el conocimiento de nivel 2 de un módulo: rutas, componentes, endpoints, schema, reglas de negocio, specs de bot-test, filas del E2E maestro, impacto cruzado y edge cases.
> El módulo de un ticket se obtiene de su **Iond Subcategory** con [`knowledge/L1-project/subcategory-map.md`](../L1-project/subcategory-map.md).

## Módulos disponibles

| Carpeta | Corresponde en la app a | Prefijo(s) del E2E maestro |
|---|---|---|
| `accounts/` | Accounts (cuentas asociadas a companies) y Settings del tenant | `TEN-ACC`, `TEN-SET` |
| `auth/` | Login/SSO (Keycloak), companies, usuarios, Teams y Account | `KC-AUT`, `ADM-CMP`, `TEN-TEA`, `TEN-PRF` |
| `billing/` | Suscripciones, planes, features y consumo (Stripe) | `ADM-BIL` |
| `boards/` | Boards: lista, editor, commits, export/import, Flow Pilot, templates | `TEN-BRD`, `ADM-BRD`, `TEN-TPL`, `ADM-TPL` |
| `connections/` | **App Connectors** (definición de conectores y sus nodos) | `TEN-APC`, `ADM-APC` |
| `dashboard/` | Dashboard, notificaciones e idioma | `TEN-DSH`, `ADM-DSH`, `TEN-NTF`, `TEN-LNG` |
| `data-store/` | **Persistent Data** (Data Store y Data Structure) | `TEN-PDS` |
| `developer-apps/` | Developer Apps | `TEN-DVA`, `ADM-DEV` |
| `executions/` | **Execution History** | `TEN-EXH` |
| `integrations/` | **Connections** (conexiones activas con apps externas) | `TEN-CNX` |
| `keys/` | **Credentials** (LLM y servicios) | `TEN-CRD` |
| `nodes/` | Nodos del canvas (All Tools, Storage, ION PDF, Tenant App) | `TEN-BRD` (rutas `Create Board › …`) |
| `pdf-templates/` | PDF Templates | `TEN-PDF` |
| `services/` | Catálogo de services, Apps del admin y del Gateway | `TEN-CAT`, `ADM-APP`, `ADM-SET`, `GTW-APP`, `GTW-CUS` |
| `webhooks/` | Webhooks | `TEN-WHK` |

## Crear o actualizar un módulo

1. Copiar `_template.md` a `<módulo>/module.md`.
2. Ejecutar `skills/knowledge/update-module.md` (lee los repos `../` en solo lectura) y validar con el QA.
3. Completar *Reglas de negocio* (desde los REQ críticos de los tickets desplegados), *Specs bot-test* y *Filas E2E*.
4. Si el módulo es nuevo, agregarlo a `knowledge/test-suites/_config/modules.csv` y a `subcategory-map.csv`.

## Fuentes de contexto (solo lectura)

- `../flow_binaries` — APIs, lógica, migraciones (SQLite de ejecuciones)
- `../gateway-ion` — rutas, vistas, componentes, stores
- `../webcomponents-flow` — canvas y nodos visuales
- `../gateway` — auth y legacy (migraciones PostgreSQL)
- `../bot-test` — specs E2E existentes

## Retroalimentación post-release

Después de cada release desplegado, `skills/knowledge/update-module.md` (modo lote) actualiza los módulos de los tickets del release: rutas, endpoints, reglas de negocio, edge cases descubiertos y specs de bot-test nuevas.
