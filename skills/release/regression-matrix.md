# Skill: release/regression-matrix

> Genera una matriz de regresión completa por versión, cubriendo todos los módulos críticos
> y los tickets del release que pudieron introducir regresiones.
> Consume artefactos de `release/ingest` (preferido) o `tracking-list.md` como mínimo.
> Usa el CSV `Test Plan - IONFLOW - Smoke Test.csv` como guía complementaria.

---

## Cuándo usar este skill

**Frase disparadora:**
```
Generar regression matrix: v[X.Y.Z]
```

**Pre-condición**: El release ingest o plan debe haberse ejecutado.

---

## Pre-requisitos

### Fuentes de datos (en orden de preferencia)

| Prioridad | Artefacto | Generado por | Contenido |
|-----------|-----------|-------------|----------|
| 1️⃣ Preferida | `ticket-synthesis.md` + `module-impact-map.md` | `release/ingest` | Síntesis completa con tipo, área, scope, AC |
| 2️⃣ Alternativa | `tracking-list.md` | `release/plan` | Lista clasificada de tickets |

### Contexto obligatorio

- ✅ `knowledge/L1-project/test-priorities.md` para criticidad por módulo
- ✅ `knowledge/L2-modules/<módulo>/module.md` de los módulos afectados
- ✅ CSV de regresión: `Test Plan - IONFLOW - Smoke Test.csv` (guía complementaria)
- ✅ Los 4 repositorios de desarrollo accesibles en `../`

### Herencia de versiones anteriores (opcional)

- ⬜ `knowledge/releases/<version-anterior>/regression-matrix.md` — Si existe, heredar TCs BASELINE relevantes

---

## Stage 1 — PLANNING

### Paso 1.1 — Cargar contexto

1. Leer `ticket-synthesis.md` + `module-impact-map.md` (si existen, del ingest)
   - Si no existen → leer `tracking-list.md` como alternativa
2. Leer `knowledge/L1-project/test-priorities.md` (criticidad por módulo)
3. Leer CSV de regresión como guía complementaria
4. Leer `regression-matrix.md` de la versión anterior (si existe) para herencia de TCs

> ⚠️ El CSV es solo una **guía complementaria**. La skill debe complementarlo con:
> - Datos reales de los tickets: AC, descripción, repos (de `ticket-synthesis.md`)
> - Módulos/features que el CSV marcaba como "Skipped" pero que ahora están implementados
> - TCs específicos derivados del contenido real del ticket (cross-impact)
> - Actualización de observaciones que ya no apliquen

### Paso 1.2 — Identificar módulos

**Si `module-impact-map.md` existe (del ingest):**
- Usar directamente como fuente de mapeo ticket → módulo(s) L2
- Incluye distribución core vs ux-ui por módulo

**Si no existe:**
- Desde la tracking list, mapear cada ticket → módulo(s) L2 afectados usando:
  - `custom_iond_subcategory` (si disponible) → módulo L2 directo
  - Heurísticas del nombre (fallback)

Cargar los L2 de cada módulo afectado.

### Paso 1.2b — Herencia de versión anterior

Si existe `knowledge/releases/<version-anterior>/regression-matrix.md`:
1. Leer la matriz anterior
2. Identificar TCs BASELINE que siguen siendo relevantes
3. Preservar TCs que cubren módulos críticos no tocados en esta versión
4. Actualizar observaciones que ya no apliquen por cambios de esta versión

### Paso 1.3 — Anunciar el plan

```
🔍 REGRESSION MATRIX — PLAN

Versión: v[X.Y.Z]
Tickets del release: [N]
Módulos afectados directamente: [lista]
Módulos cross-impact: [lista]
Módulos baseline (críticos, no tocados): [lista]

Fuentes:
  - Tracking list del release
  - CSV de regresión (guía)
  - L1 test-priorities.md
  - L2 de cada módulo

Repos a actualizar: gateway-ion, flow_binaries, gateway, webcomponents-flow

¿Procedo?
```

**Esperar confirmación.**

---

## Stage 2 — EXECUTION

### Paso 2.1 — Actualizar repos a DEVELOPMENT

```bash
# OBLIGATORIO: actualizar antes de analizar
cd ../gateway-ion && git fetch origin && git checkout DEVELOPMENT && git pull origin DEVELOPMENT
cd ../flow_binaries && git fetch origin && git checkout DEVELOPMENT && git pull origin DEVELOPMENT
cd ../gateway && git fetch origin && git checkout DEVELOPMENT && git pull origin DEVELOPMENT
cd ../webcomponents-flow && git fetch origin && git checkout DEVELOPMENT && git pull origin DEVELOPMENT
```

> ❌ NUNCA hacer git push, commit, ni merge — Solo operaciones de LECTURA

### Paso 2.2 — Mapear tickets a módulos

**Si `module-impact-map.md` existe:**
- Usar directamente — ya contiene el mapeo ticket → módulo(s) con scope (core/ux-ui)

**Si no existe, construir manualmente:**

```
| Ticket | Descripción | Módulo directo | Módulos cross-impact (del L2) | Scope |
|--------|-------------|---------------|-------------------------------|-------|
| IONF-1 | Nodo Memoria | data-store | boards (usa storage), canvas | core |
```

Consultar sección "Impacto Cruzado" de cada L2 afectado para identificar módulos indirectos.

