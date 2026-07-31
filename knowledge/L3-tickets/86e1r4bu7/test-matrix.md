# Test Matrix — IONF-1076 / 86e1r4bu7 (Community Templates) — Ronda 2

## Resumen
- Total de TCs: 39
  - Smoke: 2
  - Happy Path: 8
  - Re-verificación OBS (🔴 Urgent): 6
  - Re-verificación OBS (🟡 High): 10
  - Edge Cases: 4
  - Negativos: 2
  - Regresión: 2
  - Code Review: 5 (RISK: 3, EDGE: 2)
- Origen: Ticket AC: 10, Observaciones Ronda 1: 16, QA adicional: 8, Code Review: 5

---

## Suite 1 — Smoke

| TC ID | Tipo | Caso de Test | Pasos | Expected | Prioridad | Estado |
|-------|------|-------------|-------|----------|-----------|--------|
| TC-001 | Smoke | Templates accesible desde Admin | 1) Login como Admin (`admin@shipedge.com`)<br>2) Navegar a sección Templates en sidebar<br>3) Verificar que la tabla de templates carga | La tabla de templates se renderiza con datos, sin errores en consola | 🔴 | ⬜ Pendiente |
| TC-002 | Smoke | Templates accesible desde Tenant | 1) Login como Company (`skuanquis@gmail.com`)<br>2) Navegar a sección Templates en sidebar<br>3) Verificar que la galería carga | La galería de templates se renderiza con cards visibles, sin errores en consola | 🔴 | ⬜ Pendiente |

## Suite 2 — Happy Path

| TC ID | Tipo | Caso de Test | Pasos | Expected | Prioridad | Estado |
|-------|------|-------------|-------|----------|-----------|--------|
| TC-003 | HP | Admin: Crear template tipo Flow | 1) Admin Login<br>2) Templates > Create template<br>3) Seleccionar compañía<br>4) Seleccionar un flow con nodos<br>5) Completar campos requeridos<br>6) Guardar | Template creado exitosamente, aparece en la tabla con estado correcto | 🔴 | ⬜ Pendiente |
| TC-004 | HP | Admin: Crear template tipo PDF | 1) Admin Login<br>2) Templates > Create template<br>3) Seleccionar compañía<br>4) Seleccionar tipo PDF<br>5) Completar campos<br>6) Guardar | Template PDF creado, visible en tabla | 🔴 | ⬜ Pendiente |
| TC-005 | HP | Admin: Editar template existente | 1) Admin Login<br>2) Templates > seleccionar template<br>3) Editar campos permitidos (nombre, descripción, categorías, estado)<br>4) Guardar | Cambios persistidos correctamente, campos no editables no modificables | 🔴 | ⬜ Pendiente |
| TC-006 | HP | Admin: Eliminar template | 1) Admin Login<br>2) Templates > seleccionar template<br>3) Eliminar<br>4) Confirmar | Template eliminado, no aparece en tabla ni en marketplace tenant | 🟠 | ⬜ Pendiente |
| TC-007 | HP | Admin: Asignar categorías con color | 1) Admin Login<br>2) Templates > seleccionar template > Editar<br>3) Asignar 2-3 categorías con colores<br>4) Guardar | Categorías asignadas visibles como chips con color en tabla y en card del tenant | 🟠 | ⬜ Pendiente |
| TC-008 | HP | Tenant: Buscar template en marketplace | 1) Company Login<br>2) Templates > galería<br>3) Usar buscador con texto parcial de un template conocido | Resultados filtrados correctamente según búsqueda | 🔴 | ⬜ Pendiente |
| TC-009 | HP | Tenant: Preview de template | 1) Company Login<br>2) Templates > galería<br>3) Click en un template<br>4) Verificar drawer de preview | El drawer muestra información del template: nombre, descripción, apps usadas, PDFs asociados | 🟠 | ⬜ Pendiente |
| TC-010 | HP | Tenant: Instalar template con wizard | 1) Company Login<br>2) Templates > galería > seleccionar template<br>3) Click en instalar/usar<br>4) Completar wizard (mapeo conexiones)<br>5) Confirmar instalación | Template instalado: copia editable del flow en la cuenta del usuario. PDFs clonados con IDs remapeados. Toast de confirmación visible | 🔴 | ⬜ Pendiente |

## Suite 3 — Re-verificación OBS 🔴 Urgent (Ronda 1)

