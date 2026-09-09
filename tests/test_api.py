import unittest

from app import app

import copy

from rutas.productos import productos
from servicios.archivo import guardar_productos

class TestApi(unittest.TestCase):
    def setUp(self):
        self.cliente = app.test_client()
        self.productos_originales = copy.deepcopy(productos)


    def tearDown(self): 
        productos[:] = self.productos_originales
        guardar_productos(productos)

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
            "id": 1,
            "nombre": "Auriculares"
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
            "precio": 20.0
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
        cantidad_inicial = len(productos)
        
        nuevo_producto = {
            "id": 6,
            "nombre": "Auriculares",
            "precio": 20.0
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

        self.assertEqual(len(productos), cantidad_inicial + 1)
        
    def test_actualizar_producto_valido_devuelve_200(self):
        
        producto_modificado = {
            "precio": 40.0
        }
        
        respuesta = self.cliente.patch(
            "/productos/4",
            json=producto_modificado
        )

        self.assertEqual(respuesta.status_code, 200)

        datos = respuesta.get_json()

        self.assertEqual(datos["precio"], 40.0)
        self.assertEqual(datos["id"], 4)
        self.assertEqual(datos["nombre"], "Parlante Bluetooth")
        
    def test_eliminar_producto_valido_devuelve_200(self):
        cantidad_inicial = len(productos)
        
        respuesta = self.cliente.delete("/productos/4")

        self.assertEqual(respuesta.status_code, 200)

        datos = respuesta.get_json()

        self.assertEqual(
            datos["mensaje"],
            "Producto eliminado correctamente"
        )

        self.assertEqual(datos["producto"]["id"], 4)
        self.assertEqual(len(productos), cantidad_inicial - 1)
        respuesta_2 = self.cliente.get("/productos/4")
        self.assertEqual(respuesta_2.status_code, 404)
        
    def test_reemplazar_producto_con_id_distinto_devuelve_400(self):
        producto_modificado = {
            "id":99,
            "nombre": "Parlante cambiado",
            "precio": 40.0
        }
        
        respuesta = self.cliente.put(
            "/productos/4",
            json=producto_modificado
        )
        
        datos = respuesta.get_json()
        
        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(datos["error"], "El id del JSON debe coincidir con el id de la URL")
        