# Test Matrix — [TICKET-ID]

> Generada por `test-docs/document` (modo matrix)
> Fecha: [fecha]
> Módulo: [nombre del módulo]

## Resumen

| Métrica | Valor |
|---------|-------|
| Total de casos | |
| Happy path | |
| Edge cases | |
| Negativos | |
| Regresión | |
| Code Review | |
| Automatizables | |
| Cobertura de AC | /[total AC] |

---

## Test Matrix

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-001 | | AC-1 | Happy Path | | | Company Login > Sidebar: [Módulo] > ... | | 🔴 | ⬜ | ⬜ Pendiente |
| TC-002 | | AC-1 | Edge Case | | | Company Login > Sidebar: [Módulo] > ... | | 🟠 | ⬜ | ⬜ Pendiente |
| TC-003 | | AC-1 | Negativo | | | Company Login > Sidebar: [Módulo] > ... | | 🟡 | ⬜ | ⬜ Pendiente |

### Formato de Pasos (OBLIGATORIO)

> Los pasos DEBEN usar formato **breadcrumb** explícito.
> Esto permite que cualquier persona (IA o humano) pueda reproducir el caso sin ambigüedad.

**Formato**: `[Rol] Login > Sidebar: [Módulo] > [Acción] > [Sub-acción] > [Verificación]`

| Elemento | Formato | Ejemplo |
|----------|---------|--------|
| Login | `Company Login` / `Admin Login` | `Company Login` |
| Sidebar | `Sidebar: [nombre]` | `Sidebar: Boards` |
| URL | `Navigate: /ruta` | `Navigate: /workflows` |
| Click | `Click [elemento]` | `Click [Flow "Mi Flow"]` |
| Botón | `Button: [nombre]` | `Button: "Save"` |
| Drawer | `Drawer: [nombre]` | `Drawer: Code Config` |
| Fill | `Fill [campo]: [valor]` | `Fill "Name": "Test"` |
| Select | `Select [campo]: [opción]` | `Select "Language": Python` |
| Verify | `Verify: [qué]` | `Verify: Toast "Created"` |
| Wait | `Wait: [qué]` | `Wait: Agent response` |

❌ `Abrir flow | Click en Code | Verificar drawer`
✅ `Company Login > Sidebar: Boards > Click [Flow "Test"] > Canvas: Click [Code Node] > Drawer: Code Config > Verify: Button "Save" visible`

### Leyenda de Tipos
- **Happy Path**: Flujo principal esperado
- **Edge Case**: Caso borde identificado
- **Negativo**: Caso que NO debería funcionar (validación)
- **Code Review**: Caso inyectado desde el code review QA (TC-CR-xxx)
- **Regresión**: Caso que verifica que funcionalidad existente no se rompió

### Leyenda de Prioridad
- 🔴 Crítico — Testear siempre, bloqueante si falla
- 🟠 Alto — Testear siempre, puede ser bloqueante
- 🟡 Medio — Testear si hay tiempo
- 🟢 Bajo — Nice to have

### Leyenda de Estado
- ⬜ Pendiente
- ✅ Pasó
- ❌ Falló
- ⏭️ Saltado (con justificación)

---

## Casos de Regresión

| ID | Módulo impactado | Caso de regresión | Por qué podría romperse | Prioridad | Estado |
|----|-----------------|-------------------|------------------------|-----------|--------|
| REG-001 | | | | 🟠 | ⬜ |

---

## Queries de Verificación BD

> ⚠️ Queries basadas EXCLUSIVAMENTE en schemas de migraciones.
> NUNCA inventar campos, tablas ni relaciones.
> SIEMPRE incluir referencia a la migración fuente como comentario.

```sql
-- Fuente: ../gateway/database/migrations/<archivo>.php
-- Tabla: <tabla> | Columnas verificadas: <lista>

-- TC-001: [Descripción de la verificación]
-- BD: PostgreSQL
SELECT <columnas> FROM <tabla> WHERE <condición>;
-- Esperado: [descripción del resultado esperado]

-- TC-003: [Verificación de caso negativo]
SELECT COUNT(*) FROM <tabla> WHERE <condición>;
-- Esperado: 0
```

---

## Notas

- Queries ejecutadas en DBeaver (PostgreSQL via SSH tunnel)
- Para datos de ejecución de nodos, verificar via UI de historial de ejecuciones (SQLite)
- Fuentes de schema: `../gateway/database/migrations/*.php` y `../flow_binaries/migrations/*.sql`
