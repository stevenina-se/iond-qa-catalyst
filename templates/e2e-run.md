# E2E maestro capa 2 — [producto] v[X.Y.Z]

> **Plantilla del QA Catalyst** — E2E maestro como capa 2 de `regression` (REL-05 · `Q-50` · fuente canónica §7.4 y §7.7 · `knowledge/test-suites/README.md` § *Capa 2 y rotación*).
> **Se guarda en:** `knowledge/releases/[producto]/v[X.Y.Z]/e2e-run.md` + `e2e-run.csv` · **Skill:** `skills/release/e2e.md` · Comentario **C-27** (sección capa 2).
> Corre **todo lo automatizado** sin supervisión (jueves noche) y el **grupo de rotación manual** que corresponde, sin repetir lo que ya corrió en la capa 1. El maestro completo se cubre cada 4 releases. **Peso en el Go/No-Go:** una falla es un hallazgo; solo es NO-GO si es `urgent` y la provocó el release.

## Encabezado

| Campo | Valor |
|---|---|
| Producto / versión | [iond / IonMind / StageMind] v[X.Y.Z] |
| Ambiente · build | preprod · [commit RC] |
| Grupo de rotación de este release | G[n] |
| Grupo del release anterior | G[n-1] — `knowledge/releases/[producto]/v[X.Y.Z-1]/e2e-run.md` · Ninguno (primer release: G1) |
| Pendientes arrastrados del grupo | [IDs no ejecutados en la última corrida de G[n]] · Ninguno |
| Riesgo del release | Alto → la capa 1 ya es la suite extendida: la rotación manual queda vacía · Medio / Bajo |
| Corrida automática | Jueves [AAAA-MM-DD hh:mm] · perfil `.env.preprod` (solo el nombre) |
| Rotación manual | [AAAA-MM-DD] · @[qa] · timebox ≈ 0,5 día |
| Consolidado | Viernes [AAAA-MM-DD] antes de las 09:00 |

## Comandos

```bash
# Selección (desde la raíz del catalyst)
python -I scripts/e2e_master.py select --layer 2 --group G[n] \
  --exclude knowledge/releases/[producto]/v[X.Y.Z]/regression-matrix.csv \
  --out knowledge/releases/[producto]/v[X.Y.Z]/e2e-run.csv
```

```bash
# Comando de bot-test generado (desde ../bot-test/apps/bot-test, con el perfil de preprod cargado)
npx playwright test [specs] --config=tests/IONFLOW/playwright.ionflow.config.ts --project=ionflow-chromium -g "[IDs]"
```

Los tests `@slow` (scheduler) y `@ai` (créditos de IA) corren en esta corrida nocturna.

## Resumen automático

| Automatizados | ✅ | ❌ | Inestables | Omitidos | Duración | Reporte HTML |
|---|---|---|---|---|---|---|
| [N] | [n] | [n] | [n] | [n] | [hh:mm] | `apps/bot-test/test-results/[JOB_ID / local]/` |

## Fallas clasificadas

Clases de `skills/release/regression.md`: 🔴 Real · 🟠 Inestable · 🟡 Ambiente · 🔵 Test desactualizado · ⚪ Dato de prueba.

| Fila | Test (spec › TC) | Clase | Reproducida a mano | ¿La provocó el release? | Severidad | Acción / hallazgo |
|---|---|---|---|---|---|---|
| E2E-[SIDE]-[MOD]-[NNN] | [spec] › [TC] | [...] | Sí / No | Sí / No | `urgent` / `high` / `normal` / `low` | [...] |

## Cuarentena

Las pruebas inestables se ponen en cuarentena **de forma visible** (nunca se ignoran en silencio) y se ejecutan a mano mientras tanto. El catalyst no modifica bot-test: el cambio (`@bug` o `test.fail()`) lo hace su responsable.

| Test | Spec | Desde | Motivo | Ejecución manual sustituta | Resultado manual |
|---|---|---|---|---|---|
| [TC] | [spec] | [AAAA-MM-DD] | [...] | [ID de la fila] | ✅ / ❌ |

## Rotación manual G[n]

`RESULTADO`: ✅ · ❌ · ⏭️ *No ejecutado — pasa al siguiente release del grupo*.

| ID | MODULE | FEATURE / CASO | PRIORITY | RESULTADO | Evidencia |
|---|---|---|---|---|---|
| E2E-[SIDE]-[MOD]-[NNN] | [...] | [...] | Urgent / High / Normal / Low | | |

**Rotación:** [n/n] ejecutadas · [n] pendientes que se arrastran.

## Comparación con la corrida anterior

- Filas que pasaban y ahora fallan (probable regresión real): [...]
- Filas nuevas automatizadas o specs que cambiaron de estado: [...] → actualizar `AUTOMATIZACION` en `knowledge/test-suites/_config/rules.csv` y reimportar (`python -I scripts/e2e_master.py import`).

## Hallazgos

| ID | Fila | Severidad | ¿`urgent` provocado por el release? | Decisión | Ticket |
|---|---|---|---|---|---|
| [...] | [ID] | [...] | Sí → NO-GO salvo fix-forward (C-28) / No | Improvements con `det-regression` (previa discusión con PO y LD) | #[id] |

## Borrador C-27 — sección capa 2

Completar en el borrador iniciado en `regression-matrix.md` (`comments/C-27-[AAAA-MM-DD].md`) y publicar el C-27 completo el viernes antes de las 09:00:

```markdown
**Capa 2 (E2E maestro):** automatizado [n/n] · rotación G[n] [n/n] · inestables en cuarentena [n]
```
