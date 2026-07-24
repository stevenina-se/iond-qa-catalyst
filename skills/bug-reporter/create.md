# Skill: bug-reporter/create

> Genera un ticket de bug completo y categorizado a partir de una descripción informal del QA Engineer.
> Independiente del Discovery Track y del Deployment Track.

---

## Cuándo usar este skill

**Frase disparadora:**
```
Crea un nuevo ticket:
```

Seguida de:
- **Path de navegación** — indicando el módulo afectado. Ejemplo: `Company > Boards > [funcionalidad]`
- **Descripción informal del bug** — puede ser telegráfica o no técnica; el agente la formaliza

**Ejemplos de invocación válidos:**

```
Crea un nuevo ticket: Company > Boards — al crear un flow con nombre duplicado no muestra error

Crea un nuevo ticket: Company > Connections > ZID — el OAuth falla con state field required

Crea un nuevo ticket: Admin > Accounts — el botón de desactivar cuenta no responde en móvil
```

---

## Pre-requisitos

No se requieren artefactos previos (L3, test-matrix, etc.). Este skill opera desde cero.

Lo que SÍ se necesita:
- ✅ `knowledge/L1-project/` disponible para leer
- ✅ `knowledge/L2-modules/<módulo>/` del módulo identificado disponible
- ✅ Los 4 repositorios de desarrollo accesibles en `../`

---

## Stage 1 — PLANNING

### Paso 1.1 — Parsear la invocación

Al recibir `Crea un nuevo ticket:`, extraer:

1. **Path de navegación** → identificar el/los módulo(s) L2 afectados
2. **Descripción del bug** → guardar tal cual para procesarla después

**Mapeo path → L2:**

| Path recibido (ejemplos) | Módulo L2 a cargar |
|--------------------------|-------------------|
| `Company > Boards` | `knowledge/L2-modules/boards/` |
| `Company > Connections` | `knowledge/L2-modules/connections/` |
| `Company > Executions` | `knowledge/L2-modules/executions/` |
| `Company > Dashboard` | `knowledge/L2-modules/dashboard/` |
| `Company > Data Store` | `knowledge/L2-modules/data-store/` |
| `Company > Keys` | `knowledge/L2-modules/keys/` |
| `Company > Webhooks` | `knowledge/L2-modules/webhooks/` |
| `Company > Integrations` | `knowledge/L2-modules/integrations/` |
| `Company > Developer Apps` | `knowledge/L2-modules/developer-apps/` |
| `Company > PDF Templates` | `knowledge/L2-modules/pdf-templates/` |
| `Company > Services` | `knowledge/L2-modules/services/` |
| `Company > Accounts` | `knowledge/L2-modules/accounts/` |
| `Admin > *` | Cargar módulo correspondiente |

> Si el módulo no está claro → preguntar al QA Engineer antes de continuar.
> Si afecta múltiples módulos → cargar todos los L2 relevantes.

### Paso 1.2 — Anunciar el plan

Reportar al QA Engineer **antes de ejecutar**:

```
🐛 BUG REPORTER — PLAN

Módulo identificado: [módulo(s)]
L2 a cargar: knowledge/L2-modules/[módulo]/
Repos a actualizar: gateway-ion, flow_binaries, gateway, webcomponents-flow

Bug reportado (descripción original):
"[descripción tal como la dio el QA Engineer]"

Plan de ejecución:
1. Actualizar los 4 repos a DEVELOPMENT
2. Cargar L1 + L2 del módulo
3. Analizar el bug con contexto técnico real
4. Generar draft completo del ticket

¿Procedo?
```

**Esperar confirmación del QA Engineer.**

---

## Stage 2 — EXECUTION

### Paso 2.1 — Actualizar repos a DEVELOPMENT

```bash
# OBLIGATORIO: actualizar antes de leer código
cd ../gateway-ion && git fetch origin && git checkout DEVELOPMENT && git pull origin DEVELOPMENT
cd ../flow_binaries && git fetch origin && git checkout DEVELOPMENT && git pull origin DEVELOPMENT
cd ../gateway && git fetch origin && git checkout DEVELOPMENT && git pull origin DEVELOPMENT
cd ../webcomponents-flow && git fetch origin && git checkout DEVELOPMENT && git pull origin DEVELOPMENT
```

