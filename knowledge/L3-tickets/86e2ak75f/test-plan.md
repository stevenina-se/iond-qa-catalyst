# Test Plan — 86e2ak75f

> Standardize Execution UI & Build Execution Replay Engine

## Información del Ticket

| Campo | Valor |
|-------|-------|
| ID | [86e2ak75f](https://app.clickup.com/t/86e2ak75f) |
| Título | Standardize Execution UI & Build Execution Replay Engine |
| Módulo | Executions (principal), Boards (secundario) |
| QA Engineer | Steve Nina |
| Fecha del plan | 2026-08-27 |

## Resumen

| Métrica | Valor |
|---------|-------|
| Total de casos | 35 |
| Smoke tests | 4 |
| Happy path | 10 |
| Edge cases | 11 |
| Negativos | 6 |
| Regresión | 4 |
| Automatizables | 18 |
| Tiempo estimado | ~165 min (~2h 45min) |
| Artefactos de Discovery | risk-triage.md ✅, ac-consolidated.md ✅, test-matrix.md ✅ |

---

## Orden de Ejecución

### BLOQUE 1 — SMOKE TESTS (ejecutar primero, si alguno falla → escalar)

```
□ SM-001: Vista de ejecuciones carga correctamente — Prioridad: 🔴
□ SM-002: Replay de ejecución carga el canvas — Prioridad: 🔴
□ SM-003: Acceso al historial desde lista de boards — Prioridad: 🔴
□ SM-004: Acceso al historial desde editor de board — Prioridad: 🔴
```

> ⚠️ Si algún smoke falla → PARAR y escalar al Developer. No continuar con el resto.

### BLOQUE 2 — HAPPY PATH (verificar flujo principal)

```
□ TC-001: Consistencia visual Dev vs Live — Prioridad: 🔴
□ TC-002: Inspección de nodo con I/O — Prioridad: 🔴
□ TC-003: Nodos con diferentes estados (éxito/error/omitido) — Prioridad: 🔴
□ TC-004: URL compartible — Prioridad: 🔴
□ TC-006: Snapshot muestra board al momento de ejecución — Prioridad: 🔴
□ TC-005: Metadata de modo y trigger — Prioridad: 🟠
□ TC-009: Botón de ejecutar se bloquea — Prioridad: 🟠
□ TC-007: Ejecución expirada muestra metadata — Prioridad: 🟠
□ TC-008: Recuperación de SQLite desde R2 — Prioridad: 🟠
□ TC-010: Botón de descarga de registro — Prioridad: 🟡
```

### BLOQUE 3 — EDGE CASES (verificar bordes)

```
□ EC-007: Concurrencia — dos usuarios ejecutan mismo board — Prioridad: 🔴
□ EC-001: Board con muchos nodos (50+) — Prioridad: 🟠
□ EC-002: Board eliminado después de ejecución — Prioridad: 🟠
□ EC-003: Ejecución con nodo que falló en primer paso — Prioridad: 🟠
□ EC-004: Distinción expiró vs no disponible — Prioridad: 🟠
□ EC-006: SQLite no disponible en R2 ni local — Prioridad: 🟠
□ EC-008: Ejecución que tarda mucho — Prioridad: 🟠
□ EC-005: Ejecución en el límite exacto de 7 días — Prioridad: 🟡
□ EC-009: Board sin ejecuciones — Prioridad: 🟡
□ EC-010: Nodo con payload I/O grande (>1MB) — Prioridad: 🟡
□ EC-011: Mezcla de ejecuciones nuevas y legacy — Prioridad: 🟡
```

### BLOQUE 4 — NEGATIVOS (verificar que NO se pueda romper)

```
□ NEG-001: URL de ejecución de otra company — Prioridad: 🔴
□ NEG-005: Doble clic rápido en ejecutar — Prioridad: 🔴
□ NEG-006: Ejecutar board con ejecución activa — Prioridad: 🔴
□ NEG-002: URL de ejecución inexistente — Prioridad: 🟠
□ NEG-003: Usuario sin permiso READ_EXECUTION — Prioridad: 🟠
□ NEG-004: Eliminar sin permiso DELETE_EXECUTION — Prioridad: 🟠
```

### BLOQUE 5 — REGRESIÓN (verificar que no rompimos nada)

```
□ REG-001: Lista de boards sigue funcionando — Prioridad: 🔴
□ REG-002: Editor de board sigue funcionando — Prioridad: 🔴
□ REG-003: Ejecución de flow funciona correctamente — Prioridad: 🔴
□ REG-004: Dashboard muestra métricas de ejecuciones — Prioridad: 🟡
```

### BLOQUE 6 — DB EVIDENCE (queries de verificación)

```
□ DB-001: Schema de executions — verificar nuevas columnas (modo, trigger)
□ DB-002: Aislamiento multi-tenant — ejecuciones filtradas por account_id
□ DB-003: No hay ejecuciones huérfanas sin estado final
□ DB-004: Estados de nodos en SQLite (pending/processing/success/error)
□ DB-005: Integridad de edges — nodos source/target existen
□ DB-006: Logs de ejecución registrados correctamente
□ DB-007: Tabla de snapshot del flow existe en SQLite
```

---

## Datos Necesarios

| Dato | Cómo obtenerlo | Notas |
|------|---------------|-------|
| Usuario Company (tenant) | `.env` → `IONFLOW_COMPANY_USERNAME` | Rol principal de testing |
| Usuario Admin | `.env` → `IONFLOW_ADMIN_USERNAME` | Para tests de permisos |
| Usuario sin permisos | Crear o usar existente sin `READ_EXECUTION` | Para NEG-003, NEG-004 |
| Board con ejecuciones recientes | Crear o usar board existente, ejecutar | Para SM-001, SM-002, TC-001 a TC-004 |
| Board con ejecución Dev + Live | Ejecutar mismo board en ambos modos | Para TC-001 |
| Board con nodos que fallan | Configurar nodo con datos inválidos | Para TC-003, EC-003 |
| Board complejo (50+ nodos) | Crear o usar board existente complejo | Para EC-001 |
| Ejecución > 7 días | Esperar o verificar si hay historial antiguo | Para TC-007, EC-005 |
| Ejecución legacy (pre-deploy) | Verificar si existen en el entorno | Para EC-004, EC-011 |
| Segunda company | Crear o usar company existente | Para NEG-001 |

---

## Criterios de Aprobación/Rechazo

### APROBACIÓN ✅
- ✅ TODOS los smoke tests pasan (SM-001 a SM-004)
- ✅ TODOS los happy path pasan (TC-001 a TC-010)
- ✅ Al menos 80% de los edge cases pasan (≥ 9 de 11)
- ✅ TODOS los negativos pasan (NEG-001 a NEG-006)
- ✅ TODOS los casos de regresión pasan (REG-001 a REG-004)
- ✅ DB evidence confirma integridad de datos

### RECHAZO ❌
- ❌ Algún smoke test falla → rechazo inmediato
- ❌ Happy path falla → rechazo
- ❌ Caso negativo falla (el sistema se puede romper) → rechazo
- ❌ Caso de regresión crítico falla → rechazo con análisis de impacto
- ❌ DB evidence muestra datos corruptos → rechazo
- ❌ Multi-tenant violado (NEG-001 falla) → rechazo CRÍTICO

### APROBACIÓN CON OBSERVACIONES ⚠️
- ⚠️ Edge case falla pero no es bloqueante → aprobar con bug registrado
- ⚠️ Problema visual menor → aprobar con observación
- ⚠️ AC-12 (botón descarga) no implementado → aprobar si es solo sugerencia del review
- ⚠️ AC 5-7 (concurrencia/lifecycle) parciales si se resuelven en IONF-1248

---

## Estimación de Tiempo

| Bloque | Casos | Tiempo estimado |
|--------|-------|-----------------|
| Smoke tests | 4 | ~15 min |
| Happy path | 10 | ~50 min |
| Edge cases | 11 | ~45 min |
| Negativos | 6 | ~25 min |
| Regresión | 4 | ~15 min |
| DB evidence | 7 | ~15 min |
| **Total** | **42** (35 TCs + 7 DBs) | **~165 min (~2h 45min)** |

> Nota: El tiempo puede variar según la disponibilidad de datos de prueba (ejecuciones > 7 días, ejecuciones legacy, segunda company).

---

## Dependencias y Riesgos del Plan

| Dependencia | Impacto si no está disponible |
|-------------|-------------------------------|
| Ejecuciones > 7 días | No se puede testear AC-3, EC-005 → diferir o crear datos |
| Ejecuciones legacy (pre-deploy) | No se puede testear AC-4, AC-10, EC-011 → puede no existir en staging |
| Segunda company | No se puede testear NEG-001 → crítico para seguridad multi-tenant |
| Board con 50+ nodos | No se puede testear EC-001 → crear o simplificar |
| SQLite en R2 (no local) | No se puede testear TC-008, EC-006 → verificar con Developer |

---

## Estado

⏳ Plan creado — esperando inicio de ejecución (Deployment Track)
