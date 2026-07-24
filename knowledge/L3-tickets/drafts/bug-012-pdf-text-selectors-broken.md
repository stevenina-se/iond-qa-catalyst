# QA FOUND ISSUE ESCALATION REPORT — IOND

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | PDF Templates |
| Path | Company > PDF Templates > New Template > Elemento de texto |
| Versión | gateway-ion v0.1.0 · flow_binaries v0.1.0 · gateway v2.0.0 |

## Título

**PDF Templates — Selectores de tipo de dato y fuente no funcionan en el panel de configuración de texto**

## Description of the validated/replicated problem

Al crear un nuevo template PDF y arrastrar un elemento de tipo texto al canvas, en el panel de configuración del elemento los selectores de tipo de dato no funcionan correctamente. Adicionalmente, el selector de tipo de fuente tampoco opera. Se requiere específicamente soporte para fuentes adicionales para el diseño de templates de Nestlé.

## Steps to Reproduce

1. Company Login > Sidebar: PDF Templates
2. Presionar Button: "New Template"
3. Arrastrar un elemento de tipo "Texto" al canvas del template
4. Observar el panel de configuración del elemento a la derecha/izquierda
5. Intentar cambiar el tipo de dato mediante el selector → no responde
6. Intentar cambiar el tipo de fuente mediante el selector → no responde

## Datos utilizados

- Rol: Company User con permiso `READ_PDF_TEMPLATE`
- Entorno: Staging
- Versión: v0.1.0
- Requerimiento específico: Fuentes para diseño de Nestlé

## Current Behavior

Los selectores (dropdowns) de tipo de dato y tipo de fuente en el panel de configuración del elemento de texto no responden a la interacción del usuario. No se despliegan ni permiten seleccionar opciones.

## Expected Behavior

1. Los selectores de tipo de dato deberían desplegarse y permitir seleccionar entre las opciones disponibles
2. El selector de tipo de fuente debería desplegarse y mostrar las fuentes disponibles
3. Se debería incluir las fuentes necesarias para el diseño de Nestlé
4. Los cambios en los selectores deberían reflejarse inmediatamente en el elemento del canvas

## Impacto

- **Bloqueante** para la configuración de elementos de texto en templates PDF
- Impide personalizar la tipografía y el tipo de dato de los elementos
- Impacto directo en el requerimiento de Nestlé que necesita fuentes específicas

## Categorización

- 📊 Prioridad: **high** — funcionalidad core del editor de templates rota, bloquea requerimiento de cliente
- 🏷️ Tipo: **bug** — los selectores deberían funcionar correctamente
