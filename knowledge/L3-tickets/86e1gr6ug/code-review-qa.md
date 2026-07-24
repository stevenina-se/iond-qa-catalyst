# Code Review QA — 86e1gr6ug
## Mejoras de la interface en ionflow dualtrack

> **Fecha**: 2026-06-25
> **QA Engineer**: Steve Nina
> **Reviewer IA**: QA Catalyst
> **Branch analizada**: `IONF-1030` (mergeada en `DEVELOPMENT`)
> **Repos revisados**: `gateway-ion`, `flow_binaries`, `gateway`
> **Modo**: Deployment / Bug Hunting

---

## Resumen de Commits Analizados

| Repo | Commits IONF-1030 |
|------|-------------------|
| `gateway-ion` | 20 commits (feat, fix, test, refactor) |
| `flow_binaries` | 10 commits (feat, fix, test) |
| `gateway` | 7 commits (feat, fix, refactor, test) |

---

## Cambio Arquitectonico Mayor (Post-Discovery)

> El "HUB Move": La logica de listado y clonacion de flows migro de Laravel (gateway) a Go HUB (flow_binaries).
> Este cambio no estaba en el Discovery original y modifica los endpoints que el Frontend consume.

**Impacto en testing**:
- El endpoint de lista de flows (GET /flows) ahora responde desde el HUB (Go), no desde Laravel
- El endpoint de clone (POST /flows/{id}/clone) ahora es del HUB tambien
- El flows.service.ts del Frontend fue actualizado para apuntar a VITE_APP_HUB_URL

---

## Hallazgos del Code Review

### BUG-CR-001 — [RIESGO A VERIFICAR] Backfill de last_execution_id con executable_type incorrecto

**Severidad**: Alta
**Tipo**: Bug corregido en codigo — verificar que la correccion aplico en staging

**Hallazgo**:
En el commit ceb57972, se corrigio la migracion 2026_06_02_120000_add_last_execution_id_to_flows_table.php:
- ANTES (incorrecto): WHERE e.executable_type = 'tenant_flow'
- DESPUES (correcto):  WHERE e.executable_type = 'flow'

**Riesgo**: Si la migracion de backfill ya corrio con el valor incorrecto en staging antes del fix,
el last_execution_id puede estar NULL en todos los flows existentes aunque tengan ejecuciones.

**Verificacion necesaria (BD)**:
```sql
-- Fuente: gateway/database/migrations/tenants/2026_06_02_120000_add_last_execution_id_to_flows_table.php
SELECT f.id, f.name, f.last_execution_id, MAX(e.id) as latest_exec_id
FROM flows f
LEFT JOIN executions e ON e.executable_id = f.id AND e.executable_type = 'flow'
GROUP BY f.id, f.name, f.last_execution_id
HAVING MAX(e.id) IS NOT NULL AND f.last_execution_id IS NULL;
-- Si retorna rows -> el backfill no corrio correctamente
```

**Clasificacion**: [RIESGO A VERIFICAR] — Depende del orden de deploy de las migraciones.

---

### BUG-CR-002 — [RIESGO A VERIFICAR] deriveTerminalStatus solo aplicado en Dev Flow tras segundo fix

**Severidad**: Alta
**Tipo**: Bug corregido — verificar funcionamiento en ambos modos

**Hallazgo**: El commit ac640db extrae deriveTerminalStatus en flow_helpers.go y lo aplica al company_dev_flow.go.
El commit anterior 0d36b0e ya lo habia aplicado al company_live_flow.go (modo Live).

**Logica implementada (flow_helpers.go)**:
```go
func deriveTerminalStatus(hadFatalError bool, errors []string) ExecutionStatus {
    if hadFatalError { return StatusError }
    if len(errors) > 0 { return StatusWarning }
    return StatusCompleted
}
```

**Verificacion en testing**: TC-008 (completed), TC-009 (warning), TC-003 (error).
Ejecutar flows que fallen un nodo en modo Dev Y modo Live.

**Clasificacion**: [RIESGO A VERIFICAR] — Necesita reproduccion con flows que fallen un nodo.

---

### BUG-CR-003 — [RIESGO A VERIFICAR] Payload Diet con data NULL en flow nuevo

**Severidad**: Media
**Tipo**: Edge case

**Hallazgo**: El trimmedFlowDataSQL en company_flow_service.go tiene guards para jsonb_typeof y coalesce.
Sin embargo, si el campo data es NULL (flow recien creado sin grafo), devuelve {nodes:[], edges:[]}.
Puede causar que el Frontend muestre un flow con 0 nodos cuando en realidad tiene grafo.

**Clasificacion**: [RIESGO A VERIFICAR] — Verificar con TC-004 y REG-002.

---

### BUG-CR-004 — [RIESGO A VERIFICAR] applyILIKE: verificar escape de caracteres especiales en runtime

**Severidad**: Alta
**Tipo**: Edge case en escape SQL

**Hallazgo (search_helpers.go)**:
```go
var likeEscaper = strings.NewReplacer(`\`, `\\`, `%`, `\%`, `_`, `\_`)
```
El orden es correcto (backslash primero). Codigo parece seguro estaticamente.

**Verificacion en testing** (TC-043 SQL injection, TC-045 caracteres especiales):
- "100%" -> debe buscar literalmente "100%", no como wildcard
- "test_user" -> debe buscar literalmente "test_user"
- "'; DROP TABLE flows; --" -> no debe ejecutar SQL

