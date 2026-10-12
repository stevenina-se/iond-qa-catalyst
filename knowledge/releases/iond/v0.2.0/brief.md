# Brief del release — iond v0.2.0 (beta) + IonMind v1.10.2

> Resumen de una página para stakeholders y líderes. Se regenera al cerrar cada suite (skill `release/brief`) y no reemplaza a los comentarios C-23 a C-31 de las tareas de Release.

**Estado de la tarea:** `dev preparation` · **Actualizado:** 2026-10-10 · **Go/No-Go:** viernes 2026-10-16 10:00

## Alcance

Primera versión **beta** de iond con el nuevo modelo de pruebas. Llegan:

- el marketplace con pagos a vendedores;
- el control de consumo por plan;
- la API pública 2.0;
- la nueva marca iond, con dominios, emails y landing;
- el acceso de soporte para administradores;
- un motor de ejecución más robusto, con historial y replay;
- el menú reorganizado y notificaciones en tiempo real;
- mejoras en la creación de conectores con IonMind.

IonMind v1.10.2 acompaña la versión con los logos vía Logo.dev.

| Dato | Valor |
|---|---|
| Tickets incluidos | **84** — iond 79 (49 principales + 30 subtareas) · IonMind 5 (2 + 3) |
| Principales por tipo | Correcciones 22 · Nuevas funcionalidades 12 · Mejoras 8 · Reestructuraciones 6 · Tareas 3 |
| Módulos | App Connectors e IonMind (12) · Grapps, Webhooks, Connections, Templates y registro (7) · Motor y ejecución (6) · Nodos del canvas (5) · Boards (4) · PDF Templates (4) · Navegación (3) · Marketplace (2) · Billing (2) · Flow Pilot (2) · Accesos de soporte (2) · Rebranding (1) · API 2.0 (1) |
| Diferidos | Ninguno por ahora. Una definición de precios entra como informativa, sin pruebas. |

## Riesgo

**Alto**: toca cobros y consumo, pagos del marketplace, accesos, el motor de ejecución y un contrato de API externa. Hay unos 140 puntos de prueba en una semana, así que las suites están **priorizadas**: lo crítico se prueba completo y lo demás queda cubierto por la regresión automatizada o se registra para la decisión del viernes.

**Dependencia:** IonMind se despliega antes que iond.

## Avance por suite

| Paso | Suite | Estado | Resultado | Nota |
|---|---|---|---|---|
| 1 | Smoke maestro (preprod) | ⬜ Pendiente | —/16 | Lunes PM – martes AM · gate del release |
| 2 | Sanity (criterios críticos de cada ticket) | ⬜ Pendiente | —/183 | Martes – miércoles |
| 3 | Regression capa 1 (por riesgo) | ⬜ Pendiente | Flujos críticos —/106 | Jueves |
| 4 | E2E maestro capa 2 | ⬜ Pendiente | Automatizado —/71 · rotación G1 —/11 | Jueves noche |
| 5 | Go/No-Go | ⬜ Pendiente | — | Viernes 10:00 · PO + LQA + RM |
| 6 | Smoke en producción | ⬜ Pendiente | —/16 | ≤ 2 h tras el despliegue |

## Hallazgos

| Severidad | Abiertos | Tratamiento |
|---|---|---|
| `urgent` | 0 | Corrección en la versión (fix-forward) o retiro del cambio |
| `high` | 0 | Requiere aceptación del riesgo por el PO |
| `normal` / `low` | 0 | Mejoras programadas en Improvements |

En la preparación aparecieron **28 observaciones**: desvíos aprobados respecto de lo pedido, validaciones incompletas y datos a corregir. El PO decide sobre ellas el miércoles. Las que pueden frenar la salida son tres:

- la integración del marketplace tenía un rechazo de QA sin cerrar;
- un posible acceso cruzado entre clientes en la actualización de logos;
- la confirmación de que todas las correcciones de IonMind entran a la versión.

## Decisión y despliegue

**Decisión:** pendiente · **Ventana:** viernes 2026-10-16, antes de las 14:00, con DevOps (IonMind → iond) · **Release notes:** se preparan el viernes por la mañana

## Pendientes y bloqueos

| Pendiente | Responsable (rol) | Fecha |
|---|---|---|
| Aplicar las acciones de ClickUp (versiones, tareas de Release, datos) | SM · RM | 2026-10-11 |
| Cerrar la validación de las notificaciones en tiempo real (websockets) | QA | 2026-10-11 |
| Corte, ramas de la versión y despliegue en preprod | RM · LD | 2026-10-12 09:00 |
| Company de prueba en producción para el smoke post-despliegue | LD · DevOps | 2026-10-15 |
| Decisiones sobre las observaciones de preparación | PO | 2026-10-14 |

## Texto corto para el canal del equipo (≤ 10 líneas)

```text
📦 iond v0.2.0 (beta) + IonMind v1.10.2 — preparación lista
Alcance: 84 tickets (12 nuevas funcionalidades, 22 correcciones, 8 mejoras, 6 reestructuraciones, 3 tareas en los principales)
Riesgo: Alto — cobros y consumo, pagos, accesos, motor y API externa; suites priorizadas
Smoke ⬜ (lun–mar) · Sanity ⬜ (mar–mié) · Regresión ⬜ (jue) · E2E ⬜ (jue noche)
Observaciones para el PO: 28 (revisión el miércoles)
Go/No-Go: viernes 16/10 10:00 · Ventana: viernes antes de las 14:00 (IonMind → iond)
```
