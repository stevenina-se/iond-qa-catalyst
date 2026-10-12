# Template de Rechazo — 86e1y463z

Estimado @Jose Enrique Ricaldi Juchani

**El resultado de pruebas para este ticket es: RECHAZADO ❌**

**Ticket**: 86e1y463z — Absorción y Unificación de NOVASPHERE en Gateway e Ionflow
**Módulo**: developer-apps (Marketplace) — Stores, Apps, Pricing, Plans Studio, Billing, Webcomponents
**QA Engineer**: Steve Nina
**Fecha**: 2026-09-06

### Resumen de Testing
- Observaciones encontradas: 39 (OBS-01 a OBS-39)
- Severidad 🔴 Urgent: 17
- Severidad 🟡 High: 15
- Severidad 🔵 Normal: 0
- Severidad ⚪ Low: 7
- Preguntas abiertas: 8

### Code Review QA
> No realizado en este ciclo — testing exploratorio directo sobre el entorno desplegado.

---

### 📌 Observaciones

---

**🔴 OBS-01 - Urgent - Estado: Nuevo**
**Área / Flujo: Permisos — Teams / Marketplace Store**

**Descripción:**
El permiso **Invoices & Subscriptions** no persiste el valor "Read and Write". Adicionalmente existe un bug visual: al seleccionar "Read and Write" en el dropdown, inmediatamente revierte visualmente a "Read Only".

**Pasos de reproducción:**
1. Company Login > Sidebar: Settings > Teams > Seleccionar un equipo
2. Sección: Marketplace Store > Permiso: Invoices & Subscriptions
3. Dropdown: Seleccionar "Read and Write"
4. Button: "Save" / Guardar

**Resultado esperado:**
El permiso se guarda como "Read and Write" y persiste al recargar la página.

**Comportamiento actual:**
El dropdown revierte visualmente a "Read Only" inmediatamente después de seleccionar "Read and Write". Al guardar y recargar, el valor es "Read Only".

**Evidencia:**
- Pendiente de screenshot

---

**🔴 OBS-02 - Urgent - Estado: Nuevo**
**Área / Flujo: Permisos — Pricing**

**Descripción:**
Un usuario con permisos de solo lectura en pricing puede acceder a las opciones de creación de planes, pero la operación falla con error. Las opciones de creación deberían estar bloqueadas/ocultas según TENANT_PERMS.

**Pasos de reproducción:**
1. Company Login (usuario con rol `read pricing` solamente)
2. Sidebar: Apps > Pricing Plans
3. Button: "+Create" o equivalente de creación de plan

**Resultado esperado:**
Las opciones de creación están deshabilitadas o no visibles. Si se intenta, se muestra tooltip indicando la falta de permisos.

**Comportamiento actual:**
El usuario puede acceder a las opciones de creación, pero al intentar crear recibe un error. La UI no bloquea la acción previamente.

**Evidencia:**
- Pendiente de screenshot

---

**🟡 OBS-03 - High - Estado: Nuevo**
**Área / Flujo: UI — Vista de Apps / Tabla**

**Descripción:**
Los badges de **type** en la tabla de apps no coinciden en color con los iconos de los cards. Flow Apps: ambos morados (✅). Code Apps: card azul, badge en tabla verde (❌). App Connectors y Products and Forms: colores no coinciden. PDFs: correcto (✅).

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > App Stores
2. Ver la vista de cards de apps y comparar los iconos/colores por tipo
3. Cambiar a la vista de tabla
4. Comparar los colores de los badges de "type" con los iconos de los cards

**Resultado esperado:**
Los colores de los badges de tipo en la tabla son idénticos a los colores de los iconos en los cards para cada tipo de app.

**Comportamiento actual:**
Code Apps: card usa azul, badge en tabla usa verde. App Connectors: colores no coinciden. Products and Forms: colores no coinciden.

**Evidencia:**
- Pendiente de screenshot comparativo cards vs tabla

---

**🟡 OBS-04 - High - Estado: Nuevo**
**Área / Flujo: UI — Vista de Apps / Filtros**

**Descripción:**
Elementos desalineados visualmente y se muestran múltiples botones de borrado de filtros cuando debería haber solo uno.

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > App Stores
2. Aplicar varios filtros activos
3. Observar la zona de filtros y sus botones de limpieza

**Resultado esperado:**
Todos los elementos alineados visualmente con un único botón de borrado/limpieza de filtros.

**Comportamiento actual:**
Elementos desalineados y existen múltiples botones de borrado de filtros.

**Evidencia:**
- Pendiente de screenshot

