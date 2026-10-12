# SDLC IOND — Fuente canónica de estados, roles, campos, tags, comentarios y automatizaciones

> **Versión:** 2.3 — 2026-10-11 (incorpora las decisiones Q-01 a Q-55)
> **Estado:** Vigente. Propuesta por Steve Nina — Scrum Master IOND.
> **Aplica a:** IOND · IonMind · StageMind — Espacio ClickUp **NEW GATEWAY IOND** (`90171116803`)
> **Propósito:** Única fuente de verdad del flujo SDLC de IOND. Los documentos de `docs/sdlc-iond/` (Acuerdo de trabajo, Estándar de QA, guías de ClickUp, dashboards) se derivan de este archivo. Las skills del catalyst (`SKILL.md` y `skills/`) lo usan como Regla #1. Las suites de prueba del release viven en `knowledge/test-suites/`.
> **Convenciones:** los nombres de estado se escriben **exactamente** como en ClickUp (`minúsculas`). Cada regla remite a su decisión `Q-xx` del *Registro de Decisiones* (`docs/sdlc-iond/src/03-preguntas-inconsistencias-riesgos.md`). Las tareas aún abiertas figuran allí como *Acciones de verificación* (AV-xx).

---

## 0. Principios del flujo

1. **El PO define la necesidad y la prioridad; QA documenta los requerimientos; el PO da su VoBo con un comentario; Development construye solo lo acordado; QA valida contra lo acordado.**
2. **La Matriz de Requerimientos con VoBo del PO es el criterio oficial de aceptación y rechazo.** Lo que no está en ella no es motivo de rechazo: se registra como requerimiento o ticket nuevo.
3. **Sin aprobación punto por punto:** el PO valida la matriz completa con un único comentario de VoBo.
4. **Ante un desacuerdo no se asume ni se continúa con interpretaciones distintas:** se escala al PO el mismo día.
5. **Avance sin bloqueos:** si una duda afecta a un requerimiento (p. ej. REQ-03), se sigue avanzando con los demás mientras se resuelve.
6. **Trazabilidad en ClickUp:** toda transición relevante deja su comentario estándar (sección 14). Lo que no está en el ticket no existe.
7. **Documentación proporcional** a la complejidad e impacto del cambio.
8. **Los tickets cierran en su propio kanban** (`merged`). El tablero de Releases gestiona versiones, no tickets.

---

## 1. Tableros

| Tablero | Tipo | ID ClickUp | Propósito |
|---|---|---|---|
| **Discovery** | Kanban (lista) | `901717038641` | Funcionalidades nuevas, refactorizaciones y cambios estructurales o de reglas de negocio, desde la idea hasta el merge. |
| **Improvements** | Kanban (lista) | `901717038640` | Bugs, hallazgos de QA/Pilot, mejoras puntuales y deuda técnica acotada, sin cambios en reglas de negocio troncales. |
| **Releases** | Folder de sprints semanales | `901711332702` | Una **tarea de Release por versión de producto** por semana; flujo de la Release Candidate (RC) hasta el Go/No-Go. |

Folder contenedor de los kanbans: **SDLC [GATEWAY/IOND]** (`901711332688`). Los folders legacy (Sprints/Deployment/Old Sprint/Preparations/QA [Gateway/ION]) **siguen operando** y quedan fuera de este flujo.

---

<!-- BEGIN:roles -->
## 2. Roles

| Código | Rol | Responsabilidad en el SDLC |
|---|---|---|
| **PO** | Product Owner | Define la necesidad de negocio y la prioridad. Da el **VoBo** de la Matriz de Requerimientos. Resuelve dudas y desacuerdos. Decide `invalid`, alcance y UAT. Clasifica los tickets de Discovery y aprueba la clasificación de bugs. Vota en el Go/No-Go. Un PO por producto (en IOND la misma persona para los tres — `Q-01`). |
| **SM** | Scrum Master | Facilita el flujo, vela por los acuerdos, gestiona `blocked` e impedimentos, facilita Pilot y ceremonias, **crea la tarea de Release** (con verificación del Dev) y audita el cumplimiento en ClickUp. Si el SM es parte de un desacuerdo, facilita el LD/RM (`Q-03`). |
| **LD** | Lead Dev | Hace el **`assignment`**, valida la arquitectura en R&D y Prototype Review, hace o coordina el **Code Review** y decide con el PO la prioridad de los bugs de release. En IOND el LD **es también el RM**; sus PRs los revisan **dos miembros del equipo con mayor antigüedad y ambos deben aprobar** (`Q-02`). Asigna un Dev como assignee en `assignment` (`Q-46`). |
| **DEV** | Developer | Investigación (R&D), prototipo, desarrollo según la matriz, pruebas unitarias, handoff a QA y correcciones. |
| **QA** | Quality Assurance (Analista de Calidad y Requerimientos) | Redacta la **Matriz de Requerimientos** (con casos fuera de alcance), diseña y ejecuta la **Matriz de Pruebas** en `mock testing` y ejecuta Smoke, Sanity y Regression en el Release. |
| **LQA** | Lead QA | Asigna el QA del ticket (**Reviewer QA**): en Discovery **desde `assignment`**, junto con el Dev que asigna el LD, para que el QA siga el R&D y el `prototype review` y llegue listo a redactar la matriz en `requirements`; en Improvements, al entrar a `requirements` o a `ready for qa` (`Q-55`). Gestiona la capacidad de QA, certifica la calidad del release y vota en el Go/No-Go. |
| **RM** | Release Manager | Gestiona `ready to merge` → `merged` (merge a la rama RC), conduce `dev preparation`, despliega el build de cada ticket en el ambiente de QA con los workflows de DevOps (`Q-04`) y coordina el despliegue a producción. En IOND es la misma persona que el LD. |
| **SH** | Stakeholders | Negocio, clientes y equipos consumidores (internos o externos). Aportan validación de negocio en Request, Prototype, Pilot y UAT. Si no pueden asistir, participan de forma asíncrona por video (`Q-06`). |
| **DEVOPS** | DevOps (equipo externo) | Prepara los workflows de despliegue (ambiente de QA, preprod y producción), ejecuta el despliegue a producción y opera la infraestructura. |

> **Soporte:** no es un rol del equipo IOND. Se trabaja con el **servicio de soporte general de la empresa**, que reporta incidentes (carril de hotfix o `backlog`) y recibe las release notes de cliente.

### 2.1 Asignación actual (confirmada el 2026-10-09)

| Rol | Persona | Estado |
|---|---|---|
| PO (IOND, IonMind y StageMind) | Marcel Herrera Rendón | Confirmado (`Q-01`) |
| SM | Steve Nina | Confirmado |
| LQA | Steve Nina | Confirmado |
| QA (2) | Steve Nina · Mijael Rojas | Confirmado (2 QAs) |
| RM | Rodolfo Merlo Ali | Confirmado |
| LD | Rodolfo Merlo Ali (es también el RM) | Confirmado (`Q-02`) |
| DevOps | Equipo externo | Confirmado |

> ⚠️ Concentración de roles: SM, QA y LQA recaen en la misma persona; LD y RM en otra. Salvaguardas: los PRs del LD/RM los aprueban dos miembros con mayor antigüedad; cuando el SM es parte de un desacuerdo facilita el LD/RM; el Go/No-Go es colegiado (PO + LQA + RM). Ver `R-07` y `R-08`.
<!-- END:roles -->

---

<!-- BEGIN:clasificacion -->
## 3. Clasificación del ticket y campo TYPE

### 3.1 ¿Discovery o Improvements?

Un ticket va a **Discovery** si cumple **al menos una** condición:

- Nace de un requerimiento de cliente que se maneja como proyecto.
- Crea o modifica una **regla de negocio** del producto (billing, planes, permisos, consumo, marketplace, etc.).
- Impacta **más de un módulo, servicio, repositorio o producto** (p. ej. iond + IonMind).
- Requiere **investigación técnica (R&D)** o cambios de arquitectura o de contrato de API.
- Es una funcionalidad nueva, una refactorización o un cambio estructural.

Va a **Improvements** cuando es un bug, un hallazgo de QA/Pilot/UAT, una mejora puntual de bajo impacto (UI/UX, textos, validaciones) o deuda técnica acotada a un módulo, **sin** cambiar reglas de negocio troncales.

**Quién clasifica (`Q-15`):** en Discovery clasifica el **PO**. En los bugs, **QA clasifica** según su criterio (tablero, TYPE y prioridad = severidad) y el **PO aprueba** la clasificación en el triage (C-33).

**Escalamiento:** si en `requirements` una mejora resulta compleja o toca reglas troncales, el **PO** la reclasifica a Discovery (`idea/request`).

### 3.2 TYPE (naturaleza del ticket, independiente del tablero)

| TYPE | Uso | Tablero habitual |
|---|---|---|
| `New Feature` | Capacidad nueva para el usuario | Discovery (Improvements solo si es pequeña y sin regla de negocio, con `requirements` obligatorio) |
| `Improvement` | Mejora de algo existente | Improvements (Discovery si toca reglas o varios módulos) |
| `Bug` | Comportamiento que contradice lo especificado o esperado | Improvements |
| `Refactor` | Cambio interno sin cambio funcional esperado | Discovery si es estructural; Improvements si es acotado |
| `Task` | Trabajo técnico u operativo sin entrega funcional directa (configuraciones, integraciones de datos, spikes) | Ambos |

> Valores y definiciones confirmados (`Q-43`).
<!-- END:clasificacion -->

---

## 4. Orden y tipo de estados en ClickUp (`Q-41`)

**Decisión:** se mantienen los tipos actuales de ClickUp. `uat`, `ready to merge` y `merged` son de tipo **Done**; `merged` es el **último estado y el cierre del flujo**; `invalid` es el único **Closed**. Dos ajustes de configuración (los aplica el SM — AV-04):

