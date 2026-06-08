# Architecture Brief — QA Checklist — [TICKET-ID]

> Checklist de QA para validar el Architecture Brief del ticket.
> Referencia: Paso 7 del Altacrest Dual-Track (Architecture Brief - Mandatory)
> Skill: `test-docs/document` (modo Architecture Brief)
> Fecha: [fecha]

## Información del Ticket

| Campo | Valor |
|-------|-------|
| Ticket ID | |
| Título | |
| Developer | |
| Módulo principal | |
| Architecture Brief revisado | ✅/❌ |

---

## Checklist de Validación QA

### Seguridad y Permisos

| # | Pregunta | Estado | Observación |
|---|----------|--------|-------------|
| 1 | ¿Se validaron permisos por company (multi-tenant)? | ⬜ | |
| 2 | ¿Se validaron permisos por rol de usuario? | ⬜ | |
| 3 | ¿Los endpoints nuevos requieren autenticación (SSO Keycloak)? | ⬜ | |
| 4 | ¿Se evita el acceso cruzado entre companies? | ⬜ | |
| 5 | ¿Las credenciales se manejan de forma segura? | ⬜ | |

### API y Endpoints

| # | Pregunta | Estado | Observación |
|---|----------|--------|-------------|
| 6 | ¿Los endpoints nuevos tienen validación de input? | ⬜ | |
| 7 | ¿Se documentaron los contratos de request/response? | ⬜ | |
| 8 | ¿Se manejan correctamente los errores (4xx, 5xx)? | ⬜ | |
| 9 | ¿Los endpoints existentes mantienen retrocompatibilidad? | ⬜ | |

### Base de Datos

| # | Pregunta | Estado | Observación |
|---|----------|--------|-------------|
| 10 | ¿Las migraciones son reversibles? | ⬜ | |
| 11 | ¿Se mantiene la integridad referencial? | ⬜ | |
| 12 | ¿Se consideró el impacto en la BD de ejecuciones (SQLite)? | ⬜ | |
| 13 | ¿Hay índices para las queries frecuentes? | ⬜ | |

### Ejecución de Flows/Nodos

| # | Pregunta | Estado | Observación |
|---|----------|--------|-------------|
| 14 | ¿Se afecta la ejecución de flows existentes? | ⬜ | |
| 15 | ¿Qué pasa si un nodo falla a mitad de ejecución? | ⬜ | |
| 16 | ¿Se registran correctamente los logs de ejecución? | ⬜ | |
| 17 | ¿El cambio funciona en modo Development y Production? | ⬜ | |

### Connectors y Apps

| # | Pregunta | Estado | Observación |
|---|----------|--------|-------------|
| 18 | ¿El feature funciona para connectors globales y de company? | ⬜ | |
| 19 | ¿Las conexiones existentes se mantienen estables? | ⬜ | |
| 20 | ¿Se manejan las credenciales de apps externas correctamente? | ⬜ | |

### Rollback y Recuperación

| # | Pregunta | Estado | Observación |
|---|----------|--------|-------------|
| 21 | ¿Se puede revertir el cambio sin pérdida de datos? | ⬜ | |
| 22 | ¿Hay un plan de rollback documentado? | ⬜ | |
| 23 | ¿Los webhooks se mantienen estables después del cambio? | ⬜ | |

### Performance

| # | Pregunta | Estado | Observación |
|---|----------|--------|-------------|
| 24 | ¿El cambio puede impactar el rendimiento del motor de ejecución? | ⬜ | |
| 25 | ¿Se consideraron escenarios con alto volumen de datos? | ⬜ | |

---

## Resumen

| Métrica | Valor |
|---------|-------|
| Total de checks | 25 |
| Aprobados | |
| Pendientes | |
| Con observaciones | |
| Bloqueantes | |

## Conclusión

> ⬜ **Aprobado para Deployment** — El Architecture Brief cumple con los estándares de QA
> ⬜ **Aprobado con observaciones** — Requiere atención en los puntos marcados
> ⬜ **Requiere revisión** — Los puntos bloqueantes deben resolverse antes de continuar
