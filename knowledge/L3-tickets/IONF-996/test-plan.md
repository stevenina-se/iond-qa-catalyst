# Test Plan — IONF-996

## Información del Ticket
- **ID**: IONF-996
- **Título**: Endpoints de Instalación de Grapps (API-First)
- **Módulos**: Connections, Integrations, Accounts
- **QA Engineer**: Steve Nina
- **Fecha del plan**: 2026-06-02
- **QA Points**: 3

## Resumen
- Total de casos: 30 (24 funcionales + 6 regresión)
- Tiempo estimado: ~90 min
- Artefactos de Discovery usados: Ninguno (ticket pasó directo a Deployment)
- Test Matrix: Generada en esta sesión (30 casos, 6 AC derivados)
- **Naturaleza**: 100% API testing (no hay cambios de UI) — se testea con requests HTTP directos

---

## Setup Previo (BLOQUE 0 — PREREQUISITOS)

> ⚠️ Este ticket es **API-Only**. No hay UI de Ion involucrada. Todo el testing se realiza con HTTP requests usando autenticación M2M (client_credentials).

### Paso 1: Obtener OAuth Client M2M

Necesitamos un OAuth client configurado con `client_credentials` grant type y los scopes necesarios. Opciones:

| Opción | Cómo |
|--------|------|
| **A. Client existente** | Buscar un OAuth client ya configurado con scopes `app:connection-*` y `app:integration-create` |
| **B. Crear client nuevo** | Via UI: Developer Apps → crear app → crear client → asignar scopes |
| **C. Usar Postman con token existente** | Si ya existe un token M2M de otra sesión |

**Scopes necesarios en el client:**
- `app:connection-read`
- `app:connection-create`
- `app:connection-update`
- `app:connection-delete`
- `app:integration-create`

### Paso 2: Obtener Token M2M

```bash
# Obtener token con client_credentials
POST {base_url}/oauth/token
Content-Type: application/json

{
  "grant_type": "client_credentials",
  "client_id": "{CLIENT_ID}",
  "client_secret": "{CLIENT_SECRET}",
  "scope": "app:connection-read app:connection-create app:connection-update app:connection-delete app:integration-create"
}
```

### Paso 3: Identificar datos de prueba

| Dato | Cómo obtenerlo | Notas |
|------|---------------|-------|
| `account.remote_id` | Query BD: `SELECT remote_id FROM accounts LIMIT 5;` o via API `GET /2.0/app/accounts` | Necesario para todas las rutas |
| `service_id` válido | Query BD: `SELECT id, name FROM services LIMIT 5;` | Para crear connections e integrations |
| OAuth Client M2M | Developer Apps UI o BD | Con todos los scopes del Paso 1 |
| Token M2M | POST /oauth/token | Duración del token a verificar |

### Paso 4: Variables de Entorno para la Sesión

```
BASE_URL = https://dev-app.ionflow.io/api/2.0/app
ACCOUNT_REMOTE_ID = {a obtener}
SERVICE_ID = {a obtener}
TOKEN = {a obtener}
```

---

## Orden de Ejecución

### BLOQUE 1 — SMOKE TESTS (ejecutar primero, si falla → escalar)

> Verifican que los endpoints existen, responden, y la auth M2M funciona.

| □ | ID | Caso | Prioridad |
|---|-----|------|-----------| 
| □ | TC-023 | Acceso sin token → 401 Unauthorized | 🔴 |
| □ | TC-001 | Listar connections de un account (GET) | 🔴 |
| □ | TC-007 | Instalar integración para un account (POST) | 🔴 |

> **GATE**: Si alguno falla aquí → PARAR. Reportar al dev. No continuar con el resto.

### BLOQUE 2 — HAPPY PATH — Connections CRUD (verificar flujo principal)

| □ | ID | Caso | Prioridad |
|---|-----|------|-----------| 
| □ | TC-003 | Crear connection con todos los campos | 🔴 |
| □ | TC-002 | Ver detalle de la connection creada | 🔴 |
| □ | TC-004 | Actualizar connection CON nuevo secreto | 🔴 |
| □ | TC-005 | Actualizar connection SIN secreto → preserva el original | 🔴 |
| □ | TC-006 | Eliminar connection | 🔴 |
| □ | TC-008 | Listar con paginación (per_page, order_by, order_direction) | 🟠 |

