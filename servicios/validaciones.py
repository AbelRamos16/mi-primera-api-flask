def validar_datos_producto(producto):
    if not isinstance(producto["id"], int):
        return "El id debe ser un número entero"

    if not isinstance(producto["nombre"], str) or not producto["nombre"].strip():
        return "El nombre debe ser un texto no vacío"
    
    if not isinstance(producto["categoria_id"], int):
        return "La categoría debe ser un número entero"

    if (
        not isinstance(producto["precio"], (int, float))
        or producto["precio"] <= 0
    ):
        return "El precio debe ser un número mayor que cero"

    return None


def validar_cambios_producto(cambios):
    campos_permitidos = ["nombre", "precio", "categoria_id"]

    for campo in cambios:
        if campo not in campos_permitidos:
            return f"Campo no permitido: {campo}"

    if "nombre" in cambios:
        if not isinstance(cambios["nombre"], str) or not cambios["nombre"].strip():
            return "El nombre debe ser un texto no vacío"

    if "precio" in cambios:
        if (
            not isinstance(cambios["precio"], (int, float))
            or cambios["precio"] <= 0
        ):
            return "El precio debe ser un número mayor que cero"
        
    if "categoria_id" in cambios:
        if not isinstance(cambios["categoria_id"], int):
            return "La categoría debe ser un número entero"

    return None