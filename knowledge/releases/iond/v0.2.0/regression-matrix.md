# Regression capa 1 — iond v0.2.0 (beta) + IonMind v1.10.2

> **Regresión de la versión, capa 1** (REL-05 · `Q-49` · fuente canónica §7.7 y §9.4 · Estándar de QA §6.3 · `knowledge/test-suites/README.md`) · Skill `skills/release/regression.md` · Comentario **C-27** (sección capa 1).
> Riesgo **Alto** → suite extendida, **priorizada** para entrar en el jueves 15/10 (regla de recorte del §6.3).
> **Hoja de ejecución:** `regression-matrix.csv`. Columnas de ejecución: ID · PRIORIDAD · SIDE · MODULE · FEATURE · CASO · RESULTADO ESPERADO · QA ASIGNADO · RESOLUCION · OBSERVACION · TICKET · PRIORIDAD BUG. Después vienen el contexto de la selección (MOTIVO, TICKETS_RELEASE, CROSS_SYSTEM) y las columnas de automatización (EJECUCION, AUTOMATIZACION, BOT_TEST_SPEC, BOT_TEST_TC), que pueden ocultarse en la hoja. Las filas `RGR-xx` van al final.
> **Criterio:** `urgent` al 100 % (baseline, foco del release y RGR). `high` tan completo como permita el timebox. `normal` pasa a la capa 2 (`e2e-run.md`) y al release siguiente; lo no ejecutado se lista en el Go/No-Go.

## Parámetros de selección

| Parámetro | Valor | Fuente |
|---|---|---|
| Iond Subcategory de los tickets | App Stores, Billing, API, Boards, Execution History, Flowpilot, PDF Templates, Connections, App Connectors, Ionmind, Grapps, Webhooks, Admin, Register Company, Templates, Menu, Infra + nodos Simple Decision, Iterator, Timer y Form | `tickets.md` |
| Módulos E2E impactados | ADM-APC, ADM-APP, ADM-BIL, ADM-BRD, ADM-CMP, ADM-DEV, ADM-TPL, GTW-APP, GTW-CUS, KC-AUT, TEN-APC, TEN-BRD, TEN-CNX, TEN-CRD, TEN-DSH, TEN-EXH, TEN-LNG, TEN-PDF, TEN-PDS, TEN-SET, TEN-TPL, TEN-WHK | `knowledge/test-suites/_config/subcategory-map.csv` |
| Foco del release | 79 filas tocadas por los tickets (`urgent` aunque en la hoja sean `Normal` o estén bloqueadas) | `_impact/focus.csv` ← `_impact/impact-map.csv` |
| Riesgo | **Alto** — billing y consumo, pagos, accesos, motor de ejecución, contrato de API, migraciones | `release-task.md` |
| Sistemas cruzados | Apps externas, Gateway, IonMind, Keycloak, Stripe | Columna `CROSS_SYSTEM` del maestro |
| Cross-system completo (mensual) | No (se cubre con las filas RGR) | Calendario |

## Priorización

Una sola escala de prioridad, la misma que usan los bugs: la PRIORIDAD de la fila es la del **release** (no la de la hoja del E2E maestro).

| PRIORIDAD | Regla | Filas | Automáticas | Manuales | Cuándo |
|---|---|---|---|---|---|
| `urgent` | Baseline + foco del release (+ nodos tocados) | 94 | 23 | 71 | Jueves AM — obligatoria para el GO |
| `urgent` (RGR) | Cross-system y contratos fuera del maestro | 12 | 0 | 12 | Jueves AM — obligatoria para el GO |
| `high` | `Urgent`/`High` de la hoja en los módulos impactados o cross-system, fuera del foco | 74 | 39 | 35 | Jueves PM |
| `normal` | Resto de la extendida | 71 | 9 | 62 | Pasa a la capa 2 (automatizado nocturno + rotación) |
| **Total** | | **251** | 71 | 180 | |

## Comandos

```bash
# Selección (desde la raíz del catalyst). Las filas RGR y el QA ASIGNADO se agregan después de la selección.
python -I scripts/e2e_master.py select --layer 1 --risk Alto \
  --subcategories "App Stores,Billing,API,Boards,Execution History,Flowpilot,PDF Templates,Connections,App Connectors,Ionmind,Grapps,Webhooks,Admin,Register Company,Templates,Menu,Infra,Nodo Simple Decision,Nodo Iterator,Nodo Timer,Nodo Form" \
  --focus knowledge/releases/iond/v0.2.0/_impact/focus.csv \
  --out knowledge/releases/iond/v0.2.0/regression-matrix.csv
```

```bash
# Automáticas urgent + high (desde ../bot-test/apps/bot-test, rama E2E, con el perfil .env.preprod cargado)
npx playwright test tests/IONFLOW/Company-ION/nodes/schedule/company-node-schedule.spec.ts tests/IONFLOW/Company-ION/boards/company-boards.spec.ts tests/IONFLOW/Company-ION/pdf-templates/company-pdf-templates.spec.ts tests/IONFLOW/Company-ION/credentials/company-credentials.spec.ts tests/IONFLOW/Company-ION/notifications/company-notifications.spec.ts tests/IONFLOW/Company-ION/settings/company-settings.spec.ts tests/IONFLOW/Company-ION/account/company-account.spec.ts tests/IONFLOW/Company-ION/language/company-language.spec.ts tests/IONFLOW/Company-ION/dashboard/company-dashboard.spec.ts tests/IONFLOW/Company-ION/persistent-data/company-persistent-data.spec.ts --config=tests/IONFLOW/playwright.ionflow.config.ts --project=ionflow-chromium -g "TC-ACCT-01|TC-BOARD-CMT-01|TC-BOARD-CMT-02|TC-BOARD-CMT-03|TC-BOARD-CMT-04|TC-BOARD-CMT-05|TC-BOARD-CMT-06|TC-BOARD-CMT-07|TC-BOARD-CMT-08|TC-BOARD-CRUD-01|TC-BOARD-CRUD-02|TC-BOARD-CRUD-03|TC-BOARD-CRUD-04|TC-BOARD-CRUD-05|TC-BOARD-CRUD-06|TC-BOARD-CRUD-07|TC-BOARD-CRUD-08|TC-BOARD-EXP-01|TC-BOARD-EXP-02|TC-BOARD-EXP-03|TC-BOARD-FP-01|TC-BOARD-FP-02|TC-BOARD-FP-03|TC-BOARD-FP-04|TC-BOARD-LIST-01|TC-BOARD-LIST-02|TC-CRED-01|TC-CRED-02|TC-CRED-03|TC-CRED-04|TC-CRED-05|TC-CRED-06|TC-DASH-01|TC-LANG-01|TC-LANG-02|TC-NODE-SCHED-01|TC-NODE-SCHED-02|TC-NODE-SCHED-03|TC-NODE-SCHED-04|TC-NODE-SCHED-05|TC-NOTIF-01|TC-PDATA-DS-01|TC-PDATA-DS-02|TC-PDATA-DS-03|TC-PDATA-DS-04|TC-PDATA-DS-05|TC-PDATA-DST-01|TC-PDATA-DST-02|TC-PDATA-DST-03|TC-PDATA-DST-04|TC-PDF-01|TC-PDF-02|TC-PDF-03|TC-PDF-04|TC-PDF-05|TC-PDF-06|TC-PDF-07|TC-PDF-08|TC-PDF-09|TC-PDF-10|TC-PDF-11|TC-PDF-12|TC-PDF-13|TC-PDF-14|TC-PDF-15|TC-PDF-16|TC-PDF-17|TC-PDF-18|TC-PDF-19|TC-PDF-20|TC-PDF-21|TC-SETT-01|TC-SETT-02|TC-SETT-03"
```

