# Skill: code-review/review

> Revisión de código desde perspectiva QA. Dos modos de ejecución:
> **Discovery** (opcional, exploratorio) y **Deployment** (obligatorio, Bug Hunting activo).

## Cuándo usar este skill

- **Discovery Track**: Solo si el QA Engineer acepta cuando se le pregunta (Paso 3.5 del Discovery Runbook)
- **Deployment Track**: SIEMPRE antes del testing funcional (Paso 2 del Deployment Runbook)

## Modos de Ejecución

### Modo Discovery (Opcional)

```
┌─────────────────────────────────────────────────────────────┐
│  MODO DISCOVERY — Exploratorio                               │
├─────────────────────────────────────────────────────────────┤
│  Activación:  SOLO si el QA Engineer acepta                  │
│  Enfoque:     Explorar prototipo para enriquecer análisis    │
│  Busca:       "Señales" para la discusión con el Developer   │
│  NO busca:    Bugs formales                                  │
│  Tono:        Preguntas abiertas, NO objeciones              │
│  Output:      Enriquece risk-triage.md + opcional review.md  │
└─────────────────────────────────────────────────────────────┘
```

### Modo Deployment / Bug Hunting (Obligatorio)

```
┌─────────────────────────────────────────────────────────────┐
│  MODO DEPLOYMENT — Bug Hunting Activo                        │
├─────────────────────────────────────────────────────────────┤
│  Activación:  SIEMPRE antes del testing funcional            │
│  Enfoque:     Encontrar BUGS reales en el código             │
│  Busca:       Defectos, vulnerabilidades, errores lógicos    │
│  Requisito:   Todo bug DEBE ser REPRODUCIBLE                 │
│  Output:      code-review-qa.md + TCs inyectados en matrix   │
└─────────────────────────────────────────────────────────────┘
```

---

## Navegación de Repositorios (CRÍTICO)

> **Los repos de desarrollo están en `../` (UN NIVEL ARRIBA de este repositorio).**
> Ver Regla #7 del SKILL.md para referencia completa.

### Antes de Revisar — Actualizar Repos (OBLIGATORIO)

```bash
# OBLIGATORIO: actualizar antes de revisar
cd ../gateway-ion && git fetch origin && git checkout DEVELOPMENT && git pull origin DEVELOPMENT
cd ../flow_binaries && git fetch origin && git checkout DEVELOPMENT && git pull origin DEVELOPMENT
cd ../gateway && git fetch origin && git checkout DEVELOPMENT && git pull origin DEVELOPMENT
cd ../webcomponents-flow && git fetch origin && git checkout DEVELOPMENT && git pull origin DEVELOPMENT
```

### Identificar Cambios del Ticket

```bash
# Opción A: buscar commits por mensaje del ticket
cd ../<repo> && git log --oneline DEVELOPMENT -30 | grep -i "<ticket-id>"

# Opción B: buscar por autor del developer
cd ../<repo> && git log --oneline DEVELOPMENT --author="<developer>" -15

# Opción C: ver diff de branch del ticket (si existe)
cd ../<repo> && git branch -r | grep -i "<ticket-id>"
git diff DEVELOPMENT..<branch> --stat
git diff DEVELOPMENT..<branch>
```

### Repos Disponibles

| Repo | Path | Stack | Qué buscar |
|------|------|-------|------------|
| Frontend | `../gateway-ion/` | Vue 3 + TS | Vistas, componentes, stores, rutas, validaciones UI |
| Backend core | `../flow_binaries/` | Go | Endpoints, handlers, migraciones, lógica de negocio |
| Canvas | `../webcomponents-flow/` | Vue 3 + TS | Componentes de nodos, drawer, edges |
| Legacy/Auth | `../gateway/` | PHP 8.2 | Auth, permisos, migraciones BD, routes |

### Restricciones

❌ NUNCA hacer git push, commit, ni merge en repos de desarrollo
❌ NUNCA modificar archivos en repos de desarrollo
✅ Solo operaciones de LECTURA (checkout, pull, diff, log, cat)

---

## Pre-requisitos

- ✅ `knowledge/L1-project/` cargado
- ✅ `knowledge/L2-modules/<módulo>/module.md` cargado (incluyendo sección Impacto Cruzado)
- ✅ Ticket ID para buscar commits en los repos
- ✅ Repos actualizados (git pull ejecutado)
- ✅ En Deployment: `test-matrix.md` y `test-matrix.csv` existentes (para inyectar TCs)

---

## Instrucciones — Modo Discovery (Opcional)

