# Protocolo de Despliegue — Ionflow v0.1.0

**Versión:** v0.1.0 — Primera Release a Producción
**Responsable:** Scrum Master
**Fecha:** 2026-06-30
**Tipo de Despliegue:** 🔴 **Alto Riesgo** — Primera release a producción. Sin versión anterior activa.

---

## Repositorios y Ramas de Despliegue

| Repositorio | Stack | Rama | Namespace Kubernetes |
|-------------|-------|------|---------------------|
| `gateway` | PHP 8.2 / Laravel 11 | **`v2.0.0`** | `ionflow-shipedge` |
| `flow_binaries` | Go 1.25 / Alpine 3.23 | **`v0.1.0`** | `ionflow-shipedge` |
| `gateway-ion` | Vue 3 + Vite + pnpm | **`v0.1.0`** | — (static deploy) |
| `webcomponents-flow` | Vue 3 + pnpm monorepo | **`v0.1.0`** | CDN Shipedge |

> **Confirmado localmente** — todas las ramas verificadas con `git branch --show-current` en cada repo.

---

## Último commit por repo (al momento del release)

| Repositorio | Último commit | Mensaje |
|-------------|--------------|---------|
| `gateway` | `d5f154db` | Revert "IONF-1049" from v2.0.0 release branch |
| `flow_binaries` | `58c5a5a` | Revert "IONF-1049" from v0.1.0 release branch |
| `gateway-ion` | `83fece96` | med |
| `webcomponents-flow` | `83fece96` | med |

---

## Preparación de Ramas

### En `gateway` → rama `v2.0.0`
- Todas las ramas aprobadas por QA fusionadas a `v2.0.0`
- Despliegue de rama `v2.0.0` en ambiente de staging para revisión de producto
- Validación final completada ✅
- **Nota:** Los commits IONF-1049 e IONF-1030 fueron revertidos de esta rama deliberadamente.

### En `flow_binaries` → rama `v0.1.0`
- Todas las ramas aprobadas por QA fusionadas a `v0.1.0`
- CI/CD configurado para disparar deploy staging en push a `v0.1.0`
- El pipeline construye la imagen Docker (Go 1.25 Alpine) y actualiza el tag en el repositorio GitOps
- Validación final completada ✅

### En `gateway-ion` → rama `v0.1.0`
- Todas las ramas aprobadas por QA fusionadas a `v0.1.0`
- Despliegue del frontend (Vite build) en ambiente de staging
- Validación final completada ✅

### En `webcomponents-flow` → rama `v0.1.0`
- Todas las ramas aprobadas por QA fusionadas a `v0.1.0`
- Despliegue de `ionbeta.js` e `ionalpha.js` al CDN de Shipedge
- Validación final completada ✅

---

## Fase 0 — Pre-Despliegue (Infraestructura)

> ⚠️ Ejecutar **ANTES** de iniciar cualquier despliegue de código.

- [ ] Detener todo el tráfico al dominio de producción de Ionflow
- [ ] Esperar a que todas las colas de Redis se hayan procesado (queue workers)
- [ ] Realizar una **copia completa de la base de datos** (PostgreSQL landlord + tenants) antes de cualquier migración
- [ ] Documentar estado del cluster antes del deploy:

```bash
kubectl get pods -n ionflow-shipedge
```

- [ ] Revisar variables de entorno para el nuevo despliegue (ver sección Variables)
- [ ] Confirmar que el dominio de staging está aislado durante el proceso

---

## Fase 1 — Despliegue de `gateway` (PHP 8.2 / Laravel 11)

### Pre-Despliegue

```bash
# Actualizar repositorio
git fetch origin

# Cambiar a rama del release
git checkout v2.0.0

# Hacer pull de cambios
git pull origin v2.0.0
```

### Variables de Entorno

Consultar el documento de variables en Google Sheets para versión `v2.0.0`.
Todas las variables deben actualizarse en el archivo `.env` del servidor antes de ejecutar los comandos.

El archivo de referencia de variables es `.env.gitlab`. Las variables requeridas para producción son:

```bash
# --- Aplicación ---
APP_NAME=Gateway
APP_ENV=production
APP_KEY=                          # Generar con: php artisan key:generate
APP_DEBUG=false
APP_URL=<url-de-produccion>
APP_ENCRYPTION_KEY=               # Clave de cifrado AES-256-CBC
APP_ENCRYPTION_CIPHER=AES-256-CBC

# --- Logs ---
LOG_CHANNEL=daily
LOG_LEVEL=error                   # prod: error
LOG_RETENTION_DAYS=7

# --- Base de Datos Principal (landlord) ---
DB_CONNECTION=pgsql
DB_HOST=<postgres-host>
DB_PORT=5432
DB_DATABASE=<nombre-bd-produccion>
DB_USERNAME=<usuario>
DB_PASSWORD=<password>

# --- Base de Datos Tenants ---
TENANT_HOST=<tenants-postgres-host>
TENANT_PORT=5432
TENANT_DATABASE=<nombre-bd-tenants-produccion>
TENANT_USERNAME=<usuario>
TENANT_PASSWORD=<password>

# --- Redis ---
QUEUE_CONNECTION=redis
BROADCAST_DRIVER=redis
REDIS_HOST=<redis-host>
REDIS_PASSWORD=<redis-password>
REDIS_PORT=6379
REDIS_DB=0

# --- Keycloak SSO ---
KEYCLOAK_ENDPOINT=<https://keycloak-host>
KEYCLOAK_REALM=<realm>
KEYCLOAK_CLIENT_ID=<client-id>
KEYCLOAK_CLIENT_SECRET=<client-secret>
KEYCLOAK_REALM_PUBLIC_KEY=<realm-public-key>
KEYCLOAK_ISSUER=                  # Opcional, default: {ENDPOINT}/realms/{REALM}
KEYCLOAK_LEEWAY=10

# --- CORS / Sesión ---
CORS_ALLOWED_ORIGINS=<https://app.ionflow.io,https://gateway.ionflow.io>
SESSION_DOMAIN=.ionflow.io
SESSION_SECURE_COOKIE=true

# --- IonMind (Agente IA) ---
IONMIND_URL=<ionmind-url>
IONMIND_TOKEN=<ionmind-bearer-token>

# --- Frontend / URLs ---
ION_FRONTEND_URL=<https://app.ionflow.io>
ION_PRIVACITY_URL=<privacy-url>
ION_TERMS_URL=<terms-url>
ION_SUPPORT_URL=<mailto:help@ionflow.io>

# --- Telescope (Monitoreo) ---
TELESCOPE_ENABLED=true
TELESCOPE_REQUEST_WATCHER=true
TELESCOPE_JOB_WATCHER=true
TELESCOPE_SCHEDULE_WATCHER=true
TELESCOPE_EXCEPTION_WATCHER=true
TELESCOPE_CLIENT_REQUEST_WATCHER=true
TELESCOPE_LOG_WATCHER=true
TELESCOPE_LOG_LEVEL=error
TELESCOPE_LOG_RETENTION_HOURS=168

# --- Nodo ---
NODE_SIGNATURE=ion

# --- Mail ---
MAIL_MAILER=smtp
MAIL_HOST=<smtp-host>
MAIL_PORT=<smtp-port>
MAIL_USERNAME=<usuario>
MAIL_PASSWORD=<password>
MAIL_ENCRYPTION=tls
MAIL_FROM_ADDRESS=noreply@ionflow.io
```

### Acceso al POD de `gateway`

```bash
# Listar pods disponibles
kubectl get pods -n ionflow-shipedge | grep gateway

# Ingresar al POD de gateway
kubectl exec -it <pod-name-gateway> -n ionflow-shipedge -- bash

# Validar conectividad y permisos antes de continuar
php artisan --version
```

### Ejecución de Comandos Obligatorios (en orden estricto)

> ⚠️ Ejecutar **en el siguiente orden**. Validar que cada comando se ejecute sin errores antes de continuar al siguiente.

```bash
# 1. Ejecutar migraciones — landlord (base principal)
php artisan migrate --force

# 2. Ejecutar seeders — orden definido en DatabaseSeeder.php:
#    AuthenticationSeeder → AppServicesSeeder → PassportSeeder →
#    LaratrustSeeder → ServicesSeeder → CategoriesSeeder →
#    CompanySeeder → TenantPermissionSeeder → FeatureSeeder
php artisan db:seed --force

# 3. Ejecutar migraciones de tenants
php artisan migrate --tenants

# 4. Ejecutar seeders de tenants
php artisan tenants:seed

# 5. Limpiar cache de configuración
php artisan config:clear

# 6. Regenerar claves de Passport (si es la primera vez en este entorno)
php artisan passport:keys --force

# 7. Reiniciar colas (workers de procesamiento de flows)
php artisan queue:restart
```

