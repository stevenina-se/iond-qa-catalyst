# Mapa Iond Subcategory → módulo L2 → E2E maestro

> El campo **Iond Subcategory** de ClickUp indica el área funcional del ticket. Las skills lo usan para cargar el **L2** correcto y para seleccionar la **regresión de la versión** (capa 1).
> **Fuente de datos:** [`knowledge/test-suites/_config/subcategory-map.csv`](../test-suites/_config/subcategory-map.csv). Este archivo explica cómo usarlo; los valores se mantienen solo en el CSV.

## Columnas del CSV

| Columna | Qué indica |
|---|---|
| `IOND_SUBCATEGORY` | Valor del campo en ClickUp (sin distinguir mayúsculas). `Nodo *` cubre cualquier valor "Nodo <nombre>" |
| `L2_MODULE` | Carpeta de `knowledge/L2-modules/` que se carga como contexto |
| `E2E_MODULES` | Prefijos del E2E maestro (`TEN-BRD`, `TEN-APC`, …) que se consideran impactados |
| `E2E_EXCLUDE` | Rutas que no se arrastran aunque el módulo esté impactado (por ejemplo, los nodos del canvas cuando la subcategoría es `Boards`) |
| `CROSS_SYSTEM` | Sistemas cruzados que activan flujos cross-system en la regresión (`IonMind`, `Gateway`, `Keycloak`, `Stripe`, `Apps externas`) |
| `NOTA` | Criterio o advertencia para QA |

## Cómo se usa

1. `release/ingest` lee la subcategoría de cada ticket y la busca en el CSV.
2. Si el ticket es de un nodo (`Nodo Mapper`, `Nodo Simple Decision`…), la selección toma la fila de ese nodo por similitud de nombre (tolera diferencias de escritura de la hoja).
3. Si la subcategoría **no existe** en el CSV, la skill infiere el módulo por el título del ticket, lo marca como *inferido* y pide a QA agregar la fila al CSV antes de seleccionar la regresión.
4. Si el campo está **vacío**, se registra como alerta del release (el campo es obligatorio en Discovery e Improvements).

## Nombres L2 que se prestan a confusión

| Carpeta L2 | Corresponde en la app a |
|---|---|
| `connections/` | **App Connectors** (definición de conectores y sus nodos) |
| `integrations/` | **Connections** (conexiones activas con apps externas) |
| `keys/` | **Credentials** (credenciales de LLM y servicios) |
| `data-store/` | **Persistent Data** (Data Store y Data Structure) |
| `executions/` | **Execution History** |
| `services/` | Catálogo de services y apps del Gateway |