Las automáticas `normal` corren en la capa 2 (`e2e-run.md`).

## Reparto del jueves (QA ASIGNADO)

El QA ASIGNADO se reparte por módulo, equilibrando las filas manuales `urgent` y `high`; las automáticas las lanza el QA del módulo y revisa su resultado.

| MODULE | Manuales `urgent` | Manuales `high` | Filas totales | QA ASIGNADO |
|---|---|---|---|---|
| App Connectors | 11 | 9 | 20 | Mijael Rojas |
| Boards | 14 | 2 | 52 | Steve Nina |
| Customer | 7 | 7 | 14 | Steve Nina |
| Developers | 12 | 0 | 12 | Mijael Rojas |
| Templates | 1 | 9 | 13 | Steve Nina |
| Billing | 8 | 0 | 8 | Steve Nina |
| Execution History | 6 | 0 | 6 | Mijael Rojas |
| Webhooks | 0 | 6 | 6 | Mijael Rojas |
| Apps | 5 | 0 | 42 | Mijael Rojas |
| Connections | 2 | 2 | 4 | Steve Nina |
| Companies | 2 | 0 | 6 | Steve Nina |
| Forgot Password | 1 | 0 | 1 | Mijael Rojas |
| Login with SSO | 1 | 0 | 1 | Mijael Rojas |
| Register with SSO | 1 | 0 | 1 | Mijael Rojas |
| Account | 0 | 0 | 1 | Mijael Rojas |
| Connectors | 0 | 0 | 1 | Mijael Rojas |
| Credentials | 0 | 0 | 6 | Mijael Rojas |
| Dashboard | 0 | 0 | 2 | Mijael Rojas |
| Laanguaje | 0 | 0 | 1 | Mijael Rojas |
| Notifications | 0 | 0 | 6 | Mijael Rojas |
| PDF Templates | 0 | 0 | 19 | Mijael Rojas |
| Persisten Data | 0 | 0 | 7 | Mijael Rojas |
| Settings | 0 | 0 | 6 | Mijael Rojas |
| Teams | 0 | 0 | 4 | Mijael Rojas |
| RGR-01…RGR-12 | 12 | 0 | 12 | Steve Nina 6 · Mijael Rojas 6 |

Carga manual `urgent` + `high` (con RGR): Mijael Rojas 58 · Steve Nina 60 filas.

## Resumen

| Filas | Automáticas | Manuales | ✅ | ❌ | ⏭️ No ejecutado | Flujos críticos (`urgent` + RGR) |
|---|---|---|---|---|---|---|
| 251 | 71 | 180 | | | | [n]/106 |

## Filas RGR (cross-system o API/contrato fuera del maestro)

| ID | MODULE | FEATURE | CASO | RESULTADO ESPERADO | QA ASIGNADO | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|---|---|
| RGR-01 | DevApp API 2.0 (OAuth2) | Contrato de la API externa | Token client_credentials → accounts con Account-Id → action de connector → spec y render de PDF → listar y ejecutar flows; repetir desde la app de B. Precondición: Apps de la compañía A (2) y B (1) con client id/secret; connector Shipedge vinculado; seeder de PDF templates | Códigos según contrato (200/400/401/403/404/409/422); sin datos de otra compañía; respuestas sin detalles internos | Mijael Rojas | | | | |
| RGR-02 | iond ↔ Stripe Connect ↔ Gateway | Compra en el marketplace (NOVASPHERE) | Plans Studio → <gt-pricing-table> → checkout embebido → webhook Connect → invoice y subscription → notificación al seller → instalación del GRAPP; luego renovación y cancelación. Precondición: Seller Connect ACTIVE con plan publicado; buyer con tarjeta de prueba; webhook_url del seller | Direct charge con application fee; ledger y entitlement correctos; GRAPP instalado; el billing IOND de la company sin cambios | Steve Nina | | | | |
| RGR-03 | Billing local (sin Stripe) | Enforcement de consumo y emails | Consumir hasta 80 % y 100 % desde editor, live, webhook y scheduler; agotar pdf_impressions diario y ai_credits. Precondición: Company con plan y cuotas bajas de execution_time, pdf_impressions y ai_credits; inbox del contacto | Un email por umbral con 'contact us' (sin overage); 403 quota_exhausted sin borrar schedules ni webhooks; ninguna llamada a Stripe | Steve Nina | | | | |
| RGR-04 | iond ↔ IonMind | Generación de un App Connector | Elegir tier → modal de costo → Discovery con descripciones → Import Nodes (máx. 5) → reimportar → logo vía Logo.dev. Precondición: URL de documentación nueva; tiers configurados; LOGO_DEV_ENABLED=true | Un job y un cobro; descripciones persistidas; sin endpoints duplicados; atribución 'Logos provided by Logo.dev' solo si source=logo.dev | Mijael Rojas | | | | |
| RGR-05 | iond ↔ IonMind | Conectores generados (mensajería y logística) | Buscar cada conector en el catálogo y usar un endpoint en un board con una conexión de prueba. Precondición: Catálogo con los conectores de Telegram, WhatsApp, Instagram, Messenger, UPS y FedEx | Un solo conector por plataforma; endpoints con source_url; el nodo se configura sin errores | Mijael Rojas | | | | |
| RGR-06 | IonMind → Gateway → email / Mattermost | Notificación de fallo terminal de Discovery | Lanzar Discovery hasta el fallo terminal; repetir el polling del job. Precondición: URL inaccesible; MATTERMOST_WEBHOOK_URL y SMTP configurados (solo existencia) | Evento ionmind.discovery.failed tras persistir; un email y un mensaje por job; sin secretos en el payload | Mijael Rojas | | | | |
| RGR-07 | Dominios iond.ai | Rebranding de dominios, redirects y emails | Abrir app/landing/docs; URLs legacy de alpha.ionflow.io con path y query; OAuth callback de un conector; webhook entrante; email transaccional. Precondición: DNS y TLS de app, landing y docs; remitente hello@iond.ai | TLS válido; 301 sin loops conservando path y query; OAuth, CORS y webhooks sin regresión; emails con marca iond | Steve Nina | | | | |
| RGR-08 | Admin ↔ tenant (VPN) | Sesión de soporte del admin | Iniciar soporte, operar, navegar a /admin, salir con Leave company; repetir sin VPN; llamar la API de B con el usuario de A. Precondición: Admin con VPN; usuario miembro solo de la compañía A | Banner y Leave company correctos; /admin bloqueado durante la sesión; fail-closed sin VPN (403 vpn_required); 401 en la API ajena | Steve Nina | | | | |
| RGR-09 | Motor → R2 | Sincronización de ejecuciones a R2 | Ejecutar flows dev y live; esperar el cron; simular R2 no disponible. Precondición: STORAGE_SYNC_ENABLED=true; dos companies con flows | Jobs pending → done → cleaned; rutas separadas por company; reintentos hasta 5 y archivo local conservado si falla | Steve Nina | | | | |
| RGR-10 | Reverb (websockets) | Autenticación Bearer del socket | Mint del ws-token → suscripción → canal ajeno → token expirado → logout. Precondición: Usuario con sesión Keycloak; segundo usuario de otra company | 200 en broadcasting/auth; 403 ws_token_scope fuera de broadcasting; canal ajeno denegado; renovación con un reintento; socket cerrado al salir | Steve Nina | | | | |
| RGR-11 | iond → IonMind (proxy de Logo.dev) | Aislamiento del force-update de logos | Llamar force-update con el jobId de otro tenant. Precondición: Dos tenants con jobs propios | 403/404; el logo del otro tenant no cambia | Mijael Rojas | | | | |
| RGR-12 | Flow Pilot ↔ proveedor LLM | Tokens, costo y error 402 | Conversación con herramientas; retomar y borrar el chat; Flow Pilot en Gateway > Board sin créditos. Precondición: Modelo configurado; company con y sin créditos | Tokens y costo por turno y sesión correctos; soft delete conserva consumo; el 402 muestra un mensaje en vez de quedar sin respuesta | Mijael Rojas | | | | |