- **Discovery:** `to do` pasa de *Not started* a **Active** y se ubica después de `requirements`; se crea `blocked` (Active); `uat` se ubica antes de `ready to merge`.
- **Ambos tableros:** `done w/d` (hoy Active) pasa a **Done**, porque cierra subtareas.
- **Improvements:** se intercambia el orden de `to do` y `requirements`.

ClickUp ordena los grupos así: *Not started* → *Active* → *Done* → *Closed*.

| # | Discovery | Tipo | # | Improvements | Tipo |
|---|---|---|---|---|---|
| 1 | `idea/request` | Not started (open) | 1 | `backlog` | Not started (open) |
| 2 | `assignment` | Not started | 2 | `requirements` *(opcional)* | Not started |
| 3 | `r, d & architect review` | Active | 3 | `to do` | Not started |
| 4 | `prototype review` | Active | 4 | `dev in progress` | Active |
| 5 | `requirements` | Active | 5 | `code review` | Active |
| 6 | `to do` | Active | 6 | `ready for qa` | Active |
| 7 | `dev in progress` | Active | 7 | `mock testing` | Active |
| 8 | `pilot presentation` | Active | 8 | `blocked` *(transversal)* | Active |
| 9 | `code review` | Active | 9 | `ready to merge` | Done |
| 10 | `ready for qa` | Active | 10 | `done w/d` *(subtareas)* | Done |
| 11 | `mock testing` | Active | 11 | **`merged`** *(cierre)* | Done |
| 12 | `blocked` *(transversal)* | Active | 12 | `invalid` | Closed |
| 13 | `uat` *(condicional)* | Done | | | |
| 14 | `ready to merge` | Done | | | |
| 15 | `done w/d` *(subtareas)* | Done | | | |
| 16 | **`merged`** *(cierre)* | Done | | | |
| 17 | `invalid` | Closed | | | |

**Releases** (sin cambios): `dev preparation` (open) → `unit test & ci` → `smoke` → `sanity` → `regression` → `ready for release` (closed).

**Efecto en las métricas:** las tarjetas nativas de *Lead time* y *Cycle time* de ClickUp se detienen en el **primer estado Done** (`uat` o `ready to merge`). El tiempo total hasta `merged` se mide sumando *Time in Status* (ver el documento 07).

> **Sin `uat` en Improvements (`Q-30`):** en un caso muy excepcional que requiera validación del cliente, el **PO** decide si se valida en el `sanity` del release o si el ticket pasa a Discovery.

---

<!-- BEGIN:estados-discovery -->
## 5. Discovery — ficha por estado

**Flujo feliz (primera vez):**
`idea/request` → `assignment` → `r, d & architect review` → `prototype review` → `requirements` → `to do` → `dev in progress` → `pilot presentation` → `code review` → `ready for qa` → `mock testing` → [`uat`] → `ready to merge` → `merged`

**Ciclo de rechazo (QA):** `mock testing` → `to do` → `dev in progress` → `code review` → `ready for qa` → `mock testing` (**no vuelve a pasar por `pilot presentation`**).

### D-01 · `idea/request`
- **Tipo:** open · **Owner (A):** PO · **Quién mueve:** PO → `assignment` / `invalid`
- **Reunión:** obligatoria — SH + PO + LD + QA (refinamiento; se agrupa en la **Discovery Review** semanal, en un día dedicado que se acuerda con el SH — `Q-07`, AV-01).
- **Entrada:** ticket creado con la plantilla **T-01** y los campos TYPE, Project e Iond Subcategory (si Project = Iond).
- **Salida:** historia de usuario con criterios de aceptación de alto nivel, valor de negocio validado por SH y prioridad asignada. Comentario **C-01**.
- **SLA:** se refina en la siguiente *Discovery Review*.

### D-02 · `assignment`
- **Tipo:** unstarted · **Owner (A):** **LD** (Dev) · **LQA** (QA) · **Quién mueve:** el LD asigna un Dev como **assignee** (`Q-46`) y el LQA asigna el **Reviewer QA** (`Q-55`); el Dev acepta y mueve a `r, d & architect review`.
- **Reunión:** no obligatoria.
- **Entrada:** request refinado y priorizado.
- **Salida:** Dev asignado (assignee), **Dev Reviewer** definido, **Reviewer QA** asignado por el LQA y tamaño estimado (S/M/L). El Dev confirma que tiene la información básica. Comentario **C-02**.
- **Por qué el QA se asigna aquí (`Q-55`):** el mismo QA sigue el R&D y el `prototype review`, redacta la matriz en `requirements` y ejecuta `mock testing`, sin traspasos de contexto.
- **SLA:** 1 día hábil.

### D-03 · `r, d & architect review`
- **Tipo:** active · **Owner (A):** LD (aprueba) · **Responsable (R):** Dev · **Quién mueve:** Dev → `prototype review` una vez aprobado por el LD.
- **Reunión:** no obligatoria (sincronización técnica Dev–LD puntual).
- **Entrada:** Dev asignado.
- **Salida:** spike/POC documentado — opciones, recomendación, repos afectados, borrador del contrato de API, dependencias, riesgos y requisitos no funcionales — **aprobado por el LD** en comentario **C-03**. Los spikes se crean como **subtareas** de la funcionalidad y cierran en `done w/d` (`Q-14`).
- **Timebox (Q-08):** S ≤ 1 día · M ≤ 3 días · L ≤ 5 días.
- **QA (Reviewer QA):** sigue el R&D (C-03) para anticipar requisitos no funcionales, dependencias y datos de prueba (`Q-55`).
- **Si es inviable:** el PO decide `invalid` o replantear (`idea/request`).

### D-04 · `prototype review`
- **Tipo:** active · **Owner (A):** PO (decide avanzar) · **Responsables:** Dev (presenta), LD (valida arquitectura), QA (testabilidad y captura inicial de requerimientos) · **SM:** opcional (facilita).
- **Reunión:** **obligatoria — PO + Dev + QA + LD** (SM opcional; SH convocados si aplica).
- **Entrada:** R&D aprobado; prototipo según el tipo de ticket (ver `Q-09`): wireframe/UX navegable, contrato de API (OpenAPI), diseño de board/flow y mapeo de datos, o dataset y criterio de calidad (IA).
- **Salida:** acta **C-04** con la aprobación formal del prototipo y del **contrato de interfaz**. El contrato aprobado pasa a formar parte de la **línea base** de la Matriz de Requerimientos (`Q-10`).
- **Siguiente:** OK → `requirements` · Errores de arquitectura o de concepto → `r, d & architect review`.

### D-05 · `requirements`
- **Tipo:** active · **Owner (A):** PO (VoBo) · **Responsable (R):** QA (el Reviewer QA asignado en `assignment`, redacta) · **Consultados:** Dev, LD · **Quién mueve:** QA → `to do`, **solo con VoBo del PO** (comentario **C-06** + tag `po-vobo`).
- **Reunión:** no obligatoria (QA + Dev; PO si hay dudas).
- **Entrada:** acta de `prototype review`.
- **Salida:**
  - **Matriz de Requerimientos v1** en la descripción del ticket (formato en la sección 9), con su columna **Fuera de alcance**, los datos de prueba y mocks necesarios, y el marcado de REQ críticos.
  - Solicitud de VoBo **C-05**.
  - **Acuse del Dev:** ítem de checklist del ticket *"Matriz de Requerimientos vN leída por el Dev"*, marcado por el Dev (`Q-23`). Las dudas se comentan con **C-07**.
  - VoBo del PO **C-06** + tag `po-vobo`.
- **SLA:** matriz en 1 día hábil (S/M) o 2–3 días (L) · VoBo del PO en 24 h hábiles · respuestas de QA a Dev en < 2 h hábiles.
- **VoBo que no llega (Q-17):** no hay aprobación tácita. A las 24 h QA vuelve a mencionar al PO y el SM lo plantea en la daily. A las 48 h el ticket pasa a `blocked` con `bloq-definicion`.
- **Siguiente:** VoBo → `to do` · Ajustes pedidos por el PO → permanece (matriz v+1) · Inviable → `prototype review`.

### D-06 · `to do`
- **Tipo:** active · **Owner (A):** Dev · **SM:** prioriza la cola · **Quién mueve:** Dev → `dev in progress` al iniciar.
- **Entrada:** (a) primera vez: matriz con VoBo (`po-vobo`) y checklist de acuse marcado; (b) **retorno por rechazo de QA** (comentario **C-14**).
- **Salida:** el Dev toma el ticket.

### D-07 · `dev in progress`
- **Tipo:** active · **Owner (A):** Dev · **Quién mueve:** Dev → `pilot presentation` (primera vez) o → `code review` (si viene de un rechazo).
- **Reunión:** Daily (Dev + SM).
- **Entrada:** ticket en `to do`.
- **Salida:**
  - Código según la matriz.
  - Pruebas unitarias en verde (meta de cobertura ≥ 80 % en código nuevo, si el repositorio lo soporta — `L-11`).
  - Linters limpios.
  - PR(s) registrados en **Merge Request 1–4**.
  - Comentario de handoff **C-09** (*Changes and Specifications Form for QA*).

### D-08 · `pilot presentation`
- **Tipo:** active · **Owner (A):** SM (facilita y da seguimiento) · **Responsable (R):** Dev (presenta) · **Quién mueve:** SM → `code review`.
- **Reunión:** **obligatoria — SH + PO + LD + QA + Dev**. Se agrupa en la *Discovery Review* cuando sea posible.
- **Entrada:** funcionalidad terminada en el ambiente local/dev (solo la **primera vez**).
- **Salida:** acta **C-10** con el visto bueno preliminar del PO/SH. Tratamiento de ajustes (Q-11):
  - **Contradice la matriz** → se corrige dentro del ticket (vuelve a `dev in progress`).
  - **Es nuevo y el PO lo considera imprescindible** para el valor mínimo → cambio de alcance (matriz v+1, tag `cambio-alcance`, nuevo VoBo).
  - **Es nuevo y no imprescindible** → ticket nuevo en Improvements con tag `pilot-feedback`, enlazado al padre.

