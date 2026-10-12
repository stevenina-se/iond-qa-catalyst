# Discovery — Reconciliación de AC con ClickUp

## Ticket: 86e1wfhcq (IONF-1085) — API REST de workspace/company de IOND (FASE 2)

> Generado: 2026-10-08
> Fuentes: Descripción del ticket + Comentario de Rodolfo Merlo Ali (2026-10-05)

---

## Resumen Ejecutivo

Este ticket es un **epic padre** que expone la REST API pública de company bajo `/api/2.0/workspace/`, usando Personal Access Tokens (PAT) con autorización de doble llave (scopes del token ∩ permisos actuales del usuario). Cubre **8 subtareas funcionales** que abarcan prácticamente **todos los módulos** del producto.

### Decisiones transversales vigentes

1. **Dominio y tenant** — Todo recurso se resuelve por la company del token. NO se acepta `Account-Id` ni `workspaceId` en paths.
2. **Principal** — Siempre un usuario. NO app tokens, service accounts ni client_credentials.
3. **Autenticación** — Personal Access Tokens (`iondwk_`) desde UI con sesión Keycloak, ligados a company, con scopes, TTL y revocación.
4. **Autorización** — Scopes efectivos = scopes PAT ∩ permisos TPerm actuales. Membresía revalidada en cada request.
5. **Auditoría** — ⚠️ **NO IMPLEMENTADA** (NFS no soporta escrituras). Registrar como follow-up.
6. **Consumo** — ConsumptionParams.Subscriber usando models.Morph. Cobra exactamente 1 vez.
7. **Implementación** — Go contiene dominio de company. Laravel cambió más de lo previsto (cast cifrado, seeder permisos) con aprobación del Tech Lead.
8. **Separación MCP** — `/api/2.0/mcp` reservado para IONF-1277.

---

## Divergencias Identificadas

| # | AC/Decisión Original | Decisión Final en Comentarios | Impacto QA | Fuente |
|---|---|---|---|---|
| D-1 | Auditoría mínima (helper logs) | NO implementada (NFS <50 MB/s) | ❌ No se puede validar. Evaluar para release | Rodolfo 2026-10-05 |
| D-2 | "Laravel no cambia salvo migraciones" | Se cambió AppConnection (cast cifrado), CompanyAppTrait, seeder permisos | ⚠️ Validar que cambios Laravel no rompen contratos existentes | Rodolfo 2026-10-05 |
| D-3 | IONF-1289 (IonMind workspace) en alcance | Sin endpoints, por decisión Tech Lead | ✅ No testear. Registrar como N/A | Rodolfo 2026-10-05 |
| D-4 | IONF-1293 (Templates company) en alcance | Excluido por decisión Tech Lead | ✅ No testear. Registrar como N/A | Rodolfo 2026-10-05 |
| D-5 | DoD: "Cada escritura emite auditoría" | Auditoría no implementada | ⚠️ Conflicto con DoD. Decisión QA requerida | Rodolfo 2026-10-05 |
| D-6 | Recurso único devapp con envoltorio | Ahora sin envoltorio (breaking?) | ⚠️ Validar impacto en clientes existentes de `/api/2.0/app` | Rodolfo 2026-10-05 |

---

## AC Consolidados por Familia

### Familia 1 — PAT y Autenticación (IONF-1279)

| ID | Acceptance Criteria | Fuente | Tipo |
|----|-------------------|--------|------|
| AC-1.1 | Un PAT válido (`iondwk_`) identifica usuario y company del token | Descripción | Original |
| AC-1.2 | Scopes efectivos = scopes PAT ∩ permisos TPerm actuales del usuario en la company | Descripción | Original |
| AC-1.3 | La membresía del usuario en la company se revalida en cada request | Descripción | Original |
| AC-1.4 | PAT revocado o vencido → 401 | Descripción + Comentarios | Original |
| AC-1.5 | Token se muestra UNA sola vez al crear. Si se pierde, crear otro | Comentarios | Nuevo |
| AC-1.6 | Límite de tokens activos por usuario+company (env `WORKSPACE_TOKEN_LIMIT`, default 3) | Comentarios | Nuevo |
| AC-1.7 | UI: Settings → API Tokens (crear, listar, revocar) | Comentarios | Nuevo |
| AC-1.8 | `GET /api/2.0/workspace/me` responde usuario y company del token | Comentarios | Nuevo |
| AC-1.9 | Quitar permiso al usuario → esa ruta responde 403 nombrando el permiso; devolver → funciona sin crear otro token | Comentarios | Nuevo |

### Familia 2 — Aislamiento y Seguridad Cross-company

| ID | Acceptance Criteria | Fuente | Tipo |
|----|-------------------|--------|------|
| AC-2.1 | No se acepta `Account-Id` ni `workspaceId` en paths de `/api/2.0/workspace/` | Descripción | Original |
| AC-2.2 | Recurso de otra company o inexistente → 404 uniforme (sin fuga de información) | Descripción + Comentarios | Original |
| AC-2.3 | ID malformado → mismo 404 uniforme | Comentarios | Nuevo |
| AC-2.4 | App tokens (de `/api/2.0/app`) NO obtienen acceso a `/api/2.0/workspace/` | Descripción | Original |
| AC-2.5 | Credenciales de workspace NO obtienen permisos sobre la API app | Descripción | Original |
| AC-2.6 | ⚠️ DESVIACIÓN: Auditoría NO implementada — logs de rechazo cross-tenant no están | Comentarios | Desviación |

