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


           def add(self, product, quantity=1, size_value='L'):
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
                       self.cart[product_id]['quantityS'] = quantity
                   if size_value == 'M':
                       self.cart[product_id]['sizeM'] = size_value
                       self.cart[product_id]['quantityM'] = quantity
                   if size_value == 'L':
                       self.cart[product_id]['sizeL'] = size_value
                       self.cart[product_id]['quantityL'] = quantity
                   if size_value == 'XL':
                       self.cart[product_id]['sizeXL'] = size_value
                       self.cart[product_id]['quantityXL'] = quantity
                   if size_value == 'XXL':
                       self.cart[product_id]['sizeXXL'] = size_value
                       self.cart[product_id]['quantityXXL'] = quantity

               else:
                   if size_value == 'S':
                       self.cart[product_id]['sizeS'] = size_value
                       self.cart[product_id]['quantityS'] = quantity
                   if size_value == 'M':
                       self.cart[product_id]['sizeM'] = size_value
                       self.cart[product_id]['quantityM'] = quantity
                   if size_value == 'L':
                       self.cart[product_id]['sizeL'] = size_value
                       self.cart[product_id]['quantityL'] = quantity
                   if size_value == 'XL':
                       self.cart[product_id]['sizeXL'] = size_value
                       self.cart[product_id]['quantityXL'] = quantity
                   if size_value == 'XXL':
                       self.cart[product_id]['sizeXXL'] = size_value
                       self.cart[product_id]['quantityXXL'] = quantity


               self.save()

           def save(self):
                   # mark the session as "modified" to make sure it gets saved
                   self.session.modified = True

           def remove(self, product_id, product_size):
                   """
                   Remove a product from the cart.
                   """

                   product_id = str(product_id)

                   #size_value = product.sizes
                   if product_id in self.cart:
                       #del self.cart[product_id]

                       if product_size == 'sizeS':
                           self.cart[product_id]['sizeS'] = None;
                           self.cart[product_id]['quantityS'] = 0;
                           self.cart[product_id]['priceS'] = 0;
                       if product_size == 'sizeM':
                           self.cart[product_id]['sizeM'] = None;
                           self.cart[product_id]['quantityM'] = 0;
                           self.cart[product_id]['priceM'] = 0;
                       if product_size == 'sizeL':
                           self.cart[product_id]['sizeL'] = None;
                           self.cart[product_id]['quantityL'] = 0;
                           self.cart[product_id]['priceL'] = 0;
                       if product_size == 'sizeXL':
                           self.cart[product_id]['sizeXL'] = None;
                           self.cart[product_id]['quantityXL'] = 0;
                           self.cart[product_id]['priceXL'] = 0;
                       if product_size == 'sizeXXL':
                           self.cart[product_id]['sizeXXL'] = None;
                           self.cart[product_id]['quantityXXL'] = 0;
                           self.cart[product_id]['priceXXL'] = 0;
                       self.save()


           def __iter__(self):
                   """
                   Iterate over the items in the cart and get the products
                   from the database.
                   """

                   product_ids = self.cart.keys()
                   # get the product objects and add them to the cart
                   products = Product.objects.filter(id__in=product_ids)

                   cart = self.cart.copy()
                   for product in products:

                       cart[str(product.id)]['product'] = product
                   for item in cart.values():


                       if item['sizeS']:
                           item['price'] = Decimal(item['price'])

                           item['priceS'] = item['price'] * item['quantityS']


                       if item['sizeM']:
                           item['price'] = Decimal(item['price'])
                           item['priceM'] = item['price'] * item['quantityM']


                       if item['sizeL']:
                           item['price'] = Decimal(item['price'])
                           item['priceL'] = item['price'] * item['quantityL']

                       if item['sizeXL']:
                           item['price'] = Decimal(item['price'])
                           item['priceXL'] = item['price'] * item['quantityXL']

                       if item['sizeXXL']:
                           item['price'] = Decimal(item['price'])
                           item['priceXXL'] = item['price'] * item['quantityXXL']

                       yield item



           def __len__(self):
                   """
                   Count all items in the cart.
                   """
                   sum_list = 0
                   for item in self.cart.values():
                       sum_list+= item['quantityS'] + item['quantityM']+ item['quantityL']+ item['quantityXL']+ item['quantityXXL']
                   return sum_list

           def get_total_price(self):
                   total_sum = 0
                   for item in self.cart.values():
                       total_sum += Decimal(item['price']) * item['quantityS'] + Decimal(item['price']) * item['quantityM']+ \
                       Decimal(item['price']) * item['quantityL']+ \
                       Decimal(item['price']) * item['quantityXL']+ Decimal(item['price']) * item['quantityXXL']+\
                       Decimal(item['price']) * item['quantity']
                   return total_sum

           def clear(self):
                   # remove cart from session
                   del self.session[settings.CART_SESSION_ID]
                   self.save()

           def total_products(self):
                   product_ids = self.cart.keys()
                   products = Product.objects.filter(id__in=product_ids)
                   return products
