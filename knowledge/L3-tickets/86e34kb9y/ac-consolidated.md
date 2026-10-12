# Acceptance Criteria Consolidados — 86e34kb9y

> Ticket: [IOND] Mejorar búsqueda y jerarquía de resultados en Admin Companies
> Fecha de consolidación: 2026-10-05
> Fuentes: Descripción original del ticket + Comentario Marcel (23-Sep) + R,D & Architect Review de Gustavo (28-Sep) + Risk Triage
> Modo: Discovery — los AC propuestos son SUGERENCIAS para acuerdo con el equipo

---

## Evaluación de AC Originales (Gherkin del ticket)

| AC | Texto original | ¿Verificable? | ¿Completo? | ¿Ambiguo? | Observación |
|----|---------------|----------------|------------|-----------|-------------|
| AC-G1 | Email principal exacto → compañía como Mejor coincidencia + explica match | ✅ | ✅ | ❌ | Claro y verificable. Gherkin bien definido. |
| AC-G2 | Fragmento o dominio → compañía encontrada + case-insensitive | ✅ | ✅ | ❌ | Claro. Cubre búsqueda parcial. |
| AC-G3 | Deduplicación → compañía una sola vez si varios users coinciden | ✅ | ✅ | ❌ | Claro. Criterio binario verificable. |
| AC-G4 | Permisos y privacidad → compañía no aparece sin permiso, email no se expone | ✅ | ✅ | ❌ | Claro. Crítico para seguridad. |
| AC-G5 | Catálogo completo → búsqueda sobre colección completa antes de paginar | ✅ | ⚠️ | ❌ | Verificable pero requiere datos suficientes para que haya paginación. |
| AC-G6 | Jerarquía determinista → ranking estable entre ejecuciones | ✅ | ✅ | ❌ | Verificable ejecutando la misma query múltiples veces. |
| AC-G7 | Sin resultados → estado vacío + acción limpiar consulta | ✅ | ✅ | ❌ | Claro. UI state verificable. |

---

## AC Consolidados — Lista Final

> Estructura: AC Gherkin preservados + AC expandidos por divergencias + AC nuevos por features implementados
> Cada AC incluye su fuente y justificación

### GRUPO A — Motor de Búsqueda (Backend — `gateway`)

> Estos AC cubren la escalera de relevancia, el motor de búsqueda y la respuesta aditiva del API.

**AC-A1**: Dado que una compañía tiene un Company User con email `owner@billing.com`, cuando un administrador busca `owner@billing.com` en Admin > Companies, entonces la compañía aparece como Mejor coincidencia y el resultado explica que coincide por Company User (`search_match_field: company_user_email`).
- Fuente: AC-G1 original del ticket
- Riesgo: R-001 (🔴 Crítico)

**AC-A2**: Dado que una compañía tiene un email de contacto `contact@acme.com`, cuando un administrador busca `contact@acme.com`, entonces la compañía aparece y el resultado explica que coincide por email de contacto (`search_match_field: company_contact_email`).
- Fuente: D-2 (divergencia — Developer amplió a email de contacto de company)
- Riesgo: R-001 (🔴 Crítico)

**AC-A3**: Dado que una compañía tiene un usuario con email `owner@billing.com`, cuando el administrador busca `billing.com`, entonces la compañía aparece y la búsqueda ignora diferencias entre mayúsculas y minúsculas.
- Fuente: AC-G2 original del ticket
- Riesgo: R-007 (🟠 Alto)

**AC-A4**: Dado que varios Company Users de la misma compañía coinciden con la consulta, cuando el administrador realiza la búsqueda, entonces la compañía aparece una sola vez.
- Fuente: AC-G3 original del ticket
- Riesgo: R-004 (🟠 Alto)

**AC-A5**: Dado que el usuario no tiene permiso para consultar una compañía, cuando realiza una búsqueda que coincide con su email, entonces la compañía no aparece y el email restringido no se expone.
- Fuente: AC-G4 original del ticket
- Riesgo: R-002 (🔴 Crítico)

**AC-A6**: Dado que una compañía coincidente se encuentra fuera de la página visible, cuando el administrador busca su email, entonces la compañía aparece y la paginación refleja la colección filtrada completa.
- Fuente: AC-G5 original del ticket
- Riesgo: R-004 (🟠 Alto)

**AC-A7**: Dado que existen coincidencias exactas y parciales por email, nombre o ID, cuando el administrador realiza la misma consulta en el mismo contexto, entonces se aplica el ranking de compañías definido y el orden permanece estable entre ejecuciones.
- Fuente: AC-G6 original del ticket
- Riesgo: R-001 (🔴 Crítico)

  **Ranking esperado (consulta con @ o formato email):**
  1. Coincidencia exacta con email principal
  2. Coincidencia exacta con email de otro Company User
  3. Coincidencia parcial con email principal
  4. Coincidencia parcial con otros emails
  5. Coincidencias por nombre, ID u otros campos actuales

  **Ranking esperado (consulta normal):**
  1. Coincidencia exacta con nombre o ID de compañía
  2. Coincidencia por inicio del nombre
  3. Coincidencia parcial con nombre
  4. Coincidencia exacta con email principal
  5. Coincidencia con otros emails o campos secundarios