---

**🟡 OBS-05 - High - Estado: Nuevo**
**Área / Flujo: UI — Features**

**Descripción:**
Si el nombre de una feature es demasiado largo, no existe un scroll horizontal para poder desplazar el contenido.

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > Pricing Plans > Seleccionar un pricing
2. Plans Studio > Agregar una feature con nombre muy largo (80+ caracteres)
3. Observar el comportamiento visual del contenedor

**Resultado esperado:**
Se habilita scroll horizontal para desplazar el contenido de features largas.

**Comportamiento actual:**
Desbordamiento visual o truncamiento no controlado sin opción de scroll.

**Evidencia:**
- Pendiente de screenshot

---

**🟡 OBS-06 - High - Estado: Nuevo**
**Área / Flujo: Webcomponent — Filtros**

**Descripción:**
Los filtros disponibles en el webcomponente usan nomenclatura incorrecta que no corresponde a la taxonomía actual.

**Pasos de reproducción:**
1. Acceder al webcomponente `<gt-pricing-table>` / App Store público
2. Observar los filtros de tipo de app disponibles

**Resultado esperado:**
Los filtros usan la nomenclatura actual: "Code Apps", "App Connectors", "Flow Apps", etc.

**Comportamiento actual:**
Los filtros muestran: "Legacy" (debería ser Code Apps), "Apps" (debería ser App Connectors), "Grapps" (debería ser Flow Apps). Los demás también requieren revisión.

**Evidencia:**
- Pendiente de screenshot

---

**🟡 OBS-07 - High - Estado: Nuevo**
**Área / Flujo: Apps — Code Apps**

**Descripción:**
Se permite habilitar un Code App que ya estaba previamente habilitado. Esto rompe con la lógica vista en Gateway Legacy.

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > Apps Catalog
2. Buscar un Code App que ya esté habilitado (status: Active/Enabled)
3. Intentar habilitarlo nuevamente

**Resultado esperado:**
No se permite habilitar una app que ya está habilitada. El botón de habilitar debería estar deshabilitado o no visible.

**Comportamiento actual:**
Se permite re-habilitar la app sin validación, rompiendo la lógica de Gateway Legacy.

**Evidencia:**
- Pendiente de screenshot

---

**🟡 OBS-08 - High - Estado: Nuevo**
**Área / Flujo: Apps — App Connectors**

**Descripción:**
Al crear/configurar un App Connector, se establece por defecto la categoría "Applications".

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > Apps Catalog
2. Crear o editar un App Connector
3. Observar el campo Category

**Resultado esperado:**
La categoría por defecto debería ser la apropiada para el tipo App Connector (no "Applications").

**Comportamiento actual:**
La categoría se establece por defecto como "Applications".

**Evidencia:**
- Pendiente de screenshot

---

**🟡 OBS-09 - High - Estado: Nuevo**
**Área / Flujo: Apps — Navegación y Edición**

**Descripción:**
Inconsistencia en la experiencia de navegación y edición entre tipos de app. Products and Forms y PDF Templates navegan directamente a configuración interna al hacer clic. Flow Apps y Code Apps no lo hacen. Además existen dos formas de editar: menú de acciones (modal) y clic sobre el nombre.

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > Apps Catalog
2. Hacer clic sobre el nombre de un Product and Form → navega a configuración interna
3. Hacer clic sobre el nombre de un PDF Template → navega a configuración interna
4. Hacer clic sobre el nombre de un Flow App → NO navega a configuración interna
5. Hacer clic sobre el nombre de un Code App → NO navega a configuración interna
6. Para Flow/Code Apps: usar menú de acciones (⋮) > Edit → abre modal

**Resultado esperado:**
Comportamiento de navegación y edición consistente para todos los tipos de app.

**Comportamiento actual:**
Products and Forms y PDFs navegan directo a la configuración. Flow Apps y Code Apps no. Existen dos formas de editar (modal vs navegación) sin consistencia entre tipos.

**Evidencia:**
- Pendiente de screenshot/grabación

---

**🟡 OBS-10 - High - Estado: Nuevo**
**Área / Flujo: Apps — Flow App Card**

**Descripción:**
La descripción dentro del card para la creación de apps de tipo Flow App hace referencia a "Gateway".

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > Apps Catalog
2. Button: "Create" o "+" > Seleccionar tipo: Flow App
3. Leer la descripción del card

**Resultado esperado:**
La descripción referencia al contexto actual del Marketplace, no a "Gateway".

**Comportamiento actual:**
La descripción menciona "Gateway" como contexto.

