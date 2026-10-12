# Template de Rechazo — 86e3dhzre

Estimado @Juan José Potes Riveros

**El resultado de pruebas para este ticket es: RECHAZADO ❌**

**Ticket**: 86e3dhzre — [Deploy] Nuevo template de login Keycloak (IOND)
**Módulo**: Keycloak / Auth
**QA Engineer**: Steve Nina
**Fecha**: 2026-10-01

### Resumen de Testing
- Casos ejecutados: 10
- Casos aprobados: 7
- Casos fallidos: 2
- Bloqueados: 4
- Bugs encontrados en Code Review: 0
- Bugs encontrados en Testing: 4
- Bugs totales (bloqueantes): 1

### Code Review QA
> No aplica para este ticket — no hay código de aplicación IOND involucrado. El cambio es de configuración de variables de entorno apuntando al nuevo realm de Keycloak (`AuthFlow`).

---

### 📌 Observaciones

**🔴 OBS-01 - Urgent - Estado: Nuevo**
**Área / Flujo: Auth — SSO Callback (Keycloak → IOND)**

**Descripción:**
Keycloak autentica correctamente al usuario con el nuevo template, pero cuando redirige de vuelta a IOND, el callback SSO falla con HTTP 401 Unauthorized. El usuario queda atrapado en la pantalla "Signing you in..." y nunca accede al producto. El error expone detalles técnicos al usuario: `"SSO Error — AxiosError: Request failed with status code 401"`.

**Pasos de reproducción:**
1. Navegar a `https://dev-app.ionflow.io`
2. Keycloak redirige a `sso.omniorders.com/realms/AuthFlow/...`
3. Ingresar email → Continue → password → Sign In
4. Keycloak autentica OK → redirige a IOND con code+state en URL
5. IOND muestra "Signing you in..."
6. ❌ Toast: `"SSO Error — AxiosError: Request failed with status code 401"`
7. Pantalla cambia a: "We couldn't complete the SSO authentication." + botón "Retry now"

**Resultado esperado:**
El SSO callback debería completar la autenticación y redirigir al dashboard de IOND.

**Comportamiento actual:**
Error 401 en el callback. El usuario nunca accede al producto. El botón "Retry now" vuelve a fallar con el mismo error.

**Análisis técnico — ¿Qué necesita verificar/cambiar IOND?**
| # | Causa probable | Qué verificar |
|---|---|---|
| 1 | `KEYCLOAK_REALM_PUBLIC_KEY` no actualizada para realm `AuthFlow` | Pedir nueva PUBLIC_KEY a admin de Keycloak |
| 2 | Issuer mismatch — el token del nuevo realm tiene un `iss` diferente | Verificar que IOND acepta el issuer de `AuthFlow` |
| 3 | `CLIENT_SECRET` incorrecto para `AuthFlow` | Verificar que el secret es válido en el nuevo realm |
| 4 | Audience validation — nuevo realm emite `aud` diferente | Verificar audience esperado por IOND |
| 5 | `redirect_uri` no registrada en `AuthFlow` | Verificar que `https://dev-app.ionflow.io/*` está registrada como redirect válida |

**Evidencia:**
- Screenshot: `screenshots/tc04-sso-error-401.png`

**ACs bloqueados por este bug:** AC-3, AC-5, AC-6, AC-7, AC-12

---

**🟡 OBS-02 - High - Estado: Nuevo**
**Área / Flujo: Keycloak Template — Registration Form (Prefill)**

**Descripción:**
La URL de registro con parámetros `?email=`, `firstName=` y `lastName=` no prellena los campos del formulario. Todos aparecen vacíos cuando deberían estar prellenados y en solo lectura.

**Pasos de reproducción:**
1. Navegar a la URL de registro de Keycloak
2. Agregar parámetros: `?email=test@test.com&firstName=John&lastName=Doe`
3. Observar que todos los campos aparecen vacíos

**Resultado esperado:**
Los campos Email, First name y Last name deberían estar prellenados con los valores de la URL y en modo read-only.

**Comportamiento actual:**
Todos los campos aparecen vacíos, sin prefill.

