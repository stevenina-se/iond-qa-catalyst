# Dashboard: Sprint Review — Métricas para Retrospectiva

> **Audiencia**: Todo el equipo (Scrum Master, Devs, QA, Product)
> **Frecuencia**: Una vez al final de cada sprint (ceremonia de review)
> **Pregunta central**: "¿Qué logramos? ¿Qué aprendimos? ¿Cómo mejoramos?"

---

## Cuándo usar este dashboard

- **Día del sprint review** (último día del sprint o el siguiente lunes)
- Los datos deben ser del sprint **ya cerrado**
- Complementar con notas cualitativas del equipo

---

## Sección A: Resultados del Sprint

### Widget A.1 — Sprint Completion Rate (Donut Chart)
- **Tipo**: Donut Chart / Progress
- **Source**: Lista del Sprint cerrado
- **Value**: % de tickets con Status = `done` o `ready to merge`
- **📖 Interpretación**:
  - **¿Cuánto del sprint se completó?**
  - **>80%** 🟢 = Sprint exitoso. El equipo estimó bien y ejecutó.
  - **60-80%** 🟡 = Aceptable. Algunos tickets no se completaron — revisar por qué.
  - **<60%** 🔴 = Sprint problemático. Hubo sobre-estimación, bloqueos, o cambios de scope mid-sprint.
  - **Tendencia**: Comparar con sprints anteriores. Debería ser estable o mejorar.
  - **Acción si <70%**: En la retro, discutir: ¿Estimamos mal? ¿Hubo interrupciones? ¿Scope creep?

### Widget A.2 — Committed vs Completed (Bar Chart)
- **Tipo**: Grouped Bar Chart
- **Barras**:
  - Barra 1: Total tickets al inicio del sprint (committed)
  - Barra 2: Tickets completados (done + ready to merge)
  - Barra 3: Tickets agregados mid-sprint
  - Barra 4: Tickets removidos/pospuestos
- **📖 Interpretación**:
  - Compara lo **planeado vs lo ejecutado**.
  - **Barra 3 grande** (agregados) = scope creep. El equipo aceptó trabajo extra mid-sprint.
  - **Barra 4 grande** (removidos) = mal planning o prioridades cambiaron.
  - **✅ Ideal**: Barra 1 ≈ Barra 2, Barras 3-4 pequeñas.
  - **Acción**: Si agregados > 20% del committed, el equipo necesita proteger el scope del sprint.

### Widget A.3 — Tickets Completados por Status Final (Pie Chart)
- **Tipo**: Pie Chart
- **Source**: Sprint cerrado, todos los tickets
- **Group by**: Status
- **📖 Interpretación**:
  - Muestra la **foto final** del sprint.
  - `done` + `ready to merge` = completados.
  - `code review` + `qa testing` = no llegaron a tiempo.
  - `fortification` + `sprint intake` = ni se empezaron o no se terminaron.
  - **Insight**: Si hay muchos en `code review`, el bottleneck fue el CR, no el dev.
  - **Acción**: Discutir en retro los tickets que no cruzaron el finish line y por qué.

---

## Sección B: Velocidad y Productividad

### Widget B.1 — Velocity por Developer (Bar Chart)
- **Tipo**: Bar Chart
- **Source**: Sprint cerrado
- **Filter**: Status IN (`done`, `ready to merge`)
- **Group by**: Assignee
- **Value**: Count de tickets completados
- **📖 Interpretación**:
  - **Cuántos tickets completó cada dev**. NO es para comparar devs entre sí (la complejidad varía).
  - **Uso correcto**: Comparar cada dev **consigo mismo** sprint a sprint.
  - **🚨 Alerta**: Dev con 0 tickets completados → ¿estuvo bloqueado? ¿Trabajó en tickets grandes? ¿Estuvo ausente?
  - **Contexto**: Un dev que completó 2 tickets complejos aportó más que uno que completó 5 triviales.
  - **Acción**: No usar para presionar. Usar para entender carga y ayudar.

