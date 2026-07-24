# Dashboard: Version Tracking — Seguimiento de Versión y Tickets

> **Audiencia**: QA Engineer, Scrum Master, Dev Lead
> **Frecuencia**: Semanal + pre-release
> **Pregunta central**: "¿Cuántos tickets están listos para la versión? ¿Qué falta?"

---

## Campos y filtros utilizados

| Campo | Filtro | Uso |
|-------|--------|-----|
| `Tags` | `qa-regression-v0.1.0`, `iond-core-issue`, `iond-uxui-issue` | Clasificar fixes |
| `Status` | Pipeline completo | Posición del ticket |
| `Iond Subcategory` | Módulos | Agrupar por área |
| `Type` | Bug, New Feature, Improvement | Tipo de ticket |
| `Project` | Iond, Gateway, IonMind | Producto |
| `Merge Request` | URLs de PRs | Links al código |

---

## Sección A: Progreso de la Versión

### Widget A.1 — Regression Fixes Progress (Status Bar Chart)
- **Tipo**: Bar/Status chart horizontal
- **Filter**: Tag = `qa-regression-v0.1.0`
- **Group by**: Status
- **📖 Interpretación**:
  - Muestra el **progreso de todos los fixes de regresión** para la versión target.
  - **Meta**: 100% en `ready to merge` o `done` para el deadline.
  - **🚨 Alerta**: Tickets en `sprint intake` o `fortification` después del QA CUTOFF → no entrarán en la versión. Mover a next.
  - **✅ Ideal al cierre**: Toda la barra verde. Todo fix de regresión resuelto.
  - **Métrica clave**: `% regression fixes completados` = indicador de calidad del release.
    - **100%** = Release limpio, todos los bugs conocidos resueltos.
    - **80-99%** = Release aceptable si los pendientes son `low/normal`.
    - **<80%** = Release riesgoso, hay bugs conocidos `high` sin resolver.

### Widget A.2 — Version Scorecard (Number Widgets)
- **Tipo**: 6 calculation widgets en fila
  - 📦 Total tickets en la versión
  - ✅ Ready to merge / Done
  - 🔬 En QA
  - 👀 En Code Review
  - 🔨 En Desarrollo
  - 🚫 Bloqueados
- **📖 Interpretación**:
  - **GO para release**: Ready ≥ 80% del total AND Bloqueados = 0 AND En QA = 0.
  - **NO-GO**: Bloqueados > 0 con `high/urgent`, o regression fixes en desarrollo.
  - **Release parcial**: Si tickets no-críticos están pendientes, moverlos a next y hacer release con lo aprobado.
  - **Fórmula**: `Release Readiness % = (Ready + Done) / Total × 100`

### Widget A.3 — Version Timeline (Text/Embed Widget)
- **Tipo**: Text widget con cutoff dates
- **Contenido**:
  ```
  ┌─────────────────────────────────────────────────────┐
  │  DEV CUTOFF   CR CUTOFF   QA CUTOFF   FREEZE   DL  │
  │     Vie 10      Mar 14     Mié 15     Jue 16   V17 │
  │       ▼           ▼          ▼          ▼        ▼  │
  │  [Dev listo]  [CR aprobado] [QA inicia] [QA done]   │
  └─────────────────────────────────────────────────────┘
  ```
- **📖 Interpretación**:
  - Referencia visual de las **fechas límite**. Cada milestone es un gate.
  - Si un ticket no pasó el gate a tiempo, no entra en la versión.
  - **Acción**: Compartir con el equipo al inicio del sprint.

---

## Sección B: Estado de Tickets por Categoría

### Widget B.1 — Regression Fixes (Filtered Table)
- **Tipo**: Task List
- **Filter**: Tag = `qa-regression-v0.1.0`
- **Sort**: Status (pipeline order), then Priority (desc)
- **Columnas**: Custom ID, Name, Status, Priority, Assignee, Iond Subcategory, Merge Request
- **📖 Interpretación**:
  - **Lista maestra** de fixes de regresión. Fuente de verdad para el release.
  - Revisar **diariamente**. Cada ticket debería avanzar al menos un status por semana.
  - **🚨 Alerta**: Ticket sin Merge Request → dev no abrió PR. Follow-up inmediato.
  - **Código de colores por status**: Leer de arriba (completados) a abajo (pendientes) para ver el progreso.

### Widget B.2 — Features del Sprint (Filtered Table)
- **Tipo**: Task List
- **Filter**: Type = `New Feature` AND Status NOT IN (`done`)
- **Sort**: Status (pipeline order), then Priority (desc)
- **Columnas**: Custom ID, Name, Status, Priority, Assignee, Project, Merge Request
- **📖 Interpretación**:
  - Features nuevas que podrían entrar en la versión.
  - **Prioridad**: Siempre después de los regression fixes. Features incompletas pueden moverse a next sin riesgo.
  - **Acción**: Si una feature está en `code review` y un regression fix en `qa testing`, priorizar el fix.

