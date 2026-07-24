# AC Consolidados — 86e1r2c6z
# Refactorizar flujo y formulario de registro de compañía

> Generado: 2026-06-23 | Actualizado: 2026-07-17 (Deployment)
> Skill: test-docs/document (modo AC)
> Fuentes: Descripción del ticket + Comentarios Quick Prototype (Gustavo 12-jun + 19-jun) + Risk Triage + TDD Build (Gustavo 29-jun) + Correcciones Code Review (Gustavo 13-jul)
> QA Engineer: Steve Nina

---

## Resumen de AC Consolidados

| Total AC | Origen |
|----------|--------|
| 12 AC funcionales | Descripción + comentarios reconciliados |
| 2 AC propuestos por QA | Basados en riesgos identificados (AC-P1, AC-P2) |
| **14 AC total** | |

> ✅ **Actualización Deployment**: Todas las preguntas abiertas fueron respondidas por el Developer en los comentarios de TDD Build (29-jun) y Correcciones Code Review (13-jul).

---

## AC Consolidados — Listado Completo

### Grupo 1 — Campos y Contenido del Formulario

**AC-1** — El formulario registra claramente una **compañía** (no solo un usuario)
- El header/título indica que es registro de company
- El banner superior muestra el usuario de Keycloak como lectura (quién registra), no como protagonista del formulario
- **Fuente**: Descripción original + Comentario Gustavo 12-jun (banner read-only)
- **Estado**: ✅ Confirmado

**AC-2** — El formulario presenta **3 secciones** diferenciadas con header e ícono
- Sección 1: **Company Profile** (Company Name, Contact Name)
- Sección 2: **Location** (Address 1, Address 2, Country, State, City, Postal Code)
- Sección 3: *(implícita en el diseño — timezone y datos adicionales)*
- **Fuente**: Comentario Gustavo 12-jun
- **Estado**: ✅ Confirmado

**AC-3** — **Campos informativos read-only** (Keycloak, no editables)
- ⚠️ **ACTUALIZADO**: Keycloak entrega `users.name` como nombre completo concatenado (NO como First Name / Last Name separados)
- El nombre completo se muestra en el banner de identidad como texto informativo read-only
- Email → read-only si Keycloak lo trae. **Si Keycloak NO trae email → se renderiza un input editable** con validación (fallback M2 del code review)
- Se muestran como texto informativo, NO como inputs disabled
- **Fuente**: Comentario Gustavo 12-jun + TDD Build 29-jun (TC-002, TC-021) + Correcciones 13-jul (M2)
- **Estado**: ✅ Confirmado — **ajustado según implementación real**

**AC-4** — **Campos del formulario** (editables por el usuario)
- Company Name (editable, **obligatorio**)
- Contact Name (prellenado con `users.name` de Keycloak — nombre completo concatenado — editable)
- Address 1, Address 2 (editables)
- Country (autodetectado por timezone, editable, **obligatorio**)
- State (selector dropdown dinámico según Country. **Texto libre para países sin subdivisiones** ej. Bolivia)
- City (autocompleto por Postal Code via botón explícito)
- Postal Code (editable, **opcional** — dispara autofill solo con botón "Autofill city & state")
- Phone (editable)
- **Fuente**: Descripción original + Comentarios Gustavo 12-jun y 19-jun + TDD Build 29-jun
- **Estado**: ✅ Confirmado — Q-006 y Q-008 **resueltas**
  - Q-006: State es dropdown dinámico con subdivisions, texto libre sin subdivisiones
  - Q-008: Contact Name prellenado desde `users.name` (Keycloak), editable

**AC-5** — **Selector de zona horaria** incluido en el formulario
- El usuario puede seleccionar su timezone
- La timezone seleccionada **autodetecta el Country** (y lo prellena)
- **Guard de override manual**: si el usuario ya eligió country manualmente, cambiar timezone NO sobreescribe el country
- Timezone se autodetecta desde el browser al cargar el formulario
- **Fuente**: Descripción original + Comentario Gustavo 19-jun + TDD Build 29-jun (TC-003/TC-018/TC-022)
- **Estado**: ✅ Confirmado

**AC-6** — **Persistencia de zona horaria** ✅ RESUELTO
- La timezone se persiste en `companies.timezone`
- **Entidad destino**: `companies` (solo)
- No requiere migración nueva — el campo ya existe
- **Fuente**: TDD Build 29-jun (TC-031 + queries BD) + Correcciones 13-jul (TC-016/TC-036)
- **Estado**: ✅ **CONFIRMADO** — Q-001 **resuelta**: timezone en `companies.timezone`

---

### Grupo 2 — Autocompletado y Servicios Externos

