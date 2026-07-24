# Skill: release/smoke-matrix

> Genera una matriz de smoke test acotada para validar rápidamente que un deploy no rompió el sistema.
> Se construye desde cero basada en los 9 flujos críticos del L1.
> Consume artefactos de `release/ingest` (preferido) para mapeo de riesgo automático.

---

## Cuándo usar este skill

**Frase disparadora:**
```
Generar smoke matrix: v[X.Y.Z]
```

Seguida opcionalmente de:
- **URL del entorno** — ej. `entorno: dev-app.ionflow.io`

**Pre-condición**: El release ingest o plan debe haberse ejecutado.

---

## Pre-requisitos

### Fuentes de datos (en orden de preferencia)

| Prioridad | Artefacto | Generado por | Contenido |
|-----------|-----------|-------------|----------|
| 1️⃣ Preferida | `module-impact-map.md` + `ticket-synthesis.md` | `release/ingest` | Mapeo automático de riesgo por flujo + datos de tickets |
| 2️⃣ Alternativa | `tracking-list.md` | `release/plan` | Lista clasificada de tickets |

### Contexto obligatorio

- ✅ `knowledge/L1-project/test-priorities.md` (sección "Áreas de Regresión Crítica")
- ✅ `knowledge/L2-modules/<módulo>/module.md` de los módulos principales

---

## Stage 1 — PLANNING

### Paso 1.1 — Cargar contexto

1. Leer `module-impact-map.md` + `ticket-synthesis.md` (si existen, del ingest)
   - Si no existen → leer `tracking-list.md` como alternativa
2. Leer `knowledge/L1-project/test-priorities.md` → sección "Áreas de Regresión Crítica" (9 flujos)
3. Leer L2 de los módulos principales para complementar

> ⚠️ El smoke se construye **desde cero cada vez**, tomando como columna vertebral
> los 9 flujos de "Áreas de Regresión Crítica" del L1.

### Paso 1.2 — Identificar riesgo por release

**Si `module-impact-map.md` existe (del ingest):**
- Cruzar automáticamente módulos impactados con los 9 flujos críticos
- Tickets con tag `core` → riesgo sistémico (más TCs de smoke funcionales)
- Tickets con tag `ux-ui` → riesgo visual (TCs de smoke visuales obligatorios)

**Si no existe:**
- Desde la tracking list, identificar manualmente qué flujos fueron impactados

```
| Flujo Crítico | ¿Impactado? | Tickets que lo afectan | Scope |
|--------------|------------|----------------------|-------|
| Login / Auth | ✅ Sí | IONF-362, IONF-114 | core |
| Crear flow   | ❌ No | — | — |
| ...          | ... | ... | ... |
```

### Paso 1.3 — Anunciar el plan

```
🔍 SMOKE MATRIX — PLAN

Versión: v[X.Y.Z]
Entorno: [URL]
Flujos críticos: 9 (de test-priorities.md)
Flujos impactados por release: [N] de 9

Plan de ejecución:
  1. Generar 1-3 TCs por cada flujo crítico
  2. Agregar TCs específicos para flujos impactados
  3. Marcar riesgo por versión
  4. Exportar en .md y .csv

Tiempo estimado de ejecución: ~[X] min

¿Procedo?
```

**Esperar confirmación.**

---

## Stage 2 — EXECUTION

### Paso 2.1 — Generar TCs desde los 9 flujos críticos

Columna vertebral del smoke (de `test-priorities.md`):

| # | Flujo Crítico | Pregunta clave |
|---|--------------|----------------|
| 1 | Login / Auth flow | ¿Los usuarios pueden entrar? |
| 2 | Crear un flow | ¿Se puede crear y guardar un flow nuevo? |
| 3 | Agregar nodos a un flow | ¿El canvas funciona y los nodos se conectan? |
| 4 | Ejecutar un flow | ¿La ejecución termina correctamente? |
| 5 | Ver historial de ejecuciones | ¿Los logs son correctos? |
| 6 | Crear conexiones | ¿Es posible crear nuevas conexiones? |
| 7 | Crear y editar un conector | ¿Se puede crear y editar un conector nuevo? |
| 8 | Crear y editar un service | ¿Se puede crear y editar un service nuevo? |
| 9 | Template PDF | ¿Se puede crear, editar y utilizar un template de PDF? |

