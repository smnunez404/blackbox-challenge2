# Herramientas propias de investigación

- `fuzz_cases.py` genera nueve mutaciones acotadas de una semilla de ALTA; imprimirlas no consulta el servicio. Los casos propuestos son candidatos, no resultados.
- `differential_runner.py` compara capturas offline o envía una secuencia únicamente a una réplica en loopback (`localhost`, `127.0.0.1` o `::1`). Informa la primera divergencia de status o cuerpo.
- `release_preflight.py` revisa la estructura del log y la especificación, citas, IDs repetidos, patrones de credenciales y dependencias prohibidas del runtime. No mide paridad funcional.
- `smoke_runtime.py` arranca el entrypoint Python real en un puerto local efímero con un token ficticio y comprueba health, autenticación, reset, ruta desconocida y los 20 ejemplos oficiales en secuencia; nunca contacta al original.

`fixtures/ping-after-reset.json` es un caso mínimo derivado de observaciones registradas de reset y PING. Su reset explícito permite compararlo con una réplica local desde estado conocido. Ninguno de estos scripts necesita el token del servicio original para funcionar; el runner puede leer el token **del equipo** de una variable de entorno si se le indica `--token-env FRONTIER_TEAM_TOKEN`.

Ejemplo de generación sin red:

```sh
python tools/fuzz_cases.py --limit 3
python tools/smoke_runtime.py
```

Ejemplo de comparación de dos capturas locales:

```sh
python tools/differential_runner.py --mode offline --sequence tools/fixtures/ping-after-reset.json --fixture tools/fixtures/ping-after-reset.json
```

Para el modo `replica`, inicia primero el servicio local y usa una fixture que **incluya reset**. El runner rechaza hosts externos y no abre solicitudes al original.
