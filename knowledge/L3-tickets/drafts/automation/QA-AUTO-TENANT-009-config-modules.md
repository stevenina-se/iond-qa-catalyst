## Contexto

### Descripción
Automatización de módulos de configuración del tenant: Credentials (API keys), Notifications, Settings (company info, appearance), Teams (invitaciones, permisos), Account (perfil), y Language (i18n).

### Módulo afectado
- Módulo principal: `Tenant / Config modules`
- Módulos relacionados: `Keycloak`, `Company`

---

## Test Cases

### Credentials

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-CRED-01 | Happy Path | Editar API Key | 🟠 | ⬜ |
| TC-CRED-02 | Happy Path | Seleccionar un Provider | 🟠 | ⬜ |
| TC-CRED-03 | Happy Path | Seleccionar un Model | 🟠 | ⬜ |
| TC-CRED-04 | Happy Path | Eliminar API Key | 🟠 | ⬜ |
| TC-CRED-05 | Happy Path | Filtros en listado de credentials | 🟡 | ⬜ |
| TC-CRED-06 | Happy Path | Columnas del listado | 🟡 | ⬜ |

### Notifications

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-NOTIF-01 | Happy Path | Abrir panel de notificaciones | 🟠 | ⬜ |
| TC-NOTIF-02 | Happy Path | Marcar notificación como leída | 🟠 | ⬜ |
| TC-NOTIF-03 | Happy Path | Eliminar notificación | 🟡 | ⬜ |
| TC-NOTIF-04 | Happy Path | Configurar columnas | 🟡 | ⬜ |
| TC-NOTIF-05 | Happy Path | Aplicar filtros | 🟡 | ⬜ |
| TC-NOTIF-06 | Happy Path | Ver todas las notificaciones | 🟡 | ⬜ |

### Settings

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-SETT-01 | Happy Path | Editar información de compañía | 🟠 | ⬜ |
| TC-SETT-02 | Happy Path | Cambiar a Dark Mode | 🟠 | ⬜ |
| TC-SETT-03 | Happy Path | Colapsar menú lateral | 🟡 | ⬜ |

### Teams

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-TEAM-01 | Happy Path | Invitar miembro al equipo | 🟠 | ⬜ |
| TC-TEAM-02 | Happy Path | Editar invitación pendiente | 🟠 | ⬜ |
| TC-TEAM-03 | Happy Path | Eliminar invitación | 🟠 | ⬜ |
| TC-TEAM-04 | Happy Path | Editar permisos — verificar CADA permiso individual | 🔴 | ⬜ |
| TC-TEAM-05 | Edge Case | Invitar miembro con email ya existente | 🟡 | ⬜ |

### Account

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-ACCT-01 | Happy Path | Actualizar información personal | 🟠 | ⬜ |
| TC-ACCT-02 | Happy Path | Cambiar email | 🟠 | ⛔ Blocked |

### Language

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-LANG-01 | Happy Path | Cambiar idioma | 🟠 | ⬜ |
| TC-LANG-02 | Negativo | Verificar vistas con traducciones faltantes (i18n) | 🟠 | ⬜ |

---

## Notas de Automatización
- Teams > Edit Permissions: requiere verificar CADA permiso individual — test extenso
- Change Email: BLOCKED por ahora
- Language: observación del CSV — "Verify Missing Views with i18n"
- Tenant Dashboard se incluye aquí como test base:

### Dashboard

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-DASH-01 | Happy Path | Dashboard del tenant carga correctamente | 🟡 | ⬜ |
