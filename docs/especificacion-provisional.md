---
type: arquitectura
tags: [reto-2, caja-negra, especificacion, evidencia]
created: 2026-10-10
updated: 2026-10-10
status: en-revision
sources:
  - "[[raw/referencias/frontier-reto-2/README]]"
  - "[[raw/referencias/frontier-reto-2/pruebas/ejemplos]]"
  - "[[output/experimentos]]"
---

# Especificación provisional del servicio — evidencia disponible

**Especificación histórica y provisional.** Las secciones base compilan la línea de referencia y observaciones previas a la captura explícita de V2; no se deben usar solas como contrato vigente. El [addendum del incidente V2](incidente-v2.md) contiene los overrides confirmados desde el replay V2 (ID 723 en adelante) y es la referencia para la implementación actual. El log íntegro llega al ID 832. La columna «Evidencia» cita el log **propio**; `confirmado` se reserva para una observación repetida; `probable` cubre una muestra o inferencia limitada; `supuesto` indica una decisión aún sin prueba. La [estrategia experimental](estrategia-experimental-reto-2.md) indica cómo promover reglas.

## 1. Entrada

| ID | Comportamiento observable | Evidencia del log | Confianza |
|---|---|---|---|
| EN-01 | `GET /health` con token personal válido devolvió 200 `{"ok":true}`. | 1, 5 | confirmado para este método/ruta |
| EN-02 | `GET /health` sin token y con token inválido devolvió 401 `{"error":"E001","mensaje":"no autorizado"}`. | 34, 35 | probable para ambas variantes; falta repetición |
| EN-03 | `GET /ruta-inexistente-prueba` con token válido devolvió 404 `{"error":"E404","mensaje":"ruta desconocida"}`. | 36 | probable; otras rutas/métodos pendientes |
| EN-10 | La misma ruta inexistente devolvió 404 E404 tanto con GET sin credencial como con POST y credencial inválida. | 92–93 | probable para los dos casos; no fija precedencia para rutas conocidas con auth inválida |
| EN-04 | `POST /msg` con cuerpo JSON `{"m":"PING;64"}` devolvió 200 `{"pong":true}`. | 2, 8, 10, 18 | confirmado para este mensaje literal |
| EN-05 | `POST /__reset` con token válido devolvió 200 `{"ok":true}`; sin token o con token inválido devolvió 401 E001 `no autorizado`. | 64, 71, 132–134, 154 | confirmado para las variantes probadas |
| EN-06 | Con token válido, las combinaciones ensayadas `OPTIONS`/`PUT /health`, `GET /msg`, `POST /health` y `GET /__reset` devolvieron 404 E404 `ruta desconocida`. | 88–89, 102–104 | probable para cada combinación; matriz HTTP incompleta |
| EN-07 | `POST /msg` con cuerpo vacío o JSON sintácticamente inválido devolvió 400 E100 `json inválido`. | 82, 108 | probable para esas entradas |
| EN-08 | `POST /msg` con `m` ausente, null o no textual, o JSON superior no objeto, devolvió 400 E102 `falta m`. | 83–86, 98–101 | probable para esas formas |
| EN-09 | Con estado tras el replay oficial, `CONSULTA;AC-0001;14` más una propiedad JSON extra devolvió 200 con saldo 210000. No se ejecutó una consulta idéntica sin la propiedad extra en ese mismo estado. | 175; estado previo 154–174 | probable solo para esta propiedad y request |

Para una ruta inexistente, los casos 92–93 devolvieron E404 antes de que la credencial cambiara la respuesta; para `POST /msg`, la autenticación inválida precedió el parseo del cuerpo en 94 y 135. No se conoce la precedencia global para cada ruta, método y tipo de cuerpo. El token del reemplazo es otro y debe verificarse como indica el README; jamás se envía al original.

## 2. Integridad

