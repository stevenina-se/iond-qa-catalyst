# Skill: sprint-testing/test

> Guía al QA Engineer a través de una sesión de testing completa para un ticket. Soporta dos modos de ejecución: manual (el QA navega la app) y asistido (la IA navega con Playwright MCP bajo supervisión del QA).

## Modos de Ejecución

### Opción A: Manual (por defecto)

```
┌─────────────────────────────────┐     ┌──────────────────────────────┐
│        QA CATALYST (IA)         │     │       QA ENGINEER (Humano)   │
├─────────────────────────────────┤     ├──────────────────────────────┤
│ ✅ Guía paso a paso por el plan │     │ ✅ Interactúa con la app     │
│ ✅ Genera queries de BD         │     │ ✅ Ejecuta queries en DBeaver │
│ ✅ Documenta cada resultado     │     │ ✅ Captura screenshots/video  │
│ ✅ Registra bugs encontrados    │     │ ✅ Reporta lo que observa     │
│ ✅ Sugiere veredicto            │     │ ✅ Decide el veredicto final  │
│ ❌ NO abre el browser           │     │                              │
│ ❌ NO hace clicks en la UI      │     │                              │
│ ❌ NO ejecuta queries directo   │     │                              │
└─────────────────────────────────┘     └──────────────────────────────┘
```

### Opción B: Asistido con Playwright MCP

Requiere que `@playwright/mcp` esté configurado. El QA Engineer elige este modo al inicio.

```
┌─────────────────────────────────┐     ┌──────────────────────────────┐
│        QA CATALYST (IA)         │     │       QA ENGINEER (Humano)   │
├─────────────────────────────────┤     ├──────────────────────────────┤
│ ✅ Navega el browser (MCP)      │     │ ✅ Supervisa la sesión       │
│ ✅ Ejecuta clicks y formularios │     │ ✅ Verifica visualmente      │
│ ✅ Captura screenshots automát. │     │ ✅ Confirma pass/fail        │
│ ✅ Documenta cada resultado     │     │ ✅ Puede interrumpir         │
│ ✅ Genera queries de BD         │     │ ✅ Ejecuta queries en DBeaver │
│ ✅ Registra bugs encontrados    │     │ ✅ Decide el veredicto final  │
└─────────────────────────────────┘     └──────────────────────────────┘
```

**Reglas de Opción B:**
1. El browser se abre **visible** (no headless) — el QA Engineer ve todo
2. La IA **anuncia cada acción** antes de ejecutarla: "Voy a hacer click en [X]"
3. Si un TC falla → la IA **para y reporta** — el QA Engineer verifica manualmente
4. Screenshots automáticos → `L3-tickets/<id>/screenshots/`
5. El QA Engineer puede decir "para" en cualquier momento
6. La IA **NUNCA** marca un TC como FAIL sin confirmación del QA Engineer

### Protocolo Reforzado — Playwright MCP (Canal 1)

> Cuando el QA Engineer elige Opción B, se DEBEN seguir estas instrucciones
> para testing de UI de gateway-ion.

#### Pre-requisitos del Canal 1
1. Leer `.env` de este repo para obtener credenciales:
   - `IONFLOW_ENVIRONMENT_URL`
   - `IONFLOW_KC_DOMAIN`
   - Credenciales según rol (Company o Admin)
2. Preguntar al QA Engineer: "¿Qué rol usar? Company o Admin"
3. El browser DEBE estar visible — el QA Engineer supervisa en tiempo real

#### Protocolo de Login
1. Navegar a `IONFLOW_ENVIRONMENT_URL`
2. El sistema redirige automáticamente a Keycloak (`IONFLOW_KC_DOMAIN`)
3. Llenar formulario de login (`#username`, `#password`, `#kc-login`)
4. Esperar redirect a la app
5. Confirmar al QA Engineer: "Login exitoso como [rol]. ¿Continúo?"

#### Protocolo de Ejecución de TCs
Para cada TC del test-plan que involucra UI de gateway-ion:

1. **ANUNCIAR**: "Voy a ejecutar TC-[ID]: [descripción]. Navegaré a [ruta]."
2. **ESPERAR**: Confirmación del QA Engineer
3. **NAVEGAR**: Ir a la ruta correspondiente
4. **EJECUTAR**: Cada paso del TC, anunciando antes de hacer click/llenar
5. **CAPTURAR**: Screenshot después de cada acción relevante
   → Guardar en `L3-tickets/<id>/screenshots/TC-[ID]-paso-[N].png`
