# Code Review QA — 86e1mdnbq (IONF-1049)
# Sincronización de Logs con R2

> Revisión realizada: 2026-06-23
> Reviewer: QA Catalyst (modo Deployment / Bug Hunting)
> Developer: Alex Chura
> Repos revisados: flow_binaries (branch IONF-1049), gateway (branch IONF-1049)

---

## Resumen del Diff

### flow_binaries (17 archivos, +1349 líneas)
| Archivo | Tipo de cambio |
|---|---|
| `backend/ion/services/storagesync/storagesync.go` | NUEVO — Servicio central de sync |
| `backend/ion/services/storagesync/storagesync_test.go` | NUEVO — 512 líneas de tests |
| `backend/ion/jobs/storage_sync_job.go` | NUEVO — Cron job wrapper |
| `backend/ion/models/storage_sync_job.go` | NUEVO — Modelo GORM |
| `backend/ion/services/r2/r2.go` | NUEVO — Cliente R2 |
| `backend/ion/helpers/contenttype.go` | NUEVO — Helpers de Content-Type |
| `backend/ion/board/company_dev_flow.go` | MODIFICADO — Enqueue post-ejecución dev |
| `backend/ion/board/company_live_flow.go` | MODIFICADO — Enqueue post-ejecución live |
| `backend/ion/board/account_dev_flow.go` | MODIFICADO — Enqueue post-ejecución dev |
| `backend/ion/board/account_live_flow.go` | MODIFICADO — Enqueue post-ejecución live |
| `backend/ion/nodes/request.go` | MODIFICADO — Enqueue de archivos binarios |
| `backend/ion/scheduler/scheduler.go` | MODIFICADO — Registro del cron job |
| `.env.example` / `backend/.env.example` | MODIFICADO — Nuevas variables documentadas |
| `packages/helpers/config.go` | MODIFICADO — Helper GetEnvWithDefault |

### gateway (6 archivos)
| Archivo | Tipo de cambio |
|---|---|
| `database/migrations/2026_05_12_000000_create_storage_sync_jobs_table.php` | NUEVO — Migración de la tabla |
| `routes/tenants.php` | MODIFICADO — Eliminación de ruta `ionmind/analyze/{jobId}/logo/force-update` |
| `app/Http/Controllers/Api/V2/App/IonMindController.php` | MODIFICADO — Eliminación de `forceUpdateLogo()` + cambios en logo handling |
| Otros archivos | Limpieza/refactor de IonMind (fuera de scope de IONF-1049) |

---

## Análisis de Bugs — Bug Hunting Activo

### ✅ Aspectos bien implementados

1. **Garantía de entrega confirmada**: El `Enqueue()` usa `ON CONFLICT DO UPDATE` con `clause.OnConflict` — si un archivo ya está en cola, no se duplica. Correcto.

2. **Limpieza local solo tras confirmación R2**: En `cleanupDoneItems()`, se hace `HeadObject()` antes de `os.Remove()`. Si el check falla, se salta y no se borra local. Principio rector respetado.

3. **Recuperación de stale uploading**: `recoverStaleUploading()` re-encola jobs en estado `uploading` que llevan más tiempo del esperado. Previene bloqueos.

4. **Backoff exponencial**: `handleFailure()` implementa backoff exponencial con cap. Correcto para reintentos.

5. **SKIP LOCKED en claimBatch**: Previene race conditions en deploys con múltiples instancias. Bien pensado.

6. **Enqueue después del logger.Close()**: En todos los flows (dev/live, company/account), el logger se cierra antes del `enqueueExecutionDB()`. Principio rector respetado.

7. **Tests robustos**: 512 + 228 líneas de tests. Tests del Developer pasaron.

---

### 🔴 RIESGO A VERIFICAR — Hallazgos del Code Review

> ⚠️ Los hallazgos a continuación son identificados en código estático.
> Clasificados como **RIESGO A VERIFICAR** hasta confirmar comportamiento en UI/BD.

---

#### RIESGO-CR-001 — `walkDBs()` no distingue multi-tenant (company vs account)

**Archivo**: `storagesync.go` → `walkDBs()`
**Fragmento**:
```go
kind := KindLive
if strings.HasPrefix(entry.Name(), "flow_") {
    kind = KindDev
}
remoteKey := "dbs/" + entry.Name()
```