| ID | Comportamiento observable | Evidencia del log | Confianza |
|---|---|---|---|
| IN-01 | `ALTA;Lucia;83` devolvió 400 E202 `control inválido`; la grafía íntegra se capturó tras corregir UTF-8. | 38; 30 solo para código/status | probable |
| IN-02 | `ALTA;Lucia;Gomez;5X` devolvió 400 E201 `control mal formado`, aun con aridad incorrecta. | 32–33 | probable, solo este par de fallos |
| IN-03 | `SALDOS;AC-0001;5X` devolvió 400 E201 antes de informar comando desconocido. | 52–53 | probable, solo este par de fallos |
| IN-04 | `{"m":""}` y `PING` sin separador devolvieron E103 `falta control`; `PING;` devolvió E104 `segmento vacío`. | 109–111 | probable para estas entradas |
| IN-05 | `CONSULTA;AC-0001;14 ` y `CONSULTA;AC-0001;014` devolvieron E201 `control mal formado`. | 139–140 | probable para esos formatos |
| IN-06 | Controles alterados para `ALTA` fueron rechazados con E202 `control inválido`: `Lucia;81`, `Lucia;84`, `Mateo;82` y `Lucia;3`. | 115, 117, 119, 121 | probable por cada par nombre-control; fórmula desconocida |
| IN-07 | Tras el replay oficial, `CONSULTA;;14` devolvió 400 E104 `segmento vacío`. | 176 | probable para ese mensaje; no fija prioridad global |
| IN-08 | Para `CONSULTA;AC-XXXX`, `(17 - 3 × número_de_cuenta) mod 97` es un control candidato compatible con los IDs ensayados; el control predicho de cuentas inexistentes llegó a E401, y vecinos rechazados dieron E202. | 177–181; `sites/caja-negra-lab/infer_consulta_control.py` | probable; fórmula observacional, no implementación interna confirmada |
| IN-09 | Para `ANULA;OP-XXXX`, `(75 - 3 × número_de_operación) mod 97` es candidato: OP-0005 con 60 llegó a E402 antes de existir y se anuló tras crearse; con 61 dio E202. OP-0004 con 63 se anuló. | 167, 182–184, 195–196 | probable para formato probado |

**Desconocido crítico:** no conocemos una fórmula común a todos los comandos. Hay candidatas contrastadas para CONSULTA y ANULA, pero DEPOSITO no heredó la pendiente ensayada y ALTA permanece abierta (IDs 186–194). `PING;XX` también devolvió pong (IDs 6–8), de modo que no debe aplicarse un validador universal sin nueva evidencia.

## 3. Comandos

### PING

| ID | Comportamiento observable | Evidencia del log | Confianza |
|---|---|---|---|
| CO-06 | `PING;64` devolvió 200 `{"pong":true}`; `ping;64` también devolvió pong. | 2, 8, 10, 18, 113, 155 | confirmado para el literal en mayúsculas; probable para minúsculas |

### ALTA

| ID | Comportamiento observable | Evidencia del log | Confianza |
|---|---|---|---|
| CO-01 | Desde reset, `ALTA;Lucia;82` produjo 201 y `AC-0001`; `ALTA;Mateo;3` produjo `AC-0002` tras aquella. | 25–28, 39–41 | confirmado para esas entradas y órdenes |
| CO-07 | Dos altas nominalmente idénticas consecutivas produjeron cuentas distintas; `alta;Lucia;82` produjo `AC-0001` tras reset. | 71–73, 141–142 | probable para duplicado y variante de mayúsculas probados |

### CONSULTA

| ID | Comportamiento observable | Evidencia del log | Confianza |
|---|---|---|---|
| CO-08 | `CONSULTa;AC-0001;14` y `consulta;AC-0001;14` devolvieron 200 con cuenta y saldo 0 después de crearla. | 136–138, 151–153 | probable para esas variantes |
| CO-10 | En el replay oficial, consultas de `AC-0001` y `AC-0002` reflejaron los saldos tras depósitos, transferencias y anulación; una cuenta inexistente devolvió E401/404. | 159, 162, 165, 169, 173 | probable para esa secuencia; también ver ER-05 |

