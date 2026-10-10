# Réplica local del Reto 2

Contrato interno de implementación:

- `domain.py` expone `Model`. `Model.reset()` restablece cuentas, operaciones y contadores. `Model.process(message: str) -> tuple[int, dict]` procesa un mensaje de `/msg`, devuelve status HTTP y cuerpo JSON; no hace red ni lee tokens.
- `http_server.py` expone `serve(host, port)` y `main()`. Usa una sola instancia de `Model`, lee únicamente `FRONTIER_TEAM_TOKEN` del entorno, sirve `GET /health`, `POST /__reset`, `POST /msg` y responde en otras rutas/métodos según la evidencia. Nunca lee `FRONTIER_ORIGINAL_TOKEN` ni `FRONTIER_BASE_URL`.
- `test_replica.py` prueba offline el modelo y el adaptador HTTP, incluida la secuencia oficial de 20 ejemplos desde reset. No contacta al original.
- `audit_observed.py` vuelve a ejecutar offline las observaciones del log que tienen reset observado, autenticación válida y un mensaje de dominio comparable. No hace HTTP ni llama al original; excluye explícitamente las filas que no puede reproducir con seguridad.
- `audit_http_observed.py` reproduce por loopback observaciones HTTP elegibles con un token ficticio. Excluye headers no conservados, mensajes sin reset observado y respuestas no confirmadas; tampoco llama al original.

La evidencia disponible está en `output/experimentos.jsonl`; la especificación base conserva la línea V1 y [`docs/incidente-v2.md`](../../docs/incidente-v2.md) documenta los overrides del incidente. Los 20 ejemplos de `raw/referencias/frontier-reto-2/pruebas/ejemplos.jsonl` fueron repetidos contra V2 en IDs 723–743. Lo no observado se implementa como supuesto explícito, nunca se presenta como regla confirmada.

La réplica se ejecuta localmente para pruebas diferenciales. El despliegue público y la validación del entrypoint son etapas posteriores.

## Preparación para un despliegue de una instancia

`Dockerfile` empaqueta únicamente `domain.py` y `http_server.py`; el proceso escucha en `HOST=0.0.0.0` y en el `PORT` que entregue la plataforma (8000 por defecto). Configurar `FRONTIER_TEAM_TOKEN` como secreto del servicio en la plataforma: nunca incluir su valor en la imagen, el repositorio ni comandos compartidos. Mantener **una sola instancia** porque cuentas, operaciones y contadores viven en memoria del proceso. Las conexiones HTTP pueden atenderse en paralelo, pero reset y mensajes usan un bloqueo del modelo para no intercalar mutaciones. Un reinicio borra ese estado; cada test oficial empieza con `POST /__reset`.

Desde la raíz, cuando Docker esté disponible, la imagen se construye con `docker build -t blackbox-replica services/replica`. Este corte no dispone de Docker local, así que la construcción de la imagen queda pendiente de verificar; las pruebas HTTP locales sí ejercitan el mismo punto de entrada Python. El banco experimental `sites/caja-negra-lab/` queda fuera del contexto y de la imagen.

## Verificación local

Desde la raíz del proyecto:

    python -m unittest discover -s services/replica -p 'test_*.py' -v
    python services/replica/audit_observed.py  # por defecto, IDs >= 723 (incidente V2)
    python services/replica/audit_http_observed.py  # por defecto, IDs >= 723

En el corte actual, la auditoría V2 del modelo compara 28 observaciones elegibles y obtiene 28 coincidencias; la auditoría HTTP compara 110 y obtiene 110 coincidencias (IDs >= 723). Esto no equivale a paridad completa ni cubre los tests ocultos. La suite de la réplica tiene 25 pruebas aprobadas. Ninguna de estas verificaciones llama al servicio original.
