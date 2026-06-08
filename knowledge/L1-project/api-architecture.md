# Arquitectura de APIs — Ionflow

> Ionflow consta de 4 repositorios principales + 1 de automatización E2E. Este documento describe la arquitectura, responsabilidades y relaciones entre ellos.

## Mapa de Repositorios

```
┌──────────────────────────────────────────────────────────────────────┐
│                        USUARIO (Browser)                             │
└─────────────────────────────┬────────────────────────────────────────┘
                              │
                    ┌─────────▼──────────┐
                    │   gateway-ion       │
                    │   (Vue 3 + TS)      │
                    │   Frontend SPA      │
                    │                     │
                    │  Importa via CDN:   │
                    │  webcomponents-flow │
                    └──────┬──────┬───────┘
                           │      │
              ┌────────────▼┐    ┌▼────────────┐
              │ flow_binaries│    │  gateway     │
              │   (Go)       │    │  (PHP 8.2)   │
              │              │    │              │
              │ Core engine  │    │ Auth (SSO    │
              │ Nodes logic  │    │  Keycloak)   │
              │ Flow exec    │    │ Users/Roles  │
              └────┬───┬─────┘    └──────┬───────┘
                   │   │                │
                   │   │    ┌───────────┘
                   │   │    │
         ┌─────────▼┐  │    │
         │  SQLite    │  │    │
         │ (ejecución │  │    │
         │ de nodos)  │  │    │
         └───────────┘  │    │
                       │    │
              ┌────────▼────▼─────┐
              │    PostgreSQL        │
              │    (via SSH tunnel)  │
              └─────────────────────┘
```

## Detalle de Cada Repositorio

### 1. `flow_binaries` — Core Engine (Go)
**Ruta local**: `../flow_binaries`

| Aspecto | Detalle |
|---------|---------|
| Lenguaje | Go |
| Responsabilidad | Core del motor de ejecución de nodos y flows |
| Gestiona | Nodos, flows, ejecuciones, conectores, lógica de negocio principal |
| API | REST (endpoints documentados en L2 por módulo) |
| BD Principal | PostgreSQL — schema principal del producto (compartida con gateway) |
| BD Ejecuciones | **SQLite** — logs de ejecución de cada nodo por flow (interna al backend) |
| Migraciones | `migrations/` |

### 2. `gateway-ion` — Frontend (Vue 3 + TypeScript)
**Ruta local**: `../gateway-ion`

| Aspecto | Detalle |
|---------|---------|
| Framework | Vue 3 con TypeScript |
| Responsabilidad | Interfaz de usuario, vistas, CRUDs |
| NO gestiona | Canvas de nodos (eso es webcomponents-flow) |
| State management | Pinia (stores) |
| Routing | Vue Router |
| Consume APIs de | `flow_binaries` y `gateway` |

### 3. `webcomponents-flow` — Canvas de Nodos (Vue 3 + TypeScript)
**Ruta local**: `../webcomponents-flow`

| Aspecto | Detalle |
|---------|---------|
| Framework | Vue 3 con TypeScript |
| Librería core | Vue Flow (para el canvas de nodos) |
| Responsabilidad | Componentes del canvas: nodos, edges, drawer, formularios |
| Distribución | Compilados y expuestos via CDN |
| Consumido por | `gateway-ion` (los importa como web components) |

### 4. `gateway` — Auth y Legacy (PHP 8.2)
**Ruta local**: `../gateway`

| Aspecto | Detalle |
|---------|---------|
| Lenguaje | PHP 8.2 |
| Framework | Laravel |
| Responsabilidad | Autenticación (SSO Keycloak), gestión de usuarios, permisos, companies |
| Legacy | Aún gestiona parte de la lógica de flows (en migración) |
| BD | PostgreSQL — schema de usuarios, auth, companies y permisos |
| Migraciones | `database/migrations/` |
| Estado | Repo legacy, se planea migrar progresivamente a Go |

### 5. `bot-test` — E2E Automation (Playwright + NX)
**Ruta local**: `../bot-test`

| Aspecto | Detalle |
|---------|---------|
| Framework | Playwright |
| Monorepo | NX workspace |
| Tests Ionflow | `apps/bot-test/tests/IONFLOW/` |
| Skill de IA | `.agents/skills/ionflow-playwright-creator/SKILL.md` |
| Ejecución | `npx nx run bot-test:test:ionflow --args="--spec=..."` |

## Relaciones entre Repos

| Desde | Hacia | Tipo de relación |
|-------|-------|------------------|
| `gateway-ion` | `flow_binaries` | Consume API REST (nodos, flows, ejecuciones) |
| `gateway-ion` | `gateway` | Consume API REST (auth SSO Keycloak, usuarios, sesiones) |
| `gateway-ion` | `webcomponents-flow` | Importa web components via CDN |
| `flow_binaries` | PostgreSQL | Schema principal del producto |
| `flow_binaries` | SQLite | Logs de ejecución de nodos por flow (interno) |
| `gateway` | PostgreSQL | Schema de auth/usuarios/companies (legacy) |
| `bot-test` | `gateway-ion` | Testea la UI del frontend |

---

*Este archivo se actualiza cuando se agrega o migra un repositorio. Última actualización: Initial setup.*