### DEPOSITO

| ID | Comportamiento observable | Evidencia del log | Confianza |
|---|---|---|---|
| CO-02 | En secuencia conocida, `DEPOSITO;AC-0001;250000;86` produjo 200 `{"status":"recieved","operacionId":"OP-0001"}`. | 42; 14 | confirmado para esa preparación |

| CO-13 | `DEPOSITO;AC-0002;700;35` produjo OP-0004 en el replay. Con AC-0002 y monto 250000, controles 83 y 86 devolvieron E202; después, sin depósitos exitosos intermedios, el vector conocido de AC-0001 produjo OP-0005. | 172, 186–187, 195 | probable para estos vectores; el rechazo no consumió ID de operación en esta secuencia |

### TRANSFER

| ID | Comportamiento observable | Evidencia del log | Confianza |
|---|---|---|---|
| CO-03 | Transferencias de 40000 y 100000, tras preparar cuentas y depósito, produjeron `OP-0002` y `OP-0003`. | 43–44 | probable para esa secuencia |
| CO-14 | Para `TRANSFER;AC-0001;AC-0002;40000`, el control 86 fue aceptado; al cambiar solo el control a 87, el servicio devolvió E202. Los saldos se conservaron y el siguiente vector válido recibió OP-0003. Esto confirma el contraste solo para esa secuencia, no una fórmula general. | 239–244 | probable para esta combinación; regla general pendiente |

### ANULA

| ID | Comportamiento observable | Evidencia del log | Confianza |
|---|---|---|---|
| CO-04 | `ANULA;OP-0003;66` produjo 200 `{"ok":true,"anulada":"OP-0003"}`; repetirla produjo 200 `{"ok":false,"motivo":"ya anulada"}`. | 46, 49 | probable para esa operación y secuencia |
| CO-09 | Anular el depósito `OP-0003` redujo el saldo de `AC-0001` de 460000 a 210000 en una secuencia observada. | 122–130 | probable para esa operación |
| CO-11 | Anular el depósito `OP-0004` devolvió 200 `{"ok":true,"anulada":"OP-0004"}`; luego `AC-0002` mostró 40000 en vez de los 40700 consultados antes. | 173, 184–185 | probable para esta operación y secuencia |
| CO-12 | Repetir `DEPOSITO;AC-0001;250000;86` generó `OP-0005`; `ANULA;OP-0005;60` devolvió 200 `{"ok":true,"anulada":"OP-0005"}`. | 195–196; preparación 154–194 | probable para esta secuencia; saldo posterior no consultado |

Estos bloques describen entradas concretas. No se conoce una fórmula general para controles ni todos los límites de montos, reversas y errores de cada comando.

## 4. Memoria entre requests

| ID | Comportamiento observable | Evidencia del log | Confianza |
|---|---|---|---|
| ME-01 | Un reset entre dos `ALTA;Lucia;82` hizo que ambas devolvieran `AC-0001`. | 25–28 | confirmado para ID de cuenta en esta secuencia |
| ME-02 | Un alta rechazada por control no desplazó el ID de la siguiente alta válida, que recibió `AC-0001`. | 29–31 | probable para este error |
| ME-03 | Antes de anular `OP-0003`, el origen tenía saldo 110000; después, 210000. El destino consultado después tenía 40000. | 45–48 | probable: reversión de esta transferencia; saldo previo del destino no medido directamente |
| ME-04 | Tras un rechazo E506 de transferencia, la siguiente transferencia aceptada recibió `OP-0003` después de `OP-0002`; ese rechazo no consumió el siguiente ID en esta secuencia. | 64–70 | probable |
| ME-05 | Repetir un alta nominalmente idéntica creó otra cuenta con ID distinto. | 71–73 | probable |
| ME-06 | Al anular el depósito `OP-0003`, el saldo observado de `AC-0001` pasó de 460000 a 210000; después `AC-0002` mostró 40000. | 122–131 | probable; no prueba todos los casos de anulación |
| ME-07 | El mismo `ANULA;OP-0005;60` devolvió E402 antes de que existiera la operación y 200 con anulación después de que un depósito recibiera ese ID. | 182, 195–196 | probable para este cambio de estado |
| ME-08 | Tras un reset posterior a saldos 210000/40000, la AC-0001 recreada consultó cero; el OP-0001 anterior dio E402 y un nuevo depósito reutilizó ese ID y pudo anularse. AC-0002 y OP-0002 antiguos no se consultaron tras reset. | 214–234 | probable para este escenario |

