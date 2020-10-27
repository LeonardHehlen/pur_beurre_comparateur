from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship
 
app = Flask(__name__)
 
db = SQLAlchemy(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/db'

class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True, nullable=False)
    other_tests = db.relationship("Other_test", backref='parent')


class Other_test(db.Model):
    __tablename__ = 'other_test'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True, nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id')) 

# x = Other_test(title='Hello', test_id=1)

# db.session.add(x)
# db.session.commit()


x = Test.query.filter_by(id=1).first()

for y in x.other_tests:
    print(y.parent.title)
# When I Call User_product, I got the searched_product associated