# Test Matrix — 86e1r2c6z
# Refactorizar flujo y formulario de registro de compañía

> Generada: 2026-06-23 | Actualizada: 2026-07-17 (Deployment — reconciliación con TDD Build)
> Módulo: auth (formulario /create-company)
> QA Engineer: Steve Nina | Developer: Gustavo Mamani
> Track: Deployment

## Resumen

| Métrica | Valor |
|---------|-------|
| Total de casos | 42 |
| Happy path | 8 |
| Edge cases | 13 |
| Negativos | 7 |
| Regresión | 9 |
| Code Review | 5 |
| Automatizables | 4 (UI gateway-ion) |
| Cobertura de AC | 14/14 AC (AC-6 ✅ resuelto — `companies.timezone`) |

> ✅ **Actualización Deployment**: TC-016 y TC-036 desbloqueados. TC-002, TC-004, TC-011, TC-020, TC-021, TC-031 ajustados según implementación real del Developer. TC-037 (email fallback) agregado.

---

## Test Matrix

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-001 | auth/register | AC-1, AC-13 | Happy Path | Registro completo de company con datos válidos | Usuario autenticado en Keycloak sin company asignada | Navigate: /create-company > Verify: formulario carga con 3 secciones > Fill "Company Name": "Test Company" > Fill "Contact Name": test > Select "Timezone": America/New_York > Verify: Country autodetectado = USA > Fill "Postal Code": 10001 > Button: "Autofill city & state" > Verify: State y City autocompletos > Verify: hint badge "✓ City and state filled" > Fill "Address 1": "123 Main St" > Fill "Phone": "+1234567890" > Button: "Create Company" > Verify: company creada | Company se crea exitosamente. Usuario redirigido al flujo post-registro. Sin errores | 🔴 | ✅ Sí | ✅ PASS |
| TC-002 | auth/register | AC-3 | Happy Path | Campos read-only de Keycloak se muestran correctamente | Usuario autenticado en Keycloak con nombre y email | Navigate: /create-company > Verify: Banner de identidad muestra nombre completo (`users.name` concatenado) y email > Verify: mostrados como texto informativo (NO inputs) > Verify: NO son editables > Verify: NO hay campos separados "First Name" / "Last Name" | Banner muestra nombre completo y email como texto read-only. No hay cursor de edición. No hay inputs de First/Last Name separados | 🔴 | ✅ Sí | ✅ PASS |
| TC-003 | auth/register | AC-5, AC-4 | Happy Path | Timezone autodetecta el Country | Formulario abierto | Navigate: /create-company > Select "Timezone": America/La_Paz > Verify: campo Country muestra "Bolivia" automáticamente | Al seleccionar timezone América/La_Paz, Country se autocompleta con Bolivia | 🔴 | ✅ Sí | ✅ PASS |
| TC-004 | auth/register | AC-7 | Happy Path | Autocompletado State y City por Postal Code (botón explícito) | Servicio externo disponible (GEOAPIFY_API_KEY configurada) | Navigate: /create-company > Fill "Postal Code": 10001 (≥ 3 chars) > Verify: botón "Autofill city & state" aparece > Button: "Autofill city & state" > Verify: State selector muestra "New York" > Verify: City muestra "New York" > Verify: hint badge "✓ City and state filled from postal code" visible > Cambiar Postal Code > Verify: hint desaparece, botón reaparece | State y City se autocompletan al hacer click en botón. Hint badge aparece. Al cambiar CP, hint desaparece y botón reaparece | 🟠 | ❌ No (servicio externo) | ✅ PASS |
| TC-005 | auth/register | AC-12 | Happy Path | "Back to login" navega correctamente | Formulario abierto | Navigate: /create-company > Button: "Back to login" > Verify: redirige al flujo de login | Usuario regresa al login sin errores. Sin company creada parcialmente | 🔴 | ✅ Sí | ✅ PASS |
| TC-006 | auth/register | AC-14 | Happy Path | Formulario visible y funcional en desktop | Viewport ≥ 1024px | Navigate: /create-company en desktop > Verify: 2 paneles visibles (izquierdo + derecho formulario) > Verify: todos los campos accesibles y alineados > Verify: botones en fila horizontal > Verify: contenido dentro de max-w-2xl | Layout de 2 paneles correcto. Sin campos desbordados. Botones en misma fila. Contenido no se estira en monitores anchos | 🟠 | ❌ No (visual) | ✅ PASS |
| TC-007 | auth/register | AC-14 | Happy Path | Formulario visible y funcional en mobile | Viewport ≤ 375px (iPhone SE) | Navigate: /create-company en mobile > Verify: formulario en columna única > Verify: scroll habilitado > Verify: botones en columna vertical (Create Company arriba, Back to login abajo — flex-col-reverse) > Verify: todos los campos accesibles | Layout mobile correcto. Botones apilados con CTA primario arriba. Scroll funcional. Sin campos cortados | 🟠 | ❌ No (visual) | ✅ PASS |
| TC-008 | auth/register | AC-2, AC-10 | Happy Path | Diseño visual con 3 secciones y panel izquierdo mejorado | Formulario cargado en modo dark | Navigate: /create-company > Verify: sección "Company Profile" con ícono > Verify: sección "Location" con ícono > Verify: panel izquierdo dark minimalista (sin degradado azul) > Verify: blend en límite de paneles (sin línea dura) > Verify: inputs con estilo "filled/raised" | 3 secciones con headers claramente visibles. Panel izquierdo dark consistente. Sin degradado celeste. Inputs con jerarquía visual clara | 🟡 | ❌ No (visual) | ✅ PASS |
| TC-009 | auth/register | AC-8 | Negativo | Submit sin campos obligatorios → validación inline | Formulario vacío | Navigate: /create-company > Button: "Create Company" (sin llenar campos) > Verify: formulario NO se envía > Verify: error inline junto a Company Name > Verify: error inline junto a Country > Verify: Timezone puede tener valor autodetectado del browser | Sistema previene el envío. Muestra errores claros junto a Company Name y Country. Timezone puede ya estar autodetectado | 🔴 | ✅ Sí | ✅ PASS |
| TC-010 | auth/register | AC-8 | Negativo | Submit sin Company Name → error específico en ese campo | Formulario con todos los campos salvo Company Name | Navigate: /create-company > Fill todos los demás campos > Leave "Company Name" vacío > Button: "Create Company" > Verify: error junto a "Company Name" | Error inline en el campo Company Name. El formulario no se envía. Los demás campos mantienen sus valores | 🔴 | ✅ Sí | ✅ PASS |
| TC-011 | auth/register | AC-8 | Negativo | Submit sin Country → error específico | Formulario sin Country seleccionado | Navigate: /create-company > Fill "Company Name" > Ensure Country vacío (limpiar si autodetectado) > Button: "Create Company" > Verify: error junto a Country | Error inline en Country. Formulario no enviado. Demás campos intactos. **Nota**: Timezone se autodetecta desde browser y siempre se envía, por lo que es difícil testearlo vacío en condiciones normales | 🟠 | ❌ No | ✅ PASS |
| TC-012 | auth/register | AC-9 | Negativo | Error de servidor al guardar → datos conservados | Simular error 500 del backend al crear company | Navigate: /create-company > Fill todos los campos > (mockear error 500) > Button: "Create Company" > Verify: mensaje de error controlado visible (i18n) > Verify: datos del formulario se conservan > Verify: serverErrors se limpia en nuevo intento | Mensaje de error genérico controlado (no stack trace). Datos del formulario permanecen. El usuario puede reintentar. isLoading se resetea en finally | 🟠 | ❌ No | ✅ PASS |
| TC-013 | auth/register | AC-7, AC-NUEVO-1 | Negativo | Postal Code inválido → servicio externo no devuelve datos | Servicio externo disponible pero sin datos para ese CP | Navigate: /create-company > Fill "Postal Code": 00000 (inválido) > Button: "Autofill city & state" > Wait: respuesta del servicio > Verify: State y City NO se autocompletan con datos incorrectos > Verify: toast notification de fallback > Verify: formulario no bloquea al usuario | Los campos State y City quedan vacíos. Toast de fallback visible. El usuario puede ingresarlos manualmente. No hay error crítico | 🟠 | ❌ No | ✅ PASS |
| TC-014 | auth/register | AC-NUEVO-1 | Negativo | Servicio externo de autocompletado caído → modo degradado | Simular API externa no disponible (quitar GEOAPIFY_API_KEY) | Navigate: /create-company > Fill "Postal Code": 10001 > Verify: botón "Autofill city & state" aparece > Button: "Autofill city & state" > Verify: endpoint retorna 404 > Verify: toast notification de fallback > Verify: formulario no bloquea > Verify: State y City editables manualmente | El formulario continúa funcionando sin autocompletado. Endpoint retorna 404 (degradación graceful). Toast informativo. El usuario puede ingresar State y City manualmente | 🔴 | ❌ No | ✅ PASS |
| TC-015 | auth/register | AC-P2 | Negativo | Timezone UTC → Country no se autodetecta incorrectamente | Formulario abierto | Navigate: /create-company > Select "Timezone": UTC > Verify: comportamiento del campo Country > Verify: guard de manual-override no causa comportamiento inesperado | El campo Country no se autocompleta con un país incorrecto. Queda vacío o pide selección manual | 🟠 | ❌ No | ✅ PASS |
| TC-016 | auth/register | AC-6 | Happy Path | Timezone se persiste en `companies.timezone` | Company creada exitosamente con timezone seleccionada | Navigate: /create-company > Select "Timezone": America/New_York > Fill datos válidos > Button: "Create Company" > Verify BD: `SELECT timezone FROM companies WHERE name = '<nombre>' ORDER BY created_at DESC LIMIT 1;` > Verify: timezone = 'America/New_York' | La timezone seleccionada se persiste en `companies.timezone`. El valor en BD coincide con la selección del formulario | 🔴 | ❌ No (BD check) | ✅ PASS |
| TC-017 | auth/register | AC-4 | Edge Case | Contact Name prellenado desde Keycloak | Usuario con nombre completo en Keycloak | Navigate: /create-company > Verify: campo "Contact Name" viene prellenado con `users.name` de Keycloak (nombre completo concatenado) > Verify: campo es editable | Contact Name tiene un valor inicial basado en el nombre completo de Keycloak. El campo es editable | 🟠 | ❌ No | ✅ PASS |
| TC-018 | auth/register | AC-5, AC-4 | Edge Case | Timezone América/Chicago → Country USA | Formulario abierto | Navigate: /create-company > Select "Timezone": America/Chicago > Verify: Country = United States | Country se autocompleta con USA al seleccionar una timezone americana | 🟠 | ❌ No | ✅ PASS |
| TC-019 | auth/register | AC-7 | Edge Case | Postal Code UK → autocompletado UK | Servicio externo con datos UK | Navigate: /create-company > Fill "Postal Code": SW1A 1AA > Button: "Autofill city & state" > Verify: State y City autocompletos con datos de UK | El servicio distingue códigos postales internacionales. Los datos son correctos para UK | 🟡 | ❌ No | ✅ PASS |
| TC-020 | auth/register | AC-4 | Edge Case | Country sin subdivisiones (Bolivia) → State como texto libre | Formulario con Country=Bolivia | Navigate: /create-company > Select "Timezone": America/La_Paz > Verify: Country = Bolivia > Verify: campo State se renderiza como **texto libre** (NO dropdown) > Verify: botón "Autofill city & state" **NO aparece** (Bolivia no usa CP) > Verify: State selector funciona mostrando departamentos | State es texto libre para países sin subdivisiones definidas. Sin botón de autofill para países sin CP. **Nota dev**: En Bolivia sí aparecen departamentos en selector pero no hay botón de autofill por CP | 🟡 | ❌ No | ✅ PASS |
| TC-021 | auth/register | AC-3 | Edge Case | Nombre de Keycloak con caracteres especiales (ñ, á, é...) | Usuario Keycloak con nombre "José García Ñ" | Navigate: /create-company > Verify: banner de identidad muestra nombre completo con caracteres correctos > Verify: sin símbolos extraños ni encoding incorrecto > **Nota**: el nombre se muestra como `users.name` concatenado, no separado en First/Last | Caracteres Unicode se muestran correctamente en el banner de identidad. Sin encoding incorrecto | 🟠 | ❌ No | ✅ PASS |
| TC-022 | auth/register | AC-5, AC-4 | Edge Case | Cambio de timezone después de autodetectar Country → Country se actualiza | Formulario con Country ya autodetectado | Navigate: /create-company > Select "Timezone": America/New_York > Verify: Country = USA > Select "Timezone" (cambiar): Europe/Madrid > Verify: Country se actualiza a Spain | Al cambiar la timezone, el campo Country se actualiza acorde. **Nota**: Si el usuario eligió Country manualmente primero, cambiar timezone NO sobreescribe (guard de manual-override) | 🟠 | ❌ No | ✅ PASS |
| TC-023 | auth/register | AC-7 | Edge Case | Postal Code válido con múltiples resultados | Postal Code que cubre múltiples áreas | Navigate: /create-company > Fill "Postal Code": <CP ambiguo> > Button: "Autofill city & state" > Wait: autocompletado > Verify: el sistema elige un valor o presenta opciones | El sistema maneja la ambigüedad sin crash. Geoapify retorna primer resultado global. Se muestra el resultado más probable | 🟡 | ❌ No | ✅ PASS |
| TC-024 | auth/register | AC-14 | Edge Case | Formulario en tablet (768px) — breakpoint intermedio | Viewport 768px (tablet portrait) | Navigate: /create-company con viewport 768px > Verify: layout coherente sin superposición > Verify: campos accesibles > Verify: botones visibles | Layout en tablet no presenta campos superpuestos ni cortados. Botones accesibles. Sin scroll horizontal | 🟠 | ❌ No (visual) | ✅ PASS |
| TC-025 | auth/register | AC-12 | Edge Case | Back to login después de llenar parcialmente el formulario | Formulario con datos parciales | Navigate: /create-company > Fill Company Name > Fill Timezone > Button: "Back to login" > Verify: redirige al login > Verify: no se crea company parcial en BD | El usuario regresa al login sin ningún dato guardado. Sin company huérfana en BD | 🔴 | ❌ No | ✅ PASS |
| TC-026 | auth/register | AC-7 | Edge Case | Cuota de API de autocompletado agotada (simulado) | Simular cuota 0 tokens disponibles | Navigate: /create-company > Fill "Postal Code": 10001 > Button: "Autofill city & state" > Verify: servicio retorna error de cuota > Verify: toast fallback visible > Verify: formulario no bloquea | El formulario no bloquea. State y City quedan editables. Toast informativo de que el autocompletado no está disponible | 🟠 | ❌ No | ✅ PASS |
| TC-027 | auth/register | AC-7 | Edge Case | Segunda búsqueda del mismo Postal Code usa caché | Postal Code ya buscado previamente | Navigate: /create-company > Fill "Postal Code": 10001 > Button: "Autofill city & state" > Wait: autocompletado > Cambiar CP y volver a 10001 > Button: "Autofill city & state" > Verify: autocompletado inmediato (caché in-process TTL 24h) | El sistema usa el caché. El autocompletado es más rápido. No se consume un token adicional de Geoapify | 🟡 | ❌ No | ✅ PASS |
| TC-028 | auth/register | AC-8 | Edge Case | Submit mientras el autocompletado está en proceso (request pendiente) | CP válido recién ingresado, autocompletado en curso | Navigate: /create-company > Fill "Postal Code" > Button: "Autofill city & state" > Immediately Button: "Create Company" (antes de respuesta API) > Verify: comportamiento | El formulario espera o advierte. No se envían State/City vacíos si son obligatorios. Sin race condition | 🟠 | ❌ No | ✅ PASS |
| TC-029 | auth/register | AC-1, AC-13 | Regresión | El flujo de login existente no se ve afectado | Usuario ya registrado con company | Navigate: /login > Login con credenciales válidas > Verify: login correcto > Verify: company selection funciona > Verify: acceso al dashboard | El login existente funciona sin cambios. Company selection intacto. Dashboard accesible | 🔴 | ✅ Sí | ✅ PASS |
| TC-030 | auth/register | AC-13 | Regresión | Company creada via nuevo formulario aparece en company selection | Company creada con el nuevo formulario | Login con usuario que tiene company creada > Navigate: /company-selection > Verify: la company aparece en la lista | La company creada con el formulario refactorizado está disponible en el selector de companies | 🔴 | ❌ No | ✅ PASS (re-test) |
| TC-031 | auth/register | AC-13 | Regresión | Datos de la company creada correctos en BD (companies + contacts) | Company creada exitosamente | Crear company via formulario > Verify BD: tabla `companies` tiene registro con `name`, `timezone` > Verify BD: tabla `contacts` (morphOne) tiene registro con `country`, `state`, `postal_code`, `contact_name` > Verify: campos Company Name y timezone en `companies` correctos > Verify: campos Country, State, Postal Code, Contact Name en `contacts` correctos | Company Name y timezone persisten en `companies`. Country, State, Postal Code, Contact Name persisten en `contacts` (morphOne). Sin campos nulos no intencionados | 🔴 | ❌ No (BD check) | ✅ PASS |
| TC-032 | auth/register | AC-13 | Regresión | Registro de company sin SSO ya existente (nuevo usuario) | Usuario nuevo que no tiene company | Completar flujo completo Keycloak → /create-company → submit > Verify: flujo completo sin interrupciones | El onboarding completo funciona de inicio a fin. No hay estados intermedios rotos | 🔴 | ❌ No | ✅ PASS (re-test) |
| TC-033 | boards | AC-13 | Regresión | Flow existente ejecuta correctamente después del deploy | Flow activo en staging | Company Login > Sidebar: Boards > Ejecutar flow dev > Verify: resultado correcto | Los flows no se ven afectados. El refactor del formulario no introduce regresión en otros módulos | 🟠 | ❌ No | ✅ PASS |
| TC-034 | auth/users | AC-13 | Regresión | Vista de usuarios sigue funcionando | Usuario con permiso READ_USER | Company Login > Sidebar: Users/Teams > Verify: lista de usuarios carga | El módulo de usuarios no se ve afectado por el refactor del formulario de registro | 🟠 | ❌ No | ✅ PASS |
| TC-035 | auth/settings | AC-13 | Regresión | Vista de Settings sigue funcionando | Usuario con permiso READ_SETTING | Company Login > Sidebar: Settings > Verify: vista carga correctamente | El módulo de settings no se ve afectado | 🟡 | ❌ No | ✅ PASS (re-test) |
| TC-036 | auth/register | AC-6 | Regresión | Timezone en BD correcta después de editar company | Company creada con timezone, luego verificar que se mantiene | Crear company con timezone America/New_York > Login > Navigate: Settings o Profile > Verify: timezone visible > Verify BD: `SELECT timezone FROM companies WHERE name = '<nombre>';` = 'America/New_York' | La timezone del registro persiste en `companies.timezone` y es visible/recuperable en la UI | 🔴 | ❌ No (BD check) | ✅ PASS |
| TC-037 | auth/register | AC-3 | Edge Case | Email no disponible en Keycloak → input editable de email | Usuario Keycloak sin email (edge case) | Navigate: /create-company > Verify: si Keycloak NO trae email → se renderiza input editable con id `register-email` > Verify: input tiene validación > Verify: placeholder visible > Verify: trim funciona en el valor | Si no hay email de Keycloak, aparece input editable de email con validación y trim. Si hay email, se muestra como texto read-only en banner | 🟠 | ❌ No | ✅ PASS |
| TC-CR-001 | auth/register | AC-8 | Code Review | Verificar que City y Address1 son realmente obligatorios en el formulario | Formulario con Company Name, Timezone y Country llenados | Navigate: /create-company > Fill "Company Name": "Test" > Select "Timezone": America/New_York > Verify: Country autodetectado > Leave City y Address 1 vacíos > Button: "Create Company" > Verify: ¿error inline en City y Address1? | El schema Zod marca City y Address1 como requeridos (`min(1)`). El formulario debe mostrar error inline en ambos campos. Verificar si esto contradice la comunicación del Developer (solo Company Name, Timezone, Country obligatorios) | 🟠 | ❌ No | ✅ PASS |
| TC-CR-002 | auth/register | AC-3 | Code Review | Email fallback input: validación Zod con texto no-email | Usuario Keycloak sin email | Navigate: /create-company (usuario sin email Keycloak) > Verify: input `register-email` aparece > Fill: "abc123" (no es email) > Button: "Create Company" > Verify: error de validación email formato > Verify: input usa `type="text"` (no `type="email"`) | Zod valida formato email aunque input es type="text". Error visible. En mobile, teclado NO muestra `@` (UX menor) | 🟡 | ❌ No | ✅ PASS |
| TC-CR-003 | auth/register | AC-4 | Code Review | Company Name sugerido desde email corporativo: verificar UX | Usuario con email corporativo (no free domain) | Navigate: /create-company con email `wodev22789test5@cimario.com` > Verify: Company Name muestra "Cimario" > Verify: indicador "✨ Suggested" visible > Focus en Company Name > Verify: texto se selecciona para fácil reemplazo > Verify: si email es Gmail/Outlook → NO hay sugerencia | Sugerencia "Cimario" visible con indicador. Focus selecciona texto. Free email domains excluidos de sugerencia | 🟡 | ❌ No | ✅ PASS |
| TC-CR-004 | auth/register | AC-12 | Code Review | Back to login con datos parciales: sin confirmación de pérdida de datos | Formulario con datos parciales ingresados | Navigate: /create-company > Fill "Company Name": "Test" > Select "Timezone" > Fill "Postal Code" > Button: "Back to login" > Verify: ¿se muestra diálogo de confirmación? > Verify: ¿los datos se pierden? > Verify BD: no se crea company parcial | El sistema ejecuta logout directamente sin confirmación. Los datos del formulario se pierden. Sin company huérfana en BD. (Decisión de diseño, no bug — pero verificar) | 🟠 | ❌ No | ✅ PASS |
| TC-CR-005 | auth/settings | AC-13 | Code Review | Settings > Company Profile: CompanyForm funciona en contexto de edición | Usuario Company con company existente y permiso UPDATE_COMPANY | Company Login > Sidebar: Settings > Verify: CompanyForm carga en modo edición (isRegisterContext=false) > Verify: sección Contact Details visible (no se muestra en registro) > Verify: campos editables > Verify: email editable > Verify: status selector visible | El CompanyForm funciona correctamente en Settings. Secciones distintas al registro. Sin regresión por el redesign | 🟠 | ❌ No | ✅ PASS |

