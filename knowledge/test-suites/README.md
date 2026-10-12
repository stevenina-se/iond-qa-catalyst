# Suites de prueba del release — IOND

> Estrategia vigente desde el 2026-10-10 (decisiones `Q-47` a `Q-51` del Registro de Decisiones; fuente canónica `knowledge/L1-project/sdlc-consolidation.md` §7.7).
> Las skills que usan estas suites están en `skills/release/` y `skills/test-suites/`.

## Las cuatro suites

| Suite | Alcance | Fuente | Ambiente | Cuándo | Comentario |
|---|---|---|---|---|---|
| **Smoke maestro** | Única y fija para todo release (SMK-01…SMK-17) | [`smoke-master.md`](smoke-master.md) | Preprod y producción (company de prueba) | `smoke` (lunes PM – martes AM) y post-despliegue | C-25 · C-31 |
| **Sanity** | Propia de la versión: REQ críticos de los tickets del release | Matrices L3 de cada ticket | Preprod | `sanity` (martes – miércoles) | C-26 |
| **Regression capa 1** | Propia de la versión, por riesgo | [`e2e-master.csv`](e2e-master.csv) + `_config/subcategory-map.csv` + riesgo de la T-04 | Preprod | `regression` (jueves) | C-27 |
| **E2E maestro capa 2** | Todas las features: lo automatizado completo + un grupo de rotación manual | [`e2e-master.csv`](e2e-master.csv) | Preprod | `regression` (jueves noche → viernes 09:00) | C-27 |

### Selección de la regresión (capa 1)

| Riesgo de la T-04 | Qué entra |
|---|---|
| **Bajo** | Baseline crítico + filas `Urgent` de los módulos impactados + flujos cross-system de los sistemas que tocan los tickets |
| **Medio** | Igual, con filas `Urgent` y `High` |
| **Alto** | Suite extendida: todas las filas no bloqueadas |

- **Baseline crítico:** filas con `BASELINE = sí` (login/SSO, crear y ejecutar boards, historial, conexiones y App Connectors, plantillas PDF, consumo y billing). Corre siempre.
- **Módulos impactados:** se derivan de la **Iond Subcategory** de cada ticket con `_config/subcategory-map.csv`. Una subcategoría `Nodo <nombre>` selecciona la fila de ese nodo.
- **Flujos cross-system:** se toman de la columna `CROSS_SYSTEM` del mapa (IonMind, Gateway, Keycloak, Stripe, apps externas). Una vez al mes se corre la cross-system completa con `--cross-system sí`.
- Si la selección no entra en el timebox, QA ejecuta primero lo automatizado, el baseline y las filas `Urgent`. Lo que queda afuera se registra como *No ejecutado — fuera de timebox* y lo cubre la rotación.

#### Prioridad dentro de la capa 1 (`PRIORIDAD`)

La salida de la capa 1 trae la columna `PRIORIDAD` y viene ordenada por ella. Usa la misma escala que los bugs (`urgent`, `high`, `normal`) y es la prioridad **del release**, no la de la hoja (`PRIORITY`). Es la regla de recorte del Estándar de QA §6.3 aplicada fila por fila:

| Prioridad | Qué entra | Cuándo |
|---|---|---|
| **`urgent`** | Baseline + **foco del release** (`--focus`) + filas de los nodos tocados. Las filas `RGR-xx` se agregan como `urgent` | Jueves AM; 100 % para el GO |
| **`high`** | `Urgent`/`High` de los módulos impactados o cross-system que no están en el foco | Jueves PM |
| **`normal`** | Resto de la extendida | Pasa a la capa 2 (automatizado y rotación); lo no ejecutado se lista en el Go/No-Go |

