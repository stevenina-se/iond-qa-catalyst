# Protocolo de despliegue — [producto] v[X.Y.Z]

> **Plantilla del QA Catalyst** — despliegue (ACT-01) y validación post-despliegue (ACT-02) de la fuente canónica §7.3 (`Q-33`, `Q-36`, `Q-37`, `Q-38`, `Q-39`, `Q-52`).
> **Se guarda en:** `knowledge/releases/[producto]/v[X.Y.Z]/deployment-protocol.md` · **Skill:** `skills/release/deployment-protocol.md` · Comentarios **C-30** (RM) y **C-31** (QA); ante un incidente, **C-32** (hotfix).
> QA no despliega: valida. El LD/RM coordina, **DevOps ejecuta** y el PO comunica a los clientes. Nunca incluir valores de variables, credenciales ni URLs internas sensibles.

## 1. Información general

| Campo | Valor |
|---|---|
| Producto / versión | [iond / IonMind / StageMind] v[X.Y.Z] |
| Decisión Go/No-Go | GO / CONDITIONAL GO — C-29 [AAAA-MM-DD] |
| Ventana de despliegue | [AAAA-MM-DD hh:mm] — acordada con DevOps (viernes antes de las 14:00 o lunes temprano) |
| Tickets incluidos · diferidos | [n] · [n] |
| Tareas de Release relacionadas | [Release producto - vX.Y.Z] · Ninguna |
| Responsables (roles) | RM coordina · DevOps ejecuta · QA valida · PO comunica · LD/RM + DevOps monitorean 48 h |

## 2. Repositorios y ramas RC (merge atómico — `Q-33`)

Todos los PRs de un ticket entran a la RC juntos o ninguno. Las ramas RC por repositorio las documenta el RM en el C-23.

| # | Repo (`altacrest/[repo]`) | Rama RC | Commit validado en preprod | Commit a desplegar | Tickets | ✅ |
|---|---|---|---|---|---|---|
| 1 | [...] | [...] | [...] | [igual al validado] | #[id], #[id] | [ ] |

## 3. Pre-despliegue (prerrequisitos de la T-04)

- [ ] Go/No-Go con GO o CONDITIONAL GO (C-29) y quórum PO + LQA + RM.
- [ ] El commit a desplegar es el mismo commit RC validado en preprod (smoke, sanity y regression).
- [ ] Migraciones: [nombres] — reversibles · backup previo si hay migración de datos.
- [ ] Variables nuevas configuradas en producción: [solo nombres].
- [ ] Dependencias de otros productos desplegadas (IonMind / StageMind).
- [ ] Plan de rollback documentado en la tarea de Release y **probado en preprod**.
- [ ] Ventana confirmada con DevOps.
- [ ] Release notes de cliente aprobadas por el PO.
- [ ] Company de prueba en producción y perfil `.env.prod-testco` disponibles para QA (AV-09).

## 4. Orden de despliegue

Con dependencias entre productos: **StageMind → IonMind → iond** (`Q-37`). Dentro de un producto: backend → frontend / web components.

| Paso | Producto / repo | Acción | Ejecuta | Verificación | ✅ |
|---|---|---|---|---|---|
| 1 | [StageMind (si aplica)] | Desplegar [rama RC / commit] | DevOps | Health del servicio | [ ] |
| 2 | [IonMind (si aplica)] | [...] | DevOps | Health del servicio | [ ] |
| 3 | [iond — backend] | Migraciones + despliegue | DevOps | Health de la API · logs sin 5xx | [ ] |
| 4 | [iond — frontend / web components] | Despliegue | DevOps | La app carga | [ ] |

## 5. Variables y migraciones

| Tipo | Nombre (nunca el valor) | Repo | Ticket | Reversible |
|---|---|---|---|---|
| Variable / migración | [...] | [...] | #[id] | Sí / No |

## 6. Despliegue ejecutado — borrador C-30 (lo publica el RM)

Texto de `templates/comments/C-30.md`:

```markdown
## 🚀 DEPLOYED — [producto vX.Y.Z] — [fecha hora]
**Ejecutó:** DevOps @[..] · **Coordinó:** RM @[..]
**Repos / versiones:** [...] · **Incidencias:** ninguna / [...]
```

## 7. Validación post-despliegue (ACT-02)

### 7.1 Smoke maestro en producción (QA, ≤ 2 h)

- [ ] Iniciado dentro de las 2 h posteriores al C-30, con `templates/smoke-run.md` en modo producción → `smoke-prod.md` (skill `release/smoke`).
- [ ] Solo la **company de prueba**; datos con prefijo `autobot-smoke-`; la cuenta de administración solo en SMK-13 y SMK-14 (lectura).
- [ ] Resultado: [n/n] · core (SMK-01 a SMK-05 y SMK-15) ✅ / ❌.
- [ ] **Limpieza:** board y webhook del smoke eliminados; ningún dato `autobot-smoke-` remanente.

### 7.2 Monitoreo de 48 h (LD/RM con DevOps)

| Ventana | Qué se mira | Estado |
|---|---|---|
| 0–2 h | Health de servicios, errores 5xx, logs de despliegue | ⬜ / ✅ / ❌ |
| 24 h | Ejecuciones de boards, consumo y billing, integraciones (App Connectors, webhooks) | ⬜ / ✅ / ❌ |
| 48 h | Cierre del monitoreo; incidentes reportados por el soporte general de la empresa | ⬜ / ✅ / ❌ |

### 7.3 Borrador C-31 (lo publica QA)

Texto de `templates/comments/C-31.md`:

```markdown
## 🔎 POST-DEPLOY — [✅ estable / ❌ incidente]
**Smoke en producción (company de prueba):** [n/n] · **Limpieza de datos:** ✅ · **Monitoreo 48 h:** [en curso / OK]
**Incidentes:** [#id hotfix]
```

## 8. Rollback

**Disparadores:** core del smoke en producción fallido · incidente `urgent` atribuible a la versión · decisión de PO + LD + RM.

1. El RM avisa a PO, LQA y DevOps: *"Rollback iniciado para [producto] v[X.Y.Z]"*.
2. DevOps revierte en orden inverso al despliegue.
3. Migraciones: se aplica el rollback probado en preprod.
4. QA verifica la versión anterior con el core del smoke maestro en la company de prueba.
5. Se registra el incidente (sección 9) y se relaciona con esta tarea de Release.
6. El RM avisa: *"Rollback completado"*.

## 9. Hotfix (incidente en producción — `Q-38`)

Ticket en Improvements (TYPE `Bug`, prioridad `urgent`, tags `hotfix` + `det-prod`, relacionado con esta tarea de Release) → `to do` directo → flujo normal hasta `ready to merge` → release extraordinario `Hotfix [producto] - v[X.Y.Z+1]` (tag `hotfix`) con smoke y sanity focalizado → despliegue. Autorizan el PO y el LD; ejecuta el RM. Objetivo: **≤ 24 h a producción**. Comentario de apertura **C-32**.