**Evidencia:**
- Pendiente de screenshot

---

**🔴 OBS-11 - Urgent - Estado: Nuevo**
**Área / Flujo: Apps — Code Apps / Configuración**

**Descripción:**
No se identifica cómo configurar los parámetros de canales legacy para Code Apps (autenticación, dynamic parameters). En la creación se muestra "Features", pero no queda clara la diferencia con "I. Features" de la vista principal.

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > Apps Catalog
2. Crear un nuevo Code App o editar uno existente
3. Buscar las opciones de configuración de: autenticación, dynamic parameters
4. Observar el campo "Features" en la creación vs "I. Features" en la vista principal

**Resultado esperado:**
Existen controles claros para configurar autenticación y dynamic parameters de canales legacy. Las secciones "Features" e "I. Features" tienen propósitos claramente diferenciados.

**Comportamiento actual:**
No se identifican controles para configurar autenticación ni dynamic parameters. La diferencia entre "Features" e "I. Features" no es clara.

**Evidencia:**
- Pendiente de screenshot

---

**🟡 OBS-12 - High - Estado: Nuevo**
**Área / Flujo: Apps — Edición de Flow App / Formulario**

**Descripción:**
Al editar una Flow App, en la sección "Name" aparece el campo **description**, y en la sección "Description" el contenido comienza desde **details**. En la creación, la descripción está correctamente en la sección "Description".

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > Apps Catalog
2. Crear un Flow App → observar que "Description" está en su sección correcta
3. Editar el mismo Flow App → sección "Name" contiene el campo description
4. Sección "Description" comienza desde details

**Resultado esperado:**
Los campos no se mezclan entre secciones. La organización es consistente entre creación y edición.

**Comportamiento actual:**
En modo edición, el campo description se encuentra en la sección "Name" y la sección "Description" comienza desde details, mezclando los campos entre secciones.

**Evidencia:**
- Pendiente de screenshot comparativo creación vs edición

---

**🔴 OBS-13 - Urgent - Estado: Nuevo**
**Área / Flujo: Apps — Products and Forms**

**Descripción:**
Se permite colocar un action button a cada elemento individual del formulario. El comportamiento debería ser único por formulario, no por elemento.

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > Apps Catalog
2. Seleccionar/editar un Product and Form
3. Configurar el formulario con múltiples elementos
4. Intentar asignar un action button a cada elemento individual

**Resultado esperado:**
Solo se permite un action button por formulario completo.

**Comportamiento actual:**
Se permite agregar un action button a cada elemento individual del formulario.

**Evidencia:**
- Pendiente de screenshot

---

**🟡 OBS-14 - High - Estado: Nuevo**
**Área / Flujo: Plans Studio — Ícono de Plan**

**Descripción:**
Dentro del Plans Studio, una vez asignado un ícono a un plan, no existe opción para eliminarlo/quitarlo.

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > Pricing Plans > Seleccionar un pricing
2. Plans Studio > Seleccionar un plan > Asignar un ícono
3. Intentar eliminar/quitar el ícono asignado

**Resultado esperado:**
Existe una opción (botón X, reset, etc.) para quitar el ícono del plan.

**Comportamiento actual:**
No existe opción para eliminar el ícono una vez asignado.

**Evidencia:**
- Pendiente de screenshot

---

**⚪ OBS-15 - Low - Estado: Nuevo**
**Área / Flujo: Plans Studio — Cards de Planes**

**Descripción:**
Los cards de planes no están alineados en la parte superior e inferior. Deben ser del mismo tamaño/altura para mantener armonía visual.

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > Pricing Plans > Seleccionar un pricing
2. Plans Studio > Observar los cards de planes con diferentes cantidades de features/contenido

**Resultado esperado:**
Todos los cards tienen la misma altura, alineados tanto arriba como abajo.

**Comportamiento actual:**
Los cards tienen alturas diferentes según su contenido, generando desalineación visual.

**Evidencia:**
- Pendiente de screenshot

---

**🔴 OBS-16 - Urgent - Estado: Nuevo**
**Área / Flujo: Plans Studio — Validación de Campos Numéricos**

**Descripción:**
Los campos numéricos de `amount` y `every` aceptan valores negativos. Se deben implementar validaciones (min ≥ 0).

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > Pricing Plans > Seleccionar un pricing
2. Plans Studio > Seleccionar un plan > Editar un precio
3. Campo "Amount": Ingresar valor -10
4. Campo "Every": Ingresar valor -5
5. Button: "Save" / Guardar

