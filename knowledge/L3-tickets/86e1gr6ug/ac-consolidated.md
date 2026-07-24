# Acceptance Criteria Consolidados — 86e1gr6ug

> Módulo principal: boards | Módulo secundario: pdf-templates | Track: Discovery
> Generado: 2026-06-08 | Última actualización: 2026-06-08 15:42 (formato Gherkin)
> Aprobación QA: Pendiente

---

## Fuentes de AC

| Fuente | Fecha | Autor | Contenido |
|--------|-------|-------|-----------|
| Descripción del ticket | 2026-05-21 | Marcel Herrera Rendón | 3 mejoras genéricas (IonPDF, previsualizaciones, estética) |
| Comentario EPIC 1 | 2026-06-03 | Jose Enrique Ricaldi | Flow Execution Telemetry — architecture brief |
| Comentario EPIC 2 | 2026-06-03 | Jose Enrique Ricaldi | PDF Templates List + Generation Telemetry — architecture brief |
| **Epic Update** | **2026-06-08** | **Jose Enrique Ricaldi** | **Desglose técnico completo: Unified Search, Clone nativo, Payload Diet, FTS, A11y, Dark Mode, bug fixes** |
| Decisión QA Engineer | 2026-06-08 | Steve Nina | Tooltips y Responsividad dentro del scope |

> ⚠️ El Epic Update (2026-06-08) expandió significativamente el scope original.
> ~73 archivos tocados (35 frontend, 9 Laravel, 29 Go) en 8+ pantallas.

---

## EPIC 1 — Flow Execution Telemetry (Boards "Last Run")

### AC-1: Badge de estado de última ejecución en la lista de Boards

```gherkin
Feature: Badge de estado de última ejecución

  Scenario: Flow con ejecución exitosa muestra badge completed
    Given un usuario con permiso "READ_BOARD" está autenticado
    And existe un flow cuya última ejecución finalizó con todos los nodos exitosos
    When el usuario navega a "/workflows"
    Then el flow muestra un badge visual con runState "completed"
    And el badge tiene severidad de éxito (color verde)

  Scenario: Flow con falla parcial muestra badge warning
    Given un usuario con permiso "READ_BOARD" está autenticado
    And existe un flow cuya última ejecución finalizó con al menos un nodo en error pero el flow completó
    When el usuario navega a "/workflows"
    Then el flow muestra un badge visual con runState "warning"
    And el badge tiene severidad de advertencia (StatusWarning)

  Scenario: Flow con error total muestra badge error
    Given un usuario con permiso "READ_BOARD" está autenticado
    And existe un flow cuya última ejecución propagó un StatusError
    When el usuario navega a "/workflows"
    Then el flow muestra un badge visual con runState "error"
    And el badge tiene severidad de error (color rojo)
```

> Componentes: `FlowRunCell`, `FlowStatusBadge`
> Fuente: Comentario EPIC 1 (2026-06-03) + Epic Update (2026-06-08)

---

### AC-2: Separación de estado de usuario vs estado de ejecución (sin corrupción de grafo)

```gherkin
Feature: Separación de estado controlado por usuario vs badge de ejecución

  Scenario: Switch de estado y badge de ejecución son independientes
    Given un flow con status "activo" y última ejecución con runState "error"
    When el usuario visualiza la lista de boards
    Then el switch muestra "Activo"
    And el badge de ejecución muestra "error"
    And ambos indicadores son visualmente independientes

  Scenario: Cambiar estado no corrompe el grafo del flow
    Given un flow activo con nodos y edges configurados
    And la lista de boards usa payload reducido (Payload Diet)
    When el usuario hace click en el switch de FlowStatusBadge para cambiar a "Pausado"
    Then el frontend envía solo el campo de estado al backend
    And el grafo completo del flow no se sobrescribe con el payload reducido
    And el flow mantiene todos sus nodos y edges intactos
```

> Fuente: Epic Update (2026-06-08) — "switch de Activo/Pausado que envía solo el estado para no sobrescribir el grafo reducido"
> ⚠️ **Detalle crítico**: El payload reducido ya no incluye el grafo completo. Enviar el objeto completo sobrescribiría el grafo → corrupción de datos.

---

### AC-3: Puntero FK `last_execution_id` en tabla `flows`

