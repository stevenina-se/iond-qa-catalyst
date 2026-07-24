# Test Matrix — IONF-1121

> Bug Fix: Board sugiere cambios sin guardar tras commit exitoso

| TC | Categoría | Descripción | Pre-condición | Pasos | Resultado Esperado | Prioridad | Estado |
|-----|-----------|-------------|---------------|-------|--------------------|-----------|--------|
| TC-01 | Smoke | Fix del bug: No alerta tras commit exitoso | Board existente con nodos | 1. Abrir board en canvas 2. Agregar nodo 3. Commit 4. Navegar a otra sección 5. Volver a Boards 6. Re-abrir el board | NO debe mostrar alerta de cambios sin guardar | 🔴 | Passed |
| TC-02 | Happy Path | Cambios reales SÍ muestran alerta | Board con commit previo | 1. Abrir board 2. Agregar/mover un nodo 3. Sin hacer commit 4. Intentar salir | Debe mostrar alerta de cambios sin guardar | 🔴 | Passed |
| TC-03 | Happy Path | Commit exitoso - flujo normal | Board vacío o existente | 1. Abrir board 2. Realizar cambios 3. Commit 4. Verificar toast de éxito 5. Verificar que no hay indicador de cambios pendientes | Toast de éxito, no indicador de pendientes | 🟠 | Passed |
| TC-04 | Edge | Múltiples commits seguidos | Board con cambios | 1. Abrir board 2. Cambio + Commit 3. Otro cambio + Commit 4. Salir y volver | Sin alerta falsa después de múltiples commits | 🟠 | Passed |
| TC-05 | Edge | Refresh de página después de commit | Board con commit reciente | 1. Abrir board 2. Hacer cambios 3. Commit exitoso 4. F5 (refresh) | Sin alerta de cambios sin guardar | 🟡 | Passed |
| TC-06 | Edge | Navegación rápida salir/entrar | Board con commit reciente | 1. Commit exitoso 2. Salir rápido 3. Volver inmediatamente | Sin alerta falsa (sin ventana de tiempo) | 🟡 | Passed |
| TC-07 | Regresión | Crear nuevo board desde cero | N/A | 1. Ir a Boards 2. Crear nuevo Board 3. Agregar nodos 4. Primer commit 5. Salir y volver | Board creado OK, sin alerta falsa | 🟠 | Passed |
| TC-CR-001 | Code Review | Carga inicial NO dispara auto-save (ignoreNextChange) | Board con nodos y commit previo | 1. Abrir DevTools Network tab 2. Abrir un board existente con commit 3. Esperar 15 segundos sin hacer nada 4. Verificar que NO hubo request a /flows/{id} con método PUT | No debe haber request PUT a updateFlow durante la carga | 🟠 | Passed |
| TC-CR-002 | Code Review | Auto-save silencioso al navegar (onlyEmitEvent) | Board con commit previo + cambios pendientes | 1. Abrir board con commit previo 2. Mover un nodo 3. Abrir DevTools Network tab 4. Click en Dashboard (sidebar) 5. Verificar que se ejecuta auto-save (request PUT a updateFlow) | El auto-save se ejecuta exitosamente → request 200 en network tab | 🟠 | Passed |
