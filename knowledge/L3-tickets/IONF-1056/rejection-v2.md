# Reporte de Retesteo (2do Ciclo) — IONF-1056-B

Estimado @Enrique Vicente

**El resultado de pruebas para este ticket es: RECHAZADO ❌**

**Ticket**: IONF-1056-B — Zero-Stripe (Billing & Consumption Guard)
**Módulo**: Billing, Scheduler, Webhooks, Execution Engine, Notifications, Admin Panel
**QA Engineer**: Steve Nina
**Fecha**: 2026-08-14
**Ciclo**: Retesteo (2do ciclo de QA — verificación de correcciones OBS-01 a OBS-18)

---

### Resumen del Retesteo
- Observaciones del 1er ciclo verificadas: OBS-01 a OBS-18
- Nuevas observaciones encontradas: **10**
- Severidad 🔴 Urgent: **6** (OBS-R01, OBS-R03, OBS-R04, OBS-R06, OBS-R08, OBS-R10)
- Severidad 🟡 High: **4** (OBS-R02, OBS-R05, OBS-R07, OBS-R09)
- Observaciones reincidentes: **1** (OBS-R10 → reincidente de OBS-02)

> La verificación completa de las correcciones anteriores se ve parcialmente obstruida por las nuevas observaciones encontradas, especialmente OBS-R08 que afecta la estabilidad de la plataforma. Se recomienda abordar las observaciones urgentes antes de re-ejecutar la suite completa de verificación.

---

### 📌 Nuevas Observaciones del Retesteo

---

**🔴 OBS-R01 - Urgent - Estado: Nuevo**
**Área / Flujo: Billing — PDF Impressions Quota Guard (Concurrencia vía Scheduler)**
**Observación anterior relacionada:** OBS-17 (enforcement mid-execution + concurrencia)

**Descripción:**
En un escenario de 8 flows siendo ejecutados por un scheduler que los dispara cada minuto, se observó que la cuota de impresiones PDF diarias fue **superada** a pesar de que el sistema debería bloquear inmediatamente al alcanzar el límite. En la primera ejecución se generó un excedente de **2 impresiones** por encima de la cuota, y en la segunda ejecución el excedente aumentó a **4 impresiones**.

**Pasos de reproducción:**

1. Configurar 8 flows con nodo PDF, cada uno configurado para generar al menos 1 impresión
2. Configurar un scheduler que dispare los 8 flows cada minuto
3. Configurar la cuota de `pdf_impressions` con un límite bajo (ej. 10)
4. Observar las ejecuciones del scheduler
5. En la primera ejecución, se dispararon primero 5 flows (no los 8 simultáneamente)
6. Los 5 flows presentaron errores de ejecución en algunos nodos (ver video adjunto)
7. Luego se dispararon los 3 flows restantes
8. Se repitió el ciclo: 5 flows primero, 3 después
9. Verificar el contador de `pdf_impressions` → excedente de +2 (primer ciclo) y +4 (segundo ciclo)

**Resultado esperado:**
La impresión de PDF debe bloquearse **inmediatamente** al alcanzar la cuota diaria. No debe ser posible generar impresiones por encima del límite configurado. El guard de `pdf_impressions` debe operar con consistencia atómica, independientemente de cuántos flows se ejecuten concurrentemente.

**Comportamiento actual:**
Cuando múltiples flows ejecutan nodos PDF de forma concurrente (disparados por scheduler), el guard no bloquea de forma atómica, permitiendo que varios flows "pasen" el guard simultáneamente antes de que el consumed se actualice, generando un excedente que crece con cada ciclo de ejecución.

**Impacto:** Pérdida económica — se generan impresiones PDF que no deberían existir, sin posibilidad de cobro. El excedente es acumulativo y escala con la concurrencia.

**Evidencia:** Video adjunto mostrando errores de ejecución en nodos y excedente de cuota.

---

**🟡 OBS-R02 - High - Estado: Nuevo (Cuestión/Pregunta abierta)**
**Área / Flujo: Billing — Scheduler (Concurrencia y desfase de ejecuciones)**
**Observación anterior relacionada:** OBS-17/18

