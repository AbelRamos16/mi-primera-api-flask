import requests

producto_cambio = {
    "id": 5,
    "nombre": "Cámara web HD",
    "precio": 45.0
}

try:
    respuesta = requests.put(
        "http://127.0.0.1:5000/productos/5",
        json=producto_cambio,
        timeout=10
    )
    
    respuesta.raise_for_status()

    print(respuesta.json())
    print(respuesta.status_code)

except requests.RequestException as error:
    print(f"No se pudo reemplazar el producto: {error}")