from flask import Blueprint, render_template, request
from controllers.user_controller import register_user, login_user, reset_password

user_bp = Blueprint("user_bp", __name__)

# Ruta para mostrar el formulario de login
@user_bp.route("/users/login", methods=["GET"])
def login_page():
    return render_template("login.html")

# Ruta para manejar el login
@user_bp.route("/users/login", methods=["POST"])
def login():
    return login_user()

# Ruta para mostrar el formulario de registro
@user_bp.route("/users/register", methods=["GET"])
def register_page():
    return render_template("register.html")

# Ruta para manejar el registro de usuarios
@user_bp.route("/users/register", methods=["POST"])
def register():
    return register_user()

@user_bp.route("/users/generate_password", methods=["POST"])
def reset():
    return reset_password()

@user_bp.route("/users/generate_password", methods=["GET"])
def generated_password():
    return render_template("generate_password.html")