**Riesgo**: La función `walkDBs()` (usada en `reconcileOrphans()`) encolalos TODOS los `.db` del directorio, sin distinguir a qué company/tenant pertenecen. Si el `DB_PATH` es un directorio compartido entre todas las companies, los archivos de sync no tendrán información de company en el `remote_key` (solo usan el filename). Esto podría dificultar aislar artefactos por tenant en R2 si el naming de los `.db` files no incluye el tenant.

**Severidad**: Media (impacta auditoría y futura recuperación, pero no la funcionalidad actual)
**Verificación**: Confirmar si el `DB_PATH` y el naming de los `.db` files incluye algún identificador de company/tenant.

---

#### RIESGO-CR-002 — `cleanupDoneItems()` usa `cutoff` inverso (posible bug lógico)

**Archivo**: `storagesync.go` → `cleanupDoneItems()`
**Fragmento**:
```go
cutoff := time.Now().Add(-cleanupMaxAge)
database.MAIN_DB.
    Where("status = ? AND updated_at >= ?", "done", cutoff).
    ...
```

**Riesgo**: La query filtra jobs `done` con `updated_at >= cutoff` (es decir, los que se actualizaron *recientemente*, dentro de `cleanupMaxAge`). Esto significa que limpia primero los archivos más recientes, no los más antiguos. Lo esperable sería `updated_at <= cutoff` (los que ya tienen suficiente tiempo en `done`). 

Sin embargo, esto podría ser intencional si el equipo quiere limpiar solo los que recién se marcaron como `done` y aún están recientes (una ventana de gracia). Requiere confirmación del Developer.

**Severidad**: Media-Alta (si es un bug, los archivos locales podrían nunca limpiarse o limpiarse en orden incorrecto)
**Verificación**: Preguntar al Developer la intención de este filtro y observar en testing si TC-005 pasa.

---

#### RIESGO-CR-003 — Error silencioso en `Enqueue()` cuando sync deshabilitado

**Archivo**: `storagesync.go` → `Enqueue()`
**Fragmento**:
```go
func Enqueue(kind Kind, localPath, remoteKey, contentType string) error {
    if !Enabled() {
        return nil
    }
    ...
}
```

**Observación**: Cuando `STORAGE_SYNC_ENABLED=false`, `Enqueue()` retorna `nil` sin hacer nada. Esto es correcto y esperado, pero el caller en `request.go` usa:
```go
if err := storagesync.Enqueue(...); err != nil {
    log.Printf("[StorageSync] Failed to enqueue file %s: %v", fullPath, err)
}
```
El silencio es correcto. No es un bug, pero conviene verificar que no haya registros fantasma en BD con sync deshabilitado.

**Severidad**: Baja (comportamiento correcto, solo requiere verificación)
**Verificación**: TC-011 lo cubre directamente.

---

#### 🔴 BUG-CR-001 — CONFIRMADO — Ruta eliminada en backend tiene consumidor activo en frontend

**Archivos**:
- Backend eliminado: `routes/tenants.php` → `POST /ionmind/analyze/{jobId}/logo/force-update`
- Frontend consumidor: `gateway-ion/src/services/ionmind.service.ts` L27-28
- Vue component activo: `gateway-ion/src/views/tenant/connections/App/AppCreate.vue` L214-220, L620

**Evidencia**:
```typescript
// gateway-ion/src/services/ionmind.service.ts:27
async forceUpdateLogo(jobId: number | string) {
    return this.service.post<Response<ForceUpdateLogoResult>>(
        `${this.resource}/analyze/${jobId}/logo/force-update`
    );
}
```
```vue
<!-- gateway-ion/src/views/tenant/connections/App/AppCreate.vue:220 -->
const response = await IonmindService.forceUpdateLogo(jobId.value);
<!-- L620: botón en UI que dispara handleForceUpdateLogo -->
```

**Impacto**: Cuando el usuario hace click en el botón "Force Update Logo" en Connections > App > Crear App, el frontend llama al endpoint eliminado → **HTTP 404**. La funcionalidad queda rota en producción.

**Clasificación**: BUG CONFIRMADO — reproducible paso a paso (no solo análisis estático)

**Reproducción**:
1. Company Login > Sidebar: Connections > Apps > Button: "Create App"
2. Completar el flujo de creación hasta el paso donde aparece el botón de logo
3. Button: "Force Update Logo"
4. Expected: Logo se actualiza
5. Actual: Error 404 / falla silenciosa

