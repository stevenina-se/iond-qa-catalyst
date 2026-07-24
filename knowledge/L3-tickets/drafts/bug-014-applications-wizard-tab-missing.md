# QA FOUND ISSUE ESCALATION REPORT — IOND

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | Developer Apps |
| Path | Admin > Applications > New GRAPP |
| Versión | gateway-ion v0.1.0 · flow_binaries v0.1.0 · gateway v2.0.0 |

## Título

**Applications — Tab de configuración del Wizard de instalación ausente al crear GRAPP**

## Description of the validated/replicated problem

Al ingresar a la vista de Admin > Applications y crear un nuevo GRAPP, no se encuentra el tab de configuración del Wizard de instalación. Esta feature existía previamente y ha desaparecido, lo que sugiere una regresión. Sin el Wizard de instalación, no es posible configurar el flujo de onboarding para los GRAPPs, lo cual es una funcionalidad importante para la distribución de flows.

## Steps to Reproduce

1. Admin Login > Sidebar: Applications
2. Crear un nuevo GRAPP (o editar uno existente)
3. Observar los tabs disponibles en la configuración del GRAPP
4. Verificar que NO existe el tab de configuración del Wizard de instalación

## Datos utilizados

- Rol: Admin
- Entorno: Staging
- Versión: v0.1.0
- Cualquier GRAPP nuevo o existente

## Current Behavior

El tab de configuración del Wizard de instalación no aparece en la interfaz de configuración del GRAPP. La feature ha desaparecido.

## Expected Behavior

Debería existir un tab de configuración del Wizard de instalación que permita definir el flujo de onboarding para los GRAPPs, tal como existía en versiones anteriores.

## Impacto

- Afecta exclusivamente a usuarios Admin que crean/configuran GRAPPs
- Regresión de funcionalidad existente
- Impide configurar el flujo de instalación de GRAPPs para las companies

## Categorización

- 📊 Prioridad: **high** — regresión de funcionalidad existente, bloquea configuración de GRAPPs
- 🏷️ Tipo: **bug** — la funcionalidad existía previamente y debería estar disponible (regresión)
