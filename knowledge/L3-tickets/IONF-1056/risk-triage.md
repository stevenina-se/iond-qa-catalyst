# Risk Triage — IONF-1056
> Módulo: billing (nuevo)
> Generado: 2026-06-14
> Basado en: AC reconciliados (ac-reconciliation.md) + L1-project + L2-modules/billing

---

## Resumen de Riesgo Global

| Dimensión | Nivel | Justificación |
|-----------|-------|---------------|
| Complejidad técnica | 🔴 Alta | Nuevo módulo con 3 repos, Stripe, lazy resets, overage clipping |
| Impacto en negocio | 🔴 Crítico | Controla acceso a flows — un bug puede bloquear clientes o cobrar de más |
| Cobertura de pruebas previa | 🔴 Nula | Módulo completamente nuevo, sin tests E2E existentes |
| Regresión en módulos existentes | 🟠 Alta | Executions, PDF Templates, Boards, Nodes afectados directamente |
| Ambigüedad de AC | 🟠 Media | 2 contradicciones críticas abiertas (grace, cron vs lazy) |

---

## Área 1 — Suscripción y Ciclo de Vida

| ID | Riesgo | Tipo | Prioridad | Pregunta / Mitigación |
|----|--------|------|-----------|----------------------|
| R-01 | Estado derivado de timestamps → si `canceled_at` o `expires_at` se escriben mal, el estado queda inconsistente | Lógica | 🔴 Crítico | Testear cada webhook Stripe y verificar en BD qué timestamps quedan |
| R-02 | `payment_succeeded` mientras `canceled_at IS NOT NULL` no debe deshacer la cancelación | Lógica | 🔴 Crítico | Edge case documentado — necesita test específico |
| R-03 | `renews_at` no debe avanzar en facturas de overage (solo base lines) | Lógica | 🔴 Crítico | Una factura mensual de overage sobre plan anual no debe tocar la fecha de renovación |
| R-04 | `subscription.deleted` → DowngradeToFree: ¿queda acceso hasta `expires_at` o corta inmediato? | Lógica | 🟠 Alto | Clarificar comportamiento de acceso post-deleted |
| R-05 | Plan free auto-aprovisionado: ¿qué pasa si falla el provisioning al crear company? | Edge case | 🟠 Alto | ¿La company queda sin suscripción? ¿Hay retry? |

---

## Área 2 — Consumo y Ledger (feature_consumptions)

| ID | Riesgo | Tipo | Prioridad | Pregunta / Mitigación |
|----|--------|------|-----------|----------------------|
| R-06 | Lazy reset: si `reset_at` pasó, `consumed` debe empezar en `qty` — no en `consumed + qty` | Lógica | 🔴 Crítico | Error aquí = consumo incorrecto persistente + bloqueo falso o facturación errónea |
| R-07 | Anchor lattice: si el clock del servidor tiene drift, los anchors de `reset_at` pueden quedar mal | Infra | 🟠 Alto | Verificar con fechas límite (fin de mes, años bisiestos) |
| R-08 | Ventana múltiple por feature: si se agota la ventana diaria, bloquea aunque la mensual tenga saldo | Lógica | 🟠 Alto | Testear escenario "diaria agotada, mensual con saldo" |
| R-09 | Concurrencia: dos ejecuciones simultáneas sobre el mismo subscriber pueden duplicar consumo | Concurrencia | 🟠 Alto | ¿El mutex por `(subscriber, feature)` está cubierto en todos los paths? |
| R-10 | `available = 0` siempre bloquea aunque `consumed = 0` — ¿es intencional en enterprise? | Lógica | 🟠 Alto | Enterprise tier sin features configuradas → guard bloquea todo |
| R-11 | **[PREGUNTA ABIERTA]** `reset_at` ¿controlado por cron job (comentario 08-jun) o por lazy reads? | Contradicción | 🔴 Crítico | Preguntar a Enrique: ¿el cron fue eliminado del código? |

---

## Área 3 — Enforcement y Bloqueo