**Descripción:**
En el escenario del caso anterior (8 flows disparados por un scheduler cada minuto), se observó que los 8 flows **no se ejecutaron al mismo tiempo**. Primero se ejecutaron 5 flows, lo cual demoró alrededor de 1 minuto y algunos segundos. Luego se ejecutaron los 3 flows restantes, demorando aproximadamente medio minuto.

**Pregunta abierta:**
Si la ejecución de los primeros 5 flows demoró más de 1 minuto, y el scheduler está configurado para disparar cada minuto, **¿no debería haberse disparado una nueva ejecución de los 8 flows inmediatamente al cumplirse el siguiente minuto, incluso antes de que finalizaran los 3 restantes?** Esto sugiere un posible desfase o cola de ejecuciones donde el scheduler no respeta estrictamente el intervalo configurado cuando hay ejecuciones previas aún en curso.

**Pasos de reproducción:**

1. Configurar 8 flows con un scheduler de ejecución cada 1 minuto
2. Observar la primera ejecución: solo se disparan 5 de los 8 flows
3. Los 5 flows demoran ~1 minuto y algunos segundos en completarse
4. Luego se disparan los 3 flows restantes (~30 seg)
5. Observar que el siguiente ciclo del scheduler no se disparó al cumplirse el minuto

**Comportamiento observado:**
- Minuto 0:00 → Se disparan 5 de 8 flows
- Minuto ~1:05 → Finalizan los 5 flows, se disparan los 3 restantes
- Minuto ~1:35 → Finalizan los 3 flows
- Minuto ~1:35+ → Recién se vuelven a disparar los 5 flows del siguiente ciclo

**Comportamiento esperado (cuestionado):**
- Minuto 0:00 → Se disparan los 8 flows simultáneamente
- Minuto 1:00 → Se disparan nuevamente los 8 flows (independiente de si los anteriores finalizaron)

> ⚠️ **Nota:** Esto se plantea como **cuestión de diseño** más que como observación de rechazo. ¿Es intencional que el scheduler espere a que finalice el ciclo anterior antes de disparar el siguiente? ¿Cuál es el comportamiento esperado cuando los flows tardan más que el intervalo del scheduler?

---

**🔴 OBS-R03 - Urgent - Estado: Nuevo**
**Área / Flujo: Billing — Execution History (Status `pending` permanente al superar cuota)**
**Observación anterior relacionada:** OBS-17/18 (estado `quota_exhausted`)

**Descripción:**
Tanto para ejecuciones disparadas por **schedulers** como por **webhooks**, al superar la cuota de ejecución se crean registros en la execution history que permanecen **permanentemente en estado `pending`** sin ninguna finalización. Estos registros deberían crearse con el status `quota_exhausted` como fue acordado en la corrección de OBS-17/18.

**Pasos de reproducción:**

1. Agotar la cuota de `execution_time` o `pdf_impressions`
2. Disparar ejecuciones adicionales vía scheduler o webhook
3. Consultar la execution history
4. Observar que los registros quedan con status `pending` indefinidamente

**Resultado esperado:**
Las ejecuciones que no puedan iniciarse por cuota agotada deben registrarse con el status **`quota_exhausted`** en la execution history, proporcionando visibilidad clara al usuario de por qué la ejecución no se completó.

**Comportamiento actual:**
Los registros quedan en `pending` permanentemente, sin resolución ni indicador de la causa. Esto genera confusión en el usuario y contamina la execution history con registros "colgados" que nunca finalizan.

**Impacto:** Degradación de UX, datos de execution history inconsistentes, imposibilidad de distinguir ejecuciones genuinamente en progreso de ejecuciones bloqueadas por cuota.

---

**🔴 OBS-R04 - Urgent - Estado: Nuevo**
**Área / Flujo: Billing — Webhook Trigger (504 Timeout + inconsistencia de status)**
**Observación anterior relacionada:** OBS-03 (webhook devolvía 504 en vez de 403)