### D-09 · `code review`
- **Tipo:** active · **Owner (A):** LD · **Quién mueve:** LD (o Dev Reviewer) → `ready for qa` (aprobado) · → `dev in progress` (rechazado).
- **Reunión:** no obligatoria (asíncrona vía PR).
- **Entrada:** PR(s) en Merge Request 1–4; Dev Reviewer asignado.
- **Salida:** PR aprobado por al menos un LD o Senior (los PRs del LD/RM los revisan dos miembros con mayor antigüedad y **ambos deben aprobar**), CI en verde y análisis estático sin fallos (si existe). Comentario **C-11**.
- **SLA:** 1 día hábil.

### D-10 · `ready for qa`
- **Tipo:** active · **Owner (A):** LQA · **Quién mueve:** el QA asignado → `mock testing` al iniciar.
- **Reunión:** no obligatoria (cola).
- **Entrada:** CR aprobado; build de la rama del ticket desplegado en el ambiente de QA, con migraciones y variables aplicadas. **Lo despliega el LD/RM con los workflows preparados por DevOps** (`Q-04`).
- **Salida:** el **Reviewer QA** asignado en `assignment` confirma los **QA Points** y la fecha de inicio; el LQA solo lo reasigna si la capacidad lo exige (`Q-55`). Comentario **C-12**.
- **SLA:** confirmación o reasignación en ≤ 1 día hábil.

### D-11 · `mock testing`
- **Tipo:** active · **Owner (A):** QA · **Quién mueve:** QA → `uat` (con tag `uat-requerido`) / → `ready to merge` (aprobado) / → `to do` (rechazado; **Rejection_count + 1**).
- **Reunión:** no obligatoria (QA con soporte puntual del Dev).
- **Entrada:** ticket asignado; **Matriz de Pruebas** derivada de la Matriz de Requerimientos (trazabilidad REQ-ID → TC).
- **Salida:**
  - **100 % de los REQ críticos aprobados** y cero bugs `urgent` abiertos.
  - Comentario de aprobación **C-13** o de rechazo **C-14**, citando REQ-IDs y con evidencia.
  - Hallazgos fuera de la matriz → ticket nuevo con tag `fuera-de-matriz` (**no** bloquean). Comentario **C-17**.
- **Ambiente:** el **ambiente asignado al QA**, con la rama del ticket (`Q-05`). Si una integración no tiene sandbox, la sección *Datos de prueba* de la matriz indica cómo se prueba (mock, colección simulada o cuenta de prueba).

### D-12 · `uat` (condicional)
- **Tipo:** Done (se ubica antes de `ready to merge`) · **Owner (A):** PO · **Responsables:** SH o cliente (validan), SM (coordina), QA (acompaña).
- **Reunión:** convocada — SH + Cliente + PO (+ QA).
- **Aplica solo si:** el ticket tiene el tag `uat-requerido` (lo marca el PO en `requirements`).
- **Entrada:** `mock testing` aprobado; rama del ticket desplegada en el ambiente de QA o preprod (Q-16).
- **Salida:** aprobación formal del PO/cliente en comentario **C-18** → `ready to merge`. Observaciones que contradicen la matriz → `to do` (bug). Observaciones nuevas → ticket nuevo.
- **SLA:** ≤ 3 días hábiles desde la convocatoria.

### D-13 · `ready to merge`
- **Tipo:** Done · **Owner (A):** RM · **Quién mueve:** RM → `merged` durante `dev preparation` del release.
- **Entrada:** QA aprobado (y UAT si aplica); todos los PRs del ticket listos y sin conflictos.
- **Salida:** **versión objetivo** registrada según el Project (Iond.Version, Ionmind.Version, Stagemind.Version o G.Version). Entra al siguiente corte semanal. Sus subtareas en `done w/d` pasan también a `ready to merge` (**A-20**, `Q-53`).

### D-14 · `blocked` (transversal)
- Ver la sección 8.3.

### D-15 · `done w/d` (Done With Dependencies)
- **Tipo:** Done · **Uso exclusivo de subtareas** técnicas de una historia principal.
- **Owner (A):** Dev asignado a la subtarea · **Quién mueve:** Dev.
- **Entrada:** porción de código terminada, validada localmente e integrada en la rama del ticket padre.
- **Salida:** la subtarea se cierra **sin QA individual**; QA valida en el ticket padre. Cuando todas las subtareas cierran se notifica al owner del padre (**A-14**).
- **Sigue al padre (`Q-53`):** cuando el padre pasa a `ready to merge`, sus subtareas en `done w/d` pasan a `ready to merge`; cuando el padre pasa a `merged`, ellas también (**A-20**). Si el padre vuelve a `to do` por un rechazo, las subtareas permanecen en `done w/d` hasta que el Dev reabra la que corresponda.
- **No usar** en tickets padre.

### D-16 · `merged` (cierre)
- **Tipo:** Done (último estado del flujo) · **Owner (A):** RM · **Quién mueve:** RM.
- **Entrada:** PR(s) mergeados a la rama RC de la semana.
- **Salida:** comentario **C-19** con la rama RC, la versión y el enlace a la tarea de Release. Sus subtareas pasan también a `merged` (**A-20**). **El ticket queda cerrado en su kanban.**

### D-17 · `invalid`
- **Tipo:** Closed · **Owner (A):** PO · **Quién mueve:** PO (o el SM por instrucción del PO).
- **Entrada:** decisión del PO (prioridad cambiada, requerimiento obsoleto o duplicado).
- **Salida:** comentario obligatorio **C-22** con el motivo exacto o el enlace al duplicado. Se cierra sin escribir código.
<!-- END:estados-discovery -->

---

<!-- BEGIN:estados-improvements -->
## 6. Improvements — ficha por estado

**Bug:** `backlog` → `to do` → `dev in progress` → `code review` → `ready for qa` → `mock testing` → `ready to merge` → `merged`
**Mejora con criterios:** `backlog` → `requirements` → `to do` → … (igual que el bug)
**Rechazo (QA):** `mock testing` → **`to do`** (+ Rejection_count)

### I-01 · `backlog`
- **Tipo:** open · **Owner (A):** PO (prioriza) · **SM:** ordena y depura · **Registran:** QA, Dev, PO o el soporte general de la empresa, con la plantilla **T-02** (bug) o **T-03** (mejora), idealmente vía Form.
- **Reunión:** *Triage* semanal (PO + QA; LD si hace falta) (`Q-28`).
- **Clasificación (`Q-15`):** QA clasifica cada bug según su criterio (tablero, TYPE y prioridad = severidad) y el PO lo aprueba en el triage.
- **Entrada:** ticket con TYPE, Project, Iond Subcategory y prioridad (para bugs, la prioridad expresa la **severidad**: sección 10). Los bugs llevan el tag de detección `det-*`.
- **Salida:** priorizado y con decisión sobre si pasa por `requirements` (`Q-29`): bug → nunca; mejora → sí cuando el criterio no cabe en ≤ 3 líneas verificables; toca validaciones (cálculos, permisos, datos persistidos) o mensajes visibles para el usuario; o el TYPE es `New Feature`. Comentario **C-33**.

### I-02 · `requirements` (opcional)
- **Tipo:** unstarted · **Owner (A):** PO (VoBo) · **Responsable (R):** QA (el LQA asigna el **Reviewer QA** al entrar — `Q-55`) · **Quién mueve:** QA → `to do` con `po-vobo`.
- **Reunión:** opcional (QA + Dev + LD).
- **Salida:** **mini-matriz** (≤ 5 REQ, con su columna Fuera de alcance), checklist de no regresión de zonas cercanas y checklist de acuse del Dev (`Q-23`). Comentarios **C-05**, **C-06** y tag `po-vobo`.
- **SLA:** QA 1 día hábil · VoBo 24 h hábiles.
- **Escalamiento:** si resulta compleja o toca reglas troncales → el PO reclasifica a Discovery.

### I-03 · `to do`
- **Tipo:** unstarted · **Owner (A):** SM (priorización ágil) · **Quién mueve:** Dev → `dev in progress`.
- **Entrada:** priorizado (y con VoBo si pasó por `requirements`) **o** devuelto por rechazo de QA.

### I-04 · `dev in progress`
- **Tipo:** active · **Owner (A):** Dev · **Reunión:** Daily.
- **Salida:** fix o mejora implementado, **prueba unitaria que certifica la solución del defecto**, PR en Merge Request, handoff **C-09** (versión corta).

### I-05 · `code review`
- **Tipo:** active · **Owner (A):** LD · **Salida:** PR aprobado y CI en verde → `ready for qa` · rechazo → `dev in progress`. Comentario **C-11**.

### I-06 · `ready for qa`
- **Tipo:** active · **Owner (A):** LQA · **Salida:** Reviewer QA asignado por el LQA (o confirmado, si la mejora pasó por `requirements` — `Q-55`); build en el ambiente de QA. Comentario **C-12**.

### I-07 · `mock testing`
- **Tipo:** active · **Owner (A):** QA.
- **Criterio de aprobación:**
  - **Bug:** se cumple el resultado esperado del reporte y pasa el checklist de no regresión de zonas cercanas.
  - **Mejora:** mini-matriz aprobada.
- **Siguiente:** aprobado → `ready to merge` (**C-13**) · rechazo → **`to do`** (**C-14**, Rejection_count + 1).

### I-08 · `ready to merge`
- **Tipo:** Done · **Owner (A):** RM · **Salida:** versión objetivo registrada; entra al corte semanal. Las subtareas en `done w/d` lo acompañan (**A-20**).

### I-09 · `blocked` (transversal)
- Ver la sección 8.3.

### I-10 · `done w/d`
- Igual que **D-15** (solo subtareas; siguen al padre a `ready to merge` y `merged`).

### I-11 · `merged` (cierre)
- **Tipo:** Done (último estado del flujo) · **Owner (A):** RM · **Salida:** PR mergeado a la rama RC; comentario **C-19**; subtareas a `merged` (**A-20**). El ticket queda cerrado en Improvements.

