# Test Plan — IONF-999

## Información del Ticket
- **ID**: IONF-999
- **Título**: Agregar descripciones automáticas de los boards
- **Módulo**: Boards
- **QA Engineer**: Steve Nina
- **Fecha del plan**: 2026-06-01
- **QA Points**: 2

## Resumen
- Total de casos: 18 (13 funcionales + 5 regresión)
- Tiempo estimado: ~45 min
- Artefactos de Discovery usados: Ninguno (ticket pasó directo a Deployment)
- Test Matrix: Generada en esta sesión

---

## Orden de Ejecución

### BLOQUE 1 — SMOKE TESTS (ejecutar primero, si falla → escalar)

| □ | ID | Caso | Prioridad |
|---|-----|------|-----------|
| □ | REG-001 | Lista de boards carga correctamente con columna Description | 🔴 |
| □ | TC-001 | Generar descripción con IA — flujo completo funciona | 🔴 |

### BLOQUE 2 — HAPPY PATH (verificar flujos principales)

| □ | ID | Caso | Prioridad |
|---|-----|------|-----------|
| □ | TC-002 | Descripción generada respeta límite 500 chars | 🔴 |
| □ | TC-003 | Editar manualmente una descripción existente | 🔴 |
| □ | TC-004 | Sobrescribir descripción IA con texto manual | 🔴 |

### BLOQUE 3 — EDGE CASES (verificar bordes)

| □ | ID | Caso | Prioridad |
|---|-----|------|-----------|
| □ | TC-005 | Board vacío (sin nodos) — generar IA no crashea | 🟠 |
| □ | TC-007 | Cancelar edición descarta cambios (botón ✕) | 🟠 |
| □ | TC-008 | Cancelar con Esc | 🟠 |
| □ | TC-009 | Guardar con Enter | 🟠 |
| □ | TC-006 | Board con muchos nodos (>50) | 🟠 |
| □ | TC-010 | Navegar sin guardar pierde cambios | 🟡 |

### BLOQUE 4 — NEGATIVOS (verificar que NO se pueda romper)

| □ | ID | Caso | Prioridad |
|---|-----|------|-----------|
| □ | TC-011 | Usuario sin permiso NO puede editar | 🟠 |
| □ | TC-012 | IA no disponible — error manejado con toast | 🟡 |
| □ | TC-013 | Descripción >500 chars — trunca o rechaza | 🟡 |

### BLOQUE 5 — REGRESIÓN (verificar que no rompimos nada)

| □ | ID | Caso | Prioridad |
|---|-----|------|-----------|
| □ | REG-002 | Crear board nuevo — descripción inicia vacía | 🟠 |
| □ | REG-003 | FlowPreviewDrawer muestra descripción correcta | 🟠 |
| □ | REG-004 | Edición manual sin IA sigue funcionando | 🟠 |
| □ | REG-005 | Performance de la lista no degradada | 🟡 |

### BLOQUE 6 — DB EVIDENCE (si aplica)

| □ | ID | Query | Verificar |
|---|-----|-------|-----------|
| □ | DB-001 | `SELECT description FROM company_flows WHERE id = ?` | Descripción IA persistida correctamente |
| □ | DB-002 | `SELECT LENGTH(description) FROM company_flows WHERE id = ?` | Longitud ≤ 500 |

---

## Datos Necesarios

| Dato | Cómo obtenerlo | Notas |
|------|---------------|-------|
| Usuario con UpdateBoard | Login Company normal | `IONFLOW_COMPANY_USERNAME` |
| Usuario sin UpdateBoard | Login con user limitado | ⚠️ Verificar si hay user de prueba disponible |
| Board con nodos | Cualquier board existente en staging | Verificar que tenga ≥1 nodo |
| Board vacío | Crear board sin nodos o encontrar uno existente | Para TC-005 |
| Board complejo | Board con >50 nodos | Para TC-006 — puede no existir en staging |

---

## Criterios de Aprobación/Rechazo

### ✅ APROBACIÓN
- TODOS los smoke tests (BLOQUE 1) pasan
- TODOS los happy path (BLOQUE 2) pasan
- Al menos 80% de los edge cases (BLOQUE 3) pasan
- TODOS los negativos (BLOQUE 4) pasan
- TODOS los casos de regresión (BLOQUE 5) pasan

### ❌ RECHAZO
- Algún smoke test falla → **rechazo inmediato**
- Happy path falla → **rechazo**
- Negativo falla (el sistema se puede romper) → **rechazo**
- Regresión falla → **rechazo con análisis de impacto**

### ⚠️ APROBACIÓN CON OBSERVACIONES
- Edge case falla pero no es bloqueante → aprobar con bug registrado
- Problema visual menor → aprobar con observación
- TC-011 no testeado por falta de usuario read-only → documentar

---

## Estimación de Tiempo

| Bloque | Casos | Tiempo estimado |
|--------|-------|-----------------|
| Smoke tests | 2 | ~5 min |
| Happy path | 3 | ~10 min |
| Edge cases | 6 | ~12 min |
| Negativos | 3 | ~8 min |
| Regresión | 4 | ~8 min |
| DB evidence | 2 | ~3 min |
| **Total** | **20** | **~46 min** |

---

## Observaciones del Code Review QA (BLOQUE 0)

