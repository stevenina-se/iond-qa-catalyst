# Skill: release/ingest

> Orquestador de datos de release. Procesa el CSV de tickets (fuente de verdad) y usa
> ClickUp MCP para obtener detalles de cada ticket bajo demanda. Genera los artefactos
> base que alimentan al resto del pipeline de release.

---

## Cuándo usar este skill

**Frase disparadora:**
```
Preparar datos de release: v[X.Y.Z]
```

**Pre-condición**: Debe existir el CSV de tickets en `knowledge/releases/<version>/release-tickets.csv`

---

## Pre-requisitos

- ✅ `knowledge/releases/<version>/release-tickets.csv` — CSV con columnas: `internal_id,custom_id,nombre,status,prioridad`
- ✅ Acceso al ClickUp MCP (`getTaskById`)
- ✅ `knowledge/L2-modules/` — Para mapeo de áreas a módulos L2

---

## Stage 1 — PLANNING

### Paso 1.1 — Verificar pre-requisitos

1. Verificar que existe el CSV en la ruta esperada
2. Parsear CSV para obtener conteo total de tickets
3. Verificar acceso al MCP con un ticket de prueba: `getTaskById(<primer_internal_id>)`

| Verificación | Estado | Acción si falla |
|-------------|--------|----------------|
| CSV existe | ✅/❌ | **PARAR** → Pedir al QA Engineer el CSV |
| CSV tiene formato correcto | ✅/❌ | **PARAR** → Verificar columnas |
| MCP responde | ✅/❌ | **PARAR** → Verificar conexión ClickUp |

### Paso 1.2 — Anunciar el plan

```
🔄 RELEASE INGEST — PLAN

Versión: v[X.Y.Z]
CSV: [N] tickets encontrados
MCP: Conectado ✅

Plan de ejecución:
  1. Procesar [N] tickets via MCP (getTaskById × [N])
  2. Extraer: tipo, área, scope, AC, repos, aprobación
  3. Clasificar y generar 3 artefactos:
     - ticket-synthesis.md
     - tracking-list.md + .csv
     - module-impact-map.md

Tiempo estimado: ~[N×3] segundos (3s por ticket via MCP)

¿Procedo?
```

**Esperar confirmación.**

---

## Stage 2 — EXECUTION

### Paso 2.1 — Procesar tickets del CSV

Para cada fila del CSV:

```
Para ticket en CSV:
  1. Invocar getTaskById(ticket.internal_id) via ClickUp MCP
  2. Si MCP falla → marcar como [MCP-ERROR] y continuar
  3. Extraer datos del ticket (ver Paso 2.2)
  4. Reportar progreso: "Procesado [i]/[N]: IONF-XXX ✅"
```

> **Rate limiting**: Procesar uno a uno para no saturar el MCP.
> Si un ticket falla, continuar con el siguiente y reportar al final.

### Paso 2.2 — Extracción de datos por ticket

Para cada respuesta del MCP, extraer:

| Dato | Campo del MCP | Procesamiento |
|------|--------------|---------------|
| **ID interno** | `task_id` | Directo |
| **ID custom** | Del CSV: `custom_id` | Directo (IONF-XXX) |
| **Nombre** | `name` | Directo |
| **Status** | `status` | Directo |
| **Prioridad** | `priority` o CSV: `prioridad` | Directo (urgent/high/normal/low) |
| **Tipo** | `custom_type` | Mapear: Bug→bug-fix, New Feature→new-feature, etc. |
| **Área (subcategoría)** | `custom_iond_subcategory` | Mapear a módulo L2 |
| **Scope** | `tags` | Buscar: "core", "ux-ui" |
| **Versión** | `custom_iond.version` | Directo |
| **QA Points** | `custom_qa_points` | Directo (complejidad QA) |
| **Rechazos** | `custom_rejection_count` | Directo |
| **Asignees** | `assignee` | Lista de desarrolladores |
| **Lista/Sprint** | `list` | Nombre del sprint |
| **Descripción** | Body del ticket (después de los custom fields) | Extraer hasta primer `Comment by` |
| **AC (Gherkin)** | Buscar en descripción: `Scenario:`, `Given`, `When`, `Then` | Extraer bloques Gherkin |
| **Repos afectados** | `custom_merge_request`, `_2`, `_3` | Parsear URLs → nombre del repo |
| **Comentario de aprobación** | Buscar en comentarios: "APROBADO ✅", "resultado de pruebas" | Capturar comentario completo |
| **Comentario de rechazo** | Buscar en comentarios: "RECHAZADO ❌" | Capturar para contexto |
| **Info de infra** | Buscar en comentarios del developer: variables env, migraciones, endpoints | Extraer si existe |
| **Status history** | Líneas `Status set to '...' on ...` | Extraer timeline |

### Paso 2.3 — Clasificación