**Resultado esperado:**
Los campos no permiten valores negativos. Se muestra validación indicando que el valor mínimo es 0.

**Comportamiento actual:**
Los campos aceptan valores negativos sin ninguna validación.

**Evidencia:**
- Pendiente de screenshot

---

**⚪ OBS-17 - Low - Estado: Nuevo**
**Área / Flujo: Plans Studio — Modal de Confirmación**

**Descripción:**
Al finalizar la asignación de productos, el modal de confirmación se muestra excesivamente grande.

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > Pricing Plans > Seleccionar un pricing
2. Asignar productos al pricing
3. Confirmar la asignación → observar el modal de confirmación

**Resultado esperado:**
El modal tiene un tamaño apropiado para su contenido.

**Comportamiento actual:**
El modal se ve demasiado grande, desproporcionado respecto a su contenido.

**Evidencia:**
- Pendiente de screenshot

---

**⚪ OBS-18 - Low - Estado: Nuevo**
**Área / Flujo: Pricing Plans — Carga de Planes**

**Descripción:**
Al ingresar a un pricing plan, mientras cargan los planes la vista sugiere que no existen planes disponibles. Falta un skeleton/loader.

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > Pricing Plans
2. Seleccionar un pricing plan que tenga planes configurados
3. Observar la vista durante la carga (antes de que se muestren los planes)

**Resultado esperado:**
Se muestra un skeleton/loader indicando que la carga está en progreso.

**Comportamiento actual:**
Mientras cargan, la vista muestra el estado "vacío" (sin planes), sugiriendo erróneamente que no existen planes.

**Evidencia:**
- Pendiente de screenshot

---

**⚪ OBS-19 - Low - Estado: Nuevo**
**Área / Flujo: Pricing Plans — Modal Vacío**

**Descripción:**
Cuando el modal de pricing está vacío, el botón "+Create a new pricing" se encuentra "flotando" sin posición visualmente coherente.

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > Pricing Plans
2. Abrir el modal de pricing cuando no hay pricings creados
3. Observar la posición del botón "+Create a new pricing"

**Resultado esperado:**
El botón tiene una posición centrada o claramente anclada visualmente.

**Comportamiento actual:**
El botón se encuentra "flotando" dentro del modal vacío sin posición coherente.

**Evidencia:**
- Pendiente de screenshot

---

**🟡 OBS-20 - High - Estado: Nuevo**
**Área / Flujo: Apps — Categorías**

**Descripción:**
Para las categorías de las apps, ¿se debería usar el motor de categorías existente en la plataforma en lugar de categorías hardcoded?

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > Apps Catalog
2. Crear/editar una app > Observar el campo de categorías
3. Verificar si las categorías son dinámicas (motor) o estáticas (hardcoded)

**Resultado esperado:**
Las categorías se gestionan mediante el motor de categorías de la plataforma, permitiendo CRUD dinámico.

**Comportamiento actual:**
Las categorías parecen ser estáticas/hardcoded. No se utiliza el motor de categorías existente.

**Evidencia:**
- Pendiente de verificación

---

**🔴 OBS-21 - Urgent - Estado: Nuevo**
**Área / Flujo: App Stores — Preview vs Webcomponent**

**Descripción:**
El preview de la app dentro de la vista de App Stores > App es significativamente diferente a la experiencia real expuesta en los webcomponents.

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > App Stores > Seleccionar un store
2. Seleccionar una app > Observar el preview de la app
3. Acceder al webcomponente `<gt-pricing-table>` correspondiente
4. Comparar ambas vistas

**Resultado esperado:**
El preview es una representación fiel del webcomponente real.

**Comportamiento actual:**
El preview difiere significativamente del webcomponente en layout, estilos y/o contenido.

**Evidencia:**
- Pendiente de screenshot comparativo

---

**🔴 OBS-22 - Urgent - Estado: Nuevo**
**Área / Flujo: Pricing — Creación de Price**

**Descripción:**
Al crear un pricing con el botón `+`, se disparan **dos requests**, y un precio se queda vacío en Stripe. Dentro del Studio también se lanzan dos requests.

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > Pricing Plans > Seleccionar un pricing
2. Plans Studio > Button: "+" (crear nuevo precio/tier)
3. Observar en DevTools (Network tab) los requests disparados
4. Verificar en Stripe Dashboard que se crearon dos precios (uno vacío)

**Resultado esperado:**
Se dispara un único request y se crea un único precio en Stripe.

**Comportamiento actual:**
Se disparan dos requests. Un precio se crea correctamente y otro se queda vacío en Stripe.

