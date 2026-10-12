# Test Plan — 86e1wfhcq (IONF-1085)
## API REST de workspace/company de IOND (FASE 2)

> Generado: 2026-10-08
> Basado en: risk-triage.md, ac-consolidated.md, test-matrix.md
> QA Engineer: Steve Nina
> Developer: Rodolfo Merlo Ali

---

## Contexto

| Campo | Valor |
|-------|-------|
| Ticket | IONF-1085 — API REST workspace/company FASE 2 |
| Tipo | New Feature (8 subtareas funcionales) |
| Riesgo | 🔴 Crítico |
| Test Cases | 87 (28 HP + 22 EC + 16 NEG + 10 SEC + 11 REG) |
| Automatizables (API) | 72 / 87 (83%) |
| Repos | flow_binaries, gateway-ion, gateway |
| Branch | IONF-1085 |

---

## Pre-requisitos de Deploy (obligatorios antes de testear)

> ⚠️ Sin estos pasos, las pruebas no pueden ejecutarse.

| # | Acción | Repo | Comando/Detalle |
|---|--------|------|-----------------|
| 1 | Correr migraciones globales | Gateway | `php artisan migrate` → crea `workspace_tokens` |
| 2 | Cargar permisos nuevos | Gateway | `execute-board`, `execute-app`, `create-cron`, `read-cron`, `update-cron`, `delete-cron`, `publish-app`, `execute-pdf-template` |
| 3 | Asignar permisos a usuarios existentes | Gateway | Comandos proporcionados por Dev |
| 4 | Cifrar common existente | Gateway | Comando idempotente (proporcionado por Dev) |
| 5 | Instalar dependencias Go | flow_binaries | `go mod download` (jsonschema/v6, packages/validation) |
| 6 | Recompilar backend | flow_binaries | Build Go |
| 7 | Variables de entorno (opcionales) | flow_binaries | `EXECUTION_RETENTION_DAYS=7`, `WORKSPACE_TOKEN_LIMIT=3` |
| 8 | Build frontend | gateway-ion | Build Vue |
| 9 | Post-deploy: borrar rutas deprecated | Gateway | Rutas `@deprecated IONF-1287/1288` (wizard NO se borra) |

---

## Datos de Prueba Necesarios

| Dato | Requisito | Para |
|------|-----------|------|
| Company A (principal) | Con usuario autenticado, boards, connectors, data stores, PDF templates | Todas las pruebas |
| Company B (aislamiento) | Con recursos diferentes para cross-company | TC-006, TC-012, TC-021, TC-029 |
| PAT con todos los scopes | Creado desde Settings → API Tokens | Happy paths |
| PAT sin scope específico | Para cada permiso individual | Negativos 403 |
| Board con ejecución rápida | Termina en <5 min | TC-025 |
| Board con ejecución lenta | Termina en >5 min | TC-026 |
| Board con connection cruzada | Connection de otro connector | TC-030 |
| Connector con common OAuth | Con client_secret en common | TC-061, TC-087 |
| Connector con method "post" | En minúsculas en DB | TC-062 |
| Store con >1000 registros | Para test de límite búsqueda | TC-073 |
| Template PDF activo e inactivo | Para test de execute | TC-078, TC-080 |
| Boards con IDs 1, 10, 12, 100 | Para test bug LIKE | TC-048, TC-049 |
| Demo requests | `gateway/workspace-token.http` | Referencia para todas las APIs |

---

## Orden de Ejecución

### FASE 1 — SMOKE TESTS Y FUNDACIÓN (ejecutar primero — si falla, escalar)

> Si alguno de estos falla, el resto del testing es irrelevante.

| □ | TC | Caso | Prioridad |
|---|-----|------|-----------|
| □ | TC-003 | PAT aceptado como bearer en workspace/me | 🔴 |
| □ | TC-004 | Doble llave scope+TPerm → 200 | 🔴 |
| □ | TC-012 | Cross-company ID → 404 uniforme | 🔴 |
| □ | TC-009 | App token rechazado en workspace | 🔴 |

### FASE 2 — HAPPY PATH FUNCIONAL (flujo principal por subtarea)

