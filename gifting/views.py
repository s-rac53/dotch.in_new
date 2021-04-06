from django.shortcuts import render, get_object_or_404
from gifting.models import ProductGifting, ProductImage
from orders.models import Review


def product_list(request):
    products = ProductGifting.objects.filter(available=True)
    reviews = Review.objects.filter().order_by('-id')[:5]
    review_id = Review.objects.latest().id
    all_stars = range(1,6)
    return render(request, 'gifting/product/list.html',{'products': products, 'reviews':reviews, 'review_id':review_id, 'all_stars':all_stars})


def product_detail(request, id, slug):

    variants = None
    vid = None
    product = get_object_or_404(ProductGifting, id=id, slug=slug, available=True)
    images = ProductImage.objects.filter(product=product)

    variants = product.variants.filter(available=True)
    if variants:
     vid = variants.values()[0]['id']

    return render(request, 'gifting/product/detail.html', {'product':product, 'images': images,
                                                           'variants': variants, 'vid' : vid})

