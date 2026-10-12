Estimado @rodolfo.merlo

**El resultado de pruebas para este ticket es: RECHAZADO ❌**

---

### 📌 Observaciones

**🔴 BUG-01 — P1 — Estado: Nuevo**
**Área / Flujo: Gateway — Developer Apps — AppEdit Dialog — Connection URI**

**Descripción:**
El diálogo AppEdit es compartido: el Connection URI no se limpia al cambiar de app y contamina otras apps (rabbit sin URI real o URI con `***` literal).

**Precondiciones:**
- User Role: Developer (dueño de la app)
- User State: Logged in en el webcomponent gateway
- App exists: Yes
- Integration exists: Yes (canal con get_orders; ej. Shopify)
- Workers: `queue:work` activos (`JOBS_ENABLE=true`)
- Broker: RabbitMQ accesible (IONF-1044-mock/docker-compose.yml o broker real)
- Receptor webhook: IONF-1044-mock/webhook_receiver.py corriendo y configurado como Webhook URL de la app
- App A: rabbit con URI guardado
- App B: webhook sin `transport_config`

**Pasos de reproducción:**
1. Developer Apps > Edit App A > verificar URI enmascarado > cerrar
2. Developer Apps > Edit App B > cambiar Default transport a RabbitMQ
3. Observar el campo URI
4. Save
5. `GET /api/2.0/user/apps/{B}`
6. Disparar `get_orders` en una integración de B
7. Repetir pasos 1-4 con 'New App' (Create)

**Resultado esperado:**
En B el campo URI aparece vacío; el form bloquea el Save hasta ingresar un URI; la app nueva no hereda datos de A.

**Comportamiento actual:**
El campo muestra `amqp://user:***@hostA` de la app A; el submit pasa la validación (campo no vacío); en update el hook restaura 'el original' de B que es `null` → B queda rabbit sin URI → `RuntimeException 'missing transport_config.connection_uri'` al entregar (job fallido / runEvent 500); en Create se guarda el string enmascarado literal con password `***`.

**Impacto:** P1 — Doble impacto: (1) App B queda configurada con rabbit pero sin URI válido → jobs fallan con RuntimeException al intentar entregar, causando pérdida de mensajes. (2) App nueva creada guarda literalmente el string enmascarado `***` como password → conexión al broker imposible.

**Causa raíz sugerida:**
El watcher del diálogo solo resetea el Connection URI si la app editada tiene un URI guardado. Como el componente AppEdit se instancia una sola vez y se reutiliza para todas las apps, los campos `overrideRows`/`staticParamRows`/`transport`/`compress` sí se resetean, pero el Connection URI queda con el valor de la app anterior. Variante en la misma app: quitar rabbit y guardar borra el URI y al reabrir sigue mostrando el enmascarado viejo.

**Evidencia:**
- Sin evidencia adicional

---

**🟠 BUG-02 — P2 — Estado: Nuevo**
**Área / Flujo: Gateway — Developer Apps — AppEdit Dialog — Connection URI (edición parcial)**

**Descripción:**
Editar host/puerto/vhost del URI enmascarado conservando `:***@` descarta el cambio en silencio.

**Precondiciones:**
- User Role: Developer (dueño de la app)
- User State: Logged in en el webcomponent gateway
- App exists: Yes
- Integration exists: Yes (canal con get_orders; ej. Shopify)
- Workers: `queue:work` activos (`JOBS_ENABLE=true`)
- Broker: RabbitMQ accesible (IONF-1044-mock/docker-compose.yml o broker real)
- Receptor webhook: IONF-1044-mock/webhook_receiver.py corriendo y configurado como Webhook URL de la app
- App con URI guardado `amqp://qa:S3cret@localhost:5672`

**Pasos de reproducción:**
1. Developer Apps > Edit app
2. En el campo URI (`amqp://qa:***@localhost:5672`) cambiar solo el host a `broker2` y el puerto a `5673` sin tocar `***`
3. Save (200)
4. Reabrir Edit y leer el URI
5. Disparar `get_orders`

**Resultado esperado:**
El form advierte que para cambiar el destino debe reingresar la credencial completa; o el nuevo host/puerto se guarda.

**Comportamiento actual:**
El hook de actualización detecta `:***@` y reemplaza TODO el URI por el original guardado → el host/puerto nuevo se pierde sin feedback; la entrega sigue apuntando a `localhost:5672`.

**Impacto:** P2 — El developer puede creer que migró su app a otro broker cuando en realidad el cambio fue descartado silenciosamente. No hay error ni advertencia; el payload sigue yendo al broker anterior.

**Causa raíz sugerida:**
La lógica de restauración del URI enmascarado no compara los segmentos de host/port/path con el original; simplemente descarta todo el URI editado si detecta el patrón `***` en la password. Fix mínimo: responder 422 si host/puerto/path difieren del original, o dejar el campo como solo-lectura hasta un botón "Replace URI".

**Evidencia:**
- Sin evidencia adicional

---
| Details | |
|---|---|
| BROWSER | Chrome |
| BRANCH | IONF-1044 |
| ENV | qa8-gateway.omniorders.com |
| MERGE REQUEST | YES |
