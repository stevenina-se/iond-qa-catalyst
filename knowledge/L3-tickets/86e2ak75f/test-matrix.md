# Test Matrix — 86e2ak75f

> Standardize Execution UI & Build Execution Replay Engine

## Resumen

- **Total de casos**: 35
- **Happy path**: 10
- **Edge cases**: 11
- **Negativos**: 6
- **Regresión**: 4
- **Smoke**: 4
- **Automatizables**: 18 (de los 31 funcionales)

---

## Test Matrix

### SMOKE TESTS

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| SM-001 | Executions | AC-2 | Smoke | Vista de ejecuciones carga correctamente | Board con al menos 1 ejecución reciente | Company Login > Sidebar: Execution History > Verify: tabla de ejecuciones visible con datos | La tabla de ejecuciones se muestra con al menos 1 registro | 🔴 | ✅ | ⬜ |
| SM-002 | Executions | AC-2 | Smoke | Replay de ejecución carga el canvas | Ejecución reciente (< 7 días) con snapshot | Company Login > Sidebar: Execution History > Click [Ejecución reciente] > Verify: canvas read-only visible con nodos coloreados | Canvas muestra el flow ejecutado con nodos coloreados por estado | 🔴 | ❌ | ⬜ |
| SM-003 | Boards | AC-2a | Smoke | Acceso al historial desde lista de boards | Al menos 1 board existente | Company Login > Sidebar: Boards > Click [Menú contextual de board] > Click [Execution History] > Verify: vista de ejecuciones del board | Navega a la vista de ejecuciones filtrada por ese board | 🔴 | ✅ | ⬜ |
| SM-004 | Boards | AC-2b | Smoke | Acceso al historial desde editor de board | Board abierto en editor | Company Login > Sidebar: Boards > Click [Board] > Click [Tab: Ejecuciones] > Verify: historial del board | Muestra el historial de ejecuciones del board abierto | 🔴 | ✅ | ⬜ |

### HAPPY PATH

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-001 | Executions | AC-1 | Happy Path | Consistencia visual Dev vs Live | Board ejecutado en Dev y Live | Company Login > Sidebar: Execution History > Click [Ejecución Dev] > Verify: estructura UI > Navigate: back > Click [Ejecución Live] > Verify: misma estructura UI | Ambas vistas usan los mismos componentes, estilos y jerarquía visual | 🔴 | ❌ | ⬜ |
| TC-002 | Executions | AC-2 | Happy Path | Inspección de nodo con I/O | Ejecución reciente con nodos procesados | Company Login > Sidebar: Execution History > Click [Ejecución] > Canvas: Click [Nodo exitoso (verde)] > Panel: Verify: Input JSON visible > Verify: Output JSON visible | Panel muestra estructura exacta de datos de entrada y salida del nodo | 🔴 | ❌ | ⬜ |
| TC-003 | Executions | AC-2 | Happy Path | Nodos con diferentes estados | Ejecución con nodos success, error y omitido | Company Login > Sidebar: Execution History > Click [Ejecución con errores] > Canvas: Verify: nodos verdes (éxito) + rojos (error) + grises (omitido) | Cada nodo muestra indicador visual correcto según su resultado | 🔴 | ❌ | ⬜ |
| TC-004 | Executions | AC-2c | Happy Path | URL compartible | Ejecución abierta | Company Login > Sidebar: Execution History > Click [Ejecución] > Copy URL > Open new tab > Paste URL > Verify: misma ejecución | La URL directa carga la misma ejecución. Botón "atrás" funciona | 🔴 | ✅ | ⬜ |
| TC-005 | Executions | AC-8 | Happy Path | Metadata de modo y trigger | Ejecución manual en Dev + ejecución schedule en Live | Company Login > Sidebar: Execution History > Verify: columna modo muestra "Dev"/"Live" > Verify: columna trigger muestra "Manual"/"Schedule" | Las columnas de modo y trigger muestran valores correctos | 🟠 | ✅ | ⬜ |
| TC-006 | Executions | AC-9 | Happy Path | Snapshot muestra board al momento de ejecución | Board ejecutado, luego modificado (agregar/eliminar nodo) | Company Login > Ejecutar board > Sidebar: Boards > Modificar board (agregar nodo) > Sidebar: Execution History > Click [Ejecución anterior] > Canvas: Verify: muestra versión ANTERIOR del board (sin el nodo nuevo) | El replay muestra el board como era al ejecutarse, no la versión actual | 🔴 | ❌ | ⬜ |
| TC-007 | Executions | AC-3 | Happy Path | Ejecución expirada muestra metadata | Ejecución con > 7 días de antigüedad | Company Login > Sidebar: Execution History > Click [Ejecución antigua (> 7 días)] > Verify: muestra estado, duración, errores generales > Verify: NO muestra canvas replay > Verify: aviso de expiración visible | Muestra solo metadata con aviso de que el detalle expiró | 🟠 | ✅ | ⬜ |
| TC-008 | Executions | AC-11 | Happy Path | Recuperación de SQLite desde R2 | Ejecución cuyo SQLite está solo en R2 (no local) | Company Login > Sidebar: Execution History > Click [Ejecución con SQLite en R2] > Wait: descarga > Verify: canvas replay visible con datos de nodos | El sistema descarga desde R2, cachea, y muestra el replay correctamente | 🟠 | ❌ | ⬜ |
| TC-009 | Executions | AC-6 | Happy Path | Botón de ejecutar se bloquea | Board listo para ejecutar | Company Login > Sidebar: Boards > Click [Board] > Button: "Ejecutar" > Verify: botón se bloquea inmediatamente > Verify: indicador visual de ejecución en proceso | El botón se deshabilita y muestra indicador antes de respuesta del servidor | 🟠 | ✅ | ⬜ |
| TC-010 | Executions | AC-12 | Happy Path | Botón de descarga de registro | Historial con ejecuciones | Company Login > Sidebar: Execution History > Button: "Descargar" > Verify: se descarga archivo con registro de ejecuciones | Se obtiene un archivo descargable con el registro | 🟡 | ✅ | ⬜ |

