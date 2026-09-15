import sqlite3


id_producto = 2
nuevo_precio = 40.0

conexion = sqlite3.connect("base_datos/productos.db")

cursor = conexion.execute(
    """
    UPDATE productos
    SET precio = ?
    WHERE id = ?
    """,
    (nuevo_precio, id_producto)
)

conexion.commit()

if cursor.rowcount > 0:
    print("Precio actualizado correctamente.")
else:
    print("Producto no encontrado.")

conexion.close()