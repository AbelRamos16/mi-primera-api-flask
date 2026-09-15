import requests

try:
    respuesta = requests.delete(
        "http://127.0.0.1:5000/productos/3",
        timeout=10
    )
    
    respuesta.raise_for_status()

    print(respuesta.json())
    print(respuesta.status_code)

except requests.RequestException as error:
    print(f"No se pudo eliminar el producto: {error}")