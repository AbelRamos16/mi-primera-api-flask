import requests

cambio = {
    "precio": 250.0
}

try:
    respuesta = requests.patch(
        "http://127.0.0.1:5000/productos/3",
        json=cambio,
        timeout=10
    )
    
    respuesta.raise_for_status()

    print(respuesta.json())
    print(respuesta.status_code)

except requests.RequestException as error:
    print(f"No se pudo actualizar el producto: {error}")