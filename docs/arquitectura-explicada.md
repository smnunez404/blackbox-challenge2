# Cómo leer y defender el diagrama

El [diagrama](arquitectura-reto-2.png) muestra **nuestra réplica propuesta**. No intenta adivinar cómo estaba programado el servicio original. Elegimos una vista de componentes porque la entrega pide explicar qué recibe el sistema, cómo produce cada respuesta y dónde vive el estado entre requests. Un diagrama de clases describiría objetos internos, pero aportaría menos para justificar el contrato HTTP y el límite de despliegue.

## El recorrido principal

1. **Evaluador → HTTP + auth.** Llega una petición con método, ruta, cuerpo y token del equipo. La réplica decide si la ruta existe y si la credencial corresponde. El token personal solo sirve para investigar el original.
2. **Parser.** Para `POST /msg`, interpreta el JSON y separa el texto como `ALTA;Lucia;82`. Conserva la grafía necesaria para reproducir errores de formato y espacios.
3. **Validación.** Aplica las comprobaciones observadas de aridad, control y precedencia de errores. Una entrada rechazada puede producir la respuesta directamente.
4. **Comandos ↔ Estado.** PING, ALTA, CONSULTA, DEPOSITO, TRANSFER y ANULA consultan o cambian cuentas, saldos, operaciones y contadores. Una consulta lee; un depósito o transferencia modifica.
5. **Respuesta → Evaluador.** La salida son el status HTTP y el cuerpo exacto. El evaluador compara ambos en cada paso; por eso importan textos literales como `recieved` o el espacio final de un error.

La flecha horizontal es el camino conceptual de `POST /msg`, no una obligación de que **toda** ruta recorra todos los bloques. La línea verde desde `HTTP + auth` hasta `Respuesta` marca las salidas tempranas de `GET /health`, errores de autenticación y rutas desconocidas. `POST /__reset` vuelve el estado y los contadores al inicio y también responde al cliente. El código HTTP y las pruebas fijan el comportamiento concreto de cada rama.

**Diseño lógico frente a código actual.** Los bloques del dibujo son responsabilidades, no seis microservicios ni seis archivos. En el prototipo, `http_server.py` contiene el adaptador HTTP y `domain.py` reúne parser, validación, comandos y estado en la clase `Model`; las ramas por comando todavía comparten un método. El PDF de Systems Design describe la separación *propuesta* para facilitar cambios, no una refactorización ya terminada. Si preguntan por este trade-off: se priorizó obtener una réplica medible con tiempo limitado, y los tests por secuencia permiten extraer handlers después sin cambiar el contrato. No afirmar que esa separación física ya existe.

## Por qué hay dos zonas

El recuadro morado es **una instancia del reemplazo**. Mantiene estado en memoria porque el contrato del reto indica que el evaluador habla con un proceso y hace reset antes de cada test. La ventaja es simplicidad y transiciones reproducibles; el límite es que un reinicio pierde ese estado y varias instancias independientes divergirían.

La franja inferior es el **banco de investigación**, fuera del proceso entregado. Allí scripts propios envían secuencias al original, registran cada request y comparan sus respuestas con la réplica local. La réplica desplegada no importa ese cliente ni lee el token personal. La evidencia describe el contrato externo observado; no revela la implementación interna del servicio perdido.

## Qué podemos afirmar con evidencia

- El log propio conserva 832 requests. La auditoría de V2 compara por separado 28 respuestas de dominio y 110 respuestas HTTP elegibles (IDs >= 723); ambas pasan. Eso no cubre entradas desconocidas ni el set oculto.
- La especificación provisional cita IDs del log para cada comportamiento y separa `confirmado`, `probable` y `supuesto`. Los controles generales de ALTA, DEPOSITO y TRANSFER siguen sin fórmula descubierta.
- Tras el incidente anunciado a las 15:30 Colombia, los canarios deben determinar si alguna respuesta cambió. Una diferencia solo delimita el intervalo entre la última medición igual y la primera distinta.

## Respuesta breve para el debrief

“Recibimos un request y un estado anterior; devolvemos exactamente un status y un cuerpo, y quizá un estado nuevo. El diseño distingue entrada HTTP, interpretación, validación y comandos para localizar qué regla causa una diferencia. Hoy algunas responsabilidades comparten código: el diagrama es lógico, no una lista de módulos. El banco de investigación queda fuera del servicio desplegado; sus observaciones alimentan una especificación con evidencia, pero el reemplazo responde por sí mismo. La mayor incertidumbre actual es el cálculo general del campo de control; por eso los casos no demostrados están marcados como supuestos.”
