# Template de Rechazo — 86e2ee6d6

Estimado @Yamil Paredes

**El resultado de pruebas para este ticket es: RECHAZADO ❌**

**Ticket**: 86e2ee6d6 — STAGEMIND - API extensible de feedback de ejecuciones para Xenvio
**Módulo**: STAGEMIND (ai_productmind)
**QA Engineer**: Steve Nina
**Fecha**: 2026-08-11

### Resumen de Testing
- Casos ejecutados: N/A
- Casos aprobados: N/A
- Casos fallidos: N/A
- Bugs encontrados en Code Review: N/A (repo externo — sin code review)
- Bugs encontrados en Testing: 3
- Bugs totales (bloqueantes): 3

### Code Review QA
> No se realizó code review QA ya que el repositorio `ai_productmind` es externo al ecosistema de repos de Ionflow y no forma parte del scope habitual de revisión.

- Repos revisados: N/A
- Hallazgos: N/A
- TCs inyectados en la test matrix desde el code review: N/A
- Bugs del código que contribuyen al rechazo: N/A

---

### 📌 Observaciones

---

**🔴 OBS-01 - Urgent - Estado: Nuevo**
**Área / Flujo: Feedback API — `processing_result_id` no accesible vía endpoints**

**Descripción:**
Al utilizar cualquiera de los endpoints de procesamiento de imágenes (imagen generada, imagen editada, OCR), la respuesta devuelve un `transaction_id`. Sin embargo, al intentar utilizar este ID en el endpoint de feedback (`POST /api/v1/feedback`), el campo `processing_result_id` requerido internamente no es aceptado ya que indica que no existe. En la tabla `processing_results` existe un ID diferente al `transaction_id` que no tiene forma de obtenerse de manera natural a través de los endpoints disponibles — solo es accesible consultando la base de datos directamente.

**Pasos de reproducción:**

1. Autenticarse con Bearer token válido
2. Ejecutar cualquier endpoint de procesamiento de imágenes (generar, editar u OCR)
3. Obtener el `transaction_id` devuelto en la respuesta
4. `POST /api/v1/feedback` con el `transaction_id` obtenido y un `processing_result_id` derivado de la respuesta
5. Observar que el endpoint rechaza el `processing_result_id` indicando que no existe
6. Consultar directamente la tabla `processing_results` en la BD → se encuentra un ID diferente que sí es aceptado

**Resultado esperado:**
El `processing_result_id` debe ser accesible y obtenible a través de los endpoints disponibles de la API (por ejemplo, incluido en la respuesta de los endpoints de procesamiento de imágenes o consultable mediante un endpoint dedicado). El usuario no debería necesitar acceder a la base de datos para obtener este valor.

**Comportamiento actual:**
El `processing_result_id` necesario para enviar feedback a un resultado específico solo existe en la tabla `processing_results` de la BD y no es expuesto por ningún endpoint de la API. No hay forma de obtenerlo de forma natural sin consultar la base de datos directamente.

**Evidencia:**
- Respuesta de endpoints de procesamiento: solo devuelve `transaction_id`
- Tabla `processing_results`: contiene un ID diferente no expuesto vía API

---

**🔴 OBS-02 - Urgent - Estado: Nuevo**
**Área / Flujo: Feedback API — Idempotency Key bloquea múltiples feedbacks por resultado**

**Descripción:**
Al intentar enviar más de un feedback para un mismo resultado de procesamiento, el sistema rechaza la solicitud indicando que ya existe un registro. Se espera que al utilizar un `Idempotency-Key` diferente se pueda enviar múltiples reacciones (feedbacks) para un mismo resultado, ya que la unicidad debería estar dada por la combinación de `Idempotency-Key` + resultado, no solo por el resultado en sí.

**Pasos de reproducción:**

1. Autenticarse con Bearer token válido
2. `POST /api/v1/feedback` con un `transaction_id` válido, `Idempotency-Key: key-001` y feedback `like` → responde `201 Created` ✅
3. `POST /api/v1/feedback` con el mismo `transaction_id`, **diferente** `Idempotency-Key: key-002` y feedback `dislike` → responde error indicando que el registro ya existe ❌
4. Verificar que no se creó el segundo feedback

**Resultado esperado:**
Al enviar un nuevo feedback con un `Idempotency-Key` diferente para el mismo `transaction_id`, el sistema debería permitir crear un nuevo registro de feedback. La restricción de unicidad de la `Idempotency-Key` debe garantizar que cada key sea única (evitando duplicados con la misma key), pero no debería impedir enviar múltiples feedbacks con keys diferentes para el mismo resultado.

**Comportamiento actual:**
El sistema tiene una restricción `UNIQUE(transaction_id)` en la tabla `feedbacks` que limita a un solo feedback por transacción, independientemente del `Idempotency-Key` utilizado. Esto impide que múltiples actores o el mismo actor envíen feedbacks adicionales con diferentes keys.

**Evidencia:**
- Segundo `POST /api/v1/feedback` con diferente `Idempotency-Key` → rechazado
- Restricción `UNIQUE(transaction_id)` en tabla `feedbacks`

---

**🟡 OBS-03 - Normal - Estado: Nuevo**
**Área / Flujo: Feedback API — Inconsistencia en tipos de ID entre tablas**

**Descripción:**
Se observó que algunas tablas del sistema utilizan IDs incrementales (enteros auto-incrementados) mientras que otras utilizan UUIDs como identificadores primarios. Se espera que los tipos de identificadores se uniformicen a lo largo de todas las tablas del sistema para mantener consistencia en el modelo de datos.

**Pasos de reproducción:**

1. Revisar la estructura de la tabla `feedbacks` → utiliza un tipo de ID
2. Revisar la estructura de la tabla `processing_results` → utiliza un tipo de ID diferente
3. Revisar la estructura de `request_logs` → comparar tipo de ID
4. Observar la inconsistencia entre los tipos de identificadores utilizados

**Resultado esperado:**
Todas las tablas del sistema deben utilizar un tipo de identificador uniforme (preferiblemente UUID) para mantener consistencia en el modelo de datos, facilitar la integración entre tablas y seguir un estándar único en el diseño de la base de datos.

**Comportamiento actual:**
Existe una mezcla de IDs incrementales (enteros) y UUIDs entre las distintas tablas del sistema, lo que genera inconsistencia en el modelo de datos y puede provocar confusiones al momento de relacionar registros entre tablas.

**Evidencia:**
- Tabla `processing_results`: utiliza ID incremental
- Tabla `feedbacks` / `request_logs`: utilizan UUID
- Inconsistencia visible al inspeccionar el esquema de la BD

---

### Evidencia General
- Test Matrix: N/A (repo externo — testing funcional directo sobre API)
- QA Report: N/A
- Code Review QA: N/A (repo externo `ai_productmind`)
- DB Evidence: Inspección directa de tablas `feedbacks`, `processing_results`, `request_logs`

| Details | |
|---|---|
| BROWSER | N/A (API Testing) |
| BRANCH | IONF-1194 |
| ENV | Staging |
| TEST MATRIX | N/A |
| CODE REVIEW | N/A (repo externo) |
| MERGE REQUEST | https://github.com/altacrest/ai_productmind/pull/3 |
