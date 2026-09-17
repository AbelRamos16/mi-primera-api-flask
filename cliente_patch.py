import requests

cambio = {
    "categoria_id": 2
}

try:
    respuesta = requests.patch(
        "http://127.0.0.1:5000/productos/3",
        json=cambio,
        timeout=10
    )
    
    

    print(respuesta.json())
    print(respuesta.status_code)
    
    respuesta.raise_for_status()

except requests.RequestException as error:
    print(f"No se pudo actualizar el producto: {error}")