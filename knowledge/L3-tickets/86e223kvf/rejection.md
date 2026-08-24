# Template de Rechazo — 86e223kvf

Estimado @enrique

**El resultado de pruebas para este ticket es: RECHAZADO ❌**

---

### 📌 Observaciones

---

**🔴 OBS-01 - Urgent - Estado: Nuevo**
**Área / Flujo: Boards — Clonación (Concurrencia de clicks)**

**Descripción:**
Al presionar el icono de clonar board, es posible presionar múltiples veces el botón mientras la petición se está ejecutando, generando múltiples requests al backend y potencialmente clones duplicados.

**Pasos de reproducción:**

1. Company Login > Sidebar: Boards > Seleccionar cualquier board
2. Presionar el icono de clonar board
3. Inmediatamente presionar nuevamente antes de que finalice la petición
4. DevTools > Network: observar múltiples requests de clonación enviados

**Resultado esperado:**
El botón de clonar debe deshabilitarse al primer click y mostrar una animación de "loading" mientras la petición se ejecuta. Solo un request debe enviarse al backend.

**Comportamiento actual:**
El botón permanece activo durante la ejecución de la petición. Múltiples clicks generan múltiples requests simultáneos de clonación.

**Evidencia:**
- DevTools: múltiples requests de clonación al presionar rápidamente

---

**🟡 OBS-02 - High - Estado: Nuevo**
**Área / Flujo: Toast System — Contraste insuficiente en Dark Mode (Generalizado)**

**Descripción:**
Los toasts de éxito y error en modo oscuro no contrastan adecuadamente con el tema de la plataforma. Este problema es generalizado y afecta a todos los toasts del sistema (clonación, edición, eliminación, exportación, etc.). Adicionalmente, el botón de cerrar el toast por estándar debe estar ubicado en la esquina superior derecha. Cada toast debe reflejar el icono y status correspondiente a la acción realizada.

**Pasos de reproducción:**

1. Company Login > Activar modo oscuro
2. Realizar cualquier acción que dispare un toast (clonar board, editar, eliminar, etc.)
3. Observar el contraste del toast con el fondo oscuro
4. Forzar un error y verificar el contraste del toast de error
5. Verificar la posición del botón de cerrar

**Resultado esperado:**
- En dark mode: los colores del toast (éxito y error) deben contrastar claramente con el tema oscuro de la plataforma
- El botón de cerrar el toast debe estar en la esquina superior derecha (estándar)
- Cada toast debe incluir icono, status y mensaje corto acorde a la acción

**Comportamiento actual:**
En dark mode el contraste de los toasts es insuficiente tanto para éxito como para error. El botón de cerrar no está en la posición estándar.

**Evidencia:**
- Verificar visualmente en dark mode con distintas acciones (clonar, editar, eliminar, exportar)

---

**🔴 OBS-03 - Urgent - Estado: Nuevo**
**Área / Flujo: Boards — Edición de Flow (Sobreescritura de posiciones de nodos)**

**Descripción:**
Al editar un flow mediante la opción "Edit Flow", las posiciones visuales de los nodos se sobreescriben. La posición visual de los nodos no debe verse afectada al realizar cambios editoriales en el flow.

**Pasos de reproducción:**

1. Company Login > Sidebar: Boards > Abrir un board con nodos posicionados manualmente en el canvas
2. Recordar las posiciones actuales de los nodos
3. Editar el flow mediante la opción "Edit Flow"
4. Realizar cualquier cambio editorial y guardar
5. Observar que las posiciones de los nodos han cambiado respecto a su ubicación original

**Resultado esperado:**
Las posiciones visuales de los nodos en el canvas deben mantenerse intactas tras una edición editorial del flow. Solo los datos editados deben cambiar.

**Comportamiento actual:**
Al guardar la edición del flow, las posiciones de los nodos se sobreescriben, perdiendo la disposición visual que el usuario había configurado.

**Evidencia:**
- Comparar posiciones de nodos antes y después de editar

---

**🔴 OBS-04 - Urgent - Estado: Nuevo**
**Área / Flujo: Boards — Filtro de búsqueda borra filtro activo**

**Descripción:**
En la vista de Boards, al tener un filtro de status activo (ej. "Active") y luego escribir un término de búsqueda, el request al backend se envía SIN el filtro de status, pero el chip visual sigue mostrando "Active". Resultados sin filtrar bajo un chip que indica lo contrario. También afecta PDF Templates con filtro de usage. 

**Pasos de reproducción:**

1. Company Login > Sidebar: Boards
2. Fijar filtro status=Active y verificar en DevTools que el request incluye `status=ACTIVE`
3. Escribir un término de búsqueda y presionar Enter
4. Inspeccionar el request en DevTools: el parámetro `status` desaparece
5. Observar que el chip visual sigue mostrando "Active"
6. Repetir en PDF Templates con filtro de usage
7. Probar in use y luego buscar

