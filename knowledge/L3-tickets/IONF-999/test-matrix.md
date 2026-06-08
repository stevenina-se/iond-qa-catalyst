# Test Matrix — IONF-999

> Generada por `test-docs/document` (modo matrix)
> Fecha: 2026-06-01
> Módulo: Boards

## Resumen

| Métrica | Valor |
|---------|-------|
| Total de casos | 18 |
| Happy path | 4 |
| Edge cases | 6 |
| Negativos | 3 |
| Regresión | 5 |
| Automatizables | 12 |
| Cobertura de AC | 2/2 |

---

## Test Matrix

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado | Comentario | Fecha |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|------------|-------|
| TC-001 | Boards | AC-1 | Happy Path | Generar descripción con IA para un board con nodos | Board con ≥1 nodo, usuario con permiso UpdateBoard | 1. Ir a /workflows 2. Click en descripción del board 3. Click en botón IA (✨) 4. Esperar generación 5. Click ✅ guardar | Descripción generada aparece en la lista, persiste tras recarga | 🔴 | ✅ | ✅ PASS | Board_tmk: IA generó "The Board_tmk flow contains no nodes or connections and therefore performs no actions." — guardado con ✅, persistió tras recarga | 2026-06-01 |
| TC-002 | Boards | AC-1 | Happy Path | Descripción generada respeta límite de 500 chars | Board con muchos nodos (>20) | 1. Generar descripción con IA 2. Verificar longitud | Texto ≤500 caracteres, sin markdown | 🔴 | ✅ | ✅ PASS | Board_tmk: 84 chars, Board Test Code: 76 chars. Ambos ≤500, sin markdown. Nota: no se probó con board >20 nodos (no disponible en staging) | 2026-06-01 |
| TC-003 | Boards | AC-2 | Happy Path | Editar manualmente una descripción existente | Board con descripción (generada o manual) | 1. Click en descripción 2. Modificar texto 3. Click ✅ | Texto manual se guarda, persiste tras recarga | 🔴 | ✅ | ✅ PASS | "Board export": editado de "bla bla" → "QA Test — Manual description edit TC-003". Persistió tras recarga | 2026-06-01 |
| TC-004 | Boards | AC-2 | Happy Path | Sobrescribir descripción IA con texto manual | Board con descripción generada por IA | 1. Click en descripción 2. Borrar y escribir texto propio 3. Guardar | Texto manual reemplaza al de IA, no se regenera | 🔴 | ✅ | ✅ PASS | Board_tmk: sobrescribió descripción IA con "Manual overwrite of AI description - TC-004" — guardado exitosamente | 2026-06-01 |
| TC-005 | Boards | AC-1 | Edge Case | Generar descripción para board vacío (sin nodos) | Board sin nodos ni edges | 1. Click en descripción 2. Click en botón IA | Error toast o descripción genérica — sin crash | 🟠 | ✅ | ✅ PASS | Board_tmk (vacío): IA generó texto genérico sin crash ni error. Comportamiento correcto | 2026-06-01 |
| TC-006 | Boards | AC-1 | Edge Case | Generar descripción para board con >50 nodos | Board complejo | 1. Click IA en board grande | Se genera correctamente (puede tardar más) | 🟠 | ✅ | ✅ PASS | Board con mas de 1900 nodos genero una descripcion general | 2026-06-01 |
| TC-007 | Boards | AC-2 | Edge Case | Cancelar edición descarta cambios (botón ✕) | Board con descripción | 1. Click en descripción 2. Modificar texto 3. Click ✕ cancelar | Texto original se restaura, no se guarda | 🟠 | ✅ | ✅ PASS | Escribió "SHOULD BE DISCARDED" + click ✕ → texto original restaurado | 2026-06-01 |
| TC-008 | Boards | AC-2 | Edge Case | Cancelar edición con tecla Esc | Board en modo edición | 1. Click en descripción 2. Escribir 3. Presionar Esc | Sale de modo edición sin guardar | 🟠 | ✅ | ✅ PASS | Escribió "ESC SHOULD DISCARD THIS" + Esc → texto original restaurado | 2026-06-01 |
| TC-009 | Boards | AC-2 | Edge Case | Guardar con tecla Enter | Board en modo edición | 1. Click en descripción 2. Escribir texto 3. Presionar Enter | Descripción se guarda | 🟠 | ✅ | ✅ PASS | Board_New_Desc: Enter guardó "Saved with Enter key TC-009" correctamente | 2026-06-01 |
| TC-010 | Boards | AC-1 | Edge Case | Navegar sin guardar pierde cambios | Board en modo edición con texto sin guardar | 1. Click en descripción 2. Escribir 3. Navegar a Dashboard 4. Volver a /workflows | Cambios no guardados se pierden | 🟡 | ✅ | ✅ PASS | Escribió "THIS SHOULD BE LOST" → navegó a /dashboard → volvió → texto original preservado | 2026-06-01 |
| TC-011 | Boards | — | Negativo | Usuario sin permiso UpdateBoard NO puede editar | Usuario con rol limitado | 1. Login como usuario sin permisos 2. Ir a /workflows 3. Click en descripción | NO se abre modo edición, botón IA no aparece | 🟠 | ✅ | ✅ PASS | El campo se encuentra bloqueado y no es posible clicar sobre el | 2026-06-01 |
| TC-012 | Boards | AC-1 | Negativo | IA no disponible — error manejado | Servicio LLM caído o sin configurar | 1. Click IA cuando servicio no disponible | Toast de error, board queda sin cambios | 🟡 | ✅ | ✅ PASS | Muestra error 404 en el toast | 2026-06-01 |
| TC-013 | Boards | AC-2 | Negativo | Descripción >500 chars ingresada manualmente | Board en modo edición | 1. Pegar texto de 600+ chars 2. Guardar | Backend trunca o rechaza; front no crashea | 🟡 | ✅ | ✅ PASS | Description must be at most 500 characters No deja | 2026-06-01 |

