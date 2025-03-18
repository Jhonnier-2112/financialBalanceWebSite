from flask import Blueprint, render_template, request, jsonify

profiability_bp = Blueprint('porfiability', __name__)

# ➡ **Rutas del front para balance financiero**
@profiability_bp.route('/profiability', methods=['GET'])
def balance_page():
    return render_template('profiability.html')