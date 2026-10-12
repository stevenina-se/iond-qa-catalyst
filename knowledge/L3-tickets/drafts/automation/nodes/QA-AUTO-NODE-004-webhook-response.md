## Contexto

### Descripción
Automatización del nodo **Webhook Response**. Este nodo permite configurar la respuesta HTTP que se envía al caller que disparó el webhook, incluyendo status code y body personalizado.

> **Fuente**: `Iond Testing Plan - Iond Automation Plan.csv` (línea 58)
> **Referencia técnica**: `knowledge/L2-modules/nodes/module.md` — Sección 14 (Triggers)

### Módulo afectado
- Módulo principal: `Tenant / Boards / Canvas / Webhook Response`
- Backend: `com.ion.webhook_response`
- Módulos relacionados: `Webhook (trigger)`, `Boards`

### Pre-requisitos
- Board con nodo Webhook configurado como trigger
- Herramienta para enviar HTTP requests y verificar la respuesta

---

## Test Cases

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-NODE-WHR-01 | Happy Path | Configurar Webhook Response y verificar que la respuesta llega al caller | 🔴 | ⬜ |
| TC-NODE-WHR-02 | Happy Path | Configurar status code y body personalizado en la response | 🔴 | ⬜ |
| TC-NODE-WHR-03 | Edge Case | Webhook Response con datos dinámicos del flow `{{$N.field}}` en el body | 🟠 | ⬜ |
| TC-NODE-WHR-04 | Negativo | Flow con Webhook pero sin Webhook Response — verificar comportamiento del caller | 🟡 | ⬜ |

---

## Notas de Automatización
- Siempre se testea en conjunto con el nodo Webhook (trigger)
- Verificar que las expresiones dinámicas se resuelven antes de enviar la response
- 4 test cases
