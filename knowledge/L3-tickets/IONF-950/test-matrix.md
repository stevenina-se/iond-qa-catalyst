# Test Matrix — IONF-950

> Generada por `test-docs/document` (modo matrix)
> Fecha: 2026-06-04
> Módulo: Nodes (Code node — `ion.action.code`) + Flow Pilot (agente IA)
> Ticket: Integración de la Interacción del Agente (Flow Pilot) con el Nodo Código (Custom Code)

## Resumen

| Métrica | Valor |
|---------|-------|
| Total de casos | 28 |
| Happy path | 6 |
| Edge cases | 9 |
| Negativos | 5 |
| Smoke tests | 3 |
| Regresión | 5 |
| Automatizables | 5 (UI button/drawer) |
| Cobertura de AC | 2/2 |

---

## Acceptance Criteria (Consolidados)

| AC | Descripción | Origen |
|----|-------------|--------|
| AC-1 | Generación de script inicial: Dado que el usuario instruye a Flow Pilot sobre una integración deseada → el agente procesa la solicitud → se inyecta un script de Python o JS válido en el contexto del nodo Code | Ticket original |
| AC-2 | Corrección autónoma de código fallido: Dado que el nodo ha devuelto un error de compilación y el usuario solicita a Flow Pilot que lo repare → el agente analiza la traza de error → se aplica un parche en el código resolviendo la excepción | Ticket original |
| AC-3 (implícito) | Botón "Ask Flow Pilot" visible en el panel de configuración del Code node, que abre el chat con contexto del nodo seleccionado | Dev changes (UI) |
| AC-4 (implícito) | El agente sigue convenciones del Code node: sin `main()`, usa objeto `input`, devuelve resultado vía `result`/`return`, soporta Python y JavaScript | Dev changes (skill generate-code) |

---

## Test Matrix

### BLOQUE 0 — SMOKE TESTS

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-001 | Nodes/Code + UI | AC-3 | Smoke | Botón "Ask Flow Pilot" visible en Code node | Flow existente con un Code node agregado | 1. Abrir flow existente en el canvas\n2. Hacer click en el Code node\n3. Verificar que se abre el drawer de configuración (CodeConfig) | El botón "Ask Flow Pilot" con ícono Sparkles aparece al lado de "Open Editor" | 🔴 | ✅ | ⬜ Pendiente |
| TC-002 | Nodes/Code + Flow Pilot | AC-1 | Smoke | Generación básica de código Python desde Flow Pilot | Flow con Code node configurado en Python, variables declaradas | 1. Abrir Code node → click "Ask Flow Pilot"\n2. Instruir: "Genera un script que tome el campo 'name' del input y lo devuelva en mayúsculas"\n3. Esperar respuesta del agente | Flow Pilot genera un script Python válido que usa `input` para acceder a las variables y devuelve el resultado. El código aparece en el editor CodeMirror | 🔴 | ❌ | ⬜ Pendiente |
| TC-003 | Nodes/Code + Flow Pilot | AC-2 | Smoke | Corrección básica de código fallido | Flow con Code node que tiene un error de sintaxis, nodo ejecutado con error | 1. Tener un Code node con código que falle al ejecutar\n2. Abrir Flow Pilot desde el Code node\n3. Pedir al agente: "Repara el error del código"\n4. Esperar la corrección | Flow Pilot lee el error de ejecución, analiza el traceback, y sobrescribe el código con la versión corregida | 🔴 | ❌ | ⬜ Pendiente |

---

### BLOQUE 1 — HAPPY PATH (AC-1: Generación de script)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-004 | Nodes/Code + Flow Pilot | AC-1 | Happy Path | Generación de código JavaScript | Flow con Code node configurado en JavaScript, con variables de input | 1. Configurar Code node con language=JavaScript y declarar variables (ej: `price`, `quantity`)\n2. Click "Ask Flow Pilot"\n3. Instruir: "Calcula el total multiplicando price por quantity y devuelve el resultado"\n4. Esperar generación | El agente genera código JS válido que: usa `input.price` y `input.quantity`, calcula el total, y usa `return` para devolver el resultado. Sin `main()` | 🔴 | ❌ | ⬜ Pendiente |
| TC-005 | Nodes/Code + Flow Pilot | AC-1, AC-4 | Happy Path | Generación con detección de output esperado (downstream) | Flow con Code node → conectado a un nodo downstream (ej: Mapper/Form) | 1. Crear flow: Trigger → Code node → Form node\n2. Configurar variables en el Code node\n3. Abrir Flow Pilot desde el Code node\n4. Instruir: "Genera código que prepare los datos para el siguiente nodo" | El agente detecta el nodo downstream, lee su spec de entrada, y genera código cuyo `result` tiene la estructura que el nodo downstream espera | 🔴 | ❌ | ⬜ Pendiente |
| TC-006 | Nodes/Code + Flow Pilot | AC-1 | Happy Path | Código generado se visualiza en tiempo real en el editor | Flow con Code node, Flow Pilot abierto | 1. Abrir Flow Pilot desde Code node\n2. Solicitar generación de código\n3. Observar el editor CodeMirror mientras el agente genera | El código aparece en el editor CodeMirror en tiempo real (streaming). El usuario ve el código escribirse progresivamente | 🔴 | ❌ | ⬜ Pendiente |