> **Flujo sugerido**: Crear (TC-003) → Leer (TC-002) → Actualizar con secreto (TC-004) → Actualizar sin secreto (TC-005) → Listar (TC-008) → Eliminar (TC-006). Este orden genera un CRUD completo en secuencia natural.

### BLOQUE 3 — EDGE CASES (verificar bordes)

| □ | ID | Caso | Prioridad |
|---|-----|------|-----------| 
| □ | TC-009 | Crear connection sin campo `data` (opcional) | 🟠 |
| □ | TC-010 | Crear connection sin campo `metadata` (opcional) | 🟠 |
| □ | TC-011 | Instalar grapp con payload mínimo | 🟠 |
| □ | TC-012 | Listar connections de account vacío | 🟠 |
| □ | TC-013 | Actualizar solo el `name` (campos restantes preservados) | 🟠 |
| □ | TC-015 | Verificar preservación de tipos JSON (number, boolean, array) | 🟠 |
| □ | TC-014 | JSON grande en `data` y `metadata` (~50KB) | 🟡 |

### BLOQUE 4 — NEGATIVOS Y SEGURIDAD (verificar que NO se puede romper)

| □ | ID | Caso | Prioridad |
|---|-----|------|-----------| 
| □ | TC-016 | Crear sin `service_id` → 422 | 🔴 |
| □ | TC-017 | Crear sin `name` → 422 | 🔴 |
| □ | TC-018 | Scope incorrecto → 403 Forbidden | 🔴 |
| □ | TC-021 | Instalar integración sin `service_id` → 422 | 🔴 |
| □ | TC-022 | Mass assignment (id, account_id, created_at inyectados) → IGNORADOS | 🔴 |
| □ | TC-024 | App viene del token, no del body → app_id del body IGNORADO | 🔴 |
| □ | TC-019 | Account inexistente → 404 | 🟠 |
| □ | TC-020 | Connection inexistente → 404 (GET, PUT, DELETE) | 🟠 |

> **⚠️ CRÍTICO**: TC-022 (mass assignment) y TC-024 (app del token) son los tests de seguridad más importantes. Si fallan = vulnerabilidad.

### BLOQUE 5 — REGRESIÓN (verificar que no rompimos nada)

| □ | ID | Caso | Prioridad |
|---|-----|------|-----------| 
| □ | REG-001 | CRUD tenant connections sigue funcionando | 🔴 |
| □ | REG-002 | Webcomponent integrations (install/uninstall) siguen funcionando | 🔴 |
| □ | REG-005 | Go runtime lee connections creadas via nuevos endpoints | 🔴 |
| □ | REG-003 | App API integrations existentes (GET, action, update) | 🟠 |
| □ | REG-004 | OAuth tokens con scopes existentes no se rompieron | 🟠 |
| □ | REG-006 | Legacy integrations (v1.0 con user_id) siguen funcionando | 🟠 |

> **Nota REG-005**: Este es el riesgo más crítico del ticket. Si la columna `connection` no se escribe correctamente, el motor Go no puede autenticar los grapps. Para verificarlo necesitamos crear una connection → intentar que un grapp la use (o verificar directamente en BD que la columna tiene valor encriptado).

### BLOQUE 6 — DB EVIDENCE (queries de verificación)

| □ | ID | Query | Verificar |
|---|-----|-------|-----------| 
| □ | DB-001 | `SELECT connection, data FROM connections WHERE id = ?` | `connection` encriptado, `data` espejo |
| □ | DB-002 | `SELECT app_id, account_id, user_id, configuration FROM integrations WHERE id = ?` | app del token, user_id NULL, config `{}` |
| □ | DB-003 | `SELECT id, account_id FROM connections WHERE id = ?` (post mass-assignment) | account_id del binding, NO del body |
| □ | DB-004 | `SELECT user_id FROM integrations WHERE user_id IS NOT NULL LIMIT 3` | Integrations legacy con user_id preservadas |

---

## Datos Necesarios

