import sqlite3


conexion = sqlite3.connect("base_datos/productos.db")

conexion.execute("PRAGMA foreign_keys = ON")

conexion.execute("""
    CREATE TABLE productos_nueva (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL,
        categoria_id INTEGER NOT NULL,
        FOREIGN KEY (categoria_id) REFERENCES categorias(id)
    )
""")

conexion.execute("""
    INSERT INTO productos_nueva (id, nombre, precio, categoria_id)
    SELECT id, nombre, precio, 1
    FROM productos
""")

conexion.execute("DROP TABLE productos")

conexion.execute("""
    ALTER TABLE productos_nueva
    RENAME TO productos
""")

conexion.commit()

print("Tabla productos migrada correctamente.")

conexion.close()