6. **REPORTAR**: Resultado del TC al QA Engineer
7. **NUNCA** marcar PASS o FAIL sin confirmación del QA Engineer

#### Protocolo de Bugs / Fallos en Canal 1
Si durante la ejecución se detecta un comportamiento inesperado:
1. **PARAR** la ejecución del TC actual
2. **Capturar screenshot** del bug inmediatamente
   → Guardar como: `L3-tickets/<id>/screenshots/FAIL-TC-[ID].png`
3. **Reportar** al QA Engineer: "Encontré un comportamiento inesperado en TC-[ID]..."
4. El QA Engineer decide: ¿Es bug? ¿Continuar? ¿Investigar más?
5. Si es bug → documentar inmediatamente con formato BUG-[NNN]
6. **Los screenshots de fallos son EVIDENCIA PERMANENTE del reporte**

#### REGLA OBLIGATORIA — Sincronización de Test Matrix en tiempo real

> ⚠️ **CRÍTICO**: Cuando el Catalyst ejecuta TCs con Playwright MCP (Opción B),
> la columna `Estado` de `test-matrix.md` DEBE actualizarse **inmediatamente
> después de cada TC ejecutado** — no al final de la sesión.

1. **Después de cada TC**: Actualizar la fila correspondiente en `test-matrix.md`
   - `⬜ Pendiente` → `✅ PASS` o `❌ FAIL — BUG-XXX`
2. **Nunca** acumular resultados para actualizar al final de la sesión
3. **Nunca** dejar TCs marcados como PASS sin haber verificado el flujo completo
4. Si un TC cubre un flujo E2E (ej: registro → dashboard → settings), el TC
   **NO es PASS** hasta que se verifique la última vista de la cadena

#### REGLA OBLIGATORIA — Verificación Post-Acción

> ⚠️ **CRÍTICO**: Un toast de éxito o un redirect al dashboard NO es suficiente
> para marcar un TC como PASS. Se DEBE verificar el estado completo post-acción.

Para cualquier TC que involucre creación, actualización o eliminación de datos:
1. **Verificar persistencia**: Navegar a la vista que muestra los datos (ej: /profile, /settings)
2. **Verificar permisos**: Navegar a TODAS las vistas principales (Settings, Users, Teams, Accounts) con el usuario que realizó la acción
3. **Verificar consistencia**: Los datos mostrados en la vista de verificación coinciden con los ingresados
4. **Si el TC crea un usuario/company nuevos**: Los TCs de regresión DEBEN re-ejecutarse con ese usuario nuevo, no solo con usuarios existentes

**Ejemplo de lo que NUNCA debe pasar:**
```
❌ INCORRECTO: TC-001 (registro company) → Toast "Success" → Dashboard carga → "PASS"
✅ CORRECTO:   TC-001 (registro company) → Toast "Success" → Dashboard carga 
               → Navigate /settings → Verificar acceso → Navigate /profile 
               → Verificar datos → RECIÉN ENTONCES → "PASS"
```


#### Selectores para Navegación
> Consultar L2 del módulo para selectores específicos.

| Elemento | Selector recomendado |
|----------|---------------------|
| Sidebar items | `role="menuitem"` con name del módulo |
| Botones PrimeVue | `role="button"` con name del texto |
| Inputs | `label` del campo o `placeholder` |
| Tablas PrimeVue | `tr[data-pc-section='bodyrow']` |
| Dialogs | `role="dialog"` |
| Toast/Notificaciones | `.p-toast-message` |

## Cuándo usar este skill

- **Deployment Track**: Cuando el ticket está listo para testing y el plan fue aprobado
- **Support Lane**: Para validar hotfixes con scope reducido

## Pre-requisitos

Antes de ejecutar este skill, el agente DEBE haber cargado:
- ✅ `knowledge/L1-project/` (completo)
- ✅ `knowledge/L2-modules/<módulo>/module.md`
- ✅ `L3-tickets/<ticket-id>/test-plan.md` (del skill `sprint-testing/plan`)
- ✅ `L3-tickets/<ticket-id>/test-matrix.md` (del skill `test-docs/document`)

