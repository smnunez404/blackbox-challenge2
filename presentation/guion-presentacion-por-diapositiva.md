# Guion para presentar — La caja negra

**Duración objetivo:** cerca de 2 minutos; ensayar con cronómetro.  
**Público:** jurado, reclutadores y personas que no conocen el proyecto.  
Este es el texto hablado, no el contenido que se proyecta. Las notas están ocultas durante la presentación a pantalla completa.

## 1. El reto

Este reto nos presentó un servicio de diez años, sin código ni manual. Cuando apareció una versión nueva sin aviso, debíamos descubrir sus reglas y crear un reemplazo independiente.

## 2. Qué hacía el servicio

El servicio permitía crear cuentas, consultar saldos, depositar, transferir y anular operaciones. Aquí enviamos 40 mil entre dos cuentas; la respuesta asigna OP-0002.

## 3. Qué se debía copiar

Replicar no era adivinar el código interno, sino igualar lo visible: estado HTTP, respuesta JSON y efectos sobre la siguiente solicitud. Comparamos secuencias desde el mismo estado.

## 4. Método y herramientas

Probamos cambios pequeños y registramos cada intento. Codex, con los modelos Luna y Sol, apoyó el análisis; Obsidian conservó fuentes y decisiones. Definimos seis roles, pero no pudimos ejecutar diez agentes en paralelo. El generador solo preparaba variantes.

## 5. Arquitectura

Separamos el banco de investigación del servicio entregado. El primero comparaba el original con la réplica local; el reemplazo mantiene su propio estado y no llama al proveedor.

## 6. Cambios en la nueva versión

En V2 confirmamos dos diferencias. En los casos probados, 40000 pasó a «400.00». Una transferencia concreta de 100000 pasó de aceptada a 422 E506. El límite general sigue desconocido.

## 7. Efectos y dudas

El rechazo impidió crear OP-0003; por eso falló su anulación y cambió el siguiente identificador. Es una cascada, no una tercera regla confirmada. La tercera diferencia anunciada quedó sin aislar.

## 8. Resultado

La primera evaluación oculta fue 22 de 100. Salud, reinicio y un ejemplo público pasaron, pero no prueban equivalencia completa. Entregamos una réplica y evidencia; permanecen límites por resolver.