**Evidencia:**
- Pendiente de screenshot (DevTools Network + Stripe Dashboard)

---

**🔴 OBS-23 - Urgent - Estado: Nuevo**
**Área / Flujo: Pricing — Sincronización con Stripe**

**Descripción:**
Cuando se elimina un plan directamente en Stripe e intenta manipularse desde Ionflow, se obtiene un error 500. No hay sincronización ni manejo graceful del estado divergente.

**Pasos de reproducción:**
1. Stripe Dashboard > Productos > Eliminar/archivar un plan existente
2. Company Login > Sidebar: Apps > Pricing Plans > Seleccionar el pricing afectado
3. Plans Studio > Intentar editar o manipular el plan eliminado en Stripe

**Resultado esperado:**
El sistema detecta que el plan fue eliminado en Stripe y muestra un mensaje descriptivo, o sincroniza el estado.

**Comportamiento actual:**
Error 500 sin mensaje descriptivo.

**Evidencia:**
- Pendiente de screenshot (error 500 + Stripe Dashboard)

---

**🔴 OBS-24 - Urgent - Estado: Nuevo**
**Área / Flujo: Pricing — Activación sin Stripe Configurado**

**Descripción:**
Inconsistencia de estado al activar planes sin cuenta Stripe configurada. Al iniciar onboarding el status cambia a Active. Al desactivar y querer reactivar, vuelve a pedir configurar la cuenta.

**Pasos de reproducción:**
1. Company Login > Crear un pricing sin configurar cuenta de Stripe
2. Intentar activar un plan → mensaje: "Configure Stripe account first"
3. Iniciar onboarding de Stripe (PayoutsCard > Start payouts)
4. Observar que el status de los planes cambia a "Active" automáticamente
5. Desactivar un plan
6. Intentar reactivar el plan → mensaje: "Finish configuring your account"

**Resultado esperado:**
Comportamiento consistente: si el onboarding está incompleto, el estado no debería cambiar a Active. Si ya cambió, no debería bloquearse la reactivación.

**Comportamiento actual:**
Inconsistencia: el onboarding (incompleto) activa los planes, pero luego bloquea la reactivación con mensaje de "terminar de configurar".

**Evidencia:**
- Pendiente de screenshot del flujo completo

---

**🔴 OBS-25 - Urgent - Estado: Nuevo**
**Área / Flujo: Stripe Connect — Cuentas Duplicadas**

**Descripción:**
Al hacer doble clic rápido en "Start payouts" en PayoutsCard, se pueden crear cuentas Connect duplicadas para la misma company. El `create` en Stripe está fuera de la transacción.

**Pasos de reproducción:**
1. Company Login > PayoutsCard > Button: "Start payouts" (doble clic rápido)
2. Verificar en Stripe Dashboard > Connect > Accounts: buscar la company
3. Alternativa: Forzar fallo de BD (e.g. `company_id` ya existe en `stripe_connect_accounts`) y reintentar

**Resultado esperado:**
Solo se crea una cuenta Connect por company. El botón se deshabilita al primer clic o hay protección contra duplicados.

**Comportamiento actual:**
Se crean múltiples cuentas Connect para la misma company en Stripe.

**Evidencia:**
- Pendiente de screenshot (Stripe Dashboard con cuentas duplicadas)

---

**🔴 OBS-26 - Urgent - Estado: Nuevo**
**Área / Flujo: Plans Studio — Atomicidad del Guardar**

**Descripción:**
El `prices-bulk` queda persistido en Stripe aunque el `PUT` del plan falle. La operación de guardar no es atómica.

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > Pricing Plans > Seleccionar un pricing
2. Plans Studio > Añadir un tier nuevo
3. Cambiar el título del plan a 141+ caracteres (superar la validación del backend)
4. Button: "Save" / Guardar
5. Observar toast de error
6. Recargar la página
7. Verificar en Stripe Dashboard: los precios del tier se crearon

**Resultado esperado:**
Si el PUT del plan falla, los precios creados en Stripe se revierten (operación atómica).

**Comportamiento actual:**
Los precios se crean en Stripe exitosamente pero el plan no se guarda, dejando datos huérfanos en Stripe.

**Evidencia:**
- Pendiente de screenshot (toast de error + Stripe Dashboard con precios huérfanos)

---

**🔴 OBS-27 - Urgent - Estado: Nuevo**
**Área / Flujo: Stripe Connect — Onboarding**

**Descripción:**
La cuenta Connect siempre se crea con `country=US` y `email=null`, sin importar la ubicación real del seller.

