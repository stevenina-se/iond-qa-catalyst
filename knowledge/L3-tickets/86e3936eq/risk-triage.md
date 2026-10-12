# Risk Triage — 86e3936eq

> FlowPilot: evaluar migración del arnés custom a un runtime open source

## Resumen

- **Módulo principal**: Boards / FlowPilot
- **Módulos impactados**: Boards, Nodes (Agent, Code), Auth (permisos TPerm), Executions (sesiones/transcripts), Keys (credenciales LLM)
- **Riesgo general**: 🔴 Crítico
- **Total riesgos identificados**: 14
- **Total edge cases identificados**: 12
- **Total preguntas para Developer**: 15
- **Contexto de ClickUp**: 1 comentario extenso leído (ADR completo), sin divergencias entre descripción y comentario — el comentario **enriquece y concreta** la descripción con decisión técnica + sub-tickets

---

## Análisis de Lógica de Negocio (L1)

| Pregunta | Análisis |
|----------|----------|
| ¿El feature respeta las reglas multi-tenant (company)? | 🔴 **NO actualmente** — El Developer documentó que `current_execution` acepta un `flow_id` generado por el modelo y lo usa como nombre de fichero. Un `../` sale del directorio y puede abrir la BD de otro tenant (path traversal). Además, la tool policy debe respetar `TPerm ∩ rol ∩ decisión` por company. |
| ¿Afecta la ejecución de flows/nodos? | 🔴 **SÍ directamente** — FlowPilot crea, modifica y ejecuta flows. La migración cambia el engine que orquesta estas operaciones. La nueva tool `run_preview` ejecutará flows con confirmación. El ciclo completo (leer→modificar→aprobar→ejecutar→diagnosticar) pasa por el motor de ejecución. |
| ¿Hay impacto en connectors globales vs company? | 🟡 **Indirecto** — FlowPilot opera sobre flows que contienen nodos de connectors. Las tools del agente no modifican connectors directamente, pero un flow creado por FlowPilot podría incluir nodos de connector company o global. |
| ¿Se tocan datos de ejecución (SQLite) o datos persistentes (PostgreSQL)? | 🔴 **SÍ** — Sesiones de FlowPilot se almacenan en disco (transcripts JSONL actualmente). Eino introduce `CheckPointStore` para persistencia de sesiones. Los resultados de `run_preview` leerán la SQLite de ejecuciones. Los payloads de ejecución (con headers Authorization) llegan al modelo sin redaction. |
| ¿Hay impacto en el sistema de permisos por usuario/company? | 🔴 **SÍ — VULNERABILIDAD EXISTENTE** — El chat está gateado en `ReadBoard`, pero el agente crea, actualiza y borra elementos. Un miembro read-only puede reescribir un board pidiendo por chat. La migración debe corregir esto con una policy table por tool. |
| ¿El feature puede romper flujos de e-commerce existentes? | 🟠 **Riesgo medio-alto** — Si el cutover (`FLOWPILOT_ENGINE=legacy|eino`) tiene bugs, FlowPilot podría dejar de funcionar o generar cambios incorrectos en flows de producción. El rollback es env var + restart, pero los dos engines quedan compilados. |

---

## Análisis de Impacto por Módulo (L2)

| Área | Impacto | Riesgo |
|------|---------|--------|
| **Backend — Agent Loop** (`flow_binaries`) | Reemplazo completo del loop ReAct custom por Eino. Nuevas interfaces: `ToolProvider`, `SessionStore`, `EventSink`, `Engine`. Package `einoengine` nuevo. 13 tool schemas deben sobrevivir round-trip. | 🔴 Crítico |
| **Backend — Seguridad** | Path traversal en `current_execution`, permiso `ReadBoard` insuficiente, cero redaction de credentials. Los 3 primeros sub-tickets son de seguridad sobre el loop actual. | 🔴 Crítico |
| **Backend — Approval Gate** | Nuevo sistema de approval duradero: turno parked en row, stream cierra, sobrevive reload/deploy. Botones Accept/Decline en UI hoy no tienen handler. Cierra IONF-860. | 🔴 Crítico |
| **Frontend — SSE Events** | Los eventos de Eino se traducen a nombres SSE actuales. Se preservan `board_lock`/`board_unlock`/`board_refresh`. Si la traducción falla, la UI de FlowPilot se rompe. | 🟠 Alto |
| **Frontend — Chat UI** | FlowPilot conserva su frontend. Los eventos de texto, tool, aprobación, estado y error no deben acoplarse a un harness específico. | 🟠 Alto |
| **API — Tool Provider** | Las 13 tools actuales + la nueva `run_preview` deben mantener schemas, nombres e IDs públicos consistentes entre Tool Provider, API Workspace y MCP. | 🟠 Alto |
| **BD — Sessions** | Checkpoint Store de Eino para persistir sesiones. Actualmente en disco local — NO se mueve a réplica (fuera de scope, IONF-1355). `TokenUsage` de Eino no trae coste y OpenRouter lo descarta → sniffear del stream. | 🟠 Alto |
| **Canvas (webcomponents-flow)** | Sin cambios directos al canvas. FlowPilot modifica flows via API, no via canvas. | 🟢 Bajo |
| **BD PostgreSQL** | Sin migraciones directas documentadas en este ticket. La policy table por tool podría requerir nueva tabla. | 🟡 Medio |
| **MCP Público** (IONF-1277) | Validación conceptual de que un cliente MCP autorizado puede operar IOND desde interfaz externa. MCP no vive dentro del harness. | 🟡 Medio |
| **Multiagente** | Diseño preparatorio para Planner, FlowPilot, CodePilot, QA. Lease de escritor por flow, presupuesto AI credits unificado. No implementado en este ticket. | 🟡 Medio |

