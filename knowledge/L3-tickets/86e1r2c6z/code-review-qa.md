# Code Review QA — 86e1r2c6z (Modo Deployment / Bug Hunting)

> Generado: 2026-07-17 | Skill: code-review/review (modo Deployment)
> Ticket: Refactorizar flujo y formulario de registro de compañía
> QA Engineer: Steve Nina | Developer: Gustavo Mamani
> Code Review LD: Rodolfo Merlo Ali ✅ | Enrique Vicente ✅

---

## Resumen

| Métrica | Valor |
|---------|-------|
| Repos revisados | `gateway-ion`, `flow_binaries` |
| Archivos modificados analizados | 51 (43 gateway-ion + 8 flow_binaries) |
| Bugs confirmados (reproducibles) | 0 |
| Riesgos a verificar en testing | 5 |
| Módulos con impacto cruzado | auth (principal), settings (UpdateCompanyForm comparte CompanyForm) |
| TCs inyectados en test-matrix | 5 (TC-CR-001 a TC-CR-005) |

> ✅ El código está bien estructurado. El code review del LD (Rodolfo + Enrique) ya capturó y corrigió los issues más graves (H1-H3, M1-M4). Los hallazgos del QA code review son riesgos a verificar en testing, no bugs bloqueantes.

---

## Archivos Modificados

### REPO: gateway-ion (43 archivos, +6583/-359 líneas)

**Archivos clave del ticket:**
| Archivo | Cambio | Relevancia |
|---------|--------|------------|
| `src/components/CompanyForm.vue` | Redesign completo (+677 líneas) | 🔴 Core — formulario principal |
| `src/models/company.ts` | Schema de validación Zod (+24 líneas) | 🔴 Validaciones |
| `src/services/postal.service.ts` | Nuevo servicio (+29 líneas) | 🟠 Autofill |
| `src/views/tenant/company/CreateCompany.vue` | Layout actualizado (+71 líneas) | 🟠 Vista principal |
| `src/views/Section.tsx` | Panel izquierdo restyled (+66 líneas) | 🟡 Visual |
| `src/assets/states.json` | Datos de estados por país (+5359 líneas) | 🟡 Datos estáticos |
| `src/lang/en/message.ts` | 16 nuevas keys i18n | 🟡 i18n |
| `src/lang/es/message.ts` | 16 nuevas keys i18n | 🟡 i18n |
| `src/components/CompanyForm.spec.ts` | 17 tests unitarios (+332 líneas) | ✅ Cobertura |

**Archivos colaterales (otros módulos):**
| Archivo | Cambio | Relevancia |
|---------|--------|------------|
| `src/views/tenant/settings/components/UpdateCompanyForm.vue` | Ajustado (+94 líneas) | 🟠 Impacto cruzado — Settings |
| `src/views/CompanySelectionView.vue` | Minor (+2 líneas) | 🟡 Regresión |
| `src/composables/useLocale.ts` | Nuevo composable (+8 líneas) | 🟡 Utilidad compartida |

### REPO: flow_binaries (8 archivos, +426/-0 líneas)

| Archivo | Cambio | Relevancia |
|---------|--------|------------|
| `backend/ion/controllers/geoapify_controller.go` | Nuevo controller (+33 líneas) | 🟠 Endpoint postal lookup |
| `backend/ion/services/geoapify/service.go` | Nuevo servicio con caché (+221 líneas) | 🟠 Lógica de negocio |
| `backend/ion/services/geoapify/config.go` | Config desde env (+20 líneas) | 🟡 Config |
| `backend/routes/api.go` | Nueva ruta (+2 líneas) | 🟠 Routing con auth |
| `backend/.env.example` | Vars Geoapify (+5 líneas) | 🟡 Configuración |
| `backend/ion/controllers/geoapify_controller_test.go` | Tests (+65 líneas) | ✅ Cobertura |
| `backend/ion/services/geoapify/service_test.go` | Tests (+75 líneas) | ✅ Cobertura |

