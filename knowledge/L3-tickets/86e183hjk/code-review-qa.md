# Code Review QA — 86e183hjk (Modo Discovery)

> Modo: **Discovery — Exploración de señales para discusión con el Developer**
> Generado: 2026-07-06
> Repos revisados: `gateway` (branch IONF-1044) · `webcomponents-flow` (branch IONF-1044)
> Tono: Preguntas abiertas — NO objeciones

---

## Resumen

| Ítem | Valor |
|------|-------|
| Repos revisados | gateway (PHP/Laravel), webcomponents-flow (Vue 3 + TS) |
| Archivos clave analizados | 8 |
| Señales encontradas | 9 |
| Señales de alto interés | 4 |
| Señales de medio interés | 5 |

---

## Archivos Analizados

| Repo | Archivo | Rol |
|------|---------|-----|
| gateway | `app/Services/Delivery/Contracts/DeliveryDriver.php` | Contrato/Interface del motor |
| gateway | `app/Services/Delivery/DeliveryFactory.php` | Factory de drivers |
| gateway | `app/Services/Delivery/Drivers/RabbitDriver.php` | Driver RabbitMQ |
| gateway | `app/Services/Delivery/Drivers/WebhookDriver.php` | Driver Webhook |
| gateway | `app/Services/Delivery/ConnectionRegistry.php` | Cache de conexiones AMQP |
| gateway | `app/Models/App.php` | Motor de deliver + resolveRoute + masking |
| gateway | `app/Jobs/IntegrationActionJob.php` | Job que llama al motor |
| gateway | `app/Http/Controllers/Api/V2/User/AppController.php` | CRUD de apps (update) |
| webcomponents-flow | `src/gateway/views/apps/components/App/AppEdit.vue` | Form de configuración (frontend) |
| webcomponents-flow | `src/gateway/views/apps/schema/app.ts` | Validación yup del form |

---

## Observaciones para Discusión con el Developer

### 🟠 SEÑAL-01 — `RabbitDriver`: ¿El channel se cierra en caso de excepción antes del `close()`?

**Archivo**: `app/Services/Delivery/Drivers/RabbitDriver.php`
**Código relevante**:
```php
$channel = app(ConnectionRegistry::class)->get($this->connectionUri)->channel();
$channel->queue_declare($this->queue, false, true, false, false);
// ... (si falla aquí)
$message = new AMQPMessage(...);
$channel->basic_publish($message, '', $this->queue);
$channel->close(); // ← solo se ejecuta si no hubo excepción antes
```

**Señal**: Si `queue_declare()` o `basic_publish()` lanzan una excepción, el `$channel->close()` **no se ejecuta**. El canal queda abierto. La conexión sí se cierra en `ConnectionRegistry::closeAll()`, pero el canal puede quedar en estado inválido hasta entonces.

**Pregunta para el Developer**: ¿Se consideró wrapping en try/finally para garantizar el cierre del canal incluso en caso de excepción? ¿Hay algún mecanismo que compense esto?

---

### 🟠 SEÑAL-02 — `IntegrationActionJob`: Timeout = 0, Tries = 1 — ¿Compensación de pérdida de mensajes?

**Archivo**: `app/Jobs/IntegrationActionJob.php`
**Código relevante**:
```php
public $timeout = 0;   // antes: 600 (10 minutos)
public $tries = 1;     // antes: 3 (3 reintentos)
public $failOnTimeout = false;
```

**Señal**: El timeout pasó de 600s a 0 (sin límite), y los intentos bajaron de 3 a 1. El comentario del driver dice "on failure the exception bubbles up so the job fails (tries=1) and the business re-poll recovers". Esto asume que el mecanismo de re-poll de ShipEdgeCore es suficiente para recuperar chunks perdidos.

**Pregunta para el Developer**: ¿El "business re-poll" de Core siempre recupera chunks perdidos? ¿En qué tiempo? ¿Hay algún SLA de recuperación o el chunk puede perderse definitivamente si el job falla?

---

### 🟠 SEÑAL-03 — `AppController::update()` — ¿Dónde se validan `static_params` y `compress_payload`?

**Archivo**: `app/Http/Controllers/Api/V2/User/AppController.php`
**Código relevante**:
```php
public function update(Request $request, $appId): ApiResource
{
    // ...
    $app->fill($request->all())->save(); // ← sin validación de configuration
```

