# Módulo: PDF Templates

> Módulo de templates PDF de Ionflow donde es posible customizar templates que son consumidos por sistemas externos.

## Información General

| Campo | Valor |
|-------|-------|
| Nombre interno | pdf-template |
| Criticidad | 🟠 Alto |
| Repos involucrados | `gateway-ion` (UI), `gateway` (API) |
| Última actualización | 2026-07-09 — v0.1.0 batch update |

---

## Rutas del Frontend (gateway-ion)

| Ruta | Vista | Componente | Permiso |
|------|-------|-----------|---------|
| `/pdf-templates` | Lista de templates | `views/tenant/pdf-template/list.vue` | `READ_PDF_TEMPLATE` |
| `/admin/templates` | Admin: templates globales | `views/admin/templates/TemplateList.vue` | Admin |

---

## Schema de BD (PostgreSQL — gateway)

- `2026_04_02_210000_create_pdf_templates_table.php`

---

## Reglas de Negocio

1. Los templates son consumidos por sistemas externos
2. Se debe asegurar su correcto funcionamiento ya que generan documentos para terceros
3. La generación se efectúa dentro del nodo en el canvas
4. Cada template pertenece a una company
5. Los templates se crean desde dos flujos: la vista de lista (`/pdf-templates`) y desde el **nodo IonPDF** dentro del canvas
6. Al crear desde el nodo IonPDF, el sistema llama a `onPdfTemplateSaved()` en `FlowEditor.vue`

---

## Lógica Backend (flow_binaries)

> Fuente: `../flow_binaries/docs/features/pdf-template/`

### Modelo de ejecución
- **Patrón de BD**: Tenant (`CompanySchema()`) para templates de company
- **Multi-tenant**: Sí — templates aislados por company
- **Nodo de flow**: Los flows generan PDFs via nodos especializados que renderizan templates

### Archivos centinela
| Repo | Archivo | Razón |
|------|---------|-------|
| flow_binaries | `docs/features/pdf-template/` | Documentación de la feature |
| gateway-ion | Vistas de PDF Templates | UI de gestión |

---

## Impacto Cruzado

### Módulos que PDF Templates afecta
| Módulo destino | Componente afectado | Tipo | Ejemplo |
|---------------|--------------------|-----------------|---------| 
| **Boards** | Flows que generan PDFs | Ejecución | Si un template se elimina, el nodo de PDF en el flow falla |
| **Nodes** | Nodo de generación | Ejecución | El nodo referencia el template por ID |

### Módulos que afectan a PDF Templates
| Módulo origen | Componente | Tipo | Ejemplo |
|--------------|------------|-----------------|---------| 
| **Auth** | Permisos | API | Solo users autorizados gestionan templates |

---

## Edge Cases Conocidos (v0.1.0)

1. **IONF-1087** — Al crear un template desde el nodo IonPDF **sin nodo conectado** (sin edge de entrada):
   - El template se crea correctamente en el servidor
   - Pero aparecen **dos toasts simultáneos**: uno de éxito (`"Template Created"`) y uno de error (`"Failed to save template"`)
   - El botón Save queda en **spinner permanente** porque `FlowEditor.vue` no llama a `pdfTemplateDialogRef.value?.resetSaving()` en el bloque `finally`
   - La excepción ocurre al intentar ejecutar `options?.setValue(savedId)` cuando `options` refleja un nodo sin conexión de entrada
   - **Pre-condición crítica**: el nodo IonPDF **no debe tener ningún nodo conectado** (sin edge)
   - **Nota**: El flujo desde la vista `list.vue` **sí** implementa el `resetSaving()` correctamente

---

## Historial de Actualizaciones

| Fecha | Tickets | Cambios | Actualizado por |
|-------|---------|---------|----------------|
| Initial | — | Creación inicial | QA Catalyst |
| 2026-06-07 | — | Backend Logic + Impacto Cruzado | QA Catalyst |
| 2026-07-09 | IONF-1087 | Edge case documentado: nodo IonPDF sin edge → Save spinner permanente, doble toast, resetSaving() faltante en FlowEditor.vue | QA Catalyst (batch v0.1.0) |
