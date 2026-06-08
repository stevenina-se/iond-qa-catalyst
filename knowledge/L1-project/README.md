# L1 — Conocimiento del Proyecto Ionflow

> Este directorio contiene el conocimiento de nivel 1: todo lo que un agente de IA necesita saber sobre el proyecto Ionflow ANTES de trabajar en cualquier módulo o ticket.

## Archivos

| Archivo | Contenido |
|---------|-----------|
| [business-rules.md](business-rules.md) | Reglas de negocio de Ionflow |
| [api-architecture.md](api-architecture.md) | Los 4 repositorios, sus APIs y relaciones |
| [test-priorities.md](test-priorities.md) | Ranking de módulos y áreas por criticidad |
| [stack-overview.md](stack-overview.md) | Stack técnico completo con versiones y convenciones |

## Cuándo Actualizar

Estos archivos se actualizan **solo** cuando:
- Cambia la arquitectura del proyecto (nuevo repo, nueva tecnología)
- Se agregan reglas de negocio fundamentales
- Se redefinen las prioridades de testing
- Se migra parte del stack (ej: gateway PHP → Go)

**NO se actualiza por cada ticket o feature.**
