# Bug — [PRODUCTO][Módulo] [qué falla, en una línea]

> **Plantilla del QA Catalyst = T-02** (fuente canónica §13) + datos de clasificación. Tablero: **Improvements** → `backlog` (un incidente de producción va por el carril de hotfix: `to do` directo).
> **Se guarda en:** `knowledge/L3-tickets/drafts/` mientras es borrador y, cuando QA crea el ticket, en `knowledge/L3-tickets/[id-del-bug]/bug-report.md`; el ticket origen (o la tarea de Release, si nace en el release) se referencia por relación · **Skill:** `skills/bug-reporter/create.md`. El catalyst prepara; QA crea el ticket en ClickUp (MCP de solo lectura).
> **Clasificación (`Q-15`):** QA propone tablero, TYPE y prioridad (= severidad); el PO la aprueba en el triage (C-33).

## Campos y tags en ClickUp

| Campo | Valor |
|---|---|
| Título | `[PRODUCTO][Módulo] Verbo + objeto` (`Q-46`) |
| Tablero | Improvements |
| TYPE | `Bug` |
| Project | `Iond` / `IONMIND` / `STAGEMIND` / `Gateway` |
| Iond Subcategory | [Boards / Connections / App Connectors / PDF Templates / Billing / API / Nodo X …] — obligatorio si Project = Iond |
| Prioridad (= severidad) | `urgent` / `high` / `normal` / `low` — [motivo según la tabla de severidad] |
| Tag de detección | `det-mock` / `det-uat` / `det-smoke` / `det-sanity` / `det-regression` / `det-prod` / `det-exploratorio` |
| Tag de área (iond) | `iond-core` / `iond-uxui` / `iond-infra` / `iond-ia` |
| Otros tags | `fuera-de-matriz` (hallazgo fuera de matriz) · `pilot-feedback` · `hotfix` (incidente en producción) |
| REQ violado | REQ-[xx] de la Matriz v[N] del ticket #[id] · Ninguno (fuente del esperado: [L2 / documentación / comportamiento previo]) |
| Ticket padre / relación | #[id del ticket origen] o tarea de Release `[producto] - v[X.Y.Z]` — relación en ClickUp |
| Duplicados | Descartados — búsqueda: [términos] |

## Descripción (pegar en ClickUp)

```markdown
## Resumen
[Qué falla, en una línea]

## Ambiente
- Producto / versión: [Iond vX.Y.Z | IonMind | StageMind] · Ambiente: [QA | preprod | producción] · Rama/commit: [..]
- Fase de detección: [det-*]

## Pasos para reproducir
1. ...

## Resultado esperado
[Qué debería pasar — cita el REQ-ID si existe]

## Resultado actual
[Qué pasa]

## Evidencia
[Capturas, logs, transaction_id, request/response]

## Impacto
[Usuarios o clientes afectados, workaround]
```

## Severidad (prioridad nativa)

| Prioridad | Severidad | Definición |
|---|---|---|
| `urgent` | Bloqueante | Funcionalidad core rota sin workaround; pérdida o corrupción de datos; seguridad; cobro incorrecto |
| `high` | Alta | Funcionalidad importante falla con workaround |
| `normal` | Media | Funcionalidad secundaria o UX con impacto moderado |
| `low` | Baja | Cosmético |

## Según dónde se detecta

| Fase | Tratamiento |
|---|---|
| `mock testing` — fuera de matriz | Ticket nuevo con `fuera-de-matriz` (+ `det-mock`); C-17 en el ticket origen; no bloquea |
| `mock testing` — `urgent` preexistente | Ticket nuevo con `det-mock` y aviso inmediato al PO; no bloquea el ticket en prueba |
| Release (`smoke`, `sanity`, `regression`) — `urgent` | **Fix-forward**: subtarea de la tarea de Release con tag `fix-forward` y C-28 (esta misma descripción) |
| Release — resto | Ticket en `backlog` con `det-smoke` / `det-sanity` / `det-regression`, previa discusión con PO y LD |
| Producción — incidente | Carril de hotfix: `urgent` + `hotfix` + `det-prod`, `to do` directo, C-32; relacionar con la tarea de Release de la versión |
| Producción — no urgente / bug bash | `backlog` con `det-prod` / `det-exploratorio` |

## Checklist de calidad (Estándar de QA, Anexo B)

1. [ ] **Resumen** en una línea: qué falla y dónde.
2. [ ] **Ambiente:** producto y versión, ambiente (QA, preprod o producción) y rama o commit.
3. [ ] **Tag de detección** `det-*` y, en iond, tag de área.
4. [ ] **Pasos** numerados y reproducibles desde un estado conocido (breadcrumb `Company Login > Sidebar: [Módulo] > ...`), con datos y rol; frecuencia si es intermitente (p. ej. 3 de 5).
5. [ ] **Resultado esperado** con el REQ-ID si existe, o la fuente del esperado.
6. [ ] **Resultado actual**, factual y sin interpretaciones.
7. [ ] **Evidencia:** captura o video, logs, `transaction_id`, request/response, con datos sensibles enmascarados.
8. [ ] **Impacto:** usuarios o clientes afectados y workaround, si existe.
9. [ ] **Prioridad (= severidad)** según la tabla.
10. [ ] **Campos:** TYPE `Bug`, Project e Iond Subcategory (si Project = Iond); un bug por ticket y duplicados descartados.
