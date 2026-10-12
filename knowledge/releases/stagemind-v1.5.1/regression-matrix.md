# Regression Matrix — StageMind v1.5.1

> Generado por `ionflow-qa-catalyst`
> Fecha: 2026-09-15
> Versión: **StageMind v1.5.1**
> Total de tickets: 14
> Repo principal: `ai_productmind`
> Nota: Sin data L2/L3 disponible — TCs basados en información de tickets

---

## Resumen

| Métrica | Valor |
|---------|-------|
| Versión | StageMind v1.5.1 |
| Total de TCs | 35 |
| TCs Regresión Directa | 28 |
| TCs Regresión Indirecta | 3 |
| TCs Baseline | 4 |
| Repo principal | `ai_productmind` |
| Tickets del release | 14 |

---

## Cobertura por Módulo

| Módulo | Tickets | Directos | Indirectos | Total | Riesgo |
|--------|---------|----------|------------|-------|--------|
| Endpoints / API Core | 4 | 8 | 1 | 9 | 🔴 Crítico |
| Observabilidad / Performance | 4 | 6 | 1 | 7 | 🟠 Alto |
| Costos / Billing | 3 | 5 | 0 | 5 | 🟠 Alto |
| Seguridad / NSFW | 1 | 3 | 1 | 4 | 🟠 Alto |
| Feedback / Xenvio | 1 | 3 | 0 | 3 | 🟡 Medio |
| Catalog Builder | 1 | 2 | 0 | 2 | 🟡 Medio |
| Baseline | — | 0 | 0 | 4 | 🟡 Medio |

---

## Matriz de Regresión Detallada

### 🔌 Endpoints / API Core

| ID | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Ticket |
|----|------|-------------|-------------|-------|-------------------|-----------|--------|
| SM-01 | DIRECTA | Endpoint para creación de boxes | API accesible | POST /api/boxes > Body con parámetros válidos | Boxes creados correctamente, respuesta 200 con data | 🔴 Crítico | 86e0rqvqr |
| SM-02 | DIRECTA | Endpoint creación de boxes — validación de input | API accesible | POST /api/boxes > Body inválido/vacío | Error 400 con mensaje descriptivo (no 500) | 🟠 Alto | 86e0rqvqr |
| SM-03 | DIRECTA | Endpoint para escalado de imágenes | API accesible, imagen válida | POST /api/images/scale > Imagen + parámetros | Imagen escalada correctamente, respuesta con URL resultado | 🔴 Crítico | 86e0rqwgd |
| SM-04 | DIRECTA | Endpoint escalado — imagen inválida NO devuelve Error 400 | API accesible | POST /api/images/scale > Imagen válida | Respuesta exitosa (fix del bug previo de Error 400) | 🔴 Crítico | 86e0tkajg |
| SM-05 | DIRECTA | Endpoint escalado — imagen realmente inválida devuelve error controlado | API accesible | POST /api/images/scale > Archivo corrupto | Error descriptivo, no crash | 🟠 Alto | 86e0tkajg |
| SM-06 | DIRECTA | Endpoint para generación de prompts de edición | API accesible | POST /api/prompts/edit > Parámetros de edición | Prompt generado correctamente para edición de imagen | 🔴 Crítico | 86e0rxzem |
| SM-07 | DIRECTA | STAGEMIND v1.4 — funcionalidad general actualizada | Servicio desplegado | Ejecutar flujo completo: imagen > proceso > resultado | Pipeline completo funciona con mejoras de v1.4 | 🟠 Alto | 86e0ega5d |
| SM-08 | INDIRECTA | API endpoints accesibles desde Xenvio | Xenvio conectado | Xenvio > Llamar endpoints de StageMind | Respuestas correctas desde cliente externo | 🟡 Medio | 86e2ee6d6 |

### 📊 Observabilidad / Performance

| ID | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Ticket |
|----|------|-------------|-------------|-------|-------------------|-----------|--------|
| SM-09 | DIRECTA | Instrumentación de tiempos de respuesta por request | Servicio con requests | StageMind > Ejecutar requests > Verificar métricas de tiempo | Tiempos de respuesta registrados con breakdown por etapa | 🟠 Alto | 86e0ethmp |
| SM-10 | DIRECTA | Métricas operativas registradas | Servicio operativo | StageMind > Admin > Métricas > Verificar dashboard | Métricas operativas (CPU, memoria, requests/s) visibles | 🟠 Alto | 86e0ethmv |
| SM-11 | DIRECTA | Consultas y umbrales de performance | Servicio con métricas | StageMind > Admin > Performance > Verificar umbrales | Alertas se disparan cuando se exceden umbrales definidos | 🟠 Alto | 86e0ethmr |
| SM-12 | DIRECTA | Documentación de observabilidad actualizada | Docs existentes | StageMind > Docs > Observabilidad | Documentación refleja nuevas métricas y costos | 🟡 Medio | 86e0ethmq |
| SM-13 | DIRECTA | Validación de costos documentada | Docs existentes | StageMind > Docs > Costos > Verificar | Documentación de costos actualizada y validada | 🟡 Medio | 86e0ethmq |
| SM-14 | INDIRECTA | Performance bajo carga | Servicio con métricas | StageMind > Ejecutar N requests concurrentes > Verificar métricas | Tiempos de respuesta dentro de umbrales bajo carga | 🟠 Alto | 86e0ethmp |