### I-12 · `invalid`
- **Tipo:** Closed · **Owner (A):** PO · **Salida:** comentario obligatorio **C-22**.

> **Sin `uat` en Improvements (`Q-30`):** si un caso muy excepcional requiere validación del cliente, el PO decide si se valida en el `sanity` del release o si el ticket pasa a Discovery.
<!-- END:estados-improvements -->

---

<!-- BEGIN:estados-releases -->
## 7. Releases — tarea de Release, estados, calendario y reglas

### 7.1 Modelo

- Cada semana existe una lista de sprint en el folder **Releases**: `Sprint N (fecha inicio - fecha fin)`.
- El **SM crea una tarea de Release por producto y versión** — `Release <producto> - vX.Y.Z` — con la plantilla **T-04** y la verificación del Dev. La tarea documenta: alcance, tickets incluidos (relación con los tickets y lista), repos y ramas RC, ambiente, prerrequisitos, smoke, plan de regresión, hallazgos y Go/No-Go.
- **Los tickets no se mueven al tablero de Releases**: permanecen en su kanban y cierran en `merged`. La tarea de Release los referencia por relación y por **versión objetivo** (Iond.Version, Ionmind.Version, Stagemind.Version o G.Version, según el Project).
- Si en el corte no hay tickets en `ready to merge` para un producto, **no se crea release** esa semana (Q-32).
- **Datos mínimos de la tarea de Release** (para métricas): **fecha de vencimiento** = viernes del Go/No-Go, **Project**, **versión** (Iond.Version, Ionmind.Version, Stagemind.Version o G.Version) y **relación** con cada ticket incluido. El resultado del Go/No-Go se escribe en **C-29** con el texto normalizado `Decisión: GO | CONDITIONAL GO | NO-GO` (en la plantilla se deja una sola opción; la lectura automática ignora negritas y emoji).
- Todo bug `det-prod` o `hotfix` se **relaciona** con la tarea de Release de la versión donde se detectó (cálculo del change failure rate).

### 7.2 Estados de la tarea de Release

| # | Estado | Tipo | Owner (A) | Qué ocurre | Salida | Timebox (Q-32) |
|---|---|---|---|---|---|---|
| REL-01 | `dev preparation` | open | **RM** | Corte; merge de los tickets en `ready to merge` (versión objetivo) a la rama RC de cada repo; conflictos resueltos; despliegue a preprod; tickets → `merged`. | Ramas RC creadas, builds OK, preprod actualizado y prerrequisitos verificados. Comentario **C-23**. | ≤ 0,5 d (lunes AM) |
| REL-02 | `unit test & ci` | active | LD (pipeline) · Dev | Ejecución automática de las pruebas unitarias de los repos de la RC. Si fallan, bloquean el pipeline. | 100 % en verde. Comentario **C-24**. | Horas (lunes) |
| REL-03 | `smoke` | active | QA | **Smoke maestro** (`Q-47`): la misma lista fija SMK-01…SMK-17 en todo release (login SSO, dashboard, crear y ejecutar un board en test y producción, historial, listados clave, admin y health de iond, IonMind y StageMind). No incluye verificaciones de la versión: esas van en `sanity`. | Smoke OK (**C-25**). Si falla en el core: fix-forward o No-Go. | ≤ 0,5 d (lunes PM – martes AM) |
| REL-04 | `sanity` | active | QA | **Sanity de la versión** (`Q-48`): re-ejecución de los **REQ críticos** de la matriz de cada ticket del release en el ambiente integrado (preprod), más las interacciones entre tickets del mismo módulo o Iond Subcategory. | Todos los tickets validados en conjunto sin efectos colaterales (**C-26**). | ≤ 1,5 d (martes–miércoles) |
| REL-05 | `regression` | active | QA | **Capa 1 — regresión de la versión** (`Q-49`): suite basada en riesgo seleccionada del E2E maestro (baseline crítico + módulos impactados + cross-system iond ↔ IonMind ↔ StageMind ↔ Gateway/ShipEdge Core; extendida si el riesgo es Alto). **Capa 2 — E2E maestro** (`Q-50`): la parte automatizada completa, sin supervisión, y el grupo de rotación manual que corresponde (G1–G4). Usa bot-test donde exista. | Capa 1: flujos críticos al 100 %. Capa 2: fallas analizadas y clasificadas. **C-27** con ambas capas. | Capa 1 ≤ 1 d (jueves) · capa 2 jueves noche, resultados el viernes antes de las 09:00 |
| REL-06 | `ready for release` | closed | **LQA** (certifica) | Mesa de decisión **Go/No-Go** — reunión obligatoria **PO + LQA + RM** (Q-35) al cerrar `regression`. La tarea pasa a `ready for release` solo con GO o CONDITIONAL GO; con NO-GO permanece en `regression` (Q-35). | Decisión GO / CONDITIONAL GO / NO-GO (**C-29**), release notes, plan de rollback verificado y ventana de despliegue con DevOps. | ≤ 0,5 d (viernes AM) |

### 7.3 Actividades posteriores (sin estado en ClickUp; se registran como comentario en la tarea de Release)

| Código | Actividad | Owner | Salida |
|---|---|---|---|
| ACT-01 | **Deployment** | LD/RM coordina · **DevOps ejecuta** · el PO comunica a clientes | Despliegue ejecutado; comentario **C-30** con fecha/hora, versiones y repos. |
| ACT-02 | **Validación post-despliegue** | QA (smoke maestro en producción con la **company de prueba**, ≤ 2 h, `Q-52`) · LD/RM con DevOps (monitoreo 48 h) | Comentario **C-31** (incluye la limpieza de los datos creados); los incidentes abren `hotfix`. |
| ACT-03 | **Exploratory testing / Bug bash** | QA + Dev + SM | Sesión quincenal de 60–90 min (Q-39); hallazgos → `backlog` con `det-exploratorio`. |
| ACT-04 | **Validación continua en producción** | PO + QA (con los reportes del soporte general de la empresa) | Incidentes → `hotfix` o `backlog` con `det-prod`. |

### 7.4 Calendario semanal (Q-32)

| Día | Actividad |
|---|---|
| Viernes previo | El SM verifica los candidatos (tickets en `ready to merge` con versión objetivo) y prepara la tarea de Release. |
| Lunes 09:00 | **Corte.** `dev preparation` (RM) + `unit test & ci`. Smoke por la tarde. |
| Martes | Smoke (cierre AM) + Sanity. |
| Miércoles | Sanity. |
| Jueves | Regression capa 1 (día) · E2E maestro capa 2 automatizado (noche) · rotación manual del grupo que corresponde. |
| Viernes 09:00 | QA consolida la capa 2 en el C-27. |
| Viernes 10:00 | Go/No-Go. Despliegue en la ventana acordada con DevOps (Q-36). Post-despliegue: smoke maestro en producción con la company de prueba. |

### 7.5 Bugs encontrados durante el release

1. **Bug bloqueante (`urgent`)** → **fix-forward** en la misma rama RC. Se registra como subtarea de la tarea de Release con el tag `fix-forward` (comentario **C-28**); el Dev corrige, el LD revisa y QA re-ejecuta la verificación afectada.
2. **Resto de bugs** → según su prioridad, **tickets nuevos en Improvements** (`backlog`, tag `det-smoke` / `det-sanity` / `det-regression`), previa discusión con el **PO y el LD**.
3. Si el fix-forward no está listo en el plazo acordado (Q-34: decisión ≤ 4 h, fix ≤ 1 día): el PO, el LD y el RM deciden entre **revertir el ticket de la RC** (vuelve a `to do` con el tag `diferido`) o **NO-GO**.

### 7.6 Hotfix (incidentes en producción) (Q-38)

Se reporta un incidente (soporte general de la empresa, clientes o monitoreo) → ticket en Improvements (TYPE Bug, prioridad `urgent`, tags `hotfix` + `det-prod`) → `to do` directo (sin backlog) → `dev in progress` → `code review` → `ready for qa` → `mock testing` → `ready to merge` → **Release extraordinario** `Hotfix <producto> - vX.Y.Z+1` (con tag `hotfix`) en el sprint vigente (smoke + sanity focalizado) → despliegue. Lo autorizan el PO y el LD; lo ejecuta el RM.

### 7.7 Suites de prueba del release (`Q-47` a `Q-51`)

| Suite | Alcance | Fuente | Ambiente | Comentario | Peso en el Go/No-Go |
|---|---|---|---|---|---|
| **Smoke maestro** | Única y fija para todo release (SMK-01…SMK-17) | `knowledge/test-suites/smoke-master.md` | Preprod (gate) y producción con la company de prueba | C-25 · C-31 | Core fallido = fix-forward o NO-GO |
| **Sanity** | Propia de la versión: REQ críticos de los tickets del release | Matrices de Requerimientos y de Pruebas de cada ticket | Preprod | C-26 | 100 % de los REQ críticos |
| **Regression capa 1** | Propia de la versión, por riesgo | E2E maestro + mapa Iond Subcategory → módulo + riesgo de la T-04 | Preprod | C-27 (capa 1) | 100 % de los flujos críticos |
| **E2E maestro capa 2** | Todas las features: automatizado completo + rotación manual G1–G4 (maestro completo cada 4 releases) | `knowledge/test-suites/e2e-master.csv` (IDs estables; la hoja "Iond Testing Plan" es la fuente editable) | Preprod | C-27 (capa 2) | Falla = hallazgo; NO-GO solo si es `urgent` provocado por el release |

Los hallazgos de cualquier suite siguen la sección 7.5 (tags `det-smoke`, `det-sanity`, `det-regression`).
<!-- END:estados-releases -->

---

<!-- BEGIN:transiciones -->
## 8. Reglas transversales de transición

