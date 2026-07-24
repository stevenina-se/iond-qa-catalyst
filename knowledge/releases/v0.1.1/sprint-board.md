# Sprint 4 — Board de Planificación v0.1.1

> **Sprint**: 4 | **Período**: 6 Jul – 17 Jul 2026
> **Target Version**: v0.1.1 (regression fixes de v0.1.0 + features del sprint)
> **Hoy**: Jueves 9 Jul (Día 4 de 10)
> **Tickets totales**: 31

---

## Cutoff Dates

| Milestone | Fecha | Día | Significado |
|-----------|-------|-----|-------------|
| **DEV CUTOFF** | Vie 10 Jul | D5 | Último día para completar desarrollo |
| **CR CUTOFF** | Mar 14 Jul | D7 | Último día para aprobar Code Review |
| **DEPLOY** | Mar 14 Jul | D7 | Deploy a dev-app.ionflow.io |
| **QA CUTOFF** | Mié 15 Jul | D8 | Último día para que QA comience testing |
| **QA FREEZE** | Jue 16 Jul | D9 | Último día para completar QA testing |
| **DEADLINE** | **Vie 17 Jul** | **D10** | Todo aprobado → ready to merge |

```
Jul:  6    7    8    9    10   |  13   14   15   16   17
      L    M    X    J    V   |  L    M    X    J    V
      D1   D2   D3   D4   D5 |  D6   D7   D8   D9   D10
      ─── SEMANA 1 ──────────|──── SEMANA 2 ──────────
                     HOY  DEV |       CR    QA   QA   DEADLINE
                         CUTOFF     CUTOFF START FREEZE
                              |
      ◄── Dev window ────────►|◄─── QA window ───────►
```

> [!IMPORTANT]
> **Quedan 6 días hábiles** (Vie 10 + Lun-Vie 13-17).
> Todo ticket que no esté en `code review` para el **Vie 10** tiene riesgo alto.
> Todo ticket que no esté en `qa testing` para el **Mié 15** NO entrará en v0.1.1.

---

## Tickets v0.1.1 — Regression Fixes (Categoría A)

> Bugs encontrados en v0.1.0 → target: v0.1.1

| # | Ticket | Descripción | Status | Prior. | Dev | Riesgo | ETA QA |
|---|--------|-------------|--------|--------|-----|--------|--------|
| 1 | IONF-1121 | Boards — False unsaved alert | ✅ **QA APPROVED** | 🟠 | Gustavo | 🟢 | ✅ Done |
| 2 | IONF-1126 | PDF Templates — Unsaved changes | ✅ **QA APPROVED** | 🔴 | Alex | 🟢 | ✅ Done |
| 3 | IONF-1116 | PDF Templates — File size limit | ✅ **QA APPROVED** | 🔴 | Alex | 🟢 | ✅ Done |
| 4 | IONF-1007 | Error UTC/Local Schedules | 🔬 qa in process | 🔴 | Enrique | 🟢 | Jul 10-14 |
| 5 | IONF-1030 | Mejoras interface dualtrack | 🔬 qa in process | 🟠 | Jose Enrique | 🟢 | Jul 10-14 |
| 6 | IONF-1128 | Boards — Simple Decision strings | 👀 code review | 🔴 | Gustavo | 🟡 | Jul 15 (si CR aprueba Jul 14) |
| 7 | IONF-1127 | Boards — Scheduler error status | 👀 code review | 🔴 | Enrique | 🟡 | Jul 15 (si CR aprueba Jul 14) |
| 8 | IONF-1114 | Connections — API Key duplicada | 👀 code review | 🔴 | Gustavo | 🟡 | Jul 15 (si CR aprueba Jul 14) |
| 9 | IONF-1141 | App Connectors — nodos minados | 🔨 fortification | 🟠 | Jhoel | 🔴 | No viable sin aceleración |
| 10 | IONF-1119 | PDF Templates — error 500 imagen | 📥 sprint intake | 🟠 | Jose Enrique | 🔴 | No viable |
| 11 | IONF-1043 | Auto-mapper PDF Template | 📥 sprint intake | 🟠 | Alex | 🔴 | No viable |

### Resumen de Regression Fixes

```
✅ Completados:  3/11  (IONF-1121, 1126, 1116)
🟢 On Track:     2/11  (IONF-1007, 1030)
🟡 At Risk:      3/11  (IONF-1128, 1127, 1114) — dependen de CR approval
🔴 Off Track:    3/11  (IONF-1141, 1119, 1043) — no llegarán al deadline
```

> [!WARNING]
> **IONF-1141, 1119, 1043**: Recomendación → mantener en v0.1.1-next.
> Si no se completan en este sprint, pasan al Sprint 5 pero mantienen el target v0.1.1.

