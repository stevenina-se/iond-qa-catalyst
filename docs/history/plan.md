# ionflow-qa-catalyst — Plan de Implementación

## ¿Qué es esto?

**ionflow-qa-catalyst** es un sistema de orquestación de QA potenciado por IA para el proyecto Ionflow.
Funciona como una **capa de inteligencia** que:

1. Mantiene una **base de conocimiento estructurada en 3 niveles** sobre el proyecto
2. Expone un **motor de skills** que los agentes de IA ejecutan para automatizar tareas de QA
3. Se integra con **ClickUp** (vía MCP) para obtener contexto de tickets
4. Orquesta la skill existente **`ionflow-playwright-creator`** del repo `../bot-test` para generar y ejecutar tests E2E
5. Aplica en ambos tracks del **Dual-Track Agile**: Discovery y Deployment

> El sistema NO es una app de software tradicional.
> Es un repositorio de conocimiento + instrucciones estructuradas que los agentes de IA leen y ejecutan como si fuera un "manual de operaciones de QA vivo".

---

## Regla Central del Sistema

```
"LA IA LEE EL NIVEL CORRECTO ANTES DE REALIZAR CADA TAREA"

- Skill de proyecto / priorización  → Lee L1
- Skill de módulo / test-docs       → Lee L1 + L2 del módulo
- Skill de ticket                   → Lee L1 + L2 del módulo + L3 del ticket
```

---

## Modelo de Orquestación: ¿Cómo trabajan los Skills?

> **IA principal delega → Sub-agentes ejecutan → Yo decido**

El sistema no ejecuta trabajo silencioso. Cada acción pasa por tres etapas controladas por el QA Engineer.

```
┌─────────────────────────────────────────────────────────┐
│                  CENTRO DE COMANDOS                     │
│           (SKILL.md activa el flujo correcto)           │
└───────────────────────┬─────────────────────────────────┘
                        │ despacha
                        ▼
          ┌─────────────────────────┐
          │   STAGE 1 — PLANNING    │
          │  Cada sub-agente reporta│
          │  su plan antes de actuar│
          │  ❌ No hay trabajo silent│
          └────────────┬────────────┘
                       │ aprobado por QA Engineer
                       ▼
          ┌─────────────────────────┐
          │   STAGE 2 — EXECUTION   │
          │  Puedo detener, redirigir│
          │  o modificar en cualquier│
          │  momento del proceso    │
          └────────────┬────────────┘
                       │ completado
                       ▼
          ┌─────────────────────────┐
          │   STAGE 3 — REPORTING   │
          │  Transcript completo    │
          │  guardado en L3-tickets │
          │  Auditable paso a paso  │
          └─────────────────────────┘
```

### Principios del modelo de orquestación

| Principio | Descripción |
|-----------|-------------|
| **Transparencia total** | Ningún sub-agente ejecuta trabajo sin reportar primero su plan |
| **Control humano** | El QA Engineer puede interrumpir, corregir o redirigir en cualquier Stage |
| **Trazabilidad** | Cada sesión genera un transcript completo auditável en `L3-tickets/` |
| **Delegación clara** | La IA principal (SKILL.md) solo despacha; los sub-skills son los que actúan |
| **No hay caja negra** | Todo lo que hace la IA es visible, explicado y loggeado |

---

## Flujo de Testing de un Ticket

> Cómo se ve una sesión completa de QA desde que llega el ticket hasta el veredicto final.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  FASE 1 — SESSION START
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ① Load Context     → Lee L1 (proyecto) + L2 (módulo afectado)
  ② Fetch Ticket     → ClickUp MCP extrae AC, descripción, decisiones
  ③ Load Test Data   → Inicializa L3-tickets/<id>/ con template

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  FASE 2 — PLANNING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ① Risk Triage      → skill: test-docs/prioritize
                       ¿Qué puede romper? ¿Qué es crítico?
  ② Test Plan        → skill: sprint-testing/plan
                       Lista ordenada de casos a ejecutar
  ③ Link Cases       → Casos vinculados a AC del ticket

  ⏸ QA Engineer revisa y aprueba el plan antes de continuar

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  FASE 3 — EXECUTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ① Smoke Tests      → Verificación rápida de que el feature existe
  ② UI Testing       → Happy path + edge cases + negativos
  ③ API Testing      → Validación de endpoints y contratos
  ④ DB Evidence      → Verificación de persistencia de datos
  ⑤ Evidence Log     → Screenshots / videos / responses guardados en L3

  ⏸ QA Engineer puede interrumpir, escalar o redirigir en cualquier punto

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  FASE 4 — REPORTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ① QA Report        → skill: sprint-testing/report
                       Veredicto: ✅ Approved / ❌ Rejected
  ② Bug Log          → Lista de defectos encontrados con evidencia
  ③ Comment          → (Futuro) Comentario en ClickUp con resumen
  ④ Transcript       → Sesión completa loggeada en L3-tickets/<id>/
