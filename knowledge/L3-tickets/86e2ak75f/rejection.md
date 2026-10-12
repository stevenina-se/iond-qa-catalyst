Estimado @Gustavo Mamani

**El resultado de pruebas para este ticket es: RECHAZADO ❌**

---

### 📌 Observaciones

---

**🔴 OBS-01 — Urgent — Estado: Nuevo**
**Área / Flujo: Backend > Sub-flujo > Modo de ejecución heredado**

**Descripción:**
Cuando un board A (padre) se ejecuta en modo Dev y este invoca un sub-flujo (board B), la ejecución del board B se registra como `Live · Sub-flujo` en lugar de `Dev · Sub-flujo`. El sub-flujo nunca hereda el modo del padre.

**Pasos de reproducción:**

1. Company Login > Sidebar: Boards > Abrir Board A (contiene nodo Workflow que invoca Board B) en el editor
2. Ejecutar Board A en modo **Dev**
3. Sidebar: Execution History > Filtrar por Board B
4. Verificar la columna **Origen** de la ejecución generada por el sub-flujo
5. Verificar el campo `mode` en la tabla `executions` de la BD

**Resultado esperado:**
Según las instrucciones de QA del dev (2026-09-02), el sub-flujo hereda el modo del padre. La ejecución del Board B debería mostrarse como `Dev · Sub-flujo`.

**Comportamiento actual:**
La ejecución del Board B se guarda como `Live · Sub-flujo`. El metadata de consumo muestra `trigger_type=subflow` con `mode=live`, independientemente del modo del padre.

**Evidencia:**
- Verificado en entorno local el 2026-09-07
- Acción sugerida: Confirmar con dev/PM si el comportamiento fue intencional; si lo fue, actualizar las instrucciones de QA y la documentación

---

**🔴 OBS-02 — Urgent — Estado: Nuevo**
**Área / Flujo: Backend > Tests Go > Compilación rota en rama IONF-1170**

**Descripción:**
Los tests de los servicios de replay de ejecución y almacenamiento de snapshots no compilan en la rama IONF-1170. El merge de DEVELOPMENT introdujo un cambio de ubicación de una dependencia interna que no se reflejó en estos tests. El comando de verificación de tests del backend falla.

**Pasos de reproducción:**

1. Posicionarse en la rama IONF-1170 del backend
2. Ejecutar los tests unitarios del backend
3. Revisar la salida del compilador

**Resultado esperado:**
Los tests compilan y pasan (el dev reportó la ejecución de tests como comando de verificación).

**Comportamiento actual:**
La compilación falla con errores de referencia a una función que fue movida de ubicación. Se afectan 5 archivos de test en dos paquetes.

**Evidencia:**
- Evidencia obtenida en local el 2026-09-07
- Los tests unitarios de frontend no se pudieron ejecutar por falta de dependencias locales
- Los tests de webcomponents: 16/16 OK
- Otros paquetes del backend sí compilan correctamente

---

**🟠 OBS-03 — High — Estado: Nuevo**
**Área / Flujo: Frontend > Historial de ejecuciones > Enlace directo a ejecución fuera del listado**

**Descripción:**
Cuando se navega a una ejecución antigua (mayor a 7 días o más allá de las 50 más recientes) mediante enlace directo (`?run={uuid}`), la cabecera del panel central no muestra el estado, la duración ni el origen de la ejecución. Solo se muestra el título genérico "Historial de ejecuciones" y el tile "Nombre".

**Pasos de reproducción:**

1. Company Login > Navegar directamente a `/workflows/{id}/executions?run={uuid de ejecución antigua}`
2. Verificar la cabecera del panel central: icono de estado, etiqueta, tiles Duración/Origen

**Resultado esperado:**
AC-3: La ejecución expirada muestra estado, duración y errores generales junto con el aviso de expiración.

**Comportamiento actual:**
La ejecución seleccionada se busca dentro de la lista visible (limitada a 50 registros y dentro del período de retención). Si la ejecución no está en la lista, la cabecera solo muestra el título genérico. El estado, la duración y el origen no se muestran, aunque el backend sí devuelve la ejecución correctamente.

**Evidencia:**
- Verificado en entorno local
- Sugerencia mínima: cuando la ejecución no esté en la lista, consultar el detalle individualmente o incluir el resumen que ya devuelve el backend

---

**🟠 OBS-04 — High — Estado: Nuevo**
**Área / Flujo: Frontend > Historial de ejecuciones > Validación de pertenencia de ejecución al board**

**Descripción:**
La vista acepta el parámetro `?run=` con un UUID de una ejecución de otro board y muestra su replay bajo la URL del board actual. No se valida que la ejecución pertenezca al board de la ruta.

**Pasos de reproducción:**

