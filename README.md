# Mi Primera API de Productos

## Descripción

API REST desarrollada con **Python, Flask y SQLite** para administrar productos y categorías.

La API permite consultar, crear, actualizar, reemplazar y eliminar productos. La información se almacena en una base de datos SQLite, por lo que los cambios se conservan aunque el servidor se detenga.

El proyecto incluye validaciones, relaciones entre tablas, estructura modular y pruebas automatizadas con `unittest`.

## Funcionalidades

* Consultar todos los productos.
* Consultar un producto por su `id`.
* Consultar el estado de la API.
* Crear productos nuevos.
* Evitar IDs duplicados.
* Reemplazar productos completamente con `PUT`.
* Actualizar productos parcialmente con `PATCH`.
* Eliminar productos.
* Registrar productos asociados a categorías.
* Validar datos obligatorios y tipos de datos.
* Validar que la categoría exista.
* Activar claves foráneas en SQLite.
* Ejecutar pruebas automatizadas sin iniciar el servidor.

## Tecnologías

* Python
* Flask
* SQLite
* unittest
* requests

## Estructura del proyecto

```text
mi_primer_api/
├── base_datos/
│   ├── __init__.py
│   ├── conexion.py
│   ├── crear_base.py
│   ├── crear_categorias.py
│   ├── insertar_categorias.py
│   ├── consultar_categorias.py
│   ├── consultar_productos.py
│   ├── insertar_producto.py
│   ├── buscar_producto.py
│   ├── actualizar_precio.py
│   ├── eliminar_producto.py
│   ├── migrar_productos_categoria.py
│   └── productos.db
├── data/
│   └── productos.json
├── rutas/
│   ├── __init__.py
│   └── productos.py
├── servicios/
│   ├── __init__.py
│   ├── archivo.py
│   ├── productos_db.py
│   └── validaciones.py
├── tests/
│   └── test_api.py
├── app.py
├── cliente_delete.py
├── cliente_patch.py
├── cliente_post.py
├── cliente_put.py
├── cliente_validacion.py
├── .gitignore
└── README.md
```

## Organización del código

### `app.py`

Crea la aplicación Flask y registra el Blueprint de productos.

### `rutas/productos.py`

Contiene las rutas HTTP de la API:

* `GET`
* `POST`
* `PUT`
* `PATCH`
* `DELETE`

También recibe las solicitudes, ejecuta validaciones y devuelve respuestas JSON.

### `servicios/productos_db.py`

Contiene las funciones que interactúan con SQLite:

* Consultar productos.
* Buscar productos por ID.
* Crear productos.
* Actualizar productos.
* Eliminar productos.
* Verificar si una categoría existe.

### `servicios/validaciones.py`

Contiene las validaciones de los datos recibidos por la API.

### `base_datos/conexion.py`

Centraliza la conexión con SQLite y activa las claves foráneas:

```sql
PRAGMA foreign_keys = ON;
```

### `tests/test_api.py`

Contiene las pruebas automatizadas utilizando `unittest` y el cliente de pruebas de Flask.

## Base de datos

La aplicación utiliza SQLite con dos tablas principales.

### Tabla `categorias`

Almacena las categorías disponibles.

| Campo    | Tipo    | Descripción                  |
| -------- | ------- | ---------------------------- |
| `id`     | INTEGER | Clave primaria               |
| `nombre` | TEXT    | Nombre único de la categoría |

### Tabla `productos`

Almacena los productos.

| Campo          | Tipo    | Descripción         |
| -------------- | ------- | ------------------- |
| `id`           | INTEGER | Clave primaria      |
| `nombre`       | TEXT    | Nombre del producto |
| `precio`       | REAL    | Precio del producto |
| `categoria_id` | INTEGER | Clave foránea       |

La relación entre las tablas es:

```text
categorias.id ← productos.categoria_id
```

Esto permite que cada producto pertenezca a una categoría existente.

## Instalación

1. Clonar o descargar el repositorio.
2. Abrir una terminal dentro de la carpeta del proyecto.
3. Instalar las dependencias:

```bash
pip install flask requests
```

## Ejecutar la API

Desde la carpeta principal del proyecto:

```bash
python app.py
```

El servidor estará disponible en:

```text
http://127.0.0.1:5000
```

## Endpoints

