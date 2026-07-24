# Test Plan — 86e1r2c6z
# Refactorizar flujo y formulario de registro de compañía

> Generado: 2026-06-23 | Skill: sprint-testing/plan
> Track: Discovery → (pendiente Deployment cuando el ticket entre en sprint)
> QA Engineer: Steve Nina | Developer: Gustavo Mamani
> Estimación total: ~2h 30min

---

## 1. Objetivo del Testing

Verificar que el formulario `/create-company` refactorizado de Ionflow:
- Registra compañías correctamente con todos los campos nuevos
- El autocompletado (Country por timezone, State/City por Postal Code) funciona y degrada gracefully
- La timezone se persiste en la entidad correcta *(pendiente AC-6)*
- No introduce regresión en el flujo de login ni en otros módulos
- La experiencia visual y responsive cumple el nivel de calidad definido en el prototipo

---

## 2. Scope del Testing

### In scope
- Formulario `/create-company` completo (todos los campos)
- Flujo de registro end-to-end (Keycloak → create-company → dashboard)
- Campos read-only de Keycloak (email, first name, last name)
- Selector de timezone + autodetección de Country
- Autocompletado State/City por Postal Code (servicio externo)
- Comportamiento degradado del servicio externo (caído / cuota agotada)
- Validaciones de campos obligatorios
- Manejo de errores del servidor
- "Back to login"
- Responsive (desktop, tablet 768px, mobile 375px)
- Regresión: login existente, company selection, flows, usuarios, settings

### Out of scope
- El contenido del carousel del panel izquierdo (decisión de diseño pendiente)
- Tests de performance de la API de autocompletado
- Accesibilidad avanzada (WCAG)
- Tests de seguridad

---

## 3. Prerequisitos de Testing (para cuando pase a Deployment)

### Confirmaciones pendientes del Developer ANTES de iniciar testing
> ⚠️ Las siguientes deben responderse antes de ejecutar el Bloque 2 y el Bloque BD

| Pregunta | Criticidad | Impacto si no se responde |
|----------|-----------|--------------------------|
| Q-001: ¿En qué entidad persiste timezone — companies / user / ambas? | 🔴 Crítica | TC-016 y TC-036 bloqueados |
| Q-002: ¿Qué servicio externo de autocompletado se usa? | 🟠 Alta | Verificar disponibilidad en staging |
| Q-003: Si el servicio externo está caído → ¿modo degradado definido? | 🟠 Alta | TC-014 no tiene resultado esperado claro |
| Q-007: ¿Cuáles son todos los campos obligatorios para submit? | 🟠 Alta | TCs de validación pueden quedar incompletos |
| Q-009: ¿El servicio externo está configurado y funcional en staging? | 🟠 Alta | Bloque de autocompletado no testeable |

### Setup de entorno
1. ✅ Branch `86e1r2c6z` (o similar) mergeada a staging
2. ✅ Migración BD ejecutada (si se agregaron columnas nuevas en `companies`)
3. ✅ Acceso a usuario sin company asignada para testear el registro completo
4. ✅ Acceso a DBeaver (PostgreSQL via SSH) para verificaciones de BD
5. ✅ API key del servicio de autocompletado configurada en staging
6. ✅ Respuestas a Q-001, Q-002, Q-007, Q-009

---

## 4. Bloques de Ejecución

### Bloque 0 — Pre-flight (10 min)
**Objetivo**: Confirmar entorno antes de iniciar

- [ ] Confirmar respuestas a preguntas críticas del Developer (Q-001, Q-007, Q-009)
- [ ] Navegar a `/create-company` — verificar que el formulario carga
- [ ] Verificar que el usuario de testing no tiene company asignada
- [ ] Verificar acceso a DBeaver con SSH tunnel activo
- [ ] Verificar que el servicio de autocompletado está disponible en staging

