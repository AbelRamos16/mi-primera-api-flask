import sqlite3


id_buscado = 2

conexion = sqlite3.connect("base_datos/productos.db")

cursor = conexion.execute(
    """
    SELECT id, nombre, precio
    FROM productos
    WHERE id = ?
    """,
    (id_buscado,)
)

producto = cursor.fetchone()

if producto is not None:
    id_producto, nombre, precio = producto

    print(
        f"Id: {id_producto} | "
        f"Nombre: {nombre} | "
        f"Precio: ${precio:.2f}"
    )
else:
    print("Producto no encontrado.")

conexion.close()