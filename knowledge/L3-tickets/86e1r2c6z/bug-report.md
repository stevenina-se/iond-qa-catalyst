# Reporte de Bugs — 86e1r2c6z
# Refactorizar flujo y formulario de registro de compañía

> Generado: 2026-07-17 | Testing Sesión 1 — Post-Registro
> Entorno: https://dev-app.ionflow.io | Branch: DEVELOPMENT
> QA Engineer: Steve Nina | Usuario de prueba: testqacatalyst2026@gmail.com
> Company creada: "QA Catalyst Test Company"

---

## Resumen

| Métrica | Valor |
|---------|-------|
| Bugs críticos (Blocker) | 1 |
| Bugs altos (Major) | 1 |
| Bugs medios | 1 |
| **Total** | **3** |
| **Veredicto** | ❌ **REJECTED** |

---

## BUG-001 — 403 Forbidden en Settings, Teams y Accounts después del registro

| Campo | Valor |
|-------|-------|
| **Severidad** | 🔴 **BLOCKER** |
| **Tipo** | Funcional — Permisos/Autorización |
| **AC afectado** | AC-1, AC-12, AC-13 |
| **TCs afectados** | TC-035, TC-034, TC-CR-005 |
| **Reproducible** | ✅ Sí — 100% reproducible |

### Descripción

Después de registrar una company exitosamente a través de `/create-company`, el usuario es redirigido al Company Dashboard. Sin embargo, al intentar acceder a **Settings**, **Teams** o **Accounts**, el sistema muestra **"403 Forbidden Resource"** y redirige a `/403`.

### Pasos para reproducir

1. Registrar un nuevo usuario en Keycloak
2. Login → el sistema redirige a `/create-company`
3. Completar todos los campos obligatorios del formulario
4. Click "New Company" → Toast "Success: Save successful" → Redirect a Dashboard ✅
5. Click en Sidebar → **Settings** → **403 Forbidden** ❌
6. Click en Sidebar → **Teams** → **403 Forbidden** ❌
7. Click en Sidebar → **Accounts** → **403 Forbidden** ❌

### Resultado esperado

El usuario que registra una company debe tener **todos los permisos básicos** (Owner/Admin de su propia company) y poder acceder a Settings, Teams y Accounts inmediatamente después del registro.

### Resultado actual

El usuario queda con permisos insuficientes después del registro. Solo puede ver:
- ✅ Dashboard (carga pero sin company name en header)
- ✅ Boards (/workflows — carga vacío)
- ✅ Users (/users — carga vacío)
- ❌ Settings → 403
- ❌ Teams → 403
- ❌ Accounts → 403

### Análisis de causa raíz (hipótesis)

El endpoint `POST /companies` en el backend (Laravel) crea la company y la relación `company_user`, pero **no asigna los roles/permisos necesarios** al usuario. El sistema de permisos de Ionflow requiere que el usuario tenga roles específicos (READ_SETTING, READ_TEAM, READ_ACCOUNT, etc.) para acceder a cada vista. El registro no está asignando estos roles.

Alternativamente, podría ser que el `schema_suffix` generado por el frontend (`Date.now()`) no coincide con lo que el backend espera para configurar las tablas tenant del usuario.

### Evidencia

- `screenshots/BUG-002-settings-403.png` — Settings muestra 403
- `screenshots/BUG-002-teams-403.png` — Teams muestra 403
- `screenshots/BUG-002-accounts-403.png` — Accounts muestra 403

### Impacto

**BLOQUEANTE**: El usuario que registra una company nueva no puede administrar su propia empresa. El flujo de registro es funcionalmente inútil si el usuario no puede acceder a Settings para configurar su company.

---

## BUG-002 — /profile no carga datos de contacto después del registro

| Campo | Valor |
|-------|-------|
| **Severidad** | 🟠 **MAJOR** |
| **Tipo** | Funcional — Persistencia de datos |
| **AC afectado** | AC-1, AC-9 |
| **TCs afectados** | TC-031, TC-016 |
| **Reproducible** | ✅ Sí — 100% reproducible |

### Descripción