**Resultado esperado:**
La búsqueda debe respetar el filtro activo. Ambos parámetros (status + search) deben viajar juntos en el request.

**Comportamiento actual:**
`useListQuerySync` ejecuta `apply()` en cada búsqueda y borra el parámetro del filtro porque su `filterQuery` interno nunca se actualiza. Resultados sin filtrar bajo un chip que indica lo contrario.

**Evidencia:**


**🔴 OBS-05 - Urgent - Estado: Nuevo**
**Área / Flujo: Integrations — Eliminar conexión muestra toast de error**

**Descripción:**
Al eliminar una conexión exitosamente en Integrations, se muestra un toast de error en vez de éxito. el usuario ve un toast rojo "Cannot read properties of null" en un delete exitoso. 

**Pasos de reproducción:**

1. Company Login > Sidebar: Integrations
2. Seleccionar cualquier conexión y eliminar
3. Confirmar la eliminación en el dialog
4. Observar el toast: muestra error rojo ❌
5. Refrescar la página y verificar que la conexión sí se eliminó ✅

**Resultado esperado:**
Toast de éxito nombrando la conexión eliminada.

**Comportamiento actual:**
ConfirmDialog cierra y anula `deleteTarget` mientras el `await` sigue en vuelo. `deleteTarget.value.name` lanza TypeError. El usuario ve toast de error en una operación exitosa.

**Evidencia:**


---

**🔴 OBS-06 - Urgent - Estado: Nuevo**
**Área / Flujo: DataTable — Paginación no resincroniza al resetear filtros **

**Descripción:**
Al cambiar filtros, orden o búsqueda en las DataTables, el `pageIndex` interno nunca se resetea cuando el padre pone `params.page=1`. El footer y la navegación quedan desincronizados. Afecta 6+ tablas.

**Pasos de reproducción:**

1. Company Login > Sidebar: Execution History (o cualquier tabla con 40+ registros)
2. Navegar a la página 3
3. Aplicar un filtro (ej. status=failed)
4. Observar que el footer sigue diciendo "21 to 30" y Prev habilitado aunque el server devolvió página 1
5. Hacer clic en Next
6. Observar el salto directo a la página 4 del server (se saltan la 2 y 3)

**Resultado esperado:**
Al cambiar filtros, la tabla vuelve visualmente a página 1 y Next lleva a la 2.

**Comportamiento actual:**
El `pageIndex` interno del DataTable nunca se resetea. Footer y navegación desincronizados en 6+ tablas.

**Evidencia:**

---

**🔴 OBS-07 - Urgent - Estado: Nuevo**
**Área / Flujo: Data Store — Paginación clavada en StoreViewer**

**Descripción:**
En el visor de un Data Store con 30+ registros.

**Pasos de reproducción:**

1. Company Login > Sidebar: Data Store > Abrir un store con 30+ registros
2. Hacer clic en Next
3. Observar que carga la página 2 pero el footer vuelve a "1 to 10"
4. Hacer clic en Next otra vez
5. Observar que vuelve a pedir la página 2 permanentemente
6. Notar el flash del estado vacío ("No data") en cada cambio

**Resultado esperado:**
Navegación normal entre todas las páginas sin flash de "No data".

**Comportamiento actual:**
Imposible pasar de la página 2. Flash de estado vacío en cada cambio de página.

**Evidencia:**

---

**🔴 OBS-08 - Urgent - Estado: Nuevo**
**Área / Flujo: Global Search — localStorage sin guard puede dejar en blanco todo el tenant**

**Descripción:**


**Pasos de reproducción:**

1. Setear manualmente `recent_searches_tenant` con JSON truncado (ej. `[{`)
2. Refrescar cualquier ruta del tenant
3. Observar la página en blanco (GlobalSearch revienta en setup → TenantTopbar → TenantLayout)
4. Con storage lleno (Safari privado): hacer clic en un resultado y observar que la navegación no ocurre
5. Setear el valor a `{}` y guardar una búsqueda

**Resultado esperado:**
La búsqueda degrada con gracia: recientes vacíos y navegación intacta.

**Comportamiento actual:**
Cualquier corrupción de localStorage o storage lleno rompe la feature del buscador.

**Evidencia:**

---

**🟡 OBS-10 - High - Estado: Nuevo**
**Área / Flujo: Global — Mensajes de toast y títulos de modales**

**Descripción:**
Se identificaron múltiples oportunidades de mejora en los mensajes de los toasts y títulos de modales de confirmación a lo largo de la plataforma. Los mensajes actuales no siempre reflejan correctamente la acción realizada o no son lo suficientemente descriptivos. Las siguientes son **sugerencias** que se pueden consultar con **Marcel** para definir los textos específicos finales.

