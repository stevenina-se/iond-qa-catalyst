# Skill: automation/plan

> Decide qué casos conviene **automatizar** en bot-test, con la prioridad del release (`Q-40`, `Q-50`): **smoke → baseline crítico → TC estables de sanity → resto del E2E maestro**. Trabaja sobre la Matriz de Pruebas de un ticket (después de `merged`) o sobre un módulo del E2E maestro.

## Cuándo usar

- Ticket en `merged` con `qa-report.md` aprobado (C-13): automatizar lo validado que se repetirá en releases.
- Planificación de una ola de `automation-roadmap.md` para un módulo.
- Frase disparadora: `Planificar automatización: <ticket-id>` o `Planificar automatización: <prefijo E2E, p. ej. TEN-APC>`.

## Pre-requisitos (gates)

| Check | Si falla |
|---|---|
| Ticket: `test-matrix.md` con resultados y `qa-report.md` aprobado | Solo se automatiza lo validado manualmente |
| Módulo: filas del módulo en `e2e-master.csv` | Ejecutar `test-suites/import-e2e` |

## Contexto a cargar

L2 del módulo (rutas, componentes, *Specs bot-test*), `skills/_shared/bot-test.md`, `knowledge/test-suites/automation-roadmap.md`, specs y page objects existentes del módulo en `../bot-test/apps/bot-test/tests/IONFLOW/` (solo lectura).

## Stage 1 — Planning

Anunciar el alcance (ticket o módulo), la cantidad de TC/filas y la estimación inicial de automatizables. Esperar confirmación.

## Stage 2 — Execution

1. **Clasificar cada caso:**

   | Criterio | Automatizable | No automatizable (o diferir) |
   |---|---|---|
   | Interacción | Formularios, listas, navegación, CRUD, canvas a través de los componentes aislados de bot-test (`board-canvas.component`, `node-config-drawer.component`) | Gestos que el componente de canvas no soporta todavía |
   | Datos | Generables (`autobot-*`) y limpiables | Datos de terceros sin sandbox ni mock |
   | Verificación | Texto, URL, estado, respuesta de API, archivo exportado | Juicio visual, UX, calidad de salida de IA (solo estructura) |
   | Tiempo | Determinista | Esperas largas sin control (se marca `@slow`, va a la corrida nocturna) |
   | BD | Verificable por UI o API | Solo por SQL en el túnel (queda manual) |

2. **Priorizar:** 🔴 casos del smoke maestro o del baseline (`BASELINE = sí`) · 🟠 TC de REQ críticos que se repiten en sanity · 🟡 resto por prioridad de la hoja.
3. **Recursos existentes:** page objects, componentes y helpers reutilizables; IDs `TC-…` ya usados en el módulo (para no repetirlos).
4. **Mapeo:** cada caso a automatizar → fila(s) del E2E maestro (`E2E-…`) y, si existe, ticket de QA Kanban. Si no hay ticket, proponerlo como draft en `knowledge/L3-tickets/drafts/automation/`.

## Stage 3 — Reporting

`automation-plan.md` (en el L3 del ticket o en `knowledge/test-suites/plans/<prefijo>-<fecha>.md`):
```
Alcance · Casos totales · Automatizables [n] ([%]) · No automatizables [n] (motivo)
Candidatos priorizados (🔴/🟠/🟡) con: caso → fila E2E → TC-ID propuesto → complejidad
Recursos a reutilizar · Ticket de QA Kanban (existente o propuesto)
```
Siguiente skill: `automation/code` (paquete para el responsable de bot-test).

## Reglas

- Solo se automatiza lo **validado manualmente**.
- El plan es una propuesta: el LQA decide qué entra en cada ola.
- Un test inestable vale menos que ninguno: si no se puede hacer determinista, no se automatiza.