| ID | Riesgo | Tipo | Prioridad | Pregunta / Mitigación |
|----|--------|------|-----------|----------------------|
| R-12 | **[PREGUNTA ABIERTA]** Grace execution: ¿está implementada o fue descartada? | Contradicción | 🔴 Crítico | Descripción del ticket dice "1 ejecución de gracia"; comentarios de IONF-1058 no la mencionan |
| R-13 | Guard fail-open: error de infra permite ejecución → ¿cómo se loggea? ¿hay alertas? | Lógica | 🟠 Alto | Sin log, errores de infra pasan inadvertidos y el consumo no se registra |
| R-14 | `execution_time` bloqueado: schedules y webhooks quedan activos pero no corren → ¿el usuario recibe feedback claro? | UX | 🟠 Alto | ¿Qué ve el usuario si intenta ejecutar un flow bloqueado? |
| R-15 | `pdf_impressions` falla mid-execution: ¿el flow completo falla o solo el nodo PDF? | Lógica | 🟠 Alto | Impacto en datos del e-commerce si el flow queda parcialmente ejecutado |
| R-16 | Bloqueo de feature eliminada del plan: rows kept con `available=0` → guard bloquea permanentemente | Lógica | 🟡 Medio | ¿El usuario ve por qué está bloqueado si el feature ya no está en su plan? |

---

## Área 4 — Overage y Stripe Billing Meters

| ID | Riesgo | Tipo | Prioridad | Pregunta / Mitigación |
|----|--------|------|-----------|----------------------|
| R-17 | `billableDelta` clipping: error en el cálculo = over-billing o under-billing de clientes | Lógica | 🔴 Crítico | Testear exactamente los 6 casos de la tabla del prototipo |
| R-18 | Stripe meter event no enviado (fallo de red post-commit): under-billing silencioso | Infra | 🟠 Alto | ¿Se loggea el fallo? ¿Hay retry? |
| R-19 | Redelivery de Stripe: mismo evento con `fcl:<log_id>` duplicado → ¿Stripe deduplica correctamente en ~24h? | Idempotencia | 🟠 Alto | Testear con reenvío manual de webhook |
| R-20 | Activación de overage mientras en dunning → debe retornar 422 | Gate | 🟠 Alto | Gate "Not dunning" debe testearse explícitamente |
| R-21 | Plan change con overage activo: ¿se re-establecen los metered items en ambas fases (immediate + deferred)? | Lógica | 🟠 Alto | Si se pierde el metered item en el schedule, el overage deja de cobrarse |
| R-22 | Pago fallido: revoca overage → ¿la `available` del headline vuelve a `included`? | Lógica | 🟠 Alto | Debe hacer SyncConsumptions con `overage = 0` |
| R-23 | Feature sin producto Stripe → intento de activar overage → ¿error claro 422 o fallo silencioso? | Validación | 🟡 Medio | Testear con feature sin precio Stripe asociado |
| R-24 | Overage `units=0` (remoción): eventos ya reportados siguen siendo cobrados — ¿se comunica al usuario? | UX | 🟡 Medio | El usuario debe saber que el overage ya registrado aún se factura |

---

## Área 5 — IONPDF (Oferta standalone y add-on)

| ID | Riesgo | Tipo | Prioridad | Pregunta / Mitigación |
|----|--------|------|-----------|----------------------|
| R-25 | Compra standalone IONPDF: ¿la bolsa de segundos se aprovisiona correctamente en `feature_consumptions`? | Lógica | 🟠 Alto | Verificar seed/sync post-compra |
| R-26 | Add-on IONFLOW+IONPDF: ¿los entitlements de IONFLOW no se ven afectados al agregar el add-on? | Regresión | 🟠 Alto | SyncConsumptions no debe pisar ventanas existentes |
| R-27 | **[DEPENDENCIA]** Especificación final de IONPDF depende de trabajo previo de Rodolfo Merlo | Bloqueo | 🟠 Alto | ¿El ledger de Rodolfo ya está integrado en el prototipo? |
| R-28 | IONPDF tratado como OCR (error de clasificación de nodo) | Conceptual | 🟡 Medio | Verificar que ningún nodo lo categoriza como OCR |

---

## Área 6 — Runtime History (IONF-1057)

