# Módulo: Dashboard

> Vistas informativas del dashboard de Ionflow.

## Información General

| Campo | Valor |
|-------|-------|
| Nombre interno | dash / dashboard |
| Criticidad | 🟢 Bajo |
| Repos involucrados | `gateway-ion` (UI), `gateway` (API) |
| Última actualización | Initial setup — Fase 5 |

---

## Rutas del Frontend (gateway-ion)

| Ruta | Vista | Componente | Permiso |
|------|-------|-----------|---------|
| `/dashboard` | Dashboard tenant | `views/tenant/dash/index.vue` | `READ_DASHBOARD` |
| `/admin/dashboard` | Dashboard admin | `views/admin/dashboard/index.vue` | Admin |

---

## Reglas de Negocio

1. Errores aquí no bloquean operaciones
2. Muestra información estadística del uso de Ionflow

---

## Impacto Cruzado

### Módulos que Dashboard afecta
| Módulo destino | Componente afectado | Tipo | Ejemplo |
|---------------|--------------------|-----------------|---------| 
| Ninguno | — | — | Dashboard es solo lectura, no afecta otros módulos |

### Módulos que afectan a Dashboard
| Módulo origen | Componente | Tipo | Ejemplo |
|--------------|------------|-----------------|---------| 
| **Executions** | Stats de ejecuciones | Datos | Dashboard muestra métricas de ejecuciones |
| **Boards** | Conteo de flows | Datos | Dashboard muestra cantidad de flows |
| **Auth** | Permisos | API | `READ_DASHBOARD` requerido |
| **Billing** | Tier (Fase 2) | Datos | Futuro: dashboard podría mostrar consumo vs límite |

---

## Historial de Actualizaciones

| Fecha | Tickets | Cambios | Actualizado por |
|-------|---------|---------|----------------|
| Initial | — | Creación inicial | QA Catalyst |
| 2026-06-07 | — | Impacto Cruzado | QA Catalyst |