Para cada flujo, generar **1-3 TCs concretos** que verifiquen la pregunta clave.

**Reglas para cada TC:**
- Paso breadcrumb explícito
- Verificable en **menos de 2 minutos**
- Sin acceso a BD — solo UI/API observable
- Compatible con ejecución vía Playwright MCP

**Ejemplo:**
```
| SM-001 | Login / Auth | Login Company con Keycloak |
  Pasos: Navigate: dev-app.ionflow.io > Fill #username: [user] > Fill #password: [pass] > Click #kc-login > Verify: Dashboard visible
  Esperado: Dashboard carga correctamente con el nombre de la company visible
  Riesgo: 🔴 (impactado por IONF-362)
  Prioridad: 🔴
```

### Paso 2.2 — Agregar TCs específicos del release

Para flujos tocados por el release actual: agregar **1-2 TCs de validación específica** derivados de la tracking list.

Estos TCs tienen prefijo `SM-R-` y se enfocan en el cambio concreto del ticket:

```
| SM-R-001 | IONF-362 | Verificar login SSO funciona después del cambio |
  Pasos: Navigate: dev-app.ionflow.io > Click "Login with SSO" > ...
  Esperado: SSO redirige correctamente y el usuario accede
```

### Paso 2.3 — Marcar riesgo por versión

- TCs cuyo módulo fue tocado por el release → `🔴 Riesgo Alto`
- TCs de módulos no tocados → `🟢 Baseline`

### Paso 2.4 — Estimar tiempo total

```
| Bloque | TCs | Tiempo estimado |
|--------|-----|----------------|
| Flujos base (9) | [N] | ~[X] min |
| TCs específicos del release | [N] | ~[X] min |
| **Total** | **[N]** | **~[X] min** |
```

---

## Stage 3 — REPORTING

### Paso 3.1 — Presentar al QA Engineer

```
🔍 SMOKE MATRIX v[X.Y.Z] — DRAFT

Total TCs: [N]
  - Flujos base: [N] TCs en 9 flujos
  - TCs específicos del release: [N]
  - Riesgo Alto: [N]
  - Baseline: [N]

Tiempo estimado: ~[X] min

Modo sugerido: [Playwright MCP / Manual]

¿Apruebas la matriz o deseas ajustar?
```

### Paso 3.2 — Guardar artefactos

Una vez aprobado:

1. **`smoke-matrix.md`** → `knowledge/releases/<version>/`
2. **`smoke-matrix.csv`** → `knowledge/releases/<version>/`

---

## Reglas de este Skill

1. **Se construye desde cero** — No hay CSV de referencia, solo los 9 flujos del L1
2. **Cada TC verificable en < 2 minutos** — El smoke debe ser rápido
3. **Sin acceso a BD** — Solo UI/API observable
4. **Pasos breadcrumb obligatorios** — Reproducibles por cualquier persona
5. **Compatible con Playwright MCP** — Los TCs deben poder ejecutarse con el browser asistido
6. **Output en .md Y .csv** — Siempre ambos formatos
7. **NUNCA modificar skills, templates o artefactos existentes**
8. **Artefactos por versión** — Output en `knowledge/releases/<version>/`

---

## Checklist de cierre

- □ Tracking list cargada
- □ test-priorities.md cargado (9 flujos críticos)
- □ L2 de módulos principales cargados
- □ Los 9 flujos críticos cubiertos con TCs
- □ TCs específicos del release agregados
- □ Riesgo marcado por versión
- □ Tiempo estimado calculado
- □ Matriz exportada en .md y .csv
- □ **NINGÚN skill o template existente fue modificado**