---

## Bugs Confirmados (Reproducibles)

> ✅ No se encontraron bugs reproducibles bloqueantes. El code review del LD ya corrigió los issues más graves.

---

## Riesgos a Verificar

### BUG-CR-001: Schema Zod requiere `city` y `address1` como obligatorios pero el Developer dijo que no lo son
- **Clasificación**: RIESGO A VERIFICAR
- **Severidad**: 🟠 Alto
- **Repo**: gateway-ion
- **Archivo**: `src/models/company.ts` — líneas 26-27
- **Evidencia**:
  ```typescript
  // línea 26
  city: z.string({ required_error: 'City is required' }).trim().min(1, { message: 'City is required' }).max(255, ...),
  // línea 27
  address1: z.string({ required_error: 'Address1 is required' }).trim().min(1, { message: 'Address1 is required' }).max(255, ...),
  ```
- **Descripción**: El schema `CompanyCreateSchema` marca `city` y `address1` como **obligatorios** (`min(1)` + `required_error`). Sin embargo, en las correcciones del code review (M4), el Developer indicó que los campos obligatorios son **Company Name, Timezone y Country**. Si el usuario intenta enviar sin city ni address1, el formulario bloqueará el envío con error inline — esto puede ser intencional o una inconsistencia con lo que el Developer comunicó.
- **Escenario para verificar**:
  1. Navigate: /create-company
  2. Fill: Company Name, Timezone, Country (los 3 obligatorios según Developer)
  3. Leave City y Address 1 vacíos
  4. Button: "Create Company"
  5. Verificar: ¿el formulario se envía o muestra error en City y Address 1?
- **Por qué es riesgo**: Si City y Address1 son realmente obligatorios en el schema pero no lo son para el negocio, el formulario podría bloquear registros legítimos
- **Impacto potencial**: Usuarios no pueden registrar company sin city ni address1
- **Módulos afectados**: auth/register

### BUG-CR-002: El email fallback input (Keycloak sin email) usa `type="text"` en lugar de `type="email"`
- **Clasificación**: RIESGO A VERIFICAR
- **Severidad**: 🟡 Medio
- **Repo**: gateway-ion
- **Archivo**: `src/components/CompanyForm.vue` — líneas 382-391
- **Evidencia**:
  ```html
  <!-- línea 385 -->
  <InputText
    id="register-email"
    v-model="email"
    type="text"       <!-- ← debería ser type="email" para validación nativa del browser -->
    :placeholder="$t('message.emailPlaceholder')"
    ...
  />
  ```
- **Descripción**: Cuando Keycloak no provee email, se renderiza un input editable. El input usa `type="text"` en lugar de `type="email"`. Aunque Zod valida el formato email en el schema (`z.string().email()`), el browser no mostrará validación nativa (teclado de email en mobile, autocompletado, etc.)
- **Escenario para verificar**:
  1. Navigate: /create-company (con usuario Keycloak sin email)
  2. Verificar: input de email aparece
  3. Ingresar texto no-email (ej. "abc123")
  4. Button: "Create Company"
  5. Verificar: ¿se muestra error de validación de Zod? ¿El browser muestra sugerencia de formato?
- **Por qué es riesgo**: En mobile, `type="text"` no muestra teclado con `@`, degradando UX
- **Impacto potencial**: UX menor, validación funciona igual via Zod

### BUG-CR-003: Company Name sugerido desde dominio de email podría ser inapropiado
- **Clasificación**: RIESGO A VERIFICAR
- **Severidad**: 🟡 Medio
- **Repo**: gateway-ion
- **Archivo**: `src/components/CompanyForm.vue` — líneas 90-100
- **Evidencia**:
  ```typescript
  // líneas 94-100
  const companySuggestion = computed(() => {
    if (!props.isRegisterContext) return '';
    const domain = authStore.user?.email?.split('@')[1]?.toLowerCase();
    if (!domain || FREE_EMAIL_DOMAINS.has(domain)) return '';
    const sld = domain.split('.')[0];
    return sld ? sld.charAt(0).toUpperCase() + sld.slice(1) : '';
  });
  ```
