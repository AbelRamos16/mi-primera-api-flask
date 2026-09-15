import sqlite3


conexion = sqlite3.connect("base_datos/productos.db")

cursor = conexion.execute("""
                          SELECT id, nombre, precio
                          FROM productos""")

productos = cursor.fetchall()

for id_producto, nombre, precio in productos:
    print(
        f"Id: {id_producto} | "
        f"Nombre: {nombre} | "
        f"Precio: ${precio:.2f}"
    )
    
conexion.close()