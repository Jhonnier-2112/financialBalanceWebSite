from config.database import db

class CategoryType(db.Model):
    __tablename__ = "category_types"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    observation = db.Column(db.String(100), nullable=False)

    def __init__(self, name, observation):
        self.name = name
        self.observation = observation