---

### BLOQUE 2 — HAPPY PATH (AC-2: Corrección de errores)

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-007 | Nodes/Code + Flow Pilot | AC-2 | Happy Path | Corrección de error Python (runtime error) | Code node Python con error runtime (ej: `NameError`, `TypeError`) ya ejecutado | 1. Ejecutar flow con Code node que tiene error runtime\n2. Verificar que el nodo muestra status error\n3. Abrir Flow Pilot desde el Code node\n4. Solicitar: "El código falló, por favor corrige el error"\n5. Esperar corrección | El agente lee los logs de ejecución (`execution_logs`/`execution_node_detail`), identifica el error, y sobrescribe el código con la corrección. El nuevo código resuelve la excepción | 🔴 | ❌ | ⬜ Pendiente |
| TC-008 | Nodes/Code + Flow Pilot | AC-2 | Happy Path | Corrección de error JavaScript (syntax error) | Code node JS con error de sintaxis ya ejecutado | 1. Escribir código JS con error de sintaxis en el Code node\n2. Ejecutar el flow\n3. Abrir Flow Pilot desde el Code node\n4. Pedir corrección del error | El agente identifica el error de sintaxis desde el traceback, corrige el código JS y lo sobrescribe en el editor | 🔴 | ❌ | ⬜ Pendiente |
| TC-009 | Nodes/Code + Flow Pilot | AC-2 | Happy Path | Loop de recuperación de errores (retry) | Code node con error complejo que requiere más de un intento | 1. Configurar Code node con código que falla por lógica compleja\n2. Ejecutar → falla\n3. Pedir a Flow Pilot que corrija\n4. Si la primera corrección falla, pedir corrección nuevamente\n5. Verificar que el agente intenta hasta 3 veces | El agente intenta corregir hasta un máximo de 3 intentos (según skill generate-code). Cada intento usa el error del intento anterior como contexto | 🟠 | ❌ | ⬜ Pendiente |

---

