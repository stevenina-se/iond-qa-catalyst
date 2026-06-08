# Discovery Runbook — Revisión de Prototipo

> **Cuándo seguir este runbook**: Cuando el QA Engineer dice "revisar prototipo de ticket <ID>",
> "realizar discovery del ticket <ID>", o se está en fase de Discovery.

> **REGLA FUNDAMENTAL DE DISCOVERY: QA no rechaza al Developer.**
> QA da feedback constructivo y trabaja con el Developer para llegar a un acuerdo.
> El objetivo es asegurar que la lógica de negocio se mantenga estable, NO bloquear.

---

## Cómo Usar Este Runbook

1. **Seguir los pasos EN ORDEN** — No saltarse pasos ni ejecutarlos en paralelo
2. **Cada GATE es bloqueante** — Si un gate falla, PARAR y resolver antes de avanzar
3. **Anunciar cada paso** — Antes de ejecutar un skill, usar el protocolo Announce → Confirm → Act (Regla #5 del SKILL.md)
4. **Registrar progreso** — Marcar cada □ como ✅ conforme se completa

---

## DISCOVERY RUNBOOK — Ticket <ID>

```
════════════════════════════════════════════════════════════════
PASO 1 — INICIALIZACIÓN Y CARGA DE CONTEXTO
════════════════════════════════════════════════════════════════
```

### Checklist

- □ Cargar `knowledge/L1-project/` completo:
  - `business-rules.md` — Reglas de negocio de Ionflow
  - `test-priorities.md` — Qué es crítico, alto, medio, bajo
  - `api-architecture.md` — Repos, endpoints, relaciones
  - `stack-overview.md` — Stack técnico

- □ Obtener contexto del ticket desde ClickUp MCP:
  - Usar `getTaskById` con el ID del ticket
  - Extraer: **descripción completa** del ticket
  - Extraer: **Acceptance Criteria** (si existen en la descripción)
  - Leer: **sección de Actividades/Comentarios** de todos los involucrados

- □ Identificar módulo(s) afectados por el ticket
  - ¿A qué módulo de `knowledge/L2-modules/` pertenece?
  - ¿Hay módulos secundarios impactados?

- □ Cargar `knowledge/L2-modules/<módulo>/module.md` del módulo principal

- □ Leer sección **"Impacto Cruzado"** del L2 → identificar módulos secundarios afectados
  - Si la sección no existe → documentar que falta y continuar con lo disponible

- □ Crear `knowledge/L3-tickets/<id>/` con template si no existe:
  - Copiar desde `knowledge/L3-tickets/_template.md`
  - Marcar como modo Discovery

### Gate 1

```
GATE 1: ¿Todos los checks están ✅?
  → SÍ: Continuar al Paso 2
  → NO: Resolver cada □ pendiente antes de avanzar
```

---

```
════════════════════════════════════════════════════════════════
PASO 2 — RECONCILIACIÓN DE AC CON CLICKUP
════════════════════════════════════════════════════════════════
```

> ⚠️ **Los AC de la descripción del ticket pueden estar DESACTUALIZADOS.**
> Las decisiones reales se toman en los comentarios/actividades.
> Este paso es CRÍTICO para evitar testear contra AC obsoletos.

### Checklist

- □ Leer los AC que existen en la **descripción del ticket**

- □ Leer **TODOS los comentarios** de la sección de actividades del ticket
  - Identificar comentarios de: PO, Developers, QA, Stakeholders
  - Buscar especialmente:
    - Decisiones que **modifican el alcance** original
    - Aclaraciones sobre **comportamiento esperado**
    - Nuevos requerimientos que surgieron **después** de la descripción
    - Cambios de rumbo ("finalmente decidimos que...", "actualizamos el approach a...")
    - Restricciones técnicas descubiertas durante desarrollo

- □ Identificar si hubo **divergencias** entre AC originales y comentarios

- □ Si hay divergencia entre AC y comentarios:
  - Documentar las divergencias encontradas en este formato:

    | AC Original | Decisión en Comentarios | AC Reconciliado | Fuente |
    |---|---|---|---|
    | AC-1: "El usuario puede crear..." | Comentario de PO: "Limitamos a admin solamente" | AC-1 ACTUALIZADO: "Solo admin puede crear..." | Comentario [fecha] por [autor] |
    | AC-2: (no existe) | Developer: "Agregamos validación de formato" | AC-3 NUEVO: "El sistema valida el formato del campo X" | Comentario [fecha] por [autor] |

  - Presentar tabla de reconciliación al QA Engineer para validación

- □ Consolidar los **AC finales** (descripción + comentarios reconciliados)
  - Cada AC debe incluir su fuente (descripción, comentario, acuerdo)

### Gate 2

```
GATE 2: ¿AC reconciliados con las últimas decisiones del equipo?
  → SÍ: Continuar al Paso 3
  → NO: Presentar divergencias al QA Engineer y esperar decisión
```

---

```
════════════════════════════════════════════════════════════════
PASO 3 — ANÁLISIS DE RIESGO (obligatorio)
════════════════════════════════════════════════════════════════
```

### Anuncio (Announce → Confirm → Act)

```
🔄 SIGUIENTE SKILL: test-docs/prioritize
   Razón: Necesito analizar los riesgos del ticket antes de construir la test matrix.
   Prerequisitos:
     ✅ L1-project/ cargado
     ✅ L2-modules/<módulo>/module.md cargado
     ✅ AC reconciliados del Paso 2
   Output esperado: L3-tickets/<id>/risk-triage.md

¿Procedo?
```

### Checklist

- □ Ejecutar skill: `test-docs/prioritize`
  - Usar los AC reconciliados del Paso 2 como entrada
  - Incluir contexto de los comentarios del ticket para enriquecer el análisis

- □ Verificar que existe: `L3-tickets/<id>/risk-triage.md`

- □ Presentar hallazgos y preguntas al QA Engineer:
  - Riesgos identificados por área
  - Preguntas para el Developer (formato abierto, NO objeciones)
  - Edge cases potenciales

- □ QA Engineer aprueba risk-triage

### Gate 3

```
GATE 3: ¿risk-triage.md existe y fue aprobado por el QA Engineer?
  → SÍ: Continuar al Paso 3.5
  → NO: Iterar con el QA Engineer hasta aprobación
```

---

```
════════════════════════════════════════════════════════════════
PASO 3.5 — CODE REVIEW DE PROTOTIPO (opcional)
════════════════════════════════════════════════════════════════
```

> **Este paso es OPCIONAL.** Preguntar al QA Engineer antes de ejecutar.
> En Discovery el prototipo puede ser solo un Figma, mockup o explicación verbal.
> Si existe una branch del ticket, este paso enriquece la discusión.

### Decisión del QA Engineer

Preguntar:

```
❓ ¿Hay una branch del ticket disponible para revisar el código del prototipo?
   ¿Deseas que haga una revisión de código para enriquecer el análisis?

   Opciones:
   A) Sí, revisar código del prototipo
   B) No, continuar sin code review
```

### Si el QA Engineer dice SÍ:

- □ Ejecutar skill: `code-review/review` (modo Discovery)
  - Enfoque: buscar "señales" para la discusión, NO bugs formales
  - Formular observaciones como PREGUNTAS
- □ Verificar que existe: `L3-tickets/<id>/code-review-qa.md`
- □ Enriquecer `risk-triage.md` con hallazgos del código

### Si el QA Engineer dice NO:

- □ Continuar al Paso 4

### Gate 3.5

```
GATE 3.5: ¿QA Engineer decidió?
  → SÍ (con review): code-review-qa.md existe → Continuar al Paso 4
  → SÍ (sin review): Continuar al Paso 4
  → NO: Esperar decisión del QA Engineer
```

---

```
════════════════════════════════════════════════════════════════
PASO 4 — CONSOLIDACIÓN DE AC (obligatorio)
════════════════════════════════════════════════════════════════
```

### Anuncio

```
🔄 SIGUIENTE SKILL: test-docs/document (modo AC)
   Razón: Necesito consolidar y validar los Acceptance Criteria.
   Prerequisitos:
     ✅ AC reconciliados del Paso 2
     ✅ risk-triage.md del Paso 3
     ✅ code-review-qa.md del Paso 3.5 (si aplica)
   Output esperado: L3-tickets/<id>/ac-consolidated.md

¿Procedo?
```

### Checklist

- □ Ejecutar skill: `test-docs/document` (modo AC)
  - Usar como entrada los **AC reconciliados** del Paso 2
  - Incorporar **riesgos** del Paso 3 (risk-triage.md)
  - Si hubo code review (Paso 3.5), incorporar **hallazgos del código**
  - Cada AC propuesto se presenta como SUGERENCIA, no como mandato

- □ Verificar que existe: `L3-tickets/<id>/ac-consolidated.md`

- □ QA Engineer aprueba los AC consolidados

### Gate 4

```
GATE 4: ¿ac-consolidated.md existe y fue aprobado?
  → SÍ: Continuar al Paso 5
  → NO: Iterar con el QA Engineer hasta aprobación
```

---

```
════════════════════════════════════════════════════════════════
PASO 5 — TEST MATRIX (obligatorio)
════════════════════════════════════════════════════════════════
```

### Anuncio

```
🔄 SIGUIENTE SKILL: test-docs/document (modo matrix)
   Razón: Necesito construir la Test Matrix completa basada en los AC consolidados.
   Prerequisitos:
     ✅ ac-consolidated.md del Paso 4
     ✅ risk-triage.md del Paso 3
     ✅ L2-modules/<módulo>/module.md cargado
   Output esperado: L3-tickets/<id>/test-matrix.md + test-matrix.csv

¿Procedo?
```

### Checklist

- □ Ejecutar skill: `test-docs/document` (modo matrix)
  - Basada en los AC consolidados + risk-triage + contexto L2
  - Incluir: happy path, edge cases, negativos y regresión
  - **Pasos en formato breadcrumb** (ver formato en document.md):
    `Company Login > Sidebar: Boards > Click [Flow] > ...`
  - Queries de BD basadas **exclusivamente en migraciones** del repo fuente

- □ Verificar que existe: `L3-tickets/<id>/test-matrix.md`

- □ Verificar que existe: `L3-tickets/<id>/test-matrix.csv`

- □ QA Engineer aprueba la matrix

### Gate 5

```
GATE 5: ¿test-matrix.md + .csv existen y fueron aprobados?
  → SÍ: Continuar al Paso 6
  → NO: Iterar con el QA Engineer hasta aprobación
```

---

```
════════════════════════════════════════════════════════════════
PASO 6 — PLAN DE TESTING (obligatorio)
════════════════════════════════════════════════════════════════
```

### Anuncio

```
🔄 SIGUIENTE SKILL: sprint-testing/plan
   Razón: Necesito crear el plan de testing para cuando el ticket pase a Deployment.
   Prerequisitos:
     ✅ test-matrix.md del Paso 5
     ✅ ac-consolidated.md del Paso 4
     ✅ risk-triage.md del Paso 3
   Output esperado: L3-tickets/<id>/test-plan.md

¿Procedo?
```

### Checklist

- □ Ejecutar skill: `sprint-testing/plan`

- □ Verificar que existe: `L3-tickets/<id>/test-plan.md`

- □ QA Engineer aprueba el plan

### Gate 6

```
GATE 6: ¿test-plan.md existe y fue aprobado?
  → SÍ: Discovery COMPLETO
  → NO: Iterar con el QA Engineer hasta aprobación
```

---

```
════════════════════════════════════════════════════════════════
✅ DISCOVERY COMPLETO
════════════════════════════════════════════════════════════════
```

### Artefactos Generados

Verificar que todos existen en `L3-tickets/<id>/`:

| Artefacto | Estado | Obligatorio |
|-----------|--------|-------------|
| `risk-triage.md` | ✅ | Sí |
| `ac-consolidated.md` | ✅ | Sí |
| `test-matrix.md` | ✅ | Sí |
| `test-matrix.csv` | ✅ | Sí |
| `test-plan.md` | ✅ | Sí |
| `code-review-qa.md` | ⬜/✅ | Solo si el QA lo pidió |

### Siguiente Fase

El ticket está listo para pasar a **Deployment**.
Cuando el QA Engineer indique "testear ticket <ID>", seguir:

**→ `skills/deployment-runbook.md`**

---

## Reglas de Discovery (Recordatorio)

| Regla | Descripción |
|---|---|
| **No rechazar** | QA NUNCA rechaza un prototipo. Da feedback y busca acuerdo |
| **Visión QA** | El foco es asegurar que la lógica de negocio se mantenga estable |
| **Preguntas > Objeciones** | Formular preguntas abiertas, no objeciones cerradas |
| **Acuerdo documentado** | Todo acuerdo con el Developer queda en el L3 del ticket |
| **Gate de calidad** | QA no aprueba para Deployment sin Test Matrix completa y AC verificables |
| **Retroalimentación** | Si el prototipo cambió después del acuerdo → repetir análisis |
| **ClickUp es la verdad** | Los comentarios/actividades del ticket reflejan las decisiones reales |
