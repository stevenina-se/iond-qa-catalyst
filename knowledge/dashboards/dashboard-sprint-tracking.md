# Dashboard: Sprint Tracking — Seguimiento del Sprint

> **Audiencia**: Scrum Master, QA Engineer, Developers
> **Frecuencia**: Diario (standup) + semanal (mid-sprint check)
> **Pregunta central**: "¿Cómo va el sprint? ¿Quién necesita ayuda?"

---

## Campos y filtros utilizados

| Campo | Filtro | Uso |
|-------|--------|-----|
| `Status` | Pipeline completo | Posición del ticket |
| `Priority` | urgent, high, normal, low | Urgencia |
| `Assignee` | Todos los devs + QA | Responsable |
| `Reviewer QA` | Steve Nina | QA asignado |
| `Merge Request` | URLs de PRs | Link al código |
| `Tags` | `qa-regression-v*` | Identificar fixes |

---

## Sección A: Vista General del Sprint

### Widget A.1 — Sprint Progress (Status Pie Chart)
- **Tipo**: Pie Chart
- **Source**: Lista del Sprint activo
- **Group by**: Status
- **Colores**:
  - `sprint intake` → gris | `fortification` → azul | `code review` → naranja
  - `qa testing` → amarillo | `qa in process` → cyan
  - `ready to merge` → verde | `blocked` → rojo | `done` → verde oscuro
- **📖 Interpretación**:
  - **Semana 1**: Normal ver mucho azul (fortification) y gris (intake). Si >50% está en gris al cierre de semana 1, el sprint está atrasado.
  - **Semana 2**: El pie debe moverse hacia naranja→amarillo→verde. Si aún hay mucho azul, hay riesgo de no completar.
  - **🚨 Alerta**: Rojo (blocked) en cualquier momento = acción inmediata.
  - **✅ Ideal al cierre**: >70% verde, 0% rojo.

### Widget A.2 — Tickets por Prioridad (Stacked Bar Chart)
- **Tipo**: Bar Chart
- **Source**: Sprint activo
- **Group by**: Priority
- **Stack by**: Status
- **📖 Interpretación**:
  - Verifica que los tickets `high/urgent` **avanzan más rápido** que los de `normal/low`.
  - **🚨 Alerta**: Si `high/urgent` siguen en `fortification` a mitad de sprint, el equipo no está priorizando correctamente. Escalar al Scrum Master.
  - **✅ Ideal**: Las barras de `urgent` y `high` deberían ser mayormente verdes antes que las de `normal` y `low`.

### Widget A.3 — Burndown Chart
- **Tipo**: Sprint Burndown (nativo ClickUp)
- **Source**: Sprint activo
- **📖 Interpretación**:
  - La línea real debe seguir la línea ideal (diagonal descendente).
  - **📉 Por debajo** de la ideal = adelantados (excelente).
  - **📈 Por encima** de la ideal = atrasados. Considerar reducir scope.
  - **Línea plana** por >2 días = nada avanza, hay bloqueo sistémico.
  - **Caída pronunciada al final** = tickets completados en bloque. Aceptable pero no ideal (indica que devs entregan todo al final).

### Widget A.4 — Blocked Tickets (Filtered List)
- **Tipo**: Task List
- **Filter**: Status = `blocked`
- **Columnas**: Custom ID, Name, Assignee, Priority, Tags
- **📖 Interpretación**:
  - **Este widget debería estar VACÍO.** Cada ticket aquí es un problema activo.
  - **🚨 Alerta**: Ticket bloqueado `high/urgent` → acción en <24h.
  - **Acción**: Para cada uno preguntar: ¿Qué lo bloquea? ¿Dependencia externa? ¿Mover a next sprint?
  - **Métrica**: Tiempo promedio en `blocked` no debe superar 3 días hábiles.

---

## Sección B: Seguimiento a Developers

### Widget B.1 — Workload por Developer (Stacked Bar Chart)
- **Tipo**: Stacked Bar Chart
- **Source**: Sprint activo
- **Group by**: Assignee
- **Stack by**: Status
- **📖 Interpretación**:
  - Barra más alta = dev con más tickets. Colores muestran en qué fase están.
  - **🚨 Alerta si**:
    - Un dev tiene barra muy alta con mucho azul (fortification) → no va a entregar a tiempo.
    - Un dev tiene mucho naranja (code review) → el bottleneck es el CR, no el dev.
  - **✅ Ideal**: Barras similares (3-5 tickets), colores avanzando hacia verde día a día.
  - **Acción**: Dev con >6 tickets → reasignar los de baja prioridad a otro dev.

### Widget B.2 — Code Reviews Pendientes (Filtered List)
- **Tipo**: Task List
- **Filter**: Status = `code review`
- **Group by**: Assignee
- **Columnas**: Custom ID, Name, Priority, Merge Request, Date Updated
- **Sort**: Date Updated (asc) → los más antiguos primero
- **📖 Interpretación**:
  - Tickets **esperando aprobación de CR** y hace cuánto tiempo.
  - **🚨 Alerta**: Ticket con >3 días en `code review` = bottleneck. El reviewer no revisa o hay feedback sin resolver.
  - **Regla del equipo**: CR debería completarse en ≤2 días hábiles.
  - **Acción**: Follow-up a reviewers de tickets más antiguos. Priorizar CRs de tickets `high/urgent` y `qa-regression-v*`.

