# Acceptance Criteria Consolidados — 86e2ak75f

> Standardize Execution UI & Build Execution Replay Engine

---

## AC Originales (del ticket)

### AC-1: Consistencia visual Dev/Live
```gherkin
Given que existe una ejecución disponible para inspección en Dev y Live
When el usuario abre el detalle o modal de la ejecución en cualquiera de los dos entornos
Then la interfaz mantiene la misma estructura, estilos y jerarquía visual
And presenta los estados y datos de ejecución con los mismos componentes visuales.
```
**Fuente**: Descripción original del ticket
**¿Verificable?**: ✅ — Se puede comparar visualmente Dev vs Live
**¿Completo?**: ⚠️ Parcial — No especifica QUÉ componentes deben ser idénticos
**¿Ambiguo?**: ⚠️ "Misma estructura, estilos y jerarquía" es subjetivo

### AC-2: Inspección desde historial con canvas read-only
```gherkin
Given que existen registros en Company > Execution History
When el usuario selecciona una ejecución terminada
Then el sistema carga el lienzo del flujo tal como se ejecutó en ese instante de tiempo (modo lectura)
And los nodos muestran indicadores visuales de su resultado individual (verde = éxito, rojo = error, gris = omitido)
And al seleccionar cualquier nodo, se abre el panel de inspección mostrando la estructura exacta de datos de entrada (Input JSON) y salida (Output JSON).
```
**Fuente**: Descripción original del ticket, AMPLIADO por UX Research (2026-07-30)
**¿Verificable?**: ✅ — Acciones y resultados claros
**¿Completo?**: ❌ — Falta especificar los 3 puntos de acceso y la URL compartible
**¿Ambiguo?**: ⚠️ "Tal como se ejecutó" requiere snapshot — resuelto en comentarios (2026-08-04)

---

## AC Derivados de Comentarios del Developer (Propuestos como AC)

### AC-3: Retención de 7 días — Vista reducida para ejecuciones expiradas
```gherkin
Given que existe una ejecución con más de 7 días de antigüedad
When el usuario accede a su detalle
Then el sistema muestra: estado, duración y errores generales
And muestra un aviso indicando que el detalle expiró y desde cuándo
And NO muestra el canvas replay, I/O de nodos ni logs.
```
**Fuente**: UX Research Report — Gustavo Mamani (2026-07-30)
**Justificación**: Retención de 7 días es una política definida. El usuario debe saber por qué no ve el detalle.

### AC-4: Mensajes diferenciados — "expiró" vs "no disponible"
```gherkin
Given que una ejecución no tiene detalle disponible
When el sistema presenta el estado al usuario
Then diferencia entre:
  - "El detalle de esta ejecución expiró el [fecha]" (para ejecuciones > 7 días)
  - "El detalle de esta ejecución no está disponible" (para ejecuciones que nunca guardaron detalle)
And NUNCA dice que expiró algo que en realidad no se guardó.
```
**Fuente**: UX Research Report — "No decir que expiró, porque no es cierto" (2026-07-30)
**Justificación**: El UX Research identifica esto como problema de confianza.

### AC-5: Concurrencia — No dos ejecuciones simultáneas por board
```gherkin
Given que un board tiene una ejecución activa
When un usuario intenta iniciar una segunda ejecución del mismo board
Then el sistema rechaza la segunda ejecución
And muestra un mensaje indicando que ya hay una ejecución en curso.
```
**Fuente**: UX Research Report — "Validaciones necesarias" (2026-07-30)
**Nota**: ⚠️ Posible overlap con IONF-1248

### AC-6: Botón de ejecutar — Bloqueo inmediato
```gherkin
Given que el usuario está en la vista de un board
When presiona el botón de ejecutar
Then el botón se bloquea inmediatamente (antes de contactar al servidor)
And muestra un indicador visual de que la ejecución está en proceso.
```
**Fuente**: UX Research Report — "El botón de ejecutar se bloquea apenas se presiona" (2026-07-30)
**Nota**: ⚠️ Posible overlap con IONF-1248

