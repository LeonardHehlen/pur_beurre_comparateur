from flask import Flask, render_template, url_for, redirect, request
from alphabet import ALPHABET
import requests

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def main():
    results = []
    user_product = []
    error = None
    if request.method == 'POST':
        barcode = request.form['code']

        user_product = requests.get("https://fr.openfoodfacts.org//api/v0/produit/" + barcode)

        try:
            nutriscore = str(user_product.json()['product']['nutrition_grade_fr'])
        except:
            results = []
            user_product = []
            return render_template('index.html', results=results, user_product=user_product, error='Produit Introuvable')

        generic_name = str(user_product.json()['product']['generic_name'])
        print(generic_name, ' , ' ,nutriscore.capitalize())

        categories = []

        alphabet = ALPHABET

        for i, letter in enumerate(alphabet):
            if nutriscore == letter:
                nutriscore = i

        for category in user_product.json()['product']['categories_hierarchy']:
            categories.append(category)

        search_url = 'https://fr.openfoodfacts.org/cgi/search.pl?action=process&page_size=1000&tagtype_0=categories&tag_contains_0=contains&tag_0=' + str(categories[0] + '&json=true')

        search_products = requests.get(search_url)
        products = search_products.json()['products']

        final_products = []

        for product in products:
            c = product['categories_hierarchy']
            if c[c.__len__()-2] == categories[categories.__len__()-2]:
                final_products.append(product)

        results = []

        for i, product in enumerate(final_products):
            product_nutriscore = product['nutrition_grade_fr']
            try:
                name = product['generic_name']
            except:
                pass

            for i, letter in enumerate(alphabet):
                if product_nutriscore == letter:
                    product_nutriscore = i

            if product_nutriscore <= nutriscore:
                if product_nutriscore is not 4:
                    if name =! '':
                        results.append(product)

        for result in results:
            try:
                print(result['generic_name'], ' , ', result['nutrition_grade_fr'])
            except:
                print("Element erroné")

    return render_template('index.html', results=results, user_product=user_product)

if __name__ == '__main__':
   app.run(debug=True)