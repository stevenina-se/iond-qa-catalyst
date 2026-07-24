# Test Matrix — IONF-1126

> Bug Fix: PDF Templates — Cambios sin guardar se pierden al presionar Escape o cerrar modal sin confirmación

| TC | Categoría | Descripción | Pre-condición | Pasos | Resultado Esperado | Prioridad | Estado |
|-----|-----------|-------------|---------------|-------|--------------------|-----------|--------|
| TC-01 | Smoke | Diálogo al cerrar modal con cambios (botón ×) | Template PDF abierto con cambios | 1. Company Login > PDF Templates 2. Abrir template existente 3. Modificar algún elemento 4. Click en botón × (cerrar) | Aparece diálogo: "Continuar editando" / "Descartar cambios" | 🔴 | ✅ Passed |
| TC-02 | Happy Path | Diálogo al presionar Escape con cambios | Template PDF abierto con cambios | 1. Abrir template 2. Hacer modificaciones 3. Presionar tecla Escape | Aparece diálogo de confirmación, NO se cierra directamente | 🔴 | ✅ Passed |
| TC-03 | Happy Path | Diálogo al presionar "New Template" con cambios | Template en edición con cambios | 1. Estar editando un template con cambios pendientes 2. Click en "New Template" | Aparece diálogo de confirmación antes de resetear | 🔴 | ✅ Passed |
| TC-04 | Happy Path | Cerrar sin cambios — cierre inmediato | Template abierto SIN cambios | 1. Abrir template existente 2. Sin hacer cambios, click × o Escape | Modal se cierra inmediatamente sin diálogo | 🟠 | ✅ Passed |
| TC-05 | Happy Path | "Continuar editando" mantiene cambios | Template con cambios + diálogo visible | 1. Hacer cambios 2. Click × → aparece diálogo 3. Click "Continuar editando" | Diálogo se cierra, cambios se mantienen, sigue editando | 🟠 | ✅ Passed |
| TC-06 | Happy Path | "Descartar cambios" cierra y pierde cambios | Template con cambios + diálogo visible | 1. Hacer cambios 2. Click × → aparece diálogo 3. Click "Descartar cambios" | Modal se cierra, cambios se pierden (comportamiento esperado) | 🟠 | ✅ Passed |
| TC-07 | Edge | Escape con diálogo PrimeVue activo — Drawer NO se cierra | Drawer abierto + diálogo de confirmación visible | 1. Estar en el canvas con Drawer abierto 2. Tener diálogo de PrimeVue activo (ej: confirmación) 3. Presionar Escape | El Drawer NO se cierra; solo el diálogo se cierra | 🟠 | ✅ Passed |
| TC-08 | Edge | Escape sin diálogo activo — Drawer se cierra | Drawer abierto, sin diálogos | 1. Estar en el canvas con Drawer abierto 2. Sin ningún diálogo activo 3. Presionar Escape | Drawer se cierra normalmente | 🟡 | ✅ Passed |
| TC-09 | Edge | Guardar y luego cerrar — sin diálogo | Template editado y guardado | 1. Hacer cambios 2. Click "Save" → guardar exitoso 3. Click × para cerrar | Modal se cierra inmediatamente sin diálogo (isDirty reseteado por save) | 🟡 | ✅ Passed |
| TC-10 | Regresión | Importar JSON y cerrar — sin diálogo | Template con JSON importado | 1. Importar un template JSON válido 2. Sin hacer más cambios 3. Click × | Modal se cierra sin diálogo (isDirty reseteado por import) | 🟡 | ✅ Passed |
