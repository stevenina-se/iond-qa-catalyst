# QA-AUTO-ADMIN-001 — Admin: Dashboard

> Módulo: Admin > Dashboard
> Side: ADMIN
> Assignee: Mijael
> Prioridad: 🟡 Low
> Status: Pending

## Contexto

### Descripción
Automatización de la validación del Dashboard administrativo. Verificar carga correcta, widgets, datos estadísticos y navegación principal.

### Módulo afectado
- Módulo principal: `Admin / Dashboard`
- Módulos relacionados: `Companies`, `Boards`, `Connectors`

---

## Test Cases

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-ADMIN-DASH-01 | Happy Path | Dashboard carga correctamente tras login como admin | 🟠 | ⬜ |
| TC-ADMIN-DASH-02 | Happy Path | Widgets de estadísticas muestran datos correctos | 🟡 | ⬜ |
| TC-ADMIN-DASH-03 | Happy Path | Navegación desde dashboard a cada módulo funciona | 🟡 | ⬜ |
| TC-ADMIN-DASH-04 | Edge Case | Dashboard con datos vacíos (sin compañías) muestra estado vacío | 🟡 | ⬜ |

---

## Notas de Automatización
- Pre-requisito: Login como usuario con rol Admin
- Verificar tiempos de carga del dashboard