---

## Tabla de Riesgos

| ID | Área | Riesgo | Descripción | Prioridad de testing | Justificación |
|----|------|--------|-------------|---------------------|---------------|
| R-001 | Seguridad | 🔴 Crítico | **Path traversal** en `current_execution`: `flow_id` generado por modelo usado como nombre de fichero. `../` accede a BD de otro tenant | 1 | Vulnerabilidad de aislamiento multi-tenant. Un modelo malicioso o un prompt injection podría acceder a datos de otros clientes |
| R-002 | Seguridad | 🔴 Crítico | **Permiso equivocado**: chat gateado en `ReadBoard` pero agente puede crear/actualizar/borrar. Un usuario read-only puede reescribir un board | 2 | Escalación de privilegios. Rompe el modelo de permisos de IOND |
| R-003 | Seguridad | 🔴 Crítico | **Cero redaction**: payloads de ejecución con headers `Authorization` intactos llegan al modelo y se guardan en transcript. Truncar ≠ redactar | 3 | Fuga de credenciales. Doble punto de redaction necesario: antes del modelo y antes del tracing |
| R-004 | Approval Gate | 🔴 Crítico | **Approval no sobrevive restart** en el loop actual. Eino ofrece `CheckPointID`+`CheckPointStore` pero hay que construir el gate igualmente | 4 | Sin approval duradero, IONF-860 no es implementable. El usuario pierde la confirmación si el proceso reinicia |
| R-005 | Costos | 🔴 Crítico | **`TokenUsage` de Eino no trae coste** y OpenRouter lo descarta. Si no se sniffea del stream, se deja de facturar AI credits en silencio | 5 | Impacto financiero directo. Los clientes no verían su consumo real |
| R-006 | Engine Migration | 🟠 Alto | **Cutover `FLOWPILOT_ENGINE=legacy\|eino`**: los dos engines quedan compilados. Si la paridad de eventos no es perfecta, la UI se rompe | 6 | Regresión en producción. El rollback es env var + restart, pero requiere validación exhaustiva de eventos SSE |
| R-007 | Tool Schemas | 🟠 Alto | **13 tool schemas deben sobrevivir round-trip** por Eino. Si algún schema se transforma o pierde campos, las tools fallan silenciosamente | 7 | Las tools son el hot path del agente. Un fallo aquí rompe toda la funcionalidad |
| R-008 | SSE Events | 🟠 Alto | **Traducción de eventos Eino → nombres SSE actuales**. Eventos: texto, tool, aprobación, estado, error, board_lock, board_unlock, board_refresh | 8 | El frontend depende de estos eventos para renderizar el chat y las acciones |
| R-009 | New Tool | 🟠 Alto | **`run_preview` no existe** — el ADR la da por existente. Ejecuta preview con confirmación, devuelve resultados por nodo redactados. Policy: always ask | 9 | Es la tool que justifica el approval gate. Sin ella, el ciclo de ajuste no cierra |
| R-010 | Concurrencia | 🟠 Alto | **Lease de escritor por flow**: dos agentes no deben escribir el mismo board. El board_lock actual puede no ser suficiente para multiagente | 10 | Corrupción de flows si dos agentes escriben simultáneamente |
| R-011 | MCP Boundary | 🟡 Medio | **MCP público independiente del harness**: el servidor de IONF-1277 consume `/api/2.0/workspace/` y no debe depender de Eino internamente | 11 | Acoplamiento arquitectónico. Si MCP depende de Eino, cambiar harness afecta la API pública |
| R-012 | Multiagente | 🟡 Medio | **Permisos diferenciados por rol**: Planner, FlowPilot, CodePilot, QA deben recibir conjuntos mínimos de tools. TPerm ∩ rol ∩ decisión | 12 | Diseño preparatorio. Un error de diseño aquí bloquearía la evolución futura |
| R-013 | Fallback | 🟡 Medio | **Mastra como fallback**: runtime Node en deploy, latencia en cada tool call, autorización fina detrás de licencia Enterprise, "breaking changes sin major version" | 13 | Si Eino falla el go/no-go, el plan B tiene costos operacionales significativos |
| R-014 | Sessions | 🟡 Medio | **Sesiones en disco local**: la aprobación sobrevive a restart y reload, pero no a caer en otra réplica (IONF-1355 fuera de scope) | 14 | Limitación conocida y aceptada, pero debe documentarse en DoD |

