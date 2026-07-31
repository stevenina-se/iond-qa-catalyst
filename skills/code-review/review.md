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
> Cada hallazgo se clasifica en 4 categorías: **BUG** / **RISK** / **SEC** / **EDGE**.
> **Todo bug DEBE ser REPRODUCIBLE** — si no se puede reproducir, es un RIESGO.
>
> El análisis tiene **2 niveles**:
> - **Nivel 1 (Genérico)**: Checklists de seguridad y calidad estándar
> - **Nivel 2 (Negocio)**: Heurísticas de lógica de dominio, específicas al tipo de feature

##### Checklist de Bug Hunting — BACKEND Nivel 1: Genérico (flow_binaries / gateway)

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

##### Checklist de Bug Hunting — BACKEND Nivel 2: Lógica de Negocio (Profundo)

> ⚠️ **Este nivel es OBLIGATORIO.** Los bugs más graves suelen estar en la lógica de dominio,
> no en las vulnerabilidades genéricas. El Nivel 1 detecta el 20% de los bugs reales;
> el Nivel 2 detecta el 80% restante.

| Qué buscar | Cómo detectarlo | Severidad |
|---|---|---|
| **Asimetría CRUD en guards/validación** | La operación A tiene guard/validación/registro pero su operación inversa B no. Buscar: create vs delete, upgrade vs downgrade, enable vs disable — una dirección valida/registra y la otra no | 🔴 Crítico |
| **Divergencia cross-repo para el mismo flujo** | La misma lógica implementada en dos repos/stacks se comporta distinto para el mismo input. Buscar funciones con el mismo propósito en Go vs PHP y comparar edge cases | 🔴 Crítico |
| **Registro de uso sin enforcement** | Se registra una métrica/consumo pero ningún guard/middleware consulta ese dato → la métrica se mide pero nunca se aplica, el recurso es ilimitado en la práctica | 🟠 Alto |
| **Enforcement sin registro** | Un guard/middleware bloquea basándose en un contador que ningún servicio incrementa → el guard nunca dispara porque el contador nunca avanza | 🟠 Alto |
| **Deduplicación anclada a timestamp incorrecto** | Lógica de "enviar solo una vez" que usa un timestamp que solo cambia bajo condiciones raras (no en cada ciclo/ventana) → se ejecuta una sola vez para siempre en vez de una vez por ciclo | 🟠 Alto |
| **Medición wall-clock vs active-time** | Tiempo de uso calculado como (cierre - apertura) sin descontar tiempo idle/inactivo → sesiones ociosas se facturan como activas | 🟠 Alto |
| **Cambio de estado que no revoca permisos/recursos del estado anterior** | Al transicionar de estado A a estado B, los permisos/recursos exclusivos de A sobreviven porque la limpieza solo itera lo que B define, no lo que A tenía | 🔴 Crítico |
| **Aprovisionamiento lazy incompleto** | Primera llamada a un entity sin datos previos falla (`nil`/`null`) en vez de inicializar automáticamente como hace otro componente del sistema para el mismo entity | 🟠 Alto |
| **Seeder/fixture que pisa datos configurados por admin** | `updateOrCreate` (o equivalente) con campos mutables en el payload de actualización → re-ejecutar destruye configuraciones manuales del admin | 🟠 Alto |
| **Seeder/fixture match por campo no único** | Lookup por `name` u otro campo sin constraint unique; puede pisar registros homónimos o vincular al registro equivocado | 🟡 Medio |
| **Tests unitarios que dependen de estado artificial** | Test que muta manualmente un campo que ningún código productivo muta → el test pasa pero la feature no funciona en producción con datos reales | 🟠 Alto |
| **Registro huérfano por guard post-insert** | Se inserta fila (ej: status `pending`) antes de la validación/guard; al rechazar no se limpia la fila → se acumulan registros huérfanos | 🟠 Alto |
| **Early return que descarta acumulador** | Loop/iteración con múltiples `return` donde algunos paths no persisten el acumulador (totales, contadores, logs) → los casos más costosos/fallidos quedan sin medir | 🟠 Alto |
| **Columna generada/computed sin fallback** | Lógica que depende de una columna `generated`/`virtual` de la BD sin fallback en código → si la columna falta o difiere, fail-open silencioso | 🔴 Crítico |
| **API que acepta valores inválidos sin validar contra enum** | PUT/POST acepta campos de tipo enum (status, type, visibility, role) como texto libre sin validación → un typo puede causar comportamiento inesperado en cascada | 🔴 Crítico |
| **Endpoint read-only bloqueado por guard de recursos** | Endpoint GET de datos que ya existen o ya fueron generados que pasa por un guard de consumo → el usuario pierde acceso a sus propios datos al agotar un recurso | 🟡 Medio |
| **Edición de configuración sin re-sync a dependientes** | Cambiar la configuración de un recurso padre no propaga a los hijos/suscriptores existentes → registros del mismo tipo divergen en sus valores | 🟡 Medio |

