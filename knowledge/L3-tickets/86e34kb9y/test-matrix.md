# Test Matrix — 86e34kb9y

> Ticket: [IOND] Mejorar búsqueda y jerarquía de resultados en Admin Companies
> Fecha de generación: 2026-10-05
> Basada en: AC Consolidados (21 AC en 5 grupos) + Risk Triage (11 riesgos, 18 edge cases)
> Módulo principal: Auth (Admin > Companies)

---

## Resumen

- **Total de casos**: 42
- **Happy path**: 15
- **Edge cases**: 14
- **Negativos**: 6
- **Regresión**: 7
- **Automatizables**: 28
- **Prioridad Crítica**: 14
- **Prioridad Alta**: 16
- **Prioridad Media**: 10
- **Prioridad Baja**: 2

---

## Test Matrix — Grupo A: Motor de Búsqueda

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-001 | Auth | AC-A1 | Happy Path | Buscar email exacto de Company User → company aparece como mejor match | Admin logueado. Company con user `owner@billing.com` existe | `Admin Login > Topbar: ⌘K > Fill Search: "owner@billing.com" > Verify: Company aparece como Mejor coincidencia > Verify: Match explanation muestra "Company User"` | La company aparece como mejor coincidencia. `search_match_field: company_user_email`, `search_match_value: owner@billing.com` | 🔴 | ✅ | ⬜ |
| TC-002 | Auth | AC-A2 | Happy Path | Buscar email de contacto de company → company aparece con match de contacto | Admin logueado. Company con contacto `contact@acme.com` existe en tabla `contacts` | `Admin Login > Topbar: ⌘K > Fill Search: "contact@acme.com" > Verify: Company aparece > Verify: Match explanation muestra "email de contacto"` | La company aparece. `search_match_field: company_contact_email` | 🔴 | ✅ | ⬜ |
| TC-003 | Auth | AC-A3 | Happy Path | Buscar fragmento de dominio → companies con ese dominio aparecen (case-insensitive) | Admin logueado. Company con user `owner@billing.com` existe | `Admin Login > Topbar: ⌘K > Fill Search: "billing.com" > Verify: Company aparece > Fill Search: "BILLING.COM" > Verify: Mismos resultados` | Company aparece. La búsqueda ignora mayúsculas/minúsculas | 🔴 | ✅ | ⬜ |
| TC-004 | Auth | AC-A4 | Happy Path | Deduplicación: múltiples users coinciden → company aparece 1 sola vez | Company con 3 users con emails `a@domain.com`, `b@domain.com`, `c@domain.com` | `Admin Login > Topbar: ⌘K > Fill Search: "domain.com" > Verify: Company aparece exactamente 1 vez` | La company aparece una sola vez, no 3 | 🔴 | ✅ | ⬜ |
| TC-005 | Auth | AC-A5 | Happy Path | Permisos: company sin permiso no aparece en búsqueda | Admin con permisos restringidos (sin acceso a Company X). Company X tiene user con email buscado | `Admin Login (permisos restringidos) > Topbar: ⌘K > Fill Search: "email-de-company-x@test.com" > Verify: Company X NO aparece > Verify: Email NO se muestra` | Company X no aparece. Email restringido no se expone | 🔴 | ✅ | ⬜ |
| TC-006 | Auth | AC-A6 | Happy Path | Catálogo completo: company fuera de página visible aparece al buscar | Admin logueado. Company objetivo está en página 5+ de resultados normales | `Admin Login > Navigate: /admin/companies > Verify: Company no visible en página 1 > Fill Search bar: "email-de-company-lejana@test.com" > Verify: Company aparece > Verify: Paginación refleja colección filtrada` | Company aparece aunque estaba fuera de la página visible | 🟠 | ✅ | ⬜ |
| TC-007 | Auth | AC-A7 | Happy Path | Jerarquía determinista: ranking estable con consulta de email | Admin logueado. Existen companies con coincidencias exactas y parciales | `Admin Login > Topbar: ⌘K > Fill Search: "@billing.com" > Verify: Orden de resultados > Repetir búsqueda 3 veces > Verify: Mismo orden cada vez` | Resultados en orden: exacto email > parcial email > nombre. Orden estable entre ejecuciones | 🔴 | ✅ | ⬜ |
| TC-008 | Auth | AC-A7 | Happy Path | Jerarquía determinista: ranking con consulta normal (sin @) | Admin logueado. Company "Billing Corp" existe con users con emails | `Admin Login > Topbar: ⌘K > Fill Search: "Billing" > Verify: Orden: exacto nombre > inicio nombre > parcial nombre > exacto email > parcial email` | Orden cambia cuando la consulta no tiene formato email | 🔴 | ✅ | ⬜ |
| TC-009 | Auth | AC-A8 | Happy Path | Sin resultados: estado vacío con acción de limpiar | Admin logueado | `Admin Login > Topbar: ⌘K > Fill Search: "zzznoexiste999@fake.xyz" > Verify: Estado sin resultados visible > Verify: Botón/acción para limpiar consulta > Click [Limpiar] > Verify: Input vacío` | Se muestra estado sin resultados con acción para limpiar | 🟠 | ✅ | ⬜ |
| TC-010 | Auth | AC-A9 | Edge Case | Buscar email con caracteres especiales: `user+tag@domain.com` | Company con user `user+tag@domain.com` existe | `Admin Login > Topbar: ⌘K > Fill Search: "user+tag@domain.com" > Verify: Company aparece > Verify: El `+` se preservó en la búsqueda` | El `+` no se elimina. Company encontrada correctamente | 🟠 | ✅ | ⬜ |
| TC-011 | Auth | AC-A9 | Edge Case | Buscar email con puntos y guiones en dominio | Company con user `user@my-company.co.uk` existe | `Admin Login > Topbar: ⌘K > Fill Search: "my-company.co.uk" > Verify: Company aparece` | Puntos y guiones se preservan. Company encontrada | 🟠 | ✅ | ⬜ |
| TC-012 | Auth | AC-A10 | Edge Case | Company sin Company Users → sigue siendo buscable por nombre/ID | Company "Orphan Corp" sin users asociados en `company_user` | `Admin Login > Topbar: ⌘K > Fill Search: "Orphan Corp" > Verify: Company aparece > Fill Search: ID de la company > Verify: Company aparece` | Company sin users sigue siendo localizable por nombre e ID | 🟠 | ✅ | ⬜ |
| TC-013 | Auth | AC-A4 | Edge Case | Email de contacto = email de company user → company aparece 1 vez con match correcto | Company donde contacto y user principal tienen el mismo email | `Admin Login > Topbar: ⌘K > Fill Search: "same@email.com" > Verify: Company aparece exactamente 1 vez > Verify: Match explanation muestra tipo correcto` | Deduplicación funciona. Company aparece 1 vez | 🟠 | ✅ | ⬜ |
| TC-014 | Auth | AC-A5 | Negativo | Usuario Company (no admin) no puede buscar companies por email | Login como Company User (no admin) | `Company Login > Verify: No hay acceso a /admin/companies > Verify: Buscador global de tenant NO muestra sección Companies` | El buscador de tenant no expone búsqueda de companies por email | 🔴 | ✅ | ⬜ |
| TC-015 | Auth | AC-A7 | Edge Case | Query vacía → no ejecuta búsqueda, muestra estado inicial | Admin logueado | `Admin Login > Topbar: ⌘K > Verify: Búsquedas recientes o estado vacío > Clear input > Verify: No hay resultados de búsqueda` | Input vacío no dispara búsqueda. Muestra estado inicial | 🟡 | ✅ | ⬜ |

