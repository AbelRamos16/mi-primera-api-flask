import sqlite3


categorias = [
    (1, "Tecnología"),
    (2, "Accesorios"),
    (3, "Oficina")
]

conexion = sqlite3.connect("base_datos/productos.db")

conexion.executemany(
    """
    INSERT INTO categorias (id, nombre)
    VALUES (?, ?)
    """,
    categorias
)

conexion.commit()

print("Categorías guardadas correctamente.")

conexion.close()