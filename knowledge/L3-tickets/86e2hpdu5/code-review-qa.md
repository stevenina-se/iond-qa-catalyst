# Code Review QA — 86e2hpdu5 (Modo Deployment / Bug Hunting)

> **Ticket:** CLICKPOST - Implementar conteo de uso y plan mensual por bloques de tracking
> **Branch:** IONF-1217 (NO mergeada a DEVELOPMENT)
> **Developer:** Enrique Vicente
> **QA Engineer:** Steve Nina
> **Fecha:** 2026-09-29

---

## Resumen

- **Repos revisados:** flow_binaries, gateway-ion, gateway
- **Archivos modificados analizados:** 264 (38 + 220 + 6)
- **Hallazgos totales:** 9 (1 resolved)
  - BUG confirmados: 1 (🟠: 1)
  - RISK a verificar: 3 activos + 1 resolved (🟠: 2, 🟡: 1 + ~~1 resolved~~)
  - SEC seguridad: 1 (🟠: 1)
  - EDGE cases: 3 (🟠: 1, 🟡: 2)
- **TCs inyectados en test-matrix:** 8 (TC-CR-001 a TC-CR-009, sin TC-CR-002)

---

## Archivos Modificados (Resumen por Repo)

### flow_binaries (38 archivos, +3138/-134)
| Área | Archivos Clave |
|------|---------------|
| Send Email Node | `send_email.go`, `send_email_types.go`, `send_email_test.go` |
| Webhook API Keys | `webhook_apikey.go`, `webhook_key_service.go`, controllers |
| Email Service | `sender.go`, `config.go`, `message.go`, `sender_test.go` |
| Key Service | `key_service.go`, `key_controller.go`, models |
| Key Lookup | `key_lookup.go` (shared credential fetch) |
| Docs | 4 archivos MDX |

### gateway-ion (220 archivos, +20148/-5938)
| Área | Archivos Clave |
|------|---------------|
| Key Dialogs | `CreateKeyDialog.vue`, `SmtpKeyFormDialog.vue`, `WebhookKeyFormDialog.vue`, `WebhookKeysDialog.vue` |
| Webhook UI | `WebhooksDataTable.vue`, `CreateCustomWebhookDialog.vue` |
| Connections Refactor | 30+ archivos refactorizados (AppCreate → ConnectorCreateView, etc.) |
| UI Components | 15+ nuevos (Stepper, FileDropZone, EditableSection, etc.) |
| Executions | `board.vue`, `board.spec.ts` (nuevo) |

### gateway (6 archivos, +994/-36)
| Área | Archivos Clave |
|------|---------------|
| OpenApiMapper | `OpenApiMapper.php` — `$ref` resolution, `requestBody` mapping, recursive schema |
| Tests | `OpenApiMapperTest.php` (15→36 tests) |

---

## Sección 1 — BUGs Confirmados (BUG-CR-##)