### 8.1 Rechazo
- **Discovery:** `mock testing` → `to do` → `dev in progress` → `code review` → `ready for qa` → `mock testing`. **Bypass de Pilot:** ningún ticket corregido tras un rechazo vuelve a `pilot presentation`.
- **Improvements:** `mock testing` → `to do`.
- **Code review rechazado:** → `dev in progress` (no cuenta en Rejection_count).
- Cada rechazo de QA: comentario **C-14** (cita los REQ-ID incumplidos) + **Rejection_count + 1**.
- En el re-test, QA verifica las correcciones **sin exigir repetir etapas ya aprobadas** (Pilot, definiciones).

### 8.2 Criterio de rechazo
- QA rechaza **únicamente** contra la Matriz de Requerimientos con VoBo vigente (incluido el contrato aprobado en `prototype review` cuando la matriz lo referencia — `Q-10`).
- Lo no contemplado **no** es rechazo directo: es un ticket nuevo con `fuera-de-matriz` (**C-17**) y el PO decide la prioridad.
- Implementar algo distinto de lo acordado **sí** es motivo de rechazo.

### 8.3 `blocked` (transversal)
- **Entra:** quien detecta el impedimento, desde cualquier estado activo. Tag de causa obligatorio: `bloq-externo`, `bloq-ambiente`, `bloq-definicion` o `bloq-dependencia`. Comentario **C-20** con el plan de acción. Si aplica, se usa la dependencia nativa de ClickUp (*waiting on*).
- **Seguimiento:** actualización diaria del plan (**C-20**) en la daily (Dev + LD + SM + QA).
- **48 h** → escalamiento automático (**A-13**) a SM + LD (+ PO si es `bloq-definicion`).
- **72 h** → decisión: (a) reprogramar, (b) dividir el ticket, (c) reclasificar a Discovery **solo** si la causa es de alcance o estructura (decide el PO).
- **Sale:** vuelve al estado previo con el comentario **C-21**. El tag `bloq-*` se conserva como historial (métricas de bloqueo por causa).

### 8.4 Desacuerdos (QA ↔ Dev)
1. Registrar en el ticket el punto exacto y la postura de cada parte en 1–2 líneas (**C-15**) y agregar el tag `escalado-po`.
2. Notificar al PO el mismo día (automatización **A-15**).
3. El PO decide (**C-16**, SLA 4 h hábiles) y se retira `escalado-po`.
4. Si hace falta, sincronización de 10 minutos facilitada por el SM. Si el SM es parte del desacuerdo, **facilita el LD/RM** (`Q-03`).
5. La decisión queda registrada en el ticket.

### 8.5 Cambio de alcance (después del VoBo)
1. Solo lo solicita o aprueba el **PO**.
2. QA actualiza la matriz a la versión v+1 y marca las filas cambiadas (**C-08**). Se agrega el tag `cambio-alcance` y se retira `po-vobo` (**A-04**). El tag `cambio-alcance` se conserva como historial; si el ticket ya lo tenía, QA retira `po-vobo` manualmente.
3. El PO vuelve a dar su VoBo (**C-06**) y **luego** se modifica el código.

### 8.6 `invalid`
- Solo el PO decide. Comentario obligatorio **C-22**.

### 8.7 Corte de transición (Q-45)
- Tickets que aún no llegaron a `dev in progress` adoptan el flujo completo (Matriz de Requerimientos + VoBo).
- Tickets en `dev in progress` o más adelante terminan con su documentación vigente y siguen el resto de reglas (rechazo, `merged`, Release).
<!-- END:transiciones -->

---

<!-- BEGIN:matrices -->
## 9. Matrices

### 9.1 Matriz de Requerimientos (en la descripción del ticket, sección `## Matriz de Requerimientos vN`)

| ID | Módulo / Servicio | Requerimiento / Regla | ¿Cuándo aplica? (condición) | ¿Qué debe pasar? (resultado) | Excepciones / Fuera de alcance | Crítico |
|---|---|---|---|---|---|---|
| REQ-01 | Billing / Suscripciones | Regla funcional o de negocio esperada | Escenario o datos que disparan la regla | Respuesta, estado o comportamiento exacto y verificable | Casos NO considerados en esta entrega | Sí/No |

**Reglas:**
- Redacta QA con el apoyo técnico del Dev. **Valida el PO con un único comentario de VoBo** (sin aprobación fila por fila).
- **Parte de la especificación del PO** (historia, criterios y fuera de alcance): QA la **normaliza** en REQ-IDs, completa las condiciones, excepciones y límites, y **no reescribe** lo que ya está claro (`Q-19`).
- **Fuera de alcance** es obligatoria: protege al Dev de exigencias no planificadas y evita que QA reporte como error algo excluido a propósito.
- **Requisitos no funcionales** (rendimiento, seguridad, compatibilidad) como filas `REQ-NF-xx` con métrica (`Q-13`).
- **Salidas de IA** (IonMind/StageMind): el "¿Qué debe pasar?" se expresa con **umbral medible** sobre un dataset definido (`Q-24`).
- **Épicas con subtareas:** una matriz en el ticket padre, con REQ agrupados por subtarea (`REQ-<SUB>-01`) (`Q-12`).
- **Datos de prueba y mocks** necesarios: sección `### Datos de prueba` debajo de la matriz.
- **Versionado:** `vN` en el título de la sección. Cada cambio posterior al VoBo genera v+1 (regla 8.5).

### 9.2 Mini-matriz (Improvements)
Hasta 5 REQ con el mismo formato + checklist de no regresión de zonas cercanas.

### 9.3 Matriz de Pruebas (interna de QA, no requiere VoBo)
- Se usa en `mock testing`, se reutiliza en `sanity` y alimenta la regresión.
- Cada TC referencia su **REQ-ID** (trazabilidad obligatoria) y el tipo (Happy Path, Negativo, Borde, Regresión, NF).
- El veredicto (**C-13** / **C-14**) debe coincidir con el estado registrado en la matriz de pruebas.

### 9.4 Matrices de Release
- **Smoke:** smoke maestro fijo (SMK-01…SMK-17), igual en preprod y en producción; sin verificaciones de la versión.
- **Sanity:** consolidado de los REQ críticos de los tickets del release (`SAN-<ticket>-<REQ>`; bugs sin matriz: `SAN-<ticket>-T-02`) y de las interacciones entre tickets (`SAN-INT-xx`).
- **Regression capa 1:** filas del E2E maestro seleccionadas por riesgo + flujos cross-system (`RGR-xx`).
- **E2E maestro capa 2:** parte automatizada completa + grupo de rotación manual; IDs `E2E-<SIDE>-<MOD>-NNN`.

| | Matriz de Requerimientos | Matriz de Pruebas |
|---|---|---|
| Pregunta | ¿Qué debe hacer el sistema? | ¿Cómo comprobamos que funciona? |
| Momento | `requirements` (antes de desarrollar) | `mock testing` (y `sanity`) |
| Elabora | QA (con apoyo técnico del Dev) | QA |
| Valida | PO (comentario de VoBo) | QA (no requiere VoBo del PO) |
<!-- END:matrices -->

---

<!-- BEGIN:severidad -->
## 10. Severidad de hallazgos (prioridad nativa de ClickUp)

| Prioridad | Severidad | Definición | Efecto en `mock testing` | Efecto en el Release |
|---|---|---|---|---|
| `urgent` | **Bloqueante** | Funcionalidad core rota sin workaround; pérdida o corrupción de datos; seguridad; cobro incorrecto | Rechazo | **Fix-forward** obligatorio o NO-GO |
| `high` | Alta | Funcionalidad importante falla con workaround | Rechazo si incumple un REQ | CONDITIONAL GO solo si el PO acepta el riesgo y se agenda el fix |
| `normal` | Media | Funcionalidad secundaria o UX con impacto moderado | Rechazo si incumple un REQ; si es fuera de matriz, ticket nuevo | No bloquea; ticket en Improvements |
| `low` | Baja | Cosmético | Rechazo solo si incumple un REQ explícito | No bloquea |

> En tickets que no son bugs, la prioridad expresa la **prioridad de negocio** (la define el PO).
<!-- END:severidad -->

---

<!-- BEGIN:campos -->
## 11. Custom fields de IOND

> Los custom fields administrables de IOND son los **13 originales + Stagemind.Version** (lo crea el SM — `Q-42`, AV-04). Entre los campos **heredados**, solo **G.Version** se usa, y únicamente para registrar la versión objetivo de los tickets con Project = Gateway (`Q-44`): se llena su valor, pero no se modifica su configuración. El resto de heredados (`item_type`, `o.version`, `category`, `description`, `repro_points`, `goal_progress`) **no se usan** en el SDLC ni en los dashboards. Cualquier necesidad adicional se cubre con **tags** (sección 12) o con campos nativos (prioridad, assignee, fechas, relaciones, dependencias, checklists).

| Campo | Tipo | Significado | Quién lo llena | Obligatorio desde |
|---|---|---|---|---|
| **TYPE** | Dropdown | Naturaleza del ticket (sección 3.2) | Creador; el PO valida | Creación (`idea/request` / `backlog`) |
| **Project** | Dropdown | Producto: `Iond`, `IONMIND`, `STAGEMIND` o `Gateway` (los tickets de Gateway siguen en el SDLC de IOND — `Q-44`) | Creador | Creación |
| **Iond Subcategory** | Dropdown | Módulo funcional de iond (Boards, Connections, App Connectors, PDF Templates, Billing, API, Nodo X…) | Creador / PO | Creación (si Project = Iond) |
| **Iond.Version** | Dropdown | Versión de iond: `DEVELOPMENT` mientras no tenga destino; `vX.Y.Z` = versión objetivo o entregada | SM / RM | `ready to merge` |
| **Ionmind.Version** | Dropdown | Igual para IonMind (`develop` / `vX.Y.Z`) | SM / RM | `ready to merge` (si Project = IONMIND o hay impacto en IonMind) |
| **Stagemind.Version** *(nuevo)* | Dropdown | Igual para StageMind (`develop` / `vX.Y.Z`) | SM / RM | `ready to merge` (si Project = STAGEMIND o hay impacto en StageMind) |
| **G.Version** *(heredado)* | Dropdown | Versión objetivo de los tickets de Gateway (solo se llena el valor) | SM / RM | `ready to merge` (si Project = Gateway) |
| **Dev Reviewer** | People | Revisor(es) de código | LD | `assignment` |
| **Reviewer QA** | People | QA responsable del ticket: el mismo redacta la matriz y ejecuta `mock testing` | LQA | `assignment` (Discovery) / `requirements` o `ready for qa` (Improvements) — `Q-55` |
| **QA Points** | Number | Esfuerzo de QA estimado (Fibonacci 1-2-3-5-8) | QA | Salida de `requirements` o `ready for qa` |
| **Merge Request** · **Merge Request 2/3/4** | URL | Un PR por repositorio afectado | Dev | Antes de `code review` |
| **Rejection_count** | Number | Rechazos de QA en `mock testing`/`uat` (uno por iteración rechazada) | QA (recordatorio por **A-09**) | Se inicializa en **0** al entrar a `ready for qa` (**A-08**; un número vacío no cuenta como 0 en las métricas) y suma 1 en cada rechazo |

