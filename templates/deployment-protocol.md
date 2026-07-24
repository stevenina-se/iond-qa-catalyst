# Deployment Protocol — [VERSIÓN]

> Template generado por `skills/release/deployment-protocol`
> Fecha: [fecha]
> Versión: v[X.Y.Z]

---

## Información General

| Campo | Valor |
|-------|-------|
| Versión | `v[X.Y.Z]` |
| Fecha de deploy | [fecha] |
| Repos afectados | [lista] |
| Total tickets | [N] |
| Go/No-Go | [resultado] |

---

## Repositorios y Ramas

| # | Repo | Stack | Rama actual | Rama deploy | Último commit | ✅ |
|---|------|-------|------------|-------------|---------------|---|
| 1 | | | DEVELOPMENT | main | | □ |
| 2 | | | DEVELOPMENT | main | | □ |

---

## Pre-Deploy Checklist

- □ Todos los tickets en status `merged` o `production deploy`
- □ Regression test completado
- □ Smoke test completado
- □ Go/No-Go aprobado
- □ Ramas DEVELOPMENT actualizadas
- □ No hay MRs pendientes
- □ Backup de BD realizado
- □ Equipo notificado

<!--
Items adicionales (auto-detectados de los tickets):
- □ [migración / variable / endpoint nuevo]
-->

---

## Fases de Despliegue

### Fase 1 — Backend

- □ Merge DEVELOPMENT → main en [repo backend 1]
- □ Merge DEVELOPMENT → main en [repo backend 2]
- □ Verificar CI/CD pipeline
- □ Deploy backend
- □ Health check: [URL]

### Fase 2 — Frontend

- □ Merge DEVELOPMENT → main en [repo frontend 1]
- □ Merge DEVELOPMENT → main en [repo frontend 2]
- □ Verificar CI/CD pipeline
- □ Deploy frontend
- □ Verificar app: [URL]

### Fase 3 — Verificación Post-Deploy

- □ Ejecutar smoke checklist
- □ Verificar logs (sin errores 500/502)
- □ Login SSO funciona

---

## Variables de Entorno

<!--
Solo si hay cambios detectados. Si no hay cambios, escribir "Sin cambios."
-->

| Variable | Valor | Repo | Ticket |
|----------|-------|------|--------|
| | | | |

---

## Smoke Checklist Post-Deploy

| # | Verificación | ✅ |
|---|-------------|---|
| 1 | Login SSO funciona | □ |
| 2 | Dashboard carga | □ |
| 3 | Crear Board nuevo | □ |
| 4 | Ejecutar Flow | □ |
| 5 | Crear Connection | □ |

---

## Rollback Procedure

```
SI HAY PROBLEMAS CRÍTICOS:

1. Notificar: "Rollback iniciado para v[X.Y.Z]"
2. Revertir frontend (git revert → re-deploy)
3. Revertir backend (git revert → re-deploy)
4. [Si hubo migraciones]: Rollback BD
5. Verificar versión anterior funciona
6. Documentar incidencia
7. Notificar: "Rollback completado"
```

---

## Notas

[Notas o dejar vacío]