### Widget B.2 — Tickets por Tipo (Pie Chart)
- **Tipo**: Pie Chart
- **Source**: Sprint cerrado, completados
- **Group by**: Type (Bug, New Feature, Improvement)
- **📖 Interpretación**:
  - **¿En qué se gastó el sprint?**
  - **Mayoría bugs** (>50%): Sprint de estabilización. Necesario pero no agrega features nuevas.
  - **Mayoría features** (>50%): Sprint productivo. Se están construyendo cosas nuevas.
  - **Balance ideal**: 40% bugs / 50% features / 10% improvements.
  - **Tendencia**: Si bugs dominan sprint a sprint, el producto tiene deuda de calidad creciente.

### Widget B.3 — Lead Time por Status (Bar Chart / Stacked)
- **Tipo**: Stacked Bar Chart
- **Source**: Sprint cerrado, completados
- **Group by**: Ticket
- **Stack by**: Tiempo en cada status (días)
- **📖 Interpretación**:
  - Muestra **cuánto tiempo pasó cada ticket en cada fase** del pipeline.
  - **Bottleneck detection**: La fase con la barra más gruesa es el cuello de botella.
    - `fortification` grueso = devs tardan mucho en codificar.
    - `code review` grueso = reviewers tardan en aprobar.
    - `qa testing` grueso = QA está sobrecargado.
  - **✅ Ideal**: Barras delgadas y uniformes = flujo continuo.
  - **Acción**: Atacar la fase más gruesa en la retro. Establecer time limits (ej: CR ≤ 2 días).

---

## Sección C: Calidad

### Widget C.1 — QA Approval Rate (Number Widget)
- **Tipo**: Single number (grande)
- **Value**: (Aprobados / (Aprobados + Rechazados)) × 100
- **📖 Interpretación**:
  - **¿Qué calidad de código llega a QA?**
  - **>85%** 🟢 = Devs entregan código limpio. Pocas iteraciones de re-work.
  - **70-85%** 🟡 = Aceptable pero mejorable. Algunos devs no testean localmente.
  - **<70%** 🔴 = Problema sistémico. Los devs no verifican antes de enviar. Necesita acción.
  - **Tendencia**: Debería mejorar sprint a sprint. Si baja, investigar qué cambió.

### Widget C.2 — Bugs Encontrados en QA (Number Widget)
- **Tipo**: Single number
- **Value**: Count de tickets rechazados o bugs nuevos creados durante el sprint
- **📖 Interpretación**:
  - **Bugs encontrados por QA durante testing** (no confundir con bugs del backlog).
  - **0** = ¿QA está siendo demasiado permisivo? ¿O el código es perfecto?
  - **1-3** 🟢 = Normal. QA encuentra issues y los reporta.
  - **>5** 🟡 = Muchos bugs. El código necesita más revisión pre-QA.
  - **Contexto**: Más bugs encontrados por QA = menos bugs en producción (es bueno encontrarlos).

### Widget C.3 — Regression Fixes Completion (Progress Bar)
- **Tipo**: Battery/Progress widget
- **Filter**: Tag = `qa-regression-v0.1.0`
- **Value**: % completados
- **📖 Interpretación**:
  - **¿Se resolvieron todos los bugs de regresión de la versión anterior?**
  - **100%** 🟢 = Deuda de regresión saldada. Release limpio.
  - **<100%** = Algunos fixes pasan a next. Documentar cuáles y por qué.
  - **Acción en retro**: Si <80%, discutir por qué no se priorizaron los fixes.

### Widget C.4 — Bugs por Módulo (Bar Chart)
- **Tipo**: Bar Chart
- **Filter**: Type = `Bug`, sprint cerrado
- **Group by**: Iond Subcategory
- **Sort**: Count (desc)
- **📖 Interpretación**:
  - **¿Qué módulos generaron más bugs?** Indica áreas problemáticas.
  - **Top 3 módulos**: Necesitan atención especial (más tests, refactoring, o code review estricto).
  - **Módulo sin bugs**: Está estable o no se tocó en este sprint.
  - **Tendencia**: Si un módulo baja de posición sprint a sprint = está mejorando.
  - **Acción**: Top módulo con bugs → candidato para sprint de estabilización dedicado.

