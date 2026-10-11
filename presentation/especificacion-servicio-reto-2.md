# Especificación observable del servicio — Reto 2

**Corte de evidencia:** 10 de octubre de 2026, log hasta ID 832.  
**Estado:** especificación parcial de compatibilidad; no se afirma equivalencia total.  
**Fuentes:** `raw/referencias/frontier-reto-2/README.md`, `raw/referencias/frontier-reto-2/pruebas/ejemplos.jsonl` y `output/experimentos.jsonl` (IDs citados abajo).

## 1. Propósito y alcance

El objetivo es sustituir una caja negra HTTP sin código ni documentación. La equivalencia se mide por el status HTTP y el cuerpo JSON de cada paso, incluidos errores y cambios de estado. La especificación registra comportamiento externo observado; no pretende describir cómo está implementado internamente el original.

El registro de experimentos es la fuente primaria de observaciones. `confirmado` significa que el vector se reprodujo o se compara contra un ejemplo oficial; no significa que se conozca una regla universal. Una afirmación limitada a una combinación concreta se identifica expresamente como tal.

## 2. Contrato HTTP conocido

| Método/ruta | Comportamiento observado | Evidencia / alcance |
|---|---|---|
| `GET /health` | Con credencial válida: `200 {"ok":true}`. Sin credencial o inválida: `401 {"error":"E001","mensaje":"no autorizado"}`. | IDs 1, 5, 34–35; variantes observadas. |
| `POST /__reset` | Con credencial válida: `200 {"ok":true}`; devuelve el estado de la réplica al estado inicial según el contrato del reto. | IDs 64, 71, 132–134, 154; el reto lo invoca antes de cada caso oculto. |
| `POST /msg` | Recibe JSON con campo textual `m`, por ejemplo `{"m":"PING;64"}`. La respuesta observable consta de status y JSON. | Ejemplos oficiales y IDs 2–832. |
| Otras rutas o combinaciones | Las combinaciones ensayadas de ruta/método no reconocidas devolvieron `404 E404 ruta desconocida`; la matriz completa no está explorada. | IDs 36, 88–93, 102–104. |

El token usado para el original y el token del reemplazo son credenciales distintas. Nunca se incorporan a esta especificación ni al log como valores. La autenticación se evalúa en el servicio y el banco local mantiene el token del original fuera del navegador.

## 3. Formato del mensaje y validación

En los casos normales, `m` es una cadena separada por punto y coma: `COMANDO;argumentos...;control`. Los mensajes observados incluyen `PING`, `ALTA`, `CONSULTA`, `DEPOSITO`, `TRANSFER` y `ANULA`. La sensibilidad a mayúsculas no es uniforme en todos los campos; se observaron nombres de comando en minúsculas aceptados para varios vectores, pero no se demuestra una regla global.

| Condición observada | Resultado observado | Evidencia |
|---|---|---|
| JSON vacío o sintácticamente inválido | `400 E100`, `json inválido` | IDs 82, 108. |
| Campo `m` ausente, nulo o no textual; JSON superior no objeto | `400 E102`, `falta m` | IDs 83–86, 98–101, 829–832. |
| Control ausente en mensajes de comando observados | `400 E103`, `falta control` | IDs 109–110. |
| Segmento vacío | `400 E104`, `segmento vacío` | IDs 111, 176. |
| Control con caracteres no numéricos | `400 E201`, `control mal formado` | Ejemplo oficial 17; IDs 32–33, 51, 53, 55. |
| Control numérico no aceptado para ese vector | `400 E202`, `control inválido` | Ejemplo oficial 2; IDs 38, 115, 117, 119, 121. |
| Aridad no admitida en el vector | `400 E302`, `aridad inválida` | Ejemplo oficial 20; ID 50. |
| Comando desconocido con control numérico | `400 E301`, `comando desconocido ` (con espacio final en el caso observado) | Ejemplo oficial 12; IDs 54–55, 166. |

La precedencia entre errores está solo parcialmente determinada. Por ejemplo, un control mal formado precedió a errores de aridad/comando en algunas combinaciones (IDs 32–33, 51–55); no se infiere una prioridad universal.

## 4. Comandos y efectos observados

| Comando | Contrato observado en vectores concretos | Evidencia |
|---|---|---|
| `PING` | `PING;64` → `200 {"pong":true}`. También se aceptaron algunos valores de control alternos y el nombre en minúscula; no se generaliza la validación de control. | Ejemplo oficial 1; IDs 2, 6–10, 113. |
| `ALTA` | `ALTA;Lucia;82` → `201 {"cuentaId":"AC-0001"}` tras reset; siguiente alta aceptada creó `AC-0002`. Algunos controles inválidos devuelven E202. | Ejemplos oficiales 2–4; IDs 25–41. |
| `CONSULTA` | Para cuenta existente devuelve `200` con `cuenta_id` y `saldo`; inexistente: `404 E401 cuenta inexistente`. En V1 el saldo observado es número entero; en V2, ver sección 5. | Ejemplos oficiales 5, 8, 11, 15; IDs 75–76, 159–181. |
| `DEPOSITO` | Vector oficial `DEPOSITO;AC-0001;250000;86` → `200 {"status":"recieved","operacionId":"OP-0001"}`. El servicio conserva literalmente `recieved`. Un control mal formado devuelve E201 en el ejemplo 17. | Ejemplos oficiales 6, 17–19; IDs 42, 172, 186–187. |
| `TRANSFER` | El ejemplo oficial de 40000 creó operación OP-0002; una transferencia sin fondos observada da `422 E507 saldo insuficiente`; el vector 100000/control 12 es distinto entre V1 y V2, sección 5. | Ejemplos oficiales 7, 9–10, 16; IDs 64–70, 77–80. |
| `ANULA` | Anulación exitosa observada: `200 {"ok":true,"anulada":"OP-0003"}`; repetirla: `200 {"ok":false,"motivo":"ya anulada"}`. Operación inexistente: `404 E402 operación inexistente`. | Ejemplos oficiales 13–14; IDs 46, 49, 182–196. |

