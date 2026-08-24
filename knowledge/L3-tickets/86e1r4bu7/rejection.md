# Template de Rechazo — 86e1r4bu7

Estimado @Alex Chura

**El resultado de pruebas para este ticket es: RECHAZADO ❌**

**Ticket**: 86e1r4bu7 — [Ionflow] Crear boards de ejemplo documentados y publicarlos como templates editables
**Módulo**: Templates
**QA Engineer**: Steve Nina
**Fecha**: 2026-08-11
**Iteración**: Retest #3 (R3)

### Resumen de Testing
- Observaciones previas R1 (Mijael): 16 → Resueltas ✅
- Observaciones previas R2 (Steve): 12 → Resueltas ✅
- Observaciones nuevas R3: 3 (1 persistente de R2, 2 nuevas)
- Bugs totales (bloqueantes): 3

### Code Review QA
> Code review realizado y aprobado por @Enrique Vicente y @Rodolfo Merlo Ali.

- Repos revisados: gateway-ion (IONF-1076)
- Code review: ✅ Aprobado

---

### 📌 Observaciones

---

**🔴 OBS-R3-01 — Urgent — Estado: Nuevo**
**Área / Flujo: Tenant > Instalación Template > Configuración de Conexiones (Apps Globales)**

**Descripción:**
Cuando un board/template tiene más de una app global configurada, al intentar instalar el template y configurar las conexiones, el wizard presenta datos incorrectos. Al presionar la opción de añadir una nueva conexión para la primera app, el modal se abre correctamente con los datos correspondientes. Sin embargo, al intentar añadir una nueva conexión para la segunda app, el modal muestra los datos de la primera app en lugar de los datos de la app seleccionada.

**Pasos de reproducción:**

1. Prerequisito: template activo con más de una app global (ej. Google Gmail + Shopify QA-S)
2. Tenant Login > Templates > Seleccionar el template con múltiples apps globales
3. Click en "Use" / "Install"
4. En el paso de configuración de conexiones: click en "+" para la primera app (ej. Google Gmail) → se abre el modal de conexión con datos de Google Gmail ✅
5. Cerrar el modal sin completar
6. Click en "+" para la segunda app (ej. Shopify QA-S) → se abre el modal pero muestra los datos de Google Gmail ❌

**Resultado esperado:**
Al presionar "+" en cada app, el modal de configuración de conexión debe abrirse con los datos correspondientes a la app seleccionada. Cada app global del template debe abrir su propio formulario de autenticación/configuración.

**Comportamiento actual:**
El modal de nueva conexión siempre muestra los datos de la primera app global del template, independientemente de cuál app se esté intentando configurar. Esto impide configurar correctamente las conexiones para apps distintas a la primera.

**Evidencia:**
- Wizard de instalación con múltiples apps globales: al seleccionar "+" en la segunda app se cargan datos de la primera

---

**🟡 OBS-R3-02 — High — Estado: Nuevo**
**Área / Flujo: Admin > Companies > Paginación de tabla**

**Descripción:**
En la vista de Companies del panel de administración, al seleccionar el valor máximo de registros por página (48), el menú de paginación al pie de la tabla desaparece completamente, dejando al usuario sin controles de navegación entre páginas.

**Pasos de reproducción:**

1. Admin Login > Companies (o vista con listado de compañías)
2. Localizar el selector de registros por página
3. Seleccionar el valor máximo: 48
4. Observar el pie de la tabla donde debería estar el menú de paginación

**Resultado esperado:**
El menú de paginación debe permanecer visible y funcional al pie de la tabla independientemente de la cantidad de registros por página seleccionada. Incluso si todos los registros caben en una sola página, los controles de paginación (indicador de página actual, total de registros) deben estar presentes.

**Comportamiento actual:**
Al seleccionar 48 registros por página, el componente de paginación desaparece por completo del pie de la tabla, dejando al usuario sin forma de navegar ni de conocer la cantidad total de registros.

**Evidencia:**
- Selector de registros: 48 → menú de paginación desaparece del pie de tabla

---

**🔴 OBS-R3-03 — Urgent — Estado: Persistente (OBS-R2-07)**
**Área / Flujo: General > Nomenclatura — Mensaje de error de validación de template**

**Descripción:**
Persiste la observación OBS-R2-07 de la iteración anterior. El mensaje de error "could not identify template type a flow template must have 'nodes' and..." sigue utilizando la terminología obsoleta "flow template" en lugar de "board template". Esta observación fue reportada como resuelta en la iteración R2 pero el fix no se aplicó correctamente o se revirtió.

**Pasos de reproducción:**

1. Admin Login > Templates > Create template
2. Intentar crear un template con un board/JSON que no contenga nodos válidos
3. Observar el mensaje de error devuelto por el sistema

**Resultado esperado:**
El mensaje de error debe usar la nomenclatura actual del producto: "Could not identify template type. A **board** template must have 'nodes' and..." — reemplazando toda referencia a "flow" por "board" y "tenant" por "company", según lo establecido en OBS-R2-07.

**Comportamiento actual:**
El mensaje sigue mostrando: "could not identify template type a flow template must have 'nodes' and...", usando la terminología obsoleta "flow" que debió haber sido corregida en la iteración anterior.

**Evidencia:**
- Mensaje de error al crear template con JSON sin nodos: sigue usando "flow template"

---

### Evidencia General
- Test Matrix: L3-tickets/86e1r4bu7/test-matrix.md
- Code Review QA: L3-tickets/86e1r4bu7/code-review-qa.md
- Historial de rechazos: R1 (16 obs), R2 (12 obs), R3 (3 obs — actual)

| Details | |
|---|---|
| BROWSER | Chrome |
| BRANCH | IONF-1076 (merged to DEVELOPMENT) |
| ENV | dev-app.ionflow.io |
| TEST MATRIX | L3-tickets/86e1r4bu7/test-matrix.md |
| CODE REVIEW | ✅ Aprobado (Enrique Vicente + Rodolfo Merlo Ali) |
| MERGE REQUEST | https://github.com/altacrest/ion_gateway_ion/pull/34 |
