Estimada @Sonia Vale

**El resultado de pruebas para este ticket es: APROBADO ✅**


### Requerimiento 1. OAuth2 y Paginado

**Company > App Connectors > Salla > Connections > OAuth2**

El App Connector configurado para la aplicación de Salla cuenta con la lista de nodos necesarios para realizar los procesos de Get Orders, Sync Inventory, Update Tracking y Get Products.
Se configuró el método de autenticación OAuth2 correctamente.
Se habilitó paginado en todos los flujos, tanto en los nodos de Salla como de Shipedge, permitiendo procesar grandes volúmenes de datos sin pérdida de información ni saturación de la API.

La conexión es atachada al momento de configurar algún nodo dentro de los boards.

**Evidencia:**

---

### Requerimiento 2. Get Orders

**Company > Boards > [Salla - Shipedge] > Get Orders Flow**

Se cuenta con el flow para el proceso de Get Orders. Se verificaron las correcciones de todas las observaciones del R1:

**Caso 1 (OBS R1):** Se adicionó la salida por `true` al nodo Simple Decision, el flujo continúa correctamente después de que la custom integration se haya creado ✅

**Caso 2 (OBS R1):** Se ajustaron los campos del nodo Form. Se removió el campo "Archive Orders" (no aplicable en Salla). Se añadió la funcionalidad para filtrar por tags utilizando el ID del tag (endpoint `GET /admin/v2/orders/tags`) ✅

**Caso 3 (OBS R1):** Los campos Order Status, From Date y Tags ahora se extraen del contexto del nodo Form. Se removieron los campos Payment Method y To Date que no eran utilizados ✅

**Caso 4 (OBS R1):** Se corrigió la referencia al array de items. Se añadió un nodo Form intermedio para mapear los campos, ya que el nodo List Orders no devuelve la información del SKU directamente. Se llama al nodo List Products y luego se realiza el respectivo mapeo ✅

**Nota:** Antes de ejecutar el flow de Get Orders, se debe ejecutar el flow de Get Products, debido a que al crear una orden en Shipedge se valida que el producto ya exista.

Ionflow mapea la siguiente información de cada orden: información de la orden, información sobre el shipping address y billing address, e información de los items de la orden.

Las órdenes llegaron correctamente a Shipedge Core mediante la API v5.

**Evidencia:**

---

### Requerimiento 3. Update Tracking

**Company > Boards > [Salla - Shipedge] > Update Tracking Flow**

Se cuenta con el flow para el proceso de Update Tracking. Se verificaron las correcciones de todas las observaciones del R1:

**Caso 1 (OBS R1):** Se reemplazó el nodo erróneo Get Customer Details por el nodo correcto User Information Details ✅

**Caso 2 (OBS R1):** Se adicionó la salida por `false` del nodo Simple Decision con la acción de crear la integración en caso de que no existiera en Core ✅

**Caso 3 (OBS R1):** Se removió el nodo Multiple Decision que hacía referencia a un nodo inexistente ✅

**Caso 4 (OBS R1):** Se revisó y corrigió la configuración del nodo Update Shipment Details para enviar correctamente el shipment ID ✅

**Caso 5 (OBS R1):** Al finalizar el flow, se adicionó el nodo ACK de la orden en Shipedge para que no vuelva a ser recuperada ✅

Al pasar una orden a status Shipped en Shipedge y asignarle un tracking number, la orden se marcó como Shipped en Salla. La orden en Shipedge se marca como Acknowledged y al volver a llamar al endpoint de GET shipped orders, esta orden no es recuperada nuevamente.

**Nota:** La actualización de tracking numbers no soporta órdenes divididas u órdenes multibox. En caso de realizar el envío de este tipo de órdenes a Salla, se tomará en cuenta el primer shipment.

**Evidencia:**


---

### Requerimiento 4. Sync Inventory

**Company > Boards > [Salla - Shipedge] > Sync Inventory Flow**

Se cuenta con el flow para el proceso de Sync Inventory. Se verificaron las correcciones de todas las observaciones del R1:

**Caso 1 (OBS R1):** Se reemplazó el nodo erróneo Get Customer Details por el nodo correcto User Information Details. Se removió el nodo Form que no era utilizado ✅

**Caso 2 (OBS R1):** Se adicionó la salida por `false` del nodo Simple Decision con la acción de crear la integración en caso de que no existiera en Core ✅

**Caso 3 (OBS R1):** Se cambió el nodo V5 Get Channel Inventory por el nodo V5 Get Unified Inventory Catalog for a Channel, que es un endpoint más actual que soporta la extracción de inventario dentro de una ventana de tiempo (configurada a una semana) ✅

**Caso 4 (OBS R1):** Se corrigió el nodo Update Product by SKU, ahora actualiza el inventario en Salla correctamente ✅

**Evidencia:**


---

### Requerimiento 5. Get Products / Import Products

**Company > Boards > [Salla - Shipedge] > Get Products Flow**

Se cuenta con el flow para el proceso de Get Products / Import Products. Se verificaron las correcciones de las observaciones del R1:

**Caso 1 (OBS R1):** Tras revisión, se determinó que la extracción de información del cart y la verificación del campo custom no son necesarias ya que el endpoint para crear productos aún no cuenta con el parámetro `store_id` ✅

**Caso 2 (OBS R1):** Se corrigió el nodo Mapper, ahora emite el array de items correctamente ✅

**Evidencia:**


---

| Details | |
|---|---|
| BROWSER | Chrome |
| BRANCH | None (it is a board) |
| ENV | dev-app.ionflow.io / qa46.shipedge.com |
| TEST MATRIX | YES |
| MERGE REQUEST | YES |
