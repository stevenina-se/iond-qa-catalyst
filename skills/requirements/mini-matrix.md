# Skill: requirements/mini-matrix

> Redacta la **mini-matriz** de una mejora de Improvements (hasta 5 REQ con su columna *Fuera de alcance*) más el **checklist de no regresión de zonas cercanas**, y acompaña el estado hasta `to do` con el VoBo del PO. Improvements `requirements` (**I-02**); reglas §9.2; `Q-15`, `Q-17`, `Q-19` a `Q-23`, `Q-29`, `Q-30`.

## Cuándo usar
- Tablero **Improvements**, estado `requirements` (opcional en ese tablero), o en `backlog` cuando el C-33 decidió "¿Requiere requirements? Sí".
- Frase disparadora: `Mini-matriz del ticket <id>`

## Pre-requisitos (gates)
| Check | Si falla |
|---|---|
| Improvements y estado `requirements` (o C-33 con "Requiere requirements: Sí") | PARAR e indicar la skill del estado actual |
| TYPE distinto de `Bug` | PARAR: los bugs nunca pasan por `requirements` (`Q-29`); el reporte T-02 es su especificación |
| Existe la T-03 (situación actual, mejora propuesta, criterio breve, fuera de alcance) | Lo que falte va a C-05 como punto para el PO |
| La mejora cabe en ≤ 5 REQ, no toca reglas troncales y no impacta varios módulos o productos | PARAR: advertir al PO para que la reclasifique a Discovery (`idea/request`). Borrador de comentario con el motivo |
| Existe `triage.md` del ticket | Seguir; tomar la clasificación del C-33 publicado |

## Contexto a cargar
- **L1:** `sdlc-consolidation.md` (§3, §6 I-01 a I-03, §8.5, §9.1–9.2, §14 C-05 a C-08 y C-33) · doc 05 (§3.B, §4.2, §4.3, §4.5, §4.9, Anexo A).
- **L2:** módulo vía `subcategory-map.csv` → `L2_MODULE` (reglas de negocio, Impacto Cruzado, archivos centinela, edge cases). Filas del E2E maestro del módulo (`knowledge/test-suites/e2e-master.csv`, columna `L2_MODULE`) como fuente de la no regresión.
- **L3:** `triage.md`, `ticket-memory.md`.
- **ClickUp:** descripción T-03, comentarios (C-33, dudas), tags, checklist de acuse *"Mini-matriz vN leída por el Dev"*.

## Stage 1 — Planning
```
🔄 SIGUIENTE SKILL: requirements/mini-matrix
   Ticket: <id> · Improvements · `<estado>` · TYPE <..> · Iond Subcategory <..>
   Criterios de la T-03: <n> · Estimación: <n> REQ (máx. 5)
   SLA: QA 1 día hábil · VoBo 24 h hábiles · dudas del Dev < 2 h hábiles
   Output esperado: L3/<id>/requirements-matrix-v<N>.md (mini-matriz) + comments/C-05-<fecha>.md
¿Procedo?
```

## Stage 2 — Execution
1. **Leer y reconciliar** la T-03, el C-33 y los comentarios. Las decisiones posteriores entran con su fuente; las contradicciones van a C-05.
2. **Normalizar los criterios** de la T-03 en REQ (`Q-19`) con las columnas de §9.1: `ID | Módulo / Servicio | Requerimiento / Regla | ¿Cuándo aplica? | ¿Qué debe pasar? | Excepciones / Fuera de alcance | Crítico`. Trazabilidad `CA-1 → REQ-01`. Máximo **5 REQ**; si se necesitan más, aplicar el escalamiento del gate.
3. **Completar** con la heurística de doc 05 §4.3 solo en lo que toca la mejora (validaciones, mensajes, permisos, límites, datos existentes).
4. **Marcar críticos** con la definición de doc 05 §4.5. Agregar `REQ-NF-xx` solo si la mejora tiene un requisito no funcional con métrica.
5. **Fuera de alcance:** columna por fila y bloque de la entrega, empezando por el *Fuera de alcance* de la T-03.
6. **Checklist de no regresión de zonas cercanas** (3 a 5 verificaciones): flujos del mismo módulo y flujos que comparten el código modificado. Fuentes: Impacto Cruzado y archivos centinela del L2, filas del E2E maestro del módulo (preferir las de `BASELINE = sí` o prioridad `Urgent`), riesgos del T-03. Cada verificación en una línea con resultado observable.
7. **Datos de prueba** breves (`### Datos de prueba`): company, usuario y rol, estado inicial, mocks si aplica.
8. **Puntos para el PO:** reglas indefinidas con opciones y **opción recomendada** (`Q-20`, `Q-21`); la fila queda *Pendiente de decisión PO* hasta el VoBo.
9. **UAT:** Improvements no tiene `uat` (`Q-30`). Si la mejora requiriera validación del cliente, plantearlo en C-05: el PO decide si se valida en el `sanity` del release o si el ticket pasa a Discovery.
10. **Autorrevisión** con los puntos aplicables del Anexo A (1–7 y 9–10).
11. **QA Points:** proponerlos (se registran a más tardar en `ready for qa`).

### Seguimiento (mismas reglas que `requirements/matrix.md`, Modo B y C)
- **Dudas del Dev (C-07):** respuesta en < 2 h hábiles; aclaración (misma versión) o cambio (v+1).
- **VoBo (C-06 + `po-vobo`):** verificar que corresponde a la versión vigente; checklist de salida a `to do`: C-06 · `po-vobo` · checklist *"Mini-matriz vN leída por el Dev"* marcado (`Q-23`).
- **VoBo que no llega (`Q-17`):** 24 h hábiles → nueva mención al PO y aviso al SM; 48 h → `blocked` con `bloq-definicion` (C-20).
- **Cambio de alcance después del VoBo:** seguir el Modo C de `skills/requirements/matrix.md` (v+1, C-08, `cambio-alcance`, nuevo VoBo antes de tocar código).

## Stage 3 — Reporting
- `knowledge/L3-tickets/<id>/requirements-matrix-v<N>.md` con `templates/mini-matrix.md`: bloque para pegar en la descripción bajo `## Matriz de Requerimientos vN` (mini-matriz; mismo encabezado para que el C-06 y la auditoría lo lean igual), *Fuera de alcance*, checklist de no regresión, *Datos de prueba* y trazabilidad.
- `comments/C-05-<fecha>.md` (y, según el seguimiento, `C-07-respuesta-<fecha>.md`, `C-20-<fecha>.md` o `C-08-<fecha>.md`).
- **Acciones manuales para QA:** pegar la mini-matriz, publicar C-05, agregar `po-vobo` al recibir el C-06 y mover a `to do`.
- `ticket-memory.md`: tablero Improvements, versión, fechas de C-05 y C-06, vencimientos de VoBo.

```
📋 MINI-MATRIZ v<N> — <id>
REQ: <n>/5 (críticos <n>) · Fuera de alcance: <n> · No regresión: <n> verificaciones · Puntos para el PO: <n>
Estado destino: `requirements` (esperando VoBo) → `to do` con po-vobo
```

## Reglas
- Hasta 5 REQ. Más de 5, una regla troncal o varios módulos o productos → el PO reclasifica a Discovery.
- La mini-matriz con VoBo y su checklist de no regresión son el criterio de aprobación de la mejora en `mock testing` (I-07).
- QA propone; el PO decide las reglas y da el VoBo con un único comentario. Sin `po-vobo` no hay `to do`.
- El MCP es de solo lectura: QA pega y publica.