> ❌ NUNCA hacer git push, commit, ni merge — Solo operaciones de LECTURA
> ✅ Este paso es OBLIGATORIO para tener contexto técnico real y actualizado

### Paso 2.2 — Cargar contexto

1. Leer `knowledge/L1-project/`:
   - `business-rules.md`
   - `stack-overview.md`
   - `api-architecture.md`

2. Leer `knowledge/L2-modules/<módulo>/module.md`:
   - Sección de lógica de negocio (rutas, endpoints, validaciones)
   - Sección de Base de Datos (schema para evidencia técnica)
   - Sección de Edge Cases Conocidos (¿es un bug ya documentado?)
   - Sección de Impacto Cruzado (¿afecta otros módulos?)

### Paso 2.3 — Análisis técnico del bug

Con los repos actualizados y el L2 cargado, investigar siguiendo el protocolo de evidencia verificable.

#### A) Ejecutar búsquedas reales y documentar el resultado

Correr los greps necesarios usando los términos clave del bug (nombre de función, endpoint, componente, mensaje de error, etc.).
El resultado del grep — incluyendo cuándo da **0 resultados** — es parte de la evidencia.

```bash
# Buscar en el frontend (Vue)
grep -r "[término clave del bug]" ../gateway-ion/src/ --include="*.vue" --include="*.ts" -l

# Buscar en el backend Go
grep -r "[término clave]" ../flow_binaries/ --include="*.go" -l

# Buscar en el legacy PHP
grep -r "[término clave]" ../gateway/app/ --include="*.php" -l

# Para ver contexto de líneas alrededor del hit:
grep -rn "[término clave]" ../gateway-ion/src/ --include="*.vue" -A 5 -B 2
```

> 🔴 REGLA CRÍTICA: Antes de citar cualquier fragmento de código en la sección "Evidencia Técnica",
> DEBES haber ejecutado el grep y obtenido un hit real (archivo + número de línea concretos).
> **Nunca construir un bloque de código a partir de lo que "debería existir" según el L2 o la intuición.**

#### B) Clasificar la evidencia encontrada

Cada pieza de evidencia técnica debe etiquetarse con uno de estos tres niveles:

| Nivel | Cuándo usar | Cómo presentar en el ticket |
|-------|-------------|-----------------------------|
| `[CONFIRMADA]` | Se encontró el código/log/query con grep o lectura directa y verificada | Incluir bloque de código con ruta exacta y número de línea real |
| `[INFERIDA]` | El L2 documenta el comportamiento esperado pero el grep no devolvió hits concretos | Citar el L2 como fuente, NO construir código ficticio. Usar lenguaje de hipótesis |
| `[AUSENTE]` | Se buscó y no existe validación / manejo del caso | Declarar explícitamente que la búsqueda dio 0 resultados, no inventar el código faltante |

**Ejemplo de uso correcto:**

```
[CONFIRMADA] Frontend — ../gateway-ion/src/views/boards/BoardsView.vue:142
  const handleDuplicate = async (flow) => {
    await api.duplicateFlow(flow.id)   // sin validación de nombre único
  }

[AUSENTE] No se encontró lógica de validación de nombre único en el handler de duplicación.
  Búsqueda ejecutada: grep -rn "duplicate" ../gateway-ion/src/ --include="*.vue"
  Resultado: 0 archivos con validación de nombre en el flujo de duplicación.

[INFERIDA] Según el L2 (boards/module.md — sección Validaciones), el backend debería
  rechazar duplicados vía el endpoint POST /flows/duplicate, pero no se encontró
  el guard correspondiente en ../flow_binaries/.
```

**Ejemplo de lo que NUNCA hacer:**

