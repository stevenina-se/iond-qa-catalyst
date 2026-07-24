# Skill: release/bug-hunt

> Búsqueda proactiva de bugs antes de salir a producción.
> Dado un módulo, combina análisis de código estático + API attack vectors + opcionalmente Playwright MCP.
> Todos los bugs deben ser reproducibles. Se integra con `bug-reporter/create` cuando el QA lo autoriza.

---

## Cuándo usar este skill

**Frase disparadora:**
```
Bug Hunt: <Módulo>
```

Seguida opcionalmente de:
- **Área específica** — ej. `Bug Hunt: Boards — validaciones de duplicación`
- **Versión del release** — ej. `para v1.0.0` (para guardar en el directorio correcto)

**Ejemplos:**
```
Bug Hunt: Boards
Bug Hunt: Connections — métodos de autenticación
Bug Hunt: Data Store — CRUD operations para v1.0.0
```

---

## Pre-requisitos

- ✅ `knowledge/L1-project/` completo (business-rules, test-priorities, api-architecture, stack-overview)
- ✅ `knowledge/L2-modules/<módulo>/module.md` del módulo indicado
- ✅ Los 4 repositorios de desarrollo accesibles en `../` y actualizados a DEVELOPMENT

---

## Stage 1 — PLANNING

### Paso 1.1 — Cargar contexto completo

1. Leer L1 completo:
   - `business-rules.md` — Reglas de negocio
   - `test-priorities.md` — Criticidad del módulo
   - `api-architecture.md` — Repos, endpoints, rutas
   - `stack-overview.md` — Stack técnico

2. Leer `knowledge/L2-modules/<módulo>/module.md` completo:
   - Lógica de negocio (rutas, endpoints, validaciones)
   - Base de Datos (schema para queries)
   - **Edge Cases Conocidos** — Para no reportar lo ya documentado
   - **Impacto Cruzado** — Módulos que podrían afectarse

### Paso 1.2 — Actualizar repos

```bash
# OBLIGATORIO: actualizar antes de buscar bugs
cd ../gateway-ion && git fetch origin && git checkout DEVELOPMENT && git pull origin DEVELOPMENT
cd ../flow_binaries && git fetch origin && git checkout DEVELOPMENT && git pull origin DEVELOPMENT
cd ../gateway && git fetch origin && git checkout DEVELOPMENT && git pull origin DEVELOPMENT
cd ../webcomponents-flow && git fetch origin && git checkout DEVELOPMENT && git pull origin DEVELOPMENT
```

> ❌ NUNCA hacer git push, commit, ni merge — Solo operaciones de LECTURA

### Paso 1.3 — Anunciar el plan

```
🐛 BUG HUNT — PLAN

Módulo: [módulo]
Área específica: [área o "módulo completo"]
Criticidad (L1): [🔴/🟠/🟡/🟢]
Versión del release: [versión o "standalone"]

Contexto cargado:
  ✅ L1 completo
  ✅ L2 de [módulo]
  ✅ Repos actualizados a DEVELOPMENT
  ✅ Edge Cases Conocidos leídos ([N] documentados)

Plan de búsqueda:
  Fase 1: Análisis estático del código (grep + lectura)
  Fase 2A: Verificación Backend — API attack vectors (OBLIGATORIA)
  Fase 2B: Verificación UI — Playwright MCP (opcional, preguntaré)

Repos a analizar:
  - Frontend: ../gateway-ion/src/ (Vue 3 + TS)
  - Backend: ../flow_binaries/ (Go)
  - Legacy: ../gateway/app/ (PHP 8.2)
  - Canvas: ../webcomponents-flow/ (Vue 3 + TS)

¿Procedo?
```

**Esperar confirmación del QA Engineer.**

---

## Stage 2 — EXECUTION

### Fase 1 — Análisis de código (estático)

> 🔴 **Protocolo de evidencia del `bug-reporter/create` aplica aquí al 100%.**
> No se puede citar código sin grep hit verificado.
> Reglas 11-14 del bug-reporter son obligatorias.
> Cada pieza de evidencia: `[CONFIRMADA]`, `[INFERIDA]` o `[AUSENTE]`.

#### 1.1 — Buscar en el código

Ejecutar greps con términos clave del módulo (endpoints, funciones, componentes, validaciones):

```bash
# Frontend (Vue)
grep -rn "[término clave]" ../gateway-ion/src/ --include="*.vue" --include="*.ts" -A 3 -B 1

# Backend (Go)
grep -rn "[término clave]" ../flow_binaries/ --include="*.go" -A 3 -B 1

# Legacy (PHP)
grep -rn "[término clave]" ../gateway/app/ --include="*.php" -A 3 -B 1

# Canvas
grep -rn "[término clave]" ../webcomponents-flow/ --include="*.vue" --include="*.ts" -A 3 -B 1
```

#### 1.2 — Qué buscar

