# Test Matrix — 86e3936eq

> FlowPilot: evaluar migración del arnés custom a un runtime open source
> Tipo de ticket: Discovery / Refactor arquitectónico
> Módulo principal: Boards / FlowPilot

---

## Resumen

- **Total de casos**: 32
- **Happy path**: 9
- **Edge cases**: 9
- **Negativos**: 7
- **Regresión**: 7
- **Automatizables**: 4 (la mayoría son validaciones de documento/diseño/prototipo)

> ⚠️ **Nota**: Este ticket es un Discovery de refactor arquitectónico. La mayoría de los TCs validan entregables (ADR, diseños, prototipos) y no interacción UI. Los TCs de seguridad (AC-5/6/7) se validarán funcionalmente cuando los sub-tickets de corrección se implementen.

---

## Test Matrix

### AC-1: Decidir entre Go embebido y servicio desacoplado

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-001 | Boards/FlowPilot | AC-1 | Happy Path | ADR documenta comparación completa de candidatos con métricas | ADR entregado por Developer | `Review ADR > Sección: Comparación > Verify: métricas de latencia, aislamiento, operación, actualización, costo para cada topología evaluada` | ADR contiene tabla comparativa con métricas cuantitativas para al menos Go embebido y sidecar/microservicio | 🔴 | ❌ | ⬜ |
| TC-002 | Boards/FlowPilot | AC-1 | Happy Path | ADR recomienda opción principal + fallback verificable | ADR entregado | `Review ADR > Sección: Recomendación > Verify: opción principal (Eino) y fallback (Mastra) con justificación` | ADR contiene recomendación explícita con go/no-go, opción principal, fallback y riesgos de cada una | 🔴 | ❌ | ⬜ |
| TC-003 | Boards/FlowPilot | AC-1 | Edge Case | Candidatos descartados tienen razones documentadas por gate | ADR entregado | `Review ADR > Sección: Descartados > Verify: cada candidato tiene al menos un gate fallido (G1/G2/G3) documentado` | Los 10 candidatos descartados tienen razones trazables a los 3 gates descalificatorios | 🟠 | ❌ | ⬜ |
| TC-004 | Boards/FlowPilot | AC-1 | Negativo | ADR sin métricas reproducibles es incompleto | ADR entregado | `Review ADR > Verify: las comparaciones NO son opiniones subjetivas > Verify: hay datos de pruebas reproducibles (prompts iguales, tools iguales, fallos inducidos)` | Si las comparaciones son solo opiniones sin datos → ADR marcado como incompleto | 🟠 | ❌ | ⬜ |

---

### AC-2: Cerrar el ciclo de ajuste de una integración

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-005 | Boards/FlowPilot | AC-2 | Happy Path | Prototipo demuestra ciclo completo: leer→modificar→aprobar→ejecutar→diagnosticar | Prototipo funcional disponible | `Review Prototipo > Verify: agente lee flow > modifica flow > solicita aprobación > usuario aprueba > ejecuta preview > recibe resultados por nodo > diagnostica problema > propone corrección` | El ciclo completo se demuestra end-to-end sin exponer secretos | 🔴 | ❌ | ⬜ |
| TC-006 | Boards/FlowPilot | AC-2 | Edge Case | Approval sobrevive a restart del proceso | Prototipo con approval gate | `Review Prototipo > Trigger: approval pendiente > Kill: proceso IOND > Restart: proceso > Verify: approval sigue pendiente y puede completarse` | El turno parked en row persiste. El usuario puede aprobar/declinar después del restart | 🔴 | ❌ | ⬜ |
| TC-007 | Boards/FlowPilot | AC-2 | Edge Case | Resultados de ejecución truncados para payloads grandes | Prototipo con ejecución | `Review Prototipo > Trigger: ejecución con payload > 1MB > Verify: resultados truncados antes de enviar al modelo` | Payloads grandes se truncan a un tamaño razonable sin perder información diagnóstica clave | 🟠 | ❌ | ⬜ |
| TC-008 | Boards/FlowPilot | AC-2 | Negativo | Agente NO puede ejecutar sin aprobación del usuario | Prototipo con approval gate | `Review Prototipo > Verify: tool run_preview tiene policy "always ask" > Verify: no existe path de ejecución que salte la confirmación` | La ejecución de preview SIEMPRE requiere confirmación. No hay bypass | 🔴 | ❌ | ⬜ |

---

