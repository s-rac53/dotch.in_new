from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart(object):

    def __init__(self, request):
       """
       Initialize the cart.
       """
       self.session = request.session
       cart = self.session.get(settings.CART_SESSION_ID)
       if not cart:
           # save an empty cart in the session
           cart = self.session[settings.CART_SESSION_ID] = {}
       self.cart = cart


    def add(self, product, quantity=1, size_value='L',duplicate=False):
           """
           Add a product to the cart or update its quantity.
           """
           product_id = str(product.id)




           if product_id not in self.cart:
               self.cart[product_id] = {
                                                     'quantity': 0,

                                                     'quantityS': 0,
                                                     'quantityM': 0,
                                                     'quantityL': 0,
                                                     'quantityXL': 0,
                                                     'quantityXXL': 0,


                                                     'sizeS': None,
                                                     'sizeM': None,
                                                     'sizeL': None,
                                                     'sizeXL': None,
                                                     'sizeXXL': None,



                                                     'priceS': 0,
                                                     'priceM': 0,
                                                     'priceL': 0,
                                                     'priceXL': 0,
                                                     'priceXXL': 0,


                                                     'price': str(product.price)
                                       }

               if size_value == 'S':
                   self.cart[product_id]['sizeS'] = size_value
                   self.cart[product_id]['quantityS'] += quantity
               elif size_value == 'M':
                   self.cart[product_id]['sizeM'] = size_value
                   self.cart[product_id]['quantityM'] += quantity
               elif size_value == 'L':
                   self.cart[product_id]['sizeL'] = size_value
                   self.cart[product_id]['quantityL'] += quantity
               elif size_value == 'XL':
                   self.cart[product_id]['sizeXL'] = size_value
                   self.cart[product_id]['quantityXL'] += quantity
               elif size_value == 'XXL':
                   self.cart[product_id]['sizeXXL'] = size_value
                   self.cart[product_id]['quantityXXL'] += quantity




           if duplicate:

               if size_value == 'S':
                   self.cart[product_id]['sizeS'] = size_value
                   self.cart[product_id]['quantityS'] += quantity
               elif size_value == 'M':
                   self.cart[product_id]['sizeM'] = size_value
                   self.cart[product_id]['quantityM'] += quantity
               elif size_value == 'L':
                   self.cart[product_id]['sizeL'] = size_value
                   self.cart[product_id]['quantityL'] += quantity
               elif size_value == 'XL':
                   self.cart[product_id]['sizeXL'] = size_value
                   self.cart[product_id]['quantityXL'] += quantity
               elif size_value == 'XXL':
                   self.cart[product_id]['sizeXXL'] = size_value
                   self.cart[product_id]['quantityXXL'] += quantity



           self.save()


    def save(self):

        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True



    def remove(self, product):

           """
           Remove a product from the cart.
           """
           product_id = str(product.id)
           size_value = product.sizes
           if product_id in self.cart:
               del self.cart[product_id]
               self.save()

    def __iter__(self):
           """
           Iterate over the items in the cart and get the products
           from the database.
           """
           print(self)
           product_ids = self.cart.keys()
           # get the product objects and add them to the cart
           products = Product.objects.filter(id__in=product_ids)

           cart = self.cart.copy()

           for product in products:
               print(product)
               cart[str(product.id)]['product'] = product
           for item in cart.values():
                     if item['sizeS']:
                        item['price'] = Decimal(item['price'])
                        item['priceS'] = item['price'] * item['quantityS']
                     elif item['sizeM']:
                         item['price'] = Decimal(item['price'])
                         item['priceM'] = item['price'] * item['quantityM']
                     elif item['sizeL']:
                         item['price'] = Decimal(item['price'])
                         item['priceL'] = item['price'] * item['quantityL']
                     elif item['sizeXL']:
                         item['price'] = Decimal(item['price'])
                         item['priceXL'] = item['price'] * item['quantityXL']
                     elif item['sizeXXL']:
                         item['price'] = Decimal(item['price'])
                         item['priceXXL'] = item['price'] * item['quantityXXL']
                     yield item


    def __len__(self):
           """
           Count all items in the cart.
           """
           for item in self.cart.values():
               sum_list = (item['quantityS'],item['quantityM'],item['quantityL'],item['quantityXL'],item['quantityXXL'])
               return sum(sum_list)




    def get_total_price(self):

        for item in self.cart.values():
            total_sum = ( Decimal(item['price']) * item['quantityS'],Decimal(item['price']) * item['quantityM'],\
                          Decimal(item['price']) * item['quantityL'],\
                          Decimal(item['price']) * item['quantityXL'],Decimal(item['price']) * item['quantityXXL'])


        return sum(total_sum)



    def clear(self):

           # remove cart from session
           del self.session[settings.CART_SESSION_ID]
           self.save()


    def total_products(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products




