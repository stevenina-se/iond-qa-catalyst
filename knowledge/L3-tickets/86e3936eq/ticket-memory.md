# Ticket: 86e3936eq — [P1][Discovery] FlowPilot: evaluar migración del arnés custom a un runtime open source

> Sesión de Discovery iniciada: 2026-10-01
> Módulo: Boards / FlowPilot (Flowpilot subcategory)
> QA Engineer: Steve Nina
> Track: Discovery

## Contexto del Ticket

### Información General
| Campo | Valor |
|-------|-------|
| ID | 86e3936eq |
| Status | test matrix |
| Tipo | Refactor |
| Prioridad | High |
| Subcategoría | Flowpilot |
| Assignee | Enrique Vicente |
| Creator | Marcel Herrera Rendón |
| Tags | iond-core |
| Watchers | Steve Nina, Marcel Herrera Rendón, Enrique Vicente |
| URL | https://app.clickup.com/t/86e3936eq |

### Descripción
Evaluar y prototipar la sustitución del loop de agente construido a medida detrás de FlowPilot por un harness open source mantenido (Eino v0.9.19 de ByteDance/CloudWeGo). El discovery compara candidatos y topologías de integración: embebido en Go dentro de IOND, sidecar o microservicio desacoplado.

**FlowPilot seguirá siendo una experiencia nativa de IOND y utilizará nuestro frontend.** La migración cambia el motor interno que ejecuta sus sesiones, no la identidad del producto ni su interfaz.

### Acceptance Criteria (de la descripción)

- [ ] AC-1: **Decidir entre Go embebido y servicio desacoplado** — ADR documenta latencia, aislamiento, operación, actualización y costo. Recomienda opción principal + fallback.
- [ ] AC-2: **Cerrar el ciclo de ajuste de una integración** — El agente modifica un flow, usuario aprueba ejecución de prueba, agente recibe resultados y diagnostica sin exponer secretos.
- [ ] AC-3: **Consumir IOND desde otro agente** — Cliente MCP autorizado invoca tool de prueba desde interfaz externa con mismas capacidades y autorización que FlowPilot.
- [ ] AC-4: **Preparar la evolución multiagente** — Diseño permite agregar Planificador, FlowPilot, CodePilot y QA sin modificar contratos públicos.

### Definition of Done
1. Baseline y fronteras de responsabilidad aprobados
2. Comparación reproducible de candidatos y topologías completada
3. Prototipo mínimo ejecuta ciclo lectura→modificación→aprobación→ejecución→diagnóstico
4. Compatibilidad futura con MCP público validada
5. Frontend de FlowPilot conservado independiente del harness
6. Riesgos de ports Go y microservicio documentados
7. ADR aprobado por Tech Lead y Producto
8. Recomendación go/no-go y fallback documentados
9. Tickets de delivery para migración y multiagente propuestos

### Decisiones del equipo (de comentarios ClickUp)

**Decisión principal (Enrique, 2026-09-22):**
- **Eino v0.9.19** seleccionado como harness (Apache-2.0, ByteDance/CloudWeGo)
- Topología: **Go embebido en `ion_flow_binaries`**
- Fallback: **Mastra** (TS, sidecar) — único candidato con approval routes nativas
- 3 gates descalificatorios: OpenRouter (G1), approval persistente a restart (G2), licencia permisiva (G3)
- 10 candidatos evaluados y descartados con razones documentadas

**Hallazgos de seguridad críticos:**
1. **Path traversal** en `current_execution` — `flow_id` generado por el modelo usado como nombre de fichero, `../` sale del directorio de otro tenant
2. **Permiso equivocado** — chat gateado en `ReadBoard`, pero agente crea/actualiza/borra. Un read-only puede reescribir un board
3. **Cero redaction** — payloads con headers `Authorization` intactos al modelo y al tracing

**7 sub-tickets propuestos:**
1. Arreglar seguridad del loop actual (path traversal, permisos, redaction)
2. Crear interfaces: `ToolProvider`, `SessionStore`, `EventSink`, `Engine`
3. Approval gate duradero (cierra IONF-860)
4. Diseño arquitectura Eino — go/no-go
5. Implementar `einoengine`
6. Paridad de eventos y cutover (`FLOWPILOT_ENGINE=legacy|eino`)
7. Nueva tool `run_preview` + agentes Planner/FlowPilot/CodePilot/QA

**Fuera de scope:** IONF-1355 (sacar sesiones del disco local)

### Módulo afectado
- Módulo principal: `boards` (FlowPilot es parte del motor de boards)
- Módulos relacionados: `nodes` (Agent, Code), `auth` (permisos TPerm), `executions` (sesiones)

### Dependencias
- IONF-1085: API Workspace
- IONF-1277: MCP público de IOND
- IONF-859: Lectura y diagnóstico de ejecuciones (cerrado)
- IONF-860: Ejecución de preview con confirmación (pendiente)
- IONF-821: Skills globales y por usuario
- IONF-1355: Observabilidad de servidores y flujos

---

## Artefactos

| Artefacto | Estado | Obligatorio |
|-----------|--------|-------------|
| `risk-triage.md` | ⏳ En progreso | Sí |
| `ac-consolidated.md` | ⬜ Pendiente | Sí |
| `test-matrix.md` | ⬜ Pendiente | Sí |
| `test-matrix.csv` | ⬜ Pendiente | Sí |
| `test-plan.md` | ⬜ Pendiente | Sí |
| `code-review-qa.md` | ⬜ Pendiente | Opcional |

---

## Transcript de la Sesión

| Timestamp | Acción | Detalle |
|-----------|--------|---------|
| 2026-10-01 11:40 | Session Start | Cargado L1 completo + L2 boards + L2 nodes |
| 2026-10-01 11:40 | ClickUp Read | Ticket + 1 comentario extenso del Developer (ADR + sub-tickets) |
| 2026-10-01 11:41 | Gate 1 | ✅ Contexto completo cargado, L3 creado |
| 2026-10-01 11:41 | Paso 2 | Reconciliación de AC — ver análisis en risk-triage |
| 2026-10-01 11:42 | Paso 3 | Ejecutando test-docs/prioritize |