## 5. Errores

| ID | Comportamiento observable | Evidencia del log | Confianza |
|---|---|---|---|
| ER-01 | Control final no numérico en las dos combinaciones probadas devolvió 400 E201 `control mal formado` antes de E302/E301. | 33, 51, 53, 55 | probable; precedencia parcial, no total |
| ER-02 | Aridad incorrecta con control numérico en `ALTA;Lucia;Gomez;11` devolvió 400 E302 `aridad inválida`. | 50–51 | probable |
| ER-03 | Comando desconocido con control numérico en `SALDOS;AC-0001;38` devolvió 400 E301 `comando desconocido `; conservar el espacio final. | 54–55 | probable |
| ER-04 | Ausencia/token inválido para `GET /health`: 401 E001 `no autorizado`. | 34–35 | probable |
| ER-05 | `CONSULTA` de `AC-0009` tras reset devolvió 404 E401 `cuenta inexistente`. | 75–76, 169 | probable para las secuencias probadas |
| ER-06 | `TRANSFER` de 50000 desde `AC-0002` sin fondos devolvió 422 E507 `saldo insuficiente`. | 77–80, 170 | probable para las secuencias probadas |
| ER-07 | `TRANSFER` de 120000 devolvió 422 E506 `límite excedido` en una secuencia preparada. | 64–69, 163 | probable; umbral general no determinado |
| ER-08 | `PING;64;X` devolvió 400 E302 `aridad inválida`. | 112 | probable |
| ER-09 | `POST /msg` sin credencial y con JSON inválido devolvió 401 E001; con credencial válida y JSON inválido devolvió 400 E100. | 82, 135 | probable: precedencia solo en este par |
| ER-10 | `SALDOS;AC-0001;38` devolvió 400 E301 `comando desconocido ` con espacio final. | 54–55, 166 | probable para ese literal |
| ER-11 | `ANULA;OP-0005;60` devolvió 404 E402 `operación inexistente`; control vecino 61 para el mismo ID devolvió 400 E202. | 182–183 | probable para el par y esa precedencia |

No tratar errores de transporte (IDs 3–4) como respuestas del servicio. El ID 30 tiene texto mojibake por el cliente local; ID 38 es la referencia de grafía exacta.

## 6. Cambios durante el día

| ID | Comportamiento observable | Evidencia del log | Confianza |
|---|---|---|---|
| CH-01 | El canario de ocho pasos coincidió entre línea base y dos repeticiones previas al incidente. | 9–24, 56–63; `output/drift-latest.json` | confirmado **solo entre esas mediciones** |
| CH-02 | El canario de ocho pasos de las 16:41 UTC coincidió con su línea base; ambas mediciones fueron antes del incidente de las 20:30 UTC. | 143–150; `output/drift-reports/20261010T164125Z.json` | confirmado solo para esos ocho pasos |
| CH-03 | A las 16:57–16:58 UTC, una repetición desde reset de los 20 ejemplos oficiales de la mañana coincidió en status y cuerpo en los 20 pasos. | 154–174; `output/example-replay-latest.json` | confirmado para esa secuencia y ese horario |

