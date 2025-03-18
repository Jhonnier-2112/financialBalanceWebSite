from flask import Blueprint, render_template, request, jsonify

management_bp = Blueprint('gestion', __name__)

# ➡ **Rutas del front para balance financiero**
@management_bp.route('/gestion', methods=['GET'])
def balance_page():
    return render_template('management.html')