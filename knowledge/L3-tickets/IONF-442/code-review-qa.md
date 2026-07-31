# Code Review QA — IONF-442 (Modo Deployment / Bug Hunting)

## Resumen
- Repos revisados: `webcomponents-flow`
- Commits analizados: 4 (fce3463, 63213fd, f0fe14c, 3cd3767)
- Archivos modificados analizados: 13 (7 en fix principal + 6 en fix adicional)
- Hallazgos totales: 4
  - BUG confirmados: 0
  - RISK a verificar: 3
  - SEC seguridad: 0
  - EDGE cases: 1
- Módulos con impacto cruzado: Boards (FlowDrawer), Nodes (DataBuilder in-node)
- TCs inyectados en test-matrix: 4 (TC-CR-001 a TC-CR-004)

## Commits Analizados
| Repo | Commit | Mensaje | Archivos |
|------|--------|---------|----------|
| webcomponents-flow | fce3463 | IONF-442 (fix) fix data builder advanced fields | 7 archivos |
| webcomponents-flow | 63213fd | IONF-442 (fix) fix context panel unexpected auto close | 6 archivos |
| webcomponents-flow | f0fe14c | IONF-442 (fix) fix context panel unexpected auto close | merge |
| webcomponents-flow | 3cd3767 | IONF-442 (fix) fix code review observation | refactor |

## Archivos Modificados
| Repo | Archivo | Líneas +/- |
|------|---------|------------|
| webcomponents-flow | `src/ui/DataBuilder/FieldEditor.vue` | +48 / -38 |
| webcomponents-flow | `src/ui/FormBuilder/FieldIterator.vue` | +6 / -3 |
| webcomponents-flow | `src/ui/FormBuilder/FieldIteratorItem.vue` | +4 / -6 |
| webcomponents-flow | `src/ui/FormBuilder/FormBuilder.vue` | +15 / -8 |
| webcomponents-flow | `src/ui/FormBuilder/form.css` | +51 / -1 |
| webcomponents-flow | `src/ui/FormBuilder/lib/nestedElements.ts` | +15 / +0 |
| webcomponents-flow | `src/ui/FormBuilder/lib/nestedElements.spec.ts` | +50 / +0 |
| webcomponents-flow | `src/ui/Input/composables/useMapeableContext.ts` | +8 / -2 |
| webcomponents-flow | `src/ui/Input/InputMapeable.vue` | +1 |
| webcomponents-flow | `src/ui/Input/SpecialInputMapeable.vue` | +1 |
| webcomponents-flow | `src/flow/components/FlowDrawer/FlowDrawer.vue` | +13 / -3 |

---

## Follow-the-Flow Maps

### Flow 1: `isHiddenWhenBasic()` — Visibilidad de campos advanced
```
1. CALLERS: FieldIterator.vue (computed `showField`) → usa `isHiddenWhenBasic(props.field)`
   → Se inyecta en CADA instancia de FieldIterator en el árbol recursivo del formulario
   → FormBuilder.vue provee `showAdvanced` via inject/provide

2. PERSISTENCIA: No hay persistencia — es lógica de render pura
   → El flag `advanced` vive en el Field schema (viene del backend)

3. CONSUMIDORES: FieldIteratorItem.vue renderiza si `showField` es true
   → Si false → el componente completo se oculta (v-if, no v-show)

4. RENDER: 
   → showAdvanced=false: Se ocultan fields con `advanced:true`
   → showAdvanced=true: Se muestran todos los fields
   → isHiddenWhenBasic evalúa recursivamente colecciones y arrays

5. ERROR PATH: 
   → field.spec undefined → isHiddenWhenBasic retorna false (safe, campo visible)
   → field.spec no es array en collection → retorna false (safe)
   → Tests cubren estos edge cases ✅

6. OPERACIÓN OPUESTA: someAdvancedField() determina si mostrar el panel toggle
   → Lógica complementaria: someAdvancedField → muestra panel | isHiddenWhenBasic → oculta campos
```