> Las siguientes observaciones fueron identificadas durante el Code Review y deben tenerse en cuenta durante la ejecución.
> **Repos revisados**: `gateway-ion` (MR #218 — 11 archivos, +359 líneas) + `flow_binaries` (MR #151 — 5 archivos, +157 líneas)

### ✅ Aspectos positivos

| # | Repo | Observación |
|---|------|------------|
| P1 | front | Componente `FlowDescription.vue` bien encapsulado — props/emits limpios |
| P2 | front | Permisos respetados — `can(TENANT_PERMS.UPDATE_BOARD)` antes de editar |
| P3 | front | UX correcta — spinner, toast en error, no-reload de lista |
| P4 | front | i18n completo (EN + ES) — 3 keys nuevas |
| P5 | front | 5 test cases unitarios (`FlowDescription.spec.ts`) |
| P6 | front | Front solo envía `flowId`, backend lee de DB (decisión D3) |
| P7 | back | Mapa compacto minimiza tokens enviados a la IA |
| P8 | back | Truncado Unicode seguro con `utf8.RuneCountInString` |
| P9 | back | Prompt disciplinado — ≤500 chars, no markdown, match idioma |
| P10 | back | Service aislado — NO toca `UpdateCompanyFlow` ni `FlowParams` |

### ⚠️ Observaciones a considerar

| # | Repo | Observación | Severidad | Impacto en Testing |
|---|------|------------|-----------|-------------------|
| O1 | front | `generateAI()` no persiste automáticamente — carga en textarea pero el user debe dar ✅ para guardar. Difiere del AC-1 que dice "guardar de forma persistente" | 🟡 Media | **TC-001 debe verificar el flujo de 2 pasos**: generar → confirmar. **Consultar con PM** si el flujo es aceptable |
| O2 | back | Endpoint registrado como `GET /{flowId}/ai-description` — el análisis técnico propone `POST generate-description`. GET para una acción generativa es semánticamente incorrecto | 🟢 Baja | No afecta testing funcional |
| O3 | front | No hay validación de longitud (500 chars) en frontend. El textarea no muestra `maxlength` ni contador | 🟢 Baja | TC-002 y TC-013 verifican el comportamiento del backend |
| O4 | front | `AbortController` se crea pero nunca se aborta (no hay cleanup en `onUnmounted`) | 🟢 Baja | TC-010 (navegar sin guardar) podría tener side effects menores |
| O5 | back | No hay validación de nodos vacíos. `flowResult.Data.Nodes` podría ser `[]` → prompt con mapa vacío | 🟡 Media | **TC-005 es clave** — verificar qué pasa con board sin nodos |
| O6 | back | Prompt enviado como mensaje `User` sin `System` message separado — patrón inconsistente con otros prompts | 🟢 Baja | No afecta testing funcional |
| O7 | back | **0 tests unitarios en Go** — `buildFlowCompactMap`, `extractFlowComments`, `GenerateCompanyFlowDescription` sin cobertura | 🟡 Media | No afecta E2E, pero señalar en reporte final como deuda técnica |
| O8 | back | `extractFlowComments` depende de estructura interna de `data["comments"]` — falla silenciosamente si el formato cambia | 🟢 Baja | Fail-safe: si no hay comments, no los incluye |

---

## Cómo Ejecutar y Reportar

### Metodología de ejecución

1. **Abrir staging** → `https://dev-app.ionflow.io`
2. **Ejecutar por bloques en orden** — Si un smoke falla, NO continuar
3. **Por cada test case**:
   - Ejecutar los pasos descritos en la [test-matrix.md](./test-matrix.md)
   - Anotar: ✅ Pasó / ❌ Falló / ⏭️ Saltado
   - Si falla: capturar screenshot + descripción del error
   - Si es ambiguo: anotar como ⚠️ con comentario

### Formato de reporte — CSV

Importar el archivo `test-results.csv` que se genera junto a este plan. Las columnas son:

```
ID,Módulo,AC,Tipo,Caso,Prioridad,Estado,Comentario,Screenshot,Ejecutado Por,Fecha
```

**Valores de Estado**:
- `PASS` — El caso pasó como se esperaba
- `FAIL` — El caso falló (describir en Comentario)
- `SKIP` — No se ejecutó (justificar en Comentario)
- `BLOCKED` — No se pudo ejecutar por dependencia (describir)
- `PASS_OBS` — Pasó con observaciones menores

### Qué hacer con los resultados

| Resultado global | Acción |
|-----------------|--------|
| Todos los 🔴 pasan + ≥80% de 🟠 pasan | ✅ **Aprobar** — documentar en reporte |
| Algún 🔴 falla | ❌ **Rechazar** — crear bug y devolver al dev |
| Falla 🟠 no bloqueante | ⚠️ **Aprobar con observaciones** — crear ticket de mejora |
| Falla 🟡 | 📝 **Documentar** — no bloquea aprobación |

### Entregables al finalizar

1. **CSV con resultados** → `L3-tickets/IONF-999/test-results.csv`
2. **QA Report** → `L3-tickets/IONF-999/qa-report.md` (generado con `sprint-testing/report`)
3. **Screenshots de fallos** → `L3-tickets/IONF-999/screenshots/`

---

## Estado

⏳ Plan creado — **esperando aprobación del QA Engineer para iniciar ejecución**

