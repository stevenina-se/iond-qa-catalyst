# Release Notes — v0.1.0 (Internal)

> Generado por `skills/release/notes`
> Fecha: 8 de julio de 2026
> Tipo: `internal`
> Fuente de datos: `matched_tickets1.csv` (187 tickets) + ClickUp MCP (muestra enriquecida)

---

## Resumen Ejecutivo

La versión **v0.1.0** es el **primer release a producción de IONFLOW** — la plataforma de automatización de flujos de trabajo de nueva generación. Representa el resultado de más de 15 sprints de desarrollo acumulado, consolidando el motor de flujos, el sistema de integraciones (Grapps), la autenticación SSO, las plantillas PDF, y todo el ecosistema de herramientas IA (IonMind, StageMind, FlowPilot).

**Estadísticas:** 125 nuevas funcionalidades · 32 correcciones · 6 mejoras · 5 refactors · 7 infra · 12 tasks

**Distribución por área:**
Boards/Flujos (82) · AI Services (18) · Integrations/Grapps (14) · UI/UX (10) · Connections (7) · Gateway (7) · Accounts (7) · Auth (5) · Webhooks (3) · PDF Templates (3) · Exec History (3) · Data Store (2)

**Prioridad:** 16 urgent · 74 high · 67 normal · 13 low · 17 sin prioridad

---

## Highlights

1. **Motor de Flujos Completo** — Editor visual de Boards con nodos Switch dinámico, Timer, Code, Aggregate, Transformer, Mapper, y 15+ tipos de nodos. Incluye versionamiento Git, importación/exportación, documentación inline, y ejecución con logs detallados. (82 tickets)

2. **Ecosistema de Integraciones (Grapps)** — Marketplace de Grapps con endpoints de instalación API-First, Dynamic Wizards, Webhooks, Schedules, y sistema de logs para usuarios finales. Integraciones pre-construidas: Shopify↔Shelfter, Rithum↔Shipedge, eBay↔Omnio. (14+ tickets)

3. **Autenticación SSO Refactorizada** — Refactorización completa de Keycloak para corregir problemas de inicio de sesión, soporte multi-dominio, refresh token en flujos, y método de autenticación por cookies. (5 tickets urgentes/high)

4. **Suite de IA** — IonMind v1.8, StageMind v3, FlowPilot con motor de reconstrucción, Nodo LLM (OpenAI/Gemini/OpenRouter), Automapper, tiers de servicio, y sandbox de pruebas. (18 tickets)

5. **PDF Templates (IonPDF)** — Fork de pdfme integrado, creación de templates desde canvas, descarga de PDFs generados, y menú lateral de edición. (3 tickets)

---

## 🚀 Nuevas Funcionalidades

### 📂 Boards / Flujos (52 features)

**Motor de nodos:**
- **IONF-227** — Nodo Switch dinámico con modo Expression y múltiples outputs `(gateway-ion, flow_binaries)`
- **IONF-266** — Nodo Timer para pausas configurables en flujos
- **IONF-328** — Llamar a un flow dentro de otro flow (sub-flows)
- **IONF-320** — Expression Language en mappers con casteo de tipos
- **IONF-843** — Paneles para documentar flows inline
- **IONF-844** — Observabilidad en líneas de conexión entre nodos
- **IONF-848** — Menú contextual de nodos por doble clic + reorganización de categorías
- **IONF-919** — Nodo base de integración LLM (OpenAI, Gemini, OpenRouter)
- **IONF-935** — Nodo Aggregate para consolidación de datos
- **IONF-939** — Nodo Code para custom scripting
- **IONF-940** — Funcionalidad de Automapper
- **IONF-694** — Esquema de salida absoluto vía setOutSpec() en Mapper
- **IONF-964** — Funcionalidad ancla para mapper
- **IONF-313** — Nested elements y Advance fields en nodo Form
- **IONF-551** — Bindeo para Dropdowns y binarios en nodo Form
- **IONF-553** — Input tipo Date para fechas
- **IONF-552** — Nodos faltantes para Data Storage

**Versionamiento y gestión:**
- **IONF-419** — Motor de versionamiento de flujos basado en Git
- **IONF-482** — Restaurar un flow mediante Git
- **IONF-530** — Mejora de importación de flows
- **IONF-999** — Descripciones automáticas de boards
- **IONF-971** — Previews de boards y templates en tablas

**Canvas y UI:**
- **IONF-970** — Mini mapa interactivo y controles de zoom
- **IONF-644** — Refactor de menú de nodos a WebComponents para FlowCopilot
- **IONF-798** — Más detalles en logs de ejecución
- **IONF-950** — Integración del agente FlowPilot con nodo Code

### 📂 Integrations / Grapps (14 features)

