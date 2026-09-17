import requests

nuevo_producto = {
    "id": 6,
    "nombre": "Auriculares",
    "precio": 20.0,
    "categoria_id": 1
}

try:
    respuesta = requests.post(
        "http://127.0.0.1:5000/productos",
        json=nuevo_producto,
        timeout=10
    )
    
    print(respuesta.json())
    print(respuesta.status_code)
    
    respuesta.raise_for_status()

except requests.RequestException as error:
    print(f"No se pudo conectar con la API: {error}")