##### Checklist de Bug Hunting — FRONTEND Nivel 1: Genérico (gateway-ion)

| Qué buscar | Cómo detectarlo | Severidad |
|---|---|---|
| **XSS potencial** | `v-html` con datos de usuario sin sanitizar | 🔴 Crítico |
| **Ruta sin guard de permisos** | Route sin middleware de autenticación | 🔴 Crítico |
| **Estado no manejado** | Componente sin loading/error/empty state | 🟠 Alto |
| **Validación de formulario faltante** | Input sin reglas de validación | 🟠 Alto |
| **Manejo de error en llamadas API** | Service call sin `.catch` o try/catch | 🟠 Alto |
| **Memory leak potencial** | Watchers/listeners sin cleanup en `onUnmounted` | 🟡 Medio |
| **Accesibilidad** | Botones sin label, inputs sin aria, contraste insuficiente | 🟡 Medio |

##### Checklist de Bug Hunting — FRONTEND Nivel 2: Business Display (Profundo)

> ⚠️ **Este nivel busca errores en cómo la UI muestra datos de negocio al usuario.**
> Los bugs de "display de negocio" son invisibles en checklists genéricos pero causan
> confusión, datos incorrectos y decisiones erróneas del usuario final.

| Qué buscar | Cómo detectarlo | Severidad |
|---|---|---|
| **Formato numérico/moneda hardcodeado** | División cruda sin `Intl.NumberFormat` ni `toFixed()`; símbolo de moneda hardcodeado; formatos que no respetan locale | 🟡 Medio |
| **Placeholder i18n sin parámetro** | Key de traducción con `{variable}` pero el caller no pasa el parámetro → se renderiza literal o con artefactos visuales | 🟡 Medio |
| **Errores silenciados con catch vacío** | `catch(() => null)` o `catch(() => {})` que convierte un error de red en estado vacío falso — el usuario ve "No data" cuando el servidor está caído | 🟠 Alto |
| **Mensaje de error crudo del HTTP client** | `error.message` renderizado directamente → el toast muestra el mensaje técnico del framework en vez de un mensaje amigable | 🟠 Alto |
| **5xx body mostrado al usuario** | Error handler con condición `status >= 400` que incluye 500-599 → body interno (puede contener detalles de BD o stack traces) mostrado literal | 🟠 Alto |
| **Falsy check en valor numérico válido** | `if (value)` donde `value=0` es un valor legítimo pero se trata como falsy → muestra guion/vacío en lugar del valor real | 🟡 Medio |
| **Estado computed que oculta datos reales** | Computed property evaluada como `false` cuando el objeto fuente es `null` → muestra un estado incorrecto (ej: "Active" cuando no hay datos) | 🟠 Alto |
| **Datos de snapshot vs datos live** | UI que itera un snapshot guardado en vez de consultar el endpoint actualizado → datos reales se ocultan si el snapshot está desactualizado | 🟠 Alto |
| **CSS-only disabled sin lógica en template** | Botón con clase CSS de disabled pero sin `:disabled` real ni `@click.prevent` → el clic ejecuta la acción aunque visualmente parece deshabilitado | 🟡 Medio |
| **Dirty state no limpiado al cerrar diálogo** | Diálogo que edita directamente el objeto reactivo del store; cerrar sin guardar no revierte cambios → al reabrir muestra valores fantasma | 🟡 Medio |
| **Keys no inyectivas en v-for** | `:key` basado en campo que puede repetirse → Vue reutiliza DOM incorrecto, render duplicado o datos cruzados | 🟡 Medio |
| **Fechas parseadas como hora local** | `new Date(utcString)` sin parse UTC explícito → desfase de ±1 día en zonas horarias negativas; estados temporales se adelantan/atrasan | 🟡 Medio |
| **Permisos creados pero no adjuntados a roles** | Slugs de permisos en el seeder/migración sin attach a ningún rol → la ruta FE exige el permiso pero ningún usuario lo tiene → 403 para todos | 🔴 Crítico |
| **CTA contradictorio con los requirements** | Elemento de UI visible que contradice los AC documentados del ticket — verificar contra el AC original | 🟡 Medio |

