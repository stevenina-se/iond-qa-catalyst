# AC Consolidado — IONF-1076 / 86e1r4bu7 (Community Templates)

> Discovery Express — Basado en ticket ClickUp + 16 observaciones de Ronda 1 QA.
> Repos: `flow_binaries`, `gateway`, `gateway-ion` (branch IONF-1076)

## Fuentes

- Ticket ClickUp: `86e1r4bu7`
- PRs originales: [flow_binaries#15](https://github.com/altacrest/ion_flow_binaries/pull/15), [gateway#15](https://github.com/altacrest/ion_gateway/pull/15), [gateway-ion#14](https://github.com/altacrest/ion_gateway_ion/pull/14)
- PRs de fix (Ronda 2): [gateway#25](https://github.com/altacrest/ion_gateway/pull/25), [gateway-ion#25](https://github.com/altacrest/ion_gateway_ion/pull/25)
- Developer: Alex Chura
- Code Review: ✅ Approved (Enrique Vicente 2026-07-24, Rodolfo Merlo 2026-07-27)
- Deploy: Confirmado por Rodolfo (2026-07-30)
- QA Ronda 1: ❌ Rejected por Mijael (2026-07-22) — 16 observaciones

## Acceptance Criteria (extraídos del ticket)

### AC-1: Pantalla de templates habilitada en todas las cuentas
- La pantalla de templates/ejemplos documentados debe estar disponible para todos los usuarios y empresas de Ionflow
- Cada usuario debe poder acceder a la galería de templates desde su cuenta

### AC-2: Templates básicos aparecen por defecto
- Los boards iniciales creados deben aparecer por defecto en todas las cuentas
- Estos templates son los mismos mínimos disponibles para todas las cuentas

### AC-3: Separación catálogo global vs boards personales
- Los templates globales NO deben aparecer en la lista personal de boards del usuario
- Solo aparecen en su lista después de copiarlos/importarlos a su espacio

### AC-4: Copia/importación editable de templates
- Cuando el usuario elija usar un ejemplo, se crea una copia editable en su cuenta/empresa
- El usuario puede editar nodos, conexiones y configuración sin afectar el template original

### AC-5: Admin CRUD de templates
- Panel de administración con listado paginado, filtros, creación, edición, eliminación de templates
- Asignación de categorías con chips de color
- Cambio de estado (activo/inactivo)

### AC-6: Marketplace tenant con previsualización
- Listado de templates activas con destacados, búsqueda y cuadrícula
- Drawer de previsualización del template
- Vista de apps y PDFs del template fuente

### AC-7: Instalación con wizard
- Asistente de instalación multi-paso con mapeo de conexiones
- Clonación automática de PDFs con remapeo de IDs
- Toasts de confirmación al instalar

### AC-8: Auto-registro/sincronización
- Al crear/actualizar/eliminar un flujo o PDF en un tenant → sincronización automática en tabla `templates`
- Restricción única: `(company_id, type, original_id)`

### AC-9: Ejemplos orientados a ecommerce/Shipedge
- Los templates deben priorizar casos de ecommerce, fulfillment, inventario, órdenes
- Deben usar conectores propios o estratégicos disponibles en Ionflow

### AC-10: Credenciales seguras
- Los ejemplos NO deben exponer credenciales reales
- Al copiar un template, el sistema no reutiliza credenciales sensibles del original

## Observaciones Ronda 1 (resueltas por developer)

> Las 16 observaciones de Mijael fueron reportadas como resueltas por Alex Chura (2026-07-23).
> Deben ser RE-VERIFICADAS en Ronda 2.

| OBS ID | Severidad | Área | Descripción resumida |
|--------|-----------|------|---------------------|
| OBS-01 | 🔴 Urgent | Admin > Buscador Compañías | Buscador de compañías inoperativo al crear template |
| OBS-02 | 🔴 Urgent | Admin > Validación JSON | JSON sin nodos aceptado como válido para crear template |
| OBS-03 | 🔴 Urgent | Admin > Validación Estado | Templates PDF en Draft sin campos permitidos sin validación |
| OBS-04 | 🔴 Urgent | Admin > Filtro Activos | Filtro por activos/inactivos no funciona en tabla |
| OBS-05 | 🔴 Urgent | Admin > Campos No Editables | Campos no editables con mismo estilo que editables |
| OBS-06 | 🔴 Urgent | Admin > Modal Cerrar | Botón cerrar del modal falla con nombres largos |
| OBS-07 | 🟡 High | Admin > Diseño Modal | Modal de creación se rompe con nombres largos |
| OBS-08 | 🟡 High | Admin > Tabla | Tabla se estira con nombres largos |
| OBS-09 | 🟡 High | Tenant > Card | Card se rompe con nombres largos |
| OBS-10 | 🟡 High | Admin > Tabla Recarga | No existe botón de recarga en tabla |
| OBS-11 | 🟡 High | Admin > Selector Compañías | Selector muestra solo 5 compañías |
| OBS-12 | 🟡 High | Admin > Filtro Flows | Flows sin nodos no filtrados (cambiado a alerta) |
| OBS-13 | 🟡 High | Tenant > Tags Card | Sin límite de tags por card |
| OBS-14 | 🟡 High | Tenant > Expandir Tags | Sin funcionalidad expandir/colapsar tags |
| OBS-15 | 🟡 High | Tenant > Tamaño Tags | Tags sin límite de longitud rompen chip |
| OBS-16 | 🟡 High | Tenant > Labels Español | Labels desfasados en idioma español |

## Cambios Técnicos (del developer)

### Repos y cambios principales
- **flow_binaries**: Modelo `Template` con auto-registro fire-and-forget, endpoints de previsualización (`GetTemplateApps`, `GetTemplatePdfs`), endpoint catálogo global `/admin/apps-nodes`, función `toBase64Raw`, servicio `FindPdfTemplatesByIds`
- **gateway**: Tabla `templates` (JSONB, status, type flow/pdf, parent_id, company_id, original_id), tabla pivote `template_category`, columna `color` en `categories`, `TemplateController` completo con CRUD paginado + filtros
- **gateway-ion**: Panel admin (`TemplateTableList.vue`, `NewTemplateDialog.vue`, `EditTemplateDrawer.vue`), Marketplace tenant (`TemplateList.vue`, `TemplatePreviewDrawer.vue`, `TemplateInstallWizardDialog.vue`), composable `useTemplateInstaller.ts`, i18n completo (EN/ES, 207 claves)

### Nota importante del developer
> 🔒 **Boards Privados — Pendiente de implementación**
> No se implementó la funcionalidad de boards privados ya que el sistema de planes y billing aún está en desarrollo. Todos los boards son públicos por defecto.

### Cambio de enfoque en OBS-12
> El filtrado de flows sin nodos ejecutables por backend fue cambiado: ahora se muestra una **alerta que impide importar** los flows sin nodos ejecutables (en lugar de filtrarlos del listado).