**Hallazgos:**

**A) Toast de edición de board con mensaje incorrecto:**
- Al editar un board exitosamente, el toast indica que el board "se creó" en vez de que "se actualizó".
- Sugerencia: "Board updated successfully"

**B) Falta toast de éxito/error al exportar flow:**
- Al exportar un flow con el icono de exportar, no se muestra ningún toast de feedback.
- Sugerencias: "Board exported successfully" / "Failed to export board, please try again."

**C) Toast de clonación de board:**
- El toast tras la clonación no refleja adecuadamente la acción.
- Sugerencias: "Board cloned successfully" / "Failed to clone board. Please try again"

**D) Toast de eliminación de board:**
- El mensaje del toast al eliminar no refleja correctamente la acción.
- Sugerencias: "Board deleted successfully" / "Failed to delete board. Please try again."

**E) Títulos de modales de eliminación:**
- El título del modal de confirmación de eliminación no es descriptivo por entidad.
- Sugerencias por entidad:
  - Boards: "Delete Board"
  - Templates: "Delete Template"
  - Connections: "Delete Connection"
  - Connectors: "Delete Connector"
  - Accounts: "Delete Account"

**Pasos de reproducción:**

1. Company Login > Sidebar: Boards > Editar un board y guardar → observar toast incorrecto
2. Exportar un flow → observar ausencia de toast
3. Clonar un board → observar mensaje del toast
4. Eliminar un board → observar mensaje del toast y título del modal
5. Repetir eliminación en Templates, Connections, Connectors, Accounts → observar títulos

**Resultado esperado:**
Mensajes de toast claros, concisos y acorde a la acción realizada. Títulos de modales descriptivos por entidad. Textos finales a definir con Marcel (PO).

**Comportamiento actual:**
Mensajes genéricos, incorrectos (ej. "creado" en vez de "actualizado") o ausentes. Títulos de modales de eliminación no se adaptan a la entidad.

**Evidencia:**
- Verificar visualmente en cada flujo mencionado

---

**🟡 OBS-11 - High - Estado: Nuevo**
**Área / Flujo: Boards — Edición de título no trimea espacios**

**Descripción:**
Al editar el título de un board con espacios al inicio y/o al final del nombre, estos espacios se conservan al guardar.

**Pasos de reproducción:**

1. Company Login > Sidebar: Boards
2. Seleccionar un board > Editar
3. Cambiar el título a "   Mi Board   " (con espacios al inicio y final)
4. Guardar
5. Observar que el nombre guardado conserva los espacios

**Resultado esperado:**
Los espacios al inicio y al final del nombre deben eliminarse automáticamente al guardar (trim).

**Comportamiento actual:**
Los espacios en blanco al inicio y final se conservan en el nombre del board.

**Evidencia:**
- Verificar el nombre guardado con espacios

---

**🟡 OBS-15 - High - Estado: Nuevo**
**Área / Flujo: DataTable — Ancho mínimo de columnas roto por interacción con resize**

**Descripción:**
El ancho de las columnas puede reducirse más allá de su mínimo permitido cuando se interactúa con el resize de las demás columnas. La columna "Actions" puede romper el layout completo.

**Pasos de reproducción:**

1. Company Login > Cualquier vista con DataTable
2. Usar el resize de columnas para reducir una columna
3. Luego interactuar con el resize de otras columnas
4. Observar que algunas columnas se reducen por debajo de su ancho mínimo, perdiendo su label
5. Notar que la columna "Actions" puede romper el layout

**Resultado esperado:**
Las columnas deben respetar su ancho mínimo posible sin perder su label, independientemente de la interacción con el resize de otras columnas.

**Comportamiento actual:**
Es posible reducir columnas por debajo del mínimo cuando se interactúa con el resize de otras columnas. Las cabeceras pierden su label.

**Evidencia:**
- Verificar visualmente reduciendo columnas con resize

---

**🟡 OBS-16 - High - Estado: Nuevo**
**Área / Flujo: DataTable — Filtro de fecha con contraste insuficiente**

**Descripción:**
En el filtro de "Pick Date", cuando se selecciona un rango de fechas, la selección visual no contrasta lo suficiente para ser fácilmente distinguible.

**Pasos de reproducción:**

1. Company Login > Cualquier vista con filtro de fecha (ej. Execution History)
2. Abrir el date picker y seleccionar un rango de fechas
3. Observar el contraste visual de la selección

**Resultado esperado:**
La selección del rango de fechas debe contrastar visiblemente con el fondo del date picker para ser fácilmente identificable.

**Comportamiento actual:**
El contraste de la selección del rango de fechas es insuficiente.

**Evidencia:**
- Verificar visualmente el contraste del date picker

---

**🟡 OBS-17 - High - Estado: Nuevo**
**Área / Flujo: PDF Templates — Download template incluye campo innecesario**