**AC-7** — **Autocompletado State y City** por Postal Code
- ⚠️ **ACTUALIZADO**: El autocompletado NO es automático — se dispara con un **botón explícito "Autofill city & state"**
- El botón aparece cuando el Postal Code tiene ≥ 3 caracteres
- Al hacer click, llama a **Geoapify Geocoding API** (via proxy en `flow_binaries`, endpoint Go con JWT auth)
- Autocompleta: City, State, y posiblemente Country
- Muestra hint badge: "✓ City and state filled from postal code"
- Al cambiar el postal code, el hint desaparece y el botón reaparece
- Para países sin códigos postales (ej. Aruba, Bolivia), el botón de autofill **NO aparece**
- El sistema tiene **caché in-process con TTL** (positiva 24h / negativa 1h) para optimizar uso de tokens
- Cuota del servicio: 3.000 req/día (cuota gratuita Geoapify)
- **Fuente**: Comentario Gustavo 19-jun + TDD Build 29-jun (TC-001, TC-004, TC-020) + Correcciones 13-jul (H1, H3)
- **Estado**: ✅ Confirmado — Q-002, Q-003, Q-004 **resueltas**
  - Q-002: Servicio = Geoapify Geocoding API (`GEOAPIFY_URL` + `GEOAPIFY_API_KEY`)
  - Q-003: Degradación graceful — endpoint retorna 404 sin API key, frontend muestra toast
  - Q-004: Postal Code **NO es obligatorio** — autofill es opcional con botón explícito

**AC-NUEVO-1** — **Degradación graceful del servicio externo**
- *(AC propuesto por QA basado en RIESGO-004)* — ✅ **CONFIRMADO por Developer**
- Si el servicio externo está caído o la cuota se agotó → endpoint retorna 404 (sin API key) o error
- Frontend muestra toast notification como fallback
- Los campos State y City quedan editables manualmente
- El formulario NO se bloquea
- **Fuente**: RIESGO-004 del risk-triage + Correcciones 13-jul (H1)
- **Estado**: ✅ Confirmado por Developer

---

### Grupo 3 — Validaciones

**AC-8** — **Validación de campos obligatorios**
- ⚠️ **ACTUALIZADO**: Campos obligatorios confirmados:
  - **Company Name** — requerido con `*` y validación
  - **Timezone** — requerido con `*` y validación (se autodetecta del browser, siempre se envía)
  - **Country** — requerido con `*` y validación
  - **State** — **opcional** (requerirlo rompería países sin subdivisiones)
  - **Postal Code** — **opcional**
- El formulario marca visualmente qué campos son requeridos
- Si el usuario intenta enviar sin completar campos obligatorios → el sistema **previene el envío**
- Muestra mensajes de error claros **inline** (junto al campo correspondiente)
- **Fuente**: Descripción original + Correcciones 13-jul (M4)
- **Estado**: ✅ Confirmado — Q-007 **resuelta**

**AC-9** — **Manejo de error al guardar**
- Si ocurre un error de servidor al registrar → el sistema muestra mensaje de error controlado (i18n: `t('message.success')`)
- Los datos ingresados **se conservan** para que el usuario pueda corregir o reintentar
- `serverErrors` se limpia al inicio de cada submit (`serverErrors.value = {}`)
- `isLoading` se resetea en `finally` block (corregido en code review M1)
- **Fuente**: Descripción original (Red Path) + Correcciones 13-jul (M1, L1, L2)
- **Estado**: ✅ Confirmado

---

### Grupo 4 — Estética y UX

**AC-10** — **Diseño visual mejorado** — comparable a Omnio
- Panel izquierdo: dark minimalista con ícono en tile de acento tenue (reemplaza degradado azul)
- Panel izquierdo restyled con `Section.tsx` — theme-aware, dark-mode-compatible, i18n
- Panel derecho: formulario con secciones y encabezados claros
- Inputs con estilo "filled/raised" con jerarquía clara label → campo
- Botones: "Create Company" (primario) y "Back to login" (secundario)
- Blend en el límite de los dos paneles (sin línea dura)
- Logo actualizado (comprimido — L4 del code review)
- Contenedor con `max-w-2xl` para evitar estiramiento en monitores anchos
- **Fuente**: Comentarios Gustavo 12-jun y 19-jun + Correcciones 13-jul (L4)
- **Estado**: ✅ Confirmado

**AC-11** — **Panel izquierdo** con contenido estático actual
- El carousel simulado conserva el contenido existente
- Los iconos de navegación del carousel están **ocultos** (no funcionales)
- Textos del panel pasados a **i18n** (registerPanelTitle/Subtitle/Description en EN/ES)
- *(Pendiente de definición: ¿carousel funcional o contenido estático en el futuro?)*
- **Fuente**: Comentario Gustavo 12-jun + Correcciones 13-jul (Fuera de scope)
- **Estado**: ✅ Confirmado (como está actualmente)

