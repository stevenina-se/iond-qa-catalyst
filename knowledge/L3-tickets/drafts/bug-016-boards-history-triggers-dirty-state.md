# QA FOUND ISSUE ESCALATION REPORT — IOND

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | Boards |
| Path | Company > Boards > New Board > Historial de cambios |
| Versión | gateway-ion v0.1.0 · flow_binaries v0.1.0 · gateway v2.0.0 |

## Título

**Boards — Historial de cambios activa evento de cambios sin guardar al revisar commits con comentarios**

## Description of the validated/replicated problem

Al crear un nuevo Board, realizar un commit exitoso, utilizar el elemento de comentario, hacer un nuevo commit, y luego revisar el historial de cambios, al hacer click sobre el icono del comentario en el historial se activa el evento de "existen cambios sin guardar". Esto es incorrecto: el acto de revisar el historial no debería emitir eventos de cambios, ya que el usuario solamente está consultando commits anteriores, no realizando modificaciones.

## Steps to Reproduce

1. Company Login > Sidebar: Boards > Board existente o nuevo
2. Realizar un commit exitoso
3. Agregar un elemento de comentario en el canvas
4. Realizar un segundo commit
5. Navegar al historial de cambios/commits del Board
6. En el historial, hacer click sobre el icono del comentario de un commit anterior
7. Observar que se activa la alerta de "existen cambios sin guardar"

## Datos utilizados

- Rol: Company User con permiso `UPDATE_BOARD`
- Entorno: Staging
- Versión: v0.1.0
- Board con al menos 2 commits, incluyendo uno con comentario

## Current Behavior

Al hacer click sobre el icono del comentario en el historial de cambios, se dispara el evento de cambios sin guardar. El sistema interpreta la navegación del historial como una modificación.

## Expected Behavior

La revisión del historial de cambios debería ser una operación de solo lectura. Hacer click en elementos del historial (como el icono de comentario) no debería activar eventos de cambios sin guardar ni alterar el estado de dirty del Board.

## Impacto

- Genera confusión sobre el estado del Board al revisar el historial
- Puede llevar a commits innecesarios
- No bloqueante pero degrada la experiencia de revisión de historial

## Categorización

- 📊 Prioridad: **normal** — no bloquea funcionalidad pero genera falsos positivos de cambios sin guardar
- 🏷️ Tipo: **bug** — la revisión de historial no debería emitir eventos de cambios