**Descripción:**
Al ejecutar un flow mediante disparadores de webhook (ejemplo: 8 ejecuciones del mismo flow mediante webhook), las ejecuciones finalizaron después de aproximadamente **2 minutos**, retornando todas con un error **504 (Gateway Timeout)**. Sin embargo, las impresiones de PDF se registraron correctamente y el tiempo de ejecución también se contabilizó correctamente. Los status de las ejecuciones en la execution history registraron **`completed`**, pero el webhook retornó **504**.

**Pasos de reproducción:**

1. Configurar un flow con nodo PDF que genere impresiones
2. Disparar 8 ejecuciones del mismo flow mediante webhook simultáneamente
3. Observar las respuestas del webhook → todas retornan **504** después de ~2 minutos
4. Verificar execution history → status muestra **`completed`**
5. Verificar `pdf_impressions` → impresiones registradas **correctamente**
6. Verificar `execution_time` → tiempo contabilizado **correctamente**

**Resultado esperado:**
Si la ejecución se completó exitosamente (status `completed`, impresiones registradas, tiempo contabilizado), el webhook debería retornar **200 OK** con el resultado de la ejecución, no un 504. Si la ejecución excede el timeout del webhook, debería haber un mecanismo de respuesta asíncrona o un timeout adecuado.

**Comportamiento actual:**
Existe una **inconsistencia grave** entre:
- El response HTTP del webhook → **504 Timeout**
- El status en execution history → **`completed`**
- El consumo registrado → **Correcto**

Esto indica que el flow **sí se ejecutó y completó correctamente en el backend**, pero la respuesta no llegó al caller porque el timeout del webhook (aparentemente ~2 min) expiró antes de que el flow finalizara. El caller externo interpreta esto como un fallo y potencialmente reintenta, generando ejecuciones duplicadas.

**Impacto:** Los sistemas externos que consumen el webhook (Shopify, MercadoLibre, ERPs, etc.) reciben 504 y activan retries automáticos, causando ejecuciones duplicadas, consumo de cuota injustificado y potencial pérdida de datos por procesamiento duplicado.

> ⚠️ **ADVERTENCIA:** Esta es una **inconsistencia grave de contrato de API**. El status del webhook no refleja la realidad de la ejecución. Los callers externos no tienen forma de saber que la ejecución fue exitosa.

---

**🟡 OBS-R05 - High - Estado: Nuevo**
**Área / Flujo: Billing — PDF Impressions Counter Reset (Inconsistencia visual)**
**Observación anterior relacionada:** OBS-09 (reset_at date)

**Descripción:**
Al reiniciar el contador de impresiones PDF justo a la hora programada usando el botón **Refresh**, se observó una **inconsistencia visual en dos pasos**: primero el contador se reinició correctamente a 0, sin embargo el badge de estado **"Blocked"** continuaba visible. Al presionar el botón **Refresh** una segunda vez, recién el badge cambió a **"0%"**, generando una inconsistencia visual transitoria.

**Pasos de reproducción:**

1. Agotar la cuota de `pdf_impressions` hasta que el badge muestre "Blocked"
2. Esperar a que se cumpla la hora de reset programada (00:00 UTC)
3. Presionar el botón **Refresh** en la vista de billing/usage
4. Observar: el contador muestra **0** impresiones, pero el badge sigue mostrando **"Blocked"** ❌
5. Presionar **Refresh** una segunda vez
6. Observar: ahora el badge cambia correctamente a **"0%"** ✅

**Resultado esperado:**
Al presionar Refresh después de la hora de reset, **tanto el contador como el badge** deben actualizarse simultáneamente en un solo request, mostrando 0 impresiones y 0% de uso sin el badge de "Blocked".

**Comportamiento actual:**
El reset ocurre en dos pasos: el primer Refresh reinicia el `consumed` pero no recalcula el estado de bloqueo (badge). El segundo Refresh recalcula el estado correctamente. Esto sugiere que el lazy reset actualiza `consumed` pero no recalcula `blocked` en el mismo request, o que la UI cachea el estado de bloqueo previo.

---

