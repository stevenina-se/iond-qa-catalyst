# Reconciliación de AC — 86e34kb9y

> Ticket: [IOND] Mejorar búsqueda y jerarquía de resultados en Admin Companies
> Fecha de reconciliación: 2026-10-05
> Fuentes: Descripción del ticket + Comentario de Marcel (23-Sep) + R,D & Architect Review de Gustavo (28-Sep)

---

## Tabla de Reconciliación

### 🟠 DIVERGENCIAS ALTAS (Scope modificado o expandido)

| # | AC Original (Descripción) | Decisión en Comentarios | AC Reconciliado | Fuente |
|---|--------------------------|------------------------|-----------------|--------|
| D-1 | **Requerimiento 1** incluido implícitamente en el alcance original del ticket | Marcel: "El requerimiento 1 será cubierto en el ticket `86e1ryauq` por lo que no es necesario que sea realizado en este ticket, el resto de requerimientos no relacionados sí deben de ser realizados." | **AC REDUCIDO**: Excluir el requerimiento 1 del scope de este ticket. Solo los requerimientos no relacionados con ese ticket aplican aquí. La estimación debe revisarse tras este traslado. | Comentario Marcel (23-Sep) |
| D-2 | **Búsqueda solo por email de Company Users** — La descripción y AC Gherkin mencionan únicamente emails de Company Users como criterio nuevo | Developer implementó búsqueda por **email de Company Users** + **email de contacto de la company** (`search_match_field: company_user_email \| company_contact_email`) | **AC EXPANDIDO**: La búsqueda cubre tanto emails de Company Users como el email de contacto de la company. Los resultados distinguen el tipo de match. Ambos criterios deben testearse. | Comentario Gustavo (28-Sep) - Tarea A, campo `search_match_field` |
| D-3 | **Búsqueda del selector de nodos del Flow Editor** — En la descripción original se menciona como "no incluido" pero requiere confirmación explícita del alcance | Marcel + Descripción confirman: cubierto por IONF-1078. La estimación debe revisarse tras este traslado. | **AC EXCLUIDO CONFIRMADO**: La búsqueda del selector de nodos del Flow Editor NO es parte de este ticket. Cubierto por IONF-1078. | Descripción §Alcance §No incluido + Comentario Marcel (23-Sep) |

### 🟡 DIVERGENCIAS MEDIAS (Features adicionales implementados)

| # | AC Original | Decisión en Comentarios | AC Reconciliado | Fuente |
|---|------------|------------------------|-----------------|--------|
| D-4 | (no existe en AC) | Developer **reescribió** `GlobalSearch.vue` del tenant sobre el mismo shell reutilizable `GlobalSearchShell.vue` (5 secciones). El buscador antiguo `SearchBar/SearchAdminDialog.vue` (PrimeVue Accordion) fue **eliminado** | **AC NUEVO**: El buscador global fue reescrito completamente tanto para Admin como para Tenant. Se eliminó el componente anterior. Requiere verificación de regresión en ambos contextos. | Comentario Gustavo (28-Sep) - Tarea B |
| D-5 | (no existe en AC) | Developer migró `CompanyTable.vue` de PrimeVue `DataTable` a `@/components/ui/DataTable` (TanStack) con `useListQuerySync` — búsqueda persiste en `?search=` y sobrevive a recarga (F5) | **AC NUEVO**: La tabla de companies fue migrada completamente de PrimeVue a shadcn/TanStack Table. Verificar: paginación, ordenamiento, persistencia de búsqueda en URL query params, navegación browser (atrás/adelante). | Comentario Gustavo (28-Sep) - Tarea C |
| D-6 | (no existe en AC) | "Ver las N companies" en el buscador global navega al listado con `?search=` aplicado, en vez de paginar dentro del diálogo | **AC NUEVO**: El enlace "Ver las N companies" en el buscador global debe navegar al listado `/admin/companies?search=<query>` con la tabla ya filtrada. | Comentario Gustavo (28-Sep) - Tarea B |
| D-7 | (no existe en AC) | Developer implementó `CompanyDetailsCell.vue` con avatar/logo, nombre enlazado, badge de estado, `schema_suffix` y pista del match | **AC NUEVO**: Cada fila de la tabla de companies muestra una celda de detalles enriquecida con avatar, nombre, badge, y la razón del match cuando proviene de búsqueda por email. | Comentario Gustavo (28-Sep) - Tarea C |

### 🟡 DIVERGENCIAS TÉCNICAS (Decisiones de implementación relevantes para QA)