El estado entre requests es observable: cuentas, saldos, operaciones e identificadores influyen en respuestas posteriores. Los rechazos observados no consumieron identificador en las secuencias citadas. El contrato de reset del reto requiere que `POST /__reset` restaure el estado inicial antes de cada caso. La réplica implementada usa memoria de proceso: un reinicio la limpia; varias instancias sin estado compartido podrían divergir.

## 5. Diferencias de V1 a V2 tras el incidente FR-0153

El ticket anunció tres comportamientos cambiados. La evidencia disponible demuestra dos causas funcionales y dos dimensiones observables en una de ellas; **no se aisló una tercera regla independiente**.

| Comportamiento | V1 | V2 | Estado de evidencia |
|---|---|---|---|
| Representación de `CONSULTA.saldo` | Número JSON entero; por ejemplo `40000`. | String decimal de dos posiciones; por ejemplo `"400.00"`. Los valores comparados reflejan escala observada ÷100. | Confirmado en ejemplos 5, 8, 11, 19 frente a IDs 728, 731, 734, 742; saldo negativo contrastado en IDs 643–654. El redondeo y todos los valores no están caracterizados. |
| Transferencia `TRANSFER;AC-0001;AC-0002;100000;12` en secuencia preparada | `200` y operación creada (ejemplo oficial 10; también V1 IDs 262–267). | `422 {"error":"E506","mensaje":"límite excedido"}` (V2 IDs 453, 694, 733). | Confirmado para ese vector y estados probados. No determina umbral universal ni regla por operación/acumulado. |
| Efectos posteriores del rechazo | Al haberse creado OP-0003, `ANULA` la revierte; el depósito posterior recibe OP-0004. | OP-0003 no existe; anularla da E402 (ID 736) y el siguiente depósito recibe OP-0003 (ID 741). | Cascadas causadas por la transferencia rechazada, no un tercer cambio independiente demostrado. |

El replay de los veinte ejemplos oficiales frente a V2 (IDs 723–743) tuvo ocho respuestas puntuales distintas (728, 731, 733, 734, 736, 737, 741, 742), agrupadas por los cambios anteriores y la propagación del estado. El ticket podría contar el tipo/formato y la escala del saldo por separado junto con la transferencia, pero no hay evidencia que confirme esa clasificación. No se presenta esa posibilidad como hecho.

## 6. Errores conocidos

| Código | Status | Mensaje / ejemplo | Alcance |
|---|---:|---|---|
| E001 | 401 | `no autorizado` | Rutas protegidas probadas. |
| E100 | 400 | `json inválido` | JSON vacío o sintácticamente inválido probado. |
| E102 | 400 | `falta m` | Campo `m` ausente/nulo/no textual o JSON superior no objeto en vectores citados. |
| E103 | 400 | `falta control` | Mensajes concretos sin control. |
| E104 | 400 | `segmento vacío` | Segmentos vacíos concretos. |
| E201 | 400 | `control mal formado` | Control no numérico en ejemplos citados. |
| E202 | 400 | `control inválido` | Control numérico rechazado en ejemplos citados. |
| E301 | 400 | `comando desconocido ` | Conserva espacio final en la respuesta observada. |
| E302 | 400 | `aridad inválida` | Vector de aridad incorrecta con control numérico. |
| E401 | 404 | `cuenta inexistente` | Consulta a cuenta ausente. |
| E402 | 404 | `operación inexistente` | Anulación de operación ausente. |
| E506 | 422 | `límite excedido` | Vector de transferencia específico; V2 lo incorporó en IDs citados. |
| E507 | 422 | `saldo insuficiente` | Vector de transferencia sin fondos observado. |
| E404 | 404 | `ruta desconocida` | Rutas/métodos no reconocidos ensayados. |

No es una enumeración completa: códigos y precedencia no citados siguen pendientes.

## 7. Límites, incertidumbres y controles de calidad

- La primera corrida oculta produjo 22/100 según la pantalla de resultados consultada a las 18:21 BOG del 10-oct-2026. Esto mide un conjunto oculto; sus entradas no se conocen y el puntaje no permite asignar cada fallo a una regla.
- La implementación utiliza vectores positivos finitos para parte de los controles. Que eso explique una porción del puntaje es plausible, no demostrado caso por caso. No se debe presentar como solución general.
- No conocemos la fórmula común de controles, todos los rangos/límites, todas las prioridades de errores ni todas las combinaciones HTTP.
- Los IDs 3–4 son fallos de transporte sin respuesta confirmada; el ID 30 tiene texto dañado por codificación. El validador los marca como advertencias y no deben usarse para inferir comportamiento funcional.
- Suites locales y replays comprueban solo observaciones capturadas. Un resultado local perfecto en ese subconjunto no prueba paridad con todos los casos ocultos.
- El runtime de la réplica no puede llamar al original ni a otro reemplazo. El original solo se consulta desde el banco de experimentación autorizado.

## 8. Referencia de datos

Log canónico append-only: `output/experimentos.jsonl`, 832 filas (≈416 kB al corte). Cada fila conserva ID, secuencia, `X-Req` cuando estuvo disponible, hipótesis, request, status, response y conclusión. No se completan retrospectivamente campos ausentes. Para la clasificación de diferencias V1/V2, ver `wiki/consultas/reconciliacion-incidente-v2-2026-10-10.md`.
