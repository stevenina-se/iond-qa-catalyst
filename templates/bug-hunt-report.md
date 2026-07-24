# Bug Hunt Report — [MÓDULO]

> Template generado por `skills/release/bug-hunt`
> Fecha: [fecha]
> Versión: [versión del release]
> Módulo: [nombre del módulo]
> QA Engineer: [nombre]

---

## Resumen

| Métrica | Valor |
|---------|-------|
| Bugs confirmados (UI) | |
| Bugs confirmados (Backend) | |
| Riesgos no verificados | |
| Falsos positivos descartados | |
| Tickets creados vía bug-reporter | |

---

## Bugs Confirmados — UI

<!--
Bugs reproducibles encontrados en la interfaz de usuario.
Cada bug debe tener pasos breadcrumb + screenshot de evidencia.
Solo se marca como CONFIRMADO si se reprodujo vía Playwright MCP o manualmente.
-->

### BUG-BH-001 — [Descripción corta]

| Campo | Valor |
|-------|-------|
| Prioridad | `urgent` / `high` / `normal` / `low` |
| Canal | UI |
| Módulo | |
| Ticket creado | _Sí — [link]_ / _No — documentado internamente_ |

**Pasos de reproducción:**
1. [Paso breadcrumb]

**Resultado actual:**
[Lo que ocurre]

**Resultado esperado:**
[Lo que debería ocurrir]

**Evidencia técnica:**
```
[CONFIRMADA] Código / screenshot / respuesta
```

---

## Bugs Confirmados — Backend

<!--
Bugs reproducibles encontrados vía API requests.
Cada bug debe incluir: request completo, response, y el código confirmado con grep.
-->

### BUG-BH-002 — [Descripción corta]

| Campo | Valor |
|-------|-------|
| Prioridad | `urgent` / `high` / `normal` / `low` |
| Canal | API |
| Endpoint | `[METHOD] /api/[ruta]` |
| Ticket creado | _Sí — [link]_ / _No — documentado internamente_ |

**Request:**
```
[METHOD] /api/[ruta]
Headers: [headers relevantes]
Body: [JSON del body]
```

**Response actual:**
```
Status: [código]
Body: [respuesta]
```

**Response esperado:**
```
Status: [código esperado]
Body: [respuesta esperada]
```

**Evidencia técnica:**
```
[CONFIRMADA] ../[repo]/[archivo]:[línea]
[código relevante]
```

**Vector de ataque:**
[Qué tipo de vector: payload malformado, multi-tenant, auth bypass, etc.]

---

## Riesgos No Verificados

<!--
Hallazgos estáticos del código que no se pudieron reproducir.
Quedan como RIESGO A VERIFICAR para revisión manual futura.
-->

### RISK-BH-001 — [Descripción]

| Campo | Valor |
|-------|-------|
| Confianza | `alta` / `media` / `baja` |
| Canal | UI / API |
| Razón de no verificación | [por qué no se pudo reproducir] |

**Código:**
```
[CONFIRMADA] ../[repo]/[archivo]:[línea]
[fragmento de código]
```

**Nota:** [Qué se necesita para verificar]

---

## Falsos Positivos Descartados

<!--
Hallazgos que parecían bugs pero se descartaron tras verificación.
Documentarlos evita reportarlos de nuevo en futuros bug hunts.
-->

| ID | Descripción | Razón de descarte |
|----|-------------|-------------------|
| FP-BH-001 | | |

---

## Búsquedas Realizadas

<!--
Documentar todos los greps ejecutados para auditoría.
Incluir cuándo dieron 0 resultados (eso también es evidencia).
-->

| Término buscado | Repo | Comando | Resultado |
|----------------|------|---------|-----------|
| | | `grep -rn "..." ../[repo]/ --include="*.[ext]"` | [N] hits / 0 hits |

---

## Notas

<!--
Edge cases conocidos del L2 que se consultaron, contexto extra, etc.
-->

- Protocolo de evidencia del `bug-reporter/create` aplicado (reglas 11-14)
- Vectores de ataque backend: lista NO cerrada, se descubrieron vectores adicionales según el código
- Edge Cases Conocidos del L2 consultados para evitar falsos positivos
