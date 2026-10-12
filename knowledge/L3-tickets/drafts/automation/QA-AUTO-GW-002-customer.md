# QA-AUTO-GW-002 — Admin Gateway: Customer (Marketplace & Grapps E2E)

> Módulo: Admin Gateway > Customer
> Side: ADMIN GATEWAY
> Assignee: Steve Nina, Mijael
> Prioridad: 🔴 Urgent
> Status: Manual for now

## Contexto

### Descripción
Automatización del flujo completo del Customer en Gateway: login, canales configurados (instalación, ejecución, updates, edición, conexiones, schedules, cron de Grapps), marketplace (Grapps con/sin global apps, conexiones, configuración de flows) y funcionalidad de boards.

### Módulo afectado
- Módulo principal: `Admin Gateway / Customer`
- Módulos relacionados: `Grapps`, `Marketplace`, `Boards`, `Connections`

---

## Test Cases

### Login > Configured Channels > Grapps

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-GW-CUST-01 | Happy Path | Instalar Grapp desde canal configurado | 🔴 | ⬜ |
| TC-GW-CUST-02 | Happy Path | Ver historial de ejecución del Grapp | 🔴 | ⬜ |
| TC-GW-CUST-03 | Happy Path | Verificar actualizaciones del Grapp (Check Updates) | 🟠 | ⬜ |
| TC-GW-CUST-04 | Happy Path | Editar configuración de flow del Grapp | 🔴 | ⬜ |
| TC-GW-CUST-05 | Happy Path | Gestionar conexiones del Grapp | 🔴 | ⬜ |
| TC-GW-CUST-06 | Happy Path | Configurar Schedule del Grapp | 🟠 | ⬜ |
| TC-GW-CUST-07 | Happy Path | Configurar Cron del Grapp | 🟠 | ⬜ |

### Login > Available Marketplace

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-GW-MKT-01 | Happy Path | Instalar Grapp SIN Global Apps | 🔴 | ⬜ |
| TC-GW-MKT-02 | Happy Path | Instalar Grapp CON Global Apps | 🔴 | ⬜ |
| TC-GW-MKT-03 | Happy Path | Agregar una conexión al instalar | 🔴 | ⬜ |
| TC-GW-MKT-04 | Happy Path | Verificar una conexión (Check Connection) | 🟠 | ⬜ |
| TC-GW-MKT-05 | Happy Path | Re-autorizar conexión | 🟠 | ⬜ |
| TC-GW-MKT-06 | Happy Path | Configurar flow/acciones del Grapp | 🔴 | ⬜ |

### Login > Boards

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-GW-BRD-01 | Happy Path | Verificar funcionalidad de todos los nodos en board del customer | 🔴 | ⬜ |

---

## Notas de Automatización
- 14 test cases — Todos URGENT, actualmente "Manual for now"
- Este módulo es un E2E completo del marketplace y Grapps desde la perspectiva del customer
- Requiere: Grapps publicados, marketplace configurado, al menos 1 global app
- Pre-requisitos pesados — considerar como último módulo a automatizar por dependencias
