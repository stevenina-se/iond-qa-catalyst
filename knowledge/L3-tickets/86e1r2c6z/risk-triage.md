# Risk Triage — 86e1r2c6z
# Refactorizar flujo y formulario de registro de compañía

> Generado: 2026-06-23 | Skill: test-docs/prioritize
> Módulo: auth (formulario /create-company)
> QA Engineer: Steve Nina

---

## Prioridad General del Ticket

**Criticidad del módulo**: 🟠 Alto (Auth — primer contacto del usuario con el producto)
**Impacto de la feature**: 🟠 Alto — El formulario de registro es el punto de entrada al onboarding. Un bug aquí impide la creación de nuevas companies.
**Complejidad de la implementación**: 🟠 Media-Alta — Involucra servicio externo, autocompletado, Keycloak, y posibles cambios de schema BD.

---

## Riesgos por Área

### 🔴 Riesgos Críticos

| ID | Área | Riesgo | Probabilidad | Impacto |
|----|------|--------|-------------|---------|
| RIESGO-001 | BD / Persistencia | **Schema de `companies` puede no tener todos los campos nuevos** (Contact Name, Postal Code, State, Country). Si se envían y el schema no los acepta → error silencioso o crash | Media | Crítico |
| RIESGO-002 | BD / Timezone | **AC-6 sin resolver**: ¿La zona horaria se persiste en `companies`, en el user admin inicial, o en ambos? Si el Developer asumió una entidad y QA testea otra → datos no guardados | Alta | Crítico |
| RIESGO-003 | Auth / Keycloak | **Flujo de registro post-Keycloak**: El formulario se llena después del SSO. Si el flujo se rompe (redirect incorrecto, token expirado) → usuario queda en estado inconsistente sin company asignada | Baja | Crítico |
| RIESGO-004 | Servicio Externo | **Dependencia de API de terceros** para autocompletar State/City por Postal Code. Si la API está caída o se agota la cuota (3.000 req/día) → ¿el formulario bloquea o degrada gracefully? | Media | Alto |

### 🟠 Riesgos Altos

| ID | Área | Riesgo | Probabilidad | Impacto |
|----|------|--------|-------------|---------|
| RIESGO-005 | UX / Autocompletado | **Autocompletado incorrecto**: Si el Postal Code coincide con múltiples State/City (ej. códigos ambiguos o internacionales), el autocompletado puede llenar campos incorrectos sin que el usuario lo note | Media | Alto |
| RIESGO-006 | UX / Timezone-Country sync | **Detección de Country por Timezone**: Si el usuario selecciona una timezone que coincide con múltiples países (ej. UTC±0 cubre UK, Portugal, Ghana...) → Country puede autodetectarse incorrectamente | Media | Alto |
| RIESGO-007 | Multi-tenant | **Company creada sin timezone** si el campo falla silenciosamente → afecta ejecuciones programadas, notificaciones y configuración regional de la company en el futuro | Baja | Alto |
| RIESGO-008 | Regresión / Login | **"Back to login" debe seguir funcionando** — Si el refactor rompe la navegación de retorno, el usuario queda atrapado en la pantalla de registro | Baja | Alto |

### 🟡 Riesgos Medios

| ID | Área | Riesgo | Probabilidad | Impacto |
|----|------|--------|-------------|---------|
| RIESGO-009 | Validaciones | **Campos obligatorios no bien marcados**: Si un campo requerido no tiene validación visual clara, el usuario puede enviar el formulario incompleto y recibir un error de API en lugar de feedback inline | Media | Medio |
| RIESGO-010 | Campos read-only | **Email/First Name/Last Name mostrados como read-only** pueden confundir al usuario si no hay suficiente indicación visual de que son de solo lectura (Keycloak) | Baja | Medio |
| RIESGO-011 | Responsive | **Layout en tablet** (breakpoint intermedio): Los diseños de mobile y desktop están mostrados en el prototipo, pero la tablet puede tener comportamientos inesperados en el switch de columnas | Media | Medio |
| RIESGO-012 | Caché del servicio externo | **Caché de autocompletado**: Si el caché tiene un TTL muy largo, cambios en los datos del servicio externo no se reflejan correctamente; si es muy corto, se agota la cuota de 3.000 req/día | Baja | Medio |
| RIESGO-013 | Panel izquierdo | **Carousel con iconos ocultos**: Se acordó dejar el contenido actual con los iconos de navegación ocultos. Si los iconos siguen en el DOM pero solo ocultos, pueden ser accesibles via teclado/screen reader (accesibilidad) | Baja | Bajo |

---

## Edge Cases Identificados

