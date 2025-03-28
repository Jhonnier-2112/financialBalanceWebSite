import os

class Config:
    # Obtener la URL de la base de datos desde las variables de entorno
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///mi_base.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "mi_secreto_por_defecto")
 # Configuración de Flask-Mail
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True") == "True"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False") == "True"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")  # Tu email
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")  # Tu contraseña o App Password
    MAIL_DEFAULT_SENDER = MAIL_USERNAME  # Remitente de los correos

    @staticmethod
    def get_db_uri():
        return Config.SQLALCHEMY_DATABASE_URI
