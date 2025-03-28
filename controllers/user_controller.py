from models.user_model import db, User
from flask import jsonify, request, session
from sqlalchemy.exc import SQLAlchemyError
import bcrypt
import random
import string
from werkzeug.security import generate_password_hash
from utils.send_email import send_email

def register_user():
    """Registra un nuevo usuario en la base de datos usando bcrypt directamente"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Solicitud inválida, asegúrate de enviar un JSON"}), 400

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return jsonify({"error": "Todos los campos son obligatorios"}), 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "El correo ya está registrado"}), 400

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Usuario registrado exitosamente"}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error al registrar usuario", "details": str(e)}), 500

def login_user():
    """Autentica a un usuario"""
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email y contraseña son obligatorios"}), 400

    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    try:
        if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            session["user_id"] = user.id  
            return jsonify({"message": "Login exitoso", "token": "fake-jwt-token"}), 200
        else:
            return jsonify({"error": "Credenciales incorrectas"}), 401
    except ValueError:
        return jsonify({"error": "Formato de contraseña incorrecto. Intenta restablecer tu contraseña."}), 500

def generate_random_password(length=12):
    """Genera una contraseña aleatoria"""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def update_password(email):
    user = User.query.filter_by(email=email).first()  # Buscar usuario
    if not user:
        return False  # Si no existe, salir

    new_password = generate_random_password()  # Generar nueva contraseña
    user.password = generate_password_hash(new_password)  # Encriptar
    db.session.commit()

    # Ahora pasamos el email, nombre y la nueva contraseña a send_email()
    if send_email(user.email, user.name, new_password):
        return True
    return False


def reset_password():
    """Endpoint para restablecer la contraseña"""
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "El correo es obligatorio"}), 400

    if update_password(email):
        return jsonify({"message": "Nueva contraseña enviada al correo"}), 200
    else:
        return jsonify({"error": "Usuario no encontrado o error al enviar correo"}), 404