---

## Test Matrix — Grupo B: Buscador Global Admin

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-016 | Auth | AC-B1 | Happy Path | Abrir buscador global con ⌘K / Ctrl+K | Admin logueado en cualquier vista | `Admin Login > Press: ⌘K (Mac) o Ctrl+K (Windows) > Verify: Diálogo de búsqueda abierto > Verify: Input con foco > Verify: Secciones Pages y Companies visibles` | Buscador global se abre con shortcut. Input tiene foco. 2 secciones visibles | 🔴 | ✅ | ⬜ |
| TC-017 | Auth | AC-B1 | Edge Case | Búsquedas recientes persisten en localStorage | Admin logueado. Realizar búsqueda previa | `Admin Login > Topbar: ⌘K > Fill Search: "test query" > Verify: Resultado > Press: Esc > Topbar: ⌘K > Verify: "test query" aparece en recientes` | Búsquedas recientes se guardan y se muestran al reabrir | 🟡 | ✅ | ⬜ |
| TC-018 | Auth | AC-B3 | Happy Path | Navegación por teclado: flechas, Enter, Esc | Admin logueado | `Admin Login > Topbar: ⌘K > Fill Search: "comp" > Press: ↓ > Verify: Primer resultado resaltado > Press: ↓ > Verify: Segundo resultado resaltado > Press: ↑ > Verify: Primer resultado resaltado > Press: Enter > Verify: Navega al resultado` | Flechas mueven resaltado. Enter abre resultado. Foco permanece en input | 🟠 | ✅ | ⬜ |
| TC-019 | Auth | AC-B3 | Edge Case | Home/End en buscador → navegan a primer/último resultado (comportamiento conocido) | Admin logueado con resultados de búsqueda | `Admin Login > Topbar: ⌘K > Fill Search: "test" > Verify: Resultados > Press: End > Verify: Último resultado resaltado (no cursor al final del input) > Press: Home > Verify: Primer resultado resaltado` | Home/End navegan a primer/último resultado. Documentado como trade-off aceptado | 🟡 | ✅ | ⬜ |
| TC-020 | Auth | AC-B4 | Happy Path | "Ver las N companies" navega al listado con query aplicada | Admin logueado. Búsqueda con resultados de companies | `Admin Login > Topbar: ⌘K > Fill Search: "@example.com" > Verify: Enlace "Ver las N companies" visible > Click [Ver las N companies] > Verify: URL es /admin/companies?search=%40example.com > Verify: Tabla filtrada con resultados` | Navega a listado de companies con `?search=` en URL. Tabla ya filtrada | 🟠 | ✅ | ⬜ |
| TC-021 | Auth | AC-B5 | Edge Case | Iconos del buscador coinciden con sidebar | Admin logueado | `Admin Login > Topbar: ⌘K > Verify: Iconos de sección Pages coinciden con los iconos del sidebar > Verify: No hay iconos fallback (Circle)` | Iconos consistentes entre buscador y sidebar | 🟡 | ❌ | ⬜ |
| TC-022 | Auth | AC-B1 | Negativo | Esc cierra buscador correctamente | Admin logueado con buscador abierto | `Admin Login > Topbar: ⌘K > Fill Search: "test" > Press: Esc > Verify: Diálogo cerrado > Verify: Foco vuelve a la página` | Buscador se cierra. No quedan overlays residuales | 🟡 | ✅ | ⬜ |