---

## Tickets Sprint — Features y Otros (Categoría B)

> Features, mejoras y tickets de otros proyectos que también van a v0.1.1

| # | Ticket | Descripción | Status | Prior. | Dev | Riesgo | Proyecto |
|---|--------|-------------|--------|--------|-----|--------|----------|
| 1 | IONF-1149 | Protocolo Despliegue v0.1.0 | ✅ ready to merge | 🔴 | Rodolfo | 🟢 | Iond |
| 2 | IONF-1049 | Sync logs R2 | ✅ ready to merge | 🟠 | Alex | 🟢 | Iond |
| 3 | IONF-1020 | Monitoreo tokens Flow Pilot | ✅ ready to merge | 🔴 | Jhoel | 🟢 | Iond |
| 4 | IONF-1098 | Confirmación cobro scraping | 📋 qa testing | 🔴 | Jhoel | 🟢 | Iond |
| 5 | IONF-1047 | Gateway ZID — instalar APP | 📋 qa testing | 🔴 | Alex | 🟢 | Gateway |
| 6 | IONF-870 | STAGEMIND v1.4 | 📋 qa testing | 🟠 | Yamil | 🟢 | IonMind |
| 7 | IONF-1076 | Boards templates editables | 👀 code review | 🟠 | Alex | 🟡 | iod |
| 8 | IONF-1075 | Refactorizar registro compañía | 👀 code review | 🟠 | Gustavo | 🟡 | Iond |
| 9 | IONF-1016 | Metodología Delta Ion Mind | 👀 code review | 🟠 | Yamil | 🟡 | IonMind |
| 10 | IONF-1152 | Sync ClickPost-USPS | 🔨 fortification | 🔴 | Rodolfo | 🔴 | Iond |
| 11 | IONF-1044 | Desacoplar chunks órdenes | 🔨 fortification | 🔴 | Rodolfo | 🔴 | Gateway |
| 12 | IONF-845 | Integración Salla | 🔨 fortification | 🟠 | Sonia | 🔴 | Gateway |
| 13 | IONF-1056 | Monetización Stripe | 🚫 blocked | 🔴 | Enrique | 🔴 | Iond |
| 14 | IONF-1067 | Automatización migraciones | 🔨 fortification | 🟠 | Yamil | 🔴 | IonMind |
| 15 | IONF-1014 | IONMIND V1.9 | 🔨 fortification | 🟠 | Yamil | 🔴 | IonMind |

### Tickets que NO entraron al sprint (Categoría C — Backlog)

| Ticket | Descripción | Dev | Notas |
|--------|-------------|-----|-------|
| IONF-1167 | Problemas test y limpieza | Yamil | sprint intake |
| IONF-1166 | Webhook registros cache | Yamil | sprint intake |
| IONF-1154 | App Connector Refactor | Jhoel | sprint intake |
| IONF-1004 | Listings Etsy/WooCommerce | Sonia | sprint intake |
| IONF-858 | Amazon Seller actualización | Sonia | sprint intake |

---

## 📋 Priorización QA

> Orden en que debo testear los tickets cuando estén listos:

### Prioridad 1 — Regression Fixes v0.1.0 (CRÍTICOS)
```
1. IONF-1007  (qa in process, 🔴 high)     → Testear Jul 10-14
2. IONF-1030  (qa in process, 🟠 normal)   → Testear Jul 10-14
3. IONF-1128  (post-CR, 🔴 high)           → Testear cuando deployed (~Jul 15)
4. IONF-1127  (post-CR, 🔴 high)           → Testear cuando deployed (~Jul 15)
5. IONF-1114  (post-CR, 🔴 high)           → Testear cuando deployed (~Jul 15)
```

### Prioridad 2 — Features del Sprint (HIGH priority)
```
6. IONF-1098  (qa testing, 🔴 high)        → Testear Jul 14-15
7. IONF-1047  (qa testing, 🔴 high)        → Testear Jul 14-15
```

### Prioridad 3 — Features del Sprint (NORMAL priority)
```
8. IONF-870   (qa testing, 🟠 normal)      → Testear Jul 15-16
9. IONF-1076  (post-CR, 🟠 normal)         → Testear si hay tiempo
10. IONF-1075 (post-CR, 🟠 normal)         → Testear si hay tiempo
```

---

## 👥 Carga por Developer y Bottlenecks