```

### Reglas de la sesión

- **Una sesión = un ticket**: el contexto L3 se crea al inicio y se cierra al reportar
- **Veredicto siempre explícito**: el QA Engineer da el Approved / Rejected, nunca la IA sola
- **La IA puede sugerir el veredicto**, pero el humano firma
- **Los bugs son trazables**: cada bug incluye el paso del plan que lo generó y la evidencia

---

## Estructura de Directorios

```
ionflow-qa-catalyst/
├── README.md                          # Punto de entrada, overview del sistema
├── SKILL.md                           # Master Skill: orquestador principal de IA
├── idea.md                            # (existente) Concepto original
├── plan.md                            # (este archivo)
│
├── knowledge/                         # Base de conocimiento estructurada en 3 niveles
│   ├── README.md                      # Regla: "Lee el nivel correcto antes de actuar"
│   │
│   ├── L1-project/                    # NIVEL 1: ¿Cómo funciona el proyecto?
│   │   ├── README.md
│   │   ├── business-rules.md          # Reglas de negocio de Ionflow / e-commerce
│   │   ├── api-architecture.md        # Repos, endpoints, relaciones entre servicios
│   │   ├── test-priorities.md         # Qué es crítico, alto, medio, bajo
│   │   └── stack-overview.md          # Go, Vue 3, PHP 8.2, Playwright, NX
│   │
│   ├── L2-modules/                    # NIVEL 2: ¿Cómo funciona este módulo?
│   │   ├── README.md                  # Instrucciones para crear/actualizar módulos
│   │   ├── _template.md               # Template base para nuevos módulos
│   │   ├── auth/
│   │   │   └── module.md              # Módulo: Autenticación y usuarios
│   │   ├── flows/
│   │   │   └── module.md              # Módulo: Gestión de flows
│   │   ├── nodes/
│   │   │   └── module.md              # Módulo: Nodos (core del producto)
│   │   └── connectors/
│   │       └── module.md              # Módulo: App Connectors
│   │
│   └── L3-tickets/                    # NIVEL 3: ¿Qué estoy testeando ahora?
│       ├── README.md                  # Instrucciones de memoria por ticket
│       └── _template.md               # Template: per-ticket memory session
│
├── skills/                            # Motor de skills de IA
│   ├── README.md                      # Índice de skills y cuándo usarlos
│   │
│   ├── sprint-testing/                # SKILL: Sprint Testing
│   │   ├── plan.md                    # Genera plan de testing desde ticket/AC
│   │   ├── test.md                    # Ejecuta el plan de testing
│   │   └── report.md                  # Genera reporte de testing del sprint
│   │
│   ├── test-docs/                     # SKILL: Documentación de Testing
│   │   ├── prioritize.md              # Prioriza qué testear por riesgo
│   │   └── document.md                # Genera Test Matrix / QA Requirement List
│   │
│   ├── automation/                    # SKILL: Automatización E2E
│   │   ├── plan.md                    # Decide qué automatizar del Test Matrix
│   │   ├── code.md                    # Orquesta ionflow-playwright-creator (bot-test)
│   │   └── review.md                  # Revisa y valida tests generados por IA
│   │
│   └── regression/                    # SKILL: Regresión
│       ├── run.md                     # Ejecuta suite de regresión en bot-test
│       ├── analyze.md                 # Analiza resultados y clasifica fallas
│       └── decide.md                  # Emite veredicto: Go / Go con obs / No-Go
│
└── templates/                         # Templates reutilizables
    ├── test-matrix.md                 # QA Requirement List / Test Matrix
    ├── architecture-brief-qa.md       # Checklist QA para Architecture Brief
    ├── qa-report.md                   # Sprint QA Report
    └── ticket-memory.md               # Per-ticket memory session (L3)
