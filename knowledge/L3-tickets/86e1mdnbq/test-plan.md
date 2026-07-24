# Test Plan — 86e1mdnbq (IONF-1049)
# Sincronización de Logs con R2

> Generado: 2026-06-23
> Track: Deployment (modo directo — sin Discovery previo)
> QA Engineer: Steve Nina
> Developer: Alex Chura
> Sprint: Sprint 3 (6/22 - 7/5)

---

## 1. Objetivo del Testing

Verificar que la primera fase de sincronización de artefactos de ejecución de Flows hacia R2 funciona correctamente:
- Los SQLite generados se encolan correctamente en `storage_sync_jobs`
- El cron los sube a R2 en los estados correctos
- La sincronización no rompe el almacenamiento local ni el historial de ejecuciones
- El sistema es resiliente ante fallos de R2 (reintentos)
- El control de activación (`STORAGE_SYNC_ENABLED`) funciona

---

## 2. Scope del Testing

### In scope
- Encolado de SQLite de ejecuciones (dev y live)
- Encolado de archivos generados por nodos (kind=file)
- Proceso de sincronización con R2 (cron SyncAll)
- Limpieza de archivos locales post-sync
- Comportamiento con R2 no disponible (reintentos)
- Flag de activación `STORAGE_SYNC_ENABLED`
- Tabla `storage_sync_jobs` (schema, estados, transiciones)
- Regresión: ejecución de flows (dev y live) sin errores
- Regresión: historial de ejecuciones

### Out of scope
- Consumo de logs/archivos desde R2 (segunda fase — ticket aparte)
- Sincronización del almacén de datos persistente
- Sincronización de sesiones de IA
- UI de gateway-ion (no hay cambios de frontend en este ticket)
- Automation E2E (no hay cambios de UI)

---

## 3. Precondiciones de Testing

### Configuración de entorno
```
# Variables obligatorias
STORAGE_SYNC_ENABLED=true
STORAGE_SYNC_CRON_EXPRESSION=* * * * *     # cada minuto para agilizar testing
STORAGE_SYNC_MAX_ATTEMPTS=5
R2_SYNC_BUCKET_NAME=<bucket-de-sync>

# Credenciales R2 (ya configuradas en el servidor)
R2_ACCOUNT_ID=<...>
R2_ACCESS_KEY_ID=<...>
R2_SECRET_ACCESS_KEY=<...>

# Retención local
DEV_DB_RETENTION_DAYS=7
DEV_DB_CLEAN_CRON_EXPRESSION=0 0 * * *
```

### Setup previo
1. ✅ Migración ejecutada: `php artisan migrate` — tabla `storage_sync_jobs` creada
2. ✅ Backend Go actualizado a rama `IONF-1049` (o `DEVELOPMENT` con MR mergeado)
3. ✅ Acceso a DBeaver (SSH tunnel PostgreSQL) para verificaciones de BD
4. ✅ Acceso a Cloudflare R2 dashboard para verificar archivos subidos
5. ✅ Flow de prueba disponible en entorno de staging
6. ✅ Flow con nodo Request que genera archivo binario disponible

---

## 4. Bloques de Ejecución

### Bloque 0 — Pre-flight (5 min)
**Objetivo**: Confirmar que el entorno está listo

- [ ] Verificar tabla `storage_sync_jobs` existe (TC-017)
- [ ] Verificar variables de entorno configuradas
- [ ] Confirmar acceso al bucket R2

### Bloque 1 — Smoke Tests (15 min)
**Objetivo**: Confirmar funcionalidad base sin regresión

- [ ] TC-014 — Ejecutar flow dev → completa sin errores
- [ ] TC-015 — Ejecutar flow live → completa sin errores
- [ ] TC-016 — Historial de ejecuciones visible y correcto

> 🔴 Si algún smoke test falla → PARAR y reportar regresión crítica.

### Bloque 2 — Happy Path (30 min)
**Objetivo**: Verificar el flujo principal de sync

