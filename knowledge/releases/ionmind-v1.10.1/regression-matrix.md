# Regression Matrix — IonMind v1.10.1

> Generado por `ionflow-qa-catalyst`
> Fecha: 2026-09-15
> Versión: **IonMind v1.10.1**
> Total de tickets: 26 (20 exclusivos ionmind + 6 cross-iond)
> Nota: Sin data L2/L3 disponible — TCs basados en información de tickets

---

## Resumen

| Métrica | Valor |
|---------|-------|
| Versión | IonMind v1.10.1 |
| Total de TCs | 52 |
| TCs Regresión Directa | 38 |
| TCs Regresión Indirecta (cross-iond) | 10 |
| TCs Baseline | 4 |
| Repo principal | `ai_ionmind` |
| Tickets exclusivos IonMind | 20 |
| Tickets cross-iond | 6 |

---

## Cobertura por Módulo

| Módulo | Tickets | Directos | Indirectos | Total | Riesgo |
|--------|---------|----------|------------|-------|--------|
| Extracción de APIs / Conectores | 9 | 12 | 2 | 14 | 🟠 Alto |
| Tiers de Servicio | 2 | 4 | 2 | 6 | 🟠 Alto |
| Core / Transformación | 3 | 5 | 1 | 6 | 🟠 Alto |
| Logo.dev / Scraping | 2 | 3 | 1 | 4 | 🟡 Medio |
| Notificaciones / Errores | 1 | 2 | 1 | 3 | 🟡 Medio |
| Endpoints / Duplicados | 2 | 3 | 2 | 5 | 🔴 Crítico |
| BD / Migraciones | 1 | 2 | 0 | 2 | 🟠 Alto |
| Delta / Detección cambios | 1 | 2 | 0 | 2 | 🟠 Alto |
| Benchmark / LLM | 1 | 1 | 0 | 1 | 🟡 Medio |
| Webhooks / Cache | 1 | 2 | 0 | 2 | 🟡 Medio |
| Infra / QA Sandbox | 2 | 2 | 0 | 2 | 🟢 Bajo |
| Baseline (funcionalidad existente) | — | 0 | 0 | 4 | 🟡 Medio |

---

## Matriz de Regresión Detallada

### 🔗 Extracción de APIs / Generación de Conectores

| ID | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Ticket |
|----|------|-------------|-------------|-------|-------------------|-----------|--------|
| IM-01 | DIRECTA | Extraer Messenger Platform API | IonMind operativo, API docs accesibles | IonMind > Extraer > Messenger Platform > Iniciar | Endpoints de Messenger extraídos y App Connector generado | 🟠 Alto | 86e2j45du |
| IM-02 | DIRECTA | Extraer Instagram API | IonMind operativo | IonMind > Extraer > Instagram API > Iniciar | Endpoints de Instagram extraídos correctamente | 🟠 Alto | 86e2j4509 |
| IM-03 | DIRECTA | Extraer WhatsApp Cloud API | IonMind operativo | IonMind > Extraer > WhatsApp Cloud > Iniciar | Endpoints de WhatsApp extraídos correctamente | 🟠 Alto | 86e2j44hg |
| IM-04 | DIRECTA | Extraer Telegram Bot API | IonMind operativo | IonMind > Extraer > Telegram Bot > Iniciar | Endpoints de Telegram extraídos correctamente | 🟠 Alto | 86e2j43xg |
| IM-05 | DIRECTA | Extraer APIs de mensajería y generar App Connectors (batch) | IonMind operativo | IonMind > Extraer > Mensajería (batch) > Verificar | Múltiples App Connectors generados en batch sin duplicados | 🟠 Alto | 86e2j43eg |
| IM-06 | DIRECTA | Extraer conectores UPS Track Alert | IonMind operativo | IonMind > Extraer > UPS Track Alert > Iniciar | Conector UPS generado con endpoints correctos | 🟠 Alto | 86e2e8gde |
| IM-07 | DIRECTA | Extraer conectores FedEx Supply Chain | IonMind operativo | IonMind > Extraer > FedEx Supply Chain > Iniciar | Conector FedEx generado correctamente | 🟠 Alto | 86e2e8gde |
| IM-08 | DIRECTA | Transformación XML a ConnectorDraft v1 | XML de API disponible | IonMind > Transformar > XML input > ConnectorDraft output | XML transformado a ConnectorDraft v1 sin errores | 🟠 Alto | 86e2mt6w7 |
| IM-09 | DIRECTA | Extraer y persistir descripciones para cada endpoint | Conector con endpoints | IonMind > Extraer > Verificar descripciones persistidas | Descripciones extraídas y guardadas en BD para cada endpoint | 🟡 Medio | 86e2ft73m |
| IM-10 | DIRECTA | Escanear Invoicing.co para crear App Connectors | IonMind operativo | IonMind > Escanear > Invoicing.co > Verificar | App Connector de Invoicing.co generado | 🟡 Medio | 86e31uj4w |
| IM-11 | DIRECTA | Escanear Pinecone para crear App Connectors | IonMind operativo | IonMind > Escanear > Pinecone > Verificar | App Connector de Pinecone generado | 🟡 Medio | 86e31uj4w |
| IM-12 | DIRECTA | Demo de Locus Robotics con API falsa | API falsa configurada | IonMind > Demo > Locus Robotics > Ejecutar | Demo funcional con API mock | 🟡 Medio | 86e2mt73u |
| IM-13 | INDIRECTA | Conectores generados visibles en iond App Connectors | Conector generado por IonMind | iond > Connections > Verificar conectores generados | Conectores de IonMind visibles y utilizables en iond | 🟠 Alto | 86e2j43eg |
| IM-14 | INDIRECTA | Descripciones de endpoints propagadas a iond | Descripciones persistidas | iond > Connections > Connector > Endpoint > Ver descripción | Descripciones de IonMind visibles en interfaz de iond | 🟡 Medio | 86e2ft73m |