**Pasos de reproducción:**
1. Company Login > PayoutsCard > Button: "Start payouts"
2. Observar el país preseleccionado en el formulario de onboarding de Stripe
3. API: `POST …/stripe-connect/onboarding`
4. Verificar: `GET /v1/accounts/{acct}` → `country=US`, `email=null`

**Resultado esperado:**
El país se pre-establece según la ubicación de la company. El email del seller se envía a Stripe.

**Comportamiento actual:**
`country=US` hardcoded y `email=null` en todas las cuentas Connect creadas.

**Evidencia:**
- Pendiente de screenshot (API response + Stripe Dashboard)

---

**⚪ OBS-28 - Low - Estado: Nuevo**
**Área / Flujo: Invoices — Campos no poblados**

**Descripción:**
Los campos `application_fee_amount` y `period_start` de la tabla `marketplace_invoices` no se llenan cuando se efectúa una compra.

**Pasos de reproducción:**
1. Buyer: Realizar una compra completa en el App Store via webcomponente
2. DBeaver: `SELECT application_fee_amount, period_start FROM marketplace_invoices WHERE ...`

**Resultado esperado:**
Los campos `application_fee_amount` y `period_start` están poblados con los valores correctos.

**Comportamiento actual:**
Los campos están vacíos/null después de la compra.

**Evidencia:**
- Pendiente de query de BD

---

**⚪ OBS-29 - Low - Estado: Nuevo**
**Área / Flujo: Subscriptions — Campo cancel_at_period_end**

**Descripción:**
No se identifica en qué momento el campo `cancel_at_period_end` de la tabla `marketplace_subscriptions` cambia a `true`.

**Pasos de reproducción:**
1. DBeaver: `SELECT cancel_at_period_end FROM marketplace_subscriptions WHERE ...`
2. Verificar en diferentes estados de suscripción (activa, cancelada, etc.)

**Resultado esperado:**
El campo cambia a `true` en un momento definido y documentado del ciclo de vida de la suscripción.

**Comportamiento actual:**
No se identifica cuándo ni cómo cambia el campo. Falta documentación del comportamiento esperado.

**Evidencia:**
- Pendiente de verificación

---

**🔴 OBS-30 - Urgent - Estado: Nuevo**
**Área / Flujo: Webcomponent — Skip Payment**

**Descripción:**
Mientras el webcomponente carga los precios, se puede hacer clic en "Free" y saltar Stripe completamente, evadiendo el cobro.

**Pasos de reproducción:**
1. Acceder al webcomponente `<gt-pricing-table>` de una app con pricing configurado
2. Mientras los precios están cargando (spinner/loading visible), hacer clic en el botón "Free"
3. Observar que se salta el checkout de Stripe

**Resultado esperado:**
El botón "Free" no está disponible mientras los precios cargan. O si la app tiene pricing, el botón "Free" no debería existir.

**Comportamiento actual:**
Se puede hacer clic en "Free" durante la carga y saltar Stripe completamente.

**Evidencia:**
- Pendiente de screenshot/grabación

---

**🔴 OBS-31 - Urgent - Estado: Nuevo**
**Área / Flujo: Webcomponent — Trial Badge**

**Descripción:**
Cuando se configura un trial desde el Studio, el badge de trial NO aparece en el webcomponente.

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > Pricing Plans > Plans Studio
2. Seleccionar un tier (e.g. "Week") > Trial days: 7 > Button: "Save"
3. Verificar que el preview muestra "7-day free trial"
4. Acceder al webcomponente `<gt-pricing-table>` correspondiente
5. Observar si aparece el badge de trial

**Resultado esperado:**
El webcomponente muestra el badge "7-day free trial" en el plan correspondiente.

**Comportamiento actual:**
El badge de trial NO aparece en el webcomponente, aunque sí aparece en el preview del Studio.

**Evidencia:**
- Pendiente de screenshot comparativo (Preview vs Webcomponent)

---

**🔴 OBS-32 - Urgent - Estado: Nuevo**
**Área / Flujo: Billing — Trial no aplica**

**Descripción:**
El trial configurado en Studio nunca aplica: el Embedded Checkout cobra el primer periodo completo.

**Pasos de reproducción:**
1. Company Login > Plans Studio > Tier "Week" > Trial days: 7 > Button: "Save"
2. Verificar preview: muestra "7-day free trial"
3. Webcomponente > Bucket: "Week" > Button: "Buy"
4. Pagar con tarjeta de prueba 4242 4242 4242 4242
5. Observar el total cobrado en el Embedded Checkout

