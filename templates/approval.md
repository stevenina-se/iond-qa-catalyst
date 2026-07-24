# Template de Aprobación — [TICKET-ID]

Estimado @name_dev

**El resultado de pruebas para este ticket es: APROBADO ✅**

**Ticket**: [TICKET-ID] — [Título del Ticket]
**Módulo**: [Módulos / Componentes afectados]
**QA Engineer**: [Nombre del QA]
**Fecha**: [Fecha de hoy]

### 📊 Resumen de Testing
- **Casos ejecutados**: [N] ([N] funcionales + [N] regresión / [N] inyectados de Code Review)
- **Casos aprobados**: [N]
- **Tasa de aprobación**: 100%
- **Bugs encontrados**: [N]

---

### 🛠️ ¿Qué se construyó / cambió?
> *[Instrucción para la Skill: Explica detalladamente el cambio técnico a nivel de código, arquitectura, base de datos, endpoints o webcomponents. Menciona las clases, archivos clave o payloads modificados]*
- **[Componente/Lógica 1]**: ...
- **[Componente/Lógica 2]**: ...

### 💡 ¿Por qué es importante?
> *[Instrucción para la Skill: Detalla el impacto de este cambio en el negocio o producto. ¿Qué problema resuelve para el usuario? ¿Qué flujos o integraciones nuevas habilita que antes eran imposibles de realizar?]*
- ...

---

### 🎯 Criterios de Aceptación (AC) Clave Validados
> *[Instrucción para la Skill: Desglosa los ACs más importantes del ticket. Para cada uno, describe de forma concisa qué se probó, cómo se comportó el sistema y qué validaciones lógicas o visuales confirmaron su éxito]*

#### **AC-1. [Título del Criterio 1]**
* **Validación realizada**: ...
* **Comportamiento observado**: ...

#### **AC-2. [Título del Criterio 2]**
* **Validación realizada**: ...
* **Comportamiento observado**: ...

#### **AC-3. [Título del Criterio 3 (Opcional)]**
* **Validación realizada**: ...
* **Comportamiento observado**: ...

---

### 🔄 Pruebas de Regresión
> *[Instrucción para la Skill: Detalla qué flujos preexistentes o componentes legacy se probaron para asegurar que el nuevo cambio no introdujo efectos colaterales o "rompió" producción]*
- **[Flujo Legacy 1]**: ...
- **[Flujo Legacy 2]**: ...

---

### 🔍 Code Review QA
> Resumen de la revisión de código realizada antes del testing funcional para mitigar riesgos tempranos.

- **Repos revisados**: [lista de repositorios y PRs]
- **Hallazgos identificados**: [N] (🔴: [N], 🟠: [N], 🟡: [N])
- **Riesgos inyectados a la Matrix**: [N] TCs creados específicamente a partir del código revisado.
- **Estado**: Todos los hallazgos fueron verificados y mitigados exitosamente en Testing.

### ⚠️ Observaciones
- [Detallar observaciones de UI/UX menor, comportamientos por diseño o limitaciones no bloqueantes. Si no aplica, colocar "Ninguna"]

### 📂 Evidencia
- **Test Matrix**: [Link a documento o ruta local]
- **QA Report / Run**: [Link o referencia]
- **Code Review QA**: [Link o referencia]
- **DB Evidence**: [Queries de BD, migraciones o N/A si aplica]
- **Screenshots / Logs**: [Ruta o referencia a capturas de Postman/Playwright/UI]

---

### 📝 Conclusión de QA
> *[Instrucción para la Skill: Redacta un párrafo final robusto que sintetice la corrección o mejora principal y declare formalmente la estabilidad del entregable]*

| Details | |
|---|---|
| BROWSER | Chrome / Postman / Playwright / N/A |
| BRANCH | [Nombre de la rama / Git Branch] |
| ENV | [Ambiente de pruebas, ej: dev-app.ionflow.io] |
| TEST MATRIX | [Ruta del archivo markdown o URL] |
| MERGE REQUEST | YES / NO |