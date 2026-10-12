# E2E maestro capa 2 — iond v0.2.0 (beta) + IonMind v1.10.2

> **E2E maestro como capa 2 de `regression`** (REL-05 · `Q-50` · fuente canónica §7.4 y §7.7 · `knowledge/test-suites/README.md` § *Capa 2 y rotación*) · Skill `skills/release/e2e.md` · Comentario **C-27** (sección capa 2).
> Corre **todo lo automatizado** sin supervisión (jueves noche) y la **rotación G1**, sin repetir las filas `urgent`/`high` de la capa 1. **Peso en el Go/No-Go:** una falla es un hallazgo; solo es NO-GO si es `urgent` y la provocó el release.

## Encabezado

| Campo | Valor |
|---|---|
| Producto / versión | iond v0.2.0 + IonMind v1.10.2 |
| Ambiente · build | `preprod-app.iond.ai` · commit RC del C-23 |
| Grupo de rotación de este release | **G1** |
| Grupo del release anterior | Ninguno (primer release con el modelo de suites) |
| Pendientes arrastrados del grupo | Ninguno |
| Riesgo del release | Alto, con la capa 1 **priorizada**: las filas `normal` pasan aquí. La rotación G1 conserva sus 11 filas manuales que no son `urgent` ni `high` en la capa 1 |
| Corrida automática | Jueves 2026-10-15, desde las 20:00 · perfil `.env.preprod` (solo el nombre) |
| Rotación manual | Jueves 2026-10-15 PM, si la capa 1 `high` termina; si no, viernes antes de las 09:00 · timebox ≈ 0,3 día |
| Consolidado | Viernes 2026-10-16 antes de las 09:00 |

## Comandos

```bash
# Selección (desde la raíz del catalyst)
python -I scripts/e2e_master.py select --layer 2 --group G1 \
  --exclude knowledge/releases/iond/v0.2.0/regression-matrix.csv \
  --out knowledge/releases/iond/v0.2.0/e2e-run.csv
```

```bash
# Automáticas (desde ../bot-test/apps/bot-test, rama E2E, con el perfil .env.preprod cargado)
npx playwright test tests/IONFLOW/Company-ION/nodes/schedule/company-node-schedule.spec.ts tests/IONFLOW/Company-ION/boards/company-boards.spec.ts tests/IONFLOW/Company-ION/pdf-templates/company-pdf-templates.spec.ts tests/IONFLOW/Company-ION/persistent-data/company-persistent-data.spec.ts tests/IONFLOW/Company-ION/credentials/company-credentials.spec.ts tests/IONFLOW/Company-ION/notifications/company-notifications.spec.ts tests/IONFLOW/Company-ION/settings/company-settings.spec.ts tests/IONFLOW/Company-ION/teams/company-teams.spec.ts tests/IONFLOW/Company-ION/account/company-account.spec.ts tests/IONFLOW/Company-ION/language/company-language.spec.ts tests/IONFLOW/Company-ION/dashboard/company-dashboard.spec.ts --config=tests/IONFLOW/playwright.ionflow.config.ts --project=ionflow-chromium -g "TC-ACCT-01|TC-BOARD-CMT-01|TC-BOARD-CMT-02|TC-BOARD-CMT-03|TC-BOARD-CMT-04|TC-BOARD-CMT-05|TC-BOARD-CMT-06|TC-BOARD-CMT-07|TC-BOARD-CMT-08|TC-BOARD-CRUD-01|TC-BOARD-CRUD-02|TC-BOARD-CRUD-03|TC-BOARD-CRUD-04|TC-BOARD-CRUD-05|TC-BOARD-CRUD-06|TC-BOARD-CRUD-07|TC-BOARD-CRUD-08|TC-BOARD-EXP-01|TC-BOARD-EXP-02|TC-BOARD-EXP-03|TC-BOARD-FP-01|TC-BOARD-FP-02|TC-BOARD-FP-03|TC-BOARD-FP-04|TC-BOARD-LIST-01|TC-BOARD-LIST-02|TC-CRED-01|TC-CRED-02|TC-CRED-03|TC-CRED-04|TC-CRED-05|TC-CRED-06|TC-DASH-01|TC-LANG-01|TC-LANG-02|TC-NODE-SCHED-01|TC-NODE-SCHED-02|TC-NODE-SCHED-03|TC-NODE-SCHED-04|TC-NODE-SCHED-05|TC-NOTIF-01|TC-NOTIF-02|TC-NOTIF-03|TC-NOTIF-04|TC-NOTIF-05|TC-NOTIF-06|TC-PDATA-DS-01|TC-PDATA-DS-02|TC-PDATA-DS-03|TC-PDATA-DS-04|TC-PDATA-DS-05|TC-PDATA-DST-01|TC-PDATA-DST-02|TC-PDATA-DST-03|TC-PDATA-DST-04|TC-PDF-01|TC-PDF-02|TC-PDF-03|TC-PDF-04|TC-PDF-05|TC-PDF-06|TC-PDF-07|TC-PDF-08|TC-PDF-09|TC-PDF-10|TC-PDF-11|TC-PDF-12|TC-PDF-13|TC-PDF-14|TC-PDF-15|TC-PDF-16|TC-PDF-17|TC-PDF-18|TC-PDF-19|TC-PDF-20|TC-PDF-21|TC-SETT-01|TC-SETT-02|TC-SETT-03|TC-TEAM-01|TC-TEAM-02|TC-TEAM-03|TC-TEAM-04|TC-TEAM-05"
```

