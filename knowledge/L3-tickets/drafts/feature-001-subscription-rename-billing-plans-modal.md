# QA FOUND ISSUE ESCALATION REPORT — IOND

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | Billing / User Profile |
| Path | User Profile Menu > Subscription |
| Versión | gateway-ion (actual) |

## Description of the validated/replicated problem

En el menú desplegable del perfil de usuario, la opción de suscripción/facturación aparece con el label **"Subscription"** cuando debería decir **"Billing"**. Adicionalmente, dentro de la vista de Subscription existe un botón **"Planes"** que al hacer click navega a una vista separada de planes, cuando el comportamiento esperado es que abra un **modal** con la información de planes sin salir de la vista actual. El botón "Planes" dentro de la vista no debería existir como navegación directa; su función debe limitarse a abrir un modal overlay.

## Steps to Reproduce

1. Login > Click en el avatar / ícono de perfil (esquina superior derecha)
2. Observar que la opción del menú dice **"Subscription"** → ❌ debería decir **"Billing"**
3. Click en "Subscription" para acceder a la vista
4. Dentro de la vista, localizar el botón **"Planes"**
5. Click en el botón "Planes"
6. Observar que se navega a una vista separada de planes → ❌ debería abrir un modal

## Datos utilizados

- Rol: Cualquier usuario autenticado con acceso a la sección de suscripción
- Entorno: Staging
- Versión: actual
- No requiere datos específicos — reproducible con cualquier cuenta

## Current Behavior

- La opción del menú de perfil muestra **"Subscription"** como label.
- Dentro de la vista de Subscription, el botón **"Planes"** navega a una vista/página separada de planes, sacando al usuario del contexto actual de facturación.

## Expected Behavior

- La opción del menú de perfil debe mostrar **"Billing"** como label.
- Al hacer click en el botón **"Planes"** debe abrirse un **modal** (overlay) con la información de planes disponibles (comparación, precios, features).
- El modal debe poder cerrarse (botón X, click fuera, tecla Escape) y regresar a la vista de Billing sin pérdida de contexto.

## Impacto

- Afecta a todos los usuarios que acceden a la sección de suscripción/billing desde el menú de perfil
- No bloqueante — la funcionalidad existe pero con nomenclatura incorrecta y UX subóptima
- Genera inconsistencia con la terminología esperada del producto