---

## Edge Cases Identificados

| # | Edge Case | Módulo | Riesgo | Origen |
|---|-----------|--------|--------|--------|
| EC-1 | Flow ID con caracteres `../` en el path → acceso a BD de otro tenant | Boards/Security | 🔴 | Comentario Developer |
| EC-2 | Usuario con permiso read-only envía prompt a FlowPilot que modifica el board | Auth/Boards | 🔴 | Comentario Developer |
| EC-3 | Payload de ejecución contiene header `Authorization` → llega al LLM y queda en transcript | Security | 🔴 | Comentario Developer |
| EC-4 | Proceso de IOND reinicia mientras hay un approval pendiente → ¿se pierde? | Approval Gate | 🔴 | AC-2 + Comentario |
| EC-5 | OpenRouter no devuelve coste en `TokenUsage` → AI credits no se facturan | Billing | 🔴 | Comentario Developer |
| EC-6 | Tool schema con campo complejo (nested objects) pierde estructura en round-trip por Eino | Tools | 🟠 | Análisis del ADR |
| EC-7 | Dos sesiones de FlowPilot simultáneas sobre el mismo flow → conflicto de escritura | Concurrency | 🟠 | Sub-ticket 7 |
| EC-8 | Evento SSE de Eino no tiene equivalente en el naming actual → frontend ignora el evento | Frontend | 🟠 | Sub-ticket 6 |
| EC-9 | `run_preview` ejecuta un flow con un nodo que hace llamadas HTTP externas → side effects en producción | Executions | 🟠 | Sub-ticket 7 |
| EC-10 | Switch de `FLOWPILOT_ENGINE=eino` a `legacy` después de que un checkpoint fue guardado en formato Eino → sesiones corruptas | Migration | 🟡 | Análisis rollback |
| EC-11 | Agente MCP externo (Codex, Claude Code) invoca tool sin tener permisos TPerm del tenant | MCP/Auth | 🟡 | AC-3 |
| EC-12 | FlowPilot genera código para Code node con dependencias que exceden el timeout de 300s del Code Runner | Nodes/Code | 🟡 | L2 Nodes |

---

## Preguntas para el Developer — Ticket 86e3936eq

### [SEGURIDAD — PRIORIDAD MÁXIMA]

1. **Path traversal**: ¿La corrección planificada para `current_execution` incluye sanitización del `flow_id` antes de usarlo como path, o se cambiará a un esquema de lookup por ID en BD?
2. **Permiso del endpoint**: ¿La corrección cambiará el gate a un permiso compuesto (`ReadBoard` + `UpdateBoard`) o se creará un nuevo permiso específico para FlowPilot (ej. `UseFlowPilot`)?
3. **Redaction**: ¿La redaction se implementará como middleware (antes de que el payload llegue al handler) o como transformación en el handler de cada tool? ¿Se aplicará tanto a headers como a body?
4. ¿Hay algún otro lugar donde datos sensibles podrían filtrarse al modelo aparte de los payloads de ejecución?

### [APPROVAL GATE]

5. ¿El turno "parked" en una row se almacenará en PostgreSQL o en la SQLite de sesiones? ¿Qué tabla/schema se usará?
6. Cuando el approval sobrevive a un reload pero NO a caer en otra réplica (limitación IONF-1355): ¿hay plan de comunicar esta limitación al usuario, o simplemente la sesión se pierde silenciosamente?
7. ¿Los botones Accept/Decline en la UI enviarán un request REST o se comunicarán via WebSocket?

### [EINO INTEGRATION]

