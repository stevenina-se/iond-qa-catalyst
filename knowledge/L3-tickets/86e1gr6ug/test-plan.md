# Test Plan — 86e1gr6ug

## Información del Ticket
- ID: 86e1gr6ug
- Título: Mejoras de la interface en ionflow dualtrack
- Módulos: boards, pdf-templates, connections, integrations, keys, accounts, developer-apps, services
- QA Engineer: Steve Nina
- Fecha del plan: 2026-06-08
- Track: Discovery → preparado para Deployment
- Branches: `IONF-1030` en gateway, gateway-ion, flow_binaries

## Resumen
- Total de casos: 68 (55 funcionales + 3 bloqueados + 10 regresión)
- Tiempo estimado: ~6.5 horas (390 min)
- Artefactos de Discovery usados: risk-triage.md, ac-consolidated.md, test-matrix.md, test-matrix.csv

---

## Orden de Ejecución

### BLOQUE 1 — SMOKE TESTS (ejecutar primero — si falla → escalar)

> Si algún smoke test falla, DETENER la sesión e informar al Developer.

| # | TC | Descripción | Prioridad |
|---|-----|-------------|-----------|
| □ | REG-009 | Login SSO Keycloak funciona | 🔴 |
| □ | REG-001 | Lista de boards (/workflows) carga correctamente | 🔴 |
| □ | REG-002 | Crear flow nuevo funciona post-migraciones | 🔴 |
| □ | TC-001 | Badge de ejecución exitosa visible en lista de boards | 🔴 |
| □ | TC-005 | Switch activo/pausado independiente del badge de ejecución | 🔴 |

### BLOQUE 2 — HAPPY PATH CRÍTICO (core del ticket)

> Verificar las funcionalidades principales de cada EPIC.

**EPIC 1 — Boards Telemetry**

| # | TC | Descripción | Prioridad |
|---|-----|-------------|-----------|
| □ | TC-006 | Cambiar estado sin corromper grafo (Payload Diet safety) | 🔴 |
| □ | TC-007 | Puntero `last_execution_id` actualizado post-ejecución (+ query BD) | 🔴 |
| □ | TC-008 | Estado terminal `completed` en Go | 🔴 |
| □ | TC-010 | `execution_time` > 0 (bugfix confirmado — + query BD) | 🔴 |
| □ | TC-011 | Payload Diet — response con grafo reducido (DevTools Network) | 🟠 |
| □ | TC-014 | Expansión de fila — carga flow completo con Used Apps | 🟠 |
| □ | TC-016 | Clonar flow (endpoint nativo `replicate()`) | 🟠 |

**EPIC 2 — PDF Templates**

| # | TC | Descripción | Prioridad |
|---|-----|-------------|-----------|
| □ | TC-025 | Telemetría de generación incrementa post-render (+ query BD) | 🔴 |
| □ | TC-019 | Formato y orientación derivados del schema pdfme | 🟠 |
| □ | TC-022 | Badge "En uso" para template utilizado | 🟠 |
| □ | TC-026 | Preview con proporción real y campos dinámicos | 🟠 |
| □ | TC-028 | Clonar PDF Template (endpoint nativo Go, nombre + " (copy)") | 🟠 |
| □ | TC-029 | Payload Diet PDF — lista sin JSONB pesado | 🟠 |

**EPIC 3 — Unified Search**

| # | TC | Descripción | Prioridad |
|---|-----|-------------|-----------|
| □ | TC-032 | Búsqueda unificada en Connections (Enter-only) | 🟠 |
| □ | TC-033 | Búsqueda unificada en Integrations | 🟠 |
| □ | TC-042 | FTS PostgreSQL — búsqueda con acentos (`unaccent`) | 🟠 |
| □ | TC-044 | ILIKE search tenant-scoped (aislamiento por company) | 🔴 |
| □ | TC-039 | URL con `?search=` al cargar — sincronización | 🟠 |

**EPIC 4 — UI Polish**

| # | TC | Descripción | Prioridad |
|---|-----|-------------|-----------|
| □ | TC-050 | Reactivity fix — sin layout shifts al escribir | 🟠 |
| □ | TC-046 | Keyboard navigation en búsqueda (A11y) | 🟡 |

### BLOQUE 3 — EDGE CASES (verificar bordes)

