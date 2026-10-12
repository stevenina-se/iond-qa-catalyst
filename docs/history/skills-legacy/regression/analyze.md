# Skill: regression/analyze

> Analiza los resultados de una regresión para clasificar cada fallo: ¿es un bug real, un test flaky, o un problema de entorno?

## Cuándo usar este skill

- **Post-regression**: Después de que `regression/run` registre los resultados
- **Triage**: Cuando hay fallos y se necesita decidir el impacto antes del release

## Pre-requisitos

- ✅ Resultados de `regression/run` (regression results del run actual)
- ✅ Resultados anteriores si existen (para comparar)
- ✅ `knowledge/L1-project/test-priorities.md` — Criticidad de módulos
- ✅ Acceso al código de los tests en `../bot-test/`

---

## Instrucciones de Ejecución

### Stage 1 — PLANNING

Reporta al QA Engineer:
1. Cuántos tests fallaron
2. En qué módulos están los fallos
3. Si hay runs anteriores para comparar

### Stage 2 — EXECUTION

#### Paso 1: Clasificar cada fallo

Para cada test fallido, analiza el error y clasifica:

| Test | Error | Clasificación | Confianza | Acción |
|------|-------|--------------|-----------|--------|
| `should create flow` | Timeout `.flow-card` | 🔴 Bug real | Alta | Investigar |
| `should login` | Network error | 🟡 Entorno | Alta | Re-ejecutar |
| `should list items` | Element not found (intermitente) | 🟠 Flaky | Media | Estabilizar test |

#### Categorías de clasificación

| Categoría | Descripción | Acción sugerida |
|-----------|-------------|-----------------|
| 🔴 **Bug real** | El comportamiento de la app cambió, el test detectó un problema real | Crear bug, bloquear release si es crítico |
| 🟠 **Test flaky** | El test falla intermitentemente por timing, race conditions, etc. | Estabilizar el test (no es un bug de la app) |
| 🟡 **Entorno** | Fallo por problema del entorno (red, servidor, deploy incompleto) | Re-ejecutar en entorno estable |
| 🔵 **Test obsoleto** | El feature cambió legítimamente y el test no se actualizó | Actualizar el test |
| ⚪ **Dato de prueba** | El test depende de datos que ya no existen | Actualizar fixtures/seed |

#### Paso 2: Comparar con runs anteriores

Si hay resultados históricos:

| Test | Run anterior | Run actual | Tendencia |
|------|-------------|-----------|-----------|
| `should create flow` | ✅ Pass | ❌ Fail | 📉 Regresión (posible bug nuevo) |
| `should list items` | ❌ Fail | ❌ Fail | ➡️ Conocido (flaky existente) |
| `should validate form` | ✅ Pass | ✅ Pass | ✅ Estable |

> Si un test que antes pasaba ahora falla → alta probabilidad de **bug real**.

#### Paso 3: Analizar impacto por módulo

Consulta `test-priorities.md` para evaluar el impacto:

| Módulo | Fallos | Criticidad del módulo | Impacto en release |
|--------|--------|----------------------|-------------------|
| auth | 0 | 🟠 Alto | ✅ Sin impacto |
| flows | 2 | 🔴 Crítico | ⚠️ Investigar antes de release |
| connectors | 1 (flaky) | 🟠 Alto | ✅ Flaky conocido, no bloquea |

### Stage 3 — REPORTING

Guarda el análisis junto al run:

```markdown
# Regression Analysis — [fecha]

## Resumen
- Tests fallidos analizados: [N]
- Bugs reales: [N] — 🔴
- Tests flaky: [N] — 🟠
- Problemas de entorno: [N] — 🟡
- Tests obsoletos: [N] — 🔵
- Datos de prueba: [N] — ⚪

## Impacto por módulo
[tabla del Paso 3]

## Clasificación detallada
[tabla del Paso 1]

## Comparación con run anterior
[tabla del Paso 2]

## Recomendación
→ Pasar a `regression/decide` para el veredicto Go/No-Go
```

---

## Reglas de este Skill

1. **No asumir que todo fallo es un bug** — Clasificar antes de escalar
2. **Comparar con historial** — Un fallo nuevo tiene más peso que uno conocido
3. **La criticidad del módulo importa** — Un fallo en `flows` es más grave que en `dashboard`
4. **Tests flaky se reportan pero no bloquean release** — Se marcan para estabilizar
5. **El análisis es para informar al QA Engineer** — Él decide con `regression/decide`
