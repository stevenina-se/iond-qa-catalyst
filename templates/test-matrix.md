# Matriz de Pruebas — [id-clickup] · [título del ticket]

> **Plantilla del QA Catalyst** — Matriz de Pruebas interna de QA (fuente canónica §9.3 · D-11 / I-07 · Estándar de QA §5). No requiere VoBo del PO.
> **Se guarda en:** `knowledge/L3-tickets/[id-clickup]/test-matrix.md` + `test-matrix.csv` · **Skills:** `skills/mock-testing/plan.md` (diseño) · `skills/mock-testing/execute.md` (resultados) · `skills/mock-testing/report.md` (veredicto).
> Se usa en `mock testing`, se reutiliza en `sanity` y alimenta la regresión. El veredicto (C-13 / C-14) **debe coincidir** con el estado registrado aquí, y los totales del comentario son los de esta matriz.

## Control

| Campo | Valor |
|---|---|
| Ticket | [id-clickup] — [título] — [url] |
| Tablero · TYPE | Discovery / Improvements · [New Feature / Improvement / Bug / Refactor / Task] |
| Base de validación | Matriz de Requerimientos v[N] (VoBo C-06 [AAAA-MM-DD]) · Mini-matriz v[N] · Reporte del bug (T-02) |
| Contrato referenciado | [versión / enlace del contrato de `prototype review`] · No aplica |
| Ambiente · rama · PRs | [ambiente asignado al QA] · [rama del ticket] · [Merge Request 1–4] |
| Handoff (C-09) | [AAAA-MM-DD] — migraciones [sí/no] · variables [nombres] · datos [...] · prueba unitaria [sí/no] |
| Code review de QA | `code-review-qa.md` — [n] TC con ORIGEN `Code review` · No aplica |
| Iteración · Rejection_count | [1 / N] · [n] |
| Reviewer QA | @[qa] |

## Resumen

| Métrica | Valor |
|---|---|
| TC totales | [N] |
| Ejecutados · ✅ Aprobados · ❌ Fallidos · ⏭️ Omitidos · ⛔ Bloqueados | [N] · [n] · [n] · [n] · [n] |
| REQ cubiertos | [n]/[N] |
| REQ críticos aprobados | [n]/[N] (100 % requerido) |
| No regresión de zonas cercanas | [n]/[n] |
| USO `Sanity` · `Regresión candidata` | [n] · [n] |
| Automatizables | [n] |

## Cobertura por REQ

| REQ | Crítico | TC | Happy Path | Negativo / Borde | Estado del REQ |
|---|---|---|---|---|---|
| REQ-01 | Sí | TC-01, TC-02 | ✅ | ✅ | ✅ / ❌ / ⏳ |
| REQ-NF-01 | No | TC-05 | — | — | ✅ / ❌ / ⏳ |

Reglas: cada REQ tiene al menos un TC; cada REQ crítico tiene al menos un TC *Happy Path* y uno *Negativo* o *Borde*; cada REQ-NF se mide con su métrica.

## Matriz de Pruebas

| ID | REQ_ID | ORIGEN | TIPO | PRECONDICION | PASOS | RESULTADO_ESPERADO | USO | AUTOMATIZABLE | ESTADO | EVIDENCIA |
|---|---|---|---|---|---|---|---|---|---|---|
| TC-01 | REQ-01 | REQ | Happy Path | [Datos, rol y estado previo] | Company Login > Sidebar: [Módulo] > [Acción] > Verify: [...] | [Resultado según REQ-01] | Sanity | Sí | Pendiente | |
| TC-02 | REQ-01 | REQ | Negativo | [...] | [...] | [...] | Mock | No | Pendiente | |
| TC-03 | REQ-02 | Code review | Borde | [...] | [...] | [...] | Mock | Sí | Pendiente | |
| TC-04 | REQ-02 | Regla L2 | Borde | [...] | [...] | [...] | Regresión candidata | Sí | Pendiente | |
| TC-05 | REQ-NF-01 | REQ | NF | [Ambiente, volumen, datos] | [Cómo se mide] | [Métrica y umbral] | Mock | No | Pendiente | |
| TC-06 | — | Zona cercana | Regresión | [...] | [...] | [...] | Mock | Sí | Pendiente | |

## CSV (`test-matrix.csv`)

Mismas filas que la tabla. UTF-8, separador coma; los campos con comas o saltos de línea van entre comillas dobles. Cabecera obligatoria (las skills la leen tal cual):

```csv
ID,REQ_ID,ORIGEN,TIPO,PRECONDICION,PASOS,RESULTADO_ESPERADO,USO,AUTOMATIZABLE,ESTADO,EVIDENCIA
```

### Valores permitidos

