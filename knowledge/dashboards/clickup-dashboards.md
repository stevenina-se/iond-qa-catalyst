# ClickUp Dashboards — Propuesta de Seguimiento QA

> Basado en los tags y custom fields actuales del espacio NEW GATEWAY IOND.
> Cada dashboard usa campos existentes — no requiere crear campos nuevos.

---

## Campos disponibles para filtros

### Custom Fields
| Campo | Valores conocidos | Uso |
|-------|-------------------|-----|
| `Iond Subcategory` | Boards, PDF Templates, Connections, App Connectors, Templates, Billing, Company Schedules, Nodo Simple Decision | Clasificar por módulo |
| `Iond.Version` | DEVELOPMENT | Target version del ticket |
| `Project` | Iond, iod, Gateway, IonMind | Producto/proyecto |
| `Type` | Bug, New Feature, Improvement | Tipo de ticket |
| `Reviewer QA` | Steve Nina | QA asignado |
| `Merge Request` / `Merge Request 2` / `Merge Request 3` | URLs de PRs | Links a PRs |

### Tags
| Tag | Significado |
|-----|-------------|
| `qa-regression-v0.1.0` | Bug encontrado en v0.1.0 — va a la next version |
| `iond-core-issue` | Afecta el core de la plataforma (backend, lógica de negocio) |
| `iond-uxui-issue` | Afecta UX/UI (frontend, experiencia de usuario) |
| `iond-ib-ns` | Internal Bug — No Severity (bug interno sin severidad definida) |

### Statuses (Pipeline)
```
sprint intake → fortification → code review → qa testing → qa in process → ready to merge → done
                                                                                    └→ blocked
```

---

## Dashboard 1: 🎯 Sprint Overview

> **Propósito**: Vista general del sprint activo. El Scrum Master y QA lo revisan diario.
> **Pregunta que responde**: "¿Cómo va el sprint? ¿Estamos a tiempo?"

### Widgets

#### Widget 1.1 — Sprint Progress (Status Pie Chart)
- **Tipo**: Pie Chart
- **Source**: Lista del Sprint activo (ej: "Sprint 4 (7/6 - 7/19)")
- **Group by**: Status
- **Colores**:
  - `sprint intake` → gris
  - `fortification` → azul
  - `code review` → naranja
  - `qa testing` → amarillo
  - `qa in process` → cyan
  - `ready to merge` → verde
  - `blocked` → rojo
  - `done` → verde oscuro
- **📖 Interpretación**:
  - **Semana 1**: Es normal ver mucho azul (fortification) y gris (intake). Si >50% está en gris al final de semana 1, el sprint está atrasado.
  - **Semana 2**: El pie debería moverse hacia naranja→amarillo→verde. Si aún hay mucho azul, hay riesgo de no completar.
  - **🚨 Alerta**: Si hay rojo (blocked) en cualquier momento, requiere atención inmediata.
  - **✅ Ideal al cierre**: >70% verde (ready to merge/done), 0% rojo.

#### Widget 1.2 — Tickets por Prioridad (Bar Chart)
- **Tipo**: Bar Chart
- **Source**: Lista del Sprint activo
- **Group by**: Priority
- **Stack by**: Status
- **📖 Interpretación**:
  - Muestra si los tickets de **alta prioridad avanzan más rápido** que los de baja.
  - **🚨 Alerta**: Si los tickets `high/urgent` siguen en `fortification` o `sprint intake` a mitad de sprint, el equipo no está priorizando correctamente.
  - **✅ Ideal**: Las barras de `urgent` y `high` deberían ser mayormente verdes (ready to merge) antes que las de `normal` y `low`.
  - **Acción**: Si `high` está estancado, escalar al Scrum Master para re-priorizar.

#### Widget 1.3 — Burndown / Velocity
- **Tipo**: Sprint Burndown widget (nativo de ClickUp)
- **Source**: Lista del Sprint activo
- **📖 Interpretación**:
  - La línea real debe seguir la línea ideal (diagonal descendente).
  - **🚨 Alerta**: Si la línea real está **por encima** de la ideal, el sprint está atrasado. Considerar reducir scope.
  - **✅ Ideal**: Línea real por debajo o sobre la ideal. Caídas pronunciadas al final indican que los tickets se completan en bloque (no ideal pero aceptable).
  - **Pattern negativo**: Línea plana durante varios días = nada se está completando, hay bloqueo sistémico.

