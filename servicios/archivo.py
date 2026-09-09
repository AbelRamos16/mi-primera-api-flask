import json

RUTA_PRODUCTOS = "data/productos.json"


def cargar_productos():
    try:
        with open(RUTA_PRODUCTOS, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    except FileNotFoundError:
        return []


def guardar_productos(productos):
    with open(RUTA_PRODUCTOS, "w", encoding="utf-8") as archivo:
        json.dump(
            productos,
            archivo,
            ensure_ascii=False,
            indent=4
        )