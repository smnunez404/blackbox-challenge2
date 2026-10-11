# Guion para exponer la landing page — La caja negra

**Duración objetivo:** 1:50–2:00. **Público:** jurado y personas que no conocen el proyecto. Ensaya con cronómetro y deja pausas breves.

Las indicaciones entre corchetes son para orientarte mientras recorres la página; no se leen en voz alta.

## 1. Inicio · portada

[Presenta el título y el propósito del sitio.]

Esta página explica cómo reconstruimos un servicio sin manual ni código, usando sus respuestas como evidencia.

## 2. El reto · historia

[Desplázate a “La caja negra no se adivina”.]

El servicio llevaba diez años en producción. No teníamos su código ni documentación; debíamos descubrir sus reglas a partir de lo que respondía.

## 3. Qué hacía · servicio original

[Muestra los comandos y un ejemplo de solicitud y respuesta.]

Era una API para gestionar cuentas: crear, consultar saldos, depositar, transferir y anular operaciones. Cada orden devolvía un código HTTP y un JSON. Como las operaciones cambiaban el estado, también importaban las respuestas posteriores.

## 4. Cómo se organiza · arquitectura

[Recorre las dos franjas del diagrama.]

El diagrama separa la investigación del servicio entregado. El banco comparaba el original con una réplica local; el reemplazo final mantiene su propio estado y no llama al proveedor.

## 5. Cómo se investigó · método

[Muestra el proceso y las herramientas.]

Probamos con reinicios, variaciones pequeñas y pausas; guardamos cada intento en un log de 868 filas. Codex, con modelos Luna y Sol, apoyó el análisis; Obsidian conservó el contexto. Definimos seis roles y sus arneses, aunque no fue posible ejecutar diez agentes en paralelo. El generador solo prepara variantes; no envía llamadas.

## 6. Qué cambió · hallazgos

[Compara los dos comportamientos confirmados y señala la pregunta abierta.]

En V2 confirmamos dos diferencias: en los casos probados, 40000 pasó a «400.00»; y una transferencia concreta de 100000 pasó de aceptada a 422 E506. El error al anularla es una consecuencia en cadena. La tercera diferencia anunciada no quedó aislada.

## 7. Qué demuestra · evidencia y resultado

[Muestra cómo consultar un caso y termina en “Resultado y límites”.]

El registro permite revisar solicitudes, respuestas y el alcance de cada conclusión. La primera evaluación oculta fue 22 de 100. Salud, reinicio y un ejemplo público pasaron, pero no prueban equivalencia completa. Presentamos tanto lo comprobado como lo que sigue abierto.
