# Risk Triage — 86e2ak75f

> Standardize Execution UI & Build Execution Replay Engine

## Resumen

- **Módulo principal**: Executions (🟠 Alto)
- **Módulos impactados**: Boards (🔴 Crítico), Dashboard (🟢 Bajo - indirecto)
- **Riesgo general**: 🔴 Crítico
- **Total edge cases identificados**: 18
- **Total preguntas para Developer**: 12
- **Contexto de ClickUp**: 6 comentarios leídos, divergencias significativas encontradas (2 AC → 12 AC reconciliados)

---

## Análisis de Lógica de Negocio

| Pregunta | Análisis |
|----------|----------|
| ¿El feature respeta las reglas multi-tenant (company)? | **SÍ con riesgo.** Las ejecuciones se filtran por company, pero la nueva vista con URL propia introduce un vector de riesgo: si un usuario comparte un enlace de ejecución, ¿otro usuario de diferente company podría acceder? El permiso `READ_EXECUTION` debe verificarse por company. |
| ¿Afecta la ejecución de flows/nodos? | **SÍ directamente.** Los AC 5-7 tocan control de concurrencia, bloqueo de botón de ejecución y lifecycle de ejecuciones. El snapshot del board se guarda durante la ejecución (AC-9). |
| ¿Hay impacto en connectors globales vs company? | **NO directo.** El replay muestra el board ejecutado, pero los connectors no se re-ejecutan. Sin embargo, si un connector global se modifica después de la ejecución, el snapshot debe mostrar la versión original. |
| ¿Se tocan datos de ejecución (SQLite) o datos persistentes (PostgreSQL)? | **AMBOS.** Nueva tabla SQLite para snapshot de flows. Nuevas columnas en tabla `executions` de PostgreSQL (modo live/dev, trigger type). Servicio nuevo de sincronización SQLite ↔ R2. |
| ¿Hay impacto en el sistema de permisos por usuario/company? | **SÍ.** Se requiere `READ_EXECUTION` para acceder, `DELETE_EXECUTION` para eliminar. La nueva URL de ejecución debe respetar estos permisos. |
| ¿El feature puede romper flujos de e-commerce existentes? | **NO.** Es una feature de visualización/consulta. La única acción que modifica algo es ejecutar un board (que ya existe). |

---

## Análisis de Impacto por Módulo

### Módulo: Executions (Principal)

| Área | Impacto | Riesgo |
|------|---------|--------|
| **Frontend** (rutas, vistas, componentes) | **ALTO.** Nueva vista con URL propia (`/executions/:id` o similar). Nuevo componente de replay con canvas read-only. Panel de I/O de nodos. Tabla de ejecuciones mejorada con filtros. | 🔴 Crítico |
| **API** (endpoints, payloads) | **ALTO.** Posibles nuevos endpoints para obtener snapshot del flow. Endpoint existente de ejecución modificado para incluir nuevos campos (modo, trigger type). | 🟠 Alto |
| **Canvas** (nodos, edges, drawer) | **ALTO.** Reutiliza visor read-only existente PERO con datos de snapshot (no del board actual). Los nodos deben colorearse por estado. | 🔴 Crítico |
| **BD PostgreSQL** (tablas, relaciones) | **MEDIO.** Nuevas columnas en tabla `executions`: modo (live/dev), trigger type. No es migración destructiva pero afecta queries existentes. | 🟠 Alto |
| **BD SQLite** (ejecuciones) | **ALTO.** Nueva tabla para snapshot del flow ejecutado. Servicio de sincronización con R2. Cache temporal con cron de limpieza. | 🔴 Crítico |
| **Otros módulos afectados** | Boards (3 puntos de acceso), Dashboard (métricas), Billing (consumo) | 🟠 Alto |

### Módulo: Boards (Secundario)

| Área | Impacto | Riesgo |
|------|---------|--------|
| **Frontend** | Nuevo acceso desde lista de boards (menú contextual) + tab "Ejecuciones" en board editor | 🟠 Alto |
| **API** | Sin cambios directos a la API de boards | 🟢 Bajo |
| **Canvas** | Canvas read-only mostrando snapshot — NO el board actual | 🟠 Alto |

---

## Tabla de Riesgos

