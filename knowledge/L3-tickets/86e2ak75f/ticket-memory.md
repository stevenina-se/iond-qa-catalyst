# Ticket Memory — 86e2ak75f

> Memoria de sesión del Discovery para el ticket de Standardize Execution UI & Build Execution Replay Engine.

## Información del Ticket

| Campo | Valor |
|-------|-------|
| Ticket ID | [86e2ak75f](https://app.clickup.com/t/86e2ak75f) |
| Título | Standardize Execution UI & Build Execution Replay Engine |
| Módulo principal | Executions |
| Módulos impactados | Boards, Dashboard (indirecto) |
| Developer | Gustavo Mamani |
| QA Engineer | Steve Nina |
| Track | Discovery |
| Fecha de inicio | 2026-08-27 |

---

## Acceptance Criteria (Reconciliados — 12 ACs)

> Reconciliados de descripción + 6 comentarios del Developer en ClickUp.

- [ ] AC-1: Consistencia visual de la interfaz de ejecución en Dev y Live
- [ ] AC-2: Inspección de ejecución pasada con 3 puntos de acceso (boards list, board editor, historial general) + URL compartible
- [ ] AC-3: Ejecuciones > 7 días muestran solo metadata con aviso de expiración
- [ ] AC-4: Mensajes diferenciados para "detalle expiró" vs "detalle no guardado"
- [ ] AC-5: Board no puede tener dos ejecuciones activas a la vez (overlap IONF-1248)
- [ ] AC-6: Botón de ejecutar se bloquea inmediatamente al presionar (overlap IONF-1248)
- [ ] AC-7: Ninguna ejecución puede quedar indefinidamente "en curso" (overlap IONF-1248)
- [ ] AC-8: Ejecuciones identifican modo (live/dev) y tipo de trigger (manual/schedule/webhook/subflow)
- [ ] AC-9: Snapshot del board se guarda al ejecutar para reconstrucción exacta
- [ ] AC-10: Ejecuciones anteriores al deploy no muestran vista replay (data faltante)
- [ ] AC-11: Archivos SQLite se recuperan de R2 con cache temporal
- [ ] AC-12: Botón para descargar registro de ejecuciones (prototype review feedback)

---

## Decisiones del Equipo

> Extraídas de comentarios de ClickUp.

| Fecha | Decisión | Tomada por |
|-------|----------|------------|
| 2026-07-30 | Pantalla propia con URL (no modal) — permite compartir y navegar | Gustavo |
| 2026-07-30 | 3 puntos de acceso: boards list, board editor, historial general | Gustavo |
| 2026-07-30 | Retención de 7 días para detalle completo | Gustavo |
| 2026-07-30 | Se reutiliza visor de flows de solo lectura existente | Gustavo |
| 2026-07-30 | Sin opción de "copiar al editor" en v1 (riesgo de sobrescribir board en producción) | Gustavo |
| 2026-07-30 | Fuera de alcance: notificaciones, reintento, comparar, exportar, ampliar retención | Gustavo |
| 2026-08-04 | Nuevas columnas en `executions`: modo (live/dev) y trigger type | Gustavo |
| 2026-08-04 | Nueva tabla SQLite para snapshot del flow | Gustavo |
| 2026-08-04 | Solo ejecuciones NUEVAS tendrán vista replay | Gustavo |
| 2026-08-06 | Servicio R2 resuelto con cache temporal + cron de limpieza | Gustavo |
| 2026-08-24 | Prototype review aprobado. Sugerencia: botón de descarga | Prototype Review |

---

## Artefactos de la Sesión

| Artefacto | Estado | Archivo |
|-----------|--------|---------|
| Ticket Memory | ✅ Completado | `ticket-memory.md` |
| Risk Triage | ✅ Completado | `risk-triage.md` |
| AC Consolidados | ✅ Completado | `ac-consolidated.md` |
| Test Matrix | ✅ Completado | `test-matrix.md` + `test-matrix.csv` |
| Test Plan | ✅ Completado | `test-plan.md` |
| Code Review QA | ⬜ Pendiente (QA decide) | `code-review-qa.md` |

---

## Bugs Encontrados

| Bug ID | Severidad | Descripción | TC relacionado | Evidencia |
|--------|-----------|-------------|---------------|-----------|
| | | | | |

---

## Veredicto

| Campo | Valor |
|-------|-------|
| Veredicto | ⏳ Pendiente — En Discovery |
| Aprobado por | |
| Fecha | |
| Observaciones | |

---

## Transcript

> Log cronológico de la sesión.

| Timestamp | Stage | Acción | Detalle |
|-----------|-------|--------|---------|
| 2026-08-27 21:12 | Session Start | Contexto cargado | L1 + L2 executions + L2 boards |
| 2026-08-27 21:12 | Paso 1 | ClickUp MCP | Ticket + 6 comentarios leídos |
| 2026-08-27 21:13 | Paso 2 | Reconciliación AC | 2 → 12 ACs reconciliados |
| 2026-08-27 21:15 | Paso 3 | Risk Triage | 13 riesgos + 18 edge cases + 12 preguntas |
| 2026-08-27 21:18 | Paso 4 | AC Consolidados | 2 → 15 ACs (12 + 3 sub-ACs) |
| 2026-08-27 21:22 | Paso 5 | Test Matrix | 35 test cases + 7 queries BD |
| 2026-08-27 21:24 | Paso 6 | Test Plan | ~165 min estimados, 6 bloques |