### BLOQUE 3 — EDGE CASES

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-010 | Nodes/Code + Flow Pilot | AC-1 | Edge Case | Generación con múltiples nodos target (downstream) | Code node conectado a 2+ nodos downstream | 1. Crear flow donde Code node tiene 2 nodos conectados en su salida\n2. Abrir Flow Pilot desde el Code node\n3. Solicitar generación de código | El agente toma solo el PRIMER target conectado como referencia para la estructura del output (según diseño técnico) | 🟠 | ❌ | ⬜ Pendiente |
| TC-011 | Nodes/Code + Flow Pilot | AC-1 | Edge Case | Cambio de lenguaje entre turnos de conversación | Code node inicialmente en Python, luego cambiado a JavaScript | 1. Abrir Flow Pilot con Code node en Python\n2. Generar código Python\n3. Cambiar language del Code node a JavaScript (sin cerrar chat)\n4. Pedir al agente que regenere en JS | El agente detecta el cambio de lenguaje y genera código en el nuevo lenguaje (JS). El código anterior Python se reemplaza correctamente | 🟠 | ❌ | ⬜ Pendiente |
| TC-012 | Nodes/Code + Flow Pilot | AC-1 | Edge Case | Código con dependencias externas (pip/npm) | Code node con dependencias declaradas | 1. Configurar Code node con dependencias (ej: `requests` para Python, `axios` para JS)\n2. Instruir a Flow Pilot para generar código que use esa dependencia\n3. Verificar la generación | El agente genera código que importa y usa la dependencia declarada. El código respeta las convenciones (`import` en Python, `require`/`import` en JS) | 🟠 | ❌ | ⬜ Pendiente |
| TC-013 | Nodes/Code + Flow Pilot | AC-4 | Edge Case | Variables vacías en el Code node (sin input configurado) | Code node sin variables declaradas en el form builder | 1. Agregar Code node al flow SIN configurar variables\n2. Abrir Flow Pilot\n3. Pedir generación de código | El agente genera código sin referencias a `input` o indica al usuario que no hay variables configuradas y sugiere configurarlas | 🟠 | ❌ | ⬜ Pendiente |
| TC-014 | Nodes/Code + Flow Pilot | AC-1 | Edge Case | Code node sin nodo downstream conectado | Code node sin conexión de salida | 1. Agregar Code node sin conectar a ningún nodo downstream\n2. Abrir Flow Pilot y generar código\n3. Verificar que no intente detectar output spec | El agente genera código sin referencia a output spec del downstream. El código simplemente devuelve un resultado genérico | 🟡 | ❌ | ⬜ Pendiente |
| TC-015 | UI (webcomponents-flow) | AC-3 | Edge Case | Auto-cierre del drawer al abrir Flow Pilot | Code node drawer abierto | 1. Hacer click en Code node → se abre el drawer\n2. Click en "Ask Flow Pilot"\n3. Observar comportamiento del drawer y del chat | El drawer se cierra automáticamente y el panel de chat se abre. No hay conflictos de z-index entre drawer y chat | 🟠 | ✅ | ⬜ Pendiente |
| TC-016 | UI (gateway-ion) | AC-3 | Edge Case | Nodo Code seleccionado correctamente al abrir Flow Pilot | Flow con múltiples nodos, Code node entre ellos | 1. Tener flow con varios nodos\n2. Hacer click en el Code node → drawer\n3. Click "Ask Flow Pilot"\n4. Verificar que el chat tiene contexto del Code node | El `nodeId` del Code node se establece en `selectedNodes` del FlowEditor. El chat muestra contexto del nodo correcto | 🟠 | ✅ | ⬜ Pendiente |
| TC-017 | Nodes/Code + Flow Pilot | AC-2 | Edge Case | Error con traceback largo (payload grande) | Code node con código que genera un traceback extenso | 1. Escribir código Python que genere un stack trace largo (recursión profunda, imports fallidos en cadena)\n2. Ejecutar → falla\n3. Pedir corrección a Flow Pilot | El agente maneja el traceback largo (truncado a 30KB según `TruncateThreshold`) y aún puede identificar el error raíz | 🟡 | ❌ | ⬜ Pendiente |
| TC-018 | Nodes/Code + Flow Pilot | AC-1 | Edge Case | Generación de código complejo (integración real) | Code node con variables de un connector upstream | 1. Crear flow: Trigger → Connector node → Code node\n2. El Code node recibe datos del connector (ej: datos de Shopify)\n3. Instruir a Flow Pilot: "Transforma los datos de productos para filtrar solo los activos y calcular el total de inventario" | El agente genera código que accede correctamente a la estructura de datos del upstream vía `input`, procesa los datos, y devuelve el resultado estructurado | 🟠 | ❌ | ⬜ Pendiente |

---

### BLOQUE 4 — NEGATIVOS

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-019 | Nodes/Code + Flow Pilot | AC-4 | Negativo | Código generado NO debe usar patrón `main()` | Code node Python, Flow Pilot abierto | 1. Instruir a Flow Pilot para generar código Python\n2. Revisar el código generado | El código generado NUNCA incluye `def main()` ni patrón `main()`. Debe usar directamente `input` y devolver con `result`/`return` (según convención del skill generate-code) | 🔴 | ❌ | ⬜ Pendiente |
| TC-020 | Nodes/Code + Flow Pilot | AC-4 | Negativo | Código generado NO debe usar `processedData` | Code node, Flow Pilot generando código | 1. Generar código para Code node\n2. Inspeccionar que no use `processedData` | El código accede a datos vía objeto `input` (que viene de `staticData`), NUNCA vía `processedData` — esto es una regla de seguridad para evitar inyección de expresiones | 🔴 | ❌ | ⬜ Pendiente |
| TC-021 | UI | AC-3 | Negativo | Botón "Ask Flow Pilot" NO debe aparecer en nodos que NO son Code | Flow con otros tipos de nodos (Condition, Timer, Form) | 1. Abrir drawer de un nodo Simple Decision\n2. Abrir drawer de un nodo Timer\n3. Abrir drawer de un nodo Form\n4. Verificar que "Ask Flow Pilot" NO aparece | El botón "Ask Flow Pilot" solo aparece en el drawer del Code node (`CodeConfig.vue`), NO en otros drawers de configuración | 🟠 | ✅ | ⬜ Pendiente |
| TC-022 | Nodes/Code + Flow Pilot | AC-2 | Negativo | Error no reparable después de 3 intentos | Code node con error lógicamente irreparable | 1. Configurar Code node con código que tiene un error fundamental imposible de resolver (ej: dependencia que no existe)\n2. Pedir corrección a Flow Pilot\n3. Después de 3 intentos fallidos, verificar comportamiento | El agente se detiene después de máximo 3 intentos y comunica al usuario que no pudo resolver el error, sugiriendo revisión manual | 🟡 | ❌ | ⬜ Pendiente |
| TC-023 | Nodes/Code + Flow Pilot | AC-1 | Negativo | Instrucción vacía o sin sentido al agente | Code node, Flow Pilot abierto | 1. Abrir Flow Pilot desde Code node\n2. Enviar un mensaje vacío o sin sentido (ej: "asdfgh")\n3. Verificar respuesta del agente | El agente responde solicitando una instrucción clara. No genera código basura ni crashea | 🟡 | ❌ | ⬜ Pendiente |

