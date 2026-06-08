# Módulo: Keys (Credentials / LLMs)

> Gestión de credenciales de los usuarios para sus LLMs y servicios externos.

## Información General

| Campo | Valor |
|-------|-------|
| Nombre interno | keys / credentials |
| Criticidad | 🟠 Alto |
| Repos involucrados | `gateway-ion` (UI), `gateway` (API) |
| Última actualización | Initial setup — Fase 5 |

---

## Rutas del Frontend (gateway-ion)

| Ruta | Vista | Componente | Permiso |
|------|-------|-----------|---------|
| `/keys` | Lista de keys | `views/tenant/keys/KeyListView.vue` | `READ_KEY` |

---

## Schema de BD (PostgreSQL — gateway)

- `2024_05_30_031616_create_credentials_table.php`
- `2026_04_23_200000_create_keys_table.php`

---

## Reglas de Negocio

1. Almacena credenciales de acceso a LLMs de los usuarios
2. Las credenciales son sensibles y deben manejarse de forma segura
3. Cada key pertenece a una company

---

## Impacto Cruzado

### Módulos que Keys afecta
| Módulo destino | Componente afectado | Tipo | Ejemplo |
|---------------|--------------------|-----------------|---------| 
| **Boards** | Flows con nodos AI | Ejecución | Sin keys configuradas, nodos Agent fallan |
| **Nodes** | Agent node | Ejecución | Agent node necesita API key de LLM para funcionar |

### Módulos que afectan a Keys
| Módulo origen | Componente | Tipo | Ejemplo |
|--------------|------------|-----------------|---------| 
| **Auth** | Permisos | API | Solo users autorizados gestionan keys |

---

## Historial de Actualizaciones

| Fecha | Tickets | Cambios | Actualizado por |
|-------|---------|---------|----------------|
| Initial | — | Creación inicial | QA Catalyst |
| 2026-06-07 | — | Impacto Cruzado | QA Catalyst |
