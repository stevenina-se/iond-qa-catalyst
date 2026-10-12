## Contexto

### Descripción
Automatización del nodo **Schedule** (Trigger Programado). Este nodo inicia la ejecución de un flow de forma automática según un cron expression configurado.

> **Fuente**: `Iond Testing Plan - Iond Automation Plan.csv` (línea 55)
> **Referencia técnica**: `knowledge/L2-modules/nodes/module.md` — Sección 14 (Triggers)

### Módulo afectado
- Módulo principal: `Tenant / Boards / Canvas / Schedule`
- Backend: `com.ion.schedule` (trigger)
- Módulos relacionados: `Boards`

### Pre-requisitos
- Board de prueba creado con al menos 1 draft activo

---

## Test Cases

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-NODE-SCHED-01 | Happy Path | Configurar schedule con cron expression válida y verificar que el flow se ejecuta en el momento indicado | 🔴 | ⬜ |
| TC-NODE-SCHED-02 | Happy Path | Modificar schedule existente y verificar que el nuevo horario aplica | 🔴 | ⬜ |
| TC-NODE-SCHED-03 | Negativo | Configurar schedule con cron expression inválida — verificar mensaje de error | 🟠 | ⬜ |
| TC-NODE-SCHED-04 | Edge Case | Desactivar board con schedule activo — verificar que el trigger se desactiva | 🟠 | ⬜ |
| TC-NODE-SCHED-05 | Edge Case | Reactivar board — verificar que el schedule se reactiva sin necesidad de reconfigurar | 🟡 | ⬜ |

---

## Notas de Automatización
- Requiere esperar a que el cron se dispare — considerar cron expressions de alta frecuencia para tests (e.g. cada minuto)
- Verificar interacción con Active/Pause del board
- 5 test cases
