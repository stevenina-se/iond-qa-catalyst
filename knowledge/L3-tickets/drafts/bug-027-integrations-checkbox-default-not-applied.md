# QA FOUND ISSUE ESCALATION REPORT — GATEWAY WEBCOMPONENTS

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | Integrations — Webcomponents Flow |
| Path | Company > Integrations > ShopifyV2 > Update Tracking |
| Versión | webcomponents-flow main · gateway v1.4.12 |

## Título

**Integrations — CheckboxForm no aplica default del seeder y genera estado engañoso en UI**

## Description of the validated/replicated problem

El componente `CheckboxForm.vue` del proyecto webcomponents-flow no respeta los valores `default` declarados en los params del seeder al renderizarse por primera vez dentro de un `ResourceForm`. Esto produce un bug con dos manifestaciones encadenadas:

1. **Primera carga**: El checkbox aparece desmarcado aunque el param declare `"default": "email_notify"`.
2. **Después del primer Save**: La vista se recarga y el checkbox aparece como checked, pero el valor NO fue persistido en la base de datos. La UI muestra un estado engañoso — el usuario ve el checkbox marcado y asume que la feature está activa, cuando en realidad el backend no tiene el valor.
3. **Solo después de interactuar manualmente** con el checkbox (descheck + recheck) y guardar, el valor se persiste correctamente.

El bug afecta específicamente al campo `fulfillment_email_notify` del resource `update_tracking` en integraciones ShopifyV2, pero **cualquier checkbox con `true_value` custom** dentro de un `ResourceForm` tiene el mismo problema.

El impacto en producción es que nuevas tiendas Shopify no envían email de notificación de fulfillment al hacer Update Tracking, ya que el backend lee el campo como `false` al no existir en la configuración.

## Steps to Reproduce

### Escenario A — Checkbox no checked y valor no persistido

1. Company Login > Sidebar: Integrations
2. Instalar una nueva integración ShopifyV2 (cualquier tienda)
3. Observar la sección **Update Tracking** — el checkbox "Fulfillment Email Notify" aparece **desmarcado** ❌ (debería estar checked por su default `"email_notify"`)
4. Marcar **solo** el toggle "Sync Update Tracking" para habilitar el proceso (NO tocar el checkbox de fulfillment)
5. Click en **Save Changes**
6. Verificar el campo `configuration` de la integración en la base de datos
7. Observar que `filters.update_tracking` **no contiene** la clave `fulfillment_email_notify`

### Escenario B — UI muestra checked pero valor NO está en BD (estado engañoso)

8. Después del Save del Escenario A, la vista se recarga
9. El checkbox "Fulfillment Email Notify" ahora **aparece como checked** ✅ en la UI
10. **SIN EMBARGO**, el valor `fulfillment_email_notify` **NO existe** en `configuration.filters.update_tracking` en la base de datos
11. El usuario cree que la feature está activa, pero el backend no la tiene registrada → **no se envía email de fulfillment al cliente**

### Escenario C — Fix manual (workaround)

12. Desmarcar y volver a marcar el checkbox "Fulfillment Email Notify" manualmente
13. Click en **Save Changes**
14. Verificar que ahora `filters.update_tracking` SÍ contiene `"fulfillment_email_notify": "email_notify"` en la BD

## Datos utilizados

- Rol: Company User
- Entorno: Producción — gateway.shipedge.com
- Tienda de prueba: qa5test56.myshopify.com
- Integration ID: 479
- Gateway Key: 1f5106c7-e6f7-48c7-ad8a-81de31ad6e95
- App: shine1 (app_id: 93)
- Param del pivot:
```json
{
  "name": "fulfillment_email_notify",
  "type": "checkbox",
  "label": "Fulfillment Email Notify",
  "default": "email_notify",
  "true_value": "email_notify",
  "false_value": null
}
```

## Current Behavior

El bug tiene dos manifestaciones encadenadas:

1. **Primera carga**: El checkbox "Fulfillment Email Notify" aparece **desmarcado** aunque el param declare `default: "email_notify"`.
2. **Después del primer Save** (habilitando solo el toggle de update_tracking): La vista se recarga y el checkbox **aparece como checked**, pero el valor **no fue persistido** en la BD. La UI miente — el usuario ve el checkbox marcado y asume que la feature está activa, cuando en realidad el backend no tiene el valor y no envía emails de fulfillment.
3. **Solo después de interactuar manualmente** con el checkbox (descheck + recheck) y guardar, el valor se persiste correctamente.

### Evidencia Técnica

#### `[CONFIRMADA]` — CheckboxForm.vue (causa raíz)

**Archivo**: `webcomponents-flow/src/gateway/components/ui/Checkbox/CheckboxForm.vue` — **Línea 47-53**

```js
const {
  handleBlur,
  checked,
  handleChange,
} = useField(name, undefined, {
  type: 'checkbox',
  checkedValue: props.true_value,    // "email_notify"
  syncVModel: true,
  uncheckedValue: props.false_value, // null
  initialValue: props.modelValue,    // ← SIEMPRE undefined
});
```

**Problema**: `initialValue: props.modelValue` siempre es `undefined` porque `ResourceForm` **nunca pasa** `v-model` ni `:modelValue` al `CheckboxForm`:

**Archivo**: `webcomponents-flow/src/gateway/components/integrations/components/ResourceForm.vue` — **Líneas 188-195**

```html
<CheckboxForm
  v-if="value.type === 'checkbox'"
  :name="value.name"
  :label="value.label ?? value.name"
  :true_value="value.true_value"
  :false_value="value.false_value"
  :tooltip="value?.description"
/>
<!-- ❌ No se pasa :modelValue ni v-model -->
```

En vee-validate v4, pasar `initialValue: undefined` al `useField` con `type: 'checkbox'` **tiene prioridad** sobre los `initial-values` del componente `<Form>` padre. Esto causa que:
- El valor del field sea `undefined` (no `"email_notify"`)
- `checked` se evalúa como `false` (porque `undefined !== "email_notify"`)
- `getValues()` retorna `undefined` para ese campo
- `JSON.stringify` elimina claves con valor `undefined`

#### `[CONFIRMADA]` — parseFormData SÍ resuelve el default correctamente

**Archivo**: `webcomponents-flow/src/gateway/components/integrations/components/ResourceSettings.vue` — **Líneas 276-287**

```js
function parseFormData(params, raw) {
  if (!raw) return {};
  if (params.length === 0) return {};
  const data = {};
  params.forEach((param) => {
    data[param.name] = raw[param.name] ?? getDefault(param);
  });
  return data;
}
```

**Archivo**: `webcomponents-flow/src/gateway/lib/schema.ts` — **Líneas 290-294**

```js
export function getDefault(param) {
  if (param.default === undefined) return undefined;
  if (typeof param.default === 'string') return resolveDateToken(param.default);
  return param.default;
}
```

Para una integración nueva: `raw["fulfillment_email_notify"]` → `undefined` → `getDefault(param)` → `"email_notify"`. El `formData` queda correcto como `{ fulfillment_email_notify: "email_notify" }` y se pasa al `<Form :initial-values>`. **Sin embargo, CheckboxForm lo ignora** porque su `initialValue: undefined` tiene prioridad.

#### `[CONFIRMADA]` — Payload del primer Save (sin interactuar con el checkbox)

```json
{
  "update_tracking": {
    "subscriptions": {},
    "status": true
  }
}
```
❌ No hay clave `fulfillment_email_notify`.

#### `[CONFIRMADA]` — Payload del segundo Save (tras descheck + recheck manual)

```json
{
  "update_tracking": {
    "fulfillment_email_notify": "email_notify",
    "subscriptions": {},
    "status": true
  }
}
```
✅ La clave aparece solo después de interacción manual.

#### `[CONFIRMADA]` — Impacto en backend

