# COMPLIANCE / BREAKING CHANGE REPORT — SHOPIFY EXPIRING TOKENS (Sfipedge)

> Template generado por QA Catalyst
> Fecha: 2026-06-18
> QA Engineer: Steve

---

## Información General

| Campo | Valor |
|-------|-------|
| Ticket ID | **IONF-1091** |
| Módulo(s) afectado(s) | Gateway > Admin > Customer > Configured Channels > [Shopify] |
| Aplicación | Sfipedge (Public App de Shopify) |
| Entorno | Producción / Todos los entornos |
| Prioridad | `high` |
| Tipo | `task` / `compliance` |
| Deadline de Shopify | **1 de enero de 2027** |

---

## Descripción del Cambio Requerido

### Contexto

Shopify ha anunciado un cambio obligatorio en los requisitos de tokens de acceso para **aplicaciones públicas**. Revisando el panel de administración de la aplicación pública **"Sfipedge"**, se identifica el siguiente aviso:

> **Expiring token requirements for public apps**
>
> Public apps must use expiring tokens for offline access. Public apps created on or after April 1, 2026 must use expiring tokens, and public apps created before April 1, 2026 must migrate to expiring tokens by January 1, 2027. Starting January 1, 2027, public apps that make REST or GraphQL Admin API requests with non-expiring tokens receive error responses. These requirements don't apply to custom apps or apps created by merchants.

---

## Current Behavior (Comportamiento Actual)

Al inspeccionar el flujo de autenticación OAuth de **Sfipedge** con Shopify:

1. **Tokens no expirables en uso**: La app actualmente solicita y almacena **offline access tokens sin expiración** (`shpat_xxx`). El response del endpoint `/admin/oauth/access_token` **no retorna** los campos `expires_in`, `refresh_token`, ni `refresh_token_expires_in`.

2. **Sin lógica de refresh**: No existe mecanismo de refresh de tokens. El token se obtiene una vez durante la instalación del merchant y se reutiliza indefinidamente sin renovación.

3. **Sin campos de expiración en BD**: La base de datos de sesiones/tokens **no almacena** `expires_at`, `refresh_token`, ni `refresh_token_expires_at` — porque el token actual no expira.

4. **Background jobs sin validación de token**: Los jobs de sincronización (productos, órdenes, inventario) usan el token almacenado directamente, sin verificar si es válido o si ha expirado.

5. **Panel de administración de Shopify muestra alerta**: Al acceder al panel de la app pública "Sfipedge" en Shopify Partners, se muestra el aviso de **"Expiring token requirements for public apps"** indicando que la app debe migrar antes del 1 de enero de 2027.

**Evidencia observada**: Hoy (18 de junio de 2026), la app funciona normalmente con tokens no-expirables. Pero a partir del **1 de enero de 2027**, Shopify rechazará estos tokens con error responses en todas las llamadas a REST y GraphQL Admin API.

---

## Expected Behavior (Comportamiento Esperado)

Después de implementar el cambio:

1. **Nuevas instalaciones**: Al instalar Sfipedge en una tienda Shopify, el flujo OAuth debe solicitar **expiring offline access tokens**. El response debe incluir `access_token`, `expires_in` (3600s), `refresh_token`, y `refresh_token_expires_in` (7776000s = 90 días).

2. **Refresh automático**: Antes de cualquier API call a Shopify (especialmente en background jobs/syncs), la app debe verificar si el `access_token` ha expirado y ejecutar el flujo de refresh usando el `refresh_token`. El nuevo `access_token` y `refresh_token` deben almacenarse en BD.

3. **BD actualizada**: La tabla de tokens/sesiones debe contener los campos `expires_at`, `refresh_token`, y `refresh_token_expires_at` con valores correctos y actualizados después de cada refresh.

4. **Migración de tokens existentes**: Los merchants con tokens no-expirables existentes deben ser migrados al esquema de tokens expirables vía token exchange (`grant_type=urn:ietf:params:oauth:grant-type:token-exchange`). Verificar que el token viejo queda **revocado** y el nuevo funciona correctamente.

