# Skill: requirements/matrix

> Redacta la **Matriz de Requerimientos vN** de un ticket de Discovery a partir de la especificación del PO y del acta de `prototype review`, prepara la solicitud de VoBo (C-05) y acompaña el estado hasta `to do`: dudas del Dev (C-07), VoBo (C-06 + `po-vobo`), VoBo que no llega y cambios de alcance (C-08). Discovery `requirements` (**D-05**); reglas §8.5 y §9.1; `Q-10`, `Q-12`, `Q-13`, `Q-17` a `Q-24`, `Q-26`, `Q-27`.

## Cuándo usar
- Tablero **Discovery**, estado `requirements` (modos A y B).
- Modo C: cualquier estado posterior al VoBo (`to do` … `mock testing`, `uat`) cuando el **PO** pide o aprueba un cambio de alcance.
- Frases disparadoras: `Matriz de requerimientos del ticket <id>` (A) · `Seguimiento de requirements del ticket <id>` (B) · `Cambio de alcance del ticket <id>` (C).

## Pre-requisitos (gates)
| Check | Si falla |
|---|---|
| Discovery y estado `requirements` (A/B); en C, el cambio lo solicita o aprueba el PO (comentario, C-16 o ajuste "nuevo imprescindible" del C-10) | PARAR. Sin PO no hay cambio de alcance (`Q-18`) |
| Existe el acta C-04 | Avisar: sin C-04 no hay contrato de línea base. Seguir solo con confirmación de QA y registrarlo |
| Existe `prototype-review-qa.md` | Proponer `prototype-review/review.md` primero, o seguir con confirmación de QA |
| La T-01 trae historia, criterios de alto nivel y fuera de alcance preliminar | Lo que falte va a C-05 como punto para el PO; no se inventa |
| Reviewer QA asignado (obligatorio desde `assignment` en Discovery y desde `requirements` en Improvements — `Q-55`) | Acción para el LQA |
| El QA no tiene más de 2 matrices en curso (doc 05 §9.2) | Informar al LQA; el PO decide el orden |

## Contexto a cargar
- **L1:** `sdlc-consolidation.md` (§5 D-04 a D-06, §8.5, §9.1, §10, §12, §14 C-05 a C-08, §16) · doc 05 (§4 completo y Anexo A) · `business-rules.md`.
- **L2:** módulo vía `subcategory-map.csv` → `L2_MODULE`: reglas de negocio, Database, edge cases, Impacto Cruzado.
- **L3:** `prototype-review-qa.md`, `ticket-memory.md`, versiones anteriores `requirements-matrix-v*.md`.
- **ClickUp:** descripción (especificación del PO y matriz vigente, si existe), comentarios C-03, C-04, C-06, C-07 y posteriores, tags (`po-vobo`, `uat-requerido`, `cambio-alcance`), checklist de acuse, QA Points.

## Stage 1 — Planning
```
🔄 SIGUIENTE SKILL: requirements/matrix — Modo <A | B | C>
   Ticket: <id> · `<estado>` · tamaño <S/M/L> · matriz vigente: <vN / ninguna> · po-vobo: <sí/no>
   Prerequisitos: ✅/❌ C-04 · ✅/❌ prototype-review-qa.md · ✅/❌ Reviewer QA
   SLA: matriz <1 día (S/M) | 2–3 días (L)> · VoBo 24 h hábiles · dudas del Dev < 2 h hábiles
   Output esperado: L3/<id>/requirements-matrix-v<N>.md + comments/C-0<5|7|8>-<fecha>.md
¿Procedo?
```

## Stage 2 — Execution

