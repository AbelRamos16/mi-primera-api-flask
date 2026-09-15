from flask import Blueprint, jsonify, request

from servicios.productos_db import (
    obtener_todos_los_productos,
    obtener_producto_por_id,
    crear_producto as crear_producto_db,
    actualizar_producto as actualizar_producto_db,
    eliminar_producto as eliminar_producto_db
)
from servicios.validaciones import (
    validar_datos_producto,
    validar_cambios_producto
)


productos_bp = Blueprint("productos", __name__)


@productos_bp.get("/productos")
def obtener_productos():
    productos = obtener_todos_los_productos()

    return jsonify(productos)


@productos_bp.get("/productos/<int:producto_id>")
def obtener_producto(producto_id):
    producto = obtener_producto_por_id(producto_id)

    if producto is None:
        return jsonify({
            "error": "Producto no encontrado"
        }), 404

    return jsonify(producto)


@productos_bp.get("/estado")
def obtener_estado():
    productos = obtener_todos_los_productos()

    return jsonify({
        "estado": "activa",
        "productos_registrados": len(productos)
    })


@productos_bp.post("/productos")
def crear_producto():
    nuevo_producto = request.get_json()

    if not nuevo_producto:
        return jsonify({
            "error": "No se enviaron datos JSON"
        }), 400

    campos_requeridos = ["id", "nombre", "precio"]

    for campo in campos_requeridos:
        if campo not in nuevo_producto:
            return jsonify({
                "error": f"Falta el campo: {campo}"
            }), 400

    error_validacion = validar_datos_producto(nuevo_producto)

    if error_validacion:
        return jsonify({
            "error": error_validacion
        }), 400

    producto_creado = crear_producto_db(nuevo_producto)

    if not producto_creado:
        return jsonify({
            "error": "Ya existe un producto con ese id"
        }), 400

    return jsonify(nuevo_producto), 201


@productos_bp.put("/productos/<int:producto_id>")
def reemplazar_producto(producto_id):
    producto_actualizado = request.get_json()

    if not producto_actualizado:
        return jsonify({
            "error": "No se enviaron datos JSON"
        }), 400

    campos_requeridos = ["id", "nombre", "precio"]

    for campo in campos_requeridos:
        if campo not in producto_actualizado:
            return jsonify({
                "error": f"Falta el campo: {campo}"
            }), 400

    error_validacion = validar_datos_producto(producto_actualizado)

    if error_validacion:
        return jsonify({
            "error": error_validacion
        }), 400

    if producto_actualizado["id"] != producto_id:
        return jsonify({
            "error": "El id del JSON debe coincidir con el id de la URL"
        }), 400

    cambios = {
        "nombre": producto_actualizado["nombre"],
        "precio": producto_actualizado["precio"]
    }

    actualizado = actualizar_producto_db(producto_id, cambios)

    if not actualizado:
        return jsonify({
            "error": "Producto no encontrado"
        }), 404

    producto = obtener_producto_por_id(producto_id)

    return jsonify(producto), 200


@productos_bp.patch("/productos/<int:producto_id>")
def actualizar_producto_parcial(producto_id):
    cambios = request.get_json()

    if not cambios:
        return jsonify({
            "error": "No se enviaron datos JSON"
        }), 400

    error_validacion = validar_cambios_producto(cambios)

    if error_validacion:
        return jsonify({
            "error": error_validacion
        }), 400

    actualizado = actualizar_producto_db(producto_id, cambios)

    if not actualizado:
        return jsonify({
            "error": "Producto no encontrado"
        }), 404

    producto = obtener_producto_por_id(producto_id)

    return jsonify(producto), 200


@productos_bp.delete("/productos/<int:producto_id>")
def eliminar_producto(producto_id):
    producto = obtener_producto_por_id(producto_id)

    if producto is None:
        return jsonify({
            "error": "Producto no encontrado"
        }), 404

    eliminar_producto_db(producto_id)

    return jsonify({
        "mensaje": "Producto eliminado correctamente",
        "producto": producto
    }), 200