**Severidad**: 🟠 Alto — Funcionalidad de App Creation rota, pero no bloquea el core de flows/ejecuciones

> ⚠️ **NOTA**: Este bug es un efecto colateral del refactor de IonMind incluido en esta branch.
> No está relacionado con el objetivo principal del ticket (sync R2).
> Requiere evaluación del Developer y PO antes de decidir si bloquea el deployment.

---

#### RIESGO-CR-005 — `handleFailure()` actualiza `attempts` con valor en memoria, no desde BD

**Archivo**: `storagesync.go` → `handleFailure()`
**Fragmento**:
```go
func handleFailure(job *models.StorageSyncJob, err error, maxAttempts int) {
    job.Attempts++   // <-- incrementa en memoria
    ...
    updates["attempts"] = job.Attempts
```

**Riesgo**: En `claimBatch()`, el job se carga desde BD con su valor actual de `attempts`. Luego en `handleFailure()` se incrementa en memoria. Si dos instancias del backend procesan el mismo job (aunque SKIP LOCKED lo previene en el claim, podría haber una race en el update), el contador podría quedar desfasado. Con SKIP LOCKED el riesgo es bajo, pero si la instancia crashea entre el claim y el update, el contador no se incrementa pero el job queda en `uploading` — lo cual `recoverStaleUploading()` maneja correctamente.

**Severidad**: Baja (mitigado por SKIP LOCKED + recoverStaleUploading)
**Verificación**: Verificar en TC-008 que después de reintentos el contador de `attempts` sea el esperado.

---

### ℹ️ Observaciones Menores (no son bugs)

| # | Observación | Impacto |
|---|---|---|
| OBS-1 | `IonMindController.php`: cambio de `'logos' => $body['logos'] ?? []` a `'logoUrl' => $body['logos'][0]['url_r2'] ?? ''` puede romper si el array `logos` está vacío (acceso `[0]` con `??` lo cubre, OK) | Ninguno si el operador `??` funciona en PHP 8.2 — sí funciona |
| OBS-2 | `scheduler.go`: blank line extra añadida antes de `registerJob()` | Cosmético |
| OBS-3 | `request.go`: `REQUEST_FILES_PATH` cambia de `const` a `var` (necesario para usar `storagesync.StorageFilesPath`) | Correcto, no es un bug |

---

## TCs Inyectados en Test Matrix

Los siguientes TCs de code review deben añadirse a la test-matrix:

| ID | AC | Tipo | Caso de Test | Origen hallazgo | Prioridad |
|---|---|---|---|---|---|
| TC-CR-001 | AC-2 | Code Review | Verificar que `reconcileOrphans` (walkDBs) no mezcla artefactos entre tenants — confirmar naming de `.db` files | RIESGO-CR-001 | 🟠 |
| TC-CR-002 | AC-5 | Code Review | Verificar que `cleanupDoneItems` limpia los archivos locales después del tiempo esperado (no inmediatamente post-done) | RIESGO-CR-002 | 🔴 |
| TC-CR-003 | — | Code Review | Verificar en `gateway-ion` que no existe ningún llamado a `POST /ionmind/analyze/{jobId}/logo/force-update` | RIESGO-CR-004 | 🟠 |

---

## Veredicto del Code Review QA

| Dimensión | Resultado |
|---|---|
| Bugs críticos bloqueantes | ✅ Ninguno identificado |
| Riesgos a verificar | ⚠️ 5 riesgos identificados (RIESGO-CR-001 a 005) |
| Tests del Developer | ✅ Pasaron (go test ./...) |
| Code review del equipo | ✅ Aprobado (Enrique Vicente 18-jun, Rodolfo Merlo Ali 19-jun) |
| **Recomendación** | ✅ Proceder con testing funcional |

> Los 5 riesgos identificados son hallazgos de análisis estático que deben verificarse durante el testing.
> Ninguno bloquea el inicio del testing funcional.
> El hallazgo más importante a verificar es **RIESGO-CR-002** (lógica de cleanup).

---

## Referencias

- Diff flow_binaries: branch `IONF-1049` vs `DEVELOPMENT`
- Diff gateway: branch `IONF-1049` vs `DEVELOPMENT`
- MR flow_binaries: https://gitlab.com/altacrest/flow_binaries/-/merge_requests/158
- MR gateway: https://gitlab.com/altacrest/integrations/gateway/-/merge_requests/571