| ID | Edge Case | Por qué es relevante |
|----|-----------|---------------------|
| EC-001 | Postal Code inválido o no reconocido por el servicio externo | ¿El sistema muestra error o deja los campos vacíos? ¿Bloquea el envío? |
| EC-002 | Postal Code válido pero que cubre múltiples State/City | ¿Presenta lista de opciones o elige uno automáticamente? |
| EC-003 | Timezone que cubre múltiples países | Country autodetectado puede ser incorrecto |
| EC-004 | Usuario con Keycloak en un locale diferente (nombre con caracteres especiales: ñ, á, é...) | ¿Los campos read-only muestran correctamente caracteres Unicode? |
| EC-005 | Formulario enviado mientras la API de autocompletado está en request pendiente | ¿El formulario espera la respuesta o envía con campos vacíos? |
| EC-006 | País seleccionado donde el State/City no aplica (algunos países no tienen "State") | ¿El campo State selector se deshabilita o queda vacío y requerido? |
| EC-007 | Cuota de API (3.000 req/día) agotada | ¿El formulario funciona sin autocompletado (degraded mode) o falla completamente? |
| EC-008 | Usuario hace Back to login y luego regresa al formulario | ¿Los datos prellenados de Keycloak se mantienen? |
| EC-009 | El Company Name está vacío en Keycloak | ¿El campo Contact Name queda vacío o muestra un fallback? |
| EC-010 | Timezone seleccionada a UTC (sin país específico) | ¿Country queda vacío, muestra un default, o bloquea? |
| EC-011 | Responsive en viewport 768px (tablet portrait) | ¿Los dos paneles se muestran correctamente o colapsa a mobile? |
| EC-012 | Submit con campos de autocompletado recién llenados pero API con caché stale | ¿Los valores enviados son los de caché o los del último autocompletado? |

---

## Preguntas para el Developer (formato abierto)

> ℹ️ Estas son preguntas de aclaración, NO objeciones. El objetivo es entender el comportamiento esperado para testearlo correctamente.

| ID | Pregunta | AC relacionado |
|----|----------|----------------|
| Q-001 | ¿En qué entidad se persiste la zona horaria — `companies`, el `user` administrador inicial, o ambos? | AC-6 |
| Q-002 | ¿Qué servicio externo específico se usa para el autocompletado por Postal Code? (la URL fue truncada en el comentario) | AC-NUEVO-1 |
| Q-003 | ¿Qué ocurre si el servicio externo de autocompletado está caído o la cuota se agotó — el formulario funciona en modo degradado o muestra error? | AC-NUEVO-1 |
| Q-004 | ¿El campo Postal Code es obligatorio para el submit? ¿O el autocompletado es opcional? | AC-7 |
| Q-005 | ¿Cuál es el comportamiento esperado cuando la timezone no mapea a un único país (ej. UTC)? | AC-5 |
| Q-006 | ¿El campo State tiene una lista fija de opciones o es dinámica según el Country seleccionado? | AC-4 |
| Q-007 | ¿Qué campos son obligatorios para poder hacer submit? (Company Name, Timezone son los obvios — ¿cuáles más?) | AC-7 |
| Q-008 | ¿El campo Contact Name se prellena con el nombre del usuario de Keycloak y puede ser editado, o es también read-only? | AC-4 |
| Q-009 | ¿La branch del prototipo tiene el servicio externo configurado y funcional en el entorno de staging? | Entorno |

---

## Áreas de Regresión a Verificar

| Área | Riesgo de regresión | Prioridad |
|---|---|---|
| Flujo completo de registro de company | Cambios en el form pueden romper la creación de company end-to-end | 🔴 Crítico |
| "Back to login" navigation | Refactor de la vista puede romper el routing de retorno | 🔴 Crítico |
| Login con company ya creada (post-registro) | El registro exitoso debe llevar al usuario al flujo correcto dentro de Ionflow | 🟠 Alto |
| Campos guardados en BD | Si se agregan campos nuevos pero el schema no se actualizó → datos perdidos silenciosamente | 🔴 Crítico |
| Timezone en ejecuciones programadas | Si la timezone no se persiste correctamente → schedules en hora incorrecta | 🟠 Alto |

---

## Criterios de Priorización de Testing (cuando pase a Deployment)

### Testear siempre (bloqueante si falla)
1. El formulario puede enviarse con datos válidos completos → company se crea correctamente en BD
2. La zona horaria se persiste en la entidad correspondiente
3. El botón "Back to login" funciona
4. Los campos obligatorios muestran error si faltan
5. Los campos de Keycloak (email, nombre) se muestran correctamente como read-only

### Testear si hay tiempo (importante pero no bloqueante)
6. El autocompletado por Postal Code funciona (o degrada gracefully)
7. La detección de Country por timezone es correcta para casos comunes
8. El formulario es responsive en desktop y mobile
9. El campo Contact Name se prellena correctamente

### Nice to have
10. Panel izquierdo se ve correctamente en todos los breakpoints
11. Caché del servicio externo funciona (sin exceder cuota en testing)

---

## Historial

| Fecha | Acción | Por |
|-------|--------|-----|
| 2026-06-23 | risk-triage.md generado — Discovery track | QA Catalyst |