| □ | TC | Caso | Subtarea |
|---|-----|------|----------|
| □ | TC-001 | Crear PAT con scopes | IONF-1279 |
| □ | TC-002 | Token muestra una sola vez | IONF-1279 |
| □ | TC-015 | Listar connections filtro app_name | IONF-1284 |
| □ | TC-017 | Listar connectors instalados | IONF-1284 |
| □ | TC-019 | Ver contrato de action | IONF-1284 |
| □ | TC-023 | Listar boards | IONF-1285 |
| □ | TC-025 | Ejecutar board → execution_id | IONF-1285 |
| □ | TC-028 | Trigger type = api | IONF-1285 |
| □ | TC-033 | Listar executions con filtros | IONF-1286 |
| □ | TC-036 | Ejecutar action → execution + consumo | IONF-1286 |
| □ | TC-041 | Listar webhooks | IONF-1287 |
| □ | TC-042 | Toggle webhook enable/disable | IONF-1287 |
| □ | TC-045 | Pausar schedule | IONF-1287 |
| □ | TC-051 | Crear connector API | IONF-1288 |
| □ | TC-055 | Validate + Publish connector | IONF-1288 |
| □ | TC-063 | CRUD structures | IONF-1291 |
| □ | TC-066 | CRUD registros | IONF-1291 |
| □ | TC-074 | CRUD PDF template | IONF-1292 |
| □ | TC-076 | Export/Import PDF template | IONF-1292 |
| □ | TC-078 | Imprimir PDF → consumo correcto | IONF-1292 |

### FASE 3 — SEGURIDAD Y AISLAMIENTO

| □ | TC | Caso | Prioridad |
|---|-----|------|-----------|
| □ | TC-006 | Usuario removido → PAT rechazado | 🔴 |
| □ | TC-013 | ID malformado → mismo 404 | 🔴 |
| □ | TC-014 | Account-Id header ignorado | 🔴 |
| □ | TC-021 | Connection otra company → 404 | 🔴 |
| □ | TC-029 | Board otra company → 404 | 🔴 |
| □ | TC-058 | Common cifrado + enmascarado | 🔴 |
| □ | TC-071 | Store ID no-UUID → validado (SQL injection) | 🔴 |

### FASE 4 — EDGE CASES

| □ | TC | Caso | Prioridad |
|---|-----|------|-----------|
| □ | TC-005 | Quitar TPerm → 403 → devolver → 200 | 🔴 |
| □ | TC-010 | Token limit #4 con limit=3 | 🟠 |
| □ | TC-026 | Board >5 min → 202 | 🟠 |
| □ | TC-030 | Connection de otro connector → error pre-proveedor | 🔴 |
| □ | TC-035 | Execution vieja fuera de retención | 🟡 |
| □ | TC-044 | Deshabilitar webhook → no llama proveedor | 🟠 |
| □ | TC-046 | Pausa schedule sobrevive guardar board | 🟠 |
| □ | TC-059 | Guardar sin tocar secreto → conserva | 🟠 |
| □ | TC-064 | Structure todos los tipos | 🟠 |
| □ | TC-067 | Key repetida → 409 | 🟠 |
| □ | TC-069 | Campo extra: API 422 vs board guarda | 🔴 |
| □ | TC-079 | Render falla → no cobra | 🔴 |

### FASE 5 — NEGATIVOS (el sistema NO debe romperse)

| □ | TC | Caso | Prioridad |
|---|-----|------|-----------|
| □ | TC-007 | PAT expirado → 401 | 🔴 |
| □ | TC-008 | PAT revocado → 401 | 🔴 |
| □ | TC-027 | Sin execute-board → 403 | 🔴 |
| □ | TC-038 | Action sin Connection-Id → 400 sin cobrar | 🔴 |
| □ | TC-039 | Sin execute-app → 403 | 🟠 |
| □ | TC-047 | Schedule vencido → 409 | 🟡 |
| □ | TC-052 | Name duplicado → 422 | 🟠 |
| □ | TC-053 | Action inválida → 422 con rutas | 🟠 |
| □ | TC-056 | Sin publish-app → 403 | 🟠 |
| □ | TC-057 | Borrar en uso → 409 con lista | 🔴 |
| □ | TC-065 | Structure tipo desconocido → 422 | 🟡 |
| □ | TC-068 | Required nested → 422 | 🟠 |
| □ | TC-070 | Borrar store en uso → 409 | 🟠 |
| □ | TC-075 | Schema pdfme inválido → 422 | 🟠 |
| □ | TC-080 | Template inactive → 409 | 🟡 |
| □ | TC-081 | Sin execute-pdf-template → 403 | 🟠 |

### FASE 6 — REGRESIÓN (no rompimos nada existente)

