## Contexto

### Descripción
Automatización del nodo **HTTP Request**. Este nodo permite ejecutar requests HTTP (GET, POST, PUT, DELETE) a URLs externas o internas, con headers, body y expresiones dinámicas.

> **Fuente**: `Iond Testing Plan - Iond Automation Plan.csv` (línea 56)
> **Referencia técnica**: `knowledge/L2-modules/nodes/module.md`

### Módulo afectado
- Módulo principal: `Tenant / Boards / Canvas / HTTP Request`
- Backend: Nodo de plataforma en `backend/ion/nodes/`
- Módulos relacionados: `Connections`, `Boards`

### Pre-requisitos
- Board de prueba con draft activo
- URL de testing disponible (mock server o endpoint real)

---

## Test Cases

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-NODE-HTTP-01 | Happy Path | Configurar y ejecutar request GET exitoso — verificar output con response body | 🔴 | ⬜ |
| TC-NODE-HTTP-02 | Happy Path | Configurar y ejecutar request POST con body JSON | 🔴 | ⬜ |
| TC-NODE-HTTP-03 | Happy Path | Configurar y ejecutar request PUT — verificar actualización | 🔴 | ⬜ |
| TC-NODE-HTTP-04 | Happy Path | Configurar y ejecutar request DELETE — verificar eliminación | 🔴 | ⬜ |
| TC-NODE-HTTP-05 | Happy Path | Configurar headers personalizados (Authorization, Content-Type, etc.) | 🔴 | ⬜ |
| TC-NODE-HTTP-06 | Negativo | Request a URL inválida — verificar que activa el edge de error | 🟠 | ⬜ |
| TC-NODE-HTTP-07 | Negativo | Request que retorna 4xx/5xx — verificar que el status y body del error llegan al output de error | 🟠 | ⬜ |
| TC-NODE-HTTP-08 | Edge Case | Request con timeout largo — verificar comportamiento cuando el server no responde | 🟡 | ⬜ |
| TC-NODE-HTTP-09 | Edge Case | Usar expresiones dinámicas `{{$N.field}}` en la URL y body — verificar resolución correcta | 🔴 | ⬜ |

---

## Notas de Automatización
- Requiere un mock server o endpoint de testing para simular respuestas
- Verificar los 4 métodos HTTP principales
- Las expresiones dinámicas se resuelven con `libs.ReplaceReferences` antes de ejecutar
- 9 test cases