**Resultado esperado:**
El Checkout muestra $0.00 para el primer periodo (trial de 7 días). El cobro se realiza después de los 7 días.

**Comportamiento actual:**
El Embedded Checkout cobra el monto completo del primer periodo, ignorando el trial configurado.

**Evidencia:**
- Pendiente de screenshot (Checkout mostrando cobro completo)

---

**🔴 OBS-33 - Urgent - Estado: Nuevo**
**Área / Flujo: Billing — Descuento del Primer Periodo**

**Descripción:**
El descuento del primer periodo se muestra en la UI pero no se aplica en el cobro. No se generan Coupons ni discounts en Stripe.

**Pasos de reproducción:**
1. Company Login > Plans Studio > Tier "Day" > First-period discount %: 50 > Button: "Save"
2. Verificar card: muestra "50% off the first period; then 20.00 after"
3. Webcomponente > CE muestra la misma leyenda
4. Button: "Buy" > Pagar con tarjeta de prueba
5. Observar el monto cobrado

**Resultado esperado:**
Se cobra el 50% del precio ($10.00 si el precio es $20.00) en el primer periodo. Se genera un Coupon o discount en Stripe.

**Comportamiento actual:**
Se cobra el monto completo ($20.00) sin aplicar el descuento. No se crean Coupons ni discounts en Stripe.

**Evidencia:**
- Pendiente de screenshot (Checkout + Stripe Dashboard sin coupon)

---

**🟡 OBS-34 - High - Estado: Nuevo**
**Área / Flujo: Webcomponent — Métodos de Pago**

**Descripción:**
El Checkout ofrece métodos de pago no restringidos (Link, Adaptive Pricing/BOB) sin restricción de métodos ni moneda de presentación.

**Pasos de reproducción:**
1. Webcomponente > Button: "Buy"
2. Observar los métodos de pago ofrecidos en el Embedded Checkout
3. Observar la moneda mostrada (BOB u otra adaptativa)
4. Intentar pagar con Link

**Resultado esperado:**
Los métodos de pago están restringidos según configuración. La moneda de presentación es la configurada para el seller.

**Comportamiento actual:**
Se ofrecen Link, wallets y monedas adaptativas (BOB) sin restricción.

**Evidencia:**
- Pendiente de screenshot (Checkout con métodos no restringidos)

---

**🔴 OBS-35 - Urgent - Estado: Nuevo**
**Área / Flujo: Invoices — Application Fee en Recurrentes**

**Descripción:**
El ledger local no guarda el application fee de facturas recurrentes ni de renovaciones. La columna "Platform fee" está vacía.

**Pasos de reproducción:**
1. Company Login (seller) > Sidebar: Apps > App Stores > Seleccionar store > Invoices
2. Observar la columna "Platform fee" en facturas recurrentes (no la primera factura)

**Resultado esperado:**
La columna "Platform fee" muestra el application fee calculado para cada factura recurrente.

**Comportamiento actual:**
La columna "Platform fee" está vacía en las facturas recurrentes.

**Evidencia:**
- Pendiente de screenshot

---

**🟡 OBS-36 - High - Estado: Nuevo**
**Área / Flujo: Pricing — Asignación de Precios**

**Descripción:**
Cuando se asignan prices desde la vista de prices, se da la opción de asignar a apps que ya cuentan con un pricing asignado.

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > Pricing Plans
2. Seleccionar un pricing > Vista de prices
3. Intentar asignar precios > Observar que aparecen apps que ya tienen pricing

**Resultado esperado:**
Solo se muestran apps que NO tienen pricing asignado, o se diferencia claramente cuáles ya tienen uno.

**Comportamiento actual:**
Se muestran todas las apps incluyendo las que ya tienen pricing asignado, sin diferenciación.

**Evidencia:**
- Pendiente de screenshot

---

**🔴 OBS-37 - Urgent - Estado: Nuevo**
**Área / Flujo: Sincronización BD ↔ Stripe — Drift de Catálogo**

**Descripción:**
La sincronización BD→Stripe es unidireccional. Cambios realizados desde el Dashboard del seller en Stripe no se reflejan en Ionflow, causando drift del catálogo.

**Pasos de reproducción:**
1. Stripe Dashboard (seller) > Product catalog:
   - Archivar el price del tier "Month"
   - Renombrar el producto
   - Crear un price nuevo en el producto
2. Company Login > Sidebar: Apps > Pricing Plans > Plans Studio
3. Observar que el tier "Month" sigue mostrándose como ACTIVE
4. Webcomponente: intentar comprar el tier "Month"