### Flow 2: `onChangeType()` — Cambio de tipo de campo
```
1. CALLERS: FieldEditor.vue template → @change="onChangeType(field)"
   → Se ejecuta cada vez que el usuario cambia el dropdown de tipo

2. PERSISTENCIA: Modifica el objeto reactivo `field` in-place
   → Limpia: field.advanced (delete), field.options (delete), field.spec (reset)
   → Esto actualiza el estado reactivo que FormBuilder consume

3. CONSUMIDORES: FieldIterator.vue y FieldIteratorItem.vue reaccionan al cambio de props
   → isStringMapeable() en FieldIteratorItem decide qué renderizar por tipo

4. RENDER: 
   → text → spec=undefined, opciones limpiadas
   → date → spec=undefined
   → collection → spec=[]
   → array → spec={name:'array_specification', type:'text', ...}
   → select → spec=undefined, options=[]

5. ERROR PATH:
   → No hay catch/try — es manipulación directa del objeto reactivo
   → Si field.type tiene un valor no listado → no se ejecuta ningún bloque → spec queda como estaba
   ⚠️ RIESGO: tipos no listados (binary, number, boolean) no limpian spec

6. OPERACIÓN OPUESTA: No hay "revert type change" — el cambio es destructivo
   → Al cambiar de collection→text, los sub-fields se pierden irrecuperablemente
```

### Flow 3: `isEventInsideContext()` + `onOutsidePointerDown()` — Cierre del panel de contexto
```
1. CALLERS: FlowDrawer.vue → useEventListener(window, 'pointerdown', onOutsidePointerDown, true)
   → Captura TODOS los pointerdown del documento (capture: true)

2. PERSISTENCIA: Solo modifica ref `openContext` (false = cerrar panel)
   → No hay efectos secundarios en BD ni en estado persistente

3. CONSUMIDORES: ContextDialog.vue lee `openContext` para mostrar/ocultar
   → contextValues[contextNode]?.context ?? {} — optional chaining añadido

4. RENDER:
   → Click FUERA de .component-context y data-mapeable → cierra panel
   → Click DENTRO de .component-context o data-mapeable → NO cierra
   → El check se hace via composedPath() + classList/dataset

5. ERROR PATH:
   → Si composedPath() contiene un element que no es HTMLElement → se ignora (safe)
   → Si contextNode no existe en contextValues → optional chaining evita crash ✅

6. OPERACIÓN OPUESTA: Abrir contexto se maneja en useMapeableContext onFocus
   → onBlur ya NO cierra (el cambio removió esa línea)
   → Solo pointerdown outside cierra ahora
```

---

## Sección 2 — Riesgos a Verificar (RISK-CR-##)

### RISK-CR-001: `onChangeType` no limpia spec para tipos que no tienen bloque explícito

```
RISK-CR-001:
  Categoría: RISK
  Severidad: 🟡 Medio
  Repo: webcomponents-flow
  Commit: fce3463
  Archivo: src/ui/DataBuilder/FieldEditor.vue
  Línea: 127-170

  Descripción: Los tipos `binary`, `number`, `boolean` no tienen bloque en onChangeType() → si se cambia de collection→boolean, spec mantiene el valor anterior (array de fields)

  Evidencia:
    onChangeType maneja: select, text, date, collection, array
    NO maneja: binary, number, boolean
    → Si field.type es 'boolean' después del change, el `spec` del tipo anterior persiste

  Comportamiento Esperado:
    Al cambiar a un tipo leaf (number, boolean, binary), el spec debería limpiarse a undefined

  Comportamiento Actual:
    Los tipos no listados no ejecutan ningún bloque → spec queda con el valor del tipo anterior
    En la práctica esto puede no causar problemas visuales porque FieldIteratorItem no renderiza spec para estos tipos, pero es un estado inconsistente

  Precondiciones:
    User Role: Tenant User
    User State: Logged in
    Existing Data: Data Structure o Workflow con Form Builder

  Pasos de Reproducción:
    1) Navegar a Workflows > Data Store > Data Structure > Add
    2) Crear un array con elementos de tipo collection
    3) Agregar sub-fields a la collection
    4) Cambiar el tipo de collection a boolean
    5) Inspeccionar el estado del field (Vue DevTools) — ¿spec sigue teniendo los sub-fields?

  Test Data: Array > Collection con 2+ sub-fields > cambiar a boolean

  Impacto: Estado interno inconsistente — field.spec contiene datos del tipo anterior que podrían causar issues si el field se serializa/guarda

  Notas: El código original inline tenía el mismo issue, por lo que es un bug pre-existente que no se corrigió en la refactorización. Clasificado como RISK y no BUG porque no es introducido por el ticket, solo expuesto por la refactorización.

  Recomendación:
    - RISK → Inyectar como TC en la test-matrix
```

