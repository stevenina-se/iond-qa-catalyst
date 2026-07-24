# Skill: release/notes

> Genera dos versiones de release notes: una interna (dev/producto/soporte/compañeros) y otra para clientes.
> Requiere datos del release: `ticket-synthesis.md` (preferido) o `tracking-list.md` como mínimo.

---

## Cuándo usar este skill

**Frase disparadora:**
```
Generar release notes: v[X.Y.Z]
```

**Pre-condición**: El release plan o ingest debe haberse ejecutado previamente.

---

## Pre-requisitos

### Fuentes de datos (en orden de preferencia)

| Prioridad | Artefacto | Generado por | Contenido |
|-----------|-----------|-------------|-----------|
| 1️⃣ Preferida | `ticket-synthesis.md` | `release/ingest` | Síntesis completa: tipo, área, scope, AC, aprobación |
| 2️⃣ Alternativa | `tracking-list.md` + CSV | `release/plan` | Lista clasificada de tickets |
| 3️⃣ Mínima | `release-tickets.csv` + MCP | Manual + ClickUp | CSV como fuente de IDs, MCP para detalles |

> Si solo existe el CSV (sin ingest previo), la skill ejecutará una **mini-ingesta** on-the-fly:
> para cada `internal_id` del CSV → `getTaskById` → extraer tipo, descripción, AC, custom fields.

### Contexto obligatorio

- ✅ `knowledge/L1-project/business-rules.md` para contexto de negocio

---

## Stage 1 — PLANNING

### Paso 1.1 — Determinar fuente de datos disponible

```
¿Existe ticket-synthesis.md?
  → SÍ: Usar como fuente primaria (datos ya sintetizados)
  → NO: ¿Existe tracking-list.md?
    → SÍ: Usar tracking-list + complementar con MCP si se necesitan detalles
    → NO: ¿Existe release-tickets.csv?
      → SÍ: Ejecutar mini-ingesta on-the-fly (CSV + MCP)
      → NO: PARAR → No hay datos de release disponibles
```

### Paso 1.2 — Mini-ingesta on-the-fly (solo si no hay ticket-synthesis.md)

Si la fuente es el CSV directamente:

1. Parsear CSV → lista de `internal_id, custom_id, nombre, status, prioridad`
2. Para cada ticket, invocar `getTaskById(internal_id)` via ClickUp MCP
3. Extraer de la respuesta:
   - **Tipo**: `custom_type` del MCP (Bug, New Feature, Improvement, Refactor)
     - Si vacío → inferir del nombre: "Fix/Corregir/Error" → `bug-fix`, "Crear/Implementar" → `new-feature`, etc.
   - **Área**: `custom_iond_subcategory` del MCP (Boards, PDF Templates, Connections...)
     - Si vacío → inferir del nombre: "Board/Flow/Nodo" → `boards`, "PDF/Template" → `pdf-templates`, etc.
   - **Scope**: tags del MCP
     - `core` → cambio de motor/backend
     - `ux-ui` → cambio visual/frontend
     - Si no hay tag relevante → inferir de la descripción
   - **Descripción y AC**: body del ticket
   - **Repos afectados**: URLs de `custom_merge_request`, `_2`, `_3` → parsear dominio/path
   - **Aprobación**: buscar comentario con patrón "APROBADO ✅" o "RECHAZADO ❌"
4. Clasificar con la tabla de mapeo:

   | `custom_type` | Tag del release |
   |---------------|----------------|
   | `New Feature` | `new-feature` |
   | `Bug` | `bug-fix` |
   | `Improvement` | `improvement` |
   | `Refactor` | `refactor` |
   | `Task` | `task` |
   | `Story` | `new-feature` |
   | (vacío) | Fallback a heurísticas de texto |

### Paso 1.3 — Anunciar el plan