### Familia 3 — Connections y Connectors (IONF-1284)

| ID | Acceptance Criteria | Fuente | Tipo |
|----|-------------------|--------|------|
| AC-3.1 | Listar connections filtrando por `app_name` y `tenant_app_name` | Comentarios | Nuevo |
| AC-3.2 | Listar y buscar connectors del catálogo | Comentarios | Nuevo |
| AC-3.3 | Ver un connector con sus actions | Comentarios | Nuevo |
| AC-3.4 | Ver contrato de action: `parameters_spec_json`, `output_spec_json`, `sample_json` con datos | Comentarios | Nuevo |

### Familia 4 — Boards y Executions (IONF-1285/1286)

| ID | Acceptance Criteria | Fuente | Tipo |
|----|-------------------|--------|------|
| AC-4.1 | Ejecutar board → 200 si termina en <5 min, 202 si excede | Comentarios | Nuevo |
| AC-4.2 | Ejecutar action (con y sin `Connection-Id`) y mapper | Comentarios | Nuevo |
| AC-4.3 | Cada ejecución aparece con `trigger_type = api` y cobra exactamente 1 vez | Comentarios | Nuevo |
| AC-4.4 | Sin permiso `execute-app` / `execute-board` → 403 | Comentarios | Nuevo |
| AC-4.5 | Filtrar executions por `status`, `board_id`, `trigger_type` y fechas | Comentarios | Nuevo |
| AC-4.6 | Executions más viejas que retención no aparecen (`EXECUTION_RETENTION_DAYS`, default 7) | Comentarios | Nuevo |
| AC-4.7 | NUEVO: Boards validan connection pertenece al connector correcto ANTES de llamar proveedor | Comentarios | Nuevo (código) |
| AC-4.8 | NUEVO: Nodo core en Preview cuesta 2 créditos, igual que producción | Comentarios | Nuevo (código) |

### Familia 5 — Webhooks y Schedules (IONF-1287)

| ID | Acceptance Criteria | Fuente | Tipo |
|----|-------------------|--------|------|
| AC-5.1 | Listar, ver, deshabilitar y habilitar webhooks por API y desde UI | Comentarios | Nuevo |
| AC-5.2 | Deshabilitar webhook de app NO llama al proveedor | Comentarios | Nuevo |
| AC-5.3 | Listar, ver, pausar y reanudar schedules | Comentarios | Nuevo |
| AC-5.4 | Schedule pausado no corre; la pausa sobrevive a guardar el board | Comentarios | Nuevo |
| AC-5.5 | Schedule vencido → 409 | Comentarios | Nuevo |
| AC-5.6 | BUG FIX: Guardar/borrar board 1 NO toca schedules de board 12 (fix del LIKE) | Comentarios | Bug Fix |

### Familia 6 — Authoring de Connectors (IONF-1288)

| ID | Acceptance Criteria | Fuente | Tipo |
|----|-------------------|--------|------|
| AC-6.1 | Crear connector con name duplicado → 422 "The name has already been taken." | Comentarios | Nuevo |
| AC-6.2 | Action inválida → 422 con todos los errores y su ruta | Comentarios | Nuevo |
| AC-6.3 | Auth-method: `common` sale como `••••`; en BD cada valor está cifrado, claves visibles | Comentarios | Nuevo |
| AC-6.4 | Guardar sin tocar un secreto lo conserva | Comentarios | Nuevo |
| AC-6.5 | `validate` no cambia nada; `publish` pasa draft→active; inactive queda | Comentarios | Nuevo |
| AC-6.6 | Sin permiso `publish-app` → 403 | Comentarios | Nuevo |
| AC-6.7 | Borrar/despublicar en uso por board, connection o suscripción → 409 con lista de quién lo usa | Comentarios | Nuevo |

### Familia 7 — Persistent Data (IONF-1291)

| ID | Acceptance Criteria | Fuente | Tipo |
|----|-------------------|--------|------|
| AC-7.1 | Structure: tipo desconocido, select sin opciones, names duplicados → 422 | Comentarios | Nuevo |
| AC-7.2 | Tipos aceptados: collection, select, binary, date (con formato). Name `first-name` válido | Comentarios | Nuevo |
| AC-7.3 | Registro sin campo required → 422 (también dentro de collection) | Comentarios | Nuevo |
| AC-7.4 | Select fuera de opciones → 422; date en formato incorrecto → 422 | Comentarios | Nuevo |
| AC-7.5 | Key repetida → 409; PUT reemplaza; PATCH combina (arrays al final, como nodo) | Comentarios | Nuevo |
| AC-7.6 | Campo no en structure → 422 por API; por board se guarda como antes | Comentarios | Nuevo |
| AC-7.7 | Borrar store en uso → 409 con board; borrar structure en uso → 409 | Comentarios | Nuevo |
| AC-7.8 | Regresión: nodos `ion.store.*` (add, update, get, delete, search, count) funcionan igual | Comentarios | Regresión |

