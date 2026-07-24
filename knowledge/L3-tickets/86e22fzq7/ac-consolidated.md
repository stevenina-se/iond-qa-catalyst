# Acceptance Criteria Consolidados — 86e22fzq7

> Ticket: Connections — Reautorización por API Key crea conexión duplicada en lugar de sobrescribir
> Módulo: Connections / Integrations
> Fecha de reconciliación: 2026-07-14
> Fuentes: Descripción del ticket + Comentario del Developer (Gustavo, 2026-07-08) + QA Instructions + Code Review (Enrique + Rodolfo)

---

## AC Reconciliados

### AC-1. Reautorización de conexión actualiza en lugar de crear duplicado
> **Fuente**: Descripción del ticket + Developer spec

**Dado** una conexión activa existente con método de autenticación API Key  
**Cuando** el usuario ejecuta el proceso de reautorización  
**Entonces** las credenciales de la conexión existente se actualizan (sobrescriben), NO se crea una conexión nueva duplicada.

**Verificación**:
- Antes de reauthorize: contar conexiones en la lista
- Después de reauthorize: la cantidad es la misma
- La conexión existente tiene las credenciales actualizadas

---

### AC-2. Un único toast de éxito tras reautorización (o ninguno)
> **Fuente**: Descripción del ticket (current behavior: 2 toasts) + Developer spec ("Success toasts are now suppressed during reauthorization")

**Dado** un proceso de reautorización completado exitosamente  
**Cuando** la reautorización finaliza  
**Entonces** NO se muestran toasts de "Connection approved/validated successfully" (toasts suprimidos en reauthorize).

**Nota**: El developer decidió suprimir completamente los toasts en reauthorize, no reducirlos a 1.

---

### AC-3. Creación de conexión nueva mantiene toasts de éxito
> **Fuente**: Developer QA Instructions (punto 2)

**Dado** el proceso de crear una nueva conexión (no reauthorize)  
**Cuando** la conexión se crea exitosamente  
**Entonces** los toasts de éxito ("Connection approved/validated successfully") siguen apareciendo normalmente.

---

### AC-4. Reautorización de tenant app connections sin regresiones
> **Fuente**: Developer QA Instructions (punto 3)

**Dado** una conexión de tipo tenant app (no global)  
**Cuando** se ejecuta reautorización  
**Entonces** el flujo funciona igual que antes del fix, sin regresiones.

**Nota del Developer**: "The tenant app flow was not changed and should continue working as before."

---

### AC-5. Flows que referencian la conexión usan credenciales actualizadas
> **Fuente**: Descripción del ticket (Expected Behavior punto 4)

**Dado** un flow que referencia una conexión que fue reautorizada  
**Cuando** el flow se ejecuta después del reauthorize  
**Entonces** los nodos del flow usan automáticamente las nuevas credenciales de la conexión.

---

### AC-6. Flujos OAuth (authorizing) y success inmediato funcionan correctamente
> **Fuente**: Developer QA Instructions (punto 4)

**Dado** conexiones con diferentes flujos de autenticación  
**Cuando** se hace reauthorize en:  
- a) Una conexión OAuth (pasa por estado `authorizing` con popup)
- b) Una conexión con status `success` inmediato (API Key, sin popup)  

**Entonces** ambos flujos completan correctamente sin errores ni duplicados.

---

## Resumen

| AC | Título | Fuente | Tipo |
|----|--------|--------|------|
| AC-1 | Reauthorize actualiza, no duplica | Ticket + Developer | Bug fix core |
| AC-2 | Toasts suprimidos en reauthorize | Ticket + Developer | Bug fix UX |
| AC-3 | Toasts intactos en creación nueva | Developer Instructions | Regresión |
| AC-4 | Tenant apps sin regresiones | Developer Instructions | Regresión |
| AC-5 | Flows usan credenciales nuevas | Ticket Expected Behavior | Integración |
| AC-6 | OAuth y API Key reauthorize funcionan | Developer Instructions | Cobertura |

---

## Divergencias Encontradas

| AC Original (Ticket) | Decisión en Comentarios | AC Reconciliado |
|-----------------------|------------------------|-----------------|
| "Se debería mostrar un único toast de éxito" | Developer: "Success toasts are now suppressed during reauthorization" | AC-2: Toasts **suprimidos** (0 toasts), no reducidos a 1 |
| No mencionado en ticket | Developer: "Test tenant app connections" | AC-4 NUEVO: Tenant apps sin regresiones |
| No mencionado en ticket | Developer: "Test both authorizing and success flows" | AC-6 NUEVO: Ambos flujos de auth cubiertos |