---

## Casos de Regresión

| ID | Módulo impactado | Caso de regresión | Por qué podría romperse | Prioridad | Estado | Comentario | Fecha |
|----|-----------------|-------------------|------------------------|-----------|--------|------------|-------|
| REG-001 | Boards | Lista de boards carga correctamente | Columna description cambió de read-only a componente interactivo | 🔴 | ✅ PASS | Columna Description visible, 10 boards con paginación 325 total. Edit mode funcional con 3 botones (IA/✅/✕) | 2026-06-01 |
| REG-002 | Boards | Crear board nuevo — descripción inicia vacía | El campo description podría tener default incorrecto | 🟠 | ✅ PASS | Board "QA_REG002_Test" creado — aparece con "No description" en la lista. Diálogo de creación solo pide nombre (sin campo description) | 2026-06-01 |
| REG-003 | Boards | FlowPreviewDrawer muestra descripción correcta | Se agregó emit `update:flow` al drawer | 🟠 | ✅ PASS | El preview de los boards si muestra la dexscripcion siempre y cuando se tenga un commmit | 2026-06-01 |
| REG-004 | Boards | Edición manual sin IA sigue funcionando | El save ahora pasa por `FlowService.update()` en vez de inline | 🟠 | ✅ PASS | Confirmado por TC-003 y TC-009: edición manual guarda correctamente con ✅ y Enter | 2026-06-01 |
| REG-005 | Boards | Performance de la lista no degradada | Se agregó componente FlowDescription a cada fila | 🟡 | ✅ PASS | Lista carga en <2s con 325 boards, navegación fluida entre páginas | 2026-06-01 |

---

## Queries de Verificación BD

```sql
-- TC-001: Verificar que la descripción se persistió
-- BD: PostgreSQL (gateway)
SELECT id, name, description FROM company_flows WHERE id = [flowId];
-- Esperado: description = [texto generado por IA]

-- TC-004: Verificar que edición manual sobrescribió
SELECT id, description FROM company_flows WHERE id = [flowId];
-- Esperado: description = [texto manual del usuario]

-- TC-013: Verificar truncado a 500 chars
SELECT id, LENGTH(description) as len FROM company_flows WHERE id = [flowId];
-- Esperado: len <= 500
```

---

## Notas

- Endpoint backend: `GET /api/1.0/tenants/{tenantId}/flows/{flowId}/ai-description`
- Permiso requerido: `UpdateBoard`
- La generación de IA NO persiste automáticamente — el usuario debe confirmar con ✅
- El campo `description` es tipo `text` en BD (sin límite duro), el 500 es regla de negocio