### EDGE CASES

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| EC-001 | Executions | AC-2 | Edge Case | Board con muchos nodos (50+) | Board complejo con 50+ nodos ejecutado | Company Login > Sidebar: Execution History > Click [Ejecución de board complejo] > Canvas: Verify: todos los nodos visibles y navegables | El canvas renderiza correctamente, con scroll o zoom para navegar | 🟠 | ❌ | ⬜ |
| EC-002 | Executions | AC-9 | Edge Case | Board eliminado después de ejecución | Board ejecutado y luego eliminado | Company Login > Sidebar: Execution History > Click [Ejecución de board eliminado] > Verify: replay funciona con el snapshot guardado | El snapshot permite reconstruir el board aunque ya no exista | 🟠 | ❌ | ⬜ |
| EC-003 | Executions | AC-2 | Edge Case | Ejecución con nodo que falló en primer paso | Board con nodo trigger que falla inmediatamente | Company Login > Sidebar: Execution History > Click [Ejecución fallida en primer nodo] > Canvas: Verify: primer nodo en rojo, resto en gris | Canvas muestra correctamente que solo el primer nodo se ejecutó (y falló) | 🟠 | ❌ | ⬜ |
| EC-004 | Executions | AC-4 | Edge Case | Distinción expiró vs no disponible | Ejecución > 7 días + ejecución legacy sin snapshot | Company Login > Sidebar: Execution History > Click [Ejecución expirada] > Verify: mensaje "expiró el [fecha]" > Navigate: back > Click [Ejecución legacy] > Verify: mensaje "no disponible" (sin mencionar expiración) | Mensajes diferenciados correctamente según la causa | 🟠 | ✅ | ⬜ |
| EC-005 | Executions | AC-3 | Edge Case | Ejecución en el límite exacto de 7 días | Ejecución de exactamente 7 días de antigüedad | Company Login > Sidebar: Execution History > Click [Ejecución de 7 días exactos] > Verify: ¿muestra detalle completo o metadata? | Comportamiento consistente en el boundary (definir si 7 días = expirado o no) | 🟡 | ✅ | ⬜ |
| EC-006 | Executions | AC-11 | Edge Case | SQLite no disponible en R2 ni local | Ejecución cuyo SQLite no existe en ningún lado | Company Login > Sidebar: Execution History > Click [Ejecución sin SQLite] > Verify: mensaje comprensible (no error técnico) | Mensaje claro de que el detalle no está disponible, sin error técnico | 🟠 | ✅ | ⬜ |
| EC-007 | Executions | AC-5 | Edge Case | Concurrencia — dos usuarios intentan ejecutar mismo board | Board sin ejecución activa, 2 sesiones abiertas | Sesión 1: Button "Ejecutar" > Sesión 2: Button "Ejecutar" > Verify: solo 1 ejecución se crea > Verify: segunda sesión recibe mensaje de rechazo | Solo una ejecución se registra. La segunda recibe mensaje claro | 🔴 | ❌ | ⬜ |
| EC-008 | Executions | AC-7 | Edge Case | Ejecución que tarda mucho | Board con nodo que hace request a API lenta | Company Login > Sidebar: Boards > Click [Board] > Button: "Ejecutar" > Wait: timeout > Verify: ejecución termina en estado final (error/timeout) | La ejecución NUNCA queda en estado "en curso" indefinidamente | 🟠 | ❌ | ⬜ |
| EC-009 | Boards | AC-2a | Edge Case | Board sin ejecuciones | Board recién creado sin ejecuciones | Company Login > Sidebar: Boards > Click [Menú contextual board nuevo] > Click [Execution History] > Verify: empty state con mensaje y acción para ejecutar | Mensaje amigable + botón/acción para ejecutar el board | 🟡 | ✅ | ⬜ |
| EC-010 | Executions | AC-2 | Edge Case | Nodo con payload I/O grande (>1MB) | Ejecución con nodo cuyo output es muy grande | Company Login > Sidebar: Execution History > Click [Ejecución] > Canvas: Click [Nodo con payload grande] > Panel: Verify: datos mostrados (truncados o con opción de ver completo) | Los datos se muestran recortados con opción de ver completos | 🟡 | ❌ | ⬜ |
| EC-011 | Executions | AC-10 | Edge Case | Mezcla de ejecuciones nuevas y legacy | Historial con ejecuciones pre y post deploy | Company Login > Sidebar: Execution History > Verify: ejecuciones nuevas tienen opción de replay > Verify: ejecuciones legacy muestran solo metadata | La lista diferencia visualmente las que tienen replay disponible | 🟡 | ✅ | ⬜ |

