# Reto 2 — réplica de «La caja negra»

Este repositorio es un candidato de entrega local. Implementa una réplica independiente del servicio, basada en requests y respuestas observados. El servicio de producción **no** consulta la caja negra original: procesa los mensajes y conserva cuentas, saldos y operaciones en memoria.

## Contrato

Con `Authorization: Bearer <token del equipo>`, el proceso atiende `GET /health`, `POST /__reset` y `POST /msg`. También responde en rutas y métodos desconocidos. El estado vive en una sola instancia; cada prueba debe comenzar con `POST /__reset`. El token se configura exclusivamente mediante `FRONTIER_TEAM_TOKEN` en el entorno de despliegue.

El código está en [`services/replica/`](services/replica/README.md). Su [`Dockerfile`](services/replica/Dockerfile) escucha en el `PORT` asignado por el proveedor y usa una sola instancia. La imagen aún no se ha construido en esta máquina porque Docker no está instalado; el punto de entrada Python sí cuenta con pruebas HTTP locales.

## Evidencia y límites

- [`output/experimentos.jsonl`](output/experimentos.jsonl) conserva una línea por request registrado al original. El corte copiado aquí incluye la investigación V1/V2 hasta el ID 832; tres respuestas V1 históricas tienen avisos de captura y no se completaron por inferencia.
- Los [20 ejemplos entregados por el organizador](raw/referencias/frontier-reto-2/pruebas/ejemplos.jsonl) son una secuencia que se ejecuta después de reset; se usan como fixture de regresión.
- El replay V2 de los 20 ejemplos oficiales confirmó las diferencias documentadas en [`docs/incidente-v2.md`](docs/incidente-v2.md). La suite local prueba ese replay; no demuestra paridad general con el servicio ni con el set oculto.
- Los controles de `ALTA`, `DEPOSITO` y `TRANSFER` no tienen fórmula general descubierta. La réplica documenta sus respuestas por defecto en [`assumptions.md`](services/replica/assumptions.md).

El [documento de diseño](docs/systems-design-reto-2.pdf), el [diagrama de arquitectura](docs/arquitectura-reto-2.png) y su [explicación para el debrief](docs/arquitectura-explicada.md) son los artefactos preparados para Systems Design. La [especificación provisional](docs/especificacion-provisional.md) enlaza reglas con IDs del log y marca sus límites. El [addendum del incidente V2](docs/incidente-v2.md) detalla cambios confirmados, el vector adicional de `ALTA` y las incertidumbres restantes.

La [guía de despliegue](docs/despliegue.md) describe una sola instancia, variables de entorno, verificaciones y el cuidado especial de `/health` autenticado.

Los [scripts propios](tools/README.md) generan mutaciones limitadas, comparan secuencias y revisan la estructura del paquete. El runner permite tráfico solo hacia una réplica en loopback; el proceso desplegado no incluye herramientas de consulta al original.

## Verificación local

La CI de [offline-checks](.github/workflows/offline-checks.yml) ejecuta esta misma batería en cada push y pull request con permisos de solo lectura y sin secretos. Es un gate de regresión local; no consulta el original, no ejecuta el set oculto y no sustituye la revisión de evidencia postincidente.

Con Python 3.13 desde la raíz:

```sh
python -m unittest discover -s services/replica -p 'test_*.py' -v
python services/replica/audit_observed.py
python services/replica/audit_http_observed.py
python tools/release_preflight.py
python tools/smoke_runtime.py
```

El preflight comprueba la estructura de la especificación y del log, referencias de evidencia y separación del runtime; no mide paridad con el original. Para ejecutar la réplica, configura `FRONTIER_TEAM_TOKEN` en el entorno y ejecuta `python services/replica/http_server.py`. `HOST` y `PORT` son configurables; sus valores por defecto son `127.0.0.1` y `8000`. No se debe poner el token en comandos compartidos, archivos del repositorio o imágenes.

El candidato aún requiere gate final de publicación/despliegue y revisión del contrato; no ejecutar el set oculto desde pruebas locales.
