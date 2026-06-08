# Módulo: [NOMBRE DEL MÓDULO]

> Conocimiento de nivel 2 para el módulo **[nombre]** de Ionflow.
> Última actualización: [fecha]

## Overview

Breve descripción de qué hace este módulo en el contexto de Ionflow.

---

## Frontend (gateway-ion)

### Rutas
| Ruta | Vista | Descripción |
|------|-------|-------------|
| `/path` | `ViewName.vue` | Descripción |

### Componentes clave
| Componente | Ubicación | Props/Eventos |
|-----------|-----------|---------------|
| `ComponentName.vue` | `src/components/...` | Props: ... / Eventos: ... |

### Stores (Pinia)
| Store | Ubicación | Estado que gestiona |
|-------|-----------|---------------------|
| `useModuleStore` | `src/stores/...` | ... |

---

## API (flow_binaries / gateway)

### Endpoints
| Método | Path | Repo | Descripción | Auth requerida |
|--------|------|------|-------------|----------------|
| GET | `/api/...` | flow_binaries | Listar... | ✅ |
| POST | `/api/...` | flow_binaries | Crear... | ✅ |

### Payloads (request/response)
```json
// POST /api/...
// Request:
{
  "field": "value"
}

// Response:
{
  "id": 1,
  "field": "value"
}
```

---

## Canvas (webcomponents-flow)

> Completar solo si el módulo involucra componentes del canvas de nodos.

### Componentes
| Componente | Ubicación | Descripción |
|-----------|-----------|-------------|
| `NodeComponent` | `src/components/...` | ... |

---

## Database

> Schema reconstruido desde archivos de migración.

### Tablas principales
| Tabla | Descripción |
|-------|-------------|
| `table_name` | ... |

### Columnas clave
| Tabla | Columna | Tipo | Nullable | Descripción |
|-------|---------|------|----------|-------------|
| `table_name` | `id` | `uuid` | NO | PK |

### Relaciones (Foreign Keys)
| Tabla origen | Columna | Tabla destino | Columna destino |
|-------------|---------|--------------|-----------------|
| `table_a` | `ref_id` | `table_b` | `id` |

### Queries de verificación frecuentes
```sql
-- Verificar existencia de registro
SELECT * FROM table_name WHERE id = '<id>';

-- Verificar estado
SELECT id, status FROM table_name WHERE id = '<id>';

-- Verificar integridad referencial
SELECT a.*, b.id as related
FROM table_a a
LEFT JOIN table_b b ON a.ref_id = b.id
WHERE a.id = '<id>';
```

### Estados y transiciones
```
[estado_1] → [estado_2] → [estado_3]
                  ↓
             [estado_error]
```

---

## Test Data

### Datos necesarios para testing
| Dato | Valor/Cómo obtenerlo | Notas |
|------|---------------------|-------|
| Usuario de prueba | ... | ... |

### Seeders conocidos
- (listar si existen)

---

## Tests E2E Existentes (bot-test)

| Test file | Cobertura | Estado |
|-----------|-----------|--------|
| `tests/IONFLOW/.../spec.ts` | Happy path de... | ✅ Activo |

### Page Objects
| Page Object | Ubicación | Selectores principales |
|------------|-----------|----------------------|
| `module.page.ts` | `tests/IONFLOW/pages/` | ... |

---

## Lógica Backend (flow_binaries)

> Información técnica del backend Go relevante para testing.
> Fuente: documentación técnica de `../flow_binaries/docs/`

### Servicios involucrados
| Service | Archivo | Función |
|---------|---------|---------|
| `ServiceName` | `backend/ion/services/xxx.go` | Descripción |

### Modelo de ejecución
> ¿Cómo participa este módulo en el ciclo de ejecución de flows?

- Patrón de BD: Global (Account) / Tenant (Company) / SQLite (Ejecuciones)
- Multi-tenant: ¿Usa `CompanySchema()`? ¿Filtra por `company_id`?
- Nodos relacionados: [lista de nodos que este módulo afecta]

### Archivos centinela (cambios aquí impactan este módulo)
| Repo | Archivo | Razón |
|------|---------|-------|
| flow_binaries | `backend/ion/services/xxx.go` | Service principal |
| flow_binaries | `backend/ion/controllers/xxx.go` | Controller API |
| flow_binaries | `backend/ion/models/xxx.go` | Modelo de datos |
| gateway-ion | `src/views/xxx/xxx.vue` | Vista principal |

---

## Impacto Cruzado

> ¿Qué otros módulos se ven afectados si este módulo cambia?
> Usar para Bug Hunting en code-review/review.md

### Módulos que este módulo afecta
| Módulo destino | Componente afectado | Tipo de impacto | Ejemplo |
|---------------|--------------------|-----------------|---------| 
| [otro módulo] | [tabla/endpoint/componente] | Datos / UI / API | Si cambio X, podría romper Y |

### Módulos que afectan a este módulo
| Módulo origen | Componente | Tipo de impacto | Ejemplo |
|--------------|------------|-----------------|---------| 
| [otro módulo] | [tabla/endpoint/componente] | Datos / UI / API | Si X cambia, este módulo se rompe |

### Tablas compartidas
| Tabla | Módulos que la usan | Riesgo si cambia |
|-------|---------------------|------------------|
| `table_name` | [módulo A], [módulo B] | [qué se rompe] |

---

## Edge Cases Conocidos

| ID | Descripción | Descubierto en | Severidad |
|----|-------------|----------------|-----------|
| EC-001 | ... | Release X.X | 🟠 Alto |

---

## Historial de Cambios Post-Release

| Fecha | Release | Cambios relevantes |
|-------|---------|-------------------|
| YYYY-MM-DD | vX.X | Descripción del cambio |
