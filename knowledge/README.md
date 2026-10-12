# Knowledge Base — iond-qa-catalyst

## Regla central

```
"LA IA LEE EL NIVEL CORRECTO ANTES DE REALIZAR CADA TAREA"
```

## Niveles y áreas

```
┌───────────────────────────────────────────────────────────────────┐
│  L1-project/    ¿Cómo funciona el proyecto y el proceso?          │
│                 Fuente canónica del SDLC, reglas de negocio,      │
│                 arquitectura, prioridades, mapa de subcategorías  │
│                 ⟹ Se lee SIEMPRE (la sección que aplica)          │
├───────────────────────────────────────────────────────────────────┤
│  L2-modules/    ¿Cómo funciona este módulo?                       │
│                 Rutas, endpoints, schema, reglas, specs E2E,      │
│                 impacto cruzado, edge cases                       │
│                 ⟹ Según la Iond Subcategory del ticket            │
├───────────────────────────────────────────────────────────────────┤
│  L3-tickets/    ¿Qué estoy validando ahora?                       │
│                 Matriz de Requerimientos, Matriz de Pruebas,      │
│                 evidencia, reporte, comentarios                   │
│                 ⟹ Uno por ticket activo                           │
├───────────────────────────────────────────────────────────────────┤
│  test-suites/   Smoke maestro, E2E maestro, cobertura y           │
│                 hoja de ruta de automatización                    │
│  releases/      Artefactos de cada release (<producto>/<versión>) │
│  dashboards/    Auditorías del SDLC y métricas semanales          │
└───────────────────────────────────────────────────────────────────┘
```

## Cuándo leer cada nivel

| Tarea | L1 | L2 | L3 | test-suites | releases |
|---|---|---|---|---|---|
| Matriz de Requerimientos / prototype review | ✅ | ✅ | ✅ | — | — |
| `mock testing` de un ticket | ✅ | ✅ | ✅ | — | — |
| Release (smoke, sanity, regresión, E2E) | ✅ | ✅ (módulos impactados) | ✅ (matrices de los tickets) | ✅ | ✅ |
| Automatización | ✅ | ✅ | ✅ (si viene de un ticket) | ✅ | — |
| Auditoría y métricas (SM) | ✅ | — | — | ✅ (cobertura) | ✅ |

## Reglas

1. **L1 es estable:** la fuente canónica cambia solo con una decisión del equipo; el resto, con cambios de arquitectura o de criticidad.
2. **L2 es progresivo:** se construye por módulo y se actualiza después de cada release desplegado (`skills/knowledge/update-module.md`).
3. **L3 es por ticket:** se crea en el primer contacto de QA y queda como registro histórico.
4. **Nunca inventar contexto:** si falta el L2 de un módulo, se construye primero leyendo los repos (solo lectura).
5. **Los repositorios fuente son la verdad** para el código; **ClickUp** lo es para el estado del trabajo.
