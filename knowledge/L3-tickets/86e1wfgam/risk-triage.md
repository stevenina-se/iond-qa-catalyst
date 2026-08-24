# Risk Triage — 86e1wfgam (Motor de exposición por API — FASE 1)

## Resumen

- **Módulo principal**: Developer Apps
- **Módulos impactados**: Accounts, Connections, PDF Templates, Boards, Auth
- **Riesgo general**: 🔴 Crítico
- **Total edge cases identificados**: 24
- **Total preguntas para Developer**: 12
- **Repos impactados**: 4 (flow_binaries, gateway, gateway-ion, webcomponents-flow)
- **Contexto de ClickUp**: 4 comentarios leídos + 3 child tasks. Divergencias significativas entre AC de descripción (genéricos) y especificación técnica del Dev (detallada)

---

## Análisis de Lógica de Negocio

| Pregunta | Análisis |
|----------|----------|
| ¿El feature respeta las reglas multi-tenant (company)? | ⚠️ **Cambio fundamental**: Este ticket introduce un nuevo modelo donde accounts son propiedad de la **compañía** (no del app). Todas las apps de una misma compañía comparten customers y conexiones. Esto cambia la semántica de aislamiento existente. |
| ¿Afecta la ejecución de flows/nodos? | ✅ Sí — expone flows y mappers por API con ejecución síncrona. Comparte runner con el board (`sin cambio de comportamiento`), pero introduce nuevo contexto de ejecución (app + account). |
| ¿Hay impacto en connectors globales vs company? | ⚠️ Sí — introduce direccionamiento **namespaced** (`app.*` canónico, `tenant.*` reservado futuro). Los connectors están **por app** (`app_setup`), no por compañía, lo que crea una asimetría con el modelo de accounts compartidos. |
| ¿Se tocan datos de ejecución (SQLite) o datos persistentes (PostgreSQL)? | ✅ PostgreSQL — migración que cambia el índice unique de `accounts.remote_id` (global → por-compañía). No toca SQLite de ejecuciones. |
| ¿Hay impacto en el sistema de permisos por usuario/company? | ✅ Sí — nuevo sistema de auth OAuth2 `client_credentials` con scopes por ruta. Convive con Passport existente (misma tabla `oauth_access_tokens`). |
| ¿El feature puede romper flujos de e-commerce existentes? | ⚠️ Riesgo medio — el runner de actions es compartido con el board. El Dev indica "sin cambio de comportamiento para flows existentes" pero el refactor es significativo. |

---

## Tabla de Riesgos

