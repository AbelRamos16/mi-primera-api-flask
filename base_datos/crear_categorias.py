import sqlite3


conexion = sqlite3.connect("base_datos/productos.db")

conexion.execute("""
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL UNIQUE
    )
""")

conexion.commit()

print("Tabla categorias creada correctamente.")

conexion.close()