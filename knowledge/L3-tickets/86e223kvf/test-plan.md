# Test Plan — 86e223kvf

> Generado por `sprint-testing/plan`
> Track: Discovery — Plan preparado para ejecución en Deployment

## Información del Ticket

| Campo | Valor |
|-------|-------|
| ID | 86e223kvf |
| Título | Mejoras estéticas globales en pantallas de iond / Ionflow |
| Módulo | Multi-módulo — Migración UI Framework (PrimeVue → Tailwind 4 + shadcn-vue) |
| QA Engineer | Steve Nina |
| Fecha del plan | 2026-07-20 |
| Developer | Jose Enrique Ricaldi Juchani |
| Branches | `IONF-1104` en gateway-ion, gateway, flow_binaries |

## Resumen

| Métrica | Valor |
|---------|-------|
| Total de casos | 62 (48 funcionales + 14 regresión) |
| Tiempo estimado | ~6-7 horas (390 min) |
| Artefactos de Discovery | risk-triage.md, ac-reconciliation.md, ac-consolidated.md, test-matrix.md/.csv |
| Riesgo general | 🔴 Crítico |
| Sesiones recomendadas | 2-3 sesiones de ~2.5 horas |

---

## Orden de Ejecución

### BLOQUE 1 — SMOKE TESTS (ejecutar PRIMERO — si alguno falla → ESCALAR)

> ⚠️ Si cualquier smoke test falla, el ticket tiene un problema fundamental.
> NO continuar con los bloques siguientes hasta resolver.

```
□ TC-001: TenantLayout carga con todos los servicios — 🔴
□ TC-004: Pantallas Tenant usan estilos Tailwind correctamente — 🔴
□ TC-005: Pantallas Admin mantienen PrimeVue sin regresión — 🔴
□ TC-007: Paginación SSR funciona en DataTable — 🔴
□ TC-011: Sidebar muestra todas las secciones según permisos — 🟠
□ REG-001: Login flow funciona correctamente — 🔴
```

**Gate de Smoke**: ¿Los 6 smoke tests pasaron?
- → SÍ: Continuar a Bloque 2
- → NO: **ESCALAR al Developer.** El problema es de fundación.

---

### BLOQUE 2 — WAVE 1 HAPPY PATH (Fundación)

> Verificar que la fundación del nuevo sistema UI funciona correctamente.

```
□ TC-002: TenantLayout preserva setUser sync con canvas — 🔴
□ TC-006: Navegación rápida Admin↔Tenant sin contaminación CSS — 🔴
□ TC-008: Ordenamiento por columna en DataTable — 🔴
□ TC-012: Breadcrumbs se actualizan al navegar — 🟠
□ TC-014: Toast success aparece en operación CRUD — 🟠
□ TC-015: Toast error aparece en operación fallida — 🟠
□ REG-002: Crear flow nuevo desde lista de boards — 🔴
□ REG-003: Editar flow existente (abrir canvas) — 🔴
□ REG-004: Ejecutar flow desde canvas (modo Dev) — 🔴
```

**Gate de Fundación**: ¿Todos los tests de fundación pasaron?
- → SÍ: Continuar a Bloque 3
- → NO: Los fallos en fundación afectan TODO. Evaluar impacto antes de continuar.

---

### BLOQUE 3 — WAVE 2 HAPPY PATH (Features Nuevos + Backend)

> Verificar features nuevos y cambios de backend.

```
Features Nuevos:
□ TC-017: Búsqueda global (Ctrl+K) encuentra flows — 🟠
□ TC-018: Búsquedas recientes persisten — 🟠
□ TC-021: Toggle dark mode funciona — 🟡
□ TC-023: Vista lista de Boards carga correctamente — 🟠
□ TC-024: CreateConnectionV2Dialog funciona (primary + secondary) — 🟠

Backend - Executions:
□ TC-026: Filtrar ejecuciones por status — 🟠
□ TC-027: Filtrar ejecuciones por rango de fechas — 🟠

Backend - Data Store:
□ TC-030: Buscar Data Store por nombre — 🟠
□ TC-031: Ordenar Data Stores por created_at — 🟠
□ TC-032: StoreViewer muestra datos anidados — 🟠

Backend - Accounts/Keys:
□ TC-035: Filtrar accounts por timezone — 🟡
□ TC-037: Filtrar keys por provider — 🟡

Flow Description:
□ TC-058: Descripción de flow se guarda correctamente — 🟡
```

---

### BLOQUE 4 — EDGE CASES

> Verificar comportamiento en bordes y escenarios no ideales.