#### Widget 1.4 — Tickets por Assignee (Table)
- **Tipo**: Table / List widget
- **Source**: Lista del Sprint activo
- **Columnas**: Custom ID, Name, Status, Priority, Assignee, Tags
- **Group by**: Assignee
- **Sort**: Priority (desc)
- **📖 Interpretación**:
  - Vista rápida de **quién tiene qué** y en qué estado.
  - **🚨 Alerta**: Un developer con >5 tickets activos probablemente es un bottleneck.
  - **✅ Ideal**: Distribución equilibrada (3-5 tickets por dev). Los tickets de cada dev deberían avanzar en pipeline día a día.
  - **Acción**: Si un dev tiene todos sus tickets en el mismo status por >2 días, necesita follow-up.

#### Widget 1.5 — Blocked Tickets (Filtered List)
- **Tipo**: Task List widget
- **Filter**: Status = `blocked`
- **Columnas**: Custom ID, Name, Assignee, Priority, Tags
- **📖 Interpretación**:
  - **Este widget debería estar VACÍO**. Cada ticket aquí es un problema activo.
  - **🚨 Alerta**: Cualquier ticket bloqueado de prioridad `high` o `urgent` necesita acción en <24h.
  - **Acción**: Para cada ticket bloqueado, preguntar: ¿Qué lo bloquea? ¿Es una dependencia externa? ¿Podemos moverlo al siguiente sprint?
  - **Métrica**: Tiempo promedio en `blocked` no debe superar 3 días hábiles.

---

## Dashboard 2: 🔬 QA Pipeline

> **Propósito**: Vista exclusiva del QA Engineer. Muestra qué necesita testing, qué está en proceso, y qué ya se aprobó.
> **Pregunta que responde**: "¿Qué debo testear hoy? ¿Cuánto me falta?"

### Widgets

#### Widget 2.1 — Mi Cola de Testing (Filtered List)
- **Tipo**: Task List widget
- **Filter**: Status IN (`qa testing`, `qa in process`) AND Reviewer QA = Steve Nina
- **Sort**: Priority (desc), then by Tags (regression first)
- **Columnas**: Custom ID, Name, Status, Priority, Assignee, Iond Subcategory, Tags
- **📖 Interpretación**:
  - Esta es tu **lista de trabajo diaria**. Los tickets de arriba son los que debes testear primero.
  - **🚨 Alerta**: Si esta lista tiene >5 tickets, estás acumulando cola. Considera pedir ayuda o re-priorizar.
  - **Regla**: Tickets con tag `qa-regression-v*` siempre van primero — son fixes de regresión críticos.
  - **`qa testing`** = listo para que empieces. **`qa in process`** = ya lo empezaste.
  - **✅ Ideal**: 1-3 tickets en cola, priorizados por severity.

#### Widget 2.2 — Próximos en Cola (Filtered List)
- **Tipo**: Task List widget
- **Filter**: Status = `code review`
- **Sort**: Priority (desc)
- **Columnas**: Custom ID, Name, Assignee, Merge Request, Tags
- **📖 Interpretación**:
  - Estos tickets **llegarán a tu cola cuando CR apruebe**. Te permite planificar tu carga futura.
  - **🚨 Alerta**: Si esta lista es larga (>6 tickets) y estamos en semana 2, habrá una avalancha de testing al final. Presionar para que CR apruebe más rápido.
  - **✅ Ideal**: Los tickets con tag `qa-regression-v*` deberían tener CR aprobado lo antes posible.
  - **Acción**: Si un ticket lleva >3 días en `code review`, enviar follow-up al dev/reviewer.

#### Widget 2.3 — QA Completados en este Sprint (Filtered List)
- **Tipo**: Task List widget
- **Filter**: Status IN (`ready to merge`, `done`) AND Reviewer QA = Steve Nina
- **Columnas**: Custom ID, Name, Assignee, Iond Subcategory
- **📖 Interpretación**:
  - Tu **registro de productividad**. Cuántos tickets aprobaste en este sprint.
  - **Benchmark**: En un sprint de 2 semanas, un QA Engineer debería aprobar 8-12 tickets.
  - **✅ Bueno**: Lista creciendo día a día. Indica ritmo constante de testing.
  - **🚨 Alerta**: Si está vacía a mitad de sprint, los devs no están entregando a QA a tiempo.

