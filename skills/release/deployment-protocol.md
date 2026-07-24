# Skill: release/deployment-protocol

> Genera el `deployment-protocol.md` automáticamente con formato conciso.
> Incluye repos, ramas, checklist de pre-deploy, fases de despliegue, verificaciones
> post-deploy y procedimiento de rollback.

---

## Cuándo usar este skill

**Frase disparadora:**
```
Generar protocolo de deployment: v[X.Y.Z]
```

**Pre-condición**: El brief de regresión debe existir (o al mínimo la tracking-list).

---

## Pre-requisitos

- ✅ `knowledge/releases/<version>/tracking-list.md` (del ingest o plan)
- ✅ `knowledge/releases/<version>/regression-brief.md` (del brief, opcional)
- ✅ `knowledge/releases/<version>/ticket-synthesis.md` (del ingest, para info de infra)
- ✅ Acceso a los repositorios Git (para verificar branches y commits)

---

## Stage 1 — PLANNING

### Paso 1.1 — Identificar repositorios afectados

Desde `ticket-synthesis.md` o `tracking-list.md`, extraer todos los repos únicos:

| Repo | Stack | Fuente |
|------|-------|--------|
| gateway-ion | Vue.js + Vitest | Merge Request URLs |
| flow_binaries | Go | Merge Request URLs |
| gateway (integrations) | Laravel/PHP | Merge Request URLs |
| webcomponents-flow | Web Components | Merge Request URLs |

### Paso 1.2 — Detectar info de infra desde tickets

Buscar en `ticket-synthesis.md` patrones de:
- **Variables de entorno**: `APP_DEBUG`, `APP_URL`, `KEYCLOAK_*`, etc.
- **Migraciones de BD**: `migrate`, `migration`, `schema`, `ALTER TABLE`
- **Nuevos endpoints**: `/api/2.0/`, `POST /`, `GET /`
- **Configuraciones**: `.env`, `config`, `settings`

Si se encuentran → agregar al checklist de pre-deploy.

### Paso 1.3 — Anunciar el plan

```
🚀 DEPLOYMENT PROTOCOL — PLAN

Versión: v[X.Y.Z]
Repos afectados: [N]
Info de infra detectada: [SÍ/NO]

Plan:
  1. Documentar repos y ramas
  2. Verificar último commit por repo
  3. Generar pre-deploy checklist
  4. Definir fases de despliegue
  5. Incluir variables de entorno (si hay cambios)
  6. Integrar smoke checklist post-deploy
  7. Documentar rollback procedure

¿Procedo?
```

---

## Stage 2 — EXECUTION

### Paso 2.1 — Generar el deployment protocol

Usando template `templates/deployment-protocol.md`:

**Secciones:**

#### 1. Información General

| Campo | Valor |
|-------|-------|
| Versión | `v[X.Y.Z]` |
| Fecha de deploy | [fecha] |
| Repos | [lista] |
| Total tickets | [N] |
| Go/No-Go | [resultado de la regresión] |

#### 2. Repositorios y Ramas

| # | Repo | Stack | Rama actual | Rama deploy | Último commit | ✅ |
|---|------|-------|------------|-------------|---------------|---|
| 1 | gateway-ion | Vue.js | DEVELOPMENT | main | `abc1234 - [msg]` | □ |
| 2 | flow_binaries | Go | DEVELOPMENT | main | `def5678 - [msg]` | □ |
| ... | | | | | | |

> Verificar con `git log -1 --oneline` en cada repo si hay acceso.

#### 3. Pre-Deploy Checklist

- □ Todos los tickets del release en status `merged` o `production deploy`
- □ Regression test completado: [resultado]
- □ Smoke test completado: [resultado]
- □ Go/No-Go aprobado
- □ Ramas DEVELOPMENT actualizadas en todos los repos
- □ No hay MRs pendientes para esta versión
- □ [Si hay migraciones]: Migraciones de BD preparadas
- □ [Si hay variables]: Variables de entorno actualizadas en producción
- □ [Si hay endpoints nuevos]: Documentación de API actualizada
- □ Backup de BD de producción realizado
- □ Equipo notificado del deploy

