# QA FOUND ISSUE ESCALATION REPORT — IOND

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | PDF Templates |
| Path | Company > PDF Templates > New Template > Load Base PDF |
| Versión | gateway-ion v0.1.0 · flow_binaries v0.1.0 · gateway v2.0.0 |

## Título

**PDF Templates — Sin límite de tamaño para Load Base PDF, la vista crashea con archivos grandes**

## Description of the validated/replicated problem

Al crear un nuevo template PDF y utilizar la opción "Load Base PDF", no se implementa un límite máximo de tamaño de archivo. Al intentar subir un archivo PDF de gran tamaño (pesado), la vista del navegador crashea completamente. No existe validación previa al upload que informe al usuario sobre restricciones de tamaño.

## Steps to Reproduce

1. Company Login > Sidebar: PDF Templates
2. Presionar Button: "New Template"
3. En el modal de creación, seleccionar la opción "Load Base PDF"
4. Seleccionar un archivo PDF de gran tamaño (por ejemplo, >50MB)
5. Observar que la vista crashea (pestaña del navegador deja de responder o se cierra)

## Datos utilizados

- Rol: Company User con permiso `READ_PDF_TEMPLATE`
- Entorno: Staging
- Versión: v0.1.0
- Archivo PDF de gran tamaño (>50MB) como input

## Current Behavior

No existe validación de tamaño máximo para la carga de PDFs. Al intentar cargar un archivo grande, la vista crashea sin mensaje de error previo.

## Expected Behavior

1. Implementar un límite máximo de tamaño de archivo (configurable, por ejemplo 10-20MB)
2. Validar el tamaño del archivo ANTES de iniciar la carga
3. Si el archivo excede el límite, mostrar un mensaje de error descriptivo indicando el tamaño máximo permitido
4. Prevenir el crasheo de la vista bajo cualquier circunstancia

## Impacto

- Afecta a Company Users que cargan PDFs base para sus templates
- Puede causar pérdida de trabajo no guardado al crashear la vista
- Sin protección, un archivo malicioso/grande podría afectar la estabilidad del navegador

## Categorización

- 📊 Prioridad: **high** — causa crasheo completo de la vista, pérdida potencial de datos
- 🏷️ Tipo: **bug** — toda funcionalidad de carga de archivos debería tener validación de tamaño