## Filas del E2E maestro — `urgent` — obligatoria

RESULTADO ESPERADO de todas las filas: *Sin regresión: el flujo funciona como en la versión anterior* (salvo que la hoja traiga uno propio).

| ID | SIDE | MODULE | FEATURE | CASO | QA ASIGNADO | MOTIVO | Tickets | EJECUCION | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E2E-TEN-BRD-001 | TENANT | Boards | List | Create Board > All Tools > Scheduler | Steve Nina | baseline | — | Automática | |  | | |
| E2E-TEN-BRD-030 | TENANT | Boards | List | Create Board > Preview | Steve Nina | baseline, foco del release, módulo impactado | 86e2nazxp, 86e2xnjyz, 86e35wv7f | Automática | |  | | |
| E2E-TEN-BRD-035 | TENANT | Boards | List | Create Board > Commit > Save | Steve Nina | baseline, módulo impactado | — | Automática | |  | | |
| E2E-TEN-BRD-042 | TENANT | Boards | List | Edit | Steve Nina | baseline, módulo impactado | — | Automática | |  | | |
| E2E-TEN-BRD-043 | TENANT | Boards | List | Delete | Steve Nina | baseline, módulo impactado | — | Automática | |  | | |
| E2E-TEN-BRD-046 | TENANT | Boards | List | Active-Pause | Steve Nina | baseline, foco del release, módulo impactado | 86e2nazxp | Automática | |  | | |
| E2E-TEN-BRD-049 | TENANT | Boards | List | New Board | Steve Nina | baseline, módulo impactado | — | Automática | |  | | |
| E2E-TEN-PDF-001 | TENANT | PDF Templates | New Template |  | Mijael Rojas | baseline, foco del release, módulo impactado | 86e1wfgam | Automática | |  | | |
| E2E-TEN-PDF-004 | TENANT | PDF Templates | Load Base PDF |  | Mijael Rojas | baseline, módulo impactado | — | Automática | |  | | |
| E2E-TEN-PDF-018 | TENANT | PDF Templates | Actions | Download | Mijael Rojas | baseline, módulo impactado | — | Automática | |  | | |
| E2E-TEN-PDF-019 | TENANT | PDF Templates | Actions | Preview | Mijael Rojas | baseline, módulo impactado | — | Automática | |  | | |
| E2E-TEN-BRD-038 | TENANT | Boards | List | Create Board > Export | Steve Nina | foco del release, módulo impactado | 86e21f52d | Automática | |  | | |
| E2E-TEN-BRD-040 | TENANT | Boards | List | Create Board > Flow Pilot > Chat Sessions | Steve Nina | foco del release, módulo impactado, cross-system IonMind | 86e1fawg0 | Automática | |  | | |
| E2E-TEN-BRD-041 | TENANT | Boards | List | Create Board > Flow Pilot > IA Tools | Steve Nina | foco del release, módulo impactado, cross-system IonMind | 86e1fawg0 | Automática | | Mejorar el prompt | | |
| E2E-TEN-BRD-045 | TENANT | Boards | List | Download | Steve Nina | foco del release, módulo impactado | 86e21f52d | Automática | |  | | |
| E2E-TEN-CRD-001 | TENANT | Credentials | Edit Key |  | Mijael Rojas | foco del release, módulo impactado | 86e35882c | Automática | |  | | |
| E2E-TEN-NTF-001 | TENANT | Notifications | Open |  | Mijael Rojas | foco del release | 86e35wv7f | Automática | |  | | |
| E2E-TEN-SET-001 | TENANT | Settings | Edit Comapny Info |  | Mijael Rojas | foco del release, módulo impactado | 86e35882c | Automática | |  | | |
| E2E-TEN-SET-002 | TENANT | Settings | Appearance | Dark Mode | Mijael Rojas | foco del release, módulo impactado | 86e35882c | Automática | |  | | |
| E2E-TEN-SET-003 | TENANT | Settings | Appearance | Collapse Menu | Mijael Rojas | foco del release, módulo impactado | 86e35882c | Automática | |  | | |
| E2E-TEN-PRF-001 | TENANT | Account | Update Personal Information |  | Mijael Rojas | foco del release | 86e35882c | Automática | |  | | |
| E2E-TEN-LNG-001 | TENANT | Laanguaje | Change Languaje | Verify Misings Views with i18n | Mijael Rojas | foco del release, módulo impactado | 86e35882c | Automática | |  | | |
| E2E-TEN-DSH-001 | TENANT | Dashboard |  |  | Mijael Rojas | foco del release, módulo impactado | 86e21f52d, 86e35882c | Automática | |  | | |
| E2E-KC-AUT-002 | KC | Login with SSO |  |  | Mijael Rojas | baseline, foco del release, módulo impactado, cross-system Keycloak | 86e21f52d | Manual | |  | | |
| E2E-TEN-BRD-002 | TENANT | Boards | List | Create Board > All Tools > HTTP Request | Steve Nina | baseline | — | Manual | |  | | |
| E2E-TEN-BRD-003 | TENANT | Boards | List | Create Board > All Tools > Webhook | Steve Nina | baseline | — | Manual | |  | | |
| E2E-TEN-APC-001 | TENANT | App Connectors | List | Base > Edit | Mijael Rojas | baseline, foco del release, módulo impactado | 86e2fazfh | Manual | |  | | |
| E2E-TEN-APC-005 | TENANT | App Connectors | List | Nodes > Add | Mijael Rojas | baseline, foco del release, módulo impactado | 86e2fazfh | Manual | |  | | |
| E2E-TEN-APC-013 | TENANT | App Connectors | Create | Manual Connector | Mijael Rojas | baseline, foco del release, módulo impactado | 86e1fknjv | Manual | |  | | |
| E2E-ADM-BIL-002 | ADMIN | Billing | Plans | Create Plan | Steve Nina | baseline, foco del release, módulo impactado | 86e1pzyug | Manual | | Bloqueada en la hoja: entra porque el release toca la feature | | |
| E2E-ADM-BIL-005 | ADMIN | Billing | Plans | Assign Feature > Delete Feature | Steve Nina | baseline, foco del release, módulo impactado | 86e1pzyug | Manual | | Bloqueada en la hoja: entra porque el release toca la feature | | |
| E2E-ADM-BIL-006 | ADMIN | Billing | Plans | Assign Feature > Confirm Feature | Steve Nina | baseline, foco del release, módulo impactado | 86e1pzyug | Manual | | Bloqueada en la hoja: entra porque el release toca la feature | | |
| E2E-ADM-BIL-007 | ADMIN | Billing | Plans | Assign Feature > Add Window | Steve Nina | baseline, foco del release, módulo impactado | 86e1pzyug | Manual | | Bloqueada en la hoja: entra porque el release toca la feature | | |
| E2E-TEN-EXH-001 | TENANT | Execution History | Details |  | Mijael Rojas | baseline, foco del release, módulo impactado | 86e1mdnbq, 86e1pzyug, 86e2ak75f, 86e2nazxp, 86e2xnjyz, 86e35wv7f | Manual | |  | | |
| E2E-TEN-EXH-002 | TENANT | Execution History | View Execution Logs |  | Mijael Rojas | baseline, foco del release, módulo impactado | 86e2ak75f | Manual | | Bloqueada en la hoja: entra porque el release toca la feature | | |
| E2E-TEN-CNX-001 | TENANT | Connections | Check Connection |  | Steve Nina | baseline, módulo impactado, cross-system Apps externas | — | Manual | |  | | |
| E2E-TEN-CNX-002 | TENANT | Connections | Reauthrize |  | Steve Nina | baseline, módulo impactado, cross-system Apps externas | — | Manual | |  | | |
| E2E-ADM-CMP-005 | ADMIN | Companies | List | Company > Subscription > Assign Plan | Steve Nina | baseline, foco del release, módulo impactado | 86e1pzyug | Manual | |  | | |
| E2E-KC-AUT-001 | KC | Forgot Password |  |  | Mijael Rojas | foco del release, módulo impactado, cross-system Keycloak | 86e21f52d | Manual | |  | | |
| E2E-KC-AUT-003 | KC | Register with SSO |  |  | Mijael Rojas | foco del release, módulo impactado, cross-system Keycloak | 86e21f52d | Manual | |  | | |
| E2E-TEN-BRD-005 | TENANT | Boards | List | Create Board > All Tools > Simple Desicion | Steve Nina | módulo impactado | — | Manual | | Prioritario para el siguiente sprint | | |
| E2E-TEN-BRD-006 | TENANT | Boards | List | Create Board > All Tools > Form | Steve Nina | módulo impactado | — | Manual | | Prioritario para el siguiente sprint | | |
| E2E-TEN-BRD-009 | TENANT | Boards | List | Create Board > All Tools > Iterator | Steve Nina | módulo impactado | — | Manual | |  | | |
| E2E-TEN-BRD-010 | TENANT | Boards | List | Create Board > All Tools > Timer | Steve Nina | foco del release, módulo impactado | 86e22fzw2 | Manual | |  | | |
| E2E-TEN-BRD-016 | TENANT | Boards | List | Create Board > Storage > Save | Steve Nina | foco del release | 86e2xnjyz | Manual | |  | | |
| E2E-TEN-BRD-017 | TENANT | Boards | List | Create Board > Storage > Update | Steve Nina | foco del release | 86e2xnjyz | Manual | |  | | |
| E2E-TEN-BRD-018 | TENANT | Boards | List | Create Board > Storage > Get | Steve Nina | foco del release | 86e2xnjyz | Manual | |  | | |
| E2E-TEN-BRD-019 | TENANT | Boards | List | Create Board > Storage > Delete | Steve Nina | foco del release | 86e2xnjyz | Manual | |  | | |
| E2E-TEN-BRD-020 | TENANT | Boards | List | Create Board > Storage > Check | Steve Nina | foco del release | 86e2xnjyz | Manual | |  | | |
| E2E-TEN-BRD-021 | TENANT | Boards | List | Create Board > Storage > Count | Steve Nina | foco del release | 86e2xnjyz | Manual | |  | | |
| E2E-TEN-BRD-022 | TENANT | Boards | List | Create Board > Storage > Delete All | Steve Nina | foco del release | 86e2xnjyz | Manual | |  | | |
| E2E-TEN-BRD-023 | TENANT | Boards | List | Create Board > Storage > Search | Steve Nina | foco del release | 86e2xnjyz | Manual | |  | | |
| E2E-TEN-APC-006 | TENANT | App Connectors | List | Nodes > Add Node with Ionmind | Mijael Rojas | foco del release, módulo impactado, cross-system IonMind | 86e2fazfh | Manual | |  | | |
| E2E-TEN-APC-007 | TENANT | App Connectors | List | Nodes > Versioning a Node | Mijael Rojas | foco del release, módulo impactado | 86e2fazfh | Manual | |  | | |
| E2E-TEN-APC-008 | TENANT | App Connectors | List | Nodes > Edit | Mijael Rojas | foco del release, módulo impactado | 86e2fazfh | Manual | |  | | |
| E2E-TEN-APC-009 | TENANT | App Connectors | List | Nodes > Delete | Mijael Rojas | foco del release, módulo impactado | 86e2fazfh | Manual | |  | | |
| E2E-TEN-APC-014 | TENANT | App Connectors | Create | Connector via Ionmind > Analize | Mijael Rojas | foco del release, módulo impactado, cross-system IonMind | 86e20nmqx, 86e2mt70g, 86e35wv7f | Manual | |  | | |
| E2E-TEN-APC-015 | TENANT | App Connectors | Create | Connector via Ionmind > Upload a logo via Logo.dev | Mijael Rojas | foco del release, módulo impactado, cross-system IonMind | 86e1fknjv, 86e20nmqx | Manual | |  | | |
| E2E-TEN-APC-016 | TENANT | App Connectors | Create | Endpoints via Ionmind > Verify Notifications | Mijael Rojas | foco del release, módulo impactado, cross-system IonMind | 86e20nmqx | Manual | |  | | |
| E2E-TEN-APC-020 | TENANT | App Connectors | Filters | Search | Mijael Rojas | foco del release, módulo impactado | 86e2fazfh | Manual | |  | | |
| E2E-GTW-CUS-001 | ADMIN GATEWAY | Customer | Login | Configured Channels > Grapp Instalation | Steve Nina | foco del release, módulo impactado, cross-system Gateway | 86e1y463z | Manual | |  | | |
| E2E-GTW-CUS-008 | ADMIN GATEWAY | Customer | Login | Available Market Place > Grapp Whitout Global Apps | Steve Nina | foco del release, módulo impactado, cross-system Gateway | 86e1y463z, 86e2mc23t | Manual | |  | | |
| E2E-GTW-CUS-009 | ADMIN GATEWAY | Customer | Login | Available Market Place > Grapp Whit Global Apps | Steve Nina | foco del release, módulo impactado, cross-system Gateway | 86e1y463z, 86e2mc23t | Manual | |  | | |
| E2E-GTW-CUS-010 | ADMIN GATEWAY | Customer | Login | Available Market Place > Add a Connection | Steve Nina | foco del release, módulo impactado, cross-system Gateway | 86e1y463z, 86e2mc23t | Manual | |  | | |
| E2E-GTW-CUS-011 | ADMIN GATEWAY | Customer | Login | Available Market Place > Check a Connection | Steve Nina | foco del release, módulo impactado, cross-system Gateway | 86e1y463z, 86e2mc23t | Manual | |  | | |
| E2E-GTW-CUS-012 | ADMIN GATEWAY | Customer | Login | Available Market Place > Reauthorize | Steve Nina | foco del release, módulo impactado, cross-system Gateway | 86e1y463z, 86e2mc23t | Manual | |  | | |
| E2E-GTW-CUS-013 | ADMIN GATEWAY | Customer | Login | Available Market Place > Flow/Actions Configuration | Steve Nina | foco del release, módulo impactado, cross-system Gateway | 86e1y463z, 86e2mc23t | Manual | |  | | |
| E2E-ADM-APP-003 | ADMIN | Apps | List | Grapps > Create | Mijael Rojas | foco del release, módulo impactado, cross-system Gateway | 86e1y463z | Manual | |  | | |
| E2E-ADM-APP-004 | ADMIN | Apps | List | Grapps > Edit > Edit and verify in Gateway | Mijael Rojas | foco del release, módulo impactado, cross-system Gateway | 86e1y463z | Manual | |  | | |
| E2E-ADM-APP-005 | ADMIN | Apps | List | Grapps > Configure Flow | Mijael Rojas | foco del release, módulo impactado, cross-system Gateway | 86e1y463z | Manual | |  | | |
| E2E-ADM-APP-006 | ADMIN | Apps | List | Grapps > Grapp Wizzard > With IA and without IA | Mijael Rojas | foco del release, módulo impactado, cross-system Gateway | 86e1y463z | Manual | |  | | |
| E2E-ADM-APP-010 | ADMIN | Apps | Add App | Grapps > Simple Grapp | Mijael Rojas | foco del release, módulo impactado, cross-system Gateway | 86e1y463z | Manual | |  | | |
| E2E-ADM-DEV-010 | ADMIN | Developers | List | Grapp > Enable | Mijael Rojas | foco del release, módulo impactado | 86e1wfgam | Manual | |  | | |
| E2E-ADM-DEV-011 | ADMIN | Developers | List | Grapp > Disable | Mijael Rojas | foco del release, módulo impactado | 86e1wfgam | Manual | |  | | |
| E2E-ADM-DEV-012 | ADMIN | Developers | List | Grapp > SetUp | Mijael Rojas | foco del release, módulo impactado | 86e1wfgam | Manual | |  | | |
| E2E-ADM-BIL-001 | ADMIN | Billing | Products | Sinchronize from Stripe | Steve Nina | foco del release, módulo impactado, cross-system Stripe | 86e1pzyug | Manual | | Bloqueada en la hoja: entra porque el release toca la feature | | |
| E2E-ADM-BIL-003 | ADMIN | Billing | Plans | Edit Plan | Steve Nina | foco del release, módulo impactado | 86e1pzyug | Manual | | Bloqueada en la hoja: entra porque el release toca la feature | | |
| E2E-ADM-BIL-004 | ADMIN | Billing | Plans | Delete Plan | Steve Nina | foco del release, módulo impactado | 86e1pzyug | Manual | | Bloqueada en la hoja: entra porque el release toca la feature | | |
| E2E-ADM-BIL-008 | ADMIN | Billing | Feature | Edit Feature | Steve Nina | foco del release, módulo impactado | 86e1pzyug | Manual | | Bloqueada en la hoja: entra porque el release toca la feature | | |
| E2E-TEN-EXH-003 | TENANT | Execution History | Delete |  | Mijael Rojas | foco del release, módulo impactado | 86e2ak75f | Manual | |  | | |
| E2E-TEN-EXH-004 | TENANT | Execution History | Go to Board |  | Mijael Rojas | foco del release, módulo impactado | 86e2ak75f | Manual | |  | | |
| E2E-TEN-EXH-005 | TENANT | Execution History | Columns |  | Mijael Rojas | foco del release, módulo impactado | 86e2ak75f | Manual | |  | | |
| E2E-TEN-EXH-006 | TENANT | Execution History | Filters |  | Mijael Rojas | foco del release, módulo impactado | 86e2ak75f | Manual | |  | | |
| E2E-TEN-TPL-001 | TENANT | Templates | Public Templates | Preview | Steve Nina | foco del release, módulo impactado | 86e35882c | Manual | |  | | |
| E2E-ADM-CMP-006 | ADMIN | Companies | List | Company > User > Log as a user | Steve Nina | foco del release, módulo impactado | 86e2fpp9y, 86e31pbz9 | Manual | |  | | |
| E2E-ADM-DEV-001 | ADMIN | Developers | List | Legacy > Enable | Mijael Rojas | foco del release, módulo impactado | 86e1wfgam | Manual | |  | | |
| E2E-ADM-DEV-002 | ADMIN | Developers | List | Legacy > Disable | Mijael Rojas | foco del release, módulo impactado | 86e1wfgam | Manual | |  | | |
| E2E-ADM-DEV-003 | ADMIN | Developers | List | Legacy > SetUp | Mijael Rojas | foco del release, módulo impactado | 86e1wfgam | Manual | |  | | |
| E2E-ADM-DEV-004 | ADMIN | Developers | List | Applications > Enable | Mijael Rojas | foco del release, módulo impactado | 86e1wfgam | Manual | |  | | |
| E2E-ADM-DEV-005 | ADMIN | Developers | List | Applications > Disable | Mijael Rojas | foco del release, módulo impactado | 86e1wfgam | Manual | |  | | |
| E2E-ADM-DEV-006 | ADMIN | Developers | List | Applications > SetUp | Mijael Rojas | foco del release, módulo impactado | 86e1wfgam | Manual | |  | | |
| E2E-ADM-DEV-007 | ADMIN | Developers | List | Custom > Enable | Mijael Rojas | foco del release, módulo impactado | 86e1wfgam | Manual | |  | | |
| E2E-ADM-DEV-008 | ADMIN | Developers | List | Custom > Disable | Mijael Rojas | foco del release, módulo impactado | 86e1wfgam | Manual | |  | | |
| E2E-ADM-DEV-009 | ADMIN | Developers | List | Custom > SetUp | Mijael Rojas | foco del release, módulo impactado | 86e1wfgam | Manual | |  | | |