### Modo A — Redactar la matriz (v1, o v+1 antes del VoBo)
1. **Reconciliar fuentes.** Especificación del PO (T-01), C-04 y comentarios. Las decisiones posteriores a la descripción entran con su fuente (`comentario, fecha, autor`). Una contradicción entre fuentes no se resuelve: es un punto para el PO en C-05.
2. **Normalizar, no reescribir (`Q-19`).** Cada criterio del PO → uno o más REQ, con la trazabilidad `CA-1 → REQ-01, REQ-02`. Si el criterio ya es verificable, el REQ lo cita textual. Lo que agregue QA se lista como `completados por QA: REQ-..` y va a C-05.
3. **Filas con las columnas de §9.1:** `ID | Módulo / Servicio | Requerimiento / Regla | ¿Cuándo aplica? | ¿Qué debe pasar? | Excepciones / Fuera de alcance | Crítico`. Una regla por fila; resultado observable (valor, estado, mensaje, código o registro); nunca "correctamente", "rápido" o "adecuado"; sin solución técnica.
4. **Completar con la heurística** (doc 05 §4.3): permisos · estados previos · límites · datos vacíos, inválidos o duplicados · errores y timeouts externos · idempotencia · aislamiento entre companies · impacto cruzado · datos existentes.
5. **Contrato (`Q-10`):** si C-04 aprobó un contrato, agregar el REQ "Cumplir el contrato `<versión o enlace>`" (referencia, no copia).
6. **REQ críticos** (doc 05 §4.5): cobro incorrecto o pérdida/corrupción de datos · exposición de datos o elusión de permisos · flujo core roto (login, crear o ejecutar un board, historial) · contrato con otro producto o sistema externo roto · esencial para el valor mínimo según el PO.
7. **No funcionales (`Q-13`):** `REQ-NF-xx` con métrica y condición de medición. TYPE `Refactor`: "sin cambio funcional", REQ de invariancia + NF que no puede empeorar. POC: la pregunta a responder y su criterio de éxito.
8. **Salidas de IA (`Q-24`):** umbral medible sobre un corpus versionado (tamaño, composición, método de evaluación, revisor de dudosos, N ejecuciones si no es determinista, versión de modelo o prompt). El **PO define el umbral**; QA propone corpus y casos borde. El corpus se congela antes del VoBo.
9. **Épicas (`Q-12`):** una sola matriz en el padre con `REQ-<SUB>-01` por subtarea.
10. **Fuera de alcance obligatorio:** columna por fila + bloque *Fuera de alcance de la entrega*. Un actor, regla o módulo nuevo es otro ticket (`Q-27`).
11. **`### Datos de prueba`:** companies, usuarios y roles; estados iniciales; mocks o sandboxes; archivos o corpus; mecanismos especiales; ambiente (`Q-05`); quién prepara cada dato.
12. **Reglas indefinidas (`Q-20`, `Q-21`):** fila marcada *Pendiente de decisión PO*; en C-05, opciones + **opción recomendada justificada**. Mientras no se decida, esa fila no es criterio de rechazo y el resto avanza.
13. **UAT:** recomendación Sí/No con motivo (decide el PO con `uat-requerido`).
14. **Autorrevisión con el Anexo A** (10 puntos) y resultado en el archivo. Si el ticket es L o tiene REQ críticos de billing, permisos o integridad de datos, recomendar revisión cruzada con el otro QA.
15. **QA Points** (Fibonacci, doc 05 §9.3): 1 ≤ 2 h · 2 ≈ ½ día · 3 ≈ 1 día · 5 ≈ 2 días · 8 ≥ 3 días (evaluar dividir el alcance, `Q-27`).