- **Descripción**: El Company Name se pre-sugiere extrayendo el second-level domain del email. La lista de dominios gratuitos (`FREE_EMAIL_DOMAINS`) es limitada (10 dominios). Emails corporativos con subdomains (ej. `user@mail.company.com`) extraerían "Mail" como sugerencia, no "Company". Emails de universidades o instituciones (ej. `@umsa.bo`) podrían sugerir "Umsa" lo cual sería correcto pero poco amigable.
- **Escenario para verificar**:
  1. Navigate: /create-company con email `wodev22789test5@cimario.com`
  2. Verificar: Company Name muestra "Cimario" como sugerencia
  3. Verificar: el campo tiene indicador visual "✨ Suggested"
  4. Verificar: al hacer focus, el texto se selecciona para fácil reemplazo
- **Por qué es riesgo**: La sugerencia podría ser incorrecta para emails con subdomains
- **Impacto potencial**: UX menor — el campo es editable y la sugerencia es solo eso

### BUG-CR-004: `handleCancel` (Back to Login) no verifica datos parciales ni muestra confirmación
- **Clasificación**: RIESGO A VERIFICAR
- **Severidad**: 🟠 Alto
- **Repo**: gateway-ion
- **Archivo**: `src/views/tenant/company/CreateCompany.vue` — líneas 65-73
- **Evidencia**:
  ```typescript
  // líneas 65-73
  const handleCancel = async () => {
    const authType = localStorage.getItem('auth_type');
    if (authType === 'keycloak') {
      await authStore.logoutKeycloak();
    } else {
      authStore.logout();
      router.push({ name: 'Login' });
    }
  };
  ```
- **Descripción**: Cuando el usuario hace click en "Back to Login", el sistema ejecuta logout inmediatamente sin verificar si hay datos parciales en el formulario ni pedir confirmación. Si el usuario llenó datos pero no los envió, todo se pierde. El TC-025 cubre parcialmente esto (verifica que no se cree company huérfana), pero la UX de no pedir confirmación podría ser intencional (decisión de diseño).
- **Escenario para verificar**:
  1. Navigate: /create-company
  2. Fill: Company Name, Timezone, Postal Code
  3. Button: "Back to login"
  4. Verificar: ¿se muestra confirmación "¿Seguro que deseas salir?" o sale directamente?
  5. Verificar: ¿los datos se pierden? (esperado: sí, por decisión de diseño)
  6. Verificar: ¿no se crea company parcial en BD?
- **Por qué es riesgo**: Pérdida de datos del formulario sin confirmación
- **Impacto potencial**: UX — el usuario podría perder datos accidentalmente

### BUG-CR-005: El endpoint `/api/1.0/postal-codes/lookup` está bajo JWT auth pero NO bajo tenant auth
- **Clasificación**: RIESGO A VERIFICAR
- **Severidad**: 🟡 Medio
- **Repo**: flow_binaries
- **Archivo**: `backend/routes/api.go` — línea 154
- **Evidencia**:
  ```go
  // línea 151-154
  g := r.PathPrefix("/api/1.0").Subrouter()
  g.Use(middleware.JWTAuthMiddleware)

  g.HandleFunc("/postal-codes/lookup", controllers.LookupPostalCode).Methods("GET")
  ```
- **Descripción**: El endpoint de postal lookup está bajo `JWTAuthMiddleware` (Keycloak auth) pero NO bajo `TenantAuthMiddleware`. Esto es correcto para el contexto de registro (el usuario aún no tiene company/tenant), pero significa que cualquier usuario autenticado con JWT puede consumir la API de Geoapify sin restricción de tenant. En el contexto de registro, esto es el comportamiento esperado — el usuario no tiene company aún.
- **Escenario para verificar**:
  1. Login como Company User normal
  2. GET `/api/1.0/postal-codes/lookup?postal=10001&country=US`
  3. Verificar: ¿el endpoint responde? (esperado: sí, tiene JWT)
  4. Verificar: ¿hay rate limiting? (el caché mitiga, pero no hay rate limit explícito)
