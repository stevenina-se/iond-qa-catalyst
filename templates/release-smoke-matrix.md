# Smoke Test Matrix — [VERSIÓN]

> Template generado por `skills/release/smoke-matrix`
> Fecha: [fecha]
> Versión: [versión]
> Entorno: [URL]

## Resumen

| Métrica | Valor |
|---------|-------|
| Total de casos | |
| Flujos críticos cubiertos | /9 |
| TCs de riesgo alto (release) | |
| TCs baseline | |
| Tiempo estimado total | ~[X] min |

---

## Smoke Test Matrix

| ID | Flujo Crítico | Caso de Test | Pasos | Resultado Esperado | Riesgo | Prioridad | Estado |
|----|--------------|-------------|-------|-------------------|--------|-----------|--------|
| SM-001 | Login / Auth | | | | | 🔴 | ⬜ |
| SM-002 | Crear flow | | | | | 🔴 | ⬜ |
| SM-003 | Agregar nodos | | | | | 🔴 | ⬜ |
| SM-004 | Ejecutar flow | | | | | 🔴 | ⬜ |
| SM-005 | Historial ejecuciones | | | | | 🟠 | ⬜ |
| SM-006 | Crear conexiones | | | | | 🟠 | ⬜ |
| SM-007 | Crear/editar conector | | | | | 🟠 | ⬜ |
| SM-008 | Crear/editar service | | | | | 🟠 | ⬜ |
| SM-009 | Template PDF | | | | | 🟠 | ⬜ |

<!--
Los 9 flujos base vienen de test-priorities.md > "Áreas de Regresión Crítica".
Se construyen desde cero cada vez, NO desde un CSV de referencia.
Para cada flujo, generar 1-3 TCs concretos.
-->

### Formato de Pasos (OBLIGATORIO)

> Los pasos DEBEN usar formato **breadcrumb** explícito.
> Formato: `[Rol] Login > Sidebar: [Módulo] > [Acción] > [Verificación]`
> Cada TC debe ser verificable en **menos de 2 minutos**.
> Sin acceso a BD — solo UI/API observable.

### Leyenda de Riesgo
- `🔴 Riesgo Alto` — Módulo tocado por el release actual
- `🟢 Baseline` — Módulo no tocado directamente

### Leyenda de Prioridad
- 🔴 Crítico — Testear siempre
- 🟠 Alto — Testear siempre
- 🟡 Medio — Testear si hay tiempo

### Leyenda de Estado
- ⬜ Pendiente
- ✅ Pasó
- ❌ Falló
- ⏭️ Saltado (con justificación)

---

## TCs Específicos del Release

<!--
TCs adicionales derivados de los tickets del release actual.
Solo para flujos cuyo módulo fue tocado directamente.
1-2 TCs de validación específica por flujo impactado.
-->

| ID | Ticket Origen | Caso de Test | Pasos | Resultado Esperado | Prioridad | Estado |
|----|--------------|-------------|-------|-------------------|-----------|--------|
| SM-R-001 | | | | | 🔴 | ⬜ |

---

## Modo de Ejecución Sugerido

<!--
Playwright MCP: recomendado para velocidad y evidencia automática (screenshots)
Manual: cuando el entorno no soporta Playwright o el QA prefiere control directo
-->

| Modo | Recomendación | Razón |
|------|--------------|-------|
| Playwright MCP | ✅ Recomendado | Velocidad + screenshots automáticos |
| Manual | ⬜ Alternativa | Control directo del QA |

---

## Notas

- Columna vertebral: 9 flujos de `test-priorities.md` > "Áreas de Regresión Crítica"
- No se usa CSV de referencia — el smoke se construye desde cero cada versión
- Compatible con ejecución vía Playwright MCP
