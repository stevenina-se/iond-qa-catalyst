# Skill: sprint-testing/plan

> Genera un plan de testing estructurado para un ticket, listo para ser ejecutado en Deployment. Puede usarse en Discovery (preparar) o al inicio de Deployment (confirmar).

## Cuándo usar este skill

- **Discovery Track** (Paso 9): Crear el plan de testing antes de que el ticket pase a Deployment
- **Deployment Track** (Planning): Revisar y confirmar el plan al inicio del testing

## Pre-requisitos

Antes de ejecutar este skill, el agente DEBE haber cargado:
- ✅ `knowledge/L1-project/test-priorities.md`
- ✅ `knowledge/L2-modules/<módulo>/module.md`
- ✅ `L3-tickets/<ticket-id>/test-matrix.md` (si existe, del Discovery)
- ✅ `L3-tickets/<ticket-id>/ac-consolidated.md` (si existe)
- ✅ `L3-tickets/<ticket-id>/risk-triage.md` (si existe)

---

## Instrucciones de Ejecución

### Stage 1 — PLANNING

Reporta al QA Engineer:
1. El ticket que vas a planificar
2. Los artefactos de Discovery que encontraste (test-matrix, AC, risk-triage)
3. Si falta algún artefacto, señálalo
4. Tu propuesta de estructura del plan

**Espera aprobación antes de continuar.**

### Stage 2 — EXECUTION

#### Paso 1: Compilar contexto disponible

Revisa qué existe en `L3-tickets/<ticket-id>/`:

| Artefacto | Estado | Acción |
|-----------|--------|--------|
| `risk-triage.md` | ✅ Existe / ❌ No existe | Si no existe: ejecutar `test-docs/prioritize` primero |
| `ac-consolidated.md` | ✅ Existe / ❌ No existe | Si no existe: pedir AC al QA Engineer |
| `test-matrix.md` | ✅ Existe / ❌ No existe | Si no existe: ejecutar `test-docs/document` modo matrix |

#### Paso 2: Definir el orden de ejecución

Ordena los test cases por prioridad y dependencias:

```
ORDEN DE EJECUCIÓN — Ticket [ID]

BLOQUE 1 — SMOKE TESTS (ejecutar primero, si alguno falla → escalar)
  □ TC-001: [descripción breve] — Prioridad: 🔴
  □ TC-002: [descripción breve] — Prioridad: 🔴

BLOQUE 2 — HAPPY PATH (verificar flujo principal)
  □ TC-003: [descripción breve] — Prioridad: 🔴
  □ TC-004: [descripción breve] — Prioridad: 🔴

BLOQUE 3 — EDGE CASES (verificar bordes)
  □ TC-005: [descripción breve] — Prioridad: 🟠
  □ TC-006: [descripción breve] — Prioridad: 🟠

BLOQUE 4 — NEGATIVOS (verificar que NO se pueda romper)
  □ TC-007: [descripción breve] — Prioridad: 🟡
  □ TC-008: [descripción breve] — Prioridad: 🟡

BLOQUE 5 — REGRESIÓN (verificar que no rompimos nada)
  □ REG-001: [descripción breve] — Prioridad: 🟠
  □ REG-002: [descripción breve] — Prioridad: 🟡

BLOQUE 6 — DB EVIDENCE (queries de verificación)
  □ DB-001: [query breve] — Verificar: [qué]
  □ DB-002: [query breve] — Verificar: [qué]
```

#### Paso 3: Definir datos necesarios

| Dato | Cómo obtenerlo | Notas |
|------|---------------|-------|
| Usuario de prueba | ... | Company: ... |
| Flow de prueba | ... | Debe tener nodos de tipo... |
| Connector de prueba | ... | Global / Company |

#### Paso 4: Definir criterios de aprobación/rechazo

```
CRITERIOS DE APROBACIÓN
  ✅ TODOS los smoke tests pasan
  ✅ TODOS los happy path pasan
  ✅ Al menos 80% de los edge cases pasan
  ✅ TODOS los negativos pasan (no se puede romper el sistema)
  ✅ TODOS los casos de regresión pasan
  ✅ DB evidence confirma integridad de datos

CRITERIOS DE RECHAZO
  ❌ Algún smoke test falla → rechazo inmediato
  ❌ Happy path falla → rechazo
  ❌ Caso negativo falla (el sistema se puede romper) → rechazo
  ❌ Caso de regresión falla → rechazo con análisis de impacto
  ❌ DB evidence muestra datos corruptos → rechazo

CRITERIOS DE APROBACIÓN CON OBSERVACIONES
  ⚠️ Edge case falla pero no es bloqueante → aprobar con bug registrado
  ⚠️ Problema visual menor → aprobar con observación
```

#### Paso 5: Estimar tiempo

| Bloque | Casos | Tiempo estimado |
|--------|-------|-----------------|
| Smoke tests | [N] | ~[X] min |
| Happy path | [N] | ~[X] min |
| Edge cases | [N] | ~[X] min |
| Negativos | [N] | ~[X] min |
| Regresión | [N] | ~[X] min |
| DB evidence | [N] | ~[X] min |
| **Total** | **[N]** | **~[X] min** |

### Stage 3 — REPORTING

Guarda el output en `L3-tickets/<ticket-id>/test-plan.md`:

```markdown
# Test Plan — [TICKET-ID]

## Información del Ticket
- ID: [ticket-id]
- Título: [título]
- Módulo: [módulo]
- QA Engineer: [nombre]
- Fecha del plan: [fecha]

## Resumen
- Total de casos: [N]
- Tiempo estimado: ~[X] min
- Artefactos de Discovery usados: [lista]

## Orden de Ejecución
[Paso 2 completo]

## Datos Necesarios
[Paso 3]

## Criterios de Aprobación/Rechazo
[Paso 4]

## Estimación de Tiempo
[Paso 5]

## Estado
⏳ Plan creado — esperando inicio de ejecución
```

---

## Reglas de este Skill

1. **Si no hay test-matrix**: No generes el plan de memoria — ejecuta `test-docs/document` primero
2. **El orden importa**: Smoke tests siempre van primero. Si un smoke falla, no se sigue
3. **Los criterios de aprobación/rechazo deben ser explícitos** antes de empezar a testear
4. **El QA Engineer puede modificar el plan** en cualquier momento — el plan es una guía, no una ley
5. **Estimar tiempo es orientativo** — ayuda al QA Engineer a planificar su día