```
Fundación:
□ TC-003: TenantLayout después de sesión expirada — 🟠
□ TC-009: DataTable con 0 registros (empty state) — 🟠
□ TC-010: Column visibility toggle — 🟠
□ TC-013: Usuario con permisos parciales — 🟠
□ TC-016: Deduplicación de toasts idénticos — 🟠

Features Nuevos:
□ TC-019: Búsqueda rápida con cambio de query (race condition) — 🟠
□ TC-022: Dark mode persiste entre recargas — 🟡
□ TC-025: CreateConnectionV2Dialog — solo secondary resuelve (bugfix) — 🔴

Backend:
□ TC-028: Filtro status case-insensitive — 🟡
□ TC-033: Buscar con caracteres especiales (%_\) — 🟠
□ TC-036: Accounts sin timezone configurado — 🟡
```

---

### BLOQUE 5 — NEGATIVOS

> Verificar que el sistema NO se puede romper con inputs inválidos.

```
□ TC-020: Búsqueda sin resultados — 🟡
□ TC-029: Filtro con date_from > date_to — 🟡
□ TC-034: Ordenar por columna no whitelisted — 🟡
```

---

### BLOQUE 6 — WAVE 3 (14 Pantallas + Polish)

> Smoke test por cada pantalla migrada + verificaciones visuales.

```
Pantallas (smoke por pantalla):
□ TC-038: Boards carga — 🟠
□ TC-039: Executions carga — 🟠
□ TC-040: PDF Templates carga (referencia) — 🟠
□ TC-041: App Connectors carga — 🟠
□ TC-042: Integrations carga — 🟠
□ TC-043: Webhooks carga — 🟡
□ TC-044: Accounts carga — 🟡
□ TC-045: Keys carga — 🟡
□ TC-046: Dashboard carga — 🟡
□ TC-047: Data Store carga — 🟡
□ TC-048: Settings carga — 🟡
□ TC-049: Profile carga — 🟡
□ TC-050: Activity carga — 🟡
□ TC-051: Support (nuevo) carga — 🟢

Visual/Consistencia:
□ TC-052: Tablas siguen patrón de PDF Templates — 🟡
□ TC-053: Modal de eliminación normalizado — 🟠
□ TC-054: Otros modales de confirmación normalizados — 🟡

i18n/Responsive:
□ TC-055: Textos en español sin keys faltantes — 🟡
□ TC-056: Pantallas legibles en 1366px — 🟡
□ TC-057: Pantallas en 1024px (tablet) — 🟡
```

---

### BLOQUE 7 — REGRESIÓN EXTENDIDA

> Verificar que funcionalidad existente no se rompió.

```
□ REG-005: Crear conexión OAuth (authorize→callback→token) — 🟠
□ REG-006: Crear template PDF desde vista lista — 🟠
□ REG-007: Eliminar webhook — 🟠
□ REG-008: Visualizar datos en StoreViewer — 🟠
□ REG-009: Ver detalle de ejecución — 🟠
□ REG-010: CRUD de accounts — 🟡
□ REG-011: CRUD de keys/credentials — 🟡
□ REG-012: Métricas de Dashboard — 🟡
□ REG-013: Instalar/desinstalar integración — 🟡
□ REG-014: CRUD de data structures — 🟡
```

---

### BLOQUE 8 — DB EVIDENCE

> Queries de verificación en DBeaver (PostgreSQL via SSH tunnel).

```
□ DB-001: Filtro status case-insensitive en executions — Verificar: LOWER() funciona
□ DB-002: Filtro date_from/date_to en executions — Verificar: whereDate inclusivo
□ DB-003: Flow description persiste — Verificar: columna description actualizada
```

---

## Datos Necesarios

| Dato | Cómo obtenerlo | Notas |
|------|---------------|-------|
| **Usuario Tenant (Company)** | `.env` → `IONFLOW_COMPANY_USERNAME` / `IONFLOW_COMPANY_PASSWORD` | Rol Company — permisos completos de tenant |
| **Usuario Admin** | `.env` → `IONFLOW_ADMIN_USERNAME` / `IONFLOW_ADMIN_PASSWORD` | Rol Administrator — para verificar regresión Admin |
| **Usuario restringido** | Crear o usar usuario con permisos parciales (sin permiso Boards) | Para TC-013 (permisos parciales) |
| **URL de staging** | `.env` → `IONFLOW_ENVIRONMENT_URL` | Canal 1 (Playwright MCP) |
| **Flow de prueba** | Flow existente con nodos configurados en staging | Para TC-002, TC-058, REG-003, REG-004 |
| **Connector OAuth** | Connector con auth tipo `oauth2_code` configurado | Para TC-024, TC-025, REG-005 |
| **Data Store con datos** | Data Store existente con registros y datos anidados | Para TC-030–TC-034, REG-008 |
| **Ejecuciones históricas** | Executions existentes con distintos status y fechas | Para TC-026–TC-029, REG-009 |
| **DBeaver** | Conexión SSH tunnel activa al PostgreSQL de staging | Para DB-001 a DB-003 |

---

## Criterios de Aprobación/Rechazo

### ✅ CRITERIOS DE APROBACIÓN