> **Seeders incluidos en `DatabaseSeeder.php`:**
> `AuthenticationSeeder`, `AppServicesSeeder` (producción), `PassportSeeder`,
> `LaratrustSeeder`, `ServicesSeeder`, `CategoriesSeeder`, `CompanySeeder`,
> `TenantPermissionSeeder`, `FeatureSeeder`

> **Seeders de tenants disponibles:**
> `TenantSeeder`, `TenantAppsSeeder`, `TenantPermissionSeeder`

- [ ] Validar que cada comando se ejecute sin errores
- [ ] Revisar mensajes de confirmación de cada paso
- [ ] Documentar cualquier warning o mensaje inesperado con timestamp

---

## Fase 2 — Despliegue de `flow_binaries` (Go 1.25 / Motor de Flows)

### Pre-Despliegue

```bash
git fetch origin
git checkout v0.1.0
git pull origin v0.1.0
```

### Variables de Entorno

Consultar Google Sheets para `v0.1.0`. Variables requeridas (referencia: `.env.example`):

```bash
# --- Servidor ---
PORT=<puerto-del-servicio>

# --- Base de Datos Principal ---
DB_HOST=<postgres-host>
DB_PORT=5432
DB_DATABASE=<nombre-bd>
DB_USERNAME=<usuario>
DB_PASSWORD=<password>

# --- Base de Datos Tenants ---
TENANT_HOST=<tenants-host>
TENANT_PORT=5432
TENANT_DATABASE=<nombre-bd-tenants>
TENANT_USERNAME=<usuario>
TENANT_PASSWORD=<password>
TENANT_PREFIX_SCHEMA=shipedge_ion

# --- Runtime / Flows ---
CRON_EXPRESSION=* * * * *
NODE_SIGNATURE=ion
APP_KEY=<app-key>
APP_URL=<url-del-servicio>
INTENT_KEY=<secret-key>
ENVIRONMENT=production

# --- Keycloak ---
KEYCLOAK_ENDPOINT=<https://keycloak-host>
KEYCLOAK_REALM=<realm>
KEYCLOAK_CLIENT_ID=<client-id>
KEYCLOAK_REALM_PUBLIC_KEY=<realm-public-key>

# --- CORS ---
CORS_ALLOWED_ORIGINS=<https://app.ionflow.io>

# --- Email ---
EMAIL_PROVIDER=SMTP
EMAIL_DEFAULT_FROM_NAME=IonFlow
EMAIL_DEFAULT_FROM_ADDRESS=noreply@ionflow.io
EMAIL_SMTP_HOST=<smtp-host>
EMAIL_SMTP_PORT=587
EMAIL_SMTP_USERNAME=<usuario>
EMAIL_SMTP_PASSWORD=<password>
EMAIL_SMTP_USE_TLS=true
EMAIL_SEND_TIMEOUT=30s

# --- Frontend ---
ION_FRONTEND_URL=<https://app.ionflow.io>

# --- LLM (IonMind) ---
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=<modelo>
LLM_API_KEY=<api-key>

# --- Logs de nodos ---
NODE_LOG_STORAGE_PATH=./storage/logs
NODE_LOG_CLEAN_CRON_EXPRESSION=0 0 * * *
NODE_LOG_RETENTION_DAYS=15
INACTIVE_CONNECTIONS_CRON_EXPRESSION=0 0 * * *

# --- ION PDF ---
PDF_GENERATE_URL=<url-del-microservicio-ionpdf>

# --- Cloudflare R2 (almacenamiento de PDFs) ---
R2_ACCOUNT_ID=<account-id>
R2_ACCESS_KEY_ID=<access-key>
R2_SECRET_ACCESS_KEY=<secret-key>
R2_BUCKET_NAME=<bucket-name>
R2_PUBLIC_URL=<url-publica-del-bucket>
```

### Proceso de Deploy (vía CI/CD GitOps)

El despliegue de `flow_binaries` está **automatizado vía GitLab CI/CD**. Al hacer push a `v0.1.0`:

1. CI ejecuta `go test ./...` en `backend/` y `core/`
2. CI construye la imagen Docker con el Dockerfile multi-stage (Go 1.25 Alpine builder → Alpine 3.23.4 runtime)
3. CI actualiza el tag de imagen en el repositorio GitOps (`values-staging.yaml`)
4. El cluster Kubernetes actualiza el deployment automáticamente

**Verificación manual post-deploy:**