**Si no existe el test-plan o test-matrix**: STOP — ejecutar los skills correspondientes primero.

### En caso de Re-test (iteración > 1)

Si el ticket fue **previamente rechazado**, el agente DEBE cargar adicionalmente:
- ✅ `L3-tickets/<ticket-id>/qa-report-v1.md` (reporte de la iteración anterior)
- ✅ `L3-tickets/<ticket-id>/test-matrix-v1.md` (matrix con resultados anteriores)
- ✅ Los bugs documentados en la iteración anterior

Esto permite al Catalyst:
1. **Saber POR QUÉ se rechazó** el ticket en la iteración anterior
2. **Priorizar los re-tests de bugs** corregidos por el Developer
3. **Verificar que los fixes no rompieron** lo que ya funcionaba (regresión post-fix)
4. **Comparar resultados** entre iteraciones para detectar regresiones

> El Catalyst debe reportar al QA Engineer: "Este ticket está en su iteración N. En la iteración anterior se rechazó por [resumen de bugs]. Los puntos a re-verificar son: [lista]."

---

## Instrucciones de Ejecución

### Stage 1 — PLANNING

Reporta al QA Engineer:
1. El ticket que vas a guiar en testing
2. El plan de testing que vas a seguir (resumen de bloques)
3. Los datos de prueba necesarios (del test-plan)
4. Confirmar el entorno de testing

**Información de entorno a confirmar:**

| Campo | Valor |
|-------|-------|
| URL del entorno | dev-app.ionflow.io |
| Branch desplegada | `DEVELOPMENT` (batch de tickets del sprint) |
| Branch del ticket | `<ticket-id>` (para trazabilidad, ya mergeada en DEVELOPMENT) |
| Browser | Chrome (principal) |
| Usuario de prueba | [confirmar con QA Engineer] |
| Company de prueba | [confirmar con QA Engineer] |

> **Nota**: Los tickets se testean en batch sobre la rama DEVELOPMENT, no en ramas individuales. Pero se registra la branch de cada ticket para trazabilidad del reporte.

**Espera aprobación antes de continuar.**

### Stage 2 — EXECUTION

> ⚠️ El QA Engineer puede interrumpir, redirigir o modificar la ejecución en CUALQUIER momento.

El Catalyst guía al QA Engineer bloque por bloque. Para cada test case:
1. Catalyst presenta el caso (pasos, precondiciones, qué verificar)
2. QA Engineer ejecuta en la app y reporta lo que observa
3. Catalyst registra el resultado y la evidencia
4. Si hay fallo → Catalyst documenta el bug inmediatamente

---

#### BLOQUE 0 — CODE REVIEW QA (Pre-requisito)

> ⚠️ El code review fue extraído como skill independiente: `code-review/review.md`
> En Deployment, se DEBE haber ejecutado `code-review/review` ANTES de llegar aquí.
> En Discovery, el code review es opcional.

**GATE**:

```
¿Existe L3-tickets/<id>/code-review-qa.md?
  → SÍ: Continuar con Bloque 1.
    → Considerar los bugs y riesgos del code review durante la ejecución.
    → Los TCs del code review (TC-CR-xxx) se ejecutan como parte normal del testing.
  → NO (y estamos en Deployment): PARAR → Ejecutar code-review/review primero.
  → NO (y estamos en Discovery/Support): Continuar sin code review.
```

---

#### BLOQUE 1 — SMOKE TESTS

> Verificación rápida de que el feature existe y es accesible. Si alguno falla → STOP → escalar al QA Engineer.

Para cada smoke test:

```
SMOKE-[N]:
  Caso: [descripción]
  Pasos: [lo que hiciste]
  Resultado: ✅ PASS / ❌ FAIL
  Evidencia: [screenshot / observación]
  Tiempo: [duración]
```

**Regla de Smoke**: Si ALGÚN smoke test falla:
1. Registrar el fallo con evidencia
2. Reportar inmediatamente al QA Engineer
3. NO continuar con los siguientes bloques
4. El QA Engineer decide: escalar al Developer o continuar con los tests que se puedan

---

#### BLOQUE 2 — HAPPY PATH (UI Testing)

> Verificar el flujo principal de cada Acceptance Criteria.

Para cada test case de happy path:

```
TC-[ID] — Happy Path:
  AC vinculado: [AC-N]
  Precondición: [estado necesario antes de empezar]
  
  Paso 1: [acción] → Resultado: [lo que pasó] ✅/❌
  Paso 2: [acción] → Resultado: [lo que pasó] ✅/❌
  Paso 3: [acción] → Resultado: [lo que pasó] ✅/❌
  
  Resultado final: ✅ PASS / ❌ FAIL
  Evidencia: [screenshot / video / observación]
  Notas: [cualquier comportamiento inesperado aunque el test pase]
```

**Si un happy path falla:**
1. Registrar con evidencia detallada (pasos, expected vs actual)
2. Continuar con los demás happy paths
3. Al finalizar el bloque, reportar los fallos al QA Engineer

---

#### BLOQUE 3 — EDGE CASES

> Verificar comportamiento en los bordes identificados en Discovery.

Para cada edge case:

```
TC-[ID] — Edge Case:
  Escenario: [descripción del caso borde]
  
  Paso 1: [acción] → Resultado: [lo que pasó] ✅/❌
  ...
  
  Resultado: ✅ PASS / ❌ FAIL / ⚠️ PARCIAL
  Severidad si falla: 🔴/🟠/🟡
  Notas: [observación]
```

---

#### BLOQUE 4 — NEGATIVOS

> Verificar que el sistema NO permite acciones inválidas.

Para cada caso negativo:

```
TC-[ID] — Negativo:
  Intento: [qué se intentó hacer que NO debería funcionar]
  
  Resultado esperado: [error / validación / bloqueo]
  Resultado real: [lo que pasó]
  
  Resultado: ✅ PASS (el sistema bloqueó correctamente) / ❌ FAIL (el sistema permitió algo inválido)
```

**Regla**: Un negativo que falla (el sistema permitió algo que no debería) es 🔴 Crítico.

---

#### BLOQUE 5 — REGRESIÓN

> Verificar que el feature no rompió funcionalidad existente.

Para cada caso de regresión:

```
REG-[ID] — Regresión:
  Módulo verificado: [nombre]
  Caso: [qué se verificó que sigue funcionando]
  
  Resultado: ✅ PASS / ❌ FAIL
  Notas: [observación]
```

---

#### BLOQUE 6 — DB EVIDENCE

> Generar queries de verificación y registrar los resultados.
> Fuente del schema: archivos de migración de los repos + L2 del módulo.

> ⚠️ **REGLA CRÍTICA DE DB EVIDENCE:**
> Las queries DEBEN construirse **EXCLUSIVAMENTE** a partir de los schemas
> definidos en los archivos de migración de los repos fuente:
>
>   - `../flow_binaries/migrations/*.sql` → Schema core Go + SQLite
>   - `../gateway/database/migrations/*.php` → Schema legacy PostgreSQL
>   - `knowledge/L2-modules/<módulo>/module.md` → Sección "Database"
>
> ❌ **NUNCA** inventar nombres de campos, tablas ni relaciones
> ❌ **NUNCA** asumir que existe una columna sin verificar en las migraciones
> ❌ **NUNCA** generar queries con JOINs basados en relaciones supuestas
> ✅ **SIEMPRE** leer las migraciones del repo ANTES de generar una query
> ✅ **SIEMPRE** verificar nombres exactos de tablas y columnas
> ✅ **SIEMPRE** incluir referencia a la migración fuente como comentario SQL
> ✅ Si el L2 no tiene sección Database completa → leer las migraciones directamente

Para cada verificación de BD:

```
DB-[ID]:
  Query:
    -- Fuente: ../gateway/database/migrations/<archivo>.php
    -- Tabla: <tabla> | Columnas verificadas: <lista>
    [SQL generado por el Catalyst]
  BD: PostgreSQL / SQLite (ejecuciones)
  Propósito: [qué se verifica]
  
  ⏸ QA Engineer ejecuta en DBeaver y pega el resultado
  
  Resultado pegado:
  [resultado de DBeaver]
  
  Verificación: ✅ MATCH / ❌ MISMATCH
  Análisis: [interpretación del resultado]
```

**Proceso de DB Evidence:**
1. Catalyst **lee las migraciones** del repo para verificar el schema
2. Genera la query con referencia a la migración fuente como comentario
3. Presenta la query al QA Engineer
4. QA Engineer la ejecuta en DBeaver (conexión SSH existente)
5. Pega el resultado en la sesión
6. Catalyst analiza y registra como evidencia