```gherkin
Feature: Actualización del puntero last_execution_id

  Scenario: Puntero se actualiza después de una ejecución exitosa
    Given un flow existente en el esquema tenant
    When el motor Go ejecuta el flow y la ejecución finaliza con estado terminal
    And el motor realiza Save() de la ejecución final
    Then se ejecuta un UPDATE atómico en "flows.last_execution_id" con el ID de la ejecución completada
    And la actualización ocurre en el mismo esquema tenant

  Scenario: Ejecuciones de accounts no actualizan el puntero
    Given un flow ejecutándose en la ruta de accounts
    When la ejecución finaliza
    Then no se actualiza last_execution_id
    And la ruta de accounts queda fuera de alcance por usar un almacén separado
```

> Fuente: Comentario EPIC 1 (2026-06-03) + Epic Update (2026-06-08)

---

### AC-4: Estados terminales reales en Go (incluye `StatusWarning`)

```gherkin
Feature: Derivación de estados terminales significativos

  Scenario: Todos los nodos exitosos → estado completed
    Given un flow que ha terminado de ejecutarse
    And todos los nodos tienen resultado exitoso
    When el motor Go calcula el estado terminal
    Then el estado es "completed"

  Scenario: Al menos un nodo falló pero el flow completó → estado warning
    Given un flow que ha terminado de ejecutarse
    And al menos un nodo tiene StatusError pero el flow no se detuvo
    When el motor Go calcula el estado terminal
    Then el estado es "warning" (nuevo StatusWarning)

  Scenario: Propagación de error → estado error
    Given un flow que se detuvo por propagación de StatusError
    When el motor Go calcula el estado terminal
    Then el estado es "error"
```

> Fuente: Epic Update (2026-06-08) — "Se agregó el estado terminal StatusWarning"
> Reemplaza el estado anterior que siempre devolvía "completed".

---

### AC-5: Corrección de `execution_time` (bugfix)

```gherkin
Feature: Corrección del cálculo de execution_time

  Scenario: execution_time refleja la duración real de la ejecución
    Given un flow que se está ejecutando
    When la ejecución finaliza
    Then el campo "execution_time" contiene la duración real de la ejecución
    And el valor es mayor a 0 segundos

  Scenario: Ejecuciones previas al fix tienen execution_time incorrecto
    Given ejecuciones históricas previas al bugfix
    Then esas ejecuciones pueden tener execution_time cercano a 0s
    And esto es el comportamiento esperado del dato histórico (no se corrige retroactivamente)
```

> Causa raíz: El cálculo anterior comparaba `time.Now()` consigo mismo → siempre ~0s.
> Fuente: Epic Update (2026-06-08)

---

### AC-6: Payload Diet — Lista de Boards con grafo reducido

```gherkin
Feature: Optimización de payload en la lista de boards

  Scenario: La lista de flows retorna un payload reducido
    Given el frontend solicita la lista de flows via GET /flows
    When Laravel procesa la petición con FlowListResource
    Then la respuesta contiene solo "nodes:[id, type]" y "edges:[source, target]"
    And la respuesta contiene un objeto ligero "last_execution"
    And la respuesta NO contiene el JSONB pesado completo de los grafos

  Scenario: Eager-loading de lastExecution es eficiente
    Given una company con múltiples flows
    When se solicita la lista de flows
    Then el eager-loading de lastExecution se limita a columnas necesarias
    And se previenen consultas COUNT implícitas en toda la tabla
    And no hay N+1 queries
```

> Fuente: Epic Update (2026-06-08) — "Boards List Payload Diet"
> 🆕 AC NUEVO

---

### AC-7: Resiliencia ante poda de ejecuciones (`ON DELETE SET NULL`)

```gherkin
Feature: Manejo de poda de ejecuciones referenciadas

  Scenario: Ejecución referenciada es eliminada
    Given un flow con last_execution_id apuntando a una ejecución existente
    When la ejecución referenciada es eliminada (poda)
    Then la FK se activa con ON DELETE SET NULL
    And last_execution_id se establece en NULL
    And el flow no se elimina (no cascade delete)

  Scenario: Frontend maneja el puntero NULL post-poda
    Given un flow cuyo last_execution_id quedó en NULL por poda
    When el usuario visualiza la lista de boards
    Then el flow no muestra badge de ejecución o muestra estado neutro "sin datos"
    And la interfaz no crashea
```

