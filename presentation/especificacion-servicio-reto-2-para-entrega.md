# Especificación observable del servicio — Reto 2

**Corte:** último checkpoint disponible: 10 de octubre de 2026, 20:30 en Bolivia (11 de octubre, 00:30 UTC); registro hasta ID 868. El cierre oficial era 20:00 Colombia (21:00 Bolivia).  
**Estado:** parcial; describe lo comprobado y señala lo que aún no se conoce. No afirma equivalencia total.  
**Fuentes:** README y ejemplos oficiales conservados en `raw/referencias/frontier-reto-2/` del vault; registro experimental descargable junto a esta especificación. Las fuentes del vault no se incluyen en este micrositio.

Los IDs de evidencia remiten a output/experimentos.jsonl, salvo cuando se indica que pertenecen a los veinte ejemplos oficiales. “Confirmado” se limita a los datos y estados citados; no significa que se haya descubierto una regla universal.

## 1. Entrada

| ID | Comportamiento | Evidencia | Confianza |
|---|---|---|---|
| EN-01 | Las llamadas protegidas requieren Authorization Bearer. El token del reemplazo es distinto del token del servicio original. | Contrato del reto; IDs 1, 5, 34–35 | Confirmado en las rutas probadas |
| EN-02 | GET /health devuelve 200 con {"ok":true} cuando el servicio está listo y autorizado. | IDs 1, 5, 34–35 | Confirmado |
| EN-03 | POST /__reset devuelve 200 con {"ok":true} y restablece el estado antes de cada evaluación. | Contrato del reto; IDs 64, 71, 132–134, 154 | Confirmado |
| EN-04 | POST /msg recibe un objeto JSON con el campo textual m; la orden y sus argumentos van separados por punto y coma. | Ejemplos oficiales 1–20; IDs 2–832 | Confirmado para los formatos citados |
| EN-05 | Las combinaciones de ruta y método desconocidas probadas devuelven 404 con E404 y “ruta desconocida”. La matriz completa no se exploró. | IDs 36, 88–93, 102–104 | Confirmado en los casos probados |
| EN-06 | El reemplazo debe aceptar también rutas inexistentes y hacer que /__reset sin autorización se comporte como el original. | README del reto | Requisito del reto; cobertura parcial |

## 2. Integridad

| ID | Comportamiento | Evidencia | Confianza |
|---|---|---|---|
| IN-01 | Los mensajes normales tienen forma ORDEN;argumentos;control. El significado y la aceptación del último dato cambian según la orden. | Ejemplos oficiales 1–20; IDs 2–832 | Confirmado como formato observado; regla general pendiente |
| IN-02 | JSON vacío o inválido devuelve 400, E100, “json inválido”. | IDs 82, 108 | Confirmado para los cuerpos probados |
| IN-03 | Si m falta, es nulo o no es texto, o el JSON superior no es un objeto, devuelve 400, E102, “falta m”. | IDs 83–86, 98–101, 829–832 | Confirmado para los casos citados |
| IN-04 | Mensajes sin el último dato de control devuelven 400, E103, “falta control” en los vectores probados. | IDs 109–110 | Confirmado |
| IN-05 | Un segmento vacío devuelve 400, E104, “segmento vacío” en los casos probados. | IDs 111, 176 | Confirmado |
| IN-06 | Un control con caracteres no numéricos devuelve 400, E201, “control mal formado”. | Ejemplo oficial 17; IDs 32–33, 51, 53, 55 | Confirmado |
| IN-07 | Un control numérico rechazado devuelve 400, E202, “control inválido”. No se conoce una fórmula universal. | Ejemplo oficial 2; IDs 38, 115, 117, 119, 121 | Confirmado para esos mensajes; regla general pendiente |
| IN-08 | Una cantidad incorrecta de segmentos devuelve 400, E302, “aridad inválida” en el ejemplo probado. | Ejemplo oficial 20; ID 50 | Confirmado para el vector citado |
| IN-09 | Una orden desconocida con control numérico devuelve 400, E301, “comando desconocido ”; el mensaje observado conserva un espacio final. | Ejemplo oficial 12; IDs 54–55, 166 | Confirmado para los vectores citados |
| IN-10 | La prioridad entre errores se conoce solo en algunas combinaciones. En varios casos, un control mal formado se revisó antes que la orden o el número de segmentos. | IDs 32–33, 51–55 | Parcial; no generalizar |

## 3. Comandos