### AC-3: Consumir IOND desde otro agente

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-009 | MCP/FlowPilot | AC-3 | Happy Path | Cliente MCP autorizado invoca tool de prueba con permisos de tenant | Tool MCP de prueba creada, permisos TPerm configurados | `Review Prototipo > Verify: cliente MCP externo invoca tool > respuesta incluye capacidades y reglas de autorización consistentes con FlowPilot` | El cliente MCP externo obtiene las mismas capacidades que FlowPilot, gobernadas por los mismos permisos | 🟠 | ❌ | ⬜ |
| TC-010 | MCP/FlowPilot | AC-3 | Edge Case | Contratos comunes entre Tool Provider, API Workspace y MCP | Diseño documentado | `Review Diseño > Verify: nombres, schemas, IDs públicos, errores, confirmaciones y reglas de consumo son consistentes entre Tool Provider, API Workspace y servidor MCP` | No hay divergencia de contratos entre las tres interfaces | 🟡 | ❌ | ⬜ |
| TC-011 | MCP/FlowPilot | AC-3 | Negativo | El harness interno NO forma parte de la solicitud MCP | Diseño de MCP | `Review Diseño > Verify: servidor MCP consume /api/2.0/workspace/ > Verify: NO importa ni referencia el package del harness (einoengine)` | El MCP público es independiente del harness. Cambiar de Eino a otro harness no afecta al MCP | 🟠 | ❌ | ⬜ |
| TC-012 | MCP/Auth | AC-3 | Negativo | Cliente MCP sin permisos TPerm del tenant → error de autorización | Tool MCP creada, cliente sin permisos | `Review Diseño > Verify: cliente MCP sin permisos invoca tool > Verify: error de autorización retornado` | El servidor MCP rechaza la solicitud con error de permisos claro | 🟠 | ❌ | ⬜ |

---

### AC-4: Preparar la evolución multiagente

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-013 | Boards/FlowPilot | AC-4 | Happy Path | Diseño de sesiones/tools/eventos permite agregar 4 roles sin cambiar contratos públicos | Diseño documentado | `Review Diseño > Verify: interfaces (ToolProvider, SessionStore, EventSink) permiten instanciación por rol > Verify: contratos SSE, tool schemas y API endpoints NO requieren cambios para agregar un rol` | Es posible agregar Planificador, FlowPilot, CodePilot y QA como instancias con diferentes tools/permisos sin modificar interfaces públicas | 🟡 | ❌ | ⬜ |
| TC-014 | Boards/FlowPilot | AC-4 | Edge Case | Cada rol recibe conjunto mínimo y diferente de permisos | Diseño de roles documentado | `Review Diseño > Verify: policy table define qué tools tiene cada rol > Verify: permisos = TPerm ∩ rol ∩ decisión > Verify: un rol solo puede restringir lo que el usuario ya puede hacer` | Cada rol tiene un subconjunto distinto de las 13+ tools, y ningún rol puede escalar permisos del usuario | 🟡 | ❌ | ⬜ |
| TC-015 | Boards/FlowPilot | AC-4 | Edge Case | Lease de escritor por flow previene escrituras simultáneas | Diseño de concurrencia | `Review Diseño > Verify: existe mecanismo de lease por flow > Verify: dos agentes NO pueden escribir el mismo board > Verify: presupuesto AI credits unificado para árbol de agentes` | El diseño documenta lock exclusivo de escritura por flow y presupuesto compartido | 🟡 | ❌ | ⬜ |
| TC-016 | Boards/FlowPilot | AC-4 | Negativo | Agregar un rol requiere modificar contratos públicos → diseño incorrecto | Diseño documentado | `Review Diseño > Simulate: agregar rol "Auditor" con tools de solo lectura > Verify: ¿requiere cambiar schemas SSE, tool schemas o API endpoints?` | Si agregar un rol nuevo requiere cambios en contratos públicos → el diseño no cumple AC-4 | 🟡 | ❌ | ⬜ |

---

### AC-5: Seguridad — Path traversal corregido

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-017 | Security/Boards | AC-5 | Happy Path | flow_id normal opera correctamente | Sub-ticket 1 implementado | `Company Login > Sidebar: Boards > Click [Flow] > Canvas: Open FlowPilot Chat > Send: prompt que opera sobre el flow > Verify: agente accede solo al workspace del tenant actual` | El agente opera normalmente con flow_ids válidos | 🔴 | ✅ | ⬜ |
| TC-018 | Security/Boards | AC-5 | Edge Case | flow_id con caracteres especiales (espacios, unicode, puntos) | Sub-ticket 1 implementado | `Review Code > Verify: sanitización de flow_id incluye caracteres especiales > Test: flow_id con espacios, unicode, puntos simples` | Caracteres especiales son manejados correctamente sin vulnerabilidad | 🔴 | ✅ | ⬜ |
| TC-019 | Security/Boards | AC-5 | Negativo | flow_id con `../` es rechazado — no accede a BD de otro tenant | Sub-ticket 1 implementado | `Review Code > Test: flow_id = "../other_tenant/flow.db" > Verify: operación rechazada > Verify: NO se accede a directorio fuera del workspace > Verify: evento de seguridad en logs` | IOND rechaza la operación. No hay acceso cross-tenant. Log de seguridad generado | 🔴 | ✅ | ⬜ |