> Fuente: Comentario EPIC 1 (2026-06-03)

---

### AC-8: Expansión de fila — Carga de flow completo y Used Apps

```gherkin
Feature: Carga de flow completo al expandir fila

  Scenario: Expandir fila solicita flow completo del HUB
    Given un flow visible en la lista de boards (con payload reducido)
    When el usuario hace click en el chevron para expandir la fila
    Then el frontend solicita el flow completo del Go HUB (no el payload reducido)
    And el FlowPreviewDrawer muestra los detalles completos

  Scenario: Used Apps se separan en GLOBAL y TENANT
    Given un flow con nodos de connectors globales y de company
    When el usuario expande la fila del flow
    Then las secciones "GLOBAL" y "TENANT" apps used se muestran correctamente separadas

  Scenario: Flow sin apps muestra estado vacío
    Given un flow sin nodos de connectors
    When el usuario expande la fila
    Then la sección de apps used muestra un estado vacío apropiado
    And no crashea
```

> Componentes: `FlowPreviewDrawer`, `BoardDetailsCell`
> Fuente: Epic Update (2026-06-08) — "Used Apps Logic"
> 🆕 AC NUEVO

---

### AC-9: Flow Clone nativo (endpoint backend)

```gherkin
Feature: Clonación nativa de flows

  Scenario: Clonar flow exitosamente
    Given un flow existente con nodos y configuración
    When el usuario selecciona "Clonar" desde el FlowActionsMenu
    Then se invoca POST flows/{flow}/clone
    And Eloquent usa replicate() excluyendo referencias de tenant, commits y ejecuciones
    And el nuevo flow aparece en la lista de boards
    And el clon tiene last_execution_id = NULL
    And el clon no tiene historial de ejecuciones

  Scenario: Clonar sin permisos es rechazado
    Given un usuario sin permiso "create-board"
    When intenta clonar un flow
    Then recibe un error 403 Forbidden
    And no se crea ningún clon
```

> Fuente: Epic Update (2026-06-08) — "Native Clone"
> 🆕 AC NUEVO — Reemplaza lógica client-side.

---

### AC-10: Graph Utils para flows

```gherkin
Feature: Utilidades de grafos para flows

  Scenario: Identificación de triggers y sinks en un flow
    Given un flow con nodos y edges configurados
    When el flow se visualiza en la lista expandida o preview
    Then helpers/flow.ts identifica correctamente los nodos trigger (sin edges entrantes)
    And identifica correctamente los nodos sink (sin edges salientes)
    And calcula los componentes conectados del grafo
```

> Fuente: Epic Update (2026-06-08) — "Graph Utils"
> 🆕 AC NUEVO

---

## EPIC 2 — PDF Templates List + Generation Telemetry

### AC-11: Formato y orientación derivados del schema pdfme

```gherkin
Feature: Derivación de formato y orientación desde schema JSONB

  Scenario: Template A4 vertical muestra formato correcto
    Given un PDF Template con schema JSONB cuyas dimensiones en mm corresponden a A4 vertical
    When el usuario expande o previsualiza el template
    Then se muestra "A4 - Portrait" como formato
    And se muestran las dimensiones en mm y pulgadas

  Scenario: Template con dimensiones no estándar
    Given un PDF Template con dimensiones que no mapean a un tamaño nombrado (Carta, A4, Legal)
    When el usuario expande el template
    Then se muestra "Custom" o las dimensiones en mm
    And el adaptador no crashea

  Scenario: Template con schema vacío o malformado
    Given un PDF Template con schema JSONB vacío "{}" o malformado
    When el usuario expande el template
    Then el adaptador maneja el error graciosamente
    And muestra un valor por defecto o "Formato desconocido"
    And la lista completa de templates no crashea
```

> Componentes: `PdfTemplateDetailsCell`, formateadores de tamaño de papel
> Fuente: Comentario EPIC 2 (2026-06-03) + Epic Update (2026-06-08)
> ⚠️ **PREGUNTA PENDIENTE PD-1**: ¿La derivación se ejecuta solo al expandir la fila (dado el Payload Diet)?

---

### AC-12: Badge de Uso y etiqueta de Borrador

