# Smoke Matrix — v0.1.1

> Generado por `skills/release/smoke-matrix`
> Fecha: 2026-07-24
> Versión: **v0.1.1** (Regression fixes v0.1.0 + features Sprint 4)
> Entorno: `https://dev-app.ionflow.io`
> KC Domain: `Development_Testing`
> Fuente: 9 flujos críticos de `L1/test-priorities.md` + 16 tickets del release

---

## Resumen

| Métrica | Valor |
|---------|-------|
| Versión | v0.1.1 |
| Total TCs | 24 |
| TCs base (9 flujos) | 12 |
| TCs específicos del release | 12 |
| Riesgo Alto (🔴) | 16 |
| Baseline (🟢) | 8 |
| Flujos impactados | 7 de 9 |
| Tiempo estimado | ~35-45 min |
| Modo sugerido | Playwright MCP (Canal 1, supervisado) |

---

## Credenciales de Testing

| Rol | Usuario | Dominio KC |
|-----|---------|------------|
| Company (Tenant) | skuanquis@gmail.com | Development_Testing |
| Admin | admin@shipedge.com | Development_Testing |

> ⚠️ Passwords en `.env` — NUNCA exponer en artefactos.

---

## Cobertura por Flujo Crítico

| # | Flujo Crítico | ¿Impactado? | Tickets | TCs Base | TCs Release | Total |
|---|--------------|------------|---------|----------|-------------|-------|
| 1 | Login / Auth | ✅ Sí | IONF-1075 | 2 | 1 | 3 |
| 2 | Crear un flow | ✅ Sí | IONF-1121 | 1 | 1 | 2 |
| 3 | Agregar nodos a un flow | ✅ Sí | IONF-1128 | 1 | 1 | 2 |
| 4 | Ejecutar un flow | ✅ Sí | IONF-1127, IONF-1007 | 2 | 2 | 4 |
| 5 | Ver historial de ejecuciones | ✅ Sí | IONF-1168, IONF-1049 | 1 | 1 | 2 |
| 6 | Crear conexiones | ✅ Sí | IONF-1114 | 1 | 1 | 2 |
| 7 | Crear y editar conector | ❌ No | — | 1 | 0 | 1 |
| 8 | Crear y editar service | ❌ No | — | 1 | 0 | 1 |
| 9 | Template PDF | ✅ Sí | IONF-1126, IONF-1116 | 2 | 2 | 4 |
| — | Extras release (webhooks, billing, FlowPilot) | ✅ Sí | IONF-1169, IONF-1098, IONF-1020 | 0 | 3 | 3 |
| | **TOTAL** | | | **12** | **12** | **24** |

---

## Leyenda

### Riesgo por Versión
- 🔴 Riesgo Alto — Módulo tocado directamente por un ticket del release
- 🟢 Baseline — Módulo no tocado, verificación de que el core no se rompió

### Estado
- ⬜ Pendiente
- ✅ Pasó
- ❌ Falló
- ⏭️ Saltado (con justificación)

### Prioridad
- 🔴 Crítico — Bloqueante si falla
- 🟠 Alto — Testear siempre
- 🟡 Medio — Testear si hay tiempo

---

## TCs BASE — 9 Flujos Críticos

> Columna vertebral del smoke. Verifican que el core del producto sigue funcional.

### Flujo 1: Login / Auth

| ID | Side | Caso de Test | Pasos | Resultado Esperado | Prioridad | Riesgo | Estado |
|----|------|-------------|-------|-------------------|-----------|--------|--------|
| SM-001 | KC → TENANT | Login Company con Keycloak | Navigate: `dev-app.ionflow.io` > Keycloak login > Fill #username: `skuanquis@gmail.com` > Fill #password: `[.env]` > Click #kc-login > Select company > Verify: Dashboard visible | Dashboard carga correctamente. Se muestra el nombre de la company y el sidebar de navegación | 🔴 | 🔴 | ⬜ |
| SM-002 | KC → ADMIN | Login Admin con Keycloak | Navigate: `dev-app.ionflow.io` > Keycloak login > Fill #username: `admin@shipedge.com` > Fill #password: `[.env]` > Click #kc-login > Verify: Admin Dashboard visible | Panel de administración carga correctamente. Se muestran las opciones de admin | 🔴 | 🔴 | ⬜ |

