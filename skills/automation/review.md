# Skill: automation/review

> Revisa tests E2E generados por IA antes de que se consideren confiables. Verifica calidad del código, selectores, assertions y decide si el test pasa a suite permanente.

## Cuándo usar este skill

- **Post-generación**: Después de que `automation/code` genere los tests
- **Post-ejecución**: Después de ejecutar los tests para validar resultados

## Pre-requisitos

- ✅ `L3-tickets/<ticket-id>/automation-result.md`
- ✅ Acceso a los tests generados en `../bot-test/apps/bot-test/tests/IONFLOW/tickets/<ticket-id>/`
- ✅ `L3-tickets/<ticket-id>/test-matrix.md` — Para verificar que el test cubre el TC

---

## Instrucciones de Ejecución

### Stage 1 — PLANNING

Reporta al QA Engineer:
1. Los tests que vas a revisar
2. Los TCs que deben cubrir

### Stage 2 — EXECUTION

#### Paso 1: Revisión de código

Para cada test file generado, evalúa:

| Criterio | Estado | Notas |
|----------|--------|-------|
| **Selectores** — ¿Son reales y estables? (data-testid, IDs, no clases CSS frágiles) | ✅/❌ | |
| **Assertions** — ¿Verifican lo correcto según el TC? | ✅/❌ | |
| **Independencia** — ¿El test funciona solo, sin depender del orden? | ✅/❌ | |
| **Setup/Teardown** — ¿Se prepara y limpia el estado correctamente? | ✅/❌ | |
| **Login** — ¿Se maneja la autenticación correctamente? | ✅/❌ | |
| **Waits** — ¿Usa waits apropiados (no hardcoded timeouts)? | ✅/❌ | |
| **Page Objects** — ¿Se reusan donde es posible? | ✅/❌ | |
| **Naming** — ¿El describe/it describe claramente qué se testea? | ✅/❌ | |
| **Error handling** — ¿Maneja casos donde un elemento no aparece? | ✅/❌ | |

#### Paso 2: Verificar ejecución

Si los tests ya se ejecutaron:

| Test | TC-ID | Resultado | Consistente | Notas |
|------|-------|-----------|-------------|-------|
| `should create flow` | TC-001 | ✅/❌ | ✅ (3/3 runs) | |

> Un test es **consistente** si pasa al menos 3 de 3 ejecuciones consecutivas.

#### Paso 3: Decidir destino

| Test | Calidad | Consistencia | Decisión |
|------|---------|-------------|----------|
| `should create flow` | ✅ Buena | ✅ 3/3 | 🟢 Migrar a suite permanente |
| `should validate form` | ⚠️ Parcial | ✅ 3/3 | 🟡 Corregir y re-evaluar |
| `should handle error` | ❌ Mala | ❌ 1/3 | 🔴 Descartar o reescribir |

### Stage 3 — REPORTING

Guarda en `L3-tickets/<ticket-id>/automation-review.md`:

```markdown
# Review de Tests E2E — [TICKET-ID]

## Resumen
- Tests revisados: [N]
- Aprobados para suite permanente: [N]
- Requieren corrección: [N]
- Descartados: [N]

## Decisiones
[tabla del Paso 3]

## Migración
Tests aprobados para migrar de:
  tickets/[TICKET-ID]/ → <módulo>/
```

---

## Reglas de este Skill

1. **Un test flaky es peor que no tener test** — Si falla intermitentemente, no se sube
2. **3 ejecuciones consecutivas** es el mínimo para considerar un test estable
3. **Los selectores deben ser estables** — `data-testid` > ID > role > class
4. **El QA Engineer aprueba la migración** a suite permanente
