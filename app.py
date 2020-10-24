from flask import Flask, render_template, url_for, redirect, request
from product import Product
from alphabet import ALPHABET
import requests

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def main():
    """
    This is the main route of the program.
    It renders the index.html template.
    If a Post method is used on the template, it requests the value of the inputs in the form.
    If a barcode has been send, we send it out to the Product object, and call it's different method to get datas.
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

if __name__ == '__main__':
   app.run(debug=True)