from flask import Blueprint, render_template, request, jsonify
from controllers.user_controller import register_user 
from controllers.user_controller import login_user

user_bp = Blueprint('user_bp', __name__)

# Ruta para mostrar el formulario de login
@user_bp.route('/users/login', methods=['GET'])
def login_page():
    return render_template('login.html')

# Ruta para manejar el login
@user_bp.route('/users/login', methods=['POST'])
def login():
    return login_user()

# ➡ **Nueva ruta para el formulario de registro**
@user_bp.route('/users/register', methods=['GET'])
def register_page():
    return render_template('register.html')

# ➡ **Nueva ruta para manejar el registro de usuarios**
@user_bp.route('/users/register', methods=['POST'])
def register():
    return register_user() 
