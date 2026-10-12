# Observaciones de preparación — beta iond v0.2.0 + IonMind v1.10.2

> Hallazgos de la lectura de los 84 tickets (ClickUp en solo lectura y L3 del catalyst, 2026-10-10) que necesitan una **decisión del PO** o una **revalidación** antes del Go/No-Go.
> Se revisan con el PO, el LQA y el LD el **miércoles 14/10** y las decisiones van en el C-26. Lo que el PO acepte como desvío se registra en las release notes internas. Lo que rechace pasa a Improvements `backlog` con `det-sanity`, o se revierte de la RC con `diferido`.
> Severidad propuesta = la del hallazgo si se confirma en el sanity. Las decisiones quedan en blanco hasta la reunión.

## Resumen

| Bloque | Observaciones | Bloquean el GO si no se resuelven |
|---|---|---|
| A. Estado del ticket incoherente con lo que entra a la RC | 5 | 3 (OBS-01, OBS-02, OBS-05) |
| B. Desvíos aprobados que el PO debe aceptar o rechazar | 12 | — (decisión de alcance) |
| C. Riesgos de seguridad o de datos | 4 | 2 (OBS-18, OBS-19) |
| D. Cobertura de QA incompleta (se revalida en el sanity) | 6 | — (se cierran con el sanity) |
| E. Datos de ClickUp | 1 | — (ver `acciones-clickup.md`) |

## A. Estado del ticket incoherente