| ID | Área | Riesgo | Descripción | Prioridad de testing | Justificación |
|----|------|--------|-------------|---------------------|---------------|
| R-001 | Auth / Token OAuth2 | 🔴 Crítico | Motor de tokens `client_credentials` → es la puerta de entrada a toda la API. Si falla, nada funciona. JWT RS256, revocación, scopes por ruta. | 1 (testear primero) | Sin auth funcional, la API entera queda expuesta o inaccesible. Comparte tabla con Passport → riesgo de regresión. |
| R-002 | Accounts compartidos por compañía | 🔴 Crítico | Modelo de accounts donde apps de la misma compañía comparten customers y conexiones. Cambio de semántica de `remote_id` (de unique global a unique por-compañía). Migración de BD. | 1 (testear primero) | Error aquí → datos cruzados entre compañías, violación de multi-tenancy. La migración de índices es irreversible en presencia de duplicados. |
| R-003 | Connectors autodescriptivos / Ejecución | 🔴 Crítico | Catálogo → actions → spec → ejecución síncrona contra proveedor externo. Selección automática de `Connection-Id`. Respuesta raw. | 2 | Core de la API — si la ejecución falla, la propuesta de valor del ticket queda nula. El direccionamiento namespaced añade complejidad. |
| R-004 | Seguridad / Aislamiento | 🔴 Crítico | Garantizar que una app de compañía A NO puede ver/ejecutar recursos de compañía B. Token desconocido → 401 uniforme (no leak de existencia). Account-Id ajeno → 404. | 2 | Exposición a API pública/controlada. Un fallo de aislamiento expone datos de clientes reales. |
| R-005 | PDF Templates API + UI | 🟠 Alto | Nuevo endpoint `/pdf-templates/{id}/spec` + `/pdf-templates/execute`. Render via servicio externo (pdfme/template-maker). UI con webcomponents nuevos (`gt-pdf-list`, `gt-pdf-workspace`). | 3 | Dependencia externa (R2, template-maker). Si el servicio está caído, la API debe manejar el error gracefully. UI nueva en webcomponents. |
| R-006 | Flows por API | 🟠 Alto | Listar flows con/sin `Account-Id`, ejecutar flows almacenados, flow INACTIVE → 409. | 3 | Runner compartido con board — riesgo de regresión en flows existentes del canvas. |
| R-007 | Mappers por API | 🟠 Alto | Ejecución síncrona de mappers por app/cuenta. | 4 | Menos superficie que connectors, pero igualmente crítico si se usa como parte de un pipeline. |
| R-008 | Migración BD (`remote_id`) | 🟠 Alto | Bajar unique global de `accounts.remote_id` y reemplazar por índices parciales (por-compañía + legacy sin compañía). El `down()` puede fallar si dos compañías comparten un `remote_id`. | 2 | Migración que toca producción. Irreversible en ciertos escenarios. Verificar con datos reales. |
| R-009 | Regresión: Flows del board | 🟠 Alto | El runner de actions fue refactorizado y es compartido entre board y DevApp API. El middleware de auth baja de 3 a 2 queries por request. | 3 | Cualquier bug aquí rompe TODOS los flows existentes. Regresión smoke test obligatorio. |
| R-010 | Regresión: Rutas Laravel existentes | 🟡 Medio | "Convivencia permanente: no se eliminó ningún endpoint" — verificar que `/api/2.0/app` existentes responden igual. | 4 | Baja probabilidad pero alto impacto. |
| R-011 | Limitación conocida: Laravel `remote_id` global | 🟡 Medio | Endpoint Laravel `POST /api/2.0/app/accounts` valida `remote_id` como unique global (Go permite por-compañía). Falla seguro (422). | 5 | Dev lo documenta como limitación, no bug. Verificar que el 422 es claro para el consumidor. |
| R-012 | UI diseñador PDF (webcomponents) | 🟡 Medio | Nuevo tab "PDF Templates" en vista de customer. Webcomponents `gt-pdf-list` + `gt-pdf-workspace`. Estados de error (motor caído). | 5 | UI nueva pero acotada. Riesgo bajo si los webcomponents están bien encapsulados. |
| R-013 | Rate limit de tokens | 🟢 Bajo | `DEVAPP_TOKEN_RATE` — rate limit por minuto (default 10). | 6 | Feature defensiva. Verificar que funciona, no bloqueante. |
| R-014 | Logs de auditoría | 🟢 Bajo | Cada denegación de token deja línea de auditoría (client id + IP). | 6 | Nice-to-verify, no bloqueante. |

---

## Edge Cases Identificados

### Auth / Tokens (R-001)

| # | Edge Case | Riesgo |
|---|-----------|--------|
| EC-01 | Token con scope parcial intenta acceder a endpoint que requiere scope diferente → debe dar 403 con nombre del scope faltante | 🔴 |
| EC-02 | Token expirado → debe dar 401 "Invalid token" (no "Token expired") | 🔴 |
| EC-03 | Token revocado → mismo 401 que expirado (uniformidad deliberada) | 🔴 |
| EC-04 | Body malformado en emisión de token → 400 | 🟠 |
| EC-05 | Client ID de un OAuth client que NO es del guard `apps` → 401 | 🟠 |
| EC-06 | Scope desconocido en petición de token → 422 | 🟠 |
| EC-07 | Rate limit excedido en endpoint de token → comportamiento esperado | 🟡 |

### Accounts compartidos (R-002)