```

---

## Mapa: Skills ↔ Dual-Track Agile

### Discovery Track

> En Discovery el foco de QA **no es ejecutar tests** — es garantizar que lo que se va a construir sea testeable, correcto y completo antes de que llegue a Deployment.

El QA Engineer en Discovery actúa como **analista crítico del prototipo y guardián de la calidad del diseño**.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  QA EN DISCOVERY — LAS 4 RESPONSABILIDADES CORE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  1. ANÁLISIS DE LÓGICA DE NEGOCIO
     └─ ¿El prototipo respeta las reglas del negocio?
     └─ ¿Los flujos del feature son coherentes con cómo funciona Ionflow?
     └─ ¿Hay conflictos con otros módulos existentes?

  2. INTERROGACIÓN DEL PROTOTIPO
     └─ ¿Qué pasa si el usuario hace X en lugar de Y?
     └─ ¿Qué pasa si el nodo falla a mitad de ejecución?
     └─ ¿Qué pasa en mobile / pantallas pequeñas?
     └─ ¿Qué pasa con datos vacíos, nulos o malformados?

  3. IDENTIFICACIÓN DE CASOS BORDE Y DE USO
     └─ Edge cases que el developer no consideró
     └─ Casos de uso reales que vienen del e-commerce
     └─ Flujos alternativos (no solo el happy path)
     └─ Casos de regresión que el feature puede afectar

  4. CONSOLIDACIÓN DE CRITERIOS DE ACEPTACIÓN
     └─ Validar que los AC del ticket sean verificables
     └─ Completar AC ambiguos con el PO o el Developer
     └─ Transformar AC en casos de test concretos
     └─ Construir la Test Matrix completa como output final

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### Skills del Catalyst en Discovery

| Paso Altacrest | Actividad QA | Skill del Catalyst | Output |
|---|---|---|---|
| Paso 5 — PO + Stakeholder + QA Review | Análisis de lógica de negocio + interrogación del prototipo | `test-docs/prioritize` | Lista de riesgos y preguntas abiertas |
| Paso 5 — (mismo) | Validación y consolidación de Acceptance Criteria | `test-docs/document` (modo AC) | AC verificables y completos en L3 |
| Paso 6 — QA Requirement List | Identificación de edge cases + casos de uso + regresión | `test-docs/document` (modo matrix) | Test Matrix completa en `templates/test-matrix.md` |
| Paso 7 — Architecture Brief | QA check del brief técnico (seguridad, logging, rollback) | `test-docs/document` + `templates/architecture-brief-qa.md` | Checklist QA del Architecture Brief |
| Paso 9 — Prototype Branch | Plan de testing para cuando llegue a Deployment | `sprint-testing/plan` | Test Plan guardado en L3 del ticket |

#### Flujo de un QA en una sesión de Discovery

```
Ticket entra a Discovery
        │
        ▼
① Leer ticket + cargar contexto L1+L2 (ClickUp MCP)
        │
        ▼
② Analizar el prototipo vibe-code del Developer
   → ¿La lógica de negocio es correcta?
   → ¿Hay flows del e-commerce que no se cubren?
        │
        ▼
③ Generar preguntas y riesgos
   skill: test-docs/prioritize
   → Lista de preguntas para el Developer / PO
   → Riesgos identificados por área
        │
        ▼
④ Consolidar Acceptance Criteria
   → Validar los AC existentes del ticket
   → Proponer AC faltantes con el equipo
   → Transformar cada AC en caso de test
        │
        ▼
⑤ Construir Test Matrix
   skill: test-docs/document
   → Happy path por cada AC
   → Edge cases identificados
   → Casos negativos
   → Casos de regresión impactados
        │
        ▼
⑥ Guardar en L3-tickets/<id>/
   → test-matrix.md (listo para Deployment)
   → ac-consolidated.md
   → risks-and-questions.md