- **Por qué es riesgo**: Un usuario autenticado podría abusar del endpoint para agotar la cuota Geoapify (3000 req/día). El caché mitiga (misma key se sirve desde caché), pero keys distintas consumen un token cada una.
- **Impacto potencial**: Agotamiento de cuota Geoapify si se abusa del endpoint con CPs distintos
- **Módulos afectados**: auth/register, flow_binaries API

---

## Impacto Cruzado

| Módulo Impactado | Componente Afectado | Riesgo | Verificación Necesaria |
|---|---|---|---|
| auth/settings | `UpdateCompanyForm.vue` — comparte `CompanyForm.vue` | 🟠 Alto | Verificar que Settings/Company sigue funcionando con el CompanyForm rediseñado (props `isRegisterContext=false`) |
| auth/company-selection | `CompanySelectionView.vue` — minor change (+2 líneas) | 🟡 Bajo | TC-030 cubre regresión |
| i18n | Nuevas keys en EN/ES | 🟡 Bajo | TC i18n verifica labels |

> **Nota**: `CompanyForm.vue` se usa en DOS contextos: (1) Registro (`isRegisterContext=true`) y (2) Settings/Update (`isRegisterContext=false`). El template muestra secciones distintas según este flag. Los riesgos de regresión en Settings deben cubrirse.

---

## TCs Inyectados en Test Matrix

| TC ID | Origen | Caso de Test | Severidad |
|-------|--------|-------------|-----------|
| TC-CR-001 | BUG-CR-001 | Verificar que City y Address1 son realmente obligatorios — intentar submit sin ellos | 🟠 |
| TC-CR-002 | BUG-CR-002 | Email fallback (sin Keycloak email): verificar validación Zod con texto no-email | 🟡 |
| TC-CR-003 | BUG-CR-003 | Company Name sugerido desde email corporativo: verificar sugerencia y UX de reemplazo | 🟡 |
| TC-CR-004 | BUG-CR-004 | Back to login con datos parciales: verificar que no hay confirmación y no se crea company parcial | 🟠 |
| TC-CR-005 | BUG-CR-005 | Settings > Company profile: verificar que el CompanyForm funciona correctamente en contexto de edición (no registro) | 🟠 |

---

## Observaciones Positivas

1. ✅ **Autenticación del endpoint**: El endpoint postal está bajo `JWTAuthMiddleware` — no es público (H1 corregido)
2. ✅ **Caché robusta**: Implementación in-process con TTL positivo (24h) y negativo (1h) + cleanup goroutine
3. ✅ **Degradación graceful**: Si `GEOAPIFY_API_KEY` no está configurada, el servicio retorna `nil` y el frontend muestra toast
4. ✅ **Guard de manual-override**: Si el usuario eligió Country manualmente, cambiar timezone NO sobreescribe (`countryTouchedByUser` flag)
5. ✅ **Input sanitization**: `TrimSpace` en backend Go + `trimOnBlur` + `trimFields` en frontend
6. ✅ **i18n completo**: Todos los textos en EN/ES, incluyendo panel izquierdo
7. ✅ **Tests unitarios**: 17 tests en frontend (CompanyForm.spec.ts) + 7 tests en backend (controller + service)
8. ✅ **`isAutofilling` flag**: Previene que el watcher de `country` limpie `state` durante autocompletado
9. ✅ **`maxResponseBytes` limit**: Protección contra respuestas grandes de Geoapify (256KB)
10. ✅ **`logMissingKeyOnce`**: Solo logea una vez si la API key no está configurada (evita spam de logs)

---

## Historial

| Fecha | Acción | Por |
|-------|--------|-----|
| 2026-07-17 | Code Review QA generado — Deployment track, Bug Hunting mode | QA Catalyst |
