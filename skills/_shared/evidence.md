# Contrato compartido: evidencia y datos

> Reglas de evidencia para `mock testing`, el release y los reportes. Aplican a todas las skills que ejecutan pruebas.

## Evidencia mínima por resultado

| Resultado | Evidencia |
|---|---|
| TC aprobado | Paso final verificado (captura o salida de API) cuando el TC es de un REQ crítico; en el resto, basta el registro en la matriz |
| TC fallido / OBS | Captura o video, pasos exactos, datos usados, ambiente y build/rama, resultado esperado vs. actual, REQ-ID afectado |
| Prueba automática | Resumen del reporte de Playwright (totales, fallas con su clasificación) y ruta del reporte HTML |
| Validación en BD | Query ejecutada (solo lectura) y resultado pegado por el QA |

Capturas en `knowledge/L3-tickets/<id>/screenshots/` (ticket) o en `knowledge/releases/<producto>/<versión>/evidence/` (release), con nombre `<ID>-<paso>.png`.

## Bases de datos (solo lectura)

| BD | Motor | Schema (única fuente válida) | Acceso |
|---|---|---|---|
| Principal | PostgreSQL | `../gateway/database/migrations/*.php` | Túnel SSH (DBeaver) — la query la ejecuta el QA |
| Ejecuciones | SQLite por instancia del motor | `../flow_binaries/migrations/*.sql` | Vía UI o API del historial de ejecuciones |

- Las queries se construyen **solo** desde las migraciones. Nunca inventar tablas, campos ni relaciones.
- Solo `SELECT`. El QA ejecuta la query y pega el resultado; el catalyst lo guarda como evidencia.

## Testing asistido (Canal 1, Playwright MCP)

- Solo en `mock testing` o en ejecuciones manuales del release, con el **QA supervisando** el navegador visible.
- Credenciales desde `.env` del catalyst (o el perfil del ambiente); en los artefactos se registra el usuario, **nunca** la contraseña.
- La IA sugiere el resultado de cada TC; **el QA confirma** ✅/❌ antes de registrarlo.

## Datos de prueba

- Los datos que crea QA llevan el prefijo `qa-` (manual) o `autobot-` (automatizado) y se eliminan al terminar cuando la app lo permite.
- En producción solo se usa la **company de prueba** (AV-09); nunca datos ni cuentas de clientes.
- Las integraciones sin sandbox se prueban como indique la sección *Datos de prueba* de la matriz (mock, colección simulada o cuenta de prueba).

## Secretos

- No leer en voz alta, copiar ni guardar valores de `.env`, perfiles, tokens o entornos de Postman en artefactos del repositorio.
- Los entornos de Postman con valores reales se guardan como `*.postman_environment.local.json` (ignorados por git).
