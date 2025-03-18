import os

class Config:
    # Obtener la URL de la base de datos desde las variables de entorno
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///mi_base.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def get_db_uri():
        return Config.SQLALCHEMY_DATABASE_URI
