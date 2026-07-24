# Release Notes — v0.1.1 (Internal)

> Generado por `skills/release/notes`
> Fecha: 20 de julio de 2026
> Tipo: `internal`
> Fuente de datos: `get_tickets_deployment_4.csv` (16 tickets) + ClickUp MCP (muestra enriquecida)

---

## Resumen Ejecutivo

La versión **v0.1.1** es una **patch release** orientada a estabilización y calidad. Se compone mayoritariamente de correcciones de bugs encontrados durante el QA de la v0.1.0, acompañadas de nuevas funcionalidades que estaban en el pipeline del Sprint 4. Los fixes son predominantemente en **Boards** (Scheduler, Simple Decision, Commit) y **PDF Templates**, además de mejoras al ecosistema de integraciones y el motor de IA (Flow Pilot).

**Estadísticas:** 3 nuevas funcionalidades · 8 correcciones · 2 mejoras · 2 cambios internos · 1 task/doc

**Distribución por área:**
Boards/Flujos (5) · PDF Templates (2) · Connections/Integrations (2) · Webhooks (1) · Executions/Logs (2) · Auth (1) · Gateway Services (1) · Dashboard (1) · Billing (1)

**Distribución por scope:**
Core: 10 tickets · UX/UI: 5 tickets · Infra/Doc: 1 ticket

**Prioridad:** 9 high · 7 normal

---

## Highlights

1. **Corrección de lógica de Simple Decision** — El nodo Simple Decision comparaba valores numéricos como strings, produciendo resultados incorrectos en flujos de decisión (`2 > 12 = true`). Este es un fix crítico de lógica de negocio. Se agregó soporte de tipos (Number, String, Boolean, Array, Object) con selector explícito. `(webcomponents-flow, flow_binaries)` — IONF-1128

2. **Confirmación de cobro para scraping de plataformas** — Nuevo flujo de confirmación con modal explícito cuando un usuario solicita documentación no cacheada en IonMind. Protege contra cobros duplicados y hace transparente el costo de extracción. `(gateway, ionmind, gateway-ion)` — IONF-1098

3. **Soporte de Listings para Etsy y WooCommerce** — Nueva acción `listing` en el Gateway PHP que recibe un payload genérico de productos, los transforma al formato específico de cada carrito destino, y los envía en lotes (batching) con reporte de resultados vía webhook. Escalable a otros carritos. `(gateway)` — IONF-1004

4. **Monitoreo de tokens en Flow Pilot** — Implementación completa de contabilización de tokens (prompt/completion) de OpenRouter por usuario/sesión. Cada respuesta registra `usage_metadata` con `prompt_tokens`, `completion_tokens`, `total_tokens` y `cost`. Base para futura facturación y límites. `(flow_binaries, gateway)` — IONF-1020

5. **Fix de timestamps UTC/Local en Schedules** — Se corrigió el desfase de +4 horas en los logs de ejecución de Company Schedules en la UI del Gateway, causado por una conversión UTC/Local incorrecta. `(gateway, flow_binaries)` — IONF-1007, IONF-1168

---

## 🚀 Nuevas Funcionalidades

### 📂 Integrations / Gateway

- **IONF-1004** — Soporte de Listings para Etsy y WooCommerce en Gateway. Nueva acción `listing` con payload genérico, procesamiento en lotes (batching), transformación al formato específico de cada carrito destino (WooCommerce, Etsy), y reporte de resultados (éxito/fallo por producto) vía webhook al origen. `(gateway)`
  - Tags: `ion-sp17`
  - Subcategory: Gateway
  - Tipo: `New Feature`

- **IONF-1098** — Confirmación y cobro para primer scraping de plataformas. Modal de confirmación que muestra el costo aproximado antes de ejecutar la extracción. Verificación de caché (`bd_cache`) para evitar cobros duplicados cuando la documentación ya existe. `(gateway, ionmind, gateway-ion)`
  - Tags: `iond-core`
  - Subcategory: App Connectors
  - Tipo: `New Feature`

### 📂 Boards / Flow Pilot

- **IONF-1169** — Eliminación de restricciones CORS para rutas públicas de webhooks. Los webhooks ahora son accesibles desde cualquier origen externo sin errores de CORS. `(flow_binaries)`
  - Tags: `iond-core`
  - Tipo: `New Feature` (endpoint público)

---

## 🐛 Correcciones (8 bugs)

### 📂 Boards / Flujos

- **IONF-1128** — Fix: Simple Decision comparaba valores numéricos como strings. Se agregó selector de tipo (Number, String, Boolean, Array, Object) y se corrigió la lógica de comparación para que `2 > 12 = false` sea correcto. (high) `(webcomponents-flow, flow_binaries)`
  - Tags: `qa-regression-v0.1.0, iond-core`
  - Subcategory: Nodo Simple Decision
  - Tipo: `Bug`

- **IONF-1127** — Fix: Scheduler ejecutaba flow correctamente pero el status quedaba en "error". La ejecución completaba exitosamente pero el estado final se reportaba incorrectamente como error. (high) `(flow_binaries)`
  - Tags: `qa-regression-v0.1.0, iond-core`
  - Subcategory: Boards / Scheduler
  - Tipo: `Bug`

- **IONF-1121** — Fix: Board sugiere cambios sin guardar tras commit exitoso al re-ingresar a la vista. Falso positivo en la detección de unsaved changes post-commit. (normal) `(gateway-ion)`
  - Tags: `qa-regression-v0.1.0`
  - Subcategory: Boards / Commit
  - Tipo: `Bug`