<!-- END:campos -->

---

<!-- BEGIN:tags -->
## 12. Taxonomía de tags (tableros SDLC)

> Los tags son compartidos por todo el espacio y los folders legacy siguen activos: **no se borran tags legacy**. En los tableros SDLC **solo** se usan los siguientes (minúsculas, con guiones):

| Grupo | Tag | Significado | Lo pone | Lo quita |
|---|---|---|---|---|
| **Área (1 por ticket, iond)** | `iond-core` · `iond-uxui` · `iond-infra` · `iond-ia` | Capa técnica principal del cambio | Creador / LD | — |
| **Gobierno del flujo** | `po-vobo` | La matriz vigente tiene VoBo del PO | QA (al recibir **C-06**) o PO | A-04 (por cambio de alcance) |
| | `uat-requerido` | El ticket requiere UAT antes del merge | PO (en `requirements`) | — |
| | `cambio-alcance` | La matriz cambió después del VoBo (v+1) | QA | No se quita (historial para medir la estabilidad de requerimientos); en un cambio posterior, QA retira `po-vobo` manualmente |
| | `escalado-po` | Hay un desacuerdo esperando la decisión del PO | QA o Dev | PO tras decidir (**C-16**) |
| | `fuera-de-matriz` | Ticket nacido de un hallazgo fuera de la matriz | QA | — |
| | `pilot-feedback` | Ticket nacido de un ajuste del Pilot | SM | — |
| **Bloqueo** | `bloq-externo` · `bloq-ambiente` · `bloq-definicion` · `bloq-dependencia` | Causa del `blocked` | Quien bloquea | No se quita (historial de causas); el bloqueo vigente lo indica el estado `blocked` |
| **Detección (bugs)** | `det-mock` · `det-uat` · `det-smoke` · `det-sanity` · `det-regression` · `det-prod` · `det-exploratorio` | Fase en la que se detectó el bug | Quien reporta | — |
| **Release** | `hotfix` | Carril urgente de producción | PO / LQA | — |
| | `fix-forward` | Corrección dentro de la RC | QA / RM | — |
| | `diferido` | Ticket revertido de la RC o pasado a la siguiente versión | RM | Al reingresar |

### 12.1 Mapa de tags legacy a SDLC (no usar en tableros SDLC)

| Tags legacy | Reemplazo en el SDLC |
|---|---|
| `iond-depl-*`, `iond-dpl-4`, `iond-disc-*`, `discovery-1`, `sp*`, `s-*`, `core-s13`, `ion-sp*`, `sprint * retro` | No aplica: el tablero y la tarea de Release dan el contexto |
| `qa-regression-v*`, `qa-regresión-v*`, `qa-smoke(*)`, `qa-gateway*`, `qa-v*`, `qa-reg`, `smoke v*`, `iond-v0.1.x`, `iond-first-release`, `iond-mvp`, `iond-beta` | Iond.Version / Ionmind.Version / Stagemind.Version / G.Version |
| `iond-ib-invalid`, `ib-invalid` | Estado `invalid` |
| `iond-ib-ns` | `fuera-de-matriz` |
| `iond-ib-pending`, `iond-core-issue`, `iond-uxui-issue`, `internal bug`, `internalbug` | TYPE `Bug` + prioridad + `det-*` + tag de área |
| `for-analysis` | Estado (`idea/request` o `r, d & architect review`) |
| `iond`, `ionmind`, `stagemind`, `ionflow`, `ion` | Campo Project |
| `stagemind-v*` (p. ej. `stagemind-v1.3.0`) | Campo Stagemind.Version |
| `deuda técnica`, `technological improvements` | TYPE `Refactor` |
| `flowpilot`, `keycloak`, `ionboard`, `grapp`, `storage`, `iond-flow-integration`, `iond-webcomponent`, `iond-grapp-integration` | Iond Subcategory |
| `ux/ui`, `ioind-ux` | `iond-uxui` |
| `ia`, `ai`, `ia-ionflow` | `iond-ia` |
| `infra`, `deploy` | `iond-infra` |
| Tags de integraciones (`*-gt-se`, `*-ion-se`) | Iond Subcategory (si aplica a iond); si no, flujo legacy |
<!-- END:tags -->

---

<!-- BEGIN:plantillas-tarea -->
## 13. Plantillas de tarea (descripción)

### T-01 · Request de Discovery
```markdown
## Problema / Necesidad
[Qué problema de negocio resolvemos y para quién]

## Historia de usuario
Como [rol], quiero [capacidad] para [beneficio].

## Criterios de aceptación (alto nivel — PO)
- [ ] ...

## Valor de negocio y prioridad
[Impacto, cliente o consumidor, urgencia]

## Stakeholders
@[SH]

## Fuera de alcance (preliminar)
- ...

## Matriz de Requerimientos v1
_(la completa QA en `requirements`)_

## Checklist de acuse (ClickUp checklist)
- [ ] Matriz de Requerimientos vN leída por el Dev
```

### T-02 · Bug (Improvements / Form de intake)
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

### T-03 · Mejora (Improvements)
```markdown
## Situación actual
## Mejora propuesta
## Criterio de aceptación breve
- [ ] ...
## Fuera de alcance
## ¿Requiere `requirements`? [Sí/No — decide PO/QA en backlog]

## Checklist de acuse (solo si pasa por `requirements`)
- [ ] Mini-matriz vN leída por el Dev
```

### T-04 · Tarea de Release (`Release <producto> - vX.Y.Z`)
```markdown
## Información general
| Campo | Valor |
|---|---|
| Producto / versión | |
| Repos y ramas RC | |
| Ambiente de validación | preprod-... |
| Tickets incluidos | [N] — relación + versión objetivo |
| Riesgo | Alto / Medio / Bajo — motivo |

## Prerrequisitos (bloqueantes)
- [ ] Repos desplegados en preprod desde el mismo commit RC
- [ ] Migraciones ejecutadas · variables nuevas configuradas
- [ ] Dependencias de otros productos desplegadas (IonMind / StageMind)
- [ ] Datos de prueba cargados · acceso de QA confirmado

## Suites
| Suite | Matriz / ejecución | Resultado |
|---|---|---|
| Smoke maestro (preprod) | smoke-preprod | |
| Sanity (REQ críticos por ticket) | sanity-matrix | |
| Regression capa 1 (riesgo + cross-system) | regression-matrix | |
| E2E maestro capa 2 (automatizado + grupo G[n]) | e2e-run | |
| Smoke maestro (producción, company de prueba) | smoke-prod | |

## Hallazgos
| ID | Severidad | Fase | Decisión (fix-forward / Improvements / diferido) |

## Go / No-Go
[criterios — ver C-29]

## Despliegue y post-despliegue
[C-30 / C-31]
```
<!-- END:plantillas-tarea -->

---

<!-- BEGIN:comentarios -->
## 14. Plantillas de comentario por transición

> Se copian tal cual en ClickUp. `[...]` = completar. Los comentarios **se publican en el ticket** antes o al momento de mover el estado.

### Discovery — definición

**C-01 · `idea/request` → `assignment` (PO)**
```markdown
## ✅ REQUEST REFINADO → ASSIGNMENT
**PO:** @[po] · **Prioridad:** [urgent/high/normal/low]
**Valor de negocio:** [1–2 líneas]
**Stakeholders:** @[sh]
**Criterios de aceptación de alto nivel:** ver descripción.
@[lead-dev] por favor asignar.
```

**C-02 · `assignment` → `r, d & architect review` (LD, con el QA que asigna el LQA)**
```markdown
## 👤 ASSIGNMENT
**Asignado a:** @[dev] · **Dev Reviewer:** @[reviewer] · **Reviewer QA:** @[qa] (LQA) · **Tamaño:** S / M / L
**Foco de la investigación:** [preguntas técnicas a resolver]
**Timebox R&D:** [fecha]
```

**C-03 · `r, d & architect review` → `prototype review` (Dev + aprobación LD)**
```markdown
## 🔬 R&D CONCLUIDO
**Opciones evaluadas:** 1) ... 2) ...
**Recomendación:** [...]
**Repos afectados:** [...] · **Contrato API (borrador):** [link]
**Dependencias:** [...] · **Riesgos:** [...] · **Requisitos no funcionales:** [...]
**Aprobación LD:** ✅ @[lead-dev]
```

**C-04 · Acta de `prototype review` (SM/PO)**
```markdown
## 🧩 PROTOTYPE REVIEW — ACTA
**Asistentes:** PO @[..] · Dev @[..] · QA @[..] · LD @[..] · (SM / SH)
**Prototipo revisado:** [link wireframe / OpenAPI / diseño de board]
**Decisiones:** 1) ... 2) ...
**Contrato de interfaz aprobado:** [versión/link] — forma parte de la línea base.
**Pendientes para requirements:** [...]
**Resultado:** ✅ Aprobado → REQUIREMENTS / ❌ Volver a R&D (motivo)
```