### Paso 2.2b — Priorización por datos del release

Ajustar prioridad de los TCs basándose en:

| Factor | Efecto en prioridad |
|--------|--------------------|
| Ticket con `prioridad: urgent` | TC → 🔴 Crítico |
| Ticket con `prioridad: high` | TC → 🟠 Alto |
| Ticket con `prioridad: normal` | TC → según criticidad del módulo (L1) |
| Ticket con `prioridad: low` | TC → 🟢 Bajo |
| Tag `core` | ⬆️ Subir prioridad: más TCs de impacto cruzado |
| Tag `ux-ui` | TC solo en módulo directo (menor riesgo regresión cruzada) |
| `custom_rejection_count` > 0 | ⬆️ Subir prioridad: ticket rechazado previamente, más riesgo |

### Paso 2.3 — Generar TCs de regresión

Para cada módulo identificado, generar TCs en 3 categorías:

| Tipo | Cuándo | Fuente | Prioridad base |
|------|--------|--------|---------------|
| `[REGRESIÓN-DIRECTA]` | Módulo cambiado por un ticket del release | L2 del módulo + cambios del ticket | 🔴 Crítico |
| `[REGRESIÓN-INDIRECTA]` | Módulo impactado por cross-impact | Sección "Impacto Cruzado" del L2 | 🟠 Alto |
| `[BASELINE]` | Módulo 🔴 o 🟠 del L1, no tocado directamente | test-priorities.md "Áreas de Regresión Crítica" | 🟡 Medio |

**Para TCs de REGRESIÓN-DIRECTA:**
- Leer el L2 del módulo: sección de lógica de negocio, validaciones, edge cases
- Consultar el CSV guía: ¿qué features de este módulo estaban testeadas?
- Agregar TCs que cubran el happy path de la feature modificada
- Agregar TCs de edge cases documentados en el L2
- Revisar el código real (grep) para identificar validaciones que podrían haberse roto

**Para TCs de REGRESIÓN-INDIRECTA:**
- Basarse en la sección "Impacto Cruzado" del L2
- Verificar que la integración entre módulos sigue funcionando
- Enfocarse en las interfaces compartidas (endpoints, eventos, datos)

**Para TCs BASELINE:**
- Tomar de `test-priorities.md` los 9 flujos críticos
- Generar 1-2 TCs por flujo para verificar que el core no se rompió
- Solo para módulos que NO fueron tocados directamente

### Paso 2.4 — Construir la matriz

Usar las convenciones de `templates/release-regression-matrix.md`:

```
| ID | Side | Módulo | Tipo Regresión | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Estado |
```

**Reglas:**
- Pasos en formato **breadcrumb** obligatorio
- Prioridad basada en criticidad del módulo (L1) + tipo de regresión
- Compatible con ejecución vía Playwright MCP
- Incluir columna Side (KC, ADMIN, TENANT, ADMIN GATEWAY) heredada del CSV guía

### Paso 2.5 — Resumen de cobertura

```
| Módulo | Criticidad (L1) | Directos | Indirectos | Baseline | Total |
|--------|-----------------|---------|-----------|---------|-------|
| boards | 🔴 Crítico | 5 | 2 | 0 | 7 |
| auth   | 🟠 Alto | 0 | 1 | 2 | 3 |
```

---

## Stage 3 — REPORTING

### Paso 3.1 — Presentar al QA Engineer

```
🔍 REGRESSION MATRIX v[X.Y.Z] — DRAFT

Total TCs: [N]
  - Regresión directa: [N]
  - Regresión indirecta: [N]
  - Baseline: [N]

Módulos cubiertos: [N]

[Tabla de cobertura por módulo]

¿Apruebas la matriz o deseas ajustar?
```

### Paso 3.2 — Guardar artefactos

Una vez aprobado:

1. **`regression-matrix.md`** → `knowledge/releases/<version>/`
2. **`regression-matrix.csv`** → `knowledge/releases/<version>/`

---

## Reglas de este Skill

1. **El CSV de regresión es solo una guía** — Complementar con L1, L2 y código real
2. **Tres tipos de regresión** — DIRECTA, INDIRECTA y BASELINE. Cada TC debe estar etiquetado
3. **Pasos breadcrumb obligatorios** — Reproducibles por cualquier persona
4. **Actualizar observaciones del CSV** — Si el release invalida un "Skipped", actualizar
5. **NUNCA inventar código** — Protocolo de evidencia verificable aplica si se incluyen fragmentos
6. **Repos actualizados a DEVELOPMENT** — Obligatorio antes de analizar
7. **NUNCA hacer git push, commit, ni merge** — Solo lectura
8. **NUNCA modificar skills, templates o artefactos existentes**
9. **Output en .md Y .csv** — Siempre ambos formatos

---

## Checklist de cierre

- □ Tracking list cargada
- □ L1 test-priorities.md cargado
- □ L2 de cada módulo afectado cargado
- □ CSV de regresión leído como guía
- □ Repos actualizados a DEVELOPMENT
- □ Todos los módulos afectados cubiertos (directos + indirectos)
- □ TCs baseline para módulos críticos no tocados
- □ Pasos en formato breadcrumb
- □ Observaciones del CSV guía preservadas/actualizadas
- □ Matriz exportada en .md y .csv
- □ **NINGÚN skill o template existente fue modificado**