| ID | Riesgo | Tipo | Prioridad | Pregunta / Mitigación |
|----|--------|------|-----------|----------------------|
| R-29 | Visualización en Board pendiente: sin UI, QA no puede verificar el feature completo | Bloqueante | 🟠 Alto | ¿Existe endpoint API para consultar la última duración? Testear vía API |
| R-30 | Tiempo idle de Nodo Timer + subflow `waitForResponse` podría no registrarse si el flow es interrumpido | Edge case | 🟡 Medio | Testear con flow que tiene Timer y se cancela antes de terminar |
| R-31 | Fallback "estado neutro" si no hay histórico: no confirmado en implementación | Sin confirmar | 🟡 Medio | Testear con flow sin ejecuciones previas |

---

## Área 7 — Impacto Cruzado (Regresión)

| ID | Módulo afectado | Riesgo | Prioridad |
|----|----------------|--------|-----------|
| R-32 | **Executions** | El guard de `execution_time` podría bloquear flows que antes corrían libremente | 🔴 Crítico |
| R-33 | **Boards** | Schedule/webhook sigue activo pero no ejecuta → ¿logs de ejecución muestran error claro? | 🟠 Alto |
| R-34 | **PDF Templates** | Creación de template bloqueada por `pdf_templates` quota → UI debe comunicarlo | 🟠 Alto |
| R-35 | **Nodes (PDF)** | Nodo PDF en canvas falla mid-execution con `pdf_impressions` agotado → datos parciales | 🟠 Alto |
| R-36 | **webcomponents-flow** | Aún lee shape antiguo de suscripción → inconsistencia de datos en el canvas | 🟡 Medio |

---

## Preguntas Abiertas para el Developer (Enrique Vicente)

> Formato: preguntas abiertas, no objeciones. Objetivo: entender el comportamiento actual.

| # | Pregunta | Área | Urgencia |
|---|----------|------|----------|
| P-01 | ¿La **grace execution** (1 ejecución de gracia al agotar saldo) está implementada en el prototipo actual, o el diseño evolucionó a bloqueo directo? | Enforcement | 🔴 Urgente |
| P-02 | ¿El **cron job** mencionado en el comentario del 08-jun para manejar `reset_at` fue reemplazado por lazy resets, o conviven ambos mecanismos en el código actual? | Ledger | 🔴 Urgente |
| P-03 | Cuando `execution_time` se agota y bloquea, ¿qué mensaje recibe el usuario en la UI del canvas/editor? | UX | 🟠 Alto |
| P-04 | ¿Existe algún endpoint API para consultar la última duración de ejecución (IONF-1057) mientras la vista de Board está pendiente de rediseño? | Runtime | 🟠 Alto |
| P-05 | Si falla el envío del meter event a Stripe post-commit, ¿se loggea el error y hay mecanismo de retry? | Stripe | 🟠 Alto |
| P-06 | ¿El esquema de Rodolfo Merlo ya está completamente integrado en el prototipo, o hay partes de IONPDF aún pendientes? | IONPDF | 🟠 Alto |
| P-07 | ¿Qué pasa si falla el provisioning del plan free al crear una company? ¿Hay retry automático? | Provisioning | 🟠 Alto |

---

## Priorización de Casos de Testing

### Tier 1 — Probar primero (bloqueantes)
1. Ciclo de vida completo de suscripción (Active → Canceled → Lapsed → Free)
2. `RecordConsumption` con lazy reset — verificar que `consumed` arranca en `qty`, no en suma
3. `billableDelta` clipping en los 6 escenarios del prototipo
4. Guard de enforcement por tipo de feature (`execution_time`, `pdf_templates`, `pdf_impressions`)
5. payment_failed → revocación de overage → SyncConsumptions

### Tier 2 — Probar en segunda ronda
6. Concurrencia en consumo simultáneo
7. Gates de overage (dunning, feature sin Stripe, plan free, ilimitado)
8. Regresión: Executions, Boards, PDF Templates
9. Idempotencia de meter events con redelivery Stripe

### Tier 3 — Nice to have / cuando UI esté disponible
10. Runtime history en vista de Board
11. Pantalla comercial unificada (IONF-1059 — en `quick prototype`)
12. Emails (body/template final pendiente de definir)

---

## Estado Final

| Campo | Valor |
|-------|-------|
| Preguntas críticas abiertas | 2 (P-01, P-02) |
| Riesgos críticos identificados | 7 (R-01, R-03, R-06, R-11, R-12, R-17, R-32) |
| Riesgos altos | 15 |
| Riesgos medios | 7 |
| Aprobado por QA Engineer | ✅ (Gate 3 — avanzar) |
