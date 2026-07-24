# QA FOUND ISSUE ESCALATION REPORT — IOND

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | PDF Templates |
| Path | Company > PDF Templates > New Template > Import Template |
| Versión | gateway-ion v0.1.0 · flow_binaries v0.1.0 · gateway v2.0.0 |

## Título

**PDF Templates — Import Template no valida contenido JSON que rompe dimensiones del documento**

## Description of the validated/replicated problem

Al utilizar la opción de Import Template con un JSON de estructura correcta pero con elementos que rompen las dimensiones del documento (por ejemplo, posiciones o tamaños fuera de los límites del canvas), el sistema no valida el contenido del JSON respecto a las constraints del documento. Elementos con coordenadas fuera de rango, dimensiones negativas o valores que exceden el canvas del template son aceptados sin validación, pudiendo causar problemas de renderización.

## Steps to Reproduce

1. Company Login > Sidebar: PDF Templates
2. Presionar Button: "New Template"
3. Seleccionar la opción "Import Template"
4. Preparar un archivo JSON con estructura correcta pero con elementos que rompan las dimensiones:
   - Posiciones X/Y fuera de los límites del documento
   - Dimensiones (width/height) excesivamente grandes
   - Valores negativos en coordenadas
5. Importar el JSON
6. Observar que el template se importa sin validación de contenido
7. Verificar que los elementos importados rompen la visualización del documento

## Datos utilizados

- Rol: Company User con permiso `READ_PDF_TEMPLATE`
- Entorno: Staging
- Versión: v0.1.0
- JSON de template con estructura válida pero valores fuera de rango

## Current Behavior

El sistema acepta cualquier JSON con estructura válida sin validar que los valores de posición, dimensiones y propiedades de los elementos estén dentro de los rangos aceptables del documento.

## Expected Behavior

El sistema debería validar el contenido del JSON importado contra las restricciones del template:
1. Coordenadas X/Y dentro de los límites del canvas del documento
2. Dimensiones (width/height) positivas y dentro de rangos razonables
3. Validar que los elementos no se superpongan de forma que rompan la renderización
4. Mostrar errores específicos por cada elemento que incumpla las restricciones
5. Permitir importación parcial o rechazar el JSON completo con feedback detallado

## Pregunta abierta para el equipo

¿Qué reglas de validación específicas deberían aplicarse al contenido del JSON importado?
- ¿Máximos de posición basados en el tamaño de página seleccionado?
- ¿Restricciones de solapamiento?
- ¿Validación de tipos de fuente disponibles?
- ¿Límites de tamaño de elementos individuales?

## Impacto

- Afecta a Company Users que importan templates predefinidos
- Puede causar templates que no se renderizan correctamente
- No bloqueante (el import funciona) pero la calidad del resultado no es predecible

## Categorización

- 📊 Prioridad: **normal** — la funcionalidad opera pero la robustez de validación es deficiente
- 🏷️ Tipo: **improvement** — se trata de agregar validación adicional al contenido importado
