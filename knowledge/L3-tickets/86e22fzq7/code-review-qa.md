# Code Review QA — 86e22fzq7 (Modo Deployment / Bug Hunting)

> Fecha: 2026-07-14
> Ticket: 86e22fzq7 — Connections — Reautorización por API Key crea conexión duplicada en lugar de sobrescribir
> Branch: IONF-1114 → Mergeada en DEVELOPMENT (PR gateway-ion #12, PR flow_binaries #14)
> Revisado por: QA Catalyst
> Commits revisados: de605756 + 3533fe98 (gateway-ion) | 284fe58 + 55280d6 + 47023c3 + 127350b (flow_binaries)

---

## Resumen

| Métrica | Valor |
|---------|-------|
| Repos revisados | `gateway-ion` + `flow_binaries` |
| Archivos modificados analizados | 2 (core del fix) |
| Bugs confirmados (reproducibles) | 0 |
| Riesgos a verificar en testing | 2 |
| TCs inyectados en test-matrix | 2 (TC-CR-001, TC-CR-002) |
| Tests unitarios del Developer | ⚠️ Ninguno — no se agregaron ni modificaron tests |

---

## Archivos Modificados

### `flow_binaries`

| Archivo | Cambio Principal |
|---------|-----------------|
| `backend/ion/services/attempt_service.go` | **Fix core (4 commits)**: 1) `resolveCompanyAppAndConnection()` — cuando `attempt.ConnectionId` presente para global app, carga `ConnectionTenant` existente via `FindConnectionByCompany()` e inyecta en context. 2) `upsertCompanyConnection()` — si `connection != nil` (reauthorize), actualiza credenciales in-place con `UpdateConnectionByCompany()` en lugar de crear con `NewConnectionByCompany()`. Error handling agregado en code review fix. 3) Commit 55280d6 eliminó update del nombre, pero 127350b lo re-agregó (`connection.Connection.Name = label`). |

### `gateway-ion`

| Archivo | Cambio Principal |
|---------|-----------------|
| `src/components/workflow/components/CreateConnectionV2Dialog.vue` | **Fix frontend (2 commits)**: 1) `isReauthorize` computed: `props.connectionId != null`. 2) Refactor de `testAttempt()` en 3 helpers: `handleAuthorizingStatus()`, `handleSuccessStatus()`, `showSuccessToast()`. 3) Toast suppression: ambos `handleAuthorizingStatus` y `handleSuccessStatus` envuelven `showSuccessToast()` en `if (!isReauthorize.value)`. 4) Code review fix: tipado mejorado (`Attempt` en vez de inline type), `emit('created', intresult)` sin cast, toast summary de `'waiting'` cambiado de `message.success` a `message.info`. |
| `src/views/tenant/integrations/components/ReauthorizeConnectionButton.vue` | **Ya existía** (no modificado en este PR). Pasa `connectionId` como prop al dialog, lo que activa `isReauthorize`. |

---

## Análisis del Fix Principal

El fix es **correcto y bien estructurado**:

### Backend — `attempt_service.go`

1. **Routing lógico correcto**: `resolveCompanyAppAndConnection()` ahora distingue:
   - `attempt.ConnectionId == nil` → nueva conexión → retorna `connection = nil` → `upsertCompanyConnection` crea
   - `attempt.ConnectionId != nil` → reauthorize → carga connection existente → `upsertCompanyConnection` actualiza in-place
   ✅ Correcto

2. **Multi-tenant seguro**: `FindConnectionByCompany()` usa `company.CompanySchema()` que aplica filtro de schema por company. Un connection_id de otra company no sería encontrado → retorna error, no actualiza nada ajeno. ✅ Seguro

3. **Update in-place**: `upsertCompanyConnection()` cuando `connection != nil`:
   - Mantiene el nombre (`connection.Connection.Name = label`) — re-agregado en commit 127350b
   - Actualiza credenciales encriptadas: `.Connection` y `.Data`
   - Actualiza timestamp
   - Usa `UpdateConnectionByCompany()` con error handling
   ✅ Correcto

4. **Observación sobre la evolución del fix**: El commit 55280d6 eliminó `connection.Connection.Name = label` con comentario "keep the existing name", pero 127350b lo re-agregó. Esto sugiere que el code reviewer (Rodolfo) pidió mantener el update del nombre. **No es un bug**, pero el comentario del código ("keep the existing name") contradice lo que el código hace (actualiza el nombre). → Riesgo bajo de confusión futura.

### Frontend — `CreateConnectionV2Dialog.vue`

1. **`isReauthorize` detection**: `computed(() => props.connectionId != null)` — simple y correcto. Si `connectionId` está presente, es reauthorize. ✅

2. **Toast suppression**: `if (!isReauthorize.value) { showSuccessToast(...) }` en ambos handlers. ✅

3. **Refactor de `testAttempt`**: Bien hecho — extrae 3 funciones helper claras. No cambia la lógica, solo la estructura. ✅

4. **El componente `ReauthorizeConnectionButton.vue`** pasa `:connectionId="connection.id"` al dialog, lo que activa la detección. ✅

---

## Bugs Confirmados (Reproducibles)

> **Ninguno.** El fix es correcto. La lógica de routing backend y toast suppression frontend son coherentes.

---

## Riesgos a Verificar

### RIESGO-CR-001 — RIESGO A VERIFICAR
**Clasificación**: RIESGO A VERIFICAR
**Severidad**: 🟠 Medio
**Repo**: `flow_binaries`
**Archivo**: `attempt_service.go` — línea 621-624

**Descripción**: Si `FindConnectionByCompany()` no encuentra la connection (ej: fue eliminada entre que el usuario abrió el dialog y clickeó reauthorize), retorna error. El error se propaga hasta el handler HTTP. ¿El frontend maneja este error gracefully o queda en estado inconsistente (loader infinito, dialog sin cerrar)?

**TC inyectado**: TC-CR-001

### RIESGO-CR-002 — RIESGO A VERIFICAR
**Clasificación**: RIESGO A VERIFICAR
**Severidad**: 🟡 Bajo
**Repo**: `gateway-ion`
**Archivo**: `CreateConnectionV2Dialog.vue` — línea 200, 213

**Descripción**: Después de un reauthorize exitoso, el dialog emite `'created'` (no `'reauthorized'`). El `ReauthorizeConnectionButton.vue` escucha `@created` y lo re-emite como `@reauthorized`. ¿El componente padre que recibe `@reauthorized` actualiza la lista de connections correctamente? Si no refresca la lista, las credenciales antiguas seguirán mostrándose.

**TC inyectado**: TC-CR-002

---

## Hallazgos Adicionales (No Bugs)

| # | Tipo | Observación |
|---|------|------------|
| H-001 | Código | Comentario en línea 664 dice "keep the existing name" pero línea 665 hace `connection.Connection.Name = label` (SÍ actualiza el nombre). Contradicción menor — cosmético. |
| H-002 | Testing | Developer no agregó tests unitarios ni modificó tests existentes. Esto aumenta dependencia en testing manual de QA. |
| H-003 | Evento | El dialog emite `'created'` tanto para creación como reauthorize. Sería más claro emitir `'reauthorized'` en el segundo caso, pero funciona porque `ReauthorizeConnectionButton` re-mapea el evento. |