### Bloque 1 — Smoke Tests / Regresión Login (15 min)
**Objetivo**: Confirmar que el login y la navegación base siguen funcionando

- [ ] TC-029 — Login existente no afectado
- [ ] TC-034 — Vista de usuarios funcional
- [ ] TC-035 — Vista de settings funcional

> 🔴 Si TC-029 falla → PARAR y reportar regresión crítica. No continuar.

### Bloque 2 — Happy Path Core (30 min)
**Objetivo**: El formulario puede registrar una company de principio a fin

- [ ] TC-001 — Registro completo con datos válidos → company creada
- [ ] TC-002 — Campos read-only de Keycloak se muestran correctamente
- [ ] TC-003 — Timezone autodetecta Country (America/La_Paz → Bolivia)
- [ ] TC-005 — "Back to login" funciona
- [ ] TC-017 — Contact Name prellenado desde Keycloak
- [ ] TC-018 — Timezone América/Chicago → Country USA

> 🔴 Si TC-001 falla → PARAR y reportar bug crítico.

### Bloque 3 — Autocompletado y Servicio Externo (20 min)
**Objetivo**: Verificar el autocompletado y su comportamiento ante fallos

- [ ] TC-004 — Autocompletado State/City por Postal Code USA (10001)
- [ ] TC-013 — Postal Code inválido → sin datos incorrectos
- [ ] TC-014 — Servicio externo caído → modo degradado
- [ ] TC-022 — Cambio de timezone → Country se actualiza
- [ ] TC-026 — Cuota agotada → formulario no bloquea

### Bloque 4 — Validaciones y Negativos (20 min)
**Objetivo**: El formulario valida correctamente los datos

- [ ] TC-009 — Submit vacío → validación inline en todos los campos
- [ ] TC-010 — Submit sin Company Name → error específico en ese campo
- [ ] TC-011 — Submit sin Timezone → error específico
- [ ] TC-015 — Timezone UTC → Country no autodetectado incorrectamente
- [ ] TC-012 — Error de servidor → datos conservados

### Bloque 5 — Edge Cases Adicionales (20 min)
**Objetivo**: Verificar comportamientos de borde identificados en Discovery

- [ ] TC-021 — Caracteres especiales (ñ, á, é) en nombre Keycloak
- [ ] TC-024 — Tablet 768px — layout coherente
- [ ] TC-025 — Back to login con datos parciales → sin company huérfana en BD
- [ ] TC-028 — Submit mientras autocompletado en proceso

### Bloque 6 — Responsive Visual (15 min)
**Objetivo**: Verificar la experiencia visual y responsive

- [ ] TC-006 — Desktop — 2 paneles, campos alineados
- [ ] TC-007 — Mobile 375px — columna única, botones apilados
- [ ] TC-008 — Diseño visual dark, 3 secciones, sin degradado azul

### Bloque 7 — Regresión BD y Flows (20 min)
**Objetivo**: Verificar persistencia correcta y sin regresión en el sistema

- [ ] TC-030 — Company creada aparece en company selection
- [ ] TC-031 — Datos de company correctos en BD (verificar con DBeaver)
- [ ] TC-032 — Flujo completo nuevo usuario (Keycloak → create-company → dashboard)
- [ ] TC-033 — Flow existente ejecuta sin regresión
- [ ] TC-016 *(si AC-6 confirmado)* — Timezone persiste en entidad correcta
- [ ] TC-036 *(si AC-6 confirmado)* — Timezone correcta en BD

---

## 5. Criterios de Aceptación del Testing

### Condiciones para ✅ Approved
- TC-001 pasa (registro end-to-end funciona)
- TC-029 pasa (sin regresión en login)
- TC-002 pasa (campos read-only de Keycloak correctos)
- TC-003 pasa (timezone autodetecta country)
- TC-009 y TC-010 pasan (validaciones funcionales)
- TC-005 pasa (Back to login funcional)
- TC-031 pasa (datos en BD correctos)