## Filas del E2E maestro — `high` — jueves PM

Mismo RESULTADO ESPERADO que las filas `urgent`.

| ID | SIDE | MODULE | FEATURE | CASO | QA ASIGNADO | MOTIVO | Tickets | EJECUCION | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E2E-TEN-BRD-031 | TENANT | Boards | List | Create Board > Commit > Create Separate Draft | Steve Nina | módulo impactado | — | Automática | |  | | |
| E2E-TEN-BRD-032 | TENANT | Boards | List | Create Board > Commit > Create From Existing | Steve Nina | módulo impactado | — | Automática | |  | | |
| E2E-TEN-BRD-033 | TENANT | Boards | List | Create Board > Commit > Create From saved State | Steve Nina | módulo impactado | — | Automática | |  | | |
| E2E-TEN-BRD-034 | TENANT | Boards | List | Create Board > Commit > Change Separate Draft | Steve Nina | módulo impactado | — | Automática | |  | | |
| E2E-TEN-BRD-036 | TENANT | Boards | List | Create Board > Commit > Discard Changes | Steve Nina | módulo impactado | — | Automática | |  | | |
| E2E-TEN-BRD-037 | TENANT | Boards | List | Create Board > Commit > History | Steve Nina | módulo impactado | — | Automática | |  | | |
| E2E-TEN-BRD-039 | TENANT | Boards | List | Create Board > Import | Steve Nina | módulo impactado | — | Automática | |  | | |
| E2E-TEN-BRD-044 | TENANT | Boards | List | Clone | Steve Nina | módulo impactado | — | Automática | |  | | |
| E2E-TEN-BRD-047 | TENANT | Boards | List | Description > Add Description | Steve Nina | módulo impactado | — | Automática | |  | | |
| E2E-TEN-BRD-048 | TENANT | Boards | List | Preview | Steve Nina | módulo impactado | — | Automática | |  | | |
| E2E-TEN-PDF-002 | TENANT | PDF Templates | Import JSON |  | Mijael Rojas | módulo impactado | — | Automática | |  | | |
| E2E-TEN-PDF-003 | TENANT | PDF Templates | Export JSON |  | Mijael Rojas | módulo impactado | — | Automática | |  | | |
| E2E-TEN-PDF-005 | TENANT | PDF Templates | Page Size |  | Mijael Rojas | módulo impactado | — | Automática | |  | | |
| E2E-TEN-PDF-006 | TENANT | PDF Templates | Margins |  | Mijael Rojas | módulo impactado | — | Automática | |  | | |
| E2E-TEN-PDF-007 | TENANT | PDF Templates | Text |  | Mijael Rojas | módulo impactado | — | Automática | |  | | |
| E2E-TEN-PDF-008 | TENANT | PDF Templates | Multi Variable Text |  | Mijael Rojas | módulo impactado | — | Automática | |  | | |
| E2E-TEN-PDF-009 | TENANT | PDF Templates | Image |  | Mijael Rojas | módulo impactado | — | Automática | |  | | |
| E2E-TEN-PDF-010 | TENANT | PDF Templates | SVG |  | Mijael Rojas | módulo impactado | — | Automática | |  | | |
| E2E-TEN-PDF-011 | TENANT | PDF Templates | Signature |  | Mijael Rojas | módulo impactado | — | Automática | |  | | |
| E2E-TEN-PDF-012 | TENANT | PDF Templates | Table |  | Mijael Rojas | módulo impactado | — | Automática | |  | | |
| E2E-TEN-PDF-013 | TENANT | PDF Templates | Code 128 |  | Mijael Rojas | módulo impactado | — | Automática | |  | | |
| E2E-TEN-PDF-014 | TENANT | PDF Templates | Shapes |  | Mijael Rojas | módulo impactado | — | Automática | |  | | |
| E2E-TEN-PDF-015 | TENANT | PDF Templates | Dates |  | Mijael Rojas | módulo impactado | — | Automática | |  | | |
| E2E-TEN-PDF-016 | TENANT | PDF Templates | Form Controls |  | Mijael Rojas | módulo impactado | — | Automática | |  | | |
| E2E-TEN-PDF-017 | TENANT | PDF Templates | Actions | Clone | Mijael Rojas | módulo impactado | — | Automática | |  | | |
| E2E-TEN-BRD-050 | TENANT | Boards | List | Columns | Steve Nina | módulo impactado | — | Automática | |  | | |
| E2E-TEN-BRD-051 | TENANT | Boards | List | Filters | Steve Nina | módulo impactado | — | Automática | |  | | |
| E2E-TEN-PDS-001 | TENANT | Persisten Data | Data Store | Create | Mijael Rojas | módulo impactado | — | Automática | |  | | |
| E2E-TEN-PDS-002 | TENANT | Persisten Data | Data Store | Edit | Mijael Rojas | módulo impactado | — | Automática | |  | | |
| E2E-TEN-PDS-003 | TENANT | Persisten Data | Data Store | View | Mijael Rojas | módulo impactado | — | Automática | |  | | |
| E2E-TEN-PDS-004 | TENANT | Persisten Data | Data Store | Filters > Search | Mijael Rojas | módulo impactado | — | Automática | |  | | |
| E2E-TEN-PDS-005 | TENANT | Persisten Data | Data Structure | Create | Mijael Rojas | módulo impactado | — | Automática | |  | | |
| E2E-TEN-PDS-006 | TENANT | Persisten Data | Data Structure | Edit | Mijael Rojas | módulo impactado | — | Automática | |  | | |
| E2E-TEN-PDS-007 | TENANT | Persisten Data | Data Structure | Filters > Search | Mijael Rojas | módulo impactado | — | Automática | |  | | |
| E2E-TEN-CRD-002 | TENANT | Credentials | Select a Provider |  | Mijael Rojas | módulo impactado | — | Automática | |  | | |
| E2E-TEN-CRD-003 | TENANT | Credentials | Select a Model |  | Mijael Rojas | módulo impactado | — | Automática | |  | | |
| E2E-TEN-CRD-004 | TENANT | Credentials | Delete Key |  | Mijael Rojas | módulo impactado | — | Automática | |  | | |
| E2E-TEN-CRD-005 | TENANT | Credentials | Filters |  | Mijael Rojas | módulo impactado | — | Automática | |  | | |
| E2E-TEN-CRD-006 | TENANT | Credentials | Columns |  | Mijael Rojas | módulo impactado | — | Automática | |  | | |
| E2E-TEN-BRD-015 | TENANT | Boards | List | Create Board > All Tools > Agent | Steve Nina | cross-system IonMind | — | Manual | |  | | |
| E2E-TEN-BRD-029 | TENANT | Boards | List | Create Board > Tenant App > Add a node with Ionmind | Steve Nina | cross-system IonMind | — | Manual | | SS | | |
| E2E-TEN-APC-002 | TENANT | App Connectors | List | Webhooks > Add | Mijael Rojas | módulo impactado | — | Manual | |  | | |
| E2E-TEN-APC-003 | TENANT | App Connectors | List | Webhooks > Edit | Mijael Rojas | módulo impactado | — | Manual | |  | | |
| E2E-TEN-APC-004 | TENANT | App Connectors | List | Webhooks > Delete | Mijael Rojas | módulo impactado | — | Manual | |  | | |
| E2E-TEN-APC-010 | TENANT | App Connectors | List | Auth List > Add | Mijael Rojas | módulo impactado | — | Manual | |  | | |
| E2E-TEN-APC-011 | TENANT | App Connectors | List | Auth List > Edit | Mijael Rojas | módulo impactado | — | Manual | |  | | |
| E2E-TEN-APC-012 | TENANT | App Connectors | List | Auth List > Delete | Mijael Rojas | módulo impactado | — | Manual | |  | | |
| E2E-TEN-APC-017 | TENANT | App Connectors | Create | Filters > Search | Mijael Rojas | módulo impactado | — | Manual | |  | | |
| E2E-TEN-APC-018 | TENANT | App Connectors | Draft Connector |  | Mijael Rojas | módulo impactado | — | Manual | |  | | |
| E2E-TEN-APC-019 | TENANT | App Connectors | Delete Draft |  | Mijael Rojas | módulo impactado | — | Manual | |  | | |
| E2E-GTW-CUS-002 | ADMIN GATEWAY | Customer | Login | Configured Channels > Grapp Execution History | Steve Nina | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-CUS-003 | ADMIN GATEWAY | Customer | Login | Configured Channels > Grapp Check Updates | Steve Nina | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-CUS-004 | ADMIN GATEWAY | Customer | Login | Configured Channels > Grapp Edit a Flow Configuration | Steve Nina | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-CUS-005 | ADMIN GATEWAY | Customer | Login | Configured Channels > Grapp Connections | Steve Nina | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-CUS-006 | ADMIN GATEWAY | Customer | Login | Configured Channels > Grapp Schedule | Steve Nina | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-CUS-007 | ADMIN GATEWAY | Customer | Login | Configured Channels > Grapp Cron | Steve Nina | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-CUS-014 | ADMIN GATEWAY | Customer | Login | Boards > Check all nodes functionality | Steve Nina | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-TEN-TPL-002 | TENANT | Templates | Public Templates | Detials | Steve Nina | módulo impactado | — | Manual | |  | | |
| E2E-TEN-TPL-003 | TENANT | Templates | Public Templates | Use Template | Steve Nina | módulo impactado | — | Manual | |  | | |
| E2E-TEN-TPL-004 | TENANT | Templates | Public Templates | Expand Tags | Steve Nina | módulo impactado | — | Manual | |  | | |
| E2E-TEN-TPL-005 | TENANT | Templates | Public Templates | Filters | Steve Nina | módulo impactado | — | Manual | |  | | |
| E2E-TEN-TPL-006 | TENANT | Templates | Community Templates | Preview | Steve Nina | módulo impactado | — | Manual | |  | | |
| E2E-TEN-TPL-007 | TENANT | Templates | Community Templates | Detials | Steve Nina | módulo impactado | — | Manual | |  | | |
| E2E-TEN-TPL-008 | TENANT | Templates | Community Templates | Use Template | Steve Nina | módulo impactado | — | Manual | |  | | |
| E2E-TEN-TPL-009 | TENANT | Templates | Community Templates | Expand Tags | Steve Nina | módulo impactado | — | Manual | |  | | |
| E2E-TEN-TPL-010 | TENANT | Templates | Community Templates | Filters | Steve Nina | módulo impactado | — | Manual | |  | | |
| E2E-TEN-WHK-001 | TENANT | Webhooks | Active/Inactive |  | Mijael Rojas | módulo impactado | — | Manual | |  | | |
| E2E-TEN-WHK-002 | TENANT | Webhooks | Delete |  | Mijael Rojas | módulo impactado | — | Manual | |  | | |
| E2E-TEN-WHK-003 | TENANT | Webhooks | Go to Board |  | Mijael Rojas | módulo impactado | — | Manual | |  | | |
| E2E-TEN-WHK-004 | TENANT | Webhooks | Copy Path |  | Mijael Rojas | módulo impactado | — | Manual | |  | | |
| E2E-TEN-WHK-005 | TENANT | Webhooks | Filters |  | Mijael Rojas | módulo impactado | — | Manual | |  | | |
| E2E-TEN-WHK-006 | TENANT | Webhooks | Columns |  | Mijael Rojas | módulo impactado | — | Manual | |  | | |
| E2E-TEN-CNX-003 | TENANT | Connections | Delete |  | Steve Nina | módulo impactado | — | Manual | |  | | |
| E2E-TEN-CNX-004 | TENANT | Connections | Filters | Search | Steve Nina | módulo impactado | — | Manual | |  | | |