**AC-A8**: Dado que ninguna compañía coincide con la consulta, cuando el administrador realiza la búsqueda, entonces se muestra un estado sin resultados y existe una acción para limpiar la consulta.
- Fuente: AC-G7 original del ticket
- Riesgo: R-003 (🔴 Crítico)

**AC-A9**: La búsqueda debe conservar caracteres significativos como `+`, puntos y guiones. No debe aplicar normalización destructiva. Email completo, fragmento y dominio deben funcionar como criterios de búsqueda.
- Fuente: Requisitos R-4 y R-5 de la descripción del ticket
- Riesgo: R-007 (🟠 Alto)

**AC-A10**: Las compañías sin Company User principal válido siguen siendo localizables por los criterios actuales (nombre, ID, subdominio).
- Fuente: Requisito R-9 de la descripción del ticket
- Riesgo: R-001 (🟠 Alto)

**AC-A11**: La búsqueda resuelve la relación compañía–usuarios sin consultas N+1. Se utilizan índices `pg_trgm` de expresión.
- Fuente: Requisito R-10 de la descripción del ticket + R,D Report de Gustavo (28-Sep)
- Riesgo: R-004 (🟠 Alto)

---

### GRUPO B — Buscador Global Admin (Frontend — `gateway-ion`)

> Estos AC cubren el nuevo `AdminGlobalSearch.vue` y el shell reutilizable `GlobalSearchShell.vue`.

**AC-B1**: El buscador global de Admin se abre con `⌘K` (Mac) / `Ctrl+K` (Windows), muestra un diálogo con input de búsqueda, debounce, búsquedas recientes y estado vacío.
- Fuente: R,D Report de Gustavo (28-Sep) — Tarea B
- Riesgo: R-003 (🔴 Crítico)

**AC-B2**: El buscador global de Admin muestra dos secciones: **Pages** y **Companies**. Las compañías se buscan con la escalera de relevancia del backend (AC-A7).
- Fuente: R,D Report de Gustavo (28-Sep) — `AdminGlobalSearch.vue`
- Riesgo: R-003 (🔴 Crítico)

**AC-B3**: La navegación por teclado funciona correctamente: flechas ↑↓ mueven el resaltado vía `aria-activedescendant`, Enter abre el resultado seleccionado, Esc cierra el diálogo. El foco permanece siempre en el input.
- Fuente: R,D Report de Gustavo (28-Sep) — Tarea B + §2.4
- Riesgo: R-009 (🟡 Medio)
- **Comportamiento conocido**: Home/End navegan a primer/último resultado en lugar de mover el caret del input. Aceptado como trade-off.

**AC-B4**: El enlace "Ver las N companies" navega al listado `/admin/companies?search=<query>` con la tabla ya filtrada, en lugar de paginar dentro del diálogo.
- Fuente: R,D Report de Gustavo (28-Sep) — Tarea B
- Riesgo: R-003 (🟠 Alto)

**AC-B5**: Los iconos del buscador global coinciden con los iconos del sidebar de Admin. Se resuelven desde `nav.config.ts` vía `navIconsByHref(sections)`.
- Fuente: R,D Report de Gustavo (28-Sep) — §2.5
- Riesgo: R-010 (🟡 Medio)

---

### GRUPO C — Tabla de Companies (Frontend — `gateway-ion`)

> Estos AC cubren la migración de `CompanyTable.vue` de PrimeVue a shadcn/TanStack Table.

**AC-C1**: La tabla de companies en `/admin/companies` carga correctamente con los datos de todas las compañías, mostrando las columnas existentes más la nueva celda de detalles (`CompanyDetailsCell`) con avatar/logo, nombre enlazado, badge de estado, `schema_suffix` y pista del match.
- Fuente: R,D Report de Gustavo (28-Sep) — Tarea C
- Riesgo: R-005 (🟠 Alto)

**AC-C2**: La búsqueda en la tabla se persiste en el query param `?search=` mediante `useListQuerySync`. La búsqueda sobrevive a la recarga (F5) y funciona con la navegación del browser (atrás/adelante).
- Fuente: R,D Report de Gustavo (28-Sep) — Tarea C
- Riesgo: R-005 (🟠 Alto)

**AC-C3**: La paginación de la tabla funciona correctamente con la búsqueda activa. No hay companies repetidas ni ausentes entre páginas.
- Fuente: R,D Report de Gustavo (28-Sep) — Comprobaciones transversales §1
- Riesgo: R-004 (🟠 Alto)

---

### GRUPO D — Regresión del Buscador de Tenant

> El buscador de tenant fue reescrito sobre el mismo shell como efecto colateral del ticket.

**AC-D1**: El buscador global de Tenant fue reescrito sobre el mismo `GlobalSearchShell.vue` con 5 secciones. Debe funcionar correctamente para la búsqueda de flows, apps, appActions y las demás secciones existentes.
- Fuente: R,D Report de Gustavo (28-Sep) — Tarea B
- Riesgo: R-006 (🟠 Alto)