| Columna | Valores | Regla |
|---|---|---|
| `ID` | `TC-01`, `TC-02`… | Consecutivo; un ID eliminado no se reutiliza. |
| `REQ_ID` | `REQ-01` · `REQ-NF-01` · `REQ-[SUB]-01` · `T-02` · `—` | `—` solo con ORIGEN `Zona cercana` o `Exploratorio`. En un bug sin matriz, `T-02` (resultado esperado del reporte) o el REQ-ID que cite el reporte. |
| `ORIGEN` | `REQ` · `Regla L2` · `Code review` · `Zona cercana` · `Exploratorio` | `Regla L2`: regla del módulo en `knowledge/L2-modules/` que el REQ toca. `Code review`: riesgo detectado en `code-review-qa.md`. Ambos llevan el REQ-ID del requerimiento que verifican. |
| `TIPO` | `Happy Path` · `Negativo` · `Borde` · `Regresión` · `NF` | `NF` solo para filas `REQ-NF-xx`. |
| `USO` | `Mock` · `Sanity` · `Regresión candidata` | `Sanity`: TC de un REQ crítico (se re-ejecuta en `sanity`). `Regresión candidata`: TC estable que conviene sumar al E2E maestro o automatizar. `Mock`: solo `mock testing`. |
| `AUTOMATIZABLE` | `Sí` · `No` | |
| `ESTADO` | `Pendiente` · `Aprobado` · `Fallido` · `Omitido` · `Bloqueado` | `Fallido` → `OBS-xx` en EVIDENCIA. `Omitido` → justificación en EVIDENCIA. |
| `EVIDENCIA` | `screenshots/[TC-ID]-[paso].png` · `OBS-xx` · query o salida de API · justificación | Ver `skills/_shared/evidence.md`. |

## Formato de pasos (breadcrumb)

Los pasos usan **breadcrumb** explícito para que cualquier persona (o la IA) los reproduzca sin ambigüedad:
`[Rol] Login > Sidebar: [Módulo] > [Acción] > [Sub-acción] > Verify: [qué]`

| Elemento | Formato | Ejemplo |
|---|---|---|
| Login | `Company Login` / `Admin Login` | `Company Login` |
| Menú | `Sidebar: [nombre]` | `Sidebar: Boards` |
| URL | `Navigate: /ruta` | `Navigate: /workflows` |
| Click | `Click [elemento]` | `Click [Board "qa-board-01"]` |
| Botón | `Button: "[nombre]"` | `Button: "Save"` |
| Drawer | `Drawer: [nombre]` | `Drawer: Code Config` |
| Completar | `Fill "[campo]": "[valor]"` | `Fill "Name": "qa-board-01"` |
| Seleccionar | `Select "[campo]": [opción]` | `Select "Language": Python` |
| API | `[MÉTODO] /ruta > Body: {...}` | `POST /api/... > Body: {...}` |
| Verificar | `Verify: [qué]` | `Verify: Toast "Created"` |
| Esperar | `Wait: [qué]` | `Wait: Execution finished` |

## Verificación en BD (solo lectura)

Queries construidas **solo** desde las migraciones (nunca inventar tablas, campos ni relaciones). Solo `SELECT`; la ejecuta el QA y pega el resultado.

```sql
-- Fuente: ../gateway/database/migrations/[archivo].php
-- Tabla: [tabla] | Columnas verificadas: [lista]

-- TC-01 (REQ-01): [qué se verifica]
SELECT [columnas] FROM [tabla] WHERE [condición];
-- Esperado: [resultado]
```

- BD principal (PostgreSQL): `../gateway/database/migrations/*.php` — túnel SSH.
- Ejecuciones (SQLite por instancia del motor): `../flow_binaries/migrations/*.sql` — vía UI o API del historial de ejecuciones.

## Reglas

- **Trazabilidad obligatoria:** todo TC lleva REQ-ID y TIPO. Un TC sin REQ-ID solo se admite como regresión de zonas cercanas o exploratorio; si falla, es rechazo solo si es una regresión provocada por el cambio; si no, va como hallazgo fuera de matriz (C-17).
- **Después de cada nuevo VoBo (v+1)**, la matriz se ajusta antes de re-ejecutar.
- **Re-test:** se re-ejecutan los TC fallidos, los TC de REQ críticos de las áreas tocadas por el fix y la no regresión de zonas cercanas. Cada observación se marca *Nuevo*, *Persistente* o *Regresión*.
- **Bugs (Improvements):** el TC principal verifica el resultado esperado del reporte; se agregan de 3 a 5 TC `Zona cercana` / `Regresión`.
- Datos creados por QA con prefijo `qa-` (manual) o `autobot-` (automatizado); se eliminan al terminar cuando la app lo permite.
