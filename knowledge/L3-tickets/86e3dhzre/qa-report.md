# QA Report — [Deploy] Nuevo template de login Keycloak (IOND)

| Campo | Valor |
|---|---|
| **Ticket** | [86e3dhzre](https://app.clickup.com/t/86e3dhzre) |
| **Status** | Ready for QA |
| **Prioridad** | High |
| **Fecha** | 2026-10-01 |
| **Ambiente** | `https://dev-app.ionflow.io` → `sso.omniorders.com` / realm `AuthFlow` |
| **Herramienta** | Playwright MCP (Canal 1) |
| **Credenciales** | `bafejeg787@flakeian.com` |

---

## 🚨 Bug 1 — SSO Callback Error 401 (BLOCKER)

### Descripción

Keycloak autentica correctamente al usuario con el nuevo template. Sin embargo, cuando Keycloak redirige de vuelta a la aplicación IOND (`dev-app.ionflow.io`), el callback SSO falla con un **HTTP 401 Unauthorized**. El usuario queda atrapado y nunca accede al producto.

### Reproducción (100%)

```
1. Navegar a https://dev-app.ionflow.io
2. Keycloak redirige a: https://sso.omniorders.com/realms/AuthFlow/protocol/openid-connect/auth?...
3. Ingresar email → Continue → password → Sign In
4. Keycloak autentica OK → redirige a IOND con code+state en URL
5. IOND muestra "Signing you in... Please wait while we complete the SSO authentication."
6. ❌ Error toast: "SSO Error — AxiosError: Request failed with status code 401"
7. Pantalla cambia a: "We couldn't complete the SSO authentication." + botón "Retry now"
8. "Retry now" → vuelve a fallar con el mismo error
```

### Evidencia

- Screenshot: `screenshots/tc04-sso-error-401.png`
- Screenshot mobile: `screenshots/responsive-mobile-error.png`

### Análisis técnico — ¿Qué necesita cambiar en IOND?

> El error **401** ocurre en el **lado de IOND**, no en Keycloak. Keycloak autentica correctamente y redirige con un authorization code válido. El problema está en el **exchange del code por tokens** o en la **validación del token** por parte de la app.

**Causas probables (en orden de probabilidad):**

| # | Causa | Qué verificar/modificar en IOND |
|---|---|---|
| 1 | **KEYCLOAK_REALM_PUBLIC_KEY no actualizada** | El ticket menciona que la PUBLIC_KEY debe pedirse a un admin de Keycloak para el realm `AuthFlow`. Si IOND sigue usando la PUBLIC_KEY del realm viejo, la validación del JWT falla → 401 |
| 2 | **Issuer mismatch** | El token emitido por `sso.omniorders.com/realms/AuthFlow` tiene un `iss` claim diferente al que IOND espera. Verificar que la config de IOND acepta el issuer del nuevo realm |
| 3 | **CLIENT_SECRET incorrecto para AuthFlow** | Aunque el ticket dice "mismo client", el secret pudo cambiar al migrar al nuevo realm. Verificar que `KEYCLOAK_CLIENT_SECRET` es válido para `AuthFlow` |
| 4 | **Audience validation** | El nuevo realm puede emitir tokens con un `aud` diferente. IOND debe aceptar el audience correcto |
| 5 | **CORS/redirect_uri** | El callback endpoint de IOND puede no estar registrado como `redirect_uri` válido en el nuevo realm `AuthFlow` |

**Acción requerida del equipo de desarrollo:**

```
1. Verificar que las variables de entorno de IOND estén actualizadas:
   - KEYCLOAK_ENDPOINT=https://sso.omniorders.com
   - KEYCLOAK_REALM=AuthFlow
   - KEYCLOAK_REALM_PUBLIC_KEY=<nueva key del realm AuthFlow>
   
2. Verificar en Keycloak admin que:
   - El client de IOND tiene la redirect_uri correcta (https://dev-app.ionflow.io/*)
   - El client secret es el correcto
   
3. Verificar en los logs del backend de IOND:
   - El endpoint de callback (/api/auth/sso/callback o similar)
   - El error exacto al hacer el token exchange
   - Si el JWT se está validando con la public key incorrecta
```

### ACs bloqueados por este bug

| AC | Descripción |
|---|---|
| AC-3 | Login con email y contraseña funciona y da acceso al producto |
| AC-5 | "Stay signed in" mantiene sesión al cerrar browser |
| AC-6 | Logout explícito cierra sesión |
| AC-7 | Checkbox no autocompleta email ni contraseña (post-login) |
| AC-12 | Login con contraseña y OIDC existente siguen funcionando |

---

## 🟡 Bug 2 — Prefill de Registro no funciona (MEDIUM)

### Descripción

La URL de registro con parámetros `?email=`, `firstName=` y `lastName=` no prellena los campos del formulario. Todos aparecen vacíos.

### Reproducción (100%)

```
1. Navegar a la URL de registro con parámetros (click "Sign up" → agregar ?email=test@test.com&firstName=John&lastName=Doe)
2. El formulario muestra todos los campos vacíos
3. Esperado: Email, First name y Last name prellenados y en read-only
```

### Evidencia

- Screenshot: `screenshots/tc07-registration-prefill-fail.png`

---

## 🟡 Bug 3 — Badge "TESTING" se sobrepone a UI en Mobile (LOW-MEDIUM)

### Descripción

En resoluciones mobile, el badge flotante amarillo "TESTING" (indicador de ambiente) se sobrepone a elementos funcionales de la interfaz:

- **Mobile portrait (375x667)**: Se superpone al botón "Sign in with Google", haciendo que el texto del botón sea ilegible ("Si **TESTING** Google")
- **Mobile landscape (667x375)**: Se superpone al campo de Email y al separador "Or sign in with" al hacer scroll

### Evidencia

- Screenshot portrait: `screenshots/responsive-mobile-375.png`
- Screenshot landscape: `screenshots/responsive-landscape-667.png`

> **Nota**: Si este badge es **solo para ambientes de testing/staging** y no aparece en producción, este bug tiene prioridad baja. Si aparece en producción, la prioridad sube.

---

## 🟡 Bug 4 — Pantalla de error SSO vacía en mobile (MEDIUM)

### Descripción

En viewport mobile (375×667), la pantalla de error SSO se muestra **completamente en blanco**. El mensaje "We couldn't complete the SSO authentication", el toast de error y el botón "Retry now" **no son visibles**. El usuario en mobile no tiene feedback de que algo falló ni forma de reintentar.

### Evidencia

- Screenshot: `screenshots/responsive-mobile-error.png`

---

## ⚠️ Discrepancias AC vs Implementación — Requieren aclaración

Se encontraron 3 discrepancias entre lo que describe el ticket y lo que se observa en el template implementado. **Se requiere aclaración del Developer antes de considerarlas bug o feature intencional.**

### 1. Flujo de login en 2 pasos vs "Una sola pantalla de login con contraseña"

| Ticket dice | Implementación real |
|---|---|
| "Una sola pantalla de login con contraseña" | El flujo es en **2 pasos**: Paso 1 (Email + "Stay signed in" + Continue) → Paso 2 (Password + Sign In) |

**Pregunta**: ¿El flujo de 2 pasos es intencional (por seguridad, para determinar el Authentication Flow del usuario antes de mostrar password vs IdP)? ¿O debería ser una sola pantalla?

### 2. Separador "Or sign in with" vs "Or"

| Ticket dice | Implementación real |
|---|---|
| "Sign in with Google y Sign in with Apple **debajo de 'Or'**" | El separador dice **"Or sign in with"** (no solo "Or") |

**Pregunta**: ¿Es intencional que el separador diga "Or sign in with" o debería decir simplemente "Or"?

### 3. Selector de idioma visible (fuera de alcance del ticket)

| Ticket dice | Implementación real |
|---|---|
| "Selector de idioma (**segunda etapa; fuera de alcance**)" | Hay un dropdown **"English v"** visible en la esquina superior derecha de la pantalla de login |

**Pregunta**: El ticket dice explícitamente que el selector de idioma está fuera de alcance. Sin embargo, ya está implementado y visible. ¿Se incluyó como parte del template base de Keycloak? ¿O se añadió intencionalmente adelantando la segunda etapa? No se marca como bug, solo como discrepancia vs alcance documentado.

---

## 🔍 Análisis de Coherencia de Mensajes de Error

### Mensajes del flujo SSO cuando falla

| Momento | Mensaje | ¿Coherente? |
|---|---|---|
| **Mientras carga** | "Signing you in... Please wait while we complete the SSO authentication." | ✅ Claro y correcto |
| **Toast de error** | "SSO Error — AxiosError: Request failed with status code 401" | ❌ **Expone detalles técnicos al usuario final**. "AxiosError" y "status code 401" son información de implementación interna |
| **Mensaje post-error** | "We couldn't complete the SSO authentication." | ✅ Mensaje genérico correcto para el usuario |
| **Botón de acción** | "Retry now" | ⚠️ **Parcialmente coherente** — El retry siempre falla porque el problema es de configuración, no transitorio. El botón da la falsa impresión de que reintentar puede funcionar |

### Recomendaciones de UX para mensajes de error

1. **El toast no debería exponer `AxiosError` ni el status code** al usuario final. Sugerir reemplazar por: *"SSO Error — We had trouble verifying your credentials. Please try again or contact support."*
2. **El botón "Retry now"** está bien como opción, pero si el retry falla N veces debería mostrar un mensaje diferente como: *"This issue persists. Please contact your administrator."*
3. **Falta un link de contacto/soporte** en la pantalla de error

---

## 📱 Testing Responsivo

### Resumen por viewport

| Viewport | Resolución | Resultado | Observaciones |
|---|---|---|---|
| Mobile Portrait | 375×667 | ⚠️ | Form adapta bien. **Bug**: Badge "TESTING" tapa botón Google |
| Mobile Landscape | 667×375 | ⚠️ | Requiere scroll vertical. **Bug**: Badge "TESTING" tapa Email input |
| Tablet Portrait | 768×1024 | ✅ | Excelente layout centrado, spacing correcto |
| Tablet Landscape | 1024×768 | ✅ | Layout limpio, footer con logos visible |
| Small Desktop | 1280×720 | ✅ | Diseño centrado con padding correcto |
| Mobile - Registro | 375×667 | ✅ | Inputs adaptan bien, scroll necesario para botón Register |
| Mobile - Error SSO | 375×667 | ❌ | Pantalla de error vacía/blanca, sin mensaje ni botón visible |

### Evidencia responsiva

- Mobile Portrait: `screenshots/responsive-mobile-375.png`
- Mobile Landscape: `screenshots/responsive-landscape-667.png`
- Tablet Portrait: `screenshots/responsive-tablet-768.png`
- Mobile Register: `screenshots/responsive-mobile-register.png`
- Mobile Error: `screenshots/responsive-mobile-error.png`

---

## Resultados por AC

### ✅ PASS

| TC | AC | Descripción |
|---|---|---|
| TC-01 | AC-2 | Template nuevo de Keycloak visible — Template personalizado IOND con logo, diseño moderno |
| TC-02 | AC-4 | Checkbox "Stay signed in" — Dice exactamente "Stay signed in" |
| TC-03 | AC-8 | Botones Google y Apple debajo de separador — "Sign in with Apple" (negro) + "Sign in with Google" (outline) debajo de "Or sign in with" |
| TC-08 | AC-14 | Registro sin params: vacío, sin error — Campos vacíos, sin errores JS en consola |
| TC-09 | AC-15 | XSS sanitizado — `<script>alert('xss')</script>` no se ejecutó, payload descartado |
| TC-10 | AC-16 | Prefill solo en Registro, no en Login — Login con `?email=` en URL no prellena el campo |

### ❌ FAIL

| TC | AC | Descripción | Bug |
|---|---|---|---|
| TC-04 | AC-3 | Login con email/contraseña → acceso al producto | Bug 1 — SSO 401 |
| TC-07 | AC-13 | Registro con `?email=` prellena y readonly | Bug 2 — Prefill no funciona |

### ⏸️ BLOCKED

| AC | Descripción | Razón |
|---|---|---|
| AC-5 | "Stay signed in" persiste sesión | Bloqueado por Bug 1 (SSO 401) |
| AC-6 | Logout cierra sesión | Bloqueado por Bug 1 |
| AC-7 | Checkbox no autocompleta | Bloqueado por Bug 1 |
| AC-12 | Login con contraseña/OIDC existente siguen funcionando | Bloqueado por Bug 1 |

### ✅ Confirmado fuera de testing automatizado

| AC | Descripción | Status |
|---|---|---|
| AC-1 | Ambiente apunta a sso.omniorders.com / AuthFlow | ✅ Confirmado por URL de redirect |

### 🧑‍💻 Pendiente manual

| AC | Descripción |
|---|---|
| AC-9 | Login con Google |
| AC-10 | Login con Apple |
| AC-11 | Account linking |

---

## Resumen Ejecutivo

```
Total ACs verificables:  16  (excluyendo AC-17 administrativo)
✅ PASS:                  7   (AC-1, AC-2, AC-4, AC-8, AC-14, AC-15, AC-16)
❌ FAIL:                  2   (AC-3, AC-13)
⏸️ BLOCKED:               4   (AC-5, AC-6, AC-7, AC-12)
🧑‍💻 Manual pendiente:      3   (AC-9, AC-10, AC-11)

Bugs encontrados:         4
  🔴 Blocker:             1   (SSO callback 401)
  🟡 Medium:              2   (Prefill registro, Error SSO vacío en mobile)
  🟢 Low-Medium:          1   (Badge TESTING sobrepuesto en mobile)

Discrepancias vs AC:      3   (Requieren aclaración del Developer)
```

> **Sugerencia de veredicto: REJECTED** — El Bug 1 (SSO 401) es un blocker que impide completar el login. Sin login funcional, el 25% de los ACs no se puede verificar y el producto no cumple su propósito fundamental.
> 
> ⚠️ **El veredicto final lo decide el QA Engineer.**