**Resultado esperado:**
Los cambios en Stripe se reflejan en Ionflow (sincronización bidireccional) o se muestra advertencia de drift.

**Comportamiento actual:**
El tier archivado en Stripe sigue ACTIVE en Studio y CE. Intentar comprarlo genera inconsistencias. No existe reconciliación Stripe→BD.

**Evidencia:**
- Pendiente de screenshot (Studio vs Stripe Dashboard)

---

**🟡 OBS-38 - High - Estado: Nuevo**
**Área / Flujo: Webcomponent — Badge Free**

**Descripción:**
En los webcomponents se muestra el badge "Free" en apps que ya tienen un pricing asignado.

**Pasos de reproducción:**
1. Acceder al webcomponente de App Store
2. Observar las apps que tienen pricing configurado
3. Verificar si muestran el badge "Free"

**Resultado esperado:**
Apps con pricing asignado NO muestran el badge "Free".

**Comportamiento actual:**
Apps con pricing asignado muestran el badge "Free".

**Evidencia:**
- Pendiente de screenshot

---

**🟡 OBS-39 - High - Estado: Nuevo**
**Área / Flujo: App Stores — App Inactiva**

**Descripción:**
Cuando se inactiva una app dentro de un App Store, los planes dejan de mostrarse. No está claro si este es el comportamiento esperado ni qué pasa con suscripciones activas.

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > App Stores > Seleccionar un store
2. Inactivar una app que tiene planes y suscripciones activas
3. Acceder al webcomponente > Verificar si la app y sus planes aparecen
4. Verificar estado de suscripciones activas de esa app

**Resultado esperado:**
Comportamiento definido: si la app se inactiva, ¿se mantienen las suscripciones existentes? ¿Los planes deberían ocultarse o mostrarse como no disponibles?

**Comportamiento actual:**
Los planes dejan de mostrarse. No hay claridad sobre el impacto en suscripciones activas.

**Evidencia:**
- Pendiente de verificación

---

### ❓ Preguntas Abiertas

> Las siguientes preguntas **no son observaciones** sino dudas de negocio y técnicas que requieren respuesta del equipo de desarrollo.

**Q-01**: ¿Al asignar un base price se debe aplicar a todos los planes/productos?

**Q-02**: ¿Por qué para los Code Apps no se muestran los planes de pricing?

**Q-03**: ¿Por qué para los App Connectors no se muestran los planes de pricing?

**Q-04**: ¿Cómo se mapean los formularios y sus botones para Products and Forms?

**Q-05**: ¿Qué pasa si se edita el precio directamente en Stripe? (Dado que la sincronización es unidireccional BD→Stripe)

**Q-06**: ¿Es correcto que cada clic en "Subscribe Now" cree un invoice en Ionflow?

**Q-07**: ¿Cómo se cancela una suscripción del marketplace? (Flujo buyer y seller)

**Q-08**: ¿Los reembolsos deben sincronizarse? ¿Se debe configurar el webhook para refunds? ¿Campos `disputed_at` y `refunded_at` se llenan desde Stripe? ¿Dónde se registra el renewal?

---

### Evidencia General
- Test Matrix: [test-matrix.md](file:///c:/Users/STEVE/Desktop/Automation/ionflow-qa-catalyst/knowledge/L3-tickets/86e1y463z/test-matrix.md)
- QA Report: Este documento
- AC Consolidados: [ac-consolidated.md](file:///c:/Users/STEVE/Desktop/Automation/ionflow-qa-catalyst/knowledge/L3-tickets/86e1y463z/ac-consolidated.md)
- Risk Triage: [risk-triage.md](file:///c:/Users/STEVE/Desktop/Automation/ionflow-qa-catalyst/knowledge/L3-tickets/86e1y463z/risk-triage.md)
- Test Plan: [test-plan.md](file:///c:/Users/STEVE/Desktop/Automation/ionflow-qa-catalyst/knowledge/L3-tickets/86e1y463z/test-plan.md)
- Screenshots de fallos: Pendientes

| Details | |
|---|---|
| BROWSER | Chrome |
| BRANCH | `IONF-1088` |
| ENV | dev-app.ionflow.io |
| TEST MATRIX | [test-matrix.md](file:///c:/Users/STEVE/Desktop/Automation/ionflow-qa-catalyst/knowledge/L3-tickets/86e1y463z/test-matrix.md) |
| CODE REVIEW | ⏭️ No realizado en este ciclo |
| MERGE REQUEST | PENDIENTE (observaciones encontradas) |
