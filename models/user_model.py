from flask_bcrypt import Bcrypt
from config.database import db  # ✅ Importa desde un módulo separado

bcrypt = Bcrypt()

class User(db.Model):  
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
