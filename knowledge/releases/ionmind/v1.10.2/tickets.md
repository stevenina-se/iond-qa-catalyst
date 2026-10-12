# Tickets — IonMind v1.10.2

> Salida de `release/ingest` para IonMind dentro de la beta (tag `iond-beta`). Datos leídos de ClickUp en **solo lectura** el 2026-10-10. Inventario completo de la beta: `knowledge/releases/iond/v0.2.0/tickets.csv`.

## Tickets propios (5)

| Ticket | IONF | Título | Nivel | Estado | Project | PRs | Veredicto QA | Sanity | Version objetivo |
|---|---|---|---|---|---|---|---|---|---|
| [86e2t9962](https://app.clickup.com/t/86e2t9962) | IONF-1253 | El estado de minado de un endpoint no se actualiza en tiempo real en App Connector | Principal | `ready to merge` | IONMIND | — (reinicio de pods, sin código) | APROBADO 2026-08-19 (Mijael Rojas) | `high` | Ionmind.Version v1.10.2 |
| [86e1fknjv](https://app.clickup.com/t/86e1fknjv) | IONF-1022 | Integrar Logo.dev como fallback en el pipeline de logos de IonMind | Principal | `ready to merge` | IONMIND | — (en subtareas) | Sin veredicto de QA | `urgent` (revalidación) | Ionmind.Version v1.10.2 |
| [86e1fkxz7](https://app.clickup.com/t/86e1fkxz7) | IONF-1023 | Backend - Integrar Logo.dev y API de actualización en IonMind | Subtarea | `ready to merge` | IONMIND | ai_ionmind#8 | Sin QA propio | `urgent` | Ionmind.Version v1.10.2 |
| [86e1fky0g](https://app.clickup.com/t/86e1fky0g) | IONF-1024 | Frontend - Atribución condicional y acción manual de Logo.dev en IonFlow | Subtarea | `ready to merge` | Iond | ion_gateway_ion#17 | Sin QA propio | `urgent` | Ionmind.Version v1.10.2 · Iond.Version v0.2.0 |
| [86e1qzefc](https://app.clickup.com/t/86e1qzefc) | — | Actualización del Backend de IonFlow | Subtarea | `ready to merge` | Iond | ion_gateway#16 | Sin QA propio | `urgent` (con AC-SEC) | Ionmind.Version v1.10.2 · Iond.Version v0.2.0 |

86e1fky0g y 86e1qzefc tienen el código en repos de iond: el RM los incluye en la RC de iond y se despliegan con iond, después de IonMind.

## PRs de tickets de iond en `ai_ionmind`

Entran a la RC de IonMind y siguen en el inventario de iond. Llevan las dos versiones.

| PR | Ticket (iond) | Tema |
|---|---|---|
| ai_ionmind#3 | 86e20nmqx | Confirmación y cobro de la primera extracción |
| ai_ionmind#11 | 86e2e8gde | Conectores UPS Track Alert y FedEx Supply Chain |
| ai_ionmind#12 | 86e2ft73m (subtarea de 86e2fazfh) | Descripciones de endpoints en el Discovery |
| ai_ionmind#16 | 86e2p459r | Errores de IonMind en la UI (REQ 5 diferido) |
| ai_ionmind#17 | 86e2j43eg | Conectores de mensajería |
| ai_ionmind#21 | 86e2mt70g | Tier de IA para la generación de conectores |
| ai_ionmind#25 | 86e25j0rn | Notificaciones de fallo de Discovery |