#### Widget 2.4 — QA Stats (Battery/Number widgets)
- **Tipo**: Calculation widgets (4 números)
  - Total en cola: Count where Status IN (`qa testing`, `qa in process`)
  - Aprobados: Count where Status IN (`ready to merge`, `done`)
  - Rechazados: _(manual o por tag `qa-rejected`)_
  - Tasa de aprobación: Aprobados / (Aprobados + Rechazados) × 100
- **📖 Interpretación**:
  - **Tasa de aprobación**: Mide la calidad del código que llega a QA.
    - **>85%** = 🟢 Excelente. Los devs entregan código limpio.
    - **70-85%** = 🟡 Aceptable. Algunos tickets necesitan re-work.
    - **<70%** = 🔴 Problema. Los devs no están testeando antes de enviar a QA. Escalar al Scrum Master.
  - **Cola vs Aprobados**: Si Cola > Aprobados a mitad de sprint, estás acumulando deuda de testing.

#### Widget 2.5 — Distribución por Módulo (Pie Chart)
- **Tipo**: Pie Chart
- **Filter**: Status IN (`qa testing`, `qa in process`, `ready to merge`)
- **Group by**: Iond Subcategory
- **📖 Interpretación**:
  - Muestra **qué módulos concentran más trabajo de QA**. Útil para planificar el día.
  - **Insight**: Si un módulo domina (>40%), probablemente hubo cambios grandes o un refactor. Requiere más atención.
  - **Acción**: Si un módulo tiene muchos tickets, considerar hacer testing por lote (testear todos los tickets del módulo juntos para aprovechar el contexto).
  - **Tendencia**: Módulos que aparecen repetidamente sprint a sprint necesitan más automatización E2E.

---

## Dashboard 3: 🏷️ Version Tracker

> **Propósito**: Seguimiento de una versión específica (ej: v0.1.1). Filtra por tags de regresión.
> **Pregunta que responde**: "¿Cuántos fixes de regresión están listos para la próxima versión?"

### Widgets

#### Widget 3.1 — Regression Fixes Progress (Status Bar)
- **Tipo**: Bar/Status chart
- **Filter**: Tag = `qa-regression-v0.1.0`
- **Group by**: Status
- **📖 Interpretación**:
  - Muestra el **progreso de todos los fixes de regresión** para la versión.
  - **🚨 Alerta**: Si hay tickets en `sprint intake` o `fortification` después del QA CUTOFF, esos fixes no entrarán en la versión. Deben moverse a la siguiente.
  - **✅ Ideal al cierre**: 100% en `ready to merge` o `done`. Todo fix de regresión resuelto.
  - **Métrica clave**: % de regression fixes completados = indicador de calidad del release.

#### Widget 3.2 — Core vs UX/UI (Pie Chart)
- **Tipo**: Pie Chart
- **Filter**: Tag IN (`iond-core-issue`, `iond-uxui-issue`)
- **Group by**: Tag
- **📖 Interpretación**:
  - **Balance saludable**: ~40% core / ~60% UX/UI es normal en productos en crecimiento.
  - **Mayoría core** (>60%): El backend tiene deuda técnica significativa. Riesgo de inestabilidad.
  - **Mayoría UX/UI** (>70%): Los bugs son cosméticos/de experiencia. El core es estable.
  - **Acción**: Si core domina, priorizar esos fixes — afectan funcionalidad real. Los UX/UI pueden ir después.

#### Widget 3.3 — Regression Fix List (Table)
- **Tipo**: Task List widget
- **Filter**: Tag = `qa-regression-v0.1.0`
- **Sort**: Status (pipeline order), then Priority
- **Columnas**: Custom ID, Name, Status, Priority, Assignee, Iond Subcategory, Merge Request
- **📖 Interpretación**:
  - **Lista maestra** de todos los fixes de regresión. Es la fuente de verdad para el release.
  - **Acción**: Revisar diariamente. Cada ticket debería avanzar al menos un status por semana.
  - **🚨 Alerta**: Tickets sin Merge Request asignado → el dev aún no abrió PR. Requiere follow-up.

#### Widget 3.4 — Version Timeline (Gantt o Custom)
- **Tipo**: Línea de tiempo o texto embebido
- **Contenido**: Cutoff dates de la versión
  ```
  DEV CUTOFF → CR CUTOFF → QA CUTOFF → FREEZE → DEADLINE
  ```
- **📖 Interpretación**:
  - Referencia visual de **las fechas límite** del sprint.
  - Cada milestone es un gate: si un ticket no pasó el gate a tiempo, no entra en la versión.
  - **Acción**: Compartir con el equipo al inicio del sprint para que todos conozcan los deadlines.

