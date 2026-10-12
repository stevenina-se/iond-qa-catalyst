# QA-AUTO-SMOKE-001 — Smoke maestro automatizado (Ola 1)

> Propuesto el 2026-10-10. Ticket a crear en QA Kanban (`901705382240`) por el LQA.
> Fuente del alcance: `knowledge/test-suites/smoke-master.md`. Prioridad: 🔴 Urgent (Ola 1 de `knowledge/test-suites/automation-roadmap.md`).

## Contexto

### Descripción
Automatizar las verificaciones del smoke maestro que todavía no tienen test, de modo que el smoke completo corra en preprod (gate del release) y en producción con la company de prueba (post-despliegue) en ≈ 15 minutos. Los tests nuevos llevan las etiquetas `@smoke` y, cuando corresponda, `@prod-safe`.

### Módulos afectados
- Principal: `Tenant / Boards` (board de smoke de punta a punta) y `Tenant / Execution History`
- Relacionados: Webhooks, Connections, App Connectors, Persistent Data, Credentials, Subscription, health de servicios (iond, IonMind, StageMind)

### Requisitos previos (Ola 0, AV-11)
- PR de la rama `test/ionflow-tenant-e2e` integrado.
- Perfiles de variables por ambiente (preprod y company de prueba) y etiqueta `@smoke` acordada.
- Company de prueba en producción con la plantilla PDF fija `autobot-smoke-template` (AV-09).
- Endpoints de health definidos por el LD.

---

## Test Cases

| ID | SMK | Tipo | Caso | Prioridad | Estado |
|----|-----|------|------|-----------|--------|
| TC-SMOKE-01 | SMK-03 | Happy Path | Crear board `autobot-smoke-<fecha>` con trigger Webhook + nodo HTTP Request/Code y hacer commit | 🔴 | ⬜ |
| TC-SMOKE-02 | SMK-04 | Happy Path | Ejecutar el board en test: resultado por nodo exitoso | 🔴 | ⬜ |
| TC-SMOKE-03 | SMK-05 | Happy Path | Activar el board, disparar el webhook y verificar la ejecución en Execution History con detalle por nodo; pausar y eliminar el board | 🔴 | ⬜ |
| TC-SMOKE-04 | SMK-06 | Happy Path | Listado de Webhooks carga sin errores | 🟠 | ⬜ |
| TC-SMOKE-05 | SMK-07 | Happy Path | Listados de Connections y App Connectors cargan sin errores | 🟠 | ⬜ |
| TC-SMOKE-06 | SMK-08 | Happy Path | Persistent Data: pestañas Data Store y Data Structure cargan (solo lectura) | 🟠 | ⬜ |
| TC-SMOKE-07 | SMK-10 | Happy Path | Listado de Credentials carga sin errores | 🟠 | ⬜ |
| TC-SMOKE-08 | SMK-12 | Happy Path | Suscripción: plan vigente y consumo visibles | 🟠 | ⬜ |
| TC-SMOKE-09 | SMK-15 | API | Health de iond, IonMind y StageMind responde OK | 🔴 | ⬜ |

Las verificaciones SMK-02, SMK-09, SMK-11 y SMK-16 reutilizan tests existentes (`TC-DASH-01`, `TC-PDF-21`, `TC-NOTIF-01`, `TC-BOARD-FP-01/02`) con la etiqueta `@smoke`. SMK-01 y SMK-13 dependen de corregir las specs de login y companies (Ola 0).

---

## Notas de Automatización
- Datos: todo con prefijo `autobot-smoke-` y limpieza en `afterAll`; en producción, solo con la company de prueba.
- SMK-05 no debe depender del scheduler (usar el trigger Webhook para que la prueba sea rápida y determinista).
- Comando objetivo: `npx playwright test --config=tests/IONFLOW/playwright.ionflow.config.ts -g @smoke` (y `-g "@smoke.*@prod-safe|@prod-safe.*@smoke"` en producción, o el filtro que defina el responsable de bot-test).