### Flujo 2: Crear un flow

| ID | Side | Caso de Test | Pasos | Resultado Esperado | Prioridad | Riesgo | Estado |
|----|------|-------------|-------|-------------------|-----------|--------|--------|
| SM-003 | TENANT | Crear un flow nuevo y guardarlo | [Tenant] Login > Sidebar: Boards > Click "Create Board" > Ingresar nombre: "Smoke Test v0.1.1" > Guardar > Verificar board en la lista | El flow se crea exitosamente, aparece en la lista de boards con el nombre asignado | 🔴 | 🔴 | ⬜ |

### Flujo 3: Agregar nodos a un flow

| ID | Side | Caso de Test | Pasos | Resultado Esperado | Prioridad | Riesgo | Estado |
|----|------|-------------|-------|-------------------|-----------|--------|--------|
| SM-004 | TENANT | Agregar nodos y conectar en canvas | [Tenant] Login > Sidebar: Boards > Abrir board existente > Canvas > Agregar nodo (HTTP Request) > Agregar nodo (Mapper) > Conectar ambos nodos con edge | Los nodos se agregan al canvas. La conexión (edge) se establece visualmente entre ambos nodos | 🔴 | 🔴 | ⬜ |

### Flujo 4: Ejecutar un flow

| ID | Side | Caso de Test | Pasos | Resultado Esperado | Prioridad | Riesgo | Estado |
|----|------|-------------|-------|-------------------|-----------|--------|--------|
| SM-005 | TENANT | Ejecutar flow en modo Test | [Tenant] Login > Sidebar: Boards > Abrir board con nodos configurados > Click "Test" > Ejecutar desde nodo inicial > Esperar resultado | La ejecución recorre todos los nodos y termina con status "completed". Se muestra el resultado de cada nodo | 🔴 | 🔴 | ⬜ |
| SM-006 | TENANT | Ejecutar flow en modo Production (Scheduler) | [Tenant] Login > Sidebar: Boards > Board con Scheduler activo > Verificar que Scheduler está en Production > Verificar última ejecución en Execution History | El Scheduler está activo y la última ejecución muestra status "completed" (no "error") | 🔴 | 🔴 | ⬜ |

### Flujo 5: Ver historial de ejecuciones

| ID | Side | Caso de Test | Pasos | Resultado Esperado | Prioridad | Riesgo | Estado |
|----|------|-------------|-------|-------------------|-----------|--------|--------|
| SM-007 | TENANT | Ver historial de ejecuciones | [Tenant] Login > Sidebar: Execution History > Verificar que la lista carga > Abrir detalle de la ejecución más reciente > Verificar logs | El historial muestra las ejecuciones. Los logs del detalle muestran nodos ejecutados, resultados y timestamps | 🟠 | 🔴 | ⬜ |

### Flujo 6: Crear conexiones

| ID | Side | Caso de Test | Pasos | Resultado Esperado | Prioridad | Riesgo | Estado |
|----|------|-------------|-------|-------------------|-----------|--------|--------|
| SM-008 | TENANT | Crear conexión nueva (Check Connection) | [Tenant] Login > Sidebar: Connections (Integrations) > Check Connection > Seleccionar connector disponible > Completar credenciales > Guardar | La conexión se crea exitosamente y aparece en la lista de conexiones activas | 🟠 | 🔴 | ⬜ |

### Flujo 7: Crear y editar conector

| ID | Side | Caso de Test | Pasos | Resultado Esperado | Prioridad | Riesgo | Estado |
|----|------|-------------|-------|-------------------|-----------|--------|--------|
| SM-009 | TENANT | Crear conector manual | [Tenant] Login > Sidebar: Connections > Create > Manual Connector > Completar datos (nombre, base URL) > Guardar > Verificar en lista | El connector se crea y aparece en la lista. Se puede abrir para editar | 🟠 | 🟢 | ⬜ |

### Flujo 8: Crear y editar service