**🔴 OBS-R06 - Urgent - Estado: Nuevo**
**Área / Flujo: Billing — Flow Execution (Stop vs. Background execution)**
**Observación anterior relacionada:** OBS-17 (enforcement mid-execution)

**Descripción:**
Al stopear un flow **visualmente**, el flow se detiene en la interfaz pero **continúa ejecutándose en background**. El tiempo de ejecución en background se contabiliza en el consumo de `execution_time`, generando una discrepancia entre lo que el usuario observa (flow detenido) y el registro real en la execution history.

**Pasos de reproducción:**

1. Ejecutar un flow con múltiples nodos que toman tiempo
2. Presionar el botón **Stop** durante la ejecución
3. Observar: visualmente el flow se detiene ✅
4. Verificar en background: el flow **sigue ejecutándose** ❌
5. Verificar `execution_time` → se contabiliza **todo el tiempo**, incluyendo el background
6. Comparar con execution history → discrepancia en el tiempo registrado

**Resultado esperado:**
Al presionar Stop, la ejecución debe detenerse **completamente** (tanto visual como internamente), y el tiempo contabilizado debe corresponder únicamente al tiempo de ejecución real hasta el momento del stop.

**Comportamiento actual:**
El stop es solo visual; el proceso continúa en background consumiendo `execution_time` sin que el usuario tenga visibilidad de ello.

**Impacto:** Consumo de cuota injustificado — el usuario cree que detuvo el flow pero sigue gastando segundos de ejecución.

---

**🟡 OBS-R07 - High - Estado: Nuevo**
**Área / Flujo: Billing — Flow Execution (Pause + Stop en nodo PDF)**
**Observación anterior relacionada:** OBS-17 (enforcement mid-execution)

**Descripción:**
Al pausar un flow en modo dev, los segundos consumidos se registran correctamente. Sin embargo, si luego se stopea el flow, se contabiliza una **pequeña porción adicional de tiempo**. Se observaron además las siguientes inconsistencias:

1. Cuando se puso **pausa**: en la columna `reference_id` se registró **`null`**
2. Cuando se puso **stop**: en la columna `reference_id` se registró un **número**
3. Cuando se puso **stop** (en este escenario), el flow **ya no continúa en background** — a diferencia de OBS-R06

> **Nota:** Este comportamiento diferenciado ocurre cuando se pone **pausa justo cuando el flow ingresa al nodo PDF**. La combinación pausa-en-nodo-PDF + stop posterior presenta un comportamiento distinto al stop directo (OBS-R06), donde el flow sí continúa en background.

**Pasos de reproducción:**

1. Ejecutar un flow en modo dev que incluya un nodo PDF
2. Poner **pausa** justo cuando el flow ingresa al nodo PDF
3. Verificar `execution_time` → segundos consumidos registrados correctamente ✅
4. Verificar `reference_id` → **null** ❌
5. Presionar **Stop**
6. Verificar que se contabiliza una pequeña porción adicional de tiempo ❌
7. Verificar `reference_id` → ahora muestra un **número** ✅
8. Verificar que el flow **no continúa en background** (diferente a OBS-R06) ✅

**Resultado esperado:**
- El `reference_id` debería registrarse consistentemente tanto en pausa como en stop
- No debería contabilizarse tiempo adicional después de un stop cuando el flow ya estaba pausado
- El comportamiento de stop debería ser consistente independientemente de si se pausó primero o no

---

**🔴 OBS-R08 - Urgent - Estado: Nuevo**
**Área / Flujo: Infraestructura — Backend binaries / Base de datos (Saturación)**
**Observación anterior relacionada:** OBS-17 (enforcement mid-execution + concurrencia)

**Descripción:**
Durante los escenarios de prueba del retesteo (ejecuciones concurrentes mediante scheduler y webhooks), se observó que el **backend de los binarios llegaba a morir**. Consultando con Rodolfo y este con Henry, se identificó que la **base de datos llegaba a saturarse**, lo que afectaba al rendimiento de la plataforma como tal, e incluso llegando a dejar la **plataforma inoperable**.

**Pasos de reproducción:**

