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

### Branching Model (Altacrest Dual-Track)
- **Prototype Branch** — Para features durante Discovery (experimental, puede eliminarse)
- **Release Candidate Branch** — Merge de features del sprint con todas las validaciones
- **Production Branch** — Solo después de QA, Pilot/UAT y Release Approval

### Testing
- E2E tests en Playwright (`../bot-test`)
- Tests de Ionflow en `apps/bot-test/tests/IONFLOW/`
- Ejecución: `npx nx run bot-test:test:ionflow`
- Page objects en `tests/IONFLOW/pages/`
- Helpers en `tests/IONFLOW/utils/`

### Gestión de Tickets
- Herramienta: ClickUp
- MCP disponible para integración (por configurar)

---

*Este archivo se actualiza cuando cambia el stack o sus versiones. Última actualización: Initial setup.*
