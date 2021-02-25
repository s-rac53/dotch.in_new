from django.shortcuts import render,get_object_or_404, redirect
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    duplicate = False
    cart = Cart(request)


    product = get_object_or_404(Product, id=product_id)
    print(product)
    if request.method == 'POST':
       quantity = request.POST.get('quantity')
       quantity = int(quantity)
       size_value = request.POST.get('size_value')


    cart_products = cart.total_products()


    if product in cart_products:
        duplicate = True




    cart.add(product=product,quantity=quantity, size_value=size_value,duplicate=duplicate)
    return redirect('cart:cart_detail')



def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')



def cart_detail(request):

    cart = Cart(request)
    cart_products = cart.total_products()

    for item in cart.cart.values():
        print(item.__iter__())

    return render(request, 'cart/detail.html', {'cart': cart, 'cart_products': cart_products})