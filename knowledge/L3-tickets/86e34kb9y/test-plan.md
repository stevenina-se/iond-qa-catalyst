# Test Plan — 86e34kb9y

> Ticket: [IOND] Mejorar búsqueda y jerarquía de resultados en Admin Companies
> Módulo principal: Auth (Admin > Companies)
> Fecha del plan: 2026-10-05
> Track: Discovery → listo para Deployment

---

## Información del Ticket

| Campo | Valor |
|-------|-------|
| ID | 86e34kb9y |
| Título | [IOND] Mejorar búsqueda y jerarquía de resultados en Admin Companies |
| Módulo | Auth (Admin Companies, Global Search) |
| Tipo | Improvement |
| Repos afectados | `gateway` (PHP), `gateway-ion` (Vue 3 + TS) |
| QA Engineer | Steve Nina |
| Fecha del plan | 2026-10-05 |

## Resumen

| Métrica | Valor |
|---------|-------|
| Total de casos | 42 (33 funcionales + 2 regresión tenant + 7 regresión general) |
| Tiempo estimado | ~180 min (~3 horas) |
| Artefactos de Discovery | `ac-reconciliation.md`, `risk-triage.md`, `ac-consolidated.md`, `test-matrix.md`, `test-matrix.csv` |
| Prioridad Crítica | 14 casos |
| Prioridad Alta | 16 casos |
| Prioridad Media | 10 casos |
| Prioridad Baja | 2 casos |

---

## Orden de Ejecución

```
ORDEN DE EJECUCIÓN — Ticket 86e34kb9y

BLOQUE 1 — SMOKE TESTS (ejecutar primero, si alguno falla → escalar)
  □ REG-001: Login de admin funciona correctamente — 🔴
  □ TC-016: Abrir buscador global con ⌘K / Ctrl+K — 🔴
  □ TC-033: Búsqueda por nombre de company → resultados existentes preservados — 🔴
  □ TC-023: Tabla de companies carga con CompanyDetailsCell enriquecida — 🟠

BLOQUE 2 — HAPPY PATH: MOTOR DE BÚSQUEDA (corazón del ticket)
  □ TC-001: Buscar email exacto de Company User → mejor match — 🔴
  □ TC-002: Buscar email de contacto de company → match de contacto — 🔴
  □ TC-003: Buscar fragmento de dominio (case-insensitive) — 🔴
  □ TC-004: Deduplicación: múltiples users → company 1 sola vez — 🔴
  □ TC-007: Jerarquía determinista: ranking con query de email — 🔴
  □ TC-008: Jerarquía determinista: ranking con query normal — 🔴
  □ TC-005: Permisos: company sin permiso no aparece — 🔴
  □ TC-006: Catálogo completo: company fuera de página aparece — 🟠
  □ TC-009: Sin resultados: estado vacío + acción limpiar — 🟠

BLOQUE 3 — HAPPY PATH: UI (buscador global + tabla)
  □ TC-018: Navegación por teclado (flechas, Enter, Esc) — 🟠
  □ TC-020: "Ver las N companies" → navega a listado con query — 🟠
  □ TC-025: Persistencia de búsqueda en URL (F5) — 🟠
  □ TC-026: Navegación browser atrás/adelante con búsqueda — 🟠
  □ TC-027: Paginación estable con búsqueda: sin duplicados — 🔴
  □ TC-028: Pista del match visible en CompanyDetailsCell — 🟠

BLOQUE 4 — EDGE CASES
  □ TC-010: Email con caracteres especiales (user+tag@) — 🟠
  □ TC-011: Email con puntos y guiones en dominio — 🟠
  □ TC-012: Company sin Company Users → buscable por nombre/ID — 🟠
  □ TC-013: Email contacto = email user → deduplicación — 🟠
  □ TC-015: Query vacía → estado inicial — 🟡
  □ TC-017: Búsquedas recientes persisten en localStorage — 🟡
  □ TC-019: Home/End → primer/último resultado (trade-off) — 🟡
  □ TC-021: Iconos buscador coinciden con sidebar — 🟡
  □ TC-024: Company sin logo → fallback avatar — 🟡

BLOQUE 5 — NEGATIVOS
  □ TC-014: Company user (no admin) no puede buscar companies — 🔴
  □ TC-022: Esc cierra buscador correctamente — 🟡
  □ TC-029: URL con search param inválido/vacío — 🟡

BLOQUE 6 — REGRESIÓN
  □ REG-002: Navegación sidebar de admin funciona — 🟠
  □ REG-003: Buscador tenant: búsqueda de flows — 🟠
  □ REG-004: Buscador tenant: búsqueda de apps — 🟠
  □ REG-005: Lista companies: ordenamiento por columna — 🟠
  □ REG-006: Lista companies: acciones por fila — 🟠
  □ TC-030: Buscador global Tenant (5 secciones) — 🟠
  □ TC-031: Tenant sin permisos: fallback de icono — 🟡
  □ TC-032: Vistas admin PrimeVue sin regresión CSS — 🟡
  □ REG-007: Admin dashboard sin regresión visual — 🟡

BLOQUE 7 — DB EVIDENCE (ejecutar en DBeaver via SSH)
  □ DB-001: Verificar users con emails por company (TC-001/TC-003)
  □ DB-002: Verificar email de contacto de company (TC-002)
  □ DB-003: Verificar deduplicación multi-user (TC-004)
  □ DB-004: Verificar companies sin users (TC-012)
  □ DB-005: Verificar email contacto = email user (TC-013)
  □ DB-006: Verificar índices pg_trgm existen
```

