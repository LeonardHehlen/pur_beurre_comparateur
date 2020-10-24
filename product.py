import requests

class Product:
    """
    Takes a food barcode as a parameter.
    api_response() gives you True if the request succeeded or False if it failed.
    The get() method returns a dict with the product informations.
    fetch_similar_better_product() method fetch similar products with a better nutrionnal score.
    """
    def __init__(self, barcode):

        self.barcode = barcode

        self.user_product = requests.get("https://fr.openfoodfacts.org//api/v0/produit/" + self.barcode)

        self.nutriscore = ''
        self.name = ''
        self.generic_name = ''
        self.categories = []
        self.image_url = ''
        self.stores = ''
        self.labels = ''

    def api_response(self):
        """
        Returns True if the product has been fetched from the API, False if not.
        Note that in this configuration, the openfoodfacts API doesn't send a 404 answer, so we have to interpret
        the non-existing ['product'] key has a 404. In this case, if this methods returns False, consider that the
        barcode inputed is wrong.
        """
        try:
            test.user_product.json()['product']
            return True
        except:
            return False

    def get(self):
        """
        Returns a dict with the keys 'nutriscore', 'generic_name', 'image_url', 'name', 'labels', 'stores' and 'categories' with the values
        fetched from the openfoodfacts API in those same fields for the product with the barcode entered when this class was instancied.
        Return False api response is invalid or if one key is invalid.
        The return of False could mean either the api didn't responde to the 'product' key or one of the key FROM 'product', please use
        api_response() method to be sure that you have a valid response for the barcode of the entered product.
        """

        if self.api_response() == True:
            try:
                self.nutriscore = self.user_product.json()['product']['nutrition_grade_fr']
                self.generic_name = self.user_product.json()['product']['generic_name']
                self.image_url = self.user_product.json()['product']['image_url']
                self.name = self.user_product.json()['product']['product_name_fr']
                self.labels = self.user_product.json()['product']['labels']
                self.stores = self.user_product.json()['product']['stores']

                for category in self.user_product.json()['product']['categories_hierarchy']:
                    self.categories.append(category)
                
                return {
                        'nutriscore' : self.nutriscore,
                        'generic_name' : self.generic_name,
                        'image_url' : self.image_url,
                        'name' : self.name,
                        'labels' : self.labels,
                        'stores' : self.stores,
                        'categories' : self.categories
                        }
            except:
                return False
        else:
            return False

test = Product('helloworld')

if test.get():
    print('do your thing')

else:
    print("No response from API")