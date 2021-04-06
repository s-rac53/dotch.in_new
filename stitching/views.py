from django.shortcuts import render
from orders.models import Review

def stitching_view(request):
    reviews = Review.objects.filter().order_by('-id')[:5]
    review_id = Review.objects.latest().id
    all_stars = range(1, 6)

    return render(request,'stitching.html', {'reviews':reviews, 'review_id':review_id, 'all_stars':all_stars})