### Modo B — Seguimiento hasta `to do`
- **B1. Dudas del Dev (C-07):** responder en < 2 h hábiles. Cada respuesta se clasifica: **aclaración** (no cambia condición, resultado ni alcance → respuesta en el ticket, misma versión) o **cambio** (→ v+1: antes del VoBo, nueva versión y nuevo C-05; después, Modo C).
- **B2. VoBo recibido:** verificar que el C-06 dice `✅ VoBo PO — Matriz de Requerimientos v[N]` y que N es la versión más alta de la descripción. Las decisiones del C-06 sobre puntos abiertos se reflejan en las filas *Pendiente de decisión PO* citando el C-06 (forman parte del VoBo de vN).
- **Checklist de salida a `to do`:** C-06 de la versión vigente · tag `po-vobo` (lo agrega QA) · tag `uat-requerido` puesto por el PO si el C-06 dice "UAT: requerido" (si falta, recordárselo) · checklist *"Matriz de Requerimientos vN leída por el Dev"* marcado por el Dev (`Q-23`) · QA Points registrado · Reviewer QA. Sin `po-vobo`, A-03 revierte el estado.
- **B3. VoBo que no llega (`Q-17`):** no hay VoBo tácito. A las 24 h hábiles, borrador de nueva mención al PO y aviso al SM para la daily. A las 48 h, `blocked` con `bloq-definicion` (borrador C-20). Mientras tanto, adelantar la Matriz de Pruebas con `mock-testing/plan.md` (modo borrador).
- **Ajustes del PO antes del VoBo:** v+1 en el mismo estado y nuevo C-05. **Inviable:** el PO decide volver a `prototype review`.

### Modo C — Cambio de alcance después del VoBo (§8.5, `Q-18`)
1. Confirmar el origen: pedido o aprobación del PO (comentario, C-16, C-10 "nuevo imprescindible", requerimiento tardío exigido en `mock testing`, división de alcance de un REQ no crítico `normal`/`low` — doc 05 §7).
2. Crear v+1: filas cambiadas marcadas *Cambiado en vN+1*; las eliminadas, *Eliminado en vN+1* (su ID no se reutiliza).
3. Borrador C-08 con la tabla `REQ | Antes | Ahora`. Acciones para QA: agregar `cambio-alcance` (A-04 retira `po-vobo`; si el tag ya existía, retirar `po-vobo` a mano); tras el nuevo C-06, volver a agregar `po-vobo`. El código se modifica **después** del nuevo VoBo.
4. Si el ticket estaba en `mock testing`: vuelve a `to do` con C-08 (**no** C-14), sin sumar Rejection_count. Luego ajustar la Matriz de Pruebas (`mock-testing/plan.md`).

## Stage 3 — Reporting
- `knowledge/L3-tickets/<id>/requirements-matrix-v<N>.md` con `templates/requirements-matrix.md`: bloque listo para pegar en la descripción bajo `## Matriz de Requerimientos vN` + *Fuera de alcance de la entrega* + `### Datos de prueba` + trazabilidad + resultado del Anexo A + QA Points propuestos.
- Borradores en `comments/`: `C-05-<fecha>.md` (A) · `C-07-respuesta-<fecha>.md` (B1) · mención de VoBo pendiente o `C-20-<fecha>.md` (B3) · `C-08-<fecha>.md` (C).
- **Acciones manuales para QA:** pegar la matriz en la descripción, publicar el comentario, gestionar los tags, registrar QA Points y, con el checklist de salida completo, mover a `to do`.
- `ticket-memory.md`: versión de la matriz, fecha de C-05, vencimiento del VoBo (24 h y 48 h hábiles), estado del acuse, VoBo recibido, cambios de alcance.

```
📋 MATRIZ DE REQUERIMIENTOS v<N> — <id>
REQ: <n> (críticos <n>, NF <n>) · Fuera de alcance: <n> · Puntos para el PO: <n> · UAT recomendado: Sí/No
Anexo A: <10/10> · QA Points: <n> · Estado destino: `requirements` (esperando VoBo) → `to do` con po-vobo
```

## Reglas
- QA **redacta**; el PO **decide** y da el VoBo con un único comentario. QA nunca aprueba su propia matriz.
- La matriz con VoBo vigente es el único criterio de aceptación y rechazo; la especificación se normaliza, no se reescribe.
- Ningún ticket pasa a `to do` sin `po-vobo` y sin el acuse del Dev.
- Una aclaración no versiona; un cambio de condición, resultado o alcance sí (v+1).
- El MCP es de solo lectura: QA pega la matriz y publica los comentarios.
