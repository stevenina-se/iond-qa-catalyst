# Template de Rechazo — 86e1y463z (Iteración 2)

Estimado @Jose Enrique Ricaldi Juchani

**El resultado de pruebas para este ticket es: RECHAZADO ❌**

**Ticket**: 86e1y463z — Absorción y Unificación de NOVASPHERE en Gateway e Ionflow
**Módulo**: developer-apps (Marketplace) — Stores, Apps, Pricing, Plans Studio, Billing, Webcomponents
**QA Engineer**: Steve Nina
**Fecha**: 2026-09-21
**Iteración**: 2

### Resumen de Testing
- Observaciones de Iteración 1: 40
- Observaciones resueltas: 22 (OBS-01, 03, 04, 06, 07, 09, 10, 14, 16, 18, 19, 24, 26, 27, 30, 31, 32, 35, 36, 37, 38, 39, 40)
- Observaciones persistentes: 9 (OBS-05, 08, 12, 15, 17, 20, 21, 23, 25)
- Observaciones parciales: 2 (OBS-02, 11)
- Observaciones por verificar / preguntas: 5 (OBS-13, 22, 28, 33, 34)
- Observaciones con nota de seguimiento: 2 (OBS-10, 37)
- Preguntas nuevas Iter 2: 4
- Preguntas heredadas Iter 1: 8
- Bugs del code review (nuevos): 4 (BUG-20, BUG-21, BUG-22, BUG-28)
- Observaciones nuevas Iter 2: 4 (EDGE-30, EDGE-31, EDGE-32, EDGE-33)
- Bugs totales (bloqueantes para merge): 15

### Code Review QA
> No realizado en este ciclo — re-test de observaciones de Iteración 1.

- Repos revisados: N/A (re-test funcional)
- Hallazgos: N/A
- TCs inyectados en la test matrix desde el code review: N/A
- Bugs del código que contribuyen al rechazo: N/A

---

### 📌 Observaciones Persistentes

---

**🔴 OBS-02 - Urgent - Estado: Persistente (parcial)**
**Área / Flujo: Permisos — Pricing / Plans Studio**

**Descripción:**
Con permisos de **Read Only** aún se despliega el modal de edición. El botón debería ser visible pero no clickeable. Al asignar price, al reordenar y al abrir el Studio sale error 403.

**Pasos de reproducción:**
1. Company Login (usuario con rol `read pricing` solamente) > Sidebar: Apps > Pricing Plans
2. Seleccionar un pricing > Plans Studio
3. Intentar editar un plan → se despliega modal de edición completo
4. Intentar asignar price → error 403
5. Intentar reordenar planes → error 403
6. Abrir Studio → error 403

**Resultado esperado:**
El botón de edición es visible pero deshabilitado (no clickeable) para usuarios Read Only. Las acciones de asignar price, reordenar y abrir Studio están bloqueadas visualmente sin disparar requests que retornen 403.

**Comportamiento actual:**
El modal de edición se despliega completo para usuarios Read Only. Al ejecutar acciones se reciben errores 403 en lugar de bloquear la interacción desde la UI.

**Evidencia:**
- Pendiente de screenshot

---

**🟡 OBS-05 - High - Estado: Persistente**
**Área / Flujo: UI — Features / Board Switching**

**Descripción:**
Cuando se cambia de board seleccionado, el subpanel de configuración de features persiste en pantalla y es confuso porque muestra la configuración del board anterior.

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > Pricing Plans > Seleccionar un pricing
2. Plans Studio > Seleccionar un board > Abrir configuración de features
3. Cambiar a otro board diferente
4. Observar que el subpanel de features sigue mostrando la configuración del board anterior

**Resultado esperado:**
Al cambiar de board seleccionado, el subpanel de configuración de features se cierra/resetea o se actualiza al contexto del nuevo board.

**Comportamiento actual:**
El subpanel de configuración de features persiste al cambiar de board, mostrando información del board anterior. Genera confusión al usuario.

**Evidencia:**
- Pendiente de screenshot

---

**🟡 OBS-08 - High - Estado: Persistente**
**Área / Flujo: Apps — App Connectors / Categorías**

**Descripción:**
Persiste la categoría **"Applications"** como valor por defecto de los App Connectors. ¿Se debe renombrar la columna a **"Tags"**?

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > Apps Catalog
2. Crear o editar un App Connector
3. Observar el campo Category → valor por defecto: "Applications"

