# QA Report — [TICKET-ID]

> Reporte final de QA generado por `sprint-testing/report`
> Fecha: [fecha]
> QA Engineer: [nombre]

## Información del Ticket

| Campo | Valor |
|-------|-------|
| Ticket ID | |
| Título | |
| Módulo | |
| Branch | |
| Entorno | dev-app.ionflow.io |
| Browser | Chrome |
| QA Engineer | |
| Fecha de testing | |

---

## Resumen Ejecutivo

| Métrica | Valor |
|---------|-------|
| Total de casos ejecutados | |
| Casos aprobados | |
| Casos fallidos | |
| Casos parciales | |
| Casos saltados | |
| **Tasa de aprobación** | **%** |
| Bugs encontrados | |
| Bugs bloqueantes (🔴) | |
| Tiempo total de testing | |

---

## Evaluación contra Criterios

| Criterio | Requerido | Resultado | Cumple |
|----------|-----------|-----------|--------|
| Smoke tests | 100% | /  | ✅/❌ |
| Happy path | 100% | /  | ✅/❌ |
| Edge cases | ≥80% | / (%) | ✅/❌ |
| Negativos | 100% | /  | ✅/❌ |
| Regresión | 100% | /  | ✅/❌ |
| DB evidence | 100% | /  | ✅/❌ |
| Bugs 🔴 abiertos | 0 | | ✅/❌ |

---

## Veredicto

| Campo | Valor |
|-------|-------|
| Sugerencia del Catalyst | ✅ Approved / ⚠️ Con observaciones / ❌ Rejected |
| **Veredicto final (QA Engineer)** | **✅ Approved / ❌ Rejected** |
| Firmado por | |
| Fecha | |
| Observaciones | |

---

## Resultados por Bloque

### Smoke Tests

| ID | Caso | Resultado | Evidencia | Notas |
|----|------|-----------|-----------|-------|
| | | ✅/❌ | | |

### Happy Path

| ID | AC | Caso | Resultado | Evidencia | Notas |
|----|-----|------|-----------|-----------|-------|
| | | | ✅/❌ | | |

### Edge Cases

| ID | Escenario | Resultado | Severidad si falla | Notas |
|----|-----------|-----------|-------------------|-------|
| | | ✅/❌/⚠️ | | |

### Negativos

| ID | Intento inválido | Bloqueo esperado | Resultado | Notas |
|----|-----------------|------------------|-----------|-------|
| | | | ✅/❌ | |

### Regresión

| ID | Módulo | Caso | Resultado | Notas |
|----|--------|------|-----------|-------|
| | | | ✅/❌ | |

### DB Evidence

| ID | Query | BD | Esperado | Real | Match |
|----|-------|-----|----------|------|-------|
| | `SELECT...` | PostgreSQL/SQLite | | | ✅/❌ |

---

## Bugs Encontrados

| Bug ID | Severidad | Estado | Módulo | Descripción | TC | Evidencia |
|--------|-----------|--------|--------|-------------|-----|-----------|
| BUG-001 | 🔴/🟡/🔵/⚪ | Nuevo | | | TC-XXX | |

### Detalle de Bugs Bloqueantes

#### BUG-[ID] — [Severidad] — [Título corto]

**Módulo**: [nombre]
**TC relacionado**: TC-[ID]

**Descripción:**
[Descripción clara y corta del problema]

**Pasos de reproducción:**
1. ...
2. ...

**Resultado esperado:**
[Qué debería ocurrir]

**Comportamiento actual:**
[Qué ocurre actualmente]

**Evidencia:**
- Screenshot(s): [link]
- Logs / Payload: [si aplica]

---

## Comentario Preparado

> El siguiente comentario está listo para que el QA Engineer lo revise y publique en ClickUp.
> Template usado: `approval.md` / `rejection.md`

```
[Comentario formateado según el template correspondiente]
```

---

## Información de Entorno

| Details | |
|---------|---|
| BROWSER | Chrome |
| BRANCH | [branch] |
| ENV | dev-app.ionflow.io |
| TEST MATRIX | [link al documento] |
| MERGE REQUEST | YES/NO |
