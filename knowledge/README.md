# Knowledge Base — ionflow-qa-catalyst

## Regla Central

```
"LA IA LEE EL NIVEL CORRECTO ANTES DE REALIZAR CADA TAREA"
```

## Los 3 Niveles de Conocimiento

```
┌─────────────────────────────────────────────────────────────┐
│  L1-project/   →  ¿Cómo funciona el proyecto?              │
│                    Business rules, API architecture,         │
│                    Test priorities, Stack overview            │
│                    ⟹ Se lee SIEMPRE                          │
├─────────────────────────────────────────────────────────────┤
│  L2-modules/   →  ¿Cómo funciona este módulo?              │
│                    Rutas, endpoints, componentes, DB schema, │
│                    Test data, Edge cases conocidos            │
│                    ⟹ Se lee según el módulo del ticket       │
├─────────────────────────────────────────────────────────────┤
│  L3-tickets/   →  ¿Qué estoy testeando ahora?              │
│                    AC, decisiones, plan de testing,           │
│                    Evidencia, bugs, veredicto                 │
│                    ⟹ Se crea/lee por cada ticket activo      │
└─────────────────────────────────────────────────────────────┘
```

## Cuándo Leer Cada Nivel

| Tipo de tarea | L1 | L2 | L3 |
|---|---|---|---|
| Priorización de proyecto | ✅ | ❌ | ❌ |
| Test docs de un módulo | ✅ | ✅ | ❌ |
| Testing de un ticket | ✅ | ✅ | ✅ |
| Regresión global | ✅ | ✅ (todos) | ❌ |
| Automation de un ticket | ✅ | ✅ | ✅ |

## Reglas del Knowledge Base

1. **L1 es estable** — Se actualiza solo cuando cambia la arquitectura del proyecto
2. **L2 es progresivo** — Se construye por módulo y se retroalimenta después de cada release
3. **L3 es efímero** — Se crea al iniciar una sesión de testing y se cierra con el veredicto
4. **Nunca inventar contexto** — Si no hay L2 de un módulo, construirlo primero con el skill `knowledge/update-module`
5. **Los repos fuente son la verdad** — El L2 se construye leyendo `../flow_binaries`, `../gateway-ion`, `../webcomponents-flow`, `../gateway` y `../bot-test`
