# Test Matrix — 86e1mdnbq (IONF-1049)

> Generada para Deployment track (sin Discovery previo — AC tomados de instrucciones QA del Developer)
> Fecha: 2026-06-23
> Módulo: executions (flow_binaries) + gateway (BD)
> Developer: Alex Chura | QA Engineer: Steve Nina

## Resumen

| Métrica | Valor |
|---------|-------|
| Total de casos | 20 |
| Happy path | 5 |
| Edge cases | 5 |
| Negativos | 3 |
| Regresión | 4 |
| Code Review | 3 (inyectados desde code-review-qa.md) |
| Automatizables | 0 (no UI gateway-ion) |
| Cobertura de AC | 5/5 AC funcionales |

---

## Acceptance Criteria (extraídos del ticket)

| ID | Criterio |
|----|----------|
| AC-1 | Al finalizar un flow, el SQLite generado se sube a R2 correctamente |
| AC-2 | El archivo en R2 queda identificable para su consumo posterior |
| AC-3 | Ejecuciones de archivos adicionales (nodo Request con binario) también se sincronizan |
| AC-4 | La sincronización no rompe el flujo actual de guardado local |
| AC-5 | Los trabajos de sincronización transicionan: `pending → uploading → done → cleaned` |

---

## Test Matrix

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-001 | executions/R2 | AC-1, AC-5 | Happy Path | SQLite de ejecución dev se encola en `storage_sync_jobs` al finalizar | `STORAGE_SYNC_ENABLED=true`, migración ejecutada, flujo dev configurado | Company Login > Sidebar: Boards > Ejecutar flow en modo Dev > Esperar finalización > Verify DB: `storage_sync_jobs` WHERE kind='live' | Registro creado con `status=pending` y `kind='live'` o `kind='file'` según tipo | 🔴 | ❌ No (DB check) | ⬜ Pendiente |
| TC-002 | executions/R2 | AC-1, AC-5 | Happy Path | SQLite de ejecución live se encola en `storage_sync_jobs` al finalizar | `STORAGE_SYNC_ENABLED=true`, flow activo en modo Production | Company Login > Sidebar: Boards > Trigger flow en modo Live (webhook/schedule) > Esperar finalización > Verify DB: `storage_sync_jobs` | Registro creado con `status=pending`, `kind='live'` | 🔴 | ❌ No (DB check) | ⬜ Pendiente |
| TC-003 | executions/R2 | AC-3, AC-5 | Happy Path | Archivo binario de nodo Request se encola en `storage_sync_jobs` | `STORAGE_SYNC_ENABLED=true`, flow con nodo Request que guarda archivo binario | Company Login > Sidebar: Boards > Ejecutar flow con nodo Request (descarga binario) > Esperar finalización > Verify DB: `storage_sync_jobs` WHERE kind='file' | Registro creado con `status=pending`, `kind='file'`, `local_path` válido | 🔴 | ❌ No (DB check) | ⬜ Pendiente |
| TC-004 | executions/R2 | AC-1, AC-2, AC-5 | Happy Path | Cron de sincronización sube archivos pendientes a R2 | Registros en `storage_sync_jobs` con `status=pending` | Esperar ejecución del cron (o ejecutar SyncAll manualmente) > Verify DB: status=done > Verify R2: archivo presente en bucket | Trabajos pasan de `pending → uploading → done`. Archivo visible en R2 bucket | 🔴 | ❌ No (cron + R2 check) | ⬜ Pendiente |
| TC-005 | executions/R2 | AC-5 | Happy Path | Segunda ejecución del cron limpia el archivo local | Registro en `status=done` del ciclo anterior | Esperar siguiente ejecución del cron > Verify: local_path ya no existe > Verify DB: status=cleaned | Archivo local eliminado, estado cambia a `cleaned` | 🟠 | ❌ No (cron + FS check) | ⬜ Pendiente |
| TC-006 | executions/R2 | AC-4 | Edge Case | Sincronización activa no interrumpe ejecución de flow en curso | `STORAGE_SYNC_ENABLED=true`, cron corriendo | Ejecutar flow mientras cron activo > Verify: ejecución completa sin errores | Flow finaliza correctamente. Sin errores de concurrencia o lock en SQLite | 🔴 | ❌ No | ⬜ Pendiente |
| TC-007 | executions/R2 | AC-1 | Edge Case | Sincronización ocurre SOLO después del cierre final del SQLite | Flow en ejecución | Ejecutar flow largo > Verify DB: job no aparece hasta que flow finaliza completamente | `storage_sync_jobs` record aparece únicamente tras el cierre final del registro | 🔴 | ❌ No | ⬜ Pendiente |
| TC-008 | executions/R2 | AC-1, AC-5 | Edge Case | R2 no disponible temporalmente — job se reintenta | `STORAGE_SYNC_ENABLED=true`, R2 con credenciales inválidas temporalmente | Ejecutar flow > Esperar cron > Verify DB: attempts incrementa, status no queda en error hasta max_attempts | Registros reintentan hasta `STORAGE_SYNC_MAX_ATTEMPTS=5`. No se pierde información | 🔴 | ❌ No | ⬜ Pendiente |
| TC-009 | executions/R2 | AC-2 | Edge Case | Estructura de paths en R2 coincide con estructura local de `storage/` | Archivos subidos a R2 | Verificar en R2 bucket el path del archivo subido vs `local_path` en DB | El `remote_key` en R2 mantiene la misma estructura que el directorio `storage/` local | 🟠 | ❌ No (R2 check) | ⬜ Pendiente |
| TC-010 | executions/R2 | AC-5 | Edge Case | Multi-tenant: ejecuciones de diferentes companies no se mezclan | 2 companies activas con flows | Ejecutar flows de company A y company B > Verify DB + R2: paths correctamente segmentados por company | Cada company tiene sus artefactos en paths separados. Sin cross-tenant leakage | 🔴 | ❌ No | ⬜ Pendiente |
| TC-011 | executions/R2 | AC-4 | Negativo | Con `STORAGE_SYNC_ENABLED=false` — no se crean jobs de sincronización | `STORAGE_SYNC_ENABLED=false` | Company Login > Ejecutar flow > Finalizar > Verify DB: `storage_sync_jobs` | No se crea ningún registro en `storage_sync_jobs`. Archivos siguen en local normalmente | 🔴 | ❌ No (DB check) | ⬜ Pendiente |
| TC-012 | executions/R2 | AC-1 | Negativo | SQLite no se sube antes de estar completamente cerrado | Flow en medio de ejecución | Interrumpir o monitorear mid-execution > Verify DB: no hay job pending hasta finalización | No existe job de sync hasta que el SQLite está completamente cerrado y persistido | 🟠 | ❌ No | ⬜ Pendiente |
| TC-013 | executions/R2 | AC-5 | Negativo | Job que supera `STORAGE_SYNC_MAX_ATTEMPTS` queda en estado `failed` | Configurar credenciales R2 inválidas, `max_attempts=5` | Ejecutar flow > Esperar 5 reintentos del cron > Verify DB: status=failed | Registro marcado como `failed` después de 5 intentos. No se elimina el archivo local | 🟠 | ❌ No | ⬜ Pendiente |
| TC-014 | boards | AC-4 | Regresión | Ejecución de flow dev completa sin errores (funcionalidad base intacta) | Flow existente en modo Dev | Company Login > Sidebar: Boards > Ejecutar flow dev completo > Verify: resultado correcto en cada nodo | Flow dev ejecuta sin errores. Historial de ejecución disponible. Sin regresión en el motor | 🔴 | ❌ No | ⬜ Pendiente |
| TC-015 | boards | AC-4 | Regresión | Ejecución de flow live (production) completa sin errores | Flow activo en modo Production | Trigger flow live > Esperar finalización > Sidebar: Executions > Verify: registro de ejecución presente | Flow live completa. Historial registrado correctamente. Sin regresión | 🔴 | ❌ No | ⬜ Pendiente |
| TC-016 | executions | AC-4 | Regresión | Historial de ejecuciones sigue mostrando resultados correctos | Ejecuciones previas y nuevas | Company Login > Sidebar: Executions > Verify: lista de ejecuciones carga > Click en ejecución > Verify: detalle de nodos disponible | Vista de historial funciona. Detalles de nodos visibles. Sin regresión post-sync | 🟠 | ❌ No | ⬜ Pendiente |
| TC-017 | gateway/BD | AC-1 | Regresión | Migración de `storage_sync_jobs` aplicada correctamente en gateway | `php artisan migrate` ejecutado | Verify DB: tabla `storage_sync_jobs` existe con columnas: id, kind, local_path, remote_key, content_type, status, attempts, last_error | Tabla existe con schema correcto. Sin errores de migración | 🔴 | ❌ No (DB check) | ⬜ Pendiente |
| TC-CR-001 | executions/R2 | AC-2 | Code Review | Verificar que `reconcileOrphans` (walkDBs) no mezcla artefactos entre tenants — confirmar naming de `.db` files incluye identificador de company/tenant | `STORAGE_SYNC_ENABLED=true`, 2 companies con flows ejecutados | Ejecutar flows de company A y B > Ejecutar reconcileOrphans (o esperar cron reconcile) > Verify DB: remote_key incluye identificador de tenant > Verify R2: paths separados por tenant | Los `.db` files tienen naming que permite distinguir por tenant. Sin mezcla en R2 | 🟠 | ❌ No | ⬜ Pendiente |
| TC-CR-002 | executions/R2 | AC-5 | Code Review | Verificar que `cleanupDoneItems` limpia archivos DESPUÉS del tiempo esperado (no inmediatamente post-done) — verificar lógica de `updated_at >= cutoff` | Registros en `status=done` | Esperar tiempo de cleanupMaxAge + observar cuándo se hace la limpieza > Verify: el local file se elimina después de cleanupMaxAge, no antes | Los archivos locales se eliminan en el timing correcto según `cleanupMaxAge`. La lógica `updated_at >= cutoff` opera como el Developer diseñó | 🔴 | ❌ No | ⬜ Pendiente |
| TC-CR-003 | connections | — | Code Review | 🔴 BUG-CR-001 CONFIRMADO — Botón "Force Update Logo" en Connections > App > Crear App llama a endpoint eliminado (`POST /ionmind/analyze/{jobId}/logo/force-update`) | Company Login, flujo de creación de App activo | Company Login > Sidebar: Connections > Apps > Button: "Create App" > Completar flujo hasta botón de logo > Button: "Force Update Logo" > Verify: respuesta del endpoint | Expected: Logo se actualiza. Actual: HTTP 404 — endpoint eliminado en backend pero consumidor activo en gateway-ion/src/views/tenant/connections/App/AppCreate.vue L220 + L620 | 🟠 | ❌ No | ⬜ Pendiente |