```gherkin
Feature: Badges de estado de PDF Templates

  Scenario: Template utilizado muestra badge "En uso"
    Given un PDF Template con generation_count > 0
    When se renderiza la celda de estado en la lista
    Then muestra badge "En uso"

  Scenario: Template nunca usado muestra badge "Nunca usado"
    Given un PDF Template con generation_count = 0
    When se renderiza la celda de estado
    Then muestra badge "Nunca usado"

  Scenario: Template sin variables muestra etiqueta "Borrador"
    Given un PDF Template cuyo schema no contiene variables dinámicas
    When se renderiza la celda de estado
    Then muestra etiqueta "Borrador" derivada via isDraft
```

> Componente: `PdfTemplateStatusBadge`
> Fuente: Comentario EPIC 2 (2026-06-03) + Epic Update (2026-06-08)

---

### AC-13: Telemetría de generación (`generation_count` + `last_generated_at`)

```gherkin
Feature: Telemetría de generación de PDFs

  Scenario: Generación exitosa incrementa el contador
    Given un PDF Template existente con generation_count = N
    And un flow con un nodo de renderizado de PDF que usa ese template
    When el flow se ejecuta y la generación + upload a R2 son exitosos
    Then generation_count se incrementa atómicamente a N+1
    And last_generated_at se actualiza al timestamp actual

  Scenario: Fallo en telemetría no detiene el flow
    Given un flow ejecutando un nodo de renderizado de PDF
    When la generación del PDF es exitosa pero el incremento de generation_count falla
    Then el flow continúa su ejecución normalmente
    And el PDF generado se entrega correctamente
    And la telemetría puede quedar desfasada (best-effort)

  Scenario: Solo aplica a ruta company
    Given un PDF Template en la ruta de accounts
    When se genera un PDF
    Then no se incrementa la telemetría
    And las plantillas de account utilizan un almacén separado
```

> Fuente: Comentario EPIC 2 (2026-06-03) + Epic Update (2026-06-08) — "PDF Telemetry"

---

### AC-14: Preview de template con proporción real y campos dinámicos

```gherkin
Feature: Preview expansible de PDF Templates

  Scenario: Preview muestra mockup con proporción real
    Given un PDF Template con schema válido
    When el usuario expande el template en la lista
    Then se muestra un mockup con proporción real basado en blueprintSize
    And se muestran tarjetas de metadatos

  Scenario: Campos dinámicos se muestran como pills
    Given un PDF Template con campos dinámicos definidos en el schema
    When el usuario expande el template
    Then los campos dinámicos se muestran como pills
    And cada pill tiene función de copiar al clipboard
    And existe opción "ver más" si hay muchos campos

  Scenario: Template con dimensiones extremas
    Given un PDF Template con dimensiones muy anchas o muy altas
    When el usuario expande el preview
    Then el mockup se adapta sin desbordamiento del layout
```

> Componente: `PdfTemplatePreview`
> Fuente: Comentario EPIC 2 (2026-06-03) + Epic Update (2026-06-08)

---

### AC-15: PDF Clone nativo (endpoint Go HUB)

```gherkin
Feature: Clonación nativa de PDF Templates

  Scenario: Clonar template exitosamente
    Given un PDF Template existente con generation_count > 0
    When el usuario selecciona "Clonar" desde el menú Kebab
    Then se invoca ClonePdfTemplateByCompany en Go HUB
    And se realiza una copia profunda de los esquemas
    And el nuevo template tiene nombre original + " (copy)"
    And generation_count del clon es 0
    And last_generated_at del clon es NULL

  Scenario: Clonar template con nombre muy largo
    Given un PDF Template cuyo nombre está cerca del límite de caracteres
    When el usuario lo clona
    Then el nombre + " (copy)" no excede el límite de la columna en BD
```

> Fuente: Epic Update (2026-06-08) — "Native PDF Clone"
> ⚠️ **ACTUALIZADO**: Antes era client-side, ahora es endpoint nativo con lógica server-side.

---

### AC-16: Payload Diet — Lista de PDF Templates sin JSONB del schema

```gherkin
Feature: Optimización de payload en la lista de PDF Templates

  Scenario: Lista de templates no incluye schema JSONB pesado
    Given el frontend solicita la lista de PDF Templates
    When Go HUB procesa la petición via ListPdfTemplatesByCompany
    Then la respuesta selecciona explícitamente solo las columnas de lista
    And la respuesta NO contiene el JSONB completo del schema
    And los datos de telemetría (generation_count, last_generated_at) sí están incluidos
```