---

### AC-6: Seguridad — Permisos correctos del endpoint de chat

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-020 | Security/Auth | AC-6 | Happy Path | Usuario con UpdateBoard puede operar FlowPilot completo | Sub-ticket 1 implementado, usuario con UpdateBoard | `Company Login (user con UpdateBoard) > Sidebar: Boards > Click [Flow] > Canvas: Open FlowPilot Chat > Send: "modifica el nombre del flow" > Verify: agente ejecuta la acción` | Usuario con permisos de escritura puede usar FlowPilot para modificar el board | 🔴 | ✅ | ⬜ |
| TC-021 | Security/Auth | AC-6 | Negativo | Usuario ReadBoard-only NO puede modificar via chat | Sub-ticket 1 implementado, usuario solo ReadBoard | `Company Login (user solo ReadBoard) > Sidebar: Boards > Click [Flow] > Canvas: Open FlowPilot Chat > Send: "borra este nodo" > Verify: error de permisos` | FlowPilot retorna error de permisos. El board NO se modifica | 🔴 | ❌ | ⬜ |

---

### AC-7: Seguridad — Redaction de credentials

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-022 | Security/Boards | AC-7 | Happy Path | Resultados de ejecución llegan al modelo sin headers sensibles | Sub-ticket 1 implementado | `Review Code > Verify: middleware/transformación redacta headers Authorization, Bearer tokens, API keys antes de enviar payload al LLM` | Payloads enviados al modelo NO contienen headers de autorización ni tokens | 🔴 | ❌ | ⬜ |
| TC-023 | Security/Boards | AC-7 | Edge Case | Payloads con múltiples tipos de secrets (OAuth, API keys, Bearer, custom headers) | Sub-ticket 1 implementado | `Review Code > Test: payload con Authorization: Bearer, X-Api-Key, OAuth token, custom secret header > Verify: todos redactados` | Todos los tipos de secrets son redactados, no solo Authorization | 🔴 | ❌ | ⬜ |
| TC-024 | Security/Boards | AC-7 | Negativo | Transcript persistido con Authorization headers → falla de redaction | Sub-ticket 1 implementado | `Review Code > Verify: doble redaction (antes del modelo Y antes del tracing) > Test: buscar headers sensibles en transcript almacenado` | El transcript NO contiene headers sensibles. Doble redaction confirmada | 🔴 | ❌ | ⬜ |

---

### AC-8: Tracking de costos — AI credits

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-025 | Billing/FlowPilot | AC-8 | Happy Path | AI credits se facturan correctamente después de una sesión con Eino | Prototipo Eino funcional con sniffing de coste | `Review Prototipo > Trigger: sesión FlowPilot con múltiples turns > Verify: consumo de AI credits registrado > Verify: credits visibles para el tenant` | El consumo se contabiliza correctamente a pesar de que TokenUsage de Eino no trae coste | 🔴 | ❌ | ⬜ |
| TC-026 | Billing/FlowPilot | AC-8 | Negativo | Sesión sin coste reportado → facturación silenciosa a 0 | Prototipo Eino sin sniffing | `Review Code > Verify: existe mecanismo de sniffing de coste del stream > Test: ¿qué pasa si el sniffing falla? > Verify: error/fallback, NO facturación silenciosa a 0` | Si el sniffing falla, hay un fallback o error claro — nunca facturación a 0 | 🔴 | ❌ | ⬜ |

---

### AC-9: Cutover — Rollback funcional

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-027 | Boards/FlowPilot | AC-9 | Happy Path | Switch de eino a legacy funciona limpiamente | Ambos engines compilados, env var disponible | `Set: FLOWPILOT_ENGINE=legacy > Restart: IOND > Trigger: nueva sesión FlowPilot > Verify: sesión usa engine legacy` | Sesiones nuevas usan el engine legacy después del switch | 🟠 | ❌ | ⬜ |
| TC-028 | Boards/FlowPilot | AC-9 | Edge Case | Switch durante sesión activa | Sesión FlowPilot activa con engine eino | `Trigger: sesión activa con eino > Set: FLOWPILOT_ENGINE=legacy > Restart: IOND > Verify: sesión previa no causa errores > Verify: nueva sesión usa legacy` | Sesiones previas no activas no causan errores. Nuevas sesiones usan legacy | 🟠 | ❌ | ⬜ |

---

## Casos de Regresión