### Stage 1 — PLANNING

1. Preguntar al QA Engineer:
   ```
   ❓ ¿Hay una branch del ticket disponible para revisar el código del prototipo?
      ¿Deseas que haga una revisión de código para enriquecer el análisis?
      
      A) Sí, revisar código del prototipo
      B) No, continuar sin code review
   ```

2. Si la respuesta es **NO** → No ejecutar este skill, continuar con el flujo de Discovery
3. Si la respuesta es **SÍ** → Reportar qué repos vas a revisar

**Espera aprobación antes de continuar.**

### Stage 2 — EXECUTION

#### Paso 1: Obtener los cambios del ticket

Para cada repo afectado, obtener el diff (ver sección "Identificar Cambios del Ticket").

#### Paso 2: Exploración del prototipo (NO bugs formales)

Leer los cambios y buscar **"señales" para la discusión** con el Developer:

| Qué buscar | Cómo formularlo |
|---|---|
| Endpoints nuevos sin validación visible | "¿Se validará el campo X en el endpoint Y?" |
| Migraciones que cambian schema | "¿Esta migración es reversible? ¿Impacta datos existentes?" |
| Componentes sin manejo de estados vacíos | "¿Qué muestra la UI cuando no hay datos?" |
| Queries sin filtrado multi-tenant | "¿Este query filtrará por company_id en producción?" |
| Lógica que podría afectar otros módulos | "¿Este cambio en X podría afectar al módulo Y?" (consultar Impacto Cruzado del L2) |
| Hardcoded values | "¿Este valor estará en config/env o permanecerá hardcoded?" |

> **FORMULAR COMO PREGUNTAS, NO COMO OBJECIONES.**
> El objetivo es enriquecer la discusión, no crear fricción.

### Stage 3 — REPORTING

Enriquecer `risk-triage.md` con las observaciones del código.

Si se encontraron señales relevantes, opcionalmente documentar en `L3-tickets/<id>/code-review-qa.md`:

```markdown
# Code Review QA — [TICKET-ID] (Modo Discovery)

## Resumen
- Repos revisados: [lista]
- Archivos analizados: [N]
- Señales encontradas: [N]

## Observaciones para Discusión con Developer
1. [Señal 1]: "¿[pregunta]?" — Archivo: [ruta], línea [N]
2. [Señal 2]: "¿[pregunta]?" — Archivo: [ruta], línea [N]

## Enriquecimiento del Risk-Triage
- Estas observaciones se incorporaron al risk-triage.md
```

---

## Instrucciones — Modo Deployment / Bug Hunting (Obligatorio)

### Stage 1 — PLANNING

Reportar al QA Engineer:

```
🔄 SIGUIENTE SKILL: code-review/review (modo Deployment / Bug Hunting)
   Razón: Necesito revisar el código del ticket para encontrar bugs antes del testing.
   Prerequisitos:
     ✅ L1 + L2 cargados
     ✅ L3 del ticket cargado
     ✅ test-matrix.md existente (para inyectar TCs del code review)
     ✅ Repos de desarrollo accesibles en ../
   Repos a revisar: [lista]
   Branch/commits identificados: [info]
   Módulo principal: [módulo]
   Módulos de impacto cruzado: [lista]
   Output esperado: L3-tickets/<id>/code-review-qa.md + TCs inyectados en test-matrix

¿Procedo?
```

**Espera aprobación antes de continuar.**

### Stage 2 — EXECUTION

#### Paso 1: Obtener el Diff del Ticket

Para cada repo afectado, obtener los cambios (ver sección "Identificar Cambios del Ticket").

Documentar qué se encontró:

```
ARCHIVOS MODIFICADOS — [TICKET-ID]

[REPO: gateway-ion]
  - src/views/<módulo>/<archivo>.vue  (+N/-N líneas)
  - src/stores/<archivo>.ts           (+N/-N líneas)
  - src/router/tenant.ts              (+N/-N líneas)

[REPO: flow_binaries]
  - api/handlers/<archivo>.go         (+N/-N líneas)
  - migrations/<fecha>_<nombre>.sql   (+N/-N líneas)

[REPO: gateway]
  - routes/<archivo>.php              (+N/-N líneas)
```

#### Paso 2: Bug Hunting — Búsqueda Activa de Defectos

> ⚠️ La IA DEBE buscar activamente **BUGS**, no solo señales para testing.
> Cada hallazgo se clasifica como **BUG CONFIRMADO** o **RIESGO A VERIFICAR**.
> **Todo bug DEBE ser REPRODUCIBLE** — si no se puede reproducir, es un RIESGO.

