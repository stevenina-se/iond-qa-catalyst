# Skill: release/deployment-protocol

> Genera el **protocolo de despliegue** de un producto y versión para el LD/RM y DevOps (ACT-01) y la validación posterior (ACT-02): ramas RC, prerrequisitos, orden de despliegue, rollback, **smoke maestro en producción con la company de prueba** y monitoreo de 48 h. Comentarios **C-30** y **C-31**.

## Cuándo usar

- Tarea de Release en `ready for release`, antes de la ventana acordada con DevOps (`Q-36`).
- Frase disparadora: `Generar protocolo de despliegue: <producto> vX.Y.Z`.

## Pre-requisitos (gates)

| Check | Si falla |
|---|---|
| `tickets.md` (repos, PRs, infra de cada ticket) | Ejecutar `release/ingest` |
| C-23 con las ramas RC por repo | Pedirlas al RM |
| Ventana y rollback acordados con DevOps (AV-07) | Acción del LD/RM |

## Contexto a cargar

`tickets.md`, `release-task.md`, `go-no-go.md`, `knowledge/test-suites/smoke-master.md`, `templates/deployment-protocol.md`. Repos `../` en solo lectura para confirmar el último commit de cada rama RC (`git log -1 --oneline <rama>`).

## Stage 1 — Planning

Anunciar repos y ramas RC, cambios de infraestructura detectados y dependencias entre productos. Esperar confirmación.

## Stage 2 — Execution

Completar `templates/deployment-protocol.md`:
1. **Información general:** producto, versión, ventana, responsables por rol (RM coordina, DevOps ejecuta, QA valida, PO comunica).
2. **Repos y ramas RC** (merge atómico, `Q-33`): repo → rama RC → commit.
3. **Pre-despliegue:** prerrequisitos de la T-04 (migraciones, variables nuevas, dependencias desplegadas), backup si hay migraciones de datos, rollback probado en preprod.
4. **Orden de despliegue:** StageMind → IonMind → iond cuando hay dependencias (`Q-37`); dentro de iond, backend → frontend → web components.
5. **Variables y migraciones:** solo los nombres (nunca valores), con el ticket que las introduce.
6. **Post-despliegue (ACT-02):** smoke maestro en producción con la company de prueba en ≤ 2 h (`release/smoke` modo producción), limpieza de datos `autobot-smoke-`, monitoreo de 48 h por el LD/RM con DevOps.
7. **Rollback:** disparadores (core del smoke en producción fallido, incidente `urgent`), pasos y responsable; si se activa, se abre **hotfix** (C-32) o se revierte la versión.

## Stage 3 — Reporting

- `knowledge/releases/<producto>/<versión>/deployment-protocol.md`.
- Borradores de **C-30** (para el RM, con fecha/hora, versiones y repos) y **C-31** (para QA, se completa con `release/smoke` en producción).

## Reglas

- QA no despliega: valida. El despliegue lo ejecuta DevOps y lo coordina el RM.
- Nunca incluir valores de variables, credenciales ni URLs internas sensibles.
- Si el release incluye tickets de varios productos, un protocolo por tarea de Release, con referencias cruzadas.
