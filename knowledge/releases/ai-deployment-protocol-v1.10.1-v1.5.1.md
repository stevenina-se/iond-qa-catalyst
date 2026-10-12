# Protocolo de Despliegue — Productos IA

## IonMind v1.10.1 + StageMind v1.5.1

---

## Información General

| Campo | Valor |
|-------|-------|
| **Repos involucrados** | `ai_ionmind` · `ai_productmind` |
| **Rama release-candidate** | `v1.10.1` (IonMind) · `v1.5.1` (StageMind) |
| **Tags destino** | `v1.10.1` (IonMind) · `v1.5.1` (StageMind) |
| **Ambiente de validación** | `preprod-ionmind.iond.ai` · `preprod-stagemind.iond.ai` |
| **Responsable** | Dev Lead - Scrum Master |
| **Fecha** | [PENDIENTE — definir por Scrum Master] |
| **Tipo de Despliegue** | 🟠 **Riesgo Medio** — Mejoras incrementales en ambos productos IA, sin cambios de infraestructura mayor |

---

## Descripción

Ticket de seguimiento del ciclo de las versiones **IonMind v1.10.1** y **StageMind v1.5.1**, desde la conformación de las release candidates hasta el despliegue en los ambientes de validación y cierre.

Centraliza el contenido de ambas versiones, la coordinación de QA, las aprobaciones, los reportes de despliegue y la evidencia de verificación post-deploy.

### IonMind v1.10.1 (26 tickets)

Incluye automatización de migraciones de BD, implementación de tiers de servicio, metodología Delta para detección de cambios, notificaciones por email/Mattermost, transformación XML, extracción de APIs de mensajería (WhatsApp, Telegram, Instagram, Messenger), y correcciones de bugs en endpoints duplicados y webhooks.

### StageMind v1.5.1 (14 tickets)

Incluye validación NSFW, observabilidad y métricas operativas, monitoreo robusto de costos de Replicate, API extensible de feedback para Xenvio, y corrección de Error 400 para imágenes válidas.

### Documentos de la versión

