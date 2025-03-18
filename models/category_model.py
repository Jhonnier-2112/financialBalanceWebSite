from config.database import db

class Category(db.Model):
    __tablename__ = "categories"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    observation = db.Column(db.String(100), nullable=True)
    category_type_id = db.Column(db.Integer, db.ForeignKey('category_types.id'), nullable=True)

    def __init__(self, name,category_type_id, observation=None):
        self.category_type_id = category_type_id
        self.name = name
        self.observation = observation