8. ¿El check bloqueante de coste (`TokenUsage` sin coste + OpenRouter lo descarta) ya fue validado? ¿Se confirmó que se puede sniffear del stream de forma confiable?
9. ¿Los 13 tool schemas actuales se han testeado con el round-trip de Eino? ¿Hay algún tipo de dato (nested objects, arrays de objetos) que se pierda?
10. ¿El `CheckPointStore` de Eino se implementará sobre PostgreSQL, SQLite, o un almacenamiento propio?

### [CUTOVER Y ROLLBACK]

11. ¿El switch `FLOWPILOT_ENGINE=legacy|eino` afectará sesiones en curso, o solo sesiones nuevas?
12. Si un usuario tiene una sesión activa con el engine `eino` y se hace rollback a `legacy`: ¿qué pasa con los checkpoints de esa sesión?
13. ¿Los dos engines compilados afectan significativamente el tamaño del binario o los tiempos de compilación?

### [MULTIAGENTE — DISEÑO]

14. ¿El lease de escritor por flow es un lock exclusivo (solo un agente escribe a la vez) o permite lecturas concurrentes?
15. ¿El presupuesto unificado de AI credits por árbol de agentes se contabiliza en tiempo real o se reconcilia al final de la sesión? ¿Qué pasa si se excede el budget mid-session?

---

## Contexto del Ticket (ClickUp)

- **Divergencias detectadas entre descripción y comentarios**: **Ninguna** — el comentario del Developer (2026-09-22) enriquece y concreta la descripción original sin contradecirla. La descripción planteaba la evaluación de candidatos y topologías; el comentario entrega la decisión (Eino) con evidencia, descarta 10 alternativas con razones, y propone 7 sub-tickets concretos.
- **Últimas decisiones relevantes**:
  - Eino v0.9.19 es la opción seleccionada (3 gates pasados)
  - Mastra es el fallback (no un descarte)
  - Los 3 primeros sub-tickets van sobre el loop actual y NO dependen de Eino (si go/no-go falla, seguridad e IONF-860 quedan arreglados)
  - El approval gate hay que construirlo igual sin importar el framework
  - `run_preview` NO existe (el ADR la da por existente)
  - Fuera de scope: IONF-1355 (sesiones en disco local)

---

## Recomendación

### Áreas que requieren más atención (en orden):

1. **🔴 Seguridad (R-001, R-002, R-003)**: Son vulnerabilidades EXISTENTES en producción, no riesgos futuros. El path traversal y la escalación de privilegios son críticos. **Recomiendo que el test matrix incluya TCs explícitos para verificar que estos 3 sub-tickets se cierran ANTES de continuar con Eino.**

2. **🔴 Approval Gate duradero (R-004)**: Es el puente entre el discovery y la implementación. Sin approval gate, no hay `run_preview`, y sin `run_preview`, el AC-2 no se puede validar. **Es la dependencia más larga de la cadena.**

3. **🔴 Tracking de costos (R-005)**: Si Eino no reporta coste y el sniffing del stream falla, el impacto financiero es silencioso. **Debe ser un check bloqueante explícito en el go/no-go del sub-ticket 4.**

4. **🟠 Paridad de eventos SSE (R-006, R-008)**: La UI de FlowPilot depende de eventos con nombres específicos. La traducción de Eino a los nombres actuales debe ser verificable con tests antes del cutover. **El switch `FLOWPILOT_ENGINE` permite rollback, pero la validación debe ser exhaustiva.**

5. **🟠 Tool schemas round-trip (R-007)**: Las 13 tools + `run_preview` son el contrato entre IOND y el harness. Si un schema se corrompe en el round-trip, la funcionalidad falla silenciosamente. **Recomiendo tests unitarios que validen el round-trip de cada schema.**

### Naturaleza especial del ticket

Este ticket es un **Discovery de Refactor arquitectónico**, no un feature funcional típico. La test matrix deberá enfocarse en:
- **Validación del ADR**: ¿la evidencia justifica la decisión?
- **Completitud del análisis**: ¿se evaluaron todos los candidatos relevantes?
- **Viabilidad de la ruta de migración**: ¿los 7 sub-tickets cubren todo el scope?
- **Seguridad first**: ¿los 3 primeros sub-tickets son independientes de Eino?
- **Criterios de go/no-go**: ¿están claros y son verificables?

---

*Generado por: QA Catalyst (test-docs/prioritize) — 2026-10-01*
*Fuentes: ClickUp ticket 86e3936eq, L1-project/, L2-modules/boards/, L2-modules/nodes/*
