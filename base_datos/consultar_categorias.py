import sqlite3

conexion = sqlite3.connect("base_datos/productos.db")
conexion.row_factory = sqlite3.Row

cursor = conexion.execute("""
    SELECT id, nombre, precio, categoria_id
    FROM productos
""")

productos = cursor.fetchall()

for producto in productos:
    print(
        f"Id: {producto['id']} | "
        f"Nombre: {producto['nombre']} | "
        f"Precio: ${producto['precio']:.2f} | "
        f"Categoría id: {producto['categoria_id']}"
    )

conexion.close()