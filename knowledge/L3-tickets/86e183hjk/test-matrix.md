# Test Matrix — 86e183hjk
# [POC-GTW] Desacoplar envío de chunks de órdenes a ShipEdgeCore del ciclo HTTP síncrono

> Modo: **Discovery**
> Generado: 2026-07-06
> Repos afectados: `gateway` (PHP/Laravel), `ion_webcomponents_flow` (frontend)
> Branches: Gateway PR#4, Webcomponents PR#4

---

## Pre-requisitos de Ambiente

- RabbitMQ corriendo: `docker run -d --name rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3-management`
  - UI: `http://localhost:15672` (guest/guest)
- Workers de cola activos: `queue:work` en gateway
- Frontend: `pnpm install` + `pnpm build-gateway`
- **Sin migraciones** — no hay cambios de schema
- **Sin env vars nuevas** — la config es per-app en `apps.configuration` (JSON)

---

## Test Matrix

### GRUPO 1 — Retrocompatibilidad (Happy Path — Default Webhook)

| TC-ID | Tipo | Descripción | Pasos | Resultado Esperado | AC | Prioridad |
|-------|------|-------------|-------|-------------------|----|-----------|
| TC-001 | Happy Path | App sin configuración de transporte entrega por webhook como antes | `Company Login > Sidebar: Gateway > Developer Apps > [App sin config] > Configurar > (sin modificar transporte) > Disparar get_orders desde integración` | El chunk de órdenes llega al endpoint HTTP de Core exactamente igual que antes del ticket. Sin cambios en el comportamiento observable | AC-02 | 🔴 |
| TC-002 | Happy Path | App con Default=Webhook explícito entrega igual | `[App] > Configurar > Default transport: Webhook > Guardar > Disparar get_orders` | Mismo comportamiento que TC-001 | AC-02 | 🔴 |
| TC-003 | Regresión | Webhooks legacy siguen funcionando | `Disparar acción en app con config['webhooks'] legacy > Verificar logs` | Webhooks legacy responden normalmente. Logs NO muestran "no enviado" para acciones exitosas | AC-08 | 🟡 |

### GRUPO 2 — Motor RabbitMQ con Override por Acción

| TC-ID | Tipo | Descripción | Pasos | Resultado Esperado | AC | Prioridad |
|-------|------|-------------|-------|-------------------|----|-----------|
| TC-004 | Happy Path | Override get_orders → RabbitMQ entrega a cola correcta | `[App] > Configurar > Default transport: Webhook > + Add override: get_orders / RabbitMQ > Connection URI: amqp://guest:guest@localhost:5672 > Guardar > Disparar get_orders` | En UI de RabbitMQ (localhost:15672) aparece mensaje en cola `get_orders` con el chunk de órdenes. El resto de acciones siguen por webhook | AC-03 | 🔴 |
| TC-005 | Happy Path | Con override get_orders → Rabbit, otras acciones siguen por webhook | `Misma app del TC-004 > Disparar acción diferente (ej. get_products)` | La acción NO aparece en RabbitMQ. Llega por HTTP al endpoint de Core | AC-03 | 🟠 |
| TC-006 | Happy Path | Default transport = RabbitMQ (todas las acciones van a rabbit) | `[App] > Configurar > Default transport: RabbitMQ > Connection URI válido > Sin overrides > Guardar > Disparar get_orders y otra acción` | Ambas acciones aparecen en sus colas respectivas (cola = nombre de acción) en RabbitMQ | AC-04 | 🟠 |
| TC-007 | Edge Case | resolveRoute aplica override correctamente (case sensitive) | `Override: get_orders → Rabbit > Disparar Get_Orders (mayúsculas)` | Verificar si el override aplica o no (documentar comportamiento real) | AC-03 | 🟡 |

### GRUPO 3 — Seguridad de Credenciales

| TC-ID | Tipo | Descripción | Pasos | Resultado Esperado | AC | Prioridad |
|-------|------|-------------|-------|-------------------|----|-----------|
| TC-008 | Happy Path | connection_uri enmascarado en respuesta de API | `GET /api/2.0/user/apps/{appId} > Revisar campo connection_uri en response` | El campo devuelve `amqp://user:***@host`. La password real NUNCA aparece en el response | AC-05 | 🔴 |
| TC-009 | Happy Path | Editar app con URI configurado sin modificarlo y guardar | `[App con URI] > Configurar > (no tocar URI) > Guardar > Disparar get_orders` | El delivery sigue funcionando — la password no se corrompió al guardar | AC-06 | 🟠 |
| TC-010 | Negativo | Password nunca aparece en errores de conexión | `Check Connection con URI inválido > Revisar tooltip de error` | El tooltip muestra el error de conexión pero NO incluye la password en claro | AC-05, AC-11 | 🔴 |