No existe todavía medición posterior al incidente anunciado para las 15:30 Colombia (16:30 Bolivia / 20:30 UTC). Si aparece una diferencia, registrar último instante estable, primera divergencia, IDs, posible causa de infraestructura y nueva prueba desde reset. No cambiar el baseline antiguo ni reescribir líneas.

## 7. Riesgos

| ID | Riesgo y decisión provisional | Evidencia | Confianza |
|---|---|---|---|
| RI-01 | Si se desconoce una respuesta, la réplica debe escoger y documentar un comportamiento por defecto; no presentar como descubierto lo que no se probó. | Contrato del README | supuesto para futuros casos |
| RI-02 | Un algoritmo de control inventado o un orden de errores demasiado generalizado puede fallar en tests ocultos; investigar antes de codificar. | Ejemplos + IDs 33, 38, 51, 53, 55 | riesgo razonado |
| RI-03 | El estado en memoria funciona bajo el contrato de un proceso; reinicios/múltiples instancias pueden romper continuidad fuera de ese contrato. | README | decisión arquitectónica, no comportamiento del original |
| RI-04 | La respuesta de operaciones usa literalmente `recieved`. Un cliente nuevo no debería depender de esa grafía: conservarla en la interfaz compatible y corregirla solo en una interfaz nueva versionada. | 42–44, 160–161, 164, 172 | confirmado para las respuestas observadas; cierre propuesto |
| RI-05 | El mensaje E301 incluye un espacio final. Un cliente nuevo debería identificar errores por código, manteniendo el texto literal únicamente en la interfaz compatible. | 54–55, 166 | probable para ese error; cierre propuesto |

## Anexo de evidencia posterior — corte IDs 64–196

La matriz precedente se compiló originalmente hasta ID 63 y se actualizó con evidencia posterior sin reescribir observaciones. El registro fuente completo está en [[output/experimentos]] y la interpretación metodológica en [[wiki/consultas/descubrimiento-caja-negra-2026-10-10]].

| Área | Comportamiento observado | Evidencia | Estado |
|---|---|---|---|
| Parseo HTTP | `POST /msg` con JSON sintácticamente inválido o vacío → 400 E100; con `m` ausente/null/no texto → 400 E102. JSON superior que no es objeto también dio E102. | 82–86, 98–101, 108 | verificado para casos ensayados |
| Content-Type | PING JSON aceptado bajo text/plain, XML, octet-stream y application/json con charset. | 87, 95–97, 105–107 | provisional; solo esos tipos |
| Gramática | PING sin control → E103; control vacío final → E104; segmento extra → E302; `ping;64` → pong. | 109–113 | verificado para esos mensajes |
| Rutas/métodos | Métodos/rutas no coincidentes probados dieron E404; HEAD no produjo cuerpo observable. | 88–93, 102–104 | provisional; no cubre matriz completa |
| Orden auth/parser | POST `/msg` sin auth + cuerpo inválido dio E001; `/__reset` también requiere auth. | 94, 132–135 | probable: auth antes de parsear en POST `/msg` probado |
| Control | ALTA con valores de control cruzados 81,84,82,3 fue rechazada; CONSULTA con espacio final o 014 fue E201. | 115,117,119,121,139–140 | fórmula pendiente; no brute force |
| Rechazo/contador OP | E506 precedió a éxito con `OP-0003`; no se consumió ID en el rechazo de esa secuencia. | 64–70 | probable |
| Dominio | Duplicado nominal crea otra cuenta; cuenta inexistente → E401/404; saldo insuficiente → E507/422. | 71–80 | verificado para entradas de prueba |
| Anulación | Anular depósito de 250000 bajó saldo 460000→210000; destino quedó observado en 40000. | 122–131 | probable para esa secuencia |
| Mayúsculas | `alta` y `consulta` minúsculos tuvieron éxito; `CONSULTa` también. | 138,142,151–153 | probable para ALTA y CONSULTA; otros comandos pendientes |
| Canario previo al incidente | Canario de ocho pasos sin diferencias frente a baseline. Corrida a las 16:41 UTC (12:41 Bolivia), antes del incidente previsto a 16:30 Bolivia. | 143–150; `output/drift-reports/20261010T164125Z.json` | no cambio detectado en cobertura canario únicamente; corrida posterior pendiente |
| Replay de mañana | Reset más 20 ejemplos oficiales, coincidencia en los 20 pares status/cuerpo. | 154–174; `output/example-replay-latest.json` | verificado para esa secuencia y corte temporal |
| Entradas adicionales | Consulta de cuenta existente con propiedad JSON extra devolvió saldo 210000; cuenta vacía `CONSULTA;;14` dio E104. | 175–176 | probable para esos casos |
| Candidatos de control | CONSULTA: candidato lineal módulo 97 validado en varios IDs; ANULA: candidato similar para operación. DEPOSITO no heredó el mismo paso al cambiar cuenta; dos predicciones para ALTA con cambio de penúltima letra fallaron. | 177–190; [[wiki/consultas/analisis-control-reto-2]] | provisional para las fórmulas, verificado para las respuestas individuales |
| Familia de hash para ALTA descartada | Cuatro bases de rolling hash con multiplicador fijo ajustaban Lucia/Mateo/Lucib, pero sus cuatro predicciones para Lucja devolvieron E202. | 191–194; [[wiki/consultas/analisis-control-reto-2]] | refutación de esta familia, no de todas las fórmulas posibles |
| Operación ausente/presente | ANULA de OP-0005 con control 60 pasó de E402 a éxito cuando un depósito recibió ese ID. | 182, 195–196 | probable para este cambio de estado |

