## Contexto

### Descripción
Automatización del nodo **Agent**. Este nodo de agente de IA ejecuta lógica basada en LLMs dentro del flow, con system prompt, input prompt configurable y timeout ajustable.

> **Fuente**: `Iond Testing Plan - Iond Automation Plan.csv` (línea 69)
> **Referencia técnica**: `knowledge/L2-modules/nodes/module.md` — Sección 13 (Agent)

### Módulo afectado
- Módulo principal: `Tenant / Boards / Canvas / Agent`
- Backend: `ion.action.agent` — nuevo, en desarrollo
- Config: `{ system_prompt: string, input_prompt: string (required), timeout: 1-120s }`
- Inputs: `input`
- Outputs: `output`, `error`
- Drawer en: `FlowDrawer/Agent/`
- Dependencia: `Credentials` (API keys de LLMs)

### Pre-requisitos
- Board de prueba con draft activo
- Credenciales LLM configuradas en el módulo Credentials
- IonMind / LLM service disponible

---

## Test Cases

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-NODE-AGENT-01 | Happy Path | Configurar `system_prompt` e `input_prompt` y ejecutar — verificar respuesta del LLM | 🔴 | ⬜ |
| TC-NODE-AGENT-02 | Happy Path | Usar expresiones dinámicas `{{$N.field}}` en `input_prompt` | 🔴 | ⬜ |
| TC-NODE-AGENT-03 | Happy Path | Configurar timeout (ej. 60s) y verificar que se respeta | 🟠 | ⬜ |
| TC-NODE-AGENT-04 | Negativo | Ejecutar sin credenciales LLM configuradas — verificar error claro | 🔴 | ⬜ |
| TC-NODE-AGENT-05 | Negativo | Dejar `input_prompt` vacío (required) — verificar validación | 🟠 | ⬜ |
| TC-NODE-AGENT-06 | Negativo | Timeout excedido por respuesta lenta del LLM — verificar error y edge de error | 🟠 | ⬜ |
| TC-NODE-AGENT-07 | Edge Case | Timeout en valor límite (1s y 120s) — verificar aceptación | 🟡 | ⬜ |

---

## Notas de Automatización
- Requiere credenciales LLM activas — depende de QA-AUTO-TENANT-009 (Credentials)
- Nodo relativamente nuevo — mayor riesgo de bugs
- Las respuestas de LLM son no determinísticas — verificar estructura de respuesta más que contenido exacto
- 7 test cases