| TC ID | Tipo | OBS Ref | Caso de Test | Pasos | Expected | Prioridad | Estado |
|-------|------|---------|-------------|-------|----------|-----------|--------|
| TC-OBS-01 | Re-test | OBS-01 | Buscador de compañías funcional | 1) Admin > Templates > Create template<br>2) Localizar campo de búsqueda de compañías<br>3) Ingresar nombre de una compañía conocida | El buscador filtra en tiempo real las compañías según texto ingresado. Resultados coincidentes aparecen inmediatamente | 🔴 | ⬜ Pendiente |
| TC-OBS-02 | Re-test | OBS-02 | Validación de JSON sin nodos | 1) Admin > Templates > Crear template<br>2) Subir/seleccionar un board sin nodos en el campo JSON<br>3) Intentar guardar | El sistema muestra alerta que impide importar flows sin nodos ejecutables. No se crea template vacío | 🔴 | ⬜ Pendiente |
| TC-OBS-03 | Re-test | OBS-03 | Validación de estado y campos en PDF | 1) Admin > Templates > Crear template tipo PDF<br>2) No agregar ningún campo al template<br>3) Seleccionar estado Draft<br>4) Intentar guardar | El sistema impide la creación de templates PDF sin campos configurados. Mensaje de error claro | 🔴 | ⬜ Pendiente |
| TC-OBS-04 | Re-test | OBS-04 | Filtro de activos funcional | 1) Admin > Templates<br>2) Aplicar filtro seleccionando "Activos"<br>3) Verificar resultados<br>4) Cambiar a "Inactivos"<br>5) Verificar resultados | El filtro aplica correctamente: solo muestra templates del estado seleccionado. Los resultados se actualizan inmediatamente | 🔴 | ⬜ Pendiente |
| TC-OBS-05 | Re-test | OBS-05 | Campos no editables con estilo diferenciado | 1) Admin > Templates > seleccionar template > Editar<br>2) Identificar campos no editables<br>3) Verificar estilo visual diferenciado | Los campos no editables tienen fondo deshabilitado, sin cursor de texto, sin borde activo. No se puede intentar modificarlos | 🔴 | ⬜ Pendiente |
| TC-OBS-06 | Re-test | OBS-06 | Botón cerrar modal con nombres largos | 1) Admin > Templates > Crear template<br>2) Seleccionar un board con nombre extremadamente largo (>60 chars)<br>3) Intentar cerrar el modal usando el botón X | El botón de cierre permanece visible, correctamente posicionado y funcional independientemente del contenido | 🔴 | ⬜ Pendiente |

## Suite 4 — Re-verificación OBS 🟡 High (Ronda 1)

