---
name: sprint-planning
description: Planificación de sprint con dual track. Clasifica tickets, calcula cutoff dates, identifica riesgos, genera guiones de seguimiento y planifica la versión target del sprint.
---

# Skill: Sprint Planning — Planificación de Versión

> Genera el análisis completo de un sprint para planificar qué tickets entran en la próxima versión,
> cuáles están en riesgo, y crea guiones de seguimiento para el equipo.

## Cuándo usar este skill

- Al inicio de un sprint (días 1-3) para establecer el plan
- A mitad de sprint para ajustar prioridades
- Cuando el QA Engineer pide "planificar la versión" o "analizar el sprint"

## Modelo de Sprint: Dual Track (2+1)

```
Semana 1          Semana 2          Post-Sprint
├── Dev ──────────├── Dev + QA ─────├── Deploy ──┤
│ fortification   │ code review     │ merge      │
│ sprint intake   │ qa testing      │ release    │
│                 │ ready to merge  │            │
└─────────────────└─────────────────└────────────┘
                   ^                 ^
                   QA CUTOFF         DEADLINE
                   (Mié S2)         (Vie S2)
```

### Cutoff Dates (calculados desde el último día del sprint)

| Milestone | Fórmula | Significado |
|-----------|---------|-------------|
| **DEV CUTOFF** | DEADLINE - 5 días hábiles | Último día para que dev termine código |
| **CR CUTOFF** | DEADLINE - 3 días hábiles | Último día para que Code Review apruebe |
| **QA CUTOFF** | DEADLINE - 2 días hábiles | Último día para que QA comience testing |
| **QA FREEZE** | DEADLINE - 1 día hábil | Último día para completar QA |
| **DEADLINE** | Viernes de Semana 2 | Todo aprobado, ready to merge |

> ⚠️ Los tickets que no estén en `qa testing` para el QA CUTOFF tienen **alto riesgo de no completarse**.

---

## Instrucciones de Ejecución

### Fase 1 — DATA GATHERING

1. **Obtener lista de tickets del sprint** desde ClickUp o CSV
2. Para cada ticket, extraer:
   - `status` (pipeline position)
   - `priority`
   - `assignee`
   - `custom_type` (Bug / New Feature / Improvement)
   - `custom_iond.version` (version target)
   - `custom_iond_subcategory` (módulo)
   - `custom_project` (Iond / Gateway / IonMind)
   - `tags` (qa-regression-v0.1.0, iond-core-issue, iond-uxui-issue)
   - `custom_merge_request` (PRs)
3. **Calcular los cutoff dates** basados en el último día del sprint

### Fase 2 — CLASIFICACIÓN

Clasificar cada ticket en una de estas categorías:

#### Por Destino de Versión
- **Regression Fixes**: Tickets con prefijo `v{VERSION} -` o tag `qa-regression-v{VERSION}`
  → Son bugs encontrados en la versión actual, van a la **NEXT version**
- **Features**: Tickets sin prefijo de versión, `custom_type: New Feature`
  → Funcionalidades nuevas para la versión actual del sprint
- **Improvements**: `custom_type: Improvement`
  → Mejoras incrementales
- **Otros proyectos**: `custom_project` ≠ proyecto principal
  → Tickets de Gateway, IonMind, etc.

#### Por Viabilidad de Completar
Basado en la posición en el pipeline y los cutoff dates:

| Status actual | Días mínimos para completar | Fórmula |
|---------------|----------------------------|---------|
| ready to merge | 0 | Completado |
| qa testing / qa in process | 1-2 | Solo QA |
| code review | 3-4 | CR (1-2d) + Deploy (0.5d) + QA (1-2d) |
| fortification | 5-7 | Dev (2-3d) + CR (1-2d) + Deploy + QA |
| sprint intake | 7-10 | Todo el pipeline |

**Clasificación de riesgo:**
- 🟢 **On Track**: Días restantes ≥ días mínimos × 1.5
- 🟡 **At Risk**: Días restantes ≥ días mínimos pero < × 1.5
- 🔴 **Off Track**: Días restantes < días mínimos

### Fase 3 — SPRINT BOARD (Entregable Principal)

Generar el **Sprint Board** como artefacto persistente en:
`knowledge/releases/{version}/sprint-board.md`