### AC-7: Lifecycle — Toda ejecución termina en estado final
```gherkin
Given que una ejecución fue iniciada
When la ejecución se procesa (éxito, error o timeout)
Then SIEMPRE termina en un estado final (completed, error, stopped)
And NUNCA queda indefinidamente en estado "en curso".
```
**Fuente**: UX Research Report — "Toda ejecución termina en un estado final" (2026-07-30)
**Nota**: ⚠️ Posible overlap con IONF-1248

### AC-8: Metadata de ejecución — Modo y tipo de trigger
```gherkin
Given que se ejecuta un board
When la ejecución se registra en el sistema
Then incluye el modo de ejecución (Dev / Live)
And incluye el tipo de trigger (manual / schedule / webhook / subflow).
```
**Fuente**: Prototype Progress Report — Gustavo Mamani (2026-08-04) — "Se agregaron columnas en la tabla 'executions' para identificar si una ejecución se hizo en modo live o dev e identificar quién realizó la ejecución"

### AC-9: Snapshot del board — Reconstrucción exacta
```gherkin
Given que un board se ejecuta
When la ejecución se registra
Then el sistema guarda un snapshot del flow con los datos necesarios para su reconstrucción en una tabla separada de SQLite
And el snapshot se omite datos de configuración redundantes (ya están en tabla nodes)
And al acceder al replay, se reconstruye el board tal como fue ejecutado (no el estado actual).
```
**Fuente**: Prototype Progress Report — Gustavo Mamani (2026-08-04) — "Se agrego una nueva tabla en el snapshot sqlite para guardar el flow con los datos necesarios para su reconstrucción"

### AC-10: Ejecuciones legacy — Sin vista replay
```gherkin
Given que existen ejecuciones anteriores al deployment de esta feature
When el usuario accede a su detalle
Then el sistema indica que la vista de replay no está disponible para esta ejecución
And muestra la información básica disponible (estado, duración, errores)
And NO muestra error técnico ni pantalla en blanco.
```
**Fuente**: Prototype Progress Report — Gustavo Mamani (2026-08-04) — "Solamente las nuevas ejecuciones se podrán visualizar en esta vista"

### AC-11: SQLite de R2 — Recuperación con cache
```gherkin
Given que una ejecución tiene su archivo SQLite almacenado en R2 (no local)
When el usuario solicita ver el detalle de la ejecución
Then el sistema descarga el archivo SQLite desde R2
And lo almacena en un directorio temporal como cache
And un cron job limpia automáticamente los archivos temporales
And no se descargan repetidamente archivos ya cacheados.
```
**Fuente**: Prototype Report — Gustavo Mamani (2026-08-06) — "Se implemento un nuevo servicio para obtener archivos que se hayan sincronizado con el bucket de R2"

### AC-12: Botón de descarga — Registro de ejecuciones
```gherkin
Given que el usuario está en la vista de historial de ejecuciones
When desea obtener el registro de ejecuciones
Then existe un botón de descarga que permite obtener el registro.
```
**Fuente**: Prototype Review (2026-08-24) — "Agregar un botón de descarga del registro de ejecuciones"
**Nota**: Estado de implementación pendiente de confirmar

---

## AC de Puntos de Acceso (Derivados del AC-2 ampliado)

### AC-2a: Acceso desde lista de boards
```gherkin
Given que el usuario está en la vista de lista de boards
When abre el menú contextual de un board
Then existe una opción para ver el historial de ejecuciones de ese board
And al seleccionarla, navega a la vista de ejecuciones filtrada por ese board.
```
**Fuente**: UX Research Report (2026-07-30) — "Desde la lista de boards, con una opción en el menú de cada board"

### AC-2b: Acceso desde el board editor
```gherkin
Given que el usuario tiene un board abierto en el editor
When busca acceder al historial de ejecuciones
Then existe un toggle o tab entre "Editor" y "Ejecuciones"
And al seleccionar "Ejecuciones", muestra el historial de ese board.
```
**Fuente**: UX Research Report (2026-07-30) — "Desde el board abierto, con un cambio entre Editor y Ejecuciones"

