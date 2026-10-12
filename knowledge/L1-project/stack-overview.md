# Stack Técnico — Ionflow

> Resumen completo del stack tecnológico del proyecto Ionflow y sus convenciones.

## Stack por Repositorio

### flow_binaries — Backend Core
| Tecnología | Versión | Notas |
|-----------|---------|-------|
| Go | (verificar en go.mod) | Lenguaje principal del core |
| PostgreSQL | (verificar en servidor) | Base de datos principal |
| REST API | — | Estilo de API |

### gateway-ion — Frontend
| Tecnología | Versión | Notas |
|-----------|---------|-------|
| Vue | 3.x | Framework frontend |
| TypeScript | — | Lenguaje principal |
| Pinia | — | State management |
| Vue Router | — | Routing SPA |
| Vite | — | Build tool (verificar) |

### webcomponents-flow — Canvas de Nodos
| Tecnología | Versión | Notas |
|-----------|---------|-------|
| Vue | 3.x | Framework de componentes |
| TypeScript | — | Lenguaje principal |
| Vue Flow | — | Librería del canvas de nodos |
| Web Components | — | Distribución via CDN |

### gateway — Auth Legacy
| Tecnología | Versión | Notas |
|-----------|---------|-------|
| PHP | 8.2 | Lenguaje backend legacy |
| Laravel | (verificar) | Framework PHP |
| Eloquent | — | ORM para PostgreSQL |

### bot-test — E2E Automation
| Tecnología | Versión | Notas |
|-----------|---------|-------|
| Playwright | (verificar en package.json) | Framework de testing E2E |
| NX | — | Monorepo workspace |
| TypeScript | — | Lenguaje de tests |
| Node.js | — | Runtime |

## Infraestructura

| Componente | Tecnología | Acceso |
|-----------|-----------|--------|
| Base de datos | PostgreSQL | SSH tunnel (DBeaver) |
| Hosting | (verificar con equipo) | — |
| CI/CD | GitLab CI (bot-test) | `.gitlab-ci.yml` |

## Convenciones del Equipo

### Branching (SDLC IOND)
- **`DEVELOPMENT`** — rama de integración de cada repositorio.
- **Rama del ticket** — una por ticket (PRs en los campos Merge Request); `mock testing` se hace sobre esta rama en el ambiente asignado al QA, **antes** del merge.
- **Rama RC semanal** — en `dev preparation` el RM mergea los tickets en `ready to merge` (merge atómico por ticket) y la despliega en preprod; sobre ella corren smoke, sanity y regresión. Los fix-forward van a esta rama.
- **Producción** — después del Go/No-Go (C-29); el despliegue lo ejecuta DevOps (C-30).

### Testing
- E2E tests en Playwright (`../bot-test`)
- Tests de Ionflow en `apps/bot-test/tests/IONFLOW/`
- Estructura: `Admin-ION/<dominio>/`, `Company-ION/<módulo>/` (spec + page object + `.md`), `shared/` y `utils/`
- Ejecución por suite con IDs de test: ver `skills/_shared/bot-test.md` y `knowledge/test-suites/README.md`
- El catalyst lee y ejecuta bot-test; no modifica su código

### Gestión de Tickets
- Herramienta: ClickUp
- MCP de ClickUp configurado en modo solo lectura (`skills/_shared/clickup.md`)

---

*Este archivo se actualiza cuando cambia el stack o sus versiones. Última actualización: Initial setup.*
