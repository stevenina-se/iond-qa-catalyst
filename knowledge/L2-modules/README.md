# L2 — Módulos de Ionflow

> Cada subdirectorio contiene el conocimiento de nivel 2 para un módulo del proyecto.

## Instrucciones

### Crear un módulo nuevo
1. Copia `_template.md` al nuevo directorio: `<modulo>/module.md`
2. Activa el skill `knowledge/update-module` o rellena manualmente
3. El agente leerá los repos fuente para poblar el contexto
4. El QA Engineer valida y enriquece con conocimiento de dominio

### Módulos disponibles

| Módulo | Estado | Descripción |
|--------|--------|-------------|
| `accounts/` | ✅ Activo | Gestión de cuentas asociadas a Companies |
| `auth/` | 📝 Pendiente (Fase 5) | Autenticación y gestión de usuarios |
| `billing/` | 🚧 En construcción | Suscripciones, planes y pagos vía Stripe (Fase 1: `86dzbhzdm`) |
| `flows/` | 📝 Pendiente (Fase 5) | Gestión y ejecución de flows |
| `nodes/` | 📝 Pendiente (Fase 5) | Core de nodos y su configuración |
| `connectors/` | 📝 Pendiente (Fase 5) | Conectores con apps externas |

### Fuentes de contexto

Los módulos se construyen leyendo estos repos (solo lectura):
- `../flow_binaries` — APIs, lógica, migraciones
- `../gateway-ion` — Rutas, vistas, componentes, stores
- `../webcomponents-flow` — Canvas, nodos visuales
- `../gateway` — Auth, legacy
- `../bot-test` — Tests E2E existentes

### Retroalimentación post-release

Después de cada release, usar el skill `knowledge/update-module` para:
- Diff el repo fuente vs el L2 actual
- Actualizar rutas, endpoints, componentes que cambiaron
- Agregar edge cases descubiertos como bugs
- Referenciar nuevos tests E2E creados