**Descripción:**
Al usar la opción de "Download Template", el documento generado incluye un campo "template" que no debería estar presente.

**Pasos de reproducción:**

1. Company Login > Sidebar: PDF Templates
2. Seleccionar un template y usar la opción "Download Template"
3. Abrir el documento generado
4. Observar que contiene un campo "template"

**Resultado esperado:**
El documento descargado no debe incluir el campo "template".

**Comportamiento actual:**
El documento descargado incluye el campo "template" de forma innecesaria.

**Evidencia:**
- Inspeccionar el archivo descargado

---

**🟡 OBS-18 - High - Estado: Nuevo**
**Área / Flujo: Data Store — Tooltips persistentes al abrir modales**

**Descripción:**
Cuando se abren los modales de edición, eliminación o inspección de datos en Data Store, los tooltips de la tabla permanecen visibles por encima del modal.

**Pasos de reproducción:**

1. Company Login > Sidebar: Data Store
2. Hover sobre un elemento que muestre tooltip
3. Inmediatamente abrir un modal (editar, eliminar o inspeccionar)
4. Observar que el tooltip permanece visible sobre el modal

**Resultado esperado:**
Los tooltips deben cerrarse automáticamente al abrir cualquier modal.

**Comportamiento actual:**
Los tooltips persisten visualmente sobre los modales abiertos.

**Evidencia:**
- Verificar visualmente la persistencia de tooltips

---

**🟡 OBS-19 - High - Estado: Nuevo**
**Área / Flujo: Data Store — Mensaje incoherente en dropdown sin resultados**

**Descripción:**
Dentro de la edición de un Data Store, en el dropdown de "Data Structure", al buscar un data structure inexistente aparece el mensaje "No executions match your search or filters", que es incoherente con el contexto. Esto ocurre en todos los campos dropdown que tienen buscador.

**Pasos de reproducción:**

1. Company Login > Sidebar: Data Store > Editar un Data Store
2. En el dropdown de "Data Structure", buscar un nombre inexistente
3. Observar el mensaje "No executions match your search or filters"
4. Repetir en otros dropdowns con buscador

**Resultado esperado:**
El mensaje debe ser acorde al contexto del dropdown. Ej: "No data structures match your search".

**Comportamiento actual:**
Todos los dropdowns con buscador muestran "No executions match your search or filters" independientemente del contexto.

**Evidencia:**
- Verificar visualmente el mensaje en distintos dropdowns

---

**🔵 OBS-20 - Normal - Estado: Nuevo**
**Área / Flujo: Credentials — Formato de fecha inconsistente**

**Descripción:**
El formato de fecha en la tabla de credentials es diferente al formato usado en otras vistas como boards.

**Pasos de reproducción:**

1. Company Login > Sidebar: Credentials > Observar formato de fechas
2. Navegar a Boards > Observar formato de fechas
3. Comparar ambos formatos

**Resultado esperado:**
El formato de fecha debe ser uniforme en todas las tablas de la plataforma.

**Comportamiento actual:**
Las fechas en credentials tienen un formato diferente al resto de las vistas.

**Evidencia:**
- Comparar formatos entre vistas

---

**🔵 OBS-21 - Normal - Estado: Nuevo**
**Área / Flujo: Credentials — Labels redundantes en modales**

**Descripción:**
En el modal de creación de credenciales: (1) Step 1: el label "Enter your API Key" es redundante y no aporta valor. (2) Step 2: el label "Model" aparece duplicado. Nota: al editar, el label "Leave empty to keep current key" en el Step 1 es correcto y debe mantenerse.

**Pasos de reproducción:**

1. Company Login > Sidebar: Credentials > Crear nueva credencial
2. Step 1: observar el label "Enter your API Key" debajo del campo
3. Step 2: observar la duplicación del label "Model"
4. Abrir modal de edición y verificar que "Leave empty to keep current key" se mantiene

**Resultado esperado:**
- Step 1 (creación): eliminar label redundante "Enter your API Key"
- Step 2: eliminar uno de los labels "Model" duplicados
- Step 1 (edición): mantener "Leave empty to keep current key"

**Comportamiento actual:**
Labels redundantes en ambos steps del modal de creación.

**Evidencia:**
- Verificar visualmente ambos steps

---

**🔵 OBS-22 - Normal - Estado: Nuevo**
**Área / Flujo: Credentials — Modal de creación muestra datos cacheados**

**Descripción:**
Si previamente se editó una credencial (key), al abrir el modal de creación de una nueva key, el nombre y el proveedor aparecen pre-llenados con los datos de la edición anterior (cache).

**Pasos de reproducción:**

1. Company Login > Sidebar: Credentials
2. Editar una key existente (modificar nombre/proveedor y guardar)
3. Cerrar el modal de edición
4. Abrir el modal de creación de una nueva key
5. Observar que el nombre y proveedor están pre-llenados con los datos de la key editada