#### Widget 3.5 — Regression by Module (Bar Chart)
- **Tipo**: Bar Chart
- **Filter**: Tag = `qa-regression-v0.1.0`
- **Group by**: Iond Subcategory
- **Stack by**: Status
- **📖 Interpretación**:
  - Muestra **qué módulos tienen más bugs de regresión**. Indica dónde la versión anterior fue más frágil.
  - **Insight histórico**: Si un módulo aparece con muchos fixes sprint a sprint, necesita refactoring o más tests unitarios.
  - **Acción para el dev lead**: Módulos con >3 regression fixes deberían recibir code review más estricto en el futuro.
  - **Acción para QA**: Estos módulos necesitan smoke tests más robustos en la regression suite.

---

## Dashboard 4: 👥 Developer Load

> **Propósito**: Ver la carga de trabajo de cada developer y detectar bottlenecks.
> **Pregunta que responde**: "¿Quién está sobrecargado? ¿Dónde está el bottleneck del pipeline?"

### Widgets

#### Widget 4.1 — Workload por Developer (Bar Chart)
- **Tipo**: Stacked Bar Chart
- **Source**: Lista del Sprint activo
- **Group by**: Assignee
- **Stack by**: Status
- **📖 Interpretación**:
  - La barra más alta = dev con más tickets. Los colores muestran en qué fase están.
  - **🚨 Alerta**: Si un dev tiene una barra muy alta con mucho azul (fortification), está en riesgo de no entregar a tiempo.
  - **🚨 Alerta**: Si un dev tiene mucho naranja (code review), el bottleneck es el CR — no el dev.
  - **✅ Ideal**: Barras de tamaño similar (3-5 tickets), con colores avanzando hacia verde a lo largo del sprint.
  - **Acción**: Si un dev tiene >6 tickets, considerar reasignar los de baja prioridad.

#### Widget 4.2 — Code Reviews Pendientes (Filtered List)
- **Tipo**: Task List widget
- **Filter**: Status = `code review`
- **Group by**: Assignee
- **Columnas**: Custom ID, Name, Priority, Merge Request, date updated
- **Sort**: Date Updated (asc) → los más antiguos primero
- **📖 Interpretación**:
  - Muestra **qué tickets están esperando CR** y hace cuánto tiempo.
  - **🚨 Alerta**: Un ticket con >3 días en `code review` es un bottleneck. El reviewer no está revisando o hay feedback sin resolver.
  - **Regla del equipo**: CR debería completarse en ≤2 días hábiles.
  - **Acción**: Enviar follow-up a los reviewers de los tickets más antiguos. Priorizar CRs de tickets `high/urgent`.

#### Widget 4.3 — Developer × Priority (Heatmap/Table)
- **Tipo**: Table widget
- **Source**: Sprint activo
- **Group by**: Assignee
- **Columns**: Count by Priority (urgent, high, normal, low)
- **📖 Interpretación**:
  - **Heatmap de presión**: Devs con muchos tickets `high/urgent` están bajo más presión.
  - **🚨 Alerta**: Si un dev tiene >3 tickets `high`, está sobrecargado de trabajo crítico. Considerar redistribuir.
  - **Balance ideal**: Cada dev debería tener mix de prioridades (no todo `high`).
  - **Acción**: Si un dev solo tiene `low/normal`, puede asumir un ticket `high` de un compañero sobrecargado.

#### Widget 4.4 — Tickets sin PR (Filtered List)
- **Tipo**: Task List widget
- **Filter**: Status IN (`code review`, `qa testing`) AND Merge Request IS EMPTY
- **📖 Interpretación**:
  - **Estos tickets son anomalías**. Un ticket en `code review` sin PR no tiene código para revisar.
  - **🚨 Alerta**: Todo ticket aquí es un error de proceso. El dev movió el status sin abrir PR.
  - **Acción inmediata**: Contactar al dev y pedir que agregue la URL del PR al custom field `Merge Request`.
  - **Para QA**: No testear tickets sin PR — no hay código verificable para revisar.

---

## Dashboard 5: 🐛 Bug Tracker

> **Propósito**: Seguimiento de todos los bugs (internos y de QA) a lo largo del proyecto.
> **Pregunta que responde**: "¿Estamos mejorando la calidad? ¿Qué módulos son más problemáticos?"

### Widgets

