# Skill: test-docs/document

> Genera documentación de QA para un ticket: Acceptance Criteria consolidados y Test Matrix completa. Opera en dos modos: AC y Matrix.

## Cuándo usar este skill

- **Discovery Track — Modo AC** (Paso 5): Consolidar y validar Acceptance Criteria con el equipo
- **Discovery Track — Modo Matrix** (Paso 6): Generar la Test Matrix completa del ticket
- **Discovery Track — Modo Architecture Brief** (Paso 7): Checklist QA del Architecture Brief

## Pre-requisitos

Antes de ejecutar este skill, el agente DEBE haber cargado:
- ✅ `knowledge/L1-project/business-rules.md`
- ✅ `knowledge/L1-project/test-priorities.md`
- ✅ `knowledge/L2-modules/<módulo>/module.md`
- ✅ Acceptance Criteria del ticket
- ✅ Output de `test-docs/prioritize` (risk-triage.md) si existe

---

## Paso 0: Obtener Contexto Completo del Ticket (OBLIGATORIO)

> ⚠️ **Este paso se ejecuta ANTES de entrar en cualquier modo (AC o Matrix).**
> Los AC en la descripción del ticket pueden NO reflejar las últimas decisiones.
> Las discusiones en los comentarios de ClickUp frecuentemente cambian el rumbo.

### 0.1 — Leer Descripción del Ticket

- Obtener la descripción completa del ticket via ClickUp MCP (`getTaskById`)
- Extraer los AC si existen en la descripción

### 0.2 — Leer Actividades/Comentarios del Ticket

- Leer **TODOS los comentarios** del ticket
- Identificar comentarios de: PO, Developers, QA, Stakeholders
- Buscar especialmente:
  - Decisiones que **modifican el alcance** original
  - Aclaraciones sobre **comportamiento esperado**
  - Nuevos requerimientos que surgieron **después** de la descripción
  - Cambios de rumbo ("finalmente decidimos que...", "actualizamos el approach a...")
  - Restricciones técnicas descubiertas durante desarrollo

### 0.3 — Reconciliar AC con Comentarios

- Comparar AC de la descripción vs las últimas decisiones en comentarios
- Si hay divergencias:

| AC Original | Decisión en Comentarios | AC Reconciliado | Fuente |
|---|---|---|---|
| AC-1: "El usuario puede crear..." | Comentario de PO: "Limitamos a admin" | AC-1 ACTUALIZADO: "Solo admin puede crear..." | Comentario [fecha] por [autor] |
| AC-2: (no existe) | Developer: "Agregamos validación" | AC-3 NUEVO: "El sistema valida el formato" | Comentario [fecha] por [autor] |

- Presentar tabla de reconciliación al QA Engineer
- **El QA Engineer valida** los AC reconciliados antes de continuar

### 0.4 — Documentar Fuentes

En cada AC del output final, incluir de dónde salió:

```
AC-1: [descripción del AC]
  Fuente: Descripción original del ticket

AC-2: [descripción del AC]
  Fuente: Comentario de [autor] el [fecha] — "[cita textual relevante]"

AC-3: [descripción del AC]
  Fuente: Acuerdo entre QA y Developer el [fecha] — "[cita]"
```

> **GATE**: ¿AC reconciliados con las últimas decisiones del equipo? → Continuar al modo solicitado.

---

## Modo AC — Consolidación de Acceptance Criteria

### Instrucciones

#### Stage 1 — PLANNING

Reporta al QA Engineer:
1. Los AC originales del ticket que vas a analizar
2. Los riesgos identificados por `prioritize` (si existen)
3. Tu plan de consolidación

**Espera aprobación antes de continuar.**

#### Stage 2 — EXECUTION

##### Paso 1: Evaluar AC existentes

Para cada AC del ticket, evalúa:

| AC | Texto original | ¿Es verificable? | ¿Es completo? | ¿Es ambiguo? | Observación |
|----|---------------|-------------------|----------------|---------------|-------------|
| AC-1 | ... | ✅/❌ | ✅/❌ | ✅/❌ | ... |

##### Paso 2: Proponer AC faltantes

Basado en el risk triage y las reglas de negocio, identifica AC que deberían existir pero no están en el ticket:

```
AC PROPUESTOS (para acordar con Developer y PO)

AC-N+1: Dado que [condición], cuando [acción], entonces [resultado esperado]
  Justificación: Basado en regla de negocio [X] / edge case [Y]

AC-N+2: ...
```

> **Regla**: Los AC propuestos se presentan como SUGERENCIAS, no como mandatos.
> El QA Engineer los discute con el Developer para llegar a un acuerdo.

##### Paso 3: Transformar cada AC en caso de test

Por cada AC (original + propuesto acordado):