- [ ] TC-001 — SQLite ejecución dev → `storage_sync_jobs` con status=pending
- [ ] TC-002 — SQLite ejecución live → `storage_sync_jobs` con status=pending
- [ ] TC-003 — Archivo binario (nodo Request) → `storage_sync_jobs` kind=file
- [ ] TC-004 — Cron sync: pending → uploading → done, archivo en R2
- [ ] TC-005 — Segundo ciclo cron: local eliminado, status=cleaned

### Bloque 3 — Edge Cases (30 min)
**Objetivo**: Verificar comportamiento en condiciones especiales

- [ ] TC-006 — Sync no interrumpe ejecución en curso
- [ ] TC-007 — Sync ocurre SOLO post-cierre del SQLite
- [ ] TC-008 — R2 no disponible → reintentos correctos
- [ ] TC-009 — Estructura de paths en R2 = estructura local
- [ ] TC-010 — Multi-tenant: artefactos aislados por company

### Bloque 4 — Negativos (20 min)
**Objetivo**: Verificar que el sistema rechaza correctamente escenarios no deseados

- [ ] TC-011 — STORAGE_SYNC_ENABLED=false → sin jobs creados
- [ ] TC-012 — No sync mid-execution
- [ ] TC-013 — Max attempts alcanzados → status=failed, local preservado

### Bloque 5 — DB Evidence
**Objetivo**: Documentar evidencia de BD para el reporte

- [ ] Screenshot de `storage_sync_jobs` con registros en diferentes estados
- [ ] Ejecutar queries de verificación definidas en test-matrix.md
- [ ] Screenshot de R2 bucket con archivos subidos

---

## 5. Criterios de Aceptación del Testing

### Condiciones para ✅ Approved
- TC-001 a TC-004 pasan (happy path core funciona)
- TC-014 y TC-015 pasan (sin regresión en ejecución de flows)
- TC-016 pasa (historial intacto)
- TC-017 pasa (migración correcta)
- TC-011 pasa (flag de desactivación funciona)

### Condiciones para ❌ Rejected
- Cualquier falla en TC-014 o TC-015 (regresión en ejecución de flows)
- TC-001 o TC-002 fallan (encolado no funciona)
- TC-004 falla (sync no ocurre)
- TC-010 falla (cross-tenant leakage)
- TC-011 falla (no se puede desactivar la sync)

### Condiciones para ⚠️ Approved con observaciones
- TC-005 falla (limpieza no funciona, pero sync sí)
- TC-008 falla parcialmente (reintentos no exactamente como esperado)
- TC-009 falla (estructura de paths difiere, pero funcionalidad core OK)

---

## 6. Estimación de Tiempo

| Bloque | Duración estimada |
|--------|------------------|
| Bloque 0 — Pre-flight | 5 min |
| Bloque 1 — Smoke Tests | 15 min |
| Bloque 2 — Happy Path | 30 min |
| Bloque 3 — Edge Cases | 30 min |
| Bloque 4 — Negativos | 20 min |
| Bloque 5 — DB Evidence | 15 min |
| **Total** | **~1h 55 min** |

---

## 7. Riesgos y Mitigaciones

| Riesgo | Mitigación |
|--------|-----------|
| Cron muy lento (cada hora en producción) | Usar `STORAGE_SYNC_CRON_EXPRESSION=* * * * *` en testing o ejecutar SyncAll manualmente |
| Acceso a R2 sin permisos | Confirmar credenciales y bucket antes de iniciar |
| Flow de prueba no disponible | Tener un flow simple (ej. nodo HTTP) listo para ejecutar |
| Multi-tenant requiere 2 cuentas | Usar cuenta Company + cuenta de otra company configurada en staging |

---

## 8. Artefactos de Salida

Al finalizar, deberán existir en `L3-tickets/86e1mdnbq/`:
- [ ] `test-matrix.md` actualizada con resultados (✅/❌/⏭️)
- [ ] `test-matrix.csv` actualizada
- [ ] `code-review-qa.md` (se generará en Paso 2 del runbook)
- [ ] `qa-report.md` (se generará tras el veredicto del QA Engineer)
- [ ] `screenshots/` con evidencia de BD y R2 (si aplica)
