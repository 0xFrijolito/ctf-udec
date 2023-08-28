import string
import random
import jwt
import pymongo

from flask import Flask, render_template, request, jsonify
from functools import wraps

# Creamos la app 
app = Flask(__name__)

# Conexión a la base de datos MongoDB
client = pymongo.MongoClient("mongodb://mongo:27017/")
db = client["mydatabase"]
collection = db["users"]

# Clave para general JWTs 
SECRET_KEY = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))

# Decorador para validar JWT en las rutas protegidas
# Esta parte no es relevante.
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Obtenemos el token
        token = request.cookies.get('session')

        # Verificamos que el token si existe
        if not token:
            return jsonify({'message': 'Falta el token'}), 401

        try:
            # Obtenemos el payload si es que este es valido
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = payload

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route("/")
def index ():
    return render_template("login.html")

@app.route("/api/login", methods=["POST"])
def login ():
    # Obtenemos las credenciales del usuario 🔑
    username = request.json["username"]
    password = request.json["password"]

    # Buscamos si existe un usuario con ese username y contrasena 🔭
    # A primera vista parece seguro 🤔
    user = collection.find_one({"username": username, "password": password})

    # Si encontramos un usuario y contrasena valida redirijimos al usuario a
    # la pagina con la flag 🏴
    if user:
        # Primero generamos un JWT valido para el usuario 
        token = jwt.encode({"message": "Felicidades ;)"}, SECRET_KEY, algorithm="HS256")

        # Enviamos el token cual nos verificara para obtener la flag 👍
        return jsonify({"token": token})

    # Si es que el usuario no existe retornamos un error
    return jsonify({"message": "Las credenciales son incorrectas 😿"}), 401

@app.route("/success", methods=["GET"])
@token_required
def flag (current_user):
    # Esto solo deberia ser valido para los admins 😼
    flag_link = open("flag.txt").read()
    return render_template("flag.html", flag_link=flag_link)

if __name__ == "__main__":
    # crea el usuario "admin" si no existe
    if not collection.find_one({"username": "admin"}):
        collection.insert_one({
            "username": "admin", 
            "password": ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
        })

    app.run(
        debug = True, 
        host = '0.0.0.0', 
        port = 1337
    )