```
✅ TODOS los smoke tests (Bloque 1) pasan — 6/6
✅ TODOS los happy path de fundación (Bloque 2) pasan — 9/9
✅ Al menos 80% de los happy path de Wave 2 (Bloque 3) pasan — 10/13
✅ Al menos 75% de los edge cases (Bloque 4) pasan — 8/11
✅ TODOS los negativos (Bloque 5) pasan — 3/3
✅ Las 14 pantallas migradas cargan sin errores (Bloque 6) — 14/14
✅ TODOS los casos de regresión críticos (REG-001 a REG-004) pasan — 4/4
✅ Al menos 80% de la regresión extendida (Bloque 7) pasan — 8/10
✅ DB evidence confirma integridad de datos — 3/3
```

### ❌ CRITERIOS DE RECHAZO

```
❌ Algún smoke test falla → RECHAZO INMEDIATO
❌ TenantLayout no carga (TC-001) → RECHAZO — app inutilizable
❌ CSS bleeding a Admin (TC-005) → RECHAZO — regresión en producción
❌ DataTable sin paginación SSR (TC-007) → RECHAZO — funcionalidad core rota
❌ Login no funciona (REG-001) → RECHAZO — acceso bloqueado
❌ Canvas no carga (REG-003) → RECHAZO — funcionalidad core rota
❌ Caso negativo falla (sistema se puede romper) → RECHAZO
❌ DB evidence muestra datos corruptos → RECHAZO
```

### ⚠️ APROBACIÓN CON OBSERVACIONES

```
⚠️ Edge case falla pero no es bloqueante → Aprobar + bug registrado
⚠️ Dark mode con defecto visual menor → Aprobar con observación
⚠️ Pantalla secundaria (Support, Activity) con issue menor → Aprobar con observación
⚠️ i18n con 1-2 keys faltantes → Aprobar con bug de prioridad baja
⚠️ Responsive con issue menor en 1024px → Aprobar con observación
```

---

## Estimación de Tiempo

| Bloque | Casos | Tiempo estimado | Notas |
|--------|-------|-----------------|-------|
| 1. Smoke Tests | 6 | ~30 min | Gate bloqueante |
| 2. Wave 1 Happy Path | 9 | ~60 min | Fundación — incluye canvas |
| 3. Wave 2 Happy Path | 13 | ~75 min | Features + Backend |
| 4. Edge Cases | 11 | ~60 min | Requiere setup de datos |
| 5. Negativos | 3 | ~15 min | Rápidos |
| 6. Wave 3 Pantallas | 20 | ~90 min | 14 pantallas + visual |
| 7. Regresión Extendida | 10 | ~45 min | CRUD + OAuth |
| 8. DB Evidence | 3 | ~15 min | DBeaver queries |
| **Total** | **75** | **~390 min (~6.5 hrs)** | **2-3 sesiones recomendadas** |

### Distribución recomendada de sesiones

| Sesión | Bloques | Duración | Foco |
|--------|---------|----------|------|
| **Sesión 1** | Bloques 1 + 2 | ~1.5 hrs | Fundación. Si falla aquí → escalar antes de continuar |
| **Sesión 2** | Bloques 3 + 4 + 5 | ~2.5 hrs | Features, backend, edge cases |
| **Sesión 3** | Bloques 6 + 7 + 8 | ~2.5 hrs | Pantallas, regresión, DB evidence |

---

## Herramientas de Testing

| Herramienta | Uso | Canal |
|------------|-----|-------|
| **Playwright MCP** | Navegación asistida por IA durante la sesión | Canal 1 — supervisado por QA |
| **DBeaver** | Queries de verificación BD (PostgreSQL SSH tunnel) | Manual |
| **DevTools (F12)** | Inspección de consola (errores JS), red (API calls), estilos (CSS) | Manual |
| **Browser Resize** | Testing responsive (1920px, 1366px, 1024px) | Manual / Playwright |

---

## Preguntas Pendientes para el Developer (del Risk Triage)

> ⚠️ Estas 15 preguntas del risk-triage.md deben discutirse ANTES o DURANTE
> la sesión de testing. Las respuestas pueden afectar el plan.

Las más urgentes para la Sesión 1:
1. ¿Las 10 inyecciones de TenantLayout funcionan idénticamente a CompanyLayout?
2. ¿Se verificó CSS isolation con pantallas Admin después de los cambios?
3. ¿El DataTable tiene el mismo contrato de paginación SSR que PrimeVue?

---

## Estado

```
⏳ Plan creado en Discovery — esperando que el ticket pase a Deployment
   para confirmar y ejecutar.

Artefactos de Discovery completos:
  ✅ ac-reconciliation.md (12 divergencias documentadas)
  ✅ risk-triage.md (15 riesgos, 28 edge cases, 15 preguntas)
  ✅ ac-consolidated.md (20 ACs en 5 grupos)
  ✅ test-matrix.md + .csv (62 TCs: 48 funcionales + 14 regresión)
  ✅ test-plan.md (este documento)
```