### Widget B.3 — Improvements & Others (Filtered Table)
- **Tipo**: Task List
- **Filter**: Type IN (`Improvement`) OR Project NOT IN (`Iond`)
- **Sort**: Priority (desc)
- **Columnas**: Custom ID, Name, Status, Priority, Assignee, Project
- **📖 Interpretación**:
  - Tickets de mejora y de otros proyectos (Gateway, IonMind).
  - **Prioridad más baja** que fixes y features. Entran si hay tiempo.
  - **Acción**: Al final del sprint, si quedan pendientes → mover a next sin culpa.

---

## Sección C: Análisis por Dimensión

### Widget C.1 — Core vs UX/UI (Pie Chart)
- **Tipo**: Pie Chart
- **Filter**: Tag IN (`iond-core-issue`, `iond-uxui-issue`)
- **Group by**: Tag
- **📖 Interpretación**:
  - **Balance saludable**: ~40% core / ~60% UX/UI es normal en productos en crecimiento.
  - **Mayoría core** (>60%): Backend tiene deuda técnica. Riesgo de inestabilidad. Priorizar estos fixes.
  - **Mayoría UX/UI** (>70%): Bugs cosméticos. Core estable. Menor urgencia pero afecta percepción.
  - **Tendencia**: Este ratio debería mejorar (menos core) sprint a sprint a medida que el producto madura.

### Widget C.2 — Tickets por Módulo (Bar Chart)
- **Tipo**: Bar Chart
- **Filter**: Tag = `qa-regression-v0.1.0`
- **Group by**: Iond Subcategory
- **Stack by**: Status
- **📖 Interpretación**:
  - Muestra **qué módulos tienen más bugs de regresión**. Indica dónde la versión anterior fue frágil.
  - **Insight histórico**: Módulo que aparece con muchos fixes sprint a sprint → necesita refactoring o más tests unitarios.
  - **Acción dev lead**: Módulos con >3 regression fixes → code review más estricto en el futuro.
  - **Acción QA**: Estos módulos necesitan smoke tests más robustos en la regression suite.

### Widget C.3 — Tickets por Proyecto (Donut Chart)
- **Tipo**: Donut Chart
- **Source**: Sprint activo
- **Group by**: Project (Iond, Gateway, IonMind)
- **📖 Interpretación**:
  - Distribución del release por producto.
  - **Release mixto** (>2 proyectos): Mayor riesgo de integración. Smoke test más exhaustivo.
  - **Release mono-proyecto**: Más enfocado, menor riesgo.
  - **Acción**: Si mixto, coordinar deploys (ej: Gateway antes que Iond si hay dependencias).

---

## Sección D: Release Readiness

### Widget D.1 — Regression Fix Completion (Progress Bar)
- **Tipo**: Battery/Progress widget
- **Filter**: Tag = `qa-regression-v0.1.0`
- **Value**: % de tickets con Status = `ready to merge` o `done`
- **📖 Interpretación**:
  - **100%** 🟢 = Todos los fixes listos. Release seguro.
  - **80-99%** 🟡 = Casi listo. Pendientes probablemente pueden ir a next.
  - **<80%** 🔴 = Release riesgoso. Bugs conocidos sin resolver.
  - **Regla**: Nunca release con <80% si los pendientes son `high/urgent`.

### Widget D.2 — Outstanding PRs (Filtered List)
- **Tipo**: Task List
- **Filter**: Status IN (`code review`, `ready to merge`) AND Merge Request IS NOT EMPTY
- **Columnas**: Custom ID, Name, Merge Request, Merge Request 2, Merge Request 3
- **📖 Interpretación**:
  - PRs que **necesitan merge** antes de crear el release branch/tag.
  - **Acción pre-release**: Verificar que todos estos PRs están merged y CI/CD pasa.
  - **🚨 Alerta**: PRs con conflictos de merge → resolución manual del dev.
  - **Checklist**: Todos listados aquí deben estar merged antes del release.

### Widget D.3 — Bug Debt (Number Widget)
- **Tipo**: Single number
- **Filter**: Type = `Bug` AND Status NOT IN (`done`, `ready to merge`)
- **📖 Interpretación**:
  - Número de **bugs abiertos** que no están resueltos. Es la "deuda de bugs" del producto.
  - **Meta**: Reducir sprint a sprint.
  - **<5** 🟢 = Deuda manejable.
  - **5-15** 🟡 = Normal en desarrollo activo.
  - **>15** 🔴 = Necesita sprint de estabilización.