## Filas del E2E maestro — `normal` — pasa a la capa 2

OBSERVACION de todas las filas: *No se ejecuta en la capa 1: la cubre la capa 2*.

| ID | SIDE | MODULE | FEATURE | CASO | QA ASIGNADO | MOTIVO | Tickets | EJECUCION | RESOLUCION | OBSERVACION | TICKET | PRIORIDAD BUG |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E2E-TEN-NTF-002 | TENANT | Notifications | Mark As Read |  | Mijael Rojas | extendida | — | Automática | |  | | |
| E2E-TEN-NTF-003 | TENANT | Notifications | Delete |  | Mijael Rojas | extendida | — | Automática | |  | | |
| E2E-TEN-NTF-004 | TENANT | Notifications | Colums |  | Mijael Rojas | extendida | — | Automática | |  | | |
| E2E-TEN-NTF-005 | TENANT | Notifications | Filters |  | Mijael Rojas | extendida | — | Automática | |  | | |
| E2E-TEN-NTF-006 | TENANT | Notifications | All Notifications |  | Mijael Rojas | extendida | — | Automática | |  | | |
| E2E-TEN-TEA-001 | TENANT | Teams | Invite Member |  | Mijael Rojas | extendida | — | Automática | |  | | |
| E2E-TEN-TEA-002 | TENANT | Teams | Edit Invitation |  | Mijael Rojas | extendida | — | Automática | |  | | |
| E2E-TEN-TEA-003 | TENANT | Teams | Delete Invitation |  | Mijael Rojas | extendida | — | Automática | |  | | |
| E2E-TEN-TEA-004 | TENANT | Teams | Edit Permissions | Check Every Permissions | Mijael Rojas | extendida | — | Automática | |  | | |
| E2E-TEN-BRD-004 | TENANT | Boards | List | Create Board > All Tools > Webhook Response | Steve Nina | extendida | — | Manual | |  | | |
| E2E-TEN-BRD-007 | TENANT | Boards | List | Create Board > All Tools > Mapper | Steve Nina | extendida | — | Manual | |  | | |
| E2E-TEN-BRD-008 | TENANT | Boards | List | Create Board > All Tools > Aggregate | Steve Nina | extendida | — | Manual | |  | | |
| E2E-TEN-BRD-011 | TENANT | Boards | List | Create Board > All Tools > Multiple Desicion | Steve Nina | extendida | — | Manual | |  | | |
| E2E-TEN-BRD-012 | TENANT | Boards | List | Create Board > All Tools > Code | Steve Nina | extendida | — | Manual | |  | | |
| E2E-TEN-BRD-013 | TENANT | Boards | List | Create Board > All Tools > Call Component-Flow | Steve Nina | extendida | — | Manual | |  | | |
| E2E-TEN-BRD-014 | TENANT | Boards | List | Create Board > All Tools > On Call Component-Flow | Steve Nina | extendida | — | Manual | |  | | |
| E2E-TEN-BRD-024 | TENANT | Boards | List | Create Board > ION PDF > Edit Template on Canvas | Steve Nina | extendida | — | Manual | |  | | |
| E2E-TEN-BRD-025 | TENANT | Boards | List | Create Board > ION PDF > Add Template on Canvas | Steve Nina | extendida | — | Manual | |  | | |
| E2E-TEN-BRD-026 | TENANT | Boards | List | Create Board > ION PDF > Map Function | Steve Nina | extendida | — | Manual | |  | | |
| E2E-TEN-BRD-027 | TENANT | Boards | List | Create Board > ION PDF > Build a PDF | Steve Nina | extendida | — | Manual | |  | | |
| E2E-TEN-BRD-028 | TENANT | Boards | List | Create Board > Tenant App > Use a Tenant Node | Steve Nina | extendida | — | Manual | |  | | |
| E2E-ADM-TPL-001 | ADMIN | Templates | New Template | Via JSON | Steve Nina | módulo impactado | — | Manual | |  | | |
| E2E-ADM-TPL-002 | ADMIN | Templates | New Template | Import from Company | Steve Nina | módulo impactado | — | Manual | |  | | |
| E2E-ADM-TPL-003 | ADMIN | Templates | Actions | Edit | Steve Nina | módulo impactado | — | Manual | |  | | |
| E2E-ADM-CMP-001 | ADMIN | Companies | List | Company > Information | Steve Nina | módulo impactado | — | Manual | |  | | |
| E2E-ADM-CMP-002 | ADMIN | Companies | List | Company > Connectors > Migrate | Steve Nina | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-ADM-CMP-003 | ADMIN | Companies | List | Company > Connectors > Download Configuration | Steve Nina | módulo impactado | — | Manual | |  | | |
| E2E-ADM-CMP-004 | ADMIN | Companies | List | Company > Boards > Migrate | Steve Nina | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-ADM-APP-001 | ADMIN | Apps | List | Legacy > Edit | Mijael Rojas | módulo impactado | — | Manual | |  | | |
| E2E-ADM-APP-002 | ADMIN | Apps | List | Applications > Edit | Mijael Rojas | módulo impactado | — | Manual | |  | | |
| E2E-ADM-APP-007 | ADMIN | Apps | List | Custom > Edit | Mijael Rojas | módulo impactado | — | Manual | |  | | |
| E2E-ADM-APP-008 | ADMIN | Apps | Add App | Legacy | Mijael Rojas | módulo impactado | — | Manual | |  | | |
| E2E-ADM-APP-009 | ADMIN | Apps | Add App | Applications | Mijael Rojas | módulo impactado | — | Manual | |  | | |
| E2E-ADM-APP-011 | ADMIN | Apps | Add App | Custom | Mijael Rojas | módulo impactado | — | Manual | |  | | |
| E2E-ADM-SET-001 | ADMIN | Settings | Categories | Add | Mijael Rojas | extendida | — | Manual | |  | | |
| E2E-ADM-SET-002 | ADMIN | Settings | Categories | Edit | Mijael Rojas | extendida | — | Manual | |  | | |
| E2E-ADM-SET-003 | ADMIN | Settings | Categories | Delete | Mijael Rojas | extendida | — | Manual | |  | | |
| E2E-ADM-DSH-001 | ADMIN | Dashboard |  |  | Mijael Rojas | extendida | — | Manual | |  | | |
| E2E-ADM-APC-001 | ADMIN | Connectors | List |  | Mijael Rojas | módulo impactado | — | Manual | |  | | |
| E2E-ADM-BRD-001 | ADMIN | Boards | List |  | Steve Nina | módulo impactado | — | Manual | |  | | |
| E2E-GTW-APP-001 | ADMIN GATEWAY | Apps | Edit |  | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-002 | ADMIN GATEWAY | Apps | Delete |  | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-003 | ADMIN GATEWAY | Apps | New App |  | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-004 | ADMIN GATEWAY | Apps | App | Settings > Copy OAuth Key | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-005 | ADMIN GATEWAY | Apps | App | Settings > Copy App Url | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-006 | ADMIN GATEWAY | Apps | App | Settings > Set Image | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-007 | ADMIN GATEWAY | Apps | App | Services > Filter by Slug | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-008 | ADMIN GATEWAY | Apps | App | Services > Filter by Title | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-009 | ADMIN GATEWAY | Apps | App | Services > Filter by Description | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-010 | ADMIN GATEWAY | Apps | App | Services > Filter by Categories | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-011 | ADMIN GATEWAY | Apps | App | Services > Filter by Type | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-012 | ADMIN GATEWAY | Apps | App | Services > Enable/in bulk | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-013 | ADMIN GATEWAY | Apps | App | Services > Disable/in bulk | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-014 | ADMIN GATEWAY | Apps | App | Services > Enable | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-015 | ADMIN GATEWAY | Apps | App | Services > Disable | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-016 | ADMIN GATEWAY | Apps | App | Services > Edit > Set Image | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-017 | ADMIN GATEWAY | Apps | App | Services > Edit > Set Title | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-018 | ADMIN GATEWAY | Apps | App | Services > Edit > Set Details | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-019 | ADMIN GATEWAY | Apps | App | Services > Edit > Set Description | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-020 | ADMIN GATEWAY | Apps | App | Services > Edit > Set Features | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-021 | ADMIN GATEWAY | Apps | App | Services > Edit > Set Groups | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-022 | ADMIN GATEWAY | Apps | App | Services > Edit > Set Category | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-023 | ADMIN GATEWAY | Apps | App | Services > Edit > Enable Badge | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-024 | ADMIN GATEWAY | Apps | App | Services > Edit > Custom Credentials | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-025 | ADMIN GATEWAY | Apps | App | Services > Edit > Copy Cart | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-026 | ADMIN GATEWAY | Apps | App | Services > Edit > Copy Install | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-027 | ADMIN GATEWAY | Apps | App | Services > Edit > Copy Callback | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-028 | ADMIN GATEWAY | Apps | App | Services > Custom Integrations > Create | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-029 | ADMIN GATEWAY | Apps | App | Integrations > List | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-030 | ADMIN GATEWAY | Apps | App | Integrations > Claim | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |
| E2E-GTW-APP-031 | ADMIN GATEWAY | Apps | App | Go Back | Mijael Rojas | módulo impactado, cross-system Gateway | — | Manual | |  | | |

