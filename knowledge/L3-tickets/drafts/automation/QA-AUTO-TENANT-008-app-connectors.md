## Contexto

### Descripción
Automatización de la gestión completa de App Connectors: listado (base, webhooks, nodes, auth), creación (manual, vía IonMind, endpoints vía IonMind), draft connectors y filtros.

### Módulo afectado
- Módulo principal: `Tenant / App Connectors`
- Módulos relacionados: `IonMind`, `Boards / Tenant App`, `Connections`

---

## Test Cases

### List > Base

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-APPCON-01 | Happy Path | Editar conector base (nombre, logo, config) | 🔴 | ⬜ |

### List > Webhooks

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-APPCON-02 | Happy Path | Agregar webhook al conector | 🔴 | ⬜ |
| TC-APPCON-03 | Happy Path | Editar webhook existente | 🟠 | ⬜ |
| TC-APPCON-04 | Happy Path | Eliminar webhook | 🟠 | ⬜ |

### List > Nodes

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-APPCON-05 | Happy Path | Agregar nodo manualmente | 🔴 | ⬜ |
| TC-APPCON-06 | Happy Path | Agregar nodo con IonMind (IA) | 🔴 | ⬜ |
| TC-APPCON-07 | Happy Path | Versionar un nodo existente | 🔴 | ⬜ |
| TC-APPCON-08 | Happy Path | Editar nodo | 🟠 | ⬜ |
| TC-APPCON-09 | Happy Path | Eliminar nodo | 🟠 | ⬜ |
| TC-APPCON-10 | Edge Case | Versionar nodo — verificar que versión anterior sigue disponible | 🟠 | ⬜ |

### List > Auth List

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-APPCON-11 | Happy Path | Agregar método de autenticación | 🔴 | ⬜ |
| TC-APPCON-12 | Happy Path | Editar método de auth | 🟠 | ⬜ |
| TC-APPCON-13 | Happy Path | Eliminar método de auth | 🟠 | ⬜ |

### Create

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-APPCON-14 | Happy Path | Crear conector manual | 🔴 | ⬜ |
| TC-APPCON-15 | Happy Path | Crear conector vía IonMind — Analizar URL | 🔴 | ⬜ |
| TC-APPCON-16 | Happy Path | Upload logo vía Logo.dev | 🟠 | ⬜ |
| TC-APPCON-17 | Happy Path | Endpoints vía IonMind — verificar notificaciones | 🔴 | ⬜ |
| TC-APPCON-18 | Happy Path | Buscar conectores con filtros | 🟡 | ⬜ |

### Draft Connector

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-APPCON-19 | Happy Path | Crear y guardar draft connector | 🔴 | ⬜ |
| TC-APPCON-20 | Happy Path | Eliminar draft connector | 🟠 | ⬜ |
| TC-APPCON-21 | Happy Path | Buscar entre drafts con filtros | 🟡 | ⬜ |

---

## Notas de Automatización
- Requiere IonMind activo para tests de creación vía IA y minado de endpoints
- Logo.dev requiere API key configurada
- 21 test cases — segundo módulo más grande después de Boards
