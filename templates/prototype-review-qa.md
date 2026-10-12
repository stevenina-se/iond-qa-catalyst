# Revisión de QA en `prototype review` — [id-clickup] · [título del ticket]

> **Plantilla del QA Catalyst** — salida de QA en `prototype review` (D-04 · `Q-09`, `Q-10` · Estándar de QA §3.A). Reunión obligatoria: PO + Dev + QA + LD (SM opcional; SH si aplica).
> **Se guarda en:** `knowledge/L3-tickets/[id-clickup]/prototype-review-qa.md` · **Skill:** `skills/prototype-review/review.md` · Alimenta el acta **C-04** (la publica el SM o el PO) y la Matriz de Requerimientos v1.
> QA evalúa la **testabilidad** e inicia la captura de requerimientos. No decide reglas de negocio: las propone con una opción recomendada.

## Contexto

| Campo | Valor |
|---|---|
| Ticket | [id-clickup] — [título] — [url] |
| Tablero / estado | Discovery · `prototype review` |
| Project · Iond Subcategory · TYPE · tamaño | [...] · [...] · [...] · S / M / L |
| Dev · LD | @[dev] · @[lead-dev] |
| R&D (C-03) | [AAAA-MM-DD] — [enlace] |
| Prototipo revisado (`Q-09`) | [wireframe / OpenAPI / diseño de board / dataset de IA] — [enlace] |
| Contrato de interfaz | [versión / enlace] |
| Fecha de la reunión | [AAAA-MM-DD] |

## 1. Checklist de testabilidad (Estándar de QA §3.A)

| # | Pregunta | Respuesta | Acción |
|---|---|---|---|
| T1 | ¿Cada comportamiento produce un resultado observable (UI, respuesta de API, registro en el historial, log con `transaction_id`)? | Sí / No / Parcial | [...] |
| T2 | ¿Existen, o pueden prepararse, el ambiente y los datos (sandbox, mocks, companies de prueba)? (`Q-05`) | | |
| T3 | ¿El contrato de interfaz está versionado para referenciarlo desde la matriz? (`Q-10`) | | |
| T4 | ¿Hay dependencias de otros productos o de terceros que deban simularse? | | |
| T5 | En salidas de IA: ¿hay corpus de referencia y criterio de calidad medible? (`Q-24`) | | |
| T6 | ¿Los requisitos no funcionales tienen métrica? | | |

Detalle técnico (contrato, NFR, datos, dependencias, rollback): `templates/architecture-brief-qa.md` — recomendado en tickets L o con cambios de contrato o de BD.

## 2. Captura inicial de requerimientos (borrador, sin VoBo)

| Criterio del PO | REQ preliminar | Regla / comportamiento | ¿Crítico? (Estándar §4.5) | Duda abierta |
|---|---|---|---|---|
| CA-1 | REQ-01 | [...] | Sí / No | [...] |
| CA-2 | REQ-02 | [...] | Sí / No | [...] |

**Heurística de completitud revisada:** [ ] roles y permisos · [ ] estados previos · [ ] límites (0, exacto, máximo, ilimitado) · [ ] datos vacíos, inválidos o duplicados · [ ] errores y timeouts externos · [ ] concurrencia e idempotencia · [ ] aislamiento entre companies · [ ] impacto cruzado (iond ↔ IonMind ↔ StageMind) · [ ] datos existentes y compatibilidad.

## 3. Riesgos de calidad

| Riesgo | Impacto | Mitigación propuesta |
|---|---|---|
| [...] | Alto / Medio / Bajo | REQ / REQ-NF / dato de prueba / no regresión de zonas cercanas |

## 4. Observaciones para el acta (C-04)

1. [...]
2. [...]

**Recomendación de QA:** ✅ Avanzar a `requirements` / ❌ Volver a `r, d & architect review` — motivo: [...]. Decide el PO.

## 5. Pendientes para `requirements`

| # | Pendiente | Responsable (rol) | Destino |
|---|---|---|---|
| 1 | [Regla indefinida + opción recomendada] | PO | Punto de decisión en el C-05 |
| 2 | [Dato, sandbox o acceso] | Dev / LD / QA | `### Datos de prueba` |

## 6. Propuesta de UAT

`uat-requerido`: [Sí / No] — [motivo]. Decide el PO en `requirements`.

## 7. Siguiente paso

- Matriz de Requerimientos v1 con `templates/requirements-matrix.md` (SLA: 1 día hábil S/M · 2–3 días L desde la entrada a `requirements`).
- QA Points preliminares: [n] (se registran al salir de `requirements`).