##### Checklist de Bug Hunting — BACKEND (flow_binaries / gateway)

| Qué buscar | Cómo detectarlo | Severidad |
|---|---|---|
| **Filtrado multi-tenant faltante** | Query sin `WHERE company_id = ?` o `WHERE tenant_id = ?` | 🔴 Crítico |
| **Validación de input faltante** | Endpoint que no valida campos required/formato | 🔴 Crítico |
| **SQL injection potencial** | Queries con concatenación de strings en lugar de parámetros | 🔴 Crítico |
| **Endpoint sin autenticación** | Ruta pública que debería requerir auth | 🔴 Crítico |
| **Manejo de error ausente** | Función sin try/catch, handler sin error response | 🟠 Alto |
| **Race condition potencial** | Operaciones concurrentes sin locks/transacciones | 🟠 Alto |
| **Hardcoded values** | URLs, IDs, configuraciones que deberían ser dinámicas | 🟡 Medio |
| **Migración no reversible** | ALTER TABLE sin DOWN migration | 🟡 Medio |
| **Logs sensibles** | Passwords, tokens, PII en logs | 🟠 Alto |

##### Checklist de Bug Hunting — FRONTEND (gateway-ion)

| Qué buscar | Cómo detectarlo | Severidad |
|---|---|---|
| **XSS potencial** | `v-html` con datos de usuario sin sanitizar | 🔴 Crítico |
| **Ruta sin guard de permisos** | Route sin middleware de autenticación | 🔴 Crítico |
| **Estado no manejado** | Componente sin loading/error/empty state | 🟠 Alto |
| **Validación de formulario faltante** | Input sin reglas de validación | 🟠 Alto |
| **Manejo de error en llamadas API** | Service call sin `.catch` o try/catch | 🟠 Alto |
| **Memory leak potencial** | Watchers/listeners sin cleanup en `onUnmounted` | 🟡 Medio |
| **Accesibilidad** | Botones sin label, inputs sin aria, contraste insuficiente | 🟡 Medio |

##### Checklist de Bug Hunting — CANVAS (webcomponents-flow)

| Qué buscar | Cómo detectarlo | Severidad |
|---|---|---|
| **Evento sin cleanup** | `addEventListener` sin `removeEventListener` en destroy | 🟠 Alto |
| **Prop reactivity rota** | Cambio de prop que no re-renderiza el componente | 🟠 Alto |
| **Z-index conflictos** | Drawers/dialogs/overlays que se superponen | 🟡 Medio |

#### Paso 3: Análisis de Impacto Cruzado

1. Leer la sección **"Impacto Cruzado"** del L2 del módulo principal
2. Verificar si los cambios del ticket tocan archivos/tablas/endpoints de otros módulos
3. Si tocan otro módulo → cargar su L2 y verificar consistencia
4. Revisar la tabla de **"Archivos Centinela"** del L2

Documentar:

| Módulo Impactado | Componente Afectado | Riesgo | Verificación Necesaria |
|---|---|---|---|
| [módulo] | [tabla/endpoint/componente] | 🔴/🟠/🟡 | [qué verificar en testing] |

#### Paso 4: Documentar Bugs y Riesgos

Para cada hallazgo, usar este formato:

```
BUG-CR-[NNN]:
  Clasificación: BUG CONFIRMADO / RIESGO A VERIFICAR
  Severidad: 🔴 Crítico / 🟠 Alto / 🟡 Medio
  Repo: [gateway-ion / flow_binaries / gateway / webcomponents-flow]
  Archivo: [ruta del archivo]
  Línea: [número de línea o rango]
  
  Descripción: [qué encontré]
  
  Evidencia: 
    [fragmento de código relevante con líneas]
  
  Reproducibilidad:
    SI es BUG CONFIRMADO (reproducible):
      Pasos de reproducción:
        1. Company Login > Sidebar: [Módulo] > ...
        2. [Acción que dispara el bug]
        3. ...
      Resultado esperado: [qué debería pasar]
      Comportamiento actual: [qué pasa realmente]
    
    SI es RIESGO A VERIFICAR (hallazgo de código estático):
      Escenario para verificar:
        1. [Escenario que podría disparar el problema]
        2. [Condiciones necesarias]
      Por qué es riesgo: [explicación]
  
  Impacto potencial: [qué puede pasar si no se corrige]
  Módulos afectados: [lista de módulos, consultando Impacto Cruzado del L2]
  
  Recomendación:
    - Si BUG CONFIRMADO → Reportar al Developer antes de continuar testing
    - Si RIESGO A VERIFICAR → Inyectar como TC en la test-matrix
```

