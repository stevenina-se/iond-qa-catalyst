Estimado @Enrique

**El resultado de pruebas para este ticket es: APROBADO ✅**
---

### 💡 ¿Por qué es importante?
- El bug original causaba **errores 500 opacos** cuando un usuario enviaba una URL o texto plano como imagen al nodo PDF, impidiendo diagnosticar el problema. Ahora el nodo valida el input y retorna un mensaje descriptivo en el error output. Adicionalmente, este branch habilita la generación de PDFs con **texto en árabe** (crítico para expansión a mercados MENA) y protege la importación de templates contra archivos malformados o fuera de especificación, reduciendo soporte y errores silenciosos en producción.

---

### 🎯 Criterios de Aceptación (AC) Clave Validados

#### **AC-1. Arabic rendering — texto árabe se renderiza correctamente**
* **Validación realizada**: Se generaron PDFs con campos Arabic-only, campos mixtos (Arabic + Latin como `SKU-1024 قميص`), dígitos árabes (`مقاس ٤٢`), tablas con headers/rows árabes, y campos bold. Se verificaron límites conocidos (brackets, wrapping de líneas mixtas).
* **Comportamiento observado**: Texto árabe se renderiza right-to-left. Dígitos mantienen orden correcto. Runs Latin permanecen en orientación correcta. Templates existentes Latin-only generan output idéntico (sin regresión).

#### **AC-2. Import JSON validation — gates de validación funcionan**
* **Validación realizada**: Se probó cada gate individualmente: archivo .txt renombrado, archivo >5MB, JSON broken, template sin pages, font desconocida (`Comic Sans`), type desconocido, elemento fuera de página (`x + width > page width`). Se verificó que un export válido sigue importando y sincronizando la toolbar de dimensiones.
* **Comportamiento observado**: Cada archivo inválido muestra su propio toast de error descriptivo (hasta 5 elementos nombrados con sus números). El diseño actual no se modifica. Templates válidos importan correctamente.

#### **AC-3. Uploaded base PDF — geometry checks skipped**
* **Validación realizada**: Se importó un template con `basePdf` como PDF uploaded.
* **Comportamiento observado**: Los geometry checks se omiten correctamente. El template importa sin errores.

#### **AC-4. Node image inputs — validación con mensajes descriptivos**
* **Validación realizada**: Se ejecutó el nodo PDF Template con: PNG URL, JPEG data URI, raw base64 image, empty value, GIF image, WebP image, SVG image, y unreachable URL.
* **Comportamiento observado**: PNG URL, JPEG data URI, raw base64, y empty value → succesan. GIF/WebP/SVG y unreachable URL → fallan el nodo con mensaje descriptivo en el error output. No más errores 500 genéricos.

#### **AC-5. No regression on Latin templates**
* **Validación realizada**: Se regeneró un template Latin-only existente y se comparó contra output pre-branch.
* **Comportamiento observado**: Output idéntico. Sin regresión.

---

### 🔄 Pruebas de Regresión
- **Latin templates**: Regeneración de template existente produce output idéntico. Arabic rendering no afecta templates sin texto árabe.
- **Import JSON (export válido)**: Un template exportado previamente sigue importando correctamente. Toolbar de dimensiones sincroniza.
- **Nodo PDF (inputs válidos)**: PNG URL, JPEG data URI, raw base64 siguen funcionando normalmente. El refactor de `transformImage` no rompió flujos existentes.

---

### 📝 Conclusión de QA
El bug de error 500 genérico al enviar imágenes no-base64 al nodo PDF está completamente corregido. El backend ahora valida explícitamente los inputs de imagen con mensajes descriptivos en el error output del nodo. La validación de importación JSON en el diseñador protege contra archivos malformados con feedback claro al usuario. El soporte de renderizado árabe funciona correctamente para campos de texto, tablas y formatos bold, sin afectar templates Latin-only existentes. 19/19 TCs passed, 0 bugs, 0 bloqueantes. El entregable es estable y está listo para producción.

| Details | |
|---|---|
| BROWSER | Chrome |
| BRANCH | IONF-1119 |
| ENV | dev-app.ionflow.io |
| TEST MATRIX | N/A — testing directo desde QA Instructions |
| MERGE REQUEST | YES |