```bash
# Verificar que el nuevo pod levantó correctamente
kubectl get pods -n ionflow-shipedge | grep flow-binaries

# Verificar logs del pod
kubectl logs <pod-name-flow-binaries> -n ionflow-shipedge --tail=50

# Verificar health check del servicio
curl -f http://<service-host>:<PORT>/api/ok
```

- [ ] Pod en estado `Running` sin restarts inesperados
- [ ] Health check responde `200 OK`
- [ ] Logs de arranque sin errores de conexión a BD o Keycloak

---

## Fase 3 — Despliegue de `gateway-ion` (Frontend Vue 3 / Vite)

### Pre-Despliegue

```bash
git fetch origin
git checkout v0.1.0
git pull origin v0.1.0
```

### Variables de Entorno

El frontend usa variables `VITE_*` en el archivo `.env` (referencia: `.env.example`):

```bash
# URLs de los servicios backend
VITE_APP_URL_DEV=<url-gateway-dev>
VITE_APP_URL_PROD=<url-gateway-produccion>     # URL del repo gateway (PHP)
VITE_APP_HUB_URL=<url-flow-binaries>           # URL del motor Go
VITE_APP_HUB_WS=ws://<url-flow-binaries>       # WebSocket del motor Go
VITE_APP_URL_PROD_FRONT=<url-frontend-prod>

# Node signature
VITE_APP_NODE_SIGNATURE=ion

# Keycloak SSO
VITE_KEYCLOAK_ENABLE=true                      # true = legacy login deshabilitado

# CDN WebComponents
VITE_APP_CDN_URL=https://cdn.shipedge.com/altacrest/ion/ion.js

# Reverb (WebSockets)
VITE_REVERB_APP_KEY=ionflow
VITE_REVERB_HOST=<reverb-host>
VITE_REVERB_PORT=6001

# FlowPilot / Copilot
VITE_APP_COPILOT_CHAT=true
```

### Construcción y Despliegue

```bash
# Instalar dependencias (usa pnpm según pnpm-workspace.yaml)
pnpm install

# Build de producción (type-check + build-only)
pnpm run build

# Verificar que el build generó correctamente los artefactos
ls -la dist/
```

- [ ] Build completado sin errores de TypeScript ni Vite
- [ ] Artefactos en `dist/` desplegados al servidor/CDN de producción

---

## Fase 4 — Despliegue de `webcomponents-flow` (Canvas / CDN)

### Pre-Despliegue

```bash
git fetch origin
git checkout v0.1.0
git pull origin v0.1.0
```

### Variables de Entorno

Archivo de referencia: `.env.example`:

```bash
VITE_GATEWAY_ID=<gateway-id>
VITE_GATEWAY_KEY=<gateway-key>
VITE_GATEWAY_URL=<url-del-gateway-php>         # URL del repo gateway
VITE_ION_BIN_URL=<url-flow-binaries>           # URL del motor Go
VITE_ION_FRONTEND_URL=<url-frontend>           # URL de gateway-ion
```

### Construcción y Despliegue al CDN

```bash
# Instalar dependencias (monorepo pnpm)
pnpm install

# Build completo de todos los modos: mapper + flow + all
# Comando real del package.json:
#   vue-tsc --build --force && vite build --mode all
pnpm run build-all

# Verificar artefactos generados
ls -la dist/
# Deben generarse al menos: ionbeta.js, ionalpha.js y sus sourcemaps
```

- [ ] `build-all` completado sin errores de TypeScript ni Vite
- [ ] Artefactos `ionbeta.js` e `ionalpha.js` actualizados en el CDN: `https://cdn.shipedge.com/altacrest/ion/`

---

## Validación Post-Despliegue

### Estabilización del Cluster

```bash
# Esperar 2-3 minutos para estabilización

# Verificar estado de todos los pods en el namespace
kubectl get pods -n ionflow-shipedge

# Verificar pods en detalle (sin CrashLoopBackOff ni Error)
kubectl describe pods -n ionflow-shipedge | grep -A5 "State:"
```

### Acceso a Vistas del Servidor

- [ ] Acceder a `app.ionflow.io` — Login SSO debe estar disponible
- [ ] Navegar a `/` — Dashboard o pantalla de login operacional
- [ ] Navegar a `/telescope` — Verificar que los jobs están ejecutándose sin errores
- [ ] Crear un Board de prueba y agregar un nodo Scheduler
- [ ] Validar que no haya errores `500` o `502` en ninguna vista

### Reactivación del Tráfico

