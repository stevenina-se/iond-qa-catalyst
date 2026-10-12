# Acceptance Criteria Consolidados — 86e3936eq

> FlowPilot: evaluar migración del arnés custom a un runtime open source

---

## AC Originales (del ticket — Gherkin en descripción)

### AC-1: Decidir entre Go embebido y servicio desacoplado

```gherkin
Given existen prototipos equivalentes para las topologías seleccionadas
When se comparan con los mismos prompts, tools y fallos inducidos
Then el ADR documenta latencia, aislamiento, operación, actualización y costo de mantenimiento
And recomienda una opción principal y un fallback verificable
```

| Criterio | Evaluación |
|----------|-----------|
| ¿Es verificable? | ✅ Sí — se puede validar que el ADR contenga las métricas y la recomendación |
| ¿Es completo? | ⚠️ Parcialmente — no especifica qué métricas son aceptables ni umbrales |
| ¿Es ambiguo? | ⚠️ "prototipos equivalentes" no define qué funcionalidades deben cubrir |
| Fuente | Descripción original del ticket |
| Observación | El comentario de Enrique (2026-09-22) ya resolvió este AC: **Eino v0.9.19 embebido en Go** con **Mastra como fallback**. La decisión se basó en 3 gates descalificatorios (OpenRouter, approval persistente, licencia). 10 candidatos evaluados. |

---

### AC-2: Cerrar el ciclo de ajuste de una integración

```gherkin
Given el agente modificó un flow para una company autorizada
When el usuario aprueba una ejecución de prueba
Then el agente recibe el resultado general y el detalle de los nodos ejecutados
And puede diagnosticar el problema y proponer una corrección sin exponer secretos
```

| Criterio | Evaluación |
|----------|-----------|
| ¿Es verificable? | ✅ Sí — se puede demostrar el ciclo leer→modificar→aprobar→ejecutar→diagnosticar |
| ¿Es completo? | ⚠️ No menciona el approval gate duradero (que sobreviva restart) |
| ¿Es ambiguo? | ⚠️ "sin exponer secretos" no define qué constituye un secreto (headers, tokens, API keys, datos de tenant) |
| Fuente | Descripción original del ticket |
| Observación | Depende de: (1) approval gate duradero (sub-ticket 3), (2) tool `run_preview` (sub-ticket 7, NO existe aún), (3) redaction de credentials (sub-ticket 1). El Developer nota que el approval gate hay que construirlo igual sin importar el framework. |

---

### AC-3: Consumir IOND desde otro agente

```gherkin
Given existe una tool MCP de prueba protegida por los permisos de IOND
When un cliente MCP autorizado la invoca desde Codex, Claude Code u otra interfaz externa
Then obtiene capacidades y reglas de autorización consistentes con las que utiliza FlowPilot
And el harness interno no forma parte obligatoria de la solicitud
```

| Criterio | Evaluación |
|----------|-----------|
| ¿Es verificable? | ✅ Sí — se puede validar con una tool de prueba invocada desde cliente MCP externo |
| ¿Es completo? | ✅ Sí — cubre el desacoplamiento harness/MCP explícitamente |
| ¿Es ambiguo? | 🟡 Ligeramente — "capacidades y reglas de autorización consistentes" no define cuáles |
| Fuente | Descripción original del ticket |
| Observación | Depende de IONF-1277 (MCP público). Este AC valida que el MCP no vive dentro del harness y que el servidor consume `/api/2.0/workspace/`. |

---

### AC-4: Preparar la evolución multiagente

```gherkin
Given el primer prototipo utiliza un solo agente
When se revisa el diseño de sesiones, tools y eventos
Then es posible agregar Planificador, FlowPilot, CodePilot y QA sin modificar los contratos públicos de IOND
And cada rol puede recibir un conjunto mínimo y diferente de permisos
```

| Criterio | Evaluación |
|----------|-----------|
| ¿Es verificable? | ⚠️ Parcialmente — "es posible agregar" es difícil de verificar sin implementar |
| ¿Es completo? | ⚠️ No menciona: lease de escritor por flow, presupuesto AI credits unificado, composición agent-as-a-tool |
| ¿Es ambiguo? | ⚠️ "sin modificar los contratos públicos" necesita definir qué contratos (SSE events, tool schemas, API endpoints) |
| Fuente | Descripción original del ticket |
| Observación | El Developer propone implementar los 4 agentes en el sub-ticket 7, DESPUÉS de estabilizar harness y ciclo de ejecución. Este AC es de diseño/preparación, no implementación. |

---

## AC Propuestos (sugerencias para acordar con el equipo)

> Basados en el risk-triage y los hallazgos de seguridad documentados por el Developer.

### AC-5 (PROPUESTO): Seguridad — Path traversal corregido

```gherkin
Given el agente genera un flow_id como parte de su operación
When el flow_id contiene caracteres de path traversal (../, ..\, etc.)
Then IOND rechaza la operación y no accede a directorios fuera del workspace del tenant
And se registra un evento de seguridad en los logs
```

| Justificación | Basado en vulnerabilidad documentada por Developer (comentario 2026-09-22): "current_execution acepta un flow_id generado por el modelo y lo usa como nombre de fichero. Un ../ sale del directorio y se puede abrir la base de datos de otro tenant" |
|---|---|
| Fuente | Comentario de Enrique Vicente (2026-09-22), risk-triage R-001 |

---

### AC-6 (PROPUESTO): Seguridad — Permisos correctos del endpoint de chat

