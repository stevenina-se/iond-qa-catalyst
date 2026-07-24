# Release Notes — IONFLOW v0.1.1

> Fecha: Julio 2026

---

## Novedades de esta versión 🎉

Esta actualización se enfoca en **estabilidad, precisión y nuevas capacidades de integración**. Corregimos errores importantes reportados por nuestros usuarios y agregamos funcionalidades que amplían el ecosistema de integraciones de IONFLOW.

**En esta versión:** 3 nuevas funcionalidades · 8 correcciones · 2 mejoras

---

## Highlights

1. 🔗 **Sincronización de productos con Etsy y WooCommerce** — Exporta tus productos directamente hacia Etsy y WooCommerce desde IONFLOW, con procesamiento inteligente en lotes y reportes detallados de resultados.

2. 🤖 **Monitoreo de consumo de IA** — Ahora puedes ver exactamente cuántos tokens consume tu asistente Flow Pilot, con detalle por sesión y costos estimados.

3. 🛡️ **Confirmación antes de costos** — Cuando solicites documentación técnica de una plataforma nueva, se te mostrará el costo aproximado antes de proceder, para que tengas control total sobre tus gastos.

4. 🔧 **Scheduler más confiable** — Las tareas programadas ahora se ejecutan en la hora exacta configurada y reportan su estado correctamente.

---

## 🚀 Nuevas Funcionalidades

### 🔗 Integraciones

- **Ahora puedes** sincronizar productos hacia Etsy y WooCommerce desde tus flujos. Envía un catálogo de productos y recibe un reporte detallado del resultado por cada producto (exportado, error, SKU duplicado, etc.).

- **Ahora puedes** ver una confirmación clara del costo antes de solicitar la documentación técnica de una plataforma nueva. Si la documentación ya fue procesada anteriormente, no se cobra de nuevo.

### 🤖 Asistente de IA

- **Ahora puedes** monitorear el consumo de tokens de Flow Pilot por sesión. Cada interacción registra los tokens utilizados (solicitud y respuesta) junto con el costo estimado, para que tengas visibilidad completa de tu uso de IA.

---

## 🐛 Correcciones

- **Corregimos** un error en el nodo Simple Decision que comparaba números como texto. Por ejemplo, antes `2` se consideraba mayor que `12` (incorrecto). Ahora las comparaciones numéricas funcionan correctamente, y puedes elegir el tipo de dato (Número, Texto, Booleano) para cada condición.

- **Corregimos** un problema en las tareas programadas (Scheduler) donde el flujo se ejecutaba correctamente pero el estado final aparecía como "error" en lugar de "completado".

- **Corregimos** el desfase de +4 horas que aparecía en los logs de ejecución de Company Schedules. Ahora los timestamps muestran la hora real de ejecución.

- **Corregimos** un error donde las tareas programadas se disparaban en un horario incorrecto debido a una conversión de zona horaria incorrecta. Ahora se respeta la hora local configurada.

- **Corregimos** un problema en las Plantillas PDF donde los cambios se perdían silenciosamente al presionar Escape o cerrar la ventana de edición. Ahora se muestra una confirmación antes de descartar tus cambios.

- **Corregimos** un error en las Plantillas PDF donde cargar un archivo PDF base demasiado grande hacía que la vista dejara de responder. Ahora se valida el tamaño del archivo y se muestra un mensaje claro si excede el límite.

- **Corregimos** un problema en las Conexiones donde reautorizar una conexión por API Key creaba una conexión duplicada en lugar de actualizar la existente. Ahora la conexión se actualiza correctamente sin duplicados.

- **Corregimos** una alerta falsa de "cambios sin guardar" que aparecía en los Boards al re-ingresar a la vista después de un commit exitoso.

---

## ⚡ Mejoras

- **Mejoramos** la experiencia visual del dashboard con ajustes de interfaz en el modo Dualtrack.

- **Mejoramos** el flujo de registro de compañía con un formulario simplificado y una redirección más clara después del registro.

- **Mejoramos** los webhooks públicos para que ahora sean accesibles desde cualquier origen sin restricciones, facilitando la integración con servicios externos.

---

## 📋 Información

| Campo | Valor |
|-------|-------|
| Versión | `v0.1.1` |
| Fecha | Julio 2026 |
| Soporte | Contactar al equipo de soporte |