| # | AC Original | Decisión en Comentarios | AC Reconciliado | Fuente |
|---|------------|------------------------|-----------------|--------|
| D-8 | (no existe en AC) | Aislamiento CSS `.modern-ui` acotado al subárbol de la tabla y disparadores del buscador, **NO** en `AdminLayout`. Precedente: `DialogContent.vue:47` ya lleva `modern-ui`. | **AC TÉCNICO**: Verificar que el aislamiento CSS `.modern-ui` no rompe vistas admin PrimeVue existentes. Los componentes nuevos deben renderizar correctamente dentro del subárbol acotado. | Comentario Gustavo (28-Sep) - §2.3 |
| D-9 | (no existe en AC) | `useTenantsMenu()` consulta auth store → buscador tenant ahora **depende de Pinia**. Sin permiso sobre una sección → fila cae a fallback de iniciales en vez del icono (degrada, no rompe). `useAdminMenu()` no filtra por permisos. | **AC TÉCNICO**: El buscador de tenant degrada gracefully cuando el usuario no tiene permisos sobre una sección (muestra iniciales en vez de icono). El buscador de admin no se ve afectado por permisos. | Comentario Gustavo (28-Sep) - §2.5 |
| D-10 | (no existe en AC) | Navegación por teclado: `ListboxFilter` mapea Home/End a primer/último resultado → **dejan de mover el caret** del input. Decisión: no mitigar por ahora. | **AC TÉCNICO (Contrapartida aceptada)**: Home/End no mueven el cursor del input en el buscador global. Se aceptó como trade-off por la navegación por teclado funcional. Documentar como comportamiento conocido, no como bug. | Comentario Gustavo (28-Sep) - §2.4 |
| D-11 | (no existe en AC) | Iconos del buscador ahora se resuelven desde `nav.config.ts` vía `navIconsByHref(sections)`. Se normalizó el modificador `pi-fw` que rompía la búsqueda por clave exacta. | **AC TÉCNICO**: Los iconos del buscador deben coincidir con los del sidebar. Verificar que la normalización de `pi-fw` no causa regresión visual. | Comentario Gustavo (28-Sep) - §2.5 |

### ✅ AC ORIGINALES PRESERVADOS (sin divergencia)

| # | AC Original (Gherkin) | Estado |
|---|----------------------|--------|
| AC-1 | Email principal exacto → compañía como Mejor coincidencia + explica match | ✅ Preservado |
| AC-2 | Fragmento o dominio → compañía encontrada + case-insensitive | ✅ Preservado |
| AC-3 | Deduplicación → compañía una sola vez si varios users coinciden | ✅ Preservado |
| AC-4 | Permisos y privacidad → compañía no aparece sin permiso, email no se expone | ✅ Preservado |
| AC-5 | Catálogo completo → búsqueda sobre colección completa antes de paginar | ✅ Preservado |
| AC-6 | Jerarquía determinista → ranking estable entre ejecuciones | ✅ Preservado |
| AC-7 | Sin resultados → estado vacío + acción limpiar consulta | ✅ Preservado |

### ✅ REQUISITOS ORIGINALES PRESERVADOS

| # | Requisito | Estado |
|---|-----------|--------|
| R-1 | Email principal obligatorio | ✅ Preservado |
| R-2 | Definir usuario principal (Discovery debe confirmar) | ✅ Preservado — Developer usó relación company→users |
| R-3 | Usuarios adicionales cuando contrato/rendimiento lo permitan | ✅ Preservado — Developer incluyó TODOS los company users |
| R-4 | Coincidencia normalizada (case-insensitive, sin espacios) | ✅ Preservado |
| R-5 | Sin normalización destructiva (+, puntos, guiones conservados) | ✅ Preservado |
| R-6 | Deduplicación | ✅ Preservado |
| R-7 | Contexto del match (email permitido o "Coincidencia por Company User") | ✅ Preservado via `search_match_field` + `search_match_value` |
| R-8 | Privacidad (solo admins autorizados) | ✅ Preservado |
| R-9 | Compatibilidad (companies sin user principal siguen siendo buscables) | ✅ Preservado |
| R-10 | Rendimiento (sin consultas N+1) | ✅ Preservado — Developer usó `pg_trgm` + índices de expresión |
| R-11 | Preservar criterios existentes (nombre, ID, etc.) | ✅ Preservado |

---

## Resumen Ejecutivo de Divergencias

```
📊 ANÁLISIS DE DIVERGENCIAS — 86e34kb9y

  AC Originales: 7 escenarios Gherkin + 11 requisitos + 9 items QA Matrix + 13 DoD items
  
  Divergencias encontradas: 11
    🟠 Altas: 3 (D-1, D-2, D-3) — Scope modificado/reducido/expandido
    🟡 Medias: 4 (D-4 a D-7) — Features adicionales implementados
    🟡 Técnicas: 4 (D-8 a D-11) — Decisiones de implementación relevantes
    ✅ Preservados: 7/7 AC Gherkin + 11/11 Requisitos

  ✅ CONCLUSIÓN: El ticket conserva su scope original pero se EXPANDIÓ
     con la migración del buscador global (Admin + Tenant), la migración
     de CompanyTable a shadcn/TanStack, y la resolución de dependencias
     complejas (CSS, teclado, iconos). Los AC originales son VÁLIDOS
     pero INSUFICIENTES — se necesitan TCs adicionales para las divergencias.
```

---

## Impacto en el Testing

### Lo que CAMBIA para QA:

1. **Scope de búsqueda expandido** — No solo emails de Company Users, también email de contacto de company
2. **Buscador global reescrito** — Tanto Admin como Tenant. El buscador anterior fue eliminado → regresión obligatoria
3. **CompanyTable migrada** — PrimeVue → shadcn/TanStack. Verificar paginación, sort, persistencia URL
4. **Aislamiento CSS** — `.modern-ui` acotado a subárbol. Verificar que vistas admin PrimeVue no se rompen
5. **Trade-off de teclado** — Home/End no mueven cursor en buscador. Comportamiento conocido, no bug
6. **2 repos afectados** — `gateway` (PHP: motor de búsqueda) + `gateway-ion` (Vue: UI completa)
7. **Dependencia de Pinia** — Buscador de tenant depende de auth store para resolver iconos por permisos

### Requerimiento excluido:

> ⚠️ El requerimiento 1 fue trasladado a ticket `86e1ryauq` por decisión de Marcel (PO). NO testear en este ticket.
