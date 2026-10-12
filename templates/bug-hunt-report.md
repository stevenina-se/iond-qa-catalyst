# Bug bash — [módulo / área] — [AAAA-MM-DD]

> **Plantilla del QA Catalyst** — exploratory testing / bug bash (ACT-03 · `Q-39` · Estándar de QA §3.D): sesión **quincenal de 60–90 min** con QA + Dev + SM, con un objetivo y un área definidos.
> **Se guarda en:** `knowledge/dashboards/bug-bash/bug-hunt-[módulo]-[AAAA-MM-DD].md` (o en `knowledge/releases/[producto]/v[X.Y.Z]/` si la sesión es para un release) · **Skill:** `skills/release/bug-hunt.md`.
> Los hallazgos van a Improvements `backlog` con la plantilla T-02 (`templates/bug-ticket.md`) y el tag **`det-exploratorio`**; los registra QA (el catalyst prepara con `skills/bug-reporter/create.md`). Un incidente `urgent` en producción va por el carril de hotfix (C-32), no por `backlog`.

## Sesión

| Campo | Valor |
|---|---|
| Fecha · duración | [AAAA-MM-DD] · [60–90] min |
| Participantes (roles) | QA · Dev · SM |
| Producto / versión · ambiente | [iond / IonMind / StageMind] v[X.Y.Z] · [QA / preprod] |
| Objetivo | [pregunta o riesgo que se quiere explorar] |
| Área | [Iond Subcategory] — `knowledge/L2-modules/[módulo]` |
| Heurísticas | [permisos · límites · datos inválidos · concurrencia · aislamiento entre companies · errores externos · ...] |

## Resumen

| Métrica | Valor |
|---|---|
| Hallazgos confirmados (UI · API) | [n] · [n] |
| Riesgos no verificados | [n] |
| Falsos positivos descartados | [n] |
| Tickets propuestos (`det-exploratorio`) | [n] |

## Hallazgos confirmados

Solo se confirma lo reproducido (a mano o con Playwright MCP, con el QA supervisando).

### BB-01 — [resumen en una línea]

| Campo | Valor |
|---|---|
| Severidad propuesta (prioridad) | `urgent` / `high` / `normal` / `low` |
| Canal | UI / API |
| Módulo · tag de área | [Iond Subcategory] · `iond-core` / `iond-uxui` / `iond-infra` / `iond-ia` |
| ¿Contradice un REQ vigente? | REQ-[xx] de la matriz v[N] del ticket #[id] · No (fuente del esperado: [...]) |
| Ticket | Propuesto (T-02 + `det-exploratorio`) · creado #[id] |

**Pasos para reproducir:**
1. Company Login > Sidebar: [Módulo] > [...]

**Resultado esperado:** [...]

**Resultado actual:** [...]

**Evidencia:** [captura / video / log / `transaction_id`]

*API (si aplica):*
```text
Request:  [MÉTODO] /api/[ruta] · Body: [JSON con datos sensibles enmascarados]
Esperado: [código] · [respuesta]
Actual:   [código] · [respuesta]
```

## Riesgos no verificados

Hallazgos del análisis de código (solo lectura) que no se pudieron reproducir; quedan para verificar.

| ID | Riesgo | Confianza | Canal | Referencia (`../[repo]/[archivo]:[línea]`) | Qué falta para verificarlo |
|---|---|---|---|---|---|
| RISK-01 | [...] | Alta / Media / Baja | UI / API | [...] | [...] |

## Falsos positivos descartados

Se documentan para no volver a reportarlos.

| ID | Descripción | Motivo del descarte |
|---|---|---|
| FP-01 | [...] | [regla del L2 / comportamiento esperado / Fuera de alcance de un ticket] |

## Búsquedas en código (solo lectura)

| Término | Repo | Comando | Resultado |
|---|---|---|---|
| [...] | [...] | `grep -rn "[...]" ../[repo]/ --include="*.[ext]"` | [n] coincidencias / 0 |

## Seguimiento

- Hallazgos que escaparon a las suites del release → propuesta de TC para la regresión (fila nueva en la hoja "Iond Testing Plan" o en el E2E maestro).
- Próxima sesión: [AAAA-MM-DD] · área propuesta: [...].
