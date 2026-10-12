# Deployment Runbook — Testing de un Ticket

> **Cuándo seguir este runbook**: Cuando el QA Engineer dice "testear ticket <ID>",
> "testing del ticket <ID>", o el ticket ya pasó Discovery y está listo para testing.

---

## Cómo Usar Este Runbook

1. **Seguir los pasos EN ORDEN** — No saltarse pasos ni ejecutarlos en paralelo
2. **Cada GATE es bloqueante** — Si un gate falla, PARAR y resolver antes de avanzar
3. **Anunciar cada paso** — Antes de ejecutar un skill, usar el protocolo Announce → Confirm → Act (Regla #5 del SKILL.md)
4. **Registrar progreso** — Marcar cada □ como ✅ conforme se completa

---

## DEPLOYMENT RUNBOOK — Ticket <ID>

```
════════════════════════════════════════════════════════════════
PASO 1 — INICIALIZACIÓN Y VERIFICACIÓN DE ARTEFACTOS
════════════════════════════════════════════════════════════════
```

### Checklist

- □ Cargar `knowledge/L1-project/` completo:
  - `business-rules.md` — Reglas de negocio
  - `test-priorities.md` — Prioridades
  - `api-architecture.md` — Repos, endpoints
  - `stack-overview.md` — Stack técnico

- □ Cargar `knowledge/L2-modules/<módulo>/module.md` del módulo afectado
  - Leer sección **"Impacto Cruzado"** si existe
  - Leer sección **"Database"** — schema para queries de BD

- □ Cargar `knowledge/L3-tickets/<id>/` del ticket

- □ **Verificar que los artefactos de Discovery existen:**

  | Artefacto | ¿Existe? | Acción si no existe |
  |-----------|----------|---------------------|
  | `test-matrix.md` | ✅/❌ | **PARAR** → Ejecutar Discovery primero |
  | `test-matrix.csv` | ✅/❌ | **PARAR** → Ejecutar Discovery primero |
  | `ac-consolidated.md` | ✅/❌ | **PARAR** → Ejecutar Discovery primero |
  | `test-plan.md` | ✅/❌ | **PARAR** → Ejecutar Discovery primero |
  | `risk-triage.md` | ✅/❌ | Continuar, pero notar la ausencia |

  > Si alguno de los 4 obligatorios no existe → **PARAR y ejecutar Discovery primero**.
  > Seguir `skills/discovery-runbook.md` antes de continuar.

- □ **Re-leer comentarios recientes del ticket en ClickUp** (getTaskById):
  - ¿Hubo cambios **después del Discovery**?
  - ¿Los AC siguen vigentes?
  - ¿Hubo acuerdos nuevos entre Developer y PO?
  - Si hay divergencia → **actualizar artefactos antes de continuar**:
    - Reconciliar AC (como en Discovery Paso 2)
    - Actualizar test-matrix si los AC cambiaron

- □ Verificar entorno de testing:
  - URL del staging → leer `.env` de este repo (`IONFLOW_ENVIRONMENT_URL`)
  - Branch `DEVELOPMENT` actualizada en los repos afectados
  - Credenciales disponibles (Company y/o Admin)

### Gate 1

```
GATE 1: ¿Discovery completo + AC vigentes + entorno listo?
  → SÍ: Continuar al Paso 2
  → NO (faltan artefactos): Ejecutar Discovery primero (skills/discovery-runbook.md)
  → NO (AC desactualizados): Reconciliar AC y actualizar test-matrix
```

---

```
════════════════════════════════════════════════════════════════
PASO 2 — CODE REVIEW QA / BUG HUNTING (obligatorio)
════════════════════════════════════════════════════════════════
```

> ⚠️ **Este paso es OBLIGATORIO en Deployment.**
> El objetivo es encontrar **BUGS** en el código antes de testear.
> No es un review de calidad de código — es una búsqueda activa de defectos.

### Anuncio

```
🔄 SIGUIENTE SKILL: code-review/review (modo Deployment / Bug Hunting)
   Razón: Necesito revisar el código del ticket para encontrar bugs antes del testing.
   Prerequisitos:
     ✅ L1 + L2 cargados
     ✅ L3 del ticket cargado
     ✅ Repos de desarrollo accesibles en ../
   Output esperado: L3-tickets/<id>/code-review-qa.md + TCs inyectados en test-matrix

¿Procedo?
```

### Checklist

- □ Ejecutar skill: `code-review/review` (modo Deployment / Bug Hunting)

- □ **Actualizar repos antes de revisar:**
  ```bash
  # OBLIGATORIO: actualizar la rama DEVELOPMENT antes de leer código
  cd ../gateway-ion && git fetch origin && git checkout DEVELOPMENT && git pull origin DEVELOPMENT
  cd ../flow_binaries && git fetch origin && git checkout DEVELOPMENT && git pull origin DEVELOPMENT
  cd ../gateway && git fetch origin && git checkout DEVELOPMENT && git pull origin DEVELOPMENT
  cd ../webcomponents-flow && git fetch origin && git checkout DEVELOPMENT && git pull origin DEVELOPMENT
  ```
  > ❌ NUNCA hacer git push, commit, ni merge — Solo operaciones de LECTURA

- □ Revisar cambios del ticket en cada repo afectado:
  ```bash
  # Opción A: buscar commits por mensaje del ticket
  cd ../<repo> && git log --oneline DEVELOPMENT -30 | grep -i "<ticket-id>"

  # Opción B: buscar por autor del developer
  cd ../<repo> && git log --oneline DEVELOPMENT --author="<developer>" -15

  # Opción C: ver diff de branch del ticket
  cd ../<repo> && git branch -r | grep -i "<ticket-id>"
  git diff DEVELOPMENT..<branch> --stat
  git diff DEVELOPMENT..<branch>
  ```

- □ **Bug Hunting activo** — Buscar defectos usando el checklist del skill:
  - Backend: multi-tenant, validaciones, SQL injection, manejo de errores
  - Frontend: XSS, estados no manejados, validaciones, rutas sin guard
  - Consultar sección "Impacto Cruzado" del L2

- □ Verificar que existe: `L3-tickets/<id>/code-review-qa.md`

- □ Bugs encontrados → documentados con evidencia (formato BUG-CR-NNN)
  > ⚠️ **Todo bug del Bug Hunting DEBE ser REPRODUCIBLE.**
  > No reportar bugs que no se puedan reproducir paso a paso.
  > Cada bug debe incluir:
  >   - Pasos de reproducción exactos (formato breadcrumb)
  >   - Resultado esperado vs comportamiento actual
  >   - Evidencia del código (fragmento con línea)
  >   - Si es un hallazgo de código estático (no reproducible en UI) → clasificar como
  >     RIESGO A VERIFICAR, no como BUG CONFIRMADO

- □ **INYECTAR hallazgos en la test-matrix:**
  - Cada bug/riesgo del code review → nuevo TC en `test-matrix.md` y `.csv`
  - Marcar origen: **"Code Review"** en la columna Tipo
  - Formato de ID: `TC-CR-001`, `TC-CR-002`, etc.
  - Pasos en formato breadcrumb: `Company Login > Sidebar: [Módulo] > ...`
  - Actualizar el resumen de la test-matrix con los TCs nuevos
  - Ejemplo:

    ```
    | TC-CR-001 | Auth | N/A | Code Review | Verificar filtrado multi-tenant en endpoint /api/v1/resources |
    | Pasos: Company Login > Navigate: /resources > Button: "Create" > Fill "Name": "Test" > Button: "Save" > Verify BD: company_id presente |
    | El registro en BD tiene company_id del usuario. Otros tenants NO ven el recurso | 🔴 | No | ⬜ Pendiente |
    ```

- □ QA Engineer revisa hallazgos y bugs del código

### Gate 2

```
GATE 2: ¿code-review-qa.md existe + bugs inyectados en test-matrix + QA aprobó?
  → SÍ: Continuar al Paso 3
  → NO (bugs críticos que bloquean testing): Reportar al Developer antes de continuar
  → NO (falta revisión): Completar el code review
```

---

```
════════════════════════════════════════════════════════════════
PASO 3 — EJECUCIÓN DE TESTING (obligatorio)
════════════════════════════════════════════════════════════════
```

### Decisión de Modo de Ejecución

Preguntar al QA Engineer:

```
❓ ¿Cómo deseas ejecutar el testing?

   A) Testing Manual — Tú navegas la app, yo guío y documento
   B) Testing Asistido con Playwright MCP — Yo navego el browser, tú supervisas
```

### Anuncio

```
🔄 SIGUIENTE SKILL: sprint-testing/test
   Razón: Ejecutar el testing del ticket según la test-matrix.
   Modo: [Manual / Asistido con Playwright MCP]
   Prerequisitos:
     ✅ test-matrix.md cargada (incluyendo TCs del code review)
     ✅ test-plan.md cargado
     ✅ code-review-qa.md cargado (bugs a tener en cuenta)
     ✅ L2 del módulo cargado (selectores, rutas, schema BD)
     ✅ Entorno verificado (URL, credenciales)
   Output esperado: Resultados de cada TC + bugs documentados + sugerencia de veredicto

¿Procedo?
```

### Checklist

- □ Ejecutar skill: `sprint-testing/test`

- □ **Si Playwright MCP (Canal 1)** → seguir protocolo reforzado:
  1. Leer `.env` para credenciales
  2. Preguntar rol: Company o Admin
  3. Browser VISIBLE — QA supervisa en tiempo real
  4. Login via Keycloak (#username, #password, #kc-login)
  5. Para cada TC: **ANUNCIAR → ESPERAR → NAVEGAR → EJECUTAR → CAPTURAR → REPORTAR**
  6. Screenshots → `L3-tickets/<id>/screenshots/TC-[ID]-paso-[N].png`
  7. **NUNCA** marcar PASS/FAIL sin confirmación del QA Engineer
  8. **Si un TC FALLA → screenshot OBLIGATORIO como evidencia:**
     - Capturar screenshot inmediatamente al detectar el fallo
     - Guardar como: `L3-tickets/<id>/screenshots/FAIL-TC-[ID].png`
     - Este screenshot se incluye en el reporte final (qa-report.md)
     - Este screenshot se referencia en el comentario del ticket (approval/rejection)
     - **Los screenshots de fallos son EVIDENCIA PERMANENTE del reporte**

- □ Ejecutar todos los bloques en orden:
  - **Bloque 0** — Verificar que code-review-qa.md existe (gate pre-requisito)
  - **Bloque 1** — Smoke Tests
  - **Bloque 2** — Happy Path
  - **Bloque 3** — Edge Cases
  - **Bloque 4** — Negativos
  - **Bloque 5** — Regresión
  - **Bloque 6** — DB Evidence

- □ **Para el Bloque 6 — DB Evidence (REGLA CRÍTICA):**

  > ⚠️ Las queries DEBEN construirse **EXCLUSIVAMENTE** a partir de los schemas
  > definidos en los archivos de migración de los repos fuente.

  - Fuentes de schema:
    - `../flow_binaries/migrations/*.sql` → Schema core Go + SQLite
    - `../gateway/database/migrations/*.php` → Schema legacy PostgreSQL
    - `knowledge/L2-modules/<módulo>/module.md` → Sección "Database"
  
  - ❌ **NUNCA inventar** nombres de campos, tablas ni relaciones
  - ❌ **NUNCA asumir** que existe una columna sin verificar en las migraciones
  - ❌ **NUNCA generar** queries con JOINs basados en relaciones supuestas
  - ✅ **SIEMPRE leer** las migraciones del repo ANTES de generar una query
  - ✅ **SIEMPRE verificar** nombres exactos de tablas y columnas
  - ✅ **SIEMPRE incluir** referencia a la migración fuente como comentario:

    ```sql
    -- Fuente: ../gateway/database/migrations/2024_10_30_create_flows_table.php
    -- Tabla: flows | Columnas verificadas: id, name, company_id, status
    SELECT id, name, company_id, status 
    FROM flows 
    WHERE company_id = '<company_id>' AND name = '<nombre>';
    ```

- □ Los TCs del code review (TC-CR-xxx) se ejecutan como parte normal del testing

- □ Bugs documentados inline durante ejecución (formato BUG-NNN)

- □ Screenshots/evidencia capturada

- □ Sugerencia de veredicto generada al final:
  ```
  SUGERENCIA DE VEREDICTO:
    Total TCs: [N] (incluyendo [N] del code review)
    ✅ PASS: [N]
    ❌ FAIL: [N]
    ⚠️ PARCIAL: [N]
    ⏭️ SALTADOS: [N]
    
    Bugs encontrados en testing: [N]
    Bugs encontrados en code review: [N]
    
    Sugerencia: [✅ Approved / ❌ Rejected / ⚠️ Approved con observaciones]
    Razón: [explicación]
  ```

### Gate 3

```
GATE 3: ¿Ejecución completa + sugerencia de veredicto generada?
  → SÍ: Continuar al Paso 4
  → NO: Completar los bloques pendientes
```

---

```
════════════════════════════════════════════════════════════════
PASO 4 — VEREDICTO DEL QA ENGINEER (obligatorio)
════════════════════════════════════════════════════════════════
```

> El QA Engineer siempre tiene la última palabra. La sugerencia de la IA es solo eso: una sugerencia.

### Checklist

- □ Presentar resumen de resultados y sugerencia de veredicto al QA Engineer

- □ El QA Engineer da su veredicto:

  | Veredicto | Significado | Siguiente paso |
  |-----------|-------------|----------------|
  | ✅ **Approved** | El ticket pasa QA sin observaciones | Paso 5 → Reporte de aprobación |
  | ⚠️ **Approved con observaciones** | Pasa QA pero con notas/observaciones menores | Paso 5 → Reporte con observaciones |
  | ❌ **Rejected** | El ticket NO pasa QA — hay bugs críticos | Paso 5 → Reporte de rechazo |

- □ Veredicto registrado en L3 del ticket

### Gate 4

```
GATE 4: ¿Veredicto explícito del QA Engineer recibido?
  → SÍ: Continuar al Paso 5 (OBLIGATORIO)
  → NO: Esperar veredicto del QA Engineer

⚠️ LA SESIÓN NO TERMINA AQUÍ. EL REPORTE FINAL ES OBLIGATORIO.
```

---

```
════════════════════════════════════════════════════════════════
PASO 5 — REPORTE FINAL (obligatorio, NO SALTABLE)
════════════════════════════════════════════════════════════════
```

> ⚠️ **NUNCA detenerse sin ejecutar este paso.**
> Este paso es OBLIGATORIO independientemente del veredicto.

### Anuncio

```
🔄 SIGUIENTE SKILL OBLIGATORIO: sprint-testing/report
   Razón: El QA Engineer dio su veredicto. El reporte final es OBLIGATORIO.
   Prerequisitos:
     ✅ Ejecución de testing completada
     ✅ Veredicto del QA Engineer recibido: [✅/❌/⚠️]
     ✅ Bugs del code review documentados (code-review-qa.md)
     ✅ Bugs del testing documentados
   Output esperado:
     - L3-tickets/<id>/qa-report.md
     - Comentario del ticket (approval.md o rejection.md)
     - test-matrix.md y .csv actualizados con resultados

¿Procedo con el reporte final?
```

### Checklist

- □ Ejecutar skill: `sprint-testing/report`

- □ Verificar que existe: `L3-tickets/<id>/qa-report.md`
  - El reporte debe incluir:
    - Resumen ejecutivo
    - Resultados por TC (incluyendo TCs del code review: TC-CR-xxx)
    - Bugs del code review (BUG-CR-xxx) consolidados
    - Bugs del testing (BUG-xxx) consolidados
    - Veredicto del QA Engineer
    - Evidencia (screenshots, queries BD)

- □ Comentario para ticket preparado usando template:
  - Si ✅ Approved → usar `templates/approval.md`
  - Si ❌ Rejected → usar `templates/rejection.md`
  - Si ⚠️ Approved con obs → usar `templates/approval.md` con sección de observaciones

- □ `test-matrix.md` actualizada con resultados finales de cada TC:
  - Columna Estado actualizada: ✅ PASS / ❌ FAIL / ⚠️ PARCIAL / ⏭️ SALTADO

- □ `test-matrix.csv` actualizada con los mismos resultados

- □ Bugs del code review + bugs del testing consolidados en el reporte

- □ **Evidencia de screenshots** (si Playwright MCP fue usado):
  - Screenshots de fallos (`FAIL-TC-*.png`) referenciados en el reporte
  - Screenshots de pasos relevantes como evidencia visual
  - Los screenshots persisten en `L3-tickets/<id>/screenshots/` como evidencia permanente
  - En el comentario del ticket, referenciar los screenshots de fallos

### Gate 5

```
GATE 5: ¿qa-report.md existe + artefactos actualizados + comentario preparado?
  → SÍ: Continuar al Paso 6
  → NO: Completar el reporte
```

---

```
════════════════════════════════════════════════════════════════
PASO 6 — CIERRE (obligatorio)
════════════════════════════════════════════════════════════════
```

### Checklist

- □ Sugerir actualización de L2 si hubo hallazgos relevantes:
  - ¿Se descubrieron edge cases nuevos? → Agregar a "Edge Cases Conocidos" del L2
  - ¿Se descubrieron archivos centinela? → Agregar a "Impacto Cruzado" del L2
  - ¿Se descubrieron queries útiles? → Agregar a "Queries de verificación frecuentes" del L2

- □ Si el ticket fue **rechazado** (❌):
  - Preparar iteración N+1 de la test-matrix
  - Documentar qué TCs fallaron y qué se espera que cambie
  - Marcar los TCs que necesitan re-testing

- □ Sugerir plan de automatización si hay TCs automatizables:
  ```
  ❓ ¿Deseas ejecutar automation/plan para identificar TCs automatizables?
     TCs candidatos para E2E: [lista de TCs de UI gateway-ion que pasaron]
     Si sí → la automatización se delega a ionflow-playwright-creator en bot-test
  ```
  > La automatización E2E se maneja en el repo bot-test,
  > no en este repo. Ver `skills/automation/plan.md` y `skills/automation/code.md`.

### Gate 6

```
GATE 6: ¿Cierre completo?
  → SÍ: DEPLOYMENT COMPLETO ✅
  → NO: Completar los items pendientes
```

---

```
════════════════════════════════════════════════════════════════
✅ DEPLOYMENT COMPLETO
════════════════════════════════════════════════════════════════
```

### Artefactos Finales

Verificar que todos existen en `L3-tickets/<id>/`:

| Artefacto | Estado | Obligatorio |
|-----------|--------|-------------|
| `code-review-qa.md` | ✅ | Sí (Deployment siempre) |
| `qa-report.md` | ✅ | Sí |
| `test-matrix.md` (actualizada con resultados + TCs de code review) | ✅ | Sí |
| `test-matrix.csv` (actualizada con resultados) | ✅ | Sí |
| Comentario del ticket (approval/rejection) | ✅ | Sí |
| `screenshots/` (si Playwright MCP fue usado) | ⬜/✅ | Solo si Canal 1 |

### Resumen de Sesión

```
DEPLOYMENT COMPLETO — [TICKET-ID]

Discovery:  ✅ Completado previamente
Code Review: ✅ [N] bugs encontrados, [N] TCs inyectados en test-matrix
Testing:    ✅ [N] TCs ejecutados (✅ [N] PASS, ❌ [N] FAIL, ⚠️ [N] PARCIAL)
Veredicto:  [✅/❌/⚠️] — Dado por el QA Engineer
Reporte:    ✅ qa-report.md generado
Comentario: ✅ Preparado con template [approval/rejection]
```

---

## Referencia Rápida — Repos de Desarrollo

> Los repos están en `../` (UN NIVEL ARRIBA de este repositorio).

| Repo | Path | Stack | Cuándo leer |
|------|------|-------|-------------|
| Frontend | `../gateway-ion/` | Vue 3 + TS | Code review, UI testing, selectores |
| Backend core | `../flow_binaries/` | Go | Code review, API testing, lógica |
| Canvas | `../webcomponents-flow/` | Vue 3 + TS | Code review canvas, componentes |
| Legacy/Auth | `../gateway/` | PHP 8.2 | Auth, permisos, migraciones BD |
| E2E Tests | `../bot-test/` | Playwright NX | Delegación a ionflow-playwright-creator |

### Protocolo de Branches (OBLIGATORIO antes de leer código)

```bash
# SIEMPRE actualizar antes de leer
cd ../<repo> && git fetch origin && git checkout DEVELOPMENT && git pull origin DEVELOPMENT
```

❌ NUNCA hacer git push, commit, ni merge en repos de desarrollo
❌ NUNCA modificar archivos en repos de desarrollo
✅ Solo operaciones de LECTURA (checkout, pull, diff, log, cat)

---

## Referencia Rápida — BD y Queries

| BD | Motor | Repo de migraciones | Acceso |
|---|---|---|---|
| Principal | PostgreSQL | `../gateway/database/migrations/*.php` | SSH tunnel (DBeaver) |
| Ejecuciones | SQLite | `../flow_binaries/migrations/*.sql` | API de historial / UI |

> ⚠️ Las queries se construyen EXCLUSIVAMENTE desde los schemas de las migraciones.
> NUNCA inventar campos, tablas ni relaciones.
