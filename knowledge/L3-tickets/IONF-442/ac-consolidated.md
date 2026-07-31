# AC Consolidado — IONF-442 (Form Data Builder observations)

> Discovery Express — Basado en los 3 casos documentados en el ticket.
> Repo único: `webcomponents-flow` (branch IONF-442)

## Fuentes

- Ticket ClickUp: `86dy0bwmf`
- PR: https://github.com/altacrest/ion_webcomponents_flow/pull/10
- Developer: Gustavo Mamani
- Code Review: ✅ Approved (Alex Chura + Enrique Vicente)
- Tests: ✅ 826 PASSED (72 archivos)
- Deploy: Confirmado por Rodolfo (2026-07-28)

## Acceptance Criteria (extraídos del ticket)

### AC-1: Toggle Advanced en arrays
- La opción "Advanced" debe controlar la visibilidad del array **como estructura completa** (padre + hijos)
- NO debe mostrar items vacíos al activar el toggle
- El toggle no debe afectar la visibilidad individual de sub-items

### AC-2: Cambio de tipo de elementos de array a array anidado
- Al cambiar el tipo de elementos de un array de (text/number/boolean) a array (nested)
- Los campos generados deben renderizarse correctamente
- No deben aparecer campos rotos ni inconsistencias visuales

### AC-3: Cambio de tipo de elementos de array a collection
- Al cambiar el tipo de elementos de un array a collection
- Los items deben generarse correctamente
- La transición de tipo no debe dejar artifacts del tipo anterior

## Cambios Técnicos (del developer)

### Fix Principal — Advanced fields en DataBuilder/FormBuilder
- **FieldEditor**: Extrajo handler de cambio de tipo a `onChangeType()`. Limpia flag `advanced` al cambiar de tipo (`delete field.advanced`)
- **FormBuilder**: Panel estilizado con icono Settings2, título y texto "Some fields are hidden." cuando está colapsado
- **FieldIterator**: Nueva utilidad `isHiddenWhenBasic()` en `nestedElements.ts` — recorre recursivamente `collection` y `array` para ocultar contenedores cuyos hijos son todos avanzados. `inject` de `showAdvanced` corregido a `Ref<boolean>`
- **FieldIteratorItem**: `isStringMapeable` simplificado con short-circuits para `array` y `collection`. Optional chaining en lookup de `contextValues`

### Fix Adicional — Panel de contexto cerrándose
- `onBlur` en `useMapeableContext` ya no establece `openContext = false` incondicionalmente
- Listener `pointerdown` en `FlowDrawer` con `isEventInsideContext()` para cerrar solo cuando click es FUERA del panel
- Atributo `data-mapeable` añadido a `InputMapeable` y `SpecialInputMapeable`
- Guards de optional chaining en lookups de `contextValues`
