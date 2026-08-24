# QA FOUND ISSUE ESCALATION REPORT — SCHEDULER / EXECUTION ENGINE

> Template generado por `skills/bug-reporter/create`
> Fecha: 2026-08-23
> QA Engineer: Steve Nina

---

## Información General

| Campo | Valor |
|-------|-------|
| Módulo(s) afectado(s) | Scheduler, Execution Engine |
| Path de navegación | `Company > Boards > [Flow] > Scheduler` |
| Entorno | dev-app.ionflow.io |
| Rama | DEVELOPMENT |
| Prioridad | `normal` |
| Tipo | `improvement` |
| Origen | OBS-R02 del ticket 86e1pzyug (IONF-1056-B) |
| Ticket relacionado (causa) | `86e1mdnbq` — Sincronización de logs con R2 |

---

## Description of the validated/replicated problem

Durante el testing del ticket 86e1pzyug (Monetización unificada — IONF-1056-B), se observó un comportamiento no documentado del scheduler al ejecutar múltiples flows con un intervalo de 1 minuto. Los 8 flows configurados **no se ejecutaron simultáneamente**: primero se ejecutaron 5, y solo después de completarse (~1 min), se ejecutaron los 3 restantes. Además, cuando el primer grupo de 5 flows demoró más de 1 minuto, el siguiente ciclo del scheduler **no se disparó al cumplirse el minuto**, sino que esperó a que finalizara el ciclo anterior.

El developer (Enrique Vicente) identificó que este comportamiento fue introducido por el ticket `86e1mdnbq` (Sincronización de logs con R2), que limitó la concurrencia máxima de Cron Jobs a **5 jobs simultáneos** e implementó la regla de que **un ciclo de ejecuciones no puede iniciarse hasta que termine el anterior**. Dado que este comportamiento no está relacionado con el motor de consumos/billing, se recomienda definir y documentar el comportamiento esperado en un ticket independiente.

---

## Steps to Reproduce

1. Company Login > Boards > Crear 8 flows con nodo PDF (o cualquier nodo que tome tiempo)
2. Configurar un scheduler para cada flow con intervalo de **1 minuto**
3. Observar la primera ejecución del scheduler
4. Notar que solo **5 de los 8 flows** se disparan simultáneamente
5. Los 5 flows demoran ~1 minuto y algunos segundos en completarse
6. Después se disparan los **3 flows restantes** (~30 seg)
7. Observar que el siguiente ciclo del scheduler **no se disparó** al cumplirse el segundo minuto (mientras los primeros 5 aún estaban ejecutándose)
8. Recién al finalizar el ciclo completo (5 + 3), se inicia el siguiente ciclo

---

## Datos utilizados

| Dato | Valor |
|------|-------|
| Usuario / Rol | Company (tenant user) |
| URL / Endpoint | Scheduler interno de flow_binaries |
| ID(s) de entidad | 8 flows con scheduler cada 1 minuto |
| Versión | DEVELOPMENT |
| Ambiente | dev-app.ionflow.io |
| Ticket que introdujo el comportamiento | 86e1mdnbq |

---

## Current Behavior

El scheduler opera con las siguientes restricciones (introducidas por el ticket `86e1mdnbq`):

1. **Concurrencia máxima de 5 jobs**: Solo 5 flows se ejecutan simultáneamente. Los restantes esperan a que alguno termine.
2. **Ciclo secuencial**: Un nuevo ciclo de ejecuciones no puede iniciarse hasta que finalice el anterior, incluso si el intervalo del scheduler (ej. 1 minuto) ya se cumplió.

### Evidencia observada

```
Minuto 0:00 → Se disparan 5 de 8 flows
Minuto ~1:05 → Finalizan los 5 flows, se disparan los 3 restantes
Minuto ~1:35 → Finalizan los 3 flows
Minuto ~1:35+ → Recién se disparan los 5 flows del siguiente ciclo
```

---

## Expected Behavior

Definir y documentar el comportamiento esperado del scheduler bajo las siguientes condiciones:

1. **¿Cuántos flows se deben ejecutar simultáneamente?** — ¿El límite de 5 es configurable? ¿Debe ser por company o global?
2. **¿Qué pasa cuando los flows tardan más que el intervalo del scheduler?** — ¿Se encolan las ejecuciones perdidas? ¿Se descartan? ¿Se ejecutan inmediatamente al terminar el ciclo anterior?
3. **¿El intervalo se mide desde el inicio del ciclo o desde el fin?** — Esto determina si un scheduler de 1 minuto con flows que tardan 2 minutos produce 30 ejecuciones/hora o 20 ejecuciones/hora.

---

## Impacto

| Aspecto | Detalle |
|---------|---------|
| Usuarios afectados | Todos los tenants que usan schedulers con múltiples flows |
| Flujos bloqueados | Ninguno bloqueado — es un comportamiento existente no documentado |
| ¿Tiene workaround? | Sí — configurar intervalos más largos que consideren la demora de ejecución |

---

## Notas Adicionales

- El comportamiento fue descubierto durante el testing de billing/consumption guards (ticket 86e1pzyug), pero **no es un defecto del motor de consumos**. Es un comportamiento arquitectónico del scheduler introducido por el ticket de sincronización con R2 (`86e1mdnbq`).
- El developer (Enrique Vicente) confirmó que este es el comportamiento actual y recomendó crear un ticket independiente para definir formalmente el comportamiento esperado.
- Puntos a considerar en la definición:
  - Impacto en el consumo de `execution_time` cuando flows se encolan vs ejecutan
  - Comportamiento del guard de consumo cuando hay flows encolados
  - Configurabilidad del límite de concurrencia por company o por plan
