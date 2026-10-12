## Contexto

### Descripción
Automatización de la gestión de Developers desde Admin. Cada tipo de app (Legacy, Applications, Custom, Grapp) tiene operaciones de Enable, Disable y SetUp que deben validarse.

### Módulo afectado
- Módulo principal: `Admin / Developers`
- Módulos relacionados: `Apps`, `Gateway`

---

## Test Cases

### Legacy

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-ADMIN-DEV-01 | Happy Path | Enable developer Legacy | 🟡 | ⬜ |
| TC-ADMIN-DEV-02 | Happy Path | Disable developer Legacy | 🟡 | ⬜ |
| TC-ADMIN-DEV-03 | Happy Path | SetUp developer Legacy | 🟡 | ⬜ |

### Applications

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-ADMIN-DEV-04 | Happy Path | Enable developer Application | 🟡 | ⬜ |
| TC-ADMIN-DEV-05 | Happy Path | Disable developer Application | 🟡 | ⬜ |
| TC-ADMIN-DEV-06 | Happy Path | SetUp developer Application | 🟡 | ⬜ |

### Custom

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-ADMIN-DEV-07 | Happy Path | Enable developer Custom | 🔵 | ⬜ |
| TC-ADMIN-DEV-08 | Happy Path | Disable developer Custom | 🔵 | ⬜ |
| TC-ADMIN-DEV-09 | Happy Path | SetUp developer Custom | 🔵 | ⬜ |

### Grapp

| ID | Tipo | Caso | Prioridad | Estado |
|----|------|------|-----------|--------|
| TC-ADMIN-DEV-10 | Happy Path | Enable developer Grapp | 🔴 | ⬜ |
| TC-ADMIN-DEV-11 | Happy Path | Disable developer Grapp | 🔴 | ⬜ |
| TC-ADMIN-DEV-12 | Happy Path | SetUp developer Grapp | 🔴 | ⬜ |
| TC-ADMIN-DEV-13 | Edge Case | Disable Grapp con usuarios activos — verificar impacto | 🟠 | ⬜ |

---

## Notas de Automatización
- Pre-requisito: Al menos 1 app de cada tipo creada previamente
- Grapp developers son los de mayor prioridad por su impacto en el marketplace
