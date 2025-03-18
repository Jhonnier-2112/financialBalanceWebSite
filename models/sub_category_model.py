from config.database import db

class SubCategory(db.Model):
    __tablename__ = 'sub_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    observation = db.Column(db.String(100), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    def __init__(self, name,category_id, observation= None):
        self.name = name
        self.observation = observation
        self.category_id = category_id
        