> Fuente: Epic Update (2026-06-08) — "Payload Diet"
> 🆕 AC NUEVO
> ⚠️ **PREGUNTA PENDIENTE PD-1**: ¿Cómo se derivan formato y campos dinámicos si el schema no viene en la lista?

---

### AC-17: Exportar JSON y columnas ordenables

```gherkin
Feature: Acciones adicionales y ordenamiento de PDF Templates

  Scenario: Exportar template como JSON
    Given un PDF Template existente
    When el usuario selecciona "Exportar JSON" desde el menú Kebab
    Then se descarga un archivo JSON con el template completo desde el cliente

  Scenario: Ordenar por GenerationCount
    Given la lista de PDF Templates está visible
    When el usuario hace click en el header "Generaciones"
    Then la lista se reordena por generation_count ASC
    When el usuario hace click nuevamente
    Then la lista se reordena por generation_count DESC

  Scenario: Ordenar por LastGeneratedAt
    Given la lista de PDF Templates está visible
    When el usuario hace click en el header "Última generación"
    Then la lista se reordena por last_generated_at
    And los templates con NULL se posicionan consistentemente
```

> Fuente: Comentario EPIC 2 (2026-06-03)

---

## EPIC 3 — Unified Search & Lazy Catalog (NUEVO)

### AC-18: Componente de búsqueda unificado (`ListSearchInput`)

```gherkin
Feature: Búsqueda unificada con ListSearchInput

  Scenario Outline: Búsqueda funciona en cada pantalla integrada
    Given el usuario está autenticado con rol Company
    And existen registros en la pantalla <pantalla>
    When el usuario navega a <ruta>
    And escribe "<término>" en el campo de búsqueda
    And presiona Enter
    Then la lista se filtra mostrando solo registros que coinciden con "<término>"
    And la URL se actualiza a "<ruta>?search=<término>"

    Examples:
      | pantalla       | ruta            | término  |
      | Connections    | /connections    | Shopify  |
      | Integrations   | /integrations   | test     |
      | Keys           | /keys           | openai   |
      | Accounts       | /accounts       | test     |
      | Developer Apps | /developer-apps | app      |
      | Services       | /services       | api      |

  Scenario: La búsqueda se ejecuta solo al presionar Enter
    Given el usuario está en cualquier pantalla con búsqueda
    When escribe caracteres en el campo de búsqueda sin presionar Enter
    Then la lista NO se filtra con cada tecla
    And no se envían peticiones al backend por cada carácter

  Scenario: Carga inicial única
    Given el usuario navega a una pantalla con búsqueda
    When la pantalla carga por primera vez
    Then se realiza una única petición de carga inicial
    And no se realizan peticiones adicionales hasta que el usuario busque

  Scenario: Sincronización con URL al cargar
    Given la URL contiene "?search=Shopify"
    When el usuario navega directamente a esa URL
    Then el input de búsqueda muestra "Shopify"
    And la lista carga filtrada por "Shopify"

  Scenario: Búsqueda con Enter sin texto
    Given el usuario tiene un filtro de búsqueda activo
    When borra el texto del campo y presiona Enter
    Then la lista muestra todos los registros sin filtro
    And la URL se actualiza removiendo el parámetro "?search="

  Scenario: Búsqueda sin resultados
    Given el usuario busca un término que no coincide con ningún registro
    When presiona Enter
    Then la lista muestra un estado vacío con mensaje apropiado
```

> Fuente: Epic Update (2026-06-08) — "Unified List Search"
> 🆕 AC NUEVO — Integrado en 6 pantallas.

---

### AC-19: Lazy Catalog (`useAppCatalog`)

```gherkin
Feature: Catálogo de apps con carga diferida

  Scenario: Catálogo se carga solo al expandir una fila
    Given el usuario está en una pantalla con filas expandibles
    And el catálogo no ha sido cargado aún
    When el usuario expande una fila
    Then useAppCatalog carga el catálogo por primera vez

  Scenario: Singleton reutiliza datos dentro del cooldown
    Given el catálogo fue cargado hace menos de 30 segundos
    When el usuario expande otra fila
    Then el catálogo reutiliza los datos ya cargados
    And no se realiza una nueva petición al backend

  Scenario: Catálogo se recarga después del cooldown
    Given el catálogo fue cargado hace más de 30 segundos
    When el usuario expande una fila
    Then el catálogo se recarga con datos frescos
```

