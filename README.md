# Mi Primera API de Productos

## Descripción

Proyecto de una API REST desarrollada con Python y Flask para administrar productos.

La API permite consultar, crear, actualizar, reemplazar y eliminar productos. Los datos se almacenan en un archivo JSON, por lo que se conservan aunque el servidor se detenga y vuelva a iniciar.

El proyecto también incluye validaciones de datos, una estructura modular y pruebas automatizadas con `unittest`.

## Funcionalidades

- Consultar todos los productos.
- Consultar un producto mediante su id.
- Consultar el estado de la API y la cantidad de productos registrados.
- Crear productos nuevos.
- Evitar ids duplicados.
- Reemplazar completamente un producto con `PUT`.
- Actualizar parcialmente nombre o precio con `PATCH`.
- Eliminar productos.
- Validar campos obligatorios, tipos de datos y valores.
- Guardar los cambios automáticamente en un archivo JSON.
- Ejecutar pruebas automatizadas sin iniciar el servidor.

## Tecnologías

- Python
- Flask
- JSON
- unittest
- requests

## Estructura del proyecto

```text
mi_primer_api/
├── data/
│   └── productos.json
├── rutas/
│   ├── __init__.py
│   └── productos.py
├── servicios/
│   ├── __init__.py
│   ├── archivo.py
│   └── validaciones.py
├── tests/
│   └── test_api.py
├── app.py
├── cliente_delete.py
├── cliente_patch.py
├── cliente_post.py
├── cliente_put.py
├── cliente_validacion.py
└── README.md
```

## Organización del código

### `app.py`

Crea la aplicación Flask, define las rutas generales y registra el Blueprint de productos.

### `rutas/productos.py`

Contiene las rutas relacionadas con el CRUD de productos:

- `GET`
- `POST`
- `PUT`
- `PATCH`
- `DELETE`

También administra la lista de productos cargada desde el archivo JSON.

### `servicios/archivo.py`

Contiene las funciones para cargar y guardar los productos en `data/productos.json`.

### `servicios/validaciones.py`

Contiene las validaciones para productos completos y cambios parciales.

### `tests/test_api.py`

Contiene las pruebas automatizadas de la API utilizando `unittest` y el cliente de pruebas de Flask.

## Instalación

1. Clonar el repositorio o descargar el proyecto.

2. Abrir una terminal dentro de la carpeta del proyecto.

3. Instalar las dependencias:

```bash
pip install flask requests
```

## Ejecutar la API

Desde la carpeta principal del proyecto, ejecutar:

```bash
python app.py
```

El servidor estará disponible en:

```text
http://127.0.0.1:5000
```

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/` | Muestra un mensaje de bienvenida. |
| `GET` | `/saludo` | Muestra un saludo desde la API. |
| `GET` | `/productos` | Devuelve todos los productos. |
| `GET` | `/productos/<id>` | Devuelve un producto por su id. |
| `GET` | `/estado` | Devuelve el estado de la API y la cantidad de productos. |
| `POST` | `/productos` | Crea un producto. |
| `PUT` | `/productos/<id>` | Reemplaza completamente un producto. |
| `PATCH` | `/productos/<id>` | Actualiza parcialmente un producto. |
| `DELETE` | `/productos/<id>` | Elimina un producto. |

## Ejemplo de producto

```json
{
    "id": 4,
    "nombre": "Parlante Bluetooth",
    "precio": 35.0
}
```

## Ejemplos de solicitudes

### Obtener productos

```text
GET /productos
```

Respuesta:

```json
[
    {
        "id": 1,
        "nombre": "Mouse inalámbrico",
        "precio": 25.0
    },
    {
        "id": 2,
        "nombre": "Teclado",
        "precio": 35.0
    }
]
```

### Crear un producto

```text
POST /productos
```

```json
{
    "id": 6,
    "nombre": "Auriculares",
    "precio": 20.0
}
```

Respuesta esperada:

```text
201 Created
```

### Actualizar parcialmente un producto

```text
PATCH /productos/4
```

```json
{
    "precio": 40.0
}
```

Respuesta esperada:

```text
200 OK
```

### Eliminar un producto

```text
DELETE /productos/4
```

Respuesta esperada:

```json
{
    "mensaje": "Producto eliminado correctamente",
    "producto": {
        "id": 4,
        "nombre": "Parlante Bluetooth",
        "precio": 35.0
    }
}
```

## Validaciones

La API verifica los siguientes casos:

- No se permiten solicitudes sin JSON.
- `id`, `nombre` y `precio` son obligatorios para `POST` y `PUT`.
- El id debe ser un número entero.
- El nombre debe ser texto y no puede estar vacío.
- El precio debe ser un número mayor que cero.
- No se permiten ids duplicados.
- En `PUT`, el id del JSON debe coincidir con el id de la URL.
- En `PATCH`, solo se permite modificar `nombre` y `precio`.
- Las operaciones sobre productos inexistentes devuelven `404`.

## Códigos de respuesta

| Código | Significado |
|---|---|
| `200` | Solicitud procesada correctamente. |
| `201` | Producto creado correctamente. |
| `400` | Datos enviados inválidos. |
| `404` | Producto no encontrado. |

## Pruebas automatizadas

Para ejecutar las pruebas:

```bash
python -m unittest tests/test_api.py
```

La suite incluye pruebas para:

- Ruta principal.
- Estado y cantidad de productos.
- Búsqueda de producto inexistente.
- Campos obligatorios.
- Ids duplicados.
- Creación válida.
- Actualización parcial con `PATCH`.
- Eliminación con `DELETE`.
- Validación de id en `PUT`.

Las pruebas utilizan `setUp()` y `tearDown()` para restaurar los productos originales después de cada ejecución, evitando que los datos de prueba queden guardados en el archivo JSON.

## Aprendizajes

- Creación de APIs REST con Flask.
- Uso de rutas y métodos HTTP.
- Manejo de respuestas JSON.
- Implementación de operaciones CRUD.
- Persistencia de datos con archivos JSON.
- Validación de solicitudes y manejo de errores HTTP.
- Organización de proyectos usando módulos, paquetes y Blueprints.
- Pruebas automatizadas de una API con `unittest`.
- Uso de Git y GitHub para documentar proyectos.