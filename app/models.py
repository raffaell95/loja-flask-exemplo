from sqlalchemy.orm import backref
from app.extensions import db
from datetime import datetime
from app.enums import EStatus


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(84), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)
    items = db.relationship("Item", backref="user", uselist=True)

    def __repr__(self) -> str:
        return self.email


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(130), nullable=False, unique=True, index=True)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.LargeBinary, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    created_at = db.Column(db.DateTime, default=datetime.now())
    items = db.relationship("Item", backref="product", uselist=True)

    def __repr__(self) -> str:
        return self.name


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    slug = db.Column(db.String(35), nullable=False, unique=True, index=True)
    products = db.relationship("Product", backref="categories", uselist=True)

    def __repr__(self) -> str:
        return self.name


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    reference_id = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(30), default=EStatus.CREATED.value, nullable=False)
    item = db.relationship("Item", backref="order", uselist=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self) -> str:
        return f"order number: {self.reference_id}"


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f"order number: ${self.order.number} quantity: {self.quantity} user: {self.user.profile.first_name}"