### GRUPO 4 — Test de Conexión al Broker

| TC-ID | Tipo | Descripción | Pasos | Resultado Esperado | AC | Prioridad |
|-------|------|-------------|-------|-------------------|----|-----------|
| TC-011 | Happy Path | Check connection con URI válido y broker activo | `[App] > Configurar > transporte RabbitMQ > Connection URI: amqp://guest:guest@localhost:5672 > Click Check` | Botón queda verde. Tooltip: "Connection successful" | AC-09 | 🟠 |
| TC-012 | Negativo | Check connection con URI inválido | `Connection URI: amqp://invalid:bad@nowhere:9999 > Click Check` | Botón queda rojo. Tooltip con detalle del error de conexión | AC-09 | 🟠 |
| TC-013 | Negativo | Check connection con broker caído | `Detener RabbitMQ > Click Check con URI válido` | Botón queda rojo. Tooltip con error de timeout/conexión rechazada | AC-09 | 🟠 |
| TC-014 | Edge Case | Botón Check deshabilitado con campo URI vacío | `[App] > Configurar > RabbitMQ > Connection URI: vacío` | Botón Check está deshabilitado (no clickeable) | AC-10 | 🟡 |
| TC-015 | Edge Case | Botón Check vuelve a neutro al modificar URI | `[App con check verde] > Modificar el URI > Verificar estado del botón` | El estado del botón vuelve a neutro (ni verde ni rojo) | AC-10 | 🟡 |
| TC-016 | Edge Case | Check con URI enmascarado usa credencial real del servidor | `[App con URI ya guardado (enmascarado)] > NO modificar el URI > Click Check` | El check conecta exitosamente usando la credencial almacenada en BD, no el string con `***` | AC-11 | 🟠 |
| TC-017 | Negativo | Throttle 429 al superar 10 checks/minuto | `Hacer click en Check más de 10 veces en menos de 1 minuto` | A partir del 11° request, el backend responde 429. El botón muestra el fallo | AC-12 | 🟠 |
| TC-018 | Happy Path | Throttle se restablece después de 1 minuto | `Esperar 1 minuto después de TC-017 > Click Check nuevamente` | El botón funciona nuevamente (no sigue en 429) | AC-12 | 🟡 |

### GRUPO 5 — Static Parameters

| TC-ID | Tipo | Descripción | Pasos | Resultado Esperado | AC | Prioridad |
|-------|------|-------------|-------|-------------------|----|-----------|
| TC-019 | Happy Path | Static params aparecen top-level en payload (webhook) | `[App] > Configurar > + Static params: warehouse_code=MIA-01, priority=23 > Guardar > Disparar get_orders (transport: Webhook) > Inspeccionar payload recibido en Core` | El payload incluye `"warehouse_code": "MIA-01"` (string) y `"priority": 23` (number) como campos top-level junto a `account`, `type`, `data` | AC-13, AC-14 | 🟠 |
| TC-020 | Happy Path | Static params aparecen top-level en payload (RabbitMQ) | `Misma config del TC-019 pero con transport: RabbitMQ > Disparar get_orders > Inspeccionar mensaje en UI de RabbitMQ` | Mismo resultado que TC-019 en el mensaje de la cola | AC-13, AC-14 | 🟠 |
| TC-021 | Negativo | Key duplicada → form bloquea al instante | `+ Static params > Agregar 2 params con la misma key (ej. dos "warehouse_code")` | El form muestra error rojo inline bajo la sección al instante. No permite submit | AC-15 | 🟠 |
| TC-022 | Negativo | Key reservada → form bloquea al instante | `+ Static params > Key: "data" (reservada)` | El form muestra error rojo inline al instante ("key reservada") | AC-15 | 🟠 |
| TC-023 | Negativo | Key inválida → form bloquea al instante | `+ Static params > Key: "123" (no es tipo identificador)` | El form muestra error rojo inline al instante ("key inválida") | AC-15 | 🟠 |
| TC-024 | Negativo | Value vacío → error tras submit | `+ Static params > Key: "warehouse_code" > Value: (vacío) > Submit` | El backend responde con error 422, el mensaje se muestra visible en el form | AC-15 | 🟠 |
| TC-025 | Negativo | Key reservada por API directa (bypass frontend) | `POST /api/2.0/user/apps/{appId} body: { static_params: [{ key: "account", value: "test" }] }` | El backend responde con 422 con mensaje de error claro | AC-15 | 🟠 |
| TC-026 | Negativo | Más de 20 static params por API directa | `POST /api/2.0/user/apps/{appId} body: { static_params: [ 21 params ] }` | El backend responde con 422 | AC-15 | 🟡 |

