import sqlite3


conexion = sqlite3.connect("base_datos/productos.db")

conexion.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL
    )
""")

conexion.commit()

print("Tabla productos creada correctamente.")

conexion.close()