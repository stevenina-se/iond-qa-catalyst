# QA-AUTO-GW-001 — Admin Gateway: Apps (Services, Integrations, Settings)

> Módulo: Admin Gateway > Apps
> Side: ADMIN GATEWAY
> Assignee: [PENDIENTE]
> Prioridad: 🔵 Low
> Status: Manual for now

## Contexto

### Descripción
Automatización de la gestión de Apps en Admin Gateway: CRUD de apps, configuración (OAuth, URLs, imágenes), gestión de servicios (filtros, enable/disable individual y en bulk), edición de servicios y Custom Integrations.

### Módulo afectado
- Módulo principal: `Admin Gateway / Apps`
- Módulos relacionados: `Marketplace`, `Grapps`, `Customer`

---

## Test Cases

### App CRUD

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-GW-APP-01 | Happy Path | Crear nueva app | 🔵 | ⬜ |
| TC-GW-APP-02 | Happy Path | Editar app existente | 🔵 | ⬜ |
| TC-GW-APP-03 | Happy Path | Eliminar app | 🔵 | ⬜ |

### App > Settings

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-GW-APP-04 | Happy Path | Copiar OAuth Key | 🔵 | ⬜ |
| TC-GW-APP-05 | Happy Path | Copiar App URL | 🔵 | ⬜ |
| TC-GW-APP-06 | Happy Path | Set Image de la app | 🔵 | ⬜ |

### App > Services

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-GW-SVC-01 | Happy Path | Filtrar por Slug | 🔵 | ⬜ |
| TC-GW-SVC-02 | Happy Path | Filtrar por Title | 🔵 | ⬜ |
| TC-GW-SVC-03 | Happy Path | Filtrar por Description | 🔵 | ⬜ |
| TC-GW-SVC-04 | Happy Path | Filtrar por Categories | 🔵 | ⬜ |
| TC-GW-SVC-05 | Happy Path | Filtrar por Type | 🔵 | ⬜ |
| TC-GW-SVC-06 | Happy Path | Enable en bulk | 🔵 | ⬜ |
| TC-GW-SVC-07 | Happy Path | Disable en bulk | 🔵 | ⬜ |
| TC-GW-SVC-08 | Happy Path | Enable individual | 🔵 | ⬜ |
| TC-GW-SVC-09 | Happy Path | Disable individual | 🔵 | ⬜ |

### App > Services > Edit

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-GW-SVC-10 | Happy Path | Set Image del servicio | 🔵 | ⬜ |
| TC-GW-SVC-11 | Happy Path | Set Title | 🔵 | ⬜ |
| TC-GW-SVC-12 | Happy Path | Set Details | 🔵 | ⬜ |
| TC-GW-SVC-13 | Happy Path | Set Description | 🔵 | ⬜ |
| TC-GW-SVC-14 | Happy Path | Set Features | 🔵 | ⬜ |
| TC-GW-SVC-15 | Happy Path | Set Groups | 🔵 | ⬜ |
| TC-GW-SVC-16 | Happy Path | Set Category | 🔵 | ⬜ |
| TC-GW-SVC-17 | Happy Path | Enable Badge | 🔵 | ⬜ |
| TC-GW-SVC-18 | Happy Path | Custom Credentials | 🔵 | ⬜ |
| TC-GW-SVC-19 | Happy Path | Copy Cart | 🔵 | ⬜ |
| TC-GW-SVC-20 | Happy Path | Copy Install | 🔵 | ⬜ |
| TC-GW-SVC-21 | Happy Path | Copy Callback | 🔵 | ⬜ |

### Custom Integrations

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-GW-INT-01 | Happy Path | Crear Custom Integration | 🔵 | ⬜ |

### Integrations

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-GW-INT-02 | Happy Path | Listar integraciones | 🔵 | ⬜ |
| TC-GW-INT-03 | Happy Path | Claim integración | 🔵 | ⬜ |

### Go Back

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-GW-NAV-01 | Happy Path | Go Back navega a la pantalla anterior | 🔵 | ⬜ |

---

## Notas de Automatización
- Todos los tests son Low priority — "Manual for now"
- 29 test cases — módulo extenso pero de baja criticidad
- Automatizar después de los módulos Urgent y High
