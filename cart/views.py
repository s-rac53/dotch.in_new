from django.shortcuts import render,get_object_or_404, redirect
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart



@require_POST
def cart_add(request, product_id):


    cart = Cart(request)


    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
       quantity = request.POST.get('quantity')
       quantity = int(quantity)
       size_value = request.POST.get('size_value')



    cart.add(product=product,quantity=quantity, size_value=size_value)
    return redirect('cart:cart_detail')



def cart_remove(request, product_id, product_size):
    cart = Cart(request)


    cart.remove(product_id, product_size)
    return redirect('cart:cart_detail')



def cart_detail(request):

    cart = Cart(request)
    products = Product.objects.filter(available=True)

    return render(request, 'cart/detail.html', {'cart': cart, 'products': products})