Los tests `@slow` (scheduler) y `@ai` (créditos de IA) corren en esta corrida nocturna. Las automáticas que también son `urgent`/`high` en la capa 1 se re-ejecutan aquí sin costo: la comparación entre ambas corridas ayuda a detectar inestables.

## Resumen automático

| Automatizados | ✅ | ❌ | Inestables | Omitidos | Duración | Reporte HTML |
|---|---|---|---|---|---|---|
| 71 | | | | | | `apps/bot-test/test-results/[JOB_ID / local]/` |

## Filas automáticas

| ID | MODULE | FEATURE / CASO | PRIORITY (hoja) | Spec | TC | PRIORIDAD en capa 1 | RESULTADO |
|---|---|---|---|---|---|---|---|
| E2E-TEN-BRD-001 | Boards | List › Create Board > All Tools > Scheduler | Urgent | `Company-ION/nodes/schedule/company-node-schedule.spec.ts` | TC-NODE-SCHED-01, TC-NODE-SCHED-02, TC-NODE-SCHED-03, TC-NODE-SCHED-04, TC-NODE-SCHED-05 | urgent | |
| E2E-TEN-BRD-030 | Boards | List › Create Board > Preview | Urgent | `Company-ION/boards/company-boards.spec.ts` | TC-BOARD-CRUD-08 | urgent | |
| E2E-TEN-BRD-031 | Boards | List › Create Board > Commit > Create Separate Draft | Urgent | `Company-ION/boards/company-boards.spec.ts` | TC-BOARD-CMT-01 | high | |
| E2E-TEN-BRD-032 | Boards | List › Create Board > Commit > Create From Existing | Urgent | `Company-ION/boards/company-boards.spec.ts` | TC-BOARD-CMT-02 | high | |
| E2E-TEN-BRD-033 | Boards | List › Create Board > Commit > Create From saved State | Urgent | `Company-ION/boards/company-boards.spec.ts` | TC-BOARD-CMT-03 | high | |
| E2E-TEN-BRD-034 | Boards | List › Create Board > Commit > Change Separate Draft | Urgent | `Company-ION/boards/company-boards.spec.ts` | TC-BOARD-CMT-04 | high | |
| E2E-TEN-BRD-035 | Boards | List › Create Board > Commit > Save | Urgent | `Company-ION/boards/company-boards.spec.ts` | TC-BOARD-CMT-05, TC-BOARD-CMT-08 | urgent | |
| E2E-TEN-BRD-036 | Boards | List › Create Board > Commit > Discard Changes | Urgent | `Company-ION/boards/company-boards.spec.ts` | TC-BOARD-CMT-06 | high | |
| E2E-TEN-BRD-037 | Boards | List › Create Board > Commit > History | Urgent | `Company-ION/boards/company-boards.spec.ts` | TC-BOARD-CMT-07 | high | |
| E2E-TEN-BRD-038 | Boards | List › Create Board > Export | Urgent | `Company-ION/boards/company-boards.spec.ts` | TC-BOARD-EXP-01 | urgent | |
| E2E-TEN-BRD-039 | Boards | List › Create Board > Import | Urgent | `Company-ION/boards/company-boards.spec.ts` | TC-BOARD-EXP-02, TC-BOARD-EXP-03 | high | |
| E2E-TEN-BRD-040 | Boards | List › Create Board > Flow Pilot > Chat Sessions | Urgent | `Company-ION/boards/company-boards.spec.ts` | TC-BOARD-FP-01, TC-BOARD-FP-02, TC-BOARD-FP-04 | urgent | |
| E2E-TEN-BRD-041 | Boards | List › Create Board > Flow Pilot > IA Tools | Urgent | `Company-ION/boards/company-boards.spec.ts` | TC-BOARD-FP-03 | urgent | |
| E2E-TEN-BRD-042 | Boards | List › Edit | Urgent | `Company-ION/boards/company-boards.spec.ts` | TC-BOARD-CRUD-02 | urgent | |
| E2E-TEN-BRD-043 | Boards | List › Delete | Urgent | `Company-ION/boards/company-boards.spec.ts` | TC-BOARD-CRUD-03 | urgent | |
| E2E-TEN-BRD-044 | Boards | List › Clone | Urgent | `Company-ION/boards/company-boards.spec.ts` | TC-BOARD-CRUD-04 | high | |
| E2E-TEN-BRD-045 | Boards | List › Download | Urgent | `Company-ION/boards/company-boards.spec.ts` | TC-BOARD-CRUD-05 | urgent | |
| E2E-TEN-BRD-046 | Boards | List › Active-Pause | Urgent | `Company-ION/boards/company-boards.spec.ts` | TC-BOARD-CRUD-06 | urgent | |
| E2E-TEN-BRD-047 | Boards | List › Description > Add Description | Urgent | `Company-ION/boards/company-boards.spec.ts` | TC-BOARD-CRUD-07 | high | |
| E2E-TEN-BRD-048 | Boards | List › Preview | Urgent | `Company-ION/boards/company-boards.spec.ts` | TC-BOARD-CRUD-08 | high | |
| E2E-TEN-BRD-049 | Boards | List › New Board | Urgent | `Company-ION/boards/company-boards.spec.ts` | TC-BOARD-CRUD-01 | urgent | |
| E2E-TEN-PDF-001 | PDF Templates | New Template | Urgent | `Company-ION/pdf-templates/company-pdf-templates.spec.ts` | TC-PDF-01 | urgent | |
| E2E-TEN-PDF-002 | PDF Templates | Import JSON | Urgent | `Company-ION/pdf-templates/company-pdf-templates.spec.ts` | TC-PDF-02, TC-PDF-05 | high | |
| E2E-TEN-PDF-003 | PDF Templates | Export JSON | Urgent | `Company-ION/pdf-templates/company-pdf-templates.spec.ts` | TC-PDF-03 | high | |
| E2E-TEN-PDF-004 | PDF Templates | Load Base PDF | Urgent | `Company-ION/pdf-templates/company-pdf-templates.spec.ts` | TC-PDF-04 | urgent | |
| E2E-TEN-PDF-005 | PDF Templates | Page Size | Urgent | `Company-ION/pdf-templates/company-pdf-templates.spec.ts` | TC-PDF-06 | high | |
| E2E-TEN-PDF-006 | PDF Templates | Margins | Urgent | `Company-ION/pdf-templates/company-pdf-templates.spec.ts` | TC-PDF-07 | high | |
| E2E-TEN-PDF-007 | PDF Templates | Text | Urgent | `Company-ION/pdf-templates/company-pdf-templates.spec.ts` | TC-PDF-08, TC-PDF-18 | high | |
| E2E-TEN-PDF-008 | PDF Templates | Multi Variable Text | Urgent | `Company-ION/pdf-templates/company-pdf-templates.spec.ts` | TC-PDF-09, TC-PDF-18 | high | |
| E2E-TEN-PDF-009 | PDF Templates | Image | Urgent | `Company-ION/pdf-templates/company-pdf-templates.spec.ts` | TC-PDF-10 | high | |
| E2E-TEN-PDF-010 | PDF Templates | SVG | Urgent | `Company-ION/pdf-templates/company-pdf-templates.spec.ts` | TC-PDF-11 | high | |
| E2E-TEN-PDF-011 | PDF Templates | Signature | Urgent | `Company-ION/pdf-templates/company-pdf-templates.spec.ts` | TC-PDF-12 | high | |
| E2E-TEN-PDF-012 | PDF Templates | Table | Urgent | `Company-ION/pdf-templates/company-pdf-templates.spec.ts` | TC-PDF-13 | high | |
| E2E-TEN-PDF-013 | PDF Templates | Code 128 | Urgent | `Company-ION/pdf-templates/company-pdf-templates.spec.ts` | TC-PDF-14 | high | |
| E2E-TEN-PDF-014 | PDF Templates | Shapes | Urgent | `Company-ION/pdf-templates/company-pdf-templates.spec.ts` | TC-PDF-15 | high | |
| E2E-TEN-PDF-015 | PDF Templates | Dates | Urgent | `Company-ION/pdf-templates/company-pdf-templates.spec.ts` | TC-PDF-16 | high | |
| E2E-TEN-PDF-016 | PDF Templates | Form Controls | Urgent | `Company-ION/pdf-templates/company-pdf-templates.spec.ts` | TC-PDF-17 | high | |
| E2E-TEN-PDF-017 | PDF Templates | Actions › Clone | Urgent | `Company-ION/pdf-templates/company-pdf-templates.spec.ts` | TC-PDF-19 | high | |
| E2E-TEN-PDF-018 | PDF Templates | Actions › Download | Urgent | `Company-ION/pdf-templates/company-pdf-templates.spec.ts` | TC-PDF-20 | urgent | |
| E2E-TEN-PDF-019 | PDF Templates | Actions › Preview | Urgent | `Company-ION/pdf-templates/company-pdf-templates.spec.ts` | TC-PDF-21 | urgent | |
| E2E-TEN-BRD-050 | Boards | List › Columns | High | `Company-ION/boards/company-boards.spec.ts` | TC-BOARD-LIST-01 | high | |
| E2E-TEN-BRD-051 | Boards | List › Filters | High | `Company-ION/boards/company-boards.spec.ts` | TC-BOARD-LIST-02 | high | |
| E2E-TEN-PDS-001 | Persisten Data | Data Store › Create | High | `Company-ION/persistent-data/company-persistent-data.spec.ts` | TC-PDATA-DS-01 | high | |
| E2E-TEN-PDS-002 | Persisten Data | Data Store › Edit | High | `Company-ION/persistent-data/company-persistent-data.spec.ts` | TC-PDATA-DS-02 | high | |
| E2E-TEN-PDS-003 | Persisten Data | Data Store › View | High | `Company-ION/persistent-data/company-persistent-data.spec.ts` | TC-PDATA-DS-03, TC-PDATA-DS-05 | high | |
| E2E-TEN-PDS-004 | Persisten Data | Data Store › Filters > Search | High | `Company-ION/persistent-data/company-persistent-data.spec.ts` | TC-PDATA-DS-04 | high | |
| E2E-TEN-PDS-005 | Persisten Data | Data Structure › Create | High | `Company-ION/persistent-data/company-persistent-data.spec.ts` | TC-PDATA-DST-01, TC-PDATA-DST-04 | high | |
| E2E-TEN-PDS-006 | Persisten Data | Data Structure › Edit | High | `Company-ION/persistent-data/company-persistent-data.spec.ts` | TC-PDATA-DST-02 | high | |
| E2E-TEN-PDS-007 | Persisten Data | Data Structure › Filters > Search | High | `Company-ION/persistent-data/company-persistent-data.spec.ts` | TC-PDATA-DST-03 | high | |
| E2E-TEN-CRD-001 | Credentials | Edit Key | High | `Company-ION/credentials/company-credentials.spec.ts` | TC-CRED-01 | urgent | |
| E2E-TEN-CRD-002 | Credentials | Select a Provider | High | `Company-ION/credentials/company-credentials.spec.ts` | TC-CRED-02 | high | |
| E2E-TEN-CRD-003 | Credentials | Select a Model | High | `Company-ION/credentials/company-credentials.spec.ts` | TC-CRED-03 | high | |
| E2E-TEN-CRD-004 | Credentials | Delete Key | High | `Company-ION/credentials/company-credentials.spec.ts` | TC-CRED-04 | high | |
| E2E-TEN-CRD-005 | Credentials | Filters | High | `Company-ION/credentials/company-credentials.spec.ts` | TC-CRED-05 | high | |
| E2E-TEN-CRD-006 | Credentials | Columns | High | `Company-ION/credentials/company-credentials.spec.ts` | TC-CRED-06 | high | |
| E2E-TEN-NTF-001 | Notifications | Open | High | `Company-ION/notifications/company-notifications.spec.ts` | TC-NOTIF-01 | urgent | |
| E2E-TEN-NTF-002 | Notifications | Mark As Read | High | `Company-ION/notifications/company-notifications.spec.ts` | TC-NOTIF-02 | normal | |
| E2E-TEN-NTF-003 | Notifications | Delete | High | `Company-ION/notifications/company-notifications.spec.ts` | TC-NOTIF-03 | normal | |
| E2E-TEN-NTF-004 | Notifications | Colums | High | `Company-ION/notifications/company-notifications.spec.ts` | TC-NOTIF-04 | normal | |
| E2E-TEN-NTF-005 | Notifications | Filters | High | `Company-ION/notifications/company-notifications.spec.ts` | TC-NOTIF-05 | normal | |
| E2E-TEN-NTF-006 | Notifications | All Notifications | High | `Company-ION/notifications/company-notifications.spec.ts` | TC-NOTIF-06 | normal | |
| E2E-TEN-SET-001 | Settings | Edit Comapny Info | High | `Company-ION/settings/company-settings.spec.ts` | TC-SETT-01 | urgent | |
| E2E-TEN-SET-002 | Settings | Appearance › Dark Mode | High | `Company-ION/settings/company-settings.spec.ts` | TC-SETT-02 | urgent | |
| E2E-TEN-SET-003 | Settings | Appearance › Collapse Menu | High | `Company-ION/settings/company-settings.spec.ts` | TC-SETT-03 | urgent | |
| E2E-TEN-TEA-001 | Teams | Invite Member | High | `Company-ION/teams/company-teams.spec.ts` | TC-TEAM-01, TC-TEAM-05 | normal | |
| E2E-TEN-TEA-002 | Teams | Edit Invitation | High | `Company-ION/teams/company-teams.spec.ts` | TC-TEAM-02 | normal | |
| E2E-TEN-TEA-003 | Teams | Delete Invitation | High | `Company-ION/teams/company-teams.spec.ts` | TC-TEAM-03 | normal | |
| E2E-TEN-TEA-004 | Teams | Edit Permissions › Check Every Permissions | High | `Company-ION/teams/company-teams.spec.ts` | TC-TEAM-04 | normal | |
| E2E-TEN-PRF-001 | Account | Update Personal Information | High | `Company-ION/account/company-account.spec.ts` | TC-ACCT-01 | urgent | |
| E2E-TEN-LNG-001 | Laanguaje | Change Languaje › Verify Misings Views with i18n | High | `Company-ION/language/company-language.spec.ts` | TC-LANG-01, TC-LANG-02 | urgent | |
| E2E-TEN-DSH-001 | Dashboard |  | Normal | `Company-ION/dashboard/company-dashboard.spec.ts` | TC-DASH-01 | urgent | |