```
❌ MAL — Código inventado sin grep:
// ../gateway-ion/src/views/boards/BoardsView.vue — línea 142
// No se encontró validación de nombre único en el handler de duplicación

❌ MAL — Ruta de archivo plausible pero no verificada:
// El archivo duplicateFlow.go probablemente maneja esto en la línea ~87
```

#### C) Identificar la causa raíz probable

Basándose en el L2 y los hits reales del grep:
- ¿Qué componente/endpoint/función está involucrado? (citar solo lo encontrado)
- ¿Cuál es la causa raíz más probable?
- ¿Hay validaciones faltantes, condiciones de carrera, manejo de errores incompleto?

> Si la causa raíz es una **hipótesis** (no confirmada por código real) → colocarla en la sección
> **Notas Adicionales** del ticket, no en "Evidencia Técnica". Usar el prefijo: `[Hipótesis técnica]:`

#### D) Preparar evidencia técnica para el ticket

Recopilar solo lo verificable:
- Fragmento de código `[CONFIRMADA]`: ruta real + número de línea real
- Respuesta de API esperada vs. actual: solo si se observó en una ejecución real o en logs
- Query de BD `[CONFIRMADA]`: construida EXCLUSIVAMENTE desde migraciones verificadas en `../gateway/`
- Mensajes de error observados: exactamente como aparecen, no parafraseados
- Evidencia `[AUSENTE]` o `[INFERIDA]`: etiquetada como tal, con la búsqueda realizada documentada

> ⚠️ NUNCA inventar campos, tablas, rutas de archivo ni números de línea — solo lo que existe verificado
> ⚠️ Un fragmento de código sin un grep hit que lo respalde es una alucinación, aunque sea plausible

### Paso 2.4 — Categorizar el ticket

#### Prioridad

| Nivel | Criterio | Ejemplos |
|-------|----------|---------|
| **urgent** | Funcionalidad core completamente rota, bloqueante para producción, afecta múltiples tenants o flujos críticos | Login roto, flows no ejecutan, pérdida de datos |
| **high** | Bug que afecta flujo principal del módulo, sin workaround simple, impacto significativo en UX | Feature core inaccesible, datos incorrectos en resultados |
| **normal** | Bug con impacto moderado, hay workaround disponible, no bloquea el flujo completo | Filtro que no funciona bien, validación inconsistente |
| **low** | Cosmético, edge case muy raro, no impacta el flujo principal ni la integridad de datos | Typo en UI, alineación incorrecta, mensaje de error poco claro |

#### Tipo de ticket

| Tipo | Cuándo aplicar |
|------|---------------|
| **bug** | Comportamiento incorrecto vs. expectativa documentada o lógica de negocio establecida |
| **refactor** | El código funciona pero la implementación tiene deuda técnica que genera riesgo |
| **new feature** | Funcionalidad que no existe en el sistema y se está solicitando implementar |
| **task** | Trabajo técnico sin impacto directo en UX: configuración, infraestructura, documentación |
| **improvement** | Mejora de UX, performance o usabilidad de algo que ya funciona correctamente |

> **Regla**: Si el usuario reporta algo que "no funciona como se espera" → es **bug** por defecto.
> Solo reclasificar si hay evidencia clara de que la funcionalidad nunca existió (→ new feature)
> o de que es un problema de implementación interna sin impacto funcional (→ refactor).

### Paso 2.5 — Generar el draft del ticket

Completar el template `templates/bug-ticket.md` aplicando estas reglas:

#### Título
- Conciso, descriptivo, en formato: `[Módulo] — [Descripción corta del problema]`
- Máximo 80 caracteres
- Evitar: "bug en", "error de", "problema con" → ir directo al problema
- ✅ Bien: `Boards — Flow duplicado no genera error de validación`
- ❌ Mal: `Error al crear flow con nombre duplicado en boards`

#### Description of the validated/replicated problem
- Formalizar la descripción informal del QA Engineer
- Incluir: qué ocurre, bajo qué condiciones, si es consistente/intermitente
- Mencionar si hay contexto de regresión (funcionaba antes)
- Mencionar tickets relacionados si el QA Engineer los indicó
- Tono técnico-formal, sin jerga coloquial

