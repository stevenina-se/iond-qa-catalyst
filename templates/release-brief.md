# Regression Brief — [VERSIÓN]

> Template generado por `skills/release/brief`
> Fecha: [fecha]
> Versión: v[X.Y.Z]
> Entorno: [URL]

---

## Descripción General del Release

<!--
Sintetizar desde ticket-synthesis.md:
- Qué cambia, por qué, cuál es el impacto
- Distribución: N features, N bugs, N mejoras
- Distribución scope: N core, N ux-ui
-->

[Descripción]

**Estadísticas:** [N] features · [N] bugs · [N] mejoras · [N] internos
**Scope:** [N] core · [N] UX/UI

---

## Entorno de Prueba

| Campo | Valor |
|-------|-------|
| URL Staging | [URL] |
| Branch | `DEVELOPMENT` |
| Tipo de prueba | Regresión + Smoke |
| Credenciales | Company User / Admin Ionflow |

---

## Resumen de la Regression Matrix

| Métrica | Valor |
|---------|-------|
| Total de TCs | [N] |
| Regresión Directa | [N] |
| Regresión Indirecta | [N] |
| Baseline | [N] |
| Prioridad 🔴 | [N] |
| Prioridad 🟠 | [N] |
| Prioridad 🟡 | [N] |

### Distribución por Módulo

| Módulo | TCs | Prioridad máxima |
|--------|-----|-----------------|
| [módulo] | [N] | 🔴/🟠/🟡 |

---

## Resumen del Smoke Matrix

<!--
Solo si existe smoke-matrix.md. Si no, omitir esta sección.
-->

| Métrica | Valor |
|---------|-------|
| Total de TCs | [N] |
| Flujos críticos cubiertos | [N]/9 |
| Tiempo estimado | ~[N] min |

---

## Instrucciones para Testers

### Cómo reportar resultados

| Estado | Significado | Acción |
|--------|-------------|--------|
| ✅ PASSED | Funciona como se espera | Marcar en la matriz |
| ❌ FAILED | No funciona | Reportar bug con evidencia (screenshot + pasos) |
| ⏭️ SKIPPED | No se puede probar | Indicar razón en observaciones |
| ⚠️ BLOCKED | Dependencia bloqueante | Indicar qué bloquea |

### Formato de reporte de bug

```
**TC-ID**: [ID del caso]
**Resultado**: ❌ FAILED
**Pasos realizados**: [breadcrumb del TC]
**Resultado obtenido**: [qué pasó]
**Resultado esperado**: [qué debería pasar]
**Evidencia**: [screenshot/video]
**Entorno**: [URL + browser]
```

### Dónde registrar resultados

- Directamente en `regression-matrix.csv` — columna "Estado"
- Si es bug → crear ticket en ClickUp con tag `qa-regression-v[X.Y.Z]`

---

## Mapping de Tickets a Filas de la Matriz

<!--
Tabla que permite trazar qué filas de la matriz cubren qué ticket.
-->

| Ticket | Descripción | Fila(s) de la Matriz |
|--------|-------------|---------------------|
| IONF-XXX | [descripción] | [IDs de TCs] |

---

## Criterios de Calidad — Go/No-Go

| Resultado | Condición | Decisión |
|-----------|----------|----------|
| 🟢 GO | Todos los TCs 🔴 PASSED + ≤5% FAILED en total | Proceder con deploy |
| 🟡 CONDITIONAL GO | 1-2 FAILED en 🟠, con workaround documentado | Proceder con precaución |
| 🔴 NO-GO | Cualquier FAILED en 🔴 sin workaround | **PARAR** — Resolver antes de deploy |

---

## Notas

<!--
Decisiones, excepciones, riesgos aceptados.
-->

[Notas o dejar vacío]
