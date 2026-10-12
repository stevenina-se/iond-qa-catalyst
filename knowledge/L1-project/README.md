# L1 — Conocimiento del proyecto IOND

> Este directorio contiene el conocimiento de nivel 1: lo que un agente de IA necesita saber sobre IOND (iond + Gateway, con IonMind y StageMind como productos relacionados) **antes** de trabajar en cualquier módulo, ticket o release.

## Archivos

| Archivo | Contenido |
|---------|-----------|
| [sdlc-consolidation.md](sdlc-consolidation.md) | **Fuente canónica del SDLC** (Regla #1): tableros y estados, roles, matrices, release, severidad, campos, tags, plantillas T-xx y C-xx, automatizaciones, SLAs |
| [subcategory-map.md](subcategory-map.md) | Cómo se pasa de la Iond Subcategory de un ticket al módulo L2 y a las filas del E2E maestro |
| [business-rules.md](business-rules.md) | Reglas de negocio de iond |
| [api-architecture.md](api-architecture.md) | Repositorios, APIs y relaciones |
| [test-priorities.md](test-priorities.md) | Criticidad por módulo y prioridades por tipo de prueba |
| [stack-overview.md](stack-overview.md) | Stack técnico, versiones y convenciones |

Las suites del release (smoke maestro, E2E maestro, cobertura y hoja de ruta de automatización) están en [`knowledge/test-suites/`](../test-suites/README.md).

## Orden de lectura

1. `sdlc-consolidation.md`: las secciones del tablero y estado del ticket o del release en curso.
2. `test-priorities.md` y `business-rules.md` para el criterio de riesgo.
3. `api-architecture.md` y `stack-overview.md` cuando la tarea toca código o integraciones.

## Cuándo actualizar

- `sdlc-consolidation.md`: solo con una decisión nueva del equipo (se registra en el Registro de Decisiones `docs/sdlc-iond/src/03-…`) y se sube la versión.
- El resto: cuando cambia la arquitectura, una regla de negocio fundamental o la criticidad de un módulo. **No** por cada ticket.
