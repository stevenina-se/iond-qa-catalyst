# Regression Matrix — v0.1.0

> Generado por `skills/release/regression-matrix`
> Fecha: 2026-06-25
> Versión: **v0.1.0** (Primera release de Ionflow)
> Formato: Template aprobado `Ionflow Testing Plan - Regression Test Template.csv`
> Fuente de tickets: `matched_tickets1.csv` (182 tickets — Sprints + Deployment)

---

## Resumen

| Métrica | Valor |
|---------|-------|
| Versión | v0.1.0 |
| Total de filas en la matriz | 163 |
| Sides cubiertos | KC, ADMIN, TENANT, ADMIN GATEWAY |
| Tickets referenciados | 57 tickets del release |
| Items con Skipped (pendientes de 1.4.x) | 23 (Admin Gateway > Apps > Services) |

---

## Módulos cubiertos

| Side | Módulo | Criticidad (L1) | Tickets relacionados |
|------|--------|----------------|---------------------|
| KC | Login / Auth | 🟠 Alto | IONF-362, IONF-1074 |
| TENANT | Boards / Nodes — All Tools | 🔴 Crítico | IONF-227, IONF-266, IONF-320, IONF-328, IONF-376, IONF-379, IONF-404, IONF-449, IONF-516, IONF-680, IONF-786, IONF-901, IONF-935, IONF-939 |
| TENANT | Boards — Storage (Persistent Data) | 🟠 Alto | IONF-162, IONF-163, IONF-552 |
| TENANT | Boards — ION PDF | 🟠 Alto | IONF-820 |
| TENANT | Boards — Commit/Git | 🔴 Crítico | IONF-419, IONF-482 |
| TENANT | Execution History | 🟠 Alto | IONF-518 |
| TENANT | Webhooks | 🟠 Alto | IONF-449, IONF-695, IONF-786 |
| TENANT | Connections | 🟠 Alto | IONF-141, IONF-142, IONF-146, IONF-165, IONF-327, IONF-554 |
| TENANT | Data Store | 🟠 Alto | IONF-159, IONF-163 |
| TENANT | PDF Templates | 🟠 Alto | IONF-820 |
| TENANT | Credentials | 🟠 Alto | — |
| TENANT | Accounts | 🟠 Alto | — |
| TENANT | Developer Apps | 🟠 Alto | IONF-380 |
| TENANT | Catalog | 🟠 Alto | IONF-103 |
| TENANT | Settings / Teams | 🟡 Medio | IONF-506, IONF-485, IONF-655, IONF-763, IONF-764 |
| ADMIN GATEWAY | Apps | 🟠 Alto | IONF-116, IONF-168, IONF-281 |
| ADMIN GATEWAY | Customer / Channels | 🟠 Alto | IONF-103, IONF-128, IONF-141, IONF-165, IONF-493, IONF-548, IONF-680, IONF-911, IONF-997 |

---

## Tickets del Release Mapeados en la Matriz

