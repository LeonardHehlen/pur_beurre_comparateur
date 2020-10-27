from product import Product
from alphabet import ALPHABET
import requests
from flask import Flask, render_template, url_for, redirect, request

from __init__ import app

from models import User_product, Searched_product, db
import ast

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
            up_get = user_product.get()
            return render_template('index.html', user_product=up_get, results=user_product.fetch_similar_better_product())
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
        products = ast.literal_eval(products)

        user_product = User_product(
                                    name=products['user_product']['name'],
                                    generic_name=products['user_product']['generic_name'],
                                    nutriscore=products['user_product']['nutriscore'],
                                    image_url=products['user_product']['image_url'],
                                    labels=products['user_product']['labels'],
                                    stores=products['user_product']['stores'],
                                    categories=str(products['user_product']['categories'])
                                    )
        db.session.add(user_product)
        db.session.commit()

        user_product = User_product.query.filter_by(name=products['user_product']['name']).first()
        print(user_product.id)
        searched_product = Searched_product(
                            name=products['searched_product']['name'],
                            generic_name=products['searched_product']['generic_name'],
                            nutriscore=products['searched_product']['nutriscore'],
                            image_url=products['searched_product']['image_url'],
                            labels=products['searched_product']['labels'],
                            stores=products['searched_product']['stores'],
                            categories=products['searched_product']['categories'],

                            user_product_id=user_product.id
                            )
        db.session.add(searched_product)
        db.session.commit()
    return redirect(url_for('main'))

if __name__ == '__main__':
   app.run(debug=True)