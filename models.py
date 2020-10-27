from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship

class User_product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    generic_name = db.Column(db.String(1000), unique=False, nullable=False)
    nutriscore = db.Column(db.String(100), unique=False, nullable=True)
    image_url = db.Column(db.String(500), unique=False, nullable=False)
    labels = db.Column(db.String(3000), unique=False, nullable=False)
    stores = db.Column(db.String(500), unique=False, nullable=False)
    categories = db.Column(db.String(3000), unique=False, nullable=False)
    
    searched_products = db.relationship("Searched_product", backref="user_product")
    
    
class Searched_product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    generic_name = db.Column(db.String(1000), unique=False, nullable=False)
    nutriscore = db.Column(db.String(100), unique=False, nullable=True)
    image_url = db.Column(db.String(500), unique=False, nullable=False)
    labels = db.Column(db.String(3000), unique=False, nullable=False)
    stores = db.Column(db.String(500), unique=False, nullable=False)
    categories = db.Column(db.String(3000), unique=False, nullable=False)

    user_product_id = Column(Integer, ForeignKey('user_product.id'))