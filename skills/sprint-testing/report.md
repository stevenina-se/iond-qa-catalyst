# Skill: sprint-testing/report

> Genera el reporte final de QA para un ticket testeado. Consolida los resultados de la ejecución, los bugs encontrados y emite la sugerencia de veredicto para el QA Engineer.

## Cuándo usar este skill

- **Deployment Track**: Después de completar la ejecución del testing (`sprint-testing/test`)
- **Support Lane**: Después de testear un hotfix

## Pre-requisitos

Antes de ejecutar este skill, el agente DEBE haber cargado:
- ✅ `L3-tickets/<ticket-id>/test-matrix.md` (con resultados de ejecución)
- ✅ `L3-tickets/<ticket-id>/test-plan.md` (criterios de aprobación/rechazo)
- ✅ `L3-tickets/<ticket-id>/code-review-qa.md` (bugs del code review, si existe)
- ✅ `L3-tickets/<ticket-id>/db-evidence.md` (si existe)
- ✅ `L3-tickets/<ticket-id>/screenshots/` (evidencia visual, si existe)
- ✅ Resultados de la sesión de testing ejecutada

---

## Instrucciones de Ejecución

### Stage 1 — PLANNING

Reporta al QA Engineer:
1. El ticket que vas a reportar
2. Los artefactos de la sesión que vas a consolidar
3. Los bugs encontrados (resumen rápido)

**Espera aprobación antes de generar el reporte.**

### Stage 2 — EXECUTION

#### Paso 1: Consolidar resultados

Lee los resultados de la sesión de testing y compila:

| Métrica | Valor |
|---------|-------|
| Total de casos ejecutados | |
| Total de casos aprobados | |
| Total de casos fallidos | |
| Total de casos parciales | |
| Total de casos saltados | |
| Tasa de aprobación | % |
| Bugs encontrados en testing | |
| Bugs encontrados en code review | |
| Bugs totales | |
| Bugs bloqueantes (🔴) | |
| Bugs no bloqueantes | |
| TCs del code review ejecutados (TC-CR-xxx) | |
| Screenshots de fallos capturados | |
| Tiempo total de testing | |

#### Paso 2: Evaluar contra criterios

Usando los criterios definidos en `test-plan.md`:

| Criterio | Requerido | Resultado | Cumple |
|----------|-----------|-----------|--------|
| Smoke tests pasan | 100% | [N/N] | ✅/❌ |
| Happy path pasan | 100% | [N/N] | ✅/❌ |
| Edge cases pasan | ≥80% | [N/N] ([%]) | ✅/❌ |
| Negativos pasan | 100% | [N/N] | ✅/❌ |
| Regresión pasan | 100% | [N/N] | ✅/❌ |
| DB evidence conforme | 100% | [N/N] | ✅/❌ |
| Bugs 🔴 abiertos | 0 | [N] | ✅/❌ |

#### Paso 3: Generar la sugerencia de veredicto

Basado en la evaluación de criterios:

**Si TODOS los criterios se cumplen:**
```
SUGERENCIA: ✅ APPROVED
Todos los criterios de aprobación se cumplen.
No hay bugs bloqueantes abiertos.
```

**Si algún criterio NO se cumple pero no hay bugs 🔴:**
```
SUGERENCIA: ⚠️ APPROVED CON OBSERVACIONES
Se cumplen los criterios principales pero se encontraron [N] observaciones.
Los bugs encontrados no son bloqueantes.
Observaciones:
- [lista]
```

**Si hay bugs 🔴 o criterios principales fallan:**
```
SUGERENCIA: ❌ REJECTED
Se encontraron [N] bugs bloqueantes.
Los siguientes criterios NO se cumplen:
- [lista de criterios que fallan]
```

> ⚠️ **ESTA ES SOLO UNA SUGERENCIA. EL QA ENGINEER TOMA LA DECISIÓN FINAL.**

#### Paso 4: Compilar lista de bugs (Code Review + Testing)

> ⚠️ El reporte DEBE consolidar bugs de **AMBAS fuentes**:
> bugs del code review (BUG-CR-xxx) + bugs del testing (BUG-xxx).

**Bugs del Code Review** (de `code-review-qa.md`):

| Bug ID | Severidad | Tipo | Repo | Descripción | Verificado en Testing | TC Relacionado |
|--------|-----------|------|------|-------------|----------------------|----------------|
| BUG-CR-001 | 🔴 | BUG CONFIRMADO | [repo] | [desc] | ✅ Verificado / ❌ No verificado | TC-CR-001 |
| BUG-CR-002 | 🟠 | RIESGO | [repo] | [desc] | ✅ Verificado: [resultado] | TC-CR-002 |

**Bugs del Testing** (de la sesión de testing):

| Bug ID | Severidad | Estado | Módulo | Descripción | TC | Evidencia |
|--------|-----------|--------|--------|-------------|-----|-----------|
| BUG-001 | 🔴 Urgent | Nuevo | [mod] | [desc] | TC-XXX | [screenshot/link] |
| BUG-002 | 🟡 High | Nuevo | [mod] | [desc] | TC-YYY | [screenshot/link] |

**Resumen consolidado:**
- Total bugs del code review: [N] (confirmados: [N], riesgos verificados: [N])
- Total bugs del testing: [N]
- Total bugs combinados: [N] (🔴: [N], 🟠: [N], 🟡: [N])

#### Paso 5: Generar comentario para el ticket

