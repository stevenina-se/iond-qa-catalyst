# 🧪 Regresión E2E — v0.1.0 | Primera Release a Producción

## Descripción General

Esta es la regresión End-to-End previa al **primer despliegue a producción de Ionflow v0.1.0**. Se trata de la primera release oficial del producto, consolidando más de **182 tickets** que introducen cambios significativos en:

- **Motor de ejecución de flows** refactorizado (IONF-379) — cambios en la lógica de nodos, queue y ejecución
- **Sistema de autenticación SSO con Keycloak** (IONF-362, IONF-1074) — migración y correcciones críticas de login
- **Nuevos nodos del canvas**: Switch dinámico, Timer, Call Component-Flow, Aggregate, Code (IONF-227, IONF-266, IONF-328, IONF-935, IONF-939)
- **Motor de versionamiento Git para flows** (IONF-419, IONF-482) — commit, restore, historial
- **Nodo Transformer** con múltiples correcciones (IONF-320, IONF-376, IONF-404, IONF-416, IONF-463, IONF-516)
- **Motor de Webhooks** (IONF-449, IONF-786, IONF-695)
- **Data Store / Persistent Data** — nuevos nodos y correcciones (IONF-159, IONF-162, IONF-163, IONF-552)
- **ION PDF** integrado al canvas (IONF-820)
- **Sistema de GRAPPs** — instalación, configuración y marketplace (IONF-103, IONF-997)
- **Permisos y multi-usuario** por company (IONF-655, IONF-763, IONF-764)

⚠️ **Esta es la única oportunidad de prueba antes del lanzamiento. El criterio de calidad es cero regresiones críticas no documentadas.**

---

## 🌐 Entorno de Prueba

| Campo | Valor |
|-------|-------|
| **Ambiente** | `staging-app.ionflow.io` |
| **Branch** | `v0.1.0` |
| **Tipo de prueba** | Manual + Playwright MCP (donde aplique) |
| **Alcance** | Regresión completa E2E — todos los módulos |

---

## 📋 Matriz de Pruebas

**Archivo:** `regression-matrix.csv`
**Ubicación:** `knowledge/releases/v0.1.0/` en el repositorio `ionflow-qa-catalyst`
**Columnas:** `SIDE | MODULE/FEATURE | (jerarquía) | ASSIGNED | RESOLUTION | COMMENTS | OBSERVATION | TICKET | PRIORITY`

La matriz cubre **~200 casos de prueba** distribuidos en:

- **KC** — Forgot Password, Login Now, Login with SSO, Sign Up with SSO
- **ADMIN** — Dashboard, Templates, Companies, Connectors, Boards, Apps (Legacy/Applications/Grapps/Custom), Developers, Settings
- **TENANT** — Boards (todos los nodos + Storage + ION PDF + Git + Flow Pilot), Execution History, Webhooks, Connections, Data Store, PDF Templates, Credentials, Accounts, Developer Apps, Catalog, Notifications, Settings, Teams, Account, Language
- **ADMIN GATEWAY** — Apps (Edit/Delete/New App/Settings/Services), Customer (Configured Channels + Marketplace)

---

## 📌 Instrucciones para Testers

### 1. Ejecución de casos

- Ejecutar todos los casos asignados en **`staging-app.ionflow.io`**
- Registrar el resultado directamente en la columna **RESOLUTION** del CSV
- Prestar atención especial a la columna **OBSERVATION** de cada caso — indica contexto técnico específico (ej. "Verificar en modo Test y modo Produccion")
- Para nodos del canvas: verificar siempre **dos modos**: Development (manual/step-by-step) y Production (live/background)

### 2. Marcar como PASSED ✅

Actualizar la columna **RESOLUTION** a `Passed` si:

- La funcionalidad opera correctamente en el entorno de staging
- No se observan errores 500, pantallas en blanco, PDFs vacíos, exports corruptos, ni resultados inesperados
- El output del nodo/flow coincide con el resultado esperado

### 3. Marcar como FAILED + Reportar Bug ❌

Si se detecta un problema:

1. Actualizar **RESOLUTION → `Failed`**
2. Crear un ticket de bug en ClickUp con:
   - **Título** descriptivo del error
   - **Entorno** afectado: `staging-app.ionflow.io`
   - **Steps to reproduce**
   - **Comportamiento esperado vs. observado**
   - **Screenshot / log de error**
