# Template de Rechazo — [TICKET-ID]

Estimado @name_dev

**El resultado de pruebas para este ticket es: RECHAZADO ❌**

**Ticket**: [TICKET-ID] — [Título]
**Módulo**: [módulo]
**QA Engineer**: [nombre]
**Fecha**: [fecha]

### Resumen de Testing
- Casos ejecutados: [N] (incluyendo [N] del Code Review)
- Casos aprobados: [N]
- Casos fallidos: [N]
- Bugs encontrados en Code Review: [N]
- Bugs encontrados en Testing: [N]
- Bugs totales (bloqueantes): [N]

### Code Review QA
> Resumen de la revisión de código realizada antes del testing funcional.

- Repos revisados: [lista]
- Hallazgos: [N] (🔴: [N], 🟠: [N], 🟡: [N])
- TCs inyectados en la test matrix desde el code review: [N]
- Bugs del código que contribuyen al rechazo: [lista de BUG-CR-xxx si aplica]

---

### 📌 Observaciones

**🔴 OBS-01 - Urgent - Estado: Nuevo / Persistente / Regresión**
**Área / Flujo: {{modulo}}**

**Descripción:**
Descripción clara y corta del problema (qué falla).

**Pasos de reproducción:**
> Los pasos deben ser reproducibles y en formato breadcrumb.

1. Company Login > Sidebar: [Módulo] > ...
2. ...
3. ...

**Resultado esperado:**
Qué debería ocurrir.

**Comportamiento actual:**
Qué ocurre actualmente.

**Evidencia:**
- Screenshot(s): {{link_imagen o ruta a L3-tickets/<id>/screenshots/FAIL-TC-xxx.png}}
- Logs / Payload (si aplica)

---

**🟡 OBS-02 - High - Estado: Nuevo / Persistente**
**Área / Flujo: {{modulo}}**

**Descripción:**
Descripción clara y corta del problema (qué falla).

**Pasos de reproducción:**
1. Company Login > Sidebar: [Módulo] > ...
2. ...
3. ...

**Resultado esperado:**
Qué debería ocurrir.

**Comportamiento actual:**
Qué ocurre actualmente.

**Evidencia:**
- Screenshot(s): {{link_imagen o ruta a L3-tickets/<id>/screenshots/FAIL-TC-xxx.png}}
- Logs / Payload (si aplica)

---

**🔵 OBS-03 - Normal - Estado: Nuevo**
**Área / Flujo: {{modulo}}**

**Descripción:**
Descripción clara y corta del problema (qué falla).

**Pasos de reproducción:**
1. Company Login > Sidebar: [Módulo] > ...
2. ...
3. ...

**Resultado esperado:**
Qué debería ocurrir.

**Comportamiento actual:**
Qué ocurre actualmente.

**Evidencia:**
- Screenshot(s): {{link_imagen o ruta a L3-tickets/<id>/screenshots/FAIL-TC-xxx.png}}
- Logs / Payload (si aplica)

---

**⚪ OBS-04 - Low - Estado: Nuevo**
**Área / Flujo: {{modulo}}**

**Descripción:**
Descripción clara y corta del problema (qué falla).

**Pasos de reproducción:**
1. Company Login > Sidebar: [Módulo] > ...
2. ...
3. ...

**Resultado esperado:**
Qué debería ocurrir.

**Comportamiento actual:**
Qué ocurre actualmente.

**Evidencia:**
- Screenshot(s): {{link_imagen o ruta a L3-tickets/<id>/screenshots/FAIL-TC-xxx.png}}
- Logs / Payload (si aplica)

---

### Evidencia General
- Test Matrix: [link o referencia]
- QA Report: [link o referencia]
- Code Review QA: [link o referencia]
- DB Evidence: [link o referencia]
- Screenshots de fallos: [link a L3-tickets/<id>/screenshots/]

| Details | |
|---|---|
| BROWSER | Chrome |
| BRANCH | {{branch}} |
| ENV | dev-app.ionflow.io |
| TEST MATRIX | {{link_documento}} |
| CODE REVIEW | ✅ Realizado |
| MERGE REQUEST | PENDIENTE (bugs encontrados) |