# Risk Triage — 86e1wfhcq (IONF-1085) — API REST workspace/company FASE 2

## Resumen

| Campo | Valor |
|-------|-------|
| Módulo principal | Auth (PAT, companies, permisos) + API workspace |
| Módulos impactados | Boards, Connections, Executions, Webhooks, Data Store, PDF Templates, Billing (consumo) |
| Riesgo general | 🔴 **Crítico** |
| Total subtareas funcionales | 8 |
| Total edge cases identificados | 42 |
| Total preguntas para Developer | 15 |
| Contexto ClickUp | 2 comentarios principales (Marcel, Rodolfo) + 8 cierres de subtareas |
| Divergencias encontradas | 6 (3 bloqueantes resueltas + 3 informativas) |

---

## Análisis de Lógica de Negocio

| Pregunta | Análisis |
|----------|----------|
| ¿El feature respeta las reglas multi-tenant (company)? | 🔴 **CORE del ticket.** Todo el diseño gira en torno al aislamiento por company. El PAT liga usuario+company. Cada recurso se resuelve exclusivamente por la company del token. Es la regla de negocio #1 más expuesta a fallos. |
| ¿Afecta la ejecución de flows/nodos? | 🔴 **SÍ.** Los boards se ejecutan vía API, las actions y mappers crean CompanyExecution. Los nodos `ion.store.*` ahora comparten servicio con la API. La validación de connection en boards cambió. |
| ¿Hay impacto en connectors globales vs company? | 🟠 **SÍ.** El authoring permite crear/publicar/despublicar connectors de company. El `common` de auth-methods ahora está cifrado campo por campo. El motor lee cifrado transparentemente. |
| ¿Se tocan datos de ejecución (SQLite) o datos persistentes (PostgreSQL)? | 🔴 **SÍ.** Nueva tabla `workspace_tokens` en PG. `common` de `app_connections` ahora cifrado. Persistent Data con nuevo servicio compartido. Validación de structures. SQL injection fix. |
| ¿Hay impacto en el sistema de permisos por usuario/company? | 🔴 **SÍ.** 8 permisos nuevos: `execute-board`, `execute-app`, `create/read/update/delete-cron`, `publish-app`, `execute-pdf-template`. Sistema de doble llave PAT+TPerm. |
| ¿El feature puede romper flujos de e-commerce existentes? | 🟠 **POTENCIALMENTE.** Cambios transversales: precios centralizados, validación de connection en boards, cifrado de common, método HTTP en mayúsculas, respuesta sin envoltorio en devapp. |

---

## Análisis de Impacto por Módulo

| Área | Impacto | Riesgo | Justificación |
|------|---------|--------|---------------|
| **API workspace (Go)** | Superficie COMPLETAMENTE nueva: `/api/2.0/workspace/` con middleware PAT, 404 uniforme, doble llave | 🔴 Crítico | Cualquier falla en auth/aislamiento = fuga de datos cross-tenant |
| **API devapp (Go)** | Recursos únicos sin envoltorio (breaking change FR-028) | 🟠 Alto | Clientes existentes pueden romperse |
| **BD PostgreSQL** | Nueva tabla `workspace_tokens`, cifrado de `common` en `app_connections` | 🔴 Crítico | Migraciones, cifrado irreversible, retrocompatibilidad |
| **Auth / Permisos** | 8 permisos nuevos con backfill, catálogo scope→TPerm | 🔴 Crítico | Sin permisos correctos = 403 para todos |
| **Frontend (gateway-ion)** | Panel API Tokens en Settings, vistas de connectors migradas a Go, common enmascarado | 🟠 Alto | Migración de endpoints legacy→Go en UI |
| **Boards (motor)** | Validación de connection nueva, precios centralizados, `RunCompanyBoard` | 🔴 Crítico | Puede romper boards existentes con connections cruzadas |
| **Connections** | Endpoints workspace, filtros por app_name/tenant_app_name | 🟠 Alto | Aislamiento cross-company en connections |
| **Connectors (authoring)** | CRUD + validate + publish/unpublish, cifrado common, motor validación | 🔴 Crítico | Cifrado puede afectar connectors existentes, publicación puede romper |
| **Webhooks** | Listar/ver/habilitar/deshabilitar, migración Laravel→Go | 🟠 Alto | Rutas deprecated, bug fix del LIKE |
| **Schedules** | Listar/ver/pausar/reanudar, permisos CRUD-cron | 🟠 Alto | Bug fix del LIKE (cross-board deletion), pausa persiste |
| **Data Store (Persistent Data)** | Servicio compartido con nodos, validación de structures, CRUD registros | 🔴 Crítico | Refactor de lógica de nodos + SQL injection fix |
| **PDF Templates** | CRUD + import/export + imprimir con consumo | 🟠 Alto | Consumo exactamente 1 vez, inactive→409 |
| **Consumo / Billing** | Precios centralizados en tabla `executable`, consumo por CompanyExecution | 🔴 Crítico | Cobro incorrecto = impacto financiero directo |
| **Motor Go (transversal)** | Graceful shutdown, método HTTP mayúsculas, common cifrado transparente | 🟠 Alto | Cambios transversales que afectan a todo |
| **Canvas / Webcomponents** | Sin cambios | 🟢 Bajo | N/A |

