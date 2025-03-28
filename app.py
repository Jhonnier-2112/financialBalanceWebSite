from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from config.config import Config
from config.database import db
from config.extensions import mail  # ✅ Importar mail desde extensions.py

# Cargar variables de entorno
load_dotenv()

def create_app():
    app = Flask(__name__)

    SECRET_KEY = os.getenv("SECRET_KEY")
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config["VERSION"] = "1.0.1"

    # Cargar configuración
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    mail.init_app(app)  # ✅ Inicializar Flask-Mail
    Migrate(app, db)

    # Registrar blueprints
    from routes.user_routes import user_bp
    from routes.financial_statement_routes import financial_statement_bp
    from routes.analisis import analisis
    from routes.profiability import profiability_bp
    from routes.management import management_bp

    app.register_blueprint(financial_statement_bp, url_prefix="/api")
    app.register_blueprint(analisis, url_prefix="/api")
    app.register_blueprint(user_bp, url_prefix="/api")
    app.register_blueprint(profiability_bp, url_prefix="/api")
    app.register_blueprint(management_bp, url_prefix="/api")

    return app

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render usa la variable PORT
    app = create_app()
    app.run(host="0.0.0.0", port=port)