---

## Datos Necesarios

| Dato | Cómo obtenerlo | Notas |
|------|---------------|-------|
| Usuario Admin | `.env` de ionflow-qa-catalyst | `IONFLOW_ADMIN_USERNAME` / `IONFLOW_ADMIN_PASSWORD` |
| Usuario Company | `.env` de ionflow-qa-catalyst | `IONFLOW_COMPANY_USERNAME` / `IONFLOW_COMPANY_PASSWORD` |
| Company con Company Users + emails | Verificar en staging vía BD | Necesita al menos 1 company con 3+ users con emails en el mismo dominio |
| Company con email de contacto | Verificar tabla `contacts` en staging | `contactable_type = 'company'`, campo `email` no null |
| Company sin Company Users | Verificar en staging | Company sin registros en `company_user` |
| Company fuera de primera página | Staging debe tener 20+ companies | Para verificar catálogo completo (TC-006) |
| URL de staging | `.env` → `IONFLOW_ENVIRONMENT_URL` | Verificar que el branch IONF-1343 está deployed |
| Conexión DBeaver | SSH tunnel existente | Para queries de verificación BD |

### Verificación pre-ejecución

Antes de iniciar la ejecución, verificar:

1. **Branch IONF-1343** está mergeado/desplegado en staging (ambos repos: `gateway` + `gateway-ion`)
2. **Extensión `pg_trgm`** está habilitada en la BD de staging
3. **Las 3 migraciones** del ticket se ejecutaron correctamente
4. **Datos de prueba** existen: companies con users, contactos, etc.

---

## Criterios de Aprobación/Rechazo

```
CRITERIOS DE APROBACIÓN
  ✅ TODOS los smoke tests pasan (Bloque 1: 4 casos)
  ✅ TODOS los happy path de motor de búsqueda pasan (Bloque 2: 9 casos)
  ✅ TODOS los happy path de UI pasan (Bloque 3: 6 casos)
  ✅ Al menos 80% de los edge cases pasan (Bloque 4: 7/9 mínimo)
  ✅ TODOS los negativos pasan (Bloque 5: 3 casos)
  ✅ TODOS los casos de regresión críticos pasan (Bloque 6)
  ✅ DB evidence confirma índices pg_trgm y datos correctos

CRITERIOS DE RECHAZO
  ❌ Algún smoke test falla → rechazo inmediato
  ❌ Motor de búsqueda no encuentra por email → rechazo
  ❌ Ranking de resultados no es determinista → rechazo
  ❌ Permisos/privacidad fallan (email se expone sin autorización) → rechazo inmediato
  ❌ Paginación inestable (duplicados entre páginas) → rechazo
  ❌ Buscador global no se abre / no funciona → rechazo
  ❌ Regresión del buscador de tenant → rechazo con análisis de impacto
  ❌ DB evidence muestra ausencia de índices pg_trgm → rechazo

CRITERIOS DE APROBACIÓN CON OBSERVACIONES
  ⚠️ Home/End no mueve caret → aprobar (trade-off documentado)
  ⚠️ Icono fallback en buscador → aprobar con bug menor
  ⚠️ Company sin logo sin fallback adecuado → aprobar con observación visual
  ⚠️ Edge case de caracteres especiales falla parcialmente → aprobar con bug registrado
```

---

## Estimación de Tiempo

| Bloque | Casos | Tiempo estimado |
|--------|-------|-----------------|
| Smoke tests | 4 | ~15 min |
| Happy path: Motor de búsqueda | 9 | ~45 min |
| Happy path: UI | 6 | ~30 min |
| Edge cases | 9 | ~30 min |
| Negativos | 3 | ~15 min |
| Regresión | 9 | ~30 min |
| DB evidence | 6 | ~15 min |
| **Total** | **42 + 6 DB** | **~180 min (~3 horas)** |

> ⚠️ La estimación es orientativa. Puede variar según el estado de staging y la disponibilidad de datos de prueba.

---

## Notas para Deployment

### Riesgos a tener en cuenta:
1. **El buscador de tenant fue reescrito** como efecto colateral. Si hay regresión en tenant, el impacto es mayor que el scope original del ticket.
2. **El buscador admin anterior fue eliminado** (no hay fallback). Si el nuevo falla, admin pierde búsqueda global.
3. **CompanyTable migrada de PrimeVue** → si hay problemas de rendering, toda la vista de companies se ve afectada.

### Automatización potencial (post-deployment):
- 28 de los 42 casos son automatizables con Playwright
- Candidatos prioritarios para automatización: TC-001 a TC-008 (motor de búsqueda), TC-016 (⌘K), TC-027 (paginación)

---

## Estado

⏳ **Plan creado** — esperando que el ticket pase a Deployment para iniciar ejecución.