---

### BLOQUE 5 — REGRESIÓN

| ID | Módulo impactado | Caso de regresión | Por qué podría romperse | Prioridad | Estado |
|----|-----------------|-------------------|------------------------|-----------|--------|
| REG-001 | Flow Pilot (general) | Flow Pilot sigue funcionando para nodos NO-Code (ej: pedir ayuda con un Condition node) | El system prompt se actualizó con ~95 líneas nuevas para Code node. El skill `create-integration` fue modificado. Podría haber side effects en otros prompts/skills | 🟠 | ⬜ Pendiente |
| REG-002 | Code node (manual) | El Code node sigue permitiendo escritura manual de código sin usar Flow Pilot | Se agregó el botón "Ask Flow Pilot" en CodeConfig.vue. El botón "Open Editor" y la funcionalidad manual del editor CodeMirror no deben verse afectados | 🔴 | ⬜ Pendiente |
| REG-003 | FlowDrawer (otros nodos) | Los drawers de configuración de otros nodos siguen abriendo y cerrando normalmente | Se modificó `FlowDrawer.vue` para auto-cerrar al emitir `open_node_copilot`. Este evento solo debe dispararse desde el Code node, no desde otros drawers | 🟠 | ⬜ Pendiente |
| REG-004 | Flow Editor (chat) | El panel de chat de Flow Pilot sigue abriéndose correctamente desde el botón principal (no solo desde el Code node) | Se agregó un handler en `FlowEditor.vue` para `open_node_copilot`. El flujo normal de abrir chat (`chatOpen`) no debe verse afectado | 🟠 | ⬜ Pendiente |
| REG-005 | Code node (ejecución) | La ejecución del Code node sigue funcionando correctamente (timeout, dependencias, variables) | Aunque este ticket no modifica el runner, los cambios en el system prompt y skill podrían generar código que no siga las convenciones del runner | 🟡 | ⬜ Pendiente |

---

## Queries de Verificación BD

> **Nota**: Este ticket NO incluye cambios en base de datos (PostgreSQL ni SQLite). No hay migraciones nuevas.
> La verificación de datos se realiza via:
> - UI: Historial de ejecuciones (verificar que el Code node ejecute correctamente el código generado por Flow Pilot)
> - API: Logs de ejecución del nodo (`execution_logs`, `execution_node_detail`)

```sql
-- No aplican queries de BD para este ticket.
-- Verificación se hace via ejecución del flow y revisión de logs del nodo Code.
-- El Code node almacena resultados en SQLite de ejecución (tabla nodes.result)
-- pero esto ya existe y no fue modificado.
```

---

## Notas

- **Repos afectados**: `flow_binaries` (backend Go — skill + prompt), `webcomponents-flow` (botón UI), `gateway-ion` (handler FlowEditor)
- **MRs**: [webcomponents-flow MR#239](https://gitlab.com/altacrest/integrations/webcomponents-flow/-/merge_requests/239), [gateway-ion MR#221](https://gitlab.com/altacrest/gateway-ion/-/merge_requests/221), [flow_binaries MR#154](https://gitlab.com/altacrest/flow_binaries/-/merge_requests/154)
- **Unit tests del dev**: 4 nuevos tests (2 en flow_binaries, 1 en webcomponents-flow, 1 en gateway-ion) — todos PASSED
- **Dependencia**: Requiere que el Code node (`ion.action.code`) esté funcional y el Code Runner esté disponible en staging
- El skill `generate-code` tiene un loop de máximo 3 intentos para corrección de errores
- El system prompt tiene `TruncateThreshold` de 30KB para payloads grandes
- Para los TC de IA/agente (TC-002 a TC-009, TC-019, TC-020, TC-022, TC-023), la validación requiere interacción real con el LLM — los resultados pueden variar entre ejecuciones
