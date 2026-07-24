# Release Notes — IONFLOW v0.1.0

> Fecha: Julio 2026

---

## ¡Bienvenidos a IONFLOW! 🚀

Nos emociona presentar la primera versión de **IONFLOW**, la plataforma de automatización de flujos de trabajo de nueva generación. Esta versión incluye más de **125 nuevas funcionalidades**, **32 correcciones** y **6 mejoras** para que puedas empezar a automatizar tus procesos de negocio hoy.

---

## Highlights

1. 🔧 **Automatización Visual de Flujos** — Crea flujos de trabajo visualmente con nuestro editor de Boards: arrastra, conecta y ejecuta nodos en minutos.

2. 🔗 **Integraciones Pre-construidas** — Conecta Shopify, Shipedge, eBay, y más con Grapps listos para usar desde el Marketplace.

3. 🤖 **Asistente de IA** — FlowPilot te ayuda a construir flujos automáticamente. IonMind genera configuraciones inteligentes para tus integraciones.

4. 📄 **Plantillas PDF** — Diseña y genera documentos PDF personalizados directamente desde tus flujos.

5. 🔐 **Login Seguro con SSO** — Accede a la plataforma de forma segura con autenticación SSO vía Keycloak.

---

## 🚀 Nuevas Funcionalidades

### 🔧 Automatización de Flujos (Boards)

- **Ahora puedes** crear flujos de trabajo visuales completos con más de 15 tipos de nodos disponibles (Switch, Timer, Code, Mapper, Transformer, Form, y más).
- **Ahora puedes** usar el nodo Switch dinámico para crear lógica condicional con múltiples rutas de salida.
- **Ahora puedes** programar pausas en tus flujos con el nodo Timer.
- **Ahora puedes** escribir código personalizado dentro de un flujo con el nodo Code.
- **Ahora puedes** llamar a un flujo dentro de otro flujo (sub-flows) para reutilizar lógica.
- **Ahora puedes** versionar tus flujos con Git integrado: guarda versiones, compara cambios y restaura versiones anteriores.
- **Ahora puedes** documentar tus flujos directamente en el editor con paneles de documentación inline.
- **Ahora puedes** ver el progreso de ejecución en tiempo real con logs detallados.
- **Ahora puedes** navegar fácilmente tu flujo con el mini mapa interactivo y controles de zoom.
- **Ahora puedes** agregar nodos rápidamente con doble clic en el canvas.
- **Ahora puedes** ver previews de tus Boards y Templates directamente en las tablas.
- **Ahora puedes** importar y exportar flujos entre cuentas.

### 🔗 Integraciones (Grapps)

- **Ahora puedes** instalar integraciones pre-construidas desde el Marketplace de Grapps.
- **Ahora puedes** crear tus propias integraciones personalizadas (Grapps).
- **Ahora puedes** configurar Webhooks para recibir eventos de terceros en tus flujos.
- **Ahora puedes** programar ejecuciones automáticas de Grapps con Schedules.
- **Ahora puedes** conectar Shopify con Shelfter, eBay con Omnio, y más sin escribir código.
- **Ahora puedes** ver logs de errores en la interfaz de Grapps para diagnosticar problemas.

### 🤖 Asistente de IA

- **Ahora puedes** usar FlowPilot para generar flujos automáticamente a partir de instrucciones en lenguaje natural.
- **Ahora puedes** usar IonMind para generar configuraciones inteligentes para conectores y mapeos.
- **Ahora puedes** elegir entre diferentes tiers de servicio de IA (económico, normal, premium).
- **Ahora puedes** conectar con OpenAI, Gemini y OpenRouter desde tus flujos con el nodo LLM.

### 📄 Plantillas PDF

- **Ahora puedes** crear y editar plantillas PDF directamente en IONFLOW.
- **Ahora puedes** generar y descargar documentos PDF desde tus flujos.
- **Ahora puedes** usar el editor visual de plantillas con menú lateral de herramientas.

### 🔗 Conexiones

- **Ahora puedes** crear conexiones manuales o con el Wizard inteligente que auto-completa configuraciones.
- **Ahora puedes** ver el consumo de tus conectores con alertas de uso.
- **Ahora puedes** exponer vistas públicas para aplicaciones de terceros.

### 👥 Cuentas y Usuarios

- **Ahora puedes** tener múltiples usuarios por compañía con roles diferenciados.
- **Ahora puedes** monitorear el consumo por usuario para gestionar suscripciones.
- **Ahora puedes** configurar tu compañía desde una vista dedicada.

### 🌐 Experiencia General

- **Ahora puedes** buscar en toda la plataforma con la barra de búsqueda global.
- **Ahora puedes** ver modales de confirmación antes de acciones destructivas.
- **Ahora puedes** cambiar el idioma de la plataforma.

---

## 🐛 Correcciones

- **Corregimos** problemas de inicio de sesión con Keycloak en diferentes dominios.
- **Corregimos** errores de recursividad al conectar nodos en cadena.
- **Corregimos** el problema donde el nodo PDF no habilitaba el mapeo de datos correctamente.
- **Corregimos** errores al migrar flujos a nivel global.
- **Corregimos** el problema donde la URL no se actualizaba al crear un Board nuevo.
- **Corregimos** errores al desactivar webhooks personalizados.
- **Corregimos** problemas al cambiar el email de una cuenta.
- **Corregimos** el error que impedía crear Boards en cuentas nuevas.
- **Corregimos** doble scroll y desborde de componentes en el canvas.
- **Corregimos** problemas de permisos de usuario inicial.

---

## ⚡ Mejoras

- **Mejoramos** la edición de nombres en la vista de Conexiones.
- **Mejoramos** las confirmaciones de cambios no guardados en todas las vistas.
- **Mejoramos** la estructura de respuesta del nodo Request (ahora incluye headers, body y status).

---

## 📋 Información

| Campo | Valor |
|-------|-------|
| Versión | `v0.1.0` |
| Fecha | Julio 2026 |
| Soporte | Contactar al equipo de soporte |
