# Acceptance Criteria Consolidados — 86e1wfgam

> Motor de exposición por API (FASE 1) — DevApp API
> Módulo principal: Developer Apps
> Fecha: 2026-08-09

---

## Fuentes

| Fuente | Autor | Fecha | Peso |
|--------|-------|-------|------|
| Descripción del ticket | Marcel Herrera (PO) | 2026-06-15 | AC base (genéricos) |
| Comentario "Changes and Specifications" | Rodolfo Merlo Ali (Dev) | 2026-08-05 | **Fuente principal** — especificación técnica detallada con 7 superficies de QA |
| UX Research — App Channels | Alex Chura (Dev) | 2026-07-06 | Propuestas P1-P5 incorporadas por Rodolfo |
| Quick Prototype — PDF Template | Alex Chura (Dev) | 2026-07-17 | UI del diseñador PDF |
| Risk Triage | QA Catalyst | 2026-08-09 | Riesgos y edge cases |

---

## AC Originales (del ticket — descripción)

### AC-DESC-1: CRUD de App Connectors/Channels via API
> **Fuente**: Descripción del ticket por Marcel (PO)

```gherkin
Given un desarrollador tiene una aplicación externa con credenciales válidas
When realiza una petición POST al endpoint de connectors/channels con un payload válido
Then el sistema registra el nuevo recurso correctamente
And retorna un ID de referencia y una respuesta 200/201 según corresponda
```

**Evaluación**:
| ¿Verificable? | ¿Completo? | ¿Ambiguo? | Observación |
|:-:|:-:|:-:|---|
| ⚠️ Parcial | ❌ No | ⚠️ Sí | "Payload válido" no está definido. Solo menciona POST, pero el Dev implementó catálogo autodescriptivo + ejecución síncrona, no CRUD directo. El modelo real es: catálogo → actions → spec → execute. |

### AC-DESC-2: Gestión de mappers, boards o PDFs via API
> **Fuente**: Descripción del ticket por Marcel (PO)

```gherkin
Given una aplicación externa autorizada existe en el motor de aplicaciones de desarrollador
When solicita crear, consultar o actualizar un mapper, board o PDF
Then la API responde con el objeto solicitado o la confirmación de operación
And la respuesta cumple el esquema documentado para ese endpoint
```

**Evaluación**:
| ¿Verificable? | ¿Completo? | ¿Ambiguo? | Observación |
|:-:|:-:|:-:|---|
| ⚠️ Parcial | ❌ No | ⚠️ Sí | Demasiado genérico. El Dev implementó mappers con ejecución síncrona, PDFs con spec + render a R2, y flows con listado/ejecución. Boards no se mencionan en la implementación. |

### AC-DESC-3: Bloqueo de acceso no autorizado
> **Fuente**: Descripción del ticket por Marcel (PO)

```gherkin
Given una petición no incluye credenciales válidas o no tiene el scope requerido
When intenta consumir un endpoint de exposición Ionflow
Then el sistema rechaza la operación con un error 401 o 403
And no expone datos ni detalles internos del servicio
```

**Evaluación**:
| ¿Verificable? | ¿Completo? | ¿Ambiguo? | Observación |
|:-:|:-:|:-:|---|
| ✅ Sí | ⚠️ Parcial | ❌ No | Correcto pero incompleto. El Dev añadió: uniformidad de 401 (no distingue "App not found" de "Token revoked"), 403 con nombre del scope faltante, y 404 uniforme para aislamiento entre compañías. |

---

## AC Consolidados (descripción + comentarios + risk-triage)

> Organizados por las 7 superficies de testing definidas por el Developer.

---

### SUPERFICIE 1: Motor de Tokens y Fronteras de Auth

#### AC-1: Emisión de token OAuth2 válido
> **Fuente**: Comentario Rodolfo 2026-08-05, `devapp-token.http`

```gherkin
Given una app con client_id y client_secret válidos del guard "apps"
When solicita un token POST /api/2.0/app/token con grant_type=client_credentials y scopes válidos
Then el sistema emite un JWT RS256 (200)
And el token es compatible con Passport (misma tabla oauth_access_tokens)
And el token incluye los scopes solicitados
```

#### AC-2: Matriz completa de errores de emisión de token
> **Fuente**: Comentario Rodolfo 2026-08-05, `devapp-token.http`