**Resultado esperado:**
La categoría por defecto es apropiada para el tipo App Connector, o la columna se renombra a "Tags" según la taxonomía actualizada.

**Comportamiento actual:**
La categoría se establece por defecto como "Applications". No queda claro si la columna debería llamarse "Tags" en lugar de "Category".

**Evidencia:**
- Pendiente de screenshot

---

**🟡 OBS-11 - High - Estado: Persistente (parcial)**
**Área / Flujo: Apps — Code Apps / Configuración**

**Descripción:**
Resuelto parcialmente. Se requiere revisar y proponer mejoras a esta vista, enfocándose en tener lo necesario de la **v1.4.x**. La configuración de parámetros legacy para Code Apps aún no alcanza la paridad funcional esperada.

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > Apps Catalog
2. Crear un nuevo Code App o editar uno existente
3. Comparar las opciones de configuración disponibles con las de la v1.4.x
4. Verificar: autenticación, dynamic parameters, features vs I. Features

**Resultado esperado:**
La vista de configuración de Code Apps tiene al menos paridad funcional con la v1.4.x, incluyendo configuración de autenticación y dynamic parameters.

**Comportamiento actual:**
La vista fue parcialmente mejorada pero aún no alcanza la funcionalidad de la v1.4.x.

**Evidencia:**
- Pendiente de screenshot comparativo v1.4.x vs actual

---

**🟡 OBS-12 - High - Estado: Persistente**
**Área / Flujo: Apps — Edición de Flow App / Formulario**

**Descripción:**
Persiste la mezcla de campos entre secciones en modo edición. En la sección "Name" aparece el campo **description**, y en la sección "Description" el contenido comienza desde **details**.

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > Apps Catalog
2. Crear un Flow App → observar que "Description" está en su sección correcta ✅
3. Editar el mismo Flow App → sección "Name" contiene el campo description ❌
4. Sección "Description" comienza desde details ❌

**Resultado esperado:**
Los campos no se mezclan entre secciones. La organización es consistente entre creación y edición.

**Comportamiento actual:**
En modo edición, el campo description aparece en la sección "Name" y la sección "Description" comienza desde details.

**Evidencia:**
- Pendiente de screenshot comparativo creación vs edición

---

**⚪ OBS-15 - Low - Estado: Persistente**
**Área / Flujo: Webcomponent — Cards de Planes**

**Descripción:**
Persiste el problema de alineación de los cards de planes dentro del **webcomponent** `<gt-pricing-table>`. Los cards no están alineados en la parte superior e inferior.

**Pasos de reproducción:**
1. Acceder al webcomponente `<gt-pricing-table>` de una app con múltiples planes
2. Observar los cards de planes con diferentes cantidades de features/contenido
3. Comparar alturas y alineación

**Resultado esperado:**
Todos los cards tienen la misma altura, alineados tanto arriba como abajo.

**Comportamiento actual:**
Los cards tienen alturas diferentes según su contenido, generando desalineación visual en el webcomponent.

**Evidencia:**
- Pendiente de screenshot

---

**⚪ OBS-17 - Low - Estado: Persistente**
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

**🔴 OBS-20 - Urgent - Estado: Persistente**
**Área / Flujo: Apps — Categorías (múltiples vistas)**

**Descripción:**
Persiste en varias vistas: las categories dentro de la **vista de edición**, dentro del **preview**, y dentro del **webcomponent**. Las categorías siguen siendo estáticas/hardcoded en lugar de usar el motor de categorías de la plataforma.

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > Apps Catalog > Editar una app → observar categorías ❌
2. App Stores > Seleccionar store > Preview de una app → observar categorías ❌
3. Acceder al webcomponente `<gt-pricing-table>` → observar categorías ❌

**Resultado esperado:**
Las categorías se gestionan mediante el motor de categorías de la plataforma, consistentes en todas las vistas (edición, preview, webcomponent).

**Comportamiento actual:**
Las categorías son estáticas/hardcoded y aparecen de forma inconsistente en la vista de edición, en el preview y en el webcomponent.

**Evidencia:**
- Pendiente de screenshot comparativo de las 3 vistas

---

**🔴 OBS-21 - Urgent - Estado: Persistente**
**Área / Flujo: App Stores — Preview vs Webcomponent**

**Descripción:**
Persisten diferencias significativas entre el preview de la app dentro de App Stores y la experiencia real en el webcomponent. Las diferencias se encuentran en: el badge, la tabla, las apps con las que se conecta, y la sección de descripción.

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > App Stores > Seleccionar un store
2. Seleccionar una app > Observar el preview
3. Acceder al webcomponente correspondiente
4. Comparar: badge (diseño/colores), tabla (layout/datos), apps conectadas, sección de descripción

