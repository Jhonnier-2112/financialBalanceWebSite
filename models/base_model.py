from config.database import db 

class BaseModel(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=db.default_datetime)
    updated_at = db.Column(db.DateTime, default=db.default_datetime, onupdate=db.default_datetime)
    deleted_at = db.Column(db.DateTime, nullable=True)