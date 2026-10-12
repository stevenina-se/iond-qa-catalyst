# Skill: release/notes

> Genera las **release notes** de un producto y versión en dos variantes: **interna** (Development, producto, soporte general de la empresa) y **cliente** (la comunica el PO, `Q-36`). Se adjuntan al C-29.

## Cuándo usar

- Tarea de Release en `ready for release`, con GO o CONDITIONAL GO (o como borrador antes de la mesa).
- Frase disparadora: `Generar release notes: <producto> vX.Y.Z`.

## Pre-requisitos (gates)

| Check | Si falla |
|---|---|
| `knowledge/releases/<producto>/<versión>/tickets.md` | Ejecutar `release/ingest` |
| Tickets diferidos o revertidos identificados (tag `diferido`, C-28) | Revisar `go-no-go.md` y la tarea de Release |

## Contexto a cargar

`tickets.md`, `go-no-go.md` (hallazgos aceptados, workarounds), `templates/release-notes.md`, L2 de los módulos para los nombres amigables.

## Stage 1 — Planning

Anunciar la cantidad de tickets incluidos por TYPE, los excluidos (`diferido`) y las dos salidas. Esperar confirmación.

## Stage 2 — Execution

1. **Clasificar** por `custom_type`: `New Feature` → 🚀 Nuevas funcionalidades · `Bug` → 🐛 Correcciones · `Improvement` → ⚡ Mejoras · `Refactor`/`Task` → 🔧 Cambios internos (solo interna). Subagrupar por **Iond Subcategory**.
2. **Excluir** los tickets con `diferido` o revertidos de la RC.
3. **Versión interna** (`templates/release-notes.md`, tipo interna):
   - Resumen con totales por tipo y por módulo; 3 a 5 highlights (prioridad `urgent`/`high` y cambios del motor).
   - Por ticket: título, módulo, repos afectados; nota de *re-validado* si Rejection_count > 0.
   - Cambios de infraestructura (variables, migraciones) del C-09 y del `deployment-protocol.md`.
   - Hallazgos aceptados en un CONDITIONAL GO, con su workaround y el fix agendado.
   - Información del release: versión, fecha, ambiente, contactos por rol.
4. **Versión cliente** (tipo cliente):
   - Solo cambios visibles para el usuario, en lenguaje de beneficio ("Ahora puedes…", "Corregimos…", "Mejoramos…").
   - Sin IDs de ticket, repos, ramas ni jerga técnica; nombres amigables de los módulos (p. ej. "Automatización de flujos" para Boards).
   - Cambios que requieren acción del cliente: "Qué necesitas hacer", paso a paso.
5. **Gateway:** los tickets con Project = Gateway se incluyen en las notas de iond, en una sección propia.

## Stage 3 — Reporting

- `knowledge/releases/<producto>/<versión>/release-notes-internal.md` y `release-notes-client.md`, después de la aprobación del SM (interna) y del PO (cliente).
- Enlaces para el C-29 (`Release notes: [interna] · [cliente]`).

## Reglas

- Siempre las dos versiones.
- Los custom fields mandan; las inferencias se confirman con QA.
- La versión cliente la aprueba y comunica el **PO**; el catalyst no la envía.
