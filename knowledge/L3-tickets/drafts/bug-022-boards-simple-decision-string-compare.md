# QA FOUND ISSUE ESCALATION REPORT — IOND

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | Boards / Nodes |
| Path | Company > Boards > [Board] > Canvas > Simple Decision Node |
| Versión | gateway-ion v0.1.0 · flow_binaries v0.1.0 · gateway v2.0.0 |

## Título

**Boards — Simple Decision compara valores numéricos como strings, resultado incorrecto**

## Description of the validated/replicated problem

Al configurar un nodo Simple Decision con una condición de comparación numérica, por ejemplo "2 es mayor que 12", la salida es por la rama `true` (incorrecta). Esto indica que los valores están siendo procesados como strings en lugar de como números. En comparación de strings, `"2" > "12"` es verdadero porque la comparación lexicográfica compara carácter a carácter (`"2" > "1"`). Este es un bug crítico de lógica de negocio que produce resultados incorrectos en los flows de toma de decisiones.

## Steps to Reproduce

1. Company Login > Sidebar: Boards > [Board]
2. En el canvas, agregar un nodo Simple Decision
3. Configurar una condición: field = `2`, operator = `is_greater`, value = `12`
4. Conectar ambas salidas (true/false) a nodos subsecuentes
5. Ejecutar el flow
6. Observar que la salida es por la rama `true` (incorrecto: 2 NO es mayor que 12)

## Datos utilizados

- Rol: Company User con permiso `UPDATE_BOARD`
- Entorno: Staging
- Versión: v0.1.0
- Valores de prueba: field=2, operator=is_greater, value=12

## Current Behavior

El nodo Simple Decision evalúa `2 > 12` como `true` porque ambos valores son procesados como strings ("2" > "12" es verdadero en comparación lexicográfica). Los operadores de comparación (`is_greater`, `is_less`, etc.) no realizan conversión de tipo para valores numéricos.

## Expected Behavior

1. Cuando ambos valores son numéricos, la comparación debería realizarse como números, no como strings
2. `2 > 12` debería evaluar a `false`
3. El nodo debería detectar automáticamente el tipo de dato o permitir especificarlo explícitamente
4. Los operadores `is_greater`, `is_less`, `is_greater_equal`, `is_less_equal` deberían manejar correctamente comparaciones numéricas

## Notas Adicionales

**Pregunta adicional del QA**: ¿Es posible configurar más de una condición en el Simple Decision? ¿Es este el comportamiento correcto?

**Respuesta**: Según el L2 del módulo Nodes, el nodo Simple Decision (`ion.action.condition`) acepta un array de condiciones: `[{ "field": "...", "operator": "...", "value": "..." }]`, por lo que sí es posible configurar más de una condición. El motor de expresiones usa `expr-lang/expr`.

## Impacto

- **Crítico para la lógica de negocio**: todos los flows que usan Simple Decision con comparaciones numéricas pueden producir resultados incorrectos
- Afecta la confiabilidad de todo el motor de decisiones
- Puede causar ejecuciones incorrectas de flows en producción con impacto en datos reales

## Categorización

- 📊 Prioridad: **urgent** — bug de lógica de negocio que produce resultados incorrectos, afecta todos los flows con comparaciones numéricas
- 🏷️ Tipo: **bug** — comparación de valores debería respetar los tipos de dato
