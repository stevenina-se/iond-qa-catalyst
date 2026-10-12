# Regression capa 1 — [producto] v[X.Y.Z]

> **Plantilla del QA Catalyst** — regresión de la versión, capa 1 (REL-05 · `Q-49` · fuente canónica §7.7 y §9.4 · Estándar de QA §6.3 · `knowledge/test-suites/README.md`).
> **Se guarda en:** `knowledge/releases/[producto]/v[X.Y.Z]/regression-matrix.md` + `regression-matrix.csv` · **Skill:** `skills/release/regression.md` · Comentario **C-27** (sección capa 1).
> Selección por riesgo desde el E2E maestro: baseline crítico + módulos impactados + cross-system (extendida si el riesgo es Alto). **Criterio:** flujos críticos (baseline y `Urgent`) al 100 %. Timebox ≤ 1 día (jueves).

## Parámetros de selección

| Parámetro | Valor | Fuente |
|---|---|---|
| Iond Subcategory de los tickets | [Boards, App Connectors, Nodo X, ...] | `tickets.md` |
| Módulos E2E impactados | [TEN-BRD, TEN-APC, ...] | `knowledge/test-suites/_config/subcategory-map.csv` |
| Módulos agregados por impacto cruzado | [PREFIJO] — [archivo centinela o sección *Impacto Cruzado* del L2] · Ninguno | L2 del módulo + PRs |
| Riesgo | Alto / Medio / Bajo — [motivo] | T-04 (`release-task.md`) |
| Sistemas cruzados | [IonMind / Gateway / Keycloak / Stripe / apps externas] | Columna `CROSS_SYSTEM` del mapa |
| Cross-system completo (mensual) | Sí (primer release del mes) / No | Calendario |

| Riesgo | Qué entra |
|---|---|
| Bajo | Baseline crítico + filas `Urgent` de los módulos impactados + flujos cross-system de los sistemas que tocan los tickets |
| Medio | Igual, con filas `Urgent` y `High` |
| Alto | Suite extendida: todas las filas no bloqueadas |

## Comandos

```bash
# Selección (desde la raíz del catalyst)
python -I scripts/e2e_master.py select --layer 1 \
  --subcategories "[subcategorías]" --risk [Alto|Medio|Bajo] \
  [--modules "[PREFIJOS]"] [--cross-system sí] \
  --out knowledge/releases/[producto]/v[X.Y.Z]/regression-matrix.csv
```

Salida del script: [filas totales · automáticas · manuales · alcance impactado · sistemas cruzados · subcategorías sin mapa]

```bash
# Comando de bot-test generado (desde ../bot-test/apps/bot-test, con el perfil de preprod cargado)
npx playwright test [specs] --config=tests/IONFLOW/playwright.ionflow.config.ts --project=ionflow-chromium -g "[IDs]"
```

## Resumen

| Filas | Automáticas | Manuales | ✅ | ❌ | ⏭️ No ejecutado | Flujos críticos (baseline + `Urgent`) |
|---|---|---|---|---|---|---|
| [N] | [n] | [n] | [n] | [n] | [n] | [n/n] ✅ / ❌ |

## Filas del E2E maestro

Las columnas `MOTIVO`, `EJECUCION` y `RESULTADO` vienen del CSV de la selección. `RESULTADO`: ✅ · ❌ · ⏭️ *No ejecutado — fuera de timebox* · ⏭️ *No aplica* ([motivo]).

| ID | SIDE | MODULE | FEATURE / CASO | PRIORITY | MOTIVO | EJECUCION | RESULTADO | Evidencia / clasificación |
|---|---|---|---|---|---|---|---|---|
| E2E-[SIDE]-[MOD]-[NNN] | [KC / ADM / TEN / GTW] | [...] | [...] | Urgent / High / Normal / Low | baseline · módulo impactado · cross-system [sistema] · extendida | Automática / Manual | | |

## Filas RGR (cross-system o API/contrato fuera del maestro)

| ID | Sistemas / contrato | Flujo | Precondición | Pasos | Resultado esperado | Ticket origen | RESULTADO | Evidencia |
|---|---|---|---|---|---|---|---|---|
| RGR-01 | iond ↔ [IonMind / StageMind / Gateway] | [...] | [...] | [...] | [...] | #[id] | | |

## Fallas clasificadas

| Fila | Clase | Comparación con el release anterior | Acción | Hallazgo |
|---|---|---|---|---|
| [ID] | 🔴 Real / 🟠 Inestable / 🟡 Ambiente / 🔵 Test desactualizado / ⚪ Dato de prueba | Pasaba en v[X.Y.Z-1]: sí / no | Hallazgo · cuarentena visible + ejecución manual · re-ejecutar (si persiste, `blocked` con `bloq-ambiente`) · actualizar el test vía su responsable · corregir datos | [ID] |

## No ejecutado — fuera de timebox

Si la selección no entra en el día, se ejecuta primero lo automatizado, el baseline y las filas `Urgent`; lo demás queda aquí y lo cubre la rotación de la capa 2.

| ID | Motivo | Lo cubre |
|---|---|---|
| [ID] | No ejecutado — fuera de timebox | Rotación G[n] / siguiente release |

## Hallazgos

| ID | Fila | Severidad | Decisión | Ticket / subtarea |
|---|---|---|---|---|
| [...] | [ID] | `urgent` / `high` / `normal` / `low` | Fix-forward (C-28) / Improvements con `det-regression` / diferido | #[id] |

> Un fallo del baseline sin fix-forward verificado es NO-GO. Un test automático en rojo es un hallazgo a analizar, no un NO-GO automático.

## Borrador C-27 — sección capa 1

Texto de `templates/comments/C-27.md`. La línea de **capa 2** la completa `e2e-run.md` (skill `release/e2e`); el C-27 completo se publica el viernes antes de las 09:00 (`comments/C-27-[AAAA-MM-DD].md`).

```markdown
## 🧪 REGRESSION — [producto vX.Y.Z] — [✅ / ❌]
**Ejecutados:** [N] · ✅ [n] · ❌ [n] · ⏭️ [n] · **Automatizados:** [n]
**Hallazgos:** [ID — severidad — decisión: fix-forward / Improvements #id / diferido]
**Evidencia / matriz:** [link]

**Capa 1 (riesgo):** [n/n] · flujos críticos [✅ / ❌]
**Capa 2 (E2E maestro):** automatizado [n/n] · rotación G[n] [n/n] · inestables en cuarentena [n]
```
