Estimado @Gustavo

**El resultado de pruebas para este ticket es: APROBADO ✅**

**Ticket**: 86e22fzq7 — Connections — Reautorización por API Key crea conexión duplicada en lugar de sobrescribir
**Módulo**: Connections / Integrations
**QA Engineer**: Steve Nina
**Fecha**: 2026-07-14

### 📊 Resumen de Testing
- **Casos ejecutados**: 17 (12 funcionales + 3 regresión / 2 inyectados de Code Review)
- **Casos aprobados**: 17
- **Tasa de aprobación**: 100%
- **Bugs encontrados**: 0

---

### 🛠️ ¿Qué se construyó / cambió?
- **Backend — `flow_binaries` (PR #14)**: En `resolveCompanyAppAndConnection()`, cuando `attempt.ConnectionId` está presente para una global app, se carga el `ConnectionTenant` existente via `FindConnectionByCompany()` y se inyecta en el auth context. Esto permite que `upsertCompanyConnection()` detecte la conexión existente y actualice sus credenciales in-place (`.Connection` y `.Data` encriptados) en lugar de crear un registro nuevo. Error handling mejorado en `UpdateConnectionByCompany()`.
- **Frontend — `gateway-ion` (PR #12)**: Se introdujo `isReauthorize` computed property (`connectionId != null`) en `CreateConnectionV2Dialog.vue`. Se refactorizó el método monolítico `testAttempt()` en tres helpers: `handleAuthorizingStatus()`, `handleSuccessStatus()`, y `showSuccessToast()`. Los toasts de éxito se suprimen condicionalmente con `if (!isReauthorize.value)` en ambos handlers de status.

### 💡 ¿Por qué es importante?
- Este bug generaba **conexiones duplicadas** cada vez que un usuario reautorizaba una conexión API Key. Los flows que referenciaban la conexión original seguían usando credenciales viejas, ya que las nuevas se guardaban en un registro diferente. Además, se mostraban 2 toasts de éxito confusos. El fix asegura que la reautorización actualiza las credenciales de la conexión existente sin crear duplicados, manteniendo la integridad referencial de los flows y eliminando la confusión visual de toasts redundantes.

---

### 🎯 Criterios de Aceptación (AC) Clave Validados

#### **AC-1. Reauthorize actualiza la conexión existente, no crea duplicado**
* **Validación realizada**: Se contaron las conexiones antes y después del reauthorize (TC-003). Se verificó via UI que no hay registros duplicados (TC-015). Se probó aislamiento multi-tenant (TC-011).
* **Comportamiento observado**: La cantidad de conexiones permanece igual. Las credenciales se actualizan in-place. Sin duplicados en la lista ni en BD.

#### **AC-2. Toasts suprimidos durante reauthorize**
* **Validación realizada**: Se ejecutó reauthorize de API Key (TC-004) y se verificó que no aparecen toasts. Se probó secuencia reauthorize → create new (TC-009) para confirmar que la supresión se resetea.
* **Comportamiento observado**: 0 toasts en reauthorize. Toasts reaparecen correctamente al crear conexión nueva inmediatamente después. `isReauthorize` se resetea correctamente.

#### **AC-3. Toasts intactos en creación nueva**
* **Validación realizada**: Se creó conexión nueva (TC-005, TC-010) sin haber hecho reauthorize.
* **Comportamiento observado**: Toast "Connection validated successfully" aparece normalmente. Sin supresión accidental.

#### **AC-5. Flows usan credenciales actualizadas post-reauthorize**
* **Validación realizada**: Se reautorizó una conexión usada por un flow activo y se ejecutó el flow (TC-012).
* **Comportamiento observado**: El nodo de app del flow ejecuta correctamente con las nuevas credenciales. Sin errores de autenticación.

#### **AC-6. OAuth y API Key reauthorize funcionan**
* **Validación realizada**: Se probaron ambos flujos: OAuth con popup (TC-006) y API Key con success inmediato (TC-003/TC-004). También se verificó creación nueva OAuth (TC-013).
* **Comportamiento observado**: Ambos flujos completan sin errores ni duplicados. El refactor de `testAttempt` no introdujo regresiones.

---

### 🔄 Pruebas de Regresión
- **OAuth flow (create new)**: Creación de nueva conexión OAuth sigue funcionando. Popup abre, token se obtiene, toast aparece (TC-013).
- **Tenant app reauthorize**: Flujo de reauthorize para tenant apps no cambió. Funciona igual que pre-deploy (TC-007).
- **Flow con conexión reautorizada**: Nodos de app ejecutan correctamente con credenciales actualizadas post-reauthorize (TC-012).
- **Lista de connections**: Post-reauthorize la lista está limpia, sin duplicados, todos los status correctos (TC-014).

---

### 🔍 Code Review QA
> Resumen de la revisión de código realizada antes del testing funcional para mitigar riesgos tempranos.

- **Repos revisados**: `gateway-ion` (PR #12 — commits de605756, 3533fe98) + `flow_binaries` (PR #14 — commits 284fe58, 55280d6, 47023c3, 127350b)
- **Hallazgos identificados**: 2 (🔴: 0, 🟠: 1, 🟡: 1)
- **Riesgos inyectados a la Matrix**: 2 TCs creados específicamente a partir del código revisado (TC-CR-001, TC-CR-002).
- **Estado**: Todos los hallazgos fueron verificados y mitigados exitosamente en Testing.

### ⚠️ Observaciones
- Comentario en `attempt_service.go` línea 664 dice "keep the existing name" pero el código actualiza el nombre. Contradicción cosmética menor — no bloqueante.

### 📂 Evidencia
- **Test Matrix**: knowledge/L3-tickets/86e22fzq7/test-matrix.md
- **QA Report / Run**: knowledge/L3-tickets/86e22fzq7/qa-report.md
- **Code Review QA**: knowledge/L3-tickets/86e22fzq7/code-review-qa.md
- **DB Evidence**: Verificación vía UI — sin migraciones de BD. No hay duplicados post-reauthorize.
- **Screenshots / Logs**: Testing manual supervisado por QA Engineer

---

### 📝 Conclusión de QA
El bug de conexiones duplicadas durante reautorización está completamente corregido. El backend ahora carga la conexión existente via `FindConnectionByCompany()` y actualiza sus credenciales in-place, mientras el frontend suprime correctamente los toasts redundantes durante reauthorize sin afectar la creación de conexiones nuevas. El aislamiento multi-tenant está preservado gracias a `CompanySchema()`. Los flows que referencian conexiones reautorizadas usan automáticamente las nuevas credenciales. 17/17 TCs passed, 0 bugs, 0 bloqueantes. El entregable es estable y está listo para producción.

| Details | |
|---|---|
| BROWSER | Chrome |
| BRANCH | IONF-1114 |
| ENV | dev-app.ionflow.io |
| TEST MATRIX | knowledge/L3-tickets/86e22fzq7/test-matrix.md |
| MERGE REQUEST | YES |