#### Steps to Reproduce

**Caso A — El QA Engineer proporcionó los pasos:**
- NO reemplazar los pasos dados
- Refinar y complementar: corregir formato, agregar pasos implícitos que falten,
  asegurarse de que incluyan pre-condiciones, usar formato breadcrumb
- Formato breadcrumb: `Company Login > Sidebar: [Módulo] > Button: "[Nombre]" > ...`

**Caso B — El QA Engineer NO proporcionó los pasos:**
- Generar los pasos desde cero basándose en:
  - El path de navegación dado (`Company > Boards > ...`)
  - El L2 del módulo (rutas, flujos documentados)
  - El código real del frontend (`../gateway-ion/src/`)
- Los pasos deben ser reproducibles por un Developer sin contexto previo

#### Datos utilizados
- Siempre incluir: usuario/rol, entorno, versión (DEVELOPMENT), URL si aplica
- Si el QA Engineer dio datos específicos → incluirlos exactamente
- Si no → indicar qué datos serían necesarios para reproducir

#### Current Behavior
- Describir objetivamente lo que ocurre
- Incluir evidencia técnica real (del código actualizado)
- Fragmentos de código → siempre con ruta de archivo y número de línea
- Si hay respuesta de API errónea → incluir el JSON/respuesta exacta si se conoce

#### Expected Behavior
- Basarse en el L2 del módulo y las business rules del L1
- Si el módulo tiene criterios de aceptación documentados → referenciarlos
- Ser específico: no "debería funcionar bien" sino "debería [acción concreta]"

#### Impacto
- Identificar qué usuarios/roles se ven afectados (Company, Admin, ambos)
- Indicar si bloquea flujos completos o es parcial
- Si el L2 tiene sección "Impacto Cruzado" → verificar si otros módulos se ven afectados

---

## Stage 3 — REPORTING

### Paso 3.1 — Presentar el draft al QA Engineer

```
🐛 DRAFT DE TICKET GENERADO

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Contenido completo del ticket formateado]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Categorización:
  📊 Prioridad: [urgent / high / normal / low]
  🏷️  Tipo: [bug / refactor / task / new feature / improvement]
  📌 Módulo: [nombre del módulo L2]

Razonamiento:
  Prioridad [X] porque: [razón basada en los criterios de la tabla]
  Tipo [Y] porque: [razón basada en los criterios de la tabla]

¿Apruebas el draft o deseas ajustar algo?
```

### Paso 3.2 — Ajustes y aprobación

- El QA Engineer puede pedir ajustes en cualquier sección
- Aplicar los ajustes y presentar el draft revisado
- Una vez aprobado → el QA Engineer crea el ticket en ClickUp manualmente

### Paso 3.3 — Guardar en L3 (cuando el QA Engineer da el ID)

Cuando el QA Engineer proporcione el ID o nombre del directorio del ticket:

```
Guardar en: knowledge/L3-tickets/<ticket-id>/bug-report.md
```

El archivo `bug-report.md` es el draft aprobado del ticket.
Esto permite usar el ticket como punto de entrada para Discovery o Deployment futuros.

> **Nota**: No crear el directorio L3 hasta que el QA Engineer proporcione el ID de ClickUp.
> No es necesario esperar — la sesión puede terminar después de la aprobación del draft.

---

## Reglas de este Skill

