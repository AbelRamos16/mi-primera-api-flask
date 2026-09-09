from flask import Blueprint, jsonify, request

from servicios.archivo import cargar_productos, guardar_productos
from servicios.validaciones import (
    validar_datos_producto,
    validar_cambios_producto
)

productos_bp = Blueprint("productos", __name__)

productos = cargar_productos()


@productos_bp.get("/productos")
def obtener_productos():
    return jsonify(productos)


@productos_bp.get("/productos/<int:producto_id>")
def obtener_producto(producto_id):
    for producto in productos:
        if producto["id"] == producto_id:
            return jsonify(producto)

    return jsonify({
        "error": "Producto no encontrado"
    }), 404


@productos_bp.get("/estado")
def obtener_estado():
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

    for producto in productos:
        if producto["id"] == nuevo_producto["id"]:
            return jsonify({
                "error": "Ya existe un producto con ese id"
            }), 400

    productos.append(nuevo_producto)
    guardar_productos(productos)

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

    for indice, producto in enumerate(productos):
        if producto["id"] == producto_id:
            productos[indice] = producto_actualizado
            guardar_productos(productos)

            return jsonify(producto_actualizado), 200

    return jsonify({
        "error": "Producto no encontrado"
    }), 404
    
@productos_bp.patch("/productos/<int:producto_id>")
def actualizar_producto(producto_id):
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

    for producto in productos:
        if producto["id"] == producto_id:
            producto.update(cambios)
            guardar_productos(productos)

            return jsonify(producto), 200

    return jsonify({
        "error": "Producto no encontrado"
    }), 404
    
@productos_bp.delete("/productos/<int:producto_id>")
def eliminar_producto(producto_id):
    for indice, producto in enumerate(productos):
        if producto["id"] == producto_id:
            eliminado = productos.pop(indice)
            guardar_productos(productos)

            return jsonify({
                "mensaje": "Producto eliminado correctamente",
                "producto": eliminado
            }), 200

    return jsonify({
        "error": "Producto no encontrado"
    }), 404