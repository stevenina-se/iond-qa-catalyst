# Code Review QA — IONF-1121 (86e22fzrp)

> **Bug Fix**: Board sugiere cambios sin guardar tras commit exitoso al re-ingresar a la vista
> Repo: `gateway-ion` (GitHub: `altacrest/ion_gateway_ion`)
> Branch: `IONF-1121` | PR: #9 (mergeado en `7399495c`)
> Assignee: Gustavo Mamani | Reviewer QA: Steve Nina | Fecha: 2026-07-09

---

## Commits del Fix

| Commit | Mensaje | Archivos |
|--------|---------|----------|
| `06ce0b5a` | IONF-1121 (fix) fix false change alert | `FlowEditor.vue` (+7/-6), `FlowEditor.spec.ts` (+114/-2) |
| `c336f844` | IONF-1121 (fix) flag to prevent autosave in first load | `FlowEditor.vue` (+19/-3) |

> ⚠️ El PR #9 también incluye cambios no relacionados con el bug (limpieza de PdfTemplateDialog, AppCreate, Ionmind). Esto es una práctica cuestionable — los PRs deberían ser atómicos por ticket.

---

## Causa Raíz (Root Cause)

El bug era un **falso positivo del dirty state** causado por la carga del canvas:

```
showFlow() → setFlow(res.data.data) → VueFlow dispara evento onChange
                                             ↓
                                      onChange() se ejecuta
                                      changed = true ← INCORRECTO
                                      debouncedFn() programa autoSave en 10s
                                             ↓
                                      autoSaveFlow() → updateFlow()
                                      API graba el estado → is_dirty = true en backend
                                             ↓
                                      Al re-entrar al board:
                                      showFlow() → changedFromHead = res.data.is_dirty = TRUE
                                      → UnsavedChangesGuard activo → ALERTA FALSA
```

**En resumen**: `setFlow()` disparaba `onChange()` durante la carga inicial, lo cual ponía `changed = true` y activaba el auto-save, que marcaba el board como dirty en el backend sin que el usuario hubiera hecho cambios reales.

---

## Análisis del Fix

### Commit 1: Early return en `onChange()` (06ce0b5a)

```diff
 function onChange() {
-  changed.value = true;
   const result = isWorkflowChanged(getFlow(), flowHeadData.value);
+
+  if (!result && !changedFromHead.value) {
+    return;
+  }
+
+  changed.value = true;
   changedFromHead.value = result;
   debouncedFn();
 }
```

**Qué hace**: Si `isWorkflowChanged` retorna `false` Y `changedFromHead` ya es `false`, no marca como changed ni programa auto-save.

**Evaluación**: ✅ Correcto como primera defensa — evita marcar como dirty cuando no hay cambios reales.

### Commit 2: Flag `ignoreNextChange` (c336f844) — FIX PRINCIPAL

```diff
+const ignoreNextChange = ref(false);

 // En showFlow() — primera carga:
+  ignoreNextChange.value = true;
   setFlow(res.data.data);

 // En onChange():
+  if (ignoreNextChange.value) {
+    ignoreNextChange.value = false;
+    return;
+  }
```

**Qué hace**: Antes de llamar `setFlow()` (que dispara el evento onChange de VueFlow), activa un flag que indica que el próximo evento onChange debe ignorarse porque es una carga, no un cambio del usuario.

**Evaluación**: ✅ Solución correcta y elegante.

**Puntos de inserción del flag**: 4 lugares donde `ignoreNextChange = true`:
1. `showIntegrationFlow()` L381 — carga de flow de integración
2. `showFlow()` L425 (isFirstLoad) — primera carga del board
3. `showFlow()` L438 (else) — recarga del mismo board
4. `restoreFlowData()` L551 — restaurar al último commit

Todos son correctos — cubren todos los flujos donde `setFlow()` se llama programáticamente.

---

## Bug Hunting — Hallazgos

### BUG-CR-001 ⚠️ RIESGO A VERIFICAR — Race condition con múltiples `setFlow()` rápidos

**Ubicación**: `FlowEditor.vue` — `ignoreNextChange` es un booleano simple, no un contador.

**Escenario**: Si por alguna razón `setFlow()` se llama dos veces antes de que `onChange()` se dispare (ej: showFlow → setFlow → setFlow seguido), el flag se resetea en el primer onChange pero el segundo dispararía un cambio falso.

**Probabilidad**: Muy baja — `setFlow` se llama una sola vez por cada flujo de carga.
**Severidad**: Baja.

### BUG-CR-002 ⚠️ RIESGO A VERIFICAR — Auto-save pendiente post-commit

**Ubicación**: `FlowEditor.vue` L612-614

```typescript
const debouncedFn = useDebounceFn(() => {
  autoSaveFlow();
}, 10000);
```

**Escenario**: Si el usuario hace cambios, `debouncedFn()` programa autoSave en 10s. Si el usuario hace commit antes de los 10s:
1. Commit exitoso → `changedFromHead = false`, `changed = false`
2. Pero `autoSaveFlow()` se ejecuta después → verifica `changed.value` (ya es `false`) → early return en L582

**Evaluación**: ✅ **SIN RIESGO** — el check `if (!changed.value) return;` en L582 protege contra este caso. El auto-save no se ejecutará si ya se hizo commit.

### BUG-CR-003 ⚠️ RIESGO A VERIFICAR — `onlyEmitEvent` sin fallback de error

**Ubicación**: `FlowEditor.vue` L1108, `UnsavedChangesGuard.vue` L34-38

Cuando el board tiene un commit previo (`current_commit` existe), el guard NO muestra diálogo — llama `autoSaveFlow(true)` directamente. Si falla el auto-save (error de red), los cambios se pierden sin aviso.

**Severidad**: Media — pero no es introducido por este PR, es comportamiento preexistente.

---

## Tests del Fix

| Test | Cobertura | Evaluación |
|------|-----------|------------|
| `FlowEditor.spec.ts` | +114 líneas — test de `onChange` con `ignoreNextChange` | ✅ Bien cubierto |
| `helpers.spec.ts` | `isWorkflowChanged` — 4 cases | ✅ Sin cambios necesarios |
| Unit test command | `pnpm test:unit` → ✅ PASSED | ✅ Confirmado por developer |

---

## TCs Inyectados en Test Matrix

| TC | Origen | Descripción | Prioridad |
|----|--------|-------------|-----------|
| TC-CR-001 | Code Review | Verificar que la carga inicial del board NO dispara auto-save (network tab: no request a updateFlow en primeros 15s) | 🟠 |
| TC-CR-002 | Code Review | Auto-save silencioso al navegar: board con commit previo + cambios → navegar fuera → verificar auto-save (request 200 en network tab) | 🟠 |

---

## Veredicto del Code Review

| Criterio | Estado |
|----------|--------|
| Fix correcto para el bug reportado | ✅ `ignoreNextChange` previene el falso positivo |
| Cobertura de todos los puntos de `setFlow()` | ✅ 4 puntos de inserción del flag |
| No introduce regresiones obvias | ✅ |
| Tests unitarios del fix | ✅ +114 líneas en `FlowEditor.spec.ts` |
| Edge cases identificados | ⚠️ 1 riesgo a verificar (auto-save sin fallback — preexistente) |
| Seguridad multi-tenant | ✅ No afecta |

**Resultado**: ✅ **APROBADO para testing** — Fix correcto con buena cobertura de tests. 2 TCs adicionales inyectados.
