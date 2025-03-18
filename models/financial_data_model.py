from config.database import db

class FinancialData(db.Model):
    __tablename__ = "financial_data"

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.DECIMAL, nullable=False)
    sub_category_id = db.Column(db.Integer, db.ForeignKey('sub_categories.id'), nullable=False)

    def __init__(self, month, year, amount, sub_category_id):
        self.month = month
        self.year = year
        self.amount = amount
        self.sub_category_id = sub_category_id