| Dato | Cómo obtenerlo | Notas |
|------|---------------|-------|
| OAuth Client M2M | Developer Apps → crear app → crear client con scopes | Necesita los 5 scopes listados arriba |
| Account remote_id | BD: `SELECT remote_id FROM accounts LIMIT 5` o `GET /2.0/app/accounts` | Binding de ruta para todos los endpoints |
| Service ID válido | BD: `SELECT id, name FROM services WHERE deleted_at IS NULL LIMIT 5` | Para crear connections e integrations |
| Service ID inválido | Usar ID que no exista (ej: 99999) | Para tests negativos |
| Account remote_id inexistente | Usar string que no exista (ej: `INVALID_REMOTE_ID_QA`) | Para TC-019 |
| Token con scope limitado | Generar token con solo `app:connection-read` | Para TC-018 (scope insuficiente) |
| Usuario Company (staging) | `.env`: `skuanquis@gmail.com` | Para regresión de endpoints tenant |

---

## Criterios de Aprobación/Rechazo

### ✅ APROBACIÓN
- TODOS los smoke tests (BLOQUE 1) pasan
- TODOS los happy path (BLOQUE 2) pasan
- Al menos 80% de los edge cases (BLOQUE 3) pasan (≥6 de 7)
- TODOS los negativos y seguridad (BLOQUE 4) pasan
- TODOS los casos de regresión (BLOQUE 5) pasan
- DB evidence confirma integridad de datos (BLOQUE 6)

### ❌ RECHAZO
- Algún smoke test falla → **rechazo inmediato**
- Happy path falla → **rechazo**
- Negativo/seguridad falla → **rechazo** (especialmente TC-022 mass assignment y TC-024 app del token)
- Regresión falla → **rechazo con análisis de impacto**
- DB evidence muestra datos corruptos → **rechazo**

### ⚠️ APROBACIÓN CON OBSERVACIONES
- Edge case menor falla (TC-014 JSON grande) → aprobar con bug registrado
- REG-005 (Go runtime) no verificable end-to-end → aprobar si BD evidence es correcta + documentar
- Documentación API no renderiza correctamente → aprobar con observación

---

## Estimación de Tiempo

| Bloque | Casos | Tiempo estimado |
|--------|-------|-----------------|
| Setup (token, datos) | — | ~15 min |
| Smoke tests | 3 | ~5 min |
| Happy path (CRUD + install) | 6 | ~15 min |
| Edge cases | 7 | ~15 min |
| Negativos y seguridad | 8 | ~15 min |
| Regresión | 6 | ~15 min |
| DB evidence | 4 | ~10 min |
| **Total** | **34** | **~90 min** |

---

## Herramientas de Ejecución

| Herramienta | Uso |
|-------------|-----|
| **Playwright MCP (Canal 1)** | Ejecutar HTTP requests directos (navigate → API calls) |
| **DBeaver** | Queries de verificación BD (PostgreSQL via SSH tunnel) |
| **Postman** (alternativa) | Si el QA Engineer prefiere ejecutar requests manualmente |

### Método recomendado: Playwright MCP

La IA puede ejecutar los requests HTTP directamente usando `browser_evaluate` o `browser_navigate` del Playwright MCP, capturando los responses como evidencia. Esto es más eficiente que Postman para 30+ test cases.

Flujo por test case:
1. IA ejecuta el request HTTP
2. Captura response (status code, body)
3. Valida contra resultado esperado
4. QA Engineer supervisa y confirma resultado
5. Se registra en test-results.csv

---

## Cómo Ejecutar y Reportar

### Formato de reporte — CSV

```
ID,Módulo,AC,Tipo,Caso,Prioridad,Estado,Comentario,Fecha
```

**Valores de Estado**:
- `PASS` — El caso pasó como se esperaba
- `FAIL` — El caso falló (describir en Comentario)
- `SKIP` — No se ejecutó (justificar en Comentario)
- `BLOCKED` — No se pudo ejecutar por dependencia
- `PASS_OBS` — Pasó con observaciones menores

### Entregables al finalizar

1. **CSV con resultados** → `L3-tickets/IONF-996/test-results.csv`
2. **QA Report** → `L3-tickets/IONF-996/qa-report.md` (generado con `sprint-testing/report`)
3. **Screenshots/Evidence** → capturados durante la sesión

---

## Estado

⏳ Plan creado — **esperando aprobación del QA Engineer para iniciar ejecución**