---

## Casos de Regresión — Resumen

| ID | Módulo impactado | Caso de regresión | Por qué podría romperse | Prioridad | Estado |
|----|-----------------|-------------------|------------------------|-----------|--------|
| REG-001 | auth/login | Login existente sin impacto | Refactor del form puede afectar routing/guards | 🔴 | ⬜ |
| REG-002 | auth/company-selection | Company creada aparece en el selector | Schema changes pueden no mapear correctamente | 🔴 | ⬜ |
| REG-003 | BD/companies + contacts | Datos correctos en tablas companies y contacts | Campos nuevos en contacts (morphOne) pueden fallar | 🔴 | ⬜ |
| REG-004 | auth/onboarding | Flujo completo nuevo usuario | Cambios en /create-company pueden romper el flujo post-Keycloak | 🔴 | ⬜ |
| REG-005 | boards | Ejecución de flows no afectada | Deploy general puede introducir regresión | 🟠 | ⬜ |
| REG-006 | auth/users | Vista de usuarios intacta | Comparte guards/middleware con el módulo auth | 🟠 | ⬜ |
| REG-007 | auth/settings | Vista de settings intacta | Comparte guards/middleware con el módulo auth | 🟡 | ⬜ |

---

## Queries de Verificación BD

> ⚠️ Queries construidas EXCLUSIVAMENTE desde información confirmada por el Developer en TDD Build (29-jun).
> **Hallazgo clave**: Country, State, Postal Code y Contact Name están en tabla `contacts` (morphOne), NO en `companies`. Solo `timezone` está en `companies`.