> ⚠️ **Este archivo es el ENTREGABLE principal del skill.**
> Se genera cada vez que se ejecuta el skill y se actualiza si el sprint ya tiene un board previo.
> El nombre incluye la versión target, NO el número de sprint.

El board DEBE incluir las siguientes secciones (en este orden):

#### Sección 1 — Header y Cutoff Dates
- Información del sprint (número, período, versión target)
- Fecha actual y día del sprint
- Tabla de cutoff dates calculados
- Timeline visual ASCII

#### Sección 2 — Tickets por Categoría
- **Categoría A**: Regression fixes (con riesgo por ticket)
- **Categoría B**: Features y tickets del sprint
- **Categoría C**: Backlog / sprint intake sin iniciar
- Cada ticket con: ID, descripción, status, prioridad, dev, riesgo, ETA QA

#### Sección 3 — Priorización QA
- Lista ordenada de tickets a testear (prioridad 1, 2, 3)
- Regression fixes siempre primero

#### Sección 4 — Carga por Developer y Bottlenecks
- Tabla de carga con: total, regression, completados, pendientes, bottleneck

#### Sección 5 — Guiones de Seguimiento
- Un bloque por developer con tickets en riesgo
- Pregunta específica por ticket según su status
- Tabla resumen de deadlines por dev

#### Sección 6 — Proyección de Versión
- Tickets que entrarán en la versión target
- Tickets que se mantendrán en next

### Fase 4 — GUIONES DE SEGUIMIENTO

Generar guiones de seguimiento para cada developer con tickets en riesgo.

#### Formato del guión

```markdown
## Follow-up: [Developer Name] — [Fecha]

### Contexto
Tienes [N] tickets en el Sprint 4 que necesitan avanzar para la v{VERSION}.

### Preguntas por ticket

#### [TICKET-ID] — [Título corto]
- Status actual: [status]
- **Pregunta**: [pregunta específica según el status]
- **Deadline**: [fecha específica para que avance al siguiente status]

### Resumen de deadlines
| Ticket | Necesita estar en... | Para fecha... |
|--------|---------------------|---------------|
| IONF-XXXX | code review | [fecha] |
| IONF-YYYY | qa testing | [fecha] |
```

#### Preguntas según status

| Status | Pregunta tipo |
|--------|--------------|
| sprint intake | "¿Ya comenzaste el desarrollo? ¿Estimación de días para completar?" |
| fortification | "¿Cómo vas con el desarrollo? ¿Qué % estimas de avance? ¿Bloqueos?" |
| code review | "¿Ya tienes reviewers asignados? ¿Cuándo estimas aprobación?" |
| code review (>2d) | "El CR lleva más de 2 días. ¿Hay comentarios pendientes de resolver?" |
| qa testing | "Ya está deployed en dev? ¿Hay algo que deba saber para el testing?" |
| blocked | "¿Qué bloquea este ticket? ¿Hay algo que pueda hacer para ayudar?" |

### Fase 5 — GUARDAR ENTREGABLES

> ⚠️ **OBLIGATORIO**: Cada ejecución de este skill DEBE generar/actualizar estos archivos.

#### Archivos de salida

| Archivo | Ruta | Contenido |
|---------|------|-----------|
| **Sprint Board** | `knowledge/releases/{version}/sprint-board.md` | Entregable principal con todas las secciones |
| **Followups** | `knowledge/releases/{version}/followups/{fecha}-followup.md` | Guiones de seguimiento con fecha |

#### Reglas de generación

1. Si `sprint-board.md` ya existe, **sobrescribirlo** con la versión actualizada
2. Los followups se crean como archivos separados con fecha: `2026-07-10-followup.md`
3. El sprint board se crea **siempre** en el workspace del proyecto, NO solo como artifact temporal

---

## Reglas

1. **No tomar decisiones de cut** (quitar tickets del sprint) sin aprobación del QA Engineer
2. **Priorizar fixes de regresión** sobre features nuevas
3. **Considerar dependencias** entre tickets del mismo módulo
4. **Respetar el dual track** — Dev y QA pueden correr en paralelo pero los cutoffs son firmes
5. **El QA Engineer es quien comunica** los followups al equipo — Catalyst solo genera los guiones
6. **Cada ejecución genera un .md persistente** — el sprint-board.md es el registro vivo del estado del sprint

