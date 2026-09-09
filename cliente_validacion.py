import requests

producto_incompleto = {
    "id": 4,
    "nombre": "Parlante Bluetooth"
}

try:
    respuesta = requests.put(
        "http://127.0.0.1:5000/productos/4",
        json=producto_incompleto,
        timeout=10
    )

    print(respuesta.json())
    print(respuesta.status_code)

except requests.RequestException as error:
    print(f"No se pudo conectar con la API: {error}")