##### Checklist de Bug Hunting — CANVAS (webcomponents-flow)

| Qué buscar | Cómo detectarlo | Severidad |
|---|---|---|
| **Evento sin cleanup** | `addEventListener` sin `removeEventListener` en destroy | 🟠 Alto |
| **Prop reactivity rota** | Cambio de prop que no re-renderiza el componente | 🟠 Alto |
| **Z-index conflictos** | Drawers/dialogs/overlays que se superponen | 🟡 Medio |

#### Paso 2.5: Follow-the-Flow — Análisis End-to-End (OBLIGATORIO)

> ⚠️ **No basta con revisar el diff del ticket.**
> Los bugs más graves aparecen cuando se sigue el flujo completo de una feature:
> quién la llama → qué persiste → quién la consume → qué muestra el FE.
> Esta técnica es la que mayor densidad de bugs reales produce.

Para cada cambio significativo del ticket (nuevo servicio, guard, endpoint, componente):

```
FLOW MAP — [nombre del cambio]

1. CALLERS: ¿Quién invoca este código?
   → Listar todos los controllers/handlers/hooks que llaman al servicio/guard
   → Buscar si hay callers en OTRO repo (cross-repo)

2. PERSISTENCIA: ¿Qué se guarda en BD?
   → ¿INSERT/UPDATE se ejecuta ANTES o DESPUÉS del guard?
   → ¿Hay filas huérfanas si el guard bloquea después del insert?
   → ¿El registro es atómico o puede quedar parcial?

3. CONSUMIDORES: ¿Quién lee ese dato después?
   → ¿El FE lee del snapshot guardado o de un endpoint live?
   → ¿Hay otro servicio que asume que el dato siempre existe?

4. RENDER: ¿Cómo lo ve el usuario final?
   → ¿Qué muestra la UI cuando el dato es null/0/vacío?
   → ¿El formato (moneda, fecha, porcentaje) es correcto?

5. ERROR PATH: ¿Qué pasa cuando falla?
   → ¿Catch vacío? ¿Retry? ¿Estado huérfano?
   → ¿El error se muestra al usuario o se silencia?

6. OPERACIÓN OPUESTA: ¿Existe el flujo inverso?
   → Si hay create, ¿hay delete simétrico con guard/consumo?
   → Si hay upgrade, ¿hay downgrade que revoca?
   → Si hay subscribe, ¿hay unsubscribe que limpia?
```

Para cada flujo mapeado, buscar:

| Patrón | Qué buscar |
|--------|----------|
| **Asimetría** | Una dirección tiene guard/validación/registro y la opuesta no |
| **Hueco** | Paso que no persiste ni notifica (fire-and-forget sin registro) |
| **Divergencia** | Mismo flujo implementado en dos repos/stacks produce resultado distinto |
| **Dependencia frágil** | Paso que depende de columna computed, seeder, o estado externo sin fallback |
| **Estado zombie** | Dato insertado que nunca se limpia en el path de error/rechazo |

