# Risk Triage — 86e22fzq7

> Ticket: Connections — Reautorización por API Key crea conexión duplicada en lugar de sobrescribir
> Módulo: Connections / Integrations
> Fecha: 2026-07-14

---

## Clasificación del Ticket

| Campo | Valor |
|-------|-------|
| Tipo | Bug Fix |
| Criticidad del módulo | 🟠 Alto (Connections) |
| Impacto potencial | Integridad de datos (conexiones duplicadas) + UX (toasts duplicados) |
| Repos afectados | `gateway-ion` (PR #12) + `flow_binaries` (PR #14) |
| Migraciones de BD | ❌ No hay |
| Tests del Developer | ⚠️ Ninguno — no se agregaron ni modificaron tests |

---

## Análisis de Riesgo por Área

### 🔴 Riesgos Críticos

| # | Área | Riesgo | Justificación |
|---|------|--------|---------------|
| R-001 | Backend — Upsert logic | El fix carga `ConnectionTenant` existente para global apps. Si la lógica de `FindConnectionByCompany` falla silenciosamente (ej: connection no encontrada), podría crear duplicados igual. | El cambio central del fix — si falla, el bug persiste |
| R-002 | Multi-tenant isolation | Al inyectar `ConnectionTenant` en el auth context, ¿se valida que pertenece a la company correcta? Si no, un connection_id de otra company podría sobreescribir credenciales ajenas. | Riesgo de seguridad multi-tenant |
| R-003 | Backward compat — Tenant apps | El developer indica que "el tenant app flow was not changed", pero el refactor de `testAttempt` puede haber introducido efectos colaterales en la lógica compartida. | Refactor de método monolítico → helpers |

### 🟠 Riesgos Medios

| # | Área | Riesgo | Justificación |
|---|------|--------|---------------|
| R-004 | Frontend — Toast suppression | Los toasts se suprimen con `isReauthorize` basado en `connectionId` prop. Si el componente se reutiliza en otro contexto donde `connectionId` se pasa sin intención de reauthorize, los toasts desaparecerán incorrectamente. | Acoplamiento de prop a comportamiento |
| R-005 | OAuth flow (authorizing status) | El refactor extrajo `handleAuthorizingStatus` del monolítico `testAttempt`. Si el orden de ejecución o las condiciones cambiaron, el flujo OAuth podría romperse. | Refactor de lógica de auth |
| R-006 | Flows que referencian la conexión | Después de reauthorize exitoso, los flows que usan la conexión original ¿recogen automáticamente las nuevas credenciales? | Impacto en ejecución de flows |

### 🟡 Riesgos Bajos

| # | Área | Riesgo | Justificación |
|---|------|--------|---------------|
| R-007 | UX — Feedback de reauthorize | Sin toasts en reauthorize, ¿hay algún feedback visual al usuario de que la reautorización fue exitosa? | Usabilidad |
| R-008 | Creación de nueva conexión | Asegurar que la supresión de toasts es SOLO para reauthorize, no para creación nueva. | Regresión de UX |

---

## Matriz de Impacto Cruzado

| Módulo | Afectado por este fix | Riesgo |
|--------|----------------------|--------|
| **Boards** | Sí — flows usan connections | Si reauthorize falla silenciosamente, flows seguirán con credenciales viejas |
| **Integrations** | Sí — connections activas | Conexiones duplicadas podrían causar confusión |
| **Auth** | Sí — flujo OAuth | Refactor de `testAttempt` podría afectar OAuth flow |
| **Webhooks** | Indirecto | Webhooks de apps necesitan connection activa |

---

## Preguntas para Enriquecer Testing

1. ¿Qué métodos de autenticación soporta el sistema actualmente? (OAuth, API Key, Basic, Client Credentials — ¿todos afectados o solo API Key?)
2. El fix menciona "global app" — ¿las tenant apps también tienen el bug o solo las globales?
3. ¿Existe endpoint de API para reauthorize o es solo via UI?
4. ¿Cómo se comporta si la conexión original fue eliminada antes de intentar reauthorize?

---

## Resumen de Priorización

| Bloque | Prioridad | Casos estimados |
|--------|-----------|----------------|
| Smoke tests | 🔴 | 2 — Vista de connections carga + botón reauthorize visible |
| Happy path (bug fix) | 🔴 | 3 — Reauthorize API Key no duplica, update in-place, single toast |
| Edge cases | 🟠 | 4 — OAuth reauthorize, tenant app, connection eliminada, feedback UX |
| Negativos | 🟠 | 2 — Creación nueva sigue con toast, multi-tenant isolation |
| Regresión | 🟠 | 3 — OAuth flow intacto, tenant apps intactas, flows con connection |
| DB Evidence | 🟡 | 1 — Verificar que no hay duplicados post-reauthorize |

**Total estimado: ~15 TCs**
