# Skill: release/regression

> **Regresión de la versión — capa 1** (`Q-49`, REL-05): selección por riesgo desde el E2E maestro (baseline crítico + módulos impactados + cross-system; extendida si el riesgo es Alto). Incluye la **clasificación de fallas** que usan también el smoke y la capa 2. Comentario **C-27** (sección capa 1).
> Unifica las skills anteriores `release/regression-matrix`, `regression/run`, `regression/analyze` y `regression/decide` (la decisión ahora es el C-29 de `release/go-no-go`).

## Cuándo usar

- Tarea de Release en `regression` (jueves), después del sanity.
- Frase disparadora: `Ejecutar regresión: <producto> vX.Y.Z`.

## Pre-requisitos (gates)

| Check | Si falla |
|---|---|
| `tickets.md` con el mapa de impacto y el riesgo confirmado | Ejecutar `release/ingest` |
| `sanity-matrix.md` cerrado (o con decisiones de fix-forward/diferido registradas) | Cerrar el sanity primero |
| `knowledge/test-suites/e2e-master.csv` actualizado | `skills/test-suites/import-e2e.md` |

## Contexto a cargar

`knowledge/test-suites/README.md` (reglas de selección), `tickets.md`, L2 de los módulos impactados (secciones *Impacto Cruzado* y *Archivos centinela*), `skills/_shared/bot-test.md`.

## Stage 1 — Planning

1. Tomar del `tickets.md` las subcategorías y el riesgo, y simular la selección:
   ```bash
   python -I scripts/e2e_master.py select --layer 1 --subcategories "<lista>" --risk <Alto|Medio|Bajo> \
     [--focus knowledge/releases/<producto>/<versión>/_impact/focus.csv] \
     --out knowledge/releases/<producto>/<versión>/regression-matrix.csv
   ```
   **Foco del release.** Con riesgo Alto o muchos tickets, armar `_impact/focus.csv` (`ID,TICKETS`) desde el mapa de impacto de `tickets.md`: las filas del E2E maestro que tocan las features de los tickets. El script marca cada fila con `PRIORIDAD` `urgent`/`high`/`normal` (reglas en `knowledge/test-suites/README.md` § *Prioridad dentro de la capa 1*) y ordena la salida.
2. **Impacto cruzado.** Revisar en el L2 de cada módulo impactado la sección *Impacto Cruzado* y los *Archivos centinela* tocados por los PRs (`git diff --stat` de los PRs del ticket en los repos `../`). Si un archivo centinela de otro módulo cambió, agregar ese módulo con `--modules <PREFIJO>` (por ejemplo `TEN-EXH`).
3. **Cross-system completo mensual.** Si es el primer release del mes, agregar `--cross-system sí`.
4. **Flujos RGR.** Agregar filas `RGR-xx` para pruebas de API/contrato (subcategoría `API`, contratos con IonMind/StageMind/Gateway) que no estén en el maestro. Van al final del CSV con `PRIORIDAD` `urgent` (se vuelven a agregar si se regenera la selección).
5. Anunciar: filas totales por `PRIORIDAD`, automáticas vs manuales, estimación de esfuerzo frente al timebox (≤ 1 día) y el comando de bot-test. Si no entra, el recorte sigue la prioridad: `urgent` y `RGR-xx` completos (obligatorios para el GO), `high` hasta donde alcance y `normal` a la capa 2; lo que queda afuera se registra como *No ejecutado — fuera de timebox*. Esperar confirmación.

## Stage 2 — Execution

1. Copiar `templates/regression-matrix.md` a `knowledge/releases/<producto>/<versión>/regression-matrix.md` con los parámetros de selección y la tabla del CSV.
2. **Automático:** cargar el perfil de preprod y ejecutar el comando generado (los `@slow` y `@ai` pueden pasar a la corrida nocturna de la capa 2).
3. **Manual:** ejecutar las filas manuales por prioridad, registrando `RESULTADO` en el CSV y evidencia de las fallas.
4. **Clasificar fallas** (también para smoke y capa 2):

   | Clase | Criterio | Acción |
   |---|---|---|
   | 🔴 Falla real | El comportamiento cambió; reproducible a mano | Hallazgo con severidad → §7.5 (fix-forward si `urgent`; si no, Improvements con `det-regression`) |
   | 🟠 Inestable | Falla intermitente; pasa al re-ejecutar sin cambios | Cuarentena visible (`@bug` o `test.fail()` en bot-test, vía su responsable) + ejecución manual mientras tanto |
   | 🟡 Ambiente | Red, despliegue incompleto, servicio caído | Re-ejecutar; si persiste, `blocked` de la tarea con `bloq-ambiente` |
   | 🔵 Test desactualizado | La feature cambió a propósito (está en un REQ del release) | Actualizar el test (paquete a bot-test) y validar a mano |
   | ⚪ Dato de prueba | Faltan datos o fixtures | Corregir datos y re-ejecutar |

   Comparar con el `e2e-run.md` o `regression-matrix.md` del release anterior: una fila que antes pasaba y ahora falla es probable **regresión real**.
5. **Criterio de la capa 1:** flujos críticos (baseline y `Urgent`) al **100 %**. Un fallo del baseline sin fix-forward verificado es NO-GO.

## Stage 3 — Reporting

- `regression-matrix.md` + `.csv` con resultados, clasificación de fallas y filas no ejecutadas.
- Borrador **C-27** (sección capa 1) en `comments/`; la sección capa 2 la completa `release/e2e`.
- Siguiente skill: `release/e2e` (misma tarde/noche).

## Reglas

- La selección sale del E2E maestro y del mapa de subcategorías; no se arma "a mano" desde cero.
- Un test automático en rojo es un **hallazgo a analizar**, no un NO-GO automático (salvo que rompa el core del smoke).
- No hay veredicto en esta skill: el Go/No-Go es colegiado (C-29).
