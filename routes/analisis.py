from flask import Blueprint, render_template, request, jsonify

analisis = Blueprint('analisis', __name__)

# ➡ **Rutas del front para balance financiero**
@analisis.route('/analisis', methods=['GET'])
def balance_page():
    return render_template('analisis.html')