**Evidencia:**
- Screenshot: `screenshots/tc07-registration-prefill-fail.png`

---

**🔵 OBS-03 - Normal - Estado: Nuevo**
**Área / Flujo: IOND App — Pantalla de error SSO en mobile**

**Descripción:**
En viewport mobile (375×667), la pantalla de error SSO se muestra completamente en blanco. El mensaje "We couldn't complete the SSO authentication", el toast de error y el botón "Retry now" no son visibles. El usuario en mobile no tiene feedback de que algo falló ni forma de reintentar.

**Pasos de reproducción:**
1. Acceder a `https://dev-app.ionflow.io` desde un dispositivo mobile (375×667)
2. Completar login en Keycloak
3. Esperar el callback SSO (que falla con 401)
4. La pantalla de error se muestra vacía/blanca

**Resultado esperado:**
El mensaje de error, toast y botón "Retry now" deberían ser visibles y usables en mobile.

**Comportamiento actual:**
Pantalla completamente en blanco — sin feedback para el usuario.

**Evidencia:**
- Screenshot: `screenshots/responsive-mobile-error.png`

---

**⚪ OBS-04 - Low - Estado: Nuevo**
**Área / Flujo: Keycloak Template — Badge "TESTING" en mobile**

**Descripción:**
En resoluciones mobile, el badge flotante amarillo "TESTING" (indicador de ambiente) se sobrepone a elementos funcionales: en portrait (375×667) tapa el botón "Sign in with Google", en landscape (667×375) tapa el campo Email. Si el badge es solo de staging y no aparece en producción, la prioridad es baja.

**Pasos de reproducción:**
1. Acceder a `https://dev-app.ionflow.io` desde un dispositivo mobile
2. Observar que el badge "TESTING" se superpone a elementos interactivos

**Resultado esperado:**
El badge no debería tapar elementos funcionales de la interfaz.

**Comportamiento actual:**
Badge se superpone a botón Google (portrait) y campo Email (landscape), impidiendo la lectura/interacción.

**Evidencia:**
- Screenshot portrait: `screenshots/responsive-mobile-375.png`
- Screenshot landscape: `screenshots/responsive-landscape-667.png`

---

### ⚠️ Discrepancias AC vs Implementación — Requieren aclaración

Se encontraron 3 discrepancias entre lo descrito en el ticket y lo observado. Requieren aclaración del Developer:

1. **Flujo 2 pasos vs "Una sola pantalla"** — El ticket dice "Una sola pantalla de login con contraseña". La implementación es en 2 pasos: Email + Continue → Password + Sign In. ¿Intencional?

2. **Separador "Or sign in with" vs "Or"** — El ticket dice los botones IdP debajo de "Or". El template muestra "Or sign in with". ¿Intencional?

3. **Selector de idioma visible** — El ticket dice explícitamente "Selector de idioma (segunda etapa; fuera de alcance)". Sin embargo, hay un dropdown "English v" visible en la esquina superior derecha. ¿Viene incluido en el template base de Keycloak o se añadió intencionalmente?

---

### 🔍 Coherencia de mensajes de error

- ❌ El toast expone `"AxiosError: Request failed with status code 401"` al usuario final — esto es información técnica interna que no debería mostrarse
- ⚠️ El botón "Retry now" da falsa esperanza cuando el problema es de configuración (el retry siempre falla)
- ⚠️ Falta un link de contacto/soporte en la pantalla de error

**Recomendación:** Reemplazar el toast por un mensaje amigable como *"We had trouble verifying your credentials. Please try again or contact support."*

---

### Evidencia General
- QA Report: `L3-tickets/86e3dhzre/qa-report.md`
- Screenshots de fallos: `L3-tickets/86e3dhzre/screenshots/`

| Details | |
|---|---|
| BROWSER | Chrome (Playwright MCP) |
| BRANCH | N/A — cambio de configuración Keycloak |
| ENV | dev-app.ionflow.io |
| TEST MATRIX | N/A |
| CODE REVIEW | N/A (no hay código de aplicación) |
| MERGE REQUEST | N/A |