| # | Edge Case | Riesgo |
|---|-----------|--------|
| EC-08 | App A crea customer → App B de la **misma compañía** lo ve y puede ejecutar con su conexión | 🔴 |
| EC-09 | App B intenta crear **mismo `remote_id`** que App A → debe dar 409 (unique por compañía) | 🔴 |
| EC-10 | App de **otra compañía** crea **mismo `remote_id`** → debe crearse sin conflicto | 🔴 |
| EC-11 | App de otra compañía intenta GET account de primera compañía → 404 (mismo formato que inexistente, no leak) | 🔴 |
| EC-12 | Migración con datos legacy (accounts sin `company_id`) → índice parcial preserva garantía | 🟠 |

### Connectors / Ejecución (R-003)

| # | Edge Case | Riesgo |
|---|-----------|--------|
| EC-13 | Ejecución sin `Account-Id` en ruta account-scoped → 400 | 🔴 |
| EC-14 | `Account-Id` de customer de otra compañía → 404 uniforme | 🔴 |
| EC-15 | Connector con 1 conexión → `Connection-Id` implícito | 🟠 |
| EC-16 | Connector con 0 conexiones → ejecución sin credenciales | 🟠 |
| EC-17 | Connector con >1 conexiones y sin `Connection-Id` → 409 con lista de candidatas | 🟠 |
| EC-18 | Alias `shipedge` resuelve igual que `app.shipedge` | 🟡 |
| EC-19 | `tenant.shipedge` → 404 (reservado para fase futura) | 🟡 |
| EC-20 | Connector NO vinculado a la app → 404 | 🟠 |
| EC-21 | Action NO habilitada en la app → 400 | 🟠 |

### PDF Templates (R-005)

| # | Edge Case | Riesgo |
|---|-----------|--------|
| EC-22 | Render de PDF sin scope → 403, sin `Account-Id` → 400, sin `schema_id` → 400 | 🟠 |
| EC-23 | Plantilla de otra compañía → 404 | 🟠 |
| EC-24 | Servicio template-maker caído → la API debe manejar error (no 500 opaco) | 🟠 |

---

## Preguntas para el Developer

### [LÓGICA DE NEGOCIO]

1. **Accounts compartidos por compañía** — ¿Si una compañía tiene 5 apps, y App A registra un customer con conexión OAuth a Shopify, App B puede ejecutar actions contra Shopify usando esa conexión? ¿O la conexión también está scoped al connector del app que la creó?

2. **Runner compartido board ↔ API** — Mencionas "sin cambio de comportamiento para flows existentes". ¿Puedes confirmar que los tests de integración existentes del runner pasan sin modificación?

3. **Migración `down()`** — Indicas que el `down()` puede fallar si dos compañías comparten un `remote_id`. ¿Hay un plan de contingencia si necesitamos revertir la migración en producción?

### [EDGE CASES]

4. **Scopes granulares** — ¿Todos los scopes están documentados en el Swagger/OpenAPI? ¿Hay un scope por cada operación o son agrupados (e.g. `app:connector-read` vs `app:connector-execute`)?

5. **`Connection-Id` como header** — El child task de Alex (UX Research) sugirió mover `Connection-Id` al body o renombrar a `X-Ion-Connection-Id`. ¿Cuál fue la decisión final? ¿Hay riesgo de que proxies strippeen el header?

6. **Flows INACTIVE** — Un flow INACTIVE devuelve 409 al intentar ejecutar. ¿El listado de flows incluye el estado (active/inactive) para que el consumidor pueda filtrar antes de ejecutar?

7. **Render PDF batch** — ¿El render batch (múltiples páginas) tiene un límite de páginas por request? ¿Qué pasa si el render toma más de X segundos (timeout)?

### [INTEGRACIÓN]

8. **Regresión de webcomponent de canales** — Mencionas que el `app-auth-component` sigue instalando/testeando normal. ¿Esto fue verificado manualmente o con tests automatizados?

9. **Swagger/OpenAPI** — ¿Dónde está el archivo actualizado? ¿Es generado automáticamente o manual? Necesitamos verificar que los payloads documentados coinciden con la implementación.