1. Ejecutar escenarios de carga concurrente (8+ flows vía scheduler o webhooks)
2. Repetir los ciclos de ejecución durante varios minutos
3. Observar que el backend de flow_binaries deja de responder
4. Confirmar con el equipo de infraestructura que la BD está saturada

**Resultado esperado:**
La plataforma debe ser capaz de manejar la carga concurrente esperada sin degradación ni caídas. El motor de ejecución y el sistema de consumo deben estar diseñados para operar bajo concurrencia sin saturar la base de datos.

**Comportamiento actual:**
La carga concurrente generada por schedulers y webhooks satura la base de datos, provocando la caída del backend de binarios y dejando la plataforma inoperable para todos los tenants.

**Impacto:** **Crítico** — Afecta la disponibilidad de la plataforma completa, no solo el tenant que genera la carga.

> 🚨 **ACCIÓN REQUERIDA:** Se sugiere **analizar la arquitectura** del motor de ejecución y consumo, y consultar con Rodolfo alguna alternativa para que este escenario no vuelva a suceder. Posibles líneas de acción:
> - Limitar la concurrencia máxima por company/scheduler
> - Implementar connection pooling o backpressure en la BD
> - Evaluar Redis como buffer intermedio para writes de consumo de alta frecuencia
> - Implementar circuit breaker para proteger la BD ante picos de carga

---

**🟡 OBS-R09 - High - Estado: Nuevo**
**Área / Flujo: UI — Execution History (Filtro faltante)**

**Descripción:**
En la execution history no existe un filtro para el estado **`quota_exhausted`**. Dado que este es un nuevo estado terminal introducido en la corrección de OBS-17/18, debería estar disponible como opción de filtrado para que el usuario pueda identificar rápidamente las ejecuciones bloqueadas por cuota.

**Pasos de reproducción:**

1. Navegar a la execution history
2. Buscar la opción de filtro por status
3. Verificar que `quota_exhausted` no aparece como opción disponible

**Resultado esperado:**
El filtro de status en la execution history debe incluir **`quota_exhausted`** como opción seleccionable, permitiendo al usuario filtrar y visualizar solo las ejecuciones que fueron detenidas por agotamiento de cuota.

**Comportamiento actual:**
El estado `quota_exhausted` no está disponible en los filtros de la execution history.

---

**🔴 OBS-R10 - Urgent - Estado: Persistente (reincidente de OBS-02)**
**Área / Flujo: Billing — Notifications (Consumption Notify)**
**Observación anterior relacionada:** OBS-02 (emails de notificación de consumo no se envían)

**Descripción:**
Persiste el problema reportado en OBS-02: los emails de notificación de consumo (advertencias al 80%, 100% y bloqueo) **siguen sin enviarse al usuario**. A pesar de que la corrección del developer indicó que se resolvieron 3 defectos (orden de log vs. envío, contexto del log y resolución del destinatario), el comportamiento en el entorno de pruebas sigue siendo el mismo — los correos de advertencia no llegan.

**Pasos de reproducción:**

1. Confirmar que `EMAIL_PROVIDER=SMTP` está configurado con credenciales válidas (no `LOG`)
2. Ejecutar flows hasta cruzar el **80%** de `execution_time` o `pdf_impressions`
3. Verificar bandeja de correo del contacto de la company → **no hay email de advertencia** ❌
4. Continuar ejecutando hasta cruzar el **100%** del cupo
5. Verificar bandeja de correo → **no hay email de límite alcanzado** ❌
6. Continuar hasta bloqueo total de la feature
7. Verificar bandeja de correo → **no hay email de bloqueo** ❌
8. Verificar BD: `feature_consumption_logs` → verificar si existen registros de notificación

**Resultado esperado:**
Se deben enviar emails al contacto de la company cuando el consumo alcanza los umbrales del 80%, 100% y estado bloqueado. Los emails deben usar las plantillas `usage_warning_80`, `usage_limit_100` y `feature_blocked` respectivamente, con el contenido contextual correcto (feature, porcentaje consumido, plan).

**Comportamiento actual:**
Los correos de advertencia de consumo no llegan al destinatario. El problema persiste desde el primer ciclo de QA (OBS-02), lo que indica que la corrección implementada no resolvió el defecto de envío de manera efectiva en el entorno de pruebas.