| ID | Side | Caso de Test | Pasos | Resultado Esperado | Prioridad | Riesgo | Estado |
|----|------|-------------|-------|-------------------|-----------|--------|--------|
| SM-010 | TENANT | Crear service/grapp | [Tenant] Login > Sidebar: Catalog > Add Catalog Item > Crear Grapp > Completar datos > Guardar > Verificar en lista | El service se crea exitosamente y aparece en el catálogo. Se puede abrir para editar | 🟠 | 🟢 | ⬜ |

### Flujo 9: Template PDF

| ID | Side | Caso de Test | Pasos | Resultado Esperado | Prioridad | Riesgo | Estado |
|----|------|-------------|-------|-------------------|-----------|--------|--------|
| SM-011 | TENANT | Crear template PDF nuevo | [Tenant] Login > Sidebar: PDF Templates > New Template > Asignar nombre > Agregar elementos (Text, Image) > Guardar | El template se crea con los elementos agregados. Se guarda sin errores | 🟠 | 🔴 | ⬜ |
| SM-012 | TENANT | Editar template PDF y guardar cambios | [Tenant] Login > Sidebar: PDF Templates > Abrir template existente > Modificar un elemento > Guardar > Re-abrir > Verificar cambios | Los cambios persisten después de guardar y re-abrir. No se pierden ediciones | 🟠 | 🔴 | ⬜ |

---

## TCs RELEASE-SPECIFIC — Validación de cambios v0.1.1

> TCs derivados directamente de los 16 tickets del release.
> Prefijo `SM-R-` para diferenciarse del baseline.

### Auth — IONF-1075 (Refactor registro compañía)

| ID | Side | Caso de Test | Pasos | Resultado Esperado | Prioridad | Riesgo | Ticket | Estado |
|----|------|-------------|-------|-------------------|-----------|--------|--------|--------|
| SM-R-001 | KC | Registro de compañía funciona post-refactor | Navigate: `dev-app.ionflow.io` > Click "Sign Up" > Completar formulario registro (nombre, email, password, company) > Submit > Verificar redirección | El registro se completa sin errores. El usuario es redirigido correctamente al dashboard o selección de company | 🟠 | 🔴 | IONF-1075 | ⬜ |

### Boards — IONF-1121 (False unsaved alert)

| ID | Side | Caso de Test | Pasos | Resultado Esperado | Prioridad | Riesgo | Ticket | Estado |
|----|------|-------------|-------|-------------------|-----------|--------|--------|--------|
| SM-R-002 | TENANT | No false unsaved alert post-commit | [Tenant] Login > Sidebar: Boards > Abrir board > Hacer cambio > Save > Commit > Salir del board > Re-ingresar al mismo board | Al re-ingresar, NO aparece alerta de "cambios sin guardar". La vista carga limpia | 🟠 | 🔴 | IONF-1121 | ⬜ |

### Boards / Simple Decision — IONF-1128

| ID | Side | Caso de Test | Pasos | Resultado Esperado | Prioridad | Riesgo | Ticket | Estado |
|----|------|-------------|-------|-------------------|-----------|--------|--------|--------|
| SM-R-003 | TENANT | Simple Decision compara numéricos correctamente | [Tenant] Login > Sidebar: Boards > Board con Simple Decision > Configurar condición: valor > 10 > Ejecutar Test con input numérico (ej: 5) > Verificar rama tomada | La comparación se realiza como números (5 > 10 = false → toma rama correcta). NO compara como strings | 🔴 | 🔴 | IONF-1128 | ⬜ |

### Boards / Scheduler — IONF-1127, IONF-1007

| ID | Side | Caso de Test | Pasos | Resultado Esperado | Prioridad | Riesgo | Ticket | Estado |
|----|------|-------------|-------|-------------------|-----------|--------|--------|--------|
| SM-R-004 | TENANT | Scheduler status "completed" (no "error") | [Tenant] Login > Sidebar: Boards > Board con Scheduler activo en Production > Execution History > Verificar status de última ejecución | El status de la ejecución es "completed", NO "error". El flow se ejecutó correctamente | 🔴 | 🔴 | IONF-1127 | ⬜ |
| SM-R-005 | TENANT | Scheduler hora correcta UTC/Local | [Tenant] Login > Sidebar: Boards > Board con Scheduler > Verificar hora de próxima ejecución > Comparar con hora local del usuario | La hora configurada en el Scheduler corresponde a la hora real esperada (sin desfase UTC/Local) | 🔴 | 🔴 | IONF-1007 | ⬜ |