### NEGATIVOS

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| NEG-001 | Executions | AC-2c | Negativo | URL de ejecución de otra company | 2 companies con ejecuciones | Company A Login > Sidebar: Execution History > Copy URL de ejecución > Logout > Company B Login > Paste URL > Verify: acceso denegado o "no encontrada" | El sistema NO muestra la ejecución de otra company. Mensaje comprensible | 🔴 | ✅ | ⬜ |
| NEG-002 | Executions | AC-2c | Negativo | URL de ejecución inexistente | N/A | Company Login > Navigate: /executions/999999999 > Verify: error comprensible (no error técnico) | Mensaje "ejecución no encontrada", no un error 500 o pantalla en blanco | 🟠 | ✅ | ⬜ |
| NEG-003 | Executions | Permisos | Negativo | Usuario sin permiso READ_EXECUTION | Usuario sin permiso de ejecución | Login con usuario sin permiso > Sidebar: Verify: opción de Execution History no visible o desactivada | El acceso no aparece o aparece desactivado con explicación | 🟠 | ✅ | ⬜ |
| NEG-004 | Executions | Permisos | Negativo | Eliminar sin permiso DELETE_EXECUTION | Usuario con READ pero sin DELETE | Company Login (sin DELETE) > Sidebar: Execution History > Click [Ejecución] > Verify: opción de eliminar no visible | No se puede eliminar sin el permiso adecuado | 🟠 | ✅ | ⬜ |
| NEG-005 | Executions | AC-6 | Negativo | Doble clic rápido en ejecutar | Board listo | Company Login > Sidebar: Boards > Click [Board] > Double-click rápido "Ejecutar" > Verify: solo 1 ejecución creada | El doble clic no genera una segunda ejecución | 🔴 | ✅ | ⬜ |
| NEG-006 | Executions | AC-5 | Negativo | Ejecutar board con ejecución activa | Board con ejecución en curso | Company Login > Sidebar: Boards > Click [Board con ejecución activa] > Button: "Ejecutar" > Verify: rechazado con mensaje "ya hay una ejecución en curso" | La segunda ejecución es rechazada con mensaje claro | 🔴 | ✅ | ⬜ |