#### Clasificación de TIPO (3 niveles)

```
NIVEL 1: custom_type del MCP (fuente primaria)
  "New Feature" → new-feature
  "Bug"         → bug-fix
  "Improvement" → improvement
  "Refactor"    → refactor
  "Task"        → task
  "Story"       → new-feature
  "Test"        → infra

NIVEL 2: Fallback por nombre del ticket (si custom_type vacío)
  Contiene "Fix|Corregir|Error|Bug|Problema"     → bug-fix
  Contiene "Crear|Implementar|Nuevo|Añadir"       → new-feature
  Contiene "Refactorizar|Refactor|Migrar"         → refactor
  Contiene "Mejorar|Optimizar|Actualizar"         → improvement
  Contiene "Sonar|Warning|Mantenimiento"          → infra

NIVEL 3: Default
  Si nada coincide → task
```

#### Clasificación de ÁREA (3 niveles)

```
NIVEL 1: custom_iond_subcategory del MCP (fuente primaria)
  Valor directo → mapear a módulo L2 existente

NIVEL 2: Fallback por nombre del ticket (si subcategory vacío)
  Contiene "Board|Flow|Nodo|Canvas"             → boards
  Contiene "PDF|Template|pdfme"                 → pdf-templates
  Contiene "Connection|Auth|OAuth|Basic Auth"   → connections
  Contiene "Webhook"                            → webhooks
  Contiene "Keycloak|SSO|Login|Sesión"          → auth
  Contiene "Grapp|Service|Catalog"              → integrations
  Contiene "Data Store|Storage|Persistent"      → data-store
  Contiene "Account|Company|Team"               → accounts
  Contiene "Execution|History"                  → exec-history
  Contiene "Gateway|Webcomponent"               → gateway
  Contiene "Setting|Theme|Appearance"           → settings

NIVEL 3: Default
  Si nada coincide → general
```

#### Clasificación de SCOPE (desde tags)

```
Si tags contiene "core"    → scope: core (impacta motor/backend, riesgo regresión alto)
Si tags contiene "ux-ui"   → scope: ux-ui (impacta frontend/visual, riesgo smoke alto)
Si ninguno                 → scope: mixed (evaluar por contenido)
```

### Paso 2.4 — Parsear repos desde Merge Request URLs

```
custom_merge_request: "https://gitlab.com/altacrest/gateway-ion/-/merge_requests/225"
  → repo: gateway-ion

custom_merge_request_2: "https://gitlab.com/altacrest/integrations/gateway/-/merge_requests/570"
  → repo: gateway (integrations)

custom_merge_request_3: "https://gitlab.com/altacrest/flow_binaries/-/merge_requests/157"
  → repo: flow_binaries

custom_merge_request: "https://github.com/altacrest/ion_gateway_ion/pull/2"
  → repo: ion_gateway_ion (GitHub)
```

Regla: Extraer el path entre el dominio y `/-/merge_requests` (GitLab) o `/pull` (GitHub).

### Paso 2.5 — Detectar comentario de aprobación/rechazo

Buscar en los comentarios del MCP (formato `Comment by [nombre] on [fecha]:`):

**Patrones de APROBACIÓN:**
- `"APROBADO ✅"`
- `"resultado de pruebas para este ticket es: APROBADO"`
- `"resultado de pruebas para este ticket es: **APROBADO"`

**Patrones de RECHAZO:**
- `"RECHAZADO ❌"`
- `"resultado de pruebas para este ticket es: RECHAZADO"`
- `"resultado de pruebas para este ticket es: **RECHAZADO"`

Capturar:
- Autor del comentario
- Fecha del comentario
- Contenido completo del comentario (para posterior uso en update-modules)

### Paso 2.6 — Generar artefacto: `ticket-synthesis.md`

Formato del artefacto:

```markdown
# Ticket Synthesis — v[X.Y.Z]

> Generado por `release/ingest`
> Fecha: [fecha]
> Total de tickets: [N]
> Fuente: release-tickets.csv + ClickUp MCP

---

## Resumen

| Métrica | Valor |
|---------|-------|
| Total de tickets | [N] |
| New Features | [N] |
| Bug Fixes | [N] |
| Improvements | [N] |
| Refactors / Infra | [N] |
| Tasks | [N] |
| Con custom_type | [N]/[Total] |
| Con iond_subcategory | [N]/[Total] |
| Con tags core | [N] |
| Con tags ux-ui | [N] |
| Con MR URLs | [N] |
| Aprobados | [N] |
| Rechazados (previo a aprobación) | [N] |
| MCP errors | [N] |

---

## Tickets

### IONF-XXX — [nombre]

| Campo | Valor |
|-------|-------|
| ID interno | [internal_id] |
| Status | [status] |
| Prioridad | [prioridad] |
| Tipo | [tipo clasificado] (fuente: custom_type / fallback) |
| Área | [área clasificada] (fuente: iond_subcategory / fallback) |
| Scope | [core / ux-ui / mixed] |
| QA Points | [N] |
| Rechazos previos | [N] |
| Sprint | [sprint_name] |
| Asignees | [lista] |
| Repos | [lista de repos] |

**Descripción resumida:**
[2-3 oraciones sintetizadas de la descripción completa del ticket]

**AC principales:**
- [AC 1 resumido]
- [AC 2 resumido]

**Aprobación:**
[Aprobado ✅ / Rechazado ❌ / Pendiente ⏳] por [autor] el [fecha]
[Resumen del comentario de aprobación, máximo 3 oraciones]

---
[Repetir para cada ticket]
```