**Señal**: La segunda iteración describe validaciones de `static_params` (keys reservadas, max 20, valores max 255, formato identificador) y validación de `connection_uri`. Sin embargo, el `AppController::update()` hace un `fill($request->all())->save()` sin pasar por `App::configurationRules()` que el comentario del ticket menciona como "compartida entre store/update". No se encuentra `configurationRules()` en el código del `App.php`.

**Pregunta para el Developer**: ¿Dónde vive la validación de `static_params` y `connection_uri`? ¿Se aplica en un Request Form/middleware antes de llegar al controller? ¿O el `configurationRules()` mencionado en el comentario no llegó a este PR?

---

### 🟠 SEÑAL-04 — `AppEdit.vue`: Iteración 2 no presente — ¿Static params, Check button y compresión están en otro archivo?

**Archivo**: `src/gateway/views/apps/components/App/AppEdit.vue`

**Señal**: El `AppEdit.vue` en IONF-1044 implementa correctamente el form de transport, overrides, y connection URI (Iteración 1). Pero **no se encuentran** en el código:
- El botón **"Check"** para test de conexión al broker
- La sección de **Static Parameters** (filas key/value)
- El checkbox de **compresión**

Estos son features de la **Iteración 2** (comentario 2026-07-01). El form de `AppEdit.vue` diff tiene +121/-0 líneas — podría que la Iteración 2 esté en un sub-componente no revisado, o en otra rama que se mergeó.

**Pregunta para el Developer**: ¿Los features de la Iteración 2 (Check connection, static params, compresión) están en el mismo PR#4 o en un PR separado? ¿En qué componente Vue específicamente?

---

### 🟡 SEÑAL-05 — `resolveRoute()`: Los overrides no tienen fallback en case de `connection_uri` ausente a nivel de override

**Archivo**: `app/Models/App.php`
**Código relevante**:
```php
$connectionUri = data_get($this->configuration, 'transport_config.connection_uri');
if (empty($connectionUri)) {
    throw new \RuntimeException("Rabbit transport for process '{$process}' is missing transport_config.connection_uri.");
}
```

**Señal**: La URI de conexión es global para la app (no por override). Si se configura Default=Webhook + Override get_orders=Rabbit, la URI sigue siendo de nivel app. Esto es consistente con el diseño, pero si alguien tiene dos apps configuradas con Rabbit apuntando a brokers distintos, cada app tiene su propia URI. Si un override de acción pudiera especificar una URI diferente, no está soportado actualmente.

**Pregunta para el Developer**: ¿Es por diseño que todos los overrides de rabbit de una app apuntan al mismo broker (connection_uri a nivel app)? ¿Hay casos donde se querría un broker diferente por acción?

---

### 🟡 SEÑAL-06 — `ConnectionRegistry`: La clave de cache es el URI completo (incluyendo password)

**Archivo**: `app/Services/Delivery/ConnectionRegistry.php`
**Código relevante**:
```php
private array $connections = [];

public function get(string $uri): AMQPStreamConnection
{
    if (!isset($this->connections[$uri]) || !$this->connections[$uri]->isConnected()) {
        $this->connections[$uri] = $this->connect($uri);
    }
    return $this->connections[$uri];
}
```

**Señal**: El URI completo (incluyendo la password en texto plano) es la clave del array `$connections`. En una instancia del Registry compartida (singleton en el container de Laravel), si múltiples jobs se ejecutan con el mismo URI (cosa esperada), se reutiliza la conexión. Sin embargo, la password vive en memoria como clave del array.

**Pregunta para el Developer**: ¿El `ConnectionRegistry` es un singleton en el service container? ¿O se instancia por job? Si es singleton, la password vive en memoria durante todo el ciclo de vida del worker — ¿es eso acceptable por la política de seguridad del equipo?

---

### 🟡 SEÑAL-07 — `DeliveryDriver::send()` retorna `Response|JsonResponse` — ¿Qué hace el caller con ese valor?

**Archivo**: `app/Services/Delivery/Contracts/DeliveryDriver.php` + callers

**Señal**: El contrato `DeliveryDriver::send()` retorna `Response|JsonResponse`. El `RabbitDriver::send()` devuelve `response()->json(['message' => 'Published to queue', 'queue' => ...], 200)`. Pero el caller en `sendWebhook()` no usa el valor de retorno de `$integration->app->deliver(...)` — llama y descarta el resultado.