### Condiciones para ❌ Rejected
- TC-001 falla (registro no funciona)
- TC-029 falla (regresión crítica en login)
- TC-002 falla (campos Keycloak editables cuando no deberían)
- TC-009 falla (formulario se envía sin campos requeridos)
- TC-014 falla (servicio externo caído bloquea completamente el formulario)
- TC-016 falla *(si AC-6 confirmado)* — timezone no se guarda

### Condiciones para ⚠️ Approved con observaciones
- TC-004 falla (autocompletado no funciona, pero degraded mode sí)
- TC-024 falla (tablet con issues visuales, pero desktop y mobile OK)
- TC-008 falla (issues estéticos menores, funcionalidad core OK)
- TC-015 falla (UTC autocompleta con algún país, pero funcionalidad core OK)

---

## 6. Estimación de Tiempo

| Bloque | Duración estimada |
|--------|------------------|
| Bloque 0 — Pre-flight | 10 min |
| Bloque 1 — Smoke Tests / Regresión Login | 15 min |
| Bloque 2 — Happy Path Core | 30 min |
| Bloque 3 — Autocompletado y Servicio Externo | 20 min |
| Bloque 4 — Validaciones y Negativos | 20 min |
| Bloque 5 — Edge Cases | 20 min |
| Bloque 6 — Responsive Visual | 15 min |
| Bloque 7 — Regresión BD y Flows | 20 min |
| **Total estimado** | **~2h 30min** |

---

## 7. Riesgos y Mitigaciones

| Riesgo | Mitigación |
|--------|-----------|
| AC-6 sin definir (entidad de timezone) | Bloquear TC-016 y TC-036. Aclarar con Developer antes de Deployment |
| Servicio externo no disponible en staging | Confirmar Q-009 en pre-flight. Ejecutar TC-014 (modo degradado) independientemente |
| No tener usuario sin company para el registro end-to-end | Preparar usuario específico de testing en Keycloak antes de iniciar |
| Migración BD no ejecutada | Verificar en pre-flight con DBeaver. Si falla → PARAR |
| Quota del servicio externo agotada durante testing | Usar caché activa y limitar repeticiones del mismo Postal Code |

---

## 8. Preguntas Abiertas para el Developer

> ⚠️ Estas preguntas deben responderse ANTES del testing en Deployment.
> Documentar las respuestas en `ticket-memory.md`.

| ID | Pregunta | Criticidad |
|----|----------|-----------|
| Q-001 | ¿En qué entidad persiste timezone? (companies / user admin / ambas) | 🔴 Crítica |
| Q-002 | ¿Qué servicio externo de autocompletado se usa? (URL truncada en el comentario) | 🟠 Alta |
| Q-003 | Si el servicio externo está caído → ¿modo degradado definido? | 🟠 Alta |
| Q-004 | ¿El Postal Code es obligatorio para el submit? | 🟠 Alta |
| Q-005 | Si la timezone no mapea a un único país (UTC) → ¿qué ocurre con Country? | 🟠 Alta |
| Q-006 | ¿El selector de State tiene opciones fijas o dinámicas según Country? | 🟡 Media |
| Q-007 | ¿Cuáles son TODOS los campos obligatorios para el submit? | 🟠 Alta |
| Q-008 | Contact Name → ¿editable o read-only? ¿Desde dónde se prellena? | 🟡 Media |
| Q-009 | ¿El servicio externo está configurado y funcional en staging? | 🟠 Alta |

---

## 9. Artefactos de Salida (para Deployment)

Al finalizar el testing, deben existir en `L3-tickets/86e1r2c6z/`:
- [ ] `test-matrix.md` actualizada con resultados (✅/❌/⏭️)
- [ ] `test-matrix.csv` actualizada
- [ ] `qa-report.md` con veredicto final y evidencia
- [ ] `screenshots/` con evidencia de formulario, BD, y casos clave (si aplica)