**Resultado esperado:**
El modal de creación debe abrir siempre con todos los campos vacíos/limpios.

**Comportamiento actual:**
Los datos de la última edición persisten en cache y se muestran en el modal de creación.

**Evidencia:**
- Reproducir la secuencia editar > crear

---

**🔵 OBS-23 - Normal - Estado: Nuevo**
**Área / Flujo: DataTable — Clear Filters genera doble request**

**Descripción:**
Al utilizar el botón "Clear Filters" cuando no existen coincidencias con los filtros aplicados, se realizan dos peticiones al backend. La última petición no trae datos. Este comportamiento se replica en todas las tablas donde no se encuentran coincidencias con los filtros.

**Pasos de reproducción:**

1. Company Login > Cualquier vista con DataTable
2. Aplicar filtros que no devuelvan coincidencias
3. DevTools > Network tab
4. Presionar "Clear Filters"
5. Observar que se disparan 2 requests al backend
6. La segunda petición retorna sin datos

**Resultado esperado:**
Solo un request al backend al limpiar los filtros.

**Comportamiento actual:**
Se disparan dos requests. La segunda petición no trae datos.

**Evidencia:**
- DevTools: 2 requests al presionar "Clear Filters"

---

**🔵 OBS-24 - Normal - Estado: Nuevo**
**Área / Flujo: Webhooks — Paginación inconsistente con filtros del frontend**

**Descripción:**
En la vista de webhooks, al filtrar por "delivery enabled" y luego buscar una palabra, el filtro parece aplicarse en el frontend (no hace peticiones al backend). Al jugar con la paginación se muestran inconsistencias: a veces muestra 2 resultados, luego 4, luego 3.

**Pasos de reproducción:**

1. Company Login > Sidebar: Webhooks
2. Filtrar por "delivery enabled"
3. Buscar una palabra que tenga coincidencias
4. Observar que inicialmente muestra un resultado (sin petición al backend)
5. Navegar entre páginas
6. Observar inconsistencias: varía entre 2, 3 y 4 resultados por página

**Resultado esperado:**
La paginación debe ser consistente. Si el filtro es frontend, la paginación también debe serlo. Los resultados deben ser estables al navegar entre páginas.

**Comportamiento actual:**
Mezcla de filtrado frontend con paginación backend. Resultados inconsistentes al navegar entre páginas.

**Evidencia:**
- DevTools: verificar si los requests van al backend o se filtran en frontend

---

**🟡 OBS-25 - High - Estado: Nuevo**
**Área / Flujo: i18n — Traducciones perdidas en sidebar y headings**

**Descripción:**
8 labels del sidebar perdieron la traducción a español. Los siguientes elementos se muestran en inglés cuando el idioma está configurado en español: Dashboard, Boards, Templates, Execution History, Persistent Data, Connections, Webhooks y App Connectors. Los breadcrumbs heredan el mismo problema. Adicionalmente, en la búsqueda global (Ctrl+K), los headings de grupo "Boards" y "App Connectors" permanecen en inglés mientras los demás sí se traducen, generando mezcla de idiomas.

Para las traducciones que no estén claramente definidas se puede consultar con **Marcel** para definir los textos específicos en cada idioma.

**Pasos de reproducción:**

1. Cambiar el idioma a español
2. Revisar el sidebar: Dashboard, Boards, Templates, Execution History, Persistent Data, Connections, Webhooks, App Connectors → en inglés ❌
3. Verificar que los breadcrumbs heredan el mismo texto en inglés
4. Abrir Ctrl+K y buscar un término → observar headings "Boards" y "App Connectors" en inglés mientras otros se traducen

**Resultado esperado:**
Todas las entradas del menú, breadcrumbs y headings de la búsqueda global se muestran en español cuando el locale es español.

**Comportamiento actual:**
- Sidebar: 8 labels se muestran en inglés independientemente del idioma seleccionado.
- Global Search: dos headings de grupo permanecen en inglés generando secciones en idiomas mezclados.

**Evidencia:**
- Verificar visualmente cambiando el idioma a español en sidebar y búsqueda global

---

**🔵 OBS-26 - Normal - Estado: Nuevo**
**Área / Flujo: Sidebar — Traducciones i18n pendientes y elementos a ocultar**

**Descripción:**
En el side menu faltan traducciones i18n para: "Plantillas", "Historial de Ejecución", "Persistent Data" (sin traducción definida). Además, se deben ocultar por ahora "Novedades" y "Acerca de IOND" hasta definir su comportamiento. Para las traducciones que no estén claramente definidas, consultar con **Marcel (PO)** para confirmar los textos correctos.

**Pasos de reproducción:**

