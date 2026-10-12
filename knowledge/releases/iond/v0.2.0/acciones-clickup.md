# Acciones en ClickUp — release beta iond v0.2.0 + IonMind v1.10.2

> El catalyst **no escribe en ClickUp** (MCP de solo lectura). Esta lista la ejecutan a mano el **SM** y el **RM** antes del corte del **lunes 2026-10-12 09:00**. Marcar cada casilla al aplicarla.
> El detalle de cada ticket (estado, Project, PRs, veredicto, QA) está en `tickets-principales.csv` y `tickets.csv`.

## 1. Tareas de Release (SM)

- [ ] **Reutilizar** [86e39jadr](https://app.clickup.com/t/86e39jadr) `Release iond - v0.2.0`:
  - moverla de *Sprint 1 (9/14 - 9/20)* a *Sprint 5 (10/12 - 10/18)* del folder Releases (la lista ya existe: `901717579387`);
  - reemplazar la descripción por `ticket-86e39jadr.md` (misma plantilla del ticket, actualizada con el alcance y las suites de la beta);
  - fecha de vencimiento: **2026-10-16**;
  - Project = Iond;
  - Iond.Version = `v0.2.0`;
  - assignee: RM;
  - watchers: PO, LQA y QA.
- [ ] **Crear** `Release IonMind - v1.10.2` desde T-04 en la misma lista (*Sprint 5 (10/12 - 10/18)*):
  - descripción: el bloque T-04 de `knowledge/releases/ionmind/v1.10.2/release-task.md`;
  - fecha de vencimiento: 2026-10-16;
  - Project = IONMIND;
  - Ionmind.Version = `v1.10.2`.
- [ ] **Relacionar** las dos tareas de Release entre sí. IonMind se despliega primero.
- [ ] Relacionar cada ticket principal con su tarea de Release (relación nativa): 49 con la de iond (incluida la informativa 86e1m3jf8) y 2 con la de IonMind.

## 2. Versión objetivo (SM / RM)

Si la opción no existe en el dropdown, agregarla y anotarla en la bitácora del Anexo B de la guía 06a.

- [ ] **Iond.Version = `v0.2.0`** en los 49 principales de iond y en sus 30 subtareas. Hoy tienen `DEVELOPMENT`.
- [ ] **Ionmind.Version = `v1.10.2`**:
  - en los principales de IonMind: 86e2t9962 y 86e1fknjv (con 86e1fkxz7, 86e1fky0g y 86e1qzefc);
  - 86e1fky0g (`ion_gateway_ion#17`) y 86e1qzefc (`ion_gateway#16`) tienen el PR en repos de iond: llevan **también** Iond.Version `v0.2.0` para que el RM los incluya en la RC de iond;
  - en los tickets de iond con PR en `ai_ionmind`, para que su PR entre a la RC de IonMind: 86e20nmqx, 86e2e8gde, 86e2ft73m, 86e2p459r, 86e2mt70g, 86e25j0rn y 86e2j43eg (con sus 4 subtareas).
- [ ] **86e2jwrvc** tiene Iond.Version `v0.1.0`. Confirmar con el RM si ya salió en v0.1.x. Si no salió, cambiar a `v0.2.0`; si ya salió, quitarlo del release.

## 3. Datos a corregir (SM, con el PO)

- [ ] **86e3085ap** (Flow Pilot, error 402) tiene Project = **Gateway**, pero es una funcionalidad de iond. Propuesta: Project = Iond y Iond.Version = `v0.2.0`. Si el PO lo mantiene como Gateway, usar G.Version.
- [ ] **86e1r4bu7** tiene Project = **"iod"** → corregir a `Iond`.
- [ ] **Rejection_count** distinto de los rechazos registrados en los comentarios. Hay que alinearlo con el número de C-14; la comparación completa está en `tickets-principales.csv` (columnas `rejection_count_campo` y `rechazos_qa_comentarios`). Casos detectados:
  - 86e25dyyz: campo 1, 2 rechazos;
  - 86e1gr6ug: campo vacío, 1 rechazo;
  - 86e2fazfh: campo vacío, 1 rechazo;
  - 86e1kp55k: campo vacío, 2 rechazos;
  - 86e1pzyug: campo vacío, 2 rechazos;
  - 86e2mt70g: campo vacío, 1 rechazo;
  - 86e25j0rn: campo vacío, 1 rechazo.
- [ ] **86e1fkxz7**: Iond Subcategory y versiones vacías → Subcategory `App Connectors`.
- [ ] **86e2dpfek**: sin Iond Subcategory → `Infra` (es un fix de build).
- [ ] Tags con variantes (`iond-dpl-4` contra `iond-depl-4`) en 86e22fzq9, 86e29e6jt y 86e1r2c6z: unificar en la limpieza de tags (Anexo A). También hay tags de despliegue que no coinciden con el sprint (86e1kp55k, 86e22q9h8, 86e1gr6ug) y tickets sin tag de despliegue (86e2g4ev0, 86e2j43eg, 86e04qn0d, 86e22q3pc, 86e22fzt2, 86e3085ap).
- [ ] **Campo de MR desactualizado**: los PRs que figuran solo en comentarios están marcados *(comentario)* en `tickets.md` § *PRs por repositorio* (86e1r4bu7, 86e1kp55k, 86e25dyyz, 86e1r2c6z, 86e22fzrp, 86e1gr6ug, 86e29hc1r). El RM los confirma y completa el campo antes del corte.

## 4. Estados (RM, en `dev preparation`)

- [ ] **Websockets 86e35wv7f** está en `mock testing`. QA cierra su validación antes del corte (C-13) → `ready to merge`. Si aparece un hallazgo después del corte → fix-forward (C-28).
- [ ] **Tickets en `production deploy`** (64, en las listas legacy Sprint 4 a 8). Por el corte de transición (`Q-45`) terminan con su documentación vigente. Cuando el RM mergea su PR a la RC, pasan al estado final de su lista (equivalente a `merged`) y llevan C-19.
- [ ] **Tickets en `ready to merge`** (16, en Discovery, Improvements y Sprints 5 a 7) → `merged` con C-19 al integrarse a la RC.
- [ ] **Subtareas** (A-20): acompañan al padre a `ready to merge` y `merged`. Si A-20 no está activa, el RM las mueve a mano en el C-23.
- [ ] **86e2t9962** (minado en tiempo real) se resolvió reiniciando pods, sin código. No hay nada que mergear: se verifica en el sanity y se cierra con C-19 indicando "sin cambio de código".
- [ ] **86e1m3jf8** (pricing, estado legacy `release approval`): el PO confirma su cierre como entregable de definición (fuera de pruebas).
- [ ] **86e1pzz9j** (overage con Stripe Meters): quedó fuera del alcance B y no tiene desarrollo → proponer `done w/d` (OBS-03).
- [ ] **86e1y463z** (NOVASPHERE): el último veredicto visible es RECHAZADO. El LQA confirma si hubo un ciclo aprobado antes del corte (OBS-01).
- [ ] **86e2p459r**: tiene un comentario "Rama en IOND cerrada"; el RM confirma que `ai_ionmind#16` y `ion_gateway_ion#39` entran a las RC (OBS-05).

## 5. Comentarios a publicar

| Cuándo | Comentario | Quién | Borrador |
|---|---|---|---|
| Lunes AM | C-23 en la tarea de Release de iond | RM | `comments/C-23-2026-10-12.md` |
| Lunes | C-24 | LD | — |
| Martes AM | C-25 (smoke preprod) | QA | Se genera al ejecutar `release/smoke` |
| Miércoles | C-26 (sanity) | QA | `release/sanity` |
| Viernes 09:00 | C-27 (capa 1 y capa 2) | QA | `release/regression` + `release/e2e` |
| Viernes 10:00 | C-29 (Go/No-Go) | LQA | `go-no-go.md` |
| Viernes | C-30 / C-31 | RM / QA | `deployment-protocol.md` |
