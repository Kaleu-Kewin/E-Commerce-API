from src.database import db

class Product(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(120), nullable=False)
    price       = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(500), nullable=True)

    def __init__(self, name: str, price, description: str) -> None:
        self.name        = name
        self.price       = price
        self.description = description
