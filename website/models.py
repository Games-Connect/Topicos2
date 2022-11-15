from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, index=True)
    email = db.Column(db.String(150), unique=True, index=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    is_admin = db.Column(db.Boolean)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(150), unique=True, index=True)
    status = db.Column(db.Boolean, index=True, default=True)
    description = db.Column(db.String(1000))
    price = db.Column(db.Numeric(8,2))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    sub_categories = db.relationship('Subcategory')
    images = db.relationship('Image')

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(150), unique=True, index=True)
    status = db.Column(db.Boolean, index=True)
    photo = db.Column(db.BLOB, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

class Subcategory(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(150), index=True)
    status = db.Column(db.Boolean, index=True, default=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(150), index=True)
    status = db.Column(db.Boolean, index=True, default=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    products = db.relationship('Product')
