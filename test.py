from unittest import TestCase, main as testmain
from product import Product

class MyTest(TestCase):
    def test_api_response(self):
        """
        """
        dic = {"3017620422003" : True, "fhiufhsidfhs" : False}
        for barcode, response in dic.items():
            with self.subTest(value=barcode):
                self.assertEqual(Product(barcode).api_response(), response)

    def test_api_response_exceptions(self):
        """
        """
        dics = {
                ('dic_key_error', KeyError) : {"" : False},
                ('dic_type_error', TypeError) : {0 : False},
                ('dic_unkown', Exception) : {None : False}
        }
        
        for errors, dic in dics.items():
            for barcode, response in dic.items():
                with self.subTest(value=barcode):
                    with self.assertRaises(errors[1]):
                        Product(barcode).api_response()

if __name__ == "__main__":
    testmain()