**AC-D2**: Si un usuario de tenant no tiene permisos sobre una sección, la fila correspondiente en el buscador muestra iniciales como fallback en vez del icono (degrada gracefully, no rompe).
- Fuente: R,D Report de Gustavo (28-Sep) — §2.5
- Riesgo: R-006 (🟡 Medio)

---

### GRUPO E — Aislamiento y Regresión Técnica

**AC-E1**: El aislamiento CSS `.modern-ui` acotado al subárbol (tabla + disparadores del buscador) no rompe las vistas admin PrimeVue existentes. Las superficies, bordes y selects de componentes PrimeVue en admin deben renderizar correctamente.
- Fuente: R,D Report de Gustavo (28-Sep) — §2.3
- Riesgo: R-008 (🟡 Medio)

**AC-E2**: Los criterios de búsqueda existentes (nombre de company, ID, subdominio) siguen funcionando correctamente después de los cambios.
- Fuente: Requisito R-11 de la descripción del ticket
- Riesgo: R-001 (🟠 Alto)

---

## AC Excluidos del Scope

| AC | Razón de exclusión | Fuente |
|---|---|---|
| Búsqueda del selector de nodos del Flow Editor | Cubierto por IONF-1078 | Descripción §No incluido + Comentario Marcel (23-Sep) |
| Cambio de nombre Agent a AI Agent | Cubierto por IONF-1078 | Descripción §No incluido |
| Requerimiento 1 del ticket | Trasladado al ticket `86e1ryauq` | Comentario Marcel (23-Sep) |

---

## Transformación AC → Casos de Test

| AC | Caso de test (Happy Path) | Casos Edge | Caso Negativo |
|----|--------------------------|------------|---------------|
| AC-A1 | Buscar email exacto de company user → company aparece como mejor match | Email con mayúsculas mixtas, email con `+tag` | Buscar email de user de company sin permiso |
| AC-A2 | Buscar email de contacto de company → company aparece con match de contacto | Email de contacto = email de user → deduplicación, company sin contacto | Email de contacto de company sin permiso |
| AC-A3 | Buscar fragmento `billing.com` → companies con ese dominio aparecen | Solo `@`, solo dominio TLD, fragmento que coincide con nombre Y email | Fragmento que no coincide con nada |
| AC-A4 | 3 users del mismo dominio → company aparece 1 sola vez | Users con emails idénticos, users en companies diferentes | N/A |
| AC-A5 | Buscar email de company restringida → no aparece, email no se expone | User con permisos parciales, admin con todos los permisos | Login como company user (no admin) |
| AC-A6 | Company en página 5 → buscar su email → aparece en resultados | Buscar con per_page=3, cambiar página durante búsqueda | Búsqueda que no genera resultados paginados |
| AC-A7 | Buscar `@billing.com` → orden: exacto email > parcial email > nombre | Buscar `billing` (sin @) → orden diferente, múltiples tiers simultáneos | Query vacía |
| AC-A8 | Buscar string aleatorio → estado sin resultados + botón limpiar | Buscar después de tener resultados previos | N/A |
| AC-A9 | Buscar `user+tag@domain.com` → preserva el `+` | Email con puntos consecutivos, guiones en dominio | Caracteres especiales SQL injection |
| AC-A10 | Company sin users → sigue siendo buscable por nombre/ID | Company con user eliminado, company recién creada sin users | N/A |
| AC-B1 | `⌘K` abre buscador → escribir query → resultados aparecen | Abrir/cerrar rápidamente, debounce funciona, recientes persisten | Tecla no mapeada |
| AC-B3 | ↓↑ mueven resaltado → Enter abre → Esc cierra | Home/End (comportamiento conocido: nav a primer/último resultado) | Tab fuera del diálogo |
| AC-B4 | "Ver N companies" → navega a `/admin/companies?search=query` | Navegar y luego volver atrás en browser | Link con query vacía |
| AC-C1 | Tabla carga con avatar, nombre, badge, pista del match | Company sin logo (fallback), company sin match (búsqueda vacía) | Company con datos corruptos |
| AC-C2 | Buscar → F5 → búsqueda persiste en URL | Limpiar búsqueda → URL se actualiza, atrás/adelante en browser | URL con search param inválido |
| AC-C3 | Paginar con búsqueda activa → sin duplicados entre páginas | Cambiar per_page durante búsqueda, ir a última página | Paginación con 0 resultados |
| AC-D1 | Buscador tenant: buscar flow → resultado correcto | Buscar en las 5 secciones, cambiar de admin a tenant | Buscador sin Pinia (edge técnico) |
| AC-E1 | Abrir vista admin PrimeVue después de CompanyTable → renders OK | Alternar entre vistas nuevas y PrimeVue rápidamente | N/A |
| AC-E2 | Buscar por nombre de company → mismos resultados que antes | Buscar por ID, buscar por subdominio | Nombre con caracteres especiales |