```

#### Regla de oro del Discovery

> **"QA no aprueba un ticket para Deployment sin una Test Matrix completa y AC verificables."**
>
> Si el Developer no puede responder las preguntas del QA, el ticket NO pasa a Deployment.
> Esta es la principal forma en que QA previene defectos antes de que se construyan.

### Deployment Track

| Paso | Nombre | Skill del Catalyst |
|------|--------|--------------------|
| 3 | QA Collaboration | `sprint-testing/test` |
| 4 | Automated Test Completion | `automation/plan` → `automation/code` → `automation/review` |
| 7 | QA Regression Testing | `regression/run` + `regression/analyze` |
| 8 | Pilot / UAT | `sprint-testing/report` |
| 9 | Release Approval | `regression/decide` |

### Support Lane

| Paso | Nombre | Skill del Catalyst |
|------|--------|--------------------|
| Triage | QA Replication | `sprint-testing/test` (modo hotfix) |
| Fix | Feature Owner Analysis | `test-docs/prioritize` |
| Release | QA Validation | `regression/run` (scope reducido) |

---

## Descripción de Componentes

### SKILL.md — Master Orchestrator
El archivo principal que el agente de IA lee primero al activar cualquier skill. Contiene:
- Contexto global de Ionflow
- La regla de carga de niveles
- Índice de todos los skills disponibles y cuándo usarlos
- Instrucciones de integración con ClickUp MCP (modo lectura)
- Referencia al repo `bot-test` y cómo delegar la automatización E2E

---

### knowledge/L1-project/ — Nivel 1: Proyecto
Se llena una vez y se actualiza solo cuando cambia la arquitectura.

| Archivo | Contenido |
|---------|-----------|
| `business-rules.md` | Flujos de e-commerce que Ionflow automatiza, lógica core |
| `api-architecture.md` | Los 4 repos, responsabilidades, APIs y relaciones |
| `test-priorities.md` | Ranking de módulos por criticidad |
| `stack-overview.md` | Stack técnico completo con versiones y convenciones |

---

### knowledge/L2-modules/ — Nivel 2: Módulos

> Los 4 repositorios de Ionflow están clonados en `../` (un nivel arriba de este repo).
> Esto permite al Catalyst **leer el código fuente real** para construir y mantener el contexto de cada módulo con precisión.

---

#### Cómo se Puebla el Contexto de un Módulo

El proceso de context building es **semi-automatizado**: el agente lee los repos y extrae lo que puede, y el QA Engineer valida y enriquece con conocimiento de dominio que no está en el código.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PROCESO DE CONTEXT BUILDING POR MÓDULO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

① ACTIVACIÓN
   QA Engineer: "Construye el contexto del módulo: flows"
   Catalyst carga L1-project como base de referencia

② EXTRACCIÓN DESDE REPOS (el agente lee los repos)
   → Lee ../gateway-ion        (Frontend: rutas y UI)
   → Lee ../flow_binaries      (API: endpoints y lógica)
   → Lee ../webcomponents-flow (Canvas: componentes)
   → Lee ../gateway            (Legacy: auth y flows)
   → Lee ../bot-test           (Tests existentes)

③ DRAFT DEL MODULE.MD
   El agente genera un borrador estructurado con todo
   lo que encontró en el código

④ REVISIÓN HUMANA (QA Engineer enriquece)
   → Añade reglas de negocio que no están en el código
   → Corrige interpretaciones incorrectas
   → Agrega edge cases conocidos por experiencia
   → Agrega test data conocido

⑤ VALIDACIÓN CON BD (Modo A - DBeaver)
   → Catalyst genera queries para explorar el schema
   → QA Engineer las ejecuta y pega el resultado
   → Se documenta el schema real de las tablas del módulo

⑥ MODULE.MD FINALIZADO
   Guardado en knowledge/L2-modules/<modulo>/module.md
   Listo para ser usado por cualquier skill

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

#### Qué Leer en Cada Repo y Qué Extraer

**`../gateway-ion` — Frontend Vue 3**

| Archivos a leer | Qué se extrae |
|-----------------|---------------|
| `src/router/index.ts` o `routes/` | Rutas de la app, nombres de vistas, guards de navegación |
| `src/views/<modulo>/` | Nombres de vistas, estructura de pantallas |
| `src/components/<modulo>/` | Componentes reutilizables, props, eventos |
| `src/services/` o `src/api/` | Llamadas a API: endpoints, métodos, payloads |
| `src/stores/` (Pinia) | Estado global, qué datos maneja el módulo |

---

**`../flow_binaries` — Core en Go**

| Archivos a leer | Qué se extrae |
|-----------------|---------------|
| `routes.go` / `router.go` / `main.go` | Endpoints registrados, métodos HTTP, grupos de rutas |
| `handlers/<modulo>/` | Lógica de negocio, validaciones, respuestas |
| `models/` o `entities/` | Structs de datos, campos, tipos |
| `migrations/` | Schema de BD: tablas, columnas, índices, constraints |
| `middleware/` | Validaciones globales, autenticación requerida |

---

**`../webcomponents-flow` — Web Components Vue 3**

| Archivos a leer | Qué se extrae |
|-----------------|---------------|
| `src/components/` | Componentes del canvas: Node, Edge, Drawer, etc. |
| Archivos de definición de props | Props públicas, eventos emitidos, slots |
| `src/composables/` | Lógica compartida entre componentes |
| Archivos de build/export | Qué se expone via CDN y con qué nombre |

---

**`../gateway` — Backend PHP 8.2 (Legacy)**

| Archivos a leer | Qué se extrae |
|-----------------|---------------|
| `routes/` o `api.php` | Endpoints de auth y flows legacy |
| `app/Http/Controllers/` | Lógica de usuarios, sessions, permisos |
| `app/Models/` | Modelos Eloquent: tablas y relaciones |
| `database/migrations/` | Schema de BD legacy |

---

**`../bot-test` — E2E Playwright NX**

| Archivos a leer | Qué se extrae |
|-----------------|---------------|
| `apps/bot-test/tests/IONFLOW/<modulo>/` | Tests E2E existentes del módulo |
| `apps/bot-test/tests/IONFLOW/pages/` | Page Objects y selectores ya mapeados |
| `apps/bot-test/tests/IONFLOW/utils/` | Helpers y datos de test compartidos |

---

#### Schema de BD: Estrategia sin Acceso Directo

Dado que la BD requiere SSH tunnel, el schema se obtiene de **dos fuentes complementarias**:

```
FUENTE 1 — Archivos de migración en los repos (automático)
  ../flow_binaries/migrations/*.sql   → Schema del core Go
  ../gateway/database/migrations/     → Schema legacy PHP
  El agente lee estas migraciones y reconstruye el schema

FUENTE 2 — Queries de exploración en DBeaver (manual, primer setup)
  Catalyst genera estas queries → QA las ejecuta en DBeaver:

  -- Listar todas las tablas del módulo
  SELECT table_name, obj_description(oid)
  FROM information_schema.tables t
  JOIN pg_class c ON c.relname = t.table_name
  WHERE table_schema = 'public'
  ORDER BY table_name;

  -- Ver columnas de una tabla específica
  SELECT column_name, data_type, is_nullable, column_default
  FROM information_schema.columns
  WHERE table_name = '<tabla>'
  ORDER BY ordinal_position;

  -- Ver relaciones (foreign keys)
  SELECT tc.table_name, kcu.column_name, ccu.table_name AS foreign_table
  FROM information_schema.table_constraints AS tc
  JOIN information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name
  JOIN information_schema.constraint_column_usage AS ccu ON ccu.constraint_name = tc.constraint_name
  WHERE tc.constraint_type = 'FOREIGN KEY';
```

El resultado de estas queries se guarda en `module.md` en la sección `## Database`.

---

#### Fuentes de contexto por repositorio (resumen)

| Repo | Qué aporta al L2 |
|------|------------------|
| `../flow_binaries` | Endpoints de API, lógica de nodos, motor de flows, structs, migraciones Go |
| `../gateway-ion` | Rutas de vistas, selectores de UI, nombres de componentes, calls a API |
| `../webcomponents-flow` | Componentes del canvas de nodos, eventos, props expuestos via CDN |
| `../gateway` | Auth, gestión de usuarios, lógica flows legacy, migraciones PHP |
| `../bot-test` | Tests E2E existentes, page objects, helpers, test data |

#### Contenido final de cada `module.md`
- **Rutas del frontend** con nombres de vistas y componentes
- **Endpoints de API** con métodos, paths y payloads
- **Componentes del canvas** relevantes para el módulo
- **Schema de BD**: tablas, columnas clave, relaciones
- **Test data** compartido y cómo conseguirlo
- **Edge cases** conocidos (se enriquece con cada release)
- **Tests E2E existentes** en `bot-test` con sus rutas
- **Queries de verificación frecuentes** (reutilizables)
- **Historial de cambios post-release** (retroalimentación continua)

---



### knowledge/L3-tickets/ — Nivel 3: Ticket Memory

> **Decisión confirmada**: Los archivos de L3 se comprometen al repo. El reporte es para la empresa y puede contener datos sensibles (resultados de queries, evidencia de testing).

Un archivo por ticket activo (nombrado con el ID de ClickUp). Contiene:
- ID y título del ticket
- Acceptance Criteria (manual hasta configurar MCP, automático después)
- Decisiones del equipo
- Plan de testing activo
- Evidencia de testing (links a screenshots/videos, resultados de queries DB)
- Bugs encontrados en sesión
- Veredicto final: Approved / Rejected (usando template del equipo)
- Transcript de la sesión

---

### skills/test-docs/ — Discovery Track
- **`prioritize.md`**: Analiza el ticket + Architecture Brief + L1/L2 y genera lista priorizada por riesgo de qué testear
- **`document.md`**: Genera Test Matrix completo con happy path, edge cases, negativos, y casos de regresión. Output → `L3-tickets/<ticket-id>/test-matrix.md`

---

### skills/sprint-testing/ — Discovery + Deployment
- **`plan.md`**: Con contexto L1+L2+L3, genera el plan de sesión de testing
- **`test.md`**: Guía al QA Engineer en ejecutar el plan y registrar evidencia en L3
- **`report.md`**: Consolida L3 del ticket en reporte estructurado para Release Manager

---

### skills/automation/ — Deployment Track (Paso 4)
- **`plan.md`**: Decide qué casos del Test Matrix se deben automatizar (repetibles, estables, críticos)
- **`code.md`**: **Orquesta `ionflow-playwright-creator` de `../bot-test`**. Provee contexto L2 del módulo + L3 del ticket para que la skill de bot-test genere los tests correctamente
- **`review.md`**: Checklist de revisión: cobertura, selectores, assertions, estabilidad, no-flakiness

---

### skills/regression/ — Deployment Track (Pasos 7–9)
- **`run.md`**: Ejecuta la suite vía `npx nx run bot-test:test:ionflow`
- **`analyze.md`**: Clasifica fallas: nuevo bug / regresión / test flaky / ambiental
- **`decide.md`**: Emite veredicto: ✅ Go / ⚠️ Go con observaciones / 🚫 No-Go con justificación

---

## Integración con ClickUp MCP

**Estado actual**: 🔧 Por configurar — el MCP no está conectado aún. Se integrará en Fase 6 (validación).

**No es bloqueante para Fases 1–5.** Durante esas fases, el QA Engineer proveerá el contexto del ticket manualmente (pegando AC y descripción en L3).

**Cuando se configure**, el flujo será:
1. QA Engineer activa un skill con el ID del ticket de ClickUp
2. `SKILL.md` lee el ticket vía MCP → extrae AC, descripción, decisiones, adjuntos
3. Popula automáticamente el template de `L3-tickets/<ticket-id>/` con esa información
4. Continúa la ejecución del skill correspondiente

> ⚠️ No se realizarán comentarios ni modificaciones en ClickUp sin autorización explícita del equipo.

---

## Integración con Base de Datos (PostgreSQL vía SSH)

> La base de datos de Ionflow está en PostgreSQL y el acceso se realiza a través de un **túnel SSH** (actualmente gestionado con DBeaver). El Catalyst debe ser capaz de incorporar evidencia de BD en el flujo de testing.

### El desafío

```
QA Catalyst (local)  →  SSH Tunnel  →  Servidor remoto  →  PostgreSQL
                         (DBeaver hoy)
```

El Catalyst no puede conectarse directamente a la BD. Necesita un mecanismo para:
1. **Generar las queries** necesarias para verificar el estado de la BD
2. **Obtener los resultados** de esas queries como evidencia de testing

### Estrategia: Dos Modos de Acceso

---

#### Modo A — Guided Query (Corto Plazo / Inmediato)
> La IA genera la query, el QA Engineer la ejecuta en DBeaver y pega el resultado.

```
① skill: sprint-testing/test detecta un paso de DB Evidence
② Catalyst genera la SQL query exacta con contexto del módulo (L2)
   Ejemplo: SELECT * FROM flows WHERE id = '<ticket-flow-id>'
③ QA Engineer abre DBeaver → ejecuta la query en la conexión SSH existente
④ Pega el resultado en la sesión del L3-ticket
⑤ Catalyst analiza el resultado y registra la evidencia
```

**Ventajas**: Cero configuración adicional, funciona desde el día 1.
**Limitación**: Requiere intervención manual del QA Engineer en cada paso de BD.

---

#### Modo B — Direct SSH Tunnel (Mediano Plazo / Automatizado)
> El Catalyst abre un túnel SSH directamente y ejecuta queries sin DBeaver.

```
① Catalyst lee configuración SSH desde .env (NO del repo)
② Abre túnel SSH: ssh -L 5433:localhost:5432 <ssh-host>
③ Ejecuta psql o query via el puerto tunelizado
④ Captura el resultado → lo guarda en L3-ticket como evidencia
⑤ Cierra el túnel
```

**Ventajas**: Totalmente automatizable, sin intervención humana para queries de verificación.
**Requisito**: Configurar `.env` con credenciales SSH y de BD.

---

### Configuración de Seguridad (aplica a ambos modos)

> ⚠️ **Las credenciales NUNCA se almacenan en el repositorio.**

Se usará un archivo `.env` en la raíz del catalyst (ignorado por `.gitignore`):

```bash
# .env (NO subir al repo)
DB_SSH_HOST=<ip-o-hostname-del-servidor>
DB_SSH_USER=<usuario-ssh>
DB_SSH_KEY_PATH=~/.ssh/ionflow_key
DB_SSH_PORT=22
DB_LOCAL_PORT=5433          # puerto local del túnel
DB_HOST=localhost
DB_PORT=5432
DB_NAME=<nombre-de-la-bd>
DB_USER=<usuario-postgres>
DB_PASSWORD=<password>
```

El L2 de cada módulo documentará **qué tablas y schemas** son relevantes, pero **nunca datos de conexión**.

---

### Enfoque Confirmado — DB Evidence

> **Estrategia confirmada**: El Catalyst reconstruye el schema desde los archivos de migración y genera las queries de verificación. El QA Engineer las ejecuta en DBeaver y pega la evidencia.

```
FASE 3 — EXECUTION
  ...
  ③ DB Evidence
     ┌─────────────────────────────────────────────┐
     │  1. Catalyst lee migrations del repo fuente │
     │     (flow_binaries/migrations/ o            │
     │      gateway/database/migrations/)          │
     │  2. Reconstruye el schema de la tabla       │
     │  3. Genera las queries de verificación:     │
     │     • Verificar creación de registro        │
     │     • Verificar cambios de estado           │
     │     • Verificar integridad referencial      │
     │     • Verificar que no hay datos huérfanos  │
     │  4. QA Engineer ejecuta en DBeaver          │
     │  5. Pega el resultado en la sesión          │
     └──────────────┬──────────────────────────────┘
                    ▼
     Resultado guardado en L3-tickets/<id>/db-evidence.md
```

### Lo que el L2 de cada módulo documenta sobre la BD

Cada `module.md` incluye una sección `## Database` con:
- Schema reconstruido desde archivos de migración
- Tablas principales y columnas clave con tipos
- Relaciones (foreign keys) entre tablas
- Queries de verificación frecuentes (reutilizables por ticket)
- Estados y transiciones de datos esperados

> El `.env` con credenciales de BD **nunca se sube al repo** (ignorado por `.gitignore`).
> El Catalyst solo necesita leer las migraciones del código fuente — no acceso directo a la BD.

---



## Fases de Implementación

### Fase 1 — Estructura Base y Conocimiento del Proyecto
- [ ] Crear estructura de directorios completa
- [ ] `.gitignore` (ignorar `.env`, `L3-tickets/*/` con evidencia sensible si aplica)
- [ ] `.env.sample` (template de variables de entorno sin valores reales)
- [ ] `README.md` del repositorio con punto de entrada para el QA Engineer
- [ ] `SKILL.md` maestro (orquestador) con instrucciones de activación
- [ ] `knowledge/README.md` con la regla de niveles
- [ ] `knowledge/L1-project/` completo con contexto inicial de Ionflow
- [ ] `knowledge/L2-modules/_template.md` y `knowledge/L3-tickets/_template.md`

### Fase 2 — Skills Core (Discovery Track)
- [ ] `skills/test-docs/prioritize.md`
- [ ] `skills/test-docs/document.md`
- [ ] `skills/sprint-testing/plan.md`
- [ ] `templates/test-matrix.md`
- [ ] `templates/architecture-brief-qa.md`
- [ ] `templates/ticket-memory.md`
- [ ] `templates/approval.md` — *(template del equipo: a compartir por el QA Engineer)*
- [ ] `templates/rejection.md` — *(template del equipo: a compartir por el QA Engineer)*
- [ ] `templates/comment.md` — template para comentarios estructurados en tickets

### Fase 3 — Skills de Ejecución (Deployment Track)
- [ ] `skills/sprint-testing/test.md`
- [ ] `skills/sprint-testing/report.md`
- [ ] `templates/qa-report.md`

### Fase 4 — Automation y Regression
- [ ] `skills/automation/plan.md`
- [ ] `skills/automation/code.md` (puente a bot-test)
- [ ] `skills/automation/review.md`
- [ ] `skills/regression/run.md`
- [ ] `skills/regression/analyze.md`
- [ ] `skills/regression/decide.md`

### Fase 5 — Knowledge Base por Módulos (Context Building desde los repos)
- [ ] Leer migraciones de `../flow_binaries` → reconstruir schema de BD por módulo
- [ ] Leer migraciones de `../gateway` → schema legacy
- [ ] Leer `../flow_binaries` → mapear endpoints y estructuras por módulo
- [ ] Leer `../gateway-ion/src` → mapear rutas, vistas y componentes por módulo
- [ ] Leer `../webcomponents-flow` → mapear componentes del canvas y sus eventos
- [ ] Leer `../gateway` → mapear endpoints legacy de auth y flows
- [ ] Leer `../bot-test` → mapear tests E2E existentes por módulo
- [ ] `knowledge/L2-modules/auth/module.md` (construido desde repos)
- [ ] `knowledge/L2-modules/flows/module.md` (construido desde repos)
- [ ] `knowledge/L2-modules/nodes/module.md` (construido desde repos)
- [ ] `knowledge/L2-modules/connectors/module.md` (construido desde repos)
- [ ] `skills/knowledge/update-module.md` (skill de retroalimentación post-release)

### Fase 6 — Validación
- [ ] Ejecutar flujo completo con un ticket real de ClickUp
- [ ] Validar integración con `ionflow-playwright-creator`
- [ ] Ajustar skills según feedback del equipo

---

## Repositorios Disponibles como Fuentes de Conocimiento

Todos los repos de Ionflow están clonados en `../` (mismo nivel que este directorio).
El Catalyst los usa **solo en modo lectura** para construir y actualizar el L2.

```
Automation/
├── ionflow-qa-catalyst/   ← este repo (el Catalyst)
├── flow_binaries/          ← Go: core de nodos y motor de ejecución
├── gateway-ion/            ← Vue 3 TS: frontend y CRUDs
├── webcomponents-flow/     ← Vue 3 TS: canvas de nodos (CDN)
├── gateway/                ← PHP 8.2: auth y flows legacy
└── bot-test/               ← Playwright NX: E2E automation
```

| Repo | Stack | Rol en el Catalyst |
|------|-------|--------------------|
| `../flow_binaries` | Go | Fuente de APIs, lógica de negocio, estructuras de nodos |
| `../gateway-ion` | Vue 3 + TS | Fuente de rutas, selectores UI, nombres de componentes |
| `../webcomponents-flow` | Vue 3 + TS | Fuente de componentes del canvas y sus interfaces |
| `../gateway` | PHP 8.2 | Fuente de auth y lógica legacy |
| `../bot-test` | Playwright + NX | Fuente de tests E2E existentes y skill de automatización |
| ClickUp MCP | API | Fuente de tickets, AC y decisiones del equipo |

---

## Ciclo de Vida del Conocimiento de Módulos

> El L2 no es estático — se construye una vez y se retroalimenta después de cada release o improvement.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  FASE INICIAL — Context Building
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ① Leer repos fuente (../flow_binaries, ../gateway-ion, etc.)
  ② Extraer: rutas, endpoints, componentes, tablas, test data
  ③ Crear knowledge/L2-modules/<modulo>/module.md
  ④ Validar con el equipo que el contexto sea correcto

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DESPUÉS DE CADA RELEASE O IMPROVEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ① El QA Engineer activa el skill: knowledge/update-module
  ② El Catalyst diff los cambios en el repo fuente vs el L2 actual
  ③ Propone actualizaciones al module.md del módulo afectado
  ④ QA Engineer aprueba los cambios → L2 queda actualizado
  ⑤ Los bugs encontrados en la release se agregan como
     edge cases conocidos en el módulo
  ⑥ Los nuevos tests E2E creados en bot-test se referencian
     en el L2 del módulo correspondiente

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Regla del ciclo de vida

> **"El L2 de un módulo debe reflejar siempre lo que está en producción, no lo que fue planeado."**
>
> Después de cada release: si el feature cambió algo en el módulo → el module.md se actualiza.
> Si se encontró un bug → se agrega como edge case conocido.
> Si se creó un test E2E nuevo → se referencia en el L2.

---

*Este plan es un documento vivo. Se actualiza conforme avanzan las fases.*