---

### RISK-CR-002: `isStringMapeable` trata `array` con data no-vacío como mapeable sin verificar sintaxis

```
RISK-CR-002:
  Categoría: RISK
  Severidad: 🟡 Medio
  Repo: webcomponents-flow
  Commit: fce3463
  Archivo: src/ui/FormBuilder/FieldIteratorItem.vue
  Línea: 188-193

  Descripción: La función simplificada retorna `data !== ''` para arrays y `true` para collections, sin verificar que el string contenga doble-llave — puede mostrar input mapeable para strings que no son templates

  Evidencia:
    function isStringMapeable(data: any) {
      if (typeof data !== 'string') return false;
      if (data.includes('{{') && data.includes('}}')) return true;
      if (props.value.type === 'array') return data !== '';    // ← cualquier string no vacío
      return props.value.type === 'collection';                // ← siempre true para collection
    }

  Comportamiento Esperado:
    Solo se debería mostrar el input mapeable para strings que representan mapeos o que el usuario configuró intencionalmente

  Comportamiento Actual:
    Para arrays: cualquier string no vacío (incluso "hello") se trata como mapeable
    Para collections: cualquier string se trata como mapeable
    Esto es intencional según la lógica del FormBuilder (cualquier string en array/collection puede ser reemplazado por un mapeo), pero podría confundir si hay defaults

  Precondiciones:
    User Role: Tenant User
    User State: Logged in

  Pasos de Reproducción:
    1) Abrir un workflow con trigger configurado
    2) En un nodo, configurar un array con valores de texto estático
    3) Verificar si los campos muestran el indicador de "mapeable" visualmente
    4) ¿El usuario entiende qué es mapeable y qué no?

  Test Data: Array con field default "hello world" (sin llaves dobles)

  Impacto: Bajo — UX potencialmente confusa pero funcional. El cambio de lógica es deliberado según el short-circuit pattern.

  Notas: El código original usaba una condición OR que cubría el mismo caso. La refactorización mantiene el mismo comportamiento con mejor legibilidad. Verificar en testing que el UX es aceptable.

  Recomendación:
    - RISK → Verificar visualmente en testing
```

---

### RISK-CR-003: `someAdvancedField` no tiene null-safety en spec como sí tiene `isHiddenWhenBasic`

```
RISK-CR-003:
  Categoría: RISK
  Severidad: 🟠 Alto
  Repo: webcomponents-flow
  Commit: fce3463
  Archivo: src/ui/FormBuilder/lib/nestedElements.ts
  Línea: 126-135

  Descripción: `someAdvancedField` castea `field.spec as Field[]` sin verificar si es array/null, mientras que `isHiddenWhenBasic` sí verifica `Array.isArray(field.spec)` y `!!field.spec`

  Evidencia:
    // isHiddenWhenBasic — CON null-safety ✅
    if (field.type === 'collection') {
      return Array.isArray(field.spec) && field.spec.length > 0 && ...
    }
    if (field.type === 'array') {
      return !!field.spec && isHiddenWhenBasic(field.spec as Field);
    }

    // someAdvancedField — SIN null-safety ⚠️
    if (field.type === 'collection') {
      return (field.spec as Field[]).some(...)   // ← crash si spec es undefined
    }
    if (field.type === 'array') {
      return someAdvancedField(field.spec as Field);  // ← crash si spec es undefined
    }

  Comportamiento Esperado:
    someAdvancedField debería tener la misma null-safety que isHiddenWhenBasic

  Comportamiento Actual:
    Si un field de tipo 'collection' tiene spec=undefined (posible tras onChangeType→collection que setea spec=[]), no crashea porque spec=[] → .some() retorna false.
    PERO: si el field llegara con spec=undefined (por datos corruptos o backend inconsistente), someAdvancedField crashearía con "Cannot read properties of undefined"

  Precondiciones:
    User Role: Tenant User
    Company/Tenant: Con data structures que tengan collections vacías o datos migrados

  Pasos de Reproducción:
    1) Crear una collection sin sub-fields (spec=[])
    2) Activar/desactivar el toggle Advanced
    3) Si spec se corrompe a undefined (edge case), verificar que la UI no crashea
    4) Verificar Vue DevTools si someAdvanced genera error

  Test Data: Collection con spec=undefined, spec=null, spec=[]

  Impacto: Crash del FormBuilder si un field de tipo collection tiene spec corrupto — poco probable pero posible con datos migrados

  Notas: Esta función NO fue modificada en el ticket (ya existía), pero la nueva función isHiddenWhenBasic fue escrita CON null-safety, lo que expone la inconsistencia. Clasificado como ticket-exposed.

  Recomendación:
    - RISK → Verificar en testing con data structures vacías
```

