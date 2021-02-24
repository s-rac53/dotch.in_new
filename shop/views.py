from django.shortcuts import render, get_object_or_404
from shop.models import Category, Product, ProductImage, ProductSize
from cart.forms import CartAddProductForm


def homepage(request):
    return render(request,'homepage.html')


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    latest = Product.objects.filter(available=True)[:7]


    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, available=True)



    return render(request, 'shop/product/list.html',{'category': category,'categories': categories, 'products': products, 'latest': latest})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)

    images = ProductImage.objects.filter(product=product)
    sizes = ProductSize.objects.filter(product=product, available=True)
    cart_product_form = CartAddProductForm()


    i = range(images.count())
    array_itr = []
    for n in i:
        n= n + 1
        print(n)
        array_itr.append(n)


    quantity_range = range(1, 25)


    category = product.category
    products_same_category = Product.objects.filter(category=category, available=True)




    return render(request, 'shop/product/detail.html', {'product':product, 'category': category, \
                                                        'products_same_category': products_same_category, \
                                                        'images': images, 'sizes':sizes, 'array_itr': array_itr,
                                                        'cart_product_form': cart_product_form,
                                                        'quantity_range': quantity_range})
