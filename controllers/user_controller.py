from models.user_model import db, User
from flask import jsonify, request, session
from sqlalchemy.exc import SQLAlchemyError
import bcrypt
import random
import string
from werkzeug.security import generate_password_hash
from utils.send_email import send_email
from utils.hashing import verify_password, hash_password  
import re

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

from werkzeug.security import check_password_hash

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
        # Verificar si la contraseña es bcrypt
        if user.password.startswith("$2b$") or user.password.startswith("$2a$"):  # bcrypt hashes
            if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                session["user_id"] = user.id  
                return jsonify({"message": "Login exitoso", "token": "fake-jwt-token"}), 200
        else:  
            # Si no es bcrypt, verificar si es werkzeug y migrar
            if check_password_hash(user.password, password):
                # Migrar la contraseña a bcrypt
                salt = bcrypt.gensalt()
                user.password = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
                db.session.commit()

                session["user_id"] = user.id  
                return jsonify({"message": "Login exitoso", "token": "fake-jwt-token"}), 200

        return jsonify({"error": "Credenciales incorrectas"}), 401

    except ValueError:
        return jsonify({"error": "Formato de contraseña incorrecto. Intenta restablecer tu contraseña."}), 500

def generate_random_password(length=12):
    """Genera una contraseña aleatoria"""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def update_password(email):
    user = User.query.filter_by(email=email).first()
    if not user:
        return False

    new_password = generate_random_password()  
    salt = bcrypt.gensalt()
    user.password = bcrypt.hashpw(new_password.encode("utf-8"), salt).decode("utf-8")  
    db.session.commit()

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
    
def change_password():
    """Cambia la contraseña validando la actual y los requisitos de seguridad."""
    data = request.get_json()
    print(data)
    email = data.get("email")
    current_password = data.get("current_password")
    new_password = data.get("new_password")

    if not email or not current_password or not new_password:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "El usuario no existe"}), 404

    if not verify_password(current_password, user.password):
        return jsonify({"error": "Contraseña actual incorrecta"}), 401

    # Validar seguridad de la nueva contraseña
    password_error = is_valid_password(new_password)
    if password_error:
        return jsonify({"error": password_error}), 400

    user.password = hash_password(new_password)
    db.session.commit()

    send_email(user.email, user.name, "Tu contraseña ha sido actualizada.")

    return jsonify({"message": "Contraseña actualizada correctamente"}), 200

def is_valid_password(password):
    """Verifica si la contraseña cumple con los requisitos de seguridad."""
    if len(password) < 6:
        return "La nueva contraseña debe tener al menos 6 caracteres."
    if not re.search(r"[A-Z]", password):
        return "La nueva contraseña debe contener al menos una letra mayúscula."
    if not re.search(r"[a-z]", password):
        return "La nueva contraseña debe contener al menos una letra minúscula."
    if not re.search(r"\d", password):
        return "La nueva contraseña debe contener al menos un número."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "La nueva contraseña debe contener al menos un carácter especial."
    return None