```sql
-- TC-016: Verificar timezone en companies
-- Fuente: TDD Build 29-jun (TC-031 + TC-016/TC-036)
-- Tabla: companies | Columna verificada: timezone
SELECT id, name, timezone, created_at
FROM companies
WHERE name = '<nombre-de-company-de-test>'
ORDER BY created_at DESC
LIMIT 1;
-- Esperado: timezone = '<timezone-seleccionada-en-formulario>'

-- TC-031: Verificar datos de contacto en tabla contacts (morphOne)
-- Fuente: TDD Build 29-jun (TC-031)
-- Tabla: contacts | Columnas: country, state, postal_code, contact_name (nombres exactos pendientes de verificar en migraciones)
-- ⚠️ PENDIENTE: verificar nombres exactos de columnas leyendo migraciones del repo gateway
SELECT c.id, c.name, c.timezone, ct.*
FROM companies c
LEFT JOIN contacts ct ON ct.contactable_id = c.id AND ct.contactable_type LIKE '%Company%'
WHERE c.name = '<nombre-de-company-de-test>'
ORDER BY c.created_at DESC
LIMIT 1;
-- Esperado: todos los campos del formulario presentes con valores correctos

-- TC-030: Verificar que la company aparece para el usuario que la creó
-- Fuente: migración 2024_11_26_092110_create_company_user_table.php
SELECT c.id, c.name, c.timezone
FROM companies c
INNER JOIN company_user cu ON c.id = cu.company_id
INNER JOIN users u ON cu.user_id = u.id
WHERE u.email = '<email-del-tester>'
ORDER BY c.created_at DESC
LIMIT 5;
-- Esperado: la nueva company aparece en la relación company_user

-- TC-036: Verificar timezone persiste después de login
-- Misma query que TC-016 pero ejecutada después de login y navegación
SELECT timezone FROM companies WHERE name = '<nombre-de-test>';
-- Esperado: la timezone seleccionada en el formulario
```