---

## Tabla de Riesgos Priorizada

| ID | Área | Riesgo | Descripción | Prioridad | Justificación |
|----|------|--------|-------------|-----------|---------------|
| R-001 | Cross-company / IDOR | 🔴 Crítico | Un PAT de company A podría acceder a recursos de company B | 1 | Fuga de datos = vulnerabilidad crítica de seguridad |
| R-002 | PAT auth bypass | 🔴 Crítico | Token expirado/revocado/de app podría acceder a workspace | 1 | Bypass de autenticación |
| R-003 | Permisos nuevos no asignados | 🔴 Crítico | Sin backfill correcto, todos reciben 403 | 1 | Bloquea todo uso de la API |
| R-004 | Cifrado de common | 🔴 Crítico | Connectors existentes podrían dejar de funcionar si el cifrado rompe datos | 2 | Afecta todos los flows con connectors OAuth/API key |
| R-005 | Servicio compartido Data Store | 🔴 Crítico | Refactor de nodos ion.store.* podría romper boards existentes | 2 | Regresión en funcionalidad core del motor |
| R-006 | Consumo doble o nulo | 🔴 Crítico | Actions/boards/PDF podrían cobrar doble o no cobrar | 2 | Impacto financiero directo |
| R-007 | Bug LIKE en schedules | 🟠 Alto | El fix podría no cubrir todos los casos de IDs similares | 3 | Bug que borraba datos de otros boards |
| R-008 | Validación boards-connection | 🟠 Alto | Nueva validación podría rechazar boards que antes funcionaban | 3 | Regresión en flows de producción |
| R-009 | Respuesta devapp sin envoltorio | 🟠 Alto | Clientes que parsean el wrapper van a fallar | 3 | Breaking change en API existente |
| R-010 | Migración workspace_tokens | 🟠 Alto | Migración nueva en producción | 3 | Deploy requiere steps manuales |
| R-011 | UI connectors migrada a Go | 🟠 Alto | Vistas de edición ahora van a otro backend | 4 | Funcionalidad que ya existía podría romperse |
| R-012 | HTTP method uppercase | 🟠 Alto | Actions con método en minúsculas podrían comportarse diferente | 4 | Cambio en motor que afecta todas las llamadas |
| R-013 | SQL injection fix en Data Store | 🟠 Alto | El fix podría ser incompleto o romper consultas legítimas | 4 | Seguridad + regresión |
| R-014 | PDF render falla → no cobra | 🟡 Medio | Lógica de devolución de créditos cuando render falla | 5 | Edge case de billing |
| R-015 | Graceful shutdown | 🟡 Medio | Consumos en segundo plano podrían perderse al apagar | 5 | Edge case operativo |
| R-016 | Token limit (default 3) | 🟡 Medio | Usuarios podrían quedarse sin tokens activos | 6 | Configuración por ambiente |
| R-017 | Wizard crear connector sigue en Laravel | 🟡 Medio | Mezcla de backends podría causar inconsistencias | 6 | Migración parcial |
| R-018 | Template inactive → 409 | 🟡 Medio | Intentar imprimir un template inactivo | 6 | Edge case funcional |

---

## Edge Cases Identificados (42)

### Cross-Company y Seguridad (12)

| # | Edge Case | Subtarea |
|---|-----------|----------|
| EC-01 | PAT de company A intenta GET recurso de company B por ID válido | Todas |
| EC-02 | PAT de company A intenta enumerar IDs de company B | Todas |
| EC-03 | PAT con ID malformado (no UUID) → ¿qué error? | Todas |
| EC-04 | PAT expirado intenta operación → ¿401 o 403? | IONF-1279 |
| EC-05 | PAT revocado pero cacheado → ¿acceso temporal? | IONF-1279 |
| EC-06 | Usuario removido de company pero PAT no expirado | IONF-1279 |
| EC-07 | Permiso removido en medio de una request en curso | IONF-1279 |
| EC-08 | App token de /api/2.0/app intenta acceder a /api/2.0/workspace/ | IONF-1279 |
| EC-09 | PAT de workspace intenta acceder a /api/2.0/app | IONF-1279 |
| EC-10 | Account-Id header presente en request workspace → ¿se ignora o rechaza? | Todas |
| EC-11 | workspaceId en path → ¿qué pasa? | Todas |
| EC-12 | Dos companies con mismo nombre de connector → ¿filtrado correcto? | IONF-1284 |