```
📝 RELEASE NOTES — PLAN

Versión: v[X.Y.Z]
Fuente de datos: [ticket-synthesis.md / tracking-list.md / CSV + MCP]
Total de tickets: [N]
Distribución:
  🚀 New features: [N]
  🐛 Bug fixes: [N]
  ⚡ Improvements: [N]
  🔧 Internos (refactor/infra): [N]

Distribución por área (Iond Subcategory):
  [Área]: [N] tickets
  [Área]: [N] tickets
  ...

Tags de scope:
  Core: [N] tickets
  UX/UI: [N] tickets
  Sin tag: [N] tickets

Plan de ejecución:
  1. Agrupar tickets por tipo y área
  2. Generar versión INTERNA
  3. Generar versión CLIENTE
  4. Exportar ambos documentos

¿Procedo?
```

**Esperar confirmación.**

---

## Stage 2 — EXECUTION

### Paso 2.1 — Agrupar tickets por tipo y área

**Agrupación primaria (por tipo):**

| Categoría | Fuente de clasificación | Sección del release notes |
|-----------|------------------------|--------------------------|
| Nuevas funcionalidades | `custom_type` = `New Feature` o `Story` | 🚀 Nuevas Funcionalidades |
| Correcciones | `custom_type` = `Bug` | 🐛 Correcciones |
| Mejoras | `custom_type` = `Improvement` | ⚡ Mejoras |
| Cambios internos | `custom_type` = `Refactor` o `Task` | 🔧 Cambios Internos (solo interna) |
| Breaking changes | Detectar en comentarios/descripción | ⚠️ Breaking Changes |

**Agrupación secundaria (por área, dentro de cada tipo):**

Usar `custom_iond_subcategory` para sub-agrupar dentro de cada sección:
```
🚀 Nuevas Funcionalidades
  📂 Boards
    - IONF-XXX: [descripción]
  📂 Connections
    - IONF-YYY: [descripción]
  📂 Integrations
    - IONF-ZZZ: [descripción]
```

Si `custom_iond_subcategory` no está disponible (v0.1.0), agrupar por área inferida del nombre.

Tickets con status `Closed` y que NO estén en esta versión → NO incluir.
Tickets con tag `defer-to-next` → NO incluir.

### Paso 2.2 — Generar versión INTERNA

Usando template `templates/release-notes.md` con tipo `internal`:

**Estructura:**

1. **Resumen Ejecutivo**
   - Estadísticas: N features, N bugs, N mejoras, N internos
   - Distribución por área: "Boards ([N]), Connections ([N]), Auth ([N])..."
   - Distribución por scope: "Core: [N] cambios, UX/UI: [N] cambios"

2. **Highlights** (los 3-5 cambios más importantes)
   - Priorizar: tickets `urgent` > `high` con scope `core`
   - Cada highlight: título descriptivo + 1-2 oraciones de impacto

3. **🚀 Nuevas Funcionalidades** (sub-agrupadas por área)
   - Formato: `**IONF-XXX** — [título]` + breve descripción del cambio
   - Repos afectados entre paréntesis: `(gateway-ion, webcomponents-flow)`

4. **🐛 Correcciones** (sub-agrupadas por área)
   - Formato: `**IONF-XXX** — [título]`
   - Si hubo rechazo previo (`custom_rejection_count` > 0): notar "(re-tested)"

5. **⚡ Mejoras**
   - Formato: `**IONF-XXX** — [título]`

6. **🔧 Cambios Internos** (solo interna)
   - Refactors, infra, Sonar fixes
   - Formato: `**IONF-XXX** — [título]` + repo afectado

7. **⚠️ Breaking Changes** (si hay)
   - Qué cambió técnicamente
   - Cómo adaptarse (instrucciones)

8. **📋 Información del Release**
   - Tabla: versión, fecha, entorno, contacto

**Tono:** técnico-profesional, dirigido a compañeros de desarrollo, producto y soporte.
**Formato:** listo para copiar a Slack/email sin formateo roto.

### Paso 2.3 — Generar versión CLIENTE

Usando template `templates/release-notes.md` con tipo `client`:

**Incluir:**
- Solo cambios visibles para el usuario final (scope `ux-ui` o tickets `user-facing`)
- Tickets con scope `core` se incluyen solo si tienen impacto visible en la UI
- Lenguaje orientado a beneficios:
  - Features: "**Ahora puedes** [beneficio]"
  - Bug fixes: "**Corregimos** [problema que tenías]"
  - Improvements: "**Mejoramos** [aspecto de la experiencia]"
- Breaking changes: "**Qué necesitas hacer:**" con instrucciones paso a paso
- Resumen ejecutivo: 2-3 oraciones user-friendly

**NO incluir:**
- Cambios internos, refactors, infra, Sonar fixes
- Repos, branches, detalles técnicos, IDs de MRs
- IDs de tickets (usar descripciones user-friendly, IONF-XXX NO aparece)
- Jerga técnica

**Tono:** user-friendly, orientado al beneficio del cliente.

**Sub-agrupar por área** (usando nombres amigables):
```
🚀 Nuevas Funcionalidades
  🔧 Automatización de Flujos (Boards)
    - Ahora puedes crear flujos con el nodo Switch dinámico...
  📄 Plantillas PDF
    - Ahora puedes diseñar y editar tus propias plantillas PDF...
```

---

## Stage 3 — REPORTING

### Paso 3.1 — Presentar ambas versiones

```
📝 RELEASE NOTES v[X.Y.Z] — DRAFT

Fuente de datos: [ticket-synthesis.md / CSV + MCP]
Tickets procesados: [N] total
  🚀 Features: [N] | 🐛 Bugs: [N] | ⚡ Mejoras: [N] | 🔧 Internos: [N]

━━━ VERSIÓN INTERNA ━━━
[Contenido completo]
━━━━━━━━━━━━━━━━━━━━━━━

━━━ VERSIÓN CLIENTE ━━━
[Contenido completo]
━━━━━━━━━━━━━━━━━━━━━━━

¿Apruebas ambas versiones o deseas ajustar algo?
```

### Paso 3.2 — Guardar artefactos

Una vez aprobado:

1. **`release-notes-internal.md`** → `knowledge/releases/<version>/`
2. **`release-notes-client.md`** → `knowledge/releases/<version>/`

---

## Reglas de este Skill

1. **SIEMPRE generar ambas versiones** — Interna y cliente, sin excepción
2. **Clasificación por custom fields primero** — `custom_type` y `custom_iond_subcategory` tienen prioridad sobre heurísticas
3. **Fallback a heurísticas solo cuando custom fields están vacíos** — Común en v0.1.0, raro en v0.1.1+
4. **Tags `core`/`ux-ui` influyen en qué va a versión cliente** — Solo `ux-ui` + `user-facing` van a la versión cliente
5. **Tickets con `defer-to-next` NO se incluyen** — Solo lo que entra en este release
6. **La versión cliente NO tiene jerga técnica** — Si algo suena a desarrollo, reescribirlo
7. **El Scrum Master aprueba antes de guardar** — Los release notes son documentos oficiales
8. **NUNCA modificar skills, templates o artefactos existentes** — Solo invocar o referenciar
9. **Artefactos por versión** — Output en `knowledge/releases/<version>/`

---

## Checklist de cierre

- □ Fuente de datos identificada y cargada
- □ Mini-ingesta ejecutada (si aplica)
- □ Tickets clasificados por tipo (`custom_type` o fallback)
- □ Tickets agrupados por área (`custom_iond_subcategory` o fallback)
- □ Scope identificado (core/ux-ui desde tags)
- □ Versión interna generada (repos, detalles técnicos, agrupada por área)
- □ Versión cliente generada (beneficios, sin jerga, agrupada por área)
- □ Resumen ejecutivo en ambas versiones (con estadísticas)
- □ Highlights identificados (3-5 cambios más importantes, basados en prioridad)
- □ Ambas versiones aprobadas por el Scrum Master
- □ Artefactos guardados en `knowledge/releases/<version>/`
- □ **NINGÚN skill o template existente fue modificado**
