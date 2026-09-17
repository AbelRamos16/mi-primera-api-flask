import requests

producto_cambio = {
    "id": 2,
    "nombre": "Teclado actualizado",
    "precio": 50.0,
    "categoria_id": 99
}

try:
    respuesta = requests.put(
        "http://127.0.0.1:5000/productos/2",
        json=producto_cambio,
        timeout=10
    )
    

    print(respuesta.json())
    print(respuesta.status_code)
    
    respuesta.raise_for_status()

except requests.RequestException as error:
    print(f"No se pudo reemplazar el producto: {error}")