**Clasificacion**: [RIESGO A VERIFICAR] — Verificar en runtime.

---

### BUG-CR-005 — [RIESGO A VERIFICAR] immutable_unaccent: verificar que funcion existe en staging

**Severidad**: Critica
**Tipo**: Dependencia de migracion — puede romper busqueda completamente

**Hallazgo**: applyFTS en search_helpers.go llama a public.immutable_unaccent() en SQL.
Esta funcion la crea la migracion 2026_06_03_120100_create_immutable_unaccent_function.php.
Si esta migracion no corrio en staging, toda busqueda FTS lanzara error 500.

**Verificacion en BD**:
```sql
-- Fuente: gateway/database/migrations/2026_06_03_120100_create_immutable_unaccent_function.php
SELECT proname, provolatile FROM pg_proc WHERE proname = 'immutable_unaccent';
-- Debe retornar 1 row con provolatile = 'i' (IMMUTABLE)

-- Indice GIN
-- Fuente: gateway/database/migrations/tenants/2026_06_03_120000_add_fts_index_to_flows_table.php
SELECT indexname FROM pg_indexes WHERE indexname = 'flows_fts_idx';
-- Debe existir
```

**Clasificacion**: [RIESGO A VERIFICAR] — Si falta la funcion -> TC-042 fallara con 500.

---

### BUG-CR-006 — [VERIFICACION POSITIVA] FlowStatusBadge envia solo {status} — Payload Diet correcto

**Severidad**: OK
**Tipo**: Verificacion positiva de AC

**Hallazgo (FlowStatusBadge.vue)**:
```typescript
const response = await FlowService.update(props.flow.id, { status } as Partial<Flow>);
```
El componente envia SOLO el campo status, no el payload completo del flow.
El riesgo original del Discovery (Payload Diet sobrescribe grafo) esta MITIGADO en el Frontend.

**Clasificacion**: [VERIFICACION POSITIVA] — TC-006 deberia pasar.

---

### BUG-CR-007 — [RIESGO A VERIFICAR] attachLastExecutions — aislamiento multi-tenant

**Severidad**: Alta
**Tipo**: Multi-tenancy

**Hallazgo**: attachLastExecutions usa company.CompanySchema() correctamente para aislar ejecuciones.
Sin embargo, si last_execution_id apunta a un ID de ejecucion de OTRO tenant (por BUG-CR-001),
la query devolveria 0 resultados y el badge quedaria en "never_run" incorrectamente.

**Clasificacion**: [RIESGO A VERIFICAR] — Vinculado a BUG-CR-001.

---

### BUG-CR-008 — [RIESGO A VERIFICAR] Clone fuerza status = ACTIVE en flow clonado

**Severidad**: Alta
**Tipo**: Comportamiento de negocio

**Hallazgo**: Commit 17e1a6a: "force clone status active".
El clone fuerza status = ACTIVE en el flow clonado.
Pregunta: un flow recien clonado deberia estar ACTIVE automaticamente?
Si tiene triggers de webhook/schedule, podria ejecutarse sin que el usuario lo configure.

**Clasificacion**: [RIESGO A VERIFICAR] — Verificar con TC-016 (clonar flow).

---

## Resumen de Hallazgos

| ID | Hallazgo | Severidad | Clasificacion |
|----|----------|-----------|---------------|
| BUG-CR-001 | Backfill last_execution_id con tipo incorrecto | Alta | RIESGO A VERIFICAR |
| BUG-CR-002 | deriveTerminalStatus — verificar modo Dev | Alta | RIESGO A VERIFICAR |
| BUG-CR-003 | Payload Diet con data NULL | Media | RIESGO A VERIFICAR |
| BUG-CR-004 | ILIKE escape de % _ \ | Alta | RIESGO A VERIFICAR |
| BUG-CR-005 | immutable_unaccent debe existir en staging | Critica | RIESGO A VERIFICAR |
| BUG-CR-006 | FlowStatusBadge envia solo {status} | OK | VERIFICACION POSITIVA |
| BUG-CR-007 | attachLastExecutions — aislamiento tenant | Alta | RIESGO A VERIFICAR |
| BUG-CR-008 | Clone fuerza status = ACTIVE | Alta | RIESGO A VERIFICAR |

**Total**: 7 riesgos a verificar, 0 bugs confirmados en analisis estatico, 1 verificacion positiva.

---

## TCs Inyectados en Test Matrix

| ID | Tipo | Descripcion | Prioridad |
|----|------|-------------|-----------|
| TC-CR-001 | Code Review | Backfill last_execution_id — query BD para flows con ejecuciones sin puntero | Alta |
| TC-CR-002 | Code Review | deriveTerminalStatus modo Dev — flow con nodo fallido desde canvas | Alta |
| TC-CR-003 | Code Review | immutable_unaccent existe en BD + indice GIN activo | Critica |
| TC-CR-004 | Code Review | Flow clonado: verificar status inicial del clon | Alta |
| TC-CR-005 | Code Review | attachLastExecutions — badge no cruza tenants | Alta |

---

*Generado por QA Catalyst — 2026-06-25 | Modo: Deployment / Bug Hunting*
*Repos revisados en DEVELOPMENT (post-merge IONF-1030)*
