# QA FOUND ISSUE ESCALATION REPORT — IOND

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | Boards / Nodes |
| Path | Company > Boards > [Board] > Canvas > Iterator Node > Menú de contexto |
| Versión | gateway-ion v0.1.0 · flow_binaries v0.1.0 · gateway v2.0.0 |

## Título

**Boards — Menú de contexto del Iterator muestra data de strings como "${}" y numérica por nombre con tipo collection vacío**

## Description of the validated/replicated problem

Dentro del menú de contexto de un nodo al que el Iterator está enlazado (por ejemplo, un Form), se observan las siguientes inconsistencias en la representación de la data:
1. Si la data se trata de strings, se muestra como `${}` (interpolación vacía)
2. Si la data es numérica, se muestra por su nombre (correcto parcialmente)
3. En ambos casos, la data se visualiza como un tipo "collection vacío", lo cual es incorrecto

## Steps to Reproduce

1. Company Login > Sidebar: Boards > [Board]
2. En el canvas, agregar un nodo Iterator
3. Conectar el Iterator a un nodo (por ejemplo, un Form)
4. Ejecutar el flow con datos que incluyan strings y números
5. Abrir el menú de contexto del nodo al que el Iterator está enlazado
6. Observar las inconsistencias en la representación de la data:
   - Strings → `${}`
   - Números → nombre del campo
   - Ambos → tipo "collection vacío"

## Datos utilizados

- Rol: Company User con permiso `UPDATE_BOARD`
- Entorno: Staging
- Versión: v0.1.0
- Datos con mix de strings y números como input del Iterator

## Current Behavior

El menú de contexto muestra los datos del Iterator de forma inconsistente: strings como `${}`, números por nombre, y ambos como colección vacía.

## Expected Behavior

El menú de contexto debería mostrar correctamente:
1. Los valores de strings con su contenido real (no como `${}`)
2. Los valores numéricos con su valor real
3. El tipo de dato correcto de cada elemento (string, number, etc.), no como "collection vacío"

## Impacto

- Dificulta la configuración de nodos posteriores al Iterator
- El usuario no puede verificar qué datos fluyen a través del Iterator
- Afecta la experiencia de desarrollo de flows con iteraciones

## Categorización

- 📊 Prioridad: **normal** — no bloquea la funcionalidad pero dificulta significativamente la configuración de flows
- 🏷️ Tipo: **bug** — la representación de datos en el menú de contexto debería ser precisa