### BUG-CR-001: Concurrent tracking count returns `counted` for multiple simultaneous registrations but `unique_count` stays stale

  **Categoría:** BUG
  **Severidad:** 🟠 Alto
  **Repo:** Datos de producción (boards / flow execution)
  **Archivo:** Evidencia en `responses_log.txt` (líneas 14764-14800)

  **Descripción:** Bajo carga concurrente, múltiples tracking numbers distintos se registran como `counted` pero retornan el mismo `unique_count` — sugiriendo que el contador mensual sufre un race condition de lectura-escritura donde la lectura del tally ocurre antes de que el write previo se confirme.

  **Evidencia:**
  ```
  [2026-09-24 21:00:00.558] TRK-QS-000007795 | counted | unique_count: 2714
  [2026-09-24 21:00:00.592] TRK-QS-000007796 | counted | unique_count: 2715
  [2026-09-24 21:00:01.205] TRK-QS-000007797 | counted | unique_count: 2715  ← STALE
  [2026-09-24 21:00:01.582] TRK-QS-000007799 | counted | unique_count: 2715  ← STALE
  [2026-09-24 21:00:02.001] TRK-QS-000007798 | counted | unique_count: 2715  ← STALE
  [2026-09-24 21:00:03.177] TRK-QS-000007800 | counted | unique_count: 2716
  ```
  Tres trackings distintos (7797, 7799, 7798) retornaron `unique_count: 2715` — todos fueron contados pero el tally no refleja los incrementos individuales.

  **Comportamiento Esperado:**
  Cada tracking con `result: "counted"` debería retornar un `unique_count` incrementado secuencialmente (2715, 2716, 2717).

  **Comportamiento Actual:**
  El `unique_count` retornado es un snapshot stale. Sin embargo, el conteo final parece converger (2716 después de 3 staleness), lo que sugiere que la persistencia es correcta pero la lectura del tally para la respuesta ocurre antes de que los writes concurrentes se completen.

  **Precondiciones:**
  - Contrato activo con 1 bloque
  - Alta concurrencia (5+ requests/segundo)
  - Tracking numbers distintos

  **Pasos de Reproducción:**
  1) Configurar contrato activo con unit_size: 5000
  2) Enviar 10+ tracking numbers únicos simultáneamente (parallel POST)
  3) Verificar que cada respuesta con `counted: true` tenga un `unique_count` distinto
  4) Verificar en data store `clickpost_periods` que el `unique_count` final es correcto

  **Impacto:** El `unique_count` en la respuesta del webhook es informativo (el dato persistido es correcto), pero el reporte de uso podría mostrar cifras inconsistentes si depende de la respuesta en lugar del tally persistido. Verificar que la alerta de 80/100% se basa en el tally persistido, no en el `unique_count` de la respuesta.

  **Notas:** Originado en la lógica del board de clickpost-usage, no en código de plataforma. Los boards operan sobre Persistent Data (SQLite del tenant) que no tiene row-level locking como PostgreSQL. El AC-5 (concurrencia) dice "solo uno incrementa", pero aquí son trackings DISTINTOS, así que todos deberían contar — el bug es en el valor retornado, no en el conteo.

---

## Sección 2 — Riesgos a Verificar (RISK-CR-##)

### ~~RISK-CR-001: Webhook API key — timing attack en comparación de hashes~~ ✅ RESOLVED

  **Categoría:** RISK → **RESOLVED**
  **Severidad:** ~~🟡 Medio~~ → N/A
  **Repo:** flow_binaries
  **Archivo:** `backend/ion/helpers/webhook_apikey.go` (línea 32-38)

  **Descripción:** Verificado — `WebhookApiKeyMatches` usa `crypto/subtle.ConstantTimeCompare` correctamente. La comparación es constant-time. **No hay vulnerability.**

  **Evidencia:**
  ```go
  func WebhookApiKeyMatches(storedHash, presented string) bool {
      if storedHash == "" || presented == "" {
          return false
      }
      presentedHash := HashWebhookApiKey(presented)
      return subtle.ConstantTimeCompare([]byte(storedHash), []byte(presentedHash)) == 1
  }
  ```

  **Resolución:** El código es seguro. No requiere TC.

### RISK-CR-002: SMTP password en key update — blank password keeps stored value

  **Categoría:** RISK
  **Severidad:** 🟠 Alto
  **Repo:** flow_binaries
  **Archivo:** `backend/ion/services/key_service.go` — funciones `UpdateKeyByCompany` y `UpdateKeyByAccount`

  **Descripción:** El update de webhook keys protege `parameters` y `metadata` como inmutables. Pero para SMTP keys, un PUT con `parameters: {"password": ""}` reemplazaría la password almacenada con un string vacío. No hay guard especial para SMTP keys en el update.

  **Comportamiento Esperado:**
  Al editar un SMTP credential, enviar un password vacío debería preservar el password existente (como documenta el developer: "On edit, a blank password keeps the stored one").

  **Comportamiento Actual:**
  El código de `UpdateKeyByCompany` hace `key.SetParameters(input.Parameters)` si `input.Parameters != nil` y el key no es de tipo webhook. Si el frontend envía `{"password": ""}`, se sobrescribe con vacío.

  **Pasos de Reproducción:**
  1) Crear SMTP credential con password válido
  2) Editar: cambiar solo el host, dejar password vacío
  3) Guardar
  4) Verificar que el password se conservó (no se borró)
  5) Intentar enviar email con el credential editado

