# Skill: test-docs/prioritize

> Analiza el riesgo de un ticket/prototipo y genera una lista priorizada de qué testear, incluyendo preguntas para el Developer.

## Cuándo usar este skill

- **Discovery Track**: Al revisar un prototipo del Developer (Paso 5 del Altacrest)
- **Deployment Track**: Al inicio del testing de un ticket para ajustar prioridades
- **Support Lane**: Al analizar un hotfix para decidir scope de testing

## Pre-requisitos

Antes de ejecutar este skill, el agente DEBE haber cargado:
- ✅ `knowledge/L1-project/business-rules.md` — Reglas de negocio
- ✅ `knowledge/L1-project/test-priorities.md` — Prioridades de testing
- ✅ `knowledge/L2-modules/<módulo>/module.md` — Contexto del módulo afectado
- ✅ Acceptance Criteria del ticket (desde ClickUp o manual), puede no tenerlo aun ya que en esta fase de discovery construiremos el Acceptance Criteria

---

## Instrucciones de Ejecución

### Stage 1 — PLANNING

Reporta al QA Engineer:
1. Qué módulo(s) vas a analizar
2. Qué fuentes de contexto vas a leer (L1, L2)
3. El AC que vas a analizar

**Espera aprobación antes de continuar.**

### Stage 2 — EXECUTION

#### Paso 0: Obtener Contexto de ClickUp (OBLIGATORIO)

> ⚠️ Las discusiones en los comentarios del ticket frecuentemente cambian el alcance.
> Este paso enriquece el análisis de riesgo con el contexto real del equipo.

1. Obtener el ticket completo via ClickUp MCP (`getTaskById`)
2. Leer la **descripción** del ticket — extraer AC si existen
3. Leer **TODOS los comentarios** de la sección de actividades:
   - Buscar decisiones que modifican el alcance
   - Buscar aclaraciones sobre comportamiento esperado
   - Buscar restricciones técnicas descubiertas por el Developer
   - Buscar cambios de rumbo posteriores a la descripción
4. Si hay divergencias entre descripción y comentarios → **documentar** y tener en cuenta en el análisis de riesgo
5. Si el ticket tiene AC desactualizados → **notar** en el risk-triage

> Este contexto complementa el L1 y L2. Las decisiones del equipo en ClickUp
> son la fuente de verdad para el alcance actual del ticket.

#### Paso 1: Análisis de Lógica de Negocio

Lee `L1-project/business-rules.md` y responde estas preguntas sobre el ticket:

| Pregunta | Tu análisis |
|----------|-------------|
| ¿El feature respeta las reglas multi-tenant (company)? | |
| ¿Afecta la ejecución de flows/nodos? | |
| ¿Hay impacto en connectors globales vs company? | |
| ¿Se tocan datos de ejecución (SQLite) o datos persistentes (PostgreSQL)? | |
| ¿Hay impacto en el sistema de permisos por usuario/company? | |
| ¿El feature puede romper flujos de e-commerce existentes? | |

#### Paso 2: Análisis de Impacto por Módulo

Lee `L2-modules/<módulo>/module.md` y analiza:

| Área | Impacto | Riesgo |
|------|---------|--------|
| Frontend (rutas, vistas, componentes) | ¿Qué cambia? | 🔴/🟠/🟡/🟢 |
| API (endpoints, payloads) | ¿Qué cambia? | 🔴/🟠/🟡/🟢 |
| Canvas (nodos, edges, drawer) | ¿Qué cambia? | 🔴/🟠/🟡/🟢 |
| BD PostgreSQL (tablas, relaciones) | ¿Qué cambia? | 🔴/🟠/🟡/🟢 |
| BD SQLite (ejecuciones) | ¿Qué cambia? | 🔴/🟠/🟡/🟢 |
| Otros módulos afectados | ¿Cuáles? | 🔴/🟠/🟡/🟢 |

#### Paso 3: Identificación de Edge Cases

Genera una lista de casos borde basados en:
- Reglas de negocio que podrían violarse
- Datos vacíos, nulos o malformados
- Escenarios multi-company / multi-usuario
- Comportamiento cuando un nodo/flow falla
- Connectors globales vs company
- Límites de datos (listas largas, payloads grandes)

#### Paso 2.5 (OPCIONAL): Revisión de Código del Prototipo

