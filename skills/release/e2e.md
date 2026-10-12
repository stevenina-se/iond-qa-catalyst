# Skill: release/e2e

> **E2E maestro — capa 2** (`Q-50`, REL-05): después de la regresión priorizada, corre **todo lo automatizado** del maestro sin supervisión y el **grupo de rotación manual** que corresponde (G1–G4), sin repetir lo que ya corrió en la capa 1. Comentario **C-27** (sección capa 2).

## Cuándo usar

- Jueves: preparación por la tarde, corrida automática por la noche, rotación manual dentro del timebox (≈ 0,5 día), consolidado el **viernes antes de las 09:00**.
- Frase disparadora: `Ejecutar E2E capa 2: <producto> vX.Y.Z`.

## Pre-requisitos (gates)

| Check | Si falla |
|---|---|
| `regression-matrix.csv` de la capa 1 | Ejecutar `release/regression` primero |
| Grupo de rotación definido en la `release-task.md` | Calcularlo: siguiente al del último `e2e-run.md` del producto |
| Perfil de preprod en la máquina que corre la suite nocturna | Pedir al QA que lo cargue |

## Contexto a cargar

`knowledge/test-suites/README.md` (§ *Capa 2 y rotación*), `knowledge/test-suites/coverage.md`, `skills/_shared/bot-test.md`.

## Stage 1 — Planning

```bash
python -I scripts/e2e_master.py select --layer 2 --group G<n> \
  --exclude knowledge/releases/<producto>/<versión>/regression-matrix.csv \
  --out knowledge/releases/<producto>/<versión>/e2e-run.csv
```
Anunciar: filas automáticas (todas las ejecutables), filas manuales del grupo, duración estimada (incluye `@slow`) y el comando de bot-test. Esperar confirmación.

## Stage 2 — Execution

1. Copiar `templates/e2e-run.md` a `knowledge/releases/<producto>/<versión>/e2e-run.md` con el grupo de este release y el del anterior.
2. **Corrida automática** (noche): ejecutar el comando generado con el perfil de preprod. Si la rama E2E de bot-test todavía no está integrada, correr desde esa rama (estado `En PR`).
3. **Rotación manual:** ejecutar las filas manuales del grupo por prioridad dentro de ≈ 0,5 día. Lo que no entra queda *No ejecutado* y **pasa al siguiente release** del mismo grupo (se anota en `e2e-run.md`).
4. **Clasificar fallas** con la tabla de `release/regression.md`. Tests inestables → cuarentena visible y ejecución manual.
5. **Peso en el Go/No-Go:** una falla de la capa 2 es un hallazgo. Solo es NO-GO si es `urgent` **y la provocó el release**; el resto va a Improvements `backlog` con `det-regression`, previa discusión con PO y LD.
6. **Cobertura:** comparar con la corrida anterior (filas que pasaron a fallar, filas nuevas automatizadas).

## Stage 3 — Reporting

- `e2e-run.md` + `.csv` (totales automáticos, fallas clasificadas, rotación ejecutada, pendientes que se trasladan).
- Completar la sección **capa 2** del borrador C-27 y dejar el C-27 completo para publicar el viernes antes de las 09:00.
- Si hubo filas nuevas automatizadas o specs que cambiaron de estado: acción para actualizar `_config/rules.csv` y reimportar (`skills/test-suites/import-e2e.md`).
- Siguiente skill: `release/go-no-go`.

## Reglas

- La capa 2 **no reemplaza** a la capa 1: corre después y con otro peso en la decisión.
- Con riesgo **Alto**, la capa 1 ya es la suite extendida: la rotación manual queda vacía y la capa 2 se reduce a la corrida automática.
- La rotación avanza un grupo por release del producto, aunque el grupo haya quedado incompleto (lo pendiente se arrastra).