- **Foco del release (`--focus`):** CSV con las columnas `ID,TICKETS` (o una lista de IDs E2E) con las filas que tocan las features de los tickets. Sale del mapa de impacto de `tickets.md` y se guarda en `knowledge/releases/<producto>/<versión>/_impact/focus.csv`. Una fila del foco es `urgent` aunque sea `Normal`, y entra aunque esté bloqueada en la hoja (el release la desbloquea). La columna `TICKETS_RELEASE` del CSV indica qué tickets la tocan.
- **Sin `--focus`** (releases chicos): son `urgent` el baseline, las filas de los nodos tocados y las filas `Urgent` de los módulos impactados.
- La capa 2 con `--exclude` solo excluye las filas `urgent` y `high` de la capa 1: las `normal` se cubren allí.

### Capa 2 y rotación (G1–G4)

- Cada fila del maestro pertenece a un grupo de rotación (`ROTACION`). La unidad es el módulo completo, y se divide por nivel solo cuando supera 15 filas manuales.
- Cada release ejecuta **todo lo automatizado** y **el grupo siguiente** al del release anterior, sin repetir los IDs que ya corrieron en la capa 1. El maestro completo se cubre cada 4 releases.
- El grupo ejecutado queda registrado en `knowledge/releases/<producto>/<versión>/e2e-run.md`. El siguiente release toma el grupo que sigue.

## Archivos

| Archivo | Qué es | ¿Se edita a mano? |
|---|---|---|
| `smoke-master.md` | Smoke maestro | Sí (LQA + LD/RM; registrar en su historial) |
| `e2e-master.csv` | E2E maestro con IDs estables, baseline, rotación, automatización y trazabilidad | **No**: lo genera `scripts/e2e_master.py import` |
| `_config/modules.csv` | Código de 3 letras y módulo L2 de cada módulo de la hoja | Sí |
| `_config/rules.csv` | Reglas por ruta: baseline, prod-safe, cross-system, spec y TC de bot-test, estado de automatización, ticket de QA Kanban | Sí (es donde se mantiene el mapeo) |
| `_config/subcategory-map.csv` | Iond Subcategory → módulo L2 → módulos del E2E + sistemas cruzados | Sí (agregar cada subcategoría nueva) |
| `coverage.md` | Cobertura de automatización por SIDE y módulo, y carga de la rotación | No: lo genera `coverage` |
| `automation-roadmap.md` | Olas de automatización y estado de los tickets de QA Kanban | Sí (LQA) |
| `exports/sheet-id-ticket-spec.csv` | Columnas ID, TICKET y SPEC para pegar en la hoja | No: lo genera `export-sheet` |

## IDs

| Prefijo | Suite | Ejemplo |
|---|---|---|
| `SMK-xx` | Smoke maestro | SMK-05 |
| `SAN-<ticket>-<REQ>` · `SAN-<ticket>-T-02` · `SAN-INT-xx` | Sanity (REQ crítico · bug sin matriz · interacción entre tickets) | SAN-86exxxxxx-REQ-03 |
| `E2E-<SIDE>-<MOD>-NNN` | E2E maestro (capa 1 y capa 2) | E2E-TEN-BRD-012 |
| `RGR-xx` | Flujo cross-system o prueba de API/contrato que no está en el maestro | RGR-03 |

SIDE: `KC` · `ADM` (ADMIN) · `TEN` (TENANT) · `GTW` (ADMIN GATEWAY). Los IDs del E2E **nunca se renumeran**. Una fila que desaparece de la hoja queda como `Retirada`.

## Mantener el E2E maestro

```bash
# 1. Exportar la hoja "Iond Testing Plan" › pestaña "Iond Automation Plan" como CSV en resources/
# 2. Importar (asigna IDs nuevos solo a filas nuevas) y regenerar la cobertura
python -I scripts/e2e_master.py import
python -I scripts/e2e_master.py coverage
# 3. Devolver los IDs a la hoja: pegar las 3 columnas desde la fila 2 (alineadas fila a fila)
python -I scripts/e2e_master.py export-sheet
```