| ID | Comportamiento | Evidencia | Confianza |
|---|---|---|---|
| CO-01 | PING;64 devuelve 200 con {"pong":true}. También se aceptaron algunas variantes, pero no se conoce la regla general del control. | Ejemplo oficial 1; IDs 2, 6–10, 113 | Confirmado para los casos citados |
| CO-02 | ALTA;Lucia;82 crea AC-0001 y ALTA;Mateo;3 crea AC-0002 en la secuencia oficial. | Ejemplos oficiales 2–4; IDs 25–41 | Confirmado para esos datos |
| CO-03 | CONSULTA devuelve identificador de cuenta y saldo. Una cuenta inexistente devuelve E401. La representación del saldo cambió en la versión 2; ver sección 6. | Ejemplos oficiales 5, 8, 11, 15; IDs 75–76, 159–181, 731, 840 | Confirmado en los casos citados |
| CO-04 | DEPOSITO;AC-0001;250000;86 acepta el depósito y devuelve 200 con status “recieved” y operación OP-0001. El texto “recieved” se conserva literalmente. | Ejemplo oficial 6; IDs 42, 172, 186–187 | Confirmado para el vector citado |
| CO-05 | TRANSFER;AC-0001;AC-0002;40000;86 acepta la transferencia oficial y crea OP-0002. Una transferencia sin saldo suficiente devuelve 422, E507, “saldo insuficiente” en el caso probado. | Ejemplos oficiales 7, 16; IDs 64–70, 77–80 | Confirmado para esos casos |
| CO-06 | La transferencia 100000 con control 12 se comporta de forma distinta en las versiones 1 y 2; ver sección 6. | Ejemplo oficial 10; IDs 453, 694, 733, 845 | Confirmado para el vector y estados citados |
| CO-07 | ANULA;OP-0003;66 revierte una operación existente en la versión 1; repetir la anulación devuelve 200, ok false y motivo “ya anulada”. | Ejemplos oficiales 13–14; IDs 46, 49, 182–196 | Confirmado para los casos citados |
| CO-08 | Anular una operación inexistente devuelve 404, E402, “operación inexistente”. | IDs 736, 848 | Confirmado para el caso citado |

## 4. Memoria entre requests

| ID | Comportamiento | Evidencia | Confianza |
|---|---|---|---|
| ME-01 | El servicio recuerda cuentas y saldos entre mensajes. Crear, depositar y transferir cambia lo que devuelve una consulta posterior. | Ejemplos oficiales 3–11, 18–19; IDs 64–80, 172–187 | Confirmado en esas secuencias |
| ME-02 | Las operaciones aceptadas reciben identificadores como OP-0001 y OP-0002. La regla completa de asignación no está explorada. | Ejemplos oficiales 6–7, 10, 18 | Confirmado para la secuencia oficial |
| ME-03 | En los ejemplos oficiales, un depósito y una transferencia afectan el saldo consultado después; la cuenta AC-0002 muestra 40000 tras una transferencia de 40000. | Ejemplos oficiales 6–8 | Confirmado para la secuencia citada |
| ME-04 | Una anulación aceptada revierte la operación; repetirla no la vuelve a revertir y comunica que ya estaba anulada. | Ejemplos oficiales 13–14 | Confirmado |
| ME-05 | El reto exige reiniciar el estado antes de cada caso. La réplica implementada guarda los datos en la memoria del proceso. | README del reto; IDs 64, 71, 132–134, 154 | Requisito confirmado; persistencia del original tras reinicio no observada |
| ME-06 | En la versión 2, el rechazo impide crear OP-0003. Anularla devuelve E402; en la secuencia anterior, la siguiente operación aceptada usó OP-0003. | IDs 733, 736–737, 741, 845–850; repetición IDs 863, 866–868 | Confirmado en las secuencias citadas; es una consecuencia, no una regla aparte |

## 5. Errores

| ID | Comportamiento | Evidencia | Confianza |
|---|---|---|---|
| ER-01 | E001: 401, “no autorizado”, para accesos protegidos sin credencial válida en los casos probados. | IDs 1, 5, 34–35 | Confirmado en las rutas probadas |
| ER-02 | E100: 400, “json inválido”. | IDs 82, 108 | Confirmado |
| ER-03 | E102: 400, “falta m”. | IDs 83–86, 98–101, 829–832 | Confirmado |
| ER-04 | E103: 400, “falta control”. | IDs 109–110 | Confirmado |
| ER-05 | E104: 400, “segmento vacío”. | IDs 111, 176 | Confirmado |
| ER-06 | E201: 400, “control mal formado”. | Ejemplo oficial 17; IDs 32–33, 51, 53, 55 | Confirmado |
| ER-07 | E202: 400, “control inválido”. | Ejemplo oficial 2; IDs 38, 115, 117, 119, 121 | Confirmado para los vectores citados |
| ER-08 | E301: 400, “comando desconocido ” con espacio final observado. | Ejemplo oficial 12; IDs 54–55, 166 | Confirmado |
| ER-09 | E302: 400, “aridad inválida”. | Ejemplo oficial 20; ID 50 | Confirmado para ese caso |
| ER-10 | E401: 404, “cuenta inexistente”. | Ejemplo oficial 15; IDs 75–76, 159–181 | Confirmado |
| ER-11 | E402: 404, “operación inexistente”. | IDs 736, 848 | Confirmado para el caso citado |
| ER-12 | E404: 404, “ruta desconocida” para rutas o métodos no reconocidos probados. | IDs 36, 88–93, 102–104 | Confirmado para esos casos |
| ER-13 | E506: 422, “límite excedido”, para la transferencia concreta que la versión 2 rechaza. | IDs 453, 694, 733, 845 | Confirmado para ese vector; límite general pendiente |
| ER-14 | E507: 422, “saldo insuficiente”, para la transferencia sin fondos del ejemplo público. | Ejemplo oficial 16; IDs 77–80 | Confirmado para el caso citado |
| ER-15 | No se conoce el orden completo de revisión de credenciales, formato, orden y argumentos. | IDs 32–33, 51–55 y conjunto experimental | Parcial; hacen falta casos que separen cada prioridad |

