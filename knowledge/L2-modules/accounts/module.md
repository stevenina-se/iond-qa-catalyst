# Módulo: Accounts

> Gestión de cuentas asociadas a las Companies que podrán instalar integraciones (GRAPPs).

## Información General

| Campo | Valor |
|-------|-------|
| Nombre interno | accounts |
| Criticidad | 🟠 Alto |
| Repos involucrados | `gateway-ion` (UI), `gateway` (API) |
| Última actualización | Initial setup — Fase 5 |

---

## Rutas del Frontend (gateway-ion)

| Ruta | Vista | Componente | Permiso |
|------|-------|-----------|---------|
| `/accounts` | Lista de cuentas | `views/tenant/accounts/list.vue` | `READ_ACCOUNT` |

---

## API Endpoints

### Accounts CRUD (gateway — `routes/api.php`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/1.0/accounts` | Lista de cuentas |
| GET | `/1.0/accounts/{account}` | Detalle de cuenta |
| POST | `/1.0/accounts` | Crear cuenta |
| PUT | `/1.0/accounts/{account}` | Actualizar |
| DELETE | `/1.0/accounts/{account}` | Eliminar |

### App API (acceso programático)

| Método | Endpoint | Scope | Descripción |
|--------|----------|-------|-------------|
| GET | `/2.0/app/accounts` | `app:account-read` | Lista de accounts |
| GET | `/2.0/app/accounts/{remote_id}` | `app:account-read` | Detalle por remote_id |
| POST | `/2.0/app/accounts` | `app:account-create` | Crear account |
| PUT | `/2.0/app/accounts/{accountId}` | `app:account-update` | Actualizar |
| POST | `/2.0/app/intent/{account:remote_id}` | `app:intent-create` | Crear intent para account |

### Webcomponent API

| Método | Endpoint | Scope | Descripción |
|--------|----------|-------|-------------|
| GET | `/2.0/webcomponent/account` | `account-read` | Datos del account actual |

---

## Contexto de flow_binaries

> Los accounts son referenciados en flow_binaries a través del `clientPath` (ruta al data store del account).
> Cuando un flow se ejecuta en el contexto de un GRAPP, el `clientPath` apunta al data store específico del account.
> Esto permite que las ejecuciones de store nodes (Persistent Data) operen sobre los datos del account correcto.

---

## Impacto Cruzado

### Módulos que Accounts afecta
| Módulo destino | Componente afectado | Tipo | Ejemplo |
|---------------|--------------------|-----------------|---------| 
| **Integrations** | Integraciones instaladas | Datos | Las accounts instalan integraciones |
| **Developer Apps** | Apps vinculadas | Datos | Las dev apps se vinculan a accounts |
| **Services** | Services usados | Datos | Las accounts usan services del catálogo |
| **Billing** | Suscripciones | Datos | Las accounts pueden tener suscripciones (polimórfico) |

### Módulos que afectan a Accounts
| Módulo origen | Componente | Tipo | Ejemplo |
|--------------|------------|-----------------|---------| 
| **Auth** | Gestión de cuentas | API | Solo users autorizados gestionan accounts |

---

## Historial de Actualizaciones

| Fecha | Tickets | Cambios | Actualizado por |
|-------|---------|---------|----------------|
| Initial | — | Creación inicial | QA Catalyst |
| 2026-06-07 | — | Impacto Cruzado | QA Catalyst |