3. Colocar el **ID del ticket creado** en la columna **TICKET** del mismo caso en la matriz

### 4. Marcar como SKIPPED ⏭️

Los ítems del side **ADMIN GATEWAY > Apps > Services** están marcados como `Skipped` porque dependen de la fusión de la rama `1.4.x` a `DEVELOPMENT`. No testear en esta regresión.

### 5. Casos con riesgo de falla silenciosa ⚠️

Estos casos requieren verificación **activa** — no basta con que la pantalla no muestre error:

- **Ejecución de flows con nodos Transformer/Iterator** → Verificar que el output tiene los datos correctos (no null, no vacío, no acumulado de otra ejecución)
- **Historial de ejecuciones** → Confirmar que cada nodo registra su status y resultado en el historial
- **Webhooks como triggers** → Verificar en el historial de ejecuciones que el flow fue disparado con el payload correcto
- **Data Store (Persistent Data)** → Verificar que los datos guardados persisten y son recuperables correctamente. Que no haya solapamiento entre sesiones o companies
- **PDF Templates / Nodo ION PDF** → Abrir el PDF generado y verificar: contenido correcto, sin páginas en blanco, sin truncamiento
- **Git / Versionamiento de flows** → Confirmar que el restore recupera exactamente el estado anterior, sin pérdida de nodos o configuración
- **Permisos por rol** → Un usuario sin permiso específico (ej. READ_BOARD) no debe poder acceder al módulo — verificar que retorna error o redirige, no solo que el botón desaparece
- **OAuth / Refresh Token** → Ejecutar un flow con nodo de connector cuyo token esté próximo a expirar y verificar que se refresca sin interrumpir la ejecución

---

## 🚦 Criterios de Prioridad

Al reportar un bug, asignar prioridad según la siguiente guía:

| Severidad | Criterio | Ejemplos |
|-----------|----------|---------|
| 🔴 **Urgent** | Bloquea completamente la funcionalidad principal. Sin workaround posible | Login SSO no funciona; flow no ejecuta; nodo Transformer nunca emite output |
| 🟠 **High** | Funcionalidad importante afectada. Puede tener workaround parcial | Webhook trigger no dispara el flow; Git restore no recupera el estado |
| 🟡 **Normal** | Funcionalidad secundaria afectada o comportamiento incorrecto no bloqueante | Preview de nodo muestra datos de otro nodo; URL no se actualiza al crear Board |
| 🟢 **Low** | Error cosmético o de UX menor, sin impacto funcional | Scroll doble en canvas; colores de modal incorrectos |

**¿Por qué esta prioridad?** Cada bug reportado debe incluir una línea explicando el impacto operativo concreto.
*Ejemplo: "Prioridad Urgent: el nodo Transformer no emite output cuando el input contiene un campo boolean sin valor default, lo que rompe todos los flows que usan esta configuración."*

---

## 🔁 Flujos Cross-Módulo E2E (Prioridad Máxima)

Los siguientes flujos deben ejecutarse con **especial atención** ya que cruzan múltiples módulos y validan la integración completa del stack:

1. **Auth → Boards → Execution**: Login SSO con Keycloak → crear flow → ejecutarlo → verificar historial de ejecuciones
2. **Boards → Webhook → Execution**: Crear flow con Webhook trigger → enviar POST externo → verificar ejecución en historial con payload correcto
3. **Boards → Data Store → Boards**: Flow con nodo Persistent Data Save → flow diferente con nodo Persistent Data Get sobre el mismo store → verificar aislamiento multi-tenant
4. **Connections → Boards → Execution**: Crear connector con Basic Auth → configurar nodo de app en flow → ejecutar → verificar que la llamada a la API externa retorna datos correctos
5. **Canvas → Git → Canvas**: Crear flow con nodos → hacer commit → modificar el flow → restaurar versión anterior → verificar estado idéntico al del commit
6. **Boards → PDF → Download**: Configurar nodo ION PDF con template → ejecutar flow → descargar PDF generado → verificar que el PDF tiene el contenido esperado
7. **GRAPP → Tenant → Connections**: Instalar GRAPP desde Admin Gateway → verificar en Tenant que la instalación aparece → configurar conexión → verificar que el flow del GRAPP ejecuta correctamente
8. **Auth → Permissions → Boards**: Crear usuario con permisos limitados → verificar que no puede acceder a módulos restringidos → verificar que el usuario con todos los permisos sí puede

