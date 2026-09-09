from flask import Flask, jsonify

from rutas.productos import productos_bp


app = Flask(__name__)


@app.get("/")
def inicio():
    return jsonify({
        "mensaje": "Mi primera API funciona correctamente"
    })


@app.get("/saludo")
def saludo():
    return jsonify({
        "mensaje": "¡Hola! Bienvenido a mi API"
    })


app.register_blueprint(productos_bp)


if __name__ == "__main__":
    app.run(debug=True)