**Resultado esperado:**
El preview es una representación fiel del webcomponente real en todos los aspectos: badge, tabla, apps conectadas y descripción.

**Comportamiento actual:**
Diferencias en: badge (diseño/colores distintos), tabla (layout/datos diferentes), apps con las que se conecta (inconsistencia), sección de descripción (contenido/formato diferente).

**Evidencia:**
- Pendiente de screenshot comparativo Preview vs Webcomponent

---

**🔴 OBS-22 - Urgent - Estado: Persistente + Pregunta**
**Área / Flujo: Pricing — Eliminación de Plan / Evento**

**Descripción:**
Al eliminar un plan se emite el evento `plan.deleted` pero no ejecuta ninguna acción en Ionflow. ¿Es correcto este comportamiento? Adicionalmente, el error al intentar manipular el plan eliminado en Stripe aún continúa.

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > Pricing Plans > Plans Studio
2. Eliminar un plan
3. Verificar que se emite el evento `plan.deleted` (DevTools / logs)
4. Observar que Ionflow no reacciona al evento
5. Intentar manipular el plan eliminado → error persiste

**Resultado esperado:**
Al recibir el evento `plan.deleted`, Ionflow debe sincronizar el estado (eliminar/archivar el plan localmente). No debe haber error 500 al interactuar con planes eliminados.

**Comportamiento actual:**
El evento `plan.deleted` se emite pero Ionflow no ejecuta ninguna acción. El error al manipular el plan eliminado persiste.

**Evidencia:**
- Pendiente de screenshot (logs del evento + error)

---

**🔴 OBS-23 - Urgent - Estado: Persistente**
**Área / Flujo: Pricing — Activación con Stripe Connect**

**Descripción:**
Persiste el error: **"This cannot be activated until the connected account can accept charges"**. No se puede activar el plan cuando la cuenta Connect no está completamente configurada para aceptar cargos.

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > Pricing Plans > Seleccionar un pricing
2. Plans Studio > Intentar activar un plan
3. Observar el mensaje de error

**Resultado esperado:**
Si la cuenta Connect está parcialmente configurada, el mensaje debe ser descriptivo y guiar al usuario para completar la configuración. Si está completa, la activación debe funcionar sin error.

**Comportamiento actual:**
Error: "This cannot be activated until the connected account can accept charges". La activación falla sin orientación clara al usuario.

**Evidencia:**
- Pendiente de screenshot

---

**🔴 OBS-25 - Urgent - Estado: Persistente**
**Área / Flujo: Plans Studio — Validación de Título / Capitalizer**

**Descripción:**
Persiste el error de validación: **"title must be 140 characters or fewer capitalizer"**. El capitalizer interfiere con la validación de longitud del título.

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > Pricing Plans > Plans Studio
2. Seleccionar un plan > Editar el título
3. Ingresar un título cercano al límite de 140 caracteres
4. Button: "Save" / Guardar
5. Observar el error de validación

**Resultado esperado:**
El título se valida correctamente considerando la transformación del capitalizer. Si el título post-capitalizer excede 140 caracteres, el mensaje de error debe ser claro y descriptivo.

**Comportamiento actual:**
Error: "title must be 140 characters or fewer capitalizer". El mensaje es confuso y la validación no considera la transformación del capitalizer.

**Evidencia:**
- Pendiente de screenshot

---

**🔴 OBS-28 - Urgent - Estado: Persistente / Verificar**
**Área / Flujo: Invoices — Webhook y API**

**Descripción:**
Revisar el comportamiento con el webhook y por API. Al intentar sacar un token salió **error 500**.

**Pasos de reproducción:**
1. Verificar configuración del webhook para invoices
2. API: Intentar obtener un token → error 500
3. Verificar si los campos `application_fee_amount` y `period_start` se llenan correctamente vía webhook

**Resultado esperado:**
El token se obtiene correctamente por API. Los campos de invoices se llenan vía webhook sin errores.

**Comportamiento actual:**
Error 500 al intentar obtener un token por API. Comportamiento del webhook pendiente de verificación.

**Evidencia:**
- Pendiente de screenshot (error 500 + payload)

---

**🔴 OBS-29 - Urgent - Estado: Persistente**
**Área / Flujo: Webcomponent — Pricing Display**