### 💰 Costos / Billing

| ID | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Ticket |
|----|------|-------------|-------------|-------|-------------------|-----------|--------|
| SM-15 | DIRECTA | Cálculo de costos de Replicate robusto | Replicate configurado | StageMind > Ejecutar proceso con Replicate > Verificar costo | Costo calculado correctamente, sin discrepancias | 🟠 Alto | 86e0ethmn |
| SM-16 | DIRECTA | Monitoreo de costos de Replicate | Replicate con uso | StageMind > Admin > Costos > Replicate | Costos de Replicate monitoreados en tiempo real | 🟠 Alto | 86e0ethmn |
| SM-17 | DIRECTA | Consulta mensual de gastos por proveedor | Datos de costos históricos | StageMind > Admin > Reportes > Gastos mensuales | Reporte mensual con desglose por proveedor | 🟡 Medio | 86e0fazj2 |
| SM-18 | DIRECTA | Gastos por proveedor — múltiples proveedores | Múltiples proveedores usados | StageMind > Admin > Reportes > Filtrar por proveedor | Cada proveedor con total correcto | 🟡 Medio | 86e0fazj2 |

### 🔒 Seguridad / NSFW

| ID | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Ticket |
|----|------|-------------|-------------|-------|-------------------|-----------|--------|
| SM-19 | DIRECTA | Validación de contenido NSFW — imagen inapropiada bloqueada | Servicio operativo | POST /api/images > Imagen NSFW | Imagen rechazada con mensaje de contenido inapropiado | 🔴 Crítico | 86e0j62tv |
| SM-20 | DIRECTA | Validación NSFW — imagen apropiada aceptada | Servicio operativo | POST /api/images > Imagen apropiada | Imagen procesada correctamente (sin falso positivo) | 🔴 Crítico | 86e0j62tv |
| SM-21 | DIRECTA | Validación NSFW — edge cases (imagen ambigua) | Servicio operativo | POST /api/images > Imagen en zona gris | Comportamiento predecible (rechazo o aprobación con log) | 🟠 Alto | 86e0j62tv |
| SM-22 | INDIRECTA | NSFW no bloquea imágenes de productos legítimos | Servicio operativo | POST /api/images > Imagen de producto (ropa, accesorios) | Imagen procesada sin bloqueo NSFW | 🟠 Alto | 86e0j62tv |

### 📩 Feedback / Xenvio

| ID | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Ticket |
|----|------|-------------|-------------|-------|-------------------|-----------|--------|
| SM-23 | DIRECTA | API extensible de feedback — enviar feedback de ejecución | Ejecución completada | POST /api/feedback > Datos de ejecución | Feedback registrado y accesible | 🟡 Medio | 86e2ee6d6 |
| SM-24 | DIRECTA | API de feedback — extensible con campos custom | Ejecución completada | POST /api/feedback > Campos adicionales | Campos custom aceptados y persistidos | 🟡 Medio | 86e2ee6d6 |
| SM-25 | DIRECTA | Feedback de ejecuciones accesible desde Xenvio | Feedback registrado | Xenvio > Consultar feedback > Verificar data | Feedback visible y filtrable desde Xenvio | 🟡 Medio | 86e2ee6d6 |

### 📦 Catalog Builder

| ID | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Ticket |
|----|------|-------------|-------------|-------|-------------------|-----------|--------|
| SM-26 | DIRECTA | Catalog Builder v1.3.5 — añadidos StageMind | Catalog Builder operativo | StageMind > Catalog Builder > Crear catálogo > Verificar | Catálogo generado con funcionalidad StageMind integrada | 🟡 Medio | 86e0rj0u4 |
| SM-27 | DIRECTA | Catalog Builder — generación de productos | Catálogo existente | StageMind > Catalog Builder > Generar productos | Productos generados con imágenes y descripciones | 🟡 Medio | 86e0rj0u4 |

### 🔒 Baseline (Funcionalidad Existente)

| ID | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Ticket |
|----|------|-------------|-------------|-------|-------------------|-----------|--------|
| SM-28 | BASELINE | Pipeline completo de procesamiento de imagen | Servicio desplegado | POST /api/process > Imagen válida > Resultado | Imagen procesada de extremo a extremo | 🔴 Crítico | — |
| SM-29 | BASELINE | Health check del servicio StageMind | Servicio desplegado | GET /health | Respuesta 200 OK | 🟠 Alto | — |
| SM-30 | BASELINE | Autenticación API (API Key / Bearer token) | API Key válida | POST con API Key válida vs inválida | Acceso permitido con key válida, 401 con key inválida | 🟠 Alto | — |
| SM-31 | BASELINE | Rate limiting funcional | API accesible | Enviar requests por encima del límite | Rate limiting aplicado, respuesta 429 | 🟡 Medio | — |

---

## Instrucciones

- **StageMind es un servicio independiente** — No comparte repos con iond ni IonMind
- **Sin L2/L3 disponible** — Los TCs se basan en la información de los tickets
- **Testing de NSFW** requiere imágenes de prueba clasificadas (apropiadas e inapropiadas)
- **Testing de costos** requiere acceso a dashboard de Replicate y datos históricos
- **Xenvio** es el cliente principal — verificar integración end-to-end

---

*Generado por ionflow-qa-catalyst — StageMind v1.5.1*
*Fecha: 2026-09-15*