1. Company Login > Sidebar: Execution History > Board B > Copiar el UUID de una ejecución del Board B
2. Navegar a `/workflows/{idA}/executions?run={uuidB}` (Board A)
3. Verificar el canvas y la cabecera

**Resultado esperado:**
UX Research: si el enlace apunta a una ejecución inexistente o de otro board, se informa con un mensaje comprensible.

**Comportamiento actual:**
No se valida que la ejecución pertenezca al board de la ruta. El sistema devuelve el replay y se dibuja el flujo del Board B mientras el botón "Abrir board" lleva al Board A. La lista lateral muestra las ejecuciones de A sin selección.

**Evidencia:**
- Verificado en entorno local
- Sugerencia mínima: validar que la ejecución pertenece al board de la URL o redirigir al board correcto

---

**🟠 OBS-05 — High — Estado: Nuevo**
**Área / Flujo: Frontend > Historial de ejecuciones > Lista lateral limitada a 50 sin paginación**

**Descripción:**
La lista lateral de ejecuciones del board está limitada a 50 registros (`per_page: 50`) sin paginación ni aviso al usuario. Las ejecuciones por encima de la posición 51 no son accesibles desde esta vista.

**Pasos de reproducción:**

1. Generar más de 50 ejecuciones del board (por ejemplo, webhook en bucle)
2. Company Login > Sidebar: Boards > Board > Tab: Ejecuciones
3. Contar las filas de la lista lateral
4. Buscar la ejecución número 51

**Resultado esperado:**
La UI debería paginar o avisar que solo se muestran las 50 más recientes. Las restantes siguen accesibles desde Execution History general.

**Comportamiento actual:**
La vista solicita un máximo de 50 registros y la lista lateral no ofrece paginación. Las ejecuciones 51+ no aparecen ni hay aviso. Boards con webhooks de alto volumen superan 50 ejecuciones en horas.

**Evidencia:**
- Verificado en entorno local

---

**🟠 OBS-06 — High — Estado: Nuevo**
**Área / Flujo: Backend/Frontend > Replay de ejecución en curso (running)**

**Descripción:**
Al intentar ver el replay de una ejecución que se encuentra en estado running o pending, no se muestra un mensaje informativo propio. Existe un texto de traducción preparado para este caso ("ejecución en curso") pero no se utiliza.

**Pasos de reproducción:**

1. Company Login > Sidebar: Boards > Board con nodo lento (HTTP con retraso de 60s) > Ejecutar
2. Mientras la ejecución corre, abrir el historial del board
3. Seleccionar la ejecución en estado running
4. Verificar el mensaje mostrado
5. Repetir al terminar la ejecución

**Resultado esperado:**
La UI debería indicar que la ejecución sigue en curso y no mostrar datos parciales ni errores técnicos.

**Comportamiento actual:**
Los datos de replay se persisten solo al finalizar la ejecución, por lo que el sistema responde con un error 404 indicando que no hay estado registrado. No se muestra un mensaje amigable al usuario.

**Evidencia:**
- Verificado en entorno local

---

**🟡 OBS-07 — Normal — Estado: Nuevo**
**Área / Flujo: Frontend > Historial de ejecuciones > Race condition al intercambiar ejecuciones**

**Descripción:**
Cuando se tienen ejecuciones con errores y se intercambia rápidamente entre ellas en la lista lateral, es posible ver brevemente los datos de replay de la ejecución anterior antes de que se carguen los datos de la ejecución seleccionada. Esto se debe a una condición de carrera en la carga asíncrona del replay: la respuesta de la primera solicitud llega después de que el usuario ya seleccionó otra ejecución, y se dibuja momentáneamente el canvas equivocado.

**Pasos de reproducción:**

1. Company Login > Sidebar: Boards > Board con múltiples ejecuciones con errores
2. Seleccionar una ejecución con error en la lista lateral
3. Inmediatamente (antes de que termine de cargar), seleccionar otra ejecución distinta
4. Observar el canvas: brevemente se muestra el replay de la primera ejecución antes de actualizarse

**Resultado esperado:**
Al seleccionar una nueva ejecución, el canvas debe limpiar los datos de la ejecución anterior inmediatamente y mostrar un loading state hasta que lleguen los datos correctos. No debe mostrarse el replay de otra ejecución en ningún momento.

**Comportamiento actual:**
Se muestra brevemente el replay de la ejecución anterior cuando la respuesta asíncrona de la primera solicitud llega con retraso. No se cancela la solicitud anterior al seleccionar una nueva ejecución.

**Evidencia:**
- Reproducible al hacer clic rápido entre ejecuciones con errores en la lista lateral

---

| Details | |
|---|---|
| BROWSER | Chrome |
| BRANCH | IONF-1170 |
| ENV | dev-app.ionflow.io |
| TEST MATRIX | YES |
| MERGE REQUEST | YES |
