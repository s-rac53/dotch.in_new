from django.shortcuts import render, get_object_or_404
from shop.models import Category, Product, ProductImage, ProductSize
from cart.cart import Cart
from orders.models import Review
from django.http import JsonResponse





def homepage(request):
    return render(request,'homepage.html')


def product_list(request, category_slug=None):
    products_category = None
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    latest = Product.objects.filter(available=True)[:7]
    reviews = Review.objects.filter().order_by('-id')[:5]
    review_id = Review.objects.latest().id
    all_stars = range(1, 6)

    if 'term' in request.GET:

        product_qs = Product.objects.filter(name__icontains=request.GET.get('term'))
        results = list()

        for prd in product_qs:
            results.append(prd.name)
        return JsonResponse(results, safe=False)

    cart = Cart(request)
    cart_num_items = cart.__len__()


    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products_category = Product.objects.filter(category=category, available=True)
        products = Product.objects.filter(available=True)



    return render(request, 'shop/product/list.html',{'category': category,'categories': categories, 'products': products,
                                                     'latest': latest, 'cart_num_items':cart_num_items,
                                                     'reviews':reviews, 'review_id':review_id,
                                                     'all_stars':all_stars,'products_category':products_category})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)

    images = ProductImage.objects.filter(product=product)
    sizes = ProductSize.objects.filter(product=product, available=True)
    products = Product.objects.filter(available=True)

    cart = Cart(request)
    cart_num_items = cart.__len__()



    i = range(images.count())
    array_itr = []
    for n in i:
        n= n + 1

        array_itr.append(n)


    quantity_range = range(1, 25)


    category = product.category
    products_same_category = Product.objects.filter(category=category, available=True)





    return render(request, 'shop/product/detail.html', {'product':product, 'category': category, \
                                                        'images': images, 'sizes':sizes, 'array_itr': array_itr,
                                                        'quantity_range': quantity_range, 'products_same_category':products_same_category,
                                                        'cart_num_items':cart_num_items, 'products':products})