### REGRESIÓN

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| REG-001 | Boards | N/A | Regresión | Lista de boards sigue funcionando | Boards existentes | Company Login > Sidebar: Boards > Verify: lista de boards carga correctamente > Verify: CRUD de boards funciona | La adición del menú contextual no rompió la lista de boards | 🔴 | ✅ | ⬜ |
| REG-002 | Boards | N/A | Regresión | Editor de board sigue funcionando | Board existente | Company Login > Sidebar: Boards > Click [Board] > Verify: canvas del editor carga > Verify: se pueden agregar/editar nodos | El tab de ejecuciones no interfiere con el editor | 🔴 | ❌ | ⬜ |
| REG-003 | Executions | N/A | Regresión | Ejecución de flow funciona correctamente | Board con nodos configurados | Company Login > Sidebar: Boards > Click [Board] > Button: "Ejecutar" > Wait: ejecución completa > Verify: resultado correcto | La ejecución del flow no fue afectada por los cambios de UI | 🔴 | ✅ | ⬜ |
| REG-004 | Dashboard | N/A | Regresión | Dashboard muestra métricas de ejecuciones | Ejecuciones existentes | Company Login > Sidebar: Dashboard > Verify: métricas/stats de ejecuciones correctas | Los cambios en la tabla de ejecuciones no rompieron las métricas | 🟡 | ✅ | ⬜ |

---

## Queries de Verificación BD

### PostgreSQL (tabla `executions`)

```sql
-- Fuente: ../gateway/database/migrations/2025_07_23_145811_create_table_executions.php
-- Tabla: executions | Columnas verificadas: id, name, label, status, content, execution_time, executable_type, executable_id, account_id, created_at

-- DB-001: Verificar que ejecución nueva tiene campos de modo y trigger
-- NOTA: Las columnas de modo (live/dev) y trigger type fueron agregadas por el Developer.
-- Verificar que existen en el schema actual.
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'executions' 
ORDER BY ordinal_position;

-- DB-002: Verificar aislamiento multi-tenant
SELECT e.id, e.name, e.status, e.account_id 
FROM executions e 
WHERE e.account_id = '<account_id>' 
ORDER BY e.created_at DESC 
LIMIT 10;

-- DB-003: Verificar que no hay ejecuciones huérfanas (sin estado final)
SELECT e.id, e.name, e.status, e.created_at 
FROM executions e 
WHERE e.status NOT IN ('completed', 'error', 'stopped', 'success') 
AND e.created_at < NOW() - INTERVAL '1 hour';
```

### SQLite (por ejecución — archivo `<flowId>.db`)

```sql
-- Fuente: ../flow_binaries/core/db/database.go (migrateSchema)
-- Tablas verificadas: nodes, edges, outputs, logs

-- DB-004: Verificar estados de nodos en una ejecución
SELECT id, type, status, data_type, result_type 
FROM nodes;

-- DB-005: Verificar que edges conectan nodos existentes
SELECT e.id, e.source, e.target, 
  (SELECT COUNT(*) FROM nodes n WHERE n.id = e.source) as source_exists,
  (SELECT COUNT(*) FROM nodes n WHERE n.id = e.target) as target_exists
FROM edges e;

-- DB-006: Verificar logs de ejecución
SELECT id, type, content, created_at 
FROM logs 
ORDER BY created_at;

-- DB-007: Verificar que la tabla de snapshot del flow existe
-- NOTA: Nueva tabla agregada por el Developer (2026-08-04).
-- Nombre de tabla pendiente de confirmar en el código actual.
SELECT name FROM sqlite_master WHERE type='table';
```