| Developer | Sprint Total | Regression | Completado | En pipeline | Bottleneck |
|-----------|-------------|------------|------------|-------------|------------|
| **Gustavo** | 4 | 3 | 1 ✅ | 2 CR (1128, 1114) + 1 CR (1075) | 🟠 3 tickets en CR simultáneo |
| **Enrique** | 3 | 2 | 0 | 1 QA (1007) + 1 CR (1127) + 1 blocked | 🟠 Divided attention |
| **Alex** | 6 | 3 | 2 ✅ | 1 intake (1043) + 3 sprint | 🟢 Regression casi listo |
| **Jhoel** | 3 | 1 | 0 | 1 fort (1141) + 2 sprint | 🔴 IONF-1141 en riesgo |
| **Jose Enrique** | 2 | 2 | 0 | 1 QA (1030) + 1 intake (1119) | 🟡 1 viable, 1 no |
| **Rodolfo** | 3 | 0 | 1 | 2 fort (infra) | 🟢 No tiene regression |
| **Yamil** | 5 | 0 | 0 | Todo en fort/CR/intake | 🟢 No tiene regression |
| **Sonia** | 3 | 0 | 0 | 1 fort + 2 intake | 🟢 No tiene regression |

> [!IMPORTANT]
> **Bottleneck principal: Gustavo** — tiene 3 tickets en Code Review (2 regression + 1 feature).
> Si estos CRs no se aprueban para el **Martes 14**, los tickets no llegarán a QA a tiempo.

---

## 📞 Guiones de Seguimiento — Para usar el Viernes 10 Jul

> Estos guiones son para que el QA Engineer envíe a cada dev con tickets en riesgo.
> El objetivo es obtener ETAs y detectar bloqueos antes de que sea tarde.

---

### Follow-up: Gustavo Mamani — Jul 10

**Contexto**: Tienes 3 tickets en Code Review para la v0.1.1. Necesitan aprobación de CR para el **Martes 14** para que QA alcance a testearlos.

#### IONF-1128 — Simple Decision compara strings (🔴 HIGH)
- Status: `code review`
- PRs: webcomponents-flow #7, flow_binaries #13
- **Pregunta**: "¿Ya tienes reviewers asignados para el PR #7 y #13? ¿Hay comentarios pendientes de resolver? ¿Estimación de cuándo se aprueba el CR?"
- **Deadline**: CR aprobado para **Martes 14 Jul**

#### IONF-1114 — Connections API Key duplicada (🔴 HIGH)
- Status: `code review`
- **Pregunta**: "¿En qué estado está el Code Review? ¿Hay feedback pendiente? Necesito tenerlo en QA para el Miércoles 15."
- **Deadline**: CR aprobado para **Martes 14 Jul**

#### IONF-1075 — Refactorizar registro compañía (🟠 NORMAL)
- Status: `code review`
- **Pregunta**: "Este es de prioridad normal pero si podemos incluirlo en la v0.1.1 sería ideal. ¿ETA del CR?"
- **Deadline**: CR aprobado para **Martes 14 Jul** (si da tiempo)

**Resumen para Gustavo:**

| Ticket | Necesita estar en... | Para fecha... |
|--------|---------------------|---------------|
| IONF-1128 | ✅ CR aprobado + deployed | Mar 14 Jul |
| IONF-1114 | ✅ CR aprobado + deployed | Mar 14 Jul |
| IONF-1075 | ✅ CR aprobado | Mar 14 Jul (best effort) |

---

### Follow-up: Enrique Vicente — Jul 10

**Contexto**: Tienes 1 ticket en QA y 1 en CR para la v0.1.1. Además, IONF-1056 está bloqueado.

#### IONF-1007 — Error UTC/Local Schedules (🔴 HIGH)
- Status: `qa in process`
- **Pregunta**: "Este ticket está en QA. ¿Ya está deployed en dev-app.ionflow.io? ¿Hay algo que deba saber antes de testear? ¿Instrucciones especiales?"
- **Deadline**: QA completado para **Jue 16 Jul**

#### IONF-1127 — Scheduler error status (🔴 HIGH)
- Status: `code review`
- **Pregunta**: "¿Quién tiene asignado el CR? ¿Hay feedback pendiente? Necesito este ticket en QA testing para el Miércoles 15."
- **Deadline**: CR aprobado para **Mar 14 Jul**

#### IONF-1056 — Monetización Stripe (🔴 HIGH, BLOCKED)
- Status: `blocked`
- **Pregunta**: "¿Qué está bloqueando este ticket? ¿Es algo que se pueda resolver en este sprint o lo movemos al siguiente?"
- **Info**: Solo para awareness, no crítico para v0.1.1

**Resumen para Enrique:**

