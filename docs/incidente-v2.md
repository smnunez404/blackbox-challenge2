# Addendum de incidente — versión 2

## Resultado

La comparación confirma **dos causas funcionales independientes**:

1. `CONSULTA.saldo` cambió de entero JSON en V1 a texto decimal en V2 y, en los valores observados, se representa en escala `/100` (por ejemplo, `40000` → `"400.00"`). Tipo y escala son dos diferencias observables del mismo campo; no sabemos si el organizador las cuenta como dos comportamientos.
2. `TRANSFER;AC-0001;AC-0002;100000;12`, aceptado en V1, ahora responde HTTP 422 `E506` (`límite excedido`). La frontera general no se conoce. Los vectores de 40000 y 50000 ensayados siguen aceptándose.

Por tanto, hay **tres dimensiones observables** si se cuentan por separado el tipo de `saldo`, su escala y el rechazo de la transferencia. No se ha demostrado una tercera regla independiente distinta de esas dimensiones.

## Cascadas que no son cambios adicionales

El rechazo de la transferencia no crea la operación que V1 llamaba `OP-0003`. Por eso la anulación posterior obtiene `E402` y el depósito siguiente usa ese ID. Son consecuencias del rechazo y del contador de operaciones, no una tercera causa raíz.

## Evidencia y controles negativos

- Replay oficial V2: IDs 723–743; diferencias agrupadas en saldo, rechazo del vector de 100000 y sus cascadas.
- Replays históricos dirigidos: IDs 643–816; no apareció una tercera diferencia funcional independiente.
- Segunda anulación de `OP-0003`: V2 devuelve `{"ok":false,"motivo":"ya anulada"}` como V1 (IDs 823–824).
- Consulta con espacio inicial en el ID de cuenta: V2 devuelve `E401`, igual que V1 (ID 828 frente a V1 ID 287).
- `m:null`, `m:42` y `m:["PING;64"]`: V2 devuelve E102, igual que V1 IDs 84–86 (IDs 830–832).
- `ALTA;Lucid;73` fue aceptado en V2 como `AC-0002` tras crear `AC-0001` (IDs 749–750). Es un vector válido que ahora incluye la réplica. La misma entrada no figura en la línea base V1, por lo que no se afirma que sea el tercer cambio del incidente.

El replay no usó las corridas ocultas. Los IDs y requests completos están en [`../output/experimentos.jsonl`](../output/experimentos.jsonl); la fuente V1 del organizador permanece inmutable en `raw/referencias/frontier-reto-2/pruebas/ejemplos.jsonl`.

## Límite de la réplica

La implementación modela el rechazo observado para montos `>=100000`; no afirma que ese sea el umbral real. Antes de describir una frontera exacta se necesita un vector de transferencia con control válido en la zona intermedia. Los controles generales de TRANSFER siguen sin inferirse.
