# Skill: release/sanity

> **Sanity de la versión** (`Q-48`, REL-04): re-ejecuta en preprod los **REQ críticos** de cada ticket del release y las interacciones entre tickets que tocan el mismo módulo o Iond Subcategory. Comentario **C-26**.

## Cuándo usar

- Tarea de Release en `sanity` (martes – miércoles), después de un smoke OK.
- Frase disparadora: `Ejecutar sanity: <producto> vX.Y.Z`.

## Pre-requisitos (gates)

| Check | Si falla |
|---|---|
| `smoke-preprod.md` sin fallas de core abiertas en el área | No iniciar en esa área (regla de core del smoke) |
| `tickets.md` de `release/ingest` | Ejecutar `release/ingest` |
| Cada ticket tiene matriz con REQ críticos y `test-matrix.md` en L3 | Avisar al LQA; el ticket se valida con su matriz de la descripción o se registra como hallazgo de proceso |

## Contexto a cargar

`tickets.md`, las matrices de cada ticket (`knowledge/L3-tickets/<id>/requirements-matrix-v<N>.md`, `test-matrix.md`, `qa-report.md`), L2 de los módulos impactados, `skills/_shared/evidence.md`.

## Stage 1 — Planning

Anunciar tickets, cantidad de REQ críticos y TC a re-ejecutar, interacciones detectadas, TC automatizables (si alguno ya existe en bot-test) y el reparto entre los QAs (≤ 1,5 días). Esperar confirmación.

## Stage 2 — Execution

1. **Construir la matriz** con `templates/sanity-matrix.md` en `knowledge/releases/<producto>/<versión>/sanity-matrix.md`:
   - Por ticket: cada **REQ crítico** → sus TC de la Matriz de Pruebas (columna `USO` = Mock/Sanity) → ID `SAN-<ticket>-<REQ>`.
   - Un REQ crítico sin TC → crear el TC mínimo (Happy Path) y marcarlo como brecha de la matriz.
   - **Interacciones:** pares de tickets con la misma Subcategory o el mismo módulo L2 → 1 a 3 verificaciones del flujo combinado (`SAN-INT-xx`).
   - Bugs del release: el resultado esperado del reporte + la no regresión de zonas cercanas.
2. **Ejecutar** en preprod (ambiente integrado), manual o con el comando de bot-test si un TC ya está automatizado. Registrar evidencia de cada REQ crítico.
3. **Resultados.** Cada falla: ¿la provocó el ticket o la integración con otro ticket? Severidad (prioridad nativa) y decisión según la fuente canónica §7.5:
   - `urgent` → **fix-forward** (C-28) en la rama RC; QA re-ejecuta el REQ afectado.
   - Resto → propuesta de ticket en Improvements `backlog` con `det-sanity`, previa discusión con PO y LD.
   - Si el fix-forward no llega en plazo (≤ 4 h decisión, ≤ 1 día fix): PO + LD + RM deciden **revertir** el ticket (vuelve a `to do` con `diferido`) o NO-GO.
4. **Candidatos a la regresión.** Los TC estables de REQ críticos que se repiten en varios releases se marcan como candidatos a automatizar (`skills/automation/plan.md`) y a agregar como fila del E2E maestro si la feature no está en la hoja.

## Stage 3 — Reporting

- `sanity-matrix.md` completo (ticket → REQ crítico → TC → resultado → evidencia).
- Borrador **C-26** en `comments/` (lista ticket → REQ críticos → resultado; hallazgos y decisiones).
- Siguiente skill: `release/regression`.

## Reglas

- El criterio de salida es el **100 % de los REQ críticos aprobados** por ticket, sin efectos colaterales entre tickets.
- No se re-prueba todo `mock testing`: solo lo crítico y lo que cruza tickets.
- Un hallazgo fuera de matriz no bloquea el ticket (C-17) salvo que sea una regresión `urgent` provocada por el release.
