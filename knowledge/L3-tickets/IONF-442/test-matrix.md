# Test Matrix — IONF-442 (Form Data Builder observations)

## Resumen
- Total de TCs: 11
  - Happy Path: 3 (los 3 casos del ticket)
  - Edge Case: 4 (code review)
  - Regresión: 3 (context panel fix + FormBuilder general)
  - Smoke: 1
- Prioridad: P1: 3, P2: 5, P3: 3
- Origen: Ticket: 7, Code Review: 4

---

## Suite 1 — Smoke

| TC ID | Tipo | Caso de Test | Pasos | Expected | Estado |
|-------|------|-------------|-------|----------|--------|
| TC-001 | Smoke | FormBuilder renderiza correctamente al abrir configuración de nodo | 1) Login como Tenant<br>2) Ir a Workflows > List > Crear Workflow<br>3) Agregar un nodo con trigger "On execute workflow"<br>4) Verificar que el FormBuilder se renderiza sin errores | El formulario del trigger se renderiza con campos configurables visibles, sin errores en consola | ✅ |

## Suite 2 — Happy Path (Casos del ticket)

| TC ID | Tipo | Caso de Test | Pasos | Expected | Estado |
|-------|------|-------------|-------|----------|--------|
| TC-002 | HP | **Caso 1**: Toggle Advanced en array no muestra items vacíos | 1) Login como Tenant<br>2) Ir a Workflows > Data Store > Data Structure > Add<br>3) Agregar un array structure<br>4) Activar "Advanced options"<br>5) Verificar visibilidad de items | El toggle "Advanced" controla la visibilidad del array como estructura completa. No aparecen items vacíos al activar. Panel muestra "Some fields are hidden." cuando está desactivado | ✅ |
| TC-003 | HP | **Caso 2**: Cambio de tipo de array elements a nested array | 1) Login como Tenant<br>2) Ir a Workflows > Data Store > Data Structure > Add<br>3) Crear un array con elementos tipo text/number/boolean<br>4) Agregar 2-3 elements<br>5) Cambiar tipo de elements del array a "Array" (nested)<br>6) Agregar elements al nested array | Los campos se generan correctamente sin fields rotos. El array anidado renderiza su propia estructura limpia | ✅ |
| TC-004 | HP | **Caso 3**: Cambio de tipo de array elements a collection | 1) Login como Tenant<br>2) Ir a Workflows > List > Crear Workflow > Tools > On execute trigger<br>3) Agregar un array con element type text<br>4) Agregar algunos items<br>5) Cambiar tipo de elements del array a "Collection"<br>6) Agregar items | Los elements se generan correctamente como collection. Sin inconsistencias ni artifacts del tipo anterior | ✅ |

## Suite 3 — Edge Cases (Code Review)

| TC ID | Tipo | Caso de Test | Pasos | Expected | Severidad | Estado |
|-------|------|-------------|-------|----------|-----------|--------|
| TC-CR-001 | EC | Cambio de tipo collection→boolean: verificar que spec se limpia | 1) Crear data structure con array > collection<br>2) Agregar sub-fields a la collection<br>3) Cambiar tipo a boolean<br>4) Inspeccionar estado del field | El field de tipo boolean no debería conservar spec con sub-fields del tipo anterior | 🟡 | ✅ |
| TC-CR-002 | EC | String no-template en array muestra como mapeable | 1) Abrir workflow con trigger<br>2) En un nodo, configurar array con valores texto estático (sin `{{ }}`)<br>3) Verificar si los campos muestran indicador "mapeable" | UX aceptable — verificar que el indicador no confunde al usuario | 🟡 | ✅ |
| TC-CR-003 | EC | Collection vacía + toggle Advanced no crashea | 1) Crear data structure con collection vacía (sin sub-fields)<br>2) Activar/desactivar toggle Advanced<br>3) Verificar consola del browser | No hay crash ni error en consola. El toggle funciona correctamente con collections vacías | 🟠 | ✅ |
| TC-CR-004 | EC | Flag advanced se limpia al cambiar tipo de field | 1) Crear data structure con field marcado como advanced<br>2) Cambiar el tipo del field<br>3) Verificar que el flag advanced desaparece<br>4) Si hay opción de clonar/duplicar, verificar flag en el clon | El flag advanced se limpia al cambiar tipo. Nuevos sub-fields no heredan advanced | 🟡 | ✅ |

## Suite 4 — Regresión (Context Panel Fix)

| TC ID | Tipo | Caso de Test | Pasos | Expected | Estado |
|-------|------|-------------|-------|----------|--------|
| TC-005 | REG | Panel de contexto NO se cierra al hacer clic en input mapeable | 1) Login como Tenant<br>2) Abrir un workflow con nodos configurados<br>3) Abrir un nodo con inputs mapeables<br>4) Hacer clic en un input mapeable para abrir el panel de contexto<br>5) Hacer clic en OTRO input mapeable en el mismo drawer | El panel de contexto se mantiene abierto (no se cierra inesperadamente). Se actualiza al nuevo input | ✅ |
| TC-006 | REG | Panel de contexto SÍ se cierra al hacer clic fuera | 1) Abrir panel de contexto en un nodo<br>2) Hacer clic fuera del panel y fuera de inputs mapeables (en el canvas o en otra zona) | El panel de contexto se cierra correctamente | ✅ |
| TC-007 | REG | FormBuilder en nodo sin datos de contexto no crashea | 1) Abrir un nodo cuyo contextNode no tiene datos en contextValues<br>2) Verificar que el drawer renderiza sin errores | El drawer renderiza correctamente. La condición `contextValues[contextNode]?.context ?? {}` evita el crash | ✅ |