| AC | Caso de test (happy path) | Casos edge | Caso negativo |
|----|--------------------------|------------|---------------|
| AC-1 | "El usuario puede..." | "Si el dato está vacío..." | "Si no tiene permisos..." |

#### Stage 3 — REPORTING

Guarda el output en `L3-tickets/<ticket-id>/ac-consolidated.md`:

```markdown
# Acceptance Criteria Consolidados — [TICKET-ID]

## AC Originales (del ticket)
[lista]

## AC Propuestos (acordados con el equipo)
[lista con justificación]

## AC Rechazados o Diferidos
[lista con razón — esto es normal, no es un fallo]

## Transformación AC → Casos de Test
[tabla del Paso 3]
```

---

## Modo Matrix — Generación de Test Matrix

### Instrucciones

#### Stage 1 — PLANNING

Reporta al QA Engineer:
1. Los AC consolidados que vas a usar como base
2. Los edge cases del risk triage
3. El módulo y sus dependencias
4. Estimación de cantidad de casos

**Espera aprobación antes de continuar.**

#### Stage 2 — EXECUTION

##### Paso 1: Generar Test Matrix

Usa el template `templates/test-matrix.md` y genera la matriz completa:

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-001 | [mod] | AC-1 | Happy Path | ... | ... | Company Login > Sidebar: [Módulo] > ... | ... | 🔴 | ✅/❌ | ⬜ |
| TC-002 | [mod] | AC-1 | Edge Case | ... | ... | Company Login > Sidebar: [Módulo] > ... | ... | 🟠 | ✅/❌ | ⬜ |
| TC-003 | [mod] | AC-1 | Negativo | ... | ... | Company Login > Sidebar: [Módulo] > ... | ... | 🟡 | ✅/❌ | ⬜ |

##### Formato de Pasos (columna "Pasos" — OBLIGATORIO)

> Los pasos DEBEN usar un formato de ruta de navegación explícito tipo **breadcrumb**.
> Esto permite que cualquier persona (IA o humano) pueda reproducir el caso sin ambigüedad.

**Formato**: `[Rol] Login > Sidebar: [Módulo] > [Acción] > [Sub-acción] > [Verificación]`

| Elemento | Formato | Ejemplo |
|----------|---------|--------|
| Login con rol | `Company Login` / `Admin Login` | `Company Login` |
| Navegación sidebar | `Sidebar: [nombre]` | `Sidebar: Boards` |
| Navegación URL | `Navigate: /ruta` | `Navigate: /workflows` |
| Click en elemento | `Click [elemento]` | `Click [Flow "Mi Flow"]` |
| Click en botón | `Button: [nombre]` | `Button: "Ask Flow Pilot"` |
| Abrir panel/drawer | `Drawer: [nombre]` / `Panel: [nombre]` | `Drawer: Code Config` |
| Llenar campo | `Fill [campo]: [valor]` | `Fill "Name": "Test Flow"` |
| Seleccionar opción | `Select [campo]: [opción]` | `Select "Language": Python` |
| Verificar | `Verify: [qué]` | `Verify: Toast "Created successfully"` |
| Esperar | `Wait: [qué]` | `Wait: Agent response` |

**Ejemplos:**

❌ Incorrecto: `Abrir flow | Click en Code node | Verificar drawer`

✅ Correcto: `Company Login > Sidebar: Boards > Click [Flow "Test Flow"] > Canvas: Click [Code Node] > Drawer: Code Config > Verify: Button "Ask Flow Pilot" visible`

##### Paso 2: Agregar casos de regresión

Identifica tests de regresión que el feature podría romper:

| ID | Módulo impactado | Caso de regresión | Por qué podría romperse | Prioridad |
|----|-----------------|-------------------|------------------------|-----------|
| REG-001 | [otro módulo] | ... | Porque el feature toca [tabla/endpoint/componente] | 🔴/🟠 |

##### Paso 3: Agregar verificaciones de BD

> ⚠️ **REGLA CRÍTICA: Las queries DEBEN basarse EXCLUSIVAMENTE en los schemas**
> **definidos en los archivos de migración de los repos fuente.**
>
> Fuentes de schema:
>   - `../flow_binaries/migrations/*.sql` → Schema core Go + SQLite
>   - `../gateway/database/migrations/*.php` → Schema legacy PostgreSQL
>   - `knowledge/L2-modules/<módulo>/module.md` → Sección "Database"
>
> ❌ NUNCA inventar nombres de campos, tablas ni relaciones
> ❌ NUNCA asumir que existe una columna sin verificar en las migraciones
> ✅ SIEMPRE leer las migraciones del repo ANTES de generar una query
> ✅ SIEMPRE incluir referencia a la migración fuente como comentario

Antes de generar cualquier query:
1. Leer las migraciones relevantes del repo fuente
2. Verificar que la tabla existe y tiene las columnas referenciadas
3. Verificar las relaciones (foreign keys) desde las migraciones