## Fallas clasificadas

| Fila | Clase | Comparación con el release anterior | Acción | TICKET |
|---|---|---|---|---|
| | 🔴 Real / 🟠 Inestable / 🟡 Ambiente / 🔵 Test desactualizado / ⚪ Dato de prueba | Pasaba en v0.1.x: sí / no | | |

## No ejecutado — fuera de timebox

Por diseño, las 71 filas `normal` no se ejecutan en la capa 1: las automáticas corren en la capa 2 y las manuales del grupo G1 en la rotación; el resto queda para los grupos G2–G4 de los releases siguientes. Si `high` no se completa el jueves, sus filas se marcan ⏭️ con el motivo.

## Hallazgos

| ID de la fila | PRIORIDAD BUG | Decisión | TICKET |
|---|---|---|---|
| | `urgent` / `high` / `normal` / `low` | Fix-forward (C-28) / Improvements con `det-regression` / diferido | |

> Un fallo de una fila `urgent` o RGR sin fix-forward verificado es NO-GO. Un test automático en rojo es un hallazgo a analizar, no un NO-GO automático.

## Borrador C-27 — sección capa 1

El C-27 completo (`comments/C-27-2026-10-16.md`) se publica el viernes antes de las 09:00; la línea de la capa 2 sale de `e2e-run.md`.

```markdown
## 🧪 REGRESSION — iond v0.2.0 + IonMind v1.10.2 — [✅ / ❌]
**Ejecutados:** [N]/180 (urgent + RGR + high) · ✅ [n] · ❌ [n] · ⏭️ [n] · **Automatizados:** [n]/62
**Hallazgos:** [ID — prioridad — decisión: fix-forward / Improvements #id / diferido]
**Evidencia / matriz:** knowledge/releases/iond/v0.2.0/regression-matrix.csv

**Capa 1 (riesgo):** urgent [n]/94 · RGR [n]/12 · high [n]/74 · flujos críticos [✅ / ❌]
**Capa 2 (E2E maestro):** automatizado [n/n] · rotación G1 [n/n] · inestables en cuarentena [n]
```
