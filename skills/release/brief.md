# Skill: release/brief

> Genera el `regression-brief.md` automáticamente, consolidando toda la información
> del release en un documento ejecutivo para testers que van a ejecutar la regresión.

---

## Cuándo usar este skill

**Frase disparadora:**
```
Generar brief de regresión: v[X.Y.Z]
```

**Pre-condición**: Las matrices de regresión y/o smoke deben haberse generado.

---

## Pre-requisitos

- ✅ `knowledge/releases/<version>/tracking-list.md` (del ingest o plan)
- ✅ `knowledge/releases/<version>/regression-matrix.md` + `.csv` (de regression-matrix)
- ✅ `knowledge/releases/<version>/smoke-matrix.md` (opcional, de smoke-matrix)
- ✅ `knowledge/releases/<version>/ticket-synthesis.md` (del ingest, para contexto)
- ✅ `knowledge/L1-project/test-priorities.md` — Para flujos críticos

---

## Stage 1 — PLANNING

### Paso 1.1 — Verificar artefactos disponibles

| Artefacto | ¿Existe? | Acción si no existe |
|-----------|----------|---------------------|
| `tracking-list.md` | ✅/❌ | **PARAR** → Ejecutar `release/ingest` o `release/plan` |
| `regression-matrix.md` + `.csv` | ✅/❌ | **PARAR** → Ejecutar `release/regression-matrix` |
| `smoke-matrix.md` | ✅/❌ | Continuar sin smoke (solo regresión) |
| `ticket-synthesis.md` | ✅/❌ | Continuar, pero resumen será menos detallado |

### Paso 1.2 — Anunciar el plan

```
📋 REGRESSION BRIEF — PLAN

Versión: v[X.Y.Z]
Regression matrix: [N] TCs
Smoke matrix: [N] TCs (o "no disponible")
Tickets del release: [N]

Plan:
  1. Sintetizar descripción general del release
  2. Documentar entorno de prueba
  3. Resumir matrices (distribución por módulo, prioridad)
  4. Generar instrucciones para testers
  5. Mapear tickets a filas de la matriz
  6. Definir criterios Go/No-Go

¿Procedo?
```

---

## Stage 2 — EXECUTION

### Paso 2.1 — Generar el regression brief

Usando template `templates/release-brief.md`:

**Contenido auto-generado:**

1. **Descripción General del Release**
   - Sintetizada desde `ticket-synthesis.md`
   - Párrafo ejecutivo: qué cambia en esta versión, por qué, cuál es el impacto
   - Distribución: N features, N bugs, N mejoras
   - Distribución scope: N core, N ux-ui

2. **Entorno de Prueba**
   - URL staging: `dev-app.ionflow.io` (leer de `.env` si disponible)
   - Branch: `DEVELOPMENT`
   - Tipo de prueba: Regresión + Smoke
   - Credenciales: Company user + Admin (sin valores reales)

3. **Resumen de la Regression Matrix**
   - Total de TCs
   - Distribución por Side (KC, ADMIN, TENANT, ADMIN GATEWAY)
   - Distribución por módulo
   - TCs con prioridad 🔴 vs 🟠 vs 🟡
   - TCs con riesgo DIRECTA vs INDIRECTA vs BASELINE
   - Items SKIPPED (si hay)

4. **Resumen del Smoke Matrix** (si existe)
   - Total de TCs
   - Flujos críticos cubiertos: [N]/9
   - Tiempo estimado

5. **Instrucciones para Testers**
   - Cómo reportar resultados:
     - ✅ PASSED — Funciona como se espera
     - ❌ FAILED — No funciona, reportar bug con evidencia
     - ⏭️ SKIPPED — No se puede probar (indicar razón)
     - ⚠️ BLOCKED — Dependencia bloqueante
   - Formato de reporte de bug
   - Dónde registrar resultados (directamente en la matriz CSV)

6. **Mapping de Tickets del Release a Filas de la Matriz**
   - Tabla: IONF-XXX → fila(s) de la matriz donde se prueba
   - Permite trazar qué filas cubren qué ticket

7. **Criterios de Calidad y Go/No-Go**
   - 🟢 GO: Todos los TCs de prioridad 🔴 PASSED + ≤5% FAILED en total
   - 🟡 CONDITIONAL GO: 1-2 FAILED en prioridad 🟠, con workaround documentado
   - 🔴 NO-GO: Cualquier FAILED en prioridad 🔴 sin workaround

---

## Stage 3 — REPORTING

### Paso 3.1 — Presentar el brief

```
📋 REGRESSION BRIEF v[X.Y.Z] — DRAFT

Descripción: [1-2 oraciones del release]
Regression: [N] TCs | Smoke: [N] TCs
Criterios Go/No-Go definidos

¿Apruebas el brief o deseas ajustar algo?
```

### Paso 3.2 — Guardar artefacto

`regression-brief.md` → `knowledge/releases/<version>/`

---

## Reglas de este Skill

1. **El brief es un documento ejecutivo** — No repetir detalles de la matriz, resumir
2. **Siempre incluir criterios Go/No-Go** — El tester debe saber cuándo parar
3. **Mapping de tickets obligatorio** — Cada ticket del release debe tener al menos 1 fila en la matriz
4. **NUNCA modificar skills, templates o artefactos existentes**
5. **Artefactos por versión** — Output en `knowledge/releases/<version>/`

---

## Checklist de cierre

- □ Artefactos de input verificados
- □ Descripción general del release sintetizada
- □ Entorno de prueba documentado
- □ Resumen de regression matrix incluido
- □ Resumen de smoke matrix incluido (si existe)
- □ Instrucciones para testers documentadas
- □ Mapping tickets → filas de la matriz
- □ Criterios Go/No-Go definidos
- □ Brief aprobado por el Scrum Master
- □ Artefacto guardado