### 📂 PDF Templates

- **IONF-1126** — Fix: Cambios sin guardar se pierden al presionar Escape o cerrar modal sin confirmación. Se implementó diálogo de confirmación antes de descartar cambios. (high) `(gateway-ion)`
  - Tags: `qa-regression-v0.1.0`
  - Subcategory: PDF Templates
  - Tipo: `Bug`

- **IONF-1116** — Fix: Sin límite de tamaño para Load Base PDF, la vista crasheaba con archivos grandes. Se implementó validación de tamaño con error controlado. (high) `(gateway-ion)`
  - Tags: `qa-regression-v0.1.0`
  - Subcategory: PDF Templates
  - Tipo: `Bug`

### 📂 Connections

- **IONF-1114** — Fix: Reautorización por API Key creaba conexión duplicada en lugar de sobrescribir la existente. La lógica ahora detecta conexiones existentes y las actualiza. (high) `(gateway-ion, flow_binaries)`
  - Tags: `qa-regression-v0.1.0, iond-core`
  - Subcategory: Connections / Integrations
  - Tipo: `Bug`

### 📂 Executions / Logs

- **IONF-1168** — Fix: Error de visualización de +4 horas en los logs de ejecución de Company Schedules en UI Gateway. Conversión UTC/Local corregida. (normal) `(gateway)`
  - Subcategory: Execution History / Gateway UI
  - Tipo: `Bug`

- **IONF-1007** — Fix: Error de sincronización UTC/Local en los disparadores de Company Schedules. Los schedules se disparaban en hora incorrecta. (high) `(gateway, flow_binaries)`
  - Tags: `qa-regression-v0.1.0, iond-core`
  - Subcategory: Boards / Scheduler
  - Tipo: `Bug`

---

## ⚡ Mejoras (2)

- **IONF-1020** — Monitoreo de uso de tokens por usuario en Flow Pilot. Implementación de contabilización de tokens (prompt_tokens, completion_tokens, total_tokens, cost) por sesión de chat. Registros persistidos en SQLite por sesión. Base para facturación y límites por usuario. (high) `(flow_binaries, gateway)`
  - Tags: `iond-core, iond-ia`
  - Subcategory: FlowPilot
  - Tipo: `Improvement`

- **IONF-1030** — Mejoras visuales de la interface en Ionflow Dualtrack. Ajustes de UI/UX en el dashboard y vistas principales. (normal) `(gateway-ion)`
  - Tipo: `Improvement`

---

## 🔧 Cambios Internos

### Refactors

- **IONF-1075** — Refactorización del flujo y formulario de registro de compañía. Simplificación del formulario de onboarding y mejora del flujo post-registro. (normal) `(gateway-ion)`
  - Tipo: `Refactor`

- **IONF-1049** — Sincronización de logs de ejecución con Cloudflare R2. Los logs de ejecución ahora se persisten en R2 para disponibilidad a largo plazo. (normal) `(flow_binaries)`
  - Tipo: `Task/Infra`

### Tasks / Documentación

- **IONF-1149** — Protocolo de Despliegue Iond — Versión v0.1.0. Documentación del protocolo de deploy establecido para la v0.1.0. (high)
  - Tipo: `Task` (Documentación, sin impacto funcional)

---

## ⚠️ Breaking Changes

No hay breaking changes en esta versión. Todos los cambios son correcciones retrocompatibles y nuevas funcionalidades aditivas.

> **Nota sobre CORS (IONF-1169):** Las rutas públicas de webhooks ya no tienen restricción CORS. Si algún sistema dependía del bloqueo CORS como mecanismo de seguridad en los webhooks, este cambio puede requerir atención. Los webhooks dedicados (no públicos) no se ven afectados.

---

## 📋 Información del Release

| Campo | Valor |
|-------|-------|
| Versión | `v0.1.1` |
| Fecha de deploy | Julio 2026 |
| Entorno | `dev-app.ionflow.io` → producción |
| Total tickets | 16 (ready to merge) |
| Repos | gateway-ion, flow_binaries, gateway, webcomponents-flow, ionmind |
| Sprint | Sprint 4 (7/6 – 7/19) |
| Release anterior | v0.1.0 (187 tickets, Julio 2026) |

### Tickets por repo

| Repo | Tickets |
|------|---------|
| `flow_binaries` | IONF-1128, 1127, 1007, 1020, 1049, 1169, 1114 |
| `gateway-ion` | IONF-1126, 1116, 1121, 1075, 1030, 1098 |
| `gateway` | IONF-1004, 1168, 1098, 1020, 1007 |
| `webcomponents-flow` | IONF-1128 |
| `ionmind` | IONF-1098 |

### Merge Requests referenciados (del MCP)

| Ticket | PRs |
|--------|-----|
| IONF-1128 | webcomponents-flow #7, flow_binaries #13 |
| IONF-1098 | gateway #12, ionmind #3, gateway-ion #6 |
| IONF-1004 | gateway #17 |
| IONF-1020 | gateway #11, flow_binaries #12 |

---

## Comparativa con v0.1.0

| Métrica | v0.1.0 | v0.1.1 |
|---------|--------|--------|
| Total tickets | 187 | 16 |
| Features | 125 | 3 |
| Bug fixes | 32 | 8 |
| Improvements | 6 | 2 |
| Internos | 24 | 3 |
| Tipo de release | Primer release a producción | Patch (estabilización) |

---

*Generado por ionflow-qa-catalyst — skill: release/notes*
*Fecha: 20 de julio de 2026*
