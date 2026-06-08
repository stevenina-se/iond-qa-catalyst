# Ticket Memory: IONF-999

## Datos del Ticket

| Campo | Valor |
|-------|-------|
| ID ClickUp | `86e180hw9` |
| ID Interno | IONF-999 |
| URL | https://app.clickup.com/t/86e180hw9 |
| Título | Agregar descripciones automáticas de los boards |
| Status | `qa testing` |
| Tipo | New Feature |
| Prioridad | High |
| Sprint | Sprint 1 (5/25 - 6/7) |
| Space | NEW GATEWAY IOND |
| Proyecto | IONFLOW |
| QA Points | 2 |
| Creador | Marcel Herrera Rendón |
| Asignado (Dev) | Alex Chura |
| Watchers | Rodolfo Merlo Ali, Steve Nina, Alex Chura, Gustavo Mamani, Marcel Herrera Rendón, Enrique Vicente |

---

## Merge Requests

| Repo | MR | Branch |
|------|----|--------|
| `flow_binaries` | https://gitlab.com/altacrest/flow_binaries/-/merge_requests/151 | `IONF-999` |
| `gateway-ion` | https://gitlab.com/altacrest/gateway-ion/-/merge_requests/218 | `IONF-999` |
| `webcomponents-flow` | N/A | — |
| `gateway` (Laravel) | N/A | — |

---

## Resumen Funcional

Implementar un botón de IA en la lista de Boards que genera automáticamente una descripción corta del flow analizando nodos, conexiones y comentarios. La descripción se guarda en el campo `description` existente (máx 500 chars). El campo sigue siendo editable manualmente.

---

## Acceptance Criteria (Gherkin)

### Escenario 1: Generación exitosa de descripción mediante FlowPilot
- **Given** el usuario está en la vista de lista de Boards
- **And** visualiza un tablero sin descripción o que requiere actualización
- **When** hace clic en el botón de IA
- **Then** el sistema invoca al motor de IA compartiendo la info interna del flow
- **And** renderiza automáticamente la descripción corta generada en el campo de texto
- **And** guarda el cambio de forma persistente en la BD

### Escenario 2: Edición manual sobre descripción generada
- **Given** un tablero con descripción generada por IA
- **When** el usuario modifica el contenido manualmente
- **Then** el sistema permite la escritura libre
- **And** guarda la entrada manual respetando el límite de longitud

---

## Análisis Técnico (del ticket)

### Backend (flow_binaries)
- **Endpoint nuevo**: `POST /api/1.0/tenants/{tenantId}/flows/{flowId}/generate-description`
- **Permiso**: `UpdateBoard`
- **Service**: `GenerateCompanyFlowDescription(company, flowId)`
  1. `FindCompanyFlow(company, flowId)` — obtiene nodos/edges parseados
  2. Arma mapa compacto: tipo de nodo + label, edges (source→target), comentarios
  3. Cliente IA: `NewClientFromEnv()` + `ChatCompletion` (síncrono, no streaming)
  4. Trunca a 500 chars → `Update("description", ...)` puntual (NO `Save`)
  5. Devuelve el string

### Frontend (gateway-ion)
- **Archivo**: `src/views/tenant/workflows/components/FlowList.vue` — columna `description`
- **Service**: `src/services/tenant/flows.service.ts` — método nuevo (molde: `getAIMapperSuggestion`)
- **UX**: Click botón → spinner → renderiza descripción sin recargar lista
- **Test unitario**: `FlowDescription.spec.ts` (agregado por dev)

### Decisiones clave
| # | Decisión |
|---|----------|
| D1 | Generación solo on-demand (botón), NUNCA en save/update |
| D2 | Endpoint síncrono (spinner espera) |
| D3 | Backend lee el flow de DB, NO se envía desde front |
| D5 | Persistir con `Update("description", ...)` puntual, sin git/IsDirty |
| D6 | Service nuevo dedicado, no tocar `UpdateCompanyFlow` |
| D8 | Límite 500 chars forzado en backend + prompt |
| D9 | Fallo IA = error toast, flow queda igual |

---

## Historial de Status

| Fecha | Status |
|-------|--------|
| 2026-05-05 | ideas |
| 2026-05-25 | for analysis |
| 2026-05-27 | fortification |
| 2026-05-27 | code review |
| 2026-05-29 | qa testing |

## Code Review

- **Enrique Vicente** (2026-05-28): Observaciones en `gateway-ion`
- **Alex Chura** (2026-05-29): Resolvió observaciones
- **Gustavo Mamani** (2026-05-29): ✅ Code review approved
- **Enrique Vicente** (2026-05-29): ✅ Code review approved
- **Rodolfo Merlo Ali** (2026-06-01): `deployed`

---

## Módulos Afectados

| Módulo L2 | Impacto |
|-----------|---------|
| **Boards** | Principal — nuevo endpoint, nuevo botón en lista |
| **Nodes** | Lectura — se leen nodos/edges para generar descripción |

---

## Recursos

- **Demo video**: [Screen Recording](https://t8501689.p.clickup-attachments.com/t8501689/74191c83-3cf4-4341-bad5-e96b6e08a7ac/Screen%20Recording%202026-05-27%20at%207.22.31%E2%80%AFPM.mov)