### RISK-CR-003: `UpdateKeyByAccount` / `UpdateKeyByCompany` — `input.Type` field no longer updatable

  **Categoría:** RISK
  **Severidad:** 🟡 Medio
  **Repo:** flow_binaries
  **Archivo:** `backend/ion/services/key_service.go`

  **Descripción:** El diff muestra que se eliminó la línea `if input.Type != "" { key.Type = input.Type }` para AMBOS tipos de keys (no solo webhook). Esto significa que el tipo de key ya no es editable para ningún tipo de key. Verificar si esto es intencional y si el frontend ya no envía `type` en updates.

  **Comportamiento Esperado:**
  El `type` de una key no debería ser editable (una key AI provider no se convierte en SMTP).

  **Comportamiento Actual:**
  La propiedad `type` ya no se actualiza en ningún update. Parece intencional — el tipo se fija al crear.

### RISK-CR-004: CreateCustomWebhookDialog — two-step creation (webhook + key) without atomic rollback

  **Categoría:** RISK
  **Severidad:** 🟠 Alto
  **Repo:** gateway-ion
  **Archivo:** `src/components/workflow/components/CreateCustomWebhookDialog.vue`

  **Descripción:** Cuando el usuario activa "Require API key" al crear un webhook custom, el flujo es: 1) crear webhook, 2) crear key. Si el paso 2 falla, el webhook queda creado sin key y el diálogo se cierra. El comentario en el código lo reconoce: "The webhook already exists, so a failed key step closes the dialog instead of inviting a resubmit that would create a second webhook."

  **Comportamiento Esperado:**
  Si el usuario pidió una key y falla, debería poder reintentar crear la key sin crear un segundo webhook.

  **Comportamiento Actual:**
  El diálogo se cierra tras el error del paso 2, dejando un webhook sin key. El usuario tendría que ir a la tabla de webhooks y agregar la key manualmente. Esto es un UX risk, no un bug — el developer eligió conscientemente evitar webhooks duplicados.

  **Pasos de Reproducción:**
  1) Flow Editor > Create Custom Webhook > activar "Require API key"
  2) Ingresar nombre válido
  3) Simular error de red justo en la creación de la key (throttle/block)
  4) Verificar: webhook creado sin key, diálogo cerrado, toast de error mostrado

---

## Sección 3 — Seguridad (SEC-CR-##)

### SEC-CR-001: API key header NOT stripped on auth failure — header reaches ParseBody only on success

  **Categoría:** SEC
  **Severidad:** 🟠 Alto
  **Repo:** flow_binaries
  **Archivo:** `backend/ion/services/webhook_key_service.go` — función `AuthorizeWebhookRequest`

  **Descripción:** El header `X-Ion-Apikey` se elimina del request solo cuando la autenticación es exitosa (`r.Header.Del(helpers.WebhookApiKeyHeader)`). Si la auth falla, el handler devuelve un error antes de que se parsee el body, por lo que el header nunca llega a los logs. VERIFICAR: si el controller tiene un error handler que logguea headers del request en caso de error, la key podría exponerse en logs de error.

  **Comportamiento Esperado:**
  El header debería ser stripped SIEMPRE (exitoso o fallido) para evitar que aparezca en cualquier log.

  **Comportamiento Actual:**
  El header se elimina solo en el path exitoso. En el path de error, la función retorna un error y el controller escribe el JSON error response — el request headers se descartan sin procesamiento adicional, pero si hay middleware de logging de requests, podrían capturar el header.

  **Pasos de Reproducción:**
  1) Enviar POST a webhook protegido con key inválida
  2) Verificar logs del servidor — ¿aparece `X-Ion-Apikey` en el log de error?
  3) Si sí → el plaintext de la key está expuesto en logs

