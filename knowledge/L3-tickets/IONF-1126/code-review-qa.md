# Code Review QA — IONF-1126 (86e22fzut)

> **Bug Fix**: PDF Templates — Cambios sin guardar se pierden al presionar Escape o cerrar modal sin confirmación
> Repos: `gateway-ion` (PR #11) + `webcomponents-flow` (PR #6)
> Branch: `IONF-1126` | Assignee: Alex Chura
> Reviewer QA: Steve Nina | Fecha: 2026-07-09

---

## Commits del Fix

### gateway-ion (PR #11)
| Commit | Mensaje | Archivos |
|--------|---------|----------|
| `1e3db5ee` | IONF-1126 (Feat) Implement unsaved changes confirmation dialog | `PdfTemplateDialog.vue` (+80/-7), `PdfTemplateDialog.spec.ts` (+5) |
| `17d57dc0` | IONF-1126 (Refactor) Implement dirty state tracking | `PdfTemplateDialog.vue` (+64/-47), `PdfTemplateDialog.spec.ts` (+133/-1) |

### webcomponents-flow (PR #6)
| Commit | Mensaje | Archivos |
|--------|---------|----------|
| `445d575` | IONF-1126 (Fix) Prevent drawer from closing on escape key when PrimeVue dialog is active | `Drawer.vue` |

---

## Análisis del Fix

### Cambio 1: Dirty state reactivo en PdfTemplateDialog (gateway-ion)

**Antes**: Usaba `savedTemplateSnapshot` (JSON.stringify del template) y `checkDirty()` que comparaba snapshots en cada acción. Costoso y frágil.

**Después**: Usa `isDirty = ref(false)` + `designer.value.onChangeTemplate(() => { isDirty.value = true; })`. El designer de pdfme notifica cada cambio directamente.

```typescript
// NUEVO: Reactive dirty state
const isDirty = ref(false);

// Se registra el callback en onDialogShow():
designer.value.onChangeTemplate(() => {
  isDirty.value = true;
});
isDirty.value = false;
```

**Evaluación**: ✅ Correcto — usa el API nativo de pdfme en vez de comparación manual por snapshot.

### Cambio 2: Diálogo de confirmación reutilizable (gateway-ion)

**Antes**: `requestClose()` tenía el diálogo inline. `onNewBlankTemplate()` duplicaba el mismo diálogo.

**Después**: `confirmUnsavedChanges(onDiscard: () => void)` es reutilizable. `requestClose()` y `onNewBlankTemplate()` la llaman.

```typescript
function confirmUnsavedChanges(onDiscard: () => void) {
  confirm.require({
    header: t('message.unsavedChanges'),
    // ...
    reject: onDiscard,
  });
}

function requestClose() {
  if (!isDirty.value) { visible.value = false; return; }
  confirmUnsavedChanges(() => { visible.value = false; });
}
```

**Evaluación**: ✅ Correcto — DRY, reutilizable.

### Cambio 3: Reset de isDirty en puntos clave (gateway-ion)

| Punto | `isDirty` | Razón |
|-------|-----------|-------|
| `onDialogShow()` post-init | `false` | Template recién cargado, no hay cambios |
| `onDialogHide()` | `false` | Limpieza al cerrar |
| `onNewBlankTemplate()` doReset | `false` | Template reseteado |
| `onSave()` post-save | `false` | Cambios guardados |
| `onImportJson()` post-import | `false` | Template importado es el nuevo baseline |

**Evaluación**: ✅ Todos los puntos de reset son correctos.

### Cambio 4: Escape key en Drawer (webcomponents-flow)

**Antes**: `document.addEventListener('keydown', (e) => { if (e.key === 'Escape') open.value = false; })` — cerraba siempre, sin importar si había diálogos activos.

**Después**: 
```typescript
function onEscapeKey(e: KeyboardEvent) {
  if (e.key === 'Escape' && !document.querySelector('.p-dialog-mask')) {
    open.value = false;
  }
}
```

**Evaluación**: ✅ Usa `.p-dialog-mask` (selector de PrimeVue) para detectar si hay un diálogo activo. Si hay diálogo, Escape no cierra el Drawer.

**Bonus**: También corrige un bug preexistente donde `removeEventListener` no funcionaba porque pasaba una función anónima nueva (no la misma referencia). Ahora usa la función `onEscapeKey` como referencia.

---

## Bug Hunting — Hallazgos

### BUG-CR-001 ⚠️ RIESGO BAJO — `.p-dialog-mask` selector hardcoded

**Ubicación**: `webcomponents-flow/src/ui/Drawer/Drawer.vue`

El selector `.p-dialog-mask` es de PrimeVue. Si PrimeVue cambia el nombre de la clase en una versión futura, el check dejaría de funcionar y Escape cerraría el Drawer con diálogos activos.

**Severidad**: Muy baja — PrimeVue es estable en esto. No requiere TC.

### BUG-CR-002 ✅ SIN RIESGO — `onChangeTemplate` callback

El callback `onChangeTemplate` se registra una vez en `onDialogShow()`. No se acumulan listeners porque `designer.destroy()` se llama en `onDialogHide()`, que limpia el designer completo.

---

## Veredicto del Code Review

| Criterio | Estado |
|----------|--------|
| Fix correcto para el bug reportado | ✅ Diálogo de confirmación + Escape key |
| No introduce regresiones | ✅ |
| Tests unitarios | ✅ +138 líneas en `PdfTemplateDialog.spec.ts` |
| DRY / Reutilizable | ✅ `confirmUnsavedChanges()` centralizado |
| Seguridad | ✅ No afecta |

**Resultado**: ✅ **APROBADO para testing** — Fix limpio y bien estructurado.