5. **Manejo de expiración del refresh token**: Si el `refresh_token` expira (>90 días sin actividad), la app debe detectar este estado y solicitar al merchant que re-autorice la app, sin crashear ni generar errores silenciosos.

6. **Sin interrupción de servicio**: Todas las sincronizaciones (productos, órdenes, inventario) deben continuar funcionando sin interrupción después de la migración, usando los nuevos tokens expirables.

7. **Compatibilidad post-deadline**: A partir del 1 de enero de 2027, **ningún** API call de Sfipedge debe usar tokens no-expirables. Verificar que no quedan tokens legacy en producción.

---

### Impacto si no se actúa

A partir del **1 de enero de 2027**, cualquier request de la API de Admin (REST o GraphQL) hecho con tokens **no expirables** recibirá **respuestas de error**. Esto significa que la integración de Sfipedge con Shopify **dejará de funcionar completamente** para todos los customers que tengan el canal Shopify configurado.


## Documentación de Referencia

- **URL oficial de Shopify**: [About offline access tokens](https://shopify.dev/docs/apps/build/authentication-authorization/access-tokens/offline-access-tokens)

### Resumen Técnico de la Documentación

#### Tokens Expirables (Expiring Offline Access Tokens)

Los tokens expirables de offline access incluyen:

| Campo | Descripción |
|-------|-------------|
| `access_token` | Token de acceso con prefijo `shpat_`. Expira según `expires_in`. |
| `expires_in` | Tiempo de expiración en segundos (por defecto **3600** = 1 hora). |
| `refresh_token` | Token de refresh con prefijo `shprt_`. Sirve para renovar el access token. |
| `refresh_token_expires_in` | Tiempo de expiración del refresh token (**7776000** segundos = ~90 días). |
| `scope` | Los scopes otorgados por el merchant. |

#### Flujo de Refresh de Tokens

Para renovar un token expirado, se hace un POST a:
```
POST https://{shop}.myshopify.com/admin/oauth/access_token
```

Con los parámetros:
- `client_id` — API key de la app
- `client_secret` — Client secret de la app
- `grant_type` = `refresh_token`
- `refresh_token` — El refresh token almacenado

#### Comportamiento del Refresh

- **Nuevos tokens en cada refresh**: Shopify retorna un nuevo access token Y un nuevo refresh token.
- **Expiración extendida**: El nuevo refresh token tiene una nueva expiración de 90 días desde el momento del refresh.
- **Token retirado**: El access token anterior sigue válido hasta su expiración, pero se debe usar el nuevo para nuevos requests.
- **Uso único del refresh token**: Shopify invalida el refresh token anterior después de usarlo. Si la app no recibe respuesta, debe reintentar inmediatamente con el mismo refresh_token (hay una ventana corta de reintento).

> ⚠️ **CAUTION**: Si el refresh token expira (después de 90 días sin uso), el usuario de la app necesita relanzar la app para que se inicie el flujo de adquisición de token.

#### Migración de Tokens No-Expirables a Expirables

Shopify provee un mecanismo de **token exchange** para migrar tokens existentes:

**Pasos de migración:**

1. **Actualizar el almacenamiento de sesión** de la app para incluir:
   - `expires_at` — Cuándo expira el access token
   - `refresh_token` — El valor del refresh token
   - `refresh_token_expires_at` — Cuándo expira el refresh token

2. **Implementar lógica de token refresh** — antes de hacer API requests (especialmente en background jobs), verificar si el token ha expirado y refrescarlo si es necesario.

3. **Solicitar tokens expirables para nuevas instalaciones** — agregar `&grant_options[]=per-user` o el parámetro `expiring=1` al flujo de OAuth.

4. **Migrar tokens existentes** vía token exchange:
   ```
   POST https://{shop}.myshopify.com/admin/oauth/access_token
   ```
   Con parámetros:
   - `client_id` (required)
   - `client_secret` (required)
   - `grant_type` = `urn:ietf:params:oauth:grant-type:token-exchange`
   - `subject_token` = token offline no-expirable actual
   - `subject_token_type` = `urn:shopify:params:oauth:token-type:offline-access-token`
   - `requested_token_type` = `urn:shopify:params:oauth:token-type:offline-access-token`
   - `expiring` = `1`

> ⚠️ **CAUTION**: El token no-expirable original será **revocado** tras el exchange exitoso. Esta migración es **irreversible**. Para obtener un nuevo token offline no-expirable, la app tendría que re-ejecutar el flujo de adquisición con interacción del merchant.

---

## Acceptance Criteria Propuestos

- [ ] AC 1: La aplicación Sfipedge debe solicitar **tokens expirables** (expiring offline access tokens) en nuevas instalaciones de la app.
- [ ] AC 2: La aplicación debe implementar lógica de **refresh automático** del access token antes de que expire (~1 hora).
- [ ] AC 3: La aplicación debe almacenar de forma segura el `refresh_token`, `expires_at`, y `refresh_token_expires_at` en la base de datos.
- [ ] AC 4: Se debe implementar un mecanismo de **migración** de tokens existentes (no-expirables) a tokens expirables usando el endpoint de token exchange de Shopify.
- [ ] AC 5: La aplicación debe manejar el caso edge donde el refresh token expira (>90 días sin actividad) y el merchant debe re-autorizar la app.
- [ ] AC 6: Todos los requests a la API de Admin de Shopify (REST y GraphQL) deben funcionar correctamente con tokens expirables antes del **1 de enero de 2027**.
- [ ] AC 7: Se debe implementar manejo de errores robusto para el flujo de refresh (reintentos, logging, fallback a re-autorización).

---

## Áreas de Impacto / Risk Assessment

| Área | Riesgo | Detalle |
|------|--------|---------|
| Integración Shopify (OAuth) | 🔴 Crítico | Cambio en el flujo de autenticación — debe soportar tokens expirables |
| Base de Datos | 🟠 Alto | Nuevos campos para almacenar refresh_token y metadata de expiración |
| Background Jobs / Syncs | 🔴 Crítico | Todos los jobs que hacen API calls a Shopify deben verificar y refrescar el token antes de cada operación |
| Migración de datos | 🟠 Alto | Los tokens existentes de todos los customers deben migrarse de forma controlada |
| UX / Merchant Experience | 🟡 Medio | Si el refresh token expira (90 días sin uso), el merchant deberá re-autorizar — debe haber notificación/UX clara |
| Rollback | 🔴 Crítico | La migración de tokens es **irreversible** — no se puede volver a tokens no-expirables una vez migrados |

---

## Timeline

| Hito | Fecha |
|------|-------|
| Anuncio de Shopify | Ya activo |
| Apps nuevas (post abril 2026) deben usar expiring tokens | 1 de abril de 2026 |
| **Deadline para migración de apps existentes** | **1 de enero de 2027** |
| Tokens no-expirables dejan de funcionar | 1 de enero de 2027 |
| Fecha actual | 18 de junio de 2026 |
| **Tiempo restante** | **~6 meses** |

---

## Módulos Afectados en Ionflow

| Módulo | Impacto |
|--------|---------|
| `Gateway > Admin > Customer > Configured Channels > [Shopify]` | Principal — configuración del canal |
| Sfipedge (Backend de la public app) | Toda la lógica de OAuth y API calls |
| Sincronización de productos, órdenes, inventario | Todos los background jobs que usan la API de Shopify |
| Base de datos de tokens/sesiones | Schema update para nuevos campos |

---

## Notas Adicionales

- Este cambio **no aplica a custom apps ni apps creadas por merchants** — solo afecta a **public apps** como Sfipedge.
- Se recomienda implementar primero en un entorno de staging con una tienda de desarrollo de Shopify antes de migrar tokens de producción.
- Considerar implementar un mecanismo de migración gradual (por customer) en lugar de migrar todos los tokens simultáneamente, dado que la migración es irreversible.
- Es altamente recomendable implementar **logging detallado** durante la migración para poder rastrear cualquier issue.
- Evaluar si el SDK/librería de Shopify que se usa actualmente ya soporta tokens expirables out-of-the-box o si requiere actualización.
- Referencia técnica completa: https://shopify.dev/docs/apps/build/authentication-authorization/access-tokens/offline-access-tokens
