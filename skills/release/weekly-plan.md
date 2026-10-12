# Skill: release/weekly-plan

> Herramienta del **Scrum Master** para el corte semanal. Arma el borrador de la **tarea de Release** (T-04) de cada producto con tickets listos, propone el riesgo del release y el calendario de la semana, y deja el checklist de acciones del SM y del RM.
> Reglas: fuente canónica §7.1–§7.4 y §7.7 (`Q-32`, `Q-33`, `Q-35`, `Q-37`, `Q-47` a `Q-51`). Reemplaza a `release/plan`, `release/plan-v1` y `sprint-planning`.

## Cuándo usar

- **Viernes previo** al corte (preparación) y **lunes 09:00** (confirmación del corte).
- Frase disparadora: `Planificar release semanal` o `Planificar release: <producto> vX.Y.Z`.

## Pre-requisitos (gates)

| Check | Si falla |
|---|---|
| MCP de ClickUp responde (`getListInfo 901717038641`) | PARAR: revisar la conexión |
| Existe la lista del sprint semanal en el folder Releases | Acción del SM: crearla (`Sprint N (fecha - fecha)`) |
| `knowledge/test-suites/e2e-master.csv` existe | Ejecutar `skills/test-suites/import-e2e.md` |

## Contexto a cargar

- `knowledge/L1-project/sdlc-consolidation.md` §7 y §13 (T-04).
- `docs/sdlc-iond/src/05-estandar-operativo-qa-iond.md` §6.3 (riesgo del release) y §9.2 (capacidad).
- `skills/_shared/clickup.md` y `skills/_shared/artifacts.md`.

## Stage 1 — Planning

Anunciar:
```
🔄 SIGUIENTE SKILL: release/weekly-plan
   Corte: lunes [fecha] 09:00 · Sprint: [nombre de la lista]
   Productos a revisar: iond (+ Gateway) · IonMind · StageMind
   Fuente: tickets en `ready to merge` de Discovery e Improvements (MCP, solo lectura)
   Output: knowledge/releases/<producto>/<versión>/release-task.md (uno por producto con tickets)
¿Procedo?
```

## Stage 2 — Execution

1. **Candidatos.** `searchTasks` con `list_ids = [901717038641, 901717038640]` y `status = ["ready to merge"]`. Para cada ticket, `getTaskById` y registrar: Project, versión objetivo (según el Project), Iond Subcategory, TYPE, prioridad, QA Points, Merge Requests, tags, subtareas en `done w/d`.
2. **Agrupar por producto y versión.** Project `Iond` y `Gateway` → release de `iond` (Gateway usa G.Version); `IONMIND` → `ionmind`; `STAGEMIND` → `stagemind`.
   - Versión vacía o `develop`/`DEVELOPMENT` → **no entra**: acción para RM/SM "registrar la versión objetivo" (A-11).
   - Sin C-13 en los comentarios → **no entra**: inconsistencia para el LQA.
   - Con `uat-requerido` y sin C-18 → **no entra**.
   - Subtareas en `done w/d` → acompañan al padre (A-20); listar las que no estén en `done w/d`.
3. **Release vacío.** Si un producto no tiene tickets válidos, **no hay release** esa semana (`Q-32`). Registrarlo en el resumen.
4. **Límite de lote.** Sumar los QA Points de sanity estimados por QA (≤ 15 por QA y semana, `Q-32`). Si se excede, proponer al PO qué tickets diferir (el PO decide).
5. **Riesgo del release** (doc 05 §6.3): **Alto** si toca billing o consumo, autenticación o permisos, motor de ejecución, contratos de API o migraciones de datos; **Medio** si toca varios módulos sin reglas troncales; **Bajo** si solo UI y textos. Registrar el motivo.
6. **Dependencias entre productos** (`Q-37`): si hay releases de varios productos, ordenar el despliegue StageMind → IonMind → iond y relacionar las tareas.
7. **Plan de suites de la semana:**
   - Smoke maestro (siempre).
   - Sanity: lista de tickets con su matriz (verificar que cada uno tenga `requirements-matrix-v<N>.md` o matriz en la descripción y `test-matrix.md` en L3; si falta, avisar al LQA).
   - Regresión capa 1: subcategorías del lote + riesgo → parámetros para `scripts/e2e_master.py select --layer 1`.
   - Capa 2: grupo de rotación = el siguiente al del último `e2e-run.md` del producto (G1 → G2 → G3 → G4 → G1). Si no hay uno anterior, G1.
8. **Calendario** (fuente canónica §7.4) con fechas reales de la semana y el quórum del Go/No-Go (PO + LQA + RM).
9. **Borrador de la T-04** con `templates/release-task.md` en `knowledge/releases/<producto>/<versión>/release-task.md`.

## Stage 3 — Reporting

Presentar al SM:
```
📦 PLAN SEMANAL — Sprint [N]
| Producto | Versión | Tickets | QA Points sanity | Riesgo | Grupo capa 2 |
| iond     | vX.Y.Z  | [n]     | [n]              | Medio  | G2           |
Excluidos: [#id — motivo (sin versión / sin C-13 / sin UAT)]
Acciones del SM: crear la tarea "Release iond - vX.Y.Z" con T-04 en la lista del sprint, relacionar los [n] tickets, fecha de vencimiento = viernes [fecha], Project, versión.
Acciones del RM: registrar versiones faltantes; preparar ramas RC (`Q-33`).
```
Salidas:
- `knowledge/releases/<producto>/<versión>/release-task.md` (contenido para pegar en la descripción de la tarea de Release).
- Borrador de **C-23** para el RM en `comments/C-23-<fecha>.md` (corte, tickets incluidos, diferidos).
- Siguiente skill sugerida: `release/ingest` (lunes, tras el corte).

## Reglas

- El catalyst **no crea** la tarea de Release ni mueve tickets: lo hace el SM (y el RM en `dev preparation`).
- Un ticket entra al release solo por **versión objetivo + `ready to merge` + C-13** (y C-18 si aplica).
- Los tickets no se mueven al tablero de Releases; la tarea los referencia por relación (fuente canónica §7.1).
- La decisión de diferir por capacidad es del **PO**.