```gherkin
Given un usuario tiene permiso ReadBoard pero NO UpdateBoard
When el usuario interactúa con FlowPilot vía chat
Then FlowPilot NO puede crear, actualizar ni borrar elementos del board en nombre de ese usuario
And el sistema retorna un error de permisos adecuado
```

| Justificación | Basado en vulnerabilidad documentada por Developer: "el chat está gateado en ReadBoard, pero el agente detrás crea, actualiza y borra elementos" |
|---|---|
| Fuente | Comentario de Enrique Vicente (2026-09-22), risk-triage R-002 |

---

### AC-7 (PROPUESTO): Seguridad — Redaction de credentials

```gherkin
Given un flow ejecutado contiene payloads con headers de autorización, tokens o datos sensibles
When el agente recibe los resultados de ejecución o se almacena el transcript
Then los datos sensibles están redactados (no solo truncados)
And la redaction se aplica antes de enviar al modelo Y antes de persistir en tracing
```

| Justificación | Basado en vulnerabilidad documentada por Developer: "los payloads de ejecución llegan al modelo con sus headers Authorization intactos y se guardan así en el transcript" |
|---|---|
| Fuente | Comentario de Enrique Vicente (2026-09-22), risk-triage R-003 |

---

### AC-8 (PROPUESTO): Tracking de costos — AI credits no se pierden

```gherkin
Given Eino no reporta coste en TokenUsage y OpenRouter descarta ese campo
When el agente completa una sesión
Then el consumo de AI credits se contabiliza correctamente (sniffeado del stream u otro mecanismo)
And los credits son visibles para el tenant
```

| Justificación | El Developer lo identificó como "check bloqueante del punto 4". Si falla, se dejaría de facturar en silencio |
|---|---|
| Fuente | Comentario de Enrique Vicente (2026-09-22), risk-triage R-005 |

---

### AC-9 (PROPUESTO): Cutover — Rollback funcional

```gherkin
Given el sistema está ejecutando con FLOWPILOT_ENGINE=eino
When se cambia a FLOWPILOT_ENGINE=legacy y se reinicia
Then las sesiones nuevas usan el engine legacy
And las sesiones previas de eino que no estaban activas no causan errores
```

| Justificación | La estrategia de rollback (env var + restart) es clave para la confianza del deploy. Debe ser verificable |
|---|---|
| Fuente | Comentario de Enrique Vicente (2026-09-22) — sub-ticket 6, risk-triage R-006 |

---

## AC Diferidos (para sub-tickets posteriores)

| AC | Razón del diferimiento |
|---|---|
| Implementación completa de `run_preview` | Es un sub-ticket separado (7). El Discovery valida que el diseño lo permite |
| Implementación de 4 agentes (Planner, FlowPilot, CodePilot, QA) | Explícitamente fuera de scope — solo se valida el diseño preparatorio |
| Sesiones fuera de disco local | IONF-1355, fuera de scope de este ticket |

---

## Transformación AC → Casos de Test

| AC | Caso de test (happy path) | Casos edge | Caso negativo |
|----|--------------------------|------------|---------------|
| AC-1 | ADR documenta comparación de candidatos con métricas de latencia, aislamiento, operación, actualización y costo | ADR documenta fallback (Mastra) con pros/cons | ADR sin métricas reproducibles → incompleto |
| AC-2 | Agente modifica flow → usuario aprueba → ejecuta → recibe resultados → diagnostica | Aprobación sobrevive a restart del proceso | Agente intenta ejecutar sin aprobación → bloqueado |
| AC-3 | Cliente MCP externo invoca tool con permisos de tenant → respuesta consistente con FlowPilot | Cliente MCP sin permisos → error de autorización | El harness interno es requerido por la solicitud → violación de desacoplamiento |
| AC-4 | Diseño de sesiones/tools/eventos permite agregar roles sin cambiar contratos | Un rol tiene permisos diferentes a otro | Agregar un rol requiere modificar contratos públicos → diseño incorrecto |
| AC-5 | `flow_id` normal opera correctamente | `flow_id` con caracteres especiales (espacios, unicode) | `flow_id` con `../` → rechazado |
| AC-6 | Usuario con UpdateBoard puede operar FlowPilot completo | Usuario con permisos parciales (ej. solo ReadBoard + CreateBoard) | Usuario ReadBoard only → no puede modificar via chat |
| AC-7 | Resultados de ejecución llegan al modelo sin headers sensibles | Payloads con múltiples tipos de secrets (OAuth, API keys, Bearer tokens) | Transcript persiste con Authorization headers → falla de redaction |
| AC-8 | AI credits se facturan correctamente después de una sesión | Sesión con múltiples turns y múltiples tool calls | Costos no reportados → facturación en silencio a 0 |
| AC-9 | Switch de eino a legacy funciona limpiamente | Restart durante sesión activa + switch de engine | Sesiones corruptas después del rollback |

---

## Resumen

| Categoría | Cantidad |
|---|---|
| AC Originales | 4 (de la descripción del ticket) |
| AC Propuestos | 5 (AC-5 a AC-9, basados en risk-triage y comentarios del Developer) |
| AC Diferidos | 3 (para sub-tickets posteriores) |
| Divergencias descripción vs comentarios | **0** — el comentario enriquece sin contradecir |
| Total AC para Test Matrix | **9** |

---

*Generado por: QA Catalyst (test-docs/document modo AC) — 2026-10-01*
*Fuentes: ClickUp 86e3936eq, risk-triage.md, L1-project/, L2-modules/boards/, L2-modules/nodes/*
