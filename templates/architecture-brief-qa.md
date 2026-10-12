# Checklist técnico de QA — `prototype review` — [id-clickup] · [título del ticket]

> **Plantilla del QA Catalyst** — revisión técnica de QA sobre el R&D (C-03) y el prototipo (D-03 / D-04 · `Q-09`, `Q-10`, `Q-13`, `Q-24` · Estándar de QA §3.A).
> Se completa **antes** de la reunión de `prototype review` y alimenta `prototype-review-qa.md` (observaciones para el acta C-04 y pendientes para `requirements`). Se pega como anexo de `prototype-review-qa.md`; en tickets L o con cambios de contrato o de BD se guarda aparte en `knowledge/L3-tickets/[id-clickup]/architecture-brief-qa.md`. **Skill:** `skills/prototype-review/review.md`.
> Estado de cada punto: ✅ cubierto · ⚠️ observación · ❌ bloqueante · N/A.

## Insumos revisados

| Insumo | Referencia |
|---|---|
| R&D (C-03) | Opciones, recomendación, repos afectados, dependencias, riesgos, requisitos no funcionales — [enlace] |
| Prototipo (`Q-09`) | Wireframe/UX navegable · contrato OpenAPI · diseño de board y mapeo de datos · dataset y criterio de calidad (IA) — [enlace] |
| Contrato de interfaz | [versión / enlace] |
| Repos afectados | [gateway-ion / flow_binaries / webcomponents-flow / gateway / ...] |
| L2 del módulo | `knowledge/L2-modules/[módulo]` — reglas, *Impacto Cruzado*, *Archivos centinela* |

## 1. Contrato de interfaz (`Q-10`)

| # | Punto | Estado | Observación |
|---|---|---|---|
| 1 | El contrato (OpenAPI, mapeo de datos, diseño del board) está versionado y se puede referenciar desde la matriz | | |
| 2 | Request/response, validaciones de entrada y códigos de error (4xx / 5xx) definidos | | |
| 3 | Compatibilidad hacia atrás con los consumidores existentes (iond ↔ IonMind ↔ StageMind ↔ Gateway) | | |
| 4 | Autenticación y permisos por rol definidos (SSO Keycloak; respuesta esperada sin permiso, p. ej. 403) | | |
| 5 | Idempotencia y reintentos (doble clic, webhooks duplicados, reintentos del proveedor) | | |

## 2. Testabilidad

| # | Punto | Estado | Observación |
|---|---|---|---|
| 6 | Cada comportamiento produce un resultado observable (UI, respuesta de API, historial de ejecuciones, log con `transaction_id`) | | |
| 7 | Los datos persistidos se pueden verificar (BD en solo lectura desde las migraciones, o UI/API del historial) | | |
| 8 | El ambiente asignado al QA puede desplegar la rama del ticket con migraciones y variables (`Q-05`) | | |
| 9 | El aislamiento entre companies se puede verificar | | |
| 10 | Los errores de servicios externos (timeouts, respuestas de error) se pueden simular | | |

## 3. Requisitos no funcionales (`Q-13`) → filas `REQ-NF`

| # | Punto | Estado | Observación |
|---|---|---|---|
| 11 | Rendimiento con métrica y condición de medición (p. ej. p95 ≤ [n] s con [n] registros en preprod) | | |
| 12 | Seguridad: manejo de credenciales, datos sensibles y acceso cruzado entre companies | | |
| 13 | Impacto en el motor de ejecución de boards (volumen, concurrencia, ejecuciones en curso) | | |
| 14 | Observabilidad: logs y trazas suficientes para diagnosticar | | |
| 15 | Refactor: métrica que no puede empeorar · POC: pregunta y criterio de éxito | | |
| 16 | Salida de IA: corpus de referencia y criterio de calidad medible (`Q-24`) | | |

## 4. Datos de prueba

| # | Punto | Estado | Observación |
|---|---|---|---|
| 17 | Companies, usuarios y roles necesarios | | |
| 18 | Sandbox o mock para cada integración (proveedor de pagos, App Connectors, apps externas); si no hay sandbox: mock, colección simulada o cuenta de prueba | | |
| 19 | Mecanismos especiales (fechas simuladas, seeds, migraciones) y quién los prepara (QA o Dev, informado en C-09) | | |
| 20 | Compatibilidad con datos existentes y migración de registros previos | | |

## 5. Dependencias, despliegue y rollback

| # | Punto | Estado | Observación |
|---|---|---|---|
| 21 | Dependencias de otros productos o terceros que deban simularse o desplegarse antes | | |
| 22 | Migraciones reversibles y plan de rollback (BD principal y BD de ejecuciones) | | |
| 23 | Variables nuevas y orden de despliegue entre repos y productos | | |
| 24 | Impacto cruzado en otros módulos (L2) → candidatos a no regresión de zonas cercanas | | |
| 25 | Webhooks, conexiones y App Connectors existentes se mantienen estables | | |

## 6. ¿UAT requerido?

| # | Punto | Propuesta | Motivo |
|---|---|---|---|
| 26 | El cambio requiere validación del cliente o de SH antes del merge | Sí / No | [...] — propuesta de QA para `uat-requerido`; decide el PO en `requirements` (Improvements no tiene `uat`) |

## Resumen

| Total | ✅ | ⚠️ | ❌ | N/A |
|---|---|---|---|---|
| 26 | | | | |

**Conclusión de QA para el acta (C-04):**
- [ ] Testable, sin observaciones.
- [ ] Testable con observaciones → pendientes para `requirements`.
- [ ] No testable todavía → propuesta: volver a `r, d & architect review` ([motivo]). Decide el PO.

**Pendientes para `requirements`:** [...]
**Candidatos a `REQ-NF`:** [...]