| TC ID | Tipo | OBS Ref | Caso de Test | Pasos | Expected | Prioridad | Estado |
|-------|------|---------|-------------|-------|----------|-----------|--------|
| TC-OBS-07 | Re-test | OBS-07 | Modal creación no se rompe con nombres largos | 1) Admin > Templates > Crear template<br>2) Seleccionar board con nombre >60 chars + nombre PDF largo<br>3) Verificar estado visual del modal | El modal mantiene su estructura. Textos extensos se truncan con ellipsis. Elementos interactivos accesibles | 🟠 | ⬜ Pendiente |
| TC-OBS-08 | Re-test | OBS-08 | Tabla no se estira con nombres largos | 1) Admin > Templates<br>2) Verificar template con nombre de board/PDF extenso<br>3) Verificar columnas de la tabla | Columnas mantienen ancho fijo. Texto truncado con ellipsis. Tooltip al hover muestra nombre completo. Sin scroll horizontal | 🟠 | ⬜ Pendiente |
| TC-OBS-09 | Re-test | OBS-09 | Card en tenant no se rompe con nombres largos | 1) Company Login<br>2) Templates > galería<br>3) Localizar template con nombre extenso<br>4) Verificar estructura del card | Card mantiene diseño y proporciones. Texto truncado. Botones y etiquetas visibles y accesibles | 🟠 | ⬜ Pendiente |
| TC-OBS-10 | Re-test | OBS-10 | Botón de recarga en tabla admin | 1) Admin > Templates<br>2) Buscar botón de recarga en la barra de acciones<br>3) Realizar operación (crear/eliminar template)<br>4) Usar botón de recarga | Existe botón de recarga visible. Al usarlo, la tabla se actualiza sin recargar página completa. Filtros se mantienen | 🟠 | ⬜ Pendiente |
| TC-OBS-11 | Re-test | OBS-11 | Selector de compañías muestra todos los registros | 1) Admin > Templates > Crear template<br>2) Desplegar selector de compañías<br>3) Verificar cantidad de registros | El selector muestra todas las compañías con scroll interno. No hay límite artificial de 5. Sin espacio en blanco al final | 🟠 | ⬜ Pendiente |
| TC-OBS-12 | Re-test | OBS-12 | Alerta para flows sin nodos (nuevo enfoque) | 1) Admin > Templates > Crear template<br>2) Revisar listado de flows<br>3) Seleccionar un flow sin nodos<br>4) Verificar alerta | El sistema muestra alerta que impide importar flows sin nodos ejecutables. El flow aparece en el listado pero no se permite crear template con él | 🟠 | ⬜ Pendiente |
| TC-OBS-13 | Re-test | OBS-13 | Límite de tags por card | 1) Admin > Templates > editar template<br>2) Agregar 10+ tags<br>3) Guardar<br>4) Revisar card en catálogo tenant | Card muestra número máximo de tags con indicador "+N más" o expansión. Sin desbordamiento del diseño | 🟠 | ⬜ Pendiente |
| TC-OBS-14 | Re-test | OBS-14 | Expandir/colapsar tags en card | 1) Tenant > catálogo de templates<br>2) Localizar card con múltiples tags<br>3) Buscar control expandir/colapsar | Existe control visual para expandir/colapsar bloque de tags. Alternar entre vista colapsada y expandida funciona sin romper layout | 🟠 | ⬜ Pendiente |
| TC-OBS-15 | Re-test | OBS-15 | Tags con nombre largo truncados | 1) Admin > Templates > editar template<br>2) Agregar tag con nombre >30 caracteres<br>3) Guardar<br>4) Revisar card | Tag truncada con ellipsis en chip. Tooltip al hover muestra nombre completo. Card no se deforma | 🟠 | ⬜ Pendiente |
| TC-OBS-16 | Re-test | OBS-16 | Labels correctos en idioma español | 1) Configurar idioma en español<br>2) Tenant > catálogo de templates<br>3) Comparar posición de labels con vista en inglés | Labels correctamente posicionados y alineados en español. Diseño flexible absorbe mayor longitud del texto | 🟠 | ⬜ Pendiente |

## Suite 5 — Edge Cases

| TC ID | Tipo | Caso de Test | Pasos | Expected | Prioridad | Estado |
|-------|------|-------------|-------|----------|-----------|--------|
| TC-EC-01 | EC | Template con JSON vacío | 1) Admin > Templates > Crear template<br>2) Intentar subir JSON completamente vacío `{}`<br>3) Intentar guardar | Sistema rechaza con mensaje claro. No se crea template | 🟠 | ⬜ Pendiente |
| TC-EC-02 | EC | Instalar mismo template dos veces | 1) Company Login<br>2) Templates > instalar template A<br>3) Volver a galería<br>4) Intentar instalar template A nuevamente | Sistema permite o maneja correctamente la duplicación. No errores. Si permite, crea segunda copia independiente | 🟠 | ⬜ Pendiente |
| TC-EC-03 | EC | Template con nodos pdfme_schema_id → clonación PDFs | 1) Admin: crear template con flow que usa nodos `pdfme_schema_id`<br>2) Tenant: instalar template<br>3) Verificar que PDFs fueron clonados<br>4) Verificar que IDs fueron remapeados en el flow instalado | PDFs clonados correctamente en la cuenta del tenant. IDs en nodos actualizados al nuevo PDF. Toast de confirmación | 🔴 | ⬜ Pendiente |
| TC-EC-04 | EC | toBase64Raw devuelve resultado correcto | 1) En un flow, usar expresión `{{toBase64Raw('hello')}}`<br>2) Ejecutar el nodo<br>3) Verificar resultado | Salida esperada: `aGVsbG8` (Base64 URL-safe sin padding) | 🟡 | ⬜ Pendiente |

## Suite 6 — Negativos

