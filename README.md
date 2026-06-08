# ionflow-qa-catalyst

> Sistema de orquestación de QA potenciado por IA para el proyecto Ionflow.

## ¿Qué es esto?

**ionflow-qa-catalyst** es una capa de inteligencia que automatiza el proceso de QA del proyecto Ionflow. No es una app de software tradicional — es un repositorio de **conocimiento estructurado + instrucciones para agentes de IA** que funciona como un manual de operaciones de QA vivo.

### Lo que hace:
1. Mantiene una **base de conocimiento en 3 niveles** sobre el proyecto
2. Expone un **motor de skills** que los agentes de IA ejecutan para automatizar tareas de QA
3. Se integra con **ClickUp** (vía MCP) para obtener contexto de tickets
4. Orquesta la skill **`ionflow-playwright-creator`** del repo `../bot-test` para E2E
5. Aplica en ambos tracks del **Dual-Track Agile**: Discovery y Deployment

---

## Quick Start

### 1. Activar el Catalyst
El punto de entrada principal es **`SKILL.md`**. Todo agente de IA debe leer este archivo primero.

### 2. Entender los niveles de conocimiento
```
L1-project  → ¿Cómo funciona el proyecto?     (leer siempre)
L2-modules  → ¿Cómo funciona este módulo?      (leer según el módulo afectado)
L3-tickets  → ¿Qué estoy testeando ahora?      (leer/crear por ticket activo)
```

### 3. Usar un skill
Los skills están en `skills/`. Cada uno es una instrucción que el agente de IA sigue para ejecutar una tarea de QA.

```
skills/
├── sprint-testing/   → plan, test, report
├── test-docs/        → prioritize, document
├── automation/       → plan, code, review
└── regression/       → run, analyze, decide
```

---

## Regla Central

```
"LA IA LEE EL NIVEL CORRECTO ANTES DE REALIZAR CADA TAREA"
```

- Skill de proyecto → Lee L1
- Skill de módulo → Lee L1 + L2 del módulo
- Skill de ticket → Lee L1 + L2 del módulo + L3 del ticket

---

## Modelo de Orquestación

```
IA principal delega → Sub-agentes ejecutan → QA Engineer decide
```

Cada skill pasa por 3 stages:
1. **Planning** — El agente reporta su plan antes de actuar (no hay trabajo silencioso)
2. **Execution** — El QA Engineer puede detener, redirigir o modificar en cualquier momento
3. **Reporting** — Transcript completo guardado en L3-tickets, auditable paso a paso

---

## Estructura del Repositorio

```
ionflow-qa-catalyst/
├── SKILL.md                  # Punto de entrada para agentes de IA
├── README.md                 # Este archivo
├── idea.md                   # Concepto original
├── plan.md                   # Plan de implementación detallado
│
├── knowledge/                # Base de conocimiento (3 niveles)
│   ├── L1-project/           # Nivel 1: Proyecto
│   ├── L2-modules/           # Nivel 2: Módulos
│   └── L3-tickets/           # Nivel 3: Tickets activos
│
├── skills/                   # Motor de skills de IA
│   ├── sprint-testing/
│   ├── test-docs/
│   ├── automation/
│   └── regression/
│
└── templates/                # Templates reutilizables
```

---

## Repositorios del Ecosistema

```
Automation/
├── ionflow-qa-catalyst/   ← este repo
├── flow_binaries/          ← Go: core de nodos y motor
├── gateway-ion/            ← Vue 3: frontend
├── webcomponents-flow/     ← Vue 3: canvas de nodos
├── gateway/                ← PHP 8.2: auth y legacy
└── bot-test/               ← Playwright: E2E automation
```

---

## Setup

1. Clonar este repo en `Automation/` junto con los demás repos de Ionflow
2. Copiar `.env.sample` a `.env` y rellenar las credenciales de BD (solo si usas verificación DB)
3. Leer `SKILL.md` para activar el Catalyst

---

## Documentación

- [Plan de implementación](plan.md) — Diseño completo del sistema
- [Idea original](idea.md) — Concepto y visión del proyecto
- [Knowledge README](knowledge/README.md) — Reglas de los niveles de conocimiento