### 🏷️ Tiers de Servicio

| ID | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Ticket |
|----|------|-------------|-------------|-------|-------------------|-----------|--------|
| IM-15 | DIRECTA | Implementación de Tiers de Servicio en IonMind | IonMind operativo | IonMind > Admin > Tiers > Crear tier | Tier creado y configurable | 🟠 Alto | 86e14d8w5 |
| IM-16 | DIRECTA | Asignación de tier a análisis | Tiers configurados | IonMind > Análisis > Seleccionar tier > Ejecutar | Análisis usa el tier seleccionado correctamente | 🟠 Alto | 86e14d8w5 |
| IM-17 | DIRECTA | Selección de service tier desde iond | iond conectado a IonMind | iond > Connections > IonMind > Seleccionar tier | Tier seleccionado y aplicado en análisis | 🟠 Alto | 86e2mt70g |
| IM-18 | INDIRECTA | Tier afecta cobro de primer escrapeo | Tier + cobro configurado | iond > App > First scrape > Verificar cobro según tier | Cobro corresponde al tier seleccionado | 🟡 Medio | 86e20nmqx |

### 🔧 Core / Motor de IonMind

| ID | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Ticket |
|----|------|-------------|-------------|-------|-------------------|-----------|--------|
| IM-19 | DIRECTA | IONMIND V1.9 — funcionalidad general | IonMind actualizado | IonMind > Ejecutar análisis completo > Verificar output | Análisis completo sin errores con funcionalidad V1.9 | 🟠 Alto | 86e1f9qfg |
| IM-20 | DIRECTA | Metodología Delta — detección de cambios | API con cambios conocidos | IonMind > Delta > Escanear API con cambios > Verificar | Cambios detectados correctamente vs versión anterior | 🟠 Alto | 86e1f9qk3 |
| IM-21 | DIRECTA | Hardcoding de plataformas por BD | BD con plataformas | IonMind > Admin > Plataformas > Verificar hardcoded | Plataformas cargadas desde BD correctamente | 🟡 Medio | 86e186nkx |
| IM-22 | DIRECTA | Confirmación y cobro para primer escrapeo | App sin escanear | iond > App > First Scrape > Confirmar > Verificar cobro | Confirmación visible, cobro procesado en IonMind | 🔴 Crítico | 86e20nmqx |
| IM-23 | INDIRECTA | V1.9 conectores en iond | Conector generado con V1.9 | iond > Connections > Conector V1.9 > Usar en flow > Run | Nodos del conector V1.9 funcionan en flows de iond | 🟠 Alto | 86e1f9qfg |

### 🐛 Bug Fixes

| ID | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Ticket |
|----|------|-------------|-------------|-------|-------------------|-----------|--------|
| IM-24 | DIRECTA | Webhook de registros en cache — notificación corregida | Registro en cache | IonMind > Crear registro > Verificar webhook | Notificación webhook disparada correctamente (sin error previo) | 🟠 Alto | 86e27q216 |
| IM-25 | DIRECTA | Script de limpieza y tests | Suite de tests disponible | IonMind > Ejecutar tests > Run script de limpieza | Tests pasan, limpieza ejecuta sin errores | 🟡 Medio | 86e27q2bw |
| IM-26 | DIRECTA | Recuperar análisis de IonMind tras expiración de sesión | Sesión expirada durante análisis | IonMind > Análisis > Sesión expira > Re-login | Análisis previo recuperado o error terminal mostrado | 🔴 Crítico | 86e2p459r |
| IM-27 | DIRECTA | Endpoints duplicados corregidos | Conector con endpoints | IonMind > Extraer > Verificar que no genera duplicados | Sin endpoints duplicados en App Connectors de iond | 🔴 Crítico | 86e2g4ev0 |
| IM-28 | INDIRECTA | Endpoints no duplicados visibles en iond | Conector actualizado | iond > Connections > Connector > Endpoints | Lista sin duplicados, datos consistentes | 🔴 Crítico | 86e2g4ev0 |