### GRUPO 6 — Compresión zlib del Payload

| TC-ID | Tipo | Descripción | Pasos | Resultado Esperado | AC | Prioridad |
|-------|------|-------------|-------|-------------------|----|-----------|
| TC-027 | Happy Path | Compresión ON + RabbitMQ: mensaje comprimido con señal deflate | `[App] > Configurar > Send payload compressed: ✅ > transport: RabbitMQ get_orders > Disparar get_orders > Inspeccionar mensaje en UI RabbitMQ` | El mensaje trae `content_encoding: deflate`. El body descomprimido con `gzuncompress()` da el JSON original | AC-16 | 🟡 |
| TC-028 | Happy Path | Compresión ON + Webhook: header Content-Encoding en POST | `[App] > Configurar > Send payload compressed: ✅ > transport: Webhook > Disparar get_orders > Inspeccionar request HTTP recibido en Core` | El POST incluye header `Content-Encoding: deflate`. El body es el JSON comprimido | AC-16 | 🟡 |
| TC-029 | Happy Path | Compresión OFF (default): payload idéntico al actual | `[App] > Configurar > Send payload compressed: ☐ (desactivado) > Disparar get_orders` | Sin header `Content-Encoding`. Sin propiedad `content_encoding`. JSON plano. Idéntico al comportamiento pre-ticket | AC-17 | 🟡 |
| TC-030 | Regresión | Apps sin checkbox de compresión configurado (old apps) | `[App existente sin la config compress_payload] > Disparar get_orders` | El payload llega sin compresión — el default es OFF | AC-17 | 🟡 |

### GRUPO 7 — Validaciones y Errores

| TC-ID | Tipo | Descripción | Pasos | Resultado Esperado | AC | Prioridad |
|-------|------|-------------|-------|-------------------|----|-----------|
| TC-031 | Negativo | Elegir RabbitMQ sin Connection URI → form bloquea | `[App] > Configurar > Default transport: RabbitMQ > Connection URI: vacío > Submit` | El form bloquea el submit. No se permite guardar sin URI | AC-07 | 🟠 |
| TC-032 | Negativo | Connection URI malformado → backend rechaza con 422 | `PUT /api/2.0/user/apps/{appId} body: { connection_uri: "not-a-valid-uri" }` | Backend responde 422 con mensaje de error descriptivo. No lanza TypeError ni 500 | AC-07 | 🟠 |
| TC-033 | Negativo | Error 422 del backend visible en el form | `Enviar datos inválidos que pasen la validación del frontend > Verificar que el error del backend es visible` | El mensaje de error 422 del backend aparece en el form (en el slot correcto) | AC-15 | 🟡 |

### GRUPO 8 — Logs y Observabilidad

| TC-ID | Tipo | Descripción | Pasos | Resultado Esperado | AC | Prioridad |
|-------|------|-------------|-------|-------------------|----|-----------|
| TC-034 | Happy Path | Log de RabbitDriver incluye cola, resource e items (sin credenciales) | `Disparar get_orders con RabbitMQ > Revisar storage/logs` | Log: `RabbitDriver: published to queue {"queue":"get_orders","resource":"get_orders","items":N}` Sin password ni payload de órdenes | AC-08 | 🟡 |
| TC-035 | Negativo | Log NO incluye payload completo (50 órdenes) | `Inspeccionar storage/logs tras TC-004` | El log no contiene el JSON de las órdenes. Solo metadatos | AC-08 (implícito) | 🟡 |

---

## Matriz de Cobertura por AC