**C-05 · Solicitud de VoBo (QA → PO)**
```markdown
## 📋 MATRIZ DE REQUERIMIENTOS v[N] LISTA PARA VoBo
@[po] la matriz está en la descripción (sección "Matriz de Requerimientos v[N]").
- REQ totales: [N] · Críticos: [N] · Fuera de alcance: [N]
- Puntos que requieren tu decisión: 
  1. [pregunta + opción recomendada]
- ¿Requiere UAT? [Sí/No — recomendación de QA; decide el PO]
SLA de VoBo: 24 h hábiles. @[dev] cuando la leas, marca el checklist de acuse del ticket.
```

**C-06 · VoBo del PO**
```markdown
## ✅ VoBo PO — Matriz de Requerimientos v[N]
Apruebo la matriz v[N] como criterio de aceptación de este ticket.
Decisiones sobre los puntos abiertos: 1) [...]
UAT: [requerido / no requerido]
```

**C-07 · Dudas del Dev sobre la matriz (opcional)**
```markdown
## ❓ DUDAS SOBRE LA MATRIZ v[N] — @[dev]
1. REQ-[xx]: [duda]
> El acuse de lectura se registra marcando el checklist del ticket (Q-23).
```

**C-08 · Cambio de alcance (matriz v+1)**
```markdown
## 🔁 CAMBIO DE ALCANCE — Matriz v[N] → v[N+1]
**Solicitado por:** @[po] · **Motivo:** [...]
| REQ | Antes | Ahora |
|---|---|---|
@[po] se requiere nuevo VoBo antes de modificar el código.
```

### Discovery / Improvements — construcción y validación

**C-09 · Handoff del Dev (*Changes and Specifications Form for QA*)**
```markdown
## 📦 CHANGES AND SPECIFICATIONS FORM FOR QA
**Resumen del cambio:** [...]
**REQ cubiertos:** REQ-01 ... REQ-0N
**Repos / ramas / PRs:** [repo] — [rama] — [PR]
**Instrucciones para QA:** migraciones [sí/no] · variables [..] · comandos [..] · datos de prueba [..]
**Pruebas unitarias:** [comando] — [N] agregadas — ✅ PASSED · cobertura [..]
**Riesgos o zonas sensibles:** [...]
```

**C-10 · Acta de `pilot presentation` (SM)**
```markdown
## 🎬 PILOT PRESENTATION — ACTA
**Asistentes:** SH · PO · LD · QA · Dev
**Visto bueno preliminar:** ✅ / ⚠️ con ajustes
**Ajustes:**
| # | Ajuste | Tipo | Tratamiento |
|---|---|---|---|
| 1 | [...] | Contradice matriz / Nuevo imprescindible / Nuevo no imprescindible | Corregir en ticket / Cambio de alcance (C-08) / Ticket nuevo #[id] (`pilot-feedback`) |
→ CODE REVIEW
```

**C-11 · Resultado de Code Review (LD)**
```markdown
## CODE REVIEW APROBADO ✅   |   ## CODE REVIEW RECHAZADO ❌
**PR(s):** [...] · **CI:** ✅/❌ · **Análisis estático:** ✅/❌/N.A.
**Observaciones:** [...]
```

**C-12 · `ready for qa` — confirmación del QA (LQA)**
```markdown
## 🧪 READY FOR QA
**Reviewer QA:** @[qa] · **QA Points:** [n] · **Ambiente:** [url] · **Build/rama:** [..]
**Inicio estimado:** [fecha]
```

**C-13 · Aprobación de QA (`mock testing` → `uat` / `ready to merge`)**
```markdown
Estimado @[dev]
**El resultado de pruebas para este ticket es: APROBADO ✅**
**Matriz de Requerimientos:** v[N] (VoBo PO ✅)
| REQ | Resultado | Evidencia |
|---|---|---|
| REQ-01 | ✅ | [link] |
**TCs ejecutados:** [N] — ✅ [n] · ❌ 0 · ⏭️ [n] (justificación)
**Regresión de zonas cercanas:** ✅
**Hallazgos fuera de matriz (no bloquean):** [#id — `fuera-de-matriz`] / Ninguno
**Ambiente / rama / PRs:** [...]
→ [UAT | READY TO MERGE]
```

**C-14 · Rechazo de QA (`mock testing` → `to do`)**
```markdown
Estimado @[dev]
**El resultado de pruebas para este ticket es: RECHAZADO ❌** — Iteración [N] (Rejection_count → [N])
**Matriz de Requerimientos:** v[N]
### OBS-01 — [urgent/high/normal/low] — REQ-[xx] — Estado: Nuevo / Persistente / Regresión
**Área / Flujo:** [...]
**Pasos:** 1. ...
**Resultado esperado (según REQ-[xx]):** [...]
**Resultado actual:** [...]
**Evidencia:** [...]
---
**Hallazgos fuera de matriz (no son causa de rechazo):** [#id]
**Ambiente / rama / PRs:** [...]
→ TO DO
```

**C-15 · Escalamiento de desacuerdo (QA o Dev)**
```markdown
## ⚖️ ESCALADO AL PO — decisión requerida (SLA 4 h hábiles)
**Punto en discusión:** REQ-[xx] / [comportamiento]
**Postura QA:** [1–2 líneas]
**Postura Dev:** [1–2 líneas]
**Impacto si no se decide:** [...]
@[po]
```

**C-16 · Decisión del PO**
```markdown
## 🧭 DECISIÓN PO
**Sobre:** [punto] · **Decisión:** [...]
**Efecto:** [es bug del ticket / se acepta el comportamiento / cambio de alcance (C-08) / ticket nuevo #id]
```

**C-17 · Hallazgo fuera de matriz**
```markdown
## 📝 HALLAZGO FUERA DE MATRIZ (no bloquea este ticket)
**Observación:** [...] · **Por qué está fuera:** [no contemplado en REQ / listado en Fuera de alcance]
**Ticket creado:** #[id] (`fuera-de-matriz`) — prioridad a decidir por @[po]
```

**C-18 · Resultado de UAT**
```markdown
## 🤝 UAT — [APROBADO ✅ / CON OBSERVACIONES ⚠️]
**Participantes:** [cliente / SH] · PO · QA · **Ambiente:** [..]
**Observaciones:** [contradice matriz → bug / nueva → ticket #id]
→ [READY TO MERGE | TO DO]
```

**C-19 · `merged` (RM)**
```markdown
## 🔀 MERGED
**PR(s):** [...] → rama RC [nombre por repo] · **Conflictos:** ninguno / resueltos
**Versión:** [producto vX.Y.Z] · **Tarea de Release:** #[id]
```

**C-20 · `blocked` — inicio y actualización diaria**
```markdown
## ⛔ BLOQUEADO — [bloq-externo / bloq-ambiente / bloq-definicion / bloq-dependencia]
**Desde:** [fecha] · **Estado previo:** [estado]
**Impedimento:** [...] · **Depende de:** @[persona / equipo / ticket]
**Plan de acción:** [...] · **Próxima revisión:** [fecha]
```

**C-21 · Desbloqueo**
```markdown
## ✅ DESBLOQUEADO — vuelve a [estado]
**Resolución:** [...] · **Tiempo bloqueado:** [h/días]
```

**C-22 · `invalid` (PO)**
```markdown
## 🚫 INVALID
**Motivo:** [prioridad cambiada / obsoleto / duplicado de #id / otro: ...]
**Decidido por:** @[po]
```

### Releases

**C-23 · `dev preparation` concluido (RM)**
```markdown
## 🏗️ DEV PREPARATION — [producto vX.Y.Z]
**Corte:** [fecha hora] · **Tickets incluidos:** [N] (relación) · **Diferidos:** [#ids]
**Ramas RC:** [repo → rama] · **Builds:** ✅ · **Preprod:** desplegado [commit]
**Prerrequisitos verificados:** ✅ (ver checklist)
```

**C-24 · `unit test & ci`**
```markdown
## ⚙️ UNIT TEST & CI — [✅ verde / ❌ fallas]
| Repo | Pipeline | Resultado |
```

**C-25 / C-26 / C-27 · `smoke` / `sanity` / `regression` (QA)**
```markdown
## 🧪 [SMOKE | SANITY | REGRESSION] — [producto vX.Y.Z] — [✅ / ❌]
**Ejecutados:** [N] · ✅ [n] · ❌ [n] · ⏭️ [n] · **Automatizados:** [n]
**Hallazgos:** [ID — severidad — decisión: fix-forward / Improvements #id / diferido]
**Evidencia / matriz:** [link]

<!-- Solo en SANITY (C-26) -->
**Por ticket:** [#id → REQ críticos n/n ✅ / ❌] · **Interacciones:** [SAN-INT-xx]

<!-- Solo en REGRESSION (C-27) -->
**Capa 1 (riesgo):** [n/n] · flujos críticos [✅ / ❌]
**Capa 2 (E2E maestro):** automatizado [n/n] · rotación G[n] [n/n] · inestables en cuarentena [n]
```

**C-28 · Bug en RC / fix-forward**
```markdown
## 🩹 FIX-FORWARD — [ID] (urgent)
**Detectado en:** [smoke/sanity/regression] · **Ticket origen:** #[id]
**Decisión:** PO @[..] + LD @[..] — fix en la rama RC · **Plazo:** [..]
**PR del fix:** [...] · **Re-verificación QA:** [pendiente / ✅]
```

**C-29 · Acta Go / No-Go (`ready for release`)**
```markdown
## 🚦 GO / NO-GO — [producto vX.Y.Z]
**Decisión:** 🟢 GO / 🟡 CONDITIONAL GO / 🔴 NO-GO
**Votos:** PO @[..] [✅/❌] · LQA @[..] [✅/❌] · RM @[..] [✅/❌]
**Resultados:** Smoke [..] · Sanity [..] · Regression capa 1 [..] · E2E capa 2 [..]
**Hallazgos abiertos:** [ID — severidad — aceptado por PO / workaround]
**Release notes:** [interna] · [cliente]
**Rollback:** plan verificado ✅ · **Ventana de despliegue:** [fecha hora] con DevOps
```