#### 4. Fases de Despliegue

```
FASE 1 — Backend (gateway / flow_binaries)
  □ Merge DEVELOPMENT → main en gateway
  □ Merge DEVELOPMENT → main en flow_binaries
  □ Verificar CI/CD pipeline green
  □ Deploy backend a producción
  □ Verificar health check: [URL]

FASE 2 — Frontend (gateway-ion / webcomponents-flow)
  □ Merge DEVELOPMENT → main en gateway-ion
  □ Merge DEVELOPMENT → main en webcomponents-flow
  □ Verificar CI/CD pipeline green
  □ Deploy frontend a producción
  □ Verificar que la app carga: [URL]

FASE 3 — Verificación Post-Deploy
  □ Ejecutar smoke checklist (ver sección 6)
  □ Verificar logs: sin errores 500/502
  □ Verificar Keycloak: login funciona
```

#### 5. Variables de Entorno (solo si hay cambios)

> Solo incluir si se detectaron cambios en los tickets.

| Variable | Valor sugerido | Repo | Ticket origen |
|----------|---------------|------|--------------|
| `APP_DEBUG` | `false` | gateway | IONF-XXX |
| `[NUEVA_VAR]` | `<valor>` | [repo] | IONF-YYY |

#### 6. Smoke Checklist Post-Deploy

> Embeber los TCs del smoke-matrix como checklist de verificación post-deploy.

| # | Verificación | Pasos | ✅ |
|---|-------------|-------|---|
| 1 | Login SSO funciona | Navigate → Login → Dashboard visible | □ |
| 2 | Crear Board nuevo | Sidebar Boards → + New Board → Verify | □ |
| 3 | Ejecutar Flow | Board → Run → History visible | □ |
| ... | | | |

#### 7. Rollback Procedure

```
SI HAY PROBLEMAS CRÍTICOS POST-DEPLOY:

  1. Notificar al equipo: "Rollback iniciado para v[X.Y.Z]"
  2. Revertir frontend:
     □ git revert en gateway-ion → re-deploy
     □ git revert en webcomponents-flow → re-deploy
  3. Revertir backend:
     □ git revert en gateway → re-deploy
     □ git revert en flow_binaries → re-deploy
  4. [Si hubo migraciones]: Ejecutar rollback de BD
  5. Verificar que la app funciona con la versión anterior
  6. Documentar incidencia: qué falló, cuándo, impacto
  7. Notificar al equipo: "Rollback completado. [versión anterior] restaurada."
```

---

## Stage 3 — REPORTING

### Paso 3.1 — Presentar el protocolo

```
🚀 DEPLOYMENT PROTOCOL v[X.Y.Z] — DRAFT

Repos: [N] | Fases: [N] | Checklist: [N] items
Variables de entorno: [cambios detectados / sin cambios]
Rollback procedure: Documentado

¿Apruebas o deseas ajustar algo?
```

### Paso 3.2 — Guardar artefacto

`deployment-protocol.md` → `knowledge/releases/<version>/`

---

## Reglas de este Skill

1. **Formato conciso** — No más de 200-250 líneas. Los detalles extensos van en los tickets.
2. **Info de infra desde tickets** — Variables de entorno y migraciones se detectan automáticamente.
3. **Smoke checklist embebido** — Post-deploy siempre incluye verificaciones.
4. **Rollback siempre documentado** — Aunque sea corto, siempre incluir.
5. **NUNCA modificar skills, templates o artefactos existentes**
6. **Artefactos por versión** — Output en `knowledge/releases/<version>/`

---

## Checklist de cierre

- □ Repos identificados desde MR URLs
- □ Info de infra detectada (variables, migraciones, endpoints)
- □ Pre-deploy checklist generado
- □ Fases de despliegue documentadas
- □ Variables de entorno listadas (si hay cambios)
- □ Smoke checklist post-deploy embebido
- □ Rollback procedure documentado
- □ Protocolo aprobado por el Scrum Master
- □ Artefacto guardado