**Descripción:**
En Pricing del webcomponent se muestra **"From $0.00/year"** cuando el precio annual es cero pero se tiene data del precio mensual. En algunos apps sale el precio mensual.

**Pasos de reproducción:**
1. Acceder al webcomponente `<gt-pricing-table>` de una app con pricing configurado
2. Verificar un app que tenga: precio annual = $0.00 y precio mensual con valor > $0
3. Observar qué precio se muestra en el card

**Resultado esperado:**
Cuando el annual es $0.00 pero existe un precio mensual, se debe mostrar el precio mensual como referencia (o definir regla de negocio clara).

**Comportamiento actual:**
Se muestra "From $0.00/year" ignorando el precio mensual configurado. En otros apps sí aparece el mensual, generando inconsistencia.

**Evidencia:**
- Pendiente de screenshot

---

### 📌 Bugs Detectados desde Code Review — Iteración 2

---

**🔴 BUG-12-1 - P0 - Estado: Nuevo**
**Área / Flujo: API — Borrar plan o tier con ventas**

**Descripción:**
Borrar un plan o un tier que ya tiene ventas (invoice lines o subscription items) responde 500 y deja el recurso archivado en Stripe mientras permanece activo en Ionflow.

**Precondiciones:**
- User Role: Admin (seller), logged in
- Cuenta Connect ACTIVE (charges_enabled y payouts_enabled en true; card_payments y transfers active)
- Tier con al menos una línea de invoice o de suscripción (un checkout abandonado alcanza)

**Pasos de reproducción:**
1. Abrir el Studio del plan
2. Borrar el tier con el botón de borrar por tier y hacer clic en Save
3. Verificar prices-bulk con 500
4. Verificar que el price quedó active=false en Stripe
5. Refrescar el Studio: el tier sigue ACTIVE
6. Intentar comprarlo desde el webcomponent
7. Repetir borrando el plan entero

**Resultado esperado:**
El borrado de algo con ventas se rechaza ANTES de tocar Stripe (409 o 422 claro) o se archiva en los dos lados de forma consistente.

**Comportamiento actual:**
Al intentar borrar un tier o plan con ventas, el sistema responde 500. El price se archiva en Stripe (active=false) pero en Ionflow el tier permanece ACTIVE, generando un estado inconsistente entre ambos sistemas. La operación de borrado en la base de datos falla por restricciones de integridad referencial (existen facturas o suscripciones vinculadas), pero la sincronización con Stripe ya se ejecutó antes del fallo (ver también BUG-12-3).

**Notas:**
Cada checkout abierto (aunque se abandone) crea un invoice open con su línea: basta abrir View as customer > Subscribe now para que ese tier ya no se pueda borrar.

---

**🔴 BUG-12-2 - P1 - Estado: Nuevo**
**Área / Flujo: API — Editar tier ACTIVE con cuenta sin poder vender**

**Descripción:**
Editar cualquier campo de un tier ACTIVE (monto, trial, descuento) con la cuenta Connect sin capacidad de vender da error 422 "cannot be activated".

**Precondiciones:**
- User Role: Admin (seller), logged in
- Cuenta Connect con charges_enabled=true y card_payments=active pero payouts_enabled=false (status RESTRICTED)
- Tier ACTIVE creado cuando la cuenta sí podía vender

**Pasos de reproducción:**
1. En el Studio cambiar solo el monto (o el trial o el % de descuento) de un tier ACTIVE
2. Hacer clic en Save
3. Verificar prices-bulk con 422 "this cannot be activated until the connected account can accept charges"
4. Probar enviando el mismo payload con status ACTIVE y luego sin status, comparar

**Resultado esperado:**
Editar sin pedir activar no se trata como una activación: el status no cambia o se informa el motivo real. Se espera también que se muestre un mensaje más explicativo y no haga referencias a temas técnicos al usuario.

**Comportamiento actual:**
Al guardar cualquier cambio en un tier ACTIVE, el sistema reenvía el status ACTIVE como parte del payload y lo interpreta como una solicitud de activación. Dado que la cuenta Connect no puede aceptar cobros, responde 422 "this cannot be activated until the connected account can accept charges" y revierte todos los cambios del prices-bulk.

**Notas:**
Sin status en el body el mismo tier se degrada en silencio a INACTIVE (ver BUG-26). El prefijo "update[0] id=N:" llega tal cual al toast (EDGE-25).

---

**🔴 BUG-12-3 - P1 - Estado: Nuevo**
**Área / Flujo: API — Mapeos de errores de BD del catálogo son código muerto**