## 6. Cambios durante el día

| ID | Comportamiento | Evidencia | Confianza |
|---|---|---|---|
| CH-01 | En la versión 1, el saldo se devolvía como número entero; en la versión 2, como texto con dos decimales. Los valores comparados también reflejan una división por 100. | Ejemplos oficiales 5, 8, 11, 19; IDs 728, 731, 734, 742; IDs 840, 846–850, 858, 864–868 | Confirmado en esos valores; regla para todos los importes desconocida |
| CH-02 | La transferencia de 100000 con control 12, aceptada en la versión 1, devuelve en la versión 2 422 E506 (“límite excedido”) en los estados comparados. | Ejemplo oficial 10; versión 1 IDs 262–267; versión 2 IDs 453, 694, 733, 845, 863 | Confirmado para ese vector; no demuestra un umbral universal |
| CH-03 | El rechazo evita crear OP-0003; por eso la anulación devuelve E402. En una secuencia anterior, la siguiente operación aceptada recibió OP-0003 en vez de OP-0004. | Versión 2 IDs 736–737, 741, 845–850; repetición 863, 866–868 | Confirmado como efecto de CH-02; no contar como cambio independiente probado |
| CH-04 | El aviso del incidente declaró tres cambios. Se confirmaron dos comportamientos distintos; no se aisló una tercera regla independiente. El cambio en tipo y escala del saldo podría contarse de formas diferentes, pero el organizador no aclaró su agrupación. | Repetición de ejemplos IDs 723–743; canarios IDs 833–868; ticket FR-0153 | Tercer cambio pendiente; no inferir ni inventar |
| CH-05 | El checkpoint más reciente volvió a encontrar saldo como texto decimal, el rechazo E506 y E402 al intentar anular la operación que no llegó a crearse. | IDs 851–868; registro del monitor del 11-oct-2026 00:30 UTC | Confirmado en esa secuencia; no demuestra una tercera regla independiente |

## 7. Riesgos

| ID | Comportamiento | Evidencia | Confianza |
|---|---|---|---|
| RI-01 | La primera evaluación reservada obtuvo 22/100. Sus casos no fueron revelados, así que no puede asignarse cada fallo a una regla. | Resultado de Frontier registrado en wiki/estado/estado-actual.md | Puntaje confirmado; causas individuales desconocidas |
| RI-02 | Los controles de ALTA, DEPOSITO y TRANSFER no están caracterizados para todos los valores; ejemplos aceptados no prueban una fórmula general. | Ejemplos oficiales 2–20; IDs 25–80, 115–121 | Parcial; riesgo de cobertura |
| RI-03 | No se conoce el límite de transferencia fuera del vector 100000 con control 12 ni su relación con saldo o movimientos anteriores. | IDs 453, 694, 733, 845 | Parcial |
| RI-04 | La tercera regla independiente anunciada en el incidente no se identificó. Los efectos en cadena no bastan para demostrarla. | IDs 723–743, 833–868 | Pendiente |
| RI-05 | Rutas, métodos, errores y prioridad de validaciones solo se probaron en parte. | IDs 36, 82–121; conjunto experimental | Parcial |
| RI-06 | Los IDs 3–4 no tienen respuesta confirmada y el texto del ID 30 está dañado por codificación. No deben usarse como respuestas funcionales concluyentes. | IDs 3, 4, 30; validador del banco local | Limitación confirmada |
| RI-07 | Las pruebas conocidas no demuestran que la réplica coincida en todos los casos no probados. | Resultado 22/100; contrato de evaluación del README | Límite confirmado |
| RI-08 | La réplica guarda su estado en la memoria del proceso. Reinicios o varias instancias simultáneas requieren cuidado para no perder o separar datos. | Implementación de la réplica y requisito de /__reset | Riesgo del diseño; no describe al original |

### Alcance de la evidencia

El registro canónico es output/experimentos.jsonl, con 868 entradas hasta el último checkpoint disponible (10-oct-2026 20:30 Bolivia / 11-oct-2026 00:30 UTC). No representa vigilancia completa hasta el cierre oficial de 21:00 Bolivia. Se conserva cada intento; los fallos de conexión no se completan por inferencia. Esta especificación resume los comportamientos importantes y no afirma que se hayan probado todas las entradas posibles. El servicio entregado no depende del original.