---

## Test Matrix — Grupo C: Tabla de Companies

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-023 | Auth | AC-C1 | Happy Path | Tabla de companies carga con CompanyDetailsCell enriquecida | Admin logueado | `Admin Login > Navigate: /admin/companies > Verify: Tabla carga con datos > Verify: Cada fila muestra avatar/logo, nombre enlazado, badge de estado, schema_suffix` | Tabla renderiza correctamente con celda de detalles enriquecida | 🟠 | ✅ | ⬜ |
| TC-024 | Auth | AC-C1 | Edge Case | Company sin logo → fallback de avatar | Company sin logo configurado | `Admin Login > Navigate: /admin/companies > Verify: Company sin logo muestra avatar fallback (iniciales o placeholder)` | Fallback de avatar funciona. No hay imagen rota | 🟡 | ✅ | ⬜ |
| TC-025 | Auth | AC-C2 | Happy Path | Persistencia de búsqueda en URL: sobrevive a F5 | Admin logueado | `Admin Login > Navigate: /admin/companies > Fill Search: "test query" > Verify: URL contiene ?search=test+query > Press: F5 (recarga) > Verify: Búsqueda sigue activa > Verify: Resultados son los mismos` | Búsqueda persiste en `?search=` y sobrevive a recarga | 🟠 | ✅ | ⬜ |
| TC-026 | Auth | AC-C2 | Happy Path | Navegación browser atrás/adelante con búsqueda | Admin logueado | `Admin Login > Navigate: /admin/companies > Fill Search: "query1" > Verify: Resultados > Fill Search: "query2" > Verify: Resultados > Press: Browser Back > Verify: Búsqueda vuelve a "query1" > Press: Browser Forward > Verify: Búsqueda vuelve a "query2"` | Historial de búsqueda funciona con atrás/adelante del browser | 🟠 | ✅ | ⬜ |
| TC-027 | Auth | AC-C3 | Happy Path | Paginación estable con búsqueda activa: sin duplicados entre páginas | Búsqueda activa con resultados que ocupan múltiples páginas. `per_page=3` | `Admin Login > Navigate: /admin/companies?search=@example.com&per_page=3 > Verify: Página 1 muestra 3 companies > Click [Página 2] > Verify: Companies de página 2 ≠ companies de página 1 > Recorrer todas las páginas > Verify: Ninguna company repetida ni ausente` | Paginación estable. Sin duplicados entre páginas | 🔴 | ✅ | ⬜ |
| TC-028 | Auth | AC-C1 | Happy Path | Pista del match visible en CompanyDetailsCell | Admin logueado. Búsqueda por email activa | `Admin Login > Navigate: /admin/companies?search=owner@billing.com > Verify: Cada fila que coincide por email muestra la pista del match (ej. "Coincidencia por Company User")` | La razón del match se muestra en la celda de detalles | 🟠 | ✅ | ⬜ |
| TC-029 | Auth | AC-C2 | Negativo | URL con search param inválido o vacío | Admin logueado | `Admin Login > Navigate: /admin/companies?search= > Verify: Tabla carga normalmente con todos los resultados > Navigate: /admin/companies?search=%00%00 > Verify: No errores. Estado vacío o resultados normales` | Params inválidos no rompen la tabla | 🟡 | ✅ | ⬜ |