1. Company Login > Cambiar idioma a español
2. Verificar sidebar: "Plantillas", "Historial de Ejecución", "Persistent Data"
3. Buscar opciones "Novedades" y "Acerca de IOND"

**Resultado esperado:**
- Traducciones correctas para todas las opciones del menú (consultar con Marcel/PO para confirmar)
- "Novedades" y "Acerca de IOND" ocultos hasta definición

**Comportamiento actual:**
Algunas traducciones faltan o son incorrectas. "Novedades" y "Acerca de IOND" visibles sin funcionalidad definida.

**Evidencia:**
- Verificar visualmente en español

---

**🔵 OBS-28 - Normal - Estado: Nuevo**
**Área / Flujo: Perfil — Hover en menú de usuario en dark mode + layout responsivo**

**Descripción:**
(1) En las opciones del menú del perfil en modo oscuro, el hover no contrasta suficiente con el tema oscuro. (2) En la vista de edición del perfil, falta espacio entre el botón "Actualizar información de contacto" y el fin de página. (3) El campo de email debe estar bloqueado a edición (puede causar problemas con Keycloak). (4) En pantallas pequeñas, el campo de edición de imagen se sobrepone sobre los demás inputs.

**Pasos de reproducción:**

1. Company Login > Dark mode > Abrir menú de perfil > Observar hover
2. Navegar a vista de edición de perfil > Scroll al final > Observar espacio con botón
3. Verificar si el campo de email es editable
4. Reducir el tamaño de la ventana y verificar el campo de imagen

**Resultado esperado:**
- Hover con contraste visible en dark mode
- Espacio suficiente entre botón de actualizar y fin de página
- Campo de email bloqueado a edición
- En pantallas pequeñas, el campo de imagen no se sobrepone a los inputs

**Comportamiento actual:**
- Hover insuficiente en dark mode
- Sin separación adecuada al final de la vista
- Campo de email editable
- Sobreposición de imagen en pantallas pequeñas

**Evidencia:**
- Verificar visualmente en dark mode y responsive

---

**🔵 OBS-29 - Normal - Estado: Nuevo**
**Área / Flujo: DataTable — Cabecera puede perder su label con resize**

**Descripción:**
En las tablas, es posible achicar una cabecera hasta que se pierda su label utilizando el resize.

**Pasos de reproducción:**

1. Company Login > Cualquier vista con DataTable
2. Utilizar el resize de columnas para reducir el ancho de una columna
3. Continuar reduciendo hasta que el label de la cabecera desaparezca

**Resultado esperado:**
No debe ser posible reducir la cabecera hasta que su label se pierda. Debe existir un ancho mínimo que preserve el label.

**Comportamiento actual:**
Se puede reducir la columna hasta que el label desaparezca por completo.

**Evidencia:**
- Verificar visualmente reduciendo columnas

---

**🔵 OBS-30 - Normal - Estado: Nuevo**
**Área / Flujo: Settings — Separación entre imagen y botón de actualizar**

**Descripción:**
En la vista de configuración falta separación entre el campo de imagen y el botón de actualizar.

**Pasos de reproducción:**

1. Company Login > Sidebar: Settings > Observar la separación entre imagen y botón

**Resultado esperado:**
Separación adecuada entre el campo de imagen y el botón de actualizar.

**Comportamiento actual:**
Sin separación visual adecuada.

**Evidencia:**
- Verificar visualmente

---

**🔵 OBS-31 - Normal - Estado: Nuevo**
**Área / Flujo: Navegación — Renombrar "Actividad" a "Notificaciones"**

**Descripción:**
Según lo acordado en reunión, la sección "Actividad" debe renombrarse a "Notificaciones" y añadirse al menú desplegable del usuario. Además, se necesita diferenciación visual entre elementos leídos y no leídos, y acciones por elemento individual (marcar como leída).

**Pasos de reproducción:**

1. Company Login > Verificar la sección "Actividad" en el sidebar
2. Verificar el menú desplegable del usuario
3. Observar que no hay diferencia visual entre leídos y no leídos
4. Verificar que no existe opción de marcar como leída individualmente

**Resultado esperado:**
- Sección renombrada a "Notificaciones"
- Incluida en el menú desplegable del usuario
- Diferencia visual entre leídos (fondo ligeramente distinto) y no leídos
- Botón/icono para "Marcar como leída" en cada elemento individual

**Comportamiento actual:**
- Se llama "Actividad"
- No está en el menú desplegable del usuario
- Sin diferencia visual entre leídos y no leídos
- Sin opción de marcar como leída individualmente

**Evidencia:**
- Verificar visualmente

---

**🟡 OBS-32 - High - Estado: Nuevo**
**Área / Flujo: Boards Canvas — Flow Pilot z-index vs menú de usuario**

