import sqlite3


RUTA_BASE_DATOS = "base_datos/productos.db"


def obtener_conexion():
    conexion = sqlite3.connect(RUTA_BASE_DATOS)
    conexion.row_factory = sqlite3.Row

    conexion.execute("PRAGMA foreign_keys = ON")

    return conexion