#### Paso 2.75: QA Heuristics Sweep (OBLIGATORIO)

> ⚠️ **Después del Follow-the-Flow, aplicar este checklist de micro-patrones.**
> Son patrones que aplican a CUALQUIER ticket, independientemente del dominio.
> Recorrer cada uno mentalmente contra los archivos modificados.

| Categoría | Qué verificar |
|-----------|---------------|
| **Inputs** | Trimming, campos required, max length, caracteres especiales, inyección en campos de texto libre |
| **UX states** | Loading visible mientras carga; estado empty cuando no hay datos; error accionable cuando falla; primary actions deshabilitados durante loading |
| **Double actions** | Doble clic en botones de submit/save/delete; retry rápido; misma acción desde múltiples tabs del browser |
| **Data integrity** | Registros duplicados por doble submit; saves parciales por error mid-transaction; stale cache tras update |
| **Permisos** | Acciones restringidas no expuestas en UI O que fallan con mensaje claro; verificar que el backend también valida (no solo el FE) |
| **Cross-repo contracts** | Nombres de campos consistentes entre backend response y frontend binding; response shapes esperadas; status codes acordados; timeouts configurados |
| **Observabilidad** | Errores visibles y accionables (no silenciosos); toasts/banners con mensaje útil; logs suficientes para debugging sin exponer datos sensibles |
| **Idempotencia** | Re-ejecutar seeders/fixtures/migraciones no duplica datos; re-intentar una operación fallida no corrompe estado |

---

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

> Cada hallazgo usa un **prefijo de categoría** para clasificación rápida:
> - `BUG-CR-##` — Bug confirmado reproducible (introducido o expuesto por el ticket)
> - `RISK-CR-##` — Riesgo que podría fallar bajo condiciones específicas
> - `SEC-CR-##` — Hallazgo de seguridad (auth, autorización, exposición de datos)
> - `EDGE-CR-##` — Edge case, regresión en componentes compartidos, idempotencia

##### Clasificación de Origen (OBLIGATORIO)

> ⚠️ **Antes de documentar un hallazgo, determinar si es del ticket o pre-existente.**
> Mezclar bugs pre-existentes con bugs del ticket contamina el reporte y genera fricción con el developer.

| Origen | Criterio | Dónde va |
|--------|---------|----------|
| **Ticket-introduced** | El issue está en líneas/archivos tocados por commits del ticket Y el comportamiento coincide con el scope del cambio | En `code-review-qa.md` como BUG-CR/RISK-CR/SEC-CR/EDGE-CR |
| **Ticket-exposed** | El issue está en código no tocado PERO la feature del ticket lo expone o activa por primera vez | En `code-review-qa.md` con nota: "Expuesto por el ticket, no introducido" |
| **Pre-existente** | El issue está en archivos NO tocados por el ticket Y no tiene relación lógica con el cambio | En archivo separado: `L3-tickets/<id>/pre-existing-bugs.md` |
| **Origen incierto** | No se puede determinar con certeza si es del ticket o pre-existente | Clasificar como RISK-CR con nota: "Origen incierto — verificar con git blame" |

**Pre-existentes** — formato de `pre-existing-bugs.md`:

```markdown
# Bugs Pre-existentes — Encontrados durante Code Review de [TICKET-ID]

> Estos bugs NO fueron introducidos por el ticket. Se documentan por separado
> para evitar contaminar el reporte del developer.

## PRE-001: [título]
- Repo + Archivo + Línea: [evidencia]
- Por qué es pre-existente: [el archivo no fue tocado / el bug existía antes]
- Pasos de reproducción: [si aplica]
- Impacto: [qué afecta]
- Acción sugerida: [crear ticket separado / ignorar / documentar]
```

Para cada hallazgo, usar este formato:

```
[BUG|RISK|SEC|EDGE]-CR-[NNN]:
  Categoría: BUG / RISK / SEC / EDGE
  Severidad: 🔴 Crítico / 🟠 Alto / 🟡 Medio
  Repo: [gateway-ion / flow_binaries / gateway / webcomponents-flow]
  Commit: [hash del commit del ticket que introduce/expone el hallazgo]
  Archivo: [ruta del archivo]
  Línea: [rango de líneas, ej: 94-229]
  
  Descripción: [qué encontré — una línea concisa]
  
  Evidencia: 
    [fragmento de código relevante con líneas]
  
  Comportamiento Esperado:
    [qué debería hacer el código según los AC/dominio]
  
  Comportamiento Actual:
    [qué hace el código hoy — descripción técnica precisa]
    [Esto permite evaluar el bug sin ejecutar el código]
  
  Precondiciones:
    User Role: [Admin / Tenant User / Account User]
    User State: [Logged in / Logged out]
    Company/Tenant: [Nueva / Existente / Sin suscripción / Plan específico]
    Existing Data: [datos que deben existir para reproducir]
    Environment State: [condiciones especiales — si aplica]
  
  Pasos de Reproducción:
    [Usar el template de UI que mejor aplique — ver "Templates de Pasos por Tipo de UI" abajo]
    1) [Paso concreto con ruta de navegación]
    2) [Acción que dispara el bug]
    3) [Verificación — qué observar]
  
  Test Data: [datos específicos necesarios para reproducir]
  
  Impacto: [consecuencia concreta si no se corrige — una línea]
  
  Notas: [referencia cruzada con otros bugs, tests unitarios existentes,
          divergencia documentada vs código, etc.]
  
  Recomendación:
    - Si BUG → Reportar al Developer antes de continuar testing
    - Si RISK/EDGE → Inyectar como TC en la test-matrix
    - Si SEC → Escalar al Developer Y documentar en el reporte de seguridad
```

##### Templates de Pasos por Tipo de UI

> Usar el template que mejor se ajuste al tipo de interacción. Adaptar al caso concreto.
> **Siempre** empezar con contexto de navegación e incluir al menos un paso de verificación.

**Template A — CRUD (Create/Edit/Delete)**
```
1) Navegar a [Módulo] → [Sección]
2) Clic en [New/Create]
3) Completar campos requeridos
4) Clic en [Save]
5) Verificar: el item aparece en la lista con datos correctos
6) (Edit) Abrir item → modificar campo → [Save] → verificar actualización
7) (Delete) [Delete] → confirmar modal → verificar que desaparece sin ghost entries
```

**Template B — Form Submit / Auth / Settings**
```
1) Navegar a [Página]
2) Ingresar valores (incluir al menos un caso inválido)
3) Clic en [Submit/Save]
4) Verificar: feedback de éxito + redirect/estado esperado
5) Refrescar página y verificar que el estado persiste
```

**Template C — Table/List (Filtros, Búsqueda, Paginación)**
```
1) Navegar a [Página de lista]
2) Aplicar filtro/búsqueda
3) Verificar: solo filas que coinciden + conteo correcto
4) Cambiar orden → verificar ordenamiento
5) Paginar → verificar cambio de datos
6) Limpiar filtros → verificar retorno al estado por defecto
```

**Template D — Modal / Diálogo / Confirmación**
```
1) Navegar a [Página]
2) Disparar modal (clic en [Edit/Delete/Configure])
3) Verificar: modal abre con título/contenido correcto
4) Intentar submit inválido → verificar error inline
5) Submit válido → verificar que el modal cierra + datos se actualizan
6) Cerrar vía X / Cancel / Esc → verificar que no se aplicaron cambios
```

**Template E — Builder/Canvas (Editor de Flows/Boards)**
```
1) Navegar a Boards/Spaces → abrir board existente o crear nuevo
2) Agregar nodo (Trigger/Action)
3) Configurar campos requeridos
4) Conectar nodos
5) Clic en [Save]
6) Recargar board → verificar que nodos y conexiones persisten
7) Run/Preview (si disponible) → verificar status y output en UI
```

**Template F — Error/Resiliencia (Red, Backend errors)**
```
1) Navegar a [Página de la feature]
2) Simular red lenta (throttle) o forzar error de backend
3) Ejecutar acción (Save/Run/Create)
4) Verificar: UI muestra mensaje de error accionable (no silencio)
5) Verificar: path de retry existe y funciona (si aplica)
6) Verificar: no se crearon registros parciales/duplicados
```