### AC-2c: URL compartible
```gherkin
Given que el usuario está viendo el detalle de una ejecución
When copia la URL del navegador
Then la URL es directa y compartible (otro usuario puede acceder con la misma URL)
And el botón "atrás" del navegador funciona con normalidad.
```
**Fuente**: UX Research Report (2026-07-30) — "La vista tiene dirección propia, así que el enlace de una ejecución puntual se puede compartir"

---

## AC Rechazados o Diferidos

| AC | Razón | Fuente |
|----|-------|--------|
| Notificaciones de fallo | Fuera de alcance — decisión del UX Research | UX Research 2026-07-30 |
| Reintentar o reejecutar desde la vista | Fuera de alcance — decisión del UX Research | UX Research 2026-07-30 |
| Comparar dos ejecuciones | Fuera de alcance — decisión del UX Research | UX Research 2026-07-30 |
| Exportar el detalle | Fuera de alcance — decisión del UX Research | UX Research 2026-07-30 |
| Ampliar retención más allá de 7 días | Fuera de alcance — decisión de infraestructura | UX Research 2026-07-30 |
| Copiar flow al editor | Fuera de alcance v1 — riesgo de sobrescribir board en producción | UX Research 2026-07-30 |

---

## Transformación AC → Casos de Test (Preview)

| AC | Caso Happy Path | Casos Edge | Caso Negativo |
|----|----------------|------------|---------------|
| AC-1 | Abrir misma ejecución en Dev y Live, comparar UI | Ejecución con solo Dev o solo Live | N/A |
| AC-2 | Seleccionar ejecución completada → ver canvas con colores | Ejecución con 50+ nodos, ejecución con sub-flows | Seleccionar ejecución inexistente |
| AC-2a | Menú contextual de board → ver historial | Board sin ejecuciones | Board eliminado |
| AC-2b | Tab Editor → Ejecuciones en board abierto | Board recién creado sin ejecuciones | Usuario sin permiso READ_EXECUTION |
| AC-2c | Copiar URL → abrir en otra pestaña | URL de ejecución eliminada | URL de ejecución de otra company |
| AC-3 | Ver ejecución de 8 días → solo metadata | Ejecución en el límite exacto del día 7 | N/A |
| AC-4 | Ejecución expirada muestra "expiró" | Ejecución legacy sin snapshot muestra "no disponible" | Mensajes no se confunden |
| AC-5 | Intentar 2da ejecución → rechazada con mensaje | Dos usuarios diferentes ejecutan el mismo board | Primera ejecución termina justo cuando llega la segunda |
| AC-6 | Click en ejecutar → botón se bloquea visualmente | Doble clic rápido → solo una ejecución | Click + desconexión de red |
| AC-7 | Ejecución con error → estado final "error" | Ejecución que tarda mucho (timeout) | Nodo que nunca responde |
| AC-8 | Ejecutar manualmente en Dev → metadata correcta | Ejecutar via webhook en Live → metadata correcta | N/A |
| AC-9 | Ejecutar → snapshot guardado → replay coincide | Ejecutar board, modificar board, verificar replay muestra versión anterior | Board con nodos eliminados post-ejecución |
| AC-10 | Ver ejecución pre-deploy → mensaje informativo | Mezcla de ejecuciones nuevas y legacy en la lista | N/A |
| AC-11 | Ver ejecución con SQLite en R2 → descarga y muestra | SQLite no disponible en R2 ni local | R2 no responde (timeout) |
| AC-12 | Click botón descarga → se obtiene registro | Lista vacía → ¿botón activo? | N/A |

---

## Resumen

| Métrica | Valor |
|---------|-------|
| AC Originales | 2 |
| AC Derivados de Comentarios | 10 |
| Sub-ACs (puntos de acceso) | 3 |
| AC Rechazados/Diferidos | 6 |
| **Total AC para testing** | **15** (12 + 3 sub-ACs) |
| AC con overlap IONF-1248 | 3 (AC-5, AC-6, AC-7) |
