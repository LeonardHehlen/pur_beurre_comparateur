import requests
from alphabet import ALPHABET

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
        self.nutriscore_in_number = 0
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
    
    def fetch_similar_better_product(self):
        """
        If the api_response() isn't True, this method will returns False.

        Returns a dict of Products with similar categories and better Nutriscore.
        First it requests all items with the same Major Category in common in the categories hierarchy.
        Then it filters out everything that doesn't have in common the 2 last categories in the categories hierarchy.
        So now the level of relevance by category is at it's best.
        Then, it converts the letter of the nutriscore into it's index number in the alphabet, and only add to our final result 
        the ones that are equal or less than the product nutriscore.
        And finally, returns a list containing a dict for every product left, with the keys : 'nutriscore', 'generic_name',
        'image_url', 'name', 'labels', 'stores' and 'categories'.
        """
        if self.api_response() == True:
            correct_categories_results = []
            best_nutriscore_results = []
            final_results = []
            search_url = 'https://fr.openfoodfacts.org/cgi/search.pl?action=process&page_size=100&tagtype_0=categories&tag_contains_0=contains&tag_0=' + str(self.categories[0] + '&json=true')
            search_results = requests.get(search_url).json()['products']

            def convert_letter_to_number(letter_to_convert):
                """
                Convert a letter to it's index number in the alphabet.
                """
                letter_to_convert = letter_to_convert.casefold()
                number = False

                for i, letter in enumerate(ALPHABET):
                    if letter == letter_to_convert:
                        number = i
                        return number

            for search_result in search_results:
                search_result_categories = search_result['categories_hierarchy']
                if search_result_categories[search_result_categories.__len__()-2] == self.categories[self.categories.__len__()-2]:
                    correct_categories_results.append(search_result)
        
            self.nutriscore_in_number = convert_letter_to_number(str(self.nutriscore))

            for result in correct_categories_results:
                result_nutriscore_in_number = convert_letter_to_number(str(result['nutrition_grade_fr']))

                if result_nutriscore_in_number < self.nutriscore_in_number:
                    best_nutriscore_results.append(result)

            for result in best_nutriscore_results:
                final_results.append(
                    {
                        'name' : result['product_name_fr'],
                        'nutriscore' : result['nutrition_grade_fr']
                    }
                )
                    
            return final_results
        else:
            return False