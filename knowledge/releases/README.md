# Artefactos de release

> Una carpeta por **producto y versión**: `knowledge/releases/<producto>/<versión>/` (`iond`, `ionmind`, `stagemind`). Los tickets con Project = Gateway van en el release de `iond`. Los hotfix usan su propia versión.
> Los generan las skills de `skills/release/` a lo largo de la semana del release (ver el calendario en `SKILL.md`).

## Contenido de una versión

| Artefacto | Skill | Estado de la tarea de Release |
|---|---|---|
| `release-task.md` | `release/weekly-plan` | Viernes previo · `dev preparation` |
| `tickets.md` · `tickets.csv` | `release/ingest` | `dev preparation` |
| `smoke-preprod.md` | `release/smoke` | `smoke` |
| `sanity-matrix.md` | `release/sanity` | `sanity` |
| `regression-matrix.md` · `.csv` | `release/regression` | `regression` (capa 1) |
| `e2e-run.md` · `.csv` | `release/e2e` | `regression` (capa 2) |
| `go-no-go.md` | `release/go-no-go` | `ready for release` |
| `release-notes-internal.md` · `release-notes-client.md` | `release/notes` | `ready for release` |
| `deployment-protocol.md` | `release/deployment-protocol` | `ready for release` → despliegue |
| `smoke-prod.md` | `release/smoke` (producción) | Post-despliegue (ACT-02) |
| `brief.md` | `release/brief` | Cualquiera |
| `bug-hunt-<módulo>-<fecha>.md` | `release/bug-hunt` | Opcional |
| `comments/` · `evidence/` | Varias | — |

## Reglas

1. Una carpeta por producto y versión; no se mezclan versiones.
2. La carpeta nace con `release-task.md` (plan semanal).
3. Los artefactos se acumulan a medida que avanza el release; no se reescriben los de suites ya cerradas (las correcciones se anotan).
4. El grupo de rotación de la capa 2 del release siguiente se toma del `e2e-run.md` del último release del mismo producto.

## Historial

Las carpetas `v0.1.0/`, `v0.1.1/`, `v1.0.0/`, `ionmind-v1.10.1/`, `stagemind-v1.5.1/` y el archivo `ai-deployment-protocol-v1.10.1-v1.5.1.md` pertenecen al proceso anterior y se conservan sin mover como historial. El release beta **iond v0.2.0** se arma desde cero en `iond/v0.2.0/` (con `ionmind/v1.10.2/` relacionado).