---

### Stage 3 — REPORTING

#### Paso 1: Resumen de ejecución

Genera un resumen inmediato para el QA Engineer:

```
RESUMEN DE EJECUCIÓN — [TICKET-ID]

| Bloque | Total | ✅ Pass | ❌ Fail | ⚠️ Parcial | ⏭️ Saltado |
|--------|-------|---------|---------|------------|-----------|
| Smoke | | | | | |
| Happy Path | | | | | |
| Edge Cases | | | | | |
| Negativos | | | | | |
| Regresión | | | | | |
| DB Evidence | | | | | |
| **TOTAL** | | | | | |

Bugs encontrados: [N]
Tiempo total: [duración]
```

#### Paso 2: Registrar bugs

Por cada fallo encontrado, generar un bug en formato del equipo:

```
BUG-[NNN]:
  Severidad: 🔴 Urgent / 🟡 High / 🔵 Normal / ⚪ Low
  Estado: Nuevo
  Módulo: [nombre]
  TC relacionado: TC-[ID]
  
  Descripción: [descripción clara y corta]
  
  Pasos de reproducción:
  1. ...
  2. ...
  
  Resultado esperado: [qué debería pasar]
  Comportamiento actual: [qué pasa realmente]
  
  Evidencia: [screenshot / video / log]
```

#### Paso 3: Sugerir veredicto

Basado en los criterios del test-plan, sugiere el veredicto:

```
SUGERENCIA DE VEREDICTO:

Basado en los criterios definidos en el test-plan:
  - Smoke tests: [N/N] ✅
  - Happy path: [N/N] ✅
  - Edge cases: [N/N] ✅ (umbral: 80%)
  - Negativos: [N/N] ✅
  - Regresión: [N/N] ✅
  - DB Evidence: [N/N] ✅

SUGERENCIA: ✅ Approved / ❌ Rejected / ⚠️ Approved con observaciones

⚠️ ESTA ES SOLO UNA SUGERENCIA. EL QA ENGINEER TOMA LA DECISIÓN FINAL.
```

#### Paso 4: Actualizar L3

Guarda todo el registro de la sesión en `L3-tickets/<ticket-id>/`:
- Actualizar `test-matrix.md` con los estados de cada TC
- Actualizar `test-matrix.csv` con los resultados
- Crear `db-evidence.md` con todas las queries y resultados
- Actualizar el `ticket-memory.md` con el transcript

#### Paso 5: Trigger del Reporte Final (OBLIGATORIO)

> ⚠️ **LA SESIÓN NO TERMINA AQUÍ.**

Después de que el QA Engineer confirme su veredicto:

```
🔄 SIGUIENTE SKILL OBLIGATORIO: sprint-testing/report
   Razón: El QA Engineer dio su veredicto. El reporte final es OBLIGATORIO.
   Prerequisitos:
     ✅ Ejecución de testing completada
     ✅ Veredicto del QA Engineer recibido: [✅/❌/⚠️]
     ✅ Bugs del code review documentados (code-review-qa.md)
     ✅ Bugs del testing documentados
   Output esperado: L3-tickets/<id>/qa-report.md + comentario del ticket

¿Procedo con el reporte final?
```

**NUNCA detenerse sin ejecutar este paso.**

---

## Reglas de este Skill

1. **SIEMPRE seguir el orden del test-plan** — No saltarse bloques sin aprobación
2. **Si un smoke falla → STOP** — Escalar inmediatamente
3. **Registrar CADA paso** — Nada puede quedar sin documentar
4. **DB Evidence requiere intervención humana** — El QA Engineer ejecuta las queries
5. **DB queries basadas en migraciones** — NUNCA inventar campos, tablas ni relaciones
6. **El veredicto es SUGERENCIA** — El QA Engineer decide siempre
7. **Si se descubre algo no contemplado en el plan** — Reportar y preguntar si investigar
8. **Bugs se registran inmediatamente** — No esperar al final para documentar fallos
9. **Screenshots/videos son obligatorios** para cualquier fallo
10. **Screenshots de fallos en Playwright MCP son evidencia permanente** — Persisten en L3
11. **El reporte final es OBLIGATORIO** — Nunca terminar sin ejecutar sprint-testing/report
12. **TCs del code review (TC-CR-xxx)** se ejecutan como parte normal del testing
