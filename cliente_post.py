import requests

nuevo_producto = {
    "id": 5,
    "nombre": "Cámara web",
    "precio": 40.0
}

try:
    respuesta = requests.post(
        "http://127.0.0.1:5000/productos",
        json=nuevo_producto,
        timeout=10
    )
    
    respuesta.raise_for_status()

    print(respuesta.json())
    print(respuesta.status_code)

except requests.RequestException as error:
    print(f"No se pudo conectar con la API: {error}")