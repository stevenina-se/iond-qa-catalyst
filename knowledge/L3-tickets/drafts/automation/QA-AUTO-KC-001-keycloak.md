## Contexto

### Descripción
Automatización de los flujos de autenticación de Keycloak: login SSO, registro SSO y recuperación de contraseña. Estos flujos son pre-requisito para todas las demás pruebas del sistema.

### Módulo afectado
- Módulo principal: `Keycloak / SSO`
- Módulos relacionados: `Admin`, `Tenant`, `Gateway`

---

## Test Cases

### TC-KC-001 — Forgot Password

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-KC-001-01 | Happy Path | Solicitar recuperación con email válido registrado | 🔴 | ⬜ |
| TC-KC-001-02 | Happy Path | Recibir email de recuperación y restablecer contraseña | 🔴 | ⬜ |
| TC-KC-001-03 | Negativo | Solicitar recuperación con email no registrado | 🟠 | ⬜ |
| TC-KC-001-04 | Negativo | Intentar usar link de recuperación expirado | 🟠 | ⬜ |
| TC-KC-001-05 | Edge Case | Solicitar recuperación múltiples veces — solo el último link es válido | 🟡 | ⬜ |

---

### TC-KC-002 — Login with SSO

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-KC-002-01 | Happy Path | Login exitoso con credenciales válidas vía SSO | 🔴 | ⬜ |
| TC-KC-002-02 | Negativo | Login fallido con credenciales inválidas | 🔴 | ⬜ |
| TC-KC-002-03 | Negativo | Login fallido con usuario deshabilitado | 🟠 | ⬜ |
| TC-KC-002-04 | Edge Case | Login con sesión previa activa — redirigir al dashboard | 🟠 | ⬜ |
| TC-KC-002-05 | Edge Case | Login con sesión expirada — solicitar re-autenticación | 🟠 | ⬜ |
| TC-KC-002-06 | Negativo | Login con campos vacíos — validación de formulario | 🟡 | ⬜ |

---

### TC-KC-003 — Register with SSO

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-KC-003-01 | Happy Path | Registro exitoso con datos válidos vía SSO | 🔴 | ⬜ |
| TC-KC-003-02 | Negativo | Registro con email ya existente | 🟠 | ⬜ |
| TC-KC-003-03 | Negativo | Registro con datos incompletos | 🟠 | ⬜ |
| TC-KC-003-04 | Edge Case | Registro y login inmediato — flujo completo | 🟡 | ⬜ |

---

## Notas de Automatización
- Requiere configuración de Keycloak en ambiente de test
- Los tests de email (forgot password) pueden requerir un servicio de email mock (ej. Mailhog)
- Considerar timeout de tokens de SSO para edge cases
