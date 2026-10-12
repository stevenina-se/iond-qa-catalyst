# Template de Rechazo — 86e35zdkx

Estimado @Yamil

**El resultado de pruebas para este ticket es: RECHAZADO ❌**

**Ticket**: 86e35zdkx — [STAGEMIND] Catalog Builder: operación compuesta para nombre y descripción
**Módulo**: StageMind (ai_productmind)
**QA Engineer**: Steve Nina
**Fecha**: 2026-10-01

### Resumen de Testing
- Casos ejecutados: pendiente de completar
- Casos aprobados: pendiente
- Casos fallidos: pendiente
- Bugs encontrados en Code Review: pendiente
- Bugs encontrados en Testing: 2
- Bugs totales (bloqueantes): 2

### Code Review QA
> Pendiente de ejecución formal. Los hallazgos actuales provienen del testing funcional del endpoint `POST /api/v1/text/title-description`.

---

### 📌 Observaciones

**🔴 OBS-01 - Urgent - Estado: Nuevo**
**Área / Flujo: StageMind — Endpoint `POST /api/v1/text/title-description`**

**Descripción:**
El parámetro `target_title_length` no se respeta en la generación del nombre. Se solicita un nombre con máximo 25 caracteres pero el campo `data.name` retorna un texto de ~469 caracteres compuesto por keywords repetitivas, excediendo drásticamente el límite solicitado.

Adicionalmente, existe una **inconsistencia entre la validación del endpoint y la generación**: cuando se envía `target_title_length < 10`, el endpoint **acepta** la petición (no rechaza con error de validación), sugiriendo implícitamente que es capaz de generar títulos con esa cantidad de caracteres. Sin embargo, el endpoint de generación de títulos separado (`create-title`) **no soporta** longitudes tan cortas. Se espera que se unifiquen los comportamientos de validación entre el endpoint compuesto y los endpoints separados existentes.

**Pasos de reproducción:**
1. `POST /api/v1/text/title-description` con payload:
```json
{
  "image_url": "https://i5.walmartimages.com/seo/Apple-MacBook-Pro-14-inch-Apple-M1-Pro-chip-with-8-core-CPU-and-14-core-GPU-16GB-RAM-512GB-SSD-Space-Gray-New-Open-Box_0c58794a-1339-43fe-bb2d-998d6400d9a3.b31e77570774d20505e055d600da2dd6.jpeg",
  "language": "en",
  "user_prompt": "",
  "target_title_length": 25,
  "target_description_length": 100
}
```
2. Observar el campo `data.name` en la respuesta

**Resultado esperado:**
- `data.name` debería respetar el `target_title_length` de 25 caracteres (ej: "Apple MacBook Pro 14-inch")
- Si `target_title_length < 10`, debería rechazarse con error de validación (consistente con `create-title`) O bien ambos endpoints deberían soportar el mismo rango de valores

**Comportamiento actual:**
- `data.name` retorna ~469 caracteres: `"Apple MacBook Pro Laptop Gray Aluminum Body 14-inch Display Screen Device Electronics PC Computer Workstation Hardware Apple Brand Office Gear Sleek Modern Design Portable Notebook Professional Computing Tool Reliable Tech Equipment High Performance Laptop High Resolution Visuals Durable Metal Chassis Lightweight Design Advanced Technology Device Premium Build Quality Essential Work Tool Superior Screen Clarity Compact Form Factor Efficient Mobile Computing"`
- `data.description` retorna `null` (status `PARTIAL_SUCCESS`)
- Con `target_title_length < 10`, el endpoint no rechaza la petición sino que la acepta, comportamiento **contrario** al endpoint `create-title`

**Evidencia:**
- Response status: `200 PARTIAL_SUCCESS`
- `transaction_id`: `dc80273d-f0d4-406d-bd56-ff8609cee9ca`
- `tokens_input`: 534, `tokens_output`: 77, `cost_usd`: 0.000249
- Warning: `"Only partial product metadata could be identified with high confidence."`

---

**🟡 OBS-02 - High - Estado: Nuevo**
**Área / Flujo: StageMind — Endpoint `POST /api/v1/text/title-description`**

**Descripción:**
Al enviar una imagen con URL inaccesible (URL malformada que no apunta a una imagen real), la documentación (`docs/HTTP_STATUS_CODES.md`) especifica que el endpoint debería retornar **error 400**, sin embargo el endpoint retorna **error 422**. Existe discrepancia entre la documentación y el comportamiento real del endpoint.

**Pasos de reproducción:**
1. `POST /api/v1/text/title-description` con payload:
```json
{
  "image_url": "https://i5.walmartimages.com/seo/Apple-MacBook-Pro-14-inch-Apple-M1-Pro-chip-with-8-core-CPU-and-14-core-GPU-16GB-RAM-512GB-SSD-Space-Gray-New-Open-Box_0c58794a-1339-43fe-bb2d-998d6400d9a3.b31e77570774d20505e055d600da2d9d6.jpeg",
  "language": "en",
  "user_prompt": "",
  "target_title_length": 25,
  "target_description_length": 100
}
```
2. Observar el código de error retornado

**Resultado esperado:**
Error `400 Bad Request` según la documentación (`docs/HTTP_STATUS_CODES.md`): imagen inválida o inaccesible debería retornar 400.

**Comportamiento actual:**
Error `422 Unprocessable Entity` retornado. Discrepancia con la documentación.

**Evidencia:**
- Response HTTP status: 422
- URL de imagen contiene un hash deliberadamente incorrecto (9d6 en vez de d6 al final)
- La documentación del endpoint en `docs/HTTP_STATUS_CODES.md` especifica 400 para este escenario

---

### Evidencia General
- Test Matrix: Pendiente de generación formal
- QA Report: Pendiente — se requiere completar el deployment track completo
- Code Review QA: Pendiente
- Merge Request: https://github.com/altacrest/ai_productmind/pull/5

| Details | |
|---|---|
| BROWSER | Postman / API Client |
| BRANCH | IONF-1348 |
| ENV | dev-app.ionflow.io |
| TEST MATRIX | Pendiente |
| CODE REVIEW | Pendiente |
| MERGE REQUEST | PENDIENTE (bugs encontrados) |
