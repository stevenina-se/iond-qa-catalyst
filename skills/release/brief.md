# Skill: release/brief

> Genera el **brief del release**: una página para los stakeholders y los líderes con el alcance, el riesgo, el avance de las suites (smoke → sanity → regresión capa 1 → E2E capa 2) y la decisión Go/No-Go. Sirve también para la daily del release y la Discovery Review.

## Cuándo usar

- En cualquier estado de la tarea de Release; se regenera al cerrar cada suite.
- Frase disparadora: `Generar brief de release: <producto> vX.Y.Z`.

## Pre-requisitos (gates)

| Check | Si falla |
|---|---|
| `release-task.md` y `tickets.md` | Ejecutar `release/weekly-plan` y `release/ingest` |

## Contexto a cargar

Todos los artefactos existentes en `knowledge/releases/<producto>/<versión>/`, `templates/release-brief.md`.

## Stage 1 — Planning

Anunciar qué artefactos existen y en qué estado está la tarea de Release. Esperar confirmación.

## Stage 2 — Execution

Completar `templates/release-brief.md`:
1. **Alcance:** producto, versión, cantidad de tickets por TYPE y por módulo, tickets diferidos.
2. **Riesgo:** Alto / Medio / Bajo con su motivo; dependencias con otros productos (orden de despliegue).
3. **Avance por suite:** estado y resultado (n/n) de smoke, sanity, capa 1 y capa 2; grupo de rotación.
4. **Hallazgos:** abiertos por severidad y decisión (fix-forward / Improvements / diferido).
5. **Decisión:** Go/No-Go (o fecha de la mesa) y ventana de despliegue.
6. **Pendientes y bloqueos:** con responsable y fecha.

Lenguaje no técnico, sin IDs de PR ni detalles de código.

## Stage 3 — Reporting

- `knowledge/releases/<producto>/<versión>/brief.md`.
- Texto corto (≤ 10 líneas) listo para pegar en el canal del equipo, si el SM lo pide.

## Reglas

- El brief resume; no reemplaza a los comentarios C-23 a C-31 de la tarea de Release.
- No incluir nombres de personas fuera de los roles (PO, LD/RM, LQA, SM).