| TC ID | Tipo | Caso de Test | Pasos | Expected | Prioridad | Estado |
|-------|------|-------------|-------|----------|-----------|--------|
| TC-NEG-01 | NEG | Template inactivo no visible en marketplace | 1) Admin: cambiar template a estado inactivo<br>2) Company Login<br>3) Templates > galería<br>4) Buscar el template inactivo | Template inactivo NO aparece en la galería del tenant | 🟠 | ⬜ Pendiente |
| TC-NEG-02 | NEG | Credenciales no heredadas al instalar | 1) Verificar template original usa conexiones con credenciales<br>2) Company Login > instalar template<br>3) Verificar configuración del flow instalado | El flow instalado NO reutiliza credenciales del template original. Solicita al usuario configurar sus propias credenciales | 🔴 | ⬜ Pendiente |

## Suite 7 — Regresión

| TC ID | Tipo | Caso de Test | Pasos | Expected | Prioridad | Estado |
|-------|------|-------------|-------|----------|-----------|--------|
| TC-REG-01 | REG | Boards existentes siguen funcionando | 1) Company Login<br>2) Workflows > abrir un board existente<br>3) Verificar que carga y funciona correctamente | Boards existentes cargan sin errores. No hay impacto del feature de templates | 🟠 | ⬜ Pendiente |
| TC-REG-02 | REG | PDF Templates existentes no afectados | 1) Company Login<br>2) PDF Templates > abrir template existente<br>3) Verificar que funciona correctamente | PDF templates pre-existentes funcionan sin impacto | 🟠 | ⬜ Pendiente |

## Suite 8 — Code Review (Bug Hunting)

### Riesgos (RISK-CR)

| TC ID | Tipo | Origen | Caso de Test | Pasos | Expected | Prioridad | Estado |
|-------|------|--------|-------------|-------|----------|-----------|--------|
| TC-CR-001 | EC | RISK-CR-001 | Búsqueda + paginación de compañías funciona correctamente (params como ref) | 1) Admin Login<br>2) Templates > Create template > From Company<br>3) Verificar que la lista de compañías carga<br>4) Buscar una compañía por nombre parcial<br>5) Verificar resultados filtrados<br>6) Navegar entre páginas de compañías | Los parámetros de búsqueda se envían correctamente. La paginación funciona sin errores. Los resultados reflejan el filtro aplicado | 🟠 | ⬜ Pendiente |
| TC-CR-002 | EC | RISK-CR-002 | Opciones de gestión para templates community (delete/toggle bloqueados) | 1) Admin Login<br>2) Templates > localizar un template con source "Company" (icon building azul)<br>3) Click en menú de contexto (3 puntos)<br>4) Verificar opciones disponibles<br>5) Verificar si el toggle de activo/inactivo funciona | Templates community solo muestran opción "Edit" (no Delete). Toggle disabled. Verificar si es comportamiento intencional | 🟠 | ⬜ Pendiente |
| TC-CR-003 | EC | RISK-CR-003 | No hay textos hardcoded en inglés con idioma español | 1) Configurar idioma en español<br>2) Admin > Templates<br>3) Verificar todos los textos visibles (fechas, labels, tooltips)<br>4) Tenant > catálogo de templates<br>5) Verificar todos los textos visibles | Todos los textos están traducidos al español. No aparece "Today", "Yesterday", "d ago" u otros textos en inglés | 🟡 | ⬜ Pendiente |

### Edge Cases (EDGE-CR)

| TC ID | Tipo | Origen | Caso de Test | Pasos | Expected | Prioridad | Estado |
|-------|------|--------|-------------|-------|----------|-----------|--------|
| TC-CR-004 | EC | EDGE-CR-001 | Toggle rápido activo/inactivo con verificación de revert | 1) Admin Login<br>2) Templates > localizar template admin-created<br>3) Toggle activo → inactivo<br>4) Esperar 1 segundo<br>5) Toggle inactivo → activo inmediatamente<br>6) Verificar estado final | El toggle refleja el estado correcto del servidor. No hay parpadeo visual ni estado inconsistente | 🟡 | ⬜ Pendiente |
| TC-CR-005 | EC | EDGE-CR-002 | Crear dos templates con mismo título | 1) Admin Login<br>2) Templates > Create template > JSON<br>3) Crear template con título "Test Duplicate"<br>4) Crear otro template con mismo título "Test Duplicate"<br>5) Verificar respuesta | El sistema rechaza la duplicación con mensaje 409 Conflict O permite la creación con diferenciación. No se crea registro huérfano | 🟡 | ⬜ Pendiente |
