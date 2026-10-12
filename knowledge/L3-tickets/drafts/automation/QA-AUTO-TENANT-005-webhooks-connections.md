## Contexto

### Descripción
Automatización de la gestión de Webhooks (activar/desactivar, eliminar, copiar path, filtros) y Connections (check, reauthorize, delete, filtros).

### Módulo afectado
- Módulo principal: `Tenant / Webhooks`, `Tenant / Connections`
- Módulos relacionados: `Boards`, `App Connectors`

---

## Test Cases

### Webhooks

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-WHK-01 | Happy Path | Activar webhook | 🟠 | ⬜ |
| TC-WHK-02 | Happy Path | Desactivar webhook activo | 🟠 | ⬜ |
| TC-WHK-03 | Happy Path | Eliminar webhook | 🟠 | ⬜ |
| TC-WHK-04 | Happy Path | Navegar al board asociado (Go to Board) | 🟡 | ⬜ |
| TC-WHK-05 | Happy Path | Copiar path del webhook | 🟡 | ⬜ |
| TC-WHK-06 | Happy Path | Aplicar filtros al listado | 🟡 | ⬜ |
| TC-WHK-07 | Happy Path | Configurar columnas visibles | 🟡 | ⬜ |

### Connections

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-CONN-01 | Happy Path | Verificar conexión existente (Check Connection) | 🟠 | ⬜ |
| TC-CONN-02 | Happy Path | Re-autorizar conexión (Reauthorize) | 🟠 | ⬜ |
| TC-CONN-03 | Happy Path | Eliminar conexión | 🟠 | ⬜ |
| TC-CONN-04 | Happy Path | Buscar conexión con filtro de búsqueda | 🟡 | ⬜ |
| TC-CONN-05 | Edge Case | Check Connection de app custom — requiere app custom existente | 🟠 | ⬜ |
| TC-CONN-06 | Negativo | Re-autorizar con credenciales expiradas | 🟠 | ⬜ |

---

## Notas de Automatización
- Webhooks: Pre-requisito — al menos 1 board con nodo webhook configurado
- Connections: Pre-requisito — al menos 1 app custom creada (ver observación del CSV)
