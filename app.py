from product import Product
from alphabet import ALPHABET
import requests
from flask import Flask, render_template, url_for, redirect, request

from __init__ import app

from models import User_product, Searched_product, db
import ast

import socket

errors = []

@app.route('/', methods = ['POST', 'GET'])
def main():
    """
    This is the main route of the program.
    It renders the index.html template.
    If a Post method is used on the template, it requests the input value of the form.
    If a barcode has been sent, we use it as a parameter of the Product object, and call its different method to get datas.
    For more informations on what datas are sent, type help(Product).
    """ 
    print("after : ", errors)

    if request.method == 'POST':
        barcode = request.form['barcode']
        user_product = Product(barcode)

        if user_product.api_response() == True:
            up_get = user_product.get()
            return render_template('index.html', user_product=up_get, results=user_product.fetch_similar_better_product())
        else:
            c = 0
            for error in errors:
                if error == 'Produit Introuvable':
                    c = 1
            if c == 0:
                errors.append('Produit Introuvable')

            return render_template('index.html', errors=errors)
    return render_template('index.html', errors=errors)

@app.route('/save_in_db/', methods = ['POST', 'GET'])
def save_in_db():
    """
    Take the "searched_product" dictionnary of datas to save it next to the initial "user_product".
    """
    #errors = []
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
        try:
            db.session.add(user_product)
            db.session.commit()
        except:
            db.session.rollback()
            #print("Produt already in database.")

        user_product = User_product.query.filter_by(name=products['user_product']['name']).first()

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
        try:
            db.session.add(searched_product)
            db.session.commit()
        except:
            db.session.rollback()
            c = 0
            for error in errors:
                if error == 'Ce produit est déjà sauvegardé':
                    c = 1
            if c == 0:
                errors.append('Ce produit est déjà sauvegardé')
            print("except : ", errors)

    return redirect(url_for('main'))

@app.route('/mesproduits')
def my_products():
    """
    This is the my products route, that displays the searched product and the alternative saved.
    """
    products = User_product.query.all()
    return render_template('my_products.html', products=products)

@app.route('/delete_from_db', methods = ['POST', 'GET'])
def delete_from_db():
    """
    Here we request the product that the user wants to delete and its alternative and we delete it from the db.
    """
    if request.method == 'POST':
        products = request.form['products']
        products = ast.literal_eval(products)
        user_product = User_product.query.filter_by(id=products['user_product']).first()
        searched_product = Searched_product.query.filter_by(id=products['searched_product']).first()
        db.session.delete(user_product)
        db.session.delete(searched_product)
        db.session.commit()

    return redirect(url_for('my_products'))
  


# Function to display hostname and 
# IP address 
def get_Host_name_IP(): 
    try: 
        host_name = socket.gethostname() 
        host_ip = socket.gethostbyname(host_name)
        print("host : ", host_name)
        return str(host_ip)
    except: 
        print("Unable to get Hostname and IP") 
  
# Driver code 
 #Function call 
if __name__ == '__main__':
   app.run(debug=True, host=get_Host_name_IP())