**Descripción:**
Los mapeos 409/422 de errores de BD del catálogo son código muerto y todo sale como 500.

**Precondiciones:**
- User Role: Admin (seller), logged in

**Pasos de reproducción:**
1. Ejecutar DELETE de plan con ventas y verificar 500 en vez de 422
2. Revisar en el log de binaries "[internal error] cause: … violates foreign key constraint"
3. Buscar en el log cualquier "duplicated key not allowed" de rutas del catálogo

**Resultado esperado:**
23503 → 422; 23505 → 409; 23514 → 422 con mensaje claro.

**Comportamiento actual:**
Las validaciones de errores de base de datos (foreign key, duplicated key, check constraint) nunca se ejecutan porque el driver traduce los errores a un formato diferente al que las funciones de mapeo esperan. Como resultado, todos los errores de integridad de BD se devuelven como 500 genérico en lugar de los códigos 409/422 con mensajes claros que deberían mostrarse al usuario.

**Notas:**
22001 y 23502 no se traducen y sí se mapean: por eso sí aparece "a field is longer than the column allows".

---

**🟡 BUG-12-4 P2 - Estado: Nuevo**
**Área / Flujo: UI/UX — Columnas de fecha de facturación vacías**

**Descripción:**
Todas las columnas de fecha de facturación salen vacías (Issued, Started, Current period end).

**Precondiciones:**
- User Role: Admin (seller), logged in
- Facturas y suscripciones existentes

**Pasos de reproducción:**
1. Abrir Accounting > Invoices y revisar la columna Issued
2. Abrir Subscriptions y revisar Started y Current period end
3. Abrir las líneas de una factura
4. En la consola verificar el warning de vue-i18n "Not found short key in en locale datetime formats"

**Resultado esperado:**
Fechas visibles con formato corto.

**Comportamiento actual:**
Las columnas de fecha aparecen completamente vacías. En la consola del navegador se observa el warning "Not found short key in en locale datetime formats". El sistema intenta formatear las fechas con un formato nombrado ('short') que no está definido en la configuración de internacionalización, por lo que devuelve cadena vacía.

**Notas:**
Fix mínimo: definir datetimeFormats.short en la configuración de i18n o usar Intl.DateTimeFormat directo.

---

**🟡 BUG-12-5 - High - Estado: Nuevo**
**Área / Flujo: Pricing Studio — Moneda congelada a USD**

**Descripción:**
En la vista del Pricing Studio se había acordado congelar la moneda a USD; sin embargo, actualmente aún es posible cambiarla.

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > Pricing Plans > Plans Studio
2. Seleccionar un pricing o crear uno nuevo
3. Observar el selector de moneda → aún es editable

**Resultado esperado:**
El selector de moneda está deshabilitado/fijado en USD según lo acordado.

**Comportamiento actual:**
El selector de moneda sigue siendo editable y permite cambiar a otra moneda.

---

**🔴 BUG-12-6 - Urgent - Estado: Nuevo**
**Área / Flujo: Webcomponent — Switch Price sin confirmación de checkout**

**Descripción:**
Dentro del webcomponente, en un base price de un storefront, al hacer switch price no se tiene ningún modal de alerta que confirme el checkout. Se espera que lo tenga.

**Pasos de reproducción:**
1. Acceder al webcomponente del storefront
2. En un base price, hacer clic en switch price
3. Observar que el checkout se inicia directamente sin confirmación

**Resultado esperado:**
Al hacer switch price se muestra un modal de confirmación antes de iniciar el proceso de checkout.

**Comportamiento actual:**
El switch de precio procede directamente al checkout sin ningún modal de alerta o confirmación.

---

**🟡 EBUG-12-7 - High - Estado: Nuevo (relacionado con OBS-37)**
**Área / Flujo: Apps — Alerta de inactivación incorrecta**

**Descripción:**
Dentro de la vista de apps del storefront, al querer inactivar una app se muestra la alerta: *"Set 'Woocommerce' to inactive? It will disappear from this list, and there is no way to turn it back on from here."* — lo cual no es correcto, ya que sí es posible volver a reactivarla.

**Pasos de reproducción:**
1. Company Login > Sidebar: Apps > App Stores > Seleccionar un store
2. Seleccionar una app activa > Intentar inactivarla
3. Leer el mensaje del modal de confirmación

**Resultado esperado:**
El mensaje de confirmación refleja correctamente que la app puede ser reactivada posteriormente (por ejemplo: *"Set 'Woocommerce' to inactive? It will disappear from this list. You can reactivate it later from the Apps Catalog."*).