**Diseño:** estos resultados informan el contrato externo y el modelo de estado; no prescriben la arquitectura interna del servicio perdido. La arquitectura de réplica debe tratarse como una decisión explícita que se valida mediante pruebas diferenciales. La paridad completa y el descubrimiento exhaustivo siguen pendientes.

## Anexo de evidencia posterior — corte IDs 197–327

Las filas siguientes amplían las siete secciones exigidas por el README. Son observaciones del original por el banco local; una misma respuesta puntual no se presenta como regla universal.

### Entrada e integridad

| ID | Comportamiento observado | Evidencia del log | Confianza |
|---|---|---|---|
| EN-11 | En las rutas probadas, `/health?probe=1` y `/msg?probe=1` procesaron igual que sin query; `/health/` y `/msg/` dieron 404 E404. | 198–201 | probable para esas cuatro solicitudes |
| EN-12 | El cuerpo JSON con `m` array o `m` objeto devolvió 400 E102 `falta m`. | 304–305 | probable para esos dos tipos |
| EN-13 | JSON de nivel superior array devolvió E102; JSON válido con salto final procesó PING. | 203–204 | probable para esas entradas |
| IN-10 | Dos claves `m` con valores PING válido y `PING;64;X` dieron E302, compatible con que el último valor prevalezca. | 202 | probable para ese cuerpo duplicado; no define todos los duplicados |
| IN-11 | Tres altas consecutivas `Lucia;82`, `Lucib;79`, `Lucic;76` fueron aceptadas; la variante exacta `ALTA; Lucia;82` también fue aceptada. | 211, 280–282 | probable para esos vectores; no se deriva fórmula general |

### Comandos y memoria entre requests

