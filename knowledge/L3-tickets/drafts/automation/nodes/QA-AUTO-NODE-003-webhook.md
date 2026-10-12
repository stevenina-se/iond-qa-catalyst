## Contexto

### Descripción
Automatización del nodo **Webhook** (Trigger). Este nodo inicia la ejecución de un flow cuando recibe un HTTP request externo en la URL del webhook.

> **Fuente**: `Iond Testing Plan - Iond Automation Plan.csv` (línea 57)
> **Referencia técnica**: `knowledge/L2-modules/nodes/module.md` — Sección 14 (Triggers)

### Módulo afectado
- Módulo principal: `Tenant / Boards / Canvas / Webhook`
- Backend: `com.ion.request` (trigger)
- Módulos relacionados: `Boards`, `Webhooks`

### Pre-requisitos
- Board de prueba con draft activo
- Herramienta para enviar HTTP requests (Postman, curl, etc.)

---

## Test Cases

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-NODE-WH-01 | Happy Path | Configurar webhook y enviar request externa — verificar que el flow se dispara | 🔴 | ⬜ |
| TC-NODE-WH-02 | Happy Path | Verificar que el payload del request externo llega correctamente al output del nodo | 🔴 | ⬜ |
| TC-NODE-WH-03 | Negativo | Enviar request al webhook con método HTTP incorrecto — verificar comportamiento | 🟠 | ⬜ |
| TC-NODE-WH-04 | Edge Case | Enviar múltiples requests simultáneos al webhook — verificar que se generan ejecuciones independientes | 🟠 | ⬜ |
| TC-NODE-WH-05 | Edge Case | Webhook en board desactivado — verificar que no se ejecuta | 🟠 | ⬜ |

---

## Notas de Automatización
- La URL del webhook se obtiene en el módulo Webhooks del tenant
- Verificar relación con el módulo de Webhooks (QA-AUTO-TENANT-005)
- 5 test cases