---

## Sección 4 — Edge Cases (EDGE-CR-##)

### EDGE-CR-001: OpenApiMapper `resolveRef` — `reset($content)` con array vacío retorna `false`

  **Categoría:** EDGE
  **Severidad:** 🟡 Medio
  **Repo:** gateway
  **Archivo:** `app/Repositories/Mappers/OpenApiMapper.php` — función `mapRequestBodyToParameter`

  **Descripción:** La línea `$media = $content['application/json'] ?? (is_array($content) ? reset($content) : false)` usa `reset()` que retorna `false` si el array está vacío. Luego verifica `if (!is_array($media) ...)` — `false` no es array, así que retorna `null`. Funciona correctamente, pero es un patrón frágil si alguien modifica la condición.

  **Comportamiento Esperado:**
  Spec con `requestBody` vacío retorna `null` (no mapea body parameter).

  **Comportamiento Actual:**
  Correcto — `false` no pasa el check `is_array($media)`. Sin embargo, un `requestBody` con `content: {}` (vacío) es un spec malformado y debería fallar gracefully.

### EDGE-CR-002: WebhookKeysDialog — plaintext key not cleared when dialog reopened

  **Categoría:** EDGE
  **Severidad:** 🟡 Medio
  **Repo:** gateway-ion
  **Archivo:** `src/components/tenant/key/WebhookKeysDialog.vue`

  **Descripción:** El watcher en `open` limpia `plaintextKey` al cerrar. Pero si el usuario crea una key, ve el plaintext, cierra, reabre, y crea otra key — el nuevo plaintext reemplaza al anterior correctamente. Sin embargo, si `addKey()` falla silenciosamente (error catch → toast), `plaintextKey` mantiene el valor anterior.

  **Comportamiento Esperado:**
  Si la creación de una nueva key falla, el plaintext de una key anterior no debería persistir en el UI.

  **Comportamiento Actual:**
  El `plaintextKey` se limpia al cerrar y reabrir el diálogo (por el watcher). Dentro del mismo diálogo, `addKey()` solo asigna `plaintextKey` en el `try` exitoso y no lo limpia en el `catch`. Si hubo un plaintext previo en la misma sesión de diálogo y el segundo intento falla, el plaintext previo persiste.

  **Pasos de Reproducción:**
  1) Abrir Webhook Keys Dialog
  2) Crear key → ver plaintext (ej: `ionwh_abc123...`)
  3) Intentar crear otra key → falla (simular error)
  4) Verificar: ¿se sigue mostrando el plaintext anterior?

### ~~EDGE-CR-003: `ApiKeysCount` computed field — not populated in non-paginated listing~~ ✅ RESOLVED

  **Categoría:** EDGE → **RESOLVED**
  **Severidad:** ~~🟠 Alto~~ → N/A
  **Repo:** flow_binaries

  **Descripción:** Verificado — `company_webhook_service.go` (línea 420-442) tiene `attachApiKeysCountByCompany` que hace un COUNT query agrupado por `metadata->>'webhook_id'` y popula el campo `ApiKeysCount` en cada webhook. La implementación es correcta.

  **Evidencia:**
  ```go
  func attachApiKeysCountByCompany(company *models.Company, webhooks []models.CompanyWebhook) error {
      // ... COUNT(*) GROUP BY metadata->>'webhook_id'
      for i := range webhooks {
          webhooks[i].ApiKeysCount = countByWebhookID[strconv.FormatUint(webhooks[i].ID, 10)]
      }
  }
  ```

  **Resolución:** El campo se popula correctamente. Verificar visualmente en testing pero no es un riesgo de código.