### Execution History — IONF-1168

| ID | Side | Caso de Test | Pasos | Resultado Esperado | Prioridad | Riesgo | Ticket | Estado |
|----|------|-------------|-------|-------------------|-----------|--------|--------|--------|
| SM-R-006 | TENANT | Logs de ejecución sin desfase +4h | [Tenant] Login > Sidebar: Execution History > Abrir detalle de ejecución reciente > Verificar timestamps de los logs > Comparar con hora actual | Los timestamps de los logs coinciden con la hora real de ejecución. NO hay desfase de +4 horas | 🔴 | 🔴 | IONF-1168 | ⬜ |

### Connections — IONF-1114

| ID | Side | Caso de Test | Pasos | Resultado Esperado | Prioridad | Riesgo | Ticket | Estado |
|----|------|-------------|-------|-------------------|-----------|--------|--------|--------|
| SM-R-007 | TENANT | Reauthorize API Key no duplica conexión | [Tenant] Login > Sidebar: Connections (Integrations) > Seleccionar conexión con API Key > Reauthorize > Ingresar nueva key > Guardar > Verificar lista | La conexión se actualiza con la nueva key. NO se crea una segunda conexión duplicada | 🔴 | 🔴 | IONF-1114 | ⬜ |

### PDF Templates — IONF-1126, IONF-1116

| ID | Side | Caso de Test | Pasos | Resultado Esperado | Prioridad | Riesgo | Ticket | Estado |
|----|------|-------------|-------|-------------------|-----------|--------|--------|--------|
| SM-R-008 | TENANT | Escape con cambios → confirmación | [Tenant] Login > Sidebar: PDF Templates > Abrir template > Hacer cambio > Presionar Escape | Se muestra modal de confirmación "¿Descartar cambios?" antes de cerrar. Los cambios NO se pierden silenciosamente | 🔴 | 🔴 | IONF-1126 | ⬜ |
| SM-R-009 | TENANT | Load Base PDF grande → error controlado | [Tenant] Login > Sidebar: PDF Templates > New Template > Load Base PDF > Seleccionar archivo > límite de tamaño | Mensaje de error claro indicando el límite. La vista NO crashea ni se queda en spinner | 🔴 | 🔴 | IONF-1116 | ⬜ |

### Webhooks — IONF-1169

| ID | Side | Caso de Test | Pasos | Resultado Esperado | Prioridad | Riesgo | Ticket | Estado |
|----|------|-------------|-------|-------------------|-----------|--------|--------|--------|
| SM-R-010 | TENANT | Webhook público accesible sin CORS | Obtener URL de webhook público de un flow en Production > Enviar POST request desde origen externo (curl/Postman) > Verificar respuesta | La request es aceptada sin error CORS. El flow se dispara correctamente. Status 200 en la respuesta | 🟠 | 🔴 | IONF-1169 | ⬜ |

### Billing — IONF-1098

| ID | Side | Caso de Test | Pasos | Resultado Esperado | Prioridad | Riesgo | Ticket | Estado |
|----|------|-------------|-------|-------------------|-----------|--------|--------|--------|
| SM-R-011 | TENANT | Confirmación de cobro antes de scraping | [Tenant] Acceder a funcionalidad de scraping de plataforma > Iniciar primer scraping > Verificar que aparece modal de confirmación de cobro | Se muestra modal de confirmación con costo aproximado antes de ejecutar el scraping. No se cobra sin confirmación | 🔴 | 🔴 | IONF-1098 | ⬜ |

### Boards / Flow Pilot — IONF-1020

| ID | Side | Caso de Test | Pasos | Resultado Esperado | Prioridad | Riesgo | Ticket | Estado |
|----|------|-------------|-------|-------------------|-----------|--------|--------|--------|
| SM-R-012 | TENANT | Flow Pilot chat funcional con token tracking | [Tenant] Login > Sidebar: Boards > Abrir board > Nodo Code > Ask FlowPilot > Enviar prompt > Verificar respuesta y tracking | El chat de Flow Pilot responde correctamente. El uso de tokens se registra (visible en la UI si aplica) | 🟠 | 🔴 | IONF-1020 | ⬜ |

