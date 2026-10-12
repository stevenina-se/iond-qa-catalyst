## Contexto

### Descripción
Automatización de los nodos **Tenant App** en el canvas. Estos nodos representan las acciones de las apps instaladas del tenant (app connectors). Incluyen uso directo de nodos y creación de nodos asistida por IonMind (IA).

> **Fuente**: `Iond Testing Plan - Iond Automation Plan.csv` (líneas 82-83)
> **Referencia técnica**: `knowledge/L2-modules/nodes/module.md` — Backend nodes en `backend/ion/nodes/`

### Módulo afectado
- Módulo principal: `Tenant / Boards / Canvas / Tenant App`
- Backend: Backend nodes en `backend/ion/nodes/` — usan `packages/channel/` para auth
- Dependencia: `Connections` (conexiones activas), `App Connectors` (apps configuradas)
- Módulos relacionados: `Connections`, `App Connectors`, `Integrations`, `IonMind`

### Pre-requisitos
- Board de prueba con draft activo
- Al menos un App Connector configurado con nodos disponibles
- Conexión activa para la app del tenant
- IonMind desplegado para tests de creación con IA

---

## Test Cases

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-NODE-TAPP-01 | Happy Path | Usar un nodo de app del tenant — verificar que ejecuta la acción configurada | 🔴 | ⬜ |
| TC-NODE-TAPP-02 | Happy Path | Agregar nodo con IonMind — verificar que el nodo se crea correctamente con la configuración generada | 🔴 | ⬜ |
| TC-NODE-TAPP-03 | Happy Path | Configurar y ejecutar nodo de app con conexión activa — verificar resultado | 🔴 | ⬜ |
| TC-NODE-TAPP-04 | Negativo | Ejecutar nodo de app sin conexión configurada — verificar error claro | 🔴 | ⬜ |
| TC-NODE-TAPP-05 | Negativo | Ejecutar nodo de app con conexión expirada — verificar error y refresh attempt | 🟠 | ⬜ |
| TC-NODE-TAPP-06 | Edge Case | Nodo de app con autenticación OAuth — verificar refresh token durante ejecución | 🟠 | ⬜ |

---

## Notas de Automatización
- Los app nodes dependen de `packages/channel/` para auth — OAuth refresh puede causar flakiness
- Requiere conexiones activas — depende de QA-AUTO-TENANT-005 (Connections)
- IonMind debe estar desplegado para TC-NODE-TAPP-02
- 6 test cases