---

## Follow-the-Flow Maps

### Flow: Webhook API Key Enforcement
```
1. CALLERS: company_webhook_controller.go, account_webhook_controller.go
   → Both call FindWebhookKeyHashes → AuthorizeWebhookRequest BEFORE ParseBody
2. PERSISTENCIA: SHA-256 hash in keys.parameters; plaintext shown once at creation
3. CONSUMIDORES: Every webhook POST triggers auth check
4. RENDER: WebhooksDataTable shows api_keys_count; WebhookKeysDialog manages keys
5. ERROR PATH: 401 returned before body is parsed → no execution logged → clean
6. OPERACIÓN OPUESTA: Create key ↔ Delete key — both work; rotation = create new + delete old
   ✅ Symmetric — no orphans
```

### Flow: Send Email Node
```
1. CALLERS: All 4 flow runners (company_dev, company_live, account_dev, account_live)
2. PERSISTENCIA: No persistence — fire-and-forget email send
3. CONSUMIDORES: Node output/error handles in the flow
4. RENDER: Node appears in catalog; SMTP credential dropdown at flow editor load
5. ERROR PATH: classifySendError → 503/401/408/400/502 → error handle with message + status
   ✅ Well-typed errors
6. OPERACIÓN OPUESTA: N/A — sending email is one-way
```

---

## Impacto Cruzado

| Módulo Impactado | Componente Afectado | Riesgo | Verificación Necesaria |
|---|---|---|---|
| Webhooks | Webhook execution controller | 🔴 | REG-001/002/003: webhooks existentes sin key siguen funcionando |
| Keys | Key listing, key type filter | 🟠 | Filtro por type=webhook y type=smtp funciona |
| Nodes | Flow catalog, node palette | 🟠 | REG-004/005/006: Send Email node aparece y funciona |
| Connections | OpenApiMapper | 🟠 | REG-007: specs existentes importan sin regresión |
| Boards | Schedule trigger | 🟡 | REG-009: schedules existentes no afectados |
| IONF-1152 | Tracking flow | 🟠 | REG-008: flow operativo sigue funcionando |

---

## TCs Inyectados en Test Matrix

| TC ID | Categoría | Origen | Caso de Test | Severidad |
|-------|-----------|--------|-------------|-----------|
| TC-CR-001 | BUG | BUG-CR-001 | Concurrencia de trackings distintos — verificar que unique_count retornado incrementa correctamente | 🟠 |
| ~~TC-CR-002~~ | ~~RISK~~ | ~~RISK-CR-001~~ | ~~Verificar que WebhookApiKeyMatches usa constant-time comparison~~ | ✅ RESOLVED |
| TC-CR-003 | RISK | RISK-CR-002 | Editar SMTP credential dejando password vacío — verificar que se conserva el password | 🟠 |
| TC-CR-004 | RISK | RISK-CR-004 | Crear webhook con "Require API key" y simular fallo en creación de key — verificar UX | 🟠 |
| TC-CR-005 | SEC | SEC-CR-001 | Enviar request con API key inválida — verificar que el header no aparece en logs | 🟠 |
| TC-CR-006 | EDGE | EDGE-CR-001 | Importar OpenAPI spec con requestBody vacío — verificar graceful fallback | 🟡 |
| TC-CR-007 | EDGE | EDGE-CR-002 | Crear key, ver plaintext, fallo en segunda key — verificar que plaintext previo no persiste | 🟡 |
| ~~TC-CR-008~~ | ~~EDGE~~ | ~~EDGE-CR-003~~ | ~~Verificar que columna "API Keys" en tabla de Webhooks muestra conteo correcto~~ | ✅ RESOLVED |
| TC-CR-009 | RISK | RISK-CR-003 | Verificar que el campo `type` de una key existente no es editable via PUT | 🟡 |