**Descripción:**
Dentro del canvas de boards, si se abre el Flow Pilot y se hace clic sobre el menú del perfil de usuario, el menú del perfil queda por debajo del chat del Flow Pilot.

**Pasos de reproducción:**

1. Company Login > Sidebar: Boards > Abrir un board en el canvas
2. Abrir el Flow Pilot (chat)
3. Hacer clic en el menú del perfil de usuario (icono en la topbar)
4. Observar que el menú del perfil queda por debajo del Flow Pilot

**Resultado esperado:**
El menú del perfil de usuario debe estar por encima de cualquier otro elemento, incluyendo el Flow Pilot.

**Comportamiento actual:**
El menú del perfil queda por debajo del chat del Flow Pilot debido a un conflicto de z-index.

**Evidencia:**
- Verificar visualmente abriendo Flow Pilot + menú de usuario

---

**🟡 OBS-33 - High - Estado: Nuevo**
**Área / Flujo: DataTable — Buscadores de tablas sin debounce**

**Descripción:**
Los buscadores implementados en cada tabla envían peticiones al backend con cada tecla presionada. Se espera que funcionen similar al buscador global: sin enviar peticiones mientras se escribe, y con búsqueda automática tras finalizar de escribir (debounce), sin necesidad de presionar Enter.

**Pasos de reproducción:**

1. Company Login > Cualquier vista con DataTable que tenga buscador
2. DevTools > Network tab
3. Comenzar a escribir un término de búsqueda
4. Observar que se dispara una petición por cada tecla

**Resultado esperado:**
Los buscadores de tablas deben implementar debounce: no enviar peticiones mientras se escribe, y buscar automáticamente al terminar de escribir (similar al buscador global con ~600ms de debounce).

**Comportamiento actual:**
Se envía una petición al backend por cada carácter tecleado, generando peticiones innecesarias.

**Evidencia:**
- DevTools: múltiples requests por cada carácter

---

**🟡 OBS-34 - High - Estado: Nuevo**
**Área / Flujo: Global Search — Skeleton de carga, contraste y subrayado de coincidencias**

**Descripción:**
(1) El skeleton de carga del modal de búsqueda global no contrasta bien en modo oscuro ni en modo claro. (2) Falta el subrayado de las letras que coinciden con la búsqueda (ej. buscar "temp" debería subrayar "temp" en "Board_template"). (3) Verificar si la búsqueda incluye PDF templates como antes; si sí, restablecer esa funcionalidad.

**Pasos de reproducción:**

1. Company Login > Abrir Ctrl+K (búsqueda global)
2. Escribir un término y observar el skeleton de carga
3. En dark mode: observar que el skeleton no contrasta con el fondo
4. En light mode: observar que el skeleton contrasta muy poco
5. Observar los resultados: verificar si las letras coincidentes están subrayadas
6. Buscar un término que coincida con un PDF template

**Resultado esperado:**
- Skeleton de carga con contraste adecuado en ambos modos (light/dark)
- Letras coincidentes con la búsqueda resaltadas/subrayadas en los resultados
- Resultados de PDF templates incluidos si estaban disponibles previamente

**Comportamiento actual:**
- Skeleton sin contraste adecuado en dark mode y contraste muy tenue en light mode
- Sin subrayado/resaltado de coincidencias en los resultados
- PDF templates posiblemente excluidos de los resultados

**Evidencia:**
- Verificar visualmente en ambos modos

---

**🟡 OBS-35 - High - Estado: Nuevo (Code Review)**
**Área / Flujo: Global Search — Errores espurios al borrar texto + input pisado (BUG-14, BUG-15)**

**Descripción:**
Al borrar el texto del buscador global con requests en vuelo, se disparan toasts de error espurios sin que nada haya fallado. El input pisa lo tecleado cuando llegan respuestas del servidor. Al escribir "invoice" + pausar 600ms + continuar escribiendo "-sync", cuando llega la respuesta el input vuelve a "invoice" y se pierde "-sync".

**Pasos de reproducción:**

1. Company Login > Abrir Ctrl+K
2. BUG-14: Escribir un término, esperar a que arranquen los requests, seleccionar todo y borrar → esperar ~600ms → toast rojo sin motivo
3. BUG-15: Escribir "invoice", pausar 600ms (disparan requests), continuar escribiendo "-sync" → cuando llega respuesta el input vuelve a "invoice"

**Resultado esperado:**
- Abortar la búsqueda al vaciar el input no produce ningún error
- El texto tecleado nunca se pierde por respuestas asíncronas

**Comportamiento actual:**
- Toast de error espurio al borrar texto
- El `:value` renderiza `searchText` (600ms atrás por debounce) y el re-render por datos async reescribe el DOM

**Evidencia:**

---

**🟡 OBS-36 - High - Estado: Nuevo**
**Área / Flujo: Breadcrumbs — Rotos o sin traducir en múltiples rutas**

