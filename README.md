# Aliado Envíos

Servicio independiente de cotización de envíos (Flask + Gunicorn) que consume
el marketplace "Nómada" (repo `TopicosProject`) como servicio del equipo aliado.

## Endpoint

`GET /api/v2/envios/tarifas` — lista todas las tarifas.
`GET /api/v2/envios/tarifas?ciudad=Medellín` — cotiza una ciudad (sin importar
tildes ni mayúsculas). Devuelve `404` con `{"error": ...}` si no hay cobertura.

```json
{
  "servicio": "Servicio Aliado de Envíos (v2)",
  "moneda": "COP",
  "tarifas": [{"ciudad": "Medellín", "costo": 8000, "dias": 1}]
}
```

## Ejecutar

```shell
docker compose up -d --build   # expone el puerto 80
curl "http://localhost/api/v2/envios/tarifas?ciudad=Cali"
```

## Pruebas

```shell
pip install -r requirements.txt
python -m unittest
```

## Despliegue en AWS Academy (EC2)

1. Instancia EC2 con Docker y Docker Compose instalados.
2. Grupo de seguridad: permitir HTTP (puerto 80) desde cualquier origen.
3. Clonar este repositorio y ejecutar `docker compose up -d --build`.
4. Compartir la IP elástica: el marketplace la usa en `ALLY_SERVICE_URL`.
