# Test Plan — IONF-950

## Información del Ticket

| Campo | Valor |
|-------|-------|
| ID | IONF-950 (ClickUp: 86e0w3rxf) |
| Título | Integración de la Interacción del Agente (Flow Pilot) con el Nodo Código (Custom Code) |
| Módulo | Nodes (Code node — `ion.action.code`) + Flow Pilot (agente IA) |
| Tipo | New Feature |
| Prioridad | High |
| QA Engineer | Steve Nina |
| Fecha del plan | 2026-06-04 |
| Status actual | QA In Process (deployed en staging) |
| Repos afectados | `flow_binaries`, `webcomponents-flow`, `gateway-ion` |

## Resumen

| Métrica | Valor |
|---------|-------|
| Total de casos | 28 |
| Smoke tests | 3 |
| Happy path | 6 |
| Edge cases | 9 |
| Negativos | 5 |
| Regresión | 5 |
| Tiempo estimado | ~120-150 min |
| Artefactos de Discovery usados | Ninguno (ticket entró directo a Deployment) |

---

## Orden de Ejecución

### BLOQUE 1 — SMOKE TESTS (ejecutar primero, si alguno falla → escalar)

| Orden | ID | Descripción | Prioridad | Rol |
|-------|------|-------------|-----------|-----|
| 1 | TC-001 | Botón "Ask Flow Pilot" visible en Code node | 🔴 | Company |
| 2 | TC-002 | Generación básica de código Python desde Flow Pilot | 🔴 | Company |
| 3 | TC-003 | Corrección básica de código fallido | 🔴 | Company |

> ⚠️ **Gate**: Si cualquier smoke test falla → **PARAR** y escalar al developer (Gustavo Mamani). No continuar con el resto del plan.

---

### BLOQUE 2 — HAPPY PATH — Generación de código (AC-1)

| Orden | ID | Descripción | Prioridad |
|-------|------|-------------|-----------|
| 4 | TC-004 | Generación de código JavaScript | 🔴 |
| 5 | TC-005 | Generación con detección de output esperado (downstream) | 🔴 |
| 6 | TC-006 | Código generado se visualiza en tiempo real en editor (streaming) | 🔴 |

---

### BLOQUE 3 — HAPPY PATH — Corrección de errores (AC-2)

| Orden | ID | Descripción | Prioridad |
|-------|------|-------------|-----------|
| 7 | TC-007 | Corrección de error Python (runtime: NameError/TypeError) | 🔴 |
| 8 | TC-008 | Corrección de error JavaScript (syntax error) | 🔴 |
| 9 | TC-009 | Loop de recuperación de errores (retry hasta 3 intentos) | 🟠 |

---

### BLOQUE 4 — EDGE CASES

| Orden | ID | Descripción | Prioridad |
|-------|------|-------------|-----------|
| 10 | TC-015 | Auto-cierre del drawer al abrir Flow Pilot | 🟠 |
| 11 | TC-016 | Nodo Code seleccionado correctamente al abrir Flow Pilot (selectedNodes) | 🟠 |
| 12 | TC-010 | Generación con múltiples nodos target (downstream) | 🟠 |
| 13 | TC-011 | Cambio de lenguaje entre turnos de conversación | 🟠 |
| 14 | TC-012 | Código con dependencias externas (pip/npm) | 🟠 |
| 15 | TC-018 | Generación de código complejo (integración real con connector) | 🟠 |
| 16 | TC-013 | Variables vacías en Code node (sin input configurado) | 🟠 |
| 17 | TC-014 | Code node sin nodo downstream conectado | 🟡 |
| 18 | TC-017 | Error con traceback largo (payload > TruncateThreshold) | 🟡 |

---

### BLOQUE 5 — NEGATIVOS

| Orden | ID | Descripción | Prioridad |
|-------|------|-------------|-----------|
| 19 | TC-019 | Código generado NO debe usar patrón `main()` | 🔴 |
| 20 | TC-020 | Código generado NO debe usar `processedData` | 🔴 |
| 21 | TC-021 | Botón "Ask Flow Pilot" NO aparece en nodos no-Code | 🟠 |
| 22 | TC-022 | Error no reparable después de 3 intentos | 🟡 |
| 23 | TC-023 | Instrucción vacía o sin sentido al agente | 🟡 |

> **Nota**: TC-019 y TC-020 son verificaciones de seguridad/convención que se validan durante la ejecución de TC-002, TC-004, TC-005 y TC-006. Se pueden verificar en paralelo al inspeccionar el código generado.

---

### BLOQUE 6 — REGRESIÓN

| Orden | ID | Descripción | Prioridad |
|-------|------|-------------|-----------|
| 24 | REG-002 | Code node permite escritura manual sin Flow Pilot | 🔴 |
| 25 | REG-001 | Flow Pilot funciona para nodos NO-Code | 🟠 |
| 26 | REG-003 | Drawers de otros nodos abren y cierran normalmente | 🟠 |
| 27 | REG-004 | Chat de Flow Pilot abre desde botón principal | 🟠 |
| 28 | REG-005 | Ejecución del Code node funciona correctamente (manual) | 🟡 |

---

## Datos Necesarios

