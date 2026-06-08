# Reglas de Negocio — Ionflow

> Ionflow es un SaaS de automatización de procesos mediante conexión de nodos, orientado a e-commerce.

## Qué es Ionflow

Ionflow permite a sus usuarios automatizar procesos repetitivos del e-commerce conectando **nodos** en un canvas visual, similar a plataformas como Make.com, Zapier o n8n.

## Diferencial Competitivo

1. **Extrema simplicidad** — Elimina la complejidad de configuración de nodos
2. **Sin conocimientos técnicos** — Cualquier persona puede automatizar sus procesos
3. **Orientado a e-commerce** — Los flujos más comunes del e-commerce vienen pre-configurados o son fáciles de armar

## Conceptos Core del Negocio

### Flows (Flujos)
- Un **flow** es una secuencia de nodos conectados que automatizan un proceso
- Los flows tienen un trigger (inicio) y una o más acciones
- Un flow puede estar activo (ejecutándose) o inactivo (draft/paused)

### Nodes (Nodos)
- Un **nodo** es una unidad de trabajo dentro de un flow
- Cada nodo representa una acción o una condición
- Los nodos se conectan entre sí formando un grafo dirigido
- Cada nodo tiene una configuración específica según su tipo

### Connectors (Conectores de Apps)
- Un **connector** conecta Ionflow con una plataforma externa
- Ejemplos: Shopify, WooCommerce, MercadoLibre, etc.
- Cada connector expone acciones disponibles como nodos

### Triggers
- Un **trigger** inicia la ejecución de un flow
- Puede ser: webhook, schedule (cron), manual, o evento de una app conectada

## Reglas de Negocio Clave

- Ionflow es una aplicacion multi company, cada compania puede tener uno o mas usuarios, los usuarios pueden tener diferentes permisos.
- Para que un flow pueda ser ejecutado mediante un scheduuler o un webhook debe estar es status Active o en Produccion, en caso de estar en modo development se debe de ejecutar manualmente para que escuche el trigger.
- Se tienen dos tipos de App Connector, los de company o tenant y los globales, los globales son los que son migrados/aprobados por el usuario admin y sus nodos pueden ser utilizados por todos los companies, y los connectors de Company solo pueden ser usados por la company que los creo
- Se tiene dos tipos de boards, los globales que son utilizados para la construccion de grapps, para que un flow pueda ser migrado a global por el admin, en el diseno no debe contar con nodos de connctors de tipo company, todos deben ser nodos de tipo connector global
> ⚠️ Esta sección debe enriquecerse con reglas específicas a medida que el equipo las documenta. (AUN en construccion)

### Ejecución de Flows
- Un flow solo puede ejecutarse si está en estado **activo** a este modo se lo llama Production
- Si un flos es ejecutado desde el canvas se llama Development
- Si un nodo falla, el comportamiento depende de la configuración (datos introducidos, conexiones establecidas ejemplo las credenciales de alguna app)
- Los flows tienen un historial de ejecuciones con logs por nodo (los logs aun son un poco simples) pero si se cuenta con el resultado para cada una de las ejecuciones

### Gestión de Usuarios
- Autenticación gestionada actualmente por el repo `gateway` (PHP) y gestionado por SSO Keycloak
- Cada usuario pertenece a una **company** (multi-tenant)
- Los permisos determinan qué flows y conectores puede ver/editar un usuario y no solmanete esto sino tambien cada seccion que puede visitar

### Datos del E-commerce
- Los datos que fluyen por los nodos pueden incluir: pedidos, productos, inventarios, clientes y no se limitan a esto es depende a la configuracion de los nodos
- La integridad de estos datos es **crítica** — un error en un flow puede afectar pedidos reales

---

*Este archivo se actualiza cuando cambian las reglas fundamentales del negocio. Última actualización: Initial setup.*
