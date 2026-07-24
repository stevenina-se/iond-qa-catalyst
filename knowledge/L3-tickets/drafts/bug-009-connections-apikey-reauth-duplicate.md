# QA FOUND ISSUE ESCALATION REPORT — IOND

## Información General

| Campo | Valor |
|-------|-------|
| Módulo | Connections / Integrations |
| Path | Company > Connections > Reauthorize |
| Versión | gateway-ion v0.1.0 · flow_binaries v0.1.0 · gateway v2.0.0 |

## Título

**Connections — Reautorización por API Key crea conexión duplicada en lugar de sobrescribir**

## Description of the validated/replicated problem

Al realizar el proceso de reautorización de una conexión con método de autenticación API Key, el sistema crea una nueva conexión adicional en lugar de sobrescribir/actualizar la conexión existente. Adicionalmente, se emiten dos toasts de éxito de reautorización. Esto genera conexiones duplicadas en el sistema, lo que puede causar confusión y problemas de integridad de datos cuando los flows referencian la conexión original.

## Steps to Reproduce

1. Company Login > Sidebar: Connections
2. Seleccionar una conexión activa que utilice método de autenticación API Key
3. Presionar Button: "Reauthorize"
4. Completar el proceso de reautorización con la nueva API Key
5. Observar que se crea una nueva conexión en la lista (duplicada)
6. Verificar que la conexión original permanece inalterada
7. Observar que se muestran DOS toasts de éxito

## Datos utilizados

- Rol: Company User con permiso de gestión de connections
- Entorno: Staging
- Versión: v0.1.0
- Conexión con método de autenticación API Key

## Current Behavior

1. Se crea una nueva conexión extra en lugar de actualizar la existente
2. La conexión original permanece sin cambios
3. Se muestran 2 toasts de éxito
4. Los flows que referenciaban la conexión original siguen apuntando a la credencial vieja

## Expected Behavior

1. La reautorización debería actualizar (sobrescribir) las credenciales de la conexión existente
2. No debería crearse una conexión nueva
3. Se debería mostrar un único toast de éxito
4. Los flows que referencian la conexión deberían usar automáticamente las nuevas credenciales

## Impacto

- **Crítico para integridad de datos**: genera conexiones duplicadas
- Los flows que usan la conexión original no se benefician de la reautorización
- Afecta a Company Users con conexiones API Key
- Potencial acumulación de conexiones huérfanas

## Categorización

- 📊 Prioridad: **high** — afecta integridad de datos y la funcionalidad de reautorización no opera correctamente
- 🏷️ Tipo: **bug** — la reautorización debería actualizar, no crear duplicados
