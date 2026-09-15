import sqlite3


conexion = sqlite3.connect("base_datos/productos.db")

conexion.execute(
    """
    INSERT INTO productos (id, nombre, precio)
    VALUES (?, ?, ?)
    """,
    (2, "Teclado", 35.0)
)

conexion.commit()

print("Producto guardado correctamente.")

conexion.close()