| Área | Qué buscar | Indicadores de bug |
|------|------------|-------------------|
| Validaciones | Campos sin validar, tipos no verificados | Datos corruptos en BD |
| Multi-tenant | `company_id` no filtrado en queries | Fuga de datos entre tenants |
| Manejo de errores | `catch` vacíos, errores silenciosos, panic sin recover | Fallos silenciosos |
| Edge cases | Listas vacías, null/undefined, strings vacíos | Crash en UI o backend |
| Inconsistencias FE/BE | Frontend acepta lo que backend rechaza (o viceversa) | UX confusa, datos inválidos |
| Permisos | Endpoints sin guard de autenticación/autorización | Acceso no autorizado |
| Concurrencia | Operaciones no atómicas, race conditions | Datos inconsistentes |
| SQL/Queries | Queries sin parametrizar, concatenación de strings | SQL injection |

#### 1.3 — Clasificar hallazgos

Cada hallazgo estático es `[RIESGO A VERIFICAR]`, **NUNCA** `[BUG CONFIRMADO]` en esta fase.

Consultar "Edge Cases Conocidos" del L2:
- Si el hallazgo ya está documentado → marcarlo como `[CONOCIDO]` y no reportar como nuevo
- Si NO está documentado → es un `[RIESGO A VERIFICAR]` genuino

---

### Fase 2A — Verificación Backend (API attack vectors)

> Esta fase es **OBLIGATORIA** (no opcional como la UI).

Desde el L2 del módulo y el código del backend, construir y proponer requests que intenten romper el sistema.

> ⚠️ Los vectores de ataque a continuación son **ejemplos de referencia, NO una lista cerrada**.
> La skill debe descubrir vectores adicionales específicos al módulo basándose en el código real,
> el L2, y la arquitectura de cada endpoint.

#### Vectores de ejemplo

| Vector | Qué buscar | Ejemplo |
|--------|-----------|---------|
| Payloads malformados | JSON con tipos incorrectos, campos extra, nested objects inesperados | `POST /api/flows` con `{"name": 123}` |
| Campos requeridos faltantes | Omitir obligatorios y verificar que rechaza | `POST /api/flows` sin `company_id` |
| Boundary values | Strings vacíos, enormes (>10K), negativos, 0, MAX_INT, unicode, caracteres especiales | `{"name": ""}`, `{"limit": -1}` |
| Inyección SQL/NoSQL | Inyectar queries vía input | `{"name": "'; DROP TABLE flows;--"}` |
| Multi-tenant violations | Acceder a recursos de otra company | `GET /api/flows/<id-de-otra-company>` |
| Auth bypass | Sin token, token expirado, token de otro rol | `GET /api/admin/...` con token Company |
| Rate limiting / abuse | Requests masivos al mismo endpoint | Loops de `POST /api/flows` |
| File upload abuse | Extensiones prohibidas, tamaños excesivos, MIME falsos | Upload `.php` como `.png` |
| CORS / Headers | Origins no permitidos, headers inesperados | `Origin: evil.com` |
| Race conditions | Requests concurrentes que crean estados inconsistentes | Crear 2 flows con mismo nombre simultáneamente |
| *(descubrir más)* | Cualquier patrón que el código real revele | Depende del módulo |

#### Protocolo de ejecución

Para cada vector identificado:

1. **Identificar el endpoint** en el código (grep obligatorio)
2. **Construir el request** con body exacto
3. **PROPONER al QA Engineer** antes de ejecutar:
   ```
   🐛 REQUEST PROPUESTO:
     Endpoint: POST /api/v1/flows
     Body: {"name": ""}
     Vector: Boundary value — string vacío
     Riesgo esperado: El backend acepte un flow sin nombre
     
   ¿Ejecuto este request?
   ```
4. Si el QA aprueba → ejecutar (curl o similar)
5. **Documentar response**: status code, body, headers
6. Si el backend no valida correctamente → `[BUG CONFIRMADO]`

> ⚠️ Los requests se PROPONEN al QA antes de ejecutar. No ejecutar requests destructivos sin aprobación.
> ✅ Se pueden ejecutar GET requests de lectura sin aprobación previa.

---

### Fase 2B — Verificación UI (opcional, con Playwright MCP)

Preguntar al QA Engineer:

```
¿Deseas verificar los hallazgos de UI con el browser (Playwright MCP)?
  A) Sí — Verifico cada riesgo de UI con el browser
  B) No — Los riesgos quedan como [RIESGO A VERIFICAR] para revisión manual
```

**Si SÍ:**
- Para cada `[RIESGO A VERIFICAR]` de UI:
  1. Generar pasos breadcrumb
  2. Ejecutar con Playwright MCP
  3. Si se reproduce → `[BUG CONFIRMADO]` + screenshot (`FAIL-BH-*.png`)
  4. Si no se reproduce → `[FALSO POSITIVO]` con nota de por qué

**Si NO:**
- Los riesgos quedan como `[RIESGO A VERIFICAR]` para revisión manual futura

---

### Fase 3 — Clasificación y presentación al QA

Presentar la lista completa:

```
🐛 BUG HUNT — Resultados para [Módulo]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BUGS CONFIRMADOS — UI ([N]):
  1. [BUG-BH-001] [Descripción] — Prioridad: [X] — Canal: UI
     Pasos: Company Login > Sidebar: [Módulo] > ...
     Evidencia: screenshot + código [CONFIRMADA]

BUGS CONFIRMADOS — BACKEND ([N]):
  2. [BUG-BH-002] [Descripción] — Prioridad: [X] — Canal: API
     Request: POST /api/flows — Body: {"name": ""}
     Response: 200 OK (debería ser 422)
     Evidencia: código [CONFIRMADA] en ../flow_binaries/...

RIESGOS NO VERIFICADOS ([N]):
  3. [RISK-BH-001] [Descripción] — Confianza: [X]
     Código: [CONFIRMADA] en ../gateway-ion/src/...
     Nota: Requiere datos de prueba específicos

FALSOS POSITIVOS DESCARTADOS ([N]):
  4. [FP-BH-001] [Descripción] — Razón: [por qué se descartó]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Resumen:
  Bugs confirmados: [N] ([N] UI + [N] Backend)
  Riesgos pendientes: [N]
  Falsos positivos: [N]

¿Qué deseas hacer con cada bug confirmado?
  A) Crear ticket → dime el ID del bug (ej. "crea ticket para BUG-BH-001")
  B) Documentar internamente → se queda en el reporte
  C) Descartar → se mueve a falsos positivos
```

El QA Engineer decide para cada bug:
- ✅ **Escalar a ticket** → El QA dice "crea ticket para BUG-BH-001" y el agente invoca `bug-reporter/create`
- 📝 **Documentar internamente** → Se queda en el reporte del bug hunt
- ❌ **Descartar** → Se mueve a falsos positivos

> **La skill NO invoca `bug-reporter/create` automáticamente.**
> Solo lo hace cuando el QA Engineer lo indica explícitamente para un bug específico.
> Al invocar `bug-reporter/create`, se pasa toda la evidencia ya recopilada (código, request, response).

---

## Stage 3 — REPORTING

### Paso 3.1 — Guardar artefactos

Una vez que el QA Engineer terminó de clasificar los bugs:

1. **`bug-hunt-<modulo>.md`** → `knowledge/releases/<version>/` (si hay versión)
   - O → `knowledge/L3-tickets/` (si es standalone)
2. Usar template `templates/bug-hunt-report.md`

### Paso 3.2 — Sugerir siguiente paso

```
🐛 BUG HUNT [Módulo] — COMPLETADO ✅

Artefactos:
  ✅ knowledge/releases/[version]/bug-hunt-[modulo].md
  ✅ [N] tickets creados vía bug-reporter/create

Siguientes pasos:
  - Bug Hunt de otro módulo → "Bug Hunt: [otro módulo]"
  - Regression matrix → "Generar regression matrix: v[X.Y.Z]"
  - Smoke matrix → "Generar smoke matrix: v[X.Y.Z]"
```

---

## Reglas de este Skill

1. **Protocolo de evidencia verificable** — Reglas 11-14 del `bug-reporter/create` aplican al 100%
2. **Todo código citado requiere grep hit** — Un bloque de código sin grep es una alucinación
3. **Cada evidencia etiquetada** — `[CONFIRMADA]`, `[INFERIDA]`, `[AUSENTE]`, `[RIESGO A VERIFICAR]`
4. **Hallazgos estáticos NUNCA son BUG CONFIRMADO** — Solo `[RIESGO A VERIFICAR]` hasta reproducir
5. **Backend testing es OBLIGATORIO** — La fase 2A no es opcional
6. **Vectores de ataque son ejemplos, NO lista cerrada** — Descubrir más según el código real
7. **Requests se PROPONEN al QA antes de ejecutar** — Excepto GETs de lectura
8. **Edge Cases Conocidos del L2** — Consultar para evitar falsos positivos
9. **El QA decide qué escalar a ticket** — No invocar `bug-reporter/create` automáticamente
10. **NUNCA hacer git push, commit, ni merge** — Solo operaciones de lectura
11. **NUNCA modificar skills, templates o artefactos existentes** — Solo invocar o referenciar
12. **Repos actualizados a DEVELOPMENT** — Obligatorio antes de analizar

---

## Checklist de cierre

- □ L1 completo cargado
- □ L2 del módulo cargado (incluyendo Edge Cases Conocidos)
- □ Repos actualizados a DEVELOPMENT
- □ Fase 1 completada: análisis estático con greps documentados
- □ Fase 2A completada: API attack vectors ejecutados (los aprobados por QA)
- □ Fase 2B completada o rechazada por el QA (opcional)
- □ Todos los hallazgos clasificados: CONFIRMADO / RIESGO / FALSO POSITIVO
- □ QA Engineer revisó la lista y decidió qué escalar
- □ Tickets creados vía `bug-reporter/create` (los que el QA aprobó)
- □ Reporte exportado con template `bug-hunt-report.md`
- □ Búsquedas realizadas documentadas (tabla de greps)
- □ **NINGÚN skill o template existente fue modificado**
