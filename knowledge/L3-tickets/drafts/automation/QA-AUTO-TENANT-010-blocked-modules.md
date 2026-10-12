# QA-AUTO-TENANT-010 — Tenant: Accounts, Developer Apps, Catalog (Blocked)

> Módulo: Tenant > Accounts, Developer Apps, Catalog
> Side: TENANT
> Assignee: [PENDIENTE]
> Prioridad: 🟠 High
> Status: ⛔ Blocked

## Contexto

### Descripción
Automatización de módulos actualmente bloqueados: Accounts (depende de feature de marketplaces), Developer Apps y Catalog (depende de Grapps).

### Módulo afectado
- Módulo principal: `Tenant / Accounts`, `Tenant / Developer Apps`, `Tenant / Catalog`
- Módulos relacionados: `Marketplace`, `Grapps`, `Gateway`

### Blocker
> ⚠️ Todos estos módulos están **BLOCKED**:
> - **Accounts**: "Se debe tener lista la feature de los marketplaces"
> - **Developer Apps**: Bloqueado por dependencias
> - **Catalog**: Bloqueado por Grapps

---

## Test Cases

### Accounts

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-ACCTS-01 | Happy Path | Agregar account | 🟠 | ⛔ Blocked |
| TC-ACCTS-02 | Happy Path | Editar account | 🟠 | ⛔ Blocked |
| TC-ACCTS-03 | Happy Path | Eliminar account | 🟠 | ⛔ Blocked |

### Developer Apps

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-DEVAPP-01 | Happy Path | Agregar Developer App | 🟠 | ⛔ Blocked |
| TC-DEVAPP-02 | Happy Path | Configurar App | 🟠 | ⛔ Blocked |
| TC-DEVAPP-03 | Happy Path | Editar App | 🟠 | ⛔ Blocked |
| TC-DEVAPP-04 | Happy Path | Eliminar App | 🟠 | ⛔ Blocked |

### Catalog

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-CAT-01 | Happy Path | Agregar item al catálogo (Crear Grapp) | 🟠 | ⛔ Blocked |
| TC-CAT-02 | Happy Path | Editar item del catálogo | 🟠 | ⛔ Blocked |
| TC-CAT-03 | Happy Path | Eliminar item del catálogo | 🟠 | ⛔ Blocked |

---

## Notas de Automatización
- Todos los tests están bloqueados hasta que las features dependientes estén listas
- Revisar en cada sprint si los blockers fueron resueltos