#### Paso 5: Inyectar Hallazgos en la Test Matrix (OBLIGATORIO)

> ⚠️ Los hallazgos del code review NO quedan solo en code-review-qa.md.
> Cada bug/riesgo que requiere verificación se AGREGA como TC nuevo en la test-matrix.

Para cada hallazgo que requiere verificación en testing:

1. **Agregar un nuevo TC** a `test-matrix.md` y `test-matrix.csv` con:
   - **ID**: `TC-CR-001`, `TC-CR-002`, etc. (prefijo CR = Code Review)
   - **Tipo**: `EC` (Edge Case) — categoría que identifica el origen
   - **Caso de Test**: Descripción del escenario a verificar
   - **Pasos**: Ruta de navegación explícita con precondiciones estructuradas
   - **AC**: Referencia al hallazgo origen (ej: `BUG-CR-001`)
   - **Resultado Esperado**: Comportamiento correcto según AC/dominio
   - **Comportamiento Actual**: Qué hace el código hoy (permite evaluar sin ejecutar)
   - **Prioridad**: Heredada de la severidad del hallazgo
   - **Notas**: `Repo: <name> | Commit: <hash> | Files: <paths>` para trazabilidad

2. **Agrupar los TCs inyectados** en una Suite dedicada con subsecciones:
   - **Bugs Confirmados** (BUG-CR): Primero, porque son los más urgentes
   - **Riesgos** (RISK-CR): Segundo, requieren verificación manual
   - **Seguridad** (SEC-CR): Si aplica para este ticket
   - **Edge Cases** (EDGE-CR): Regresiones, idempotencia, boundary

3. **Actualizar el resumen de la test-matrix**:
   - Agregar línea: `Code Review: [N]` al conteo de tipos con desglose por categoría
   - Actualizar total de casos

Ejemplo de TC inyectado (formato de test-matrix.md):

```
| TC-CR-001 | EC | [Descripción concisa del hallazgo] |
  1. [Precondición o navegación]<br>
  2. [Acción que dispara el bug]<br>
  3. [Verificación — qué observar] |
  [BUG|RISK|SEC|EDGE]-CR-NNN | 🔴/🟠/🟡 | ⬜ |
```

Ejemplo de TC inyectado (formato CSV para test-matrix.csv):

```csv
"[PREFIJO]-CR-NNN [Descripción concisa del hallazgo]",
"User Role: [rol]; User State: [estado]; Existing Data: [datos necesarios]",
"1) [Paso 1]; 2) [Paso 2]; 3) [Verificación]",
"[Datos de prueba específicos]",
"[Comportamiento esperado según AC/dominio]",
"[Comportamiento actual observado en código]",
"P1/P2/P3",
"[Notas relevantes]",
"Repo: [nombre] | Commit: [hash] | Files: [rutas:líneas]",
""
```

### Stage 3 — REPORTING

Guardar en `L3-tickets/<id>/code-review-qa.md`:

```markdown
# Code Review QA — [TICKET-ID] (Modo Deployment / Bug Hunting)

## Resumen
- Repos revisados: [lista]
- Commits analizados: [N] (hashes listados abajo)
- Archivos modificados analizados: [N]
- Hallazgos totales: [N]
  - BUG confirmados: [N] (🔴: N, 🟠: N, 🟡: N)
  - RISK a verificar: [N]
  - SEC seguridad: [N]
  - EDGE cases: [N]
- Módulos con impacto cruzado: [lista]
- TCs inyectados en test-matrix: [N] (TC-CR-001 a TC-CR-NNN)

## Commits Analizados
| Repo | Commit | Mensaje | Archivos |
|------|--------|---------|----------|
| [repo] | [hash] | [mensaje] | [N archivos] |

## Archivos Modificados
[tabla de archivos por repo con líneas cambiadas]

## Sección 1 — BUGs Confirmados (BUG-CR-##)
> Defectos reproducibles introducidos o expuestos por los cambios del ticket.
[lista de BUG-CR-NNN con formato completo]
[Cada uno incluye Comportamiento Esperado, Comportamiento Actual, Precondiciones y Pasos]

## Sección 2 — Riesgos a Verificar (RISK-CR-##)
> Patrones frágiles que podrían fallar bajo condiciones específicas.
[lista de RISK-CR-NNN con escenario para verificar]

## Sección 3 — Seguridad (SEC-CR-##)
> Hallazgos de autenticación, autorización, exposición de datos.
> Solo si aplica para este ticket — si no hay hallazgos, omitir esta sección.
[lista de SEC-CR-NNN]

## Sección 4 — Edge Cases (EDGE-CR-##)
> Casos límite, regresiones en componentes compartidos, idempotencia.
[lista de EDGE-CR-NNN]

## Follow-the-Flow Maps
[Flujos mapeados durante el Paso 2.5 — solo los que revelaron hallazgos]

## Impacto Cruzado
[tabla de módulos impactados]

## TCs Inyectados en Test Matrix
| TC ID | Categoría | Origen | Caso de Test | Severidad |
|-------|-----------|--------|-------------|-----------|
| TC-CR-001 | BUG | BUG-CR-001 | [descripción] | 🔴 |
| TC-CR-002 | RISK | RISK-CR-001 | [descripción] | 🟠 |
| TC-CR-003 | SEC | SEC-CR-001 | [descripción] | 🔴 |
| TC-CR-004 | EDGE | EDGE-CR-001 | [descripción] | 🟡 |
```

> Los bugs del code review se INCLUYEN en el reporte final (`sprint-testing/report`).
> Los TCs del code review se EJECUTAN como parte normal del testing en `sprint-testing/test`.
> Los screenshots de fallos de TCs del code review persisten como evidencia permanente.

---

## Reglas de este Skill

1. **Todo bug DEBE ser reproducible** — Si no se puede reproducir paso a paso, es un RIESGO A VERIFICAR, no un BUG CONFIRMADO
2. **Los pasos de reproducción usan templates de UI** — Usar el template (A-F) que mejor aplique al tipo de interacción; siempre incluir verificación
3. **Actualizar repos ANTES de leer código** — Nunca revisar código desactualizado
4. **Solo operaciones de LECTURA** — Nunca modificar código de los repos de desarrollo
5. **Consultar Impacto Cruzado del L2** — Siempre verificar qué módulos pueden verse afectados
6. **Los hallazgos se inyectan en la test-matrix** — No quedan solo en el code-review-qa.md
7. **Queries de BD basadas en migraciones** — Nunca inventar campos, tablas ni relaciones
8. **En Discovery: preguntas, no objeciones** — El tono es colaborativo
9. **En Deployment: búsqueda activa de defectos** — El tono es riguroso
10. **El QA Engineer decide** — La IA sugiere, el QA Engineer aprueba
11. **Nivel 2 es obligatorio** — Los checklists de Lógica de Negocio y Business Display NO son opcionales; los bugs más graves están ahí
12. **Follow-the-Flow es obligatorio** — Para cada cambio significativo, mapear el flujo end-to-end antes de documentar hallazgos
13. **QA Heuristics Sweep es obligatorio** — Aplicar el checklist de micro-patrones después del Follow-the-Flow
14. **Siempre documentar Comportamiento Actual** — Cada hallazgo debe incluir qué hace el código hoy, no solo qué debería hacer
15. **Commit hash en cada hallazgo** — Trazabilidad al commit específico del ticket que introduce/expone el bug
16. **4 categorías, no 2** — Usar BUG/RISK/SEC/EDGE, no solo "confirmado" vs "riesgo"
17. **Separar pre-existentes** — Bugs que NO son del ticket van a `pre-existing-bugs.md`, nunca al reporte del developer
18. **Clasificar origen antes de documentar** — Determinar si es ticket-introduced, ticket-exposed, pre-existente o incierto ANTES de escribir el hallazgo