---

## Casos de Regresión

| ID | Módulo impactado | Caso de regresión | Por qué podría romperse | Prioridad | Estado |
|----|-----------------|-------------------|------------------------|-----------|--------|
| REG-001 | Boards/Executions | Ejecución de flow dev sin errores | El proceso de sync post-ejecución podría introducir locks o errores en el cierre del SQLite | 🔴 | ⬜ |
| REG-002 | Boards/Executions | Ejecución de flow live sin errores | El encolado asíncrono podría interferir con el cierre del SQLite en modo background | 🔴 | ⬜ |
| REG-003 | Executions | Vista de historial de ejecuciones | Si el path del SQLite cambia al sincronizar, la lectura del historial podría romperse | 🟠 | ⬜ |
| REG-004 | Gateway/BD | Migración de storage_sync_jobs | La migración podría fallar o dejar el schema incompleto | 🔴 | ⬜ |

---

## Queries de Verificación BD

> ⚠️ Queries basadas EXCLUSIVAMENTE en la tabla `storage_sync_jobs` confirmada por el Developer.
> SIEMPRE incluir referencia a la migración fuente.

```sql
-- Fuente: ../gateway/database/migrations/ (nueva migración de IONF-1049)
-- Tabla: storage_sync_jobs | Columnas: id, kind, local_path, remote_key, content_type, status, attempts, last_error

-- TC-001/TC-002: Verificar encolado de SQLite de ejecución
-- BD: PostgreSQL
SELECT id, kind, local_path, remote_key, status, attempts
FROM storage_sync_jobs
ORDER BY id DESC
LIMIT 20;
-- Esperado: registros con status='pending', kind='live' (para flows) o kind='file' (para archivos)

-- TC-004: Verificar sincronización exitosa
SELECT id, kind, local_path, remote_key, status, attempts
FROM storage_sync_jobs
WHERE status = 'done'
ORDER BY id DESC
LIMIT 10;
-- Esperado: registros con status='done', remote_key con path en R2

-- TC-005: Verificar limpieza post-sync
SELECT id, kind, local_path, status
FROM storage_sync_jobs
WHERE status = 'cleaned'
ORDER BY id DESC
LIMIT 10;
-- Esperado: registros con status='cleaned'

-- TC-011: Verificar que con SYNC_ENABLED=false no hay registros nuevos
SELECT COUNT(*) FROM storage_sync_jobs
WHERE created_at > NOW() - INTERVAL '5 minutes';
-- Esperado: 0 (si se ejecutó con STORAGE_SYNC_ENABLED=false)

-- TC-013: Verificar registro fallido por max_attempts
SELECT id, kind, status, attempts, last_error
FROM storage_sync_jobs
WHERE status = 'failed';
-- Esperado: attempts=5, last_error con mensaje descriptivo

-- TC-017: Verificar existencia de tabla y schema
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'storage_sync_jobs'
ORDER BY ordinal_position;
-- Esperado: columnas id, kind, local_path, remote_key, content_type, status, attempts, last_error
```

---

## Notas

- Queries ejecutadas en DBeaver (PostgreSQL via SSH tunnel)
- Verificación de R2: acceder al bucket configurado en `R2_SYNC_BUCKET_NAME` via Cloudflare dashboard
- Verificación de archivo local: SSH al servidor para confirmar existencia/eliminación del path en `local_path`
- La tabla `storage_sync_jobs` fue confirmada por el Developer (screenshot en ClickUp)
- Tests TC-014 al TC-016 (Regresión) deben ejecutarse ANTES de verificar la sync para confirmar baseline

---

## Historial de Estado

| Fecha | Acción | Por |
|-------|--------|-----|
| 2026-06-23 | Test matrix creada — Deployment directo (sin Discovery previo) | QA Catalyst |
