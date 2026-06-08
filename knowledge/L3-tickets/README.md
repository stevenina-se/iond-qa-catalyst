# L3 — Ticket Memory

> Cada archivo en este directorio es la memoria de una sesión de testing para un ticket específico. Se crea al iniciar una sesión y se cierra con el veredicto.

## Instrucciones

### Crear una nueva sesión
1. Copia `_template.md` y nómbrala con el ID del ticket: `<TICKET-ID>.md`
2. Rellena la sección de contexto (AC, módulo, equipo)
3. El Catalyst irá llenando el resto durante la sesión

### Convención de nombres
- Usa el ID del ticket de ClickUp como nombre de archivo
- Ejemplo: `TASK-12345.md`

### Ciclo de vida
```
Ticket nuevo → Crear L3 → Planning → Execution → Reporting → Veredicto
```

- El archivo permanece en el repo como registro histórico
- Los archivos cerrados (con veredicto) no se eliminan

### Contenido
Cada sesión contiene:
- Acceptance Criteria (del ticket)
- Plan de testing aprobado
- Evidencia de ejecución (UI, API, DB)
- Bugs encontrados
- Veredicto final (Approved / Rejected)
- Transcript completo de la sesión
