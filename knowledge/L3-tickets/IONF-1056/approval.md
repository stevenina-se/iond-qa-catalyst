Estimado @Enrique Vicente

**El resultado de pruebas para este ticket es: APROBADO ✅**

> **Nota**: La subtarea de integración Stripe (86e1pzz9j) fue marcada como "done without delivery" ya que esta entrega (IONF-1056-B) implementa exclusivamente el **motor de consumo interno** sin integración con Stripe. La facturación de overage queda planificada para una fase posterior. Las 5 subtareas entregadas fueron desarrolladas e integradas en la rama del ticket padre (IONF-1056-B).

#### 📌 Resumen por Subtarea

**1. Catálogo comercial y planes unificados** ([86e1pzz9f](https://app.clickup.com/t/86e1pzz9f))
Se implementó el modelo de catálogo comercial con productos y precios gestionados localmente (`provider='local'`). Cada plan cuenta con un producto asociado que almacena su estructura de precios (mensuales y anuales) en el campo `data.prices`, eliminando la dependencia de Stripe para la definición de la oferta. Desde el Admin Panel, el catálogo de productos se visualiza en una vista read-only sin botón de Stripe sync ni `stripe_id` visible. La asignación de planes a compañías opera desde la pestaña Subscription del Admin → Companies, donde el admin selecciona un plan diferente al actual y confirma la asignación. La operación genera automáticamente la re-sincronización de `feature_consumptions` con las ventanas del nuevo plan y registra un evento `admin_assigned` en `subscription_renewals`. El botón "Assign plan" permanece deshabilitado hasta que se seleccione un plan diferente al vigente, y se bloquea durante la operación para evitar doble envío.
**ACs cubiertos**: AC-B01, AC-B02, AC-B03, AC-B04, AC-B05, AC-B06, AC-B13, AC-B14.

> 📸 **Screenshot 1a**: Admin → Companies → Subscription tab — dropdown de plan con botón "Assign plan" (antes de asignar)
> 📸 **Screenshot 1b**: Admin → Companies → Subscription tab — después de asignar plan (plan cambiado, included features actualizadas)
> 📸 **Screenshot 1c**: BD — `SELECT * FROM subscription_renewals WHERE ... ORDER BY created_at DESC LIMIT 1` mostrando `event='admin_assigned'`
> 📸 **Screenshot 1d**: Admin → Billing → Products — vista read-only del catálogo (sin botón Stripe sync)

**2. Oferta IONPDF standalone y metering específico** ([86e1pzz9g](https://app.clickup.com/t/86e1pzz9g))
IONPDF fue configurado como un producto que puede operar de forma independiente (standalone) o como add-on complementario para IONFLOW. El plan IONPDF standalone provisiona una bolsa de segundos de `execution_time` menor que la de IONFLOW, permitiendo la creación y ejecución de templates sin requerir el plan completo. Las features medibles de IONPDF incluyen `pdf_impressions` con soporte para ventanas de consumo diarias y mensuales simultáneas. Se implementó un mecanismo de reserva atómica para las impresiones PDF que garantiza que, bajo escenarios de concurrencia elevada (múltiples flows ejecutándose vía schedulers o webhooks), la cuota no pueda ser excedida — cada impresión es reservada antes de generarse. El cambio de plan vía admin preserva los entitlements existentes de IONFLOW cuando se agrega IONPDF como add-on. El consumo de IONPDF queda registrado en el ledger unificado (`feature_consumption_logs`).
**ACs cubiertos**: AC-51, AC-52, AC-53, AC-54, AC-55.

> 📸 **Screenshot 2a**: BD — `SELECT * FROM feature_consumptions WHERE subscriber_id=<company_ionpdf>` mostrando windows de IONPDF standalone (execution_time menor + pdf_impressions)
> 📸 **Screenshot 2b**: BD — `SELECT * FROM feature_consumption_logs` mostrando registros de consumo IONPDF

**3. Ledger de consumo y segundos por ejecución** ([86e1pzz9h](https://app.clickup.com/t/86e1pzz9h))
Se construyó un ledger unificado basado en la tabla `feature_consumptions` que registra el consumo de las tres features medibles: tiempo de ejecución (`execution_time`), créditos de inteligencia artificial (`ai_credits`) e impresiones PDF (`pdf_impressions`). Cada feature puede tener múltiples ventanas simultáneas (ej. mensual + diaria), representadas como filas independientes con distinto `measure`. El motor de medición opera en streaming: acumula los segundos activos en memoria y los persiste periódicamente en la base de datos (configurable vía `CONSUMPTION_FLUSH_SECONDS`). Tras cada flush, el sistema re-evalúa el guard para determinar si la ejecución puede continuar o debe detenerse por agotamiento de cuota (detección mid-execution). Los resets son lazy: cuando `reset_at` ha vencido y se registra un consumo, el `consumed` arranca desde el `qty` consumido (no acumula sobre el anterior) y el anchor avanza desde la fecha del ciclo anterior (no desde `now`). La feature `available = -1` indica ilimitada y nunca bloquea; `available = 0` bloquea incluso con `consumed = 0`. No existe cron de billing — los resets se triggerean exclusivamente por consumo o lectura.
**ACs cubiertos**: AC-16, AC-17, AC-18, AC-19, AC-20, AC-21, AC-22, AC-23, AC-24.

> 📸 **Screenshot 3a**: BD — `SELECT measure, available, consumed, blocked, reset_at FROM feature_consumptions WHERE subscriber_id=<id>` mostrando múltiples ventanas (daily + monthly) para la misma feature
> 📸 **Screenshot 3b**: BD — Después de lazy reset: `consumed` arrancó desde qty consumido y `reset_at` avanzó desde anchor anterior

**4. Historial de runtime y estimación de duración** ([86e1pzz9c](https://app.clickup.com/t/86e1pzz9c))
Cada ejecución completada registra ahora tres métricas de duración: `active_seconds` (tiempo real de procesamiento de nodos), `idle_seconds` (tiempo de espera en nodos como Timer o Subflow con `waitForResponse`) y `units_consumed` (total contabilizado para facturación). Esta descomposición permite al usuario entender cuánto tiempo real consumió su flow vs. cuánto fue de espera pasiva. La columna "Execution Time" es visible en el historial de ejecuciones mostrando la duración total en formato legible. El alcance fue simplificado para el MVP: solo muestra la última duración de ejecución completada, sin promedios, predicciones ni estimaciones avanzadas. La visualización en el Board queda pendiente por rediseño de UI (AC-58 bloqueado).
**ACs cubiertos**: AC-56, AC-57, AC-59. **Bloqueado**: AC-58 (rediseño UI Board).

> 📸 **Screenshot 4a**: Execution History — lista con columna "Execution Time" visible mostrando duraciones (ej. 6.14s, 9.12s)
> 📸 **Screenshot 4b**: Execution detail modal — mostrando `active_seconds`, `idle_seconds`, `units_consumed`

**5. Enforcement, warnings y estado combinado** ([86e1pzz9e](https://app.clickup.com/t/86e1pzz9e))
Se implementó el sistema completo de enforcement de cuotas con cuatro capas:
- **Guard de consumo**: Evalúa la disponibilidad antes de despachar cualquier ejecución. Cuando la cuota está agotada, las ejecuciones (editor, live, webhooks, schedulers) reciben un bloqueo inmediato (HTTP 403) y el registro en el historial queda con estado `quota_exhausted`. Los schedules y webhooks permanecen activos — solo la ejecución se bloquea. El guard opera en modo fail-open: si hay error de infraestructura, la ejecución se permite. Features no provisionadas retornan 403 (`ErrQuotaBlocked`). No hay grace execution — la ejecución parcial que detecta el agotamiento mid-run ES la gracia (decisión de diseño aceptada).
- **AI Credits**: Flow-pilot chat consume `ai_credits` y al agotar muestra mensaje SSE amigable "reached your AI credits limit". Gateway `IonMind` endpoints retornan 403 "Feature quota exceeded" cuando `ai_credits` está agotado.
- **Notificaciones por email**: Correos al contacto de la compañía en umbrales del 80%, 100% y bloqueo total. Los emails usan el layout unificado de IonFlow, dicen "contact us" (sin mención de overage en IONF-1056-B), se deduplican por threshold por ciclo, y solo se generan para ventanas mensuales/anuales (no diarias). Se corrigió el envío de notificaciones duplicadas en concurrencia.
- **Tenant UI read-only**: `/billing/plans` muestra pricing cards informativos sin botones de compra. `/billing/subscription` muestra plan actual con usage bars por feature, badge "Blocked" cuando la cuota está agotada, y fecha/hora del próximo reinicio en la zona horaria del navegador. Sin acciones de cancel, resume ni overage.
- **Admin Panel mejorado**: Detalle del plan con carga fresca, fila resaltada durante edición, validaciones completas (UI + API), botones bloqueados durante operaciones en vuelo, mensajes de error contextuales internacionalizados, y filtro por estado `quota_exhausted` en el historial de ejecuciones.
**ACs cubiertos**: AC-25 a AC-31, AC-33 a AC-39, AC-B07 a AC-B12. **Decisión de diseño**: AC-32 (sin grace execution).

> 📸 **Screenshot 5a**: Execution History — ejecución con status `quota_exhausted` (filtro aplicado)
> 📸 **Screenshot 5b**: Flow editor — intento de ejecución con cuota agotada mostrando error/bloqueo
> 📸 **Screenshot 5c**: Email — notificación "Usage Warning" al 80% (layout IonFlow unificado)
> 📸 **Screenshot 5d**: Email — notificación "Usage Limit Reached" al 100%
> 📸 **Screenshot 5e**: Email — notificación "Execution Time Paused" (bloqueo total con "contact us")
> 📸 **Screenshot 5f**: Tenant → /billing/subscription — plan actual con usage bars, badge "Blocked" visible, fecha de próximo reinicio
> 📸 **Screenshot 5g**: Tenant → /billing/plans — pricing cards read-only (sin botones de compra/upgrade)
> 📸 **Screenshot 5h**: Flow-pilot chat — mensaje SSE "reached your AI credits limit" al agotar ai_credits

**6. Integración Stripe y facturación de overage** ([86e1pzz9j](https://app.clickup.com/t/86e1pzz9j)) — ⏸ Fuera del alcance
Esta subtarea fue marcada como "done without delivery" dado que IONF-1056-B implementa la variante zero-Stripe. Toda la integración con Stripe (checkout, portal, webhooks, meter events, cancel/resume, overage) fue eliminada del branch. La verificación residual confirmó que `grep -ri stripe` en flow_binaries solo encuentra mappings de columna dormidos, sin imports ni llamadas al SDK. La facturación de overage queda planificada para una fase posterior cuando se implemente el motor de marketplace (86e1y463z).
**ACs cubiertos**: AC-B15 (verificación residual). **N/A**: Bloques 2 y 6 completos (21 ACs archivados).

---

### 🛠️ ¿Qué se construyó / cambió?

**1. Catálogo comercial y planes unificados** (86e1pzz9f)
Se implementó el modelo de catálogo comercial con productos y precios gestionados localmente. Cada plan cuenta con un producto asociado que almacena su estructura de precios (mensuales y anuales), eliminando la dependencia de proveedores externos para la definición de la oferta comercial. El administrador puede visualizar el catálogo de productos en una vista read-only desde el Admin Panel, y asignar planes a las compañías desde la sección de suscripciones. La asignación de un plan genera automáticamente la re-sincronización de las ventanas de consumo de la compañía, registrando un evento de auditoría en el historial de renovaciones.

**2. Oferta IONPDF standalone y metering específico** (86e1pzz9g)
IONPDF fue configurado como un producto que puede operar de forma independiente (standalone) o como add-on complementario para IONFLOW. Las features medibles de IONPDF incluyen `pdf_impressions` con soporte para ventanas de consumo diarias y mensuales simultáneas. Se implementó un mecanismo de reserva atómica para las impresiones PDF que garantiza que, bajo escenarios de concurrencia elevada (múltiples flows ejecutándose vía schedulers o webhooks), la cuota no pueda ser excedida. Cada impresión es reservada antes de generarse, asegurando consistencia atómica independientemente del número de flows concurrentes.

**3. Ledger de consumo y segundos por ejecución** (86e1pzz9h)
Se construyó un ledger unificado que registra el consumo de las tres features medibles: tiempo de ejecución (`execution_time`), créditos de inteligencia artificial (`ai_credits`) e impresiones PDF (`pdf_impressions`). El motor de medición opera en streaming: acumula los segundos activos de cada ejecución en memoria y los persiste periódicamente en la base de datos. Tras cada persistencia, el sistema re-evalúa el guard de consumo para determinar si la ejecución puede continuar o debe detenerse por agotamiento de cuota. Este diseño permite detectar el agotamiento de cuota durante la ejecución de un flow (mid-execution), no solo al inicio.

**4. Historial de runtime y estimación de duración** (86e1pzz9c)
Cada ejecución registra ahora tres métricas de duración: segundos activos (tiempo real de procesamiento de nodos), segundos inactivos (tiempo de espera en nodos como Timer o Subflow con espera de respuesta) y unidades consumidas (total contabilizado para facturación). Esta descomposición permite al usuario entender cuánto tiempo real consumió su flow vs. cuánto tiempo fue de espera. La columna "Execution Time" es visible en el historial de ejecuciones, mostrando la duración total en formato legible.

**5. Enforcement, warnings y estado combinado** (86e1pzz9e)
Se implementó el sistema completo de enforcement de cuotas con tres capas:
- **Guard de consumo**: Evalúa la disponibilidad de cuota antes de iniciar cualquier ejecución. Cuando la cuota está agotada, las ejecuciones disparadas por webhooks o schedulers reciben un bloqueo inmediato (HTTP 403), y el registro en el historial de ejecuciones queda con estado `quota_exhausted`, proporcionando visibilidad clara de por qué la ejecución no se completó.
- **Notificaciones por email**: Se envían correos electrónicos al contacto de la compañía cuando el consumo alcanza los umbrales del 80%, 100% y bloqueo total. Los emails utilizan el diseño unificado de IonFlow con plantillas específicas para cada umbral. Se corrigió el envío de notificaciones duplicadas en escenarios de ejecuciones concurrentes.
- **Tenant UI read-only**: La interfaz del tenant muestra el plan actual con usage bars que reflejan el porcentaje de consumo por feature, badge de estado "Blocked" cuando la cuota está agotada, fecha y hora del próximo reinicio en la zona horaria del navegador, y pricing cards informativos sin acciones de compra.
- **Admin Panel mejorado**: Detalle del plan con carga fresca, fila resaltada durante edición, validaciones completas tanto en la interfaz como en la API, botones bloqueados durante operaciones en vuelo, y mensajes de error contextuales internacionalizados. Nuevo filtro por estado `quota_exhausted` en el historial de ejecuciones.

### 💡 ¿Por qué es importante?

- **Habilita la monetización de IONFLOW e IONPDF** bajo un modelo unificado con planes asignados por admin y un motor de consumo robusto que mide `execution_time`, `ai_credits` y `pdf_impressions`.
- **Protege contra pérdida económica**: El guard atómico para `pdf_impressions` y el medidor en streaming para `execution_time` previenen el consumo ilimitado sin cobro.
- **Mejora la visibilidad del consumo**: Los flows concurrentes ven el consumo actualizado con desfase máximo de una ventana de flush, y el estado `quota_exhausted` proporciona trazabilidad clara.
- **Establece la base para facturación futura**: El ledger unificado y el catálogo de productos locales preparan la infraestructura para integración de pagos en una fase posterior.

---

### 🎯 Criterios de Aceptación (AC) Clave Validados

#### **AC-B01. Admin asigna plan a company**
* **Validación realizada**: Admin → Companies → Subscription tab → seleccionar plan → Assign plan.
* **Comportamiento observado**: `feature_consumptions` se re-sincronizan, `subscription_renewals` registra `admin_assigned`. Botón y dropdown deshabilitados durante la operación. No-op si se asigna el mismo plan. ✅

> 📸 **Screenshot AC-B01**: Admin asignando plan — antes y después (BD: feature_consumptions re-sincronizadas)

#### **AC-B07. Guard sin overage — 403 + email "contact us"**
* **Validación realizada**: Agotar `execution_time`, ejecutar flow y verificar bloqueo.
* **Comportamiento observado**: Guard retorna 403 inmediato. Email con "contact us" (sin overage). ✅

> 📸 **Screenshot AC-B07**: Respuesta 403 del guard (consola/API) + email de bloqueo recibido

#### **AC — Medidor en streaming (OBS-17 corregido)**
* **Validación realizada**: Flow pesado con `CONSUMPTION_FLUSH_SECONDS=5`, verificar consumo incremental en BD.
* **Comportamiento observado**: `feature_consumptions.consumed` crece durante la ejecución. Al agotar saldo, flow termina con `quota_exhausted`. Flows concurrentes ven consumo actualizado. ✅

> 📸 **Screenshot AC-STREAM**: BD — `feature_consumptions.consumed` creciendo durante ejecución (dos queries separados mostrando incremento)

#### **AC — Reserva atómica de pdf_impressions (OBS-R01 corregido)**
* **Validación realizada**: 8 flows con nodo PDF disparados por scheduler, cuota baja.
* **Comportamiento observado**: La cuota no se excede bajo concurrencia. Reserva atómica impide race conditions. ✅

> 📸 **Screenshot AC-PDF**: BD — `SELECT consumed, available FROM feature_consumptions WHERE feature_id=<pdf_impressions>` después de 8 flows concurrentes (consumed ≤ available)

---

### 🔄 Pruebas de Regresión

- **Flows con saldo disponible ejecutan correctamente**: Verificado que el billing no interfiere con ejecuciones normales. ✅
- **Execution history sigue funcional**: Lista carga, detalle con logs por nodo, filtro `quota_exhausted` disponible. ✅
- **Schedules y webhooks no se eliminan al agotar cuota**: Configuraciones persisten, solo se bloquean las ejecuciones. ✅
- **Stop detiene completamente**: No continúa en background tras presionar Stop. `reference_id` consistente. ✅
- **Reset de ventanas**: Badge y contador se actualizan simultáneamente con un solo Refresh. ✅
---

### 📝 Conclusión de QA

El ticket IONF-1056-B implementa exitosamente el motor de consumo unificado para IONFLOW e IONPDF. Después de 3 ciclos de QA intensivo con 32 observaciones reportadas (incluyendo 11 urgentes), todas las correcciones fueron verificadas satisfactoriamente. Las 5 subtareas entregadas cubren: catálogo comercial con planes unificados, oferta standalone de IONPDF con metering específico, ledger de consumo con medición por segundos, historial de runtime con estimación de duración, y enforcement con warnings y estado combinado. La subtarea de integración Stripe queda fuera del alcance de esta entrega. El sistema opera correctamente con guard atómico para `pdf_impressions`, medidor en streaming para `execution_time`, notificaciones por email funcionales, y una UI de admin/tenant robusta con validaciones completas. Las dos observaciones restantes (OBS-R02 sobre comportamiento del scheduler y OBS-R08 sobre saturación de BD) no son parte del motor de consumos y se trasladan a tickets independientes. El entregable es estable y cumple con todos los criterios de aceptación vigentes.

| Details | |
|---|---|
| BROWSER | Chrome |
| BRANCH | IONF-1056-B |
| ENV | dev-app.ionflow.io |
| TEST MATRIX | test-matrix.md |
| MERGE REQUESTS | YES |
