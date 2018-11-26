from sqlalchemy.sql import func

from project import db


class Smartphone(db.Model):

    __tablesmartphone__ = 'smartphones'
    idSmartphone = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    brand = db.Column(db.String(128), nullable=False)
    price = db.Column(db.String(4), nullable=False)
    quantity = db.Column(db.String(128), nullable=False)
    color = db.Column(db.String(128), nullable=False)
    creation_date = db.Column(db.DateTime, default=func.now(), nullable=False)
    modification_date = db.Column(
        db.DateTime, default=func.now(), nullable=True)
    status = db.Column(db.Boolean(), default=True, nullable=False)

    def to_json(self):
        return {
            'idSmartphone': self.idSmartphone,
            'name': self.name,
            'brand': self.brand,
            'price': self.price,
            'quantity': self.quantity,
            'color': self.color
        }

    def __init__(self, name, brand, price, quantity, color):
        self.name = name
        self.brand = brand
        self.price = price
        self.quantity = quantity
        self.color = color