> Fuente: Epic Update (2026-06-08) — "Lazy Catalog"
> 🆕 AC NUEVO

---

### AC-20: Postgres Full-Text Search (FTS) para flows

```gherkin
Feature: Búsqueda Full-Text Search en PostgreSQL

  Scenario: Búsqueda insensible a acentos
    Given un flow con nombre "Ejecución automática"
    When el usuario busca "ejecucion" (sin acento) en la lista de boards
    Then el flow "Ejecución automática" aparece en los resultados
    And la búsqueda usa to_tsvector + ts_rank con el wrapper IMMUTABLE de unaccent

  Scenario: Ranking de resultados por relevancia
    Given múltiples flows con nombres que contienen parcialmente el término buscado
    When el usuario busca
    Then los resultados se ordenan por ts_rank (relevancia)

  Scenario: Intento de inyección SQL via FTS
    Given un usuario malintencionado
    When busca "'; DROP TABLE flows; --"
    Then el input es sanitizado
    And no se ejecuta SQL arbitrario
    And la lista muestra resultados vacíos o sin error
```

> Fuente: Epic Update (2026-06-08) — "Postgres Full-Text Search (FTS)"
> 🆕 AC NUEVO — Requiere migración para wrapper IMMUTABLE + índice GIN.

---

### AC-21: ILIKE Search unificada en Go HUB (tenant-scoped)

```gherkin
Feature: Búsqueda ILIKE segura y aislada por tenant

  Scenario: Búsqueda aislada por company
    Given accounts existen en Company A y Company B
    When un usuario de Company A busca "test"
    Then solo ve accounts de Company A en los resultados
    And nunca ve datos de Company B

  Scenario: Caracteres especiales son escapados
    Given el usuario busca "100%"
    When la búsqueda se ejecuta via applyILIKE
    Then el carácter "%" es escapado correctamente
    And no se interpretan como wildcards de SQL
    And los caracteres "_ \" también se escapan

  Scenario Outline: ILIKE se aplica en todos los servicios refactorizados
    Given el usuario busca en el servicio <servicio>
    When la query se construye
    Then se aplica: filtro tenant PRIMERO, luego ILIKE, luego Count/Paginación

    Examples:
      | servicio       |
      | accounts       |
      | services       |
      | apps           |
      | keys           |
      | developer-apps |
```

> Fuente: Epic Update (2026-06-08) — "Unified ILIKE Search (Tenant-Scoped)"
> 🆕 AC NUEVO — Refactor con implicación de seguridad.

---

## EPIC 4 — UI Polish, A11y & Safety (NUEVO)

### AC-22: Accesibilidad (A11y)

```gherkin
Feature: Accesibilidad en elementos de búsqueda y controles

  Scenario: Icono de búsqueda es operable con teclado
    Given el usuario navega con teclado (Tab)
    When el foco llega al icono de búsqueda
    Then el icono tiene tabindex, role y soporte para Enter/Espacio
    And el foco es visible (focus-visible)
    When el usuario presiona Enter o Espacio
    Then se activa la funcionalidad de búsqueda

  Scenario: Animaciones respetan prefers-reduced-motion
    Given el sistema operativo tiene activada la preferencia de movimiento reducido
    When la pantalla muestra iconos de carga
    Then los iconos no tienen animación (motion-reduce:animate-none)

  Scenario: Todos los elementos interactivos tienen ARIA labels
    Given cualquier pantalla con elementos interactivos nuevos
    When un lector de pantalla procesa la página
    Then todos los botones, inputs e iconos tienen etiquetas ARIA descriptivas

  Scenario: Focus visible en todos los controles
    Given el usuario navega con teclado
    When el foco pasa por cada control interactivo
    Then el estado focus-visible está aplicado con indicador visual claro
```

> Fuente: Epic Update (2026-06-08) — "Accessibility (A11y)"
> 🆕 AC NUEVO

---

### AC-23: Safety durante recarga de datos

