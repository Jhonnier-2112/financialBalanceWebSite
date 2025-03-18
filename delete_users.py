from app import create_app
from config.database import db
from models.user_model import User

# Crear la aplicación y establecer el contexto
app = create_app()
with app.app_context():
    db.session.query(User).delete()
    db.session.commit()
    print("✅ Todos los usuarios han sido eliminados correctamente.")