| Ticket | Necesita estar en... | Para fecha... |
|--------|---------------------|---------------|
| IONF-1007 | ✅ QA completado | Jue 16 Jul |
| IONF-1127 | ✅ CR aprobado + deployed | Mar 14 Jul |
| IONF-1056 | Info: ¿se desbloquea? | — |

---

### Follow-up: Jhoel Legua — Jul 10

**Contexto**: IONF-1141 es un regression fix que está en riesgo de no llegar a la v0.1.1.

#### IONF-1141 — App Connectors nodos minados (🟠 NORMAL)
- Status: `fortification`
- **Pregunta**: "¿Cómo va el desarrollo? ¿Qué % de avance estimas? Para que entre en la v0.1.1 necesito que esté en CR para el **Lunes 13** a más tardar. ¿Es viable?"
- **Deadline**: Dev completado para **Vie 10 Jul**, CR para **Lun 13 Jul**
- **Si no es viable**: "No pasa nada, lo mantenemos en la v0.1.1 para el próximo sprint."

#### IONF-1098 — Confirmación cobro scraping (🔴 HIGH)
- Status: `qa testing`
- **Pregunta**: "¿Ya está deployed? ¿Hay instrucciones especiales para el testing?"
- **Deadline**: QA completado para **Jue 16 Jul**

**Resumen para Jhoel:**

| Ticket | Necesita estar en... | Para fecha... |
|--------|---------------------|---------------|
| IONF-1141 | ✅ Dev completo → CR | Vie 10 → Lun 13 Jul |
| IONF-1098 | ✅ QA completado | Jue 16 Jul |

---

### Follow-up: Jose Enrique Ricaldi — Jul 10

**Contexto**: IONF-1030 está en QA, IONF-1119 no ha iniciado.

#### IONF-1030 — Mejoras interface dualtrack (🟠 NORMAL)
- Status: `qa in process`
- **Pregunta**: "¿Está deployed? ¿Hay algún cambio reciente que deba considerar en el testing?"
- **Deadline**: QA completado para **Jue 16 Jul**

#### IONF-1119 — PDF Templates error 500 imagen (🟠 NORMAL)
- Status: `sprint intake`
- **Pregunta**: "¿Tienes planeado iniciar el desarrollo de este ticket en este sprint? Si no, lo mantendremos para el siguiente sprint dentro de la v0.1.1."
- **Info**: Baja probabilidad de completar en este sprint

**Resumen para Jose Enrique:**

| Ticket | Necesita estar en... | Para fecha... |
|--------|---------------------|---------------|
| IONF-1030 | ✅ QA completado | Jue 16 Jul |
| IONF-1119 | Info: ¿inicia en este sprint? | — |

---

### Follow-up: Alex Chura — Jul 10

**Contexto**: Alex ya tiene 2 tickets aprobados ✅. IONF-1043 está sin iniciar.

#### IONF-1043 — Auto-mapper PDF Template (🟠 NORMAL)
- Status: `sprint intake`
- **Pregunta**: "¿Tienes planeado trabajar en este ticket? Si no arranca hoy, no alcanzará para la v0.1.1 de este sprint. ¿Lo dejamos para el siguiente?"
- **Deadline**: Si inicia hoy → dev Vie 10, CR Lun-Mar 13-14, QA Mié-Jue 15-16

#### IONF-1047 — Gateway ZID instalar APP (🔴 HIGH)
- Status: `qa testing`
- **Pregunta**: "¿Está deployed y listo para testing?"
- **Deadline**: QA completado para **Jue 16 Jul**

**Resumen para Alex:**

| Ticket | Necesita estar en... | Para fecha... |
|--------|---------------------|---------------|
| IONF-1043 | Info: ¿inicia hoy? | Dev cutoff: Vie 10 |
| IONF-1047 | ✅ QA completado | Jue 16 Jul |

---

## Versión v0.1.1 — Projection

### Si todo sale según el plan:

| Tipo | En v0.1.1 | Pendientes (→ next sprint) |
|------|-----------|---------------------------|
| Regression fixes | 8 de 11 | 3 (IONF-1141, 1119, 1043) |
| Features | ~5-7 de 15 | Resto |
| **Total tickets aprobados** | **~13-15** | **~16-18** |

### Regression fixes incluidos en v0.1.1:
1. ✅ IONF-1121 — Boards false alert
2. ✅ IONF-1126 — PDF Templates unsaved changes
3. ✅ IONF-1116 — PDF Templates file size
4. 🟢 IONF-1007 — UTC/Local schedules
5. 🟢 IONF-1030 — Interface improvements
6. 🟡 IONF-1128 — Simple Decision strings
7. 🟡 IONF-1127 — Scheduler error status
8. 🟡 IONF-1114 — Connections API Key
