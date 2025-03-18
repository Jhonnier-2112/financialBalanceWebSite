from models.category_model import db, Category
from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from models.financial_data_model import FinancialData
from models.sub_category_model import SubCategory
from models.category_type_model import CategoryType

def get_category_types_controller():
    """Obtener los IDs y nombres de los tipos de categoría"""
    try:
        # Consulta para obtener los IDs y nombres de los tipos de categoría
        categories = db.session.query(CategoryType.id, CategoryType.name).all()

        if not categories:
            return jsonify({"message": "No hay tipos de categoría registrados"}), 404

        # Formatear la respuesta en JSON
        data = [{"id": category.id, "name": category.name} for category in categories]

        return jsonify(data), 200
    
    except SQLAlchemyError as e:
        return jsonify({"error": "Error al obtener tipos de categoría", "details": str(e)}), 500

def create_category_type_controller():
    """Crea una nueva categoría con nombre y observación"""
    try:
        data = request.get_json()

        name = data.get("name")
        observation = data.get("observation")

        if not name:
            return jsonify({"error": "El campo 'name' es obligatorio"}), 400

        # Verificar si ya existe una categoría con ese nombre
        existing_category = CategoryType.query.filter_by(name=name).first()
        if existing_category:
            return jsonify({"error": "Ya existe una categoría con este nombre"}), 400

        # Crear la nueva categoría
        new_category = CategoryType(name=name, observation=observation)
        db.session.add(new_category)
        db.session.commit()

        return jsonify({
            "message": "Categoría creada exitosamente",
            "category_id": new_category.id
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error al crear la categoría", "details": str(e)}), 500

def get_categories_by_type_controller():
    """Obtener categorías filtradas por el ID del tipo de categoría"""
    try:
        category_type_id = request.args.get("category_type_id", type=int)

        if not category_type_id:
            return jsonify({"error": "El parámetro 'category_type_id' es obligatorio"}), 400

        category_type = db.session.query(CategoryType).filter_by(id=category_type_id).first()
        if not category_type:
            return jsonify({"error": "Tipo de categoría no encontrado"}), 404

        categories = db.session.query(Category.id, Category.name).filter_by(category_type_id=category_type_id).all()

        if not categories:
            return jsonify({"message": "No hay categorías registradas para este tipo de categoría"}), 404

        data = [{"id": category.id, "name": category.name} for category in categories]

        return jsonify(data), 200
    
    except SQLAlchemyError as e:
        return jsonify({"error": "Error al obtener categorías", "details": str(e)}), 500
    
def get_subcategories_by_category_controller():
    """Obtener subcategorías filtradas por el ID de la categoría"""
    try:
        category_id = request.args.get("category_id", type=int)

        if not category_id:
            return jsonify({"error": "El parámetro 'category_id' es obligatorio"}), 400

        # Verificar si la categoría existe
        category = db.session.query(Category).filter_by(id=category_id).first()
        if not category:
            return jsonify({"error": "Categoría no encontrada"}), 404

        # Obtener las subcategorías asociadas a la categoría
        subcategories = db.session.query(SubCategory.id, SubCategory.name).filter_by(category_id=category_id).all()

        if not subcategories:
            return jsonify({"message": "No hay subcategorías registradas para esta categoría"}), 404

        # Formatear la respuesta en JSON
        data = [{"id": sub.id, "name": sub.name} for sub in subcategories]

        return jsonify(data), 200
    
    except SQLAlchemyError as e:
        return jsonify({"error": "Error al obtener subcategorías", "details": str(e)}), 500
    

def create_sub_category_controller():
    """Crea una nueva subcategoría asociada a una categoría existente"""
    try:
        data = request.get_json()

        category_id = data.get("category_id")  # Corregido el nombre de la clave
        sub_category_name = data.get("sub_category_name")

        if not category_id or not sub_category_name:
            return jsonify({"error": "Todos los campos (category_id, sub_category_name) son obligatorios"}), 400

        # Verificar si la categoría existe
        category = Category.query.get(category_id)
        if not category:
            return jsonify({"error": "La categoría especificada no existe"}), 404

        # Verificar si la subcategoría ya existe dentro de esa categoría
        existing_sub_category = SubCategory.query.filter_by(name=sub_category_name, category_id=category.id).first()
        if existing_sub_category:
            return jsonify({"error": "La subcategoría ya existe en esta categoría"}), 400

        # Crear la nueva subcategoría
        new_sub_category = SubCategory(name=sub_category_name, category_id=category.id)
        db.session.add(new_sub_category)
        db.session.commit()

        return jsonify({"message": "Subcategoría creada exitosamente", "sub_category_id": new_sub_category.id}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error al crear la subcategoría", "details": str(e)}), 500

def update_sub_category_controller(sub_category_id):
    """Actualiza una subcategoría existente por su ID"""
    try:
        data = request.get_json()

        new_name = data.get("sub_category_name")
        new_category_id = data.get("category_id")

        if not new_name or not new_category_id:
            return jsonify({"error": "Todos los campos (category_id, sub_category_name) son obligatorios"}), 400

        # Buscar la subcategoría por ID
        sub_category = SubCategory.query.get(sub_category_id)
        if not sub_category:
            return jsonify({"error": "Subcategoría no encontrada"}), 404

        # Verificar si la nueva categoría existe
        category = Category.query.get(new_category_id)
        if not category:
            return jsonify({"error": "La nueva categoría especificada no existe"}), 404

        # Verificar si ya existe una subcategoría con ese nombre en la misma categoría
        existing_sub_category = SubCategory.query.filter_by(name=new_name, category_id=new_category_id).first()
        if existing_sub_category and existing_sub_category.id != sub_category.id:
            return jsonify({"error": "Ya existe una subcategoría con ese nombre en esta categoría"}), 400

        # Actualizar datos
        sub_category.name = new_name
        sub_category.category_id = new_category_id

        db.session.commit()

        return jsonify({"message": "Subcategoría actualizada exitosamente"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error al actualizar la subcategoría", "details": str(e)}), 500
        
def create_category_controller():
    """Crea una nueva categoría asociada a un tipo de categoría existente"""

    try:
        data = request.get_json()

        category_type_id = data.get("category_type_id")
        category_name = data.get("category_name")

        if not category_type_id or not category_name:
            return jsonify({"error": "Todos los campos (category_type_id, category_name) son obligatorios"}), 400

        # Verificar si el tipo de categoría existe
        category_type = CategoryType.query.get(category_type_id)
        if not category_type:
            return jsonify({"error": "El tipo de categoría especificado no existe"}), 404

        # Verificar si la categoría ya existe dentro de ese tipo de categoría
        existing_category = Category.query.filter_by(name=category_name, category_type_id=category_type.id).first()
        if existing_category:
            return jsonify({"error": "La categoría ya existe en este tipo de categoría"}), 400

        # Crear la nueva categoría
        new_category = Category(name=category_name, category_type_id=category_type.id)
        db.session.add(new_category)
        db.session.commit()

        return jsonify({"message": "Categoría creada exitosamente", "category_id": new_category.id}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error al crear la categoría", "details": str(e)}), 500
    
def save_financial_data_controller():
    """Guarda una cantidad asociada a una subcategoría en un mes y año específicos"""
    try:
        data = request.get_json()
        
        year = data.get("year")
        month = data.get("month")
        sub_category_id = data.get("sub_category_id")
        amount = data.get("amount")

        if not year or not month or not sub_category_id or amount is None:
            return jsonify({"error": "Los campos year, month, sub_category y amount son obligatorios"}), 400

        # Buscar la subcategoría
        sub_category = SubCategory.query.filter_by(id=sub_category_id).first()
        if not sub_category:
            return jsonify({"error": "La subcategoría no existe"}), 404

        # Crear y guardar el registro de datos financieros
        financial_data = FinancialData(
            year=year,
            month=month,
            amount=amount,
            sub_category_id=sub_category.id
        )
        db.session.add(financial_data)
        db.session.commit()

        return jsonify({"message": "Cantidad guardada exitosamente"}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error al guardar la cantidad", "details": str(e)}), 500

def get_financial_amount_controller():
    """Obtiene la cantidad almacenada, permitiendo filtrar por año, lista de meses y subcategoría"""
    try:
        year = request.args.get("year", type=int)
        months = request.args.getlist("months", type=int)  # Ahora acepta una lista de meses
        sub_category_id = request.args.get("sub_category_id", type=int)

        # Construcción de la consulta dinámica
        query = db.session.query(FinancialData.amount)

        if year:
            query = query.filter(FinancialData.year == year)
        if months:  # Si se pasan varios meses, usamos .in_()
            query = query.filter(FinancialData.month.in_(months))
        if sub_category_id:
            query = query.filter(FinancialData.sub_category_id == sub_category_id)

        result = query.all()

        # Retornar solo los amounts en una lista
        data = [float(row[0]) for row in result]

        return jsonify(data), 200

    except SQLAlchemyError as e:
        return jsonify({"error": "Error al obtener la cantidad", "details": str(e)}), 500