#### Paso 5: Inyectar Hallazgos en la Test Matrix (OBLIGATORIO)

> ⚠️ Los hallazgos del code review NO quedan solo en code-review-qa.md.
> Cada bug/riesgo que requiere verificación se AGREGA como TC nuevo en la test-matrix.

Para cada hallazgo que requiere verificación en testing:

1. **Agregar un nuevo TC** a `test-matrix.md` y `test-matrix.csv` con:
   - **ID**: `TC-CR-001`, `TC-CR-002`, etc. (prefijo CR = Code Review)
   - **Tipo**: `Code Review` (nueva categoría que identifica el origen)
   - **Caso de Test**: Descripción del escenario a verificar
   - **Pasos**: Ruta de navegación explícita en formato breadcrumb
   - **Resultado Esperado**: Comportamiento correcto vs el bug encontrado
   - **Prioridad**: Heredada de la severidad del hallazgo

2. **Actualizar el resumen de la test-matrix**:
   - Agregar línea: `Code Review: [N]` al conteo de tipos
   - Actualizar total de casos

Ejemplo de TC inyectado:

```
| TC-CR-001 | Auth | N/A | Code Review | Verificar filtrado multi-tenant en endpoint /api/v1/resources |
  Company Login > Navigate: /resources > Button: "Create" > Fill "Name": "Test Resource" > Button: "Save" > 
  Verify BD: SELECT company_id FROM resources WHERE name = 'Test Resource' |
  El registro tiene company_id del usuario logueado. Otros tenants NO ven el recurso | 🔴 | No | ⬜ Pendiente |
```

### Stage 3 — REPORTING

Guardar en `L3-tickets/<id>/code-review-qa.md`:

```markdown
# Code Review QA — [TICKET-ID] (Modo Deployment / Bug Hunting)

## Resumen
- Repos revisados: [lista]
- Archivos modificados analizados: [N]
- Bugs confirmados (reproducibles): [N] (🔴: N, 🟠: N, 🟡: N)
- Riesgos a verificar en testing: [N]
- Módulos con impacto cruzado: [lista]
- TCs inyectados en test-matrix: [N] (TC-CR-001 a TC-CR-NNN)

## Archivos Modificados
[tabla de archivos por repo con líneas cambiadas]

## Bugs Confirmados (Reproducibles)
[lista de BUG-CR-NNN con clasificación BUG CONFIRMADO]
[Cada uno incluye pasos de reproducción en formato breadcrumb]

## Riesgos a Verificar
[lista de BUG-CR-NNN con clasificación RIESGO A VERIFICAR]
[Cada uno incluye escenario para verificar]

## Impacto Cruzado
[tabla de módulos impactados]

## TCs Inyectados en Test Matrix
| TC ID | Origen | Caso de Test | Severidad |
|-------|--------|-------------|-----------|
| TC-CR-001 | BUG-CR-001 | [descripción] | 🔴 |
| TC-CR-002 | BUG-CR-003 | [descripción] | 🟠 |
```

> Los bugs del code review se INCLUYEN en el reporte final (`sprint-testing/report`).
> Los TCs del code review se EJECUTAN como parte normal del testing en `sprint-testing/test`.
> Los screenshots de fallos de TCs del code review persisten como evidencia permanente.

---

## Reglas de este Skill

1. **Todo bug DEBE ser reproducible** — Si no se puede reproducir paso a paso, es un RIESGO A VERIFICAR, no un BUG CONFIRMADO
2. **Los pasos de reproducción usan formato breadcrumb** — `Company Login > Sidebar: Boards > ...`
3. **Actualizar repos ANTES de leer código** — Nunca revisar código desactualizado
4. **Solo operaciones de LECTURA** — Nunca modificar código de los repos de desarrollo
5. **Consultar Impacto Cruzado del L2** — Siempre verificar qué módulos pueden verse afectados
6. **Los hallazgos se inyectan en la test-matrix** — No quedan solo en el code-review-qa.md
7. **Queries de BD basadas en migraciones** — Nunca inventar campos, tablas ni relaciones
8. **En Discovery: preguntas, no objeciones** — El tono es colaborativo
9. **En Deployment: búsqueda activa de defectos** — El tono es riguroso
10. **El QA Engineer decide** — La IA sugiere, el QA Engineer aprueba