```gherkin
Given diferentes escenarios de error en la emisión de token
Then el sistema responde:
  | Escenario | Status esperado |
  | Grant no soportado | 400 |
  | Sin scope | 400 |
  | Scope desconocido | 422 |
  | Secret incorrecto | 401 |
  | Client ID de otro guard (no "apps") | 401 |
  | Body malformado | 400 |
And ningún error expone datos internos del sistema
```

#### AC-3: Registro y listado de accounts (customers)
> **Fuente**: Comentario Rodolfo 2026-08-05, `devapp-token.http`

```gherkin
Given un token válido con scope de account
When registra un customer POST /accounts con remote_id
Then el sistema crea la cuenta (201)
And repetir con el mismo remote_id → 409
And GET /accounts lista los customers
And GET /accounts/{remoteId} retorna el detalle
```

#### AC-4: Header Account-Id obligatorio en rutas account-scoped
> **Fuente**: Comentario Rodolfo 2026-08-05

```gherkin
Given un token válido
When accede a una ruta account-scoped sin el header Account-Id
Then el sistema responde 400
When accede con Account-Id de una cuenta ajena (otra compañía)
Then el sistema responde 404 (mismo formato que inexistente)
```

#### AC-5: Scope faltante → 403 con nombre del scope
> **Fuente**: Comentario Rodolfo 2026-08-05

```gherkin
Given un token con scope parcial (ej: solo read, no execute)
When intenta acceder a un endpoint que requiere un scope diferente
Then el sistema responde 403 nombrando el scope faltante
```

#### AC-6: Token inválido → 401 uniforme
> **Fuente**: Comentario Rodolfo 2026-08-05 — "cambio de mensaje esperado, deliberado"

```gherkin
Given un token desconocido, revocado o expirado
When intenta acceder a cualquier endpoint protegido
Then el sistema responde 401 "Invalid token"
And NO distingue entre "App not found", "Token revoked" o "Token expired"
And el error es uniforme para no permitir enumerar clientes
```

---

### SUPERFICIE 2: Connectors Autodescriptivos (viaje del developer)

#### AC-7: Catálogo de connectors con namespacing
> **Fuente**: Comentario Rodolfo 2026-08-05, `devapp-connectors.http`

```gherkin
Given un token válido
When solicita GET al catálogo de connectors
Then los nombres vienen namespaced: "app.<tipo>"
And "app.shipedge" y alias "shipedge" resuelven al mismo connector
And "tenant.shipedge" → 404 (reservado para fase futura)
```

#### AC-8: Detalle de connector con actions habilitadas
> **Fuente**: Comentario Rodolfo 2026-08-05

```gherkin
Given un token válido y un connector vinculado a la app
When solicita detalle del connector CON Account-Id
Then la respuesta incluye actions habilitadas + conexiones del customer
When solicita detalle del connector SIN Account-Id
Then la respuesta incluye solo specs (sin conexiones)
```

#### AC-9: Ejecución de action con selección de conexión
> **Fuente**: Comentario Rodolfo 2026-08-05

```gherkin
Given un connector con action habilitada y Account-Id válido
When ejecuta la action:
  | Escenario | Connection-Id | Resultado |
  | 1 conexión disponible | (omitido) | Ejecución con conexión implícita |
  | Explícito | Connection-Id válido | Ejecución con esa conexión |
  | >1 conexiones | (omitido) | 409 con lista de candidatas |
Then la respuesta es RAW (payload del proveedor sin envelope {data})
```

#### AC-10: Fronteras de connectors
> **Fuente**: Comentario Rodolfo 2026-08-05

```gherkin
Given diferentes escenarios de error:
  | Escenario | Status |
  | Connector no vinculado a la app | 404 |
  | Action no habilitada | 400 |
  | Sin Account-Id en ruta account-scoped | 400 |
  | Customer de otra compañía | 404 |
  | Token read-only intentando ejecutar | 403 |
```

---

### SUPERFICIE 3: PDF Templates via API

#### AC-11: Spec y render de PDF templates
> **Fuente**: Comentario Rodolfo 2026-08-05, `devapp-pdf.http`