- **IONF-103** — Unificación de endpoints para creación de Grapps `(gateway-ion, gateway, flow_binaries)`
- **IONF-996** — Endpoints de Instalación de Grapps (API-First)
- **IONF-997** — Dynamic Wizards for Grapps
- **IONF-917** — Marketplace de Grapps y Template Maker desde Figma
- **IONF-968** — Compañías pueden crear sus propios Grapps
- **IONF-911** — Schedules de Grapps, configuración desde IONFLOW y Gateway
- **IONF-825** — Logs en la interface de Grapps para errores de usuarios
- **IONF-548** — Check Updates en Grapps del Gateway
- **IONF-260** — Flow Shopify↔Shelfter (BinLogic)
- **IONF-262** — Integración SQUARE UP ↔ SHELFTER
- **IONF-386** — Integración Rithum (Channel Advisor) ↔ Shipedge
- **IONF-532** — Nodos para conectar con Omnio
- **IONF-538** — Board con flujos para atributos dinámicos de eBay
- **IONF-541** — Integración profunda con SHIPEDGE

### 📂 AI Services (18 features)

- **IONF-483** — IonMind v1.3
- **IONF-504** — IonMind v1.2
- **IONF-603** — IonMind v1.4
- **IONF-638** — IonMind v1.5
- **IONF-721** — IonMind v1.6
- **IONF-790** — IonMind v1.7
- **IONF-877** — IonMind v1.8
- **IONF-976** — Tiers de Servicio (Cheap/Normal/Premium) con mix de modelos
- **IONF-672** — StageMind v1
- **IONF-722** — StageMind v2
- **IONF-793** — StageMind v3
- **IONF-927** — StageMind para Catalog Builder v1.3.5
- **IONF-859** — FlowCopilot Fase 1: herramienta current_execution y motor de reconstrucción
- **IONF-954** — Desarrollo e integración de Skills en el agente
- **IONF-714** — MCPs Fase 1: CRUD Batch de nodos y lectura de estado
- **IONF-719** — MCPs y FlowPilot Fase 2: Skills, Templates y Drafts
- **IONF-1012** — Sandbox para probar funcionalidades de IonMind
- **IONF-645** — IonMind: estandarizar respuesta JSON según Ultimate API Mapping Guide

### 📂 Connections (7 features)

- **IONF-116** — Crear app de forma manual
- **IONF-128** — Formulario de instalación de servicio
- **IONF-110** — Exponer vistas públicas con aplicaciones de terceros
- **IONF-779** — Wizard Create Connector: Auto-fill desde IonMind, persistencia de estado, autenticación
- **IONF-650** — Sistema de rastreo de uso de App Connectors y alertas por usuario
- **IONF-591** — Motor para descargar integración a un Cart (Custom App) desde Admin
- **IONF-1002** — Hardcoding de plataformas por BD

### 📂 Auth / SSO (3 features)

- **IONF-114** — Crear o validar cuenta en IonFlow con Keycloak
- **IONF-362** — Configurar flujo de Login SSO funcional como método principal
- **IONF-556** — Método de autenticación basado en cookies

### 📂 Accounts / Users (5 features)

- **IONF-655** — Más de un usuario por compañía y roles
- **IONF-879** — Monitoreo de consumo por usuario/compañía para pricing
- **IONF-506** — Vista de configuración de Company
- **IONF-492** — Petición de renovación por correo
- **IONF-493** — Botón de reauthentication

### 📂 PDF Templates (3 features)

- **IONF-1003** — Fork de pdfme integrado en IONFLOW
- **IONF-958** — Menú lateral en ventana de edición de templates
- **IONF-820** — Nodo exportación PDF mediante CDN y microservicio

### 📂 UI/UX General (8 features)

- **IONF-226** — Migración de componentes a TailwindCSS
- **IONF-281** — Modales de confirmación para acciones de eliminación
- **IONF-510** — Unificación del menú superior en aplicaciones web
- **IONF-444** — Barra de búsqueda global (Global Search)
- **IONF-657** — Botón de idioma con i18n
- **IONF-590** — Renombrar operaciones de versionado a terminología simplificada
- **IONF-587** — Nuevo Wizard interactivo con soporte de versiones
- **IONF-164** — Mejoras de estilo en webcomponents

---

## 🐛 Correcciones (32 bugs)

### 📂 Boards / Flujos

- **IONF-406** — Fix: Error de recursividad en nodos entrelazados (urgent)
- **IONF-376** — Fix: problema de casteo en expression language con sanitización
- **IONF-404** — Fix: problema con acumulador en transformer, salida collection
- **IONF-416** — Default para booleans en nodo Transformer
- **IONF-414** — Estructura de tipo Array no añade items
- **IONF-509** — Doble scroll en nodos del lienzo y desborde de componentes
- **IONF-511** — Preview de Transformer conserva info de otros Transformers
- **IONF-512** — Error en reinicio de secuencia de IDs de nodos
- **IONF-516** — Nodo Transformer no emite salida al ejecutar
- **IONF-1013** — Nodo Output genera array de arrays
- **IONF-522** — Sobrecarga en vista de git-diff de flows
- **IONF-900** — Bug al actualizar label de un nodo
- **IONF-901** — Bug no permite mapeo de campos select y boolean
- **IONF-899** — URL no se actualiza al crear Board, se pierde al refrescar
- **IONF-1063** — Problema con campo select en nodos al hacer doble click
- **IONF-1123** — Nodo PDF no habilita mapeo hasta abrir y guardar modal (urgent)
- **IONF-1108** — Migración de flow a global retorna error 500 (urgent)
- **IONF-1143** — FlowPilot no reconoce nodo PDF Template