## Fallas clasificadas

Clases de `skills/release/regression.md`: 🔴 Real · 🟠 Inestable · 🟡 Ambiente · 🔵 Test desactualizado · ⚪ Dato de prueba.

| Fila | Test (spec › TC) | Clase | Reproducida a mano | ¿La provocó el release? | Severidad | Acción / hallazgo |
|---|---|---|---|---|---|---|
| | | | | | | |

## Cuarentena

Las pruebas inestables se ponen en cuarentena **de forma visible** y se ejecutan a mano mientras tanto. El catalyst no modifica bot-test: el cambio lo hace su responsable.

| Test | Spec | Desde | Motivo | Ejecución manual sustituta | Resultado manual |
|---|---|---|---|---|---|
| | | | | | |

## Rotación manual G1

`RESULTADO`: ✅ · ❌ · ⏭️ *No ejecutado — pasa al siguiente release del grupo*.

| ID | MODULE | FEATURE / CASO | PRIORITY (hoja) | PRIORIDAD en capa 1 | RESULTADO | Evidencia |
|---|---|---|---|---|---|---|
| E2E-TEN-BRD-004 | Boards | List › Create Board > All Tools > Webhook Response | Urgent | normal | | |
| E2E-TEN-BRD-007 | Boards | List › Create Board > All Tools > Mapper | Urgent | normal | | |
| E2E-TEN-BRD-008 | Boards | List › Create Board > All Tools > Aggregate | Urgent | normal | | |
| E2E-TEN-BRD-011 | Boards | List › Create Board > All Tools > Multiple Desicion | Urgent | normal | | |
| E2E-TEN-BRD-012 | Boards | List › Create Board > All Tools > Code | Urgent | normal | | |
| E2E-TEN-BRD-013 | Boards | List › Create Board > All Tools > Call Component-Flow | Urgent | normal | | |
| E2E-TEN-BRD-014 | Boards | List › Create Board > All Tools > On Call Component-Flow | Urgent | normal | | |
| E2E-ADM-APC-001 | Connectors | List | Low | normal | | |
| E2E-GTW-APP-007 | Apps | App › Services > Filter by Slug | Low | normal | | |
| E2E-GTW-APP-011 | Apps | App › Services > Filter by Type | Low | normal | | |
| E2E-GTW-APP-015 | Apps | App › Services > Disable | Low | normal | | |

**Rotación:** [n]/11 ejecutadas · [n] pendientes que se arrastran.

## Comparación con la corrida anterior

Primera corrida con el modelo de suites: no hay corrida anterior de la capa 2. La línea base queda registrada aquí para el release siguiente (grupo G2).

## Hallazgos

| ID | Fila | Severidad | ¿`urgent` provocado por el release? | Decisión | Ticket |
|---|---|---|---|---|---|
| | | | | | |

## Borrador C-27 — sección capa 2

```markdown
**Capa 2 (E2E maestro):** automatizado [n]/71 · rotación G1 [n]/11 · inestables en cuarentena [n]
```