```gherkin
Given un template PDF existente (ej: seeder "Demo Order Receipt") y token válido con scope PDF
When solicita GET /pdf-templates/{id}/spec
Then recibe el shape autodescriptivo (como una action; params es un array)
When solicita POST /pdf-templates/execute con payload válido
Then recibe 200 con {filename, public_url}
And la URL pública descarga un PDF válido
And render batch (2+ páginas) funciona correctamente
```

#### AC-12: Fronteras de PDF
> **Fuente**: Comentario Rodolfo 2026-08-05

```gherkin
Given diferentes escenarios de error:
  | Escenario | Status |
  | Sin scope de PDF | 403 |
  | Sin Account-Id | 400 |
  | Sin schema_id | 400 |
  | Plantilla de otra compañía | 404 |
```

---

### SUPERFICIE 4: UI del Diseñador PDF

#### AC-13: Diseñador PDF en webcomponents
> **Fuente**: Child task 86e1wfguh, comentario Alex 2026-07-17

```gherkin
Given un usuario con permisos en la vista de customer
When navega al tab "PDF Templates"
Then ve la lista de templates (gt-pdf-list)
When crea un nuevo template (diálogo "Create PDF Template")
Then se abre el workspace embebido (gt-pdf-workspace) con el diseñador pdfme
When diseña, guarda y vuelve al listado
Then el listado refresca con el nuevo template
And estados de error visibles cuando el motor está caído (mensaje, no fallo silencioso)
```

---

### SUPERFICIE 5: Accounts Compartidos por Compañía (prueba central del modelo)

#### AC-14: Apps de la misma compañía comparten customers
> **Fuente**: Comentario Rodolfo 2026-08-05 — "la prueba central del modelo"

```gherkin
Given App A y App B son dos apps de la MISMA compañía (dos clientes OAuth del guard "apps")
When con token de App A → POST /accounts (registra customer, remote_id propio)
And con token de App B → GET /accounts
Then App B VE el customer que creó App A
And App B puede GET /accounts/{remoteId} del customer de App A
And App B puede ejecutar contra él usando su conexión
```

#### AC-15: Unicidad de remote_id por compañía
> **Fuente**: Comentario Rodolfo 2026-08-05

```gherkin
Given App A creó un customer con remote_id="CUST-001" (compañía X)
When App B (misma compañía X) intenta crear remote_id="CUST-001"
Then → 409 (unique por compañía)
When App C (compañía Y diferente) crea remote_id="CUST-001"
Then → 201 (sin conflicto)
And GET /accounts/CUST-001 desde compañía X → el customer de X
And GET /accounts/CUST-001 desde compañía Y → el customer de Y
And compañía X no ve la existencia del customer de Y (404 uniforme)
```

#### AC-16: Accounts en UI
> **Fuente**: Comentario Rodolfo 2026-08-05

```gherkin
Given un customer creado vía API
When un usuario con permiso READ_ACCOUNT navega a tenant → Accounts
Then la cuenta aparece en la lista
And sin permiso READ_ACCOUNT → la vista sigue gateada
```

#### AC-17: Matiz de ejecución cross-app
> **Fuente**: Comentario Rodolfo 2026-08-05 — "matiz importante"

```gherkin
Given App B quiere ejecutar contra el customer de App A (misma compañía)
When App B tiene el connector vinculado Y la action habilitada en su Configure
Then la ejecución funciona (los customers y conexiones se comparten)
When App B NO tiene el connector vinculado
Then → 404 del connector (comportamiento correcto, no fallo del modelo)
```

---

### SUPERFICIE 6: Flows por API

#### AC-18: Listado y ejecución de flows
> **Fuente**: Comentario Rodolfo 2026-08-05

```gherkin
Given un token válido
When GET /flows SIN Account-Id
Then retorna agregado de toda la app, cada ítem con account_remote_id
When GET /flows CON Account-Id
Then retorna flows filtrados para ese account
When POST execute un flow activo (status ACTIVE)
Then la ejecución es síncrona y retorna resultado
When POST execute un flow INACTIVE
Then → 409 "flow is not active" (pero sí se puede leer)
```

---

### SUPERFICIE 7: Regresión

#### AC-19: Regresión de flows del board
> **Fuente**: Comentario Rodolfo 2026-08-05 — "runner compartido"

```gherkin
Given flows existentes del board funcionan
When se despliega la nueva versión con el runner compartido
Then los flows del board ejecutan igual que antes (sin cambio de comportamiento)
And el middleware de auth baja de 3 a 2 queries por request (sin cambio funcional)
```