**Descripción:**
Se identificaron dos problemas de breadcrumbs:

**Problema 1 — Breadcrumbs no se traducen:**
Las siguientes rutas muestran sus breadcrumbs siempre en inglés, incluso cuando el idioma está configurado en español:
- `/settings` → muestra "Settings"
- `/profile` → muestra "Profile"
- `/activity` → muestra "Activity"
- `/support` → muestra "Contact support"

**Problema 2 — Breadcrumbs ausentes o incorrectos:**
Las siguientes rutas no muestran su nombre en el breadcrumb, solo aparece "Dashboard" sin identificar la página actual:
- `/users` → solo muestra "Dashboard"
- `/teams` → solo muestra "Dashboard"
- `/billing/plans` → solo muestra "Dashboard"
- `/billing/subscription` → solo muestra "Dashboard"
- `/connections/create` → último crumb es "App Connectors" (padre) no clickeable
- `/connections/{id}/auth` → breadcrumb muestra padre sin link de regreso
- `/connections/{id}/webhook` → breadcrumb muestra padre sin link de regreso
- `/connections/{id}/module/{id}` → breadcrumb muestra padre sin link de regreso

**Pasos de reproducción:**

1. Configurar idioma en español
2. Navegar a /settings, /profile, /activity, /support → observar breadcrumbs en inglés
3. Navegar a /users, /teams, /billing/plans, /billing/subscription → observar que solo dice "Dashboard"
4. Navegar a /connections/create → observar último crumb "App Connectors" sin link

**Resultado esperado:**
Cada ruta muestra su propio nombre en el breadcrumb y permite volver al padre. Con locale español, todos los breadcrumbs deben mostrarse en español.

**Comportamiento actual:**
- 4 rutas muestran breadcrumbs en inglés independientemente del idioma
- 8 rutas no muestran su nombre en el breadcrumb o muestran el padre sin link

**Evidencia:**
- Verificar visualmente navegando a cada ruta listada

---

**⚪ OBS-38 - Low - Estado: Nuevo**
**Área / Flujo: Support — Vista SupportView crea tickets falsos**

**Descripción:**
`SupportView` crea tickets con ID fabricado (ION-{random}) sin llamar a ningún servicio. El `submit()` solo espera 900ms y fabrica un ID aleatorio. Se debe ocultar esta vista por ahora hasta tener la integración con un servicio real de soporte.

**Pasos de reproducción:**

1. Navegar a /support desde el menú
2. Completar el formulario y enviar
3. Observar mensaje "Ticket ION-#### created"
4. Verificar en backend/logs que no se envió nada

**Resultado esperado:**
La vista no debe estar publicada hasta tener integración real. Ocultar por ahora.

**Comportamiento actual:**
Submit() fabrica un ID falso. El usuario cree que pidió soporte pero nadie lo recibirá.

**Evidencia:**
- Repo: gateway-ion | Commit: 3066ab7f
- Archivos: `src/views/tenant/support/SupportView.vue:38-45`, `src/router/tenant.ts:147-155`

---

### ❓ Preguntas abiertas para el Developer

| # | Pregunta | Urgencia | Observación relacionada |
|---|----------|----------|------------------------|
| 1 | ¿Es correcto que exista scroll horizontal cuando el tamaño de columnas sea modificado via resize? | 🟡 | OBS-15 |
| 2 | ¿La búsqueda global incluía PDF templates en la versión anterior? Si sí, ¿se debe restablecer? | 🟡 | OBS-34 |

---

### Evidencia General
- Test Matrix: [test-matrix.md](file:///c:/Users/STEVE/Desktop/Automation/ionflow-qa-catalyst/knowledge/L3-tickets/86e223kvf/test-matrix.md)
- Code Review QA: [code-review-qa.md](file:///c:/Users/STEVE/Desktop/Automation/ionflow-qa-catalyst/knowledge/L3-tickets/86e223kvf/code-review-qa.md)
- AC Consolidado: [ac-consolidated.md](file:///c:/Users/STEVE/Desktop/Automation/ionflow-qa-catalyst/knowledge/L3-tickets/86e223kvf/ac-consolidated.md)
- Risk Triage: [risk-triage.md](file:///c:/Users/STEVE/Desktop/Automation/ionflow-qa-catalyst/knowledge/L3-tickets/86e223kvf/risk-triage.md)

| Details | |
|---|---|
| BROWSER | Chrome |
| BRANCH | IONF-1104 |
| ENV | dev-app.ionflow.io |
| TEST MATRIX | [test-matrix.md](file:///c:/Users/STEVE/Desktop/Automation/ionflow-qa-catalyst/knowledge/L3-tickets/86e223kvf/test-matrix.md) |
| CODE REVIEW | ✅ Realizado |
| MERGE REQUEST | PENDIENTE (bugs encontrados) |