| # | TC | Descripción | Prioridad |
|---|-----|-------------|-----------|
| □ | TC-002 | Badge warning vs error (diferenciación visual) | 🟠 |
| □ | TC-003 | Badge error (propagación StatusError) | 🟠 |
| □ | TC-004 | Flow sin ejecuciones (NULL — estado vacío) | 🟠 |
| □ | TC-009 | Estado terminal StatusWarning (falla parcial de nodo) | 🟠 |
| □ | TC-012 | Payload Diet performance con muchos flows | 🟡 |
| □ | TC-013 | Poda ejecución — ON DELETE SET NULL (+ query BD) | 🟠 |
| □ | TC-015 | Expansión fila — flow sin apps (estado vacío) | 🟡 |
| □ | TC-020 | Schema vacío/malformado en adaptador pdfme | 🟠 |
| □ | TC-021 | Dimensiones custom no mapeables | 🟡 |
| □ | TC-023 | Badge "Nunca usado" (`generation_count = 0`) | 🟡 |
| □ | TC-024 | Etiqueta "Borrador" (template sin variables) | 🟡 |
| □ | TC-027 | Preview con dimensiones extremas | 🟡 |
| □ | TC-038 | Búsqueda Enter sin texto | 🟡 |
| □ | TC-045 | ILIKE con caracteres especiales `% _ \` | 🟠 |
| □ | TC-047 | Motion reduce — sin animaciones | 🟡 |
| □ | TC-054 | Responsividad 768px tablet | 🟡 |
| □ | TC-055 | Responsividad 375px mobile | 🟡 |

### BLOQUE 4 — NEGATIVOS (verificar que NO se pueda romper)

| # | TC | Descripción | Prioridad |
|---|-----|-------------|-----------|
| □ | TC-043 | FTS — intento de inyección SQL | 🔴 |
| □ | TC-017 | Clonar flow sin permisos (403) | 🟡 |
| □ | TC-040 | Búsqueda sin resultados (estado vacío) | 🟡 |

### BLOQUE 5 — REGRESIÓN (verificar que no rompimos nada)

| # | TC | Descripción | Prioridad |
|---|-----|-------------|-----------|
| □ | REG-003 | Editar flow existente (canvas carga post-Payload Diet) | 🟠 |
| □ | REG-004 | Ejecutar flow Production (estados terminales + UPDATE) | 🔴 |
| □ | REG-005 | Ver historial de ejecuciones | 🟠 |
| □ | REG-006 | Crear/editar PDF template (CRUD intacto post-columnas) | 🟠 |
| □ | REG-007 | Generar PDF desde nodo en flow (telemetría no afecta) | 🟠 |
| □ | REG-008 | CRUD de connections (post-ListSearchInput) | 🟠 |
| □ | REG-010 | Navegación general entre módulos (sidebar) | 🟠 |

### BLOQUE 6 — REMAINING SEARCH SCREENS + UX

| # | TC | Descripción | Prioridad |
|---|-----|-------------|-----------|
| □ | TC-034 | Búsqueda en Keys | 🟡 |
| □ | TC-035 | Búsqueda en Accounts | 🟡 |
| □ | TC-036 | Búsqueda en Developer Apps | 🟡 |
| □ | TC-037 | Búsqueda en Services | 🟡 |
| □ | TC-041 | Lazy Catalog con cooldown 30s | 🟡 |
| □ | TC-030 | Exportar JSON de template | 🟡 |
| □ | TC-031 | Columnas ordenables en PDF Templates | 🟡 |
| □ | TC-018 | Graph Utils — triggers y sinks | 🟡 |
| □ | TC-048 | Safety — pointer-events-none durante recarga | 🟡 |
| □ | TC-049 | Dark Mode — contraste enlaces/superficies | 🟡 |
| □ | TC-051 | PrimeVue `pt` — sin hacks CSS (code review) | 🟡 |
| □ | TC-052 | Tooltips en elementos interactivos | 🟡 |
| □ | TC-053 | Responsividad 1920px desktop | 🟡 |

### BLOQUE 7 — DB EVIDENCE (queries de verificación)

| # | Query | Verificar |
|---|-------|-----------|
| □ | DB-001 | `last_execution_id` actualizado post-ejecución (TC-007) |
| □ | DB-002 | `execution_time > 0` en ejecuciones recientes (TC-010) |
| □ | DB-003 | `ON DELETE SET NULL` funciona correctamente (TC-013) |
| □ | DB-004 | `generation_count` incrementa post-render (TC-025) |
| □ | DB-005 | Clon PDF con `generation_count = 0` (TC-028) |
| □ | DB-006 | Índice GIN existe en tabla flows (TC-042) |
| □ | DB-007 | Wrapper IMMUTABLE de `unaccent` existe (TC-042) |
| □ | DB-008 | Flow creado con `last_execution_id = NULL` (REG-002) |

### BLOQUE PENDIENTE — BLOQUEADOS (esperar Developer)

| # | TC | Pregunta Pendiente | Prioridad |
|---|-----|--------------------|-----------|
| ⏳ | TC-PD1 | ¿Derivación de formato sin JSONB en lista? | 🟠 |
| ⏳ | TC-PD2 | ¿Switch de estado PATCH o PUT? ¿Cómo evita sobrescribir grafo? | 🔴 |
| ⏳ | TC-PD3 | ¿Migración FTS reversible? ¿Impacto en escritura? | 🟡 |

---

## Datos Necesarios

| Dato | Cómo obtenerlo | Notas |
|------|---------------|-------|
| Credenciales Company | `.env` del repo `ionflow-qa-catalyst` | `IONFLOW_COMPANY_USERNAME` / `PASSWORD` |
| Credenciales Admin | `.env` del repo `ionflow-qa-catalyst` | `IONFLOW_ADMIN_USERNAME` / `PASSWORD` |
| URL staging | `.env` → `IONFLOW_ENVIRONMENT_URL` | Verificar que IONF-1030 esté desplegado |
| Flow de prueba (con nodos) | Crear en staging o usar uno existente | Necesita: trigger + al menos 2 nodos + connector |
| Flow con nodo PDF | Crear o usar existente | Necesita: nodo de renderizado de PDF template |
| PDF Template con schema | Crear con pdfme (A4 vertical) | Para TC-019 a TC-031 |
| PDF Template sin variables | Crear sin campos dinámicos | Para TC-024 (Borrador) |
| Usuario sin permisos | Crear o usar existente sin `create-board` | Para TC-017 |
| Acceso DBeaver | SSH tunnel configurado al tenant schema | Para queries BD (Bloque 7) |
| Flow con nombre acentuado | Crear: "Ejecución automática" | Para TC-042 (FTS unaccent) |

### Prerequisitos de Ambiente

| Check | Estado |
|-------|--------|
| □ Branch `IONF-1030` desplegada en staging (gateway) | ⬜ |
| □ Branch `IONF-1030` desplegada en staging (gateway-ion) | ⬜ |
| □ Branch `IONF-1030` desplegada en staging (flow_binaries) | ⬜ |
| □ Migraciones ejecutadas (FK, GIN, columnas PDF) | ⬜ |
| □ Acceso DBeaver funcional al tenant schema | ⬜ |

---

## Criterios de Aprobación/Rechazo

### ✅ APROBADO si:
- TODOS los smoke tests pasan (Bloque 1)
- TODOS los happy path críticos pasan (Bloque 2)
- Al menos 80% de los edge cases pasan (Bloque 3)
- TODOS los negativos pasan — no se puede romper el sistema (Bloque 4)
- TODOS los casos de regresión pasan (Bloque 5)
- DB evidence confirma integridad de datos (Bloque 7)

### ❌ RECHAZADO si:
- Algún smoke test falla → **rechazo inmediato**
- Happy path crítico falla → **rechazo**
- Negativo falla (inyección SQL exitosa, datos de otra company visibles) → **rechazo crítico**
- Regresión falla (canvas roto, login roto, CRUD roto) → **rechazo con análisis de impacto**
- DB evidence muestra datos corruptos (grafo sobrescrito, FK inconsistente) → **rechazo**

### ⚠️ APROBADO CON OBSERVACIONES si:
- Edge case falla pero no es bloqueante → aprobar con bug registrado
- Problema visual menor (tooltip mal posicionado, contraste en dark mode) → aprobar con observación
- TC bloqueado (PD) no se pudo ejecutar → aprobar con condición de follow-up
- Feature de búsqueda funciona en 4/6 pantallas pero falla en 2 → aprobar con bugs

---

## Estimación de Tiempo

| Bloque | Casos | Tiempo estimado | Notas |
|--------|-------|-----------------|-------|
| Smoke tests | 5 | ~20 min | Quick checks. Si falla → parar |
| Happy path crítico | 22 | ~120 min | Core del testing. Incluye ejecuciones de flows |
| Edge cases | 17 | ~90 min | Incluye manejo de estados vacíos y schemas |
| Negativos | 3 | ~20 min | Inyección SQL, permisos, estados vacíos |
| Regresión | 7 | ~45 min | CRUD existente + navegación |
| Remaining + UX | 13 | ~60 min | Búsqueda en 4 pantallas restantes + UX polish |
| DB evidence | 8 queries | ~25 min | Queries en DBeaver |
| Setup de datos | — | ~10 min | Crear flows/templates de prueba |
| **Total** | **68 + 8 queries** | **~390 min (~6.5h)** | Distribuible en 2 sesiones |

### Distribución sugerida

| Sesión | Bloques | Tiempo | Foco |
|--------|---------|--------|------|
| **Sesión 1** (~3.5h) | Smoke + Happy Path + Edge Cases + Negativos | ~250 min | Core funcional — decidir si pasa o no |
| **Sesión 2** (~3h) | Regresión + Remaining + DB Evidence | ~140 min | Completar coverage + evidencia BD |

---

## Canales de Testing

| Canal | Uso en este ticket |
|-------|-------------------|
| **Canal 1 — Playwright MCP** | Para TCs de UI (navegación, clicks, verificaciones visuales) con supervisión del QA Engineer |
| **Canal 2 — Bot-test E2E** | Para automatizar los 38 TCs automatizables post-validación manual |
| **DBeaver** | Para queries de verificación BD (Bloque 7) via SSH tunnel |
| **DevTools** | Para verificar payloads de API (Payload Diet), Network requests, estilos CSS |

---

## Estado

⏳ Plan creado — esperando inicio de ejecución (Deployment)

### Condiciones para iniciar Deployment:
1. ✅ Discovery completo (risk-triage, AC, test-matrix, test-plan — todos aprobados)
2. ⬜ Branch IONF-1030 desplegada en staging (3 repos)
3. ⬜ Migraciones ejecutadas en staging
4. ⬜ Respuestas del Developer a las 3 preguntas pendientes (TC-PD1, TC-PD2, TC-PD3)
5. ⬜ QA Engineer confirma inicio de sesión de testing