| ID | Área | Riesgo | Descripción | Prioridad | Justificación |
|----|------|--------|-------------|-----------|---------------|
| R-001 | SQLite / R2 Sync | 🔴 Crítico | Si la sincronización SQLite ↔ R2 falla, el replay es imposible para ejecuciones no locales | 1 | Es el pilar del replay. Sin datos de SQLite, no hay I/O de nodos ni snapshot |
| R-002 | Snapshot del Board | 🔴 Crítico | Si el snapshot no captura correctamente el estado del board, el replay muestra información incorrecta | 1 | El Developer notó que era provisional inicialmente. Se resolvió con nueva tabla SQLite (2026-08-04) pero necesita validación |
| R-003 | Concurrencia | 🔴 Crítico | Dos ejecuciones simultáneas pueden crear snapshots corruptos o estados huérfanos | 2 | AC 5-7 tocan esto. Overlap con IONF-1248 pero validación básica necesaria aquí |
| R-004 | Multi-tenant / URL | 🟠 Alto | URL compartible de ejecución podría exponer datos entre companies si el permiso no se valida server-side | 2 | La pantalla tiene URL propia — vector de acceso directo sin navegación natural |
| R-005 | Retención 7 días | 🟠 Alto | Mensajes incorrectos sobre disponibilidad del detalle confunden al usuario | 3 | Distinguir "expiró" vs "nunca se guardó" es un requerimiento explícito del UX Research |
| R-006 | Consistencia Dev/Live | 🟠 Alto | El mismo error puede reportarse diferente en Dev vs Live (problema documentado en UX Research) | 3 | Es el problema de confianza más grave del sistema actual según UX Research |
| R-007 | Canvas Read-only | 🟠 Alto | El visor reutilizado puede no funcionar correctamente con datos de snapshot (vs datos del board actual) | 4 | Visor existente vs datos nuevos. La posición de nodos usa auto-layout de VueFlow (provisional) |
| R-008 | Ejecuciones Legacy | 🟠 Alto | Ejecuciones anteriores al deploy no tienen datos de replay — el usuario podría confundirse | 4 | Necesita comunicación clara de que solo ejecuciones nuevas soportan replay |
| R-009 | Permisos | 🟡 Medio | DELETE_EXECUTION requiere permiso propio + confirmación. Verificar que la nueva vista respeta esto | 5 | Permisos existentes pero aplicados en contexto nuevo |
| R-010 | Performance / Payload | 🟡 Medio | Los datos I/O de nodos pueden ser muy grandes. ¿Se truncan? ¿Paginan? | 5 | UX Research menciona "mostrar recortados con opción de ver completos" |
| R-011 | Filtros / Paginación | 🟡 Medio | Filtros y paginación deben ajustarse solos ante valores fuera de rango | 6 | Requisito del UX Research — "ajustarse solos en lugar de fallar" |
| R-012 | Botón de Descarga | 🟡 Medio | AC-12 surgió del prototype review — puede no estar implementado aún | 6 | Sugerencia del prototype review, estado de implementación desconocido |
| R-013 | Accesibilidad | 🟡 Medio | Color solo no alcanza para estados de nodos — necesita iconos | 6 | Requisito explícito del UX Research por accesibilidad |

---

## Edge Cases Identificados

### Replay / Snapshot
1. **EC-01**: Board ejecutado con nodos que ya no existen en la versión actual
2. **EC-02**: Ejecución de un board que fue eliminado después de la ejecución
3. **EC-03**: Snapshot de board con muchos nodos (50+) — ¿cómo se renderiza el auto-layout?
4. **EC-04**: Board ejecutado en Dev con nodos intermedios sin datos de resultado (ejecución parcial)
5. **EC-05**: Ejecución que falló en el primer nodo — ¿qué muestra el canvas?

### SQLite / R2
6. **EC-06**: Archivo SQLite no disponible en R2 ni localmente — ¿qué mensaje muestra?
7. **EC-07**: Archivo SQLite corrupto o parcialmente descargado — ¿hay manejo de error?
8. **EC-08**: Descarga simultánea del mismo archivo SQLite desde R2 por dos requests
9. **EC-09**: Cron de limpieza elimina archivo temporal mientras se está consultando

### Multi-tenant / Permisos
10. **EC-10**: Acceso por URL directa a ejecución de otra company
11. **EC-11**: Usuario sin permiso `READ_EXECUTION` accede a URL de ejecución
12. **EC-12**: Eliminar ejecución sin permiso `DELETE_EXECUTION`

### Retención / Expiración
13. **EC-13**: Ejecución exactamente al borde del día 7 — ¿el corte es preciso?
14. **EC-14**: Ejecución legacy (pre-deploy) sin datos de snapshot — ¿mensaje correcto?
15. **EC-15**: Ejecución en curso visible — ¿indicador de actividad + opción actualizar?