10. **Superficie eliminada** — Indicas que se eliminó `/developer-apps/{appId}/accounts` (5 rutas). ¿Hay consumidores actuales de esos endpoints que puedan romperse?

11. **Documentación en `ion-binaries/docs/features/devapp-api/`** — ¿Esta documentación es la fuente de verdad para los contratos de la API, o el Swagger es más reciente?

12. **Variables de entorno nuevas** — Hay 6+ variables nuevas requeridas (`PDF_GENERATE_URL`, `R2_*`, `DEVAPP_TOKEN_RATE`, `oauth-private.key`). ¿Están todas en `.env.example` actualizado? ¿Qué pasa si `oauth-private.key` no existe al arrancar?

---

## Contexto del Ticket (ClickUp)

### Divergencias detectadas entre descripción y comentarios

| AC Original (descripción) | Decisión en Comentarios | AC Reconciliado | Fuente |
|---|---|---|---|
| AC genéricos tipo "POST → 200/201" | Developer detalló 7 superficies de testing con pasos específicos y colecciones `.http` | Los AC de la descripción son insuficientes — usar los QA Instructions del comentario del Dev como base real | Comentario Rodolfo 2026-08-05 |
| No menciona modelo de accounts compartidos | Developer explica `accounts.company_id` → todas las apps de una compañía comparten customers | AC-5 NUEVO: Accounts compartidos por compañía | Comentario Rodolfo 2026-08-05 |
| No menciona PDF UI | Child task 86e1wfguh implementó UI de PDF con webcomponents | AC-11 NUEVO: UI diseñador PDF | Child task + comentario Alex 2026-07-17 |
| Menciona "CRUD de Mappers" como separado | Child task 86e1wfgxk (pdf mapper) — Rodolfo trabajó en él | ✅ Mappers **en scope** del Discovery (confirmado por QA Engineer) | Child task 86e1wfgxk + QA 2026-08-09 |

### Últimas decisiones relevantes

1. **2026-08-05**: Rodolfo publicó especificación técnica completa con 7 superficies de testing y 3 colecciones `.http` como herramientas de QA
2. **2026-07-17**: Alex completó prototipo de UI PDF (webcomponents `gt-pdf-list`/`gt-pdf-workspace`)
3. **2026-07-06**: Alex completó UX Research de App Channels con propuestas de mejora (naming, nesting, auth errors, pagination, Connection-Id header)
4. **2026-07-10**: Rodolfo compartió PR de cambios actuales en flow_binaries

---

## Recomendación

### Áreas de máxima atención (testear primero)

1. **Motor de tokens OAuth2** — Es el gate de acceso a toda la API. Testear la matriz completa de errores de emisión antes de cualquier otra cosa (colección `devapp-token.http`).

2. **Accounts compartidos por compañía** — Esta es la prueba central del modelo según el Dev. Requiere setup con **dos apps de la misma compañía + una de otra compañía**. Un fallo aquí es un fallo de aislamiento multi-tenant.

3. **Ejecución de connectors** — El viaje completo del developer: catálogo → action → spec → execute. Verificar especialmente el comportamiento del `Connection-Id` (implícito, explícito, 409).

### Herramientas de testing recomendadas

- **Colecciones `.http`** (REST Client VS Code) — El Dev las preparó como herramienta principal de QA. Están en la raíz de `gateway/`.
- **Seeder de demo** — `php artisan db:seed --class=DevAppPdfTemplateSeeder` para tener template de prueba.
- **DBeaver** — Para queries de verificación de BD (verificar migración de índices).

### Señales de alerta

- ✅ Mappers **confirmados en scope** por QA Engineer — Rodolfo trabajó en el child task 86e1wfgxk.
- ✅ Propuestas P1-P5 de Alex **fueron incorporadas** por Rodolfo (naming kebab, nesting, auth errors genéricos, pagination, Connection-Id). Verificar en el código.
- ⚠️ Superficie eliminada (`/developer-apps/{appId}/accounts`) — verificar que no hay consumidores activos.