### Paso 2.7 — Generar artefacto: `tracking-list.md` + `.csv`

**tracking-list.csv** (columnas):
```csv
custom_id,internal_id,nombre,status,prioridad,tipo,area,scope,repos,qa_points,rechazos,aprobacion
IONF-103,86dwwf1vx,Unificar endpoints...,merged,high,new-feature,integrations,core,"gateway-ion,gateway",8,1,aprobado
```

**tracking-list.md** — Tabla visual con las mismas columnas.

### Paso 2.8 — Generar artefacto: `module-impact-map.md`

```markdown
# Module Impact Map — v[X.Y.Z]

## Resumen de Impacto

| Módulo L2 | Tickets | Core | UX/UI | Riesgo |
|-----------|---------|------|-------|--------|
| boards | [N] | [N] | [N] | 🔴/🟠/🟡 |
| connections | [N] | [N] | [N] | 🔴/🟠/🟡 |
| auth | [N] | [N] | [N] | 🔴/🟠/🟡 |
| ... | | | | |

## Detalle por Módulo

### boards
- IONF-XXX (bug-fix, core): [título]
- IONF-YYY (new-feature, ux-ui): [título]

### connections
- IONF-ZZZ (improvement, core): [título]
...
```

Riesgo = función de: cantidad de tickets × prioridad × scope core.

---

## Stage 3 — REPORTING

### Paso 3.1 — Presentar resumen

```
🔄 RELEASE INGEST v[X.Y.Z] — COMPLETADO

Tickets procesados: [N]/[Total]
MCP errors: [N] (listados abajo)

Distribución por tipo:
  🚀 New Features: [N]
  🐛 Bug Fixes: [N]
  ⚡ Improvements: [N]
  🔧 Refactors/Infra: [N]

Distribución por área:
  [área]: [N] tickets
  ...

Cobertura de custom fields:
  custom_type: [N]/[Total] ([%]%)
  iond_subcategory: [N]/[Total] ([%]%)
  tags core/ux-ui: [N]/[Total] ([%]%)

Artefactos generados:
  ✅ ticket-synthesis.md
  ✅ tracking-list.md + .csv
  ✅ module-impact-map.md

[Si hay MCP errors, listarlos aquí]

¿Procedo con el siguiente paso del pipeline?
```

### Paso 3.2 — Guardar artefactos

1. `ticket-synthesis.md` → `knowledge/releases/<version>/`
2. `tracking-list.md` → `knowledge/releases/<version>/`
3. `tracking-list.csv` → `knowledge/releases/<version>/`
4. `module-impact-map.md` → `knowledge/releases/<version>/`

---

## Reglas de este Skill

1. **CSV es la ÚNICA fuente de verdad para la lista de tickets** — Si no está en el CSV, no se procesa
2. **MCP es la fuente de detalles** — `getTaskById` para obtener custom fields, descripción, comentarios
3. **Custom fields tienen prioridad** — `custom_type` y `custom_iond_subcategory` antes que heurísticas
4. **Heurísticas son fallback** — Solo se usan cuando los custom fields están vacíos
5. **No saturar el MCP** — Procesar tickets uno a uno con reporte de progreso
6. **Errores no son bloqueantes** — Si un ticket falla en el MCP, continuar con los demás
7. **NUNCA modificar skills, templates o artefactos existentes** — Solo generar nuevos
8. **Artefactos por versión** — Output en `knowledge/releases/<version>/`

---

## Checklist de cierre

- □ CSV validado y parseado
- □ MCP conectado y funcionando
- □ [N]/[N] tickets procesados via MCP
- □ Clasificación de tipo completada (custom_type o fallback)
- □ Clasificación de área completada (iond_subcategory o fallback)
- □ Scope identificado (tags core/ux-ui)
- □ Repos parseados desde Merge Request URLs
- □ Comentarios de aprobación/rechazo detectados
- □ ticket-synthesis.md generado
- □ tracking-list.md + .csv generados
- □ module-impact-map.md generado
- □ Resumen presentado al QA Engineer
- □ **NINGÚN skill o template existente fue modificado**