| Dato | Cómo obtenerlo | Notas |
|------|---------------|-------|
| Credenciales staging | `.env` del repo `ionflow-qa-catalyst` | Usar usuario Company para tests principales |
| Flow de prueba con Code node | Crear en staging o usar existente | Debe tener al menos 1 Code node Python y 1 JS |
| Code node con variables | Configurar variables en form builder del Code node | Variables como `name`, `price`, `quantity` |
| Flow con Code → downstream | Crear flow: Trigger → Code → Form/Mapper | Para TC-005, TC-010 |
| Flow con connector upstream | Crear flow: Trigger → Connector → Code | Para TC-018 |
| Código con errores intencionales | Preparar scripts Python/JS con errores conocidos | Para TC-003, TC-007, TC-008, TC-009, TC-022 |
| Code Runner | Verificar que `CODE_RUNNER_URL` esté activo en staging | Prerequisito para ejecución de código |

### Códigos de error para preparar

| Para TC | Lenguaje | Error a provocar |
|---------|----------|------------------|
| TC-003 | Python | Error de sintaxis simple (ej: `print("hello"` — falta `)`) |
| TC-007 | Python | `NameError` — variable no definida (ej: `result = undefined_var + 1`) |
| TC-008 | JavaScript | Syntax error (ej: `const x = {` — falta `}`) |
| TC-009 | Python/JS | Error lógico complejo que requiera múltiples intentos |
| TC-022 | Python | `import nonexistent_module` — dependencia imposible |

---

## Criterios de Aprobación/Rechazo

### ✅ CRITERIOS DE APROBACIÓN

- ✅ **TODOS** los smoke tests (TC-001 a TC-003) pasan
- ✅ **TODOS** los happy path (TC-004 a TC-009) pasan
- ✅ Al menos **80%** de los edge cases pasan (7 de 9 mínimo)
- ✅ **TODOS** los negativos críticos pasan (TC-019, TC-020 — convenciones de código)
- ✅ **TODOS** los casos de regresión pasan
- ✅ El código generado por Flow Pilot es ejecutable y produce resultados correctos

### ❌ CRITERIOS DE RECHAZO

- ❌ Algún smoke test falla → **rechazo inmediato**
- ❌ Happy path falla → **rechazo**
- ❌ TC-019 o TC-020 fallan (código usa `main()` o `processedData`) → **rechazo** (violación de convención de seguridad)
- ❌ Caso de regresión falla (funcionalidad existente rota) → **rechazo con análisis de impacto**
- ❌ El botón "Ask Flow Pilot" no aparece o no abre el chat → **rechazo**

### ⚠️ CRITERIOS DE APROBACIÓN CON OBSERVACIONES

- ⚠️ Edge case falla pero no es bloqueante (TC-014, TC-017) → aprobar con bug registrado
- ⚠️ La calidad del código generado por la IA varía entre ejecuciones → aprobar si el flujo funciona aunque el código no sea perfecto
- ⚠️ TC-022 (error no reparable) no se detiene exactamente a los 3 intentos → aprobar con observación si eventualmente se detiene

---

## Estimación de Tiempo

| Bloque | Casos | Tiempo estimado | Notas |
|--------|-------|-----------------|-------|
| Smoke tests | 3 | ~15 min | Setup + 3 verificaciones rápidas |
| Happy path (generación) | 3 | ~25 min | Requiere interacción con LLM, esperar respuestas |
| Happy path (corrección) | 3 | ~25 min | Preparar errores + pedir corrección + verificar |
| Edge cases | 9 | ~35 min | Algunos requieren setup especial de flows |
| Negativos | 5 | ~15 min | TC-019/020 se verifican en paralelo con happy path |
| Regresión | 5 | ~15 min | Verificaciones rápidas de funcionalidad existente |
| **Total** | **28** | **~130 min (~2h 10min)** | Incluye setup de datos |

> **Nota**: Los TCs que involucran interacción con el LLM (TC-002 a TC-023 excepto UI) pueden tardar más si la IA tiene latencia o si los resultados requieren re-ejecución.

---

## Estrategia de Ejecución

### Canal 1 — Playwright MCP (Testing asistido)

La mayoría de los tests se ejecutarán via **Canal 1** (Playwright MCP con supervisión del QA Engineer):

1. **Login** en staging con credenciales Company
2. **Navegar** al Flow Editor
3. **Crear/abrir** flows de prueba con Code nodes
4. **Ejecutar** cada TC siguiendo los pasos de la test-matrix
5. **Capturar screenshots** como evidencia en `L3-tickets/IONF-950/screenshots/`

### Orden sugerido de flows de prueba

| # | Flow | Para TCs | Setup |
|---|------|----------|-------|
| 1 | Flow básico: Trigger → Code (Python) | TC-001, TC-002, TC-006, TC-013, TC-014, TC-019, TC-020 | Code node con variables simples |
| 2 | Flow básico: Trigger → Code (JS) | TC-004 | Code node JS con variables |
| 3 | Flow con downstream: Trigger → Code → Form | TC-005, TC-010 | Code node conectado a Form node |
| 4 | Flow con errores Python: Trigger → Code (error) | TC-003, TC-007, TC-009 | Código Python con errores intencionales |
| 5 | Flow con errores JS: Trigger → Code (error) | TC-008 | Código JS con error de sintaxis |
| 6 | Flow complejo: Trigger → Connector → Code | TC-018 | Con datos reales de connector |
| 7 | Flow existente (cualquiera) | TC-021, REG-001 a REG-005 | Para regresión y negativos UI |

---

## Estado

⏳ **Plan creado — esperando inicio de ejecución**

### Pre-checks antes de comenzar

- [ ] Staging deployed y accesible
- [ ] Code Runner (`CODE_RUNNER_URL`) activo y respondiendo
- [ ] Credenciales de `.env` verificadas
- [ ] Flow Pilot habilitado en staging
- [ ] Al menos un flow con Code node disponible (o capacidad de crear uno)
