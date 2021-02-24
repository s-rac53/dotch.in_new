from django.urls import path
from potato import views

app_name = 'potato'

urlpatterns = [

    path('', views.product_list, name='product_list'),
    path('creative-gifts/potato/<slug:category_slug>/', views.product_list, name='product_list'),
    path('creative-gifts/potato/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]