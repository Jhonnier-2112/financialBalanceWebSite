from flask import Blueprint, render_template, request, jsonify
from controllers.financial_statement_controller import  create_sub_category_controller, create_category_controller,save_financial_data_controller, get_category_types_controller, get_categories_by_type_controller, get_subcategories_by_category_controller, get_financial_amount_controller, create_category_type_controller,update_sub_category_controller

financial_statement_bp = Blueprint('financial_statement_bp', __name__)

@financial_statement_bp.route('/balance/categoryTypes', methods=['GET'])
def get_category_types():
    return get_category_types_controller()

@financial_statement_bp.route('/balance/categoryTypes', methods=['POST'])
def create_category_type():
    return create_category_type_controller()

@financial_statement_bp.route('/balance/category', methods=['GET'])
def get_categories():
    return get_categories_by_type_controller()

@financial_statement_bp.route('/balance/category', methods=['POST'])
def create_category():
    return create_category_controller()

@financial_statement_bp.route('/balance/subCategory', methods=['GET'])
def get_subcategories():
    return get_subcategories_by_category_controller()

@financial_statement_bp.route('/balance/subCategory', methods=['POST'])
def create_subcategory():
    return create_sub_category_controller()

@financial_statement_bp.route('/balance/subCategory/<int:sub_category_id>', methods=['PUT'])
def update_financial_data(sub_category_id):
    return update_sub_category_controller(sub_category_id)

@financial_statement_bp.route('/balance/financialData', methods=['GET'])
def get_financial_data():
    return get_financial_amount_controller()

@financial_statement_bp.route('/balance/financialData', methods=['POST'])
def save_financial_data():
    return save_financial_data_controller()

# ➡ **Rutas del front para balance financiero**
@financial_statement_bp.route('/balance', methods=['GET'])
def balance_page():
    return render_template('balance.html')
