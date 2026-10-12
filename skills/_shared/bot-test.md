# Contrato compartido: bot-test (automatización E2E)

> El catalyst **lee y ejecuta** bot-test; **no modifica su código** (`Q-54`). El código de los tests lo escribe su responsable con la skill del propio repositorio: `../bot-test/.agents/skills/e2e-playwright-creator/SKILL.md`.

## Ubicación y estructura

```
../bot-test/apps/bot-test/tests/IONFLOW/
├── playwright.ionflow.config.ts   ← config de IONFLOW (1 worker, baseURL = IONFLOW_ENVIRONMENT_URL)
├── Admin-ION/<dominio>/            ← spec + page object + .md por dominio
├── Company-ION/<módulo>/           ← idem (boards, pdf-templates, persistent-data, nodes/<nodo>, …)
├── shared/                         ← BasePage, login, sidebars, user menu
├── utils/                          ← generadores autobot-*, mocks, scheduler
└── data/ · documents/ · images/ · models/
```

- **IDs de test** en el título: `[TC-<MÓDULO>-<GRUPO>-NN]` (por ejemplo `[TC-BOARD-CRUD-01]`). Las specs anteriores usan títulos de `describe`.
- **Tags** por test: `@ionflow`, lado (`@company`/`@admin`), módulo, prioridad (`@critical/@high/@medium/@low`) y tipo (`@hp`, `@negative`, `@edge`, `@bug`, `@mock`, `@ai`, `@canvas`, `@slow`, `@blocked`). Todavía **no** existen `@smoke` ni `@prod-safe` (Ola 0 de `knowledge/test-suites/automation-roadmap.md`).
- **Datos:** prefijo `autobot-` + timestamp; cada suite limpia lo que crea en `afterAll`.

## Cómo se ejecuta una suite

1. Generar la selección y el comando con `python -I scripts/e2e_master.py select …` (ver `knowledge/test-suites/README.md`). El comando filtra por IDs con `-g`.
2. Cargar el **perfil del ambiente** (`.env.preprod` o `.env.prod-testco`, fuera de los repositorios). La config usa `dotenv` sin sobrescribir variables ya definidas, así que el perfil manda.
3. Ejecutar desde `../bot-test/apps/bot-test`:
   ```bash
   npx playwright test <specs> --config=tests/IONFLOW/playwright.ionflow.config.ts --project=ionflow-chromium -g "<IDs>"
   ```
4. Leer el resultado en `apps/bot-test/test-results/<JOB_ID|local>/` (HTML y `results.json`) y clasificar cada falla con `skills/release/regression.md` (§ *Clasificar fallas*).

## Estado de las suites

El estado de cada fila del E2E maestro está en la columna `AUTOMATIZACION` de `knowledge/test-suites/e2e-master.csv`:

| Estado | Significado | ¿Se ejecuta automáticamente? |
|---|---|---|
| `Ejecutable` | Spec integrada en la rama principal de bot-test | Sí |
| `En PR` | Spec en la rama `test/ionflow-tenant-e2e` (PR abierto); ejecutar desde esa rama | Sí (desde la rama) |
| `Rota` | Spec existente que no carga o no corre | No → manual |
| `Pendiente` / `Manual` / `Bloqueada` | Sin spec | No → manual (o no aplica si está bloqueada) |

## Reglas

- ✅ Leer specs, page objects y `.md` de bot-test para mapear TCs y proponer automatización.
- ✅ Ejecutar suites (local) con el perfil correcto y adjuntar el resumen al comentario C-xx.
- ❌ No editar, crear ni borrar archivos en `../bot-test` desde el catalyst. Las propuestas de código van como **paquete de automatización** (`skills/automation/code.md`) para el responsable de bot-test.
- ❌ No ejecutar en producción tests que no sean del smoke maestro y no estén marcados como seguros para la company de prueba.
- ❌ No copiar credenciales en artefactos: solo el usuario, nunca la contraseña.
