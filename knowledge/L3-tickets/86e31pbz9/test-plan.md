# Test Plan — 86e31pbz9 (Acceso directo a compañías sin inicio de sesión como usuario)

## Información del Ticket

| Campo | Valor |
|-------|-------|
| **ID** | 86e31pbz9 |
| **Título** | Acceso directo a compañías sin inicio de sesión como usuario |
| **Módulo principal** | Auth (Admin > Companies > [Company]) |
| **Tipo** | Refactor / Improvement |
| **Prioridad** | High |
| **Asignado a** | Gustavo Mamani |
| **QA Engineer** | Steve Nina |
| **Fecha del plan** | 2026-09-03 |
| **URL** | [ClickUp](https://app.clickup.com/t/86e31pbz9) |
| **PRs** | [gateway-ion #62](https://github.com/altacrest/ion_gateway_ion/pull/62), [gateway #60](https://github.com/altacrest/ion_gateway/pull/60), [flow_binaries #46](https://github.com/altacrest/ion_flow_binaries/pull/46) |

---

## Resumen

- **Total de casos**: 29
- **Tiempo estimado**: ~130 min (~2.2 horas)
- **Artefactos usados**:
  - ✅ `test-matrix.md` — 29 casos (8 happy, 6 edge, 4 negativos, 6 regresión, 5 code review)
  - ✅ `test-matrix.csv` — Versión CSV para registro
  - ✅ `code-review-qa.md` — 5 hallazgos (0 BUG, 3 RISK, 1 SEC, 1 EDGE)
  - ❌ `ac-consolidated.md` — No generado (modo mínimo)
  - ❌ `risk-triage.md` — No generado (modo mínimo)
- **Prerequisito crítico**: Estar conectado a la **VPN corporativa**

---

## Orden de Ejecución

### BLOQUE 1 — SMOKE TESTS (ejecutar primero, si alguno falla → escalar)

> Si cualquier smoke test falla, PARAR y escalar al Developer antes de continuar.

```
□ REG-001: Login de Admin funciona correctamente — 🔴
□ REG-002: Login de Company funciona correctamente — 🔴
□ TC-006: Pestaña "Support" visible en detalle de compañía — 🟠
□ REG-003: Lista de compañías en panel admin — 🟠
```

### BLOQUE 2 — CORE FLOW (flujo principal de sesión de soporte)

> El flujo completo de sesión de soporte es el corazón del ticket.

```
□ TC-001: Iniciar sesión de soporte desde panel Admin — 🔴
□ TC-002: Banner de sesión de soporte visible con info correcta — 🔴
□ TC-003: Operaciones de tenant completas durante sesión de soporte — 🔴
□ TC-005: Restricción de rutas admin durante sesión de soporte — 🔴
□ TC-004: Salir de sesión de soporte via banner — 🔴
□ TC-007: Salir de sesión de soporte via menú de usuario — 🟠
```

### BLOQUE 3 — EDGE CASES (bordes y escenarios atípicos)

> Estos casos verifican robustez.

```
□ TC-009: Multi-pestaña — sesión de soporte sincroniza entre pestañas — 🟠
□ TC-010: Switch de compañía en sesión de soporte — 🟠
□ TC-012: Persistencia de sesión — recargar página — 🟠
□ TC-014: Navegar a URL de tenant sin sesión de soporte — 🟠
□ TC-013: Cerrar y reabrir browser — sesión de soporte — 🟡
□ TC-011: Broadcasting — canales de compañía — 🟡
```

### BLOQUE 4 — NEGATIVOS (verificar que NO se pueda romper)

> Estos casos verifican seguridad y restricciones.

```
□ TC-015: Sin VPN — requests de tenant devuelven 403 — 🔴
□ TC-016: Usuario no-admin intenta acceder a sesión de soporte — 🟠
□ TC-018: Verificar eliminación completa de impersonation — 🟠
□ TC-017: Admin sin VPN intenta requests via API — 🟠
```

### BLOQUE 5 — REGRESIÓN RESTANTE

```
□ REG-004: Pestañas de configuración de compañía (Information, App Connectors, Boards, Subscription) — 🟠
□ REG-005: API de tenants funciona para Company users — 🔴
□ REG-006: Permisos de usuario Company respetados — 🟠
```

### BLOQUE 6 — VERIFICACIÓN DE CONFIG (no hay BD queries)

```
□ TC-008: Verificar config VPN — variable de entorno correcta — 🟠
```

### BLOQUE 7 — CODE REVIEW TCs (hallazgos del code review)

```
□ TC-CR-001: Error handler muestra error.message crudo en CompanySupportSession — 🟠
□ TC-CR-002: Aislamiento multi-tenant: user Company A no accede a Company B — 🟠
□ TC-CR-003: Auditoría de acciones de admin en sesión de soporte — 🟠
□ TC-CR-004: Timing de sync entre pestañas — 🟡
□ TC-CR-005: Key de localStorage consistente entre módulos — 🟡
```

---

## Datos Necesarios

| Dato | Cómo obtenerlo | Notas |
|------|---------------|-------|
| **Usuario Admin** | `.env` del repo — `IONFLOW_ADMIN_USERNAME` | Rol: administrator |
| **Usuario Company** | `.env` del repo — `IONFLOW_COMPANY_USERNAME` | Rol: tenant |
| **URL de staging** | `.env` del repo — `IONFLOW_ENVIRONMENT_URL` | dev-app.ionflow.io |
| **VPN corporativa** | Conexión activa | **Obligatorio** para tests de sesión de soporte |
| **Compañía con datos** | Verificar en panel admin que existe compañía con workflows, conexiones | Para TC-003 |
| **Usuario con permisos limitados** | Verificar en compañía que existe usuario sin todos los permisos | Para REG-006 |

---

## Criterios de Aprobación/Rechazo

### ✅ CRITERIOS DE APROBACIÓN

```
✅ TODOS los smoke tests pasan (REG-001, REG-002, TC-006, REG-003)
✅ TODOS los happy path críticos pasan (TC-001 a TC-005)
✅ Al menos 4 de 6 edge cases pasan
✅ TODOS los negativos de seguridad pasan (TC-015, TC-016, TC-017)
✅ TC-018 pasa — impersonation completamente eliminado
✅ TODOS los casos de regresión pasan — funcionalidad existente no rota
```

### ❌ CRITERIOS DE RECHAZO

```
❌ Smoke test falla → rechazo inmediato
   Login roto o lista de compañías no carga = bloqueo total.

❌ TC-001 falla (sesión de soporte no inicia) → rechazo
   Este es el flujo principal del ticket.

❌ TC-015 falla (sin VPN accede a datos de tenant) → rechazo
   Falla de SEGURIDAD. Admin sin VPN no debe poder acceder a datos de compañías.

❌ TC-005 falla (admin accede a rutas admin en sesión de soporte) → rechazo
   Violación del role guard. En sesión de soporte no debe poder acceder a /admin.

❌ REG-005 falla (API de tenants rota para Company users) → rechazo
   Los cambios en middlewares no deben afectar a usuarios regulares.

❌ TC-018 falla (endpoints de impersonation aún accesibles) → rechazo
   Riesgo de seguridad si quedan endpoints funcionales del sistema anterior.
```

### ⚠️ CRITERIOS DE APROBACIÓN CON OBSERVACIONES

```
⚠️ TC-011 (broadcasting) no reproducible fácilmente → aprobar con observación
⚠️ TC-013 (cerrar/reabrir browser) comportamiento variable → documentar comportamiento
⚠️ TC-008 (config) no verificable desde QA → aprobar con confirmación del Developer
```

---

## Estimación de Tiempo

| Bloque | Casos | Tiempo estimado |
|--------|-------|-----------------|
| Smoke tests | 4 | ~15 min |
| Core flow (sesión de soporte) | 6 | ~30 min |
| Edge cases | 6 | ~25 min |
| Negativos | 4 | ~20 min |
| Regresión restante | 3 | ~15 min |
| Config | 1 | ~5 min |
| **Total** | **24** | **~110 min (~2 horas)** |

---

## Riesgos para la Sesión de Testing

| Riesgo | Mitigación |
|--------|------------|
| VPN no disponible/inestable | Verificar conexión VPN ANTES de iniciar. Todos los tests de sesión de soporte requieren VPN |
| No se puede simular "sin VPN" | TC-015 y TC-017 requieren desconectar VPN — verificar que se pueda reconectar rápidamente |
| Multi-pestaña puede no funcionar en todos los browsers | TC-009 puede depender del storage events del browser |
| Pestaña "Users" eliminada — impacto desconocido | REG-004 verificará que las demás pestañas siguen funcionando |
| Tokens huérfanos en oauth_access_tokens | No requiere acción de QA — el sistema simplemente deja de leerlos |

---

## Estado

⏳ **Plan creado — listo para ejecución (Deployment)**
