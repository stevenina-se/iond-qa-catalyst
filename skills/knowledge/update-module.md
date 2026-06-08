# Skill: knowledge/update-module

> Retroalimenta el conocimiento L2 de un módulo después de una release, improvement o cambio en producción. Mantiene el L2 como fuente de verdad de lo que ESTÁ en producción.

## Cuándo usar este skill

- **Post-release**: Después de que un batch de tickets pasa a producción
- **Post-discovery**: Cuando el equipo toma decisiones que cambian el comportamiento de un módulo
- **Mantenimiento**: Cuando el QA Engineer detecta que el L2 está desactualizado

## Principio Fundamental

```
"El L2 de un módulo debe reflejar siempre lo que está en producción, no lo que fue planeado."
```

## Pre-requisitos

- ✅ `knowledge/L2-modules/<módulo>/module.md` — El módulo a actualizar
- ✅ Acceso de lectura al repo del módulo afectado
- ✅ Lista de tickets que se deployaron (para saber qué cambió)

---

## Instrucciones de Ejecución

### Stage 1 — PLANNING

Reporta al QA Engineer:
1. El módulo que vas a actualizar
2. Los tickets deployados que lo afectan
3. Qué secciones del L2 necesitan actualización

**Espera aprobación antes de modificar.**

### Stage 2 — EXECUTION

#### Paso 1: Identificar qué cambió

Revisa los tickets deployados y su L3:

| Ticket | Módulo | Cambio | Sección del L2 afectada |
|--------|--------|--------|------------------------|
| TASK-001 | flows | Nuevo endpoint para clonar flows | Endpoints, Rutas API |
| TASK-002 | flows | Nueva columna en tabla `flows` | Schema BD |
| TASK-003 | connectors | Nuevo tipo de connector global | Reglas de negocio |

#### Paso 2: Leer el estado actual del código

Para cada repo afectado, leer el estado actual (no el diff, sino el estado final):

```bash
# Frontend: verificar rutas actuales
cat ../gateway-ion/src/router/index.ts

# Backend: verificar endpoints actuales
find ../flow_binaries/internal/api/ -name "*.go" | head -20

# BD: verificar migraciones recientes
ls -la ../flow_binaries/migrations/ | tail -10
ls -la ../gateway/database/migrations/ | tail -10
```

#### Paso 3: Actualizar cada sección del L2

Para cada sección del `module.md`:

| Sección | Qué actualizar |
|---------|---------------|
| **Endpoints** | Agregar nuevos, actualizar payloads, marcar deprecados |
| **Rutas Frontend** | Agregar nuevas vistas, actualizar componentes |
| **Schema BD** | Agregar tablas/columnas nuevas, actualizar relaciones |
| **Reglas de negocio** | Actualizar comportamiento según decisiones del equipo |
| **Selectores E2E** | Agregar nuevos data-testid, actualizar page objects |
| **Dependencias** | Actualizar si el módulo ahora depende de otro |

#### Paso 4: Registrar el cambio

Al final del `module.md`, actualizar el historial:

```markdown
## Historial de Actualizaciones

| Fecha | Tickets | Cambios | Actualizado por |
|-------|---------|---------|----------------|
| [fecha] | TASK-001, TASK-002 | Nuevo endpoint clonar, columna en flows | QA Catalyst |
| [fecha anterior] | TASK-XXX | ... | ... |
```

### Stage 3 — REPORTING

Reporta al QA Engineer:
1. Qué secciones se actualizaron
2. Si se encontraron discrepancias entre el L2 anterior y el estado real del código
3. Si hay módulos que necesitan un L2 nuevo (no existía antes)

---

## Trigger automático

El Catalyst debe sugerir ejecutar este skill cuando:
- Se completa un `sprint-testing/report` con veredicto ✅ Approved
- Se ejecuta un `regression/decide` con veredicto 🟢 GO
- El QA Engineer indica que hubo un deploy a producción

```
Después de un Approved/GO:
  "Los tickets TASK-001 y TASK-002 fueron aprobados.
   ¿Quieres que actualice el L2 de [módulo] con los cambios?"
```

---

## Reglas de este Skill

1. **El L2 refleja producción** — No lo que fue planeado, sino lo que está deployado
2. **No eliminar información** — Marcar como deprecated, no borrar
3. **Siempre registrar el historial** — Quién actualizó, cuándo, por qué tickets
4. **Si el L2 no existe para un módulo** — Crearlo desde `_template.md`
5. **El QA Engineer aprueba antes de modificar** — El L2 es la fuente de verdad del equipo