- [ ] Remover el bloqueo de tráfico al dominio de producción
- [ ] Confirmar que las peticiones llegan correctamente a los servicios (logs de ingress)
- [ ] Verificar que el CDN de WebComponents (`ionbeta.js`) responde con la nueva versión

---

## Testing Post-Despliegue — Nivel de Riesgo Alto

> Esta release es de **Alto Riesgo** — primera vez en producción. Ejecutar **smoke matrix completa**.

Referencia: [`knowledge/releases/v0.1.0/smoke-matrix.md`](../smoke-matrix.md)

### Checklist mínimo del Scrum Master

- [ ] Login SSO funcional con Keycloak (SM-001, SM-002)
- [ ] Crear Board nuevo — URL se actualiza correctamente (SM-004)
- [ ] Agregar nodo Scheduler al canvas y configurarlo (SM-007)
- [ ] Ejecutar flow en modo Development — output visible (SM-012)
- [ ] Activar flow a modo Production — aparece en Telescope (SM-013)
- [ ] Ver historial de ejecuciones — logs por nodo visibles (SM-015)
- [ ] Acceder al Marketplace de GRAPPs (SM-023)
- [ ] Crear template PDF nuevo (SM-027)
- [ ] Verificar bugs críticos activos: SM-R-001 al SM-R-006

---

## Monitoreo

### Ventana de Monitoreo

| Campo | Valor |
|-------|-------|
| **Duración** | Mínimo **48 horas** post-despliegue |
| **Responsable** | Scrum Master |
| **Canal de reporte** | Canal de equipo |

### Checklist de Monitoreo

**Cada hora (primeras 6 horas):**

```bash
# Revisar logs del pod gateway
kubectl logs <pod-gateway> -n ionflow-shipedge --tail=100

# Revisar logs del pod flow-binaries
kubectl logs <pod-flow-binaries> -n ionflow-shipedge --tail=100

# Verificar que todos los pods siguen Running
kubectl get pods -n ionflow-shipedge
```

- [ ] Sin errores críticos en logs (500, panic, connection refused)
- [ ] Telescope: sin excepciones no controladas recurrentes
- [ ] Schedules y queue workers activos y ejecutándose en horario

**Cada 4 horas (siguientes 42 horas):**

- [ ] Revisar Telescope para patrones de errores
- [ ] Validar rendimiento (tiempos de respuesta)
- [ ] Confirmar que los jobs de flows se ejecutan correctamente
- [ ] Verificar que no hay colas de Redis bloqueadas:

```bash
# Si hay colas bloqueadas, dentro del POD de gateway:
php artisan queue:restart
```

### Métricas a Validar

| Métrica | Criterio de Éxito |
|---------|-------------------|
| **Telescope** | Sin excepciones no controladas recurrentes |
| **Base de datos** | Sin errores de conexión. Sin queries lentas (> 5s) |
| **Jobs / Flows** | Ejecución correcta y a tiempo según schedules |
| **Auth / Keycloak** | Login funcional. Refresh token renovándose sin errores |
| **CDN WebComponents** | `ionbeta.js` e `ionalpha.js` cargando desde CDN de Shipedge |
| **Pods Kubernetes** | Todos en estado `Running` en namespace `ionflow-shipedge` |
| **Health check Go** | `GET /api/ok` → `200 OK` |

---

## Escalado de Problemas

Si se detectan problemas durante el monitoreo:

1. **Documentar con exactitud:**
   - Timestamp del problema
   - Descripción del error
   - Logs relevantes (kubectl logs o Telescope)
   - Impacto en usuarios (módulo afectado, cantidad de usuarios)

2. **Determinar severidad:**
   - 🔴 **Crítico** — Login no funciona, flows no ejecutan, datos corruptos → **Rollback inmediato**
   - 🟠 **Alto** — Módulo específico no funciona, workaround disponible → Evaluar rollback
   - 🟡 **Normal** — Error cosmético o comportamiento menor → Documentar, sin rollback

3. **Comunicar al equipo** por el canal oficial con el nivel de severidad y plan de acción

---

## Rollback

### Procedimiento de Rollback

> Esta es la primera release a producción. No existe tag anterior activo. El rollback implica regresar al estado de staging.

### En `gateway` (PHP / Laravel)