### Familia 8 — PDF Templates (IONF-1292)

| ID | Acceptance Criteria | Fuente | Tipo |
|----|-------------------|--------|------|
| AC-8.1 | CRUD con schema pdfme inválido → 422; editar nombre no cambia contador impresiones | Comentarios | Nuevo |
| AC-8.2 | Exportar template y reimportar → mismo JSON. JSON de UI importable por API | Comentarios | Nuevo |
| AC-8.3 | `GET /pdf-templates/{id}/spec` muestra campos requeridos para imprimir | Comentarios | Nuevo |
| AC-8.4 | `POST /pdf-templates/execute` imprime, devuelve URL, cobra 2 créditos + 1 impresión exactamente 1 vez | Comentarios | Nuevo |
| AC-8.5 | Si render falla → no cobra créditos y devuelve la impresión | Comentarios | Nuevo |
| AC-8.6 | Template inactive → 409; sin `execute-pdf-template` → 403 | Comentarios | Nuevo |

### Familia 9 — Regresión, Transversales y UI

| ID | Acceptance Criteria | Fuente | Tipo |
|----|-------------------|--------|------|
| AC-9.1 | Suite devapp `/api/2.0/app` sigue pasando (incluido spec y execute PDF) | Descripción + Comentarios | Regresión |
| AC-9.2 | NUEVO: Recursos únicos de accounts responden SIN envoltorio | Comentarios | Cambio (potencial breaking) |
| AC-9.3 | NUEVO: Precios centralizados en tabla `executable` | Comentarios | Nuevo (código) |
| AC-9.4 | NUEVO: Graceful shutdown (SIGINT/SIGTERM): deja de aceptar, espera en curso, cierra | Comentarios | Nuevo |
| AC-9.5 | NUEVO: Motor lee `common` cifrado transparentemente; filas viejas en claro siguen leyéndose | Comentarios | Nuevo |
| AC-9.6 | NUEVO: Método HTTP de actions siempre en mayúsculas (post → POST) | Comentarios | Nuevo |
| AC-9.7 | UI: Cambiar de company sin recargar actualiza tokens, connectors y pantallas | Comentarios | Nuevo |
| AC-9.8 | UI: Diálogo de token no se cierra con Esc ni clic afuera sin confirmar | Comentarios | Nuevo |
| AC-9.9 | UI: Webhook con `/` en nombre se puede editar y borrar | Comentarios | Nuevo |
| AC-9.10 | UI: Auth-method `api_key` funciona correctamente | Comentarios | Nuevo |
| AC-9.11 | UI: Crear connector desde wizard sigue igual | Comentarios | Regresión |
| AC-9.12 | UI: Editar detalles, base, auth-method, action, webhook de connector funciona | Comentarios | Nuevo |
| AC-9.13 | UI: Action status ya no ofrece `deprecated` | Comentarios | Cambio |
| AC-9.14 | UI tenant: crear/editar structures, stores y PDF templates funciona con validación nueva | Comentarios | Nuevo |

---

## Pre-requisitos de Deploy (del comentario del Developer)

> ⚠️ Estos son necesarios para poder testear en staging.

1. **Gateway:** Correr migraciones globales `php artisan migrate` (crea `workspace_tokens`)
2. **Gateway:** Cargar permisos nuevos y asignarlos a usuarios existentes:
   - `execute-board`, `execute-app`, `create-cron`, `read-cron`, `update-cron`, `delete-cron`, `publish-app`, `execute-pdf-template`
3. **Gateway:** Cifrar `common` existente de `app_connections` (comando idempotente)
4. **Binaries:** `go mod download` + recompilar (dependencia nueva `jsonschema/v6`, módulo `packages/validation`)
5. **Binaries:** Variables de entorno opcionales:
   - `EXECUTION_RETENTION_DAYS` (default 7)
   - `WORKSPACE_TOKEN_LIMIT` (default 3)
6. **Frontend:** Build del frontend
7. **Post-deploy:** Borrar rutas Laravel marcadas `@deprecated IONF-1287` / `@deprecated IONF-1288` (wizard de crear connector NO se borra)

## Insumo de Testing

- `gateway/workspace-token.http` — Demo de requests numeradas con resultado esperado
- Crear token en Settings → API Tokens con todos los permisos para demo completa
- Para casos 403: crear segundo token sin el permiso específico

---

## Preguntas para el QA Engineer

1. **Auditoría (D-1/D-5):** La auditoría no fue implementada pero está en el DoD. ¿Cómo lo manejamos? ¿Lo aceptamos como follow-up documentado o es bloqueante?
2. **Respuesta sin envoltorio en devapp (D-6):** ¿Es un breaking change aceptable? ¿Hay clientes consumiendo ese formato?
3. **Alcance del Discovery:** Dado que este es un epic con 8 subtareas, ¿hacemos Discovery del padre consolidando o necesitamos Discovery individual por subtarea?