> - IonMind: [release-tickets.csv](file:///c:/Users/STEVE/Desktop/Automation/ionflow-qa-catalyst/knowledge/releases/ionmind-v1.10.1/release-tickets.csv)
> - StageMind: [release-tickets.csv](file:///c:/Users/STEVE/Desktop/Automation/ionflow-qa-catalyst/knowledge/releases/stagemind-v1.5.1/release-tickets.csv)

El alcance de tickets a validar es el listado en esos documentos. No se duplican las tablas completas en este ticket.

### Dependencia con iond v0.2.0

> ⚠️ **IMPORTANTE:** IonMind v1.10.1 tiene **6 tickets cross-iond** que requieren coordinación con el despliegue de iond v0.2.0. IonMind debe desplegarse **ANTES** que iond v0.2.0 para que las APIs estén disponibles. StageMind es independiente.

---

## Repositorios y Ramas de Despliegue

| Producto | Repositorio | Stack | Rama | Namespace/Host |
|----------|-------------|-------|------|----------------|
| **IonMind** | `ai_ionmind` | Python / FastAPI | **`v1.10.1`** | [PENDIENTE] |
| **StageMind** | `ai_productmind` | Python / FastAPI | **`v1.5.1`** | [PENDIENTE] |

> ⚠️ **CONFIRMAR** — Las ramas del release deben ser verificadas antes de proceder. Las ramas listadas son estimaciones basadas en la convención de versiones.

---

## Último commit por repo (al momento del release)

| Repositorio | Último commit | Mensaje |
|-------------|--------------|---------|
| `ai_ionmind` | `[PENDIENTE]` | [verificar al momento del release] |
| `ai_productmind` | `[PENDIENTE]` | [verificar al momento del release] |

---

## Comandos a ejecutar

### IonMind

```bash
# Verificar migraciones pendientes
python manage.py db upgrade --dry-run

# Ejecutar migraciones
python manage.py db upgrade

# Reiniciar servicio (vía CI/CD o manual)
```

### StageMind

```bash
# Ejecutar migraciones (si las hay)
python manage.py db upgrade

# Reiniciar servicio (vía CI/CD o manual)
```

### Variables de entorno nuevas

**IonMind v1.10.1:**

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `SMTP_HOST=<smtp-host>` | NUEVO | Notificaciones por email |
| `SMTP_PORT=587` | NUEVO | Puerto SMTP |
| `SMTP_USERNAME=<usuario>` | NUEVO | Credencial SMTP |
| `SMTP_PASSWORD=<password>` | NUEVO | Credencial SMTP |
| `SMTP_FROM=noreply@iond.ai` | NUEVO | Sender de notificaciones |
| `MATTERMOST_WEBHOOK_URL=<url>` | NUEVO | Canal de errores |
| `TIER_DEFAULT=standard` | NUEVO | Tier por defecto |
| `TIER_PRICING_ENABLED=true` | NUEVO | Activar pricing por tier |
| `AUTO_MIGRATE=true` | NUEVO | Migraciones al startup |
| `MIGRATION_BACKUP=true` | NUEVO | Backup antes de migrar |
| `LOGODEV_API_KEY=<key>` | NUEVO | Integración Logo.dev |

**StageMind v1.5.1:**

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `NSFW_ENABLED=true` | NUEVO | Activar filtro NSFW |
| `NSFW_MODEL_PATH=<path>` | NUEVO | Modelo de detección |
| `NSFW_THRESHOLD=0.85` | NUEVO | Umbral de confianza |
| `METRICS_ENABLED=true` | NUEVO | Activar métricas |
| `METRICS_EXPORT_INTERVAL=60` | NUEVO | Intervalo exportación (seg) |
| `ALERT_RESPONSE_TIME_THRESHOLD=5000` | NUEVO | Umbral de alerta (ms) |
| `COST_MONITORING_ENABLED=true` | NUEVO | Monitoreo de costos |
| `REPLICATE_COST_TRACKING=true` | NUEVO | Tracking costos Replicate |
| `COST_ALERT_MONTHLY_THRESHOLD=<monto>` | NUEVO | Alerta gasto mensual |
| `FEEDBACK_API_ENABLED=true` | NUEVO | API de feedback |
| `FEEDBACK_RETENTION_DAYS=90` | NUEVO | Retención feedback |

---

## Alcance de QA

La validación de estas versiones se compone de:

1. **Regression Test IonMind** — Ejecución de la [regression-matrix.csv](file:///c:/Users/STEVE/Desktop/Automation/ionflow-qa-catalyst/knowledge/releases/ionmind-v1.10.1/regression-matrix.csv) sobre el ambiente `preprod-ionmind.iond.ai` con la rama release-candidate.
2. **Regression Test StageMind** — Ejecución de la [regression-matrix.csv](file:///c:/Users/STEVE/Desktop/Automation/ionflow-qa-catalyst/knowledge/releases/stagemind-v1.5.1/regression-matrix.csv) sobre el ambiente `preprod-stagemind.iond.ai`.
3. **Cross-iond Test** — Validación de los 6 tickets cross-iond que involucran IonMind + iond conjuntamente (ejecutar DESPUÉS de desplegar iond v0.2.0).

### Requisito previo (bloqueante)

> ⚠️ Cada ambiente de validación debe tener exactamente el mismo build de su release candidate. Antes de habilitar QA se debe confirmar que:
>
> **IonMind:**
> - Repo `ai_ionmind` desplegado desde el commit de release-candidate
> - Migraciones ejecutadas correctamente
> - Variables de entorno nuevas configuradas (SMTP, Mattermost, Tiers, Logo.dev)
> - Conectividad con iond gateway verificada (para tickets cross)
>
> **StageMind:**
> - Repo `ai_productmind` desplegado desde el commit de release-candidate
> - Variables de entorno nuevas configuradas (NSFW, Métricas, Costos, Feedback)
> - Modelo NSFW accesible y funcional
> - Conectividad con Xenvio verificada

---

## TEST

### Objetivo

Verificar que los cambios incluidos en ambas versiones efectivamente funcionan y que los builds son estables para continuar hacia producción.

### Alcance

Validación de los tickets listados en los release-tickets.csv de cada producto, más la regression de funcionalidades heredadas.

Si algún caso de prueba falla, se reporta como bug, se corrige y se relanza el ciclo desde el inicio.

### Ambientes

| Producto | Ambiente | RC Deploy | Build Verificado | Migraciones OK | Variables OK |
|----------|----------|-----------|-----------------|----------------|--------------|
| **IonMind** | `preprod-ionmind.iond.ai` | ⬜ | ⬜ | ⬜ | ⬜ |
| **StageMind** | `preprod-stagemind.iond.ai` | ⬜ | ⬜ | ⬜ | ⬜ |

### Matrices de prueba

| Producto | Tipo | Archivo |
|----------|------|---------|
| IonMind | Regression | [regression-matrix.csv](file:///c:/Users/STEVE/Desktop/Automation/ionflow-qa-catalyst/knowledge/releases/ionmind-v1.10.1/regression-matrix.csv) |
| StageMind | Regression | [regression-matrix.csv](file:///c:/Users/STEVE/Desktop/Automation/ionflow-qa-catalyst/knowledge/releases/stagemind-v1.5.1/regression-matrix.csv) |

### Criterio de aprobación

Un ciclo se considera aprobado solo si pasa en **ambos productos**. Un fallo en cualquiera de los dos bloquea el avance, aunque el otro haya pasado.

1. **IonMind** — Todos los TCs de Regression pasan. Extracciones de APIs completando sin duplicados. Migraciones automáticas ejecutando sin errores. Tiers de servicio funcionales.
2. **StageMind** — Todos los TCs de Regression pasan. Pipeline de imagen funcional. NSFW sin falsos positivos en imágenes de productos. Métricas registrándose.
3. **Cross-iond** — Los 6 tickets cross-iond pasan su validación cuando iond v0.2.0 está desplegado.
4. **Sin regresiones funcionales** en áreas no modificadas.
5. Toda **discrepancia de comportamiento** entre los ambientes y el comportamiento documentado debe reportarse como hallazgo.

---

# 🧠 IONMIND v1.10.1

## Resumen de Cambios

| Categoría | Cantidad |
|-----------|----------|
| Nuevas funcionalidades | 5 |
| Correcciones (Bugs) | 4 |
| Mejoras | 3 |
| Tasks | 14 |
| **Total** | **26** |
| Tickets cross-iond | 6 |

### Cambios Críticos

| Cambio | Impacto en Despliegue | Acción Requerida |
|--------|----------------------|-----------------|
| **Automatización de migraciones de BD** | Nuevo sistema de migraciones automáticas | Verificar que migraciones se ejecutan correctamente al deploy |
| **Tiers de Servicio** | Nuevo concepto de tiers con pricing diferenciado | Configurar tiers en BD antes del deploy |
| **Metodología Delta** | Nuevo algoritmo de detección de cambios | Verificar datos de referencia para comparación Delta |
| **Notificaciones por email/Mattermost** | Nuevo canal de comunicación de errores | Configurar SMTP y webhook de Mattermost |
| **Transformación XML a ConnectorDraft** | Nuevo formato de input | Verificar schemas XML compatibles |

### Cross-iond — Coordinación con iond v0.2.0

> ⚠️ **IMPORTANTE:** Los siguientes cambios de IonMind requieren coordinación con el despliegue de iond v0.2.0:

| Ticket | Descripción | Impacto en iond |
|--------|-------------|-----------------|
| 86e20nmqx | Cobro por primer escrapeo | Requiere cambios en `ion_gateway` y `ion_gateway_ion` |
| 86e1f9qfg | IONMIND V1.9 | Requiere cambios en `ion_gateway` y `ion_gateway_ion` |
| 86e2p459r | Recuperar análisis tras sesión expirada | Requiere cambios en `ion_gateway_ion` |
| 86e25j0rn | Notificaciones de errores | Requiere cambios en `ion_gateway` |
| 86e2mt70g | Selección de tier desde iond | Requiere cambios en `ion_gateway` y `ion_gateway_ion` |
| 86e2g4ev0 | Fix endpoints duplicados | Requiere cambios en `ion_gateway` y `ion_gateway_ion` |

> **Recomendación:** Desplegar IonMind v1.10.1 **ANTES** que iond v0.2.0, o en paralelo, para que las APIs estén disponibles cuando el frontend de iond las necesite.

---

### Preparación de Rama — `ai_ionmind` → rama `v1.10.1`

- [ ] Todas las ramas aprobadas por QA fusionadas a `v1.10.1`
- [ ] Verificar que las migraciones de BD se ejecutan correctamente en staging
- [ ] Tiers de servicio configurados en staging
- [ ] SMTP y Mattermost webhook configurados
- [ ] Validación final completada

### Despliegue de IonMind

```bash
# Actualizar repositorio
git fetch origin
git checkout v1.10.1
git pull origin v1.10.1

# Verificar migraciones pendientes
python manage.py db upgrade --dry-run

# Ejecutar migraciones
python manage.py db upgrade

# Reiniciar servicio
# (Vía CI/CD o manual según infraestructura)
```

### Verificación Post-Deploy — IonMind

- [ ] Health check responde OK
- [ ] Análisis de API de prueba ejecuta correctamente
- [ ] Extracción de conectores funciona (probar con API pública conocida)
- [ ] Tiers de servicio visibles y seleccionables
- [ ] Notificaciones por email funcionan (forzar error de prueba)
- [ ] Notificaciones por Mattermost funcionan
- [ ] Metodología Delta detecta cambios correctamente
- [ ] Migraciones automáticas ejecutaron sin errores
- [ ] Logo.dev devuelve logos como fallback
- [ ] Sin endpoints duplicados en conectores generados

---

# 🎨 STAGEMIND v1.5.1

## Resumen de Cambios

| Categoría | Cantidad |
|-----------|----------|
| Nuevas funcionalidades | 6 |
| Correcciones (Bugs) | 1 |
| Mejoras | 4 |
| Tasks | 3 |
| **Total** | **14** |

### Cambios Críticos

| Cambio | Impacto en Despliegue | Acción Requerida |
|--------|----------------------|-----------------|
| **Validación NSFW** | Nuevo filtro de contenido | Configurar modelo NSFW y umbrales |
| **Observabilidad y métricas** | Nuevo sistema de monitoreo | Configurar dashboard de métricas y alertas |
| **Costos de Replicate** | Nuevo cálculo robusto | Verificar API keys de Replicate y pricing actualizado |
| **API de feedback para Xenvio** | Nueva API extensible | Verificar conectividad con Xenvio |
| **Fix Error 400 para imágenes válidas** | Corrección crítica de bug | Verificar con el set de imágenes que antes fallaban |

---

### Preparación de Rama — `ai_productmind` → rama `v1.5.1`

- [ ] Todas las ramas aprobadas por QA fusionadas a `v1.5.1`
- [ ] Modelo NSFW configurado y accesible
- [ ] Dashboard de métricas/observabilidad configurado en staging
- [ ] API keys de Replicate actualizadas
- [ ] Conectividad con Xenvio verificada
- [ ] Validación final completada

### Despliegue de StageMind

```bash
# Actualizar repositorio
git fetch origin
git checkout v1.5.1
git pull origin v1.5.1

# Ejecutar migraciones (si las hay)
python manage.py db upgrade

# Reiniciar servicio
# (Vía CI/CD o manual según infraestructura)
```

### Verificación Post-Deploy — StageMind

- [ ] Health check responde OK
- [ ] Pipeline completo de imagen funciona (upload > process > result)
- [ ] Endpoint de boxes crea boxes correctamente
- [ ] Endpoint de escalado procesa imágenes válidas (fix Error 400)
- [ ] Endpoint de prompts genera prompts de edición
- [ ] Filtro NSFW bloquea imágenes inapropiadas
- [ ] Filtro NSFW NO bloquea imágenes legítimas de productos
- [ ] Métricas de performance registrándose
- [ ] Costos de Replicate calculados correctamente
- [ ] Consulta mensual de gastos funciona
- [ ] API de feedback recibe y persiste datos
- [ ] Xenvio puede consultar feedback

---

## Riesgos Identificados

| Riesgo | Producto | Mitigación |
|--------|----------|-----------|
| Migraciones automáticas de IonMind fallan al startup | IonMind | Ejecutar `--dry-run` primero. Backup de BD antes de cada deploy. Verificar con `MIGRATION_BACKUP=true`. |
| NSFW bloquea imágenes legítimas de productos (falsos positivos) | StageMind | Probar con el catálogo de imágenes reales antes de activar en producción. Ajustar `NSFW_THRESHOLD` si es necesario. |
| SMTP no entrega emails de notificación | IonMind | Probar envío de email de prueba en preprod antes de activar notificaciones. Verificar SPF/DKIM del dominio `iond.ai`. |
| Costos de Replicate se disparan sin alerta | StageMind | Configurar `COST_ALERT_MONTHLY_THRESHOLD` con un valor conservador. Verificar que las alertas llegan al canal de Mattermost. |
| APIs de IonMind no disponibles cuando iond v0.2.0 las necesita | IonMind | Desplegar IonMind ANTES que iond. Verificar health check de IonMind desde el pod de iond. |
| Builds desalineados entre ambos productos | Ambos | Confirmar mismo commit de RC en cada repo antes de habilitar QA. |
| Modelo NSFW no accesible desde el pod de StageMind | StageMind | Verificar permisos y paths del modelo NSFW en el ambiente de preprod antes del deploy. |
| Endpoints de feedback no persisten datos correctamente | StageMind | Probar ciclo completo upload → feedback → consulta en preprod. |

---

## Criterios de Aceptación

- [ ] Todos los tickets listados en los release-tickets.csv están mergeados en las ramas release-candidate
- [ ] Ambos ambientes de preprod desplegados desde el commit correcto de cada RC
- [ ] Migraciones ejecutadas en ambos productos
- [ ] Variables de entorno nuevas configuradas correctamente
- [ ] Test de Regression aprobado para IonMind en `preprod-ionmind.iond.ai`
- [ ] Test de Regression aprobado para StageMind en `preprod-stagemind.iond.ai`
- [ ] Los 6 tickets cross-iond validados con iond v0.2.0 desplegado
- [ ] Sin regresiones funcionales en áreas no modificadas
- [ ] Sin falsos positivos de NSFW en imágenes de productos
- [ ] Notificaciones de IonMind entregándose por email y Mattermost
- [ ] Costos de Replicate dentro de umbrales definidos
- [ ] Aprobación explícita de Tech Lead para promover a producción
- [ ] Release notes generadas y publicadas

---

## Definición de Done

- [ ] Reporte de despliegue registrado como comentario en el ticket de ClickUp
- [ ] Evidencia de verificación post-deploy documentada (screenshots, logs, métricas)
- [ ] Monitoreo de 48 horas completado sin incidentes críticos
- [ ] Post-mortem documentado (si hubo incidentes)
- [ ] Ticket cerrado con estado `Ready for Release` o `Deployment`

---

## Orden de Despliegue Recomendado

```
1. StageMind v1.5.1 (independiente de iond)
     ↓
2. IonMind v1.10.1 (antes que iond para que APIs estén listas)
     ↓
3. iond v0.2.0 (último, consume APIs de IonMind actualizadas)
```

> ⚠️ **StageMind no tiene dependencias con iond ni IonMind** — puede desplegarse en cualquier momento.
>
> ⚠️ **IonMind debe desplegarse ANTES que iond v0.2.0** — los tickets cross-iond requieren que las APIs de IonMind v1.10.1 estén disponibles.

---

## Monitoreo — Ambos Productos

### Ventana de Monitoreo

| Campo | Valor |
|-------|-------|
| **Duración** | Mínimo **48 horas** post-despliegue |
| **Responsable** | Scrum Master / Dev Lead IA |
| **Canal de reporte** | Canal de equipo |

### Checklist de Monitoreo

**Cada hora (primeras 6 horas):**

- [ ] Health checks de ambos servicios responden OK
- [ ] Sin errores críticos en logs de IonMind
- [ ] Sin errores críticos en logs de StageMind
- [ ] Métricas de StageMind registrándose (si dashboard disponible)

**Cada 4 horas (siguientes 42 horas):**

- [ ] IonMind: extracciones completando sin errores
- [ ] StageMind: procesamiento de imágenes funcional
- [ ] Costos de Replicate dentro de umbrales
- [ ] Notificaciones de errores IonMind llegando por email/Mattermost
- [ ] Sin falsos positivos de NSFW en StageMind

### Métricas a Validar

| Producto | Métrica | Criterio de Éxito |
|----------|---------|-------------------|
| **IonMind** | Health check | Respuesta OK |
| **IonMind** | Extracciones de APIs | Completando sin errores ni duplicados |
| **IonMind** | Migraciones BD | Sin errores de schema |
| **IonMind** | Notificaciones | Emails y Mattermost entregándose |
| **StageMind** | Health check | Respuesta OK |
| **StageMind** | Procesamiento de imágenes | Sin Error 400 en imágenes válidas |
| **StageMind** | Filtro NSFW | Sin falsos positivos en imágenes de productos |
| **StageMind** | Tiempos de respuesta | Dentro de umbrales definidos |
| **StageMind** | Costos Replicate | Dentro del presupuesto mensual |

---

## Escalado de Problemas

1. **Documentar con exactitud:** timestamp, error, logs, impacto
2. **Determinar severidad:**
   - 🔴 **Crítico** — API no responde, datos corruptos, NSFW bloquea todo → **Rollback inmediato**
   - 🟠 **Alto** — Feature específica falla, workaround disponible → Evaluar rollback
   - 🟡 **Normal** — Comportamiento menor → Documentar, sin rollback
3. **Comunicar al equipo** por el canal oficial

---

## Rollback

### IonMind — Rollback

```bash
# 1. Revertir a versión anterior
git checkout <tag-anterior>

# 2. Si se hicieron migraciones de BD:
python manage.py db downgrade <revision-anterior>

# 3. Reiniciar servicio
# 4. Verificar health check
```

### StageMind — Rollback

```bash
# 1. Revertir a versión anterior
git checkout <tag-anterior>

# 2. Si se hicieron migraciones:
python manage.py db downgrade <revision-anterior>

# 3. Desactivar NSFW si causa falsos positivos:
# Set NSFW_ENABLED=false en variables de entorno

# 4. Reiniciar servicio
# 5. Verificar health check
```

### Checklist de Rollback

- [ ] Servicio revertido a versión anterior
- [ ] BD restaurada/downgraded si aplica
- [ ] Health check responde OK
- [ ] Funcionalidad básica verificada
- [ ] Equipo informado por canal oficial
- [ ] Post-mortem documentado

---

## Tickets Incluidos

### IonMind v1.10.1 (26 tickets)

| Ticket ID | Descripción | Prioridad | Cross-iond |
|-----------|-------------|-----------|------------|
| 86e186nkx | Hardcoding de plataformas por BD | 🟡 normal | ❌ |
| 86e14d8w5 | Implementación de Tiers de Servicio | 🟡 normal | ❌ |
| 86e27q216 | Fix webhook de registros en cache | 🟠 high | ❌ |
| 86e27q2bw | Fix tests y script de limpieza | 🔵 low | ❌ |
| 86e1fkxz7 | Integrar Logo.dev en IonMind | 🟡 normal | ❌ |
| 86e1f9qfg | IONMIND V1.9 | 🟡 normal | ✅ |
| 86e2mt73u | Demo Locus Robotics con API falsa | 🟠 high | ✅ |
| 86e2e8gde | Extraer conectores UPS/FedEx | 🟠 high | ✅ |
| 86e1r05nh | Automatización de migraciones de BD | 🟡 normal | ❌ |
| 86e2mt6w7 | Transformación XML a ConnectorDraft v1 | 🟠 high | ❌ |
| 86e2j45du | Extraer Messenger Platform API | 🟡 normal | ❌ |
| 86e2j4509 | Extraer Instagram API | 🟡 normal | ❌ |
| 86e2j44hg | Extraer WhatsApp Cloud API | 🟡 normal | ❌ |
| 86e2j43xg | Extraer Telegram Bot API | 🟡 normal | ❌ |
| 86e2j43eg | Extraer APIs de mensajería | 🟡 normal | ❌ |
| 86e2ft73m | Extraer descripciones de endpoints | 🟠 high | ❌ |
| 86e2p459r | Recuperar análisis tras sesión expirada | 🟠 high | ✅ |
| 86e1f9qk3 | Metodología Delta | 🟡 normal | ❌ |
| 86e31uj4w | Escanear Invoicing.co y Pinecone | 🟡 normal | ❌ |
| 86e25j0rn | Notificaciones de errores a iond | 🟡 normal | ✅ |
| 86e2mt70g | Selección de service tier desde iond | 🟡 normal | ✅ |
| 86e2g4ev0 | Fix endpoints duplicados | 🟠 high | ✅ |
| 86e20nmqx | Confirmación y cobro primer escrapeo | 🟠 high | ✅ |
| 86e2t9962 | Estado de minado no se actualiza en tiempo real | 🟠 high | ❌ |
| 86e1qzefc | Actualización del Backend de IonFlow | 🟡 normal | ❌ |
| 86e1fky0g | Atribución condicional Logo.dev en IonFlow | 🟡 normal | ❌ |

### StageMind v1.5.1 (14 tickets)

| Ticket ID | Descripción | Prioridad |
|-----------|-------------|-----------|
| 86e0rj0u4 | Catalog Builder v1.3.5 | 🟠 high |
| 86e0rxzem | Endpoint generación de prompts de edición | 🟡 normal |
| 86e0rqwgd | Endpoint escalado de imágenes | 🟠 high |
| 86e0rqvqr | Endpoint creación de boxes | 🟠 high |
| 86e0ega5d | STAGEMIND v1.4 | 🟡 normal |
| 86e0ethmq | Documentación observabilidad/costos | 🟡 normal |
| 86e0ethmn | Monitoreo costos Replicate | 🟠 high |
| 86e0ethmr | Umbrales y monitoreo de performance | 🟡 normal |
| 86e0ethmp | Tiempos de respuesta por request | 🟠 high |
| 86e0ethmv | Métricas operativas | 🟠 high |
| 86e0fazj2 | Consulta mensual gastos por proveedor | 🟡 normal |
| 86e0j62tv | Validación NSFW | 🟡 normal |
| 86e0tkajg | Fix Error 400 imágenes válidas | 🔵 low |
| 86e2ee6d6 | API feedback para Xenvio | 🟠 high |

---

## Variables de Entorno — Referencia Completa

<details>
<summary><strong>IonMind — Todas las variables</strong></summary>

```bash
# --- NUEVAS VARIABLES ---
# Notificaciones
SMTP_HOST=<smtp-host>
SMTP_PORT=587
SMTP_USERNAME=<usuario>
SMTP_PASSWORD=<password>
SMTP_FROM=noreply@iond.ai
MATTERMOST_WEBHOOK_URL=<mattermost-webhook>

# Tiers de servicio
TIER_DEFAULT=standard
TIER_PRICING_ENABLED=true

# Migraciones automáticas
AUTO_MIGRATE=true
MIGRATION_BACKUP=true

# Logo.dev
LOGODEV_API_KEY=<logodev-api-key>

# --- VARIABLES EXISTENTES (sin cambios) ---
DATABASE_URL=<postgres-connection-string>
REDIS_URL=<redis-connection-string>
API_HOST=0.0.0.0
API_PORT=<puerto>
ENVIRONMENT=production
SECRET_KEY=<secret-key>
OPENAI_API_KEY=<openai-api-key>
OPENAI_MODEL=<modelo>
IOND_GATEWAY_URL=<url-gateway-iond>
IOND_API_KEY=<api-key-iond>
SCRAPING_ENABLED=true
SCRAPING_TIMEOUT=120
```

</details>

<details>
<summary><strong>StageMind — Todas las variables</strong></summary>

```bash
# --- NUEVAS VARIABLES ---
# NSFW Detection
NSFW_ENABLED=true
NSFW_MODEL_PATH=<path-or-url-nsfw-model>
NSFW_THRESHOLD=0.85

# Observabilidad
METRICS_ENABLED=true
METRICS_EXPORT_INTERVAL=60
ALERT_RESPONSE_TIME_THRESHOLD=5000

# Costos
COST_MONITORING_ENABLED=true
REPLICATE_COST_TRACKING=true
COST_ALERT_MONTHLY_THRESHOLD=<monto>

# Feedback API
FEEDBACK_API_ENABLED=true
FEEDBACK_RETENTION_DAYS=90

# --- VARIABLES EXISTENTES (sin cambios) ---
DATABASE_URL=<postgres-connection-string>
REDIS_URL=<redis-connection-string>
API_HOST=0.0.0.0
API_PORT=<puerto>
ENVIRONMENT=production
SECRET_KEY=<secret-key>
REPLICATE_API_TOKEN=<replicate-api-token>
S3_BUCKET=<bucket-name>
S3_ACCESS_KEY=<access-key>
S3_SECRET_KEY=<secret-key>
S3_REGION=<region>
XENVIO_API_URL=<url-xenvio>
XENVIO_API_KEY=<api-key-xenvio>
```

</details>

---

*Draft generado por ionflow-qa-catalyst — Productos IA*
*IonMind v1.10.1 + StageMind v1.5.1*
*Fecha: 2026-09-15*