```bash
# 1. Redirigir tráfico de vuelta al ambiente de staging temporalmente

# 2. Dentro del POD (si el problema es de código):
git checkout <commit-estable-anterior>
# o revertir a rama DEVELOPMENT si es necesario

# 3. Restaurar la base de datos desde backup realizado en Fase 0
# (ejecutar con el DBA autorizado desde el servidor de BD)

# 4. Ejecutar comandos de actualización si la BD fue parcialmente migrada
php artisan migrate --force
php artisan config:clear
php artisan queue:restart
```

### En `flow_binaries` (Go)

```bash
# Revertir el tag de imagen en el repositorio GitOps al commit anterior
# El cluster Kubernetes actualizará el deployment automáticamente

# Verificar que el pod anterior levanta:
kubectl get pods -n ionflow-shipedge | grep flow-binaries

# Health check
curl -f http://<service-host>:<PORT>/api/ok
```

### En `gateway-ion` y `webcomponents-flow` (Frontend / CDN)

```bash
# Redeployar el build del commit anterior a producción
# Para webcomponents: restaurar la versión anterior de ionbeta.js / ionalpha.js en el CDN de Shipedge
```

### Checklist de Rollback

- [ ] Tráfico detenido al dominio de producción
- [ ] Base de datos restaurada desde backup (si se hicieron migraciones)
- [ ] Pods del cluster revertidos a versión anterior
- [ ] Ambiente de rollback validado y funcional
- [ ] Tráfico restaurado al ambiente de rollback

### Comunicación Post-Rollback

- [ ] Informar al equipo que se realizó rollback (canal de equipo)
- [ ] Documentar la causa raíz del problema con timestamps exactos
- [ ] Crear tickets en ClickUp para análisis post-mortem
- [ ] Replanificar el despliegue cuando se resuelva el problema

---

## Notas Importantes

> **Variables de entorno:** Mantener actualizado el Google Sheets con las variables de entorno de cada versión. El archivo `.env.gitlab` (gateway) y `.env.example` (flow_binaries, gateway-ion, webcomponents-flow) son las fuentes de referencia de los repos.

> **Node Signature:** El valor `NODE_SIGNATURE=ion` debe ser **idéntico** en `gateway` y `flow_binaries`. Es el identificador de los nodos internos del motor.

> **Keycloak:** Los valores `KEYCLOAK_ENDPOINT`, `KEYCLOAK_REALM`, `KEYCLOAK_CLIENT_ID` y `KEYCLOAK_REALM_PUBLIC_KEY` deben ser **exactamente iguales** en `gateway` y `flow_binaries`. Una discrepancia rompe el flujo de autenticación SSO.

> **CI/CD:** El repo `flow_binaries` tiene pipeline automático en GitLab CI que dispara el deploy al push en `v0.1.0`. Verificar que el pipeline completó exitosamente antes de continuar con las fases siguientes.

> **Monitoreo:** No omitir las 48 horas de monitoreo. Esta es la primera release a producción y cualquier comportamiento anómalo debe ser documentado.

> **Rollback:** El backup de base de datos realizado en Fase 0 es la única red de seguridad para la BD. Asegurarse de que sea exitoso **antes** de ejecutar las migraciones.

---

## Tickets Incluidos en esta Versión (v0.1.0)

**Total:** 188 tickets | **Ramas revertidas:** IONF-1049, IONF-1030 (no incluidas en este release)

| Categoría | Cantidad |
|-----------|----------|
| Nuevas Funcionalidades | 72 |
| Correcciones (Bugs) | 34 |
| Mejoras | 30 |
| Cambios Internos / Research | 52 |
| **Total** | **188** |

**Tickets de QA activos — verificar resolución antes del go-live:**

| Ticket | Descripción | Prioridad |
|--------|-------------|-----------|
| `IONF-1147` | Cambiar email de cuenta genera error que rompe la cuenta | 🔴 urgent |
| `IONF-1145` | No se pueden desactivar webhooks custom | 🔴 urgent |
| `IONF-1144` | No se puede crear Board después de crear cuenta nueva | 🔴 urgent |
| `IONF-1108` | Migración de flow a global retorna error 500 | 🔴 urgent |
| `IONF-1123` | Nodo PDF no habilita mapeo hasta abrir y guardar modal | 🔴 urgent |
| `IONF-1143` | FlowPilot no reconoce nodo PDF Template | 🟠 high |

> ⚠️ **No hacer go-live si alguno de los tickets `urgent` sigue abierto.**

---

*Generado por ionflow-qa-catalyst — Protocolo de Despliegue v0.1.0*
*Fecha: 2026-06-30 | Repos verificados localmente*
