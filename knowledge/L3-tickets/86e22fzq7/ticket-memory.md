# Ticket: 86e22fzq7 — Connections — Reautorización por API Key crea conexión duplicada en lugar de sobrescribir

> Sesión de Discovery iniciada: 2026-07-14
> Módulo: Connections / Integrations
> QA Engineer: Steve Nina

## Contexto del Ticket

### Descripción
Bug: Al realizar el proceso de reautorización de una conexión con método de autenticación API Key, el sistema crea una nueva conexión adicional en lugar de sobrescribir/actualizar la conexión existente. Adicionalmente, se emiten dos toasts de éxito de reautorización. Esto genera conexiones duplicadas en el sistema.

### Root Cause (identificado por Developer)
- **Frontend (gateway-ion)**: Los toasts de éxito para "connection approved" y "connection validated" se mostraban también durante reautorización (pensados solo para creación).
- **Backend (flow_binaries)**: En `resolveCompanyAppAndConnection`, cuando `attempt.ConnectionId` estaba presente para una global app, el `ConnectionTenant` existente no se cargaba → el upsert insertaba un duplicado en lugar de actualizar.

### Solución del Developer (branch IONF-1114)

**Repos afectados**: `gateway-ion` (PR #12) + `flow_binaries` (PR #14)

| Repo | Cambio Principal |
|------|-----------------|
| `gateway-ion` | `isReauthorize` computed property. Toasts suprimidos durante reauthorize. Refactored `testAttempt`: `handleAuthorizingStatus`, `handleSuccessStatus`, `showSuccessToast`. |
| `flow_binaries` | En `resolveCompanyAppAndConnection`, cuando `attempt.ConnectionId` presente para global app, se carga `ConnectionTenant` existente via `FindConnectionByCompany` y se inyecta en auth context para que upsert actualice en lugar de crear. |

### Módulo afectado
- Módulo principal: `Connections / Integrations`
- Módulos relacionados: `Boards` (flows que referencian connections), `Auth` (flujo OAuth)

### Datos del entorno de testing
- Rol: Company User con permiso de gestión de connections
- Entorno: Staging (dev-app.ionflow.io)
- Branch `IONF-1114` → base `DEVELOPMENT`
- PRs: gateway-ion PR #12, flow_binaries PR #14
- Deployed: ✅ confirmado por Rodolfo (2026-07-14 16:51)
- Assignee: Gustavo Mamani
- Code Review: ✅ Aprobado por Enrique Vicente (2026-07-09) + Rodolfo Merlo Ali (2026-07-14)

### QA Instructions del Developer
1. Reauthorize una conexión OAuth existente (global app) → no duplicado, no toast
2. Crear conexión nueva (global app) → toast aparece normalmente
3. Reauthorize tenant app connection → sin regresiones
4. Probar flujos `authorizing` (OAuth) y `success` inmediato (API Key)

---

## Transcript de la Sesión

| Timestamp | Acción | Detalle |
|-----------|--------|---------|
| 2026-07-14 16:54 | Session Start | Contexto cargado: L1 completo + L2 connections + ticket de ClickUp |
| 2026-07-14 16:54 | Discovery | Iniciando generación de artefactos |