---

## Test Matrix — Grupo D: Regresión Buscador Tenant

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-030 | Auth | AC-D1 | Happy Path | Buscador global de Tenant funciona con 5 secciones | Company User logueado como tenant | `Company Login > Press: ⌘K > Fill Search: "flow" > Verify: Resultados de flows aparecen > Fill Search: "app" > Verify: Resultados de apps aparecen > Verify: Las 5 secciones funcionan` | Buscador de tenant reescrito funciona correctamente con todas las secciones | 🟠 | ✅ | ⬜ |
| TC-031 | Auth | AC-D2 | Edge Case | Tenant sin permisos sobre una sección → fallback de icono | Company User con permisos restringidos (sin acceso a alguna sección) | `Company Login (permisos limitados) > Press: ⌘K > Fill Search: query > Verify: Secciones sin permiso muestran iniciales como icono (no icono lucide)` | Fallback graceful: iniciales en vez de icono. No rompe el buscador | 🟡 | ❌ | ⬜ |

---

## Test Matrix — Grupo E: Aislamiento CSS y Regresión

| ID | Módulo | AC | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Automatizable | Estado |
|----|--------|-----|------|-------------|--------------|-------|-------------------|-----------|---------------|--------|
| TC-032 | Auth | AC-E1 | Happy Path | Vistas admin PrimeVue no se rompen después de usar CompanyTable | Admin logueado | `Admin Login > Navigate: /admin/companies > Verify: Tabla shadcn carga OK > Navigate: /admin/dashboard > Verify: Dashboard PrimeVue renderiza OK > Navigate: otra vista admin PrimeVue > Verify: Renders correctos` | Las vistas PrimeVue existentes no sufren bleeding de estilos `.modern-ui` | 🟡 | ❌ | ⬜ |
| TC-033 | Auth | AC-E2 | Happy Path | Búsqueda por nombre de company → mismos resultados que antes | Admin logueado | `Admin Login > Navigate: /admin/companies > Fill Search: "Acme Corp" > Verify: Company aparece en resultados > Fill Search: ID de company > Verify: Company aparece` | Criterios de búsqueda existentes (nombre, ID) siguen funcionando | 🔴 | ✅ | ⬜ |

---

## Casos de Regresión

