# Despliegue del entrypoint

El runtime es un proceso Python con estado en memoria. Debe atender **una sola instancia** que no duerma durante la evaluación; cada test comienza con `POST /__reset`. El contenedor no necesita conectarse al servicio original.

## Configuración propuesta en Railway

1. Vincular este repositorio y usar `services/replica/` como directorio raíz de build: allí está el `Dockerfile`. Alternativamente, configurar explícitamente su ruta. [Dockerfiles de Railway](https://docs.railway.com/builds/dockerfiles).
2. Mantener una réplica y dejar **Serverless desactivado**. Dormir y despertar el contenedor puede introducir latencia o perder el estado en memoria. [Serverless](https://docs.railway.com/deployments/serverless).
3. Configurar `FRONTIER_TEAM_TOKEN` como variable secreta del servicio. No incluir su valor en Git, la imagen ni un comando compartido. No configurar `FRONTIER_ORIGINAL_TOKEN` ni `FRONTIER_BASE_URL` en producción. [Variables](https://docs.railway.com/variables).
4. Generar un dominio HTTPS público. El servidor toma `PORT` del entorno y escucha en `0.0.0.0`. [Red pública](https://docs.railway.com/networking/public-networking).
5. No activar un healthcheck de plataforma en `/health` si no puede adjuntar `Authorization: Bearer <token>`: el contrato de compatibilidad devuelve 401 sin token. Comprobar readiness manualmente con la credencial del equipo. [Healthchecks](https://docs.railway.com/deployments/healthchecks).

### Selección del builder en Railway

El servicio existente llegó a estar fijado explícitamente a `RAILPACK`, aunque el `Dockerfile` está en su directorio raíz. Para esta entrega, `services/replica/railway.json` selecciona `DOCKERFILE` y declara la ruta de forma explícita; el archivo está junto al código dentro de `services/replica/`, que es el root directory configurado en Railway. Este es un ajuste operativo temporal para el servicio heredado, no una dependencia del runtime.

Railway marca Config as Code como deprecado y anuncia que los archivos existentes seguirán funcionando hasta el 2026-12-01. Después del reto, migrar el builder a un ajuste nativo del servicio o a Infrastructure as Code y retirar este archivo tras comprobar el despliegue. [Referencia oficial de Config as Code](https://docs.railway.com/config-as-code/reference).

Antes de publicar una versión: actualizar especificación y log con la evidencia vigente, ejecutar `python -m unittest discover -s services/replica -p 'test_*.py'`, ambas auditorías, `python tools/release_preflight.py` y `python tools/smoke_runtime.py`; revisar el índice Git y escanear secretos. Tras desplegar, probar en el dominio propio `GET /health`, `POST /__reset` y `POST /msg` con `PING;64`, comprobando status/cuerpo. Esas llamadas no usan el servicio original ni el set oculto.

No ejecutar evaluaciones ocultas desde la plataforma sin autorización separada: son un recurso limitado del reto. Si la cuenta de hosting requiere compra o cambio de plan, detenerse y solicitar aprobación.

La autenticación del CLI local, si se usa, se hace mediante el flujo oficial de vinculación por código; nunca se copia un token personal al repositorio. El directorio local `.railway/` está ignorado por Git. Una autorización del CLI no crea por sí sola un servicio ni comprueba el plan de la cuenta. Para evitar el token de equipo en argumentos de proceso e historial, configurarlo desde una variable local mediante `railway variable set FRONTIER_TEAM_TOKEN --stdin`, sin mostrar su valor. La guía oficial admite ese modo de [lectura por stdin](https://docs.railway.com/cli/variable). No usar `railway variable list --kv` ni salida JSON que revele secretos.

Si se opta por despliegue local vía CLI (sin enlazar GitHub al servicio), ejecutar desde la raíz revisada `railway up ./services/replica --path-as-root` tras crear/vincular un único servicio y fijar la variable. Esa forma coloca el `Dockerfile` en la raíz del archivo enviado; cada nueva versión requiere repetir manualmente el despliegue. [CLI y subdirectorios](https://docs.railway.com/cli/deploying).
