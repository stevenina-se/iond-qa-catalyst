# Release notes — [producto] v[X.Y.Z] — [interna | cliente]

> **Plantilla del QA Catalyst** — notas de la versión semanal de un producto (fuente canónica §7.1 y C-29 · `Q-36`).
> **Se guardan en:** `knowledge/releases/[producto]/v[X.Y.Z]/release-notes-internal.md` y `release-notes-client.md` · **Skill:** `skills/release/notes.md` · Se enlazan en el C-29 (`**Release notes:** [interna] · [cliente]`).
> Una versión por producto y semana (Sprint [N], [fecha inicio] – [fecha fin]). Se excluyen los tickets con `diferido` o revertidos de la RC. La interna la aprueba el SM; la de cliente la aprueba y comunica el **PO**, apoyado por el soporte general de la empresa.

<!--
Reglas por variante (borrar este bloque en el documento final):

| | Interna | Cliente |
|---|---|---|
| Lectores | Development, producto, soporte general de la empresa | Clientes y usuarios |
| Lenguaje | Técnico | Beneficio: "Ahora puedes…", "Corregimos…", "Mejoramos…" |
| IDs de ticket, repos, ramas | Sí | No |
| Cambios internos e infraestructura | Sí | No |
| Nombres de módulos | Iond Subcategory | Nombre amigable (p. ej. "Automatización de flujos" para Boards) |

Clasificación por TYPE: New Feature → 🚀 · Bug → 🐛 · Improvement → ⚡ · Refactor / Task → 🔧 (solo interna).
Subagrupar por Iond Subcategory. Los tickets con Project = Gateway van en las notas de iond, en su propia sección.
-->

## Resumen

[Interna: 3–5 oraciones con totales por TYPE y por módulo · Cliente: 2–3 oraciones orientadas a beneficios]

**En números:** [n] nuevas funcionalidades · [n] correcciones · [n] mejoras · [n] cambios internos *(solo interna)*

## Destacados

1. **[Destacado 1]** — [descripción breve]
2. **[Destacado 2]** — [descripción breve]
3. **[Destacado 3]** — [descripción breve]

## 🚀 Nuevas funcionalidades

### [Módulo]
- [Interna: #[id] Título — repos afectados] · [Cliente: beneficio para el usuario]

## 🐛 Correcciones

### [Módulo]
- [Interna: #[id] Título — *re-validado* si tuvo rechazos] · [Cliente: "Corregimos…"]

## ⚡ Mejoras

### [Módulo]
- [...]

## 🔧 Cambios internos *(solo interna)*

- #[id] [Refactor / Task] — [descripción técnica breve]

## Gateway *(solo en iond, si hay tickets con Project = Gateway)*

- [...]

## Infraestructura y despliegue *(solo interna)*

| Tipo | Nombre (nunca el valor) | Repo | Ticket |
|---|---|---|---|
| Variable nueva / migración / dependencia | [...] | [...] | #[id] |

## Problemas conocidos

- *Interna:* hallazgos aceptados en un CONDITIONAL GO — [ID — severidad — workaround — fix agendado: #[id], v[X.Y.Z+1]].
- *Cliente:* [solo si afecta al usuario: qué pasa y cómo evitarlo, en lenguaje simple].

## Qué necesitas hacer *(cliente, solo si hay acción requerida)*

1. [Paso para el cliente]

## Información de la versión

| Campo | Valor |
|---|---|
| Producto / versión | [iond / IonMind / StageMind] v[X.Y.Z] |
| Semana | Sprint [N] ([fecha inicio] – [fecha fin]) |
| Fecha de despliegue | [AAAA-MM-DD] |
| Decisión Go/No-Go | GO / CONDITIONAL GO (C-29 [AAAA-MM-DD]) *(solo interna)* |
| Contacto | Soporte general de la empresa *(cliente)* · canal del equipo IOND *(interna)* |
