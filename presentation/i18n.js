(() => {
  const english = {
    "Saltar al contenido": "Skip to content",
    "Saltar a las diapositivas": "Skip to slides",
    "Reconstruir un servicio por sus respuestas.": "Rebuild a service from its responses.",
    "Resultado de primera evaluación oculta: 22 sobre 100": "First hidden evaluation result: 22 out of 100",
    "Diagrama: el banco local pregunta al servicio original y registra sus respuestas; después compara con una réplica local. Por separado, el evaluador usa el servicio desplegado, que tiene sus propios datos y nunca llama al original.": "Diagram: the local test bench asks the original service and records its responses, then compares them with a local replica. Separately, the evaluator uses the deployed service, which has its own data and never calls the original.",
    "Abrir el diagrama de arquitectura en tamaño completo": "Open the architecture diagram at full size",
    "CASO DOCUMENTADO · Las conclusiones se basan en pruebas registradas.": "DOCUMENTED CASE · Conclusions are based on recorded tests.",
    "El reto": "The challenge",
    "Qué hacía": "What it did",
    "Método y herramientas": "Method and tools",
    "Cambios": "Changes",
    "Evidencia": "Evidence",
    "Diapositivas": "Slides",
    "RETO 02": "CHALLENGE 02",
    "DESCUBRIR UN SISTEMA SIN MANUAL": "DISCOVERING A SYSTEM WITHOUT A MANUAL",
    "Reconstruir un servicio": "Rebuilding a service",
    "por sus": "from its",
    "respuestas.": "responses.",
    "Un servicio antiguo quedó sin manual y su proveedor anunció cambios. Este caso muestra cómo se investigó con cuidado, cómo se construyó una réplica independiente y qué se pudo comprobar.": "An old service was left without a manual, and its provider announced changes. This case shows how it was investigated carefully, how an independent replica was built, and what could be proven.",
    "Explorar hallazgos": "Explore findings",
    "Abrir presentación": "Open presentation",
    "Guion para recorrer ↘": "Tour script ↘",
    "PRIMERA EVALUACIÓN OCULTA": "FIRST HIDDEN EVALUATION",
    "· resultado registrado": "· recorded result",
    "Salud, reinicio y ejemplo 02: aprobados": "Health, reset, and example 02: passed",
    "Evaluación oculta: 22/100": "Hidden evaluation: 22/100",
    "La réplica respondió a las comprobaciones básicas, pero todavía difiere en muchos casos. Las pruebas reservadas no muestran qué solicitudes fallaron.": "The replica passed the basic checks, but still differs in many cases. The hidden tests do not show which requests failed.",
    "filas en el log experimental": "rows in the experiment log",
    "comportamientos distintos confirmados": "distinct confirmed behaviors",
    "evaluaciones reservadas usadas al corte": "hidden evaluations used at the cutoff",
    "tercer cambio independiente: no identificado": "third independent change: not identified",
    "DEMO DAY · VIDEO": "DEMO DAY · VIDEO",
    "La reconstrucción,": "The reconstruction,",
    "explicada en video.": "explained in a video.",
    "Una presentación breve del problema, la investigación, la arquitectura de la réplica y las decisiones tomadas para responder al cambio de versión.": "A short presentation of the problem, the investigation, the replica architecture, and the decisions made to respond to the version change.",
    "Ver video demo en YouTube ": "Watch the demo video on YouTube ",
    "El video resume el caso para una revisión rápida y acompaña la evidencia técnica disponible en esta página.": "The video summarizes the case for a quick review and complements the technical evidence on this page.",
    "ABRIR EN YOUTUBE ↗": "OPEN ON YOUTUBE ↗",
    "01 / EL PROBLEMA": "01 / THE PROBLEM",
    "La caja negra no se adivina.": "A black box is not guessed.",
    "Se descubre con preguntas.": "It is discovered through questions.",
    "El proveedor anunció cambios en un servicio de diez años, sin explicar cuáles. La réplica debe dar el mismo ": "The provider announced changes to a ten-year-old service without explaining which ones. The replica must return the same ",
    "El proveedor anunció cambios en un servicio de diez años, sin explicar cuáles. La réplica debe dar el mismo": "The provider announced changes to a ten-year-old service without explaining which ones. The replica must return the same",
    "código de respuesta": "response code",
    "el mismo contenido y los mismos efectos en las operaciones siguientes.": "the same content, and the same effects on subsequent operations.",
    "Preparar": "Prepare",
    "Volver al estado inicial y definir una pregunta concreta.": "Return to the initial state and define one concrete question.",
    "Observar": "Observe",
    "Guardar la solicitud, el código de respuesta y el contenido recibido.": "Save the request, response code, and received content.",
    "Comparar": "Compare",
    "Repetir la misma secuencia y anotar cada diferencia comprobada.": "Repeat the same sequence and record each confirmed difference.",
    "¿Qué hace un generador de pruebas?": "What does a test generator do?",
    "Crea variantes de una solicitud para explorar casos posibles. En este proyecto el programa solo preparaba esas variantes: no las enviaba. Cada prueba real se hizo de forma controlada y quedó registrada.": "It creates request variants to explore possible cases. In this project the program only prepared those variants; it did not send them. Every real test was controlled and recorded.",
    "02 / EL SERVICIO ORIGINAL": "02 / THE ORIGINAL SERVICE",
    "Una caja de cuentas": "An account and",
    "y movimientos.": "transaction service.",
    "No era una plataforma de pagos conectada a bancos. En los ejemplos disponibles, era un servicio pequeño que mantenía cuentas, saldos y operaciones, y respondía a órdenes de texto.": "It was not a payment platform connected to banks. In the available examples, it was a small service that maintained accounts, balances, and transactions, and responded to text commands.",
    "Crear cuenta": "Create account",
    "registra una persona y devuelve un identificador como": "registers a person and returns an identifier such as",
    "Consultar saldo": "Check balance",
    "devuelve el identificador de la cuenta y el saldo actual.": "returns the account identifier and current balance.",
    "Depositar": "Deposit",
    "suma un importe y devuelve el identificador de la operación.": "adds an amount and returns the operation identifier.",
    "Transferir": "Transfer",
    "mueve un importe de una cuenta a otra, si la operación es aceptada.": "moves an amount from one account to another if accepted.",
    "Anular operación": "Cancel operation",
    "intenta revertir una operación registrada anteriormente.": "attempts to reverse a previously recorded operation.",
    "Comprobar servicio": "Check service",
    "responde que el servicio está activo.": "confirms that the service is active.",
    "EJEMPLO DE LOS DATOS QUE DEVOLVÍA": "EXAMPLE OF THE DATA IT RETURNED",
    "Una respuesta era más que un “sí” o un “no”.": "A response was more than a “yes” or “no”.",
    "El servicio informaba si la orden se aceptó, qué cuenta u operación se creó y cuál era el saldo. Los códigos de error también formaban parte de su respuesta.": "The service reported whether the command was accepted, which account or operation was created, and the balance. Error codes were part of its response too.",
    "crea AC-0001": "creates AC-0001",
    "crea OP-0001": "creates OP-0001",
    "devuelve cuenta y saldo": "returns account and balance",
    "En otras palabras: no era una página que mostrara botones o gráficos. Recibía una orden y devolvía datos sobre la cuenta, el saldo, la operación o el error.": "In other words, it was not a page with buttons or charts. It received a command and returned data about the account, balance, operation, or error.",
    "Ejemplo de flujo de cuentas": "Account flow example",
    "Ejemplos de datos que devolvía el servicio": "Examples of data returned by the service",
    "CREAR CUENTA · 201": "CREATE ACCOUNT · 201",
    "CONSULTAR · 200": "CHECK · 200",
    "DEPOSITAR · 200": "DEPOSIT · 200",
    "Cada orden llegaba en el campo ": "Each command arrived in the ",
    "Cada orden llegaba en el campo": "Each command arrived in the",
    "de": " field of ",
    "escrita como palabras separadas por punto y coma. Por ejemplo: ": "written as words separated by semicolons. For example: ",
    "escrita como palabras separadas por punto y coma. Por ejemplo:": "written as words separated by semicolons. For example:",
    "El último número es parte del mensaje y su validación cambia según la orden.": "The last number is part of the message, and its validation changes by command.",
    "03 / CÓMO SE ORGANIZA": "03 / HOW IT IS ORGANIZED",
    "Dos caminos.": "Two paths.",
    "Un límite que no se cruza.": "One boundary that is never crossed.",
    "Durante la investigación, un programa de pruebas consulta al servicio original y guarda lo que observa. La réplica funciona por separado y no llama al sistema del proveedor.": "During the investigation, a test program queries the original service and saves what it observes. The replica runs separately and never calls the provider's system.",
    "INVESTIGACIÓN · LOCAL": "RESEARCH · LOCAL",
    "Banco de pruebas": "Test bench",
    "preguntas controladas": "controlled questions",
    "solicitudes": "requests",
    "Servicio original": "Original service",
    "referencia observable": "observable reference",
    "código + datos": "code + data",
    "Registro de pruebas": "Test record",
    "868 entradas · historial": "868 entries · history",
    "comparación repetida": "repeated comparison",
    "Réplica de prueba": "Test replica",
    "comprobación sin conexión": "offline check",
    "EL SERVICIO ORIGINAL NO SE USA EN LA RÉPLICA": "THE ORIGINAL SERVICE IS NOT USED BY THE REPLICA",
    "SERVICIO ENTREGADO": "DELIVERED SERVICE",
    "Evaluador": "Evaluator",
    "acceso protegido": "protected access",
    "solicitud": "request",
    "SERVICIO PROPIO": "OWN SERVICE",
    "Entrada": "Input",
    "acceso · rutas · reinicio": "access · routes · reset",
    "Lectura y reglas": "Parsing and rules",
    "comando · revisión": "command · validation",
    "Estado en memoria": "In-memory state",
    "cuentas · operaciones": "accounts · operations",
    "Respuesta": "Response",
    "Respuesta:": "Response:",
    "Solicitud:": "Request:",
    "el mensaje que llega; se separa en una orden y sus datos.": "the incoming message; it is split into a command and its data.",
    "tiene un código y un contenido. Si cambia cualquiera, el resultado no es igual.": "has a code and content. If either changes, the result is not the same.",
    "código + contenido": "code + content",
    "respuesta": "response",
    "Comprobación": "Check",
    "código y contenido recibidos": "received code and content",
    "Diagrama de arquitectura para descargar o ampliar.": "Architecture diagram to download or enlarge.",
    "Las cajas de lectura, validación y comandos representan responsabilidades para entender el flujo; no afirman que existan como archivos separados ni revelan cómo está construido el servicio original.": "The parsing, validation, and command boxes represent responsibilities used to understand the flow; they do not claim that separate files exist or reveal how the original service is built.",
    "Descargar imagen ↘": "Download image ↘",
    "Memoria": "Memory",
    "Memoria:": "Memory:",
    "guarda saldos y operaciones;": "stores balances and operations;",
    "vuelve al inicio.": "returns to the beginning.",
    "Si cambia cualquiera, el resultado no es igual.": "If any of them changes, the result is not the same.",
    "04 / ESTRATEGIA DE PRUEBAS": "04 / TEST STRATEGY",
    "Preguntar poco.": "Ask little.",
    "Aprender con cada respuesta.": "Learn from every response.",
    "La meta no era enviar muchas solicitudes, sino diseñar pruebas pequeñas que permitieran distinguir una regla de otra.": "The goal was not to send many requests, but to design small tests that could distinguish one rule from another.",
    "Volver al inicio": "Start from the beginning",
    "Reiniciar los datos para que cada secuencia empiece en las mismas condiciones.": "Reset the data so every sequence starts under the same conditions.",
    "Cambiar una cosa": "Change one thing",
    "Probar una variación concreta para saber qué dato provoca una diferencia.": "Test one concrete variation to learn which input causes a difference.",
    "Ir con cuidado": "Proceed carefully",
    "Espaciar las solicitudes y detenerse si el servicio indica que está ocupado.": "Space out requests and stop if the service indicates it is busy.",
    "Guardar todo": "Save everything",
    "Conservar cada intento, incluso si falla la conexión o falta una respuesta.": "Keep every attempt, including connection failures and missing responses.",
    "Comprobar de nuevo": "Check again",
    "Repetir las secuencias importantes cuando aparece una versión nueva.": "Repeat important sequences when a new version appears.",
    "Por qué funciona:": "Why it works:",
    "así se puede explicar qué se preguntó, qué respondió el servicio y qué conclusión permite la evidencia, sin confundir un problema de conexión con una regla del sistema.": "This makes it possible to explain what was asked, what the service returned, and what the evidence supports without confusing a connection problem with a system rule.",
    "HERRAMIENTAS, CONTEXTO Y ROLES": "TOOLS, CONTEXT, AND ROLES",
    "Un método que deja huella y se puede retomar.": "A method that leaves a trace and can be resumed.",
    "La solución no salió de una herramienta que adivinara el servicio. Se combinaron análisis asistido, contexto documentado y programas propios de prueba.": "The solution did not come from a tool that guessed the service. It combined assisted analysis, documented context, and custom test programs.",
    "Pasos de la estrategia de pruebas": "Test strategy steps",
    "01 · ASISTENCIA": "01 · ASSISTANCE",
    "02 · MEMORIA": "02 · MEMORY",
    "03 · PROGRAMAS PROPIOS": "03 · CUSTOM PROGRAMS",
    "04 · TÉCNICAS": "04 · TECHNIQUES",
    "Codex ayudó a coordinar análisis y entregables; el trabajo iteró con modelos Luna y Sol, según el registro del autor.": "Codex helped coordinate analysis and deliverables; the work iterated with Luna and Sol models, according to the author's record.",
    "Fuentes originales, conocimiento enlazado y un historial que solo agrega entradas. Así se recupera el contexto sin depender del chat anterior.": "Original sources, linked knowledge, and a history that only appends entries. This makes context recoverable without depending on the previous chat.",
    "Un banco serial espacia las consultas y registra cada intento. Un generador prepara entradas inusuales, pero no las envía automáticamente; la comparación y el seguimiento de casos ancla ayudan a notar cambios.": "A serial test bench spaces requests and records every attempt. A generator prepares unusual inputs but does not send them automatically; comparison and anchor-case tracking help reveal changes.",
    "Se reinicia el estado, se cambia un dato por vez y se comparan las mismas secuencias entre versiones y con la réplica local.": "The state is reset, one input changes at a time, and the same sequences are compared across versions and with the local replica.",
    "Codex + Luna y Sol": "Codex + Luna and Sol",
    "Obsidian entre sesiones": "Obsidian across sessions",
    "Banco, registro y comparación": "Test bench, record, and comparison",
    "Secuencias y diferencias": "Sequences and differences",
    "SEIS ROLES DEFINIDOS": "SIX DEFINED ROLES",
    "Protocolo · estado · pruebas · cambios · réplica · evidencia": "Protocol · state · tests · changes · replica · evidence",
    "Un ": "A ",
    "arnés de trabajo": "work harness",
    " es la ficha que da a cada rol una meta, límites, evidencia que debe entregar y una revisión antes de avanzar.": " is a brief that gives each role a goal, limits, required evidence, and a review before moving forward.",
    "Los roles se diseñaron como contratos de trabajo; no todos se convirtieron en agentes autónomos.": "The roles were designed as work contracts; not all of them became autonomous agents.",
    "Transparencia:": "Transparency:",
    "se intentó lanzar diez agentes en paralelo, pero el límite interno de orquestación no permitió ejecutar esa tanda. Hubo revisiones independientes puntuales; no se afirma que diez agentes hayan trabajado simultáneamente.": "ten agents were planned for parallel execution, but the internal orchestration limit prevented that run. There were targeted independent reviews; we do not claim that ten agents worked simultaneously.",
    "Referencias consultadas, no herramientas integradas:": "References consulted, not integrated tools:",
    "confirmado en los ejemplos citados": "confirmed in cited examples",
    "pendiente / no generalizar": "open / do not generalize",
    "V1 · ejemplo oficial": "V1 · official example",
    "V2 · experimento": "V2 · experiment",
    "CONSULTAR · SALDO DE CUENTA": "CHECK · ACCOUNT BALANCE",
    "TRANSFERENCIA · IMPORTE 100000 / ÚLTIMO DATO 12": "TRANSFER · AMOUNT 100000 / LAST VALUE 12",
    "UN EFECTO POSTERIOR NO PRUEBA UNA REGLA NUEVA": "A LATER EFFECT DOES NOT PROVE A NEW RULE",
    "05 / CAMBIO DEL SERVICIO": "05 / SERVICE CHANGE",
    "La nueva versión cambió.": "The new version changed.",
    "Esto es lo que pudimos comprobar.": "This is what we could confirm.",
    "CONFIRMADO": "CONFIRMED",
    "NO AISLADO": "NOT ISOLATED",
    "De entero a texto decimal.": "From integer to decimal text.",
    "Una operación que antes pasaba, ahora se rechaza.": "An operation that used to pass is now rejected.",
    "El ticket anuncia tres cambios. La tercera regla sigue abierta.": "The ticket announces three changes. The third rule remains open.",
    "Está confirmado para esta operación y los estados probados, incluidos los registros 845 y 863. El límite general y su posible relación con el importe o las operaciones anteriores siguen desconocidos.": "This is confirmed for this operation and the tested states, including records 845 and 863. The general limit and its possible relationship to the amount or previous operations remain unknown.",
    "El saldo cambió tanto de tipo/formato como de escala; no sabemos si el ticket cuenta eso como uno o dos cambios. El E402 al anular una operación ausente y el desplazamiento de OP-0004 a OP-0003 derivan del rechazo de la transferencia: son consecuencias, no una tercera regla probada.": "The balance changed in both type/format and scale; we do not know whether the ticket counts that as one or two changes. E402 when cancelling a missing operation and the shift from OP-0004 to OP-0003 result from the rejected transfer: they are consequences, not a third proven rule.",
    "Inspeccionar las respuestas →": "Inspect responses →",
    "POR QUÉ UNA DIFERENCIA CAMBIA LO QUE SIGUE": "WHY ONE DIFFERENCE CHANGES WHAT FOLLOWS",
    "rechazada": "rejected",
    "no existe": "does not exist",
    "recibe OP-0003": "receives OP-0003",
    "06 / EVIDENCIA": "06 / EVIDENCE",
    "Lo importante es lo que respondió.": "What matters is what it returned.",
    "Cada caso muestra la solicitud, el código de respuesta, el contenido recibido y hasta dónde llega la conclusión. Los números de registro se pueden buscar en el historial completo.": "Each case shows the request, response code, received content, and how far the conclusion goes. Record numbers can be searched in the complete history.",
    "Muestra curada para explicar el hallazgo, no el universo completo de pruebas. Los experimentos 3–4 no tienen respuesta confirmada y el ID 30 tiene texto dañado por codificación; no se usan aquí como evidencia concluyente.": "A curated sample for explaining the finding, not the complete test universe. Experiments 3–4 have no confirmed response and ID 30 has encoding-damaged text; they are not used here as conclusive evidence.",
    "Especificación · 7 secciones ↓": "Specification · 7 sections ↓",
    "Log íntegro · 868 filas ↓": "Full log · 868 rows ↓",
    "Buscar": "Search",
    "Comando": "Command",
    "Todos": "All",
    "Cargando ejemplos…": "Loading examples…",
    "CASO SELECCIONADO": "SELECTED CASE",
    "Evidencia del corpus público": "Evidence from the public corpus",
    "Solicitud · POST /msg": "Request · POST /msg",
    "Respuesta · datos recibidos": "Response · received data",
    "Código HTTP": "HTTP code",
    "Elige un ejemplo": "Choose an example",
    "07 / RESULTADO Y LÍMITES": "07 / RESULT AND LIMITS",
    "Un ejemplo correcto": "One correct example",
    "no demuestra": "does not prove",
    "que todo coincida.": "that everything matches.",
    "La primera evaluación reservada obtuvo 22 de 100. El servicio pasó la comprobación de salud, el reinicio y el ejemplo público 02. Sin conocer los casos reservados, no se puede afirmar qué regla causó cada fallo.": "The first hidden evaluation scored 22 out of 100. The service passed the health check, reset, and public example 02. Without seeing the hidden cases, we cannot say which rule caused each failure.",
    "Algunas reglas de la réplica cubren solo ejemplos conocidos. Eso podría explicar parte de la diferencia, pero no está confirmado caso por caso. El historial distingue las observaciones de las preguntas que siguen abiertas.": "Some replica rules cover only known examples. That could explain part of the difference, but it has not been confirmed case by case. The history distinguishes observations from questions that remain open.",
    "Cómo se valida el último número de ALTA, DEPOSITO y TRANSFER.": "How the last number in ALTA, DEPOSITO, and TRANSFER is validated.",
    "Qué límites y qué prioridad tienen los errores en casos no probados.": "Which limits and error priorities apply to untested cases.",
    "La tercera regla independiente anunciada, todavía no identificada.": "The announced third independent rule, still not identified.",
    "Que todos los casos produzcan la misma respuesta, aún no demostrado.": "Whether every case produces the same response, not yet demonstrated.",
    "PREGUNTAS AÚN ABIERTAS": "OPEN QUESTIONS",
    "08 / PRESENTACIÓN": "08 / PRESENTATION",
    "Un recorrido completo": "A complete tour",
    "para ver y explicar.": "to watch and explain.",
    "Guion para recorrer esta página ↓": "Script for this page ↓",
    "Abrir diapositivas ": "Open slides ",
    "Guion de diapositivas ↓": "Slide script ↓",
    "Las conclusiones separan lo comprobado de lo que aún no se sabe.": "The conclusions separate what was proven from what is still unknown.",
    "Puedes exponer esta misma página siguiendo el guion de recorrido. Si prefieres las diapositivas, tienen un guion aparte; las notas de apoyo no aparecen al proyectarlas.": "You can present this page by following the tour script. If you prefer slides, they have a separate script; speaker notes are hidden while presenting.",
    "Repositorio del proyecto ↗": "Project repository ↗",
    "Sin consultas en vivo · sin credenciales en la página": "No live queries · no credentials on this page",
    "Volver al caso": "Back to the case",
    "RETO DE RECONSTRUCCIÓN · 8 DIAPOSITIVAS": "RECONSTRUCTION CHALLENGE · 8 SLIDES",
    "RETO 02 · SISTEMA SIN MANUAL": "CHALLENGE 02 · SYSTEM WITHOUT A MANUAL",
    "Qué servicio heredamos, cómo lo reconstruimos y qué pudimos comprobar.": "What service we inherited, how we rebuilt it, and what we could confirm.",
    "PARA JURADO · VIDEO DE HASTA 2 MIN": "FOR THE JURY · VIDEO UP TO 2 MIN",
    "Descargar guion ↓": "Download script ↓",
    "Presentar a pantalla completa ↗": "Present full screen ↗",
    "Presentación del proyecto": "Project presentation",
    "Progreso de la presentación": "Presentation progress",
    "Qué servicio heredamos, cómo lo reconstruimos y qué pudimos comprobar.": "What service we inherited, how we rebuilt it, and what we could confirm.",
    "Anterior": "Previous",
    "Siguiente": "Next",
    "Mostrar guion del expositor": "Show speaker script",
    "Ocultar guion del expositor": "Hide speaker script",
    "Pantalla completa": "Full screen",
    "Salir de pantalla completa": "Exit full screen",
    "Imprimir / PDF": "Print / PDF",
    "Usa ← y → para cambiar de diapositiva; F activa pantalla completa; Esc vuelve a la página. El guion de apoyo no se muestra al proyectar; también puedes descargarlo para ensayar.": "Use ← and → to change slides; F enables full screen; Esc returns to the page. The support script is hidden while presenting; you can also download it to rehearse.",
    "El reto": "The challenge",
    "Qué hacía el servicio": "What the service did",
    "Qué se debía copiar": "What had to be copied",
    "Método y herramientas": "Method and tools",
    "Arquitectura": "Architecture",
    "Cambios en la nueva versión": "Changes in the new version",
    "Efectos y preguntas abiertas": "Effects and open questions",
    "Resultado": "Result",
    "GUION DEL EXPOSITOR": "SPEAKER SCRIPT"
    ,"01 · EL RETO": "01 · THE CHALLENGE"
    ,"02 · EL SERVICIO ORIGINAL": "02 · THE ORIGINAL SERVICE"
    ,"03 · QUÉ SIGNIFICA “RESPONDER IGUAL”": "03 · WHAT “RESPONDING THE SAME” MEANS"
    ,"04 · MÉTODO Y HERRAMIENTAS": "04 · METHOD AND TOOLS"
    ,"05 · ARQUITECTURA": "05 · ARCHITECTURE"
    ,"06 · CAMBIOS EN LA NUEVA VERSIÓN": "06 · CHANGES IN THE NEW VERSION"
    ,"07 · EFECTOS EN CADENA Y DUDAS": "07 · CASCADING EFFECTS AND OPEN QUESTIONS"
    ,"08 · RESULTADO": "08 · RESULT"
    ,"Un servicio antiguo, sin manual ni código disponible": "An old service, with no manual or available source code"
    ,"El proveedor cambió un sistema que llevaba diez años funcionando y no explicó qué modificó. El desafío fue descubrirlo y construir un reemplazo independiente.": "The provider changed a system that had run for ten years and did not explain what changed. The challenge was to discover it and build an independent replacement."
    ,"Una caja de cuentas y movimientos": "An account and transaction service"
    ,"Órdenes por POST /msg; respuestas con datos o errores": "Commands through POST /msg; responses with data or errors"
    ,"Crear": "Create"
    ,"cuentas": "accounts"
    ,"Consultar": "Check"
    ,"saldos": "balances"
    ,"dinero": "money"
    ,"entre cuentas": "between accounts"
    ,"operaciones": "operations"
    ,"Anular": "Cancel"
    ,"Validar": "Validate"
    ,"datos y controles": "data and controls"
    ,"Una transferencia aceptada queda registrada con un número de operación.": "An accepted transfer is recorded with an operation number."
    ,". Una transferencia aceptada queda registrada con un número de operación.": ". An accepted transfer is recorded with an operation number."
    ,"Se copia lo que se ve, no cómo está hecho": "Copy what can be observed, not how it is built"
    ,"El código": "The code"
    ,"Por ejemplo, 200, 400 o 422.": "For example, 200, 400, or 422."
    ,"La respuesta": "The response"
    ,"Los datos, sus tipos y sus mensajes.": "The data, its types, and its messages."
    ,"Lo que queda guardado": "What remains stored"
    ,"Una operación puede cambiar el saldo y la siguiente respuesta.": "An operation can change the balance and the next response."
    ,"Cada secuencia comienza de nuevo para que la comparación sea justa.": "Each sequence starts over so the comparison is fair."
    ,"Investigar con método.": "Investigate methodically."
    ,"Pruebas": "Tests"
    ,"Reiniciar, cambiar un dato y comparar secuencias.": "Reset, change one input, and compare sequences."
    ,"Herramientas": "Tools"
    ,"Codex, modelos Luna y Sol, y programas propios.": "Codex, Luna and Sol models, and custom programs."
    ,"Fuentes originales, conocimiento enlazado y un historial que solo agrega entradas.": "Original sources, linked knowledge, and a history that only appends entries."
    ,"Seis roles definidos.": "Six roles defined."
    ,"Un arnés fija meta, límites, evidencia y revisión.": "A harness sets the goal, limits, evidence, and review."
    ,"No se ejecutó la tanda de 10 agentes: el límite interno lo impidió. Hubo revisiones puntuales.": "The run of 10 agents was not executed because of the internal limit. There were targeted reviews."
    ,"Dos caminos, separados": "Two separate paths"
    ,"INVESTIGACIÓN · ANTES DE LA ENTREGA": "RESEARCH · BEFORE DELIVERY"
    ,"consulta al servicio original y guarda la evidencia. Luego compara la misma secuencia con una réplica de prueba.": "queries the original service and saves the evidence. It then compares the same sequence with a test replica."
    ,"EL ORIGINAL NO SE USA EN LA RÉPLICA": "THE ORIGINAL IS NOT USED BY THE REPLICA"
    ,"Evaluador → entrada → reglas → memoria propia → respuesta.": "Evaluator → input → rules → own state → response."
    ,"La réplica recibe órdenes y mantiene sus propias cuentas y operaciones.": "The replica receives commands and maintains its own accounts and operations."
    ,"El servicio entregado nunca llama al sistema del proveedor.": "The delivered service never calls the provider's system."
    ,"Dos diferencias comprobadas": "Two confirmed differences"
    ,"SALDO MOSTRADO": "DISPLAYED BALANCE"
    ,"ANTES": "BEFORE"
    ,"AHORA": "NOW"
    ,"El número se volvió texto decimal; en los casos comparados, se divide por 100.": "The number became decimal text; in the compared cases, it is divided by 100."
    ,"TRANSFERENCIA · IMPORTE 100000": "TRANSFER · AMOUNT 100000"
    ,"ACEPTADA": "ACCEPTED"
    ,"La nueva versión devuelve el error E506: “límite excedido”.": "The new version returns error E506: “limit exceeded”."
    ,"Un cambio afecta lo que viene después": "One change affects what comes next"
    ,"Al rechazarse una transferencia, OP-0003 no se crea. Al intentar anularla, el servicio responde que no existe; la siguiente operación recibe ese número.": "When a transfer is rejected, OP-0003 is not created. When we try to cancel it, the service says it does not exist; the next operation receives that number."
    ,"Una consecuencia no demuestra una regla nueva.": "A consequence does not prove a new rule."
    ,"El aviso menciona tres cambios. La evidencia confirma dos comportamientos distintos; una tercera regla independiente no quedó identificada.": "The notice mentions three changes. The evidence confirms two distinct behaviors; a third independent rule was not identified."
    ,"Se entregó una réplica; no se demostró equivalencia completa": "A replica was delivered; complete equivalence was not proven"
    ,"Primera evaluación reservada: ": "First hidden evaluation: "
    ,"Qué se entregó": "What was delivered"
    ,"Un servicio independiente y evidencia documentada.": "An independent service and documented evidence."
    ,"Qué queda abierto": "What remains open"
    ,"La tercera regla y muchas combinaciones no observadas.": "The third rule and many unobserved combinations."
    ,"Los resultados conocidos no demuestran que todos los casos sean iguales.": "Known results do not prove that every case is identical."
    ,"Replicar no era adivinar el código interno, sino igualar lo visible: estado HTTP, respuesta JSON y efectos sobre la siguiente solicitud. Comparamos secuencias desde el mismo estado.": "Replicating did not mean guessing internal code; it meant matching what was visible: HTTP status, JSON response, and effects on the next request. We compared sequences from the same state."
    ,"El servicio permitía crear cuentas, consultar saldos, depositar, transferir y anular operaciones. Aquí enviamos 40 mil entre dos cuentas; la respuesta asigna OP-0002.": "The service could create accounts, check balances, deposit, transfer, and cancel operations. Here we sent 40,000 between two accounts; the response assigned OP-0002."
    ,"Probamos cambios pequeños y registramos cada intento. Codex, con los modelos Luna y Sol, apoyó el análisis; Obsidian conservó fuentes y decisiones. Definimos seis roles, pero no pudimos ejecutar diez agentes en paralelo. El generador solo preparaba variantes.": "We tested small changes and recorded every attempt. Codex, with Luna and Sol models, supported the analysis; Obsidian preserved sources and decisions. We defined six roles, but could not run ten agents in parallel. The generator only prepared variants."
    ,"Separamos el banco de investigación del servicio entregado. El primero comparaba el original con la réplica local; el reemplazo mantiene su propio estado y no llama al proveedor.": "We separated the research bench from the delivered service. The first compared the original with the local replica; the replacement keeps its own state and does not call the provider."
    ,"En V2 confirmamos dos diferencias. En los casos probados, 40000 pasó a «400.00». Una transferencia concreta de 100000 pasó de aceptada a 422 E506. El límite general sigue desconocido.": "In V2 we confirmed two differences. In the tested cases, 40000 became “400.00”. One specific transfer of 100000 changed from accepted to 422 E506. The general limit remains unknown."
    ,"El rechazo impidió crear OP-0003; por eso falló su anulación y cambió el siguiente identificador. Es una cascada, no una tercera regla confirmada. La tercera diferencia anunciada quedó sin aislar.": "The rejection prevented OP-0003 from being created; that is why its cancellation failed and the next identifier changed. It is a cascade, not a confirmed third rule. The announced third difference was not isolated."
    ,"La primera evaluación oculta fue 22 de 100. Salud, reinicio y un ejemplo público pasaron, pero no prueban equivalencia completa. Entregamos una réplica y evidencia; permanecen límites por resolver.": "The first hidden evaluation was 22 out of 100. Health, reset, and one public example passed, but they do not prove complete equivalence. We delivered a replica and evidence; limitations remain to be resolved."
  };

  const attrTranslations = {
    "La caja negra, inicio": "The black box, home",
    "Navegación principal": "Main navigation",
    "Buscar": "Search",
    "Volver al caso": "Back to the case",
    "Guion del expositor": "Speaker script",
    "Presentación del proyecto": "Project presentation",
    "Progreso de la presentación": "Presentation progress",
    "Diapositiva anterior": "Previous slide",
    "Diapositiva siguiente": "Next slide",
    "Reconstruir un servicio por sus respuestas.": "Rebuild a service from its responses.",
    "Resultado de primera evaluación oculta: 22 sobre 100": "First hidden evaluation result: 22 out of 100",
    "Abrir el diagrama de arquitectura en tamaño completo": "Open the architecture diagram at full size",
    "Ejemplo de flujo de cuentas": "Account flow example",
    "Pasos de la estrategia de pruebas": "Test strategy steps",
    "Casos de evidencia": "Evidence cases"
  };

  const originalNodes = [];
  const originalAttributes = [];
  const skipTags = new Set(["SCRIPT", "STYLE", "CODE", "PRE"]);

  function textKey(value) {
    return value.replace(/\s+/g, " ").trim();
  }

  function translateTextNode(node, lang) {
    if (!node.parentElement || skipTags.has(node.parentElement.tagName)) return;
    if (!Object.prototype.hasOwnProperty.call(node, "__originalText")) {
      Object.defineProperty(node, "__originalText", { value: node.nodeValue, writable: true });
      originalNodes.push(node);
    }
    const original = node.__originalText;
    const key = textKey(original);
    const replacement = lang === "en" && english[key] ? english[key] : key;
    const leading = original.match(/^\s*/)?.[0] || "";
    const trailing = original.match(/\s*$/)?.[0] || "";
    node.nodeValue = `${leading}${replacement}${trailing}`;
  }

  function translateAttributes(lang) {
    document.querySelectorAll("[aria-label], [placeholder], [title], [alt]").forEach(element => {
      ["aria-label", "placeholder", "title", "alt"].forEach(attribute => {
        if (!element.hasAttribute(attribute)) return;
        const key = `${element.tagName}:${attribute}`;
        if (!element.__originalAttributes) element.__originalAttributes = {};
        if (!(attribute in element.__originalAttributes)) {
          element.__originalAttributes[attribute] = element.getAttribute(attribute);
          originalAttributes.push(element);
        }
        const original = element.__originalAttributes[attribute];
        element.setAttribute(attribute, lang === "en" ? (attrTranslations[original] || original) : original);
      });
    });
    document.title = lang === "en" ? "The Black Box — reverse engineering case" : (document.body.classList.contains("deck-body") ? "Presentación — La caja negra" : "La caja negra — caso de ingeniería inversa");
  }

  function applyLanguage(lang) {
    const chosen = lang === "es" ? "es" : "en";
    document.documentElement.lang = chosen;
    originalNodes.forEach(node => translateTextNode(node, chosen));
    translateAttributes(chosen);
    document.querySelectorAll("[data-language-choice]").forEach(button => {
      button.setAttribute("aria-pressed", String(button.dataset.languageChoice === chosen));
    });
    document.body.dataset.language = chosen;
    window.dispatchEvent(new CustomEvent("languagechange", { detail: { language: chosen } }));
  }

  function translateAll(lang) {
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(node => {
      if (!originalNodes.includes(node)) originalNodes.push(node);
      translateTextNode(node, lang);
    });
    translateAttributes(lang);
  }

  window.siteI18n = {
    get language() { return document.documentElement.lang === "es" ? "es" : "en"; },
    t(value) { return this.language === "en" ? (english[value] || value) : value; },
    apply: applyLanguage
  };

  document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    const requested = params.get("lang");
    const saved = window.localStorage.getItem("site-language");
    const initial = requested === "es" || requested === "en" ? requested : (saved === "es" ? "es" : "en");
    translateAll(initial);
    document.querySelectorAll("[data-language-choice]").forEach(button => button.addEventListener("click", () => {
      const language = button.dataset.languageChoice;
      window.localStorage.setItem("site-language", language);
      applyLanguage(language);
    }));
  });
})();
