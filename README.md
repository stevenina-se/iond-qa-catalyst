# iond-qa-catalyst

> Sistema de QA asistido por IA para IOND, alineado al **SDLC IOND** (tableros Discovery, Improvements y Releases en ClickUp).

## Qué es

Un repositorio de **conocimiento estructurado + instrucciones para agentes de IA** (skills) que acompaña al equipo en el SDLC:

1. **QA como Analista de Calidad y Requerimientos:** Matriz de Requerimientos en `requirements`, Matriz de Pruebas con REQ-ID, ejecución con evidencia, reporte y comentarios C-13/C-14.
2. **Release semanal:** plan del corte (T-04), smoke maestro, sanity de la versión, regresión por riesgo (capa 1), E2E maestro (capa 2), Go/No-Go, release notes y protocolo de despliegue.
3. **Gobierno del flujo** para el Scrum Master: auditoría de cumplimiento y métricas semanales.
4. **Automatización:** priorización y paquetes para el repositorio de pruebas E2E (`../bot-test`), sin modificarlo.

ClickUp es la fuente oficial y se lee en **solo lectura**: el catalyst prepara, las personas deciden y publican.

## Inicio rápido

1. Leer **[`SKILL.md`](SKILL.md)**: reglas, gates y enrutamiento por tablero y estado.
2. Fuente canónica del proceso: [`knowledge/L1-project/sdlc-consolidation.md`](knowledge/L1-project/sdlc-consolidation.md).
3. Suites del release: [`knowledge/test-suites/README.md`](knowledge/test-suites/README.md).
4. En Claude Code, las skills aparecen como `iond-*` (`.claude/skills/`).

## Estructura

```
iond-qa-catalyst/
├── SKILL.md                     Orquestador (leer primero)
├── skills/                      Skills por estado, release, suites, automatización y gobierno
│   └── _shared/                 Contratos: ClickUp, bot-test, evidencia, artefactos
├── .claude/skills/iond-*/       Accesos para Claude Code
├── templates/                   Plantillas de matrices, reportes, release y comentarios C-xx
├── knowledge/
│   ├── L1-project/              Proyecto + fuente canónica del SDLC
│   ├── L2-modules/              Conocimiento por módulo
│   ├── L3-tickets/              Memoria por ticket
│   ├── test-suites/             Smoke maestro, E2E maestro, cobertura, hoja de ruta de automatización
│   ├── releases/<producto>/<v>/ Artefactos de cada release
│   └── dashboards/              Auditorías y métricas
├── scripts/e2e_master.py        Importación, cobertura y selección del E2E maestro
├── docs/sdlc-iond/              Documentos del SDLC (Markdown → PDF) y su build
├── docs/history/                Material del proceso anterior (idea, plan, skills y templates retirados)
└── resources/                   CSV de referencia (SDLC por tablero y hoja del E2E maestro)
```

## Repositorios del ecosistema

```
Automation/
├── ionflow-qa-catalyst/   ← este repositorio
├── flow_binaries/         ← Go: motor y APIs
├── gateway-ion/           ← Vue 3: frontend
├── webcomponents-flow/    ← Vue 3: canvas de nodos
├── gateway/               ← PHP 8.2: auth y legacy
└── bot-test/              ← Playwright: pruebas E2E (solo lectura y ejecución desde el catalyst)
```

## Configuración

1. Clonar este repositorio en `Automation/` junto a los demás.
2. Copiar `.env.sample` a `.env` y completar las variables necesarias (nunca subir `.env` ni los perfiles `.env.<ambiente>`).
3. Configurar el MCP de ClickUp en modo lectura y, para testing asistido, el MCP de Playwright.
4. Python 3 para `scripts/e2e_master.py` y los generadores de `docs/sdlc-iond/_build/`.

## Documentación

- [Documentos del SDLC IOND](docs/sdlc-iond/README.md) — acuerdo de trabajo, estándar de QA, guías de ClickUp, métricas y registro de decisiones.
- [Knowledge README](knowledge/README.md) — niveles de conocimiento.
- [Historial](docs/history/) — idea y plan originales, skills y templates del proceso anterior.