| □ | TC | Caso | Prioridad |
|---|-----|------|-----------|
| □ | TC-040 | Devapp recurso sin envoltorio | 🟠 |
| □ | TC-048 | Bug LIKE: board 1 vs board 12 | 🔴 |
| □ | TC-049 | Bug LIKE: IDs similares 1/10/100 | 🔴 |
| □ | TC-061 | Motor lee common cifrado | 🔴 |
| □ | TC-062 | HTTP method uppercase | 🟠 |
| □ | TC-072 | Nodos ion.store.* post-refactor | 🔴 |
| □ | TC-082 | Total PDF no cuenta borrados | 🟡 |
| □ | TC-083 | Suite devapp /api/2.0/app pasa | 🔴 |
| □ | TC-087 | Flow con OAuth common cifrado | 🔴 |

### FASE 7 — UI (verificación visual)

| □ | TC | Caso | Prioridad |
|---|-----|------|-----------|
| □ | TC-011 | UI: Listar y revocar tokens | 🟠 |
| □ | TC-043 | UI: Enable/disable webhook (Go) | 🟠 |
| □ | TC-060 | UI: Edición connector (Go) | 🟠 |
| □ | TC-085 | UI: Cambiar company sin recargar | 🟠 |
| □ | TC-086 | UI: Diálogo token no cierra con Esc | 🟡 |

### FASE 8 — DB EVIDENCE

```sql
-- Verificar tabla workspace_tokens creada
SELECT id, user_id, company_id, name, scopes, expires_at, revoked
FROM workspace_tokens WHERE company_id = '<company_id>';

-- Verificar cifrado de common
SELECT id, common FROM app_connections WHERE company_id = '<company_id>' LIMIT 1;

-- Verificar schedules no afectados por bug LIKE
SELECT id, board_id FROM schedules WHERE board_id IN (1, 12, 10, 100);

-- Verificar permisos nuevos
SELECT * FROM permissions WHERE name IN ('execute-board','execute-app','create-cron','read-cron','update-cron','delete-cron','publish-app','execute-pdf-template');
```

---

## Criterios de Aprobación / Rechazo

### ✅ APROBACIÓN (todos deben cumplirse)

- ✅ **TODOS** los smoke tests (FASE 1) pasan
- ✅ **TODOS** los happy paths (FASE 2) pasan
- ✅ **TODOS** los tests de seguridad (FASE 3) pasan
- ✅ Al menos **90%** de edge cases (FASE 4) pasan
- ✅ **TODOS** los negativos (FASE 5) pasan
- ✅ **TODOS** los tests de regresión (FASE 6) pasan
- ✅ DB evidence confirma integridad
- ✅ No hay vulnerabilidades críticas abiertas

### ❌ RECHAZO (cualquiera de estos)

- ❌ Smoke test falla → **rechazo inmediato**
- ❌ Cross-company falla → **rechazo inmediato** (vulnerabilidad crítica)
- ❌ PAT auth bypass → **rechazo inmediato** (vulnerabilidad crítica)
- ❌ Happy path falla → rechazo
- ❌ Test negativo falla (sistema se puede romper) → rechazo
- ❌ Regresión falla (nodos store, motor, suite devapp) → rechazo con análisis de impacto
- ❌ Consumo incorrecto (doble cobro o no cobrar) → rechazo

---

## Estimación de Esfuerzo

| Fase | TCs | Estimación | Método |
|------|-----|------------|--------|
| FASE 1 — Smoke | 4 | 30 min | API manual (workspace-token.http) |
| FASE 2 — Happy Path | 20 | 3h | API manual + UI |
| FASE 3 — Seguridad | 7 | 1.5h | API con 2 companies |
| FASE 4 — Edge Cases | 12 | 2h | API manual |
| FASE 5 — Negativos | 16 | 2h | API con tokens sin permisos |
| FASE 6 — Regresión | 9 | 2h | API + boards existentes |
| FASE 7 — UI | 5 | 1h | Manual |
| FASE 8 — DB Evidence | 4 | 30 min | DBeaver |
| **TOTAL** | **87** | **~12.5h** | **~2 días de testing** |

---

## Notas para el Deployment

1. **Insumo principal:** `gateway/workspace-token.http` tiene todas las requests numeradas con resultado esperado
2. **Tokens de prueba:** Crear al menos 2 tokens — uno con todos los permisos, otro con permisos específicos
3. **2 companies obligatorias** para validar aislamiento cross-company
4. **Orden de deploy:** Gateway (migraciones + permisos + cifrado) → flow_binaries (build) → gateway-ion (build)
5. **⚠️ NO usar `db:seed`:** El `LaratrustSeeder` trunca las tablas de permisos