---

## Estimación de Tiempo

| Bloque | TCs | Tiempo estimado |
|--------|-----|----------------|
| Flujos base (9 flujos) | 12 | ~18 min |
| TCs específicos del release | 12 | ~18 min |
| Setup (login, navegación inicial) | — | ~2 min |
| **Total** | **24** | **~38 min** |

---

## Orden de Ejecución Sugerido

> Ejecutar en este orden para maximizar eficiencia (agrupado por módulo y rol):

### Bloque 1 — Auth & Login (~4 min)
1. SM-001 — Login Company
2. SM-002 — Login Admin
3. SM-R-001 — Registro compañía (IONF-1075)

### Bloque 2 — Boards Core (~10 min)
4. SM-003 — Crear flow
5. SM-004 — Agregar nodos y conectar
6. SM-005 — Ejecutar flow Test
7. SM-R-002 — No false unsaved alert (IONF-1121)
8. SM-R-003 — Simple Decision numéricos (IONF-1128)

### Bloque 3 — Scheduler & Executions (~8 min)
9. SM-006 — Ejecutar flow Production (Scheduler)
10. SM-R-004 — Scheduler status completed (IONF-1127)
11. SM-R-005 — Scheduler hora UTC/Local (IONF-1007)
12. SM-007 — Ver historial ejecuciones
13. SM-R-006 — Logs sin desfase +4h (IONF-1168)

### Bloque 4 — Connections (~4 min)
14. SM-008 — Crear conexión
15. SM-R-007 — Reauthorize API Key (IONF-1114)
16. SM-009 — Crear conector manual

### Bloque 5 — PDF Templates (~6 min)
17. SM-011 — Crear template PDF
18. SM-012 — Editar template PDF
19. SM-R-008 — Escape confirmación (IONF-1126)
20. SM-R-009 — Load PDF grande (IONF-1116)

### Bloque 6 — Services & Extras (~6 min)
21. SM-010 — Crear service
22. SM-R-010 — Webhook sin CORS (IONF-1169)
23. SM-R-011 — Confirmación cobro (IONF-1098)
24. SM-R-012 — Flow Pilot tokens (IONF-1020)

---

## Criterios de Aprobación del Smoke

| Criterio | Condición |
|----------|-----------|
| ✅ **PASS** | Todos los TCs 🔴 Crítico pasan. Máximo 2 TCs 🟠 Alto con falla no-bloqueante |
| ⚠️ **PASS con observaciones** | Todos los TCs 🔴 pasan. 1-3 TCs 🟠 fallan con workaround conocido |
| ❌ **FAIL** | Cualquier TC 🔴 Crítico falla. O más de 3 TCs 🟠 Alto fallan |

---

## Observaciones

1. **v0.1.1 es una patch release**: El foco está en verificar que los 8 regression fixes de v0.1.0 no introdujeron nuevos problemas.
2. **Boards es el módulo de mayor riesgo**: 5 tickets tocan Boards directamente (Scheduler, Simple Decision, Commit, Flow Pilot, Webhooks).
3. **PDF Templates tiene 2 fixes críticos**: Ambos son de UX (unsaved changes y file size limit).
4. **CORS fix (IONF-1169)**: Verificar que los webhooks públicos son accesibles pero los dedicados siguen protegidos.
5. **SM-R-001 (Registro)**: Ejecutar con precaución — puede crear datos en el ambiente de staging.
6. **Edge case vigente de v0.1.0**: IONF-1087 (nodo IonPDF sin edge → spinner permanente) NO fue corregido en v0.1.1 — no incluido en smoke.

---

## Notas

- Fuente de flujos críticos: `knowledge/L1-project/test-priorities.md` (9 flujos)
- Fuente de tickets: `knowledge/releases/v0.1.1/sprint-board.md` + `release-notes-internal.md` (16 tickets)
- Referencia cruzada: `knowledge/releases/v0.1.1/regression-matrix.md` (49 TCs de regresión)
- Credenciales: `.env` (protegido por `.gitignore`)
- Entorno: `https://dev-app.ionflow.io`

*Generado por ionflow-qa-catalyst — skill: release/smoke-matrix*
*Fecha: 2026-07-24*