```gherkin
Feature: Protección contra mutaciones durante recarga

  Scenario: Clicks bloqueados durante recarga de lista
    Given una lista está recargando datos (petición en curso)
    When el usuario intenta hacer click en una fila
    Then el click es bloqueado (pointer-events-none en la lista)
    And no se ejecuta ninguna mutación sobre datos obsoletos

  Scenario: Clicks se rehabilitan al terminar la recarga
    Given una lista acaba de completar la recarga de datos
    When la petición finaliza exitosamente
    Then pointer-events se restaura
    And el usuario puede interactuar normalmente con los datos actualizados
```

> Fuente: Epic Update (2026-06-08) — "Safety & Theme"
> 🆕 AC NUEVO

---

### AC-24: Corrección de Dark Mode

```gherkin
Feature: Corrección de contraste en modo oscuro

  Scenario: Enlaces cyan son legibles en dark mode
    Given el usuario tiene el modo oscuro activado
    When navega las pantallas afectadas
    Then los enlaces con color cyan tienen suficiente contraste contra las superficies oscuras
    And son legibles sin esfuerzo

  Scenario: Superficies slate tienen contraste correcto
    Given el modo oscuro está activado
    When se renderizan superficies con estilo slate
    Then el texto y los iconos sobre esas superficies son legibles
    And no hay problemas de contraste
```

> Fuente: Epic Update (2026-06-08) — "Safety & Theme"
> 🆕 AC NUEVO

---

### AC-25: Reactivity Fix — Aislamiento de búsqueda

```gherkin
Feature: Aislamiento de reactividad en campo de búsqueda

  Scenario: Escribir en búsqueda no causa layout shifts
    Given el usuario está en cualquier pantalla con búsqueda
    When escribe rápidamente "test de búsqueda larga" en el campo
    Then no se producen saltos de layout (layout shifts) en la pantalla
    And no se re-renderiza la lista completa mientras escribe

  Scenario: Variable de búsqueda está aislada
    Given el texto de búsqueda se almacena en una variable local dentro de ListSearchInput
    When el usuario modifica el texto
    Then la reactividad no se propaga fuera del componente
    And no hay fugas de reactividad hacia otros componentes
```

> Fuente: Epic Update (2026-06-08) — "Reactivity Fix"
> 🆕 AC NUEVO

---

## UX/UI General (Transversal)

### AC-26: Estándar de estilos PrimeVue `pt`

```gherkin
Feature: Estándar de estilos con PrimeVue pt

  Scenario: Solo se usa propiedad nativa pt de PrimeVue
    Given los nuevos componentes de UI implementados en ambos EPICs
    When se inspeccionan los estilos aplicados
    Then todos los estilos usan exclusivamente la propiedad "pt" de PrimeVue
    And no existen ocurrencias de ":deep()" en los archivos Vue
    And no existen ocurrencias de "!important" en los estilos
```

> Fuente: Comentarios EPIC 1 y 2 (2026-06-03) — "Cero tolerancia a hacks CSS"

---

### AC-27: Tooltips contextuales

```gherkin
Feature: Tooltips interactivos e informativos

  Scenario: Tooltip aparece al hacer hover
    Given un botón, icono o campo complejo que tiene tooltip configurado
    When el usuario hace hover sobre el elemento
    Then aparece un tooltip con texto informativo que provee guía rápida
    When el usuario mueve el mouse fuera del elemento
    Then el tooltip desaparece

  Scenario: Tooltip no interfiere con la interacción
    Given un botón con tooltip
    When el usuario hace click en el botón
    Then se ejecuta la acción del botón
    And el tooltip no bloquea la interacción
```

> Fuente: Descripción original del ticket — "Contexto mediante Tooltips (UX)"
> ⚠️ No se definió qué elementos específicos tendrán tooltips.

---

### AC-28: Consistencia responsiva

```gherkin
Feature: Adaptación responsiva de componentes

  Scenario: Vista desktop (1920px)
    Given el navegador tiene resolución 1920x1080
    When el usuario navega a /workflows y /pdf-templates
    Then los componentes se muestran con layout completo
    And sin truncamiento ni desbordamiento

  Scenario: Vista tablet (768px)
    Given el navegador tiene resolución 768x1024
    When el usuario navega a /workflows y /pdf-templates
    Then los componentes se adaptan al ancho disponible
    And columnas secundarias pueden ocultarse si necesario

  Scenario: Vista mobile (375px)
    Given el navegador tiene resolución 375x667
    When el usuario navega a /workflows y /pdf-templates
    Then los componentes se adaptan sin desbordamiento horizontal
    And la funcionalidad principal es accesible
```

