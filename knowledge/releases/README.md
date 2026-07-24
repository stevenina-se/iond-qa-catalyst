# Release Artifacts

> Almacén de artefactos de release organizados por versión.
> Generados por las skills de `skills/release/`.

## Estructura por versión

Cada versión (`v1.0.0/`, `v1.1.0/`, etc.) contiene:

| Artefacto | Generado por | Descripción |
|-----------|-------------|-------------|
| `release-plan.md` | `release/plan` o `release/plan-v1` | Cronograma de lanzamiento |
| `tracking-list.md` | `release/plan` o `release/plan-v1` | Lista de tickets con tags |
| `tracking-list.csv` | `release/plan` o `release/plan-v1` | Versión CSV de la tracking list |
| `release-notes-internal.md` | `release/notes` | Release notes para equipo interno |
| `release-notes-client.md` | `release/notes` | Release notes para clientes |
| `regression-matrix.md` | `release/regression-matrix` | Matriz de regresión |
| `regression-matrix.csv` | `release/regression-matrix` | Versión CSV de la regresión |
| `smoke-matrix.md` | `release/smoke-matrix` | Matriz de smoke test |
| `smoke-matrix.csv` | `release/smoke-matrix` | Versión CSV del smoke |
| `bug-hunt-<modulo>.md` | `release/bug-hunt` | Reporte de bug hunt por módulo |

## Reglas

1. **Un directorio por versión** — No mezclar artefactos de versiones distintas
2. **No crear el directorio hasta tener el release plan** — El plan es lo primero
3. **Los artefactos son acumulativos** — Se agregan conforme se ejecutan las skills