Genera queries de verificación para incluir en la ejecución:

```sql
-- Fuente: ../gateway/database/migrations/2024_10_30_create_flows_table.php
-- Tabla: flows | Columnas verificadas: id, name, company_id, status

-- TC-001: Verificar creación de registro
SELECT id, name, company_id, status FROM flows WHERE company_id = '<company_id>' AND name = '<nombre>';

-- TC-003: Verificar que el registro NO se creó (caso negativo)
SELECT COUNT(*) FROM flows WHERE company_id = '<company_id>' AND name = '<nombre>';
-- Esperado: 0
```

##### Paso 4: Generar CSV de la Test Matrix

Genera una copia de la Test Matrix en formato CSV para registro, compartir con el equipo o importar en herramientas externas.

El CSV debe tener estas columnas:

```csv
ID,Módulo,AC,Tipo,Caso de Test,Precondición,Pasos,Resultado Esperado,Prioridad,Automatizable,Estado
TC-001,[mod],AC-1,Happy Path,[descripción],[precondición],"Company Login > Sidebar: [Módulo] > ...",[esperado],Crítico,Sí,Pendiente
TC-002,[mod],AC-1,Edge Case,[descripción],[precondición],"Company Login > Sidebar: [Módulo] > ...",[esperado],Alto,No,Pendiente
TC-003,[mod],AC-1,Negativo,[descripción],[precondición],"Company Login > Sidebar: [Módulo] > ...",[esperado],Medio,No,Pendiente
REG-001,[mod],N/A,Regresión,[descripción],[precondición],"Company Login > Sidebar: [Módulo] > ...",[esperado],Alto,Sí,Pendiente
```

**Reglas del CSV**:
- Encoding: UTF-8
- Separador: coma (`,`)
- Si un campo contiene comas, encerrarlo entre comillas dobles
- Los pasos usan ` > ` como separador (formato breadcrumb)
- Prioridades como texto: `Crítico`, `Alto`, `Medio`, `Bajo`
- Automatizable: `Sí` / `No`
- Estado: `Pendiente`, `Aprobado`, `Fallido`, `Saltado`

#### Stage 3 — REPORTING

Genera **dos archivos** en `L3-tickets/<ticket-id>/`:

**1. `test-matrix.md`** — Versión Markdown (para lectura y edición):

```markdown
# Test Matrix — [TICKET-ID]

## Resumen
- Total de casos: [N]
- Happy path: [N]
- Edge cases: [N]
- Negativos: [N]
- Regresión: [N]
- Automatizables: [N]

## Test Matrix
[tabla del Paso 1]

## Casos de Regresión
[tabla del Paso 2]

## Queries de Verificación BD
[queries del Paso 3]
```

**2. `test-matrix.csv`** — Versión CSV (para compartir y registro):

Archivo CSV generado según formato del Paso 4.

---

## Modo Architecture Brief — Checklist QA

### Instrucciones

Cuando se presenta un Architecture Brief (Paso 7 del Altacrest Discovery), usa el template `templates/architecture-brief-qa.md` y evalúa:

| Área | Pregunta | Estado | Observación |
|------|----------|--------|-------------|
| Seguridad | ¿Se validaron permisos por company/usuario? | ⬜ | |
| Logging | ¿Los cambios generan logs auditables? | ⬜ | |
| Rollback | ¿Se puede revertir el cambio sin pérdida de datos? | ⬜ | |
| API | ¿Los endpoints nuevos tienen validación de input? | ⬜ | |
| BD | ¿Las migraciones son reversibles? | ⬜ | |
| Multi-tenant | ¿Funciona correctamente para diferentes companies? | ⬜ | |
| Performance | ¿El cambio puede impactar el rendimiento? | ⬜ | |
| Ejecución | ¿Impacta la ejecución de flows/nodos (SQLite)? | ⬜ | |

Guarda en `L3-tickets/<ticket-id>/architecture-brief-qa.md`.

---

## Reglas de este Skill

1. **Paso 0 es OBLIGATORIO** — Siempre reconciliar AC con comentarios de ClickUp antes de cualquier modo
2. **En modo AC**: El output son AC verificables y completos — no rechazos
3. **En modo Matrix**: El output es la matriz completa lista para ejecución en Deployment
4. **Siempre incluir happy path + edge + negativo** para cada AC
5. **Los pasos usan formato breadcrumb** — `Company Login > Sidebar: Boards > ...`
6. **Los casos de regresión son obligatorios** si el feature toca más de un módulo
7. **Las queries de BD son obligatorias** si el feature modifica datos
8. **Queries basadas en migraciones** — NUNCA inventar campos, tablas ni relaciones
9. **Si no hay risk-triage previo**, ejecutar `test-docs/prioritize` primero
10. **Cada AC incluye su fuente** — Descripción original, comentario, o acuerdo