> Fuente: Descripción original del ticket — "Consistencia Responsiva"
> ⚠️ No se definieron breakpoints específicos ni comportamiento en mobile.

---

## AC Propuestos por QA (sugeridos — para acordar con Developer y PO)

### AC-P1: Manejo de estado vacío en badge de ejecución

```gherkin
Scenario: Flow sin ejecuciones muestra estado neutro
  Given un flow recién creado que nunca ha sido ejecutado
  And last_execution_id es NULL
  When el usuario visualiza la lista de boards
  Then el flow no muestra badge de ejecución
  Or muestra un estado neutro como "Sin ejecuciones"
  And la interfaz no crashea
```

> Justificación: Edge case EC-01. Flows nuevos no tendrán ejecución.

### AC-P2: Backfill idempotente en migración

```gherkin
Scenario: Backfill asigna última ejecución a flows existentes
  Given la migración agrega last_execution_id a la tabla flows
  And existen flows con ejecuciones previas
  When la migración se ejecuta
  Then cada flow recibe el ID de su última ejecución como last_execution_id
  And flows sin ejecuciones quedan con last_execution_id = NULL
  And la migración es idempotente (ejecutable múltiples veces sin efecto)
```

> Justificación: Edge case EC-06.

### AC-P3: Manejo de schema inválido en adaptador pdfme

```gherkin
Scenario: Adaptador maneja schema inválido sin crash
  Given un PDF Template con schema JSONB vacío, malformado o con dimensiones no estándar
  When el frontend intenta derivar formato, orientación o campos dinámicos
  Then los adaptadores retornan un valor por defecto o indicador "formato desconocido"
  And la lista completa de templates no crashea
  And el error se maneja graciosamente
```

> Justificación: Edge cases EC-09 y EC-14.

### AC-P4: Seguridad de búsqueda FTS — inyección de tsvector

```gherkin
Scenario: Input de búsqueda es sanitizado contra inyección
  Given un usuario ingresa caracteres especiales en el campo de búsqueda
  When busca "'; DROP TABLE flows; --"
  Then los inputs son sanitizados antes de construir el tsvector
  And no se permite inyección SQL
  And no se permite manipulación del tsvector
  And la búsqueda retorna resultados vacíos o sin error
```

> Justificación: Seguridad derivada de la implementación de FTS.

---

## Preguntas Pendientes para el Developer (post Test Matrix)

| # | Pregunta | AC Afectado | Contexto |
|---|----------|-------------|----------|
| PD-1 | Con el Payload Diet que elimina el JSONB del schema en la lista de PDF Templates, ¿los adaptadores de derivación (`getFormat`, `getDynamicFields`, `isDraft`, `blueprintSize`) se ejecutan solo al expandir la fila? | AC-11, AC-14, AC-16 | La lista ya no trae el schema → los datos derivados no pueden calcularse en la vista de lista |
| PD-2 | ¿El `FlowStatusBadge` envía PATCH o PUT al cambiar el estado? Si es PUT, ¿cómo evita sobrescribir campos que no tiene (por el payload reducido)? | AC-2 | Riesgo de corrupción de datos si se envía el objeto completo |
| PD-3 | ¿La migración de FTS (wrapper IMMUTABLE + índice GIN) es reversible? ¿Tiene impacto en el rendimiento de escritura de la tabla flows? | AC-20 | Índices GIN pueden impactar INSERTs/UPDATEs |

---

## Resumen de AC por Área

| Área | ACs | Rango |
|------|-----|-------|
| EPIC 1 — Boards Telemetry | 10 | AC-1 a AC-10 |
| EPIC 2 — PDF Templates | 7 | AC-11 a AC-17 |
| EPIC 3 — Unified Search & Lazy Catalog | 4 | AC-18 a AC-21 |
| EPIC 4 — UI Polish, A11y & Safety | 4 | AC-22 a AC-25 |
| UX/UI General | 3 | AC-26 a AC-28 |
| Propuestos por QA | 4 | AC-P1 a AC-P4 |
| **Total** | **32** | — |