| Método   | Ruta              | Descripción                                    |
| -------- | ----------------- | ---------------------------------------------- |
| `GET`    | `/`               | Muestra un mensaje de bienvenida.              |
| `GET`    | `/saludo`         | Muestra un saludo.                             |
| `GET`    | `/productos`      | Devuelve todos los productos.                  |
| `GET`    | `/productos/<id>` | Devuelve un producto por su ID.                |
| `GET`    | `/estado`         | Devuelve el estado y la cantidad de productos. |
| `POST`   | `/productos`      | Crea un producto.                              |
| `PUT`    | `/productos/<id>` | Reemplaza completamente un producto.           |
| `PATCH`  | `/productos/<id>` | Actualiza parcialmente un producto.            |
| `DELETE` | `/productos/<id>` | Elimina un producto.                           |

## Ejemplo de producto

```json
{
    "id": 3,
    "nombre": "Monitor",
    "precio": 220.0,
    "categoria_id": 1
}
```

La categoría con ID `1` corresponde a `Tecnología`.

## Ejemplos de solicitudes

### Obtener productos

```http
GET /productos
```

Respuesta:

```json
[
    {
        "id": 2,
        "nombre": "Teclado mecánico",
        "precio": 45.0,
        "categoria_id": 1,
        "categoria": "Tecnología"
    },
    {
        "id": 3,
        "nombre": "Monitor",
        "precio": 220.0,
        "categoria_id": 2,
        "categoria": "Accesorios"
    }
]
```

### Crear un producto

```http
POST /productos
```

```json
{
    "id": 6,
    "nombre": "Auriculares",
    "precio": 20.0,
    "categoria_id": 1
}
```

Respuesta:

```text
201 Created
```

### Reemplazar un producto

```http
PUT /productos/2
```

```json
{
    "id": 2,
    "nombre": "Teclado actualizado",
    "precio": 50.0,
    "categoria_id": 1
}
```

> El ID del JSON debe coincidir con el ID de la URL.

### Actualizar parcialmente un producto

```http
PATCH /productos/3
```

```json
{
    "precio": 250.0
}
```

También es posible cambiar solamente la categoría:

```json
{
    "categoria_id": 2
}
```

### Eliminar un producto

```http
DELETE /productos/3
```

Respuesta:

```json
{
    "mensaje": "Producto eliminado correctamente",
    "producto": {
        "id": 3,
        "nombre": "Monitor",
        "precio": 250.0,
        "categoria_id": 2
    }
}
```

## Validaciones

La API verifica que:

* La solicitud contenga datos JSON.
* `id`, `nombre`, `precio` y `categoria_id` sean obligatorios en `POST` y `PUT`.
* El ID sea un número entero.
* El nombre sea texto y no esté vacío.
* El precio sea mayor que cero.
* `categoria_id` sea un número entero.
* La categoría exista en la base de datos.
* No existan IDs duplicados.
* En `PUT`, el ID del JSON coincida con el ID de la URL.
* En `PATCH`, solo se actualicen campos permitidos.
* Los productos inexistentes devuelvan código `404`.

## Códigos de respuesta

| Código | Significado                        |
| ------ | ---------------------------------- |
| `200`  | Solicitud procesada correctamente. |
| `201`  | Producto creado correctamente.     |
| `400`  | Datos enviados inválidos.          |
| `404`  | Producto no encontrado.            |

## Pruebas automatizadas

Para ejecutar las pruebas:

```bash
python -m unittest tests/test_api.py
```

Actualmente el proyecto cuenta con **12 pruebas automatizadas** para verificar:

* Ruta principal.
* Estado de la API.
* Consulta de productos.
* Búsqueda de productos inexistentes.
* Campos obligatorios.
* IDs duplicados.
* Creación válida.
* Actualización con `PATCH`.
* Reemplazo con `PUT`.
* Eliminación con `DELETE`.
* Categorías inexistentes.
* Validación del ID en `PUT`.

Las pruebas utilizan una base de datos temporal para no modificar la base de datos real.

## Aprendizajes

* Creación de APIs REST con Flask.
* Uso de métodos HTTP.
* Manejo de respuestas JSON.
* Implementación de operaciones CRUD.
* Uso de SQLite con Python.
* Creación de tablas y relaciones.
* Claves primarias y claves foráneas.
* Uso de `JOIN` para combinar información.
* Validación de datos y errores HTTP.
* Organización modular con paquetes y Blueprints.
* Pruebas automatizadas con `unittest`.
* Uso de clientes HTTP con `requests`.
* Uso de Git y GitHub para publicar proyectos.