| ID | Módulo impactado | Caso de regresión | Por qué podría romperse | Prioridad |
|----|-----------------|-------------------|------------------------|-----------
| REG-001 | Boards — Canvas | Crear, editar y ejecutar un flow sin FlowPilot | La migración del engine podría afectar el motor de ejecución general de flows (LoadFlow/RunNode/PushNode comparten el mismo backend) | 🔴 |
| REG-002 | Boards — SSE Events | Eventos SSE del canvas (board_lock, board_unlock, board_refresh) siguen funcionando | Sub-ticket 6 traduce eventos de Eino a SSE actuales — los eventos del canvas podrían verse afectados | 🔴 |
| REG-003 | Nodes — Code + FlowPilot | Botón "Ask FlowPilot" en nodo Code sigue funcionando | La interfaz FlowPilot ↔ Code node (IONF-950) podría romperse si cambia la estructura de sesiones o eventos | 🟠 |
| REG-004 | Auth — Permisos | Permisos existentes de boards (ReadBoard, UpdateBoard, CreateBoard, DeleteBoard) no se alteran | Sub-ticket 1 cambia el gate del endpoint de chat — verificar que NO afecta otros endpoints de boards | 🟠 |
| REG-005 | Executions — Historial | Historial de ejecuciones de flows sigue mostrando datos correctos | Si `run_preview` crea ejecuciones, ¿aparecen en el historial? ¿Se distinguen de ejecuciones normales? | 🟡 |
| REG-006 | Keys — Credenciales LLM | Las credenciales de LLM del tenant siguen accesibles para FlowPilot | Eino usa OpenRouter — verificar que las credenciales del tenant se pasan correctamente al nuevo engine | 🟠 |
| REG-007 | Boards — AI Description | Endpoint de AI description (`/ai-description`) sigue funcionando | Este endpoint usa LLM pero NO usa FlowPilot — verificar que la migración no lo afecta | 🟡 |

---

## Queries de Verificación BD

> ⚠️ Este ticket es un Discovery/Refactor. Las queries de BD se aplicarán cuando los sub-tickets se implementen.
> Por ahora se documentan las queries que serán necesarias.

### Verificación de sesiones (cuando se implemente checkpoint store)

```sql
-- Fuente: Pendiente — schema de checkpoint store por definir en sub-ticket 4
-- Verificar que las sesiones de FlowPilot persisten correctamente

-- TC-006: Verificar que un approval pendiente sobrevive a restart
-- Query pendiente hasta que se defina el schema del checkpoint store
-- Expectativa: row con estado "parked" y tool_call_id del approval pendiente
```

### Verificación de permisos (cuando se implemente sub-ticket 1)

```sql
-- Fuente: ../gateway/database/migrations/ (tablas de permisos existentes)
-- TC-020/TC-021: Verificar permisos del usuario

-- Verificar que el endpoint de chat valida el permiso correcto
-- (la query exacta depende de cómo se implemente el cambio de gate)
SELECT p.name, rp.role_id
FROM permissions p
JOIN role_permissions rp ON p.id = rp.permission_id
WHERE p.name IN ('read-board', 'update-board', 'create-board', 'delete-board')
ORDER BY rp.role_id, p.name;
-- Expectativa: el endpoint de chat debe validar al menos update-board para operaciones de escritura
```

### Verificación de consumo AI credits (cuando se implemente sniffing)

```sql
-- Fuente: Pendiente — verificar tabla de consumo de AI credits
-- TC-025/TC-026: Verificar que los AI credits se contabilizan

-- Query pendiente hasta confirmar la tabla de consumo
-- Expectativa: cada sesión de FlowPilot tiene un registro de consumo > 0
```

---

## Notas de Implementación

### Sobre la naturaleza Discovery de este ticket

1. **TCs de review** (TC-001 a TC-016): Se ejecutan revisando documentos, ADR, diseños y prototipos. No requieren UI funcional.
2. **TCs de seguridad** (TC-017 a TC-024): Se ejecutarán cuando los sub-tickets de corrección se implementen. Marcados como ⬜ hasta entonces.
3. **TCs de billing/cutover** (TC-025 a TC-028): Se ejecutarán cuando el engine Eino esté implementado.
4. **TCs de regresión** (REG-001 a REG-007): Se ejecutarán durante el Deployment de cada sub-ticket.

### Dependencia entre sub-tickets y TCs

| Sub-ticket | TCs que habilita |
|---|---|
| 1. Seguridad loop actual | TC-017 a TC-024 |
| 2. Interfaces | TC-013 a TC-016 (parcialmente) |
| 3. Approval gate | TC-005 a TC-008 |
| 4. Diseño Eino | TC-001 a TC-004 (go/no-go) |
| 5. Implementar einoengine | TC-025, TC-026 |
| 6. Paridad eventos + cutover | TC-027, TC-028, REG-001 a REG-007 |
| 7. run_preview + agentes | TC-005 (completo), TC-008 |

---

*Generado por: QA Catalyst (test-docs/document modo matrix) — 2026-10-01*
*Fuentes: ac-consolidated.md, risk-triage.md, L1-project/, L2-modules/boards/, L2-modules/nodes/*