**Impacto:** Los usuarios no reciben aviso previo de que se están acercando a sus límites de cuota, resultando en bloqueos inesperados de features sin oportunidad de tomar acciones preventivas (upgrade, reducción de uso, etc.).

> ⚠️ **OBSERVACIÓN REINCIDENTE:** Esta observación persiste desde el primer ciclo de QA (OBS-02). La corrección reportada por el developer no solucionó el problema en el entorno de pruebas. Se requiere verificación conjunta con el developer para determinar si es un problema de configuración de entorno o un defecto persistente en el código.

---

### 📊 Resumen de Observaciones del Retesteo

| # | Severidad | Área | Descripción resumida | Tipo |
|---|-----------|------|---------------------|------|
| OBS-R01 | 🔴 Urgent | PDF Impressions + Scheduler | Cuota de PDF excedida en ejecuciones concurrentes (+2, +4 excedente) | Bug |
| OBS-R02 | 🟡 High | Scheduler | 8 flows se ejecutan en lotes de 5+3, no simultáneamente; desfase de ciclos | Cuestión |
| OBS-R03 | 🔴 Urgent | Execution History | Ejecuciones bloqueadas quedan en `pending` permanente (no `quota_exhausted`) | Bug |
| OBS-R04 | 🔴 Urgent | Webhook + Status | Webhook retorna 504 pero ejecución registra `completed` — inconsistencia grave | Bug |
| OBS-R05 | 🟡 High | UI / Counter Reset | Badge "Blocked" persiste después del reset; requiere doble Refresh | Bug |
| OBS-R06 | 🔴 Urgent | Flow Stop | Stop visual no detiene ejecución en background; tiempo se contabiliza | Bug |
| OBS-R07 | 🟡 High | Flow Pause + Stop (PDF) | Comportamiento inconsistente de `reference_id` y tiempo en pausa+stop en nodo PDF | Bug |
| OBS-R08 | 🔴 Urgent | Infraestructura | BD se satura con carga concurrente, backend muere, plataforma inoperable | Arquitectura |
| OBS-R09 | 🟡 High | UI / Filtros | No hay filtro `quota_exhausted` en execution history | Feature gap |
| OBS-R10 | 🔴 Urgent | Notificaciones | Emails de advertencia de consumo siguen sin enviarse (reincidente OBS-02) | Bug reincidente |

---

### Evidencia General
- Test Matrix: [test-matrix.md](file:///c:/Users/STEVE/Desktop/Automation/ionflow-qa-catalyst/knowledge/L3-tickets/IONF-1056/test-matrix.md)
- Code Review QA: [code-review-qa.md](file:///c:/Users/STEVE/Desktop/Automation/ionflow-qa-catalyst/knowledge/L3-tickets/IONF-1056/code-review-qa.md)
- AC Consolidado: [ac-consolidated.md](file:///c:/Users/STEVE/Desktop/Automation/ionflow-qa-catalyst/knowledge/L3-tickets/IONF-1056/ac-consolidated.md)
- Análisis detallado: [analysis_results.md](file:///c:/Users/STEVE/Desktop/Automation/ionflow-qa-catalyst/knowledge/L3-tickets/IONF-1056/analysis_results.md)
- Reporte retesteo (artefacto): [retest_86e1pzyug.md](file:///C:/Users/STEVE/.gemini/antigravity-ide/brain/ac55e590-4234-4b99-b73d-b841c8a474e4/retest_86e1pzyug.md)

| Details | |
|---|---|
| BROWSER | Chrome |
| BRANCH | IONF-1056-B |
| ENV | dev-app.ionflow.io |
| MERGE REQUESTS | [flow_binaries PR#29](https://github.com/altacrest/ion_flow_binaries/pull/29), [gateway PR#38](https://github.com/altacrest/ion_gateway/pull/38), [gateway-ion PR#33](https://github.com/altacrest/ion_gateway_ion/pull/33) |
| CICLO | Retesteo (2do ciclo) |