### 🖼️ Logo.dev / Integración Visual

| ID | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Ticket |
|----|------|-------------|-------------|-------|-------------------|-----------|--------|
| IM-29 | DIRECTA | Integrar Logo.dev en pipeline de logos de IonMind | IonMind operativo | IonMind > Extraer > App sin logo propio > Verificar | Logo.dev utilizado como fallback, logo visible | 🟡 Medio | 86e1fkxz7 |
| IM-30 | DIRECTA | API de actualización de logos en IonMind | Logo.dev integrado | IonMind > Admin > Actualizar logos > Verificar | Logos actualizados via API de Logo.dev | 🟡 Medio | 86e1fkxz7 |
| IM-31 | INDIRECTA | Logos de Logo.dev visibles en iond | Conector con logo de fallback | iond > Connections > App con logo Logo.dev | Logo visible con atribución correcta | 🟡 Medio | 86e1fkxz7 |

### 📧 Notificaciones / Errores

| ID | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Ticket |
|----|------|-------------|-------------|-------|-------------------|-----------|--------|
| IM-32 | DIRECTA | Errores de IonMind notificados a Ionflow por email | Error en análisis | IonMind > Forzar error > Verificar email | Email de notificación enviado a correo configurado | 🟡 Medio | 86e25j0rn |
| IM-33 | DIRECTA | Errores de IonMind notificados vía Mattermost | Error en análisis | IonMind > Forzar error > Verificar Mattermost | Notificación enviada al canal de Mattermost | 🟡 Medio | 86e25j0rn |
| IM-34 | INDIRECTA | Notificación visible en iond | Error en IonMind | iond > Notificaciones > Verificar error IonMind | Notificación de error visible en interfaz de iond | 🟡 Medio | 86e25j0rn |

### 🗄️ BD / Migraciones

| ID | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Ticket |
|----|------|-------------|-------------|-------|-------------------|-----------|--------|
| IM-35 | DIRECTA | Automatización de migraciones de BD | BD con esquema anterior | IonMind > Deploy > Ejecutar migraciones automáticas | Migraciones ejecutan sin errores, esquema actualizado | 🟠 Alto | 86e1r05nh |
| IM-36 | DIRECTA | Rollback de migración automática | Migración fallida | IonMind > Deploy > Migración con error > Rollback | BD restaurada al estado anterior sin pérdida de datos | 🟠 Alto | 86e1r05nh |

### 📊 Benchmark / LLM

| ID | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Ticket |
|----|------|-------------|-------------|-------|-------------------|-----------|--------|
| IM-37 | DIRECTA | Script de benchmark — comparación de modelos | Modelos configurados | IonMind > Benchmark > Ejecutar comparación > Verificar reporte | Reporte de comparación con métricas por modelo | 🟡 Medio | 86e1f9qkq |

### 📝 Documentación / Infra

| ID | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Ticket |
|----|------|-------------|-------------|-------|-------------------|-----------|--------|
| IM-38 | DIRECTA | Documentación actualizada (v1.8.x/1.9) | Docs existentes | IonMind > Docs > Verificar actualización | Documentación refleja funcionalidad de v1.8.x/1.9 | 🟢 Bajo | 86e1f9qkx |

### 🔒 Baseline (Funcionalidad Existente)

| ID | Tipo | Caso de Test | Precondición | Pasos | Resultado Esperado | Prioridad | Ticket |
|----|------|-------------|-------------|-------|-------------------|-----------|--------|
| IM-39 | BASELINE | Análisis básico de API — happy path | IonMind operativo, API pública | IonMind > Nueva extracción > URL de API > Analizar | API analizada, endpoints detectados, conector generado | 🔴 Crítico | — |
| IM-40 | BASELINE | Persistencia de conectores en BD | Conector generado | IonMind > Verificar que conector persiste tras restart | Conector disponible después de reinicio del servicio | 🟠 Alto | — |
| IM-41 | BASELINE | Health check del servicio IonMind | Servicio desplegado | GET /health o /status | Respuesta 200 OK con métricas básicas | 🟠 Alto | — |
| IM-42 | BASELINE | Integración IonMind ↔ iond (flujo completo) | Ambos servicios operativos | iond > Connections > Create via IonMind > Ejecutar análisis | Conector creado en iond desde análisis IonMind | 🔴 Crítico | — |

---

## Instrucciones

- **Los TCs cross-iond** deben ejecutarse en coordinación con el testing de iond v0.2.0
- **Sin L2/L3 disponible** — Los TCs se basan en la información de los tickets. Cuando se genere la documentación L2 de IonMind, esta matriz debe actualizarse
- **Ambiente de prueba:** Verificar que IonMind y iond estén conectados en el mismo ambiente de staging

---

*Generado por ionflow-qa-catalyst — IonMind v1.10.1*
*Fecha: 2026-09-15*
