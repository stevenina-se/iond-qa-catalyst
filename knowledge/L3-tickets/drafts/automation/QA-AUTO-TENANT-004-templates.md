## Contexto

### Descripción
Automatización de la validación del módulo de Templates del tenant, incluyendo Public Templates y Community Templates con sus operaciones de preview, detalle, uso y filtrado.

### Módulo afectado
- Módulo principal: `Tenant / Templates`
- Módulos relacionados: `Boards`, `Admin / Templates`

---

## Test Cases

### Public Templates

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-TPL-PUB-01 | Happy Path | Preview de template público | 🟠 | ⬜ |
| TC-TPL-PUB-02 | Happy Path | Ver detalles completos del template | 🟠 | ⬜ |
| TC-TPL-PUB-03 | Happy Path | Usar template — crea board basado en template | 🔴 | ⬜ |
| TC-TPL-PUB-04 | Happy Path | Expandir tags del template | 🟡 | ⬜ |
| TC-TPL-PUB-05 | Happy Path | Aplicar filtros al listado | 🟡 | ⬜ |

### Community Templates

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-TPL-COM-01 | Happy Path | Preview de template de la comunidad | 🟠 | ⬜ |
| TC-TPL-COM-02 | Happy Path | Ver detalles completos del template | 🟠 | ⬜ |
| TC-TPL-COM-03 | Happy Path | Usar template de comunidad — crea board | 🔴 | ⬜ |
| TC-TPL-COM-04 | Happy Path | Expandir tags del template | 🟡 | ⬜ |
| TC-TPL-COM-05 | Happy Path | Aplicar filtros al listado | 🟡 | ⬜ |

---

## Notas de Automatización
- Pre-requisito: Templates públicos y de comunidad publicados desde Admin
- "Use Template" debe verificar que el board se crea correctamente con todos los nodos