**Pregunta para el Developer**: ¿El valor de retorno de `deliver()` se usa en algún caller para determinar si el envío fue exitoso? ¿O es siempre descartado? Si es descartado, ¿el 200 artificial del `RabbitDriver` tiene algún efecto en los logs de "evento enviado/no enviado"?

---

### 🟡 SEÑAL-08 — `app.ts` schema (yup): `transport` sin validación de `connection_uri`

**Archivo**: `src/gateway/views/apps/schema/app.ts`
**Código relevante**:
```ts
export const appSchema = object().shape({
  name: string().required(...),
  slug: string().required(...),
  description: string().required(...),
  webhook_url: string().required(...),
  transport: string().oneOf(['webhook', 'rabbit']),
  // ← No hay validación de connection_uri aquí
});
```

**Señal**: La validación de `connection_uri` se implementó en el handler `onSubmit` de forma imperativa (`if (usesRabbit.value && !connectionUri.value?.trim())`), no en el schema yup. Esto significa que la validación del URI queda separada de las otras validaciones del form.

**Pregunta para el Developer**: ¿Se consideró integrar la validación de `connection_uri` en el schema yup? ¿Hay alguna razón técnica para mantenerlo en el handler imperativo (ej. dependencia condicional que yup no maneja bien)?

---

### 🟡 SEÑAL-09 — `WebhooksController::sendWebhook()`: `deliver()` y el webhook legacy corren en paralelo

**Archivo**: `app/Http/Controllers/Api/WebhooksController.php`
**Código relevante**:
```php
if ($integration->app) {
    $integration->app->deliver([...]); // ← nuevo motor
}

if (!$webhook) {
    \Log::info('WEBHOOKS NOT FOUND IN THE CONFIGURATION');
    return response()->json(['message' => 'Webhook not found'], 404);
}

// ← continúa con el webhook legacy ($configuration['webhooks'])
```

**Señal**: Cuando `$integration->app` existe, `deliver()` ya envió el payload. Luego el código **continúa** y, si `$webhook` existe (config legacy), vuelve a hacer otro `Http::post()` al webhook legacy. Esto podría causar **doble entrega** del mismo payload: una vez por `deliver()` (nuevo motor) y otra por el `Http::post()` del switch/case legacy.

**Pregunta para el Developer**: Si una app tiene tanto `deliver()` configurado (nuevo motor) como webhooks legacy en `configuration['webhooks']`, ¿el payload se entrega dos veces? ¿Es intencional o hay una condición de guarda que se me escapó?

---

## Enriquecimiento del Risk-Triage

Las siguientes señales refuerzan o agregan riesgos al `risk-triage.md`:

| Señal | Riesgo relacionado | Actualización |
|-------|--------------------|---------------|
| SEÑAL-01 | R-008 (Cierre AMQP) | **Confirmado en código**: el channel no tiene try/finally → puede quedar abierto en excepción |
| SEÑAL-02 | R-002 (Fallo silencioso) | **Matizado**: no es silencioso, la excepción sube al job. Pero tries=1 + re-poll de Core asumido |
| SEÑAL-03 | R-005 (Keys reservadas en static_params) | **No encontrado en código**: la validación de static_params no se encontró en el PR analizado |
| SEÑAL-04 | R-006 (Compresión) | **No encontrado en código**: los features de Iteración 2 no están en el AppEdit.vue revisado |
| SEÑAL-09 | R-001 (Retrocompatibilidad) | **Nuevo riesgo**: posible doble entrega cuando app tiene deliver() + webhook legacy simultáneamente |

---

## Nuevo Riesgo Identificado en Code Review

> Se agrega al risk-triage:

**R-015 (🔴 CRÍTICO): Doble entrega potencial — deliver() + webhook legacy concurrentes**

En `WebhooksController::sendWebhook()`, si `$integration->app` existe, `deliver()` ya envió el payload al nuevo motor. El código **no hace early return** y continúa evaluando el webhook legacy. Si la integración tiene ambas configuraciones activas, el mismo payload se envía dos veces.

---

## Estado

> ✅ Code Review Discovery completado.
> Señales documentadas para discusión con el Developer (Rodolfo Merlo Ali).
> Risk-triage enriquecido con hallazgos del código.
> Pendiente: Respuesta del Developer a las 9 señales antes de cerrar Discovery.
