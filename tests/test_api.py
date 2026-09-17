import os
import sqlite3
import unittest

from app import app
from base_datos import conexion as conexion_db


RUTA_BASE_PRUEBA = "base_datos/test_productos.db"
RUTA_BASE_REAL = "base_datos/productos.db"


class TestApi(unittest.TestCase):

    def setUp(self):
        conexion_db.RUTA_BASE_DATOS = RUTA_BASE_PRUEBA

        if os.path.exists(RUTA_BASE_PRUEBA):
            os.remove(RUTA_BASE_PRUEBA)

        conexion = sqlite3.connect(RUTA_BASE_PRUEBA)

        conexion.execute("""
            CREATE TABLE categorias (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL UNIQUE
            )
        """)

        conexion.execute("""
            CREATE TABLE productos (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL,
                categoria_id INTEGER NOT NULL,
                FOREIGN KEY (categoria_id)
                    REFERENCES categorias(id)
            )
        """)

        conexion.executemany(
            "INSERT INTO categorias (id, nombre) VALUES (?, ?)",
            [
                (1, "Tecnología"),
                (2, "Accesorios"),
                (3, "Oficina")
            ]
        )

        conexion.executemany(
            """
            INSERT INTO productos
                (id, nombre, precio, categoria_id)
            VALUES (?, ?, ?, ?)
            """,
            [
                (1, "Mouse inalámbrico", 25.0, 1),
                (2, "Teclado", 35.0, 1),
                (4, "Parlante Bluetooth", 35.0, 2)
            ]
        )

        conexion.commit()
        conexion.close()

        self.cliente = app.test_client()

    def tearDown(self):
        if os.path.exists(RUTA_BASE_PRUEBA):
            os.remove(RUTA_BASE_PRUEBA)

        conexion_db.RUTA_BASE_DATOS = RUTA_BASE_REAL

    def test_inicio_devuelve_mensaje_correcto(self):
        respuesta = self.cliente.get("/")

        self.assertEqual(respuesta.status_code, 200)

        datos = respuesta.get_json()

        self.assertEqual(
            datos["mensaje"],
            "Mi primera API funciona correctamente"
        )

    def test_estado_coincide_con_productos(self):
        respuesta_productos = self.cliente.get("/productos")
        productos = respuesta_productos.get_json()

        respuesta_estado = self.cliente.get("/estado")
        datos_estado = respuesta_estado.get_json()

        self.assertEqual(respuesta_productos.status_code, 200)
        self.assertEqual(respuesta_estado.status_code, 200)
        self.assertIsInstance(productos, list)

        self.assertEqual(
            datos_estado["productos_registrados"],
            len(productos)
        )

    def test_buscar_producto_inexistente_devuelve_404(self):
        respuesta = self.cliente.get("/productos/999")

        self.assertEqual(respuesta.status_code, 404)

        datos = respuesta.get_json()

        self.assertEqual(
            datos["error"],
            "Producto no encontrado"
        )

    def test_crear_producto_sin_precio_devuelve_400(self):
        nuevo_producto = {
            "id": 6,
            "nombre": "Auriculares",
            "categoria_id": 1
        }

        respuesta = self.cliente.post(
            "/productos",
            json=nuevo_producto
        )

        self.assertEqual(respuesta.status_code, 400)

        datos = respuesta.get_json()

        self.assertEqual(
            datos["error"],
            "Falta el campo: precio"
        )

    def test_crear_producto_con_id_duplicado_devuelve_400(self):
        nuevo_producto = {
            "id": 1,
            "nombre": "Auriculares",
            "precio": 20.0,
            "categoria_id": 1
        }

        respuesta = self.cliente.post(
            "/productos",
            json=nuevo_producto
        )

        self.assertEqual(respuesta.status_code, 400)

        datos = respuesta.get_json()

        self.assertEqual(
            datos["error"],
            "Ya existe un producto con ese id"
        )

    def test_crear_producto_valido_devuelve_201(self):
        respuesta_inicial = self.cliente.get("/productos")
        cantidad_inicial = len(respuesta_inicial.get_json())

        nuevo_producto = {
            "id": 6,
            "nombre": "Auriculares",
            "precio": 20.0,
            "categoria_id": 1
        }

        respuesta = self.cliente.post(
            "/productos",
            json=nuevo_producto
        )

        self.assertEqual(respuesta.status_code, 201)

        datos = respuesta.get_json()

        self.assertEqual(datos["id"], 6)
        self.assertEqual(datos["nombre"], "Auriculares")
        self.assertEqual(datos["precio"], 20.0)
        self.assertEqual(datos["categoria_id"], 1)

        respuesta_final = self.cliente.get("/productos")
        cantidad_final = len(respuesta_final.get_json())

        self.assertEqual(
            cantidad_final,
            cantidad_inicial + 1
        )

    def test_actualizar_producto_valido_devuelve_200(self):
        cambios = {
            "precio": 40.0
        }

        respuesta = self.cliente.patch(
            "/productos/4",
            json=cambios
        )

        self.assertEqual(respuesta.status_code, 200)

        datos = respuesta.get_json()

        self.assertEqual(datos["id"], 4)
        self.assertEqual(datos["nombre"], "Parlante Bluetooth")
        self.assertEqual(datos["precio"], 40.0)

    def test_eliminar_producto_valido_devuelve_200(self):
        respuesta_inicial = self.cliente.get("/productos")
        cantidad_inicial = len(respuesta_inicial.get_json())

        respuesta = self.cliente.delete("/productos/4")

        self.assertEqual(respuesta.status_code, 200)

        datos = respuesta.get_json()

        self.assertEqual(
            datos["mensaje"],
            "Producto eliminado correctamente"
        )

        self.assertEqual(datos["producto"]["id"], 4)

        respuesta_busqueda = self.cliente.get("/productos/4")

        self.assertEqual(respuesta_busqueda.status_code, 404)

        respuesta_final = self.cliente.get("/productos")
        cantidad_final = len(respuesta_final.get_json())

        self.assertEqual(
            cantidad_final,
            cantidad_inicial - 1
        )

    def test_reemplazar_producto_con_id_distinto_devuelve_400(self):
        producto_modificado = {
            "id": 99,
            "nombre": "Parlante cambiado",
            "precio": 40.0,
            "categoria_id": 2
        }

        respuesta = self.cliente.put(
            "/productos/4",
            json=producto_modificado
        )

        self.assertEqual(respuesta.status_code, 400)

        datos = respuesta.get_json()

        self.assertEqual(
            datos["error"],
            "El id del JSON debe coincidir con el id de la URL"
        )
        
    def test_crear_producto_con_categoria_inexistente_devuelve_400(self):
        nuevo_producto = {
            "id": 7,
            "nombre": "Impresora",
            "precio": 150.0,
            "categoria_id": 99
        }

        respuesta = self.cliente.post(
            "/productos",
            json=nuevo_producto
        )

        self.assertEqual(respuesta.status_code, 400)

        datos = respuesta.get_json()

        self.assertEqual(
            datos["error"],
            "La categoría no existe"
        )
        
    def test_reemplazar_producto_con_categoria_inexistente_devuelve_400(self):
        producto_modificado = {
            "id": 2,
            "nombre": "Teclado actualizado",
            "precio": 50.0,
            "categoria_id": 99
        }

        respuesta = self.cliente.put(
            "/productos/2",
            json=producto_modificado
        )

        self.assertEqual(respuesta.status_code, 400)

        datos = respuesta.get_json()

        self.assertEqual(
            datos["error"],
            "La categoría no existe"
        )
        
    def test_actualizar_producto_con_categoria_inexistente_devuelve_400(self):
        cambios = {
            "categoria_id": 99
        }

        respuesta = self.cliente.patch(
            "/productos/2",
            json=cambios
        )

        self.assertEqual(respuesta.status_code, 400)

        datos = respuesta.get_json()

        self.assertEqual(
            datos["error"],
            "La categoría no existe"
        )


if __name__ == "__main__":
    unittest.main()