| ID | Comportamiento observado | Evidencia del log | Confianza |
|---|---|---|---|
| CO-15 | `CONSULTA;ac-0001;14` y `CONSULTA; AC-0001;14` dan E401, mientras la clave canónica devuelve saldo. El control es aceptado, pero el lookup no normaliza esas grafías. | 285–287 | probable para lowercase completo y un espacio inicial |
| CO-16 | `deposito`, `transfer` y `anula` en minúsculas completaron las operaciones probadas; el depósito/transferencia generaron OP-0001/OP-0002. | 296–300 | probable para esos vectores; con PING/ALTA/CONSULTA hay ejemplos lowercase de los seis verbos |
| ST-06 | Anular después de que el receptor gastó parte del crédito revirtió la transferencia original y dejó AC-0002 con saldo −10000 en esa secuencia. | 274–278 | probable para ese estado y secuencia |
| ST-07 | Rechazos de control para transferencia y depósito no cambiaron saldo ni consumieron el siguiente ID de operación en las secuencias probadas. | 226–227, 242–244, 249–250, 290–292 | probable para esas ramas |
| ST-08 | Consultar cuenta inexistente AC-0002 con control 11 devolvió E401/404 y una consulta posterior de AC-0001 conservó saldo 0. | 306–309 | probable para esa secuencia |

### Errores, precedencia y controles

| ID | Comportamiento observado | Evidencia del log | Confianza |
|---|---|---|---|
| ER-12 | Transferencias `AC-0001→AC-0009;40000;86`, `AC-0001→AC-0002;100001;12`, `AC-0002→AC-0001;10000;23` y `...;40000;87` devolvieron E202. | 218, 220, 225, 240 | probable para cada vector; no es checksum general |
| ER-13 | `TRANSFER;AC-0001;AC-0002;120000;55` dio E506 aun sin saldo de origen; después el rechazo, un vector válido obtuvo OP-0002. | 265–267 | probable para ese par de validaciones |
| ER-14 | `ANULA;OP-0001;72` dio E402 antes de existir OP-0001 y éxito tras crear el depósito que recibió ese ID. | 231–234 | probable para ese ID y control |
| ER-15 | Reutilizar el control `DEPOSITO;...;700;35` de AC-0002 con AC-0001 dio E202; saldo e identificador no cambiaron. | 290–292 | probable para esa combinación |
| ER-16 | Un `m` JSON duplicado y `m` como array/objeto dieron E302 y E102 respectivamente; son errores distintos de JSON sintácticamente inválido E100. | 202, 304–305; comparación 82–86 | probable para estos casos |

### Cambios durante el día y riesgos de implementación

| ID | Comportamiento observable | Evidencia del log | Confianza |
|---|---|---|---|
| CH-04 | Se estableció una línea base de 18 respuestas a las 18:13:11 UTC. Es una captura, no una comparación antes/después ni evidencia posterior al incidente de las 20:30 UTC. | 310–327; `output/drift-latest.json` | confirmado sobre la captura; sin conclusión de drift |
| RI-06 | La réplica local usa vectores conocidos para controles de TRANSFER, y un fallback E202 para los no observados; no se ha descubierto una fórmula universal. | Evidencia observada 218, 220, 225, 239–240, 265–267, 274; implementación `services/replica/domain.py` | supuesto para vectores desconocidos |
| RI-07 | La auditoría offline posterior a esos cambios comparó 258 observaciones elegibles y halló 258 coincidencias; 43 filas sin reset confirmado, 22 fuera del dominio y otros casos no comparables se excluyeron. | `python services/replica/audit_observed.py`; log hasta ID 327 | verificado solo para el subconjunto elegible, no paridad general |

Los controles generales de ALTA, DEPOSITO y TRANSFER, límites numéricos exhaustivos, todos los errores y todas las combinaciones de rutas/auth siguen pendientes. No promover `RI-06` a hecho sobre el original: describe deliberadamente el fallback de la réplica.

## Addendum vigente: incidente V2

Desde el replay V2 de IDs 723–832, esta página conserva evidencia histórica y el addendum V2 manda para la implementación: `CONSULTA.saldo` es texto decimal observado a escala `/100`, y el vector `TRANSFER` de 100000 recibe E506. En V2 también se observó `ALTA;Lucid;73` aceptado (IDs 749–750); no hay el mismo vector en la línea base V1, así que no se afirma que sea un cambio del incidente. La auditoría automatizada se limita por defecto a IDs >=723 para no comparar el modelo V2 contra respuestas históricas V1.