| ID | Ticket | Observación | Propuesta | Severidad si se confirma | Decisión PO |
|---|---|---|---|---|---|
| OBS-01 | 86e1y463z NOVASPHERE (+ 86e1y46c7, 86e1y46d0) | El último veredicto es **RECHAZADO**: la iteración 2 del L3 (2026-09-21) registra 15 bugs bloqueantes, p. ej. BUG-12-1, donde borrar un tier con ventas da 500 y deja Stripe y la BD inconsistentes. Aun así el ticket está en `ready to merge`. Las subtareas no tienen QA ni code review propios. | Confirmar en ClickUp si hubo un 3.er ciclo aprobado. Si no lo hubo, el ticket entra a la RC solo si el sanity cierra los bloqueantes (SAN-86e1y463z-BUG-12-1 y AC-1…AC-6); si no, se revierte con `diferido`. | `urgent` | |
| OBS-02 | 86e1pzyug Monetización (IONF-1056-B) | La aprobación viene del L3 del catalyst (2026-08-23) y no se encontró en ClickUp. El campo Rejection_count está vacío con 2 rechazos. | Confirmar el veredicto en ClickUp o tratar el sanity `urgent` completo como validación de cierre. | `high` | |
| OBS-03 | 86e1pzz9j (overage con Stripe Meters) | El alcance B quitó overage y Stripe, pero la subtarea está en `production deploy` sin desarrollo. | Cerrar como `done w/d` (descartada) y verificar que no queda Stripe en billing (SAN-86e1pzz9j-AC-B15). | `normal` | |
| OBS-04 | 86e2t9962 (minado en tiempo real) | Se resolvió reiniciando pods, sin código ni PR (Project IONMIND). | Verificar en el sanity (SAN-86e2t9962-AC-1/2) y cerrar con C-19 "sin cambio de código". | `normal` | |
| OBS-05 | 86e2p459r (errores de IonMind) | Hay un comentario "Rama en IOND cerrada" del 2026-09-09, pero el ticket está en `production deploy`. Su REQ 5, el contrato de estado terminal, se difirió a IONF-1154, y la evidencia de QA muestra un sobre `success` con `data.status=failed`. | El RM confirma que los PRs (ai_ionmind#16, ion_gateway_ion#39) entran a las RC. Si no entran, el ticket se retira del release. | `high` | |

## B. Desvíos aprobados por QA respecto de la especificación

| ID | Ticket | Desvío | Pregunta al PO | Decisión PO |
|---|---|---|---|---|
| OBS-06 | 86e35882c Menú | Execution History quedó dentro de Dashboard; "Accounting" en Marketplace en lugar de "Billing"; las rutas retiradas dan **404** en vez de redirigir. | ¿Se aceptan los tres desvíos? (El 404 rompe marcadores y enlaces de clientes.) | |
| OBS-07 | 86e2fpp9y → 86e31pbz9 Acceso de soporte | La Fase 2 reemplazó a la Fase 1 sin enmienda del PO: no hay expiración ni auditoría de la sesión, y el admin entra a cualquier compañía. | ¿Se acepta para la beta? ¿Se agenda la auditoría como mejora? | |
| OBS-08 | 86e2nazxp Ciclo de vida | Se quitó el mutex del backend (solo bloquea el front); el estado `stopped` no figura en REQ-3. | ¿Se acepta? Riesgo: doble ejecución desde API o dos pestañas. | |
| OBS-09 | 86e2xnjyz SQLite persistente | La meta de 3–5 s no se cumple: el flow de referencia pasó de 52,9 s a 36,9 s. No se midió en staging/NFS. | ¿Se acepta la mejora parcial? | |
| OBS-10 | 86e2ak75f Historial y replay | Contradicción OBS-01 (modo de subflujo). "Cargar más" convive con un aviso de 50 filas; las ejecuciones de más de 7 días no se listan; cambió el contrato del endpoint. | ¿Qué modo de subflujo es el vigente? ¿Se acepta el límite de 7 días? | |
| OBS-11 | 86e2mt70g Tier de IonMind | REQ-5 aparece tachado, pero el Gherkin 1 lo exige; el gateway vuelve a 3 tiers por defecto; no hay tests unitarios. | ¿REQ-5 está dentro o fuera? | |
| OBS-12 | 86e1fawg0 Tokens de Flow Pilot | No se implementó el bloqueo por límite (403/429); Gemini no es compatible. | ¿Se acepta sin bloqueo? (Billing B bloquea por ai_credits: ver SAN-INT-06.) | |
| OBS-13 | 86e22fzq7 Reautorización | Se muestran toasts dobles. | ¿Se acepta como `low` en Improvements? | |
| OBS-14 | 86e2fazfh Endpoints | El límite de 5 endpoints por minado y el logo en el paso 2 salieron de una reunión, no de la spec. | ¿Se confirma el límite de 5 como regla de producto? | |
| OBS-15 | 86e21f52d Rebranding | Se usa la razón social "iond Inc." en lugar de retirarla. Los precios de la landing no coinciden (Free/Go/Pro contra Starter/Growth/Pro). Quedan ~84 referencias a "ionflow" (86e2buw9u). La landing no tiene blog (86e2czvzh). 86e2buw8e cambió nombres de BD y servicios en docker-compose. | ¿Razón social y precios definitivos? ¿Las referencias pendientes pasan a Improvements? | |
| OBS-16 | 86e25j0rn Notificaciones de IonMind | Notifica desde el 2.º intento fallido; la deduplicación usa una caché de 10 min (companyId+jobId) en vez de event_id; el email va por Laravel Mail y no por un flow de IOND; no hay tests. | ¿Se acepta el comportamiento? | |
| OBS-17 | 86e223kvf Rediseño de UI | El alcance decía "sin backend", pero se entregaron cambios en Gateway y Go (filtros y guard OBS-03). | Informativo: amplía la regresión de Boards (ya incluida). | |

## C. Riesgos de seguridad o de datos

| ID | Ticket | Riesgo | Cómo se verifica | Severidad si se confirma | Decisión PO |
|---|---|---|---|---|---|
| OBS-18 | 86e1qzefc (proxy de Logo.dev) | El proxy `force-update` podría aceptar el jobId de otro tenant: se infiere del código y no se probó. | SAN-86e1qzefc-AC-SEC y RGR-11 | `urgent` | |
| OBS-19 | 86e2g4ev0 (endpoints duplicados) | El guard de duplicados de `createFromIonmind` se retiró en el code review, después del QA. La limpieza de históricos requiere un backfill SQL manual y no se agregaron tests. | SAN-86e2g4ev0-AC-2/4 y RGR-04; el RM confirma si el backfill corre en preprod y en producción | `high` | |
| OBS-20 | 86e2j43eg (mensajería) | La evidencia de QA muestra "WhatsApp Business Platform" dos veces, un posible conector duplicado. El bypass de PROHIBITED_TERMS para developers.facebook.com no tiene tests. | SAN-86e2j43eg-AC-1 y RGR-05 | `high` | |
| OBS-21 | 86e20nmqx (costo de scraping) | El QA no demostró el cobro real, la idempotencia ni la concurrencia (dos usuarios con la misma URL). | SAN-86e20nmqx-AC-5/6 y SAN-INT-06 | `high` | |

## D. Cobertura de QA incompleta

Se cierran con las revalidaciones del sanity; la lista completa con sus verificaciones está en `sanity-matrix.md` § *Revalidaciones obligatorias*.

| ID | Tickets | Situación |
|---|---|---|
| OBS-22 | 86e35wv7f Websockets | En `mock testing` al preparar. Entra sí o sí: QA cierra su validación antes del corte, y un hallazgo posterior va por fix-forward (C-28). Validar la versión final: ws_token en localStorage, TTL de 1 día, scope obligatorio. |
| OBS-23 | 86e1fknjv + 86e1fkxz7, 86e1fky0g, 86e1qzefc (Logo.dev) | No tienen veredicto de QA. Además: source "ionmind" contra "crawler" de la spec, conflicto con `LOGO_DEV_AS_PRIMARY` y `force-update` sin `source` en la respuesta. |
| OBS-24 | Subtareas sin QA ni code review propio | 86e1y46c7, 86e1y46d0, 86e2epqqc, 86e2buw9e, 86e2czvzh, 86e2ft7a8 (sin PR ni evidencia), 86e2ft73m (solo code review), las subtareas del rebranding, las de billing 86e1pzz9e/c/h y las de la API 86e1wfgt2/uh/xk. |
| OBS-25 | 86e2mc23t Webcomponent del marketplace | La lógica de los atributos se invirtió el 2026-10-09 sin re-test. |
| OBS-26 | 86e22fzw2 Timer · 86e2j44hg, 86e2j45du | La evidencia de QA es solo visual o parcial. |
| OBS-27 | 86e1wfgam DevApp API 2.0 · 86e1mdnbq R2 | La API no expone el CRUD de connectors y mappers, y los mappers no tienen TC. `POST /accounts` da 422 por `remote_id`. En R2, el L3 registra BUG-CR-001: Force Update Logo llama a un endpoint eliminado y da 404. Los lotes de 50 por hora son lentos con colas grandes. IonMindControllerTest falla con 502 en la suite del gateway. |

## E. Datos de ClickUp

| ID | Observación |
|---|---|
| OBS-28 | Hay versiones, Project, Subcategory, Rejection_count, tags y campos de MR desactualizados. La lista para el SM y el RM está en `acciones-clickup.md`. Los PRs que figuran solo en comentarios están marcados *(comentario)* en `tickets.md` § *PRs por repositorio*; el RM los confirma antes del corte. |