### Widget B.3 — Developer × Priority (Table/Heatmap)
- **Tipo**: Table widget
- **Source**: Sprint activo
- **Group by**: Assignee
- **Columns**: Count by Priority (urgent, high, normal, low)
- **📖 Interpretación**:
  - **Heatmap de presión**: Devs con muchos `high/urgent` están bajo más presión.
  - **🚨 Alerta**: Dev con >3 tickets `high` → sobrecargado de trabajo crítico. Redistribuir.
  - **Balance ideal**: Mix de prioridades por dev (no todo `high`).
  - **Oportunidad**: Dev con solo `low/normal` puede asumir un `high` de un compañero sobrecargado.

### Widget B.4 — Tickets sin PR (Filtered List)
- **Tipo**: Task List
- **Filter**: Status IN (`code review`, `qa testing`) AND Merge Request IS EMPTY
- **📖 Interpretación**:
  - **Anomalías de proceso**. Ticket en CR sin PR = no hay código para revisar.
  - **🚨 Alerta**: Todo ticket aquí es error de proceso. Dev movió status sin abrir PR.
  - **Acción inmediata**: Contactar al dev → agregar URL del PR al field `Merge Request`.
  - **Para QA**: No testear tickets sin PR — no hay código verificable.

---

## Sección C: Seguimiento a QA

### Widget C.1 — Mi Cola de Testing (Filtered List)
- **Tipo**: Task List
- **Filter**: Status IN (`qa testing`, `qa in process`) AND Reviewer QA = Steve Nina
- **Sort**: Priority (desc), Tags (regression first)
- **Columnas**: Custom ID, Name, Status, Priority, Assignee, Iond Subcategory, Tags
- **📖 Interpretación**:
  - Tu **lista de trabajo diaria**. De arriba a abajo = orden de ejecución.
  - **Regla**: Tickets con tag `qa-regression-v*` siempre van primero.
  - `qa testing` = listo para empezar. `qa in process` = ya empezaste.
  - **🚨 Alerta**: >5 tickets en cola = acumulando deuda. Pedir ayuda o re-priorizar.
  - **✅ Ideal**: 1-3 tickets en cola.

### Widget C.2 — Próximos en Cola (Filtered List)
- **Tipo**: Task List
- **Filter**: Status = `code review`
- **Sort**: Priority (desc)
- **Columnas**: Custom ID, Name, Assignee, Merge Request, Tags
- **📖 Interpretación**:
  - Tickets que **llegarán a tu cola cuando CR apruebe**. Planifica tu carga futura.
  - **🚨 Alerta**: Lista larga (>6) en semana 2 = avalancha de testing al final. Presionar para CR más rápido.
  - **Acción**: Ticket >3 días en CR → follow-up al dev/reviewer.

### Widget C.3 — QA Completados (Filtered List)
- **Tipo**: Task List
- **Filter**: Status IN (`ready to merge`, `done`) AND Reviewer QA = Steve Nina
- **Columnas**: Custom ID, Name, Assignee, Iond Subcategory
- **📖 Interpretación**:
  - Tu **registro de productividad**. Cuántos tickets aprobaste.
  - **Benchmark**: 8-12 tickets aprobados por sprint de 2 semanas.
  - **✅ Bueno**: Lista creciendo día a día = ritmo constante.
  - **🚨 Alerta**: Vacía a mitad de sprint = devs no entregan a QA a tiempo.

### Widget C.4 — QA Stats (Number Widgets)
- **Tipo**: 4 calculation widgets
  - 📥 Total en cola
  - ✅ Aprobados
  - ❌ Rechazados (por tag `qa-rejected`)
  - 📊 Tasa de aprobación (%)
- **📖 Interpretación**:
  - **Tasa de aprobación** = calidad del código que llega a QA.
    - **>85%** 🟢 Excelente — devs entregan código limpio.
    - **70-85%** 🟡 Aceptable — algunos tickets necesitan re-work.
    - **<70%** 🔴 Problema — devs no testean antes de enviar. Escalar al Scrum Master.
  - Cola > Aprobados a mitad de sprint = acumulando deuda de testing.

### Widget C.5 — Testing por Módulo (Pie Chart)
- **Tipo**: Pie Chart
- **Filter**: Status IN (`qa testing`, `qa in process`, `ready to merge`)
- **Group by**: Iond Subcategory
- **📖 Interpretación**:
  - Qué módulos concentran más QA. Si uno domina (>40%), hubo cambios grandes → más atención.
  - **Acción**: Módulo dominante → testing por lote (todos sus tickets juntos para aprovechar contexto).
  - **Tendencia**: Módulo que aparece repetidamente sprint a sprint → necesita más automatización E2E.