**Comportamiento actual:**
El mensaje dice *"there is no way to turn it back on from here"*, lo cual es incorrecto y genera confusión al usuario.

---

**🔴 BUG-12-8 - Urgent - Estado: Nuevo**
**Área / Flujo: Webcomponent / API — Marcador de Current Plan no se actualiza al cambiar plan**

**Descripción:**
Al realizar el cambio de planes vía API o mediante el webcomponente, el marcador de "current plan" no cambia visualmente y provoca errores 422.

**Preguntas asociadas (vinculadas a NQ-04):**
- ¿Al cambiar el plan se hace el checkout del nuevo plan con prorrateo?
- ¿Se registra como invoice?

**Pasos de reproducción:**
1. Acceder al webcomponente de pricing o usar la API para cambiar de plan
2. Completar el flujo de cambio de plan
3. Observar que el marcador de "current plan" sigue en el plan anterior
4. Intentar interactuar con el plan → error 422

**Resultado esperado:**
Al cambiar de plan, el marcador de "current plan" se actualiza visualmente al nuevo plan de inmediato. El flujo de prorrateo y facturación es consistente.

**Comportamiento actual:**
El marcador de "current plan" no se actualiza visualmente. Al intentar interactuar se obtienen errores 422.

---

### 📌 Observaciones por Verificar / Preguntar

---

**❓ OBS-13 - Verificar — Estado: Pendiente**
**Área / Flujo: Apps — Products and Forms / Action Button**

**Acción requerida:**
Verificar **a dónde se envía la acción** y **los datos del formulario**. Es más una pregunta al desarrollador que una observación: ¿cuál es el endpoint destino del action button y qué payload envía?

---

**❓ OBS-33 - Preguntar — Estado: Pendiente**
**Área / Flujo: Billing — Descuento del Primer Periodo**

**Acción requerida:**
Preguntar a **Beatriz** sobre el comportamiento esperado del descuento del primer periodo y su implementación con Stripe Coupons.

---

**❓ OBS-34 - Preguntar — Estado: Pendiente**
**Área / Flujo: Invoices — Campo Issued**

**Acción requerida:**
Preguntar al equipo de desarrollo **cómo se llena el campo ISSUED** en las facturas del marketplace.

---

### 📌 Observaciones Resueltas con Nota de Seguimiento

---

**✅ OBS-10 - Resuelta (con seguimiento)**
**Área / Flujo: Apps — Flow App Card / Labels**

> Resuelta, pero **se debe crear otro ticket** para modificar los demás labels que aún referencian nomenclatura antigua.

---

**✅ OBS-37 - Resuelta (con observación en copy)**
**Área / Flujo: Sincronización BD ↔ Stripe — Drift de Catálogo**

> Resuelta, pero la alerta de inactivación sugiere algo erróneo:
> *"Set 'Omniorders' to inactive? It will disappear from this list, and there is no way to turn it back on from here."*
> El mensaje implica que no hay forma de reactivar la app. Revisar el copy del mensaje de confirmación.

---

### ❓ Preguntas Nuevas — Iteración 2

> Las siguientes preguntas surgieron durante el re-test de la Iteración 2.

**NQ-01**: ¿Cómo se pobla el **CLAIMED AT**, **CLAIMED BINDING** y **CLAIMED ID**? ¿Qué acción del usuario o del sistema dispara el llenado de estos campos?

**NQ-02**: Cuando **no se configura un form**, ¿es posible hacer **varias compras** de un Product and Form? ¿Cuál es el comportamiento esperado sin formulario?

**NQ-03**: Verificar **cómo se llena el campo ISSUED** en las facturas del marketplace. ¿Es un proceso automático vía webhook o se genera al crear la factura localmente?

**NQ-04**: ¿Cómo hacemos el **upgrade de plan**? ¿Existe un flujo de upgrade/downgrade implementado? ¿Se maneja proration en Stripe?

---

### ❓ Preguntas Abiertas — Heredadas de Iteración 1

> Las siguientes preguntas se mantienen abiertas de la iteración anterior.

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
- QA Report Iteración 1: [qa-report.md](file:///c:/Users/STEVE/Desktop/Automation/ionflow-qa-catalyst/knowledge/L3-tickets/86e1y463z/qa-report.md)
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
| ITERACIÓN | 2 de N |
| MERGE REQUEST | PENDIENTE (observaciones persistentes) |