### Concurrencia / Lifecycle
16. **EC-16**: Doble clic rápido en botón de ejecutar — ¿el bloqueo es instantáneo?
17. **EC-17**: Ejecución que queda en estado "en curso" indefinidamente (timeout?)
18. **EC-18**: Board sin ninguna ejecución — ¿mensaje empty state correcto?

---

## Preguntas para el Developer

### [LÓGICA DE NEGOCIO]
1. **Multi-tenant en URLs**: ¿La nueva URL de ejecución (`/executions/:id`) valida server-side que el `execution_id` pertenece a la company del usuario autenticado?
2. **Snapshot scope**: ¿El snapshot guarda solo la estructura del board (nodos + edges + posiciones) o también incluye configuración de nodos (credenciales, parámetros)?
3. **Overlap con IONF-1248**: Los AC de concurrencia (no dos ejecuciones simultáneas), bloqueo de botón y lifecycle — ¿se implementaron en este ticket o se delegan completamente a IONF-1248?

### [EDGE CASES]
4. **Nodos eliminados**: Si un board fue ejecutado y después se eliminó un tipo de nodo del catálogo, ¿cómo se renderiza ese nodo en el replay?
5. **SQLite no disponible**: ¿Qué mensaje exacto ve el usuario cuando el archivo SQLite no se puede recuperar de R2?
6. **Datos grandes**: ¿Cómo se manejan nodos cuyo output JSON es muy grande (>1MB)? ¿Se trunca, se pagina, se limita?
7. **Auto-layout**: El UX Research mencionó que la posición de nodos usa VueFlow auto-layout. ¿Se resolvió esto con la nueva tabla de snapshot?

### [INTEGRACIÓN]
8. **R2 fallback**: Si R2 no responde, ¿hay fallback a archivos locales? ¿O la vista simplemente muestra "no disponible"?
9. **Cron de limpieza**: ¿Cuál es la frecuencia del cron? ¿Existe riesgo de que limpie archivos mientras se consultan?
10. **Logs de ejecución**: ¿Los logs que se muestran son los del `flow_logger.go` existente o se creó un nuevo sistema de logging?

### [UI / UX]
11. **Botón de descarga (AC-12)**: ¿Ya fue implementado o es solo la sugerencia del prototype review?
12. **Estados de nodos**: ¿Los estados del canvas (exitoso/error/omitido/sin datos) usan solo color o también iconos como sugiere el UX Research?

---

## Contexto del Ticket (ClickUp)

### Divergencias detectadas entre descripción y comentarios
- **Descripción tiene 2 AC** — los comentarios del Developer expandieron a 12 requisitos funcionales
- **Descripción no menciona** retención de 7 días, snapshot de board, sincronización R2, ejecuciones legacy
- **AC 5-7 (concurrencia/lifecycle)** — la descripción los incluye pero luego dice que se gestionan en IONF-1248

### Últimas decisiones relevantes
1. **Prototype aprobado** (2026-08-24): Las vistas e implementación fueron aprobadas
2. **R2 resuelto** (2026-08-06): El servicio de sincronización de archivos SQLite con R2 fue implementado
3. **Snapshot implementado** (2026-08-04): Nueva tabla SQLite para guardar flow con datos de reconstrucción
4. **Solo ejecuciones nuevas** (2026-08-04): Las antiguas no tendrán vista replay

---

## Recomendación

### Áreas que requieren más atención

1. **🔴 Sincronización SQLite ↔ R2** (R-001): Es el pilar del replay. Validar que archivos se recuperan correctamente, que el cache temporal funciona, y que el cron de limpieza no causa condiciones de carrera.

2. **🔴 Snapshot del Board** (R-002): Verificar que la nueva tabla SQLite captura fielmente el estado del board ejecutado. Especial atención a nodos con tipos que ya no existen o boards eliminados.

3. **🔴 Concurrencia** (R-003): Aunque el overlap con IONF-1248 crea ambigüedad sobre el scope, el bloqueo del botón y la prevención de ejecuciones simultáneas son requisitos funcionales de este ticket.

4. **🟠 Multi-tenant en URL** (R-004): La pantalla con URL propia es un vector de acceso directo. Validar que permisos se verifican server-side, no solo client-side.

5. **🟠 Retención y mensajes** (R-005): Distinguir "expiró" vs "no disponible" es un requerimiento explícito. El usuario confía en lo que el sistema le dice — mensajes incorrectos erosionan esa confianza.
