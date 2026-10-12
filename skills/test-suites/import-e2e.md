# Skill: test-suites/import-e2e

> Mantiene el **E2E maestro** (`Q-51`): importa la hoja "Iond Testing Plan" con IDs estables, aplica el mapeo a bot-test y a QA Kanban, regenera la cobertura y devuelve las columnas ID, TICKET y SPEC para la hoja.

## Cuándo usar

- Cuando el equipo cambia la hoja (filas nuevas, prioridades, estados) o cambia el estado de una suite de bot-test.
- Antes de seleccionar la regresión de un release si la hoja cambió desde la última importación.
- Frase disparadora: `Importar E2E maestro`.

## Pre-requisitos (gates)

| Check | Si falla |
|---|---|
| CSV exportado de la hoja en `resources/Iond Testing Plan - Iond Automation Plan.csv` | Pedir al QA que exporte la pestaña "Iond Automation Plan" como CSV |
| Python 3 disponible | — |

## Contexto a cargar

`knowledge/test-suites/README.md` (§ *Mantener el E2E maestro*), `_config/modules.csv`, `_config/rules.csv`, `skills/_shared/bot-test.md`.

## Stage 1 — Planning

Anunciar: archivo de entrada, cantidad de filas, si la hoja ya tiene la columna `ID`, y los cambios de estado de suites a reflejar en `rules.csv` (si el QA los informó). Esperar confirmación.

## Stage 2 — Execution

1. **Actualizar reglas** (si corresponde) en `knowledge/test-suites/_config/rules.csv`:
   - Suite integrada en la rama principal de bot-test → `AUTOMATIZACION = Ejecutable`.
   - Spec nueva → fila con `BOT_TEST_SPEC`, `BOT_TEST_TC` (IDs `TC-…` separados por `;`) y estado.
   - Ticket nuevo de QA Kanban → `TICKET_AUTOMATIZACION`.
   - Para conocer los IDs reales, leer los títulos de los tests en `../bot-test/apps/bot-test/tests/IONFLOW/` (solo lectura).
2. **Importar:** `python -I scripts/e2e_master.py import`
   - *Filas sin módulo* → agregar el módulo a `_config/modules.csv` (código de 3 letras único dentro del SIDE) y repetir.
   - Filas `Retirada` → confirmar con el QA que fueron eliminadas a propósito de la hoja.
3. **Cobertura:** `python -I scripts/e2e_master.py coverage`
4. **Exportar para la hoja:** `python -I scripts/e2e_master.py export-sheet` → `knowledge/test-suites/exports/sheet-id-ticket-spec.csv`, alineado fila a fila con la hoja desde la fila 2.
5. **Revisar** las diferencias con la versión anterior (`git diff --stat knowledge/test-suites/`): IDs nuevos, cambios de estado de automatización, cambios de baseline o rotación.

## Stage 3 — Reporting

```
📋 E2E MAESTRO — importado
Filas vigentes: [n] · nuevas: [n] · retiradas: [n]
Automatizadas: [n] ([%]) · ejecutables: [n] ([%])
Acciones: pegar exports/sheet-id-ticket-spec.csv en la hoja (columnas ID, TICKET, SPEC desde la fila 2)
```
Salidas: `e2e-master.csv`, `coverage.md`, `exports/sheet-id-ticket-spec.csv`.

## Reglas

- `e2e-master.csv` **no se edita a mano**: todo cambio va a la hoja o a `_config/`.
- Los IDs no se renumeran nunca; una fila borrada de la hoja queda `Retirada`.
- La primera vez que se peguen los IDs en la hoja, agregar la columna con encabezado `ID`; desde entonces la importación cruza por ID.
- La rotación (G1–G4) de una fila no cambia una vez asignada.