#### Widget 5.1 — Bugs por Tipo de Issue (Pie Chart)
- **Tipo**: Pie Chart
- **Filter**: Type = `Bug`
- **Group by**: Tags (filtrar solo `iond-core-issue`, `iond-uxui-issue`)
- **📖 Interpretación**:
  - **Core issues** = afectan funcionalidad, datos, o lógica de negocio. Impacto alto en usuarios.
  - **UX/UI issues** = afectan experiencia visual, usabilidad, interacción. Impacto en percepción.
  - **Balance ideal**: 30-40% core, 60-70% UX/UI indica que el core es estable y se está puliendo la experiencia.
  - **🚨 Alerta**: Si core >50%, hay problemas fundamentales. Necesita sprint dedicado a estabilización.
  - **Tendencia**: Este ratio debería ir mejorando (menos core) sprint a sprint a medida que el producto madura.

#### Widget 5.2 — Bugs por Módulo (Bar Chart)
- **Tipo**: Bar Chart
- **Filter**: Type = `Bug`
- **Group by**: Iond Subcategory
- **Sort**: Count (desc)
- **📖 Interpretación**:
  - El módulo con la barra más alta es el **más problemático**. Necesita atención especial.
  - **Acción para QA**: Los top 3 módulos deberían tener regression tests más exhaustivos.
  - **Acción para devs**: Módulos con muchos bugs repetidos necesitan refactoring o más tests unitarios.
  - **Benchmark**: Ningún módulo debería tener >5 bugs abiertos simultáneamente. Si lo tiene, es un red flag.
  - **Tendencia**: Monitorear si un módulo baja de posición sprint a sprint = está mejorando.

#### Widget 5.3 — Bug Trend (Line Chart)
- **Tipo**: Line Chart
- **Filter**: Type = `Bug`
- **X-axis**: Date Created (por semana)
- **Y-axis**: Count
- **📖 Interpretación**:
  - **Tendencia descendente** 📉 = El equipo está produciendo menos bugs. El producto es más estable.
  - **Tendencia ascendente** 📈 = Se están encontrando más bugs. Puede ser bueno (QA más exhaustivo) o malo (código menos estable).
  - **Picos**: Un pico en una semana indica un release o refactor grande que introdujo bugs.
  - **Meseta**: Número constante de bugs por semana indica estado estacionario — normal en productos en desarrollo activo.
  - **Meta a largo plazo**: La línea debería tender a bajar a medida que el producto madura.

#### Widget 5.4 — Internal Bugs sin Priorizar (Filtered List)
- **Tipo**: Task List widget
- **Filter**: Tag = `iond-ib-ns` (Internal Bug No Severity)
- **Sort**: Date Created (asc)
- **📖 Interpretación**:
  - Bugs encontrados internamente que **nadie ha clasificado aún**. Son deuda de triaje.
  - **🚨 Alerta**: Si esta lista crece sprint a sprint, el equipo no está priorizando. Necesita sesión de triaje.
  - **Acción**: En cada sprint planning, dedicar 15 min a clasificar los bugs de esta lista (asignar severity, módulo, versión).
  - **Meta**: Esta lista debería tener 0 items al final de cada sprint.

#### Widget 5.5 — Bugs Abiertos por Prioridad (Number widgets)
- **Tipo**: 4 calculation widgets
  - 🔴 Urgent bugs abiertos
  - 🟠 High bugs abiertos
  - 🟡 Normal bugs abiertos
  - 🔵 Low bugs abiertos
- **📖 Interpretación**:
  - **🔴 Urgent = 0**: Ideal. Si >0, son showstoppers que bloquean el release.
  - **🟠 High ≤ 3**: Aceptable. Si >5, el producto tiene problemas serios pendientes.
  - **🟡 Normal ≤ 10**: Aceptable para un producto en desarrollo activo.
  - **🔵 Low**: No hay límite práctico, pero si >20, considerar cerrar los irrelevantes.
  - **Acción**: Los urgent deben resolverse en el sprint actual. Los high deberían planificarse para el próximo sprint.

---

## Dashboard 6: 🚀 Release Readiness

> **Propósito**: Evaluar si una versión está lista para release. Se usa al final del sprint.
> **Pregunta que responde**: "¿Podemos hacer release? ¿Qué falta?"

### Widgets

#### Widget 6.1 — Release Scorecard (Number widgets)
- **Tipo**: 5 calculation widgets
  - Total tickets en la versión
  - ✅ Ready to merge
  - 🔬 En QA
  - 🔨 En desarrollo
  - 🚫 Bloqueados
