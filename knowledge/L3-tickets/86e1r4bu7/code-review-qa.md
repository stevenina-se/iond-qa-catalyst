# Code Review QA — 86e1r4bu7 / IONF-1076 (Modo Deployment / Bug Hunting) — Ronda 2

## Resumen
- Repos revisados: `gateway-ion`, `gateway`, `flow_binaries`
- Commits analizados: 4 (Ronda 2: PR#25 gateway, PR#25 gateway-ion)
- Archivos modificados analizados: 24 (19 gateway-ion + 5 gateway)
- Hallazgos totales: 5
  - BUG confirmados: 0
  - RISK a verificar: 3 (🟠: 2, 🟡: 1)
  - SEC seguridad: 0
  - EDGE cases: 2 (🟡: 2)
- Módulos con impacto cruzado: Boards, PDF Templates
- TCs inyectados en test-matrix: 5 (TC-CR-001 a TC-CR-005)

## Commits Analizados

### gateway (PR#25 — Ronda 2 fix)
| Commit | Mensaje | Archivos |
|--------|---------|----------|
| `095f4288` | Remove unused has_nodes filter from Flow query in CompanyController | 1 |
| `bc9696d6` | Add has_nodes filter to flow index endpoint (luego removido) | 1 |

### gateway-ion (PR#25 — Ronda 2 fix)
| Commit | Mensaje | Archivos |
|--------|---------|----------|
| Merge `aa33f45f` | Fix de 16 OBS (búsqueda, validación, overflow, truncado, refresh, i18n, etc.) | 19 |

## Archivos Modificados (Ronda 2 fix — gateway-ion)

| Archivo | Cambios | Relevancia |
|---------|---------|-----------|
| `TemplateTableList.vue` | +60/-44 | Admin tabla: refresh button, truncado, overflow |
| `CategoryTagList.vue` | +39/-6 | Truncado tags, maxVisible, overflow tooltip |
| `TemplateStatsCards.vue` | +12/-12 | Estadísticas rediseñadas |
| `EditTemplateDrawer.vue` | +15/-15 | Campos no editables |
| `validateTemplateJson.ts` | +62/-20 | Validación JSON mejorada (OBS-02/03) |
| `validateTemplateJson.spec.ts` | +101/-25 | Tests de validación |
| `NewTemplateDialog.vue` | +18/-18 | Modal overflow fix |
| `SelectCompanyStep.vue` | +34/-34 | Búsqueda + paginación (OBS-01/11) |
| `SelectTemplateStep.vue` | +35/-35 | Alerta flows sin nodos (OBS-12) |
| `TemplateForm.vue` | +5 | Formulario mejorado |
| `TemplateList.vue` | +38/-18 | Tenant marketplace, categorías expandibles |
| `TemplatePreviewDrawer.vue` | +7/-7 | Preview |
| `TemplateCard.vue` | +6/-6 | Card truncado (OBS-09) |
| `TemplateInstallWizardDialog.vue` | +5/-5 | Wizard |
| `message.ts` (EN) | +26 | Claves i18n nuevas |
| `message.ts` (ES) | +28 | Claves i18n español (OBS-16) |
| `format.ts` | +5 | Helper truncateText |

---

## Sección 1 — BUGs Confirmados (BUG-CR-##)

> No se encontraron bugs confirmados reproducibles en esta revisión de código.
> Los fixes de la Ronda 2 abordan correctamente las 16 observaciones previas.

---

## Sección 2 — Riesgos a Verificar (RISK-CR-##)

### RISK-CR-001: Params como `ref()` en SelectCompanyStep — posible inconsistencia reactiva

```
RISK-CR-001:
  Categoría: RISK
  Severidad: 🟠 Alto
  Repo: gateway-ion
  Archivo: src/views/admin/templates/new-template/Steps/SelectCompanyStep.vue
  Línea: 34

  Descripción: En fetchCompanies(), los params del API call se envuelven en `ref()` innecesariamente. 
  Los params deberían ser un objeto plano ya que se pasan directamente al servicio HTTP.

  Evidencia:
    ```typescript
    const params = ref({     // línea 34 — ¿por qué ref()?
      page: page.value,
      per_page: PER_PAGE,
      order_by: 'name',
      order_direction: 'asc',
      full_text_search: searchInput.value || undefined,
    });
    ```

  Comportamiento Esperado:
    Los params deberían ser un objeto plano (const params = { ... }) para pasar al servicio HTTP.

  Comportamiento Actual:
    Los params se crean como un Ref reactivo. El servicio CompanyService.searchCompanies()
    recibe un Ref en lugar de un objeto plano. Si el servicio llama `params.page` en lugar de 
    `params.value.page`, los valores serán undefined.
    NOTA: Esto podría funcionar si el servicio HTTP (axios) deserializa Refs automáticamente, 
    pero es un patrón frágil.

  Precondiciones:
    User Role: Admin
    User State: Logged in
    
  Pasos de Reproducción:
    1) Admin Login
    2) Templates > Create template
    3) Seleccionar modo "From Company"
    4) Verificar que el buscador de compañías funciona correctamente
    5) Buscar una compañía por nombre
    6) Verificar que los resultados son correctos y la paginación funciona

  Impacto: Si el servicio no maneja Refs correctamente, la búsqueda podría no enviar los parámetros.

  Recomendación: Inyectar como TC — verificar que la búsqueda y paginación funcionan en testing.
```

### RISK-CR-002: Delete template no disponible para templates con company_id

```
RISK-CR-002:
  Categoría: RISK
  Severidad: 🟠 Alto
  Repo: gateway-ion
  Archivo: src/views/admin/templates/TemplateTableList.vue
  Línea: 221-228

  Descripción: La función getRowMenuItems() solo muestra la opción "Delete" cuando template.company_id 
  es falsy (null/0). Los templates sincronizados desde compañías (community) no pueden eliminarse desde 
  la UI admin.

  Evidencia:
    ```typescript
    function getRowMenuItems(template: Template) {
      const items = [
        { label: t('message.tplEdit'), icon: 'pi pi-pencil', command: () => handleEdit(template) },
      ];
      if (!template.company_id) {    // línea 221 — solo admin-created
        items.push(
          { separator: true },
          { label: t('message.tplDelete'), ... },
        );
      }
      return items;
    }
    ```

  Comportamiento Esperado:
    Según los AC, el admin debería poder gestionar (CRUD) todos los templates.
    Es posible que sea intencional restringir delete a solo templates admin-created.

  Comportamiento Actual:
    Templates community (con company_id) solo tienen opción "Edit", no "Delete".
    El ToggleSwitch de is_active también está disabled para estos templates (línea 468).

  Precondiciones:
    User Role: Admin
    Existing Data: Al menos un template sincronizado desde una company (community template)

  Pasos de Reproducción:
    1) Admin Login
    2) Templates > localizar un template con source "Company"
    3) Click en menú de contexto (3 puntos)
    4) Verificar opciones disponibles
    5) Verificar si el toggle de activo funciona

  Impacto: Si un template community es problemático, el admin no puede eliminarlo ni desactivarlo.

  Recomendación: Verificar en testing si es comportamiento intencional. Si no, es un gap de AC.
```

### RISK-CR-003: relativeTime() no usa i18n — textos hardcoded en inglés

```
RISK-CR-003:
  Categoría: RISK
  Severidad: 🟡 Medio
  Repo: gateway-ion
  Archivo: src/views/admin/templates/helpers/format.ts
  Línea: 11-23

  Descripción: La función relativeTime() tiene strings hardcoded en inglés ("Today", "Yesterday", 
  "d ago", "w ago", etc.) sin usar el sistema i18n. Dado que OBS-16 reportaba labels desfasados 
  en español, si esta función se usa en algún lugar visible, mostrará textos en inglés independientemente
  del idioma seleccionado.

  Evidencia:
    ```typescript
    export function relativeTime(dateStr: string): string {
      // ...
      if (diffDays === 0) return 'Today';        // hardcoded
      if (diffDays === 1) return 'Yesterday';     // hardcoded
      if (diffDays < 7) return `${diffDays}d ago`; // hardcoded
      // ...
    }
    ```

  Comportamiento Esperado:
    Los textos de tiempo relativo deberían usar claves i18n para traducirse al idioma del usuario.

  Comportamiento Actual:
    Textos siempre en inglés. Sin embargo, revisando el código de la tabla admin 
    (TemplateTableList.vue L490), usa `applyFormat()` para dates, no `relativeTime()`. 
    Esta función podría NO estar siendo usada actualmente.

  Precondiciones:
    User State: Idioma configurado en español

  Pasos de Reproducción:
    1) Configurar idioma en español
    2) Admin > Templates
    3) Verificar si algún campo de fecha muestra "Today"/"Yesterday"/"d ago"

  Impacto: Bajo — la función podría no estar en uso actualmente, pero es un riesgo si se usa en el futuro.

  Recomendación: Verificar en testing visual si hay textos en inglés con idioma español.
```

---

## Sección 3 — Seguridad (SEC-CR-##)

> No se encontraron hallazgos de seguridad nuevos en la Ronda 2.
> El fix de SQL injection en orderby (`09a454da`) fue aplicado en PR#15 (Ronda 1).
> La whitelist de campos ordenables (`templateOrderableFields` en template_controller.go L85-92) 
> previene SQL injection correctamente.

---

## Sección 4 — Edge Cases (EDGE-CR-##)

### EDGE-CR-001: ToggleSwitch activa/inactiva — optimistic update sin confirm

```
EDGE-CR-001:
  Categoría: EDGE
  Severidad: 🟡 Medio
  Repo: gateway-ion
  Archivo: src/views/admin/templates/TemplateTableList.vue
  Línea: 265-277

  Descripción: El toggle de activo/inactivo en la tabla admin hace un optimistic update sin 
  diálogo de confirmación. Si el toggle falla (error de red), el estado visual se revierte 
  silenciosamente sin toast de error visible (el catch sí tiene toast, pero el revert es antes).

  Evidencia:
    ```typescript
    function onToggleActive(template: Template, val: boolean) {
      const prev = template.is_active;
      template.is_active = val;       // optimistic update
      TemplatesService.update(...)
        .then(res => { patchTemplateRow(...) })
        .catch(err => {
          template.is_active = prev;  // revert
          toast.add({ severity: 'error', ... });
        });
    }
    ```

  Comportamiento Esperado:
    El toggle con revert en catch es un patrón válido. Sin embargo, al revertir template.is_active 
    directamente (mutación del prop reactivo), la referencia muta in-place lo que puede causar 
    que el DataTable no re-renderice correctamente.

  Precondiciones:
    User Role: Admin
    Network: Inestable o con latencia alta

  Pasos de Reproducción:
    1) Admin > Templates
    2) Toggle rápidamente un template de activo a inactivo y viceversa
    3) Si hay error de red: verificar que el toggle revierte visualmente
    4) Verificar que la tabla no queda en estado inconsistente

  Impacto: Bajo en condiciones normales, potencial inconsistencia visual con red inestable.
```

### EDGE-CR-002: Unique constraint podría fallar silenciosamente al sincronizar community template

```
EDGE-CR-002:
  Categoría: EDGE
  Severidad: 🟡 Medio
  Repo: gateway
  Archivo: database/migrations/2026_06_16_163200_create_templates_table.php
  Línea: 30

  Descripción: La restricción unique `(company_id, type, original_id)` permite que un template 
  con company_id=NULL pueda tener múltiples registros con el mismo original_id y type (ya que 
  NULL != NULL en PostgreSQL). Templates admin-created (company_id=NULL) no están protegidos 
  por esta restricción.

  Evidencia:
    ```php
    $table->unique(['company_id', 'type', 'original_id'], 'templates_company_type_original_unique');
    ```

  Comportamiento Esperado:
    El constraint impide duplicación de templates sincronizados desde compañías.

  Comportamiento Actual:
    El constraint funciona correctamente para community templates (company_id NOT NULL).
    Para admin-created (company_id NULL), la restricción no aplica (comportamiento estándar de SQL).
    Esto es probablemente intencional ya que admin-created templates no tienen original_id.

  Pasos de Reproducción:
    1) Crear template admin con mismo título dos veces
    2) Verificar si el sistema permite duplicados o tiene otra validación

  Impacto: Bajo — el frontend maneja 409 Conflict para duplicados por título.
```

---

## Follow-the-Flow Maps

### Flow 1: Instalación de Template (Tenant)
```
1. CALLERS: TemplateList.vue > handleUseTemplate > useTemplateInstaller.installTemplate()
2. PERSISTENCIA: useTemplateInstaller clona PDFs + crea flow en cuenta del tenant
3. CONSUMIDORES: El flow clonado aparece en Workflows del tenant
4. RENDER: Toast de confirmación + flow editable en lista
5. ERROR PATH: Catch en installTemplate muestra toast de error
6. OPERACIÓN OPUESTA: No hay "uninstall" — el usuario debe eliminar el flow manualmente
```

### Flow 2: CRUD Admin Templates
```
1. CALLERS: TemplateTableList > handleCreate/handleEdit/handleDelete
2. PERSISTENCIA: TemplatesService > flow_binaries backend > PostgreSQL tabla templates
3. CONSUMIDORES: Marketplace tenant lee templates activos
4. RENDER: Tabla admin con paginación, filtros, categorías
5. ERROR PATH: Toast de error con mensajes i18n
6. OPERACIÓN OPUESTA: Create ↔ Delete simétrico (con confirm dialog)
```

---

## Impacto Cruzado

| Módulo Impactado | Componente Afectado | Riesgo | Verificación Necesaria |
|---|---|---|---|
| Boards | Lista de workflows | 🟡 Bajo | Los templates no deben aparecer como boards propios hasta instalarlos |
| PDF Templates | Clonación de PDFs | 🟠 Alto | Al instalar template con PDFs, los IDs deben remapearse correctamente |
| Auth/Permisos | Rutas admin | 🟡 Bajo | Solo admin debe acceder al CRUD de templates |

---

## Observaciones Positivas del Código (Ronda 2)

1. **Validación JSON robusta**: `validateTemplateJson.ts` implementa detección de tipo (flow/pdf), validación de estructura, nodos no-ejecutables y campos requeridos. Tests comprehensivos.
2. **Truncado consistente**: `truncateText()` + `title` tooltip aplicado en tabla, cards y modales.
3. **AbortController**: Implementado correctamente en fetches con cleanup en `onUnmounted`.
4. **Búsqueda con paginación**: SelectCompanyStep ahora tiene búsqueda + paginator (fix OBS-01/11).
5. **CategoryTagList con maxVisible**: Overflow de tags manejado con `+N` y tooltip (fix OBS-13/14/15).
6. **Refresh button**: Agregado en paginatorstart de DataTable (fix OBS-10).
7. **i18n**: 207 claves completas EN/ES.

---

## TCs Inyectados en Test Matrix

| TC ID | Categoría | Origen | Caso de Test | Severidad |
|-------|-----------|--------|-------------|-----------|
| TC-CR-001 | RISK | RISK-CR-001 | Verificar que búsqueda + paginación de compañías funciona (params como ref) | 🟠 |
| TC-CR-002 | RISK | RISK-CR-002 | Verificar opciones de gestión para templates community (delete/toggle bloqueados) | 🟠 |
| TC-CR-003 | RISK | RISK-CR-003 | Verificar que no hay textos hardcoded en inglés con idioma español | 🟡 |
| TC-CR-004 | EDGE | EDGE-CR-001 | Toggle rápido activo/inactivo con error de red — revert visual correcto | 🟡 |
| TC-CR-005 | EDGE | EDGE-CR-002 | Crear dos templates admin con mismo título — verificar manejo de duplicados | 🟡 |