#### AC-20: Regresión de conexiones del webcomponent
> **Fuente**: Comentario Rodolfo 2026-08-05

```gherkin
Given conexiones del webcomponente de canales (app-auth-component) existentes
When se despliega la nueva versión
Then las conexiones siguen instalando/testeando normal
```

#### AC-21: Regresión de rutas Laravel existentes
> **Fuente**: Comentario Rodolfo 2026-08-05 — "no se eliminó ningún endpoint"

```gherkin
Given rutas Laravel de /api/2.0/app existentes
When se despliega la nueva versión
Then todas responden igual (convivencia permanente)
```

---

### SUPERFICIE 8: Migración de BD

#### AC-22: Migración de remote_id scoped a compañía
> **Fuente**: Comentario Rodolfo 2026-08-05, QA Instructions

```gherkin
Given la migración 2026_08_07_000001_scope_accounts_remote_id_to_company
When se ejecuta php artisan migrate
Then el unique global de accounts.remote_id se reemplaza por:
  - Índice único parcial (company_id, remote_id) para cuentas con dueño
  - Índice único parcial (remote_id) para cuentas legacy sin compañía
And las cuentas legacy conservan exactamente la garantía que tenían
And no hay sequential scan al listar cuentas de una compañía
```

---

## AC Propuestos (sugerencias del QA para acordar con Developer)

### AC-PROP-1: Rate limit de token
> **Justificación**: Variable `DEVAPP_TOKEN_RATE` mencionada en QA Instructions. Verificar que funciona.

```gherkin
Given DEVAPP_TOKEN_RATE configurado (default 10/min)
When se excede el rate limit con requests rápidos consecutivos
Then el sistema responde con el código de error apropiado (429)
And no se emiten tokens adicionales
```

### AC-PROP-2: Logs de auditoría de tokens
> **Justificación**: Mencionado en "Additional Resources" del Dev. Importante para seguridad.

```gherkin
Given una denegación de token
Then se registra una línea de auditoría con client_id + IP resuelta
And las ejecuciones registran AccountExecution con status y duración
```

---

## Limitaciones Conocidas (NO reportar como bug)

> Documentadas por el Developer. El equipo QA las conoce y acepta.

| Limitación | Comportamiento | Razón |
|------------|---------------|-------|
| Laravel POST `/api/2.0/app/accounts` valida `remote_id` como unique global | 422 cuando otra compañía ya usa el mismo `remote_id` (Go sí permite) | Se resuelve en ticket futuro que scopee controllers Laravel por compañía |
| `EXPLAIN` muestra Seq Scan con pocos registros | Planner descarta índice cuando recorrer la tabla es más barato | Correcto; beneficio aparece al crecer la tabla |

---

## Transformación AC → Casos de Test (resumen)

| AC | Happy Path | Edge Case | Negativo |
|----|-----------|-----------|----------|
| AC-1 (token válido) | Emitir JWT con scopes → 200 | Token con scope parcial | Grant inválido, secret malo, client no-apps |
| AC-3 (accounts) | Crear + listar + detalle | Repetir mismo remote_id → 409 | Sin scope de account |
| AC-4 (Account-Id) | Con Account-Id válido → funciona | Account-Id de cuenta ajena → 404 | Sin Account-Id → 400 |
| AC-7 (catálogo) | GET connectors namespaced | Alias vs canónico | tenant.* → 404 |
| AC-9 (ejecución) | Execute con 1 conexión implícita | >1 conexiones sin Connection-Id → 409 | Action no habilitada → 400 |
| AC-11 (PDF spec/render) | Spec + render simple → PDF válido | Render batch (2 páginas) | Sin schema_id → 400, plantilla ajena → 404 |
| AC-13 (UI PDF) | Crear → diseñar → guardar → listar | Motor caído → mensaje de error | — |
| AC-14 (accounts compartidos) | App A crea, App B ve | App B ejecuta con connector de A | App de otra compañía → 404 |
| AC-18 (flows) | Listar + ejecutar flow activo | Listar con/sin Account-Id | Flow INACTIVE → 409 |
| AC-22 (migración) | Migrate OK, índices parciales | Cuentas legacy sin company_id | — |