- **📖 Interpretación**:
  - **GO para release cuando**: Ready to merge ≥ 80% del total Y Bloqueados = 0 Y En QA = 0.
  - **NO-GO si**: Bloqueados > 0 con prioridad `high/urgent`, o regression fixes en desarrollo.
  - **Parcial**: Si algunos tickets no-críticos están pendientes, se puede hacer release parcial moviendo esos tickets a la siguiente versión.
  - **Fórmula**: Release Readiness % = (Ready to merge + Done) / Total × 100.

#### Widget 6.2 — Regression Fix Completion (Progress Bar)
- **Tipo**: Battery/Progress widget
- **Filter**: Tag = `qa-regression-v0.1.0`
- **Value**: % de tickets con Status = `ready to merge` o `done`
- **📖 Interpretación**:
  - **100%** = 🟢 Todos los fixes de regresión están listos. Release seguro.
  - **80-99%** = 🟡 Casi listo. Los tickets faltantes probablemente pueden moverse a next.
  - **<80%** = 🔴 Release riesgoso. Hay bugs conocidos sin resolver.
  - **Regla**: Nunca hacer release con <80% de regression fixes completados si los pendientes son `high/urgent`.

#### Widget 6.3 — Outstanding PRs (Filtered List)
- **Tipo**: Task List widget
- **Filter**: Status IN (`code review`, `ready to merge`) AND Merge Request IS NOT EMPTY
- **Columnas**: Custom ID, Name, Merge Request, Merge Request 2
- **📖 Interpretación**:
  - **PRs que necesitan merge** antes de crear el release branch/tag.
  - **Acción**: Antes del release, verificar que todos estos PRs están merged en la rama correcta.
  - **🚨 Alerta**: PRs con conflictos de merge necesitan resolución manual del dev.
  - **Checklist pre-release**: Todos los PRs listados aquí deben estar merged y el CI/CD debe pasar.

#### Widget 6.4 — Tickets por Proyecto (Donut Chart)
- **Tipo**: Donut Chart
- **Source**: Sprint activo
- **Group by**: Project (Iond, Gateway, IonMind)
- **📖 Interpretación**:
  - Muestra la **distribución del release por producto**. ¿Es un release de Iond, Gateway, o mixto?
  - **Release mixto** (>2 proyectos): Mayor riesgo de integración. Requiere smoke test más exhaustivo.
  - **Release mono-proyecto**: Más enfocado, menor riesgo.
  - **Acción**: Si el release es mixto, verificar que los deploys se coordinan (ej: Gateway se deploya antes que Iond si hay dependencias).

---

## Resumen de Dashboards

| # | Dashboard | Audiencia | Frecuencia | Widgets | Pregunta clave |
|---|-----------|-----------|------------|---------|----------------|
| 1 | Sprint Overview | Scrum Master, Team | Diario | 5 | ¿Cómo va el sprint? |
| 2 | QA Pipeline | QA Engineer | Diario | 5 | ¿Qué debo testear hoy? |
| 3 | Version Tracker | QA + Scrum Master | Semanal | 5 | ¿Cuántos fixes están listos? |
| 4 | Developer Load | Scrum Master | Semanal | 4 | ¿Quién está sobrecargado? |
| 5 | Bug Tracker | QA + Product | Semanal | 5 | ¿Estamos mejorando la calidad? |
| 6 | Release Readiness | QA + Scrum Master | Pre-release | 4 | ¿Podemos hacer release? |

---

## Tags recomendados a agregar

> Para maximizar los dashboards, considerar agregar estos tags a los tickets futuros:

| Tag | Cuándo usar | Dashboard que lo usa |
|-----|------------|---------------------|
| `qa-approved` | Cuando QA aprueba el ticket | QA Pipeline, Release Readiness |
| `qa-rejected` | Cuando QA rechaza el ticket | QA Pipeline, Bug Tracker |
| `qa-regression-v{X.Y.Z}` | Bug encontrado en versión X.Y.Z | Version Tracker |
| `iond-core-issue` | Bug de backend/lógica | Bug Tracker, Version Tracker |
| `iond-uxui-issue` | Bug de frontend/UX | Bug Tracker, Version Tracker |
| `sprint-N` | Número de sprint | Sprint Overview |

> **Recomendación**: Empezar por Dashboard 1 (Sprint Overview) y Dashboard 2 (QA Pipeline) — son los más críticos para el día a día. Agregar los demás progresivamente.
