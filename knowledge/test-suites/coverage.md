# Cobertura de automatización del E2E maestro

> Archivo generado por `python -I scripts/e2e_master.py coverage`. No se edita a mano.

**Automatizada** = existe una spec en bot-test (`En PR`, `Ejecutable` o `Rota`). **Ejecutable** = la spec corre hoy (`En PR` o `Ejecutable`). La columna *Pending* considera solo las filas que la hoja marca como `Pending`.

## Resumen por SIDE

| SIDE | Filas | Automatizadas | % | Ejecutables | % | Pending automatizadas |
|---|---|---|---|---|---|---|
| KC | 3 | 1 | 33 % | 0 | 0 % | 1/3 (33 %) |
| ADMIN | 46 | 6 | 13 % | 0 | 0 % | 6/38 (16 %) |
| TENANT | 156 | 79 | 51 % | 71 | 46 % | 78/115 (68 %) |
| ADMIN GATEWAY | 45 | 0 | 0 % | 0 | 0 % | 0/0 (—) |
| **Total** | **250** | **86** | **34 %** | **71** | **28 %** | **85/156 (54 %)** |

## Estado de automatización

| Estado | Filas |
|---|---|
| Manual | 73 |
| Pendiente | 71 |
| En PR | 71 |
| Bloqueada | 20 |
| Rota | 15 |

## Por módulo

| SIDE | Módulo | Prefijo | Filas | Automatizadas | Ejecutables | Baseline | Rotación | Ticket(s) de automatización |
|---|---|---|---|---|---|---|---|---|
| KC | Forgot Password | `E2E-KC-AUT` | 1 | 0 | 0 | 0 | G1 | 86e2r4nqx, 86e39m0ym |
| KC | Login with SSO | `E2E-KC-AUT` | 1 | 1 | 0 | 1 | G1 | 86e2r4nqx, 86e39m0ym |
| KC | Register with SSO | `E2E-KC-AUT` | 1 | 0 | 0 | 0 | G3 | 86e2r4nqx, 86e39m0ym |
| ADMIN | Dashboard | `E2E-ADM-DSH` | 1 | 0 | 0 | 0 | G4 | — |
| ADMIN | Templates | `E2E-ADM-TPL` | 3 | 0 | 0 | 0 | G3 | 86e39kw8h |
| ADMIN | Companies | `E2E-ADM-CMP` | 6 | 3 | 0 | 1 | G2 | 86e39kx9v |
| ADMIN | Connectors | `E2E-ADM-APC` | 1 | 0 | 0 | 0 | G1 | — |
| ADMIN | Boards | `E2E-ADM-BRD` | 1 | 0 | 0 | 0 | G2 | — |
| ADMIN | Apps | `E2E-ADM-APP` | 11 | 0 | 0 | 0 | G4 | 86e39ky6f |
| ADMIN | Developers | `E2E-ADM-DEV` | 12 | 0 | 0 | 0 | G3 | 86e39kym1 |
| ADMIN | Settings | `E2E-ADM-SET` | 3 | 3 | 0 | 0 | G4 | 86e39kz87 |
| ADMIN | Billing | `E2E-ADM-BIL` | 8 | 0 | 0 | 4 | G4 | 86e39kzyb |
| TENANT | Dashboard | `E2E-TEN-DSH` | 1 | 1 | 1 | 0 | G4 | — |
| TENANT | Boards | `E2E-TEN-BRD` | 51 | 23 | 23 | 9 | G1, G2, G3, G4 | 86e39pg62, 86e3ku71p, 86e3ku75b, 86e3ku7cw, 86e3ku7hc, 86e3ku7ka, 86e3ku7p7, 86e3ku7t6, 86e3ku81d, 86e3ku849, 86e3ku856, 86e3ku877, 86e3ku89n, 86e3ku8d9, 86e3ku8j0, 86e3ku8qj, 86e3ku8uw, 86e3ku8xw, 86e3ku985 |
| TENANT | Execution History | `E2E-TEN-EXH` | 6 | 2 | 0 | 2 | G1 | 86e39pgbr |
| TENANT | Templates | `E2E-TEN-TPL` | 10 | 0 | 0 | 0 | G1 | 86e39pgn7 |
| TENANT | Webhooks | `E2E-TEN-WHK` | 6 | 2 | 0 | 0 | G4 | 86e39pgy4 |
| TENANT | Connections | `E2E-TEN-CNX` | 4 | 0 | 0 | 2 | G1 | 86e39pgy4 |
| TENANT | Persisten Data | `E2E-TEN-PDS` | 7 | 7 | 7 | 0 | G4 | 86e39phay |
| TENANT | PDF Templates | `E2E-TEN-PDF` | 19 | 19 | 19 | 4 | G4 | 86e39phnx |
| TENANT | Credentials | `E2E-TEN-CRD` | 6 | 6 | 6 | 0 | G4 | 86e39phvu |
| TENANT | App Connectors | `E2E-TEN-APC` | 20 | 4 | 0 | 3 | G1, G3, G4 | 86e39pht7 |
| TENANT | Accounts | `E2E-TEN-ACC` | 3 | 0 | 0 | 0 | G4 | — |
| TENANT | Developer Apps | `E2E-TEN-DVA` | 4 | 0 | 0 | 0 | G4 | — |
| TENANT | Catalog | `E2E-TEN-CAT` | 3 | 0 | 0 | 0 | G4 | — |
| TENANT | Notifications | `E2E-TEN-NTF` | 6 | 6 | 6 | 0 | G4 | 86e39phvu |
| TENANT | Settings | `E2E-TEN-SET` | 3 | 3 | 3 | 0 | G4 | 86e39phvu |
| TENANT | Teams | `E2E-TEN-TEA` | 4 | 4 | 4 | 0 | G4 | 86e39phvu |
| TENANT | Account | `E2E-TEN-PRF` | 2 | 1 | 1 | 0 | G4 | 86e39phvu |
| TENANT | Laanguaje | `E2E-TEN-LNG` | 1 | 1 | 1 | 0 | G4 | 86e39phvu |
| ADMIN GATEWAY | Apps | `E2E-GTW-APP` | 31 | 0 | 0 | 0 | G1, G2, G3, G4 | — |
| ADMIN GATEWAY | Customer | `E2E-GTW-CUS` | 14 | 0 | 0 | 0 | G2 | — |

## Carga de la rotación manual (capa 2)

Filas vigentes, no ejecutables y no bloqueadas que corresponden a cada grupo.

| Grupo | Filas manuales | Módulos |
|---|---|---|
| G1 | 40 | ADMIN GATEWAY › Apps, ADMIN › Connectors, KC › Forgot Password, KC › Login with SSO, TENANT › App Connectors, TENANT › Boards, TENANT › Connections, TENANT › Execution History, TENANT › Templates |
| G2 | 40 | ADMIN GATEWAY › Apps, ADMIN GATEWAY › Customer, ADMIN › Boards, ADMIN › Companies, TENANT › Boards |
| G3 | 40 | ADMIN GATEWAY › Apps, ADMIN › Developers, ADMIN › Templates, KC › Register with SSO, TENANT › App Connectors, TENANT › Boards |
| G4 | 39 | ADMIN GATEWAY › Apps, ADMIN › Apps, ADMIN › Dashboard, ADMIN › Settings, TENANT › App Connectors, TENANT › Webhooks |