---

## Sección 4 — Edge Cases (EDGE-CR-##)

### EDGE-CR-001: onChangeType limpia `advanced` flag al cambiar tipo, pero no limpia al crear un nuevo field

```
EDGE-CR-001:
  Categoría: EDGE
  Severidad: 🟡 Medio
  Repo: webcomponents-flow
  Commit: fce3463
  Archivo: src/ui/DataBuilder/FieldEditor.vue
  Línea: 128-130

  Descripción: El fix añadió `delete field.advanced` dentro de onChangeType(), pero si el usuario marca un field como advanced y luego crea un nuevo sub-field dentro de un array/collection, el nuevo field hereda el contexto sin `advanced` (correcto), excepto si se duplica/clona un field advanced

  Evidencia:
    function onChangeType(field: Field) {
      if (field.advanced !== undefined) {
        delete field.advanced;   // ← limpia al cambiar tipo ✅
      }
      ...
    }

  Comportamiento Esperado:
    Al cambiar el tipo de un field, se limpia el flag advanced (lo hace ✅)
    Al duplicar/clonar un field advanced dentro del builder, el flag debería mantenerse o limpiarse según la intención

  Comportamiento Actual:
    El delete solo ocurre en onChangeType — otros flujos de creación/duplicación no se verificaron en este diff. El fix cumple con los AC del ticket.

  Precondiciones:
    User Role: Tenant User

  Pasos de Reproducción:
    1) Crear una data structure con un field marcado como advanced
    2) Cambiar el tipo del field → verificar que advanced se limpia
    3) Crear un sub-field dentro del mismo array → verificar que el nuevo field NO hereda advanced
    4) Si hay opción de duplicar/clonar un field → verificar qué pasa con el flag advanced

  Test Data: Field con advanced=true, cambio de tipo a text/number

  Impacto: Bajo — el fix funciona para el caso documentado, el edge case es sobre flows no cubiertos por el ticket

  Notas: Los AC del ticket solo piden que el toggle controle la visibilidad completa del array. El fix del flag advanced al cambiar tipo es un complemento lógico.

  Recomendación:
    - EDGE → Inyectar como TC en la test-matrix
```

---

## Pre-existentes encontrados

> Ningún bug pre-existente que amerite archivo separado. RISK-CR-003 documenta una inconsistencia pre-existente pero está cubierta como ticket-exposed en el reporte principal.

---

## Impacto Cruzado

| Módulo Impactado | Componente Afectado | Riesgo | Verificación Necesaria |
|---|---|---|---|
| **Boards** | FlowDrawer (context panel) | 🟠 Alto | Verificar que el panel de contexto no se cierra inesperadamente al hacer clic en inputs mapeables dentro del drawer |
| **Nodes** | DataBuilder in-node | 🟡 Medio | Verificar que el DataBuilder dentro de la configuración de un nodo muestra correctamente el toggle advanced |

## TCs Inyectados en Test Matrix

| TC ID | Categoría | Origen | Caso de Test | Severidad |
|-------|-----------|--------|-------------|-----------|
| TC-CR-001 | RISK | RISK-CR-001 | Cambio de tipo collection→boolean: spec no se limpia | 🟡 |
| TC-CR-002 | RISK | RISK-CR-002 | String no-template en array muestra como mapeable | 🟡 |
| TC-CR-003 | RISK | RISK-CR-003 | Collection con spec vacío/undefined no crashea FormBuilder | 🟠 |
| TC-CR-004 | EDGE | EDGE-CR-001 | Limpiar flag advanced al cambiar tipo + verificar en sub-fields | 🟡 |