---

## ✅ Criterios de Aceptación / Definition of Done

- [ ] 100% de los casos de la matriz ejecutados (estado `Passed`, `Failed` o `Skipped` justificado)
- [ ] Ningún caso en estado vacío / `To Test` al cierre
- [ ] Todos los casos en estado `Failed` tienen un ticket de bug en ClickUp con steps to reproduce
- [ ] Cero bugs de severidad **Urgent** sin ticket creado
- [ ] Los **8 flujos Cross-Módulo E2E** han sido ejecutados en su totalidad
- [ ] La columna **TICKET** de cada `Failed` tiene el ID del bug correspondiente
- [ ] Sign-off del QA Lead antes de aprobar el release

---

## 📝 Notas Técnicas Clave para QA

### Motor de ejecución refactorizado (IONF-379)
- El motor de flows fue refactorizado en su totalidad — buscar ejecuciones que se queden colgadas o que no avancen de nodo en nodo
- En modo **Development**: verificar que el WebSocket muestra el progreso nodo por nodo en tiempo real
- En modo **Production (Live)**: verificar que la ejecución completa en background y el resultado aparece en el historial

### Nodos con bugs corregidos — verificar que el fix es efectivo
- **Transformer/Mapper** (IONF-404, IONF-516): verificar que el nodo siempre emite output y no queda vacío
- **Transformer booleans** (IONF-416): verificar default cuando el campo boolean no tiene valor en el input
- **Iterator** (IONF-404): verificar que itera correctamente listas de enteros, no solo strings
- **Recursividad** (IONF-406): probar un flow que referencie otro flow en cadena — no debe colgarse
- **Preview del Transformer** (IONF-511): verificar que el preview de un nodo Transformer no muestra datos del nodo Transformer anterior que se inspeccionó

### Autenticación Keycloak (IONF-362, IONF-1074, IONF-165)
- El flujo SSO fue refactorizado — probar login desde cero en navegador sin sesión previa
- El refresh token automático fue corregido — probar acción después de período largo de inactividad (token expirado)
- Probar login en `staging-app.ionflow.io` desde distintos navegadores (Chrome, Firefox, Safari si es posible)

### Data Store / Persistent Data (IONF-159, IONF-162, IONF-163, IONF-552)
- El modal de creación tenía un bug de estado — verificar que al crear un segundo Data Store el modal no pre-llena datos del anterior
- Verificar que los 8 nodos están disponibles: Save, Update, Get, Delete, Check, Count, Delete All, Search
- Verificar aislamiento entre companies: datos de company A no deben ser visibles en company B

### Git / Versionamiento (IONF-419, IONF-482)
- Es una feature completamente nueva — dedicar tiempo extra a este módulo
- Probar todos los escenarios: Create Separate Draft, Create From Existing, Create From Saved State, Change Draft, Save, Discard Changes, History
- El "Discard Changes" debe restaurar el flow exactamente al último estado guardado

### ION PDF (IONF-820)
- Feature nueva integrada al canvas — verificar que el nodo aparece en el panel de nodos
- Verificar el ciclo completo: crear template → agregar al canvas como nodo → mapear campos → ejecutar flow → verificar PDF generado

---

## 🔗 Recursos

| Recurso | Detalle |
|---------|---------|
| **Ambiente** | `staging-app.ionflow.io` |
| **Branch** | `v0.1.0` |
| **Matriz de pruebas** | `knowledge/releases/v0.1.0/regression-matrix.csv` |
| **Documento de contexto** | `knowledge/releases/v0.1.0/regression-matrix.md` |
| **Tickets de release** | `matched_tickets1.csv` (182 tickets) |
| **Skill de regresión** | `skills/release/regression-matrix.md` |

---

*Generado por ionflow-qa-catalyst — skill: release/regression-matrix*
*Fecha: 2026-06-25 | Versión: v0.1.0*
