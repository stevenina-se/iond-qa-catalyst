Estimado @Alex Chura

**El resultado de pruebas para este ticket es: APROBADO ✅**


### 💡 ¿Por qué es importante?

- **Cumplimiento regulatorio de Shopify**: A partir del **1 de enero de 2027**, Shopify rechazará con error responses todas las API calls (REST y GraphQL Admin API) que usen tokens no-expirables. Sin este cambio, **todas las integraciones Shopify de Sfipedge dejarían de funcionar** para todos los clientes con el canal Shopify configurado.

- **Continuidad operacional**: El refresh automático transparente (`ShopifyTokenRefresher`) asegura que los background jobs de sincronización (órdenes, productos, inventario, tracking) continúen operando sin interrupción. Los tokens expiran cada hora; sin refresh automático, los syncs fallarían cada hora.

- **Migración controlada**: El mecanismo de re-autorización manual vía UI + seeder de migración masiva permite una transición progresiva y segura de todas las integraciones existentes antes del deadline.

---

### 🎯 Criterios de Aceptación (AC) Clave Validados

#### **AC-1. Nuevas instalaciones con expiring tokens por defecto**
* **Validación realizada**: Instalación de nueva integración Shopify vía flujo OAuth completo.
* **Comportamiento observado**: El response incluyó `access_token`, `expires_in` (3600s), `refresh_token`, y `refresh_token_expires_in` (7776000s = 90 días), todos almacenados correctamente en BD.

#### **AC-2. Refresh automático de tokens antes de API calls**
* **Validación realizada**: Ejecución de syncs con token próximo a expirar (>50% del TTL consumido).
* **Comportamiento observado**: `ShopifyTokenRefresher` detectó la expiración, ejecutó el refresh con cache lock atómico, obtuvo nuevos tokens, los persistió en BD, y completó la API call sin interrupción visible al usuario.

#### **AC-4. Re-autorización manual para integraciones existentes**
* **Validación realizada**: Acceso a configuración de integración Shopify existente con token no-expirable.
* **Comportamiento observado**: Banner naranja de alerta visible en primera tarjeta Settings con texto "Shopify requires re-authorization. Integrations that are not re-authorized will stop working after January 1, 2027." y botón "Re-Authorize" que inició flujo OAuth exitosamente.

#### **AC-5. Manejo de refresh token expirado**
* **Validación realizada**: Simulación de refresh token expirado (>90 días).
* **Comportamiento observado**: Sistema detectó que el refresh token expiró, persistió `refresh_token_status: 401` en configuración, y presentó alerta de re-autorización sin crashes ni errores silenciosos.

#### **AC-8. Visibilidad condicional — solo integraciones existentes**
* **Validación realizada**: Verificación de banner en integración nueva vs existente.
* **Comportamiento observado**: Integración nueva (con `refresh_token` en configuración) no muestra banner; integración existente (sin `refresh_token`) sí lo muestra. Lógica: `service.type === 'SHOPIFYV2' && !configuration.refresh_token`.

---

### 🔄 Pruebas de Regresión
- **Integración Shopify existente (REG-001)**: Syncs funcionan correctamente con tokens legacy pre-deadline.
- **Vista Configured Channels (REG-002)**: Carga sin errores, todos los canales visibles y clickeables.
- **Campos de configuración Shopify (REG-003)**: Integration Name, Shop Host, Orders, Products, Tracking, Inventory — todos editables sin regresión.
- **OAuth de otros connectors (REG-004)**: Flujos OAuth de connectors no-Shopify no afectados por los cambios.
- **Flows con nodos Shopify (REG-005)**: Ejecución de flows existentes con nodos Shopify sin errores.
- **Eliminación de integración (REG-006)**: Delete de integración Shopify funciona correctamente.


La implementación cumple satisfactoriamente con todos los criterios de aceptación definidos. El flujo de re-autorización OAuth para integraciones existentes funciona correctamente, el refresh automático de tokens opera de forma transparente con protección contra concurrencia, y las nuevas instalaciones obtienen expiring tokens por defecto. La evidencia de BD confirma la integridad de los campos `expires_at`, `refresh_token` y `refresh_token_expires_at` en todos los escenarios probados. Las pruebas de regresión confirman que la funcionalidad existente no se vio afectada. El ticket queda **formalmente aprobado para merge y deploy**.

| Details | |
|---|---|
| BROWSER | Chrome |
| BRANCH | `IONF-1091` (wc-flow) / `IONF-1091-A` (gateway) |
| ENV | gateway.shipedge.com |
| TEST MATRIX | `L3-tickets/86e1y9k0f/test-matrix.md` |
| MERGE REQUEST | YES |