### PAT y Autenticación (6)

| # | Edge Case | Subtarea |
|---|-----------|----------|
| EC-13 | Crear token #4 cuando WORKSPACE_TOKEN_LIMIT=3 | IONF-1279 |
| EC-14 | Token con TTL=0 (sin vencimiento) + revocación posterior | IONF-1279 |
| EC-15 | Token con todos los scopes vs token con scope mínimo | IONF-1279 |
| EC-16 | Crear token, mostrar, cerrar diálogo → ¿se puede volver a ver? | IONF-1279 |
| EC-17 | Revocar token que está siendo usado en request concurrente | IONF-1279 |
| EC-18 | Token con scope que no mapea a ningún TPerm | IONF-1279 |

### Boards y Executions (6)

| # | Edge Case | Subtarea |
|---|-----------|----------|
| EC-19 | Board con ejecución >5 min → 202 → consultar estado después | IONF-1285 |
| EC-20 | Board con connection de OTRO connector → ¿falla antes de llamar? | IONF-1285 |
| EC-21 | Ejecutar board sin permiso `execute-board` | IONF-1285 |
| EC-22 | Execution más vieja que EXECUTION_RETENTION_DAYS → ¿no aparece? | IONF-1286 |
| EC-23 | Action sin Connection-Id cuando declara connection → ¿400 sin cobrar? | IONF-1286 |
| EC-24 | Mapper con datos vacíos | IONF-1286 |

### Webhooks y Schedules (5)

| # | Edge Case | Subtarea |
|---|-----------|----------|
| EC-25 | Deshabilitar webhook de app → ¿llama al proveedor? (no debería) | IONF-1287 |
| EC-26 | Schedule pausado + guardar board → ¿la pausa sobrevive? | IONF-1287 |
| EC-27 | Schedule con fecha ya vencida → ¿409? | IONF-1287 |
| EC-28 | Board 1 y Board 12 schedules → guardar B1 no toca B12 | IONF-1287 |
| EC-29 | Board 1 y Board 10, 100, 11 → ¿el fix LIKE cubre todos? | IONF-1287 |

### Authoring Connectors (4)

| # | Edge Case | Subtarea |
|---|-----------|----------|
| EC-30 | Connector con name duplicado → 422 con mensaje específico | IONF-1288 |
| EC-31 | Publicar connector con action sin campos obligatorios | IONF-1288 |
| EC-32 | Borrar connector en uso por board+connection+suscripción | IONF-1288 |
| EC-33 | Auth-method guardado sin tocar secreto → ¿conserva el valor? | IONF-1288 |

### Persistent Data (5)

| # | Edge Case | Subtarea |
|---|-----------|----------|
| EC-34 | Structure con type desconocido → 422 | IONF-1291 |
| EC-35 | Registro con campo required vacío dentro de collection anidada | IONF-1291 |
| EC-36 | PUT vs PATCH: PUT reemplaza todo, PATCH combina arrays al final | IONF-1291 |
| EC-37 | Name con caracteres especiales (`first-name`, `a.b`, `x[0]`) en filtro SQL | IONF-1291 |
| EC-38 | Borrar store en uso por board → 409 con lista de boards | IONF-1291 |

### PDF Templates (4)

| # | Edge Case | Subtarea |
|---|-----------|----------|
| EC-39 | Schema pdfme inválido → 422 | IONF-1292 |
| EC-40 | Render falla → no cobra créditos ni impresión | IONF-1292 |
| EC-41 | Export desde UI → Import por API → ¿mismo JSON? | IONF-1292 |
| EC-42 | Editar nombre de template → ¿contador impresiones se resetea? (no debería) | IONF-1292 |

---

## Preguntas para el Developer (15)

### Lógica de Negocio

1. **PAT + Membresía:** Si un usuario tiene PAT activo y se lo remueve de la company, ¿se invalidan automáticamente todos sus PATs o solo se rechazan en runtime?
2. **Cifrado de common:** Al correr el comando de cifrado idempotente sobre datos existentes, ¿qué pasa con connectors que tienen common vacío o con formato no estándar?
3. **Precios centralizados:** ¿La tabla `executable` tiene los mismos precios para todos los ambientes o varía por company/tier?

### Edge Cases

4. **Connection-Id opcional:** Cuando una action requiere connection pero no se envía Connection-Id, ¿se usa alguna connection default o siempre es 400?
5. **Schedule bug LIKE:** ¿El fix cubre también board IDs numéricos como 1, 10, 100, 11, 111?
6. **Motor HTTP uppercase:** ¿Si un connector existente tiene method "post" en la BD, se normaliza al leer o se guardó en mayúsculas al crear?
7. **Devapp sin envoltorio:** ¿Hay documentación o changelog para que los clientes de /api/2.0/app se adapten al nuevo formato?

