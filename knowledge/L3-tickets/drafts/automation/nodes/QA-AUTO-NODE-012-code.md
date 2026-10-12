## Contexto

### Descripción
Automatización del nodo **Code**. Este nodo ejecuta código Python o JavaScript en un servicio externo (Code Runner) vía gRPC. Soporta variables, dependencias externas y tiene integración con FlowPilot (IONF-950) para generación y corrección de código vía IA.

> **Fuente**: `Iond Testing Plan - Iond Automation Plan.csv` (línea 66)
> **Referencia técnica**: `knowledge/L2-modules/nodes/module.md` — Sección 2 (Code)

### Módulo afectado
- Módulo principal: `Tenant / Boards / Canvas / Code`
- Backend: `ion.action.code` — Package `core/actions/code`
- Lenguajes: `python`, `javascript`
- Config: `{ "language": "python|javascript", "code_py": "...", "code_js": "...", "variables": [...], "timeout": 1-300, "dependencies": [...] }`
- Outputs: `output` (resultado), `error`
- Response: `{ status, result, stdout, stderr, error: { type, message, line, traceback }, execution_time_ms }`
- Timeout: 1-300 segundos (default: 30s)
- Servicio externo: `CODE_RUNNER_URL` (gRPC, puede ser TLS o insecure)
- Tests backend: `code_test.go`
- Drawer en: `FlowDrawer/Code/`

### Pre-requisitos
- Board de prueba con draft activo
- Code Runner desplegado y accesible (`CODE_RUNNER_URL`)
- IonMind desplegado para tests de FlowPilot

---

## Reglas de Seguridad
- El código se lee desde `staticData` (no `processedData`) para **evitar inyección de expresiones**
- Las variables se pasan como pares name/value
- Soporta dependencias externas (pip/npm packages)

---

## Test Cases

### Ejecución Base

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-NODE-CODE-01 | Happy Path | Ejecutar código JavaScript simple — verificar output con resultado | 🔴 | ⬜ |
| TC-NODE-CODE-02 | Happy Path | Ejecutar código Python simple — verificar output | 🔴 | ⬜ |
| TC-NODE-CODE-03 | Happy Path | Pasar variables al código y leerlas desde `input` — verificar acceso | 🔴 | ⬜ |
| TC-NODE-CODE-04 | Happy Path | Verificar que el resultado se retorna con `return` | 🔴 | ⬜ |
| TC-NODE-CODE-05 | Happy Path | Usar dependencias externas (pip/npm packages) — verificar instalación y ejecución | 🟠 | ⬜ |
| TC-NODE-CODE-06 | Happy Path | Verificar campos de response: `status`, `result`, `stdout`, `stderr`, `execution_time_ms` | 🟠 | ⬜ |

### Errores y Validaciones

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-NODE-CODE-07 | Negativo | Código con error de sintaxis — verificar que error incluye `type`, `message`, `line`, `traceback` | 🔴 | ⬜ |
| TC-NODE-CODE-08 | Negativo | Código que excede timeout (default 30s) — verificar terminación y error | 🟠 | ⬜ |
| TC-NODE-CODE-09 | Edge Case | Timeout configurado al máximo (300s) — verificar que acepta | 🟡 | ⬜ |
| TC-NODE-CODE-10 | Edge Case | Timeout configurado a 0 o negativo — verificar validación | 🟡 | ⬜ |
| TC-NODE-CODE-11 | Edge Case | Código lee datos desde `staticData` (no `processedData`) — verificar seguridad contra inyección | 🟠 | ⬜ |

### Integración FlowPilot (IONF-950)

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-NODE-CODE-12 | Happy Path | Usar botón "Ask FlowPilot" ✨ — verificar que abre chat con contexto del nodo (lenguaje, variables, dependencias) | 🟠 | ⬜ |
| TC-NODE-CODE-13 | Happy Path | FlowPilot genera código — verificar que el código generado es válido y ejecutable | 🟡 | ⬜ |
| TC-NODE-CODE-14 | Happy Path | FlowPilot corrige error — enviar error de ejecución y verificar que genera corrección | 🟡 | ⬜ |

---

## Notas de Automatización
- Requiere Code Runner (`CODE_RUNNER_URL`) activo — sin él los tests fallan por timeout
- Tests de FlowPilot (12-14) requieren IonMind activo
- Frontend: módulo `codeContext.ts`, handler `open_node_copilot` en `FlowEditor.vue`
- Tests frontend existentes: `codeContext.spec.ts` (148 líneas), `FlowEditor.spec.ts`
- Regla CONFIDENTIALITY en `system.go` del agente protege contenido de skills
- 14 test cases — el ticket de nodo más grande
