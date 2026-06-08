# Comentario Estructurado — Templates

> Templates de comentarios de QA para tickets de ClickUp.
> Se usan para dejar constancia en el ticket al cerrar una fase.

---

## 1. Cierre de Discovery

> Usar cuando se completa la fase de Discovery de un ticket.
> El QA Engineer validó la lógica de negocio, consolidó AC y construyó la Test Matrix.

```
🔎 QA Discovery Review — [TICKET-ID]

📋 **Discovery completado**: [fecha]
👤 **QA Engineer**: [nombre]
📦 **Módulo**: [módulo]

---

### Análisis Realizado
- ✅ Revisión de lógica de negocio
- ✅ Interrogación del prototipo con Developer
- ✅ Consolidación de Acceptance Criteria
- ✅ Construcción de Test Matrix

### Acceptance Criteria
- **AC originales validados**: [N]
- **AC propuestos y acordados**: [N]
- **AC diferidos**: [N]

### Test Matrix
- **Total de casos**: [N]
- **Happy Path**: [N]
- **Edge Cases**: [N]
- **Negativos**: [N]
- **Regresión**: [N]

### Edge Cases Identificados
- [EC-01]: [Descripción breve]
- [EC-02]: [Descripción breve]

### Acuerdos con Developer
- [Acuerdo 1]: [Descripción breve]
- [Acuerdo 2]: [Descripción breve]

### Observaciones
- [Observación relevante para Deployment]

### Resultado: ✅ Listo para Deployment
> La Test Matrix y el plan de testing están construidos.
> El ticket puede pasar a la fase de Deployment cuando el Developer indique que está listo.

| Details |
|---------|
| TEST MATRIX | [link al documento] |
| AC CONSOLIDADOS | [link o referencia] |
```

---

## 2. Cierre de Deployment (Testing Completo)

> Usar cuando se completa la fase de testing de un ticket.

```
🔎 QA Review — [TICKET-ID]

📋 **Testing completado**: [fecha]
👤 **QA Engineer**: [nombre]
📦 **Módulo**: [módulo]

---

### Resumen
[Breve descripción de lo que se testeó]

### Resultado

| Tipo | Ejecutados | Aprobados | Fallados |
|------|-----------|-----------|---------|
| Smoke | [N] | [N] | [N] |
| Happy Path | [N] | [N] | [N] |
| Edge Cases | [N] | [N] | [N] |
| Negativos | [N] | [N] | [N] |
| Regresión | [N] | [N] | [N] |
| DB Evidence | [N] | [N] | [N] |

### Veredicto: ✅ Approved / ❌ Rejected

### Observaciones
- [Observación 1]
- [Observación 2]

### Bugs Reportados
- [BUG-001]: [Descripción breve] (Severidad: 🔴/🟠/🟡)

### Evidencia Adjunta
- [Link al QA Report completo si aplica]
```

---

## 3. Re-test (después de corrección)

> Usar cuando se re-testea un ticket que fue previamente rechazado.

```
🔎 QA Re-test — [TICKET-ID]

📋 **Re-test completado**: [fecha]
👤 **QA Engineer**: [nombre]
📦 **Módulo**: [módulo]

---

### Bugs corregidos verificados

| Bug ID | Estado anterior | Estado actual | Verificación |
|--------|----------------|---------------|-------------|
| BUG-001 | ❌ Abierto | ✅ Corregido | Verificado |
| BUG-002 | ❌ Abierto | ⚠️ Parcial | Ver observación |

### Regresión post-fix
- [Caso de regresión testeado]: ✅/❌

### Veredicto: ✅ Approved / ❌ Sigue Rejected

### Observaciones
- [Observación]
```

---

## Reglas de Uso

1. **Nunca comentar automáticamente** — El QA Engineer revisa y aprueba el comentario antes de publicarlo
2. **Formato consistente** — Usar siempre estos formatos para facilitar la auditoría
3. **Incluir siempre**: Resultado por tipo, veredicto claro, bugs si aplica
4. **El cierre de Discovery es obligatorio** antes de que un ticket pase a Deployment
5. **Idioma**: Según la preferencia del equipo
