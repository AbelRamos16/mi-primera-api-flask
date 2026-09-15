import sqlite3


id_producto = 1

conexion = sqlite3.connect("base_datos/productos.db")

cursor = conexion.execute(
    """
    DELETE FROM productos
    WHERE id = ?
    """,
    (id_producto,)
)

conexion.commit()

if cursor.rowcount > 0:
    print("Producto eliminado correctamente.")
else:
    print("Producto no encontrado.")

conexion.close()