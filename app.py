from flask import Flask, render_template, url_for, redirect, request
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

    return render_template('index.html')

if __name__ == '__main__':
   app.run(debug=True)