- La primera vez que se peguen los IDs en la hoja, agregar una columna con encabezado **`ID`**. A partir de ahí, la importación cruza por ID aunque cambie el texto de la fila.
- Si `import` informa *Filas sin módulo*, agregar el módulo a `_config/modules.csv`.
- Cuando una suite de bot-test cambia de estado (por ejemplo, se integra el PR de la rama E2E), actualizar `AUTOMATIZACION` en `_config/rules.csv` (`En PR` → `Ejecutable`; `Rota` → `Ejecutable` cuando se corrija) y reimportar.

## Seleccionar una suite

```bash
# Capa 1: regresión de la versión
python -I scripts/e2e_master.py select --layer 1 \
  --subcategories "Boards,Nodo Mapper,App Connectors" --risk Medio \
  [--focus knowledge/releases/iond/vX.Y.Z/_impact/focus.csv] \
  --out knowledge/releases/iond/vX.Y.Z/regression-matrix.csv

# Capa 2: automatizado + grupo de rotación, sin repetir la capa 1
python -I scripts/e2e_master.py select --layer 2 --group G2 \
  --exclude knowledge/releases/iond/vX.Y.Z/regression-matrix.csv \
  --out knowledge/releases/iond/vX.Y.Z/e2e-run.csv
```

La salida trae la matriz y el **comando de bot-test** con los IDs de los tests. La capa 1 sale con las **columnas de ejecución** de las matrices del release —ID · PRIORIDAD · SIDE · MODULE · FEATURE · CASO · RESULTADO ESPERADO · QA ASIGNADO · RESOLUCION · OBSERVACION · TICKET · PRIORIDAD BUG (las mismas del sanity y del smoke)—, seguidas de MOTIVO, TICKETS_RELEASE y CROSS_SYSTEM y, al final, las columnas de automatización (EJECUCION, AUTOMATIZACION, BOT_TEST_SPEC, BOT_TEST_TC), que pueden ocultarse en la hoja. Si un caso falla, la URL del bug va en TICKET y su prioridad en PRIORIDAD BUG. La capa 2 conserva su formato (columna `RESULTADO`).

## Ejecutar en bot-test (sin modificarlo)

bot-test se usa **solo para ejecutar**: el catalyst no cambia su código (`Q-54`). La configuración de IONFLOW carga `apps/bot-test/.env` con `dotenv`, que **no sobrescribe** las variables ya definidas. Por eso basta con cargar antes el perfil del ambiente:

```bash
# Git Bash — desde ../bot-test/apps/bot-test
set -a; source ~/.qa-profiles/.env.preprod; set +a      # o .env.prod-testco para el smoke de producción
npx playwright test <specs> --config=tests/IONFLOW/playwright.ionflow.config.ts --project=ionflow-chromium -g "<IDs>"
```

```powershell
# PowerShell — desde ..\bot-test\apps\bot-test
Get-Content $HOME\.qa-profiles\.env.preprod | Where-Object { $_ -match '^\s*[^#].*=' } |
  ForEach-Object { $k, $v = $_ -split '=', 2; Set-Item "env:$($k.Trim())" $v.Trim() }
npx playwright test <specs> --config=tests/IONFLOW/playwright.ionflow.config.ts --project=ionflow-chromium -g "<IDs>"
```

- Los perfiles (`.env.preprod`, `.env.prod-testco`) viven **fuera de los repositorios** y usan las claves `IONFLOW_*` de `.env.sample`.
- El reporte HTML queda en `apps/bot-test/test-results/<JOB_ID|local>/`. Se adjunta su resumen al C-25, C-27 o C-31.
- Los tests con `@slow` (scheduler, ≈ 10 min) y `@ai` (créditos de IA) se dejan para la corrida nocturna de la capa 2.
- Una falla automática se clasifica con `skills/release/regression.md` (falla real, inestable o de ambiente) antes de reportarla.
