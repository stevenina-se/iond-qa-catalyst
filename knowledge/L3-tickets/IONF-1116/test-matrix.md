# Test Matrix — IONF-1116

> Bug Fix: PDF Templates — Sin límite de tamaño para Load Base PDF, crashea con archivos grandes

| TC | Categoría | Descripción | Pre-condición | Pasos | Resultado Esperado | Prioridad | Estado |
|-----|-----------|-------------|---------------|-------|--------------------|-----------|--------|
| TC-01 | Smoke | Rechazar archivo no-PDF (ej. .png, .txt) | Editor PDF Template abierto | 1. PDF Templates > Abrir/Crear template 2. Click "Load Base PDF" 3. Seleccionar archivo .png o .txt | Toast error: "Please select a valid PDF file" — archivo rechazado | 🔴 | Passed |
| TC-02 | Happy Path | Rechazar PDF mayor a 10MB | Editor PDF Template abierto | 1. Click "Load Base PDF" 2. Seleccionar PDF > 10MB | Toast error con tamaño actual y límite 10MB — archivo rechazado, sin crash | 🔴 | Passed |
| TC-03 | Happy Path | Aceptar PDF válido menor a 10MB | Editor PDF Template abierto | 1. Click "Load Base PDF" 2. Seleccionar PDF válido < 10MB | PDF carga normalmente en el Designer sin errores | 🟠 | Passed |
| TC-04 | Edge | Archivo .pdf renombrado (no es PDF real) | Editor PDF Template abierto | 1. Renombrar un .txt a .pdf 2. Click "Load Base PDF" 3. Seleccionar el .pdf falso | Archivo aceptado por validación (extensión .pdf) pero Designer puede mostrar warning — sin crash | 🟠 | Passed |
| TC-05 | Edge | PDF exactamente 10MB (boundary) | Editor PDF Template abierto | 1. Click "Load Base PDF" 2. Seleccionar PDF de exactamente 10MB | PDF carga normalmente (límite es > 10MB, no >=) | 🟡 | Passed |
| TC-06 | Edge | Verificar toast en español | Idioma en español | 1. Cambiar idioma a español 2. Intentar cargar archivo no-PDF | Toast en español: "Por favor seleccione un archivo PDF válido" | 🟡 | Passed |
| TC-07 | Regresión | Cargar PDF válido tras error | Post-error de validación | 1. Intentar cargar .png → error 2. Intentar cargar PDF válido < 10MB | PDF válido carga correctamente después del error previo | 🟠 | Passed |