Según el veredicto del QA Engineer, prepara el comentario usando el template correspondiente:

- **Si ✅ Approved** → Usar `templates/approval.md`
  - Incluir sección "Code Review QA" con resumen de hallazgos
  - Referenciar screenshots de evidencia si Playwright MCP fue usado
- **Si ❌ Rejected** → Usar `templates/rejection.md`
  - Incluir bugs del code review Y del testing
  - Pasos de reproducción en formato breadcrumb
  - Screenshots de fallos como evidencia: `L3-tickets/<id>/screenshots/FAIL-TC-xxx.png`
- **Si ⚠️ Approved con obs** → Usar `templates/approval.md` con sección de observaciones

> Los screenshots de fallos capturados durante Playwright MCP son evidencia permanente
> y deben referenciarse en el comentario del ticket.

El QA Engineer revisa y publica el comentario manualmente.

### Stage 3 — REPORTING

Genera el reporte final usando `templates/qa-report.md` y guárdalo en `L3-tickets/<ticket-id>/qa-report.md`.

También actualiza:
- `L3-tickets/<ticket-id>/test-matrix.md` → Estados finales de cada TC
- `L3-tickets/<ticket-id>/test-matrix.csv` → Actualizar columna Estado
- `templates/ticket-memory.md` → Veredicto final, fecha, observaciones

---

## Flujo de Aprobación

```
Catalyst genera sugerencia
         │
         ▼
QA Engineer revisa el reporte
         │
    ┌────┴────┐
    ▼         ▼
APRUEBA    RECHAZA
    │         │
    ▼         ▼
Usa         Usa
approval.md rejection.md
    │         │
    ▼         ▼
QA publica  QA publica
comentario  comentario
    │         │
    ▼         ▼
Actualizar  Crear nueva iteración
L3 con      de test-matrix para
veredicto   el re-test
final       (ver abajo)
```

---

## Flujo de Rechazo e Iteración

Cuando un ticket es **rechazado**, el Catalyst prepara la siguiente iteración de testing:

```
RECHAZO → ITERACIÓN

① El QA Engineer confirma el veredicto: ❌ Rejected
② Catalyst actualiza la test-matrix actual con los resultados (Iteración N)
③ Catalyst crea una NUEVA iteración de la test-matrix (Iteración N+1):
   → Mantiene los bugs abiertos como re-test obligatorio
   → Marca los casos que pasaron como "regresión" (verificar que siguen OK)
   → Agrega nuevos casos si el Developer reporta cambios en la corrección
④ El ticket vuelve al Developer
⑤ Cuando el Developer corrige → se re-ejecuta sprint-testing/test con la Iteración N+1
```

### Archivos generados por iteración

```
L3-tickets/<ticket-id>/
├── test-matrix.md          ← Iteración actual (siempre la más reciente)
├── test-matrix.csv         ← CSV de la iteración actual
├── test-matrix-v1.md       ← Archivo de la primera iteración (historial)
├── test-matrix-v1.csv      ← CSV de la primera iteración
├── qa-report.md            ← Reporte actual
├── qa-report-v1.md         ← Reporte de la primera iteración
└── ...
```

### Contenido de la nueva iteración (test-matrix Iteración N+1)

| ID | Origen | Tipo | Caso de Test | Estado anterior | Estado nuevo | Prioridad |
|----|--------|------|-------------|-----------------|-------------|-----------|
| BUG-001-RETEST | Bug de Iter. N | **Re-test** | Verificar corrección de BUG-001 | ❌ Fail | ⬜ Pendiente | 🔴 |
| TC-001 | Iter. N | Regresión post-fix | [caso que pasó — verificar que sigue OK] | ✅ Pass | ⬜ Pendiente | 🟠 |
| TC-NEW | Nuevo | Nuevo caso | [si el Developer cambió algo adicional] | N/A | ⬜ Pendiente | 🟠 |

### Reglas de iteración

1. **Los bugs abiertos son re-test obligatorio** con prioridad 🔴
2. **Los casos que pasaron se re-verifican** como regresión post-fix (el fix pudo romperlos)
3. **Si el Developer reporta cambios adicionales** → agregar nuevos TC
4. **El historial se preserva** — nunca se sobreescribe una iteración anterior
5. **El CSV se regenera** para cada nueva iteración

---

## Reglas de este Skill

1. **El Catalyst SUGIERE, el QA Engineer DECIDE** — El veredicto final siempre es humano
2. **Consolidar bugs de AMBAS fuentes** — Code review (BUG-CR-xxx) + testing (BUG-xxx)
3. **Todos los bugs deben estar documentados** antes de generar el reporte
4. **El comentario en ClickUp lo publica el QA Engineer** — Nunca automáticamente
5. **Si el QA Engineer cambia el veredicto sugerido** — Documentar la razón en el reporte
6. **Usar los templates del equipo** — `approval.md` y `rejection.md` (actualizados con sección Code Review)
7. **Actualizar el CSV** — La versión CSV de la test matrix debe reflejar el resultado final
8. **En rechazo: crear nueva iteración** — Preservar historial y preparar para re-test
9. **Branch de entorno**: `DEVELOPMENT` (batch) — registrar branch del ticket para trazabilidad
10. **Screenshots de fallos son evidencia permanente** — Referenciar en el reporte y comentario del ticket
11. **Bugs del code review se verifican en testing** — Marcar si fueron confirmados o descartados