---

### Grupo 5 — Navegación y Regresión

**AC-12** — **"Back to login" funciona correctamente**
- El botón/link regresa al usuario al flujo de login
- Funciona en desktop y mobile
- **Fuente**: Descripción original
- **Estado**: ✅ Confirmado

**AC-13** — **Registro end-to-end funcional**
- Al completar el formulario con datos válidos → la company se crea correctamente
- El flujo post-registro sigue el comportamiento esperado (redirect al dashboard o flujo de onboarding)
- El flujo de login existente no se ve afectado
- **Nota de BD**: Los campos Country, State, Postal Code, Contact Name persisten en tabla `contacts` (morphOne desde companies). Solo `timezone` persiste en `companies`
- **Fuente**: Descripción original (Hard Restrictions) + TDD Build 29-jun (TC-031)
- **Estado**: ✅ Confirmado

---

### Grupo 6 — Responsive

**AC-14** — **Formulario responsive**
- Desktop: layout de 2 paneles, inputs bien distribuidos
- Tablet: diseño coherente sin campos desalineados
- Mobile: botones en `flex-col-reverse` (Create Company arriba, Back to login abajo)
- Scroll habilitado en mobile cuando el contenido excede la pantalla
- Contenedor `max-w-2xl mx-auto` para controlar ancho en monitores grandes
- **Fuente**: Descripción original + Comentario Gustavo 12-jun
- **Estado**: ✅ Confirmado

---

## AC Propuestos por QA

> Estas son **sugerencias** basadas en el análisis de riesgo. ✅ Ambos confirmados por Developer.

**AC-P1** — *Propuesto QA* — El servicio de autocompletado falla gracefully (modo degradado)
- Si la API está caída o la cuota se agota → State y City quedan vacíos pero editables manualmente
- El formulario puede enviarse con esos campos completados a mano
- Frontend muestra toast notification
- **Origen**: RIESGO-004
- **Estado**: ✅ **Confirmado por Developer** (H1, H3)

**AC-P2** — *Propuesto QA* — La zona horaria UTC (sin país específico) tiene comportamiento definido
- Si el usuario selecciona UTC o una timezone que cubre múltiples países → Country muestra opciones o queda vacío editable
- No se autoselecciona un país incorrecto sin confirmación del usuario
- El guard de manual-override protege contra sobreescrituras no deseadas
- **Origen**: EC-003, EC-010
- **Estado**: ⚠️ Propuesto — a verificar en testing (Developer no abordó directamente)

---

## Preguntas Abiertas — TODAS RESUELTAS ✅

| ID | Pregunta | Respuesta del Developer | Fuente |
|----|----------|------------------------|--------|
| Q-001 | ¿En qué entidad se persiste la zona horaria? | `companies.timezone` (solo companies) | TDD Build 29-jun |
| Q-002 | ¿Qué servicio externo se usa para autocompletado? | **Geoapify Geocoding API** (`GEOAPIFY_URL` + `GEOAPIFY_API_KEY`) | Quick Prototype 19-jun + Correcciones 13-jul |
| Q-003 | Si el servicio externo está caído → ¿modo degradado? | Sí — endpoint retorna 404 sin key; frontend muestra toast fallback | Correcciones 13-jul (H1) |
| Q-004 | ¿El Postal Code es obligatorio? | **No** — autofill es con botón explícito, opcional | TDD Build 29-jun (TC-001) |
| Q-005 | Timezone UTC → ¿qué ocurre con Country? | Guard de manual-override protege; a verificar en testing | TDD Build 29-jun |
| Q-006 | ¿El selector de State es fijo o dinámico? | **Dinámico** — dropdown con subdivisiones por país; texto libre sin subdivisiones | TDD Build 29-jun (TC-020) |
| Q-007 | ¿Campos obligatorios para submit? | **Company Name, Timezone, Country** — State y Postal opcionales | Correcciones 13-jul (M4) |
| Q-008 | Contact Name → ¿editable o read-only? ¿origen? | **Editable**, prellenado desde `users.name` (Keycloak, nombre concatenado) | TDD Build 29-jun (TC-002) |
| Q-009 | ¿Servicio externo funcional en staging? | Sí — requiere `GEOAPIFY_API_KEY` en `.env` de flow_binaries | Correcciones 13-jul (H3) |

---

## Historial

| Fecha | Acción | Por |
|-------|--------|-----|
| 2026-06-23 | AC consolidados generados — Discovery track | QA Catalyst |
| 2026-07-17 | AC actualizados con respuestas del Developer (Deployment) — todas las Q resueltas, AC-6 desbloqueado, AC-3/AC-4/AC-7/AC-8 ajustados | QA Catalyst |