**C-30 · Despliegue ejecutado (RM)**
```markdown
## 🚀 DEPLOYED — [producto vX.Y.Z] — [fecha hora]
**Ejecutó:** DevOps @[..] · **Coordinó:** RM @[..]
**Repos / versiones:** [...] · **Incidencias:** ninguna / [...]
```

**C-31 · Validación post-despliegue**
```markdown
## 🔎 POST-DEPLOY — [✅ estable / ❌ incidente]
**Smoke en producción (company de prueba):** [n/n] · **Limpieza de datos:** ✅ · **Monitoreo 48 h:** [en curso / OK]
**Incidentes:** [#id hotfix]
```

**C-32 · Apertura de hotfix (PO / LQA)**
```markdown
## 🔥 HOTFIX — [producto] — prioridad urgent
**Incidente:** [...] · **Clientes afectados:** [...] · **Workaround:** [...]
**Autorizan:** PO @[..] · LD @[..] · **Release extraordinario:** Hotfix [producto] vX.Y.Z+1
```

### Improvements — triage

**C-33 · `backlog` → `to do` / `requirements` (PO/SM)**
```markdown
## 🗂️ TRIAGE
**Prioridad:** [..] (bug = severidad) · **¿Requiere requirements?:** Sí / No
**Clasificación confirmada:** Improvements ✅ / reclasificar a Discovery
```
<!-- END:comentarios -->

---

<!-- BEGIN:automatizaciones -->
## 15. Catálogo de automatizaciones (ClickUp Business)

> ClickUp **no impide** transiciones de forma nativa: las reglas se hacen cumplir con automatizaciones **reactivas** (revierten el estado y comentan) más la auditoría del SM (`L-01`). Las condiciones por tag o por custom field vacío deben **verificarse** en el editor de automatizaciones antes de activarlas. Límite del plan Business: ~10.000 ejecuciones al mes.

| ID | Tablero | Disparador | Condición | Acción |
|---|---|---|---|---|
| A-01 | Discovery | Tarea creada | — | Aplicar plantilla **T-01**; estado `idea/request`; agregar al PO como watcher |
| A-02 | Improvements | Tarea creada (o Form enviado) | TYPE = Bug / ≠ Bug | Aplicar **T-02** / **T-03**; agregar al SM como watcher |
| A-03 | Ambos | Estado cambia de `requirements` a `to do` | **No** tiene el tag `po-vobo` | Volver a `requirements` + comentario "Falta VoBo del PO (C-06)" @Reviewer QA @PO |
| A-04 | Ambos | Tag `cambio-alcance` agregado | — | Quitar `po-vobo` + comentario @PO "Matriz v+1 requiere nuevo VoBo" |
| A-05 | Ambos | Estado cambia a `requirements` | — | Comentario recordatorio de SLA (matriz y VoBo) @Reviewer QA |
| A-06 | Ambos | Estado cambia a `code review` | Merge Request vacío | Volver a `dev in progress` + comentario "Registrar el PR en Merge Request" |
| A-07 | Ambos | Estado cambia a `code review` | — | Comentario @Dev Reviewer "Code Review requerido (C-11)" — estandariza la automatización existente |
| A-08 | Ambos | Estado cambia a `ready for qa` (y, en Discovery, a `r, d & architect review`) | Reviewer QA vacío / Rejection_count vacío (solo en `ready for qa`) | Comentario @LQA "Asignar Reviewer QA" (`Q-55`) / establecer Rejection_count = 0 |
| A-09 | Ambos | Estado cambia de `mock testing` (o `uat`) a `to do` | — | Comentario recordatorio "Publicar C-14 y actualizar Rejection_count" @Reviewer QA |
| A-10 | Discovery | Estado cambia de `mock testing` a `ready to merge` | Tiene `uat-requerido` | Mover a `uat` + comentario @PO "UAT requerido" |
| A-11 | Ambos | Estado cambia a `ready to merge` | La versión objetivo del Project está vacía o en `DEVELOPMENT`/`develop` (Iond.Version, Ionmind.Version, Stagemind.Version o G.Version) | Comentario @RM @SM "Registrar la versión objetivo" |
| A-12 | Ambos | Estado cambia a `blocked` | — | Comentario plantilla **C-20**; agregar al SM como watcher; fecha de vencimiento = hoy + 2 días |
| A-13 | Ambos | Llega la fecha de vencimiento | Estado = `blocked` | Comentario de escalamiento @SM @LD (+ @PO si tiene `bloq-definicion`) |
| A-14 | Ambos | Todas las subtareas resueltas | — | Comentario al assignee del padre "Subtareas en done w/d: avanzar el ticket" |
| A-20 | Ambos | El padre cambia a `ready to merge` / a `merged` | Subtareas en `done w/d` / en `ready to merge` | Mover esas subtareas al mismo estado del padre (`Q-53`). Si la acción sobre subtareas no está disponible (AV-10), el RM las mueve a mano como parte del C-23 |
| A-15 | Ambos | Tag `escalado-po` agregado | — | Comentario @PO "Decisión requerida en 4 h hábiles (C-16)"; agregar al PO como watcher |
| A-16 | Ambos | Estado cambia a `invalid` | — | Comentario @PO "Motivo obligatorio (C-22)" |
| A-17 | Improvements | Tag `hotfix` agregado | — | Prioridad `urgent`; estado `to do`; comentario @PO @LD @RM (**C-32**) |
| A-18 | Releases | Estado cambia (cada estado) | — | Comentario con la plantilla correspondiente (**C-23 … C-29**) |
| A-19 | Ambos | Tag `det-prod` agregado | — | Agregar a LQA y LD/RM como watchers; comentario de impacto |

**Automatizaciones existentes:** antes de activar el catálogo, el SM inventaría las automatizaciones actuales (p. ej. el comentario de "Code Review requerido") para evitar duplicados. Ver la guía `06a`.
<!-- END:automatizaciones -->

---

<!-- BEGIN:slas -->
## 16. SLAs y timeboxes consolidados

| Actividad | Plazo | Responsable |
|---|---|---|
| Refinamiento de un request | Siguiente *Discovery Review* (semanal, día dedicado acordado con el SH) | PO |
| `assignment` (Dev, Dev Reviewer y Reviewer QA) | 1 día hábil | LD · LQA |
| `r, d & architect review` | S ≤ 1 d · M ≤ 3 d · L ≤ 5 d | Dev / LD |
| Agenda de `prototype review` | ≤ 3 días hábiles tras la aprobación del R&D | SM |
| Matriz de Requerimientos | 1 día hábil (S/M) · 2–3 días (L) | QA |
| VoBo del PO | 24 h hábiles | PO |
| Respuesta de QA a dudas del Dev | < 2 h hábiles | QA |
| Desacuerdo bloqueante | 4 h hábiles | PO |
| Code review | 1 día hábil | LD |
| Confirmación del QA en `ready for qa` (asignación en los bugs de Improvements) | 1 día hábil | LQA |
| `mock testing` | Según QA Points y la planificación | QA |
| `uat` | ≤ 3 días hábiles desde la convocatoria | PO |
| `blocked` | Actualización diaria · escalamiento a las 48 h · decisión a las 72 h | SM |
| Release semanal | Sección 7.4 | RM / QA / LQA |
| E2E maestro capa 2 | Automatizado jueves noche · rotación ≈ 0,5 d · consolidado viernes 09:00 | QA |
| Decisión de fix-forward | 4 h · fix ≤ 1 día o diferir | PO + LD + RM |
| Hotfix | ≤ 24 h a producción | PO + LD + RM |
| Post-despliegue | Smoke maestro en producción (company de prueba) ≤ 2 h · monitoreo 48 h | QA / LD-RM |
<!-- END:slas -->

---

## 17. Historial

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-09-15 | Primera consolidación (estados, tags, campos y comentarios) sobre la versión previa de los tableros. |
| 2.0 | 2026-10-08 | Reescritura completa: tableros SDLC vigentes (16/12/6 estados), modelo de QA como Analista de Calidad y Requerimientos (Matriz de Requerimientos + VoBo del PO), roles confirmados, `done w/d` = cierre de subtarea, `merged` = cierre, `blocked` transversal, Improvements con `requirements` opcional, Releases semanales con tarea de Release, fix-forward y hotfix, 13 custom fields fijos, taxonomía única de tags, 33 plantillas de comentario y 19 automatizaciones. |
| 2.1 | 2026-10-09 | Decisiones Q-01 a Q-46 incorporadas: PO único para los tres productos; LD = RM con revisión de sus PRs por dos miembros senior (ambos aprueban); facilitador alterno = LD/RM; despliegue a QA por el LD/RM; `mock testing` en el ambiente asignado al QA; Discovery Review semanal; clasificación de bugs por QA con aprobación del PO; acuse del Dev como checklist; sin UAT en Improvements; tipos de estado actuales (Done para `uat`, `ready to merge` y `merged`; `to do` de Discovery y `done w/d` ajustados); campo Stagemind.Version; G.Version para Gateway; asignación del Dev por el LD. |
| 2.2 | 2026-10-10 | Decisiones Q-47 a Q-54: smoke maestro único (preprod y producción con company de prueba); sanity y regresión propias de cada versión; E2E maestro como capa 2 de `regression` (automatizado completo + rotación G1–G4); hoja "Iond Testing Plan" como fuente editable del E2E maestro con IDs estables; `done w/d` sigue al padre a `ready to merge` y `merged` (A-20); el catalyst lee bot-test sin modificarlo. |
| 2.3 | 2026-10-11 | Decisión Q-55: el LQA asigna el Reviewer QA en `assignment` (Discovery) para que el QA siga el R&D y el prototipo y llegue listo a `requirements`; en Improvements, al entrar a `requirements` o a `ready for qa`. Ajustados D-02, D-03, D-05, D-10, I-02, I-06, el campo Reviewer QA, C-02, C-12, A-08 y los SLAs. |