| Ticket | Descripción | Fila(s) en la matriz |
|--------|-------------|---------------------|
| IONF-103 | Unificar endpoints creación GRAPPs | ADMIN GATEWAY > Apps > New App; TENANT > Catalog; ADMIN GATEWAY > Customer > Grapp Installation |
| IONF-116 | Crear app de forma manual | TENANT > Connections > Create > Manual Connector; ADMIN GATEWAY > New App |
| IONF-128 | Formulario instalación de un servicio | ADMIN GATEWAY > Customer > Grapp Installation |
| IONF-141 | Revisar errores de Basic Auth en GET | TENANT > Connections > Auth List > Add; ADMIN GATEWAY > Customer > Add a Connection |
| IONF-142 | Refactorización de connections con integraciones | TENANT > Connections > Auth List; ADMIN GATEWAY > Customer > Grapp Connections |
| IONF-146 | Edición de nombres en Connections | TENANT > Connections > List > Base > Edit; Nodes > Edit |
| IONF-159 | Data Store — modal conserva info anterior | TENANT > Data Store > Data Store > Create |
| IONF-162 | Data Store — solapamiento en WebComponent | TENANT > Boards > Storage > Save/Update |
| IONF-163 | Data Store — visualización de datos | TENANT > Boards > Storage > Get; TENANT > Data Store > View |
| IONF-165 | Completar Refresh token | TENANT > Connections > Reauthrize; ADMIN GATEWAY > Customer > Reauthorize |
| IONF-168 | Corregir campos app | ADMIN GATEWAY > Apps > New App |
| IONF-227 | Nodo Switch dinámico | TENANT > Boards > All Tools > Multiple Decision |
| IONF-266 | Nodo Timer | TENANT > Boards > All Tools > Timer |
| IONF-281 | Modales de confirmación para eliminación | TENANT > Boards > Delete; ADMIN GATEWAY > Apps > Delete |
| IONF-320 | Expression language en mappers | TENANT > Boards > All Tools > Mapper |
| IONF-327 | Fix módulos con mismo nombre | TENANT > Connections > Nodes > Add |
| IONF-328 | Call Flow dentro de otro flow | TENANT > Boards > All Tools > Call Component-Flow / On Call Component-Flow |
| IONF-362 | Login SSO con Keycloak | KC > Login with SSO; TENANT > Account > Change Email |
| IONF-376 | Fix casteo en expression language | TENANT > Boards > All Tools > Mapper |
| IONF-379 | Refactorizar motor de ejecución | TENANT > Boards > All Tools > HTTP Request; ADMIN GATEWAY > Boards |
| IONF-380 | Motor de nodos en Go | TENANT > Developer Apps |
| IONF-404 | Fix acumulador en transformer | TENANT > Boards > All Tools > Iterator |
| IONF-406 | Fix recursividad en nodos entrelazados | ADMIN GATEWAY > Boards > Check all nodes |
| IONF-419 | Motor de versionamiento Git | TENANT > Boards > Commit (todas las sub-acciones) |
| IONF-449 | Modificaciones en nodo webhook | TENANT > Boards > All Tools > Webhook/Webhook Response |
| IONF-482 | Restaurar flow mediante git | TENANT > Boards > Commit > Discard Changes |
| IONF-485 | Actualizar tema de la plataforma | TENANT > Settings > Appearance |
| IONF-493 | Agregar botón de reauthentication | ADMIN GATEWAY > Customer > Reauthorize |
| IONF-506 | Vista configuración de company | TENANT > Settings > Edit Company Info |
| IONF-518 | Retirar metadata waiting_for_input | TENANT > Execution History > Data |
| IONF-530 | Mejorar importación de flows | TENANT > Boards > Import |
| IONF-548 | Implementar Check Updates en Grapps | ADMIN GATEWAY > Customer > Grapp Check Updates |
| IONF-551 | Bindeo para Dropdowns y binarios en Form | ADMIN GATEWAY > Customer > Flow/Actions Configuration |
| IONF-552 | Nodos faltantes para Data Storage | TENANT > Boards > Storage (Check, Count, Delete All, Search) |
| IONF-553 | Agregar input tipo Date | ADMIN GATEWAY > Customer > Flow/Actions Configuration |
| IONF-554 | Fix Refresh token in flows | TENANT > Connections > Reauthrize |
| IONF-655 | Permitir más de un usuario por company | TENANT > Teams > Invite Member |
| IONF-657 | Implementar botón de idioma con i18n | TENANT > Language > Change Language |
| IONF-680 | Fix ejecución de Schedule | TENANT > Boards > All Tools > Scheduler; ADMIN GATEWAY > Grapp Schedule |
| IONF-695 | Soportar webhooks en los grapp | TENANT > Connections > Webhooks > Add |
| IONF-763 | Usuario inicial sin todos los permisos | TENANT > Teams > Edit Permissions |
| IONF-764 | Inconsistencias en permisos de UI | TENANT > Teams > Edit Permissions |
| IONF-786 | Fix webhook con content-type | TENANT > Boards > All Tools > Webhook |
| IONF-820 | Nodo exportación PDF + ION PDF | TENANT > Boards > ION PDF (todas las sub-acciones) |
| IONF-899 | URL no se actualiza al crear Board | TENANT > Boards > Edit |
| IONF-901 | Bug mapeo campos select y boolean | TENANT > Boards > All Tools > Form |
| IONF-911 | Grapp schedules | ADMIN GATEWAY > Customer > Grapp Schedule / Grapp Cron |
| IONF-935 | Nodo Aggregate | TENANT > Boards > All Tools > Aggregate |
| IONF-939 | Nodo Code | TENANT > Boards > All Tools > Code |
| IONF-997 | Dynamic wizards for grapps | ADMIN GATEWAY > Customer > Marketplace |
| IONF-1074 | Refactorizar Keycloak — fix login | KC > Login with SSO |

---

## Items Skipped — Pendientes de 1.4.x

Los siguientes ítems del side **ADMIN GATEWAY > Apps > Services** están marcados como `Skipped` porque dependen de la fusión de la rama `1.4.x` a `DEVELOPMENT`. Deben re-evaluarse en la próxima release:

- Set Image, Filter by Slug/Title/Description/Categories/Type
- Enable/Disable in bulk, Enable, Disable
- Edit > Set Image/Title/Details/Description/Features/Groups/Category/Enable Badge/Custom Credentials
- Copy Cart/Install/Callback
- Custom Integrations > Create
- Integrations > List, Claim
- Go Back

---

## Instrucciones de uso

1. **Abrir el CSV** en Google Sheets / Excel: [regression-matrix.csv](file:///c:/Users/STEVE/Desktop/Automation/ionflow-qa-catalyst/knowledge/releases/v0.1.0/regression-matrix.csv)
2. **La columna RESOLUTION** acepta: `Passed`, `Failed`, `Skipped`, `Blocked`
3. **La columna ASSIGNED** indica el tester responsable de cada fila
4. **La columna COMMENTS** es libre para notas durante la ejecución
5. **La columna OBSERVATION** contiene instrucciones pre-existentes (ej. "Verificar en modo Test y modo Produccion")
6. **La columna TICKET** referencia los tickets de v0.1.0 que motivaron ese caso de test
7. **Los ítems sin TICKET** son parte del baseline de regresión — deben ejecutarse aunque no tengan ticket directo

---

## Notas

- Formato basado en: `Ionflow Testing Plan - Regression Test Template.csv`
- Fuente de tickets: `matched_tickets1.csv` (182 tickets reales de ClickUp)
- Tracking list base: `knowledge/releases/v0.1.0/tracking-list.md` *(pendiente de crear)*
- Los items `Skipped` de ADMIN GATEWAY preservan la observación original del template aprobado
- Esta versión se llamó **v0.1.0** — primera release oficial de Ionflow

*Generado por ionflow-qa-catalyst — skill: release/regression-matrix*
*Fecha: 2026-06-25*