### Integración

8. **Wizard de crear connector en Laravel:** ¿El connector creado con el wizard Laravel es editado después desde Go? ¿Hay inconsistencias posibles en el formato de datos?
9. **Consumo en segundo plano + graceful shutdown:** ¿Si el servidor se apaga mientras un consumo está encolado, se pierde o se retoma al reiniciar?
10. **Regresión de nodos ion.store.* :** ¿Los tests que fijaron el comportamiento antes del refactor están en la suite de CI/CD?

### Seguridad

11. **Token prefix `iondwk_`:** ¿El server valida el prefix antes de intentar el SHA-256 lookup? ¿Un token sin prefix se rechaza rápido o pasa por todo el pipeline?
12. **Rate limiting:** ¿Hay rate limits diferenciados entre PAT y sesión Keycloak? ¿Un PAT comprometido puede hacer DDoS sin throttling?
13. **SQL injection fix en Data Store:** ¿El fix de names escapados en búsqueda cubre también LIKE patterns y JSON operators?
14. **Cifrado: key rotation:** ¿Está prevista la rotación de la clave de cifrado del common? ¿Qué pasa si la clave se pierde?
15. **PAT y logout:** ¿Si el usuario hace logout de Keycloak, los PATs siguen funcionando? (deberían, son independientes)

---

## Contexto del Ticket (ClickUp)

### Divergencias con resolución

| Divergencia | Resolución QA |
|-------------|---------------|
| Auditoría no implementada (NFS) | ✅ No bloqueante. Follow-up en otro ticket. |
| Laravel cambió más allá de migraciones | ✅ Aprobado por Tech Lead. Validar retrocompatibilidad. |
| IONF-1289 (IonMind) excluido | ✅ N/A para esta fase. |
| IONF-1293 (Templates company) excluido | ✅ N/A para esta fase. |
| Respuesta devapp sin envoltorio | ✅ Documentar como casos de regresión. |
| IONF-1295 QA independiente invalidada | ✅ QA se ejecuta por ticket, evidencia en padre. |

### Decisiones clave del cierre de subtareas

| Subtarea | Decisiones/Desviaciones del Developer |
|----------|---------------------------------------|
| IONF-1279 (PAT) | Token `iondwk_`, SHA-256, doble llave funciona sin reemitir token. Auditoría diferida. |
| IONF-1284 (Connections) | Filtro por app_name XOR tenant_app_name, nunca ambos. Borrador no aparece. |
| IONF-1285 (Boards) | Execute requiere `execute-board`. 200 si <5min, 202 si no. Trigger = `api`. |
| IONF-1286 (Executions) | `execute-app` nuevo. Action sin Connection-Id → 400 sin cobrar. Logs y control diferidos. |
| IONF-1287 (Webhooks) | Enable/disable migrado a Go, rutas Laravel `@deprecated`. Bug LIKE corregido. CRUD diferido a MCP. |
| IONF-1288 (Authoring) | Motor validación nuevo `packages/validation`. Name único+fijo. PATCH parcial. Auditoría diferida. |
| IONF-1291 (Data Store) | Servicio compartido con nodos. API valida strict, boards no. SQL injection fix. Búsqueda max 1000. |
| IONF-1292 (PDF Templates) | PATCH parcial (fix del contador). JSON pdfme validado server-side. Total listado ya no cuenta borrados. |

---

## Recomendación

### Orden de testing sugerido (por prioridad de riesgo)

1. **🔴 PAT + Cross-company (IONF-1279)** — Es el fundamento. Si falla, todo el resto es irrelevante.
2. **🔴 Cifrado de common + Motor (transversal)** — Puede romper TODOS los connectors existentes.
3. **🔴 Permisos nuevos + backfill** — Sin esto, todos los endpoints dan 403.
4. **🔴 Data Store servicio compartido (IONF-1291)** — Refactor de nodos core + SQL injection.
5. **🟠 Boards execute + Executions (IONF-1285/1286)** — Consumo y ejecución por API.
6. **🟠 Authoring connectors (IONF-1288)** — CRUD + validación + publish.
7. **🟠 Webhooks/Schedules + bug LIKE (IONF-1287)** — Bug fix + migración Go.
8. **🟠 PDF Templates (IONF-1292)** — CRUD + consumo + import/export.
9. **🟠 Connections y Connectors (IONF-1284)** — Catálogo + filtros.
10. **🟠 Regresión devapp /api/2.0/app** — Suite Fase 1 + respuesta sin envoltorio.
11. **🟠 UI (Settings, connectors, tenant)** — Validaciones visuales.
12. **🟡 Graceful shutdown** — Operativo.
