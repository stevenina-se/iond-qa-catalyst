# Protocolo de despliegue — iond v0.2.0 (beta) + IonMind v1.10.2

> **Despliegue (ACT-01) y validación post-despliegue (ACT-02)** de la fuente canónica §7.3 (`Q-33`, `Q-36`, `Q-37`, `Q-38`, `Q-39`, `Q-52`) · Skill `skills/release/deployment-protocol.md` · Comentarios **C-30** (RM) y **C-31** (QA); ante un incidente, **C-32** (hotfix).
> QA no despliega: valida. El LD/RM coordina, **DevOps ejecuta** y el PO comunica a los clientes. Solo se registran nombres de variables, nunca valores, credenciales ni URLs internas sensibles.
> Pre-armado el 2026-10-10. El RM completa ramas, commits y migraciones en el C-23 (lunes) y confirma este documento antes del Go/No-Go.

## 1. Información general

| Campo | Valor |
|---|---|
| Producto / versión | IonMind v1.10.2 → iond v0.2.0 (beta) |
| Decisión Go/No-Go | [GO / CONDITIONAL GO] — C-29 2026-10-16 |
| Ventana de despliegue | 2026-10-16, antes de las 14:00 — se acuerda con DevOps |
| Tickets incluidos · diferidos | iond 79 · IonMind 5 · diferidos [n] (ver C-29) |
| Tareas de Release relacionadas | Release iond - v0.2.0 (https://app.clickup.com/t/86e39jadr) · Release IonMind - v1.10.2 |
| Responsables (roles) | RM coordina · DevOps ejecuta · QA valida · PO comunica · LD/RM + DevOps monitorean 48 h |

## 2. Repositorios y ramas RC (merge atómico — `Q-33`)

Todos los PRs de un ticket entran a la RC juntos o ninguno. La lista de PRs por repo está en `tickets.md` § *PRs por repositorio*.

| # | Repo (`altacrest/[repo]`) | Rama RC | Commit validado en preprod | Commit a desplegar | Tickets | ✅ |
|---|---|---|---|---|---|---|
| 1 | `ai_ionmind` | [RC IonMind v1.10.2] | | igual al validado | 86e1fknjv (86e1fkxz7) · 86e20nmqx · 86e2e8gde · 86e2ft73m · 86e2p459r · 86e2j43eg · 86e2mt70g · 86e25j0rn | [ ] |
| 2 | `ion_flow_binaries` | [propuesta `release/v0.2.0`] | | igual al validado | ver `tickets.md` | [ ] |
| 3 | `ion_gateway` | [propuesta `release/v0.2.0`] | | igual al validado | ver `tickets.md` | [ ] |
| 4 | `ion_gateway_ion` | [propuesta `release/v0.2.0`] | | igual al validado | ver `tickets.md` | [ ] |
| 5 | `ion_webcomponents_flow` | [propuesta `release/v0.2.0`] | | igual al validado | ver `tickets.md` | [ ] |
| 6 | `ionflow_template_maker` | [RC] | | igual al validado | 86e22fzqu | [ ] |
| 7 | `ionflow_docs` · `ion_dev_documentation` · `ionflow_ionflow_landing` | [RC] | | igual al validado | 86e2buw7v · 86e2buw8v · 86e2czvzh (rebranding) | [ ] |

## 3. Pre-despliegue (prerrequisitos de la T-04)

- [ ] Go/No-Go con GO o CONDITIONAL GO (C-29) y quórum PO + LQA + RM.
- [ ] El commit a desplegar de cada repo es el mismo commit RC validado en preprod.
- [ ] Migraciones reversibles y con backup previo: monetización (ledger, enforcement), DevApp API 2.0 (OAuth2, accounts), replay e historial (`mode` / `trigger_type`), tokens de Flow Pilot, registro de compañía.
- [ ] **Backfill de endpoints duplicados de IonMind** (86e2g4ev0): el RM decide si corre y en qué momento (OBS-19).
- [ ] Variables nuevas configuradas en producción (sección 5).
- [ ] Dominios `iond.ai`, TLS, redirects 301 desde `alpha.ionflow.io` y remitente `hello@iond.ai` listos (rebranding).
- [ ] IonMind v1.10.2 desplegado y saludable antes de iond.
- [ ] Plan de rollback documentado en las tareas de Release y **probado en preprod** (incluidas las migraciones de billing y de historial).
- [ ] Ventana confirmada con DevOps.
- [ ] Release notes de cliente aprobadas por el PO.
- [ ] Company de prueba en producción y perfil `.env.prod-testco` disponibles para QA (AV-09). Si faltan, el smoke en producción se limita a lectura, por decisión del Go/No-Go.

## 4. Orden de despliegue

**IonMind → iond** (`Q-37`). Dentro de iond: motor y backends → app → web components → documentación y landing. El RM confirma el orden en el C-23.

| Paso | Producto / repo | Acción | Ejecuta | Verificación | ✅ |
|---|---|---|---|---|---|
| 1 | IonMind — `ai_ionmind` | Desplegar la RC v1.10.2 | DevOps | Health de IonMind · `/analyze` responde | [ ] |
| 2 | iond — `ion_flow_binaries` | Desplegar el motor | DevOps | Ejecución de un flow · logs sin 5xx | [ ] |
| 3 | iond — `ion_gateway` + `ion_gateway_ion` | Migraciones + despliegue | DevOps | Health de la API · login · logs sin 5xx | [ ] |
| 4 | iond — `ion_webcomponents_flow` · `ionflow_template_maker` | Despliegue | DevOps | La app y el editor cargan; un PDF se genera | [ ] |
| 5 | Documentación y landing | Publicación + DNS/redirects | DevOps | `landing.iond.ai` y `docs.iond.ai` con TLS; 301 desde la URL legacy | [ ] |

## 5. Variables y migraciones

Solo nombres; el RM completa los que falten. Ninguno se registra con su valor.

| Tipo | Nombre | Repo | Ticket | Reversible |
|---|---|---|---|---|
| Variable | `STORAGE_SYNC_ENABLED` + credenciales del bucket R2 | `ion_flow_binaries` | 86e1mdnbq | Sí (flag) |
| Variable | `CONSUMPTION_FLUSH_SECONDS` | `ion_flow_binaries` | 86e1pzyug | Sí |
| Variable | `VPN_ALLOWED_CIDRS` | `ion_gateway_ion` / `ion_flow_binaries` | 86e31pbz9 | Sí (fail-closed si está vacía) |
| Variable | `LOGO_DEV_ENABLED` · `LOGO_DEV_AS_PRIMARY` + clave de Logo.dev | `ai_ionmind` | 86e1fknjv | Sí (flag) |
| Variable | `MATTERMOST_WEBHOOK_URL` + SMTP | `ion_gateway` | 86e25j0rn | Sí |
| Variable | Reverb (websockets) y clientes OAuth2 de la DevApp API | `ion_gateway_ion` · `ion_gateway` | 86e35wv7f · 86e1wfgam | [RM] |
| Variable | Stripe Connect y sus webhooks (marketplace) | `ion_gateway` | 86e1y463z | [RM] |
| Variable | Geoapify (registro de compañía) | `ion_gateway_ion` | 86e1r2c6z | [RM] |
| Migración | Monetización · DevApp API 2.0 · historial y replay · tokens de Flow Pilot · registro de compañía | [RM] | 86e1pzyug · 86e1wfgam · 86e2ak75f · 86e1fawg0 · 86e1r2c6z | [RM] |
| Script de datos | Backfill de endpoints duplicados de IonMind | [RM] | 86e2g4ev0 | No: backup previo |

## 6. Despliegue ejecutado — borrador C-30 (lo publica el RM)

```markdown
## 🚀 DEPLOYED — IonMind v1.10.2 + iond v0.2.0 — 2026-10-16 [hh:mm]
**Ejecutó:** DevOps @[..] · **Coordinó:** RM @[..]
**Repos / versiones:** ai_ionmind [commit] · ion_flow_binaries [commit] · ion_gateway [commit] · ion_gateway_ion [commit] · ion_webcomponents_flow [commit] · docs/landing [commit]
**Incidencias:** ninguna / [...]
```

## 7. Validación post-despliegue (ACT-02)

### 7.1 Smoke maestro en producción (QA, ≤ 2 h)

- [ ] Iniciado dentro de las 2 h posteriores al C-30, con `templates/smoke-run.md` en modo producción → `smoke-prod.md` (skill `release/smoke`).
- [ ] Solo la **company de prueba**; datos con prefijo `autobot-smoke-`; la cuenta de administración solo en SMK-13 y SMK-14 (lectura).
- [ ] Además del smoke, en lectura: login con la marca iond, menú nuevo, Billing en el menú de usuario y redirect 301 desde la URL legacy.
- [ ] Resultado: [n/16] · core (SMK-01 a SMK-05 y SMK-15) ✅ / ❌.
- [ ] **Limpieza:** board y webhook del smoke eliminados; ningún dato `autobot-smoke-` remanente.

### 7.2 Monitoreo de 48 h (LD/RM con DevOps)

| Ventana | Qué se mira | Estado |
|---|---|---|
| 0–2 h | Health de servicios, errores 5xx, logs de despliegue, reconexión de websockets | ⬜ / ✅ / ❌ |
| 24 h | Ejecuciones de boards, consumo y bloqueos del billing local, sync a R2, jobs de IonMind y sus notificaciones, webhooks del marketplace | ⬜ / ✅ / ❌ |
| 48 h | Cierre del monitoreo; incidentes reportados por el soporte general de la empresa | ⬜ / ✅ / ❌ |

### 7.3 Borrador C-31 (lo publica QA)

```markdown
## 🔎 POST-DEPLOY — [✅ estable / ❌ incidente]
**Smoke en producción (company de prueba):** [n/16] · **Limpieza de datos:** ✅ · **Monitoreo 48 h:** [en curso / OK]
**Incidentes:** [#id hotfix]
```

## 8. Rollback

**Disparadores:** core del smoke en producción fallido · incidente `urgent` atribuible a la versión · decisión de PO + LD + RM.

1. El RM avisa a PO, LQA y DevOps: *"Rollback iniciado para iond v0.2.0 / IonMind v1.10.2"*.
2. DevOps revierte en orden inverso: documentación y landing → web components → app y backends → motor → IonMind. Si el problema es solo de iond y IonMind es compatible con v0.1.x, IonMind puede quedar en v1.10.2 (lo decide el LD).
3. Migraciones: se aplica el rollback probado en preprod (billing, API 2.0 e historial primero).
4. QA verifica la versión anterior con el core del smoke maestro en la company de prueba.
5. Se registra el incidente (sección 9) y se relaciona con las tareas de Release.
6. El RM avisa: *"Rollback completado"*.

## 9. Hotfix (incidente en producción — `Q-38`)

Ticket en Improvements (TYPE `Bug`, prioridad `urgent`, tags `hotfix` + `det-prod`, relacionado con la tarea de Release) → `to do` directo → flujo normal hasta `ready to merge` → release extraordinario `Hotfix iond - v0.2.1` o `Hotfix IonMind - v1.10.3` (tag `hotfix`) con smoke y sanity focalizado → despliegue. Autorizan el PO y el LD; ejecuta el RM. Objetivo: **≤ 24 h a producción**. Comentario de apertura **C-32**.