1. **SIEMPRE actualizar los repos a DEVELOPMENT antes de analizar** — Nunca usar código desactualizado
2. **NUNCA inventar evidencia técnica** — Solo código real de los repos actualizados, con grep ejecutado y resultado documentado
3. **NUNCA hacer git push, commit, ni merge** — Solo operaciones de lectura en repos de desarrollo
4. **El draft es una propuesta** — El QA Engineer aprueba antes de crear el ticket en ClickUp
5. **Formalizar sin distorsionar** — La descripción informal del QA Engineer se formaliza pero no se altera en su esencia
6. **Pasos dados por el QA → refinar, no reemplazar** — Si el QA Engineer dio pasos, complementarlos
7. **Pasos no dados → generarlos** — Desde el path de navegación + L2 + código real
8. **La categorización va con razonamiento** — Siempre explicar POR QUÉ la prioridad y el tipo asignados
9. **El ID de L3 lo da el QA Engineer** — No crear estructura L3 hasta recibir el ID de ClickUp
10. **Si el bug ya está en Edge Cases del L2** → mencionarlo como contexto (podría ser un bug conocido que escaló)
11. **Toda evidencia técnica debe llevar su nivel: `[CONFIRMADA]`, `[INFERIDA]` o `[AUSENTE]`** — Sin etiqueta, no va al ticket
12. **Hipótesis técnicas → van en Notas Adicionales, no en Evidencia Técnica** — Usar prefijo `[Hipótesis técnica]:` y citar el razonamiento
13. **Un bloque de código sin grep hit verificado es una alucinación** — Aunque el código parezca plausible o el L2 lo sugiera, si no se encontró en el repo, no se incluye como código real
14. **Cuando el grep da 0 resultados, eso también es evidencia** — Documentar la búsqueda realizada y declarar `[AUSENTE]` en lugar de inferir el código faltante

---

## Referencia Rápida — Repos de Desarrollo

> Los repos están en `../` (UN NIVEL ARRIBA de este repositorio).

| Repo | Path | Stack | Buscar bugs en |
|------|------|-------|---------------|
| Frontend | `../gateway-ion/` | Vue 3 + TS | Componentes, rutas, validaciones UI, guards |
| Backend core | `../flow_binaries/` | Go | Endpoints, lógica de negocio, manejo de errores |
| Canvas | `../webcomponents-flow/` | Vue 3 + TS | Componentes del canvas, nodos, edges |
| Legacy/Auth | `../gateway/` | PHP 8.2 | Auth, permisos, migraciones BD, integraciones |

---

## Ejemplo Completo de Invocación

**Input del QA Engineer:**
```
Crea un nuevo ticket: Company > Boards — al duplicar un flow con nombre ya existente 
no aparece ningún mensaje de error, se crea silenciosamente con nombre duplicado
```

**Output esperado del agente:**

```
🐛 BUG REPORTER — PLAN

Módulo identificado: boards
L2 a cargar: knowledge/L2-modules/boards/
Repos a actualizar: los 4

Bug reportado:
"al duplicar un flow con nombre ya existente no aparece ningún mensaje de error, 
se crea silenciosamente con nombre duplicado"

¿Procedo?
```

→ Tras confirmación:

```
🐛 DRAFT DE TICKET GENERADO

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# QA FOUND ISSUE ESCALATION REPORT — BOARDS

## Información General
| Módulo | boards |
| Path | Company > Boards |
| Prioridad | normal |
| Tipo | bug |
...

## Description of the validated/replicated problem
Al duplicar un flow que ya tiene un nombre idéntico a otro existente en la misma 
compañía, el sistema no muestra ningún mensaje de validación y crea el flow 
silenciosamente con el nombre duplicado. El problema es consistente y reproducible...

## Steps to Reproduce
1. Company Login > Sidebar: Boards
2. Seleccionar cualquier flow existente > Button: "..." (opciones) > "Duplicate"
3. Observar que el nuevo flow es creado sin advertencia, con el mismo nombre

## Current Behavior
El sistema crea el flow duplicado sin mostrar error ni validación...

### Evidencia Técnica
// ../gateway-ion/src/views/boards/BoardsView.vue — línea 142
// No se encontró validación de nombre único en el handler de duplicación
...

## Expected Behavior
El sistema debería validar que no existe otro flow con el mismo nombre...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Categorización:
  📊 Prioridad: normal — afecta integridad de datos pero no bloquea flujo principal
  🏷️  Tipo: bug — comportamiento incorrecto vs. expectativa de unicidad de nombres
  📌 Módulo: boards

¿Apruebas el draft o deseas ajustar algo?
```