### 📂 Auth / SSO

- **IONF-543** — Problema con login Keycloak en diferentes dominios (urgent)
- **IONF-554** — Fix Refresh token en flows
- **IONF-1074** — Refactorizar Keycloak para corregir problemas de inicio de sesión

### 📂 Connections

- **IONF-141** — Errores de Basic Auth en solicitudes GET
- **IONF-327** — Error en creación de módulos con mismo nombre de diferente conexión
- **IONF-517** — Errores al configurar Custom App
- **IONF-368** — Error en pantalla de Integrations

### 📂 Webhooks

- **IONF-786** — Funcionalidad webhook con content-type y procesamiento
- **IONF-1145** — No se pueden desactivar webhooks custom (urgent)

### 📂 Accounts

- **IONF-763** — Usuario inicial sin todos los permisos asignados
- **IONF-764** — Inconsistencias UI al modificar permisos
- **IONF-1147** — Cambiar email de cuenta genera error que rompe la cuenta (urgent)
- **IONF-1144** — No se puede crear Board después de crear cuenta nueva (urgent)

### 📂 PDF Templates

- **IONF-1087** — Animación del botón Save al crear template no finaliza y muestra error

### 📂 Data Store

- **IONF-159** — Modal de creación conserva info de edición anterior (urgent)
- **IONF-162** — Solapamiento de datos en mapeo del nodo Data Store (urgent)

---

## ⚡ Mejoras (6)

- **IONF-142** — Refactorización de connections con integraciones
- **IONF-146** — Edición de nombres en vista de Connections
- **IONF-147** — Confirmación de cambios no guardados en vistas
- **IONF-643** — Soportar extraer Collection en output del mapper
- **IONF-656** — Nodo Request retorna estructura entera (headers, body, status)
- **IONF-724** — Mejorar UI de documentación de developers

---

## 🔧 Cambios Internos

### Refactors (5)

- **IONF-379** — Refactorizar motor de ejecución de flows
- **IONF-380** — Motor de nodos en Golang (developer apps y companies)
- **IONF-498** — Actualizar versión 1.2.x de gateway a IONFLOW
- **IONF-393** — Aplicar nueva terminología en UI y código
- **IONF-507** — Seeders de aplicaciones desplegadas en dev3

### Infra (7)

- **IONF-768** — Arreglar warnings de SonarQube `(flow_binaries)`
- **IONF-1042** — Warnings de SonarQube para gateway-ion
- **IONF-709** — Revisión y corrección de tests unitarios de Webcomponentes
- **IONF-713** — Refactorizar y completar tests unitarios de Gateway
- **IONF-514** — Arreglar tests de binarios (feature backend)
- **IONF-309** — Revisión Alpha de webcomponentes
- **IONF-723** — Solucionar problema de compilación de webcomponentes

### Tasks (12)

- **IONF-267** — Research: LangExtract (Google) para texto no estructurado
- **IONF-279** — Probar URL Context de Google con Gemini 2.5 Flash
- **IONF-370** — Investigación extracción de URLs con GPT 5 Mini
- **IONF-456** — Investigación tokens de LLMs
- **IONF-537** — Análisis función mapper inteligente
- **IONF-407** — Tabla comparativa IONFLOW vs competencia
- **IONF-415** — Video demostrativo de Grapps
- **IONF-447** — Documentación inter-repositorio automatizada
- **IONF-378** — Actualizar documentación técnica
- **IONF-869** — Documentar endpoints internos de IonMind v1.7
- **IONF-909** — Reunión técnica: diseño de microservicio LLM Gateway
- **IONF-725** — Motor de pruebas automáticas para gateway con IA

---

## 📋 Información del Release

| Campo | Valor |
|-------|-------|
| Versión | `v0.1.0` |
| Fecha de deploy | Julio 2026 |
| Entorno | `dev-app.ionflow.io` → producción |
| Total tickets | 187 |
| Repos | gateway-ion, flow_binaries, gateway, webcomponents-flow |

---

## ⚠️ Breaking Changes

Dado que esta es la **primera release a producción**, no hay breaking changes respecto a una versión anterior. Todos los cambios son nuevos.

> **Nota**: Los tickets con status `ready to merge` (23), `code review` (3), `qa testing` (2), `dev in progress` (1), `sprint intake` (1), y `fortification` (1) aún no están completados al momento de generar estas release notes. Se incluyen porque están en el scope de la v0.1.0.
