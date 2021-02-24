from django.shortcuts import render,get_object_or_404, redirect
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    updated = False
    cart = Cart(request)

    print(cart.cart.values())


    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
       quantity = request.POST.get('quantity')
       quantity = int(quantity)
       updated = request.POST.get('updated')
       size_value = request.POST.get('size_value')
       print(size_value)

    cart_products = cart.total_products()
    print(cart_products)


    cart.add(product=product,quantity=quantity, update_quantity=updated, size_value=size_value)
    return redirect('cart:cart_detail')



def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')



def cart_detail(request):

    cart = Cart(request)
    cart_products = cart.total_products()

    return render(request, 'cart/detail.html', {'cart': cart, 'cart_products': cart_products})