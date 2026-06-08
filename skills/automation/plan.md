# Skill: automation/plan

> Analiza la test-matrix de un ticket y decide qué test cases son candidatos para automatización E2E con Playwright. Solo considera tests de UI de gateway-ion (no webcomponents/canvas).

## Cuándo usar este skill

- **Deployment Track**: Después de completar el testing manual de un ticket, para automatizar los TCs validados
- **Post-release**: Para consolidar tests que se repetirán en regresión

## Pre-requisitos

- ✅ `knowledge/L2-modules/<módulo>/module.md` — Para conocer rutas, componentes y selectores
- ✅ `L3-tickets/<ticket-id>/test-matrix.md` — Para evaluar qué TCs automatizar
- ✅ `L3-tickets/<ticket-id>/qa-report.md` — Para saber cuáles pasaron (solo automatizamos lo validado)

---

## Instrucciones de Ejecución

### Stage 1 — PLANNING

Reporta al QA Engineer:
1. El ticket y módulo que vas a evaluar
2. Cuántos TCs tiene la test-matrix
3. Tu estimación inicial de cuántos son automatizables

**Espera aprobación antes de continuar.**

### Stage 2 — EXECUTION

#### Paso 1: Clasificar cada TC por automatizabilidad

Para cada test case de la matrix, evalúa:

| TC-ID | Tipo | Automatizable | Razón | Complejidad |
|-------|------|---------------|-------|-------------|
| TC-001 | Happy Path | ✅ Sí | UI de gateway-ion, flujo CRUD estándar | 🟢 Baja |
| TC-002 | Edge Case | ✅ Sí | Validación de formulario, selectores accesibles | 🟡 Media |
| TC-003 | Happy Path | ❌ No | Involucra canvas de webcomponents-flow | — |
| TC-004 | Negativo | ✅ Sí | Verificar mensaje de error en UI | 🟢 Baja |
| TC-005 | DB Evidence | ❌ No | Requiere DBeaver (SSH tunnel) | — |

#### Criterios de automatizabilidad

| Criterio | Automatizable | No automatizable |
|----------|--------------|------------------|
| **Repo involucrado** | `gateway-ion` (UI Vue) | `webcomponents-flow` (canvas) |
| **Tipo de interacción** | Clicks, formularios, navegación, listas | Drag & drop de nodos, canvas interactions |
| **Datos** | Datos predecibles o seedeables | Datos externos (APIs de terceros) |
| **Verificación** | Texto en pantalla, URLs, elementos DOM | Screenshots pixel-perfect, animaciones |
| **API** | Requests HTTP directos | Webhooks entrantes (requieren setup externo) |
| **BD** | No requiere verificación de BD | Requiere DBeaver (SSH tunnel) |

#### Paso 2: Priorizar los candidatos

Ordena los TCs automatizables por valor:

| Prioridad | Criterio |
|-----------|----------|
| 🔴 Alta | Happy paths de features core que se repetirán en regresión |
| 🟠 Media | Edge cases frecuentes que ahorran tiempo de testing manual |
| 🟡 Baja | Negativos simples (validaciones de formulario) |

#### Paso 3: Verificar selectores disponibles

Lee `knowledge/L2-modules/<módulo>/module.md` y el código de `../gateway-ion/src/` para verificar:
- ¿Los componentes tienen `data-testid` o selectores estables?
- ¿Existen page objects en `../bot-test/tests/IONFLOW/pages/` para este módulo?
- ¿Hay helpers reutilizables en `../bot-test/tests/IONFLOW/utils/`?

#### Paso 4: Generar el plan de automatización

```
PLAN DE AUTOMATIZACIÓN — [TICKET-ID]

Módulo: [nombre]
Total TCs en matrix: [N]
TCs automatizables: [N] ([%])
TCs NO automatizables: [N] (razón principal: [canvas/BD/externo])

CANDIDATOS PRIORIZADOS:
  🔴 Alta prioridad:
    - TC-001: [descripción] — Complejidad: 🟢
    - TC-004: [descripción] — Complejidad: 🟢
  
  🟠 Media prioridad:
    - TC-002: [descripción] — Complejidad: 🟡
  
  🟡 Baja prioridad:
    - (opcionales)

RECURSOS EXISTENTES:
  - Page Objects disponibles: [lista o "ninguno - crear nuevos"]
  - Helpers disponibles: [lista]

ESTIMACIÓN:
  - Tests a crear: [N] archivos .spec.ts
  - Destino: ../bot-test/apps/bot-test/tests/IONFLOW/tickets/[TICKET-ID]/
  - Tiempo estimado de generación: ~[X] min
```

### Stage 3 — REPORTING

Guarda el output en `L3-tickets/<ticket-id>/automation-plan.md`.

El QA Engineer revisa y aprueba qué TCs automatizar antes de pasar a `automation/code`.

---

## Reglas de este Skill

1. **Solo automatizar gateway-ion UI** — Canvas (webcomponents-flow) queda excluido
2. **Solo automatizar TCs ya validados manualmente** — No automatizar lo que no se ha testeado
3. **Priorizar por valor de regresión** — ¿Se repetirá este test en cada sprint?
4. **Verificar selectores antes de comprometerse** — Sin selectores estables no hay test confiable
5. **El QA Engineer decide qué automatizar** — El plan es una sugerencia
