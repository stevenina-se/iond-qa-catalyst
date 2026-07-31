# Test Plan — IONF-1076 / 86e1r4bu7 (Community Templates)

> Ronda 2 — Re-verificación de 16 observaciones + testing completo del feature

## Scope

### Feature
Sistema completo de community templates con:
- Panel Admin: CRUD, filtros, categorías
- Marketplace Tenant: galería, búsqueda, preview, instalación
- Auto-registro: sincronización de flows/PDFs como templates
- Wizard de instalación: mapeo de conexiones, clonación de PDFs

### Repos afectados
| Repo | Branch | Componentes |
|------|--------|-------------|
| `flow_binaries` | DEVELOPMENT (merged IONF-1076) | Modelo Template, endpoints preview, toBase64Raw |
| `gateway` | DEVELOPMENT (merged IONF-1076) | Tabla templates, TemplateController, migraciones |
| `gateway-ion` | DEVELOPMENT (merged IONF-1076) | Panel admin, marketplace tenant, wizard, i18n |

### Entorno
- URL: `https://dev-app.ionflow.io`
- Admin: `admin@shipedge.com` / `Admin123`
- Company: `skuanquis@gmail.com` / `.Shipedge12345`
- Auth: Keycloak SSO (`Development_Testing`)

## Estrategia de Testing

### Enfoque Ronda 2
1. **Smoke Tests** — Verificar que templates carga y es accesible
2. **Re-verificación OBS** — Re-testear las 16 observaciones como prioridad
3. **Happy Path** — Flujos principales del feature (CRUD admin, marketplace tenant, instalación)
4. **Edge Cases** — Nombres largos, datos vacíos, límites
5. **Negativos** — Permisos, validaciones, errores controlados
6. **Regresión** — Boards existentes no afectados, PDF templates siguen funcionales
7. **DB Evidence** — Verificar tabla `templates`, pivote `template_category`

### Risk Triage
| Área | Riesgo | Prioridad | Justificación |
|------|--------|-----------|---------------|
| Admin > Buscador compañías | Alto | 🔴 | OBS-01 era bloqueante, fix debe verificarse |
| Admin > Validación JSON/campos | Alto | 🔴 | OBS-02/03 permitían templates vacíos |
| Admin > Filtro activos | Alto | 🔴 | OBS-04 filtro completamente inoperativo |
| Admin > Campos no editables | Alto | 🔴 | OBS-05 UX confusa con errores tardíos |
| Admin > Overflow nombres largos | Alto | 🟠 | OBS-06/07/08 rompen layout y bloquean |
| Tenant > Cards con nombres largos | Medio | 🟠 | OBS-09 desbordamiento visual |
| Tenant > Tags sin límite | Medio | 🟠 | OBS-13/14/15 diseño se rompe |
| Tenant > i18n español | Medio | 🟠 | OBS-16 labels desfasados |
| Admin > Selector compañías limitado | Medio | 🟠 | OBS-11 solo 5 registros |
| Admin > Filtro flows sin nodos | Medio | 🟠 | OBS-12 cambio de enfoque (ahora alerta) |
| Instalación wizard | Alto | 🔴 | Flujo crítico: clonación PDFs + remapeo IDs |
| Multi-tenant isolation | Alto | 🔴 | Templates no deben cruzar datos entre tenants |
| Auto-registro sync | Medio | 🟠 | Fire-and-forget — verificar sincronización |

## Bloques de Ejecución

### Bloque 0 — Pre-requisitos
- [ ] Code review QA completado
- [ ] Repos actualizados en DEVELOPMENT
- [ ] Entorno accesible

### Bloque 1 — Smoke Tests
- Acceso a Templates desde Admin
- Acceso a Templates desde Tenant
- Carga sin errores en consola

### Bloque 2 — Happy Path
- Admin: Crear template (flow + PDF)
- Admin: Editar template
- Admin: Eliminar template
- Admin: Asignar categorías
- Tenant: Ver galería de templates
- Tenant: Preview de template
- Tenant: Instalar template con wizard
- Verificar copia editable del template instalado

### Bloque 3 — Re-verificación OBS (16 observaciones)
- OBS-01 a OBS-06: Re-testear (eran 🔴 Urgent)
- OBS-07 a OBS-16: Re-testear (eran 🟡 High)
- OBS-12: Verificar nuevo enfoque (alerta en lugar de filtro)

### Bloque 4 — Edge Cases
- Nombres extremadamente largos (>100 chars)
- Templates con muchas categorías/tags
- Flows sin nodos → comportamiento de alerta
- JSON vacío o malformado
- Múltiples instalaciones del mismo template

### Bloque 5 — Negativos
- Permisos: usuario sin permiso accede a admin templates
- Credenciales: template instalado no hereda credenciales del original
- Estado: template inactivo no visible en marketplace tenant

### Bloque 6 — Regresión
- Boards existentes siguen funcionando
- PDF templates existentes no afectados
- Flows se ejecutan normalmente
- Login/auth sin impacto

### Bloque 7 — DB Evidence
- Tabla `templates`: verificar registros después de CRUD
- Tabla `template_category`: verificar pivote de categorías
- Columna `color` en `categories`: verificar persistencia
- Multi-tenant: `company_id` correcto en cada registro
