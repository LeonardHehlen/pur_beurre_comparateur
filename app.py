from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from product import Product
from alphabet import ALPHABET
import requests

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/db'

@app.route('/', methods = ['POST', 'GET'])
def main():
    """
    This is the main route of the program.
    It renders the index.html template.
    If a Post method is used on the template, it requests the input value of the form.
    If a barcode has been sent, we use it as a parameter of the Product object, and call its different method to get datas.
    For more informations on what datas are sent, type help(Product).
    """

    error = ''

    if request.method == 'POST':
        barcode = request.form['barcode']
        user_product = Product(barcode)
        if user_product.api_response() == True:
            user_product.get()
            return render_template('index.html', user_product=user_product.get(), results=user_product.fetch_similar_better_product())
        else:
            error = 'Produit Introuvable'
            return render_template('index.html', error=error)

    return render_template('index.html')

@app.route('/save_in_db/', methods = ['POST', 'GET'])
def save_in_db():
    """
    Take the "searched_product" dictionnary of datas to save it next to the initial "user_product".
    """
    if request.method == 'POST':
        products = request.form['products']
        print(products)
    return redirect(url_for('main'))

if __name__ == '__main__':
   app.run(debug=True)