Después de registrar una company con todos los campos (Country, State, City, Address, Phone, Postal Code), al navegar a `/profile`, la página muestra un toast **"Error: Failed to load contact data"** y todos los campos de Personal Information (Phone, Country, State, City, Address, Postal Code) están **vacíos**.

### Pasos para reproducir

1. Registrar company con datos completos:
   - Company Name: "QA Catalyst Test Company"
   - Contact Name: "Test QACatalyst"
   - Timezone: America/New_York
   - Country: United States
   - State: New York
   - City: New York
   - Address 1: "123 Test Avenue"
   - Address 2: "Suite 42"
   - Phone: "+1234567890"
   - Postal Code: "10001"
2. Post-registro → Dashboard
3. Navigate → `/profile`
4. Toast error: **"Failed to load contact data"**
5. Campos de Personal Information: todos vacíos excepto Name y Email

### Resultado esperado

Los datos de contacto registrados deben persistir y estar disponibles en `/profile`. Al mínimo:
- Phone: "+1234567890"
- Country: United States
- State: New York
- City: New York
- Address: "123 Test Avenue"
- Postal Code: "10001"

### Resultado actual

- Name: "Test QACatalyst" ✅ (viene de Keycloak, no del formulario)
- Email: "testqacatalyst2026@gmail.com" ✅ (viene de Keycloak)
- Phone: vacío ❌
- Country: vacío ❌
- State: vacío ❌
- City: vacío ❌
- Address: vacío ❌
- Postal Code: vacío ❌

### Análisis de causa raíz (hipótesis)

El formulario de registro envía los datos de contacto al endpoint `POST /companies`, que los almacena en la tabla `contacts` (relación morphOne). Sin embargo, la vista `/profile` probablemente busca los datos de contacto del **usuario** (tabla `users` o su relación `contact`), NO de la company. Hay una desconexión entre dónde se guardan los datos (company.contact) y dónde `/profile` los busca (user.contact).

### Evidencia

- `screenshots/BUG-001-profile-empty.png` — Profile con error toast y campos vacíos

---

## BUG-003 — Company name no se muestra en el header del dashboard post-registro

| Campo | Valor |
|-------|-------|
| **Severidad** | 🟡 **MINOR** |
| **Tipo** | UI/UX — Feedback visual |
| **AC afectado** | AC-1 |
| **TCs afectados** | TC-030 |
| **Reproducible** | ✅ Sí |

### Descripción

Después de registrar la company "QA Catalyst Test Company", el header del dashboard solo muestra el nombre del usuario ("Test QACatalyst") y el email, pero **NO el nombre de la company**. El usuario no tiene confirmación visual de que su company fue creada correctamente.

### Resultado esperado

El header debería mostrar el nombre de la company ("QA Catalyst Test Company") en algún lugar visible — por ejemplo, junto al nombre del usuario o como subtítulo.

### Resultado actual

Solo se muestra "Test QACatalyst" y "testqacatalyst2026@gmail.com" en el header. Ninguna mención a la company creada.

### Evidencia

- `screenshots/BUG-003-dashboard-no-company.png`

---

## Notas del QA Engineer

### Autocrítica

El veredicto anterior (APPROVED) fue **incorrecto**. El error fue:
1. No verificar el flujo post-registro completo (solo verifiqué que el dashboard cargaba)
2. No navegar a vistas críticas como Settings, Profile, Teams después del registro
3. No verificar persistencia de datos
4. Confiar en que "el dashboard carga" = "todo funciona"

### Lección aprendida

El test de un flujo de **registro** DEBE incluir verificación de:
- ✅ Formulario → Submit → Toast ✅
- ❌ Permisos del usuario post-registro → 403
- ❌ Persistencia de datos en Profile → vacío
- ❌ Accesibilidad a todas las vistas del tenant → 403

---

## Historial

| Fecha | Acción | Por |
|-------|--------|-----|
| 2026-07-17 18:36 | Bugs reportados por QA Engineer (Steve Nina) — observó 403 y profile vacío | QA Engineer |
| 2026-07-17 18:38 | Investigación con Playwright MCP — confirmados BUG-001, BUG-002, BUG-003 | QA Catalyst |
| 2026-07-17 18:41 | Evidencia capturada — 6 screenshots | QA Catalyst |