---

## Sección D: Métricas del Equipo

### Widget D.1 — Blocked Time (Bar Chart)
- **Tipo**: Bar Chart
- **Source**: Sprint cerrado
- **Filter**: Tickets que estuvieron en `blocked` durante el sprint
- **Group by**: Ticket
- **Value**: Días en `blocked`
- **📖 Interpretación**:
  - **Tiempo perdido en bloqueos**. Cada día bloqueado = un día de trabajo perdido.
  - **Total = 0 días** 🟢 = Sprint sin interrupciones. Excelente.
  - **Total > 5 días** 🟡 = Bloqueos significativos. Investigar causas.
  - **Total > 10 días** 🔴 = Bloqueos crónicos. Necesita acción estructural.
  - **Acción**: Clasificar los bloqueos: ¿Dependencias externas? ¿Falta de info? ¿Decisiones pendientes?

### Widget D.2 — Sprint Capacity Utilization (Donut Chart)
- **Tipo**: Donut Chart
- **Segmentos**:
  - 🟢 Completados (done + ready to merge)
  - 🟡 En progreso (code review + qa)
  - 🔴 No iniciados (sprint intake)
  - ⬛ Bloqueados
- **📖 Interpretación**:
  - **¿Cuánto de la capacidad se utilizó efectivamente?**
  - **🟢 Completados > 70%** = Sprint productivo.
  - **🟡 En progreso > 20%** = Tickets que quedaron a medio camino. Work in progress excesivo.
  - **🔴 No iniciados > 10%** = Se comprometió más de lo que se podía hacer.
  - **Acción**: En el próximo sprint, comprometer menos tickets (reducir al % de completion de este sprint).

### Widget D.3 — Sprint Health Summary (Text Widget)
- **Tipo**: Text widget con resumen ejecutivo
- **Contenido generado manualmente o por el Catalyst**:
  ```
  ┌───────────────────────────────────────────┐
  │  SPRINT 4 — HEALTH SUMMARY               │
  │                                           │
  │  Completion Rate:     XX%                 │
  │  QA Approval Rate:    XX%                 │
  │  Regression Fixed:    X/Y (XX%)           │
  │  Bugs Found by QA:    X                   │
  │  Blocked Days:        X                   │
  │  Scope Change:        +X / -X tickets     │
  │                                           │
  │  Overall:  🟢 / 🟡 / 🔴                  │
  └───────────────────────────────────────────┘
  ```
- **📖 Interpretación**:
  - **Snapshot ejecutivo** para el sprint review. Un vistazo = salud del sprint.
  - **Overall**:
    - 🟢 Completion >80%, Approval >85%, Regression 100%, Blocked <3 días
    - 🟡 Completion 60-80%, Approval 70-85%, Regression >80%
    - 🔴 Completion <60%, Approval <70%, Regression <80%

---

## Preguntas para la Retro (basadas en los datos)

> Usar estos datos para guiar la retrospectiva del sprint:

| Métrica | Si el resultado es bueno | Si el resultado es malo |
|---------|--------------------------|------------------------|
| Completion Rate | "¿Qué hicimos bien para completar tanto?" | "¿Qué nos impidió completar más? ¿Estimamos mal?" |
| QA Approval Rate | "La calidad mejoró. ¿Qué prácticas mantener?" | "¿Por qué tantos rechazos? ¿Falta testing local?" |
| Blocked Days | "Sin bloqueos. Buen flujo de trabajo." | "¿Qué nos bloqueó? ¿Cómo prevenirlo?" |
| Scope Change | "Scope estable. Buena planificación." | "¿Por qué se agregaron tantos tickets? ¿Quién los aprobó?" |
| Lead Time CR | "CRs rápidos. Buen teamwork." | "¿Por qué tardan tanto los CRs? ¿Falta de reviewers?" |
| Bugs por Módulo | "Módulos estables." | "Módulo X tiene muchos bugs. ¿Necesita refactoring?" |