| ID | Módulo impactado | Caso de regresión | Por qué podría romperse | Prioridad |
|----|-----------------|-------------------|------------------------|-----------|
| REG-001 | Auth | Login de admin funciona correctamente | Los cambios en el topbar/search podrían afectar la carga del layout admin | 🔴 |
| REG-002 | Auth | Navegación sidebar de admin funciona | `navIconsByHref` modifica la resolución de iconos del menú admin | 🟠 |
| REG-003 | Auth | Buscador de tenant: búsqueda de flows funciona | `GlobalSearch.vue` fue reescrito completamente. Flows es la sección más usada | 🟠 |
| REG-004 | Auth | Buscador de tenant: búsqueda de apps funciona | Misma razón que REG-003 | 🟠 |
| REG-005 | Auth | Lista de companies: ordenamiento por columna funciona | CompanyTable migrada de PrimeVue → TanStack. Sort podría comportarse diferente | 🟠 |
| REG-006 | Auth | Lista de companies: acciones por fila (editar, eliminar) funcionan | Migración de tabla puede afectar event handlers de las acciones | 🟠 |
| REG-007 | Dashboard | Admin dashboard no tiene regresión visual | Aislamiento `.modern-ui` podría filtrar estilos si el subárbol no está bien acotado | 🟡 |

---

## Queries de Verificación BD

```sql
-- ============================================================
-- QUERIES DE VERIFICACIÓN — Ticket 86e34kb9y
-- Fuentes de schema:
--   ../gateway/database/migrations/2024_11_26_091013_create_companies_table.php
--   ../gateway/database/migrations/2024_11_26_092110_create_company_user_table.php
--   ../gateway/database/migrations/2014_10_12_000000_create_users_table.php
--   ../gateway/database/migrations/2024_11_26_140850_create_contacts_table.php
-- ============================================================

-- TC-001 / TC-003: Verificar que company tiene users con emails
-- Tablas: companies (id, name, schema_suffix, status)
--         company_user (company_id FK→companies, user_id FK→users)
--         users (id, name, email)
SELECT c.id, c.name, c.schema_suffix, c.status, u.email AS user_email
FROM companies c
JOIN company_user cu ON cu.company_id = c.id
JOIN users u ON u.id = cu.user_id
WHERE c.id = '<company_id>'
ORDER BY u.email;

-- TC-002: Verificar email de contacto de company
-- Tablas: contacts (contactable_type, contactable_id, email)
--         companies (id, name)
-- Nota: contactable_type debe ser 'company' (morph map en AppServiceProvider.php:50)
SELECT c.id, c.name, ct.email AS contact_email, ct.contactable_type
FROM companies c
JOIN contacts ct ON ct.contactable_id = c.id AND ct.contactable_type = 'company'
WHERE c.id = '<company_id>';

-- TC-004: Verificar deduplicación — company con múltiples users del mismo dominio
SELECT c.id, c.name, COUNT(u.id) AS user_count, 
       STRING_AGG(u.email, ', ') AS user_emails
FROM companies c
JOIN company_user cu ON cu.company_id = c.id
JOIN users u ON u.id = cu.user_id
WHERE u.email LIKE '%@<domain>%'
GROUP BY c.id, c.name
HAVING COUNT(u.id) > 1;

-- TC-012: Verificar companies sin users asociados
SELECT c.id, c.name, c.status
FROM companies c
LEFT JOIN company_user cu ON cu.company_id = c.id
WHERE cu.id IS NULL
LIMIT 10;

-- TC-013: Verificar si email de contacto = email de user para misma company
SELECT c.id, c.name, u.email AS user_email, ct.email AS contact_email
FROM companies c
JOIN company_user cu ON cu.company_id = c.id
JOIN users u ON u.id = cu.user_id
JOIN contacts ct ON ct.contactable_id = c.id AND ct.contactable_type = 'company'
WHERE u.email = ct.email;

-- VERIFICACIÓN DE ÍNDICES pg_trgm (ejecutar como admin de BD)
-- Nota: Las 3 migraciones del ticket agregaron extensión pg_trgm + índices de expresión
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename IN ('companies', 'users', 'contacts', 'company_user')
  AND indexdef ILIKE '%trgm%'
ORDER BY tablename, indexname;
```
