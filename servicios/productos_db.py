import sqlite3

from base_datos.conexion import obtener_conexion


def obtener_todos_los_productos():
    conexion = obtener_conexion()

    cursor = conexion.execute("""
        SELECT id, nombre, precio
        FROM productos
    """)

    filas = cursor.fetchall()

    conexion.close()

    productos = []

    for fila in filas:
        productos.append({
            "id": fila["id"],
            "nombre": fila["nombre"],
            "precio": fila["precio"]
        })

    return productos


def obtener_producto_por_id(producto_id):
    conexion = obtener_conexion()

    cursor = conexion.execute(
        """
        SELECT id, nombre, precio
        FROM productos
        WHERE id = ?
        """,
        (producto_id,)
    )

    fila = cursor.fetchone()

    conexion.close()

    if fila is None:
        return None

    return {
        "id": fila["id"],
        "nombre": fila["nombre"],
        "precio": fila["precio"]
    }


def crear_producto(producto):
    conexion = obtener_conexion()

    try:
        conexion.execute(
            """
            INSERT INTO productos (id, nombre, precio)
            VALUES (?, ?, ?)
            """,
            (
                producto["id"],
                producto["nombre"],
                producto["precio"]
            )
        )

        conexion.commit()

        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conexion.close()


def actualizar_producto(producto_id, cambios):
    conexion = obtener_conexion()

    campos = []
    valores = []

    for campo, valor in cambios.items():
        campos.append(f"{campo} = ?")
        valores.append(valor)

    valores.append(producto_id)

    cursor = conexion.execute(
        f"""
        UPDATE productos
        SET {", ".join(campos)}
        WHERE id = ?
        """,
        valores
    )

    conexion.commit()

    actualizado = cursor.rowcount > 0

    conexion.close()

    return actualizado


def eliminar_producto(producto_id):
    conexion = obtener_conexion()

    cursor = conexion.execute(
        """
        DELETE FROM productos
        WHERE id = ?
        """,
        (producto_id,)
    )

    conexion.commit()

    eliminado = cursor.rowcount > 0

    conexion.close()

    return eliminado