| AC | TCs que lo cubren |
|----|------------------|
| AC-01 | TC-004, TC-006, TC-019 |
| AC-02 | TC-001, TC-002 |
| AC-03 | TC-004, TC-005 |
| AC-04 | TC-006 |
| AC-05 | TC-008, TC-010 |
| AC-06 | TC-009 |
| AC-07 | TC-031, TC-032 |
| AC-08 | TC-003, TC-034, TC-035 |
| AC-09 | TC-011, TC-012, TC-013 |
| AC-10 | TC-014, TC-015 |
| AC-11 | TC-016 |
| AC-12 | TC-017, TC-018 |
| AC-13 | TC-019, TC-020 |
| AC-14 | TC-019, TC-020 |
| AC-15 | TC-021, TC-022, TC-023, TC-024, TC-025, TC-026, TC-033 |
| AC-16 | TC-027, TC-028 |
| AC-17 | TC-029, TC-030 |

---

## Resumen de Casos por Tipo

| Tipo | Cantidad |
|------|---------|
| Happy Path | 11 |
| Edge Case | 8 |
| Negativo | 11 |
| Regresión | 5 |
| **Total** | **35** |

---

## Estado

> ⏳ **Pendiente aprobación del QA Engineer**


---

## Grupo 9 — Code Review (TCs derivados del análisis de código)

> Prefijo `TC-CR-` indica origen en Code Review Discovery.

| TC-ID | Tipo | Descripción | Pasos | Resultado Esperado | Señal / AC | Prioridad |
|-------|------|-------------|-------|-------------------|------------|-----------|
| TC-CR-001 | Code Review | Verificar que deliver() + webhook legacy no causan doble entrega | `Company Login > Sidebar: Gateway > Developer Apps > [App con deliver() configurado que TAMBIÉN tenga configuration['webhooks'] en su config legacy] > Disparar get_orders > Inspeccionar requests recibidos en Core` | Core recibe el payload **una sola vez**. No hay doble entrega. | SEÑAL-09 / AC-18 | 🔴 |
| TC-CR-002 | Code Review | Verificar canal AMQP se cierra correctamente tras fallo en queue_declare | `Configurar app con Connection URI válido pero con permisos insuficientes para declarar la cola > Disparar get_orders > Inspeccionar conexiones abiertas en UI RabbitMQ` | La conexión no muestra canales colgados (leaked). El job falla correctamente. | SEÑAL-01 / AC-20 | 🟠 |
| TC-CR-003 | Code Review | Verificar que tries=1 + fallo de RabbitMQ va a failed_jobs (no se pierde silenciosamente) | `Detener RabbitMQ > Disparar get_orders con app configurada en rabbit > Inspeccionar tabla failed_jobs en BD` | El job aparece en `failed_jobs` con el error del broker. No hay pérdida silenciosa. | SEÑAL-02 / R-002 | 🟠 |
| TC-CR-004 | Code Review | Verificar validación backend de static_params con key reservada por API directa | `PUT /api/2.0/user/apps/{appId} con body: {"configuration": {"static_params": [{"key": "data", "value": "test"}]}} > Revisar response` | Backend responde 422 con mensaje de error claro. Si responde 200, la validación no está presente en el backend. | SEÑAL-03 / AC-15 | 🟠 |
| TC-CR-005 | Code Review | Verificar que todos los features de Iteración 2 están presentes en el form (Check, static params, compresión) | `Company Login > Sidebar: Gateway > Developer Apps > [App] > Button: "Configure" > Inspeccionar UI del form` | El form muestra: (1) botón Check junto al Connection URI, (2) sección Static Parameters con filas key/value, (3) checkbox de compresión. | SEÑAL-04 / AC-19 | 🟠 |
| TC-CR-006 | Code Review | Verificar que connection_uri no se valida solo en frontend (bypass por API directa) | `PUT /api/2.0/user/apps/{appId} con body: {"configuration": {"transport": "rabbit"}} sin connection_uri > Revisar response` | Backend responde 422 — rabbit sin URI debe ser rechazado en el backend, no solo en el frontend. | SEÑAL-08 / AC-07 | 🟠 |

---

## Resumen Actualizado de Casos

| Tipo | Cantidad |
|------|---------|
| Happy Path | 11 |
| Edge Case | 8 |
| Negativo | 11 |
| Regresión | 5 |
| **Code Review** | **6** |
| **Total** | **41** |

