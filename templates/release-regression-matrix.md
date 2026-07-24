# Regression Matrix — [VERSIÓN]

> Template generado por `skills/release/regression-matrix`
> Fecha: [fecha]
> Versión: [versión]

## Resumen

| Métrica | Valor |
|---------|-------|
| Total de casos | |
| Regresión directa | |
| Regresión indirecta | |
| Baseline | |
| Módulos cubiertos | |
| Módulos afectados por release | |

---

## Cobertura por Módulo

| Módulo | Criticidad (L1) | Directos | Indirectos | Baseline | Total |
|--------|-----------------|---------|-----------|---------|-------|
| | | | | | |

---

## Regression Matrix

| ID | Side | Módulo | Tipo Regresión | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Estado |
|----|------|--------|---------------|-------------|--------------|-------|-------------------|-----------|--------|
| REG-001 | | | `[DIRECTA]` | | | | | 🔴 | ⬜ Pendiente |
| REG-002 | | | `[INDIRECTA]` | | | | | 🟠 | ⬜ Pendiente |
| REG-003 | | | `[BASELINE]` | | | | | 🟡 | ⬜ Pendiente |

### Formato de Pasos (OBLIGATORIO)

> Los pasos DEBEN usar formato **breadcrumb** explícito.
> Formato: `[Rol] Login > Sidebar: [Módulo] > [Acción] > [Sub-acción] > [Verificación]`

### Leyenda de Tipo de Regresión
- `[DIRECTA]` — Módulo cambiado directamente por un ticket del release
- `[INDIRECTA]` — Módulo posiblemente impactado por cross-impact (sección "Impacto Cruzado" del L2)
- `[BASELINE]` — Control de que el core del producto no se rompió (módulo 🔴/🟠 del L1, no tocado directamente)

### Leyenda de Prioridad
- 🔴 Crítico — Testear siempre, bloqueante si falla
- 🟠 Alto — Testear siempre, puede ser bloqueante
- 🟡 Medio — Testear si hay tiempo
- 🟢 Bajo — Nice to have

### Leyenda de Estado
- ⬜ Pendiente
- ✅ Pasó
- ❌ Falló
- ⏭️ Saltado (con justificación)

---

## Tickets del Release vs. Módulos Impactados

<!--
Mapeo de cada ticket del release a los módulos que podría afectar.
Fuente: tracking-list.md + sección "Impacto Cruzado" de cada L2.
-->

| Ticket | Descripción | Módulo directo | Módulos cross-impact |
|--------|-------------|---------------|---------------------|
| | | | |

---

## Observaciones

<!--
Notas sobre features marcadas como "Skipped" en el CSV guía,
módulos en desarrollo activo, o áreas que requieren atención especial.
Actualizar si el release invalida observaciones anteriores.
-->

[Observaciones o dejar vacío]

---

## Notas

- CSV de regresión base usado como guía: `Test Plan - IONFLOW - Smoke Test.csv`
- Fuentes de schema: `../gateway/database/migrations/*.php` y `../flow_binaries/migrations/*.sql`
- Queries ejecutadas en DBeaver (PostgreSQL via SSH tunnel)