**Archivo**: `gateway/app/Classes/Shopifyv2/UpdateTracking/UpdateTrackingGraphql.php` — **Línea 29**

```php
$this->notifyEmail = ($configuration['filters']['update_tracking']['fulfillment_email_notify'] ?? false) ? true : false;
```

Sin la clave en los filters → `?? false` → `notifyEmail = false` → **no se envía email de fulfillment al cliente de la tienda Shopify**.

## Expected Behavior

1. Al abrir una nueva integración ShopifyV2, el checkbox "Fulfillment Email Notify" debe aparecer **marcado** (checked), reflejando el `default: "email_notify"` declarado en el param.
2. Al hacer Save por primera vez (sin tocar el checkbox), el payload debe incluir `"fulfillment_email_notify": "email_notify"` en `filters.update_tracking`.
3. El backend debe recibir el valor y activar las notificaciones por email de fulfillment por defecto.
4. El estado de la UI debe ser consistente con lo que está persistido en la BD.

## Impacto

- **Usuarios afectados**: Todos los clientes que instalen una nueva integración ShopifyV2
- **Flujo afectado**: Update Tracking — notificación por email de fulfillment al consumidor final
- **Alcance del bug**: No es exclusivo de `fulfillment_email_notify` — **cualquier checkbox con `true_value` custom** usado dentro de `ResourceForm` (sin `v-model`) tiene el mismo problema. Otros checkboxes potencialmente afectados:
  - `archive_order` (get_orders) — `true_value: "archive_order"`
  - Cualquier futuro checkbox con `true_value` string
- **Estado engañoso**: La UI muestra el checkbox como checked después del primer Save, pero el valor no está en la BD. Esto genera falsa confianza en el usuario.

## Notas Adicionales

**[Hipótesis técnica]**: El fix más conservador es modificar `CheckboxForm.vue` para no pasar `initialValue` cuando `modelValue` es `undefined`, permitiendo que el `<Form :initial-values>` del padre surta efecto:

```js
...(props.modelValue !== undefined ? { initialValue: props.modelValue } : {}),
```

Esto no afecta los casos donde `CheckboxForm` se usa con `v-model` (ya que `modelValue` sería explícito), y sí arregla todos los casos donde se usa dentro de `ResourceForm` / `ServiceInstallForm` sin binding directo.

**Tests existentes**: Los tests en `schema.spec.ts` (líneas 262-316) ya cubren la validación de `true_value`/`false_value` para checkboxes, pero no testean el flujo de inicialización del componente.

## Categorización

- 📊 Prioridad: **high** — afecta el flujo principal de Update Tracking para todas las nuevas integraciones ShopifyV2. Sin workaround automático. Genera estado engañoso en la UI que puede pasar desapercibido.
- 🏷️ Tipo: **bug** — comportamiento incorrecto: el default declarado en el param no se aplica, el valor no se persiste, y la UI muestra un estado inconsistente con la BD.

---

## Hallazgo adicional — Email no mapeado en ShopifyV2

Durante la investigación se detectó que el campo `eMail` en el mapeo de órdenes de ShopifyV2 está hardcodeado a string vacío tanto en `shippingAddress` como en `billingAddress`.

### Evidencia Técnica

#### `[CONFIRMADA]` — Shopifyv2.php (mapOrder)

**Archivo**: `gateway/app/Classes/Shopifyv2/Shopifyv2.php` — **Líneas 206 y 222**

```php
// Línea 206
$order->shippingAddress->eMail = '';

// Línea 222
$order->billingAddress->eMail = '';
```

Shopify provee el email del cliente a nivel de orden (`$orderOnShopify->email` y/o `$orderOnShopify->contact_email`), pero el mapeo nunca lo asigna a los campos de dirección. Esto causa que las órdenes importadas lleguen sin email del cliente en la información de shipping y billing.

> **Nota**: Este hallazgo puede ameritar un ticket separado ya que es un problema diferente al bug del checkbox.