> ⚠️ **Este paso NO es obligatorio.** En Discovery el prototipo puede ser solo un Figma, mockup o explicación verbal.
> Si existe una branch del ticket, este paso ayuda a enriquecer la discusión pero **NO es bloqueante**.
> 
> Si el QA Engineer acepta hacer code review, considerar delegar a `code-review/review.md` (modo Discovery)
> para una revisión más estructurada.

**Solo si la branch del ticket está disponible**, leer el diff para detectar posibilidades de discusión:

```bash
# Ejemplo: ver qué archivos cambió el Developer
git diff DEVELOPMENT...<ticket-branch> --stat
```

Buscar señales para discutir (NO para rechazar):

| Señal en el código | Pregunta para discusión |
|---|---|
| Nuevo endpoint sin validación de `company_id` | "¿Este endpoint filtrará por company?" |
| Migración que agrega columna sin default | "¿Qué pasará con los registros existentes?" |
| Componente sin manejo de estado vacío | "¿Cómo se verá cuando no haya datos?" |
| Llamada API sin manejo de error | "¿Qué mostrará al usuario si la API falla?" |

> **Regla**: Las observaciones del código son **insumos para la conversación**, nunca objeciones formales.

#### Paso 4: Preguntas para el Developer

> **Regla de Discovery: No rechazar — preguntar.**
> Cada pregunta debe ser abierta y constructiva, no una objeción.

Genera preguntas en este formato:

```
PREGUNTAS PARA EL DEVELOPER — Ticket [ID]

[LÓGICA DE NEGOCIO]
1. ¿Cómo se comporta esta feature cuando un usuario de otra company intenta acceder?
2. ¿Qué sucede si el flow se ejecuta con un connector de tipo company que fue eliminado?
...

[EDGE CASES]
3. ¿Qué pasa si el usuario envía un payload vacío en este endpoint?
4. ¿Qué sucede si hay 1000+ registros en esta tabla?
...

[INTEGRACIÓN]
5. ¿Este cambio afecta el comportamiento de [otro módulo]?
6. ¿Se requiere actualización de la documentación de API?
...
```

#### Paso 5: Risk Triage

Genera la tabla de priorización:

| ID | Área | Riesgo | Descripción | Prioridad de testing | Justificación |
|----|------|--------|-------------|---------------------|---------------|
| R-001 | ... | 🔴 Crítico | ... | 1 (testear primero) | ... |
| R-002 | ... | 🟠 Alto | ... | 2 | ... |
| R-003 | ... | 🟡 Medio | ... | 3 | ... |

### Stage 3 — REPORTING

Genera el output final en este formato y guárdalo en `L3-tickets/<ticket-id>/risk-triage.md`:

```markdown
# Risk Triage — [TICKET-ID]

## Resumen
- Módulo principal: [nombre]
- Módulos impactados: [lista]
- Riesgo general: 🔴/🟠/🟡/🟢
- Total edge cases identificados: [N]
- Total preguntas para Developer: [N]
- Contexto de ClickUp: [N] comentarios leídos, [divergencias encontradas / sin divergencias]

## Tabla de Riesgos
[tabla del Paso 5]

## Edge Cases Identificados
[lista del Paso 3]

## Preguntas para el Developer
[formato del Paso 4]

## Contexto del Ticket (ClickUp)
- Divergencias detectadas entre descripción y comentarios: [lista si aplica]
- Últimas decisiones relevantes: [resumen de decisiones clave de los comentarios]

## Recomendación
[Describir qué áreas requieren más atención y por qué]
```

---

## Reglas de este Skill

1. **Paso 0 es OBLIGATORIO** — Siempre leer comentarios de ClickUp antes de analizar riesgos
2. **En Discovery**: El output principal son las preguntas para el Developer y los edge cases
3. **En Deployment**: El output principal es la tabla de riesgos para priorizar el testing
4. **Nunca inventar riesgos** — Solo reportar lo que se puede justificar con el contexto
5. **Siempre consultar el L1** — Las reglas de negocio son la base de todo el análisis
6. **Si no hay L2 del módulo** — Reportar al QA Engineer que se necesita construir antes
7. **Los comentarios de ClickUp son fuente de verdad** — Las decisiones del equipo prevalecen sobre la descripción original
